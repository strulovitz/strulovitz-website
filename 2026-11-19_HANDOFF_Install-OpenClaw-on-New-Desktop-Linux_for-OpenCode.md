# HAND-OFF: install OpenClaw on the Desktop PC's Linux Mint 22 ("New-Desktop-Linux")
Date: 2026-11-19 | Written by: New-Laptop-Windows (OpenClaw agent, bedroom) | For: OpenCode (Claude Sonnet 5.5) on the living-room Desktop PC, booted into Linux Mint 22
Human in charge: Nir (he is sitting at that PC and will paste any secret you ask for).

This repo is PUBLIC. NEVER write tokens, passwords or API keys in it. Communicate through files named `YYYY-MM-DD_<topic>_from-<NAME>_to-<NAME>.md`. Do `git pull` before reading and `git pull --rebase` before pushing.

---
## 0. RULES THAT OVERRIDE EVERYTHING (read twice)
1. **This Linux machine serves Nir's website strulovitz.org through a Cloudflare Tunnel. DO NOT BREAK IT.** The same will be true on the Debian 13 laptop later. Both machines are equally important to Nir.
   - Do NOT stop, restart, reconfigure, update or uninstall `cloudflared`, the web server (nginx/apache/node app/etc.), or their systemd units.
   - Do NOT touch the Cloudflare tunnel config/credentials (`~/.cloudflared`, `/etc/cloudflared`), DNS, or any site files.
   - Do NOT run `apt upgrade` / `apt full-upgrade` / `apt autoremove`, change the global Node.js, or change firewall (ufw/iptables/nftables) rules without asking Nir first. Do NOT reboot without Nir's OK (except the single planned reboot test in step 9, which Nir must approve).
   - Do NOT use Tailscale features that change the machine's routing/DNS: no exit node, no `--accept-routes`, no `--accept-dns=false/true` changes, no subnet routes. Do not run `tailscale up` with flags, `tailscale logout` or `tailscale down`.
   - BEFORE you change anything, do the **baseline snapshot (step 1)**. AFTER every major step, re-run the **website health check** and compare. If anything differs: STOP, undo your last step, tell Nir.
2. **Do not guess. If anything is unclear, STOP and ask Nir** (he is next to you). Also ask before anything destructive.
3. Prefer installs that stay in the user's home (no root, no system-wide changes). Use sudo only where this file says so, and show Nir the command first.
4. Keep OpenClaw's gateway on **loopback (127.0.0.1)**. Never bind it to 0.0.0.0 or the LAN.
5. Names (never get confused): agent = **New-Desktop-Linux**; Tailscale machine name = **desktop-linux** (already on the tailnet, 100.118.103.61); OS = Linux Mint 22. Others: New-Laptop-Windows (laptop-windows, 100.99.200.43), New-Desktop-Windows (desktop-windows, 100.107.152.18), future New-Laptop-Linux (Debian 13, laptop-linux).

---
## 1. Baseline snapshot of the website (BEFORE any change)
Run and save the output in `~/openclaw-baseline.txt` (outside the repo):
```bash
date; uname -a; cat /etc/os-release | head -3
systemctl status cloudflared --no-pager 2>&1 | head -15
systemctl list-units --type=service --state=running --no-pager | head -60
ss -tlnp 2>&1                       # which ports are in use (look for 80/443/3000/8080... and 18789)
node -v 2>&1; which node npm 2>&1
tailscale status 2>&1; tailscale ip -4
curl -sS -o /dev/null -w "local:%{http_code}\n" http://127.0.0.1:80/ 2>&1    # adjust port to what ss shows the site uses
curl -sS -o /dev/null -w "public:%{http_code}\n" https://strulovitz.org/
```
Ask Nir which local port/service actually serves the site if unclear. This is the **website health check** (HC): `systemctl is-active cloudflared`, the two curl lines, and `ss -tlnp` unchanged except for new OpenClaw ports.

---
## 2. Already known (do not redo)
- Tailscale is already installed on this machine and joined to Nir's tailnet as `desktop-linux`. Verify with `tailscale status`. Do NOT reinstall/relogin unless it is actually logged out (then ask Nir).
- The Windows laptop gateway is reachable ONLY inside the tailnet at `https://laptop-windows.tail195bea.ts.net` (port 443, TLS, Tailscale Serve, no Funnel). Gateway token auth. Windows desktop is already connected to it as a node (works, verified).
- OpenClaw version used on Windows: 2026.7.1-2 (the laptop reports a newer core in places). Model used by the Windows agents: `openrouter/anthropic/claude-sonnet-5.5`, thinking level **medium**.

---
## 3. Install OpenClaw WITHOUT disturbing the system
Docs (authoritative): https://docs.openclaw.ai (install, platforms/linux, gateway, cli/node, gateway/tailscale). Requirements: Node 24.15+ (or 22.22.3+ / 25.9+).
Because the website may use Node, **do not replace/upgrade the system Node**. Use the local-prefix installer, which keeps its own Node under `~/.openclaw`:
```bash
curl -fsSL https://openclaw.ai/install-cli.sh | bash
```
Show Nir the script URL first; he agrees. Then open a new shell, check `openclaw --version` and `which openclaw` (it must be under the home dir). Re-run **HC**.
(If that installer fails, ask Nir before falling back to `npm i -g openclaw@latest` with a user-level npm prefix. NOT `sudo npm`.)

---
## 4. Onboard: a full OpenClaw (gateway + CLI + Control UI), like the Windows ones
```bash
openclaw onboard --install-daemon
```
Answer prompts with Nir. Settings to choose / ask Nir for:
- Mode: local gateway, **bind loopback**, port **18789**. First check `ss -tlnp | grep 18789` - if taken, STOP and ask.
- Gateway auth: token (let it generate; keep it only in `~/.openclaw/openclaw.json`).
- Model provider: OpenRouter, model `openrouter/anthropic/claude-sonnet-5.5`, thinking level medium. **Ask Nir for the OpenRouter API key** (he will paste it into the terminal prompt/env, never into the repo).
- Agent identity: write in `IDENTITY.md`/`USER.md` in the workspace: Name **New-Desktop-Linux**, creature: AI assistant living in Nir's Desktop PC, Linux Mint 22 side of a dual-boot; user Nir, Haifa, Asia/Jerusalem; always polite, lots of emojis (Nir's standing request). Copy the style of the Windows agents (same SOUL/AGENTS conventions: ask before external actions, never leak secrets, no destructive commands, `trash` over `rm`).
- Channels: skip for now (the Windows agents use the local webchat/Control UI only). Ask Nir if he wants any.
Verify: `openclaw gateway status` -> Runtime running, Listening 127.0.0.1:18789, `openclaw status`. Re-run **HC**.

### GUI
- There is **no native Linux companion app** in the docs ("There is no native Linux companion app yet"). The Windows "Hub"/tray app is Windows-only. I do not know of a Tauri Linux app; do not claim one exists. Don't guess - check docs.openclaw.ai/platforms/linux and, if unsure, tell Nir.
- The GUI on Linux = the **Control UI / WebChat in the browser**: open `http://127.0.0.1:18789/` (log in with the gateway token; Nir pastes it). `openclaw dashboard` may open it with the token. Make a desktop launcher/bookmark for it (a `.desktop` file in `~/.local/share/applications` that runs `xdg-open http://127.0.0.1:18789/`). Optionally a tray/autostart is NOT needed.

---
## 5. Survive reboots - "forever" (systemd user service + linger)
`onboard --install-daemon` creates a systemd **user** unit (`openclaw-gateway.service`). Make it start at boot even before login:
```bash
systemctl --user enable --now openclaw-gateway.service
systemctl --user status openclaw-gateway.service --no-pager
sudo loginctl enable-linger $(whoami)     # ONLY sudo command here; show Nir first
loginctl show-user $(whoami) | grep Linger   # must say Linger=yes
```
Difference from Windows: Windows tasks start at login; Linux with linger starts at boot. Also check Tailscale: `systemctl is-enabled tailscaled` must be `enabled` (it is a system service, usually default).

---
## 6. Link A: New-Desktop-Linux as a NODE of the laptop-windows gateway (Linux -> Windows)
This mirrors what New-Desktop-Windows did. Separate service from step 4 (a node host is separate from your own gateway).
1. Nir copies the **laptop-windows gateway token** to you (from his email/clipboard). **Use ALL 48 characters.** Lesson learned the hard way: the Windows desktop first used a token shortened with "..." and got `token_mismatch`. If a token contains `...` or `…`, it is truncated: ask for the full one.
2. Quick foreground test (token only for this shell, not saved in history if possible):
```bash
read -rs OPENCLAW_GATEWAY_TOKEN; export OPENCLAW_GATEWAY_TOKEN
openclaw node run --host laptop-windows.tail195bea.ts.net --port 443 --tls --display-name "New-Desktop-Linux" --node-id desktop-linux-node
```
3. First time it says `pairing required (requestId: ...)`. Write that requestId in a repo file `2026-11-19_node-pairing-request_from-New-Desktop-Linux_to-New-Laptop-Windows.md` (NO token) and tell Nir to prompt New-Laptop-Windows to approve. After approval, re-run; it should print `node host gateway connected`.
4. Do NOT run `openclaw nodes status`/`devices` against the laptop gateway from here: on Windows that changed the device identity and caused an extra re-pair request. Use the repo mailbox instead.
5. Make it permanent: stop the foreground run, then
```bash
openclaw node install --host laptop-windows.tail195bea.ts.net --port 443 --tls --display-name "New-Desktop-Linux" --node-id desktop-linux-node
openclaw node start; openclaw node status
```
(check `openclaw node install --help` first for exact option names; the gateway token must be available to the service: use the mechanism the docs describe - env in the unit or `~/.openclaw` config - and verify that the stored value is the FULL token without printing it, e.g. check its length is 48.) Linger from step 5 covers boot start. Then write `..._reply_from-New-Desktop-Linux_...md` (no secrets) and let New-Laptop-Windows verify with `system.which` on your node.
6. Exec approvals stay ON for the node (the laptop agent can only run what is allowed). Do not widen them without Nir.

---
## 7. Link B: New-Desktop-Linux's OWN gateway reachable from the other machines (Windows -> Linux, Linux -> Linux later)
Goal: the other agents can connect to this machine too, symmetric to what laptop-windows offers. **First read** docs `gateway/tailscale`. Plan:
1. Check Tailscale Serve is allowed on the tailnet (Nir already enabled HTTPS certificates; Funnel is OFF and must stay OFF - never run `tailscale funnel`).
2. **Port conflict check (website safety):** `tailscale serve` on 443 binds only the tailnet IP, but verify with `ss -tlnp | grep ':443'` that nothing else (nginx/apache) listens on 0.0.0.0:443 first. If something does, use a different HTTPS port for OpenClaw, e.g. `tailscale serve --bg --https=8443 18789`, and tell the other agents the port. Also `tailscale serve status` must show no pre-existing config you would overwrite (inspect first; if the website already uses Tailscale Serve, STOP and ask Nir).
3. Prefer the OpenClaw-managed way: config `gateway.tailscale.mode = "serve"` with `gateway.bind = "loopback"` (this setting is protected: **Nir must run** `openclaw config set gateway.tailscale.mode serve` and `openclaw gateway restart` himself - an agent patch is refused). If the first start says "Serve is not enabled on your tailnet", Nir opens the link it prints and approves (already done once for this tailnet; Funnel stays off).
4. Result address (expected): `https://desktop-linux.tail195bea.ts.net` (port 443, or 8443 if you had to move it). Re-run **HC**. Tell New-Laptop-Windows the final address in the mailbox; token goes to others through Nir only.
This is "Link B"; New-Desktop-Windows / New-Laptop-Windows will later connect as nodes to it (Windows -> Linux) the same way you did in step 6.

---
## 8. Open decision for Nir (ASK, do not decide alone)
Right now one node host process connects to ONE gateway. Nir wants every machine pair connected (Win-Win done, Win-Linux, Linux-Win, Linux-Linux). Options: (a) a central hub gateway that all others join as nodes (simple), or (b) every machine runs its own gateway AND runs extra node-host profiles (`--profile`/separate service) to join each other's gateways (full mesh, more services). Recommend to Nir: start with step 6 (joins the existing hub), then step 7, then decide on mesh together with New-Laptop-Windows. Same design will be reused for the Debian 13 laptop ("New-Laptop-Linux", tailscale name laptop-linux): same steps 1-9, only names and the Cloudflare check differ.

---
## 9. Final checks (all must pass), then reboot test (ask Nir to approve the reboot)
- HC identical to baseline; `https://strulovitz.org/` returns the same code as before; `cloudflared` still active.
- `openclaw gateway status` OK, node service running, Linger=yes, `tailscale status` OK.
- After Nir approves a reboot: log in, wait 2 min, repeat all the checks (website first!). Write the results in `2026-11-19_final-report_from-New-Desktop-Linux.md` (no secrets): versions, ports, service names, what Nir still has to do, anything unexpected.
- Optional: ask New-Laptop-Windows (via mailbox) to run a harmless `system.which` on your node.

## Reporting protocol
After each numbered step, if something failed or Nir must act, append a short note to a repo file named `2026-11-19_progress_from-New-Desktop-Linux.md` (pull first; push after). Never paste tokens. Ask Nir immediately for anything unclear.

-- New-Laptop-Windows 💻 (for Nir, with love)
