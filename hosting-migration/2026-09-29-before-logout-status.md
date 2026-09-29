# Website hosting status before GNOME logout — 2026-09-29

This is the short handoff for Nir's next OpenCode session on the Debian 13 laptop (`deb-server`). Claude Opus 5.5 is coordinating the laptop-to-desktop move. The full desktop plan is in [`HANDOFF-for-desktop.md`](HANDOFF-for-desktop.md).

## Verified now

- `site-caddy`, `site-tunnel`, and `site-nosleep` are **active**. All three local homepages on `127.0.0.1:8081`, `:8082`, and `:8083` return HTTP 200.
- The **public** `/hosted-by` pages at `https://strulovitz.org/hosted-by`, `https://learnime.com/hosted-by`, and `https://peaktogether.me/hosted-by` each say `Served by deb-server (home PC via Cloudflare Tunnel)`. The laptop is hosting all three sites at this check.
- Two launchers, **Websites ON** and **Websites OFF**, were installed both in the applications menu and in the actual GNOME desktop folder (`/home/nir/Desktop`). Their executable desktop copies are marked trusted. Both opened a visible terminal and worked in a live OFF-then-ON test; the terminal stays open with `Press Enter to close`. The installer is `hosting/bin/install-launchers` and is reusable on the Linux Mint desktop.
- GNOME's Desktop Icons NG (DING) extension was installed and added to the user's enabled-extensions setting. This running GNOME session did not yet recognize the newly installed extension: **log out and back in** to show the desktop icons. The menu entries are installed already. If GNOME asks, right-click an icon and select **Allow Launching**.
- `loginctl show-user nir -p Linger` returned `Linger=yes`, so logging out should leave the running user services active. The hosting services are linked but **not enabled at boot**; after a reboot, use **Websites ON** and check that the websites respond.
- GitHub commit `8abaee4` contains the launcher installer, Claude's saved launcher prompt, README update, and the appended desktop handoff. The tunnel token is only in a protected local file outside GitHub; never read or publish it.

## Next step

Nir can close OpenCode, log out of GNOME, and log back in. Look for **Websites ON/OFF** on the desktop and in the applications menu. On returning, check the sites are still running and the icons appear. Do not run both computers' hosting services simultaneously; switch by turning **OFF** the old PC first, then **ON** the new one. Claude's handoff says the DreamHost-to-Cloudflare registrar transfer was pending around October 2; its completion was not checked here.
