# REPORT FOR CLAUDE: Local Hosting Session (2026-09-28)

Update later on 2026-09-28: a tunnel token was securely saved outside GitHub and the tunnel connected. See `hosting-migration/2026-09-28-tunnel-connection-report.md` for current state; the "no tunnel/token" statements below describe the earlier stage only.

**Current outcome:** Three static sites are served by Caddy **only on this laptop's `127.0.0.1:8081-8083`**. Caddy is running; Apache remains running, unchanged, on `:80`. There is **no Cloudflare Tunnel**, no tunnel token, no DNS change, and no auto-start at boot. Nir is ending today's session while waiting for DreamHost's domain transfers; do not confuse the local preview with a live hosting cutover.

**Versions/installation:** Caddy `v2.11.4`, downloaded from the official `caddyserver/caddy` GitHub release as `caddy_2.11.4_linux_amd64.tar.gz` and checked against the official SHA-512 checksums file (`OK`), installed at `~/.local/bin/caddy`. Cloudflared **2026.9.3 is installed** from Cloudflare's official signed apt repo (keyring `/usr/share/keyrings/cloudflare-main.gpg`, source `/etc/apt/sources.list.d/cloudflared.list`). A desktop authentication prompt allowed apt to run without recording a password; apt installed one package, with **0 upgrades**. `cloudflared tunnel run --help` confirms `--token-file` is supported; `systemd-analyze verify` passed for all three user units. Git LFS was skipped (no usage found). Apt update warned that the pre-existing GitHub CLI apt source lacks a signing key; it used old index data for that unrelated repo. Nothing was changed in the GitHub CLI apt source. Do not run `cloudflared service install` or `cloudflared tunnel login`.

**Build:** `python3 ops/build-export.py` ran once from `~/strulovitz-website`, creating ignored `exports/v2026-09-28-a/` (955 versioned files, 317 root files), `exports/pointer.json`, and **untracked** `ops/pointers/pointer-v2026-09-28-a.json`. The pointer history file has **not been committed or deleted**; Claude should decide what to do with it. The build script does not parse a version argument; it chooses the current date plus an unused letter. `exports/current` is a symlink to `v2026-09-28-a`, not a second copy. No DreamHost deployment script was run.

**Caddyfile** (`hosting/Caddyfile`, validated with `caddy validate` and formatted with `caddy fmt`; the admin endpoint is loopback-only):

```caddyfile
{
	auto_https off
	admin 127.0.0.1:2019
}

:8081 {
	bind 127.0.0.1
	@hidden path_regexp hidden "(^|/)[.]"
	respond @hidden 404
	@rootDocs path_regexp rootDocs "^/[^/]+[.]md$"
	respond @rootDocs 404

	root * {$HOME}/strulovitz-website/exports
	# Keep links to the old dated version working across future builds.
	handle_path /v2026-09-11-c/* {
		root * {$HOME}/strulovitz-website/exports/current
		file_server
	}
	handle /ghost/* {
		root * {$HOME}/strulovitz-website
		file_server
	}
	handle /hive/* {
		root * {$HOME}/strulovitz-website
		file_server
	}
	handle {
		file_server
	}
}

:8082 {
	bind 127.0.0.1
	@hidden path_regexp hidden "(^|/)[.]"
	respond @hidden 404
	@rootDocs path_regexp rootDocs "^/[^/]+[.]md$"
	respond @rootDocs 404
	root * {$HOME}/Anime/learnime-site
	file_server
}

:8083 {
	bind 127.0.0.1
	@hidden path_regexp hidden "(^|/)[.]"
	respond @hidden 404
	@rootDocs path_regexp rootDocs "^/[^/]+[.]md$"
	respond @rootDocs 404
	@python path_regexp python "[.]py$"
	header @python Content-Type "text/plain; charset=utf-8"
	header @python Content-Disposition attachment
	@images path *.png *.jpg *.jpeg *.gif *.svg *.webp
	header @images Cache-Control "public, max-age=2592000"
	@cssjs path *.css *.js
	header @cssjs Cache-Control "public, max-age=604800"
	root * {$HOME}/peaktogether-website
	file_server
}
```

**Old links:** `/v2026-09-11-c/*` is served from the `exports/current` symlink; `sites-on` updates that symlink from the latest `pointer.json` after a build. The old path therefore keeps working after future builds without rewriting the Caddyfile. `/ghost/*` and `/hive/*` read directly from the same repository (not from `exports/`). Each site denies hidden URL segments and repo-root Markdown; Peak Together's Python files download as `text/plain` and are never executed.

**Local test results (HEAD unless noted):**

```text
Port/site       Home  Internal pages/assets  /.git/config  Other checks
8081 Strulovitz 200   10/10 returned 200     404           old v2026-09-11-c link, ghost, hive, JSON and JS work
8082 Learnime   200   11/11 returned 200     404           gallery images and MP4 work
8083 Peak       200   13/13 returned 200     404           no-slash folder -> 308, Python attachment/plain text, JSON work
```

All 3 ports and admin `:2019` listen on `127.0.0.1` only. Caddy serves JS modules as `text/javascript`, JSON as `application/json`, and MP4 as `video/mp4`; MP4 GET range `bytes=0-99` returned **206** with `Content-Range`, and image/CSS/JS cache headers match the requested periods. `/.htaccess`, nested hidden paths, and root Markdown returned 404. Initial security test found Peak Together's `/.git/config` returned 200 because an over-escaped matcher failed; **Caddy was immediately stopped, the matcher corrected, and all three ports now return 404**. It was never exposed via a tunnel.

**Homepage bytes vs live:** Strulovitz differs only in three versioned hrefs (`v2026-09-28-a` locally vs `v2026-09-11-c` live). Learnime differs only because Cloudflare obfuscates two email links and inserts its decoding script on the live page. Peak Together matches after normalizing CRLF/LF line endings. The local HTML itself was not edited to mimic CDN transformations.

**User units/commands:** `hosting/systemd/site-{caddy,tunnel,nosleep}.service` are symlinked into `~/.config/systemd/user/` and are **not enabled at boot**. `hosting/bin/sites-{on,off,status}` are symlinked into `~/.local/bin/`. Only `site-caddy.service` was started. `sites-status` reports Caddy active, tunnel/nosleep inactive, and all three homepages 200. `sites-on` was tested without a token: it clearly refuses to start anything and reports the missing token. `systemd-inhibit --what=sleep:handle-lid-switch --why='Hosting websites' sleep 2` worked as user `nir` without root; `site-nosleep.service` has not been started. `site-tunnel.service` is valid with the now-installed cloudflared binary, but has **not been started** (there is no token).

**Exact commands for Nir now:** Open `http://127.0.0.1:8081/`, `http://127.0.0.1:8082/`, and `http://127.0.0.1:8083/` in Firefox on this laptop to check appearance. In a terminal, run `sites-status` to see whether the previews are running. After a laptop restart, `systemctl --user start site-caddy.service` starts **only local previews**. Do **not** run `sites-on` until a tunnel token exists. No action is required while domain transfers are pending.

The Cloudflare token belongs only at `~/.config/site-hosting/tunnel-token` with mode 600, outside all repos; it does not exist yet. `**/tunnel-token` was added to the Strulovitz repo's `.gitignore` as an extra safeguard. The remaining work is DreamHost transfers, Nir's dashboard tunnel/token decision, routing and public cutover. No public cutover has occurred.
