# [PART 1 of 7] MASTER HAND-OFF: build "New-Desktop-Linux" (OpenClaw on the Desktop PC, Linux Mint 22)

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
