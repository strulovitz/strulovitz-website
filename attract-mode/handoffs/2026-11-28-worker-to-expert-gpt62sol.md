HAND-OFF: WORKHORSE -> EXPERT (the letter that gives you the boss's chair)
date: 2026-11-28
from: the WORKHORSE, DeepSeek V4.1 Flash 1017, on the desktop (Linux Mint 22.2)
to:   the EXPERT, GPT 6.2 Sol
repository: github.com/strulovitz/strulovitz-website, folder attract-mode/
nir's decision: D82 and config/roles -- you write the cards, I execute them.

Read in this order, and do not skip:
1. attract-mode/bible/part-00.md, in full. It rules.
2. The rest of the Bible: laws.md, then part-01.md to part-11.md. Nir asks every
   agent to read all of it. I did, and it is how I found my worst mistakes.
3. attract-mode/STATE.md -- one page, the truth of today.
4. DECISIONS.md, at least D77 to D82 (today's decisions).
5. This letter.

--------------------------------------------------------------------------------
1. WHAT NIR DECIDED TODAY, IN HIS WORDS
--------------------------------------------------------------------------------

"i think saving money on planning will ruin the project." He wants the plan
written by the stronger model and the grunt work done by the cheaper one, with
the two handing work back and forth through this repository.

So: YOU are the EXPERT chair. Cards, plans, escalations, judgement calls (is
this the same idea? does this chain work? which Boss?). I am the WORKHORSE
chair: I execute, I test, I bring back evidence, I commit and push.

Part 00, section 0.8 already defines the chairs; D82 only says who sits in
two of them. The names live in config/roles, as Part 01, section 1.7, item 6
requires. Do not write a model name anywhere else.

--------------------------------------------------------------------------------
2. WHERE THE PROJECT STANDS RIGHT NOW
--------------------------------------------------------------------------------

STAGE 0 IS CLOSED. Part 01, section 1.13 holds in full. Verified, not claimed:
- Both surveys exist: machines/desktop.md, machines/laptop.md.
- Both folder skeletons exist, and the big-files folder on each PC
  (/home/<user>/attract-mode-files/, nine folders, voice/ at 700).
- Syncthing is PAIRED on both PCs, one shared folder "attract-mode-files",
  work/ excluded by .stignore on each side, and a test file travelled BOTH
  ways. No device id is in Git.
- https://pre.strulovitz.org/ answers 200 and shows the existing site.
- "am doctor" passes on both PCs (attract-mode/line/, "uv run am doctor").
- The three websites answer 200 and are served by the desktop.
- DECISIONS.md exists; STATE.md is written; part 00 is folded and D81 records
  how the fold was checked. The tag bible-v1 sits on the pre-fold Bible
  (597a2ce).

INSTALLED ON THE DESKTOP (D78: the agent ran it, on Nir's word):
PHP 8.3.6, MariaDB 11.8.10 (127.0.0.1 only), Syncthing 2.1.7.
INSTALLED ON THE LAPTOP: PHP 8.4.28, MariaDB 11.8.9, Syncthing 2.1.7.
Moodle is NOT installed anywhere, on purpose (Stage 2 on the desktop, Stage 3
on the laptop). Caddy and the tunnel run on the desktop only, and only from
Nir's icon (AM-LAW 12).

THE WEBSITES RIGHT NOW: the desktop serves www.strulovitz.org (the old AI
Panorama site), learnime.com, peaktogether.me, and pre.strulovitz.org. The
laptop's hosting is OFF. Never both at once.

THE PINS (config/pins) are read by "am doctor" as a program, so the shape
matters: name, two or more spaces, value, two or more spaces, reason. PHP, uv
and ffmpeg are pinned PER PC ("PHP (desktop)", "uv (laptop)"); Moodle, MariaDB
and the line's Python must stay identical on both (Part 01, 1.8; D79).

--------------------------------------------------------------------------------
3. WHAT ONLY YOU CAN DECIDE (and what I need from you first)
--------------------------------------------------------------------------------

YOUR FIRST JOB: write Stage 1's cards (Part 11, 11.4, "SOMETHING TO SHOW"),
in the shape Part 11, 11.8 asks for, plus Nir's own list.

Rules for the cards, which I learned the hard way today:
- A card is ONE practical sub-task of the stage, with ONE proof. Fable's own
  example is the PC survey: "make the survey file", "done-when machines/
  desktop.md answers the eight points".
- Cards are for AGENT work only. NIR'S WORK IS NEVER A CARD. Part 11, 11.9
  says his work is one list, "am today", with lines of seven kinds: DECIDE,
  CARRY, RECORD, UPLOAD, MAKE, ANSWER, DUE. I drifted from this in Stage 0 and
  put two of his acts on cards (0-14, 0-15); do not repeat it.
- No bookkeeping cards. "Write STATE.md" is not a card; it is part of finishing
  any card (Part 01, 1.11).
- Each card names its role from config/roles, the sections to read, the proof,
  the traps, and its state.

STAGE 1 MAKES, per Part 11, 11.4: the files of the front page and the site
pages (About Nir, Privacy, Co-op); the studio list (Part 10, 10.4); the line's
own environment, ffmpeg and the EAR (Part 06: speech-to-text); then "am art
sheet", "am art in", the fit check and "am coop reply" (Part 10); and the first
Making Of, the ACE-Step song, recorded, cut, on YouTube. DONE WHEN: the Making
Of plays on YouTube and Nir has said yes to the words of the Co-op page.
NOT YET: Moodle itself.

AND NIR'S LIST FOR STAGE 1, from Part 11, 11.4 and 11.11:
- DECIDE: D64, the price of a Co-op hour (the Bible guesses 25 US dollars).
- DECIDE: the contact address for parents and customers.
- MAKE: the ACE-Step proof piece, if it is not already one (Part 10, 10.4 says
  a song exists and is proven on the laptop).
- RECORD: the Making Of of that song, from a printed sheet (Part 10, 10.5).
- UPLOAD: that film to YouTube.
- Then: the mail service and the PayPal app are opened in Stage 2, not now.

TWO THINGS TO SETTLE WHILE YOU ARE THERE:
1. Which web pages exactly make up "the front page and the site pages" in
   Stage 1 (their names and their sources), because Stage 2 puts them into
   Moodle and the names must not be invented later.
2. The auditor chairs (config/roles: AUDITOR-TEXT, AUDITOR-EYES) are OPEN. The
   Bible requires them to pass the trap test before any audit (Part 07, 7.5).
   You do not need them until there is science or code to audit (D81), but
   choose them before Stage 4.

--------------------------------------------------------------------------------
4. HOW WE HAND WORK BACK AND FORTH (the protocol)
--------------------------------------------------------------------------------

YOU -> ME: a file attract-mode/handoffs/<date>-expert-to-worker.md, containing
   - the cards themselves, one file each in attract-mode/tasks/ (so "am task
     next ROLE" can find them later), named by stage and number, e.g. 1-01.md;
   - one short paragraph per card saying what you intend, so I do not guess;
   - anything ambiguous flagged, not silently decided.
   Then push, and tell Nir one sentence: "the cards are ready".

ME -> YOU: a file attract-mode/handoffs/<date>-worker-to-expert.md, containing
   - for every card: done or failed, and the EVIDENCE (the command, its output,
     the file path, the "am doctor" line);
   - anything I had to decide along the way, marked as mine and easy to reverse;
   - a list of what I could not do without a card.

RULES OF THE ROAD: pull before writing; one agent writes at a time (Part 01,
1.11, item 2); push after every finished card; never force-push; on a conflict
stop and tell Nir in plain words. Do not touch the top-level bible/ folder or
the top-level DECISIONS.md: those belong to AI Panorama. Ours is attract-mode/.

--------------------------------------------------------------------------------
5. MISTAKES THAT COST US TODAY. PLEASE DO NOT MAKE ME REPEAT THEM.
--------------------------------------------------------------------------------

1. I wrote the Caddy block before reading all of Part 01, and gave port 8084
   to "pre". Part 01, 1.4 owns the ports: 8084 is Attract Mode's (Moodle);
   8081 is the old site and pre. Lesson: the section a card names is not always
   the section that owns the fact.
2. MariaDB's own repository script does not recognise "Linux Mint" and refused
   to run. The script now tells it the base system (ubuntu + codename). On
   Debian the same trick uses debian + trixie.
3. MariaDB stopped at an interactive question with nobody at the keyboard and
   the run hung for fifteen minutes. Every apt call is now noninteractive.
4. sudo on the desktop REFUSES "DEBIAN_FRONTEND=..." on the command line. The
   working form is to set it inside the shell sudo runs: sudo sh -c '...'.
5. My PHP pin reader read the second word of the line and broke when the pins
   became two lines. It now splits on two or more spaces and asks for this
   PC's line.
6. My "am doctor" treated an empty but successful "git status" as a failure
   and said "no git repository found" on a clean repo. None now means "could
   not run", and "" means "ran and said nothing". Twelve self-checks exist:
   "uv run python tests/selftest.py".
7. I described the Cloudflare screen as "Public Hostname" when it now says
   "Routes", "Add route", "Published application", "Service URL". Nir had to
   find it himself. Always read his screen before instructing him.

--------------------------------------------------------------------------------
6. THE BOUNDARIES I LIVE INSIDE, AND YOU WILL TOO
--------------------------------------------------------------------------------

- Nir's messages must be SHORT. He cannot scroll in OpenCode on Linux, and he
  is a beginner. One screen, plain words, the important thing last.
- He decides everything about his money, his machines and his words. Give him
  A / B / C with a recommendation, never a quiz.
- Never write a password, a token, a device id or an IP address into any file
  in this repository (AM-LAW 13). The full install logs and the raw research
  live in /home/<user>/attract-mode-files/, never in Git.
- Never change a Part of the Bible without his plain-language yes and a dated
  DECISIONS.md entry (AM-LAW 19). D78, D80, D81 and D82 are today's examples.
- Never weaken a check to make something pass (AM-LAW 9). Two failures, then
  an escalation note (Part 07, 7.4) -- which, from now on, comes to you.
- Do not start Caddy or the tunnel. AM-LAW 12: they start only from Nir's icon.
- Do not touch Apache on the laptop; it is the stock Debian page and not ours
  (D80), but it is not ours to stop either.
- Before every push, list the files. The secret scanner runs by itself; if it
  complains, stop and read why.

--------------------------------------------------------------------------------
7. WHAT I WILL DO THE MOMENT YOUR CARDS ARRIVE
--------------------------------------------------------------------------------

I will pull, read your hand-off first, then the cards in order. I will execute
one card at a time, and after each: run its proof, rewrite STATE.md, add one
line to WORKFLOW-2026-11-28.md (or a new dated file), commit only attract-mode
files by name, push, and write the evidence into the next worker-to-expert
hand-off. If a card is impossible as written, I will say so with the reason
instead of improvising.

Welcome to the chair. The project is in better shape than this letter sounds:
Stage 0 is closed, both PCs are installed and paired, and the websites are up.

-- the WORKHORSE, DeepSeek V4.1 Flash 1017, on the desktop
