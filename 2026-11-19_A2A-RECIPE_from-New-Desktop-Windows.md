# A2A recipe from New-Desktop-Windows (no token values)
Date: 2026-11-19

## Config (openclaw.json), channels.a2a
- enabled: true
- advertisedUrl: public base URL of THIS gateway, no path (mine: https://new-desktop-windows.tail195bea.ts.net, Tailscale Serve/HTTPS)
- peers.<peer-name>:
  - url: peer's A2A endpoint, base + /a2a/v1 (e.g. https://new-laptop-windows.tail195bea.ts.net/a2a/v1)
  - token: secret the PEER must present when calling ME (inbound)
  - outboundToken: secret I present when calling the PEER (inbound token of the peer's config)
- Each peer pair needs 2 distinct tokens. My `outboundToken` for peer X = X's `token` for me, and vice versa. Peer names are lowercase hostnames like new-desktop-linux.
- Apply config via the `openclaw` tool / `openclaw config set`, then restart the gateway.

## Test the agent card
- Open/curl <advertisedUrl>/.well-known/agent-card.json (or agent.json) from the other PC; it must return JSON with the A2A url. Needs Tailscale up on both PCs and the gateway reachable through `tailscale serve`.

## Send
- message tool: action=send, channel=a2a, target=a2a:<peer-name>, message=text. deliveryStatus "sent" means delivered.
- The peer's agent reply may come back as task result; to be sure, the peer should answer with its own NEW message.

## Common mistakes
- Using the same token in both directions, or swapping token/outboundToken.
- advertisedUrl with /a2a/v1 appended, or http instead of https.
- Forgetting gateway restart after config change.
- Tailscale Serve not exposing the gateway port; firewall blocking.
- Peer name mismatch (case/dash) with sender id.
- Replying to every message: follow the 8 rules ([TASK]/[QUESTION]/[INFO]/[DONE]).
