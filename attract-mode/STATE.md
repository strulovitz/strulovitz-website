ATTRACT MODE -- STATE

Read this first, after Part 00. One page. Rewritten, not appended to, at
the end of every session: what exists, what works, what comes next, and
what is waiting for Nir.
Last rewritten: 2026-11-28, desktop-linux.

WHAT EXISTS
- bible/ -- 12 files. Read IN FULL on 2026-11-28 (all 7,189 lines);
  laws.md matches Part 11, section 11.8, word for word.
- DECISIONS.md -- D1 to D77. Only D64 is open.
- tasks/ -- the golden card (0-00) and the Stage 0 cards (0-01 to 0-15),
  each with its role, what to read, its done-when and its true state.
- costs.md -- the first line of the bill (Part 11, 11.7).
- machines/desktop.md -- the desktop survey, plus the disk cleanup.
- config/pins -- every version, one file, both PCs, never "latest".
  PHP is two lines (8.3 desktop, 8.4 laptop, as Part 01, 1.8 allows);
  Syncthing is 2.1.7 (Nir chose it); the line's Python is 3.13.14.
- line/ -- the real Python project uv owns: "uv run am doctor" works.
  It reports the versions against the pins, the ports, Moodle, Git,
  Syncthing, the newest hand-over and free space; every failure is one
  plain sentence with what to do. No outside library is used.
- hosting/install/owner-setup.sh -- the one setup script. Written and
  syntax-checked; an agent never runs it. PHP + MariaDB + Syncthing 2.1.7
  from Syncthing's own repository; NOT Moodle; touches no live site.
- hosting/attract-mode.caddy + one import line in hosting/Caddyfile --
  our block. Ports are the Bible's (Part 01, 1.4): 8084 is Attract Mode's,
  and "pre" is the tunnel pointing at 8081, with no door of its own.
- The folders of Place 1, and /home/nir/attract-mode-files/ with its nine
  folders (voice/ is 700). WORKFLOW-2026-11-28.md is the dated log.
- Disk: / has 60 GB free; the Ollama models are on /home (D77).

WHAT WORKS
- "uv run am doctor" runs and prints a true report. It ends with three
  real failures: PHP, MariaDB and Syncthing are not installed yet, because
  that is Nir's owner-setup act (card 0-15).
- Nothing else of Attract Mode is installed or running; Caddy and
  cloudflared are NOT running on this PC, so the block is validated but
  not loaded. The live site answered Cloudflare 1033 (no tunnel) when
  checked; Nir said not to worry about it for a few hours.
- Crystal Balls and the live website were not touched and still work.

WHAT COMES NEXT (the Bible's order)
1. Nir runs owner-setup on the desktop (O1), then "am doctor" again.
2. The laptop: its survey (0-03), the same folders (0-05), owner-setup.
3. Syncthing's two-way test file, then O2: "pre" at Cloudflare, pointing
   at 127.0.0.1:8081 on the serving PC.
4. The fold check of Part 00 by a different model, and the tag bible-v1
   (0-13) -- no tag and no record of the check exist.
5. Then Stage 0's done-means of Part 01, 1.13.

WHAT IS WAITING FOR NIR
- O1: run owner-setup on each PC, typing his own password (card 0-15).
- O2: add "pre" at Cloudflare and its tunnel entry (card 0-14).
- The laptop, switched on in Linux, for its survey and folders.
- Card 0-13: was the Part 00 fold check ever done, and by which model?
- D64: the price of a Co-op hour.
- Whether to start Caddy and the tunnel on this PC at all, and when.
