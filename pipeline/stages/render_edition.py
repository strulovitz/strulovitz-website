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

from lib.db import connect, log_job, read_story, upsert_edition, upsert_story  # noqa: E402
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
    """
    Nir, 2026-09-03: "do exactly what the Bible says." Part 01 1.5 iron rule 3:
    every stage reads through Neo4j. The story and its frozen-source records
    come from the database now; only the frozen source TEXT itself stays on
    disk, exactly where the Bible wants it (Part 02 2.2.7: "raw_text_path -
    kitchen disk cache").
    """
    with connect() as db:
        story = read_story(db, slug)
    if story is None:
        raise FileNotFoundError(f"No story called {slug!r}. Run stages/make_story.py first.")
    return story


def all_story_slugs() -> list[str]:
    with connect() as db:
        with db.session() as session:
            rows = session.run("MATCH (s:Story) RETURN s.slug AS slug ORDER BY s.slug").data()
    return [r["slug"] for r in rows]


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
        write_readable(folder)
    # THE DATABASE IS THE TRUTH (Nir, 2026-09-03: "do exactly what the Bible
    # says." LAW 5 + Part 01 1.5): the same instant the files are written as
    # human-readable exports, the edition is stored in Neo4j through the one
    # door - so the reading stages (layout, home, images) never depend on the
    # files at all. If this write fails, the stage fails: an edition that
    # exists only as a file would be a return to the old violation.
    with connect() as db:
        upsert_story(db, story_details(slug))
        upsert_edition(db, story_details(slug), rendering)
    return folder


def write_readable(folder: Path) -> Path | None:
    """
    Write EVERYTHING one model produced into a single file a person can read
    top to bottom: the headline, the one-line summary, the article, the key
    points with their sources, the encyclopedia entries, the tags, the links to
    other stories, the illustration prompt, and what it cost.

    This exists because rendering.json is machine-shaped, and judging a model's
    work by reading JSON is miserable. Nothing here is new information - it is
    the same answer, laid out for human eyes.
    """
    rendering_path = folder / "rendering.json"
    if not rendering_path.exists():
        return None
    rendering = json.loads(rendering_path.read_text(encoding="utf-8"))
    produced = rendering.get("produced")
    if not produced:
        return None

    lines: list[str] = [
        f"# {produced.get('headline', '(no headline)')}",
        "",
        f"**{rendering.get('short_name')}** ({rendering.get('company')}) — "
        f"its own edition of *{rendering.get('story')}*",
        "",
        "---",
        "",
        "## The one line a reader sees when hovering over this story",
        "",
        f"> {produced.get('tldr', '')}",
        f"> *({len(produced.get('tldr', ''))} characters)*",
        "",
        "---",
        "",
        "## The article",
        "",
        str(produced.get("article", "")),
        "",
        "---",
        "",
        "## What this editor judged the sources established",
        "",
    ]
    for point in produced.get("key_points") or []:
        lines.append(f"- {point.get('point', '')}")
        lines.append(f"  — {point.get('source_url', '')}")
    lines += ["", "---", "", "## The encyclopedia entries it chose to write", ""]
    for concept in produced.get("concepts") or []:
        words = len(str(concept.get("explanation", "")).split())
        lines += [
            f"### {concept.get('term', '')}",
            f"`{concept.get('slug', '')}` — {words} words",
            "",
            str(concept.get("explanation", "")),
            "",
        ]
    lines += [
        "---",
        "",
        "## Tags it chose",
        "",
        "  ".join(f"`{tag}`" for tag in produced.get("tags") or []) or "(none)",
        "",
        "*These decide what sits near what in this edition's own galaxy, and nowhere else.*",
        "",
        "## Other stories it decided a reader should go to next",
        "",
    ]
    related = produced.get("related") or []
    lines += ([f"- `{slug}`" for slug in related] if related
              else ["(none — it judged that no other story in the magazine relates to this one)"])
    lines += [
        "",
        "*These are the edges of this edition's map. Another model will draw them differently.*",
        "",
        "---",
        "",
        "## The illustration it directed",
        "",
        f"> {produced.get('image_prompt', '')}",
        "",
        "*Rendered locally with the same image model and the same seed for every "
        "edition, so the only difference between editions' pictures is the quality "
        "of that paragraph.*",
        "",
        "---",
        "",
        "## What it cost, and how it was asked",
        "",
        f"- cost: **${rendering.get('cost_usd', 0):.4f}**"
        f"{' (half price, bought in batch)' if rendering.get('bought_in_batch') else ' (full price, bought immediately)'}",
        f"- it read {rendering.get('prompt_tokens', 0):,} tokens and wrote "
        f"{rendering.get('completion_tokens', 0):,}"
        + (f", of which {rendering.get('reasoning_tokens', 0):,} were thinking to itself"
           if rendering.get("reasoning_tokens") else ""),
        f"- it took {rendering.get('seconds_waited', 0):.0f} seconds",
        f"- asked with a strict JSON shape: {rendering.get('asked_with_strict_schema')}",
        f"- the exact model that served it: `{rendering.get('model_served')}`",
        f"- editorial brief version: `{rendering.get('brief_version')}`",
        "",
    ]
    path = folder / "EDITION.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


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


# The instruction for the missing-illustration case. It hands a model back its
# OWN finished article and asks only for the picture, so the prompt it writes is
# still entirely its own work and still comparable with the other seven.
IMAGE_PROMPT_ONLY = """You wrote the article below for AI PANORAMA, an
independent magazine about artificial intelligence. Everything about it is your
own work. The only thing still missing is the instruction for its illustration.

Write ONE paragraph describing a single illustration for this article. The
illustration must capture as many of the article's own main ideas as clearly
and completely as you can, so that a reader who only looked at the picture
would still understand what the story is actually about.

Answer with the paragraph alone. No preamble, no explanation, no quotation
marks, no JSON."""


def fill_image_prompt(slug: str, model: Model, *, actor: str,
                      another_chance: bool = False) -> str | None:
    """
    Ask a model for the illustration prompt it did not write.

    Every edition must carry an instruction for its own picture, because the
    pictures are half of what a reader compares and an edition without one is
    an unfinished job rather than an opinion. Nir, plainly: "i want each one to
    make a prompt for an image".

    The model is given back its OWN article and nothing else, so the paragraph
    it writes is still entirely its own work, written from its own words, and
    still fairly comparable with the other seven. Nothing it wrote earlier is
    altered by a single character.
    """
    folder = edition_folder(slug, model)
    rendering_path = folder / "rendering.json"
    if not rendering_path.exists():
        return None
    rendering = json.loads(rendering_path.read_text(encoding="utf-8"))
    produced = rendering.get("produced") or {}
    if not produced:
        return None
    if (produced.get("image_prompt") or "").strip() and not another_chance:
        return None  # it already has one; leave it entirely alone

    # ANOTHER CHANCE, WHICH IS NOT THE SAME AS A FIX.
    # Nir's words, on a prompt that arrived with the model's thinking-out-loud
    # sentence stuck on the front: "we are not fixing, but we will give it
    # another chance." So we ask the identical question again and keep whatever
    # comes back, good or bad. We never edit the words ourselves, and we never
    # keep the better of two answers - the new answer replaces the old one
    # whatever it looks like. The cache is deliberately bypassed, or the same
    # answer would simply be handed back.

    article = (
        f"HEADLINE: {produced.get('headline', '')}\n\n"
        f"SUMMARY: {produced.get('tldr', '')}\n\n"
        f"{produced.get('article', '')}"
    )
    answer = ask_now(
        model.id, system=IMAGE_PROMPT_ONLY, user=article, name=f"{slug}-image-prompt",
        purpose=f"the illustration prompt missing from the {model.short_name} edition of "
                f"'{story_details(slug)['title']}'",
        actor=actor, max_output_tokens=2000, use_cache=not another_chance,
    )
    prompt = " ".join(answer.text.split()).strip().strip('"').strip()
    if not prompt:
        return None

    produced["image_prompt"] = prompt
    rendering["produced"] = produced
    rendering["image_prompt_asked_separately"] = True
    if another_chance:
        rendering["image_prompt_second_chance"] = True
    rendering["image_prompt_cost_usd"] = answer.cost_usd
    rendering["cost_usd"] = rendering.get("cost_usd", 0.0) + answer.cost_usd
    rendering_path.write_text(json.dumps(rendering, ensure_ascii=False, indent=1), encoding="utf-8")
    (folder / "image-prompt.txt").write_text(prompt, encoding="utf-8")
    write_readable(folder)
    return prompt


def reparse(slug: str, model: Model) -> bool:
    """
    Read an edition's RAW answer off disk again and rebuild its rendering.

    Why this exists: the raw text a model sent is always kept in answer.txt, so
    if our own reading of that text was ever at fault - and it was once, for the
    one model that cannot be handed a strict JSON shape - the fix costs nothing.
    No model is called, no money is spent, and the model's words are not altered
    by a single character.

    This is the ONLY kind of second look allowed. A poor answer is never
    re-bought (DECISIONS.md decision 16).
    """
    folder = edition_folder(slug, model)
    raw_path = folder / "answer.txt"
    rendering_path = folder / "rendering.json"
    if not raw_path.exists() or not rendering_path.exists():
        return False

    from lib.llm import _read_json_loosely  # the same reader the live path uses

    rendering = json.loads(rendering_path.read_text(encoding="utf-8"))
    produced = _read_json_loosely(raw_path.read_text(encoding="utf-8"))
    if not isinstance(produced, dict):
        return False
    if rendering.get("understood") and rendering.get("produced"):
        return False  # already fine, leave it alone

    rendering["understood"] = True
    rendering["produced"] = produced
    rendering["reparsed_at_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rendering_path.write_text(json.dumps(rendering, ensure_ascii=False, indent=1), encoding="utf-8")
    (folder / "article.md").write_text(
        f"# {produced.get('headline', '')}\n\n*{produced.get('tldr', '')}*\n\n"
        f"{produced.get('article', '')}\n", encoding="utf-8")
    (folder / "image-prompt.txt").write_text(str(produced.get("image_prompt", "")), encoding="utf-8")
    write_readable(folder)
    return True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render editions of stories.")
    parser.add_argument("--story", help="one story slug")
    parser.add_argument("--all", action="store_true", help="every story")
    parser.add_argument("--model", help="one model id from the roster")
    parser.add_argument("--all-models", action="store_true", help="every model on the roster")
    parser.add_argument("--batch", action="store_true", help="buy at half price, collect later")
    parser.add_argument("--again", action="store_true",
                        help="render even where a rendering already exists")
    parser.add_argument("--fill-image-prompts", action="store_true",
                        help="ask any edition missing an illustration prompt for one, "
                             "giving the model back its own article")
    parser.add_argument("--reparse", action="store_true",
                        help="re-read answers already on disk. Costs nothing, calls nobody.")
    parser.add_argument("--actor", default="claude-opus-5")
    args = parser.parse_args(argv)

    if args.fill_image_prompts:
        wanted_models = roster() if args.all_models or not args.model else [model_by_id(args.model)]
        wanted_slugs = all_story_slugs() if args.all or not args.story else [args.story]
        filled, spent = 0, 0.0
        for model in wanted_models:
            for slug in wanted_slugs:
                before = edition_folder(slug, model) / "rendering.json"
                prompt = fill_image_prompt(slug, model, actor=args.actor,
                                           another_chance=args.again)
                if prompt:
                    cost = json.loads(before.read_text(encoding="utf-8")).get("image_prompt_cost_usd", 0.0)
                    spent += cost
                    filled += 1
                    print(f"  {model.short_name} / {slug}  (${cost:.4f})")
                    print(f"    {prompt[:150]}...")
        print(f"\n{filled} missing illustration prompts written, ${spent:.4f} spent.")
        if filled:
            try:
                with connect() as db:
                    log_job(db, action_type="stage_run", actor=args.actor, cost_usd=spent,
                            plain_words=(
                                f"Asked for {filled} illustration prompts that were missing from "
                                f"otherwise-finished editions. Each model was handed back its OWN "
                                f"article and asked only for the picture, so the paragraph is still "
                                f"entirely its own work and nothing it wrote earlier was altered. "
                                f"Every edition must carry an instruction for its own illustration, "
                                f"because the pictures are half of what a reader compares."))
            except Exception as problem:  # noqa: BLE001
                print(f"(could not write to the ledger: {type(problem).__name__})")
        return 0

    if args.reparse:
        fixed = 0
        for model in (roster() if args.all_models or not args.model else [model_by_id(args.model)]):
            for slug in (all_story_slugs() if args.all or not args.story else [args.story]):
                if reparse(slug, model):
                    print(f"  re-read {slug} / {model.short_name}")
                    fixed += 1
        print(f"\n{fixed} editions re-read from answers already on disk. Cost: nothing.")
        return 0

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
