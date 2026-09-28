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
- `SESSION_STATE_DEBIAN_13_RTX5090.md` already has an unrelated uncommitted change. Leave it untouched and exclude it from this commit.
- Next: ask Nir before beginning the read-only inspection; continue the original task one small step at a time. Do not change existing Cloudflare or server settings.
