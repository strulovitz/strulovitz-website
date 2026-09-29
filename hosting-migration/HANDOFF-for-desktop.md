HANDOFF FROM CLAUDE (laptop session) TO CLAUDE (desktop session). Read it all before answering.

## Who and how
- User: Nir Strulovitz (GitHub: strulovitz). Complete beginner in Linux, has ADD. Needs: max 2 steps at a time, copy+paste boxes, pitfall warnings, milestones, screenshots welcome. He is tired of this project, so be brief and kind.
- He wants to SAVE MONEY: keep your answers short, keep worker prompts compact and ask for short reports (the worker's context gets expensive).
- You are the manager. The worker is "GPT 6 Sol" running in OpenCode on the Desktop. Nir pastes your prompts to it and pastes the reports back to you.
- Nir does not want security lectures. Still: NEVER commit the tunnel token anywhere (the repos are public).
- HARD RULES for the worker: don't touch Windows or NTFS partitions; don't break existing installs; no apt upgrade/full-upgrade; no new top-level project folders; GitHub is the single source of truth; exactly ONE local clone of each repo per OS (if duplicates exist, report them, don't delete); never run ops/deploy.sh or ops/deploy_windows.py (old DreamHost upload scripts).
- VERIFIED FACTS (don't re-question them): all 3 sites are 100% static (HTML/CSS/JS/images/JSON/MP4). NO WordPress, NO database. (Once I wrongly claimed WordPress and it upset Nir badly. Don't repeat that.)

## Goal
Host 3 static websites from Nir's home PCs via ONE Cloudflare Tunnel. Only ONE PC hosts at a time, and he can choose which one: laptop (Debian 13, hostname deb-server, user nir) or Desktop (Linux Mint 22). Both run Linux from external WD_Black P40 drives (dual boot with Windows 11).

## Sites and repos (the laptop paths; Desktop paths may differ, check them)
- strulovitz.org  -> repo strulovitz-website, built output served from exports/ (build: python3 ops/build-export.py; creates exports/vYYYY-MM-DD-x/, pointer.json, exports/current symlink, ops/pointers/pointer-*.json which IS tracked by git). Also serves repo-root ghost/ and hive/. Old links /v2026-09-11-c/* are mapped to exports/current.
- learnime.com    -> repo Anime, folder learnime-site/
- peaktogether.me -> repo peaktogether-website (root). Its .htaccess rules were replicated in Caddy (dir slash redirect, .py served as text/plain download, cache headers).

## State at the end of the laptop session
- Domains: added to Cloudflare Free (nameservers lia/stanley.ns.cloudflare.com), all 3 ACTIVE. The registrar transfer DreamHost -> Cloudflare was paid and is pending; it completes automatically around 2026-10-02 (DreamHost emails say "no response needed"; the links in them are for CANCELLING, so don't click). peaktogether.me did NOT get a DreamHost email; check it in Cloudflare -> Domains -> Transfers. Until the transfer completes: don't re-lock, don't edit contacts at DreamHost, don't close DreamHost. After it completes (check Domains -> Registrations), Nir may close DreamHost (the other 7 domains there he doesn't need).
- Laptop: Caddy v2.11.4 at ~/.local/bin/caddy (official binary, not apt, because the Debian package would fight the leftover Apache on :80). cloudflared 2026.9.3 from Cloudflare's apt repo (no "service install", no "tunnel login").
- All hosting config is in the repo strulovitz-website/hosting/: Caddyfile (uses {$HOME} paths; :8081 strulovitz, :8082 learnime, :8083 peaktogether, bind 127.0.0.1, auto_https off, hidden paths and root *.md blocked, /hosted-by marker prints the hostname), systemd USER units (site-caddy, site-tunnel, site-nosleep; symlinked into ~/.config/systemd/user, NOT enabled at boot), scripts in hosting/bin/ symlinked into ~/.local/bin: sites-on / sites-off / sites-status, plus README.md. Docs and saved prompts are in hosting-migration/.
- Tunnel: remotely managed tunnel "home-sites" (ID 7f6afc07-75e6-4a42-ab93-da2dde893e42). The token lives OUTSIDE the repos at ~/.config/site-hosting/tunnel-token (dir 700, file 600). site-tunnel runs: cloudflared tunnel --no-autoupdate run --token-file ...
- Public routes (in the dashboard, part of the tunnel, so they are SHARED by both PCs): apex + www of each domain -> http://127.0.0.1:8081 / 8082 / 8083. The old DreamHost A records for apex/www were deleted. (Nir may tell you if some domain wasn't finished; the check is https://DOMAIN/hosted-by -> "Served by <hostname>".)

## Desktop plan (do it in this order, one worker prompt per phase)
1. READ-ONLY inspection: OS, hostname, username, $HOME, ~/.local/bin in PATH?, which git curl python3 cloudflared caddy nginx apache2; ports 8081-8083 and 2019 must be FREE (the routes are shared, so the ports MUST be the same as on the laptop; if one is taken, STOP and report); find existing clones of strulovitz-website, Anime, peaktogether-website (find ~ -maxdepth 4 -name .git), with their paths, remotes and git status; Anime repo size before any clone; sleep/suspend settings (Cinnamon power + logind), read-only.
2. Repos: git pull --ff-only the existing clones; clone only the missing ones into $HOME. If the existing clones live in OTHER paths, do NOT move or re-clone them: make the Caddyfile/units path-configurable (e.g. EnvironmentFile ~/.config/site-hosting/paths.env, with defaults equal to the laptop paths so the laptop keeps working unchanged). Any change to the shared hosting/ files must stay compatible with the laptop.
3. Install: Caddy official binary into ~/.local/bin (verify the checksum); cloudflared via Cloudflare's apt repo (Mint 22 = Ubuntu 24.04 base; "https://pkg.cloudflare.com/cloudflared any main", keyring /usr/share/keyrings/cloudflare-main.gpg). Build strulovitz (python3 ops/build-export.py; commit the new ops/pointers file). Link the units and scripts exactly as hosting/README.md says. Start ONLY site-caddy and test locally (homepages, /hosted-by, /.git/config -> 404).
4. Token: Nir gets the same token from Cloudflare -> Networking -> Tunnels -> home-sites -> Edit/Configure (the install command shows the token starting with "eyJ"; copy only that part). The worker saves it through a private dialog (not in chat, not in the repo) into ~/.config/site-hosting/tunnel-token, 600.
5. Switch test: on the LAPTOP Nir runs sites-off. Then on the Desktop, sites-on. Check https://strulovitz.org/hosted-by (and the other 2) in a private window -> must show the DESKTOP hostname. Then Nir chooses which PC stays on.

## Pitfalls
- NEVER run both PCs at the same time: each PC builds its own strulovitz version folder, so load-balancing between them breaks pages. The switch is always: sites-off on the old PC, then sites-on on the new PC.
- PCs in Windows, asleep or off = sites offline. That's acceptable for Nir.
- Use 127.0.0.1, not localhost, in routes. Don't use "http://127.0.0.1:8081" as a Caddy site address (the Host header would mismatch); use ":8081" + bind.
- In Cloudflare DNS, the leftover ftp/mysql/ssh A records point to DreamHost; they're harmless and can be deleted after October 2.  
