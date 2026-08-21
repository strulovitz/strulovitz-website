#!/usr/bin/env python3
"""
POUR THE PRICE ARCHIVE INTO THE LIBRARY
=======================================

WHAT THIS DOES, IN ONE SENTENCE
Takes the dated price files that the weekly snapshot already saved on disk and
writes them into Neo4j as permanent rows, so that questions can be asked of
them instead of only reading them.

WHY BOTH, THE FILES AND THE DATABASE (bible/part-09.md 9.4.1, LAW 12)
The JSON files stay exactly as they are, forever. They are the FROZEN EVIDENCE:
plain text, readable by anything, still openable in twenty years by a person
with no database and no Python. The database is the WORKING COPY, which exists
because "how did this model's price move over two years" is a question you
cannot answer by opening files by hand. If the database were ever lost, this
script rebuilds it from the files. If the files were lost, nothing could rebuild
them. That is why the files are the truth and the database is the convenience.

THE RULE THAT SHAPES THIS WHOLE SCRIPT (bible/part-02.md 2.4)
A model that appears in a price list is NOT thereby a fact about the world. The
Bible forbids silently inventing entities, because near-duplicate entities are
what has killed other knowledge bases: "GPT-5.6 Sol", "gpt5.6-sol" and "OpenAI's
Sol" becoming three different things that never join up again. So every new
model name lands in a WAITING ROOM as an EntityProposal, and becomes a real
entity only when Nir approves it. This script therefore never creates an Entity.

SAFE TO RUN AS OFTEN AS YOU LIKE (LAW 12)
Every row is written with MERGE against the database's own uniqueness rule
(date + provider + model), so running this twice writes nothing the second time.
Nothing is ever overwritten and nothing is ever deleted. Each file that has
already been loaded successfully is skipped by checking the job ledger.

HOW TO RUN IT
    cd /home/nir/strulovitz-website/pipeline && uv run stages/load_snapshots.py
Useful extras:
    --dry-run   say what would happen, write nothing at all
    --force     load even files the ledger says are already done (still cannot
                duplicate anything, because the database's rules forbid it)
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

SNAPSHOT_DIR = PIPELINE_DIR / "snapshots" / "openrouter"

# The action_type used in the ledger for this work, so that "has this file been
# loaded already" is a question with one answer.
ACTION = "stage_run"
STAGE_NAME = "load_snapshots"

# Only these fields of a snapshot row are written to the database, in this
# order. Everything else in the file stays in the file. The list is explicit on
# purpose: if OpenRouter invents a new field tomorrow, this script keeps working
# unchanged and a human decides deliberately whether the new field is wanted.
# The first eleven are the shape the Bible fixes in part-02.md 2.8; the rest are
# extras the snapshot script already collects honestly.
ROW_FIELDS = (
    "schema_version",
    "snapshot_date",
    "provider",
    "usd_per_m_input",
    "usd_per_m_output",
    "usd_per_m_cache_read",
    "usd_per_m_cache_write",
    "context_tokens",
    "max_output_tokens",
    "throughput_tps_median",
    "latency_s_p50",
    "source_api",
    "license_of_data",
    "openrouter_model_id",
    "canonical_slug",
    "display_name",
    "developer_hint",
    "modality",
    "is_moderated",
    "openrouter_created_unix",
)

# One Cypher statement, sent once per snapshot file with the whole day's rows as
# a parameter. Doing it row by row would be hundreds of round trips; doing it in
# one batch is a single conversation with the database.
WRITE_ROWS = """
UNWIND $rows AS row

// The price row itself: immutable, one per model per provider per day.
// MERGE on the key means a second run of the same day changes nothing.
MERGE (p:PriceSnapshot {
    snapshot_date: row.snapshot_date,
    provider: row.provider,
    openrouter_model_id: row.openrouter_model_id
})
ON CREATE SET p += row.properties,
              p.first_written_utc = $now_utc,
              p.from_file = $file_name,
              p.from_file_sha256 = $file_hash

// The waiting room. This is NOT an entity: it is a proposal for one, which Nir
// approves later (bible/part-02.md 2.4). first_seen is set once and never
// touched again, so the archive can always answer "when did this model appear".
MERGE (e:EntityProposal {proposed_entity_id: row.proposed_entity_id})
ON CREATE SET e.entity_type = 'model',
              e.name_canonical = row.properties.display_name,
              e.developer_hint = row.properties.developer_hint,
              e.proposed_by = 'openrouter-price-snapshot',
              e.status = 'pending',
              e.first_seen_snapshot = row.snapshot_date,
              e.schema_version = 1
SET e.last_seen_snapshot =
      CASE WHEN e.last_seen_snapshot IS NULL
                OR e.last_seen_snapshot < row.snapshot_date
           THEN row.snapshot_date ELSE e.last_seen_snapshot END

// Which price row is about which proposed model.
MERGE (p)-[:ABOUT_MODEL]->(e)
"""


def file_hash(path: Path) -> str:
    """A fingerprint of the exact bytes loaded, recorded on every row."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_rows(document: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Turn one snapshot file into the shape the Cypher statement above expects.

    A row is skipped, loudly, only if it has no model id at all, because such a
    row cannot be identified later and would be junk in the archive forever.
    """
    prepared: list[dict[str, Any]] = []
    for row in document.get("rows", []):
        model_id = row.get("openrouter_model_id")
        if not model_id:
            print(f"  skipping a row with no model id: {row.get('display_name')!r}")
            continue
        properties = {field: row.get(field) for field in ROW_FIELDS}
        prepared.append({
            "snapshot_date": row["snapshot_date"],
            "provider": row.get("provider", "openrouter"),
            "openrouter_model_id": model_id,
            # The snapshot script already worked out what entity id it would
            # PROPOSE for this model. We carry that word for word rather than
            # inventing our own, so the two scripts can never disagree.
            "proposed_entity_id": row.get("model") or f"ent-unknown-{model_id}",
            "properties": properties,
        })
    return prepared


def load_one_file(driver, path: Path, *, dry_run: bool, force: bool) -> dict[str, Any]:
    """Load one dated snapshot file. Returns a small summary for the caller."""
    document = json.loads(path.read_text(encoding="utf-8"))
    digest = file_hash(path)
    fingerprint = {"stage": STAGE_NAME, "file": path.name, "sha256": digest}

    if not force and already_done(driver, ACTION, fingerprint):
        return {"file": path.name, "status": "already loaded, skipped", "rows": 0}

    rows = prepare_rows(document)
    if dry_run:
        return {"file": path.name, "status": "would load", "rows": len(rows)}

    started = time.monotonic()
    with driver.session() as session:
        session.run(
            WRITE_ROWS,
            rows=rows,
            now_utc=time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
            file_name=path.name,
            file_hash=digest,
        )
        counted = session.run(
            "MATCH (p:PriceSnapshot {snapshot_date: $date}) RETURN count(p) AS n",
            date=document["snapshot_date"],
        ).single()["n"]
    duration = time.monotonic() - started

    log_job(
        driver,
        action_type=ACTION,
        actor="claude-opus-5",
        verdict="ok",
        inputs=fingerprint,
        outputs=[f"PriceSnapshot rows for {document['snapshot_date']}"],
        duration_s=round(duration, 2),
        plain_words=(
            f"Copied the price list of {document['snapshot_date']} into the "
            f"library, {len(rows)} models, so their prices can now be compared "
            "over time. The original file was left untouched as the evidence."
        ),
    )
    return {"file": path.name, "status": "loaded", "rows": len(rows),
            "rows_now_in_library_for_that_day": counted}


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv

    files = sorted(p for p in SNAPSHOT_DIR.glob("*.json") if p.name != "index.json")
    if not files:
        print("There are no snapshot files to load yet.")
        return 0

    with connect() as db:
        if not dry_run:
            ensure_schema(db)
        print(f"Found {len(files)} snapshot file(s)."
              + (" DRY RUN: nothing will be written." if dry_run else ""))
        for path in files:
            summary = load_one_file(db, path, dry_run=dry_run, force=force)
            print(f"  {summary['file']}: {summary['status']}, {summary['rows']} row(s)")

        # A closing count, because a number you can see is worth more than a
        # promise that it worked.
        with db.session() as session:
            totals = session.run(
                "MATCH (p:PriceSnapshot) "
                "RETURN count(p) AS rows, count(DISTINCT p.snapshot_date) AS days"
            ).single()
            pending = session.run(
                "MATCH (e:EntityProposal {status: 'pending'}) RETURN count(e) AS n"
            ).single()["n"]
        print(f"The library now holds {totals['rows']} price row(s) covering "
              f"{totals['days']} day(s), and {pending} model(s) are waiting for "
              "Nir to approve them as real entities.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
