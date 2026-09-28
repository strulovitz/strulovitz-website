# REPORT FOR CLAUDE (2026-09-28)

**Task 1:** Corrected instructions saved verbatim and pushed in `hosting-migration/2026-09-28-claude-corrected-instructions.md`. No earlier saved Claude prompt mentioned WordPress, so no superseded note was necessary.

**Task 2:** `~/websites/` does not exist; the two empty folders briefly created from the earlier instructions were already removed. `find /home/nir -maxdepth 6 -name .git -prune` found these paths and origin URLs:

```text
/home/nir/MadHoney/.git                  https://github.com/strulovitz/MadHoney.git
/home/nir/claude-memory/.git              https://github.com/strulovitz/claude-memory.git
/home/nir/TheDistributedAIRevolution/.git https://github.com/strulovitz/TheDistributedAIRevolution.git
/home/nir/HoneycombOfAI/.git              https://github.com/strulovitz/HoneycombOfAI.git
/home/nir/Anime/.git                      https://github.com/strulovitz/Anime.git
/home/nir/Anime/tools/ComfyUI/.git        https://github.com/comfyanonymous/ComfyUI.git
/home/nir/Anime/tools/sd-scripts/.git     https://github.com/kohya-ss/sd-scripts.git
/home/nir/peaktogether-website/.git       https://github.com/strulovitz/peaktogether-website.git
/home/nir/.openclaw/workspace/.git        [no origin]
/home/nir/GiantHoneyBee/.git              https://github.com/strulovitz/GiantHoneyBee.git
/home/nir/strulovitz-website/.git         https://github.com/strulovitz/strulovitz-website.git
/home/nir/clawd/.git                      [no origin]
/home/nir/.cache/uv/sdists-v9/.git        [invalid gitfile; not a valid checkout]
/home/nir/.cache/uv/git-v0/db/c009e92165a1dae1/.git [internal cache; no origin]
/home/nir/strulovitz/.git                 https://github.com/strulovitz/strulovitz.git
```

No duplicate origin URLs among the Git checkouts, so there are no duplicate last-commit/status/unpushed details to report. Existing untracked files in `~/Anime` were not touched; the other two website repositories matched their upstream branches when checked.

**Task 3:** Live home page versus local GitHub source: Learnime is byte-identical (SHA-256). Peak Together is identical after ignoring CRLF versus LF line endings. Strulovitz differs only in three deploy-time links: source uses `VERSION_FALLBACK/`, live uses `v2026-09-11-c/` for two tesseract links and `build-health.html`. The home-page internal `href`/`src` check found 38/38 present for Learnime and 13/13 for Peak Together. Strulovitz had 47/54 references present under `site/`, with **four distinct paths absent from `site/`**: `/ghost/index.html` and `/hive/index.html` exist elsewhere at repository-root `ghost/index.html` and `hive/index.html`; `v2026-09-11-c/tesseract.html` and `v2026-09-11-c/build-health.html` are live but absent under `site/` (the VR query uses the same tesseract file). The repo's `ops/build-export.py` builds the versioned export and `pointer.json`; `exports/` currently contains only `.gitkeep`. No live files were downloaded or modified. This check covers the three live home pages' HTML attributes, not every page/site asset.

**Task 4:** Working website folders: `~/strulovitz-website/site/` 918 MB, `~/Anime/learnime-site/` 177 MB, `~/peaktogether-website/` 463 MB excluding `.git`. No website file exceeds 50 MB. No `.wasm`, `.glb`, `.gltf`, `.mjs` or `.webm` found. Strulovitz has 9 `.json` galaxy files; Peak Together has JSON for game content; Learnime has none. Learnime has four `.mp4` songs; Peak Together has five `.mp4` game clips. Serve JSON as `application/json`, MP4 as `video/mp4`, and the JS module as JavaScript.

- Strulovitz: local `site/vendor/three.module.min.js`, ES module `site/src/vr/main.js` (`<script type="module">`), WebXR via `navigator.xr`; browser fetches local `pointer.json` and `data/galaxies/*.json` plus reading pages. No CDN needed for Three.js. `ops/build-export.py`, `ops/deploy.sh`, `ops/deploy_windows.py`, and `pipeline/*.py` are build/deployment/content-production tools, not web-server runtime code.
- Learnime: local `gallery.js` and HTML/CSS/images/media; no CDN, module, or local JSON fetch found in the website folder. `Anime/tools/` has scripts for ComfyUI, image training, and setup, not website runtime. Nested ComfyUI and sd-scripts are their own local Git checkouts, not duplicate Anime copies.
- Peak Together: `components.js` fetches local `/header.html` and `/footer.html`; MathJax is loaded from `cdn.jsdelivr.net`, and five arcade videos use the jsDelivr GitHub CDN. The site has `.htaccess` for directory-index/rewrite/cache headers and to force `.py` files to download (not execute as CGI). `homeworld/`, `descent/`, `loom/`, and others contain Python desktop-game/compiler/demo/test code, not code required to serve the static website.
- `git lfs ls-files` could not run: Git LFS is not installed. No tracked `.gitattributes` in these three repos and no LFS pointer signature found in site files, but LFS use cannot be conclusively ruled out with the missing command.

**Task 5:** Debian GNU/Linux 13.6 (trixie), host `deb-server`, user `nir`; `/` and `/home` on `/dev/sda4` ext4 (USB P40 Game Drive), 1.8 TB total, 262 GB used, 1.4 TB free. `/home/nir` permissions `700`, owner `nir`. On PATH: git, curl, wget, rsync, python3; not on PATH: cloudflared, nginx, caddy, apache2 (Apache service nevertheless installed and active). No cloudflared unit or `/etc/cloudflared` / `~/.cloudflared` directory; no config contents to report. nginx/caddy inactive. Unprivileged `ss` showed listeners on 80, 22, 631 (loopback), 11434 (loopback), 1716, 18789 (loopback); none on 443 or 8080-8090. Apache serves port 80. Privileged process ownership and firewall rules **not verified**; `ufw` command is missing. Effective logind defaults suspend when the lid closes (also on AC); idle action is ignore. No packages, services, config files, Windows partitions or existing Cloudflare setup were changed.
