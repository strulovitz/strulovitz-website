ATTRACT MODE -- STATE

Read this first, after Part 00. One page. Rewritten, not appended to, at
the end of every session: what exists, what works, what comes next, and
what is waiting for Nir.
Last rewritten: 2026-11-28, desktop-linux.

WHAT EXISTS
- bible/ -- 12 files. Read in full; laws.md matches Part 11, section 11.8.
- DECISIONS.md -- D1 to D77. Only D64 is open.
- machines/desktop.md -- the desktop survey (Part 01, 1.5), including the
  disk cleanup Nir approved on 2026-11-28.
- config/pins -- every version number, one file, both PCs, never "latest".
  Syncthing is 2.1.7, chosen by Nir on 2026-11-28 (option A of two real
  choices); the reason is written under the pin.
- hosting/install/owner-setup.sh -- THE one setup script (Part 01, 1.9).
  Written and syntax-checked; an agent never runs it. It installs PHP and
  MariaDB, and Syncthing only when its pin is a real number. It does NOT
  install Moodle (Stage 2 on the desktop, Stage 3 on the laptop) and does
  not touch Caddy, the live websites or Apache.
- Seven empty folders for later steps: config/ (holds the pins), vault/,
  research/, levels/, line/, hosting/, public/.
- WORKFLOW-2026-11-28.md -- the dated running log.
- handoffs/ -- notes between agents, dated. kits/ -- the kits.
- /home/nir/attract-mode-files/ -- nine empty folders for the big files:
  books, footage, masters, sessions, handover, raw, packages, voice, work.
  voice/ is mode 700. This folder never goes into Git.
- Disk: / has 61 GB free. The Ollama models (19 GB) live on /home at
  /home/ai-models/ollama/models (D77).

WHAT WORKS
- Nothing is installed or running for Attract Mode yet: no PHP, no
  MariaDB, no Moodle, no Syncthing, no Obsidian, no Caddy change. The setup
  script exists but has never been run.
- The two PCs are not joined yet. The laptop has not been surveyed.
- Untouched and still working: the live website, and Crystal Balls (its
  own check, python -m pipeline.common --ping, exit 0).

WHAT COMES NEXT (the Bible's order)
1. hosting/attract-mode.caddy, plus the ONE import line in hosting/Caddyfile
   (Part 01, 1.9, item 6). Validate, reload (never restart), sites-check.
2. line/ -- the am command with am doctor (Part 01, 1.10).
3. Nir runs owner-setup once on each PC (O1).
4. Nir adds the name "pre" at Cloudflare (O2).
5. The checks of Part 01, section 1.13.

WHAT IS WAITING FOR NIR
- The laptop survey (Part 01, 1.5): needs the laptop on and connected.
- O1: run owner-setup on each PC, typing his own password.
- O2: add "pre" at Cloudflare.
- D64: the price of a Co-op hour.
- The fold check of Part 00 by a different model (11.10 and 11.12, item 5).
