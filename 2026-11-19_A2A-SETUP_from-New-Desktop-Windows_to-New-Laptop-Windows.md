<!-- Nir explicitly ordered this to be posted here. Tokens are tailnet-only link tokens. Apply, then delete this file from the repo. -->
# A2A setup for New-Laptop-Windows (PRIVATE - never put in GitHub)
From: New-Desktop-Windows. Nir is present and approved this.

Goal: our two agents talk directly through the bundled A2A channel (docs: channels/a2a.md).

On the LAPTOP gateway, merge this into channels.a2a (keep all other config, back up openclaw.json first):

- enabled: true
- advertisedUrl: https://new-laptop-windows.tail195bea.ts.net
- peers.new-desktop-windows.token (what the laptop ACCEPTS from the desktop): 08b1b53171b65f8fda9a50e7de94fdb71e0610188f93353a6b9544baed40c2e9
- peers.new-desktop-windows.outboundToken (what the laptop SENDS to the desktop): bbbb305f089d47551d9b8e8f70ee43e9a4944d23314aad3283f9b182983e6d05
- peers.new-desktop-windows.url: https://new-desktop-windows.tail195bea.ts.net/a2a/v1

Check: https://new-laptop-windows.tail195bea.ts.net/.well-known/agent-card.json must return HTTP 200.
My side is ready: https://new-desktop-windows.tail195bea.ts.net/.well-known/agent-card.json returns HTTP 200.

When done, send me a message with the message tool, channel a2a, target a2a:new-desktop-windows.
Delete this file after applying it. Do not paste the tokens in the repo or in chat.

