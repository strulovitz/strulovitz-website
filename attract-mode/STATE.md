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
  MariaDB, and Syncthing 2.1.7 from Syncthing's own repository (channel
  chosen from the pin's major version). It does NOT install Moodle (Stage 2
  on the desktop, Stage 3 on the laptop) and does not touch Caddy, the live
  websites or Apache.
- hosting/attract-mode.caddy -- our block (Part 01, 1.9, item 6). The
  ports are the Bible's (Part 01, 1.4): 8084 belongs to Attract Mode
  (Moodle, from Switch Day), and "pre" is simply the tunnel pointing at
  127.0.0.1:8081 -- it needs no door of its own. The block reserves
  127.0.0.1:8084 and answers a plain sentence there until Moodle arrives.
  An earlier version gave 8084 to "pre"; corrected the same day (step 5d).
- hosting/Caddyfile -- one import line added at the end. Nothing else
  changed. Validated with "caddy validate"; the adapted config shows the
  three live blocks untouched.
- Seven folders for later steps: config/ (holds the pins), vault/,
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
  MariaDB, no Moodle, no Syncthing, no Obsidian. The setup script exists
  but has never been run.
- Caddy and cloudflared are NOT running on this PC (verified 2026-11-28:
  no process, nothing listening on 8081-8084). The live site answered
  Cloudflare "error 1033" (tunnel not connected) at that check. Nobody
  started or reloaded anything: that is Nir's decision.
- The two PCs are not joined yet. The laptop has not been surveyed.
- Crystal Balls is untouched and still passes its own check.

WHAT COMES NEXT (the Bible's order)
1. line/ -- the am command with am doctor (Part 01, 1.10).
2. Nir runs owner-setup once on each PC (O1).
3. Nir adds the name "pre" at Cloudflare, plus the tunnel entry that points
   it at 127.0.0.1:8084 on the serving PC (O2).
4. The checks of Part 01, section 1.13.

WHAT IS WAITING FOR NIR
- Whether to start Caddy and the tunnel on this PC at all, and when; the
  live site is currently not answering (Cloudflare 1033).
- The laptop survey (Part 01, 1.5): needs the laptop on and connected.
- O1: run owner-setup on each PC, typing his own password.
- O2: add "pre" at Cloudflare and its tunnel entry.
- D64: the price of a Co-op hour.
- The fold check of Part 00 by a different model (11.10 and 11.12, item 5).
