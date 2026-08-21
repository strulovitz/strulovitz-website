#!/usr/bin/env python3
"""
MAKING A STORY: FROM LINKS TO FROZEN EVIDENCE
=============================================

WHAT THIS IS, IN ONE SENTENCE
The stage that reads content/inbox.txt, fetches everything Nir linked, freezes
the text on disk, and writes down what the story is - and then stops, because
the writing itself belongs to the eight edition models and not to this file.

WHAT IT PRODUCES, PER STORY
    content/stories/<date>-<short-title>/
        story.json          what this story is and which sources it stands on
        sources/            the frozen text of every source, plus its details
        editions/           empty for now. One folder per model, filled later.

WHY IT STOPS THERE
Every model must read exactly the same words, or the comparison between
editions means nothing (DECISIONS.md decision 20). So the evidence is gathered
once, frozen, and never fetched again.

THE TWO-SOURCE RULE
A story with fewer than two working sources is NOT created. It is reported, with
the reason each source failed, and left in the inbox for Nir to fix. Nothing is
half-written and nothing is quietly published from a single source
(DECISIONS.md decision 13).

HOW TO RUN IT
    cd /home/nir/strulovitz-website/pipeline && uv run stages/make_story.py
Safe to re-run: stories that already exist are skipped, and a source already
frozen is not fetched again.

    uv run stages/make_story.py --refetch <story-folder-name>
Fetches a story's sources again, for the case where a link was fixed.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.db import connect, log_job  # noqa: E402
from lib.llm import settings  # noqa: E402
from lib.sources import CouldNotFetch, Source, fetch, freeze, read_frozen  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
INBOX = REPO_ROOT / "content" / "inbox.txt"
STORIES = REPO_ROOT / "content" / "stories"


def read_inbox(path: Path = INBOX) -> list[tuple[str, list[str]]]:
    """
    Read the inbox into a list of (title, links).

    The format is deliberately the simplest thing that works, because Nir types
    into it by hand: a line beginning with STORY starts a new story, every other
    non-empty line is a link, and anything after a # is a note for humans.
    """
    if not path.exists():
        return []
    stories: list[tuple[str, list[str]]] = []
    title = ""
    links: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.upper().startswith("STORY"):
            if title and links:
                stories.append((title, links))
            title = line[5:].strip(" :-")
            links = []
        elif line.startswith(("http://", "https://")):
            links.append(line)
    if title and links:
        stories.append((title, links))
    return stories


def slug_for(title: str, sources: list[Source]) -> str:
    """
    The story's folder name and its web address: a date, then a short title.

    The date is the EARLIEST date the sources themselves carry, because that is
    when the thing being reported actually happened, not when we got round to
    writing about it. Where no source carries a date, today is used and that is
    honest about what we know.
    """
    dates = sorted(s.published[:10] for s in sources if len(s.published) >= 10)
    when = dates[0] if dates else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    stub = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"{when}-{stub[:60]}"


def existing_slugs() -> dict[str, str]:
    """Every story already made, as {title: folder name}, so nothing is redone."""
    found: dict[str, str] = {}
    if not STORIES.exists():
        return found
    for folder in sorted(STORIES.iterdir()):
        details = folder / "story.json"
        if details.exists():
            try:
                found[json.loads(details.read_text(encoding="utf-8"))["title"]] = folder.name
            except (json.JSONDecodeError, KeyError, OSError):
                continue
    return found


def make_story(title: str, links: list[str], *, minimum: int) -> tuple[str, list[str]]:
    """
    Fetch and freeze one story's sources. Returns (folder name, problems).

    Nothing is written unless at least `minimum` sources came back, so a
    half-fetched story never leaves a folder behind to confuse the next run.
    """
    collected: list[Source] = []
    problems: list[str] = []
    for link in links:
        try:
            collected.append(fetch(link))
            print(f"    got  {collected[-1].words:>5} words  {collected[-1].title[:64]}")
        except CouldNotFetch as why:
            problems.append(f"{link} - {why}")
            print(f"    FAILED  {link}\n            {why}")

    if len(collected) < minimum:
        return "", problems + [
            f"Only {len(collected)} of {len(links)} sources could be collected, and the "
            f"minimum is {minimum}. This story was NOT created. Fix or replace the failed "
            f"links in content/inbox.txt and run this again."
        ]

    slug = slug_for(title, collected)
    folder = STORIES / slug
    (folder / "sources").mkdir(parents=True, exist_ok=True)
    (folder / "editions").mkdir(parents=True, exist_ok=True)
    for source in collected:
        freeze(source, folder / "sources")

    details = {
        "slug": slug,
        "title": title,
        "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "language": settings().language,
        "source_count": len(collected),
        "total_words": sum(s.words for s in collected),
        "sources": [
            {k: v for k, v in asdict(s).items() if k != "text"} | {"text_file": s.filename}
            for s in collected
        ],
        "failed_links": problems,
    }
    (folder / "story.json").write_text(
        json.dumps(details, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    return slug, problems


def main(argv: list[str]) -> int:
    minimum = settings().minimum_sources
    wanted = read_inbox()
    if not wanted:
        print(f"Nothing in {INBOX}. Add some links and run this again.")
        return 0

    already = existing_slugs()
    made: list[str] = []
    skipped: list[str] = []
    refused: list[tuple[str, list[str]]] = []

    print(f"{len(wanted)} stories in the inbox. Minimum {minimum} sources each.\n")
    for title, links in wanted:
        if title in already:
            skipped.append(f"{title}  ->  {already[title]}")
            print(f"  ALREADY DONE  {title}")
            continue
        print(f"  FETCHING  {title}  ({len(links)} links)")
        slug, problems = make_story(title, links, minimum=minimum)
        if slug:
            made.append(slug)
            print(f"    -> content/stories/{slug}\n")
        else:
            refused.append((title, problems))
            print()

    print("=" * 78)
    print(f"made {len(made)}, already done {len(skipped)}, refused {len(refused)}")
    for slug in made:
        print(f"  new: {slug}")
    for title, problems in refused:
        print(f"  refused: {title}")
        for problem in problems:
            print(f"      {problem}")

    if made or refused:
        words = (
            f"Collected the sources for {len(made)} new stories from Nir's inbox "
            f"({', '.join(made) if made else 'none'}). "
            f"{len(skipped)} were already done. "
            + (f"{len(refused)} were REFUSED because fewer than {minimum} of their sources "
               f"could be fetched, which is the rule that protects Nir from publishing a "
               f"story built on one article: {', '.join(t for t, _ in refused)}."
               if refused else "Nothing was refused.")
        )
        try:
            with connect() as db:
                log_job(db, action_type="stage_run", actor="claude-opus-5",
                        verdict="partial" if refused else "ok",
                        plain_words=words, inputs={"inbox": str(INBOX)}, outputs=made)
        except Exception as problem:  # noqa: BLE001
            print(f"\n(could not write to the ledger: {type(problem).__name__})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
