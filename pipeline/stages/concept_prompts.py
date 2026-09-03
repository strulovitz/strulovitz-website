#!/usr/bin/env python3
"""
THE PICTURES FOR THE ENCYCLOPEDIA
=================================

WHAT THIS IS, IN ONE SENTENCE
The stage that asks each of the eight models to write the illustration prompt
for its own encyclopedia entries, so that every node in the magazine finally
carries a picture - which is what the Bible demanded all along (part-00.md
0.6, the reader's ladder, rung 4: "every node has an AI-generated
illustration").

WHY ONLY NOW (Nir's question, answered in code)
The editions machine only ever asked for ONE image prompt per story, so 40
story pictures existed and the encyclopedia's ~120 entries had none, and no
agent ever raised that gap against the Bible. Nir: "ok do it" (2026-09-03).

THE INSTRUCTION IS THE CORRECTED ONE, NOTHING ELSE
Nir, 2026-09-03, explicit: "you do not put stupid things in the prompt like
'no text', 'no faces', 'same palette', none of this kind of shit!!!" The
system prompt below is the same honest instruction the story pictures used
(one paragraph, capture the ideas as fully as you can) with ZERO banned
phrases, ZERO style prohibitions, ZERO leftovers of the abandoned rule set.

ONE MODEL DOES EVERY ROLE (DECISIONS.md decision 12)
Each model writes the prompt for ITS OWN entry, from its own words, so the
concept pictures are as comparable between editions as the story pictures
are. Nothing is edited, nothing is retried for quality (decision 16): what
comes back is what gets rendered.

WHERE IT IS STORED
On the Concept node in the database (the one door), with cost and time; and
exported to concept-prompts.json beside the edition for human reading.

HOW TO RUN IT
    cd pipeline && uv run stages/concept_prompts.py
    cd pipeline && uv run stages/concept_prompts.py --again   (re-ask everything)
Safe to re-run: editions whose concepts already have prompts are skipped.

COST
About 120 short calls across the eight models. Budget: well under one dollar
at full price. The exact number is printed and ledgered at the end.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.db import (  # noqa: E402
    connect,
    log_job,
    read_concepts_for_model,
    upsert_concept_image_prompt,
)
from lib.llm import ask_now, roster  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]

CONCEPT_IMAGE_PROMPT = """You wrote the encyclopedia entry below for AI PANORAMA,
an independent magazine about artificial intelligence. Everything about it is
your own work. The only thing still missing is the instruction for its
illustration.

Write ONE paragraph describing a single illustration for this entry. The
illustration must capture the entry's own ideas as clearly and completely as
you can, so that a reader who only looked at the picture would still
understand what the entry is actually about.

Answer with the paragraph alone. No preamble, no explanation, no quotation
marks, no JSON."""


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Ask models for concept image prompts.")
    parser.add_argument("--again", action="store_true",
                        help="ask again even where a prompt already exists")
    parser.add_argument("--actor", default="glm-5.3")
    args = parser.parse_args(argv)

    started = time.monotonic()
    start_clock = datetime.now().strftime("%H:%M:%S")
    total_cost = 0.0
    asked = 0
    skipped = 0
    failed: list[str] = []

    with connect() as db:
        # The full shopping list first, so the progress line can tell the truth
        # about totals from the very first question.
        everything: list[tuple] = []
        for model in roster():
            for concept in read_concepts_for_model(db, model.slug):
                everything.append((model, concept))
        total = len(everything)
        print(f"{total} encyclopedia entries to illustrate across "
              f"{len(roster())} editions' models.")

        for index, (model, concept) in enumerate(everything, start=1):
            label = f"{concept['story']} / {model.slug} / {concept['slug']}"
            has_prompt = bool((concept.get("image_prompt") or "").strip())
            if has_prompt and not args.again:
                skipped += 1
                continue
            elapsed = time.monotonic() - started
            done = asked + skipped
            eta = f", ETA ~{(total - done) * (elapsed / done) / 60:.0f} min" if done else ""
            print(f"[{index}/{total} = {(index - 1) / total * 100:3.0f}% done | "
                  f"started {start_clock}, {total_cost:.4f} dollars so far{eta}] "
                  f"asking {model.short_name} about {concept['slug']} ...",
                  flush=True)
            try:
                answer = ask_now(
                    model.id,
                    system=CONCEPT_IMAGE_PROMPT,
                    user=f"{concept['term']}\n\n{concept['explanation']}",
                    purpose=f"the {model.short_name} encyclopedia illustration "
                            f"for {concept['slug']}",
                    actor=args.actor,
                    name=f"concept-image-prompt-{concept['slug']}",
                )
                prompt = (answer.text or "").strip()
                if not prompt:
                    failed.append(label)
                    print(f"  [{index}/{total}] {label} came back EMPTY - "
                          f"recorded as that model's result, not retried.")
                    continue
                upsert_concept_image_prompt(
                    db, concept["story"], model.slug, concept["slug"], prompt,
                    cost_usd=answer.cost_usd,
                    asked_at_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    model_served=answer.model_served,
                    generation_id=answer.generation_id,
                )
                asked += 1
                total_cost += answer.cost_usd
                print(f"  [{index}/{total}] {label} OK "
                      f"({answer.cost_usd:.4f} dollars, {answer.seconds_waited:.0f}s)")
                # The human-readable export beside the edition (LAW 5: files
                # are exports; the database is truth).
                folder = (REPO_ROOT / "content" / "stories" / concept["story"]
                          / "editions" / model.slug)
                folder.mkdir(parents=True, exist_ok=True)
                export_path = folder / "concept-prompts.json"
                prompts = json.loads(export_path.read_text(encoding="utf-8")) \
                    if export_path.exists() else {}
                prompts[concept["slug"]] = prompt
                export_path.write_text(
                    json.dumps(prompts, ensure_ascii=False, indent=1), encoding="utf-8")
            except Exception as problem:  # noqa: BLE001
                failed.append(label)
                print(f"  [{index}/{total}] {label} FAILED to ask: "
                      f"{type(problem).__name__}: {problem}")

        seconds = time.monotonic() - started
        print(f"\nFINISHED: asked {asked}, skipped {skipped} (already had one), "
              f"{len(failed)} failed, {total_cost:.4f} dollars total, "
              f"{seconds / 60:.1f} minutes.")
        for note in failed:
            print(f"  failed: {note}")

        log_job(
            db,
            action_type="stage_run",
            actor=args.actor,
            verdict="ok" if asked and not failed else ("partial" if asked else "failed"),
            cost_usd=total_cost,
            duration_s=seconds,
            plain_words=(
                f"Asked the eight models to write illustration prompts for their own "
                f"encyclopedia entries: {asked} written, {skipped} already had one, "
                f"{len(failed)} failed, for {total_cost:.4f} dollars - so every entry "
                f"in the magazine can carry a picture, as the Bible's reader ladder "
                f"always said it should."
            ),
        )
    return 0 if asked and not failed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
