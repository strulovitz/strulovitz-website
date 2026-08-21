#!/usr/bin/env python3
"""
WEEKLY SNAPSHOT OF WHAT PEOPLE ACTUALLY USE
===========================================

WHAT THIS DOES, IN ONE SENTENCE
Once a week it records how much traffic each AI model is really getting, so the
magazine can rank models by what people use instead of by what a catalogue
lists.

WHY THIS EXISTS (Nir's insight, 2026-08-21)
The project's first attempt at "which models matter" was a pile of clever rules
about version numbers and family names, and it was wrong: it declared Grok 4.20
newer than Grok 4.6, because as arithmetic 20 is bigger than 6. Nir asked the
obvious question - does the source not publish how much each model is USED? It
does. And usage settles in one number what no rule could: nobody has to judge
whether an old variant still matters when its share of traffic is zero.
It also confirmed Nir's instinct exactly: on 2026-08-20 the top ten models
carried 81.7 percent of all traffic.

WHERE THE NUMBERS COME FROM, AND THE HONEST LIMITS OF THEM
The public page https://openrouter.ai/rankings carries, inside the page itself,
the daily token and request totals per model. There is no documented API for it,
so this script reads the page and pulls out that data. Three limits must travel
with every figure ever derived from it, and they are printed by the script too:
1. It is ONE BROKER'S TRAFFIC, not the world's. Somebody calling OpenAI or
   Anthropic directly is invisible here, so the big labs' own APIs are
   under-counted. This is a measure of a large, real, but partial market.
2. The page hands out a LEADERBOARD, not a census: roughly the top twenty. A
   model missing from it is UNKNOWN, never zero. Recording a missing model as
   zero would be inventing data (bible/part-02.md 2.8: missing is missing).
3. It is a web page, not a contract, so its shape can change without warning.
   The script therefore fails loudly rather than saving something empty, and
   the price archive - which uses a proper public API - remains the project's
   solid ground.

POLITENESS AND HONESTY ABOUT SCRAPING
One request, once a week, of a public page, with a user agent that says who we
are and why. No login, no paywall, nothing hidden. The data is republished with
its source named and its limits stated, which is the whole ethic of LAW 7.

WHERE THE DATA GOES
pipeline/snapshots/openrouter-usage/YYYY-MM-DD.json plus index.json, in the same
style as the price archive, and then into Neo4j by stages/load_usage.py .

HOW TO RUN IT
    cd /home/nir/strulovitz-website/pipeline && uv run stages/snapshot_usage.py
Add --dry-run to fetch and report without saving anything.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import httpx

PIPELINE_DIR = Path(__file__).resolve().parents[1]
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

RANKINGS_URL = "https://openrouter.ai/rankings"
OUTPUT_DIR = PIPELINE_DIR / "snapshots" / "openrouter-usage"
SCHEMA_VERSION = 1

# Says who we are. A scraper that hides is a scraper that deserves blocking.
USER_AGENT = (
    "AI-PANORAMA/1.0 (+https://www.strulovitz.org/) "
    "weekly-usage-archive; contact via strulovitz.org"
)

# If a fetch yields fewer than this many models, something has changed and the
# script refuses to save a crippled file. A gap in the archive is honest; a file
# that quietly claims three models exist is not.
MINIMUM_PLAUSIBLE_ROWS = 5

# The usage records sit inside the page as JSON with escaped quotes. This finds
# them without needing to understand the rest of the page.
#
# It matches from '{"date":' up to the first closing brace, allowing no braces
# in between: the records are flat objects of numbers and short strings, so that
# is exactly right and cannot run away into the rest of the page. An earlier
# version of this pattern insisted the record ENDED with a particular field, and
# silently matched nothing when that field moved. Anchoring to the shape rather
# than to a field name is why this version survives the page being reshuffled.
RECORD_PATTERN = re.compile(
    r'\{"date":"[^"]+","model_permaslug":"[^"]+?"[^{}]*\}'
)


def fetch_page(url: str = RANKINGS_URL) -> str:
    """Fetch the rankings page once, politely, with a real timeout."""
    with httpx.Client(timeout=60, follow_redirects=True,
                      headers={"User-Agent": USER_AGENT}) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text


def extract_records(page_text: str) -> list[dict[str, Any]]:
    """
    Pull the usage records out of the page.

    The page escapes its quotes, so they are unescaped first. Anything that does
    not parse as JSON is skipped rather than patched up: a half-understood record
    is worse than a missing one.
    """
    unescaped = page_text.replace('\\"', '"')
    records: list[dict[str, Any]] = []
    for candidate in RECORD_PATTERN.findall(unescaped):
        try:
            records.append(json.loads(candidate))
        except json.JSONDecodeError:
            continue
    return records


def to_rows(records: list[dict[str, Any]], snapshot_date: str) -> list[dict[str, Any]]:
    """
    Turn the page's records into our own rows, and work out each model's share.

    The share is computed over the models PRESENT in this leaderboard, and the
    row says so in its own field name (share_of_ranked_traffic_percent) so that
    nobody can later mistake it for a share of the whole world.
    """
    total_tokens = sum(
        (r.get("total_prompt_tokens") or 0) + (r.get("total_completion_tokens") or 0)
        for r in records
    ) or 1

    rows: list[dict[str, Any]] = []
    for rank, record in enumerate(
        sorted(records,
               key=lambda r: (r.get("total_prompt_tokens") or 0) + (r.get("total_completion_tokens") or 0),
               reverse=True),
        start=1,
    ):
        tokens = (record.get("total_prompt_tokens") or 0) + (record.get("total_completion_tokens") or 0)
        permaslug = record.get("model_permaslug") or ""
        rows.append({
            "schema_version": SCHEMA_VERSION,
            "snapshot_date": snapshot_date,
            "usage_date": (record.get("date") or "")[:10],
            "provider": "openrouter",
            "rank": rank,
            "model_permaslug": permaslug,
            # The dated build suffix is stripped to give the plain model id, so
            # these rows can meet the price rows on the same name. Both are kept:
            # the exact build is evidence, the plain id is the join.
            "model_id_plain": re.sub(r"-20\d{6}$", "", permaslug),
            "variant": record.get("variant"),
            "prompt_tokens": record.get("total_prompt_tokens"),
            "completion_tokens": record.get("total_completion_tokens"),
            "reasoning_tokens": record.get("total_native_tokens_reasoning"),
            "cached_tokens": record.get("total_native_tokens_cached"),
            "total_tokens": tokens,
            "requests": record.get("count"),
            "tool_calls": record.get("total_tool_calls"),
            "share_of_ranked_traffic_percent": round(100.0 * tokens / total_tokens, 4),
            "source_page": RANKINGS_URL,
            "license_of_data": "read from a public web page; source named on publication",
            # The three limits, carried on every single row so they can never be
            # separated from the number they qualify.
            "coverage_note": ("one broker's traffic only, not the whole market; "
                              "a leaderboard of roughly the top twenty, so a model "
                              "absent from it is UNKNOWN, not zero"),
        })
    return rows


def write_snapshot(rows: list[dict[str, Any]], snapshot_date: str, *, force: bool = False) -> Path:
    """Save one dated file, refusing to overwrite an existing archive file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{snapshot_date}.json"
    if path.exists() and not force:
        raise FileExistsError(
            f"{path.name} already exists. The archive is never overwritten "
            "(bible LAW 12). Pass --force only if you truly mean to replace it."
        )

    document = {
        "schema_version": SCHEMA_VERSION,
        "snapshot_date": snapshot_date,
        "taken_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_page": RANKINGS_URL,
        "license_of_data": "read from a public web page; source named on publication",
        "what_this_is": (
            "How much traffic each AI model received, as published by one broker. "
            "Used to rank models by what people actually use rather than by what a "
            "catalogue lists."
        ),
        "limits_of_this_data": [
            "One broker's traffic only. Anybody calling a lab's own API directly "
            "is invisible here, so the big labs are under-counted.",
            "A leaderboard of roughly the top twenty models, not a census. A model "
            "missing from this file is UNKNOWN, never zero.",
            "Read from a public web page with no documented API, so its shape may "
            "change without warning.",
        ],
        "row_count": len(rows),
        "rows": rows,
    }
    path.write_text(json.dumps(document, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    update_index()
    return path


def update_index() -> None:
    """Rewrite the little list of every usage snapshot held, oldest first."""
    files = sorted(p for p in OUTPUT_DIR.glob("*.json") if p.name != "index.json")
    entries = []
    for path in files:
        document = json.loads(path.read_text(encoding="utf-8"))
        entries.append({
            "snapshot_date": document["snapshot_date"],
            "file": path.name,
            "row_count": document["row_count"],
            "taken_at_utc": document["taken_at_utc"],
        })
    index = {
        "schema_version": SCHEMA_VERSION,
        "what_this_is": ("Every model-usage snapshot this project holds, oldest "
                         "first. One entry per day taken."),
        "snapshot_count": len(entries),
        "first_snapshot": entries[0]["snapshot_date"] if entries else None,
        "latest_snapshot": entries[-1]["snapshot_date"] if entries else None,
        "snapshots": entries,
    }
    (OUTPUT_DIR / "index.json").write_text(
        json.dumps(index, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    snapshot_date = date.today().isoformat()

    try:
        page = fetch_page()
    except Exception as problem:  # noqa: BLE001
        print(f"Could not fetch the rankings page: {type(problem).__name__}. "
              "Nothing was saved.", file=sys.stderr)
        return 2

    records = extract_records(page)
    if len(records) < MINIMUM_PLAUSIBLE_ROWS:
        print(f"Only found {len(records)} usage record(s) in the page. The page "
              "has probably changed shape. Refusing to save a crippled file - a "
              "gap in the archive is honest, a wrong file is not.", file=sys.stderr)
        return 3

    rows = to_rows(records, snapshot_date)

    print(f"Found {len(rows)} models with real usage, covering "
          f"{rows[0]['usage_date']}.")
    top_ten_share = sum(r["share_of_ranked_traffic_percent"] for r in rows[:10])
    print(f"The top ten of them hold {top_ten_share:.1f} percent of the traffic "
          "in this leaderboard.")
    for row in rows[:5]:
        print(f"   {row['share_of_ranked_traffic_percent']:5.2f}%  "
              f"{row['total_tokens']/1e12:6.2f} trillion tokens  {row['model_permaslug']}")

    if dry_run:
        print("DRY RUN: nothing was saved.")
        return 0

    path = write_snapshot(rows, snapshot_date, force=force)
    print(f"Saved {path}")

    # Record it, so the logbook can answer "where did this number come from".
    try:
        from lib.db import connect, log_job
        with connect() as db:
            log_job(db, action_type="snapshot", actor="timer", verdict="ok",
                    outputs=[str(path.relative_to(PIPELINE_DIR.parent))],
                    plain_words=(
                        f"Recorded how much each AI model was actually used, "
                        f"{len(rows)} models, so the magazine can rank them by "
                        "real use instead of by what a price list happens to "
                        "contain."))
    except Exception as problem:  # noqa: BLE001
        # The file is saved; a logbook failure must never destroy a snapshot.
        print(f"Saved the file, but could not write to the logbook: "
              f"{type(problem).__name__}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
