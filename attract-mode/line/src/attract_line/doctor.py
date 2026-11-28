"""am doctor -- check this PC and say in plain words what is wrong.

Part 01, section 1.10, item 1. It reports:
  the versions against the pins; the ports; whether Moodle answers; whether
  Git is clean and up to date; whether Syncthing sees the other PC; how old
  the newest hand-over of Moodle's data is.
And, because Part 09, section 9.8 asks for it, the free space.

Every failure is ONE plain sentence saying what to do about it. A piece that
belongs to a later stage is a NOTE, not a failure: the stage map below comes
from Part 11, section 11.4 (Stage 0 the kitchen, Stage 1 something to show,
Stage 2 Moodle on the desktop). It is written down here so the report never
cries wolf about a piece that is simply not due yet.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import shutil
import socket
import subprocess
import sys
import urllib.error
import urllib.request

from . import pins

OK, NOTE, FAIL = "OK", "NOTE", "FAIL"

# Part 01, section 1.4: the ports and their owners. Not to be changed.
PORTS = [
    (8081, "www.strulovitz.org today, and pre.strulovitz.org", "Stage 0"),
    (8082, "learnime.com", "already there"),
    (8083, "peaktogether.me", "already there"),
    (8084, "Attract Mode: Moodle plus our plain files", "Stage 2"),
    (3306, "MariaDB (reached only from this PC)", "Stage 0"),
    (8384, "Syncthing's own window", "Stage 0"),
]

# Part 11, section 11.4: which stage a piece belongs to.
STAGE_OF = {
    "Moodle": "Stage 2 (Switch Day)",
    "PHP": "Stage 0",
    "MariaDB": "Stage 0",
    "Syncthing": "Stage 0",
    "Manim Community": "Stage 1",
    "ffmpeg": "Stage 1",
    "speech-to-text": "Stage 1",
    "numbers to words": "Stage 1",
    "Playwright": "Stage 1",
    "Obsidian": "any time (a viewer only)",
}

how_it_gets_there = {
    "PHP": "run owner-setup (card 0-15)",
    "MariaDB": "run owner-setup (card 0-15)",
    "Syncthing": "run owner-setup (card 0-15)",
    "Moodle": "it arrives at Stage 2 (Part 11, 11.5)",
    "Manim Community": "it arrives at Stage 1",
    "ffmpeg": "run owner-setup, or install it at Stage 1",
    "speech-to-text": "the EXPERT pins the engine version and the model, then it is installed",
    "numbers to words": "the EXPERT pins it, then it is installed",
    "Playwright": "the EXPERT pins it, then it is installed",
    "Obsidian": "install it whenever you like; nothing depends on it",
}


class Line:
    __slots__ = ("group", "name", "state", "detail")

    def __init__(self, group: str, name: str, state: str, detail: str) -> None:
        self.group, self.name, self.state, self.detail = group, name, state, detail


def run(cmd: list[str], timeout: float = 8.0) -> str | None:
    try:
        out = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return None
    text = (out.stdout or "") + (out.stderr or "")
    return text.strip() or None


def first_version(text: str | None, patterns: list[str]) -> str | None:
    """Pull the first version number out of a program's own words."""
    import re

    if not text:
        return None
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(1)
    return None


# ---------------------------------------------------------------- versions ---

def installed_versions() -> dict[str, str | None]:
    found: dict[str, str | None] = {}

    php_bin = shutil.which("php") or shutil.which("php8.4") or shutil.which("php8.3")
    found["PHP"] = first_version(
        run([php_bin, "-r", "echo PHP_VERSION;"]) if php_bin else None, [r"(\d+\.\d+\.\d+)"]
    )

    db_text = run(["mariadb", "--version"]) or run(["mysql", "--version"])
    found["MariaDB"] = first_version(db_text, [r"Distrib\s+(\d+\.\d+(?:\.\d+)?\S*)"])
    if not found["MariaDB"]:
        found["MariaDB"] = first_version(db_text, [r"(\d+\.\d+\.\d+)"])
    if found["MariaDB"]:
        found["MariaDB"] = found["MariaDB"].split("-")[0].rstrip(".,")

    found["Syncthing"] = first_version(run(["syncthing", "--version"]), [r"v(\d+\.\d+\.\d+)"])
    found["uv"] = first_version(run(["uv", "--version"]), [r"uv\s+(\d+\.\d+\.\d+)"])
    found["ffmpeg"] = first_version(run(["ffmpeg", "-version"]), [r"ffmpeg version (\d+\.\d+(?:\.\d+)?)"])
    found["Manim Community"] = first_version(run(["manim", "--version"]), [r"(\d+\.\d+\.\d+)"])

    # The line's Python is the one running this command (Part 01, 1.8).
    found["Python (the line)"] = "%d.%d.%d" % sys.version_info[:3]

    found["Obsidian"] = None
    for name in ("obsidian", "Obsidian"):
        if shutil.which(name):
            found["Obsidian"] = first_version(run([name, "--version"]), [r"(\d+\.\d+\.\d+)"]) or "installed"
            break

    found["Playwright"] = None
    if shutil.which("playwright"):
        found["Playwright"] = "installed"
    else:
        try:
            import importlib.util

            if importlib.util.find_spec("playwright") is not None:
                found["Playwright"] = "installed"
        except Exception:
            pass

    found["Moodle"] = None  # decided by the port check below
    found["speech-to-text"] = None
    found["numbers to words"] = None
    return found


def matches(pin: str, have: str) -> bool:
    """A pin decides how exact the match must be (Part 01, 1.8).

    '11.8 series' means the series. '2.1.7' means exactly that, but 2.1.7
    also accepts a build suffix like 2.1.7~ds1. '8.3' accepts 8.3.x.
    """
    pin = pin.strip()
    if pin.lower().endswith("series"):
        pin = pin.split()[0]
    return have == pin or have.startswith(pin + ".") or have.startswith(pin + "-") or have.startswith(pin + "~")


def pc_family() -> str:
    """desktop or laptop, from the Linux the survey found (Part 01, 1.5)."""
    try:
        text = pathlib.Path("/etc/os-release").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "unknown"
    for line in text.splitlines():
        if line.startswith("ID="):
            ident = line.split("=", 1)[1].strip().strip('"')
            return "laptop" if ident == "debian" else "desktop"
    return "unknown"


def version_lines(versions: dict[str, str | None], pin_map: dict[str, str]) -> list[Line]:
    out: list[Line] = []
    family = pc_family()
    for name, pin in pin_map.items():
        if name in ("id", "kind", "state"):
            continue
        # A pin that names a PC applies only to that PC: the two Linux systems
        # bring different PHP, and Part 01, section 1.8 allows exactly that.
        if name.startswith("PHP (") and not name.endswith("(" + family + ")"):
            continue
        base = name.split(" (")[0]
        have = versions.get(name) or versions.get(base)
        stage = STAGE_OF.get(base)
        get_there = how_it_gets_there.get(base, "the EXPERT decides")

        if pin == "OPEN":
            out.append(Line("THE PINS", name, NOTE, "no version pinned yet; " + get_there))
            continue
        if not have:
            state = NOTE if stage and stage != "Stage 0" else FAIL
            out.append(Line("THE PINS", name, state,
                            "pinned " + pin + "; not installed here. It belongs to "
                            + (stage or "a later stage") + "; " + get_there + "."))
            continue
        if matches(pin, have):
            out.append(Line("THE PINS", name, OK, have + " (pin " + pin + ")"))
        else:
            out.append(Line("THE PINS", name, FAIL,
                            "this PC has " + have + " but the pin says " + pin
                            + "; bring it to the pin on both PCs."))
    return out


# ------------------------------------------------------------------ ports ---

def listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.35)
        return s.connect_ex(("127.0.0.1", port)) == 0


def port_lines() -> list[Line]:
    out = []
    for port, owner, stage in PORTS:
        up = listening(port)
        if up:
            out.append(Line("THE PORTS", f"{port}", OK, f"listening; {owner}"))
        else:
            out.append(Line("THE PORTS", f"{port}", NOTE, f"free; {owner} ({stage})"))
    return out


# ----------------------------------------------------------------- moodle ---

def http_get(url: str, timeout: float = 2.0):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status, r.read(400).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        try:
            return e.code, e.read(400).decode("utf-8", "replace")
        except Exception:
            return e.code, ""
    except Exception:
        return None, ""


def moodle_line() -> Line:
    status, body = http_get("http://127.0.0.1:8084/")
    if status is None:
        return Line("MOODLE", "8084", NOTE,
                    "nothing answers on 8084 yet; Moodle arrives at Stage 2 (Part 11, 11.5).")
    lowered = body.lower()
    if "attract mode is being built" in lowered:
        return Line("MOODLE", "8084", NOTE,
                    "our own block answers; Moodle itself is not installed yet (Stage 2).")
    if "moodle" in lowered or status in (200, 303):
        return Line("MOODLE", "8084", OK, f"something answers (HTTP {status}); check it is Moodle: "
                                           "run am moodle try once that command exists.")
    return Line("MOODLE", "8084", NOTE, f"an answer came back (HTTP {status}) but it does not look like Moodle.")


# -------------------------------------------------------------------- git ---

def repo_root() -> pathlib.Path:
    return pins.pins_path().parents[1].parent


def git_lines() -> list[Line]:
    root = str(repo_root())
    out: list[Line] = []
    dirty = run(["git", "-C", root, "status", "--porcelain", "--", "attract-mode"])
    if dirty is None:
        return [Line("GIT", "repository", FAIL, f"no git repository found at {root}.")]
    if dirty:
        count = len(dirty.splitlines())
        out.append(Line("GIT", "clean", FAIL,
                        f"{count} changed file(s) under attract-mode/ not committed yet; commit and push them (Part 01, 1.11)."))
    else:
        out.append(Line("GIT", "clean", OK, "nothing uncommitted under attract-mode/"))

    ahead = run(["git", "-C", root, "rev-list", "--count", "@{u}..HEAD"])
    behind = run(["git", "-C", root, "rev-list", "--count", "HEAD..@{u}"])
    if ahead is None or behind is None:
        out.append(Line("GIT", "up to date", NOTE, "this branch has no upstream set, so it cannot be compared with GitHub."))
        return out
    a, b = int(ahead or 0), int(behind or 0)
    if a == 0 and b == 0:
        out.append(Line("GIT", "up to date", OK, "nothing to send, nothing to take"))
    elif a:
        out.append(Line("GIT", "up to date", FAIL, f"{a} commit(s) not pushed yet; push them now (Part 01, 1.11)."))
    if b:
        out.append(Line("GIT", "up to date", FAIL, f"{b} commit(s) on GitHub not taken yet; run git pull first (Part 01, 1.11)."))
    return out


# --------------------------------------------------------------- syncthing ---

def syncthing_config() -> pathlib.Path | None:
    for p in (
        pathlib.Path.home() / ".local/state/syncthing/config.xml",
        pathlib.Path.home() / ".config/syncthing/config.xml",
    ):
        if p.exists():
            return p
    return None


def syncthing_lines() -> list[Line]:
    if not shutil.which("syncthing"):
        return [Line("SYNCTHING", "the other PC", NOTE,
                     "Syncthing is not installed here yet; it comes with owner-setup (card 0-15).")]
    cfg = syncthing_config()
    if cfg is None:
        return [Line("SYNCTHING", "the other PC", NOTE,
                     "Syncthing is installed but has not been started once, so there is no settings file yet; "
                     "start it, then check again.")]
    import re

    text = cfg.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<apikey>([^<]+)</apikey>", text)
    if not m:
        return [Line("SYNCTHING", "the other PC", NOTE,
                     "no key was found in Syncthing's settings file; open its window once and check again.")]
    req = urllib.request.Request(
        "http://127.0.0.1:8384/rest/system/connections",
        headers={"X-API-Key": m.group(1)},
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
    except Exception:
        return [Line("SYNCTHING", "the other PC", NOTE,
                     "Syncthing's own window does not answer; start Syncthing and check again.")]
    conns = data.get("connections") or {}
    if not conns:
        return [Line("SYNCTHING", "the other PC", NOTE,
                     "no other PC is known to Syncthing yet; add the other PC (Part 09, 9.9, item 6).")]
    connected = [k for k, v in conns.items() if isinstance(v, dict) and v.get("connected")]
    if connected:
        return [Line("SYNCTHING", "the other PC", OK, f"{len(connected)} device(s) connected right now")]
    return [Line("SYNCTHING", "the other PC", NOTE,
                 "Syncthing knows the other PC but it is not reachable now; both PCs must be on in Linux at the same time (Part 09, 9.9, item 4).")]


# --------------------------------------------------------------- hand-over ---

def handover_lines() -> list[Line]:
    folder = pathlib.Path.home() / "attract-mode-files" / "handover"
    if not folder.exists():
        return [Line("THE HAND-OVER", "newest", NOTE,
                     f"{folder} does not exist yet; it is created with the folder skeleton (card 0-04).")]
    files = [p for p in folder.iterdir() if p.is_file()]
    if not files:
        return [Line("THE HAND-OVER", "newest", NOTE,
                     "none yet. That is normal before Moodle exists (Stage 2).")]
    newest = max(files, key=lambda p: p.stat().st_mtime)
    age = dt.datetime.now() - dt.datetime.fromtimestamp(newest.stat().st_mtime)
    days = age.days
    when = f"{days} day(s)" if days else f"{int(age.total_seconds() // 3600)} hour(s)"
    state = NOTE
    detail = f"{newest.name}, {when} old"
    if newest.name.startswith("export-") and days > 2:
        state = FAIL
        detail += "; an export older than two days means the hand-over has stopped; see Part 09, section 9.8."
    return [Line("THE HAND-OVER", "newest", state, detail)]


# ------------------------------------------------------------------- disk ---

def disk_lines() -> list[Line]:
    out = []
    for label, path in (("/", "/"), ("your home (big files)", str(pathlib.Path.home()))):
        try:
            free = shutil.disk_usage(path).free / 1024**3
        except OSError:
            continue
        state = OK if free >= 60 else FAIL
        detail = f"{free:.0f} GB free"
        if state is FAIL:
            detail += "; Part 01, section 1.5 and Part 09, section 9.8 ask for at least 60 GB; free space before building."
        out.append(Line("THE DISK", label, state, detail))
    return out


# ------------------------------------------------------------------ output ---

def main() -> int:
    pin_map = pins.read()
    if not pin_map:
        print("FAIL  the pins file was not found or is empty: " + str(pins.pins_path()))
        print("      Restore attract-mode/config/pins (Part 01, section 1.8).")
        return 1

    versions = installed_versions()
    lines: list[Line] = []
    lines.append(Line("THIS PC", "name", OK, socket.gethostname()))
    lines.append(Line("THIS PC", "python", OK, "%d.%d.%d" % sys.version_info[:3]))
    lines += version_lines(versions, pin_map)
    lines += port_lines()
    lines.append(moodle_line())
    lines += git_lines()
    lines += syncthing_lines()
    lines += handover_lines()
    lines += disk_lines()

    print("AM DOCTOR -- this PC, in plain words")
    print("=" * 62)
    group = None
    for ln in lines:
        if ln.group != group:
            group = ln.group
            print(f"\n{group}")
        mark = {OK: "  ok   ", NOTE: "  note ", FAIL: "  FAIL "}[ln.state]
        print(f"{mark}{ln.name}: {ln.detail}")

    failures = [ln for ln in lines if ln.state == FAIL]
    print("\n" + "=" * 62)
    if not failures:
        print("No failures. A 'note' is something not due yet, or something waiting for Nir.")
        return 0
    print(f"{len(failures)} thing(s) to do:")
    for n, ln in enumerate(failures, 1):
        print(f"  {n}. {ln.name}: {ln.detail}")
    return 1
