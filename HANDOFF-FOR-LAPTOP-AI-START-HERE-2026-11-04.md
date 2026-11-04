# START HERE: HANDOFF FOR THE LAPTOP AI (4 Nov 2026). ONE FILE, EVERYTHING IN IT.
Written by Claude Sonnet 5.5 on Nir's desktop-linux. Nir is NOT your messenger and will NOT
remember anything: this file is the whole instruction, nothing else needs to be told to you.
Rules: do only what is written here; emojis on every line you say to Nir; short messages, the
important thing LAST; never `pkill -f`; never say "done/live" before checking the real URL.

## WHY (3 projects had the same disease today)
Nir serves www.strulovitz.org from two PCs (desktop, laptop), one at a time. Each serving PC
reads the websites straight from its git clones. So anything a website serves that is NOT on
GitHub is invisible on the other PC. Found today: Second Opinion data (you already fixed it,
Law 16), the Demoscene Museum landing page (not connected to the web server), and Crystal Balls
`public/` (blocked by .gitignore, never on GitHub). THE LAW: everything a website serves is
tracked by git; the forbidden list holds passwords and machine junk ONLY; after a `git pull`
on any computer the site works; a page is not done until its REAL URL is checked.

## STEP 1: PULL EVERYTHING (run exactly this)
    for r in strulovitz-website second-opinion crystal-balls Anime peaktogether-website; do
      git -C ~/$r pull --rebase --autostash || echo "PROBLEM in $r"; done
    [ -d ~/demoscene-museum ] && git -C ~/demoscene-museum pull || \
      git clone https://github.com/strulovitz/demoscene-museum.git ~/demoscene-museum
Tell Nir about any PROBLEM. Do not continue past a failed pull without telling him.

## STEP 2: CRYSTAL BALLS (public/ was never on GitHub; desktop AI fixed it, commit b037332)
Desktop AI removed `public/` from .gitignore (only config/settings.env, .venv, __pycache__, *.pyc,
tmp stay forbidden), pushed all 359 files of public/, and made scripts/publish.sh commit+push
public/ and FAIL LOUDLY if the push fails or anything in public/ is ignored/untracked.
You do:
 a. `ls ~/crystal-balls/public` must show index.html app.js style.css about.html assets data.
 b. Blank-slate proof: `git clone https://github.com/strulovitz/crystal-balls.git /tmp/cb-test`;
    serve /tmp/cb-test/public with `python3 -m http.server`; with headless Chrome over CDP
    (use 127.0.0.1) confirm the page loads, country data loads, zero console errors. Delete /tmp/cb-test.
 c. Write the Site Folder Law into the Crystal Balls BIBLE (you may edit it; the desktop AI must
    not): section in Part 8 (publishing): the law above, that publish.sh enforces it, and the
    clone test. Also add it to that repo's AGENTS.md and one dated line to BIBLE/HANDOFF-FOR-FABLE.md.
 d. Commit and push. Check `git status -sb` shows nothing ahead.

## STEP 3: DEMOSCENE MUSEUM (landing page was never served; desktop AI fixed the Caddyfile, d28ff3e)
Design is fixed, never change it: the comic landing page "The Real-Time Machine" lives in
strulovitz-website/demoscene-museum/ (index.html + images/comic/page-01..13.jpg); the museum itself
lives in its own repo strulovitz/demoscene-museum cloned at ~/demoscene-museum. hosting/Caddyfile
now serves a file from the landing folder if it exists there, else from the museum clone.
You do: confirm ~/demoscene-museum exists and is current (step 1 did it).

## STEP 4: MAKE THIS UNABLE TO HAPPEN AGAIN (general code, not one-offs)
 a. hosting/bin/sites-on: pull EVERY repo the Caddyfile serves from: strulovitz-website, Anime,
    peaktogether-website, second-opinion, demoscene-museum, crystal-balls; clone any that is
    missing; a failure prints a loud warning but the other sites still start.
 b. New hosting/bin/sites-check: read the menu links of the root index.html plus the links of each
    project landing page (Second Opinion, Demoscene Museum comic, Crystal Balls), request each
    one on 127.0.0.1:8081, print every link that is not 200. sites-on runs it at the end.
 c. A tracked-files check for every repo whose files are served (strulovitz-website,
    second-opinion, crystal-balls, demoscene-museum, Anime/learnime-site, peaktogether-website):
    list files that are ignored or untracked inside the served folder (git status --porcelain
    --ignored <folder>). Put it inside sites-check. Report to Nir anything it finds, do not
    silently ignore it.
 d. hosting/README.md: add "A page is not done until its live URL is checked": menu item, landing
    page and the project's own site each fetched over the real internet before telling Nir it works.
 e. Commit and push each step.

## STEP 5: START SERVING FROM THE LAPTOP ONLY IF NIR SAYS SO
The desktop is serving right now. NEVER run both tunnels. To switch, Nir runs `sites-off` on the
desktop first, then `sites-on` on the laptop. Ask Nir; do not decide. If he says yes, after
`sites-on` run `sites-check` and test on the PUBLIC urls: /, /2nd-opinion/ (search "hernia"),
/demoscene-museum/ (comic page 1 image, /museum/), /crystal-balls/.

## STEP 6: TELL NIR, IN THIS SHAPE (emojis on every line, important thing last)
 - Second Opinion: ok or not, with the real number of files.
 - Crystal Balls: fresh-clone test result.
 - Demoscene Museum: link check result.
 - sites-check result and anything it flagged.
 - The one thing Nir must do next, last.
