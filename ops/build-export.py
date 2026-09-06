#!/usr/bin/env python3
"""
build-export.py  --  package the website into a version folder ready for FileZilla

Owned by: bible/part-01.md 1.9 (the export folder and the deployment ritual).

WHAT THIS DOES, IN PLAIN WORDS

It copies the website into a dated folder, writes a tiny file called
pointer.json that names which dated folder is live, and writes a little health
page so anyone can check what is on the server from a phone.

WHY IT IS SHAPED LIKE THIS. The public server is not allowed to run any code of
ours (LAW 4). So there is no clever deployment: Nir drags files with FileZilla.
The danger with dragging is that a visitor arrives halfway through the upload
and gets a half-new, half-old site. The version folder plus pointer.json trick
removes that danger completely:

  1. Nir uploads the new dated folder. This takes as long as it takes. The live
     site is completely untouched the whole time, because nothing points at the
     new folder yet.
  2. Nir uploads pointer.json LAST. It is a few hundred bytes, so it lands in
     about one second, and at that instant the whole site flips to the new
     version.
  3. If something is wrong, he re-uploads the PREVIOUS pointer.json, kept in
     ops/pointers/. One small file, one second, site restored, no help needed.

Run it with:  python3 ops/build-export.py
"""

import datetime
import hashlib
import json
import os
import shutil
import sys

REPOSITORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(REPOSITORY, "site")
EXPORTS = os.path.join(REPOSITORY, "exports")
POINTER_HISTORY = os.path.join(REPOSITORY, "ops", "pointers")

# What actually ships. Anything not named here stays at home, so a stray note or
# a test file cannot reach the public server by accident.
#
# There are two kinds of file, and the difference is the whole deployment trick:
#
# ROOT files sit at the top of the website and keep the address bar clean, so a
# visitor sees www.strulovitz.org and not a folder with a date in its name.
# They are small, hand-written pages that change rarely.
#
# VERSIONED files live inside a dated folder. All the code and all the data are
# in here. A new build never touches an old folder, so uploading a new version
# cannot break the live site halfway through: nothing points at the new folder
# until the tiny pointer file lands last.
SHIPPING_ROOT = [
    "index.html",
    "night-watch.html",
    "about.html",
    "home-page-gpt-image-2.html",
    "home-page-gemini-3-pro-image.html",
    "home-page-grok-imagine-image-2.html",
    "home-page-muse-image.html",
    "home-page-flux-2-max.html",
    "home-page-qwen-image-3-pro.html",
    "about-page-gpt-image-2.html",
    "about-page-gemini-3-pro-image.html",
    "about-page-grok-imagine-image-2.html",
    "about-page-muse-image.html",
    "about-page-flux-2-max.html",
    "about-page-qwen-image-3-pro.html",
    "laser-chess.html",
    "evil-genius.html",
    "second-opinion.html",
    "cheerleader.html",
    "vibe-invention.html",
    # Nir's picture galleries and the lightbox they open with. They are root
    # files because the pages that use them live at the root, and because they
    # rarely change, so an upload between versions is wasted effort.
    "lightbox.js",
    "images",
]
# "data" holds the galaxies: one four-dimensional world per edition, written by
# pipeline/stages/layout.py. Without it the live site loads the placeholder
# world instead of the real magazine, which is exactly the sort of quiet failure
# that is worth a comment rather than a shrug.
# "stories" and "ideas" hold the READING PAGES (2026-09-03): one page per story
# per edition and one per encyclopedia idea per edition, written by
# pipeline/stages/build_pages.py from the database. Clicking a node in the
# galaxy opens exactly these files, so forgetting to ship them would leave the
# magazine's clicks landing on 404s - the same quiet-failure class as above.
SHIPPING_VERSIONED = ["tesseract.html", "src", "vendor", "data", "stories", "ideas"]

# Files that must never be uploaded even if they sit inside a shipping folder.
NEVER_SHIP = {".env", ".DS_Store"}
NEVER_SHIP_SUFFIXES = (".selftest.js",)


def pick_version_name():
    """Today's date plus a letter, so several builds a day never collide."""
    today = datetime.date.today().isoformat()
    for letter in "abcdefghijklmnopqrstuvwxyz":
        name = f"v{today}-{letter}"
        if not os.path.exists(os.path.join(EXPORTS, name)):
            return name
    raise RuntimeError("twenty-six builds in one day is not a build, it is a loop")


def copy_shipping_files(destination, entries):
    copied = []
    for entry in entries:
        source = os.path.join(SITE, entry)
        if not os.path.exists(source):
            raise RuntimeError(f"missing from site/: {entry}")
        target = os.path.join(destination, entry)
        if os.path.isdir(source):
            for root, directories, files in os.walk(source):
                directories[:] = [d for d in directories if d != "__pycache__"]
                for name in files:
                    if name in NEVER_SHIP or name.endswith(NEVER_SHIP_SUFFIXES):
                        continue
                    full = os.path.join(root, name)
                    relative = os.path.relpath(full, SITE)
                    out = os.path.join(destination, relative)
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    shutil.copy2(full, out)
                    copied.append(relative)
        else:
            shutil.copy2(source, target)
            copied.append(entry)
    return sorted(copied)


def hash_of_files(folder, relative_paths):
    """One hash over every shipped file, so the pointer can name exactly what is live."""
    digest = hashlib.sha256()
    for relative in relative_paths:
        digest.update(relative.encode())
        with open(os.path.join(folder, relative), "rb") as handle:
            while True:
                chunk = handle.read(1 << 20)
                if not chunk:
                    break
                digest.update(chunk)
    return digest.hexdigest()


HEALTH_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>What is live right now - AI PANORAMA</title>
<style>
  body {{ background:#07090f; color:#dbe4f4; font:16px/1.7 system-ui,sans-serif;
          margin:0; padding:2.5rem 1.4rem; }}
  main {{ max-width:36rem; margin:0 auto; }}
  h1 {{ font-size:1.4rem; }}
  dt {{ color:#8fa3c4; margin-top:0.8rem; }}
  dd {{ margin:0; }}
  code {{ background:#131a2a; padding:0.1rem 0.35rem; border-radius:4px;
          word-break:break-all; }}
</style>
</head>
<body>
<main>
<h1>What is live right now</h1>
<p>This page is here so that anyone, including Nir on a phone, can check what
is actually on the server without asking anybody.</p>
<dl>
  <dt>Version</dt><dd>{version}</dd>
  <dt>Built</dt><dd>{built}</dd>
  <dt>Milestone</dt><dd>{milestone}</dd>
  <dt>Files shipped</dt><dd>{file_count}</dd>
  <dt>Content fingerprint</dt><dd><code>{content_hash}</code></dd>
  <dt>Real content in this version</dt><dd>{content_note}</dd>
</dl>
<p><a href="index.html">Back to the site</a></p>
</main>
</body>
</html>
"""


def main():
    os.makedirs(EXPORTS, exist_ok=True)
    os.makedirs(POINTER_HISTORY, exist_ok=True)

    version = pick_version_name()
    destination = os.path.join(EXPORTS, version)
    os.makedirs(destination)

    copied = copy_shipping_files(destination, SHIPPING_VERSIONED)
    root_copied = copy_shipping_files(EXPORTS, SHIPPING_ROOT)
    content_hash = hash_of_files(destination, copied)
    built = datetime.datetime.now().replace(microsecond=0).isoformat()

    # Every root page carries the live version's name inside its tesseract
    # links, so that the site still works for a visitor with JavaScript
    # switched off. index.html must always carry the placeholder; the other
    # root pages are only fixed up if they happen to use it.
    # encoding="utf-8" is MANDATORY: the pages carry emojis, and on Windows a
    # plain open() reads them in the local codepage and silently corrupts them.
    root_index = os.path.join(EXPORTS, "index.html")
    with open(root_index, encoding="utf-8") as handle:
        landing = handle.read()
    if "VERSION_FALLBACK" not in landing:
        raise RuntimeError("site/index.html lost its VERSION_FALLBACK placeholder")
    with open(root_index, "w", encoding="utf-8") as handle:
        handle.write(landing.replace("VERSION_FALLBACK", version))
    for name in root_copied:
        if not name.endswith(".html"):
            continue
        path = os.path.join(EXPORTS, name)
        with open(path, encoding="utf-8") as handle:
            page_text = handle.read()
        if "VERSION_FALLBACK" in page_text:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(page_text.replace("VERSION_FALLBACK", version))

    with open(os.path.join(destination, "build-health.html"), "w") as handle:
        handle.write(HEALTH_HTML.format(
            version=version, built=built, milestone="1 - Hello, Tesseract",
            file_count=len(copied), content_hash=content_hash,
            content_note="None. Every node is a placeholder with a made-up name."))

    pointer = {
        "schema_version": 1,
        "live": version,
        "built": built,
        "content_hash": content_hash,
        "milestone": "1 - Hello, Tesseract",
        "plain_words": ("The live version of the site is the folder named above. "
                        "To go back to the previous one, upload the previous "
                        "pointer.json from ops/pointers/."),
    }
    pointer_text = json.dumps(pointer, indent=2) + "\n"
    with open(os.path.join(EXPORTS, "pointer.json"), "w") as handle:
        handle.write(pointer_text)
    # Keep every pointer we have ever shipped, so rollback is always one file.
    with open(os.path.join(POINTER_HISTORY, f"pointer-{version}.json"), "w") as handle:
        handle.write(pointer_text)

    print(f"built {version}")
    print(f"  files          {len(copied)} versioned, {len(root_copied)} at the root")
    print(f"  fingerprint    {content_hash[:16]}...")
    print(f"  folder         exports/{version}/")
    print("")
    print("THE UPLOAD ORDER MATTERS. Folder first, pointer last:")
    print(f"  1. exports/{version}/       -> into the website's root")
    for name in root_copied:
        print(f"  2. exports/{name}      -> into the website's root")
    print("  3. exports/pointer.json      -> LAST. This is the moment it flips.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
