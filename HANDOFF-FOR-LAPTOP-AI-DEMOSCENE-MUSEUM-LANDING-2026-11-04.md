# HANDOFF FOR THE LAPTOP AI: DEMOSCENE MUSEUM LANDING PAGE WAS NEVER SERVED (4 Nov 2026)
Written by Claude Sonnet 5.5 on Nir's desktop-linux (Linux Mint 22). Nir is NOT your messenger:
read this yourself after `git pull`, do only what it says, emojis on every line to Nir, short messages,
the important thing LAST. Never use `pkill -f`. Never say "live" before checking the real URL.

## WHAT WAS WRONG (found today, same disease as Second Opinion)
The Demoscene Museum has TWO parts and Nir's design is fixed, do not change it:
1. The LANDING PAGE (the 13-page comic "The Real-Time Machine", 44 MB) lives in THIS repo,
   `strulovitz-website/demoscene-museum/` (index.html + images/comic/page-01..13.jpg). It stays here.
2. The MUSEUM itself lives in its own repo `strulovitz/demoscene-museum` (museum/, exhibits/,
   shared/, bible/), cloned on each serving computer at `~/demoscene-museum`.
The Caddy rule for `/demoscene-museum/*` (written 3 Nov) pointed ONLY at the museum clone, so
the comic was pushed to GitHub but never reachable: live `/demoscene-museum/images/comic/page-01.jpg`
returned 404 and the page still showed the old placeholder. Nobody checked the live URL.

## WHAT I CHANGED (commit d28ff3e, pushed): hosting/Caddyfile
`handle_path /demoscene-museum/*` now: if the requested file (or its index.html) exists in
`{$HOME}/strulovitz-website/demoscene-museum`, serve it from there (the comic wins); otherwise
serve from `{$HOME}/demoscene-museum`. Validated with `caddy validate`, Caddy restarted on the
desktop, and verified over the real internet (all 200): `/demoscene-museum/` shows the comic,
`/images/comic/page-13.jpg`, `/museum/`, `/exhibits/space-debris/original/space_debris.mod`.

## WHAT YOU DO ON THE LAPTOP, IN ORDER
1. `git -C ~/strulovitz-website pull`
2. If `~/demoscene-museum` does not exist: `git clone https://github.com/strulovitz/demoscene-museum.git ~/demoscene-museum`
   else `git -C ~/demoscene-museum pull`. (Also `~/crystal-balls` must be cloned and current: the same
   Caddyfile serves `/crystal-balls/*` from `~/crystal-balls/public`.)
3. `systemctl --user restart site-caddy.service` (ONLY if the laptop is the one serving; never run
   both tunnels at once, run `sites-off` on the other PC first).
4. Check on the laptop's own port 8081: `/demoscene-museum/` (grep "Real-Time Machine"),
   `/demoscene-museum/images/comic/page-01.jpg` (200), `/demoscene-museum/museum/` (200).
5. FIX THE ROOT CAUSE so this cannot happen again, as general code, not a one-off:
   a. Make `hosting/bin/sites-on` pull EVERY repo the Caddyfile serves from (strulovitz-website, Anime,
      peaktogether-website, second-opinion, demoscene-museum, crystal-balls), cloning any that are
      missing; a failure prints a loud warning but does not stop the other sites.
   b. Add `hosting/bin/sites-check`: reads the menu links of the root `index.html` and every
      project landing page's links, requests each one on 127.0.0.1:8081 (and optionally the
      public URL) and prints every link that is not 200. `sites-on` runs it at the end.
   c. Add to `hosting/README.md` a short section "A page is not done until its live URL is
      checked": menu item, landing page and the project's own site must each be fetched over the
      real internet (`curl` + a headless-Chrome look) before anyone tells Nir it works.
   Commit and push each step, then tell Nir the real results.

## ONE MORE THING YOU MUST KNOW (Nir said page 1 of the comic looked invisible)
On a fresh load the first image is fine: a real Chrome measured it at 1024 px natural width, 455x682
on screen, nothing covering it, and it sits BELOW the title block (about 536 px down on a phone-sized
window, so you must scroll). Cloudflare answers 200 with `cache-control: public, max-age=14400`
(4 hours). The likely cause is Nir's browser keeping the earlier 404 for page-01 (the only image
loaded eagerly while the file was still 404). A hard reload or a private window shows it. If Nir still
does not see it after that, ask him for a screenshot, do not guess.
