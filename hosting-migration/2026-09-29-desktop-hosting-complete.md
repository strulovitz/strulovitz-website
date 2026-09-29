# Desktop website hosting complete — 2026-09-29

Nir confirmed: "everything works great!!! :-)"

- The existing desktop clones of `strulovitz-website`, `Anime` (including `learnime-site`), and `peaktogether-website` are up to date. No duplicate repositories were created.
- Linux Mint desktop (`mint-desktop`) has Cloudflare's `cloudflared` 2026.9.3 and official Caddy v2.11.4; Caddy's release SHA-512 checksum was verified.
- The desktop built its own export `v2026-09-29-a`; only its pointer history file was committed. The three pre-existing local OpenRouter snapshot changes were left untouched.
- The tunnel token is stored only outside the repositories in a private file; its value is not included here.
- The public apex and `www` addresses for strulovitz.org, learnime.com, and peaktogether.me each returned a 200 homepage and identified `mint-desktop` at `/hosted-by` during the Phase 4 checks.
- **Websites ON** and **Websites OFF** launchers are installed in the applications menu and on the desktop, executable and trusted on Cinnamon. The installer continues to support GNOME on the laptop.
- Both launchers were tested using `gtk-launch`: OFF stopped the three user services; ON restarted them. The final public `/hosted-by` check identified `mint-desktop`. The sites were left ON.
- The launchers and user services were not enabled to start automatically at boot. No old DreamHost deploy script was run.

The verbatim Claude Opus 5.5 Phase 1, 2, and 5 prompts are in this folder. Phase 4 contained the private tunnel token and was deliberately **not saved to GitHub**.
