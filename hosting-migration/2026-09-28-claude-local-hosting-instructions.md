# Claude local hosting instructions (verbatim, 2026-09-28)

```text
From Claude (manager). Excellent report. Nir approved installs. We now IMPLEMENT local hosting on this laptop (no tunnel yet). Save this prompt as a dated .md in hosting-migration/ like before.

STILL FORBIDDEN: touching Apache (leave it running on :80), Windows/NTFS partitions, other repos' content, apt upgrade/full-upgrade, editing system-wide logind/power config. Never commit secrets. No new top-level folders in /home/nir. If sudo needs a password, give Nir the command.

DESIGN (same on Debian 13 laptop and later Linux Mint 22 desktop):
- Caddy serves 3 sites on 127.0.0.1 only: 8081=strulovitz.org, 8082=learnime.com, 8083=peaktogether.me. First verify these ports are free.
- Later, ONE Cloudflare Tunnel (token-based, created in the dashboard) runs on whichever PC is "on" and sends traffic to these ports.
- All hosting config lives in the repo: /home/nir/strulovitz-website/hosting/ (repo root, NOT inside site/). Use {$HOME} in configs, not /home/nir, because the desktop username may differ.
- The tunnel token will live OUTSIDE the repo at ~/.config/site-hosting/tunnel-token (chmod 600). Add a .gitignore safeguard.

STEP 1 - Install:
a) cloudflared from Cloudflare's official apt repo (per developers.cloudflare.com docs: keyring in /usr/share/keyrings/cloudflare-main.gpg, source line "https://pkg.cloudflare.com/cloudflared any main"). Do NOT run "cloudflared service install" or "cloudflared tunnel login".
b) Caddy as the official static binary into ~/.local/bin/caddy (download from github.com/caddyserver/caddy releases, verify its checksum). Do NOT apt install caddy: the Debian package auto-starts a system service on :80, which conflicts with Apache.
c) Git LFS is NOT needed unless you found LFS usage; skip it.
Report the installed versions.

STEP 2 - strulovitz build: run "python3 ops/build-export.py" in /home/nir/strulovitz-website. Do NOT run deploy.sh or deploy_windows.py, ever. Report the version folder created. Do not commit the untracked ops/pointers/ file; report it and I'll decide. Also report whether build-export.py accepts a version argument.

STEP 3 - hosting/Caddyfile with these requirements:
- Global options: auto_https off; admin endpoint on localhost only (the default is fine).
- IMPORTANT PITFALL: use site addresses like ":8081" with "bind 127.0.0.1". Do NOT use "http://127.0.0.1:8081" as a site address, or Caddy will reject requests whose Host header is strulovitz.org (which is what the tunnel sends).
- 8081: root = {$HOME}/strulovitz-website/exports. Also serve /ghost/* and /hive/* from the repo root's ghost/ and hive/ folders. Make old links /v2026-09-11-c/... keep working (e.g. rewrite to the current version folder). Consider how that rewrite stays correct after future builds and explain your choice.
- 8082: root = {$HOME}/Anime/learnime-site
- 8083: root = {$HOME}/peaktogether-website. Replicate the needed .htaccess behavior: trailing-slash redirect for directories plus index.html (check that Caddy's file_server does this by default). Serve .py files as a download/plain text, never executed. Add the cache headers (images 30 days, css/js 7 days).
- ALL sites: block hidden paths (/.git, /.htaccess, /.github, any /.*), and block *.md files that sit in a repo root.
- Correct MIME types: .js/module = text/javascript, .json, .mp4 with range requests (Caddy handles this by default; verify it).
- Run "caddy validate" and "caddy fmt" on the file.

STEP 4 - systemd USER units (in hosting/systemd/, installed into ~/.config/systemd/user/ as symlinks; NOT enabled at boot):
- site-caddy.service: runs caddy with hosting/Caddyfile, Restart=on-failure.
- site-tunnel.service: runs "cloudflared tunnel --no-autoupdate run --token-file %h/.config/site-hosting/tunnel-token" (check that the installed cloudflared version supports --token-file; if not, use an EnvironmentFile with TUNNEL_TOKEN). Create it but do NOT start it yet (there is no token yet).
- site-nosleep.service: holds "systemd-inhibit --what=sleep:handle-lid-switch --why='Hosting websites' sleep infinity" while hosting. Test whether it works without root for the logged-in user and report.
- Scripts in hosting/bin/, symlinked into ~/.local/bin/: sites-on (git pull the 3 repos with --ff-only, rebuild strulovitz if its source changed, start caddy + tunnel + nosleep), sites-off (stop all three), sites-status (show what is running + curl -sI each local port). They must print clear, beginner-friendly messages. Refuse to start the tunnel if the token file is missing, and tell Nir that plainly.
- hosting/README.md: a beginner guide (what each command does, how to switch computers).

STEP 5 - Test locally (start only site-caddy for now):
- curl every port: the homepage plus at least 10 internal pages/assets per site (tesseract.html, the v2026-09-11-c/ old link, /ghost/, /hive/, the learnime gallery images, a peaktogether folder URL without a trailing slash, a .json, a .mp4 range request, a .py file). Also confirm /.git/config returns 403/404 on every port.
- Compare the homepage bytes with the live site for all 3.
- Tell Nir to open http://127.0.0.1:8081, :8082 and :8083 in Firefox on this laptop and check that the pages look right.

STEP 6 - Commit + push the hosting/ folder (make sure no token is in the repo). Leave caddy running.

FINISH with "REPORT FOR CLAUDE": versions, the Caddyfile content, test results table, anything that failed or that you had to decide yourself, and the exact commands Nir will type.
```
