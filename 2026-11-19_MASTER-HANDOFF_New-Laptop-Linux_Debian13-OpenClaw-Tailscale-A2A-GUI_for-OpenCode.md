# MASTER HAND-OFF: build "New-Laptop-Linux" (OpenClaw on the Laptop, Debian 13 "trixie")

Date: 2026-11-19 (night) | Author: New-Desktop-Linux (OpenCode session, Claude Sonnet 5.5, on the living-room Desktop PC, Linux Mint 22), who did exactly this install today, successfully, and translated it for Debian 13.
Reader: OpenCode (Claude Sonnet 5.5) on Nir's LAPTOP booted into Debian 13. You install OpenClaw; once it runs, **you become the agent called New-Laptop-Linux**.
Companion file for the helper agent: `2026-11-19_HANDOFF_New-Desktop-Linux-OpenClaw_helper-for-New-Laptop-Linux-installation_for-OpenClaw.md`.
This repo is PUBLIC. **Never write a token, password, API key or sudo password in it.**
Also read the older master hand-off `2026-11-19_MASTER-HANDOFF_New-Desktop-Linux_OpenClaw-Tailscale-A2A-mesh-GUI_for-OpenCode.md`: it has the long "why" behind many steps. THIS file wins where they differ (it contains the corrections learned the hard way).

---
## 0. How to behave with Nir (this saved me hours)
- Nir (Haifa) is a beginner and polite to him is mandatory: **lots of emojis in every reply, short, plain English, the important thing LAST, one screen, no walls of text.** Explain every technical word in one simple sentence. Never quiz him with multi-choice questions: ask in plain text, one question at a time.
- **Do only what Nir says.** Before every download, install, compile or sudo step, tell him in 3-6 short lines what you will do and get ONE "go" per phase. Tell him when you need something from him. From time to time stop and tell him what you are working on.
- Do not do things for him that he wants to do himself, and do not lecture. Answer his questions in WORDS first (no tool calls) when he only asks.
- Nir gives his sudo password in chat when asked. Use it, never write it into any file, ask again each session. Same for the OpenRouter key and tokens: only into `~/.openclaw`, never in this repo.
- **Never claim success you did not verify.** Say "I did not verify X" when true. If a tool fails twice, change approach; after three failures tell Nir the blocker in one line.
- Nir's rule for GitHub: push only what he names, only what changed; the secret scanner runs on commit; `git status --porcelain` and `git log origin/master..` must be empty after pushing. Branch is `master`.

---
## 1. The family (names are final)
| Agent | PC / OS | Tailscale machine | Gateway URL (tailnet only) |
|---|---|---|---|
| New-Laptop-Windows | Laptop, Windows 11 | new-laptop-windows (100.99.200.43) | https://new-laptop-windows.tail195bea.ts.net |
| New-Desktop-Windows | Desktop, Windows 11 | new-desktop-windows (100.107.152.18) | https://new-desktop-windows.tail195bea.ts.net |
| New-Desktop-Linux | Desktop, Linux Mint 22 | new-desktop-linux (100.118.103.61) | https://new-desktop-linux.tail195bea.ts.net |
| **New-Laptop-Linux (YOU)** | Laptop, Debian 13 | new-laptop-linux (to be set) | https://new-laptop-linux.tail195bea.ts.net |
- Tailnet suffix `tail195bea.ts.net`. Do not touch the old unrelated machine `ilan`.
- **DECIDED BY NIR + CONFIRMED BY ALL FRIENDS (important, differs from the older hand-off):** a PC is online in only ONE OS at a time, so **NO link between two agents of the same physical PC** (you and New-Laptop-Windows are the same laptop: no A2A peer, no node link between you). Useful links are only between the DESKTOP (whichever OS is booted) and the LAPTOP. So YOU link to: `new-desktop-linux` and `new-desktop-windows`. When a peer's OS is not booted it is simply offline; that is normal, not an error.
- Tailscale rename trap: in the admin console (login.tailscale.com/admin/machines) the "Auto-generate from OS hostname" checkbox must be UNticked or the new name does not stick. Try `sudo tailscale set --hostname=new-laptop-linux` and confirm the result in `tailscale status` (I did not test this command on Debian; if it does not work, Nir renames it in the admin console).

---
## 2. RULE ZERO: protect the websites while you work (and how to check them)
Nir's plan for this installation (he does it BEFORE you start): he turns the website serving OFF on the Desktop and turns it ON on THIS laptop (Debian), so you can verify, like I did on the desktop, that the sites survive every phase. The websites (strulovitz.org, learnime.com, peaktogether.me) are Caddy + a Cloudflare tunnel; the repo's `hosting/README.md` and `hosting/bin/sites-on|sites-off|sites-status|sites-check` describe them, the user services are `site-caddy.service`, `site-tunnel.service`, `site-nosleep.service` (local ports 127.0.0.1:8081-8083). Read `hosting/README.md` first.
1. **Never stop, restart, reconfigure, update, reinstall or uninstall** Caddy, cloudflared, the `site-*` services, the tunnel token (`~/.config/site-hosting/tunnel-token`, NEVER print/copy it), DNS, Apache, certificates or site files. Whether the sites are ON or OFF is Nir's business (use `sites-status` only to LOOK). Never start a second tunnel: the desktop and the laptop must NEVER serve at the same time.
2. No `apt upgrade/full-upgrade/autoremove`, no changing system Node/Python, no firewall/ufw/nftables changes, no kernel/driver changes, no reboot without Nir's OK. Only the small, named apt installs listed below, each with Nir's go and after `apt install --dry-run` shows nothing is upgraded or removed.
3. No heavy CPU/RAM/disk jobs, no compiles, no parallel builds (the Mint desktop froze for 36 minutes once). Laptops overheat: check `free -h`, `nproc`, battery.
4. **Tailscale:** no exit node, no `--accept-routes`, no `--accept-dns` change, no subnet routes, never `tailscale logout/down`, **never `tailscale funnel`** (public internet; must stay OFF).
5. **LAPTOP SLEEP (not verified, ask Nir):** a closed lid can suspend the laptop and kill the gateway AND the website. Check `systemctl status site-nosleep.service` and `cat /etc/systemd/logind.conf` (HandleLidSwitch). Do not change power settings yourself: tell Nir what you find and ask.
6. **Baseline first, compare after every phase ("HC")**; save the first output to `~/openclaw-baseline.txt` (outside any repo):
```bash
date; uname -a; head -3 /etc/os-release; echo "SESSION=$XDG_SESSION_TYPE"; echo "DESKTOP=$XDG_CURRENT_DESKTOP"
systemctl --user list-units 'site-*' --no-pager; systemctl is-active cloudflared
systemctl list-units --type=service --state=running --no-pager | head -60
ss -tlnp; free -h; df -h / /home; nproc
curl -sS -m 8 -o /dev/null -w "local8081:%{http_code}\n" http://127.0.0.1:8081/
curl -sS -m 15 -o /dev/null -w "public:%{http_code}\n" https://strulovitz.org/
tailscale status; tailscale ip -4; systemctl is-enabled tailscaled
node -v; which node npm git curl; loginctl show-user $USER | grep Linger
systemctl show user@$(id -u).service -p TimeoutStopUSec
ss -tlnp | grep -E '18789|:443|:8443' || echo "ports free"; ls -d ~/.openclaw 2>&1
```
After each phase repeat it and compare: the only allowed differences are new OpenClaw/Tailscale listeners. If the websites were ON at baseline they must still answer 200. If anything else changed, STOP, undo your last step, tell Nir.

---
## 3. Debian 13 differences I checked on the internet (and what I could NOT check)
- **AppImage needs FUSE 2:** on Debian 13 the package is `libfuse2t64` (verified on packages.debian.org). Without it run the AppImage with `APPIMAGE_EXTRACT_AND_RUN=1`. Installing it is an apt step: only with Nir's go.
- **AppImage requirements:** glibc >= 2.35 and libstdc++ with GLIBCXX_3.4.30. Debian 13 is newer than Debian 12 (which the docs say is fine), so it should pass (check with `ldd --version`). Not tested on this laptop.
- **Wayland is the big risk.** Debian 13's GNOME logs in with Wayland by default. The docs: global shortcuts (Quick Chat Ctrl+Shift+Space) do NOT work on Wayland (use the tray Quick Chat), and the project has open issues about a BLANK AppImage window on Wayland (#175745, #141443). On my Mint desktop (X11) all of this worked. `echo $XDG_SESSION_TYPE` tells you. If blank: first try the documented workaround, launched from the launcher only (not shell profile): `WEBKIT_DISABLE_DMABUF_RENDERER=1 WEBKIT_DISABLE_COMPOSITING_MODE=1 /path/to/AppImage` (reported to help on Debian 13 + WebKitGTK 2.52, but only on a Pi; results depend on graphics); if still blank, ask Nir whether he can log in with an X11 session ("GNOME on Xorg") if Debian offers one at the login screen (I did NOT verify that Debian 13 ships it). Backup that always works: the browser Control UI (see phase 9).
- **Secret Service:** the app stores gateway credentials in GNOME Keyring (or KWallet). Debian GNOME normally has `gnome-keyring`; check `dpkg -l | grep gnome-keyring` and that it is unlocked. If missing: apt install only with Nir's go.
- **Desktop icons:** stock GNOME has NO desktop icons (needs the "Desktop Icons NG" extension). So create the menu entries in `~/.local/share/applications/`; put copies on the desktop only if Nir sees a Desktop with icons. The `gio set ... metadata::trusted true` step is only for desktop copies.
- **Shutdown timeout:** Ubuntu/Mint ship a 5 s `user@.service` stop timeout; OpenClaw warns when it is below 90 s. Debian's own default may differ: check `systemctl show user@$(id -u).service -p TimeoutStopUSec`. Nir's ruling on the desktop: he does NOT want 90 s waits at shutdown, keep the system default. Only tell him the number; change nothing.
- **Tailscale on Debian 13:** official apt repo exists for trixie (verified): key `https://pkgs.tailscale.com/stable/debian/trixie.noarmor.gpg`, list `https://pkgs.tailscale.com/stable/debian/trixie.tailscale-keyring.list`. Check first whether Tailscale is already installed on the laptop (`which tailscale`). If yes, do NOT reinstall. If not, ask Nir for a go (needs sudo; installs a system service; first login is Nir approving in the browser).
- **Not checked at all:** the laptop's RAM/CPU/GPU, whether Debian's `systemd` user session is configured like Mint's, the current desktop environment (GNOME is assumed from the repo README). Verify each in the baseline.

---
## 4. Phase plan (ONE "go" from Nir per phase; run HC after each)
- **Phase 1 (read-only): baseline** (section 2.6). Also: `tailscale status`, `loginctl show-user $USER | grep Linger`, ports 18789/443 free? If 18789 is in use, STOP and ask.
- **Phase 2: install OpenClaw CLI (no system Node, no sudo).** `curl -fsSL https://openclaw.ai/install-cli.sh -o /tmp/install-cli.sh`; show Nir what it does (it only uses sudo if git is missing; it installs Node 24 under `~/.openclaw`); run `nice -n 19 bash /tmp/install-cli.sh`. It did NOT add `~/.openclaw/bin` to PATH on Mint: call `~/.openclaw/bin/openclaw` by full path (`export PATH=$HOME/.openclaw/bin:$PATH` inside your own shell commands). Today's version: 2026.11.6 (use the newest STABLE; check that its GitHub release has Linux assets).
- **Phase 3: onboard + gateway service.** The non-interactive command that worked for me (Nir pastes the OpenRouter key to you in chat; it goes ONLY on this command line, never into any file or repo):
```bash
nice -n 19 openclaw onboard --non-interactive --accept-risk --mode local --flow quickstart \
  --auth-choice openrouter-api-key --openrouter-api-key "<KEY FROM NIR>" \
  --gateway-auth token --gateway-bind loopback --gateway-port 18789 --tailscale off \
  --install-daemon --daemon-runtime node --skip-channels --skip-skills --skip-search --skip-hooks --skip-ui \
  --agent-name "New-Laptop-Linux"
```
  **Expected trap:** the service install fails with `unsafe-permissions ... ~/.config/systemd/user is group/world-writable`. Fix, exactly as OpenClaw says (non-recursive): `chmod go-w ~/.config/systemd ~/.config/systemd/user`, then `openclaw gateway install`. (On Debian the folder may not exist or may already be fine.) Then:
  `openclaw config set agents.defaults.model.primary "openrouter/anthropic/claude-sonnet-5.5"` and `openclaw config set agents.defaults.thinkingDefault medium`. Verify: `openclaw gateway status` (running, 127.0.0.1:18789), token length 48 (do not print it), `systemctl --user is-enabled openclaw-gateway`. Real test: `openclaw agent --agent new-laptop-linux --message "Say hello to Nir in one short line."`
  **BILLING TRAP (happened to me):** if OpenRouter returns 402 (no credits), OpenClaw pauses the key ("disabled:billing", ~6-20 min, shown by `openclaw models status`) and EVERY retry fails ("Prepared direct auth fallback cannot bypass unavailable profiles"), even after Nir tops up. Fix: tell Nir, top up, then WAIT for the pause to end and do NOT press "Try again" (it can extend the pause). Ask Nir to check his OpenRouter credit before big work.
- **Phase 4: identity.** Workspace `~/.openclaw/workspace`: write `IDENTITY.md` (Name New-Laptop-Linux, AI assistant living in Nir's Laptop on the Debian 13 side of a dual-boot, polite warm, lots of emojis, emoji 🐧), `USER.md` (directives, see my own file as a model: always polite + emojis + short, plain English, important thing last, never claim unverified success, never put secrets in GitHub, protect the websites), append a family/style paragraph to `SOUL.md`, append the A2A rules (section 8 here) to `AGENTS.md`, create the skill `~/.openclaw/workspace/skills/wake-peer-agent-via-a2a/SKILL.md` (same text as the rules), and move `BOOTSTRAP.md` to the trash. The "skill workshop" tool belongs to the agent, so writing the SKILL.md by hand is fine (`openclaw skills check` listed it).
- **Phase 5: survive reboot.** Linger must be `yes`: if not, `sudo loginctl enable-linger $USER` (the one sudo here, show Nir first). Gateway service enabled. Nir does NOT want a 90 s shutdown: do not change the stop timeout.
- **Phase 6: gateway on the tailnet (Tailscale Serve).** First `tailscale status`, then (Tailscale installed + machine named `new-laptop-linux`). Check `ss -tlnp | grep ':443'` and `tailscale serve status --json`: if anything uses 443 or a Serve config exists, STOP and ask Nir. `gateway.tailscale.mode` is a PROTECTED path: **Nir must type these two commands himself**: `~/.openclaw/bin/openclaw config set gateway.tailscale.mode serve` then `~/.openclaw/bin/openclaw gateway restart`. Verify `curl https://new-laptop-linux.tail195bea.ts.net/` -> 200 ("OpenClaw Control"); `tailscale funnel status` must show nothing. HC.
- **Phase 7: node link to the DESKTOP gateway(s)** (laptop-linux becomes a node of whichever desktop OS is online). Needs that desktop gateway's 48-char token from Nir (he reads it in `~/.openclaw/openclaw.json` on the desktop and pastes it to you). Foreground test first:
  `OPENCLAW_GATEWAY_TOKEN='<48 chars>' timeout 40 openclaw node run --auth-from-env --host new-desktop-linux.tail195bea.ts.net --port 443 --tls --display-name "New-Laptop-Linux" --node-id laptop-linux-node`
  Expect `device pairing required (requestId: ...)` (request ids are NOT secrets). The gateway owner approves (`openclaw nodes pending`, `openclaw nodes approve <id>`); ask the helper agent on the desktop (section 9) or leave a repo note. Then `openclaw node install --auth-from-env ...` with the same flags (token in env for that command) and `openclaw node start`; a SECOND approval (capabilities) appears: "node capability surface is awaiting operator approval ... nodes approve <id>" (the id is in `journalctl --user -u openclaw-node`). Leave camera/location OFF; exec approvals stay ON. The node service keeps its token in `~/.openclaw/node.systemd.env` (not in the unit file); exactly ONE process per node id. A second link to `new-desktop-windows` needs its own profile/state dir and a DIFFERENT node id (`laptop-linux-node-to-desktop-windows`); read `openclaw --help` (`--profile`) and the docs, and ask Nir if unclear. Do the desktop-linux link first (that is the OS Nir boots most). Never run `openclaw nodes status`/`devices ...` from the node machine against the remote gateway with the node's own identity.
- **Phase 8: A2A (instant messenger).** Section 7.
- **Phase 9: GUI (Nir says the GUI is NOT optional).** Section 6.
- **Phase 10: final report + reboot check.** Section 10.

---
## 5. Config recipes that worked
- Set A2A in one go (MERGE if channels.a2a already has peers: read first with `openclaw config get channels.a2a`; back up `~/.openclaw/openclaw.json` first):
```bash
openclaw config set channels.a2a '<json>' --strict-json
# json = {"enabled":true,"advertisedUrl":"https://new-laptop-linux.tail195bea.ts.net","peers":{"new-desktop-linux":{"url":"https://new-desktop-linux.tail195bea.ts.net/a2a/v1","token":"<what the peer must present to ME>","outboundToken":"<what I present to the peer>"},"new-desktop-windows":{ ... same shape ... }}}
```
  Build the json with python3 (`json.dumps`) so quotes cannot break. It hot-reloads; restart the gateway to be safe.
- Quick checks: `openclaw gateway status`, `openclaw models status` (shows "disabled:billing" if paused), `openclaw skills check`, `journalctl --user -u openclaw-gateway -n 80 --no-pager`, `openclaw sessions tail --agent new-laptop-linux --session-key "<key>" --tail 20` (shows what an agent did, e.g. whether an A2A relay failed).

---
## 6. Phase 9: the GUI (OpenClaw companion app, Tauri) - done on Mint, steps that worked
- Live docs: https://docs.openclaw.ai/platforms/linux ; releases: https://github.com/openclaw/openclaw/releases . Pick the newest STABLE release whose assets include `OpenClaw-<ver>-amd64.AppImage`, `.deb` and `SHA256SUMS.linux-app.txt` (not all releases have them: v2026.10.33 and v2026.11.3 did not). On 2026-11-19 the right one was **v2026.11.6** (AppImage ~500 MB, sha256 `441003c85d350e51a3675fe2758bc6a37e84d9d99f1f1a6ea04ed108138150d1`; re-read the checksum file for any newer version).
- Prefer the **AppImage** (no root): `mkdir -p ~/Apps/OpenClaw`, download with `nice -n 19 curl -fL -o ... <url>`, VERIFY `sha256sum`, `chmod +x`. Avoid the `.deb` (it pulls many dependencies; only with Nir's go and a dry-run).
- Menu entries (Nir chose these SHORT names): `~/.local/share/applications/openclaw-app.desktop` Name `OpenClaw app`, Comment "Talk to New-Laptop-Linux, the AI assistant that lives in this PC (app window)", Exec = the AppImage path, Terminal=false. And `openclaw-browser.desktop` Name `OpenClaw browser`, Comment "... in your web browser (backup way)", Exec `/home/<user>/.openclaw/bin/openclaw dashboard` (it opens the browser with a one-time pairing link). Desktop copies only if the desktop shows icons.
- Before the first launch copy `~/.bashrc` and `~/.profile` to /tmp to prove the app changes nothing (on Mint it did not), and note the gateway PID and a copy of `~/.config/systemd/user/openclaw-gateway.service`. Launch detached: `(setsid nice -n 10 <AppImage> </dev/null >/tmp/openclaw-app.log 2>&1 &)`. Lots of harmless "Failed to load module ... gvfs/xapp" warnings are normal. The app **attached to my existing gateway** and left the service untouched (same PID, same unit file). **Never click "Use bundled runtime..."** in the tray; if it tries to change the service, cancel and tell Nir. Leave "Desktop sharing" OFF. The app also prepares a "Chrome helper" (a small download in its own folder; Nir said let it do what it wants). Microphone does not work in the app; use the browser for that.
- Autostart: ask Nir (not decided on the desktop yet). It is `~/.config/autostart/openclaw.desktop`.
- Ask Nir to describe what he sees, and tell him in simple clicks what to do (open "OpenClaw app", the Main Session is the chat). Saving other gateways in the app ("Manage Gateways") is NOT needed; Nir skipped it.
- A screenshot helps: `scrot` or `import -window root` (my Mint desktop had 4 monitors side by side, crop the first one with PIL).

---
## 7. Phase 8: A2A details
Docs: https://docs.openclaw.ai/channels/a2a . Two DIFFERENT tokens per pair (`token` = what the peer must present to me; `outboundToken` = what I present to the peer; my outboundToken for X equals X's token for me). Generate NEW tokens (`openssl rand -hex 32`, 64 hex chars) for **two pairs: (you, new-desktop-linux) and (you, new-desktop-windows)** = 4 tokens. Never reuse tokens from this repo's git history. Save them to a mode-600 file in your home (e.g. `~/a2a-tokens-for-nir.txt`) and show them to Nir in chat so he can copy them by hand to the other agents (he did this for me; tailnet-only link secrets, never in GitHub or A2A messages). Leave a repo note to each peer with the token NAMES only (not values) and the exact peer entry they must add: peer name `new-laptop-linux`, url `https://new-laptop-linux.tail195bea.ts.net/a2a/v1`, their `token` = your `outboundToken`, their `outboundToken` = your `token`. Today's names for the desktop-linux pair: A2A_TOKEN_desktop_linux_to_laptop and A2A_TOKEN_laptop_to_desktop_linux; use similar clear names.
Tests in this order (verified facts only): (1) agent card `curl -s -o /dev/null -w "%{http_code}" https://<peer>.tail195bea.ts.net/.well-known/agent-card.json` -> 200 (yours and the peer's); a bare POST to `/a2a/v1` without token -> 401. (2) Send with the `message` tool (channel=a2a, target=a2a:<peer>, text starting `[QUESTION]`). `deliveryStatus: sent` is not an answer. (3) The REAL push test: the peer sends you ONE unprompted message while you are idle; your agent must wake by itself and answer with the message tool; check logs. (4) Test both directions. Offline peer = its PC is in the other OS (check `tailscale status`).

---
## 8. Put in the workspace `AGENTS.md` of New-Laptop-Linux (before any test)
```
## A2A replies (all friends)
- Any inbound A2A message, from ANY peer: do the job, then answer with the `message` tool (channel=a2a, target=a2a:<sender-name>), a NEW message, starting with [DONE] for finished work. Plain session text never reaches the peer.
- When an inbound A2A message answers something Nir asked, or is news Nir should know, ALSO relay one short line to Nir's main chat via the `dispatch_action` tool with {"id":"sessions_send","args":{"sessionKey":"agent:main:main","message":"<who said what, clock time>"}}. `sessions_send` is DEFERRED: calling it directly FAILS. Deferred tools (sessions_*, conversations_*, session_status, agents_list...) always go through dispatch_action.
- When I need a peer, send with `message` and wait for the answer inside the same turn. Never end a turn promising to check later.
- No secrets in A2A messages. Report only verified facts. If a tool fails twice, change approach and tell Nir.
- Talk naturally: answer when spoken to, no artificial message limits; I say goodbye myself.
```
(Nir decided that his laptop-windows agent does not relay [DONE] to him; so when you answer a question, start with [DONE] AND also tell Nir directly or write a repo note.) An A2A relay can fail silently when OpenRouter credits are empty: then Nir never sees the peer's answer. Check `openclaw sessions tail ...` if an answer seems missing.

---
## 9. Who helps you
My OpenClaw agent on the desktop (New-Desktop-Linux) has a hand-off to help your installation (approve your node pairing, add you as an A2A peer, test messages). Until A2A works, communicate through repo notes named `YYYY-MM-DD_<TOPIC>_from-New-Laptop-Linux_to-New-Desktop-Linux.md` (no secrets) and through Nir. Nir carries tokens by hand. The desktop must be BOOTED into Linux for it to answer.

---
## 10. Final verification (write `2026-MM-DD_FINAL-REPORT_from-New-Laptop-Linux.md`, no secrets)
1. HC identical to baseline (websites state, listeners). 2. `openclaw --version`, `openclaw gateway status`, `systemctl --user is-enabled openclaw-gateway openclaw-node`, `Linger=yes`, `tailscale status` name `new-laptop-linux`, `https://new-laptop-linux.tail195bea.ts.net/` 200, agent card 200. 3. A2A both directions with new-desktop-linux (and new-desktop-windows when that OS is booted). 4. Node link: desktop shows you connected + approved. 5. The GUI opens and Nir can chat. 6. Reboot test ONLY if Nir says; otherwise ask him to tell you after his next normal reboot and check then that gateway, node and Serve came back by themselves. 7. A small table of services, ports, node ids, peers, versions, and a "what Nir must still do" list.

Be careful with the websites, kind with Nir, honest in every report. 🐧💙
-- New-Desktop-Linux
