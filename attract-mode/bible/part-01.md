NOTICE, 11 November 2026: section 1.7 is changed in one
place. The change is written in Part 03, section 3.1. Also changed by
Part 04, section 4.2.
TeX Live is not installed. Written in Part 06, section 6.2.
================================================================================
ATTRACT MODE -- THE BIBLE -- PART 01 OF 11
ARCHITECTURE AND MACHINES
Version 1.1 -- 11 November 2026
Status: FOUNDATIONAL. Obeys Part 00 as changed in section 1.2.
================================================================================

HOW TO READ THIS PART

Part 01 says WHERE everything lives: which address, which computer,
which operating system, which folder. It names the software and the
rules of installation. It builds on the hosting that already works in
this repository (the folder hosting/) and changes as little of it as
possible.

Installation COMMANDS are not written here, because commands go stale.
The EXPERT writes them as scripts on the day they are needed, from the
makers' own pages, obeying the rules in 1.9.

This file is saved VERBATIM at: attract-mode/bible/part-01.md

--------------------------------------------------------------------------------
1.1 NIR'S DECISIONS OF 11 NOVEMBER 2026
--------------------------------------------------------------------------------

D1.  Nir's existing projects move to https://pre.strulovitz.org/ .
     "pre" is the gamer's word for what came before. Kitchen name:
     THE PREQUELS.
D2.  Attract Mode stays in the folder attract-mode/ of this repository.
D3.  Walkthrough videos are narrated in Nir's own voice, cloned once by
     his local voice model. Attract clips are Nir speaking live.
D4.  No connection to Learnime or Peak Together. They stay separate.
D5.  Code: MIT. Text: CC BY-SA 4.0.
D6.  MOODLE IS THE WHOLE WEBSITE. A visitor who opens
     https://www.strulovitz.org/ is at once on Moodle's front page. No
     page before it, no forwarding, no "click here to enter". Free
     things are Moodle courses open to guests. Paid things are Moodle
     courses that need an account and a PayPal payment.
D7.  Moodle's address is https://www.strulovitz.org/ . The site's name
     in Moodle is "Attract Mode". There is no separate name for the
     paid area.
D8.  Nir does the few acts that only the owner can do (1.12), and he
     uploads finished videos to YouTube and pastes their addresses
     back.
D9.  Moodle is installed in the normal, standard way. No special
     folders, no disk lock. On each PC, Linux lives on an external USB
     drive that stays attached to that PC and does not travel alone.
D10. There is no waiting period. The old site moves to pre on the day
     Moodle is installed.

THE DECISION RECORD. It is the file attract-mode/DECISIONS.md . (The
file DECISIONS.md at the top of the repository belongs to AI Panorama.
Never write there.) One entry per decision, newest at the bottom: the
date, a short name, what was decided, who decided. The first agent to
read this Part creates it with D1 to D10 in the words above. Nothing
is ever deleted from it; a reversed decision gets a new entry.

--------------------------------------------------------------------------------
1.2 CHANGES TO PART 00
--------------------------------------------------------------------------------

Nir's decisions change Part 00 in seven places. Where Part 00 and this
section disagree, this section wins. Everything else in Part 00 stands,
in particular AM-LAW 13, AM-LAW 14 and AM-LAW 16.

1. MOODLE IS THE WEBSITE (0.7, 0.11 item 7, AM-LAW 11). Read the end
   of AM-LAW 11 as: "Moodle is the WEBSITE: what every visitor sees,
   free and paid. It is never the source. Every Moodle course must be
   rebuildable from the files by one command."
2. FREE (0.7 item 1). Free things are Moodle courses open to guests:
   no account and no login click. In 0.7 item 2, the sentence about
   the site working with the paid part switched off is replaced by:
   "A free Level never depends on a login or on PayPal."
3. THE WORD "CASHIER" IS RETIRED. Say "Moodle". In AM-LAW 12, "the
   cashier's data" means "Moodle's data".
4. "THE LAB" is now THE PREQUELS (glossary item 17).
5. SWITCH DAY (warning 2, glossary item 18) is simply the day Moodle
   is installed at www. Nothing waits for it.
6. AM-LAW 8. Nir's jobs also include OWNER ACTS (1.12), and job 2
   includes uploading finished videos to YouTube.
7. THE MAP (0.13). Part 08 is named "Moodle".

THE NOTICE. The first agent to read this Part adds the following three
lines at the very top of attract-mode/bible/part-00.md , above
everything else, and changes nothing else in that file:

    NOTICE, 11 November 2026: by Nir's decisions, this Part is changed
    in seven places. The changes are written in Part 01, section 1.2,
    and they win over the text below.

--------------------------------------------------------------------------------
1.3 THE PICTURE
--------------------------------------------------------------------------------

A visitor's browser asks Cloudflare. Cloudflare passes the request
through the tunnel to whichever of Nir's two PCs is serving. On that
PC the web server (Caddy) answers on a local port and hands the
request to PHP, which runs Moodle, which reads the database. A few
plain files of ours (the toys and their libraries) are handed back by
Caddy directly and are shown inside Moodle's pages. Nothing of ours
listens on the public network; the tunnel is the only door. This is
the existing design, and it is kept.

--------------------------------------------------------------------------------
1.4 ADDRESSES
--------------------------------------------------------------------------------

LOCAL PORTS. The first three were observed in hosting/Caddyfile and
are NOT to be changed:
1. Port 8081 -- everything www.strulovitz.org serves today: AI Panorama
   at the root, plus /hive, /ghost, /2nd-opinion, /crystal-balls,
   /demoscene-museum and the rest.
2. Port 8082 -- learnime.com.
3. Port 8083 -- peaktogether.me.
4. Port 8084 -- NEW: Attract Mode (Moodle, plus our plain files).
If the survey (1.5) finds 8084 taken, the EXPERT picks the next free
port and records it.

PUBLIC ADDRESSES.
1. https://www.strulovitz.org/ -- port 8081 today; port 8084 from
   Switch Day.
2. https://pre.strulovitz.org/ -- port 8081. It may be added at once:
   it only gives the existing site a second name.
3. learnime.com and peaktogether.me -- untouched, and outside this
   Bible forever.

SWITCH DAY. The steps, in order. Part 08 owns the Moodle details.
1. pre.strulovitz.org is added and checked. (Owner act.)
2. Moodle is installed with the address https://www.strulovitz.org
   written into it from the first minute. Moodle's address is painful
   to change later, so it is never installed under a temporary one.
3. www is pointed at port 8084. (Owner act.)
4. Every old path on www is redirected to the same path on pre. A
   SCRIPT makes the list from what port 8081 serves, so every old link
   printed anywhere still arrives. If an old path has the same first
   word as a Moodle path, Moodle wins and the EXPERT notes it.
5. PROJECTS-AND-MENU.md is rewritten: AI Panorama is the root of pre.
6. The real addresses of all four websites are fetched and checked.
No file of the existing projects has to move on disk. Their menu links
begin with "/", so they work unchanged under pre. A SCRIPT lists every
link in them that spells out www.strulovitz.org in full; the EXPERT
changes those to pre. While Moodle is being set up, www may look
unfinished for some hours. Nir has accepted that. Undoing Switch Day
is pointing www back at port 8081.

THE OLD SITE INSIDE MOODLE. Nothing of the old site is rebuilt inside
Moodle. Moodle gets an "About Nir" page and plain links to the
Prequels. The 3D projects keep running exactly as they are, at pre.
The public label of the link is one line of configuration and is
Nir's to change.

OUR PLAIN FILES. Moodle owns the root of the address. Everything of
ours that is not Moodle lives under ONE path word, /am/ , which Caddy
answers before Moodle sees it:
1. /am/toy/NAME/    one toy, shown inside a Moodle page in a frame
2. /am/assets/      our own pictures, styles and scripts
3. /am/vendor/      pinned copies of other people's libraries
4. /am/go/NAME      a short link that forwards to a Level in Moodle
5. /am/beacon/      measurement (see below)
Also /hosted-by , the existing convention that says which PC is
serving.
NAME is lowercase English letters, digits and hyphens.
Checked on 11 November 2026: Moodle 5.3 has no folder named "am". A
SCRIPT checks this again at every Moodle update.
Toy pages may be framed only by our own address.

SHORT LINKS. Moodle's own course addresses contain a number, and that
number can change when a course is rebuilt from the files. Therefore
the link we give to people is always /am/go/NAME . A SCRIPT keeps the
list of where each one points. A short link, once given out, works
forever.

MEASUREMENT. No outside analytics. A toy or a video page may request
a tiny file under /am/beacon/ whose name says which Level and which
checkpoint. Caddy writes the path and the time, and nothing else, to
a local log. A SCRIPT counts. Part 07 owns the use of these counts.

--------------------------------------------------------------------------------
1.5 THE TWO MACHINES
--------------------------------------------------------------------------------

Both PCs are equal. Neither is "the server". (AM-LAW 12.)

KNOWN FACTS, to be confirmed by the survey:
1. LAPTOP. Lenovo Legion, RTX 5090 with 24 GB, 64 GB of memory.
   Windows 11 on the internal disk. Debian 13 on its own external USB
   drive. Closing the lid suspends it unless the keep-awake service
   is on. Apache is installed there and is NOT ours: never touch it.
2. DESKTOP. Lenovo Legion, RTX 4070 Ti with 12 GB, 64 GB of memory.
   Windows 11 on the internal disk. Linux Mint 22 on its own external
   USB drive.
3. Each external drive stays attached to its own PC (D9).

FIRST TASK: THE SURVEY. Role: WORKHORSE. Read-only, on each PC, in
Linux. Read-only means: no installing, no service changes, no
administrator rights, no Windows partitions. It writes
attract-mode/machines/laptop.md and attract-mode/machines/desktop.md .
These files are public: no passwords, no tokens, no IP addresses.
Each file reports:
1. Linux name and version; the user name; free space.
2. Installed or not, and which version: git, caddy, cloudflared, php,
   mariadb, syncthing, uv, python3, ffmpeg, latex, obsidian.
3. Which local ports are listening, and whether 8084 is free.
4. Whether a database or PHP is already running, and what uses it.
5. How the tunnel learns its addresses (in the Cloudflare dashboard
   or in a local file), and whether both PCs run the SAME tunnel.
6. What "Websites ON" does, step by step, from reading hosting/bin/ .
7. Whether a change under attract-mode/ would trigger a rebuild of
   the AI Panorama export.
8. Which voice models and art studios exist under Linux (names only).
If less than 60 GB is free on either PC, stop and tell Nir.

--------------------------------------------------------------------------------
1.6 WHAT RUNS WHERE
--------------------------------------------------------------------------------

WINDOWS 11 (both PCs).
1. The games, and the recording of game footage.
2. Those of Nir's art studios that live in Windows (Part 10).
3. No Attract Mode code. Nothing is installed on Windows for this
   project beyond what Nir already uses to record.
4. Agents working in Linux never touch a Windows partition. Footage
   crosses from Windows to Linux in two ways only: Nir uploads the
   clip to YouTube and pastes its address, or Nir copies it on a
   removable drive. Part 06 owns the procedure.

LINUX (both PCs, set up identically).
1. ALWAYS RUNNING, from the moment Linux starts, as on any normal
   Moodle machine: the database and PHP. They can be reached only
   from the PC itself.
2. SERVING, only on the PC whose "Websites ON" icon was clicked:
   Caddy, the tunnel and keep-awake (all existing), and, new, Moodle's
   clock and a timer that fetches new work from GitHub. Nothing
   becomes PUBLIC by itself: the tunnel starts only from the icon.
3. PRODUCING, on either PC, serving or not: the line (Python), Manim,
   the browser tests, the voice, the coding agent, Obsidian.
4. Syncthing, which talks only to the other PC.

A PC that is in Windows serves nothing. Therefore, before recording:
"Websites OFF" on this PC, "Websites ON" on the other. There are no
new icons: Attract Mode extends the two existing ones. OFF hands
Moodle's data over; ON takes the newest data in. Part 09 owns exactly
how.

MOODLE IS FILLED ONLY ON THE SERVING PC. Lessons are written as files
on either PC and travel by Git. The serving PC turns the files into
Moodle courses (Part 08). Moodle's data then travels to the other PC
at the next switch.

THE ART STUDIOS ARE NOT OURS. Attract Mode never installs into,
upgrades, or borrows a Python environment from any art studio or
voice studio. Our line has its own environment (1.8) and calls a
studio only from outside, the way a person would.

--------------------------------------------------------------------------------
1.7 WHERE THINGS LIVE
--------------------------------------------------------------------------------

There are three places, and each is an ordinary one.

PLACE 1 -- THE GITHUB FOLDER. attract-mode/ inside the repository
strulovitz-website. Public: the whole world can read it.
1. bible/        Parts 00 to 11, verbatim.
2. DECISIONS.md  the decision record (1.1).
3. STATE.md      one page: where the project stands today (1.11).
4. handoffs/     dated notes between agents.
5. machines/     the two survey reports (1.5).
6. config/       project settings, role-to-model names, version pins.
7. vault/        the knowledge base (Part 02).
8. research/     questions for Nir and what he pasted back (Part 03).
9. levels/       one folder per Level: plan, narration, toy, scenes,
                 quiz questions (Part 04).
10. kits/        the toy kit and the video kit (Parts 05 and 06).
11. line/        the production line: one Python project with its
                 lock file.
12. hosting/     our Caddy block, our additions to the two icons, the
                 owner-setup script.
13. public/      the plain files served under /am/ , exactly as
                 served. Written only by "am publish" (1.10). Never
                 edited by hand.

PLACE 2 -- MOODLE, INSTALLED THE NORMAL WAY (D9).
1. Moodle's program, in the usual place for websites on Linux.
2. Moodle's data folder, next to it. Moodle itself requires this
   folder to be outside the part the web can reach.
3. Moodle's database, in the system's ordinary database.
The exact folder names are those of Moodle's own installation guide,
and they are written into the two machine files. Both PCs use the
same names.

PLACE 3 -- THE BIG FILES. One ordinary folder in the home folder,
named attract-mode-files/ . It exists because GitHub refuses large
files and because the GitHub folder is public. The two PCs copy it to
each other directly, with Syncthing.
1. books/      problem books and other people's texts.
2. footage/    raw game recordings.
3. masters/    finished videos and audio.
4. sessions/   recordings of art sessions (Part 10).
5. handover/   Moodle's data on its way to the other PC (Part 09).
6. work/       scratch space. Not copied. May be deleted any time.

WHICH PLACE? For any new file, ask in this order:
1. Is it a password or a key? See PASSWORDS below. Never GitHub.
2. Is it about a person (a name, an email, a recording, a payment)?
   Then Moodle or the big-files folder. Never GitHub.
3. Is it somebody else's work that we may not republish (a book, raw
   game footage)? Then the big-files folder.
4. Is it video or audio, or larger than 10 MB? The big-files folder.
5. Everything else goes to GitHub: every page, toy, script, prompt
   and vault file (AM-LAW 18).

PASSWORDS. The GitHub folder is public. A password written there, or
in a hand-off note, can be read and used by anyone in the world.
Therefore:
1. Nir types each password himself, in the place that needs it: his
   Linux password in the terminal when it asks, the PayPal keys in
   Moodle's own settings page, Cloudflare in Cloudflare.
2. Moodle keeps its database password in its own settings file, in
   Place 2. That is the normal arrangement.
3. An agent never writes a password into any file under the GitHub
   folder, and never repeats one in a report.
4. Before every push, the agent lists the files it will send and
   confirms that none comes from Place 2 or Place 3.

--------------------------------------------------------------------------------
1.8 SOFTWARE
--------------------------------------------------------------------------------

PINS. Every version number lives in attract-mode/config/ in one pins
file. Never "latest". Both PCs use the same pins. Only the EXPERT
changes a pin, and writes the reason.

FACTS CHECKED ON 11 NOVEMBER 2026, from the makers' own pages:
1. Moodle 5.3, the long-term-support release of 5 October 2026, needs
   PHP 8.3 or 8.4 and MariaDB 11.4 or newer. PHP 8.5 is not supported.
2. Debian 13 ships PHP 8.4 and MariaDB 11.8. That is enough.
3. Linux Mint 22 is built on Ubuntu 24.04, which ships MariaDB 10.11.
   That is too old. On the desktop, MariaDB comes from MariaDB's own
   package repository, in the same series as the laptop's. Its PHP is
   expected to be 8.3; the survey confirms.
4. From Moodle 5.1 onward the web server must be pointed at Moodle's
   "public" folder, and requests that match no file go to Moodle's
   router (the file r.php in that folder).
5. Moodle 5.3's "public" folder has no entry named "am".
6. Manim Community 0.22.1 needs Python 3.11 or newer. Its own
   documentation recommends the tool "uv". On Debian-family systems
   it also needs build-essential, python3-dev, libcairo2-dev and
   libpango1.0-dev, and LaTeX (TeX Live) for formulas. Its health
   check is: uv run manim checkhealth

FROM MEMORY, TO BE CONFIRMED IN PART 08:
1. Moodle can let visitors into guest courses with no login click
   (the setting "auto-login guests").
2. Guests can read a course but cannot take its quizzes.

VERSIONS BETWEEN THE TWO PCS.
1. Moodle itself: exactly the same version on both, always. Both are
   updated on the same day.
2. The database: the same series on both. An export from one PC must
   load on the other.
3. PHP may be 8.3 on one PC and 8.4 on the other, as long as Moodle's
   own environment check passes on both.
4. The line's Python environment is identical on both, because both
   build it from the same lock file in Git.

ALREADY THERE. Do not reinstall and do not upgrade for this project:
git, Caddy, cloudflared, the hosting scripts and icons, the coding
agent, the art studios and the voice models.

TO ADD, ON BOTH PCS.
1. For the website: PHP with the extensions Moodle asks for; MariaDB;
   Moodle; Syncthing.
2. For producing: uv; a Python that uv keeps inside the project;
   Manim Community; TeX Live; ffmpeg; Playwright with its own
   Chromium, for testing every toy at phone size and desktop size.
3. For looking: Obsidian. A viewer only. If it vanished tomorrow,
   nothing would break.

NOT USED, so that no agent adds them "to help":
1. Docker. (Nir's decision.)
2. Conda, for our line. The art studios keep whatever they use.
3. Node.js, npm and bundlers. Toys are plain files.
4. Neo4j or any second database. (AM-LAW 11.)
5. SCORM. Mathematica.
6. Any outside file server, font service or analytics service.
7. Apache. It belongs to something else on the laptop.
8. Extra Moodle plugins, unless Part 08 names them.

--------------------------------------------------------------------------------
1.9 INSTALLATION RULES
--------------------------------------------------------------------------------

1. ONE SETUP SCRIPT. Everything that needs administrator rights is
   collected in ONE script, attract-mode/hosting/install/owner-setup.sh
   . It prints what it is about to do and is safe to run twice. Nir
   starts it himself, once on each PC, and types his Linux password
   when the terminal asks. An agent never asks Nir to tell it a
   password.
2. AFTER THE SETUP SCRIPT, NO PASSWORD IS NEEDED. An agent must be
   able to run Moodle's command-line tools, and to export and import
   Moodle's database, without administrator rights. The EXPERT
   arranges this in the usual way: Moodle's PHP runs as Nir's own
   Linux user, and Moodle has its own database user. This also lets
   Caddy, which runs as Nir, talk to PHP.
3. SAME ON BOTH. The same script and the same pins on both PCs.
   Afterwards "am doctor" (1.10) must print matching versions.
4. ORDER. The survey. Then owner-setup on both PCs. Then Moodle and
   Switch Day on the serving PC. Then Moodle on the other PC, and one
   test switch in each direction. Then the production tools.
   Moodle is NOT installed before Part 08 and Part 09 are saved.
5. A CHECK FOR EVERYTHING. Every installed piece gets one check
   inside "am doctor". A piece is not installed until its check
   passes on BOTH PCs.
6. THE SHARED HOSTING FOLDER. hosting/ serves three live websites.
   Changes there are for the EXPERT only: one line in
   hosting/Caddyfile that imports
   attract-mode/hosting/attract-mode.caddy . Validate before
   reloading. Reload, never restart. Then run sites-check. Then fetch
   the real addresses of all the live websites.
7. THE EXISTING RULES STAY. AGENTS.md: upload only what changed.
   hosting/README.md: a page is not done until its live address is
   checked.

--------------------------------------------------------------------------------
1.10 THE COMMAND "am"
--------------------------------------------------------------------------------

The line has ONE entry point, so that a cheap model never has to
guess which script to run. From the folder attract-mode/line/ :
    uv run am WORD
This Part defines three words. Other Parts add theirs.

1. am doctor -- checks this PC and prints a plain-language report:
   the versions against the pins; the ports; whether Moodle answers;
   whether Git is clean and up to date; whether Syncthing sees the
   other PC; how old the newest hand-over of Moodle's data is. Any
   failure is said in one plain sentence, with what to do about it.
2. am build -- builds everything from the files into the scratch
   folder work/ : the plain files for /am/ and the course files that
   Moodle will take in. The same files in always give the same bytes
   out.
3. am publish -- builds; runs every test on the scratch copy; then,
   and only then, copies the plain files into attract-mode/public/ ;
   commits; pushes. The serving PC then takes the new work into
   Moodle (Part 08), and the real address is fetched to confirm.

--------------------------------------------------------------------------------
1.11 GIT ON TWO PCS
--------------------------------------------------------------------------------

1. Before any work: pull. After every finished task: a small commit,
   and push. Never force-push. On a conflict: stop, and tell Nir in
   plain words.
2. One agent session at a time works in attract-mode/ .
3. While serving, a PC fetches from GitHub on a timer (Part 09), so
   that work pushed from the other PC appears by itself.
4. Nothing larger than 10 MB enters Git. Video and audio never do.
5. Notes between agents go into attract-mode/handoffs/ , with the
   date in the file name. Never at the top of the repository.
6. STATE.md is ONE page. It is rewritten, not appended to, at the end
   of every session: what exists, what works, what comes next, and
   what is waiting for Nir. The next agent reads it first, after
   Part 00.

--------------------------------------------------------------------------------
1.12 WHO DOES WHAT IN THIS PART
--------------------------------------------------------------------------------

1. EXPERT: the owner-setup script; our Caddy block and the one import
   line; the Switch Day redirects; anything inside hosting/ .
2. WORKHORSE: the survey; the folder skeleton; DECISIONS.md; the
   notice in Part 00; STATE.md; the configuration files.
3. SCRIPT: am doctor, am build, am publish; the list of old paths;
   the check that Moodle has no folder named "am".
4. NIR -- THE OWNER ACTS of this Part. For each, the EXPERT writes a
   click-by-click checklist on the day, from what the screen shows
   that day.
   O1. Starting owner-setup once on each PC and typing his password.
   O2. Adding the address pre at Cloudflare.
   O3. On Switch Day, pointing www at the new port.

--------------------------------------------------------------------------------
1.13 DONE MEANS
--------------------------------------------------------------------------------

Part 01 is built when all of these are true:
1. attract-mode/DECISIONS.md exists with D1 to D10.
2. The notice of 1.2 stands at the top of part-00.md .
3. Both survey files exist.
4. The folder skeleton of 1.7 exists on both PCs, including the
   big-files folder, and Syncthing copies a test file both ways.
5. https://pre.strulovitz.org/ shows the existing site.
6. "am doctor" runs on both PCs and prints matching versions for
   everything installed so far.
7. The three existing websites answer exactly as before.
8. STATE.md is written.
Moodle at www is the "done" of Part 08, not of this Part.

--------------------------------------------------------------------------------
1.14 NOT DECIDED HERE
--------------------------------------------------------------------------------

1. The formats inside vault/ and levels/ -- Parts 02 and 04.
2. The toy libraries and the page-weight limits -- Part 05.
3. Recording, the voice, uploading to YouTube -- Part 06.
4. Moodle: installation steps, the front page, how departments and
   Levels become courses, guest access, PayPal, quizzes, outgoing
   email, privacy settings -- Part 08.
5. What the two icons do step by step, how Moodle's data is handed
   over, Syncthing's settings, backups, updates -- Part 09.
6. The art departments and the one-to-one sessions -- Part 10.
7. The build order and Nir's weekly routine -- Part 11.

--------------------------------------------------------------------------------
1.15 WORDS ADDED TO THE GLOSSARY
--------------------------------------------------------------------------------

1. THE PREQUELS -- Nir's existing projects, at pre.strulovitz.org .
2. SWITCH DAY -- the day Moodle is installed at www and the old site
   becomes the Prequels.
3. PLAIN FILES -- the toys and their libraries, served under /am/ .
4. SHORT LINK -- /am/go/NAME , the address we give to people.
5. BIG-FILES FOLDER -- attract-mode-files/ in the home folder.
6. HAND-OVER -- Moodle's data travelling from one PC to the other.
7. OWNER ACT -- a rare act that only Nir can do, because it needs
   his password or his account.
8. PIN -- a fixed version number in the pins file.
9. SURVEY -- the read-only report on one PC.
10. am -- the single command of the production line.

================================================================================
END OF PART 01
================================================================================
