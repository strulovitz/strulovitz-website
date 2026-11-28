ATTRACT MODE -- STATE

Read this first, after Part 00. One page. Rewritten, not appended to, at
the end of every session: what exists, what works, what comes next, and
what is waiting for Nir.
Last rewritten: 2026-11-28, laptop-linux (Debian 13).

WHAT EXISTS
- bible/ -- 12 files, 7,191 lines. Read IN FULL on the laptop on
  2026-11-28 as well as on the desktop; laws.md matches Part 11, 11.8.
- DECISIONS.md -- D1 to D79. Only D64 (the Co-op price) is open.
- tasks/ -- the golden card and the Stage 0 cards. Now done: 0-01, 0-02,
  0-03, 0-04, 0-05, 0-06, 0-07, 0-08, 0-09, 0-11, 0-12, 0-15.
  Waiting for Nir: 0-10 (Syncthing pairing), 0-14 (pre at Cloudflare).
  Open: 0-13 (Part 00 fold check and the tag bible-v1).
- machines/desktop.md and machines/laptop.md -- both surveys, written
  read-only. The laptop: Debian 13, 1.1 TB free, 8084 free, Apache active
  and left alone.
- config/pins -- one file, never "latest". PHP, uv and ffmpeg are now
  per PC (D79): PHP 8.3/8.4, uv 0.12.0/0.12.1, ffmpeg 6.1.1/7.1.5.
  Moodle 5.3, MariaDB 11.8 series and the line's Python 3.13.14 are the
  same on both.
- line/ -- the real uv project. "uv run am doctor" works and prints the
  versions, ports, Moodle, Git, Syncthing, the hand-over and free space.
  17 self-checks pass, including the per-PC pin rule.
- hosting/install/owner-setup.sh -- the one setup script, now following
  D78 in its comments too. hosting/attract-mode.caddy + one import line
  in hosting/Caddyfile: our block, 8084 reserved, nothing public yet.
- Place 1 on both PCs; Place 3 on the laptop at
  /home/nir/attract-mode-files/ with its nine folders (voice/ is 700).
- costs.md has the bill line; WORKFLOW-2026-11-28.md has the dated log.

WHAT WORKS
- DESKTOP: PHP 8.3.6, MariaDB 11.8.10, Syncthing 2.1.7. It reported no
  failures before the pins were split per PC; after a pull its own lines
  match, and the desktop agent is asked to confirm "am doctor" again.
- LAPTOP (this PC), installed on 2026-11-28 by owner-setup on Nir's word
  (D78): PHP 8.4.28, MariaDB 11.8.9 (listens on 127.0.0.1:3306 only),
  Syncthing 2.1.7. "am doctor" passes every pin; the only failure before
  the commit was the uncommitted files, which that commit ends.
- Syncthing runs as a user service on the laptop and answers on
  127.0.0.1:8384. It knows no other PC yet: the pairing is Nir's click.
- Moodle is NOT installed anywhere, on purpose (desktop Stage 2, laptop
  Stage 3). Caddy and cloudflared are not running here; the live site
  answered Cloudflare 1033 when last checked. Apache was not touched.
- No compile, no PPA and no third-party ffmpeg: by D79 each Linux keeps
  its own 6.1.1 / 7.1.5.

WHAT COMES NEXT (the Bible's order)
1. Syncthing's pairing and the two-way test file (card 0-10).
2. O2: add "pre" at Cloudflare and check it (card 0-14).
3. The Part 00 fold check by a different model, then the tag bible-v1
   (card 0-13).
4. That completes Part 01, section 1.13 -- Stage 0 done.
5. Then Stage 1, "something to show": the first Making Of (Part 11, 11.4).

WHAT IS WAITING FOR NIR
- Syncthing: two clicks, one on each PC, to accept the other, then the
  test file must travel BOTH ways.
- O2: add "pre" at Cloudflare and its tunnel entry.
- Card 0-13: was the Part 00 fold check ever done, and by which model?
- D64: the price of a Co-op hour.
- Whether and when to start Caddy and the tunnel on either PC.
- A separate, pre-existing apt warning on the laptop: the GitHub CLI
  repository (cli.github.com) fails signature verification because a key
  is missing. It is not ours and blocks nothing; fix it only if Nir asks.
