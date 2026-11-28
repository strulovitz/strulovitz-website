"""Reading attract-mode/config/pins (Part 01, section 1.8).

The pins file is plain text. A piece is one line shaped like:

    Moodle            5.3         LTS of 5 October 2026.

That is: a name, then two or more spaces, then the value, then two or more
spaces and the reason. A value of OPEN means nobody has pinned it yet.
Lines that begin with a space are continuations of the line above them.
"""

from __future__ import annotations

import pathlib
import re

SPLIT = re.compile(r"\s{2,}")


def pins_path() -> pathlib.Path:
    """attract-mode/config/pins, found from this file's own place."""
    here = pathlib.Path(__file__).resolve()
    # .../attract-mode/line/src/attract_line/pins.py -> attract-mode/
    root = here.parents[3]
    return root / "config" / "pins"


def read(path: pathlib.Path | None = None) -> dict[str, str]:
    """Return {name: value}. An OPEN pin comes back as "OPEN"."""
    p = path or pins_path()
    out: dict[str, str] = {}
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        parts = SPLIT.split(line.strip(), maxsplit=2)
        if len(parts) < 2:
            continue
        out[parts[0].strip()] = parts[1].strip()
    return out
