#!/usr/bin/env python3
"""
THE DAILY HEARTBEAT
===================

WHAT THIS DOES, IN ONE SENTENCE
Every morning at 10:30 Atlas looks itself over and sends Nir one short
Telegram message saying whether everything is healthy.

WHY IT EXISTS (bible/part-12.md, operations; part-00.md LAW 11)
Nir gets 45 minutes of attention per week for this whole project, and he must
never have to go looking for problems. So the machine reports to him instead.
A green message means "ignore me". A red message means "something needs you,
and here is the one thing it is".

The Bible also demands that the project survive neglect: a "vacation mode"
where the site stays honest with zero attention for a month. A heartbeat is
what makes neglect SAFE, because silence stops being ambiguous. If no message
arrives for days, that itself is information: the desktop is switched off.

WHAT IT CHECKS
1. The price archive. Is the newest snapshot recent, and how many models did
   it hold? This is the one job in the project where a missed week is
   permanent damage, so it is checked first and reported first.
2. Free space, separately for the small system disk and the big home disk.
   Decision 3 in DECISIONS.md says everything that grows lives on /home; this
   check is what would catch an installer breaking that rule.
3. Whether the repository has work that was never saved to GitHub.

WHAT IT DELIBERATELY DOES NOT DO
It does not fix anything, it does not delete anything, and it does not touch
the archive. It only looks and reports. A watchman with a hammer is a hazard.

HOW TO RUN IT BY HAND
    cd /home/nir/strulovitz-website/pipeline && uv run stages/heartbeat.py
Add --dry-run to print the message here instead of sending it to Telegram.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

# Make "from lib.telegram import send" work no matter where it is run from.
PIPELINE_DIR = Path(__file__).resolve().parents[1]
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from lib.telegram import send  # noqa: E402 - path juggling must happen first

REPO_ROOT = PIPELINE_DIR.parent
SNAPSHOT_DIR = PIPELINE_DIR / "snapshots" / "openrouter"

# How stale the newest snapshot may be before it is a problem. The timer runs
# weekly, so eight days is normal breathing room; ten days means a Monday was
# missed AND the catch-up did not happen, which is worth a red flag.
SNAPSHOT_WARN_DAYS = 10

# Free space floors, in gigabytes. The system disk is small (about 92 GB in
# total) so it gets a modest floor; /home is where the database will grow.
SYSTEM_DISK_FLOOR_GB = 5
HOME_DISK_FLOOR_GB = 100

GIGABYTE = 1024 ** 3


def free_gb(path: str) -> float:
    """Free gigabytes on the partition holding the given path."""
    return shutil.disk_usage(path).free / GIGABYTE


def check_price_archive() -> tuple[bool, str]:
    """Look at the snapshot folder. Returns (healthy, one line for Nir)."""
    if not SNAPSHOT_DIR.exists():
        return False, "Price archive: the snapshot folder is MISSING."

    dated = sorted(p for p in SNAPSHOT_DIR.glob("*.json") if p.name != "index.json")
    if not dated:
        return False, "Price archive: EMPTY. No snapshot has ever been saved."

    newest = dated[-1]
    try:
        taken_on = date.fromisoformat(newest.stem)
    except ValueError:
        return False, f"Price archive: newest file has an odd name ({newest.name})."

    age_days = (date.today() - taken_on).days

    # The model count is nice reassurance: a snapshot that saved 3 models
    # instead of 400 is technically present but actually broken.
    # The snapshot file's own shape is documented in
    # pipeline/stages/snapshot_openrouter.py: a "row_count" number and a
    # "rows" list. Both are read, and they are expected to agree.
    model_count = "an unknown number of"
    try:
        data = json.loads(newest.read_text(encoding="utf-8"))
        rows = data.get("rows")
        if isinstance(rows, list):
            model_count = str(len(rows))
        elif isinstance(data.get("row_count"), int):
            model_count = str(data["row_count"])
    except Exception:  # noqa: BLE001 - a bad file is a finding, not a crash
        return False, f"Price archive: the newest file ({newest.name}) will not open."

    when = "today" if age_days == 0 else (
        "yesterday" if age_days == 1 else f"{age_days} days ago"
    )
    kept = f"{len(dated)} snapshot" + ("" if len(dated) == 1 else "s")
    line = (f"Price archive: {kept} kept. Newest taken {when} "
            f"with {model_count} models.")
    if age_days > SNAPSHOT_WARN_DAYS:
        return False, line + " That is TOO OLD - the weekly timer may be broken."
    return True, line


def check_disks() -> tuple[bool, list[str]]:
    """Check both partitions. Returns (healthy, lines for Nir)."""
    lines: list[str] = []
    healthy = True

    system_free = free_gb("/")
    home_free = free_gb("/home")

    lines.append(f"System disk: {system_free:.0f} GB free.")
    if system_free < SYSTEM_DISK_FLOOR_GB:
        healthy = False
        lines[-1] += " That is LOW."

    lines.append(f"Big home disk: {home_free:.0f} GB free.")
    if home_free < HOME_DISK_FLOOR_GB:
        healthy = False
        lines[-1] += " That is LOW."

    return healthy, lines


def check_repository() -> tuple[bool, str]:
    """
    Is there work sitting on this computer that GitHub has never seen?

    This is a gentle reminder, not an error, so an untidy day never turns the
    whole morning message red.
    """
    try:
        changed = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
            capture_output=True, text=True, timeout=30, check=True,
        ).stdout.strip()
        unpushed = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "log", "--oneline", "@{u}..HEAD"],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
    except Exception:  # noqa: BLE001
        return True, "Repository: could not be checked this morning."

    if not changed and not unpushed:
        return True, "Repository: everything is saved to GitHub."

    parts = []
    if changed:
        parts.append(f"{len(changed.splitlines())} unsaved file(s)")
    if unpushed:
        parts.append(f"{len(unpushed.splitlines())} commit(s) not yet on GitHub")
    return True, "Repository: " + " and ".join(parts) + "."


def build_message() -> tuple[bool, str]:
    """Assemble the whole morning message. Returns (all_healthy, message)."""
    archive_ok, archive_line = check_price_archive()
    disks_ok, disk_lines = check_disks()
    _, repo_line = check_repository()

    all_healthy = archive_ok and disks_ok

    headline = ("Good morning Nir. Atlas here. Everything is healthy."
                if all_healthy else
                "Good morning Nir. Atlas here. SOMETHING NEEDS YOU.")

    body = [
        headline,
        "",
        archive_line,
        *disk_lines,
        repo_line,
    ]

    if not all_healthy:
        body += ["", "Tell your agent 'read the heartbeat' and it will look "
                     "into the line above that is not normal."]

    body += ["", datetime.now().strftime("Checked %A %d %B %Y at %H:%M.")]
    return all_healthy, "\n".join(body)


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    all_healthy, message = build_message()

    if dry_run:
        print(message)
        return 0 if all_healthy else 1

    sent = send(message)
    if not sent:
        # Exit non-zero so systemd records a failure and the next day's run
        # still happens. Never retry in a loop: Telegram dislikes it and a
        # missed heartbeat is not an emergency.
        return 2
    print("Heartbeat sent." + ("" if all_healthy else " It reported a problem."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
