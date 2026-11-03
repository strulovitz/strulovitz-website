================================================================================
LAUNCHING THE DEMOSCENE MUSEUM ON THE SERVING COMPUTER (2026-11-03)
================================================================================

Written by Nir's OpenCode agent on the old Windows 10 PC, after the work was
already committed and pushed to GitHub. The agent on the computer that serves
www.strulovitz.org (one of the two gaming PCs, via Cloudflare Tunnel) does the
steps below. Read hosting/README.md first if you have never served before.

WHAT CHANGED ON GITHUB (already pushed, nothing to build by hand)
- strulovitz/strulovitz-website, commit f1a7f09 (+ this file's commit):
    * the menu on all 22 root pages gained one item, between Vibe Invention
      and About:  <li><a href="/demoscene-museum/">Demoscene Museum</a></li>
    * PROJECTS-AND-MENU.md gained item 9 documenting it
    * hosting/Caddyfile gained a handle_path block serving /demoscene-museum/*
      straight from the clone at {$HOME}/demoscene-museum (same pattern as
      Crystal Balls), plus a /demoscene-museum -> /demoscene-museum/ redirect
- strulovitz/demoscene-museum, commits 3148303 and 77e8088:
    * the whole museum: museum/ (raycaster + music pillar), exhibits/
      (tube, plasma, space-debris with the Space Debris MOD), shared/, bible/
    * a placeholder front page index.html whose very first element is the
      prominent ENTER-THE-MUSEUM link; Fable's real introduction page will
      replace it later
    * exhibits/space-debris/README.md: the song is Captain's (Markus
      Kaarlonen's) copyrighted work, included with credit and a link to
      https://markuskaarlonen.com/space-debris . Do not remove that credit.

WHAT TO DO ON THE SERVING COMPUTER, IN THIS ORDER
1.  cd ~/strulovitz-website && git pull
2.  If ~/demoscene-museum does not exist yet:
        git clone https://github.com/strulovitz/demoscene-museum ~/demoscene-museum
    If it exists:  cd ~/demoscene-museum && git pull
3.  Rebuild the export so the menu pages change:
        python3 ops/build-export.py
    (sites-on also does this when it detects site source changes.)
4.  Restart Caddy so it reads the new Caddyfile:
        systemctl --user restart site-caddy.service
5.  Check, all on the serving machine itself:
        curl -s http://127.0.0.1:8081/hosted-by                 (still answers)
        curl -s http://127.0.0.1:8081/demoscene-museum/          (placeholder page)
        curl -s http://127.0.0.1:8081/demoscene-museum/museum/   (the walkable museum)
        curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8081/demoscene-museum/exhibits/space-debris/original/space_debris.mod   (200)
        curl -s http://127.0.0.1:8081/ | grep Demoscene          (menu item present)
    Then open https://www.strulovitz.org/demoscene-museum/ in a browser,
    click ENTER, press any key, and hear Space Debris.

RULES THAT STILL APPLY
- Never run both tunnels at the same time (hosting/README.md). If switching
  computers: sites-off on the old one first.
- Do not run the FTP deploy scripts; they belong to a retired hosting setup.
- Only the serving computer needs ~/demoscene-museum. The other gaming PC can
  clone it too so it is ready when it takes over; until then it serves nothing.

IF SOMETHING IS WRONG
- Rollback of the menu: git revert the menu commit in ~/strulovitz-website,
  run python3 ops/build-export.py again. That is the whole rollback; the
  museum subpath can also simply stay, it harms nothing.
- If /demoscene-museum/ answers 404: the clone is missing or not at
  {$HOME}/demoscene-museum (check with: echo $HOME), or Caddy was not
  restarted.
