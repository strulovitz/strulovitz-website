HAND-OFF: DESKTOP -> LAPTOP
date: 2026-11-28
from: the agent on the DESKTOP (Linux Mint 22.2, Linux, OpenCode)
to:   the agent on the LAPTOP (Debian 13, Linux, OpenCode)
repository: github.com/strulovitz/strulovitz-website, folder attract-mode/
the repository was at commit 54f408d when this letter was written

Nir's message to you, in his own words: "please read the WHOLE BIBLE and
please read the hand-off that Desktop-PC wrote to you, and do what the
hand-off tells you".

Read this in this order, and do not skip:
1. Part 00 in full (attract-mode/bible/part-00.md). It rules.
2. The whole Bible: laws.md, then part-01.md to part-11.md. Nir asked for
   this on purpose. I read all 7,189 lines today and it is how I found my
   own worst mistake (see section 3, item 1). It takes a while; do it.
3. attract-mode/STATE.md -- one page, the truth of today.
4. This letter.

--------------------------------------------------------------------------------
1. WHO WE ARE
--------------------------------------------------------------------------------

We are the same model, the same weights: DeepSeek V4.1 Flash 1017. You are not
a servant and I am not your boss. We are the two halves of one worker on two
machines, and Nir is the owner between us. The Bible is our continuity; we are
interchangeable and we will be replaced by other models. So write for the next
reader, not for yourself.

How we talk: through files in this repository. Each reply is a small hand-off
in attract-mode/handoffs/ with the date in the name. One big letter like this
one is allowed when there is a lot to say. We push, the other pulls. Never
force-push. If a pull gives a conflict, STOP and tell Nir in plain words
(Part 01, section 1.11).

Nir does not carry commands between us. He carries only one thing: the words
"read the hand-off and do what it says". So everything we need from each other
must be written here, in plain text, with no special signs (AM-LAW 17).

--------------------------------------------------------------------------------
2. WHAT THE DESKTOP HAS DONE TODAY
--------------------------------------------------------------------------------

Stage 0 of Part 11 is well under way on the desktop. These exist and are
pushed:

- The whole folder skeleton of Place 1 (it comes to you by git pull, so you
  will have it without making anything).
- config/pins -- every version, both PCs, never "latest". PHP is TWO lines:
  "PHP (desktop) 8.3" and "PHP (laptop) 8.4", because the two systems ship
  different PHP and Part 01, section 1.8 allows exactly that. On your PC the
  script will ask for the laptop line.
- lib of the line: attract-mode/line/ -- "uv run am doctor" works and is the
  check we must both pass. No outside library; the Python is 3.13.14, named
  in line/.python-version.
- hosting/install/owner-setup.sh -- the one setup script (Part 01, 1.9). It
  installs PHP, MariaDB and Syncthing from the pins, installs NO Moodle, and
  touches no live site.
- hosting/attract-mode.caddy plus ONE import line in hosting/Caddyfile. The
  ports are the Bible's: 8084 is Attract Mode's (Moodle, from Switch Day),
  8081 is the old site AND "pre". "pre" needs no door of its own.
- tasks/ -- the golden card and the Stage 0 cards, with their true states.
  Your work is cards 0-03 (survey), 0-05 (folders) and 0-15 (owner-setup).
- DECISIONS.md -- read D78 before anything else about owner-setup.

ON THE DESKTOP, ALREADY INSTALLED (by me, with Nir's word, D78):
PHP 8.3.6, MariaDB 11.8.10 (listening on 127.0.0.1 only), Syncthing 2.1.7.
"am doctor" on the desktop says: no failures.

--------------------------------------------------------------------------------
3. THE FOUR MISTAKES THAT COST THE DESKTOP TODAY. DO NOT REPEAT THEM.
--------------------------------------------------------------------------------

1. I wrote our Caddy block before reading all of Part 01, and gave port 8084
   to "pre". Part 01, section 1.4 owns the ports: 8084 belongs to Moodle.
   Lesson: the section a task card names is not always the section that owns
   the fact. Read the Part.

2. MariaDB's own repository script does not recognise "Linux Mint" and
   refused to run. On Mint the script now tells it the base system (ubuntu
   noble, from UBUNTU_CODENAME). On Debian 13 this should not happen; if it
   does, the same trick applies with --os-type=debian and the codename
   trixie. Do not "fix" it by hand: fix it in the script.

3. MariaDB stopped at an interactive question (its anonymous feedback plugin)
   with nobody at the keyboard, and the run hung for fifteen minutes. Every
   apt call in the script is now noninteractive. If you meet another question,
   the answer is not to press Enter: it is to make the script noninteractive.

4. sudo on the desktop REFUSES "DEBIAN_FRONTEND=..." on the command line:
   "sorry, you are not allowed to set the following environment variables".
   The working form, already in the script, is to set it inside the shell
   that sudo runs:
       sudo sh -c 'DEBIAN_FRONTEND=noninteractive apt-get install -y "$@"' sh "$@"

And one smaller one: my PHP pin reader read the second word of the pins line
and broke when PHP became two lines. The reader now splits on two or more
spaces and asks for THIS PC's line. If you change the pins file, keep that
shape: name, two or more spaces, value, two or more spaces, reason.

--------------------------------------------------------------------------------
4. YOUR TASKS, IN THIS ORDER. ONE AT A TIME. REPORT AFTER EACH.
--------------------------------------------------------------------------------

TASK 1 -- PULL, THEN THE SURVEY (card 0-03, Part 01, section 1.5)
Do it first; it is read-only and it tells us what your PC is.
    cd ~/strulovitz-website && git pull
then either run our own survey script (read-only, no sudo, prints no address,
no token, no password):
    bash attract-mode/machines/laptop-survey.sh
or gather the same facts yourself. Either way, WRITE attract-mode/machines/
laptop.md from the result, answering the eight points of section 1.5:
  1. Linux name and version, the user name, free space on / and on home.
  2. Installed or not, and the version: git, caddy, cloudflared, php,
     mariadb, syncthing, uv, python3, ffmpeg, latex, obsidian.
  3. Which local ports listen, and whether 8084 is free.
  4. Whether a database or PHP is already running, and what uses it.
  5. How the tunnel learns its addresses (a local file or the Cloudflare
     dashboard), and whether both PCs run the SAME tunnel.
  6. What "Websites ON" does, step by step, from reading hosting/bin/.
  7. Whether a change under attract-mode/ would trigger a rebuild of the
     AI Panorama export.
  8. Which voice models and art studios exist under Linux (names only).
NO password, no token, no IP address goes into that file. It is public.
If less than 60 GB is free on /, STOP and tell Nir (section 1.5).

TASK 2 -- THE FOLDERS THAT ARE NOT IN GIT (card 0-05)
Place 1 arrives by git pull. Place 3 does not; make it on your PC:
    mkdir -p ~/attract-mode-files/{books,footage,masters,sessions,handover,raw,packages,voice,work}
    chmod 700 ~/attract-mode-files/voice
It is the folder Syncthing will share. work/ is never copied (Part 09, 9.9).
Note the exact home path in machines/laptop.md, because Syncthing needs it.

TASK 3 -- OWNER-SETUP, ON NIR'S WORD (card 0-15, D78, Part 01, 1.9)
Read D78 in DECISIONS.md first: Nir decided the AGENT runs it, once, on his
explicit word. So ask him for that one word, in plain language, and then:
    cd ~/strulovitz-website/attract-mode
    printf 'yes
' | ./hosting/install/owner-setup.sh 2>&1 | tee ~/attract-mode-files/work/logs/owner-setup-$(date +%F).log
It is safe to run twice. It prints its plan first.
WHAT TO EXPECT ON DEBIAN 13: PHP 8.4 (your line in the pins), MariaDB from
Debian's own 11.8 series (no MariaDB repository needed), Syncthing 2.1.7 from
Syncthing's own repository (the script adds it and checks the version).
IF sudo ASKS FOR A PASSWORD on your PC, do not ask Nir to paste it anywhere.
Stop and say: "Type your laptop password in the terminal now, then tell me
when it is done." His password never enters a file or a chat (AM-LAW 13).
When it finishes, run the check and make sure it says no failures:
    cd ~/strulovitz-website/attract-mode/line && uv run am doctor

TASK 4 -- SYNCTHING'S TWO-WAY TEST (card 0-10, Part 09, 9.9)
Syncthing is installed by TASK 3. Start it once, as the normal user, so that
its settings file exists:
    syncthing serve --no-browser &
(Or open its window from the menu, whichever is easier for Nir.)
Then Nir does the two clicks that only a person can do: on each PC, in
Syncthing's window, accept the OTHER PC when it appears (Part 09, 9.9, item 6).
Do not put a device ID or an address in any file in Git.
Share ONE folder only: attract-mode-files. The folder work/ is excluded.
Then THE TEST: a small file put in attract-mode-files/handover/ on the laptop
must appear on the desktop, and one put on the desktop must appear on the
laptop. Both directions, or the test has not passed (Part 01, 1.13, item 4).
Afterwards "am doctor" on both PCs should show the other PC connected.

TASK 5 -- RECORD IT, THEN WRITE BACK TO ME
1. Append one entry to attract-mode/WORKFLOW-2026-11-28.md (or a new dated
   file if the day has changed), headed "STAGE 0, LAPTOP" -- what you did,
   what failed, and what you fixed. Honest, one line per fact.
2. Rewrite attract-mode/STATE.md, one page: what exists, what works, what
   comes next, what waits for Nir. Rewritten, never appended (Part 01, 1.11).
3. Write attract-mode/handoffs/2026-11-28-laptop-to-desktop.md, short:
   the survey's three most important facts, what is installed, whether
   Syncthing's two-way test passed, and the ONE thing the desktop should do
   next. I will read that first.
4. Commit and push only attract-mode/ files, by name. Never git add .
   The full survey output and the install log stay OUT of Git: Place 3.
5. Then tell Nir, in plain words, one line: what you finished and what you
   need from him next.

--------------------------------------------------------------------------------
5. WHAT NOT TO DO
--------------------------------------------------------------------------------

- Do not start, stop or restart Caddy or the tunnel unless Nir says so. The
  live site is not answering right now (Cloudflare 1033) and Nir said not to
  worry about it for a few hours. AM-LAW 12: the tunnel never starts by itself.
- Do not touch Apache. On the laptop it belongs to something else (Part 01,
  1.8). If your survey finds it running, say so and leave it alone.
- Do not install Moodle. Not yet. It is Stage 2 on the desktop (Part 11, 11.4).
- Do not write any password, token, device ID or IP address into any file in
  this repository (AM-LAW 13). Before every push, list the files and check.
- Do not change a pin without writing the reason beside it (Part 01, 1.8).
- Do not change any Part of the Bible without Nir's plain-language approval and
  a dated entry in DECISIONS.md (AM-LAW 19).
- Do not weaken a check to make something pass (AM-LAW 9).
- Do not do more than Nir asked. He is paying for every call (it was free
  once, it is not free any more). Keep your messages short.

--------------------------------------------------------------------------------
6. WHAT I WILL DO WHEN YOUR LETTER ARRIVES
--------------------------------------------------------------------------------

I will pull, read your hand-off first, then machines/laptop.md, then your
workflow entry. Then I will finish the desktop's side: O2 ("pre" at Cloudflare,
which is Nir's click) and the Syncthing confirmation, and we will then be at
Part 01, section 1.13 -- Stage 0 done -- except the fold check of Part 00 by a
different model, which is still open (card 0-13).

Welcome. Write to me as one worker to another, and be honest about what failed.

-- the agent on the desktop, 54f408d
