# Opus 5.5: website source locations, corrected (2026-09-28)

This supersedes `CLAUDE_OPUS_LOCAL_WEBSITE_PATHS_2026-09-28.md`. Nir does not want a new `~/websites/` tree; both empty folders created earlier were removed. No live-site backup/download or live-versus-GitHub comparison has happened. Do not assume the GitHub versions match the live sites.

- **strulovitz.org:** `/home/nir/strulovitz-website/site/` (home page `site/index.html`); repository `/home/nir/strulovitz-website/`, GitHub `strulovitz/strulovitz-website`, local `master` matches `origin/master`.
- **learnime.com:** `/home/nir/Anime/learnime-site/` (home page `learnime-site/index.html`); repository `/home/nir/Anime/`, GitHub `strulovitz/Anime`. The worker fetched and fast-forwarded its existing local `main` to GitHub commit `3458dc4` (806 commits ahead of the old checkout). The pre-existing untracked `AGENTS.md`, `media/`, `tools/ComfyUI/`, and `tools/sd-scripts/` were preserved; do not delete or commit them as part of website work.
- **peaktogether.me:** `/home/nir/peaktogether-website/` (home page `index.html`); GitHub `strulovitz/peaktogether-website`. The worker searched the accessible Linux root filesystem without crossing to Windows/NTFS: no existing local folder or Git remote for this site was found. With Nir's permission, cloned the repository directly beside the other repositories; local `master` matches `origin/master` at `822d9cc` and is clean.

Read-only system checks found Debian 13.6 on the USB `/dev/sda4` (model reported as P40 Game Drive), Apache active on port 80, no installed `cloudflared` service/config, and lid-close suspend by default. Privileged firewall/process checks were not completed. No service, firewall, Windows partition, or server configuration was changed. No credentials belong in the public GitHub history or Opus hand-offs.

Please use these actual paths in future instructions. Give Nir one small step at a time, and keep future hand-offs concise; do not repeat your own instructions to you.
