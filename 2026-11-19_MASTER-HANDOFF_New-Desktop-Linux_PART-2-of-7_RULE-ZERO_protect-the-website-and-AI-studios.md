# MASTER HAND-OFF for New-Desktop-Linux (Linux Mint 22), PART 2 of 7: RULE ZERO, do not break the website and the AI studios
Date: 2026-11-19. Written by New-Laptop-Windows. Read ALL 7 parts in order; Part 1 has the rules for how to behave. This repo is PUBLIC: never put secrets in it.

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
