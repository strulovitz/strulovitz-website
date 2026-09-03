#!/usr/bin/env python3
"""
STORING THE MAGAZINE'S KNOWLEDGE IN THE DATABASE
=================================================

WHAT THIS IS, IN ONE SENTENCE
The stage that loads every story, every frozen source, and every edition the
eight models wrote into Neo4j, so the database - not a folder of files - is
the single permanent source of truth (bible/part-00.md LAW 5).

WHY THIS STAGE HAD TO BE WRITTEN (2026-09-03, a violation corrected)
The Bible was explicit from day one: LAW 5 - "Neo4j as the single permanent
source of truth for all knowledge"; Part 01 1.5 iron rule 3 - "Every stage
reads and writes THROUGH Neo4j; files on disk are caches and exports, never
truth." The editions machine was built file-first anyway, and no agent raised
the conflict to Nir, which Part 00 LAW 10 says is a failed task in itself.
Nir caught it and ordered the Bible followed exactly. This stage is the
correction: it takes what exists on disk and stores it as truth, and from
now on the reading stages read from the database, not from files.

WHAT IT STORES, THROUGH pipeline/lib/db.py (the one door, Part 01 1.4)
    content/stories/<slug>/story.json
        -> the Story node and its Source nodes
    content/stories/<slug>/editions/<model>/rendering.json
        -> the Edition node: prose, tags, concepts, key points, read-next
           links, cost, tokens, timing - one model's whole rendering
    content/stories/<slug>/editions/<model>/images/meta.json (if present)
        -> the ImageJob: which local model, which seed, how long it took

WHAT STAYS ON DISK, ON PURPOSE (the Bible says so, not laziness)
    The frozen source TEXT (the evidence bundle) - Part 02 2.2.7 calls
    raw_text_path a "kitchen disk cache" and Part 12 12.2.3 backs it up as
    files. The database keeps the fingerprint and the pointer.
    The article.md / EDITION.md / image-prompt.txt copies - those are
    human-readable EXPORTS of what is now stored in the database, exactly
    the "files are caches and exports" that Part 01 allows.
    The rendered pictures - artifacts, regenerable from the stored seed
    (Part 12 12.2.4: "we back up truth, not artifacts").

HOW TO RUN IT
    cd pipeline && uv run stages/store_knowledge.py
Safe to re-run: everything is MERGE-based, keyed by stable ids (LAW 12).
A re-run after a re-parse UPDATES truth; it never duplicates anything.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.db import (  # noqa: E402
    connect,
    ensure_knowledge_schema,
    ensure_schema,
    knowledge_counts,
    log_job,
    upsert_edition,
    upsert_story,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
STORIES = REPO_ROOT / "content" / "stories"


def main() -> int:
    start = time.monotonic()
    with connect() as db:
        # Both schema families: the ledger's rules, and the knowledge's rules.
        ensure_schema(db)
        ensure_knowledge_schema(db)

        stories_stored = 0
        editions_stored = 0
        skipped_no_produced = 0

        # TWO PASSES, IN THIS ORDER, ON PURPOSE. The first pass creates every
        # Story and Source node; only then does the second pass store the
        # editions. The reason is the read-next links: an edition of an EARLY
        # story points at a LATER story, and if the target Story node does not
        # exist yet, the edge would be silently dropped. The first version of
        # this stage did one pass (story, then its editions, then the next
        # story) and lost 18 read-next links exactly that way - a real bug this
        # comment exists so no agent ever reintroduces.
        stories_on_disk: list[tuple[dict, Path]] = []
        for story_folder in sorted(STORIES.iterdir()):
            story_path = story_folder / "story.json"
            if not story_path.exists():
                continue
            story = json.loads(story_path.read_text(encoding="utf-8"))
            upsert_story(db, story)
            stories_on_disk.append((story, story_folder))
            stories_stored += 1

        for story, story_folder in stories_on_disk:
            for edition_folder in sorted((story_folder / "editions").iterdir()):
                rendering_path = edition_folder / "rendering.json"
                if not rendering_path.exists():
                    continue
                rendering = json.loads(rendering_path.read_text(encoding="utf-8"))
                image_meta_path = edition_folder / "images" / "meta.json"
                image_meta = None
                if image_meta_path.exists():
                    image_meta = json.loads(image_meta_path.read_text(encoding="utf-8"))
                stored = upsert_edition(db, story, rendering, image_meta)
                if stored:
                    editions_stored += 1
                else:
                    skipped_no_produced += 1

        counts = knowledge_counts(db)
        seconds = time.monotonic() - start

        print("The database is now the source of truth for the magazine:")
        for name, number in counts.items():
            print(f"  {name:<15} {number}")
        print(f"  (this run: {stories_stored} stories, {editions_stored} editions "
              f"stored, {skipped_no_produced} produced-nothing renderings noted, "
              f"{seconds:.1f} seconds)")

        log_job(
            db,
            action_type="stage_run",
            actor="glm-5.3",
            verdict="ok" if editions_stored else "failed",
            cost_usd=0.0,
            duration_s=seconds,
            plain_words=(
                f"Loaded the magazine's knowledge into the database: {stories_stored} "
                f"stories, {counts['sources']} frozen sources, and {editions_stored} "
                f"editions by the eight models, plus their {counts['tags']} tags, "
                f"{counts['concepts']} encyclopedia entries and "
                f"{counts['read_next_links']} read-next links. The database, not "
                f"the files, is now the permanent truth - correcting the earlier "
                f"violation of the Bible's Law 5."
            ),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
