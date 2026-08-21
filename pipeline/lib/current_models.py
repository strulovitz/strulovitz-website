#!/usr/bin/env python3
"""
WHAT COUNTS AS A CURRENT MODEL
==============================

WHAT THIS IS, IN ONE SENTENCE
The filter that turns a seller's catalogue of 419 listings into the much shorter
list of models a reader could sensibly use today.

WHY IT HAS TO EXIST (the honest version)
There is no such thing as a clean, up-to-date source. The source we read IS
live and up to date - it is the seller's own catalogue, fetched minutes ago -
but a seller lists everything it still SELLS, which includes museum pieces from
2024, the same model twice at a batch discount, and "routers" that are not
models at all. Asking that catalogue for "the most expensive model" gives you a
three-year-old research preview at 600 dollars, which is true and useless.

So the cleaning happens here, in one place, in code. Not in prose, not in a
rule somebody has to remember: any question the magazine asks about "models
today" goes through this file.

WHAT GETS EXCLUDED, AND HOW WE KNOW
1. ROUTERS AND META-ENTRIES. The seller's id begins with its own name, for
   example openrouter/auto . These forward your request to whatever model they
   pick, so their advertised two-million-token context belongs to nothing you
   can point at. They are a real thing worth writing about one day, but they
   are not competitors in a model comparison.
2. ALIASES. An id beginning with ~ , for example ~anthropic/claude-fable-latest ,
   is a moving pointer to whichever model is newest. Counting it alongside the
   model it points at double-counts one thing.
3. BATCH VARIANTS. An id ending in :batch is the same model at half price for
   work you are willing to wait for. That is a second price for one model, not
   a second model.
4. SUPERSEDED MEMBERS OF A FAMILY. Grok 4.20 is still on sale beside Grok 4.6,
   and still advertises a bigger context than its successor. Only the newest
   member of each family is current. Families are worked out by removing the
   version numbers from the id, so x-ai/grok-4.6 and x-ai/grok-4.20 are the
   same family, while x-ai/grok-4.20-multi-agent is its own.
5. STALE LISTINGS. Anything the seller first listed more than STALE_AFTER_DAYS
   ago and never refreshed is history, not news.

EVERY EXCLUDED ROW IS KEPT IN THE ARCHIVE FOREVER. Nothing here deletes
anything. The old prices are exactly what makes "this got thirty percent
cheaper per quarter" sayable, which is the one thing this project has that
nobody else does. Filtering happens when a question is asked, never when data
is stored.

EVERY ANSWER CARRIES ITS OWN EXCLUSIONS. describe_exclusions() returns the
plain sentence that must be printed beside any figure taken from this filter,
because a number without its exclusions is not honest.

HOW TO SEE IT WORK
    cd /home/nir/strulovitz-website/pipeline && uv run lib/current_models.py
"""

from __future__ import annotations

import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PIPELINE_DIR = Path(__file__).resolve().parents[1]
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

# A listing first published longer ago than this, whose family has no newer
# member, is treated as history rather than as a current option. Eighteen months
# is deliberately generous: some genuinely current models are old and unchanged.
STALE_AFTER_DAYS = 550

# A listing that is still the newest of its own family, but was published this
# many days before its developer's newest model, is flagged for one human look.
# It is NOT excluded: the flag asks Nir a question, it does not answer it.
REVIEW_IF_DAYS_BEHIND_DEVELOPER = 120

# Any token containing a digit is treated as a version marker and removed when
# working out which family a listing belongs to. That turns grok-4.6 and
# grok-4.20 into "grok", kimi-k3 and kimi-k2.6 into "kimi", and
# deepseek-v4-flash-0731 into "deepseek-flash".
_HAS_DIGIT = re.compile(r"\d")


def family_key(model_id: str) -> str:
    """
    The family a listing belongs to: everything about its name except its
    version. Used to decide which member of a family is the current one.
    """
    cleaned = model_id.lstrip("~").split(":", 1)[0]
    developer, _, name = cleaned.partition("/")
    tokens = [t for t in name.split("-") if not _HAS_DIGIT.search(t)]
    return f"{developer}/" + "-".join(tokens)


def version_of(model_id: str) -> tuple[float, ...]:
    """
    A comparable version number pulled out of the id, so that 4.6 beats 4.20
    and 4.20 beats 4.3. Returns an empty tuple when the id carries no version,
    which sorts below everything.
    """
    cleaned = model_id.lstrip("~").split(":", 1)[0]
    numbers = re.findall(r"\d+(?:\.\d+)*", cleaned)
    if not numbers:
        return ()
    # The FIRST version-looking number is the generation. Later numbers are
    # usually dates (0731) or sizes (26B) and would mislead a comparison.
    parts = numbers[0].split(".")
    return tuple(float(p) for p in parts)


def _age_days(created_unix: int | float | None, today: date | None = None) -> float | None:
    if not created_unix:
        return None
    listed = datetime.fromtimestamp(float(created_unix), tz=timezone.utc).date()
    return ((today or date.today()) - listed).days


def classify(rows: Iterable[dict[str, Any]], today: date | None = None) -> list[dict[str, Any]]:
    """
    Look at every row of one day's catalogue and attach an honest verdict.

    Each returned row is the original row plus two new keys:
      kind    - "model", "router", "alias" or "batch_variant"
      status  - "current", "superseded", "stale", or "not_a_model"
    Nothing is removed and nothing is changed. This function only labels.
    """
    rows = list(rows)

    # First pass: what kind of thing is each listing?
    for row in rows:
        model_id = row.get("openrouter_model_id") or ""
        seller = row.get("provider") or "openrouter"
        if model_id.startswith("~"):
            row["kind"] = "alias"
        elif model_id.endswith(":batch"):
            row["kind"] = "batch_variant"
        elif model_id.startswith(f"{seller}/"):
            # The seller selling something under its own name is a router or a
            # house product, not a third-party model.
            row["kind"] = "router"
        else:
            row["kind"] = "model"

    # Second pass: within each family of real models, who is the newest?
    # WHICH IS NEWER IS DECIDED BY THE LISTING DATE, NOT THE VERSION NUMBER.
    # This matters: as a number, "4.20" looks bigger than "4.6", so version
    # sorting declares Grok 4.20 the newest Grok, which is wrong - it was
    # listed in March and 4.6 arrived in August. Version numbers are marketing
    # and follow no arithmetic; the date the seller listed it is a fact. The
    # version is kept only as a tie-breaker for listings published the same day.
    newest_of_family: dict[str, tuple[float, tuple[float, ...]]] = {}
    for row in rows:
        if row["kind"] != "model":
            continue
        key = family_key(row.get("openrouter_model_id") or "")
        rank = (float(row.get("openrouter_created_unix") or 0),
                version_of(row.get("openrouter_model_id") or ""))
        if key not in newest_of_family or rank > newest_of_family[key]:
            newest_of_family[key] = rank

    # Third pass: the verdict.
    for row in rows:
        if row["kind"] != "model":
            row["status"] = "not_a_model"
            continue
        model_id = row.get("openrouter_model_id") or ""
        key = family_key(model_id)
        rank = (float(row.get("openrouter_created_unix") or 0),
                version_of(model_id))
        if rank != newest_of_family[key]:
            row["status"] = "superseded"
            continue
        age = _age_days(row.get("openrouter_created_unix"), today)
        row["status"] = "stale" if age is not None and age > STALE_AFTER_DAYS else "current"

    # Fourth pass: what the code REFUSES to decide by itself.
    #
    # Some listings are the newest member of their own little family and so
    # count as current, yet they are plainly an old sibling of something newer:
    # "Grok 4.20 Multi-Agent" has no successor of its own, but ordinary Grok has
    # moved on four months since. Deciding whether such a thing still belongs in
    # a comparison is an editorial judgement about product families, and the
    # Bible says that judgement is Nir's, made once, through the entity registry
    # (part-02.md 2.4). It is NOT a rule a script should guess, and every
    # automatic rule tried here was wrong for something: judging by how far
    # behind the developer's newest listing it is would have thrown out Claude
    # Haiku, which is genuinely the current Haiku and simply old.
    #
    # So these get flagged for one human look, and are still counted as current
    # until Nir says otherwise. A flag asking a question is honest; a rule
    # guessing an answer is not.
    newest_by_developer: dict[str, float] = {}
    for row in rows:
        if row["kind"] != "model":
            continue
        developer = (row.get("openrouter_model_id") or "").split("/")[0]
        newest_by_developer[developer] = max(
            newest_by_developer.get(developer, 0.0),
            float(row.get("openrouter_created_unix") or 0),
        )
    for row in rows:
        row["review_note"] = None
        if row.get("status") != "current":
            continue
        developer = (row.get("openrouter_model_id") or "").split("/")[0]
        listed = float(row.get("openrouter_created_unix") or 0)
        days_behind = (newest_by_developer.get(developer, listed) - listed) / 86400
        if days_behind > REVIEW_IF_DAYS_BEHIND_DEVELOPER:
            row["review_note"] = (
                f"listed {int(days_behind)} days before this developer's newest "
                "model; may be an old sibling rather than a current option"
            )

    return rows


def current_only(rows: Iterable[dict[str, Any]], today: date | None = None) -> list[dict[str, Any]]:
    """The rows a reader could sensibly use today, and nothing else."""
    return [r for r in classify(rows, today) if r.get("status") == "current"]


def describe_exclusions(rows: Iterable[dict[str, Any]], today: date | None = None) -> str:
    """
    The plain sentence that MUST be printed beside any figure that came from
    this filter. A number without its exclusions is not honest.
    """
    labelled = classify(rows, today)
    total = len(labelled)
    counts: dict[str, int] = {}
    for row in labelled:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    kinds: dict[str, int] = {}
    for row in labelled:
        if row["status"] == "not_a_model":
            kinds[row["kind"]] = kinds.get(row["kind"], 0) + 1

    pieces = []
    if kinds.get("router"):
        pieces.append(f"{kinds['router']} routers and house entries that are not models")
    if kinds.get("alias"):
        pieces.append(f"{kinds['alias']} moving aliases such as \"latest\"")
    if kinds.get("batch_variant"):
        pieces.append(f"{kinds['batch_variant']} batch listings, which are a discount rather than a model")
    if counts.get("superseded"):
        pieces.append(f"{counts['superseded']} older versions still on sale beside their successors")
    if counts.get("stale"):
        pieces.append(f"{counts['stale']} listings too old to count as a current option")

    return (f"Out of {total} listings the seller offers, {counts.get('current', 0)} "
            "count as models available today. Left out: " + "; ".join(pieces) + ".")


if __name__ == "__main__":
    # A demonstration on the newest snapshot in the archive. Reads only.
    import json

    snapshots = sorted((PIPELINE_DIR / "snapshots" / "openrouter").glob("*.json"))
    newest = [p for p in snapshots if p.name != "index.json"][-1]
    rows = json.loads(newest.read_text(encoding="utf-8"))["rows"]

    print(f"Reading {newest.name}\n")
    print(describe_exclusions(rows), "\n")

    current = current_only(rows)

    def price(row: dict[str, Any]) -> float:
        value = row.get("usd_per_m_output")
        return -1.0 if value is None else float(value)

    print("Most expensive models available today, per million words written:")
    for row in sorted(current, key=price, reverse=True)[:6]:
        print(f"   ${price(row):>7.2f}  {row['display_name']}")

    print("\nBiggest memory among models available today:")
    for row in sorted(current, key=lambda r: r.get("context_tokens") or 0, reverse=True)[:6]:
        print(f"   {row.get('context_tokens'):>10,}  {row['display_name']}")
