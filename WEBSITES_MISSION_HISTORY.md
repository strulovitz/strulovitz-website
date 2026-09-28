# Websites mission history

Shared coordination for strulovitz.org, learnime.com, and peaktogether.me. Append new instructions, actions, outcomes, and replies here as the mission progresses. Keep site-specific website work in its own repository; never record tokens, passwords, or other secrets.

## 2026-09-28: Original instructions from Claude Opus 5.5 (verbatim)

```text
You are working on my Debian 13 laptop. I am a complete beginner. Another AI (Claude) is the project manager; you are the worker. Your job right now is ONLY: (A) a READ-ONLY inspection of this computer, and (B) making backups of my 3 websites into a new folder. Nothing else.

STRICT RULES:
1. Do NOT install, remove, upgrade, or reconfigure anything yet. No apt install, no apt upgrade, no editing files in /etc, no enabling/disabling services.
2. Do NOT touch, mount, or write to any Windows/NTFS partition or any disk other than this Linux system. Commands like lsblk are fine because they only read.
3. If an existing Cloudflare tunnel/cloudflared setup exists, do NOT change or delete it. Just report it.
4. If a command needs sudo and asks for a password you can't type, STOP and give me the exact command so I can run it myself in a separate terminal, then wait for me to paste the output.
5. Only create files inside ~/websites/ (create this folder).

PART A - Inspection. Run these and summarize the results:
- cat /etc/os-release ; uname -a ; whoami ; hostname
- df -h / /home ; lsblk -f   (read-only, just to confirm we're on the external WD_Black NVMe)
- which git curl wget rsync lftp sftp cloudflared nginx caddy apache2 python3
- cloudflared --version (if it exists)
- systemctl status cloudflared --no-pager (if it exists) ; ls -la /etc/cloudflared ~/.cloudflared 2>/dev/null
- sudo ss -tlnp   (which ports are already in use, especially 80, 443, 8080-8090)
- systemctl is-active nginx apache2 caddy 2>/dev/null
- sudo ufw status 2>/dev/null ; sudo nft list ruleset 2>/dev/null | head -50
- Power/sleep: check whether the laptop suspends automatically (e.g. systemd-logind settings, lid switch) and just report it.

PART B - Backups (only inside ~/websites/backups/):
1. List my public GitHub repos: curl -s "https://api.github.com/users/strulovitz/repos?per_page=100" and show name + last push date for each.
2. Figure out which repos are the source for these 3 websites: strulovitz.org, learnime.com, peaktogether.me (look for CNAME files, matching titles, or index.html content). git clone each of those 3 into ~/websites/backups/github/. If you are unsure which repo matches which site, ask me.
3. Download the LIVE sites exactly as they are served today:
   cd ~/websites/backups/live && for s in www.strulovitz.org learnime.com www.peaktogether.me; do wget --mirror --page-requisites --no-parent -e robots=off --wait=0.3 "https://$s/"; done
   (Also try without "www." / with "www." if one fails.)
4. For each site, COMPARE the live download with the GitHub copy: list files that are on the live site but missing from GitHub, and vice versa (ignore .git). Tell me if GitHub looks outdated.
5. Look through all the files and report: are there any .php, .py, .cgi, .htaccess files, HTML <form> tags that post to the server, or anything else that needs a server-side program? Or is it 100% static (HTML/CSS/JS/images)? Also note total size of each site and any very large files (>50 MB).

FINISH with a section titled "REPORT FOR CLAUDE" containing: OS details, which tools are installed/missing, any existing cloudflared/web server setup (with config contents, but hide any token/secret values), ports in use, sleep settings, the repo↔site mapping, the live-vs-GitHub comparison, and the static/non-static verdict. Keep it compact.
```

## 2026-09-28: User's additional instructions and current progress

- Nir wants this shared history in the existing `strulovitz/strulovitz-website` repository, not a new repository. This explicitly permits this one file outside `~/websites/`; the original inspection and backup restrictions otherwise remain in effect.
- Future work on strulovitz.org belongs in `strulovitz-website`, work on learnime.com in `learnime`, and work on peaktogether.me in `peaktogether`. Shared coordination goes here in `strulovitz-website`, the gateway to all three. Claude: please give future instructions with this arrangement in mind.
- Nir wants Claude's instructions recorded verbatim and subsequent actions, successes, failures, and replies appended to this file and pushed to GitHub after each round.
- The worker asked for permission before the read-only inspection. Before it began, Nir requested this GitHub hand-off instead. No OS/network inspection or site backup has been performed yet.
- Found the local repository at `~/strulovitz-website` with `origin` set to `https://github.com/strulovitz/strulovitz-website.git`; GitHub CLI is already logged in as `strulovitz` with repository access. No new GitHub connection was needed.
- `SESSION_STATE_DEBIAN_13_RTX5090.md` had an unrelated uncommitted change. It was excluded from the history commit; Nir later explicitly authorized discarding that change, and the file itself remains.
- Next: ask Nir before beginning the read-only inspection; continue the original task one small step at a time. Do not change existing Cloudflare or server settings.

## 2026-09-28: GitHub publishing result

- First push of the history commit was rejected because GitHub's `master` had 155 newer commits. No force-push was attempted.
- With Nir's explicit permission, discarded only the unrelated uncommitted edit in `SESSION_STATE_DEBIAN_13_RTX5090.md`, fetched the newer commits, and rebased the one-file history commit. The push succeeded. No website files or server settings were changed.

## 2026-09-28: Read-only inspection and local path check

- Nir clarified that Learnime's GitHub source is `Anime/learnime-site`. The local `~/Anime` checkout is older and lacks that folder; `~/strulovitz-website/site/` exists; no local Peak Together checkout was found under `/home/nir`.
- Started read-only OS/service/port checks; no privileged firewall details were obtained. No site downloads or repo clones occurred.
- Created empty `~/websites/backups/` and `~/websites/` per the original backup instructions, then immediately removed both empty directories when Nir said he does not want that new backup tree. Do not recreate it without his permission.
- Nir requested a concise, standalone report for Opus, not Opus's earlier instructions repeated. See `CLAUDE_OPUS_LOCAL_WEBSITE_PATHS_2026-09-28.md` for the actual findings and remaining questions.

## 2026-09-28: Existing checkouts updated and Peak Together located

- Nir authorized using existing folders and, only if no Peak Together checkout existed anywhere accessible on the Linux root filesystem, creating a clone alongside the other repositories in `/home/nir`.
- Fetched and fast-forwarded the existing `~/Anime` from `633a58c` to `3458dc4`; `~/Anime/learnime-site/` is now present. Preserved all pre-existing untracked files.
- Searched the accessible Linux root filesystem for Peak Together names and Git repositories/remotes without crossing filesystem boundaries; none existed. Cloned `strulovitz/peaktogether-website` into `~/peaktogether-website/`, currently at `822d9cc` and clean.
- All three GitHub source folders are now local: `~/strulovitz-website/site/`, `~/Anime/learnime-site/`, and `~/peaktogether-website/`. The earlier local-paths hand-off is superseded by `CLAUDE_OPUS_WEBSITE_LOCATIONS_UPDATED_2026-09-28.md`. Live-site comparison/backups still have not happened.

## 2026-09-28: Claude's corrected inspection instructions

- Saved Claude's replacement instructions verbatim in `hosting-migration/2026-09-28-claude-corrected-instructions.md` and pushed that file first. No earlier saved prompt mentioned WordPress.
- Inspected Git checkouts for duplicates, compared the three live home pages with their GitHub sources, checked static-site assets and scripts, and performed read-only system checks. No site content, server settings, or Windows disks were changed.
- Compact results and limitations are in `hosting-migration/2026-09-28-report-for-claude.md`. Privileged firewall/process details were not obtained; do not put any password into commands or public GitHub files.
