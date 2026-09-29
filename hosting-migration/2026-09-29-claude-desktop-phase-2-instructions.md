Phase 2 (Desktop, mint-desktop). Same HARD RULES as before. Also: do NOT start site-tunnel, do NOT create the token file, do NOT enable anything at boot, do NOT run install-launchers yet.

1. Repos: `git pull --ff-only` in ~/strulovitz-website, ~/Anime, ~/peaktogether-website. In strulovitz-website, leave the 3 pre-existing local changes alone (don't commit, don't discard); report their file names.
2. cloudflared, make it match the laptop:
   a. Read-only check: `dpkg -S /usr/local/bin/cloudflared`, `systemctl status cloudflared`, `systemctl --user status cloudflared`, `ps aux | grep [c]loudflared`, `ls -la /etc/cloudflared ~/.cloudflared`.
   b. If any cloudflared service/process is running or enabled: STOP step 2 and report it. Change nothing.
   c. Otherwise: if dpkg owns it, `sudo apt remove cloudflared` (NOT purge). If not, rename it: `sudo mv /usr/local/bin/cloudflared /usr/local/bin/cloudflared.old-2026.3.0`. Leave ~/.cloudflared and /etc/cloudflared untouched.
   d. Install from Cloudflare's apt repo like the laptop: keyring /usr/share/keyrings/cloudflare-main.gpg, source "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main", then `sudo apt update && sudo apt install cloudflared` (only that package, no upgrades).
   e. Verify: `hash -r; which cloudflared` -> /usr/bin/cloudflared, and report `cloudflared --version`.
3. Caddy: install the official v2.11.4 linux amd64 binary into ~/.local/bin/caddy and verify its checksum against the official release checksums file.
4. Build: `cd ~/strulovitz-website && python3 ops/build-export.py`. Commit and push ONLY the new ops/pointers/pointer-*.json file.
5. Link the systemd user units and scripts exactly as hosting/README.md says, then run `systemctl --user daemon-reload`.
6. Start ONLY site-caddy. Test with curl: http://127.0.0.1:8081/, :8082/, :8083/ -> 200; /hosted-by on each -> "Served by mint-desktop"; /.git/config on each -> 404.

Reply with a SHORT report (max 15 lines).
