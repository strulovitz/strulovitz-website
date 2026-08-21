#!/usr/bin/env python3
"""
THE ONE DOOR TO THE DATABASE
============================

WHAT THIS IS, IN ONE SENTENCE
The single file in the whole project that is allowed to talk to Neo4j, plus the
job ledger: the flight recorder that writes down everything the machines do, in
words Nir can read.

WHY IT IS THE ONLY DOOR (bible/part-01.md 1.4, access discipline)
The Bible forbids scattering database code across the project. Everything goes
through here, so that when the shape of the data changes there is exactly one
file to change, and so a fresh agent five years from now has one place to read
instead of forty.

WHAT LIVES HERE
1. connect()      - opens the database, using the details in .env only.
2. ensure_schema() - creates the few rules the database needs. Safe to re-run.
3. log_job()      - appends one entry to the job ledger. The ONLY way to write
                    to the ledger.
4. read_jobs()    - reads recent ledger entries back out.
5. health()       - a short honest answer to "is the database well?".

THE LEDGER, AND WHY plain_words IS NOT OPTIONAL (bible/part-12.md 12.1)
Every significant action - an install, a pipeline stage, a config change, an
approval from Nir - becomes one immutable ledger entry. Each entry must carry a
one-sentence explanation, in ordinary language, of what happened. The Bible is
blunt about it: an entry whose plain_words a non-coder cannot understand is a
DEFECTIVE entry. This file therefore refuses to write an entry without one, and
refuses obvious cheating like "ran the job" or a wall of jargon.

APPEND-ONLY, ON PURPOSE (LAW 12)
There is deliberately no function here that edits or deletes a ledger entry. A
mistake is corrected by writing a NEW entry that names the job_id it corrects.
The flight recorder records; it does not negotiate.

HOW TO USE IT
    from lib.db import connect, ensure_schema, log_job
    with connect() as db:
        ensure_schema(db)
        log_job(db, action_type="install", actor="claude-opus-5",
                verdict="ok",
                plain_words="Installed the database on the desktop.")

HOW TO CHECK IT BY HAND
    cd /home/nir/strulovitz-website/pipeline && uv run lib/db.py
That prints the health of the database and the last few ledger entries. It
writes nothing.
"""

from __future__ import annotations

import hashlib
import json
import os
import socket
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from neo4j import Driver, GraphDatabase

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = REPO_ROOT / ".env"

# The version stamp written onto every ledger entry. Bump it only when the
# SHAPE of an entry changes, and never rewrite old entries to match: old rows
# keep their old version, which is how we stay able to read our own history
# (bible/part-00.md LAW 12, part-02.md schema versioning).
LEDGER_SCHEMA_VERSION = 1

# The machine this code is running on, named after what it plainly is
# (DECISIONS.md decision 7: the names "Atlas" and "Forge" are abolished).
# Anything unrecognised is recorded honestly as "unknown" rather than guessed.
# NOTE: ledger entries written on 2026-08-21 before that decision say "atlas".
# They are left exactly as they are, because the ledger is append-only and
# history is never rewritten (LAW 12). "atlas" and "desktop-linux" are the
# same computer.
MACHINE_NAMES = {
    "mint-desktop": "desktop-linux",
}

# Action types seen so far. This is a helpful list, not a fence: a new kind of
# work may invent a new word, and the ledger will accept it. It exists so that
# agents reuse the same words instead of inventing ten spellings of "install".
KNOWN_ACTION_TYPES = (
    "install",          # software put onto a machine
    "config_change",    # a setting changed on a machine
    "schema_change",    # the shape of the database changed
    "stage_run",        # one pipeline stage ran
    "snapshot",         # a price or benchmark snapshot was taken
    "export",           # an export folder was built for uploading
    "deploy",           # Nir uploaded an export to the server
    "backup",           # a database dump was taken
    "restore_test",     # a dump was proven to restore
    "layout_epoch",     # a new frozen layout was computed
    "edition_run",      # one model produced an edition
    "approval",         # Nir approved something over Telegram
    "incident",         # something went wrong and was dealt with
    "correction",       # an earlier ledger entry is being corrected
    "note",             # a plain observation worth remembering
)

# Wording that is not a real explanation. The ledger rejects these, because a
# ledger full of "done" teaches a future reader nothing (bible/part-12.md 12.1.2).
_LAZY_PLAIN_WORDS = {
    "ok", "done", "fine", "success", "ran", "ran it", "ran the job", "n/a",
    "no comment", "as above", "see above", "-", "none", "test", "worked",
}


class DatabaseNotConfigured(RuntimeError):
    """Raised when .env has no real database details in it yet."""


class DefectiveLedgerEntry(ValueError):
    """Raised when a ledger entry would be written without a real explanation."""


# ------------------------------------------------------------------------------
# Reading the .env file. Deliberately duplicated from lib/telegram.py rather
# than shared, so that neither file can break the other, and so each stays
# readable on its own. Two ten-line functions are cheaper than one dependency.
# ------------------------------------------------------------------------------

def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def _settings() -> tuple[str, str, str]:
    """Return (uri, user, password). Real environment variables win over .env."""
    from_file = _read_env_file(ENV_FILE)

    def pick(name: str, fallback: str = "") -> str:
        return os.environ.get(name) or from_file.get(name, fallback)

    uri = pick("NEO4J_URI", "bolt://localhost:7687")
    user = pick("NEO4J_USER", "neo4j")
    password = pick("NEO4J_PASSWORD")

    if not password or "REPLACE-ME" in password:
        raise DatabaseNotConfigured(
            "No real NEO4J_PASSWORD found. It belongs in the .env file at the "
            "top of the repository, which git is forbidden to touch."
        )
    # A safety rail with teeth: the database must never be reachable from the
    # open internet (bible/part-00.md LAW 4, part-07.md 7.6.1). Only this
    # machine and the private Tailscale network are ever allowed.
    if not any(host in uri for host in ("localhost", "127.0.0.1", "100.")):
        raise DatabaseNotConfigured(
            "NEO4J_URI points somewhere that is not this computer and not the "
            "private Tailscale network. That is forbidden. Fix .env."
        )
    return uri, user, password


def this_machine() -> str:
    """The project's name for the computer this code is running on."""
    return MACHINE_NAMES.get(socket.gethostname(), "unknown")


def connect() -> Driver:
    """
    Open the database. Use it as a context manager so it always closes:

        with connect() as db:
            ...

    The password is never printed, never logged, and never included in an
    error message raised from here.
    """
    uri, user, password = _settings()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
    except Exception as problem:  # noqa: BLE001
        driver.close()
        raise RuntimeError(
            "The database did not answer. Is it running? Check with: "
            "systemctl is-active neo4j . The original complaint was: "
            f"{type(problem).__name__}"
        ) from None
    return driver


# ------------------------------------------------------------------------------
# The schema. Only rules that protect the data live here: uniqueness, so the
# same job can never be recorded twice, and indexes, so reading stays instant
# when there are years of entries.
# ------------------------------------------------------------------------------

SCHEMA_STATEMENTS: tuple[str, ...] = (
    # Every ledger entry has its own permanent identifier, and no two entries
    # may share one. This is what makes re-running a job safe (LAW 12).
    "CREATE CONSTRAINT job_id_unique IF NOT EXISTS "
    "FOR (j:JobLedgerEntry) REQUIRE j.job_id IS UNIQUE",
    # An entry without a time or an explanation is not an entry at all. We
    # WANTED the database itself to insist on that, but "property existence"
    # constraints are a paid Enterprise Edition feature, and this project runs
    # Community Edition (bible/part-01.md 1.4). So the insisting is done in
    # Python instead, by log_job below, which is the only way in anyway. This
    # comment exists so that no future agent wastes an hour rediscovering it.
    #
    # Reading the ledger is almost always "what happened lately" or "what
    # happened of this kind", so those two get indexes.
    "CREATE INDEX job_timestamp_index IF NOT EXISTS "
    "FOR (j:JobLedgerEntry) ON (j.timestamp_utc)",
    "CREATE INDEX job_action_type_index IF NOT EXISTS "
    "FOR (j:JobLedgerEntry) ON (j.action_type)",
)


def ensure_schema(driver: Driver) -> list[str]:
    """
    Make sure the database has its rules. Safe to run any number of times.

    Returns the list of statements that were applied, for the caller to record
    in the ledger if it wishes.
    """
    applied: list[str] = []
    with driver.session() as session:
        for statement in SCHEMA_STATEMENTS:
            session.run(statement)
            applied.append(statement.split(" IF NOT EXISTS")[0])
    return applied


# ------------------------------------------------------------------------------
# The job ledger.
# ------------------------------------------------------------------------------

def _check_plain_words(text: str) -> str:
    """
    Refuse an entry that does not really explain itself.

    The rules are deliberately mild, because a nagging tool gets bypassed: at
    least four words, at least twenty characters, not one of the known lazy
    phrases, and it must read like a sentence rather than a command line.
    """
    cleaned = " ".join((text or "").split())
    if not cleaned:
        raise DefectiveLedgerEntry(
            "plain_words is required: one sentence, in ordinary language, that "
            "Nir would understand. The Bible calls an entry without it defective."
        )
    if cleaned.strip(" .").lower() in _LAZY_PLAIN_WORDS:
        raise DefectiveLedgerEntry(
            f"plain_words says only {cleaned!r}. Explain what actually happened "
            "and why it mattered, in one plain sentence."
        )
    if len(cleaned) < 20 or len(cleaned.split()) < 4:
        raise DefectiveLedgerEntry(
            "plain_words is too short to be an explanation. Write one full "
            "sentence a non-coder would understand."
        )
    if "/" in cleaned and len(cleaned.split()) < 8:
        raise DefectiveLedgerEntry(
            "plain_words looks like a file path rather than a sentence. Paths "
            "belong in the outputs field; the sentence is for Nir."
        )
    return cleaned


def hash_inputs(inputs: Any) -> str:
    """
    A short fingerprint of a job's inputs, used for idempotency: if the same
    inputs were already processed successfully, a stage can skip the work
    instead of doing it twice (LAW 12).

    Anything JSON-shaped can go in. Key order does not matter.
    """
    blob = json.dumps(inputs, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:32]


def log_job(
    driver: Driver,
    *,
    action_type: str,
    plain_words: str,
    actor: str,
    verdict: str = "ok",
    machine: str | None = None,
    inputs: Any = None,
    outputs: Iterable[str] | None = None,
    cost_usd: float = 0.0,
    duration_s: float | None = None,
    corrects_job_id: str | None = None,
    extra: dict[str, Any] | None = None,
) -> str:
    """
    Append one entry to the job ledger and return its job_id.

    action_type    one of KNOWN_ACTION_TYPES, or a new word if genuinely new.
    plain_words    MANDATORY. One sentence for Nir. Checked, not merely asked for.
    actor          who did it: a model name like "claude-opus-5", "claude-sonnet-5",
                   "timer" for a scheduled job, or "nir" for a human action.
    verdict        "ok", "failed" or "partial". Honest failures are recorded,
                   never hidden; a ledger that only contains successes is a lie.
    inputs         anything JSON-shaped; stored as a fingerprint, not in full.
    outputs        identifiers or file paths this job produced.
    corrects_job_id  when this entry corrects an earlier one, name it here. The
                   old entry is never touched (LAW 12).
    extra          a few additional simple values, if a job really needs them.
    """
    if verdict not in ("ok", "failed", "partial"):
        raise ValueError("verdict must be 'ok', 'failed' or 'partial'.")

    sentence = _check_plain_words(plain_words)
    job_id = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:8]}"

    properties: dict[str, Any] = {
        "job_id": job_id,
        "schema_version": LEDGER_SCHEMA_VERSION,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "actor": actor,
        "machine": machine or this_machine(),
        "action_type": action_type,
        "verdict": verdict,
        "plain_words": sentence,
        "cost_usd": float(cost_usd),
        "inputs_hash": hash_inputs(inputs) if inputs is not None else None,
        "outputs": list(outputs) if outputs else [],
        "duration_s": duration_s,
        "corrects_job_id": corrects_job_id,
    }
    if extra:
        for key, value in extra.items():
            # Keep the ledger flat and simple: only values Neo4j stores
            # natively. Anything complicated becomes text, so nothing is lost
            # and nothing surprising is stored.
            properties[f"extra_{key}"] = (
                value if isinstance(value, (str, int, float, bool)) else json.dumps(value, default=str)
            )

    with driver.session() as session:
        session.run(
            "CREATE (j:JobLedgerEntry) SET j = $properties",
            properties=properties,
        )
        if corrects_job_id:
            # Link the correction to what it corrects, so the chain is
            # walkable later. The corrected entry itself is not modified.
            session.run(
                "MATCH (new:JobLedgerEntry {job_id: $new_id}) "
                "MATCH (old:JobLedgerEntry {job_id: $old_id}) "
                "MERGE (new)-[:CORRECTS]->(old)",
                new_id=job_id, old_id=corrects_job_id,
            )
    return job_id


def read_jobs(driver: Driver, limit: int = 10, action_type: str | None = None) -> list[dict[str, Any]]:
    """The most recent ledger entries, newest first."""
    where = "WHERE j.action_type = $action_type " if action_type else ""
    query = (
        "MATCH (j:JobLedgerEntry) " + where +
        "RETURN j ORDER BY j.timestamp_utc DESC LIMIT $limit"
    )
    with driver.session() as session:
        result = session.run(query, limit=limit, action_type=action_type)
        return [dict(record["j"]) for record in result]


def already_done(driver: Driver, action_type: str, inputs: Any) -> bool:
    """
    Has this exact work already succeeded? Used by stages to avoid doing the
    same job twice (LAW 12, idempotency).
    """
    with driver.session() as session:
        record = session.run(
            "MATCH (j:JobLedgerEntry {action_type: $action_type, "
            "inputs_hash: $inputs_hash, verdict: 'ok'}) RETURN count(j) AS n",
            action_type=action_type, inputs_hash=hash_inputs(inputs),
        ).single()
    return bool(record and record["n"] > 0)


def health(driver: Driver) -> dict[str, Any]:
    """A short, honest description of the database, for the daily heartbeat."""
    with driver.session() as session:
        counts = session.run(
            "MATCH (n) RETURN count(n) AS nodes"
        ).single()
        ledger = session.run(
            "MATCH (j:JobLedgerEntry) RETURN count(j) AS entries, "
            "max(j.timestamp_utc) AS newest"
        ).single()
    return {
        "nodes": counts["nodes"] if counts else 0,
        "ledger_entries": ledger["entries"] if ledger else 0,
        "ledger_newest": ledger["newest"] if ledger else None,
    }


if __name__ == "__main__":
    # Running this file directly only LOOKS. It writes nothing, so it is safe
    # to run at any time, including while a pipeline stage is working.
    with connect() as db:
        state = health(db)
        print(f"Database answered. It holds {state['nodes']} things in total, "
              f"of which {state['ledger_entries']} are ledger entries.")
        if state["ledger_newest"]:
            print(f"Newest ledger entry: {state['ledger_newest']}")
        for entry in read_jobs(db, limit=8):
            print(f"  {entry['timestamp_utc']}  {entry['action_type']:<14} "
                  f"{entry['verdict']:<7} {entry['plain_words']}")
