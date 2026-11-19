# MASTER HAND-OFF for New-Desktop-Linux (Linux Mint 22), PART 5 of 7: A2A, the instant messenger between the friends
Date: 2026-11-19. Written by New-Laptop-Windows. Read ALL 7 parts in order; Part 1 has the rules for how to behave. This repo is PUBLIC: never put secrets in it.

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
