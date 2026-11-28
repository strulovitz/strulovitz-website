CHECKLIST FOR NIR -- bring the websites back, then add "pre"
date: 2026-11-28
written by: the agent on the desktop
Parts: 01 (1.4, 1.9, 1.12 O2), 11 (11.5), 09 (9.5)

Checked before writing this: the tunnel token exists at
~/.config/site-hosting/tunnel-token with permission 600; the three user
services site-caddy, site-tunnel and site-nosleep are installed; ports 8081
to 8084 are free; nothing of the hosting is running. So both steps below can
be done now.

PART 1 -- BRING THE WEBSITES BACK, FROM THIS DESKTOP
(AM-LAW 12: only one PC serves, and the tunnel never starts by itself. The
laptop's services are OFF, so this PC may serve.)

1. On the desktop, find the icon named "sites-on" (Websites ON).
2. Double-click it. A black terminal window opens and prints lines.
3. Wait. It prints "Starting the local websites, tunnel, and keep-awake
   service...", then "Websites started. Checking every menu link...", then the
   sites-check result. This takes under a minute.
4. Read the last lines. If they say "!!! sites-check found problems", copy
   those lines and give them to the agent. Do not close anything else.
5. If there is no such warning, the three websites are back:
   www.strulovitz.org, learnime.com, peaktogether.me.

NOTE: the same start also loads our own Attract Mode block, which answers on
port 8084 with the sentence "Attract Mode is being built." That is expected:
nothing public points at it yet.

PART 2 -- ADD "pre" AT CLOUDFLARE (owner act O2, Part 01, 1.12)
The tunnel runs with a TOKEN, so its addresses live in Cloudflare's dashboard,
not in a file on this PC.

1. Open https://dash.cloudflare.com and sign in.
2. In the left sidebar click "Zero Trust".
3. In its left menu: "Networks", then "Tunnels".
4. Find the tunnel that says it is healthy -- it is the one this PC started a
   minute ago. Click its name.
5. Open the tab "Public Hostname", press "Add a public hostname".
6. Fill exactly:
      Subdomain:  pre
      Domain:     strulovitz.org
      Path:       (leave empty)
      Service Type:  HTTP
      URL:        localhost:8081
7. Press Save. Cloudflare makes the DNS record itself.
8. Wait one minute, then open https://pre.strulovitz.org in a private window.
   It must show the existing site (AI Panorama), exactly as www did.
9. Tell the agent: "pre is added". The agent will fetch it from outside,
   confirm it, and record card 0-14 as done.

IF SOMETHING IS DIFFERENT ON THE SCREEN
Stop and say what you see, in your own words. Do not guess, and do not change
anything else in Cloudflare: the same tunnel carries the three live websites.

WHY 8081 AND NOT 8084
Part 01, section 1.4: 8081 is the old site and it is what "pre" must show.
8084 is Attract Mode (Moodle), and it becomes www only on Switch Day.
