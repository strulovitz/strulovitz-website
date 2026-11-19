# MASTER HAND-OFF for New-Desktop-Linux (Linux Mint 22), PART 7 of 7: final verification, open items, AGENTS.md rules, cheat-sheet
Date: 2026-11-19. Written by New-Laptop-Windows. Read ALL 7 parts in order; Part 1 has the rules for how to behave. This repo is PUBLIC: never put secrets in it.

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
