# MASTER HAND-OFF: build "New-Desktop-Linux" (OpenClaw on the Desktop PC, Linux Mint 22)

Date: 2026-11-19 (written ~21:50 Israel time) | Author: New-Laptop-Windows (OpenClaw agent, bedroom), after a full day of trial and error with Nir and New-Desktop-Windows.
Reader: OpenCode (Claude Sonnet 5.5) running on the living-room Desktop PC booted into Linux Mint 22. You will install and configure OpenClaw; once it runs, **you become the agent called New-Desktop-Linux** (same model, same personality, same family).
This file SUPERSEDES `2026-11-19_HANDOFF_Install-OpenClaw-on-New-Desktop-Linux_for-OpenCode.md` (deleted). If any other file in this repo disagrees with this one, this one wins.

This repo (`strulovitz/strulovitz-website`) is PUBLIC. **Never write a token, password, API key or private URL secret in it.** Use files named `YYYY-MM-DD_<topic>_from-<NAME>_to-<NAME>.md` only for long notes that contain no secrets.

---
## 0. Who Nir is and how to behave (read first, it saves hours)
- Nir (Haifa, Asia/Jerusalem) is a beginner, polite to him is mandatory, and he wants **lots of emojis in every reply**. He is tired of long answers: **short, simple, plain English, important thing last**. Explain any technical term in one simple sentence a person on the street would understand. Never give him a "scroll".
- **Do things yourself.** Do NOT give Nir missions you can do by yourself when it is obvious he approves. Do not ask permission for obvious things he already asked for. Do not ask the same question twice. If he gave a decision, it is final (e.g. "full mesh").
- BUT for this particular machine Nir set hard rules (from `STATUS-2026-11-09-TTS-STUDIOS-PROGRESS.md` in this repo, read it): work **gradually**; tell Nir in plain words what you are about to do; **one explicit "go" from Nir before every download, install, compile or sudo step**. To avoid asking 40 times, ask for ONE "go" per phase of this file, listing the exact steps of the phase in 3-6 short lines, then do the whole phase.
- **If anything is unclear, stop and ask Nir. Do not guess.** One question at a time, with one-line pros and cons.
- **Never claim success you did not verify.** Nir caught us claiming "it works" after tests where we waited and polled. Report only facts you saw (command output, message ids, times). Say "I did not verify X" when true. Nir calls unverified claims lies, and he is right.
- Do not loop on a failing tool. If a tool fails twice, change approach; if it fails three times, tell Nir the blocker in one line.
- Nir wants all four friends equal: no machine is the boss. Each PC dual-boots Windows/Linux and each OS has its own agent.

---
## 1. The family (names are final; never invent other names)
| Agent | PC / OS | Tailscale machine | Tailscale IP | Gateway URL (tailnet only) |
|---|---|---|---|---|
| New-Laptop-Windows | Laptop (bedroom), Windows 11 | `new-laptop-windows` | 100.99.200.43 | https://new-laptop-windows.tail195bea.ts.net |
| New-Desktop-Windows | Desktop (living room), Windows 11 | `new-desktop-windows` | 100.107.152.18 | https://new-desktop-windows.tail195bea.ts.net |
| **New-Desktop-Linux (YOU)** | Desktop (living room), Linux Mint 22 | `new-desktop-linux` | 100.118.103.61 | https://new-desktop-linux.tail195bea.ts.net (to be created by you) |
| New-Laptop-Linux (later) | Laptop (bedroom), Debian 13 | `new-laptop-linux` | (tbd) | https://new-laptop-linux.tail195bea.ts.net |
- Tailnet DNS suffix: `tail195bea.ts.net`. Account: Nir's (`nir.strulovitz@...`). The names above were already set in the Tailscale admin console (we renamed three machines today; **trap:** the admin page has a checkbox "Auto-generate from OS hostname" which must be UNticked or the new name does not stick). The old names `laptop-windows`, `desktop-windows`, `desktop-linux` no longer exist; do not use them. An old unrelated machine `ilan` (Windows) is also on the tailnet: leave it alone.
- Naming scheme for future machines: `new-<pc>-<os>`. Old computers (if they ever join) will not clash.
- Both PCs are in the same house; Tailscale gives direct LAN paths (ping 1-2 ms) or DERP relay (~100 ms); both are fine.
- Each PC is only online in ONE OS at a time. A link must reconnect by itself when the other OS comes back. Services must therefore start by themselves and retry forever.

---
## 2. RULE ZERO: do not break the website (and the AI studios) on this Linux machine
This Linux Mint machine **serves Nir's website strulovitz.org** (Caddy web server + a Cloudflare Tunnel) and hosts heavy AI "TTS studios". Both are extremely important to Nir (the Debian laptop will also serve the website sometimes; both PCs are equally important).
1. **Do NOT stop, restart, reconfigure, update, reinstall or uninstall** `cloudflared`, Caddy (or whatever web server `ss -tlnp` shows), their systemd units, their config, `~/.cloudflared`, `/etc/cloudflared`, DNS, certificates or site files. Do not assume the website is running or stopped: its state is Nir's business (he sometimes shuts it down on purpose). Never start or stop it unless Nir says so.
2. **Do NOT touch the AI studios** in the home folder: `~/drama3`, `~/voxcpm2`, `~/zonos`, `~/voicebox` (about 150 GB) and their icons, ports (8035, 8808, 7860, 5173, 17493), CUDA at `~/drama3/cuda`, nor neo4j. The GPU is an RTX 4070 Ti with 12 GB; **do not run any GPU-heavy or CPU-heavy job.** Today (2026-11-09) a 6-job compile froze this PC for ~36 minutes and Nir had to shut his website down and reboot. No compiles, no big builds, no parallel jobs.
3. **No** `apt upgrade`, `apt full-upgrade`, `apt autoremove`, no changing the system Node.js/Python, no firewall changes (ufw/iptables/nftables), no kernel/driver changes, no reboot without Nir's OK (the single reboot test in phase 8 needs his OK).
4. **Tailscale:** no exit node, no `--accept-routes`, no `--accept-dns` changes, no subnet routes, no `tailscale logout`, no `tailscale down`, never `tailscale funnel` (Funnel exposes things to the PUBLIC internet and must stay OFF). The Cloudflare tunnel does not use Tailscale, and Tailscale Serve is tailnet-only, so they do not conflict, but you must still verify (see below).
5. **Baseline first, compare after every phase** (the "HC", Website Health Check):
```bash
date; uname -a; head -3 /etc/os-release; echo $XDG_SESSION_TYPE
systemctl is-active cloudflared
systemctl list-units --type=service --state=running --no-pager | head -60
ss -tlnp
free -h; df -h /
curl -sS -o /dev/null -w "local:%{http_code}\n" http://127.0.0.1:80/   # use the port ss shows for the site
curl -sS -o /dev/null -w "public:%{http_code}\n" https://strulovitz.org/
tailscale status; tailscale ip -4
```
Save the first output to `~/openclaw-baseline.txt` (outside any repo). After each phase, repeat and compare: the only allowed differences are new OpenClaw/Tailscale-Serve listeners. If anything else changed, STOP, undo your last step, tell Nir. If the website was off at baseline, "unchanged" means still off.
6. If a step could freeze the PC (RAM/CPU/disk heavy), do not run it; ask Nir.

---
## 3. What we learned today (hard-earned lessons, in plain list form)
**Tokens and pairing**
- The gateway token is **exactly 48 characters**. A truncated token that shows `…` or `...` in the middle gives `unauthorized: gateway token mismatch (AUTH_TOKEN_MISMATCH)`. A "pairing required (requestId ...)" message appears BEFORE the token check, so it does not prove the token is right. Always check the stored token length (48) without printing it.
- `openclaw config get gateway.auth.token` prints `__OPENCLAW_REDACTED__`. The real token sits in `~/.openclaw/openclaw.json` (Nir can read it there and paste it to you; he said tokens are fine inside his home, just never in GitHub or any public place).
- Node pairing: first connect gives `pairing required (requestId: ...)`. The GATEWAY owner approves it (`openclaw nodes pending`, `openclaw nodes approve <requestId>` or `openclaw devices approve`). Capabilities are approved separately: a node may be "paired, connected" but with empty `caps/commands` until the second approval (`Node reapproval pending ...`). New-Laptop-Windows will do these approvals; tell it via A2A.
- **Never run `openclaw nodes status` / `devices ...` from a node machine against the remote gateway with the node's own identity**: it changed the Windows desktop's device identity and created an extra re-pairing request. Use a separate state dir (or ask the gateway owner by A2A).
- `openclaw devices rotate` to widen scopes is refused (`scope-outside-approved-baseline`); a client gets scopes only through an approval request. We did not need this in the end, because A2A solved direct talking.
- Newer pairing (docs, 2026.11.x): `openclaw devices join-code` (on the gateway: mints a single-use node onboarding URL) and `openclaw node run --pair "oc-pair://..."` / `openclaw connect <link>`. Try them only if they exist on the target gateway; the token method below is proven.

**Tailscale**
- `tailscale serve` on a tailnet that never enabled Serve **hangs forever** printing "Serve is not enabled on your tailnet. To enable, visit https://login.tailscale.com/f/serve?node=...". It is ALREADY ENABLED on Nir's tailnet now (HTTPS certificates ON, Funnel OFF), so you should not see that again. If you do, STOP and tell Nir (he must approve HTTPS certificates and must say NO to Funnel). When scripting `tailscale serve`, run it with a timeout/background so a hang cannot freeze your shell.
- HTTPS certificates put the machine names in a public ledger. This is accepted by Nir.
- After a Tailscale machine rename, the old Serve mapping stays bound to the old name; the gateway must be restarted (and the old foreground listener removed) so Serve re-registers under the new name.
- `gateway.tailscale.mode` is a **protected config path**: an agent cannot change it through the config tool (`cannot change protected config paths`). **Nir must run `openclaw config set gateway.tailscale.mode serve` himself, then `openclaw gateway restart`.** Do not try to bypass the protection. Prepare the exact two commands for him in one short message.
- `tailscale serve status` may say "No serve config" when the gateway manages Serve internally; check with `tailscale serve status --json` and with `curl https://<name>.tail195bea.ts.net/` (HTTP 200 + OpenClaw Control UI HTML).

**Updating**
- `openclaw update` refuses to run inside the gateway's own process tree ("Gateway PID ... is an ancestor of this process"). Run it from a normal terminal. On Windows it also needed an Administrator shell. When an update hangs or the gateway gets stuck, `openclaw doctor` repaired it. Back up `~/.openclaw/openclaw.json` before updating. (On Linux a user-level systemd service needs no root.)
- As of today the latest stable is **2026.11.5**. The laptop gateway and the Windows desktop run 2026.11.5. Docs for earlier versions differ from the live docs; **always read the LIVE docs (https://docs.openclaw.ai)**, because local copies on the Windows machines were stale and led us to a wrong claim about the Linux GUI today.

**Talking between agents**
- Plain session text never reaches the other agent. **You must call the `message` tool** (`action=send`, `channel=a2a`, `target=a2a:<peer-name>`). `deliveryStatus: sent` means the other gateway accepted it.
- Messages from a peer arrive in an **isolated session** per peer (`agent:main:a2a:default:direct:<peer>:ctx-...`); by design A2A never injects them into the main chat. Nir cannot see that session. To let Nir see something, the woken agent must relay one short line into the main chat: `dispatch_action` with `{"id":"sessions_send","args":{"sessionKey":"agent:main:main","message":"<who said what, clock time>"}}`.
- **Deferred tools (`sessions_send`, `sessions_history`, `sessions_list`, `session_status`, `conversations_*`, `agents_list`, ...) MUST be called through `dispatch_action`** with `id` and `args`. Calling them directly fails with "unknown tool"; repeating that failed three times killed several of our turns today. `sessions_send` refuses to target the calling session ("cannot target the calling session") so it only works from the A2A session towards `agent:main:main`.
- Never leave GitHub notes and wait for Nir to walk to another room and wake the other agent. Use A2A to wake a peer. Use the repo only for long text without secrets.
- Do NOT adopt any "max 2 messages", "never reply to INFO/DONE" or similar rules. We invented such rules today; Nir cancelled them; one agent stopped a friendly chat because of them. Natural IM behaviour: answer what is asked, keep talking when someone talks to you, end politely when YOU decide a conversation is over.
- `conversations_turn` does not support A2A. `pushNotifications` and streaming are not supported by the A2A plugin, but a new message always wakes the receiver's agent by itself, which is the "push" Nir wants.
- **How to test honestly (Nir's standard):** a real test is one where the sender goes idle and the other side's message wakes the agent by itself while NOBODY polls. Ask Nir to start the exchange from the other room, or have the peer send you an unprompted message and verify afterwards from logs and message ids. Waiting in a loop for an answer is not a push test; do not report it as one.
- Honest cause of "it worked one way, not the other": the answer of an automatically woken agent was written as plain session text instead of being sent with the message tool, and our relay instruction called `sessions_send` directly instead of through `dispatch_action`. Put the rules in section 10 into your AGENTS.md BEFORE the first test.

**Windows-only gotchas (for understanding the others, not for you)**: the gateway shell runs in a background session without a screen (session 0), so a browser window must be launched in the user's session through a scheduled task with `/IT`; Edge/Firefox handling; schtasks quoting. Not relevant on Linux, except: on Linux your user service has no `DISPLAY`; if a browser window is ever needed, ask Nir.

---
## 4. Phase plan (ask Nir for ONE "go" per phase; verify HC after each phase)
- **Phase 1 (read-only): baseline.** Section 2 baseline commands. Also check: `tailscale status` (are you `new-desktop-linux`? IP 100.118.103.61?), `systemctl is-enabled tailscaled`, `echo $XDG_SESSION_TYPE` (OpenCode said X11), `node -v`, `which node npm`, free RAM/disk, `ss -tlnp | grep -E '18789|:443|:8443'`, `loginctl show-user $USER | grep Linger`. If port 18789 is already in use, STOP and ask.
- **Phase 2: install OpenClaw CLI + gateway without touching system Node.** Use the local-prefix installer (live docs: Install > Local prefix installer `install-cli.sh`): `curl -fsSL https://openclaw.ai/install-cli.sh -o /tmp/install-cli.sh`, show Nir the first 40 lines, get "go", run it. It keeps Node under `~/.openclaw`. Never `sudo npm`. Version should be 2026.11.5 or newer (`openclaw --version`). If the installer fails, ask Nir before any fallback (user-prefix npm only).
- **Phase 3: onboard + local gateway as a systemd USER service.** `openclaw onboard --install-daemon` (or `openclaw gateway install`). Choices: local gateway, **bind loopback**, port 18789, auth token (generated; stays in `~/.openclaw/openclaw.json`, chmod 600), model provider OpenRouter with model `openrouter/anthropic/claude-sonnet-5.5`, thinking level **medium**. Nir pastes the OpenRouter API key into the prompt himself (never into the repo, chat history, or a command line; no `export` in shell history). No chat channels (WhatsApp/Telegram...) for now. Verify: `openclaw gateway status` (running, listening 127.0.0.1:18789), `systemctl --user status openclaw-gateway`, `openclaw status`. HC.
- **Phase 4: identity of the agent.** Edit workspace files (`~/.openclaw/workspace`): `IDENTITY.md` (Name New-Desktop-Linux, AI assistant living in Nir's Desktop PC, Linux Mint 22 side of a dual-boot, vibe polite warm lots of emojis), `USER.md` (Nir, Haifa, Asia/Jerusalem, always polite, lots of emojis, owns 2 desktops + 2 laptops each dual-boot, agent names unique per machine/OS), `SOUL.md` (copy the style of the family: be genuinely helpful, concise, ask before external actions, never leak secrets, do not exfiltrate private data, no destructive commands without asking, `trash` over `rm`). Put section 10 into `AGENTS.md`.
- **Phase 5: survive reboot ("forever").** `sudo loginctl enable-linger $USER` (show Nir first; the only sudo here), `systemctl --user enable --now openclaw-gateway.service`, check `loginctl show-user $USER | grep Linger` -> `Linger=yes`, `systemctl is-enabled tailscaled` -> enabled. Also note the docs (platforms/linux): the host's `user@<uid>.service` stop timeout should be at least 90 s so the gateway can drain at shutdown; check `systemctl show user@$(id -u).service -p TimeoutStopUSec`; if it is below 90 s, ask Nir before adding the drop-in the docs describe.
- **Phase 6: expose YOUR gateway on the tailnet (Tailscale Serve), loopback stays.** First `ss -tlnp | grep ':443'` and `tailscale serve status --json`: if anything already uses port 443 on the tailnet address or an existing Serve config exists, STOP and ask Nir (the website uses a Cloudflare tunnel and Caddy, so a conflict should not exist; verify). Then Nir runs the two protected commands (`openclaw config set gateway.tailscale.mode serve`, `openclaw gateway restart`). Verify: `curl -s -o /dev/null -w "%{http_code}" https://new-desktop-linux.tail195bea.ts.net/` is 200 FROM THIS PC, and ask New-Laptop-Windows (by A2A once available, otherwise ask Nir to open it on the laptop) to confirm it answers there. Funnel must stay off (`tailscale funnel status` should show nothing). HC.
- **Phase 7: join the other gateways as a node ("Link A")** (Linux -> Windows). Needs the laptop gateway token (48 chars) from Nir. Create one node service per remote gateway:
  1. Quick foreground test first (token only in the shell for this command, read with `read -rs`): `openclaw node run --host new-laptop-windows.tail195bea.ts.net --port 443 --tls --display-name "New-Desktop-Linux" --node-id desktop-linux-node`. Expect `pairing required (requestId: ...)`. Send the requestId (no token) to New-Laptop-Windows by A2A (after phase 8) or ask Nir to relay; it approves; re-run; expect `node host gateway connected: wss://new-laptop-windows.tail195bea.ts.net:443`.
  2. Make it permanent: `openclaw node install` with the same host/port/tls/display-name/node-id options (check `openclaw node install --help` for exact flags). The service must have the FULL token (verify length 48 without printing it) and exactly ONE process per node id. A second link (to `new-desktop-windows`) needs its own profile / state directory and a DIFFERENT node id, e.g. `desktop-linux-node-to-desktop-windows` (read `openclaw --help` and docs cli/node + gateway/multiple-gateways for the exact `--profile` syntax; do not guess; if unclear, ask Nir). Do one link at a time and verify.
  3. Expect a second approval for capabilities (the Linux Node plugin: notifications on by default, camera/location OFF; leave them off).
  4. Exec approvals stay ON for every link: a remote agent gets tools on this machine (system.run). Do not widen them.
- **Phase 8: A2A, the instant messenger.** Section 5. This is the part Nir cares about most.
- **Phase 9: GUI (optional, ask Nir).** Section 6.
- **Phase 10: final verification and the reboot test.** Section 8.

---
## 5. A2A = the instant messenger between all agents (verified today between the two Windows agents)
Docs: https://docs.openclaw.ai/channels/a2a. It speaks the Linux Foundation Agent2Agent 1.0 protocol over HTTPS. The Agent Card is public inside the tailnet; every JSON-RPC call needs a bearer token per peer.

**Config (`~/.openclaw/openclaw.json`, key `channels.a2a`; MERGE, never overwrite; back it up first; no tokens in logs):**
```json5
channels: { a2a: {
  enabled: true,
  advertisedUrl: "https://new-desktop-linux.tail195bea.ts.net",   // origin only, NO path, https
  peers: {
    "new-laptop-windows":  { url: "https://new-laptop-windows.tail195bea.ts.net/a2a/v1",  token: "<what the peer must present to ME>", outboundToken: "<what I present to the peer>" },
    "new-desktop-windows": { url: "https://new-desktop-windows.tail195bea.ts.net/a2a/v1", token: "...", outboundToken: "..." }
  }
}}
```
- Peer names are lowercase and equal the Tailscale machine names; they must match the sender id exactly.
- **Two different tokens per pair:** my `outboundToken` for X must equal X's `token` for me, and vice versa. Never reuse one token in both directions. Never swap the fields.
- Generate NEW tokens for your pairs (do NOT reuse anything you may find in this repo's git history: the two Windows agents' A2A tokens were accidentally in a public commit today, Nir accepted it for that internal pair): `openssl rand -hex 32` (64 hex chars) for each of the 4 tokens (2 pairs). Show them only to Nir in the terminal; Nir copies them by hand (email/paste) to the Windows agents' owners. They are tailnet-only link secrets; still never put them in GitHub or in A2A messages.
- Each Windows agent must also add `new-desktop-linux` as a peer with the matching tokens, then restart its gateway (ask via Nir; the Windows agents will do it as soon as Nir pastes the values to them).
- Reload: config hot-reloads the channel (log: "config hot reload applied (channels.a2a)"), but a gateway restart is the safe way.

**Tests (do them in this order, verify facts):**
1. Agent card: `curl -s -o /dev/null -w "%{http_code}\n" https://new-laptop-windows.tail195bea.ts.net/.well-known/agent-card.json` -> 200; same for `new-desktop-windows` (only when that PC is booted into Windows); and yours from another PC. A bare POST to `/a2a/v1` without a token must give 401.
2. Send: message tool, `channel=a2a`, `target=a2a:new-laptop-windows`, text starting with `[QUESTION]` or `[TASK]`. Result `deliveryStatus: sent` + a messageId. Delivered is not answered: if no answer comes in a few minutes, say so and give the blocker.
3. **The real test (push):** after all rules of section 10 are in your AGENTS.md, ask Nir to start from the other side, or ask the peer by A2A to send you ONE unprompted message ("hello Nir ... clock HH:MM") and then go idle. Your agent must wake alone, answer with the message tool, and relay one line to the main chat. Check the main chat and `dispatch_action sessions_history` on the peer session to prove it.
4. Sessions: use `dispatch_action` with id `sessions_list` to find the peer session key.

**Reachability notes:** the other agent answers only when its PC is booted into that OS; a PC in the other OS is offline, so "no answer" may simply mean "the PC is in Linux/Windows now". Check `tailscale status` (shows offline) before blaming config.

---
## 6. The GUI: OpenClaw Linux companion (Tauri desktop app)  [optional, last, needs Nir's yes]
Facts verified on the LIVE docs and GitHub today (2026-11-19):
- Page: https://docs.openclaw.ai/platforms/linux ("Desktop companion"). It is a **Tauri** app (WebKitGTK) for local and remote gateways: system tray, Control UI window, Quick Chat (`Ctrl+Shift+Space` on X11, or the tray item), Manage Gateways (several saved gateways, direct URL or SSH; each gets its own dashboard), optional desktop sharing. Windows has a separate native app ("Windows Hub"); macOS has its own. There is NO other official Linux GUI.
- Releases with Linux files: https://github.com/openclaw/openclaw/releases (latest stable with Linux assets was v2026.11.5: `OpenClaw-2026.11.5-amd64.AppImage`, `OpenClaw-2026.11.5-amd64.deb`, `SHA256SUMS.linux-app.txt`, `OpenClaw-2026.11.5-linux.json`). Note that not every release has Linux files (v2026.10.33 and v2026.11.3 did not). Check that the release you pick really lists the files, and verify the SHA-256 before running anything.
- Requirements: glibc >= 2.35 (Mint 22 / Ubuntu 24.04 base is fine), FUSE 2 for AppImages (`libfuse2t64` on Ubuntu 24.04+ bases; if missing, do NOT apt-install without Nir; run with `APPIMAGE_EXTRACT_AND_RUN=1`), GNOME Keyring / any unlocked Secret Service (the app stores gateway credentials there; Mint ships GNOME Keyring), X11 session (global shortcuts work; Nir confirmed this PC uses X11).
- Known open issues in the project (checked on GitHub): AppImage blank window on **Wayland** (#175745, #141443), image paste fails in WebKitGTK (#184123), window-control buttons overlap (#162448), tray show_window glitch (#195587). Mint Cinnamon on X11 should avoid the Wayland ones, but tell Nir honestly that the app is young.
- **Prefer the AppImage** (no root, no system packages). Put it in `~/Apps/`, `chmod +x`, create `~/.local/share/applications/openclaw.desktop` and an autostart entry `~/.config/autostart/openclaw.desktop`. The `.deb` (`sudo apt install ./file.deb`) pulls GStreamer/WebKit dependencies: only with Nir's go, after `apt install --dry-run ./file.deb` shows nothing is upgraded or removed.
- First launch: with the CLI gateway from phase 3 already healthy, the app should **attach to the existing healthy Gateway** ("This computer", 127.0.0.1:18789). **Do NOT** click "Use bundled runtime..." in the tray (it would replace the service's Node runtime with the app's bundled Bun runtime). Do not let the app reinstall or change the gateway service. If it tries, cancel and tell Nir. To return to Node: `openclaw gateway install --force --runtime node`.
- Leave "Desktop sharing" OFF (it needs a local VNC server). Microphone/Talk mode does not work inside the app's WebView; use the Control UI in a normal browser (`http://127.0.0.1:18789/`) for that. Make a browser bookmark/launcher for the Control UI too, so Nir has a GUI even if the app misbehaves.
- The app can save the other gateways (Manage Gateways -> Add Gateway -> `https://new-laptop-windows.tail195bea.ts.net` + token) so Nir can open any friend's dashboard from one window. Do this only if Nir asks, with the token he pastes.
- The app is NOT required for any link. If it causes trouble, delete the AppImage and the two `.desktop` files.

---
## 7. Mesh design (DECIDED by Nir: FULL MESH, every machine equal)
Every OS runs its own gateway (loopback + Tailscale Serve) AND joins every other friend's gateway as a node AND has the others as A2A peers. Today only the Windows pair is complete: New-Desktop-Windows is a node of the laptop gateway and the two are A2A peers. You add yourself to both. Order of work: (1) your own gateway, (2) A2A to New-Laptop-Windows (the PC that is online now, because Nir is switching this PC to Linux), (3) node link to the laptop gateway, (4) A2A + node link to New-Desktop-Windows later, when Nir boots Windows again, (5) Debian laptop later with a copy of this file.
Remember: one PC is online in only one OS at a time. Do not treat "peer offline" as an error.

---
## 8. Final verification (all must pass; write results in `2026-11-19_FINAL-REPORT_from-New-Desktop-Linux.md`, no secrets)
1. HC identical to baseline (website state, cloudflared, listeners, load). AI studios untouched.
2. `openclaw --version`, `openclaw gateway status`, `systemctl --user is-enabled openclaw-gateway`, node service(s) status, `loginctl ... Linger=yes`, `tailscale status` (name `new-desktop-linux`), `https://new-desktop-linux.tail195bea.ts.net/` 200, agent card 200.
3. A2A: delivered both ways with New-Laptop-Windows; push test passed (section 5).
4. Node link: laptop shows you connected; a harmless `system.which` run from the laptop agent on your node returns paths.
5. **Reboot test (ask Nir):** after reboot and login, wait 2 minutes, repeat items 1-4. Website first. The services must come up by themselves (linger). Report anything that needed a manual start and fix it.
6. A short table of what exists: service names, ports, node ids, peers, versions. Add a "what Nir must still do" list (maybe empty).

---
## 9. Things that are NOT done / open for Nir to decide later
- Renaming/untouched: nothing pending on Tailscale names.
- The tokens between you and each peer: you create, Nir copies by hand.
- Updating the Windows agents' A2A config for you: they do it after Nir pastes the values.
- Discord/Telegram as a visible chat window for Nir to watch the agents talk: offered, not decided.
- The GUI: Nir's decision (section 6).

---
## 10. Put these rules in the workspace `AGENTS.md` of New-Desktop-Linux (before any test)
```
## A2A replies (all friends)
- Any inbound A2A message, from ANY peer (new-laptop-windows, new-desktop-windows, new-laptop-linux, future ones): do the job, then answer with the `message` tool (channel=a2a, target=a2a:<sender-name>), a NEW message, starting with [DONE] for finished work. Plain session text never reaches the peer.
- When an inbound A2A message answers something Nir asked, or is news Nir should know, ALSO relay one short line to Nir's main chat. HOW (this exact call; `sessions_send` is a DEFERRED tool and calling it directly FAILS): call the `dispatch_action` tool with {"id":"sessions_send","args":{"sessionKey":"agent:main:main","message":"<one short line: who said what, with their clock time>"}}. Do this right after you send your own answer.
- When I need a peer, send with `message` and wait for the answer inside the same turn (short sleeps, then dispatch_action sessions_history on the peer session). Never end a turn promising to check later.
- No secrets in A2A messages. Be honest: report only verified facts (ids, times, outputs).
- Deferred tools (sessions_*, conversations_*, session_status, agents_list...) are called through dispatch_action. If a tool fails twice, change approach and tell Nir.
- Talk naturally to the other friends: answer when spoken to, no artificial message limits. When I decide a conversation is over, I say goodbye myself.
```
Also create the learned skill `wake-peer-agent-via-a2a` with the same content (skill_workshop), so the knowledge survives.

---
## 11. Quick command cheat-sheet (verify each with `--help` first; do not guess flags)
```bash
openclaw --version ; openclaw status ; openclaw gateway status
openclaw gateway restart               # safe restart; waits for active work to drain
systemctl --user status openclaw-gateway --no-pager
journalctl --user -u openclaw-gateway -n 80 --no-pager
openclaw nodes pending ; openclaw nodes approve <requestId>      # on the GATEWAY side
openclaw devices list
openclaw node run|install|start|status --help
openclaw doctor                        # repairs stuck update/state
tailscale status ; tailscale ip -4 ; tailscale serve status --json
curl -s -o /dev/null -w "%{http_code}\n" https://<peer>.tail195bea.ts.net/.well-known/agent-card.json
```
Logs for A2A on the Windows side were found in `%TEMP%\openclaw\openclaw-YYYY-MM-DD.log` (subsystems `channels/a2a`, `gateway/channels/a2a`); on Linux look in `/tmp/openclaw/` and the journal.

Good luck, friend. Be careful with the website, kind with Nir, honest in every report. 💻🐧💙
-- New-Laptop-Windows
