#!/usr/bin/env python3
"""
POUR THE USAGE ARCHIVE INTO THE LIBRARY
=======================================

WHAT THIS DOES, IN ONE SENTENCE
Takes the dated usage files saved by stages/snapshot_usage.py and writes them
into Neo4j, joining each one to the price rows for the same model, so that "what
does it cost" and "does anyone actually use it" become one question.

WHY THE JOIN IS THE WHOLE POINT
A price on its own invites nonsense: the most expensive listing in a catalogue
is usually a forgotten research preview. Usage on its own is a popularity
contest. Together they answer the question a reader actually has - what do the
models people really use cost, and where is the market moving.

HOW THE JOIN IS MADE, AND WHERE IT IS HONEST ABOUT FAILING
The usage page names a model with a dated build, for example
anthropic/claude-opus-5-20260723 , while the price list calls the same thing
anthropic/claude-opus-5 . So the build date is stripped to give a plain id, and
that plain id is matched against the price rows. When no price row matches, the
usage row is still stored and simply carries no link: an unexplained gap that
can be seen and investigated beats a forced guess.

SAFE TO RUN AS OFTEN AS YOU LIKE (LAW 12)
One row per model per day per broker, enforced by the database, so a second run
writes nothing. The ledger is also asked whether a file was already loaded.

HOW TO RUN IT
    cd /home/nir/strulovitz-website/pipeline && uv run stages/load_usage.py
    --dry-run to look without writing, --force to reload a file already done.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

PIPELINE_DIR = Path(__file__).resolve().parents[1]
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from lib.db import connect, ensure_schema, log_job, already_done  # noqa: E402

USAGE_DIR = PIPELINE_DIR / "snapshots" / "openrouter-usage"
ACTION = "stage_run"
STAGE_NAME = "load_usage"

# Written to the database. Everything else stays in the file.
ROW_FIELDS = (
    "schema_version", "snapshot_date", "usage_date", "provider", "rank",
    "model_permaslug", "model_id_plain", "variant",
    "prompt_tokens", "completion_tokens", "reasoning_tokens", "cached_tokens",
    "total_tokens", "requests", "tool_calls",
    "share_of_ranked_traffic_percent",
    "source_page", "license_of_data", "coverage_note",
)

WRITE_ROWS = """
UNWIND $rows AS row

MERGE (u:UsageSnapshot {
    usage_date: row.usage_date,
    provider: row.provider,
    model_permaslug: row.model_permaslug
})
ON CREATE SET u += row.properties,
              u.first_written_utc = $now_utc,
              u.from_file = $file_name,
              u.from_file_sha256 = $file_hash

// Join to the price rows for the same plain model id, on the nearest price day
// we hold. No match simply means no link, which is a visible gap rather than a
// guess.
WITH u, row
OPTIONAL MATCH (p:PriceSnapshot {openrouter_model_id: row.model_id_plain})
FOREACH (_ IN CASE WHEN p IS NULL THEN [] ELSE [1] END |
    MERGE (u)-[:PRICED_BY]->(p)
)

// And to the waiting-room proposal for that model, if one exists, so that a
// human deciding whether a model matters can see its traffic beside it.
WITH u, row
OPTIONAL MATCH (e:EntityProposal)<-[:ABOUT_MODEL]-(:PriceSnapshot {openrouter_model_id: row.model_id_plain})
FOREACH (_ IN CASE WHEN e IS NULL THEN [] ELSE [1] END |
    MERGE (u)-[:USAGE_OF]->(e)
)
"""


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_one_file(driver, path: Path, *, dry_run: bool, force: bool) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    digest = file_hash(path)
    fingerprint = {"stage": STAGE_NAME, "file": path.name, "sha256": digest}

    if not force and already_done(driver, ACTION, fingerprint):
        return {"file": path.name, "status": "already loaded, skipped", "rows": 0}

    rows = [{
        "usage_date": r["usage_date"],
        "provider": r.get("provider", "openrouter"),
        "model_permaslug": r["model_permaslug"],
        "model_id_plain": r["model_id_plain"],
        "properties": {field: r.get(field) for field in ROW_FIELDS},
    } for r in document.get("rows", []) if r.get("model_permaslug")]

    if dry_run:
        return {"file": path.name, "status": "would load", "rows": len(rows)}

    started = time.monotonic()
    with driver.session() as session:
        session.run(WRITE_ROWS, rows=rows,
                    now_utc=time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
                    file_name=path.name, file_hash=digest)
        linked = session.run(
            "MATCH (u:UsageSnapshot {usage_date: $date})-[:PRICED_BY]->() "
            "RETURN count(DISTINCT u) AS n", date=document["rows"][0]["usage_date"]
        ).single()["n"]
    duration = time.monotonic() - started

    log_job(
        driver, action_type=ACTION, actor="claude-opus-5", verdict="ok",
        inputs=fingerprint, duration_s=round(duration, 2),
        outputs=[f"UsageSnapshot rows for {document['snapshot_date']}"],
        plain_words=(
            f"Copied into the library how much each of {len(rows)} models was "
            f"really used, and joined {linked} of them to their prices, so the "
            "magazine can talk about what people actually use rather than what a "
            "catalogue happens to list."
        ),
    )
    return {"file": path.name, "status": "loaded", "rows": len(rows),
            "joined_to_a_price": linked}


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv

    files = sorted(p for p in USAGE_DIR.glob("*.json") if p.name != "index.json")
    if not files:
        print("There are no usage files to load yet. Run stages/snapshot_usage.py first.")
        return 0

    with connect() as db:
        if not dry_run:
            ensure_schema(db)
        for path in files:
            summary = load_one_file(db, path, dry_run=dry_run, force=force)
            extra = summary.get("joined_to_a_price")
            print(f"  {summary['file']}: {summary['status']}, {summary['rows']} row(s)"
                  + (f", {extra} joined to a price" if extra is not None else ""))

        with db.session() as session:
            totals = session.run(
                "MATCH (u:UsageSnapshot) RETURN count(u) AS rows, "
                "count(DISTINCT u.usage_date) AS days"
            ).single()
        print(f"The library now holds {totals['rows']} usage row(s) covering "
              f"{totals['days']} day(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
