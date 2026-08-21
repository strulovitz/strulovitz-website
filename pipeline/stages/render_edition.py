#!/usr/bin/env python3
"""
RENDERING ONE EDITION OF ONE STORY
==================================

WHAT THIS IS, IN ONE SENTENCE
The stage where one model does the entire editorial job on one story - the key
points, the article, the encyclopedia entries, the tags, the links and the
illustration prompt - and the result is written down exactly as it came back.

ONE MODEL, EVERY ROLE (DECISIONS.md decision 12)
There is no division of labour. Nir: "if for example we are doing the edition
model (A): then model A is ALL OF THE ROLES." So this file asks one model one
question and stores one answer. It does not check it, score it, grade it,
repair it or improve it. If a model writes nonsense, the nonsense is published
as that model's edition, and the reader who raises an eyebrow switches edition
and sees for themselves. That comparison is the product (decision 16).

WHAT EVERY MODEL RECEIVES, IDENTICALLY
1. The editorial brief from config/editorial-brief.md, word for word.
2. The frozen text of every source, fenced as data so that no web page can give
   our machine instructions (bible/part-00.md LAW 8).
3. The list of the other stories in the magazine, so it can choose which ones
   its article links to. What it chooses is the shape of its own galaxy.
Nothing else. No hints, no per-model tweaks, no second attempts at a poor
answer. That is what makes the comparison mean something.

WHAT IT WRITES
    content/stories/<story>/editions/<company--model>/
        rendering.json     everything the model produced, plus what it cost
        article.md         the article on its own, for reading and diffing
        image-prompt.txt   the illustration prompt on its own
        answer.txt         the raw text the model sent, before any parsing

HOW TO RUN IT
    cd pipeline && uv run stages/render_edition.py --story <slug> --model <id>
    cd pipeline && uv run stages/render_edition.py --story <slug> --all-models
    cd pipeline && uv run stages/render_edition.py --all --all-models
Add --batch to buy at half price and collect later; without it the answer is
bought immediately at full price. Nothing already rendered is redone unless
--again is given.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.db import connect, log_job  # noqa: E402
from lib.llm import (Answer, Model, Question, as_data, ask_now, model_by_id,  # noqa: E402
                     roster, settings, submit_batch)
from lib.sources import read_frozen  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
STORIES = REPO_ROOT / "content" / "stories"
BRIEF_FILE = REPO_ROOT / "config" / "editorial-brief.md"
SCHEMA_FILE = REPO_ROOT / "schemas" / "rendering.schema.json"


def brief() -> str:
    """
    The editorial brief, exactly as it sits between the markers in
    config/editorial-brief.md. Kept in that file and not in this code so that
    Nir can read and change how the whole magazine is written without touching
    a line of Python.
    """
    text = BRIEF_FILE.read_text(encoding="utf-8")
    match = re.search(r"<!-- BRIEF BEGIN -->(.*?)<!-- BRIEF END -->", text, flags=re.DOTALL)
    if not match:
        raise RuntimeError(f"{BRIEF_FILE} has lost its BRIEF BEGIN / BRIEF END markers.")
    return match.group(1).strip()


def brief_version() -> str:
    """
    A short fingerprint of the brief. Stored with every rendering, so that
    months from now it is possible to say which editions were written under
    which instructions - and so that changing the brief does not silently mix
    old and new work in the same comparison.
    """
    return hashlib.sha256(brief().encode("utf-8")).hexdigest()[:12]


def schema_or_none(model: Model) -> dict | None:
    """
    The strict JSON shape, for models that can be handed one. GLM 5.3 cannot,
    so it is asked for JSON in words instead. Which way each model was asked is
    recorded in its rendering, so the record stays honest.
    """
    if not model_supports_schema(model.id):
        return None
    return json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))


def model_supports_schema(model_id: str) -> bool:
    import tomllib
    with (REPO_ROOT / "config" / "editions.toml").open("rb") as handle:
        config = tomllib.load(handle)
    for entry in config.get("model", []):
        if entry["id"] == model_id:
            return bool(entry.get("structured_outputs", True))
    return True


# ------------------------------------------------------------------------------
# Building the question
# ------------------------------------------------------------------------------

def story_details(slug: str) -> dict:
    path = STORIES / slug / "story.json"
    if not path.exists():
        raise FileNotFoundError(f"No story called {slug!r}. Run stages/make_story.py first.")
    return json.loads(path.read_text(encoding="utf-8"))


def all_story_slugs() -> list[str]:
    if not STORIES.exists():
        return []
    return sorted(p.name for p in STORIES.iterdir() if (p / "story.json").exists())


def other_stories_list(this_slug: str) -> str:
    """
    The menu of other stories, so a model can choose what its article links to.
    Only slugs and titles: a model must not be able to read another story's
    edition, or editions would start imitating each other.
    """
    lines = []
    for slug in all_story_slugs():
        if slug == this_slug:
            continue
        lines.append(f"  {slug}   ({story_details(slug)['title']})")
    if not lines:
        return "There are no other stories in the magazine yet, so 'related' must be an empty list."
    return "The other stories in the magazine, by slug:\n" + "\n".join(lines)


def build_question(slug: str, model: Model) -> Question:
    """One story's whole request, identical in every way except the model."""
    details = story_details(slug)
    sources = read_frozen(STORIES / slug / "sources")
    if len(sources) < settings().minimum_sources:
        raise RuntimeError(f"{slug} has only {len(sources)} frozen sources.")

    parts: list[str] = [
        f"THE SUBJECT: {details['title']}",
        "",
        f"You have {len(sources)} independent sources, below. Write your edition of this story.",
        "",
    ]
    for number, source in enumerate(sources, start=1):
        kind = "video transcript (subtitles)" if source.kind == "video" else "article"
        heading = (
            f"SOURCE {number} of {len(sources)} - {kind}\n"
            f"  title:     {source.title}\n"
            f"  by:        {source.byline or 'not named'}\n"
            f"  published: {source.published or 'no date given'}\n"
            f"  web address: {source.url}\n"
            + (f"  note: {source.note}\n" if source.note else "")
        )
        parts.append(heading)
        parts.append(as_data(f"source {number}: {source.title}", source.text))
        parts.append("")

    parts.append(other_stories_list(slug))
    parts.append("")
    parts.append(
        "Now write your edition, as one JSON object in the shape given in your "
        "instructions. When you cite a source in key_points, copy its web address "
        "exactly as it appears above."
    )
    return Question(name=slug, system=brief(), user="\n".join(parts),
                    schema=schema_or_none(model))


# ------------------------------------------------------------------------------
# Writing down what came back
# ------------------------------------------------------------------------------

def edition_folder(slug: str, model: Model) -> Path:
    return STORIES / slug / "editions" / model.slug


def already_rendered(slug: str, model: Model) -> bool:
    return (edition_folder(slug, model) / "rendering.json").exists()


def store(slug: str, model: Model, answer: Answer) -> Path:
    """
    Write an answer to disk exactly as it arrived.

    answer.txt holds the raw text the model sent, always, even when it was not
    valid JSON - because a model failing to follow the shape is a fact about
    that model and belongs in the record, not in a bin.
    """
    folder = edition_folder(slug, model)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "answer.txt").write_text(answer.text, encoding="utf-8")

    produced = answer.data if isinstance(answer.data, dict) else None
    rendering = {
        "story": slug,
        "model_id": model.id,
        "model_slug": model.slug,
        "model_served": answer.model_served,
        "company": model.company,
        "short_name": model.short_name,
        "rendered_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "brief_version": brief_version(),
        "asked_with_strict_schema": model_supports_schema(model.id),
        "bought_in_batch": answer.was_batch,
        "cost_usd": answer.cost_usd,
        "prompt_tokens": answer.prompt_tokens,
        "completion_tokens": answer.completion_tokens,
        "reasoning_tokens": answer.reasoning_tokens,
        "seconds_waited": answer.seconds_waited,
        "generation_id": answer.generation_id,
        "understood": produced is not None,
        "produced": produced,
    }
    (folder / "rendering.json").write_text(
        json.dumps(rendering, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    if produced:
        (folder / "article.md").write_text(
            f"# {produced.get('headline', '')}\n\n*{produced.get('tldr', '')}*\n\n"
            f"{produced.get('article', '')}\n", encoding="utf-8"
        )
        (folder / "image-prompt.txt").write_text(
            str(produced.get("image_prompt", "")), encoding="utf-8"
        )
    return folder


# ------------------------------------------------------------------------------
# Doing it
# ------------------------------------------------------------------------------

def render_now(slug: str, model: Model, *, actor: str) -> Answer:
    """Buy one edition immediately, at full price."""
    question = build_question(slug, model)
    answer = ask_now(model.id, system=question.system, user=question.user,
                     schema=question.schema, name=slug, purpose=f"the {model.short_name} "
                     f"edition of the story '{story_details(slug)['title']}'", actor=actor)
    store(slug, model, answer)
    return answer


def render_batch(slugs: list[str], model: Model, *, actor: str) -> str:
    """Send one model every story it is missing, at half price. Returns the receipt id."""
    questions = [build_question(slug, model) for slug in slugs]
    receipt = submit_batch(
        model.id, questions, actor=actor,
        purpose=f"the {model.short_name} edition of {len(questions)} "
                f"{'story' if len(questions) == 1 else 'stories'}",
    )
    return receipt.batch_id


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render editions of stories.")
    parser.add_argument("--story", help="one story slug")
    parser.add_argument("--all", action="store_true", help="every story")
    parser.add_argument("--model", help="one model id from the roster")
    parser.add_argument("--all-models", action="store_true", help="every model on the roster")
    parser.add_argument("--batch", action="store_true", help="buy at half price, collect later")
    parser.add_argument("--again", action="store_true",
                        help="render even where a rendering already exists")
    parser.add_argument("--actor", default="claude-opus-5")
    args = parser.parse_args(argv)

    slugs = all_story_slugs() if args.all else ([args.story] if args.story else [])
    models = roster() if args.all_models else ([model_by_id(args.model)] if args.model else [])
    if not slugs or not models:
        parser.error("say which stories (--story SLUG or --all) and which models "
                     "(--model ID or --all-models).")

    print(f"{len(slugs)} stories x {len(models)} models = {len(slugs) * len(models)} cells")
    total_cost = 0.0
    done: list[str] = []
    failed: list[str] = []

    for model in models:
        wanted = [s for s in slugs if args.again or not already_rendered(s, model)]
        if not wanted:
            print(f"\n{model.short_name}: nothing missing.")
            continue

        if args.batch:
            batch_id = render_batch(wanted, model, actor=args.actor)
            print(f"\n{model.short_name}: sent {len(wanted)} at half price -> {batch_id}")
            continue

        print(f"\n{model.short_name} ({model.id})")
        for slug in wanted:
            try:
                answer = render_now(slug, model, actor=args.actor)
                total_cost += answer.cost_usd
                shape = "understood the shape" if isinstance(answer.data, dict) else "DID NOT return valid JSON"
                print(f"  {slug[:52]:<52} {answer.seconds_waited:5.0f}s "
                      f"{answer.completion_tokens:>6} written  ${answer.cost_usd:.4f}  {shape}")
                done.append(f"{slug}/{model.slug}")
            except Exception as problem:  # noqa: BLE001 - report and carry on
                print(f"  {slug[:52]:<52} FAILED: {type(problem).__name__}: {problem}")
                failed.append(f"{slug}/{model.slug}: {type(problem).__name__}")

    if not args.batch:
        print("\n" + "=" * 78)
        print(f"rendered {len(done)} cells, {len(failed)} failed, total cost ${total_cost:.4f}")
        for note in failed:
            print(f"  failed: {note}")
        try:
            with connect() as db:
                log_job(db, action_type="stage_run", actor=args.actor,
                        verdict="partial" if failed else "ok", cost_usd=total_cost,
                        plain_words=(
                            f"Had {len(models)} models each write their own edition of "
                            f"{len(slugs)} stories, every role done by the one model and "
                            f"nothing checked or corrected afterwards. {len(done)} editions "
                            f"were produced and {len(failed)} failed, at a total cost of "
                            f"{total_cost:.4f} dollars at full immediate price."),
                        outputs=done)
        except Exception as problem:  # noqa: BLE001
            print(f"(could not write to the ledger: {type(problem).__name__})")
    return 1 if failed and not done else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
