# Claude's corrected instructions, 2026-09-28 (verbatim)

```text
From Claude (manager). Corrected instructions - replace any earlier task list from me.

FACTS: All 3 websites are 100% static (HTML/CSS/JS/images). NO WordPress, NO database, NO server-side code. The reference is the GitHub repos:
- strulovitz.org  -> /home/nir/strulovitz-website/site/
- learnime.com    -> /home/nir/Anime/learnime-site/
- peaktogether.me -> /home/nir/peaktogether-website/
Nir's rules: NO new project folders. GitHub is the single source of truth. Only ONE local copy of each repo per operating system.

STRICT RULES: no installing/removing/upgrading packages, no editing /etc, no enabling/disabling services, no touching Windows/NTFS partitions, do not change or delete any existing cloudflared config. Do not delete anything unless this prompt says so. If sudo needs a password, give Nir the exact command and wait for the output. NEVER commit tokens, credentials, passwords or EPP codes (the repos are public).

TASK 1 - Save my prompts: in strulovitz-website, use the existing docs/notes location. If there is none, create "hosting-migration/" at the repo ROOT (NOT inside site/). Save this prompt there as a dated .md file, commit, push. If you saved an earlier prompt of mine that mentions WordPress, add a note at its top: "Superseded - the WordPress assumption was wrong; sites are 100% static."

TASK 2 - Cleanup check: if ~/websites was created today by my earlier prompt, delete it and report. Find all git repos: find /home/nir -maxdepth 6 -name .git -prune 2>/dev/null, and show each path + origin URL. Report duplicates (the same repo in 2+ places) with last commit date, git status --short and unpushed commits. Do NOT delete duplicates, only report them.

TASK 3 - Check that the repos match what is live:
- Compare https://www.strulovitz.org/index.html with site/index.html. Check that every internal link on it exists in site/ (tesseract.html, night-watch.html, v2026-09-11-c/tesseract.html, etc.).
- Do the same for https://learnime.com/ vs learnime-site/ and https://www.peaktogether.me/ vs peaktogether-website/.
- Report any file referenced by a page that is missing from the repo.

TASK 4 - Technology check of the 3 site folders:
- JS libraries used (three.js, WebXR, etc.) - loaded locally or from a CDN? Any fetch() of local JSON files? Any ES modules (.mjs / type="module")?
- Unusual file types that need correct MIME types (.wasm, .glb, .gltf, .mjs, .webm, .json ...).
- Git LFS used? (git lfs ls-files) Any placeholder pointer files instead of real content?
- Size of each site, and any files larger than 50 MB.
- Are there helper scripts (Python/shell) in the repos? Say what they do. Are they build tools, or are they needed while the site runs?

TASK 5 - Read-only system inspection:
cat /etc/os-release; hostname; whoami; df -h / /home; stat -c '%a %U' /home/nir
which git curl wget rsync cloudflared nginx caddy apache2 python3; cloudflared --version
systemctl status cloudflared --no-pager; ls -la /etc/cloudflared ~/.cloudflared 2>/dev/null
sudo ss -tlnp; systemctl is-active nginx apache2 caddy; sudo ufw status
Sleep/suspend and lid-close settings.

FINISH with "REPORT FOR CLAUDE": compact results for tasks 1-5, secrets hidden.
```
