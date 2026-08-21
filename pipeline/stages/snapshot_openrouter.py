#!/usr/bin/env python3
"""
WEEKLY OPENROUTER PRICE AND SPEC SNAPSHOT
=========================================

WHAT THIS DOES, IN ONE SENTENCE
Once a week this script asks OpenRouter's free public API what every AI model
currently costs and how big its memory is, and saves that answer as a dated
file that we keep forever.

WHY IT MATTERS (bible/part-09.md, section 9.4)
Release dates are public history that anyone can look up later. Prices and
specifications on a particular past Tuesday are NOT recorded anywhere you can
retrieve. So the sentence "this model is getting 30 percent cheaper every
quarter" can only be said by someone who quietly saved the Tuesdays. We are
that someone, starting now. A missing week is permanent damage: it can never
be filled in afterwards.

WHERE THE DATA GOES
pipeline/snapshots/openrouter/YYYY-MM-DD.json  (one file per snapshot day)
pipeline/snapshots/openrouter/index.json       (a list of every snapshot taken)

Later, when Neo4j exists on Atlas, a second small step will also load these
same files into the database as immutable rows. The files stay either way:
they are the frozen evidence, and they are what gets published one day as a
public dataset (bible/part-09.md 9.4.3).

RULES THIS SCRIPT OBEYS
1. It needs NO API key. The models endpoint is public. That is deliberate:
   the fewer secrets a forever-script needs, the longer it keeps working.
2. It is idempotent (bible/part-00.md LAW 12). Running it five times on the
   same day produces the same one file. It refuses to overwrite an existing
   snapshot unless you pass --force, because an archive file is sacred.
3. Missing data stays missing. Speed and latency are not offered by this API,
   so those fields are written as null, never as zero. Plotting absence as
   zero is a lie (bible/part-09.md 9.1.6).
4. It writes a plain-English summary line to standard output, suitable for
   pasting into Telegram (bible/part-00.md LAW 3).

HOW TO RUN IT BY HAND
    cd /home/nir/strulovitz-website/pipeline
    uv run stages/snapshot_openrouter.py

EXIT CODES
    0 = a snapshot exists for today (freshly written, or already there)
    1 = something failed, and nothing was written. The day is still missing.
        Fix it and re-run the same day if at all possible.
"""

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

import httpx

# ----------------------------------------------------------------------------
# Constants. Everything a future reader might want to change lives up here.
# ----------------------------------------------------------------------------

# The shape of the records we write. Bump this ONLY together with the matching
# file in schemas/, and record the change in the job ledger.
SCHEMA_VERSION = 1

# The public endpoint. No authentication, no key, no account needed.
SOURCE_API = "https://openrouter.ai/api/v1/models"

# Where snapshots are stored, relative to the pipeline folder this file is in.
SNAPSHOT_DIRNAME = Path("snapshots") / "openrouter"

# How we describe the terms under which we hold this data. Every record carries
# it so that a future dataset publication can be honest about provenance.
LICENSE_OF_DATA = "openrouter-public-api"

# Be a polite, identifiable robot (bible/part-06.md 6.1.4).
USER_AGENT = (
    "AI-PANORAMA-snapshot/1.0 (+https://www.strulovitz.org/; "
    "price and spec history archive; contact via strulovitz.org)"
)

REQUEST_TIMEOUT_SECONDS = 60.0
RETRY_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = 5.0


# ----------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------


def _per_million(price_per_token: object) -> float | None:
    """OpenRouter quotes prices per single token, as a string.

    We store US dollars per MILLION tokens, because that is how humans discuss
    model prices. Anything unparseable, negative, or absent becomes None, which
    means genuinely unknown. It never becomes 0.0, because 0.0 means free.
    """
    if price_per_token is None:
        return None
    try:
        value = float(price_per_token)
    except (TypeError, ValueError):
        return None
    if value < 0:
        return None
    # Round to 6 decimal places: enough for even the cheapest models, and it
    # stops floating-point noise from making two identical days look different.
    return round(value * 1_000_000.0, 6)


def _int_or_none(value: object) -> int | None:
    """Return a positive integer, or None if the value is absent or nonsense."""
    if value is None:
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None


def _proposed_entity_id(openrouter_model_id: str) -> str:
    """Suggest the project's own entity id for this model.

    The real entity registry (bible/part-02.md 2.4) does not exist yet, and
    entities are never created silently. So we only PROPOSE an id here, in the
    project's readable format, and a later stage resolves or merges it under
    Nir's approval. Example: "anthropic/claude-opus-5" becomes
    "ent-anthropic-claude-opus-5".
    """
    slug = openrouter_model_id.strip().lower()
    cleaned = []
    for character in slug:
        if character.isalnum():
            cleaned.append(character)
        else:
            # Any separator at all (slash, dot, colon, space) becomes a hyphen.
            cleaned.append("-")
    slug = "".join(cleaned)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return "ent-" + slug.strip("-")


def fetch_models() -> list[dict]:
    """Ask OpenRouter for the current model list, retrying a few times.

    Raises RuntimeError if every attempt fails, so the caller can report a
    failure loudly rather than writing a half-empty snapshot.
    """
    import time

    last_error: Exception | None = None
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            response = httpx.get(
                SOURCE_API,
                timeout=REQUEST_TIMEOUT_SECONDS,
                headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
                follow_redirects=True,
            )
            response.raise_for_status()
            payload = response.json()
            models = payload.get("data")
            if not isinstance(models, list) or not models:
                raise RuntimeError("the response contained no model list")
            return models
        except Exception as error:  # noqa: BLE001 - we retry on anything
            last_error = error
            if attempt < RETRY_ATTEMPTS:
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
    raise RuntimeError(f"could not fetch the model list: {last_error}")


def build_rows(models: list[dict], snapshot_date: str) -> list[dict]:
    """Turn OpenRouter's answer into our own snapshot records.

    The field names and their meanings are fixed by bible/part-02.md 2.8.
    We keep a few extra clearly-named fields that OpenRouter gives us for free
    and that we would otherwise lose forever.
    """
    rows: list[dict] = []
    for model in models:
        model_id = model.get("id")
        if not isinstance(model_id, str) or not model_id:
            # No id means we cannot identify what we are looking at. Skip it,
            # and the count difference will show up in the summary.
            continue

        pricing = model.get("pricing") or {}
        top_provider = model.get("top_provider") or {}
        architecture = model.get("architecture") or {}

        rows.append(
            {
                "schema_version": SCHEMA_VERSION,
                "snapshot_date": snapshot_date,
                # "provider" here means the marketplace we measured through.
                # The company that MADE the model is recorded separately below.
                "provider": "openrouter",
                "model": _proposed_entity_id(model_id),
                "model_is_proposed_entity": True,
                "openrouter_model_id": model_id,
                "canonical_slug": model.get("canonical_slug"),
                "display_name": model.get("name"),
                "developer_hint": model_id.split("/")[0] if "/" in model_id else None,
                # Prices, in US dollars per million tokens. None means unknown.
                "usd_per_m_input": _per_million(pricing.get("prompt")),
                "usd_per_m_output": _per_million(pricing.get("completion")),
                "usd_per_m_cache_read": _per_million(pricing.get("input_cache_read")),
                "usd_per_m_cache_write": _per_million(pricing.get("input_cache_write")),
                # Sizes.
                "context_tokens": _int_or_none(
                    top_provider.get("context_length") or model.get("context_length")
                ),
                "max_output_tokens": _int_or_none(
                    top_provider.get("max_completion_tokens")
                ),
                # We cannot measure these from this endpoint. Missing is missing.
                # They will be filled later from our own production call logs.
                "throughput_tps_median": None,
                "latency_s_p50": None,
                # Useful context that costs nothing to keep and cannot be
                # reconstructed later if the model is withdrawn.
                "modality": architecture.get("modality"),
                "is_moderated": top_provider.get("is_moderated"),
                "supported_parameters": model.get("supported_parameters"),
                "openrouter_created_unix": model.get("created"),
                # Provenance.
                "source_api": SOURCE_API,
                "license_of_data": LICENSE_OF_DATA,
            }
        )

    # Sort by model id so that two runs on the same day produce byte-identical
    # files. Determinism is what makes "did anything change?" answerable.
    rows.sort(key=lambda row: row["openrouter_model_id"])
    return rows


def write_snapshot(
    snapshot_dir: Path, snapshot_date: str, rows: list[dict], force: bool
) -> tuple[Path, bool]:
    """Write one dated snapshot file. Returns (path, was_written_now)."""
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    target = snapshot_dir / f"{snapshot_date}.json"

    document = {
        "schema_version": SCHEMA_VERSION,
        "snapshot_date": snapshot_date,
        "taken_at_utc": _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds"),
        "source_api": SOURCE_API,
        "license_of_data": LICENSE_OF_DATA,
        "row_count": len(rows),
        "rows": rows,
    }

    if target.exists() and not force:
        # LAW 12: the archive is sacred. An existing day is never overwritten
        # by accident. Re-running the script is therefore always safe.
        return target, False

    # Write to a temporary file first, then move it into place, so that a
    # crash or a power cut can never leave a half-written archive file.
    temporary = target.with_suffix(".json.partial")
    temporary.write_text(
        json.dumps(document, indent=1, ensure_ascii=False, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(target)
    return target, True


def update_index(snapshot_dir: Path) -> Path:
    """Rebuild the little index of every snapshot we hold.

    Rebuilt from what is actually on disk, never appended to blindly, so it can
    never drift out of step with reality.
    """
    entries = []
    for path in sorted(snapshot_dir.glob("20*.json")):
        if path.name == "index.json":
            continue
        raw = path.read_bytes()
        try:
            document = json.loads(raw)
            row_count = document.get("row_count")
            taken_at = document.get("taken_at_utc")
        except json.JSONDecodeError:
            row_count = None
            taken_at = None
        entries.append(
            {
                "snapshot_date": path.stem,
                "file": path.name,
                "row_count": row_count,
                "taken_at_utc": taken_at,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
            }
        )

    index_path = snapshot_dir / "index.json"
    index_path.write_text(
        json.dumps(
            {
                "schema_version": SCHEMA_VERSION,
                "what_this_is": (
                    "Every OpenRouter price and specification snapshot this "
                    "project holds, oldest first. One entry per day taken."
                ),
                "snapshot_count": len(entries),
                "first_snapshot": entries[0]["snapshot_date"] if entries else None,
                "latest_snapshot": entries[-1]["snapshot_date"] if entries else None,
                "snapshots": entries,
            },
            indent=1,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return index_path


def compare_with_previous(snapshot_dir: Path, snapshot_date: str) -> str:
    """Describe, in plain English, what changed since the previous snapshot."""
    dated = sorted(
        path for path in snapshot_dir.glob("20*.json") if path.name != "index.json"
    )
    if len(dated) < 2:
        return "This is the first snapshot, so there is nothing to compare it to yet."

    current_path = snapshot_dir / f"{snapshot_date}.json"
    previous_path = None
    for path in reversed(dated):
        if path != current_path:
            previous_path = path
            break
    if previous_path is None:
        return "No earlier snapshot was found to compare against."

    def ids_and_prices(path: Path) -> dict[str, tuple]:
        document = json.loads(path.read_text(encoding="utf-8"))
        return {
            row["openrouter_model_id"]: (
                row.get("usd_per_m_input"),
                row.get("usd_per_m_output"),
            )
            for row in document.get("rows", [])
        }

    now = ids_and_prices(current_path)
    before = ids_and_prices(previous_path)

    added = sorted(set(now) - set(before))
    removed = sorted(set(before) - set(now))
    price_changed = sorted(
        model_id for model_id in set(now) & set(before) if now[model_id] != before[model_id]
    )

    parts = [
        f"Compared with {previous_path.stem}: "
        f"{len(added)} models appeared, {len(removed)} disappeared, "
        f"{len(price_changed)} changed price."
    ]
    if added:
        parts.append("New: " + ", ".join(added[:8]) + ("..." if len(added) > 8 else ""))
    if removed:
        parts.append("Gone: " + ", ".join(removed[:8]) + ("..." if len(removed) > 8 else ""))
    if price_changed:
        parts.append(
            "Repriced: " + ", ".join(price_changed[:8]) + ("..." if len(price_changed) > 8 else "")
        )
    return " ".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Save this week's AI model prices and specifications forever."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite today's snapshot if one already exists. Use sparingly.",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Override the snapshot date, as YYYY-MM-DD. For testing only.",
    )
    arguments = parser.parse_args(argv)

    pipeline_dir = Path(__file__).resolve().parent.parent
    snapshot_dir = pipeline_dir / SNAPSHOT_DIRNAME

    snapshot_date = arguments.date or _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%d")

    try:
        models = fetch_models()
    except Exception as error:  # noqa: BLE001
        print(f"SNAPSHOT FAILED for {snapshot_date}: {error}", file=sys.stderr)
        print(
            "Nothing was written. This day is still missing from the archive. "
            "Fix the problem and run it again today if you possibly can.",
            file=sys.stderr,
        )
        return 1

    rows = build_rows(models, snapshot_date)
    if not rows:
        print(
            f"SNAPSHOT FAILED for {snapshot_date}: the API answered but no usable "
            "records could be built. Nothing was written.",
            file=sys.stderr,
        )
        return 1

    path, was_written = write_snapshot(snapshot_dir, snapshot_date, rows, arguments.force)
    index_path = update_index(snapshot_dir)
    comparison = compare_with_previous(snapshot_dir, snapshot_date)

    priced = sum(1 for row in rows if row["usd_per_m_input"] is not None)
    if was_written:
        headline = f"SNAPSHOT OK for {snapshot_date}: saved {len(rows)} models."
    else:
        headline = (
            f"SNAPSHOT ALREADY DONE for {snapshot_date}: a file was already there, "
            f"so nothing was changed ({len(rows)} models were fetched and matched)."
        )

    print(headline)
    print(f"{priced} of {len(rows)} models published a price.")
    print(comparison)
    print(f"File: {path}")
    print(f"Index: {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
