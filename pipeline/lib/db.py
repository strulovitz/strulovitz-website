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
    # notifications_disabled_classifications: the database helpfully warns
    # "that label does not exist yet" the first time any query mentions
    # something not yet created, which is normal on a young database and
    # produces a screenful of frightening-looking noise. Only that ONE
    # category (UNRECOGNIZED) is silenced. Real warnings - deprecations,
    # performance problems, wrong Cypher - still come through loudly, because
    # hiding those is how projects rot.
    driver = GraphDatabase.driver(
        uri, auth=(user, password),
        notifications_disabled_classifications=["UNRECOGNIZED"],
    )
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

    # --- The weekly price and specification archive (bible/part-02.md 2.8,
    # part-09.md 9.4). One row is one model's price on one day at one provider,
    # and that combination may exist only once, forever. This constraint is
    # what makes re-running the loader harmless: a second attempt to write the
    # same Tuesday updates nothing and duplicates nothing.
    "CREATE CONSTRAINT price_snapshot_key IF NOT EXISTS "
    "FOR (p:PriceSnapshot) REQUIRE (p.snapshot_date, p.provider, "
    "p.openrouter_model_id) IS UNIQUE",
    # Almost every question asked of this archive is "what did things cost on
    # this date" or "how did this one model's price move", so both get indexes.
    "CREATE INDEX price_snapshot_date_index IF NOT EXISTS "
    "FOR (p:PriceSnapshot) ON (p.snapshot_date)",
    "CREATE INDEX price_snapshot_model_index IF NOT EXISTS "
    "FOR (p:PriceSnapshot) ON (p.openrouter_model_id)",

    # --- Proposed entities, which are NOT yet entities (bible/part-02.md 2.4).
    # The Bible is emphatic: "Unresolved mentions never silently create
    # entities; near-duplicate entities are the disease that killed many
    # knowledge bases, and the registry is the cure." So a model noticed in a
    # price list waits here as a PROPOSAL until Nir approves it with one tap in
    # Telegram. This is a waiting room, not an archive: it may be updated.
    "CREATE CONSTRAINT entity_proposal_key IF NOT EXISTS "
    "FOR (e:EntityProposal) REQUIRE e.proposed_entity_id IS UNIQUE",
    "CREATE INDEX entity_proposal_status_index IF NOT EXISTS "
    "FOR (e:EntityProposal) ON (e.status)",

    # --- The weekly record of what people actually USE. One row is one model's
    # traffic on one day at one broker. Nir's insight, 2026-08-21: usage settles
    # in one number what no amount of clever version-numbering rules could.
    "CREATE CONSTRAINT usage_snapshot_key IF NOT EXISTS "
    "FOR (u:UsageSnapshot) REQUIRE (u.usage_date, u.provider, "
    "u.model_permaslug) IS UNIQUE",
    "CREATE INDEX usage_snapshot_date_index IF NOT EXISTS "
    "FOR (u:UsageSnapshot) ON (u.usage_date)",
    "CREATE INDEX usage_snapshot_model_index IF NOT EXISTS "
    "FOR (u:UsageSnapshot) ON (u.model_id_plain)",
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


# ==============================================================================
# THE KNOWLEDGE ITSELF: STORIES, SOURCES, AND EDITIONS
# ==============================================================================
#
# WHY THIS SECTION EXISTS (bible/part-00.md LAW 5, bible/part-01.md 1.4 and 1.5)
# LAW 5 says Neo4j is "the single permanent source of truth for all knowledge
# (articles, claims, entities, tags, editions, benchmarks, snapshots)", and
# Part 01's iron rule 3 says "Every stage reads and writes THROUGH Neo4j; files
# on disk are caches and exports, never truth." Until 2026-09-03 this section
# did not exist: the editions machine stored everything in files and the
# database only kept the bookkeeping. Nir caught this violation and ordered
# the Bible followed exactly. So the knowledge now lives HERE, and the files
# under content/stories/ are what the Bible always said they should be:
# exports and caches, regenerated from this truth.
#
# WHAT IS STORED (bible/part-02.md, applied to what exists today)
# The full Part 02 model includes claims, entity registries, canon lifecycles
# and typed claim edges - the machinery of Milestones 2-3, not yet built. What
# the magazine HAS today is stored completely and honestly:
#   Story     one news item (Part 02's event node: evt-...). Carries both the
#             two clocks Part 02 2.1.2 demands: when it happened in the world
#             (published_min, from its sources) and when we learned it
#             (created_at_utc).
#   Source    one fetched document (Part 02 2.2). The frozen text itself stays
#             on disk, exactly as the Bible wants: "raw_text_path (kitchen disk
#             cache)" - the evidence bundle, with its fingerprint recorded here.
#   Edition   one model's complete rendering of one story (Part 02 2.9): the
#             headline, TLDR, article, image prompt, cost, tokens, latency -
#             plus everything else the rendering recorded.
#   Tag       the shared tag vocabulary. Each edition CHOSE its own tags
#             (DECISIONS.md decision 20), and those choices are edges, so
#             "which models tagged this story 'open-weights'" is one query.
#   Concept   an encyclopedia entry one edition wrote (term, slug,
#             explanation). Keyed per edition, but indexed by slug so all
#             eight editions' takes on the same idea are comparable - the whole
#             point of the magazine.
#   KeyPoint  a bullet an edition extracted, with the source URL it points at -
#             the honest ancestor of Part 02's claims, which arrive with
#             Milestones 2-3.
#   ImageJob  the local render of an edition's illustration (model, seed,
#             steps, seconds) - image prompts are edition truth, image FILES
#             are artifacts (Part 12: "we back up truth, not artifacts").
#
# HOW WRITES HAPPEN (LAW 12)
# Everything below is MERGE-based and idempotent: running the loader twice
# stores the same knowledge twice ZERO times. Re-running after a re-parse
# UPDATES current state (SET over the same stable id) and replaces that
# edition's tag/concept/keypoint edges, because the database holds what is
# true NOW; the LEDGER, append-only, holds what HAPPENED - that division is
# the whole design of Part 12.

# --- The rules (constraints first, then the indexes the questions need) ---
KNOWLEDGE_SCHEMA_STATEMENTS: tuple[str, ...] = (
    "CREATE CONSTRAINT story_id_unique IF NOT EXISTS "
    "FOR (s:Story) REQUIRE s.story_id IS UNIQUE",
    "CREATE INDEX story_created_index IF NOT EXISTS "
    "FOR (s:Story) ON (s.created_at_utc)",
    "CREATE CONSTRAINT source_id_unique IF NOT EXISTS "
    "FOR (s:Source) REQUIRE s.source_id IS UNIQUE",
    "CREATE INDEX source_url_index IF NOT EXISTS "
    "FOR (s:Source) ON (s.url)",
    "CREATE CONSTRAINT edition_id_unique IF NOT EXISTS "
    "FOR (e:Edition) REQUIRE e.edition_id IS UNIQUE",
    "CREATE INDEX edition_model_index IF NOT EXISTS "
    "FOR (e:Edition) ON (e.model_slug)",
    "CREATE INDEX edition_story_index IF NOT EXISTS "
    "FOR (e:Edition) ON (e.story_slug)",
    "CREATE CONSTRAINT tag_slug_unique IF NOT EXISTS "
    "FOR (t:Tag) REQUIRE t.slug IS UNIQUE",
    "CREATE CONSTRAINT concept_key_unique IF NOT EXISTS "
    "FOR (c:Concept) REQUIRE c.key IS UNIQUE",
    "CREATE INDEX concept_slug_index IF NOT EXISTS "
    "FOR (c:Concept) ON (c.slug)",
    "CREATE CONSTRAINT keypoint_key_unique IF NOT EXISTS "
    "FOR (k:KeyPoint) REQUIRE k.key IS UNIQUE",
    "CREATE CONSTRAINT imagejob_key_unique IF NOT EXISTS "
    "FOR (i:ImageJob) REQUIRE i.key IS UNIQUE",
)

# --- The ids, shaped the way Part 02 2.1.1 taught: readable, never reused ---


def story_id(slug: str) -> str:
    return f"evt-{slug}"


def source_id(fingerprint: str) -> str:
    return f"src-{fingerprint[:12]}"


def edition_id(story_slug: str, model_slug: str) -> str:
    return f"edn-{story_slug}--{model_slug}"


def ensure_knowledge_schema(driver: Driver) -> list[str]:
    """Make sure the knowledge rules exist. Safe to run any number of times."""
    applied: list[str] = []
    with driver.session() as session:
        for statement in KNOWLEDGE_SCHEMA_STATEMENTS:
            session.run(statement)
            applied.append(statement.split(" IF NOT EXISTS")[0])
    return applied


def _edition_properties(story: dict, rendering: dict) -> dict[str, Any]:
    """The flat, Neo4j-native properties of one edition (its own words)."""
    produced = rendering.get("produced") or {}
    return {
        "edition_id": edition_id(story["slug"], rendering["model_slug"]),
        "story_slug": story["slug"],
        "story_title": story.get("title", ""),
        "model_id": rendering.get("model_id", ""),
        "model_slug": rendering.get("model_slug", ""),
        "model_served": rendering.get("model_served", ""),
        "company": rendering.get("company", ""),
        "short_name": rendering.get("short_name", ""),
        "rendered_at_utc": rendering.get("rendered_at_utc", ""),
        "reparsed_at_utc": rendering.get("reparsed_at_utc", ""),
        "brief_version": rendering.get("brief_version", ""),
        "asked_with_strict_schema": bool(rendering.get("asked_with_strict_schema")),
        "bought_in_batch": bool(rendering.get("bought_in_batch")),
        "understood": bool(rendering.get("understood")),
        "cost_usd": float(rendering.get("cost_usd") or 0.0),
        "prompt_tokens": int(rendering.get("prompt_tokens") or 0),
        "completion_tokens": int(rendering.get("completion_tokens") or 0),
        "reasoning_tokens": int(rendering.get("reasoning_tokens") or 0),
        "seconds_waited": float(rendering.get("seconds_waited") or 0.0),
        "generation_id": rendering.get("generation_id", ""),
        "image_prompt_asked_separately": bool(rendering.get("image_prompt_asked_separately")),
        "image_prompt_second_chance": bool(rendering.get("image_prompt_second_chance")),
        "image_prompt_cost_usd": float(rendering.get("image_prompt_cost_usd") or 0.0),
        # The produced content itself - prose and choices, stored as truth.
        "headline": produced.get("headline", ""),
        "tldr": produced.get("tldr", ""),
        "article": produced.get("article", ""),
        "image_prompt": produced.get("image_prompt", ""),
    }


def upsert_story(driver: Driver, story: dict) -> str:
    """
    Store one Story (the news item itself) and its frozen Sources.

    The Story's own two clocks (Part 02 2.1.2): published_min is when the
    thing happened in the world (earliest source publication date), and
    created_at_utc is when we recorded it. Corrections and re-runs update
    knowledge time, never event time.
    """
    published_min = min(
        (s.get("published", "") for s in story.get("sources", []) if s.get("published")),
        default=str(story.get("created_at_utc", ""))[:10],
    )
    with driver.session() as session:
        session.run(
            "MERGE (s:Story {story_id: $story_id}) "
            "SET s.slug = $slug, s.title = $title, s.created_at_utc = $created, "
            "    s.language = $language, s.published_min = $published_min, "
            "    s.source_count = $source_count, s.total_words = $total_words",
            story_id=story_id(story["slug"]), slug=story["slug"],
            title=story.get("title", ""), created=str(story.get("created_at_utc", "")),
            language=story.get("language", ""), published_min=published_min,
            source_count=int(story.get("source_count") or len(story.get("sources", []))),
            total_words=int(story.get("total_words") or 0),
        )
        for source in story.get("sources", []):
            session.run(
                "MERGE (src:Source {source_id: $source_id}) "
                "SET src.url = $url, src.kind = $kind, src.title = $title, "
                "    src.byline = $byline, src.published = $published, "
                "    src.fetched_at_utc = $fetched, src.site = $site, "
                "    src.words = $words, src.note = $note, src.text_file = $text_file, "
                "    src.fingerprint = $fingerprint "
                "WITH src "
                "MATCH (s:Story {story_id: $story_id}) "
                "MERGE (s)-[:HAS_SOURCE]->(src)",
                source_id=source_id(source.get("fingerprint", "")),
                url=source.get("url", ""), kind=source.get("kind", ""),
                title=source.get("title", ""), byline=source.get("byline", ""),
                published=source.get("published", ""),
                fetched=source.get("fetched_at_utc", ""), site=source.get("site", ""),
                words=int(source.get("words") or 0), note=source.get("note", ""),
                text_file=source.get("text_file", ""),
                fingerprint=source.get("fingerprint", ""),
                story_id=story_id(story["slug"]),
            )
    return story_id(story["slug"])


def upsert_edition(driver: Driver, story: dict, rendering: dict,
                   image_meta: dict[str, Any] | None = None) -> str:
    """
    Store one model's edition of one story, complete: the prose it wrote, the
    tags it chose, the encyclopedia entries it wrote, the bullets it
    extracted with the sources they point at, the stories it told readers to
    read next, and (if it exists) the local render of its illustration.

    Idempotent (LAW 12): a re-run sets the same stable edition_id and replaces
    that edition's own edges, so a re-parsed edition updates truth without
    ever duplicating it or touching any other edition's choices.
    """
    if not rendering.get("produced"):
        # An edition that produced nothing is still a fact (a result, per
        # DECISIONS.md 16), but it carries no content edges at all.
        return ""
    produced = rendering["produced"]
    eid = edition_id(story["slug"], rendering["model_slug"])
    properties = _edition_properties(story, rendering)

    with driver.session() as session:
        # The edition node itself, and its place under the story.
        session.run(
            "MERGE (e:Edition {edition_id: $eid}) SET e = $props "
            "WITH e MATCH (s:Story {story_id: $story_id}) "
            "MERGE (s)-[:HAS_EDITION]->(e)",
            eid=eid, props=properties, story_id=story_id(story["slug"]),
        )
        # This edition's own edges are replaced on every store, because the
        # database holds what is true NOW. No other edition is touched.
        session.run(
            "MATCH (e:Edition {edition_id: $eid})-[r:CHOSE_TAG|WROTE_CONCEPT|"
            "HIGHLIGHTED|POINTS_TO|RENDERED_IMAGE]->() DELETE r",
            eid=eid,
        )
        # The tags it chose (decision 20: each model chose its own), in the
        # ORDER it chose them - the order is part of the model's editorial
        # voice, so it is stored ON the edge and read back by it. Never
        # alphabetize a model's choices: that quietly rewrites its work.
        for position, tag in enumerate(produced.get("tags") or []):
            slug = str(tag).strip().lower()
            if slug:
                session.run(
                    "MERGE (t:Tag {slug: $slug}) "
                    "WITH t MATCH (e:Edition {edition_id: $eid}) "
                    "MERGE (e)-[:CHOSE_TAG {position: $position}]->(t)",
                    slug=slug, eid=eid, position=position,
                )
        # The encyclopedia entries it wrote. Keyed per edition, indexed by
        # slug so the eight takes on the same idea are one query apart. The
        # order the model listed them in is stored on the edge, the same as
        # tags: order is editorial voice.
        for position, concept in enumerate(produced.get("concepts") or []):
            slug = str(concept.get("slug") or "").strip().lower()
            if not slug:
                continue
            session.run(
                "MERGE (c:Concept {key: $key}) "
                "SET c.slug = $slug, c.term = $term, c.explanation = $explanation, "
                "    c.edition_id = $eid "
                "WITH c MATCH (e:Edition {edition_id: $eid}) "
                "MERGE (e)-[:WROTE_CONCEPT {position: $position}]->(c)",
                key=f"{eid}:{slug}", slug=slug,
                term=concept.get("term", slug),
                explanation=concept.get("explanation", ""), eid=eid, position=position,
            )
        # The bullets it extracted, each pointing at its source - the honest
        # ancestor of Part 02's claims (which arrive with the claim pipeline).
        # Order preserved on the edge, as always.
        for position, point in enumerate(produced.get("key_points") or []):
            text = str(point.get("point") or "").strip()
            if not text:
                continue
            key = hashlib.sha256(f"{eid}:{text}".encode("utf-8")).hexdigest()[:24]
            session.run(
                "MERGE (k:KeyPoint {key: $key}) "
                "SET k.text = $text, k.source_url = $source_url, k.edition_id = $eid "
                "WITH k MATCH (e:Edition {edition_id: $eid}) "
                "MERGE (e)-[:HIGHLIGHTED {position: $position}]->(k) "
                "WITH k MATCH (src:Source {url: $source_url}) "
                "MERGE (k)-[:FROM_SOURCE]->(src)",
                key=key, text=text, source_url=point.get("source_url", ""),
                eid=eid, position=position,
            )
        # The "read this next" links: this editor's strongest opinion about
        # how knowledge fits together (they are what the galaxy edges draw).
        # Order preserved, like every other choice this model made.
        for position, other in enumerate(produced.get("related") or []):
            other_slug = str(other).strip()
            if other_slug:
                session.run(
                    "MATCH (e:Edition {edition_id: $eid}) "
                    "MATCH (s:Story {story_id: $story_id}) "
                    "MERGE (e)-[:POINTS_TO {position: $position}]->(s)",
                    eid=eid, story_id=story_id(other_slug), position=position,
                )
        # The local image render, if the illustration stage has made one.
        # Image files are artifacts; the JOB (model, seed, timing) is truth.
        if image_meta:
            session.run(
                "MERGE (i:ImageJob {key: $eid}) "
                "SET i = $meta, i.key = $eid "
                "WITH i MATCH (e:Edition {edition_id: $eid}) "
                "MERGE (e)-[:RENDERED_IMAGE]->(i)",
                eid=eid, meta={k: v for k, v in image_meta.items() if k != "prompt"},
            )
    return eid


def read_editions_for_model(driver: Driver, model_slug: str) -> list[dict[str, Any]]:
    """
    Every edition one model produced, in story order, shaped EXACTLY like the
    file-based reader it replaced (stages/layout.py read_editions), so that
    switching the pipeline to the database could be verified by rebuilding
    the galaxies and comparing them byte for byte. Part 01 1.5 iron rule 3:
    every stage reads through Neo4j - this is how layout.py reads now.

    Returns one dict per edition: the rendering's own fields (cost, tokens,
    produced prose and choices...) plus the story context (title, published,
    sources) the galaxy builder needs.
    """
    with driver.session() as session:
        records = session.run(
            "MATCH (e:Edition {model_slug: $model_slug}) "
            "MATCH (s:Story)-[:HAS_EDITION]->(e) "
            "OPTIONAL MATCH (s)-[:HAS_SOURCE]->(src:Source) "
            "RETURN e, s, collect(distinct src) AS sources "
            "ORDER BY s.slug",
            model_slug=model_slug,
        ).data()
    editions: list[dict[str, Any]] = []
    for row in records:
        edition = dict(row["e"])
        story = row["s"]
        sources = [
            {"url": src.get("url", ""), "title": src.get("title", ""),
             "byline": src.get("byline", ""), "site": src.get("site", ""),
             "kind": src.get("kind", ""), "published": src.get("published", "")}
            for src in row["sources"]
        ]
        # Reassemble the exact shape the galaxy builder consumes, so nothing
        # downstream ever learns that its data source changed.
        edition["story"] = story["slug"]
        edition["story_title"] = story.get("title", "")
        edition["story_published"] = story.get("published_min", "")
        edition["story_sources"] = sources
        edition["produced"] = {
            "headline": edition.pop("headline", ""),
            "tldr": edition.pop("tldr", ""),
            "article": edition.pop("article", ""),
            "image_prompt": edition.pop("image_prompt", ""),
        }
        with driver.session() as session:
            # Every list comes back in the ORDER the model chose it (the
            # position stored on the edge at write time) - a model's chosen
            # order is part of its work, never to be alphabetized away.
            tags = session.run(
                "MATCH (:Edition {edition_id: $eid})-[r:CHOSE_TAG]->(t:Tag) "
                "RETURN t.slug AS slug ORDER BY r.position", eid=row["e"]["edition_id"],
            ).data()
            concepts = session.run(
                "MATCH (:Edition {edition_id: $eid})-[r:WROTE_CONCEPT]->(c:Concept) "
                "RETURN c.term AS term, c.slug AS slug, c.explanation AS explanation "
                "ORDER BY r.position", eid=row["e"]["edition_id"],
            ).data()
            key_points = session.run(
                "MATCH (:Edition {edition_id: $eid})-[r:HIGHLIGHTED]->(k:KeyPoint) "
                "RETURN k.text AS point, k.source_url AS source_url "
                "ORDER BY r.position", eid=row["e"]["edition_id"],
            ).data()
            related = session.run(
                "MATCH (:Edition {edition_id: $eid})-[r:POINTS_TO]->(s:Story) "
                "RETURN s.slug AS slug ORDER BY r.position", eid=row["e"]["edition_id"],
            ).data()
        edition["produced"]["tags"] = [t["slug"] for t in tags]
        edition["produced"]["concepts"] = concepts
        edition["produced"]["key_points"] = key_points
        edition["produced"]["related"] = [r["slug"] for r in related]
        editions.append(edition)
    return editions


def read_story(driver: Driver, slug: str) -> dict[str, Any] | None:
    """
    One story with its frozen sources, shaped EXACTLY like the story.json it
    replaced (render_edition.py's question builder consumes this). Returns
    None when no such story exists - the caller decides whether that is an
    error (the same honest behaviour the file reader had: a missing story
    raised "Run stages/make_story.py first").
    """
    with driver.session() as session:
        record = session.run(
            "MATCH (s:Story {slug: $slug}) "
            "OPTIONAL MATCH (s)-[:HAS_SOURCE]->(src:Source) "
            "RETURN s, collect(src) AS sources",
            slug=slug,
        ).single()
    if not record:
        return None
    story = dict(record["s"])
    story["slug"] = slug
    story["sources"] = [
        {k: src.get(k, "") for k in
         ("kind", "url", "title", "byline", "published", "fingerprint",
          "fetched_at_utc", "site", "words", "note", "text_file")}
        for src in record["sources"]
    ]
    return story


def knowledge_counts(driver: Driver) -> dict[str, int]:
    """
    The honest census, for the ledger and for Nir: how much knowledge the
    database actually holds. The pre-upload validator of Part 12 12.3.2 will
    one day compare an export's counts against these - that is when the
    "counts match Neo4j" rule gets its teeth.
    """
    queries = {
        "stories": "MATCH (:Story) RETURN count(*) AS n",
        "sources": "MATCH (:Source) RETURN count(*) AS n",
        "editions": "MATCH (:Edition) RETURN count(*) AS n",
        "tags": "MATCH (:Tag) RETURN count(*) AS n",
        "concepts": "MATCH (:Concept) RETURN count(*) AS n",
        "key_points": "MATCH (:KeyPoint) RETURN count(*) AS n",
        "image_jobs": "MATCH (:ImageJob) RETURN count(*) AS n",
        "read_next_links": "MATCH ()-[:POINTS_TO]->() RETURN count(*) AS n",
    }
    counts: dict[str, int] = {}
    with driver.session() as session:
        for name, query in queries.items():
            record = session.run(query).single()
            counts[name] = record["n"] if record else 0
    return counts


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
