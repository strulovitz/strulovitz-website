# Claude's Apache investigation instructions, 2026-09-28 (verbatim)

```text
From Claude (manager). Great report, thank you. Next: read-only investigation + a proposal. Still NO installs, NO config changes, NO service changes.

TASK 1 - Update hosting-migration/domains-status.md: learnime.com and peaktogether.me were also added to Cloudflare (Free) on 2026-09-28, with the SAME nameservers as strulovitz.org (lia.ns.cloudflare.com, stanley.ns.cloudflare.com). Use the same format as the strulovitz.org section. Save this prompt as a dated .md next to the others. Commit + push.

TASK 2 - The existing Apache on port 80 (do NOT stop or change it):
- sudo systemctl status apache2 --no-pager; apache2ctl -S 2>/dev/null (or sudo); ls -la /etc/apache2/sites-enabled/; show the enabled site configs; ls -la /var/www/
- What is it serving, and since when (package install date: grep apache2 /var/log/dpkg.log* or zgrep)? Does anything depend on it? Is this likely leftover from an earlier self-hosting experiment?
- Also check for other leftovers from earlier Cloudflare Tunnel use: dpkg -l | grep -iE 'cloudflared|caddy|nginx'; ls /etc/apt/sources.list.d/; any cloudflared binary anywhere (find / -name 'cloudflared*' -xdev 2>/dev/null | head).

TASK 3 - strulovitz.org deploy layout:
Read ops/deploy.sh, ops/build-export.py and ops/deploy_windows.py. Explain in plain terms what the deployed DreamHost directory looks like: how site/, ghost/, hive/, v2026-09-11-c/ exports and pointer.json get combined, and what command builds it. Where does the build output go? Is exports/ gitignored? We want to serve the SAME layout locally, built from the repo (the output may stay inside the repo's own gitignored exports/ folder; no new top-level folders). Do NOT run the build yet; just tell me the exact command you would run and whether it has any side effects (network, uploads, deletions).

TASK 4 - peaktogether-website/.htaccess: show its full content. Also check learnime-site and strulovitz for any .htaccess. For each rule, say what it does and whether it matters for a local static server.

TASK 5 - Also check any other redirects the live sites depend on (e.g. strulovitz.org -> www, http -> https): run curl -sI for http:// and https://, with and without www, for all 3 domains, and report the status + Location headers.

FINISH with "REPORT FOR CLAUDE" (compact) plus your own recommendation: which static web server to use (bound to 127.0.0.1 only, running as user nir because /home/nir is 700, not conflicting with Apache on :80, and easy to replicate identically on Linux Mint 22). Do not implement it yet.
```
