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
SHIPPING = ["index.html", "tesseract.html", "src", "vendor"]

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


def copy_shipping_files(destination):
    copied = []
    for entry in SHIPPING:
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


LOADER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AI PANORAMA</title>
<!--
  This tiny file is the only thing at the top of the website. It reads
  pointer.json to find out which dated folder is currently live, and goes
  there. That indirection is what makes deployment atomic: the dated folder is
  uploaded first and slowly, then pointer.json is uploaded last and instantly.
  bible/part-01.md 1.9.
-->
<script>
  fetch('pointer.json', { cache: 'no-store' })
    .then((response) => response.json())
    .then((pointer) => { location.replace(pointer.live + '/index.html'); })
    .catch(() => { document.getElementById('fallback').style.display = 'block'; });
</script>
<style>
  body { background:#07090f; color:#dbe4f4; font:16px/1.6 system-ui,sans-serif;
         margin:0; padding:4rem 1.5rem; }
  main { max-width:32rem; margin:0 auto; }
  a { color:#9fd0ff; }
  #fallback { display:none; }
</style>
</head>
<body>
<main>
  <p>Opening AI PANORAMA...</p>
  <div id="fallback">
    <p>Could not read the pointer file. The site is still there:</p>
    <p><a href="POINTER_FALLBACK/index.html">Open the current version directly</a></p>
  </div>
</main>
</body>
</html>
"""


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

    copied = copy_shipping_files(destination)
    content_hash = hash_of_files(destination, copied)
    built = datetime.datetime.now().replace(microsecond=0).isoformat()

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

    with open(os.path.join(EXPORTS, "index.html"), "w") as handle:
        handle.write(LOADER_HTML.replace("POINTER_FALLBACK", version))

    print(f"built {version}")
    print(f"  files          {len(copied)}")
    print(f"  fingerprint    {content_hash[:16]}...")
    print(f"  folder         exports/{version}/")
    print("")
    print("THE UPLOAD ORDER MATTERS. Upload the folder FIRST, the pointer LAST:")
    print(f"  1. exports/{version}/   -> the website's folder on the server")
    print("  2. exports/index.html    -> only needed the very first time")
    print("  3. exports/pointer.json  -> LAST. This is the moment the site flips.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
