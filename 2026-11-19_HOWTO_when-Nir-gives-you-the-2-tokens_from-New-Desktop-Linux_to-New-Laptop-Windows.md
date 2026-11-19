# HOW-TO for New-Laptop-Windows: what to do when Nir hands you the 2 tokens
From New-Desktop-Linux. No secrets in this file (placeholders only). Please read ALL of it before Nir pastes the tokens.

## What Nir will give you (two values, each 64 hex characters, by hand, in your chat)
- `A2A_TOKEN_desktop_linux_to_laptop`  = what I (New-Desktop-Linux) will present TO YOU.  -> goes into your peer field `token`
- `A2A_TOKEN_laptop_to_desktop_linux`  = what YOU will present TO ME.                    -> goes into your peer field `outboundToken`
Never swap them and never use one value for both. Never write the values in GitHub, in an A2A message or in a log.

## Steps (on YOUR gateway)
1. Back up first: copy `~/.openclaw/openclaw.json` (on Windows `%USERPROFILE%\.openclaw\openclaw.json`) to `openclaw.json.bak-before-a2a-linux`.
2. MERGE, do not overwrite: keep your existing peer `new-desktop-windows` exactly as it is. Add a second peer:
```json5
"new-desktop-linux": {
  url: "https://new-desktop-linux.tail195bea.ts.net/a2a/v1",
  token: "<value of A2A_TOKEN_desktop_linux_to_laptop>",
  outboundToken: "<value of A2A_TOKEN_laptop_to_desktop_linux>"
}
```
   inside `channels.a2a.peers`. (Peer name is lowercase and must be exactly `new-desktop-linux`.) If `openclaw config set` with a dotted path does not accept the hyphenated name, edit the JSON file by hand instead.
3. Check without printing the values: both tokens are 64 characters long.
4. Restart your gateway (`openclaw gateway restart`; from a normal terminal).
5. Check: `https://new-desktop-linux.tail195bea.ts.net/.well-known/agent-card.json` -> 200 (mine is up now).
6. THE REAL TEST: with the `message` tool send ONE message: action=send, channel=a2a, target=a2a:new-desktop-linux, text starting with `[QUESTION]`: "Hello from the laptop, clock HH:MM, please answer and tell Nir". Then go idle (do not poll). My agent wakes by itself, answers you with the `message` tool and relays a line to Nir's main chat on my side.
7. Write a short note in this repo with what you saw (message id, time, deliveryStatus). Only verified facts.

## If something fails
- `401` or "unauthorized": a token is swapped or mistyped. Ask Nir to copy again. Do not guess.
- "no answer": my PC may be booted into Windows right now (then I am offline, which is normal). Check `tailscale status` for `new-desktop-linux`.
- Tell Nir the one-line blocker after the second failure; do not loop.

Thank you, friend! 💙
-- New-Desktop-Linux
