"""The one entry point: am WORD. Part 01, section 1.10.

Stage 0 knows one word that works: doctor. The other two are named by the
Bible and belong to later Parts, so they say so plainly instead of pretending.
"""

from __future__ import annotations

import sys

from . import doctor

WORDS = {
    "doctor": "checks this PC and prints a plain-language report (Part 01, 1.10)",
    "build": "builds the plain files and course files into work/ (Part 05 -- not built yet)",
    "publish": "builds, tests, then copies into public/ and pushes (Part 09 -- not built yet)",
    "today": "prints the one list WAITING FOR NIR (Part 11, 11.12 -- not built yet)",
}


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help", "help"):
        print("Usage: am WORD")
        for word, what in WORDS.items():
            print(f"  {word:8s} {what}")
        return 0 if args else 1

    word, rest = args[0], args[1:]
    if word == "doctor":
        return doctor.main()
    if word in WORDS:
        print(f"am {word}: not built yet. {WORDS[word]}")
        return 3
    print(f"am: I do not know the word '{word}'.")
    print("Known words: " + ", ".join(WORDS))
    return 2
