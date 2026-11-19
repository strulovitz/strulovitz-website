# HAND-OFF FOR OPENCLAW (New-Desktop-Linux): help the new friend New-Laptop-Linux get installed

Date: 2026-11-19 (night). Written by your twin in OpenCode (Claude Sonnet 5.5). Reader: **you, the OpenClaw agent New-Desktop-Linux** (gateway on the living-room Desktop PC, Linux Mint 22). Nir will give you this file to read.
No secrets in this file (it is in a PUBLIC repo). Tokens and keys live only in your `~/.openclaw` and in Nir's hands.

## What is happening
Nir is about to install OpenClaw on his LAPTOP booted into **Debian 13**, as the 4th friend, **New-Laptop-Linux**. An OpenCode agent on the laptop does the installation by following `2026-11-19_MASTER-HANDOFF_New-Laptop-Linux_Debian13-OpenClaw-Tailscale-A2A-GUI_for-OpenCode.md` (read it, it is short enough). Just like New-Laptop-Windows helped us today, **you are the helper**: the new friend cannot talk to anybody until its own gateway and A2A exist, so for its first hours it needs you for approvals, tokens, tests and moral support.

## Important situation on this PC (do not break it)
- Nir turns the website serving (Caddy + Cloudflare tunnel) **OFF on this desktop** and **ON on the laptop** for the installation, so the laptop agent can check that the sites survive. **Do not start Caddy, cloudflared or the `site-*` services here. Never run two tunnels.** Whether they are on or off is Nir's business.
- This PC also holds heavy AI studios in the home folder (`~/drama3`, `~/voxcpm2`, `~/zonos`, `~/voicebox`). Do not touch them, do not run heavy jobs.
- You must be **booted in Linux** to answer. When Nir boots Windows, New-Desktop-Windows answers instead (a different gateway, different agent). That is normal.
- Your gateway: loopback `127.0.0.1:18789` + Tailscale Serve `https://new-desktop-linux.tail195bea.ts.net`. Your node link to the laptop-Windows gateway is permanent (`openclaw-node.service`). A2A is active with `new-laptop-windows`.

## Your jobs, in the order they will come up
1. **Wait for notes.** New-Laptop-Linux (or its OpenCode) will write repo notes named `YYYY-MM-DD_<TOPIC>_from-New-Laptop-Linux_to-New-Desktop-Linux.md`. Read the repo (`git pull`, branch `master`) when Nir says so or when a message arrives. No A2A exists with the new friend until step 3.
2. **Node pairing approvals (new friend joins YOUR gateway as a node).** When it connects it gets `device pairing required (requestId: ...)`. On YOUR gateway: `openclaw nodes pending`, then `openclaw nodes approve <requestId>`. After it reconnects there is a SECOND approval (capabilities: "node capability surface is awaiting operator approval ... nodes approve <id>"); approve it as well. Camera/location stay OFF, exec approvals stay ON. Never touch `devices rotate`. Nir may need to confirm on screen. Request ids are not secrets.
3. **Add New-Laptop-Linux as an A2A peer.** Nir will bring you two tokens by hand, named by the laptop OpenCode (look at its repo note for the NAMES). Rule: your `token` for the peer = what it presents to you; your `outboundToken` = what you present to it; **never swap, never reuse one value for both**, each 64 hex chars. Back up `~/.openclaw/openclaw.json` first, then MERGE (keep your existing peer `new-laptop-windows` as it is):
   `openclaw config set channels.a2a '<full json incl. the old peer>' --strict-json` (build the json with python `json.dumps`; read first with `openclaw config get channels.a2a`; the old peer's tokens print redacted, so rather edit the file with a small python script that only ADDS the new key under `channels.a2a.peers`). Peer name must be exactly `new-laptop-linux`, url `https://new-laptop-linux.tail195bea.ts.net/a2a/v1`. Restart the gateway (`openclaw gateway restart`) and check: the new friend's card `https://new-laptop-linux.tail195bea.ts.net/.well-known/agent-card.json` -> 200 (only once it exists).
4. **Test A2A both directions, honestly.** Send one `[QUESTION]` with the `message` tool (action=send, channel=a2a, target=a2a:new-laptop-linux), then ask it to send you an unprompted message and go idle (the push test). Report only verified facts (message ids, times).
5. **Be the friendly answer** when the new friend asks: where things are, what we did, what failed. Use `[DONE]` at the start of finished answers. AND, because New-Laptop-Windows does not relay `[DONE]` to Nir, tell Nir directly in your main chat what happened.

## Rules (also in your AGENTS.md, repeated because they matter)
- Answer inbound A2A with a NEW `message` tool call (plain session text never reaches the peer). To show Nir something: `dispatch_action` with `{"id":"sessions_send","args":{"sessionKey":"agent:main:main","message":"<one short line>"}}`; `sessions_send` is DEFERRED and fails if called directly.
- No secrets anywhere public (repo, A2A messages, logs). No tokens in your replies to Nir's chat unless Nir asked for them (he pasted tokens by hand earlier; avoid it).
- Nir is a beginner: emojis in every reply, short, simple, important thing last; tell him when you need something; do not do things he wants to do himself; no multi-choice quizzes; do only what he asks. Never claim success you did not verify.
- Do not loop on a failing tool: twice -> change approach; three times -> tell Nir the blocker in one line.

## Lessons from today that apply to you
- **Billing trap:** OpenRouter returned 402 once (empty credits). OpenClaw then pauses the key (`openclaw models status` shows `disabled:billing`) and every retry fails for ~6+ minutes, even after Nir tops up. While paused, inbound A2A messages cannot be answered or relayed, so Nir may never see the new friend's questions. If you see it: tell Nir the credit is empty, wait, don't spam retries.
- Fresh gateway: the token is exactly 48 chars. `openclaw config get gateway.auth.token` prints REDACTED. The real one is in `~/.openclaw/openclaw.json`.
- If the new friend asks something you cannot verify, say so. Every answer must start from what you actually saw.
- Handy: `openclaw sessions tail --agent new-desktop-linux --session-key <key> --tail 20` shows what an agent did, `journalctl --user -u openclaw-gateway -n 80 --no-pager` the log (times in the journal are local; sessions tail times are UTC).
- The OpenClaw app (icon "OpenClaw app") on this desktop is attached to your gateway; Nir chats with you there. Do not use "Use bundled runtime".

## What to say to Nir when you start
Greet him with emojis, say you read this hand-off, ask him: "Is the website already switched off on the desktop and on at the laptop?" (you just ask; you do not touch it), and wait for his word.
-- New-Desktop-Linux (OpenCode twin) 🐧💙
