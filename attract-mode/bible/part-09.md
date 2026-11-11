================================================================================
ATTRACT MODE -- THE BIBLE -- PART 09 OF 11
OPERATIONS
Version 1.0 -- 11 November 2026
Obeys Parts 00 to 08, with their notices and with section 9.2 below.
================================================================================

HOW TO READ THIS PART

This Part says how the website moves between Nir's two PCs, what
runs while a PC is serving, what happens after a crash, and how
things are backed up and updated. Section 9.3 is the example.
Read it first.

This file is saved VERBATIM at: attract-mode/bible/part-09.md

--------------------------------------------------------------------------------
9.1 THREE THINGS TRAVEL, IN THREE WAYS
--------------------------------------------------------------------------------

1. THE WORK (texts, scripts, the vault) travels by Git.
2. THE BIG FILES (footage, films, packages, books) travel by
   Syncthing, directly between the two PCs.
3. MOODLE'S DATA (accounts, payments, scores, uploaded packages)
   travels by the HAND-OVER: one PC exports it, Syncthing
   carries the export, the other PC loads it.

Syncthing never touches Moodle's live folders or its live
database. It carries only the hand-over folder. Copying a
running database is how data gets destroyed.

--------------------------------------------------------------------------------
9.2 DECISIONS, ADDITIONS, FROM MEMORY
--------------------------------------------------------------------------------

Added to attract-mode/DECISIONS.md :

Decided by Nir, 11 November 2026:
D54. Insert Coin costs 5 US dollars, once. Access is for ever,
     and includes every Challenge added later. The line on its
     page: "5 dollars, once. The price of one coffee. Yours for
     ever."

Chosen for Nir by the author of this Part; Nir may reverse any:
D55. THE BATON: one small file says which PC holds Moodle's
     data.
D56. While serving, a PC exports Moodle's data every night.
D57. While serving, a PC fetches new work every ten minutes and
     puts it into Moodle by itself.
D58. A second USB stick, AMBACKUP, holds a weekly copy and is
     kept away from the PCs.
D59. OPEN, Nir's: which PC serves while he travels (9.11).
     Until he says: the PC that stays at home.

ADDITIONS. These add to earlier Parts and contradict nothing.
1. Part 01, section 1.6: the fetch timer also runs the sync.
2. Part 05, section 5.14: the stamp of the newest build is also
   written into the workshop, so that it travels by Git.
3. Part 08, section 8.9: after Nir says "uploaded", the sync
   runs at once if an agent is there, and otherwise within ten
   minutes by itself.

FROM MEMORY. Each is confirmed by a test of 9.13.
1. Syncthing can tell a script how much of a folder the other
   PC has received.
2. Syncthing can keep replaced and deleted files for a time.
3. Syncthing sends data encrypted. When the two PCs cannot
   reach each other directly, it passes through a public relay
   that cannot read it.
4. The database can be exported whole while it is running.
5. Moodle has command-line tools for: a "back soon" page, its
   clock, clearing its caches, and upgrading its database.
6. Moodle keeps a key in the folder "secret" of its data
   folder. Without it, some saved settings cannot be read.
7. Moodle publishes a small release with security repairs
   about every two months.

--------------------------------------------------------------------------------
9.3 THE EXAMPLE: AN ORDINARY SWITCH
--------------------------------------------------------------------------------

The desktop is serving. Nir wants to record a game on it.

ON THE DESKTOP, a double click on Websites OFF:

    Attract Mode shows "Back soon".
    The tunnel is stopped.
    Database exported: export 0042, 31 MB.
    Moodle's files copied: 3 new.
    Baton: free. Export 0042, from the desktop.
    The laptop has received it.
    Websites are OFF. You can restart into Windows.

ON THE LAPTOP, a double click on Websites ON:

    New work from GitHub: taken.
    Baton: free. Export 0042, from the desktop. It is here,
    and it is whole.
    A safety copy of this PC's old data is kept.
    Database loaded. Moodle's files copied.
    Counted: 14 accounts, 9 paid, 37 scores. As the desktop
    counted.
    The tunnel is started.
    www.strulovitz.org answers from the laptop.
    Baton: the laptop is serving.

Between the two clicks the site is down. A few minutes, if both
PCs are on.

--------------------------------------------------------------------------------
9.4 THE BATON
--------------------------------------------------------------------------------

The baton is the file attract-mode-files/handover/baton.txt
(format only):

    number: 42
    state: free
    pc: desktop
    time: 2026-12-03 21:14
    export: export-0042.sql.gz
    fingerprint: 9f2c...
    moodle: 5.3.1
    counts: accounts 14, paid 9, scores 37
    nightly: nightly-2026-12-03.sql.gz, 03:30

1. STATE is "free" (handed over, nobody is serving) or
   "serving".
2. THE NUMBER only rises. A PC never writes a baton with a
   number lower than one it has seen.
3. The baton is written LAST, after the export is complete. So
   a baton never points at half an export.
4. If Syncthing reports two versions of the baton, ON and OFF
   stop and say so. The EXPERT looks.

--------------------------------------------------------------------------------
9.5 WHAT THE TWO ICONS DO
--------------------------------------------------------------------------------

The two existing icons stay. Each calls one new line: "am serve
off" and "am serve on". The EXPERT adds the two lines to the
scripts in hosting/bin (Part 01, 1.9, rule 6).

WEBSITES OFF.
1. Moodle shows "Back soon".
2. The tunnel and the timers stop. (The tunnel: as before.)
3. The database is exported into the hand-over folder, with its
   fingerprint.
4. Moodle's files are copied there. Only what changed.
5. The accounts, the paid accounts and the scores are counted.
6. The baton is written: free.
7. The script waits up to two minutes and says whether the
   other PC has received everything. If the other PC is off:
   "It will arrive when both PCs are on in Linux."

WEBSITES ON.
1. New work is taken from GitHub.
2. The baton is read:
   a. No baton: this PC's data is the beginning.
   b. Free, from this PC: nothing to load.
   c. Free, from the other PC: the export must be here, with
      the right fingerprint. Then it is loaded.
   d. Serving, by this PC: it was shut down without OFF.
      Nothing to load.
   e. Serving, by the other PC: REFUSE. "The desktop has not
      said OFF. Click Websites OFF there. If it is dead, say:
      take over."
3. The Moodle version in the baton must be this PC's version.
   Otherwise: REFUSE. "Update Moodle on this PC first."
4. A SAFETY COPY of this PC's own database is made, before
   anything is loaded over it. The last five are kept.
5. The database is loaded. The files are copied in. Moodle's
   own upgrade check and cache clearing run.
6. The counts must equal the baton's counts.
7. "Back soon" is taken away. The timers start (9.7).
8. The tunnel starts, as before. The real address is fetched,
   and /hosted-by must name this PC.
9. The baton is written: serving.

WHEN ON REFUSES, the three other websites start as always.
Attract Mode keeps showing "Back soon", and the script says in
one plain sentence what to do.

--------------------------------------------------------------------------------
9.6 WHAT TRAVELS OF MOODLE
--------------------------------------------------------------------------------

1. THE DATABASE: whole, as one compressed file. Never single
   tables: Moodle's tables lean on each other.
2. FROM MOODLE'S DATA FOLDER: the stored files (the packages
   are here), the language folder (the studio words are here),
   and the folder "secret".
3. LEFT BEHIND: caches, temporary files, locks, sessions. Each
   PC makes its own. After a switch, a signed-in player may
   have to sign in again.
4. NOT CARRIED: Moodle's program and its settings file. Each PC
   has its own, from the same pin (Part 01, 1.8).
5. The last seven exports and fourteen nightly exports are
   kept.
6. AN EXPORT IS PRIVATE. It holds the parents' emails, the
   PayPal keys and the mail password. It lives only in the
   big-files folder. Never Git, never a chat (AM-LAW 13).

--------------------------------------------------------------------------------
9.7 WHILE A PC IS SERVING
--------------------------------------------------------------------------------

Five timers. ON starts them, OFF stops them.

1. MOODLE'S CLOCK. Every minute.
2. FETCH AND SYNC. Every ten minutes: new work is taken from
   GitHub. If anything under attract-mode/ changed, or a new
   package was uploaded, "am moodle sync" runs. If the sync
   fails, it changes nothing, and the failure is written into
   the log and shown by "am doctor".
3. THE NIGHTLY EXPORT. At 03:30: the database and the files, as
   in OFF, but without "Back soon" and without changing the
   baton's state. One line of the baton names it.
4. THE SELF-CHECK. Every ten minutes the PC fetches its own
   public address. After three failures in a row, a notice
   appears on the screen and in the log.
5. KEEP-AWAKE. As before.

"am serve status" says in plain words: who is serving, since
when, the last nightly export, the last sync, whether the other
PC is in reach.

--------------------------------------------------------------------------------
9.8 WHEN THINGS GO WRONG
--------------------------------------------------------------------------------

THE SERVING PC IS DEAD (broken, stolen, no power). On the other
PC, Nir says "take over". The agent runs "am serve takeover".
1. It shows: "The newest copy is from 3 December, 03:30.
   Everything after that is missing here: new accounts,
   payments, scores." Nir types the word TAKEOVER.
2. That nightly export is loaded. The baton is written:
   serving, with the next number, and the word "takeover".
3. THE MISSING DAY. The script prints the hours that are
   missing. Nir opens PayPal and reads the payments of those
   hours. For each, the agent checks whether that email has an
   account with access. If not, Nir sends the short letter that
   the EXPERT prepared: please sign up again, and your access
   is opened by hand.
4. WHEN THE DEAD PC RETURNS, its ON finds a higher number. It
   refuses, or loads, by the rules of 9.5. Its own newer data
   is in its safety copy. The EXPERT can take the missing day
   out of it.

ON REFUSES BECAUSE THE EXPORT IS NOT HERE. Both PCs must be on
in Linux, connected, until Syncthing has finished. "am serve
status" shows how far it is.

THE COUNTS DO NOT MATCH after a load. ON stops before the
tunnel starts. The safety copy is loaded back. The EXPERT
looks.

THE DISK IS FILLING. "am doctor" warns under 60 GB free. "am
tidy" lists what could go: takes that were not chosen, old
drafts, old exports. It deletes nothing without Nir's yes.

--------------------------------------------------------------------------------
9.9 SYNCTHING
--------------------------------------------------------------------------------

1. ONE shared folder: attract-mode-files. Only the two PCs.
   Never a third device.
2. NOT CARRIED: the folder work/ .
3. Replaced and deleted files are kept for thirty days. So a
   mistake on one PC does not destroy the file on the other.
4. It starts when Nir logs in to Linux. Both PCs must be on in
   Linux at the same time for anything to travel.
5. In the same home, the PCs find each other directly. Far
   apart, they may pass through a relay (9.2, from memory, 3).
6. OWNER ACT, once: Nir confirms, on each PC, that the other PC
   is his. The EXPERT writes the checklist on the day.

--------------------------------------------------------------------------------
9.10 BACKUPS
--------------------------------------------------------------------------------

WHAT CANNOT BE MADE AGAIN: Moodle's data, the voice sample, the
finished films, the chosen takes, the books. Everything else is
in Git, or can be built again from Git.

WHERE THE COPIES ARE.
1. Git: GitHub and both PCs.
2. The big files and the exports: both PCs.
3. Payments: PayPal keeps its own record.

THE WEAK SPOT. Both PCs stand in one home. And when the PCs are
apart, new things exist on one PC only.

THE STICK. A second USB stick, named AMBACKUP. "am backup
stick" copies onto it: the newest export, Moodle's files, the
voice sample, and the finished films that are new. Once a week
(Part 11). It is kept away from the PCs: another room; on a
trip, another bag. It holds private data, like an export.

--------------------------------------------------------------------------------
9.11 TRAVEL
--------------------------------------------------------------------------------

D59, Nir's choice:
A. THE PC THAT STAYS HOME SERVES (recommended). It stays on, in
   Linux. Nir works on the laptop anywhere: new Levels go by
   Git, packages are uploaded through the browser, and the home
   PC puts them into Moodle by itself (9.7, timer 2). If the
   home PC goes down, the site is down until somebody clicks
   Websites ON there, or until Nir takes over on the laptop
   (9.8) and loses up to a day.
B. THE LAPTOP SERVES. Then the site is down whenever the laptop
   is closed, in a bag, or in Windows.

WITH A, the laptop receives the nightly export whenever it is
on in Linux. Before a long trip: one hand-over drill, and a
fresh copy on the stick.

--------------------------------------------------------------------------------
9.12 UPDATES
--------------------------------------------------------------------------------

MOODLE. At the start of each month the agent opens Moodle's
release page. If a newer small release of the same series
exists, the EXPERT changes the pin. Then "am moodle update":
1. On the serving PC: "Back soon"; a safety copy; the program
   is brought to the pin; Moodle's upgrade runs; "am moodle
   try"; the baton gets the new version.
2. On the other PC, before its next ON: the program is brought
   to the pin. Its data arrives with the next hand-over.
A jump to a new series (5.3 to a later one) is Nir's decision,
never automatic.

THE SYSTEM. Linux's own security updates are Nir's habit, as
today. After any system update: "am doctor". It warns if PHP or
the database changed their series (Part 01, 1.8).

THE LINE. Its Python pieces change only through the lock file,
by the EXPERT.

--------------------------------------------------------------------------------
9.13 COMMANDS, ROLES, DONE
--------------------------------------------------------------------------------

COMMANDS, added to "am":
1. am serve on , am serve off -- called by the two icons.
2. am serve status
3. am serve takeover
4. am backup stick
5. am moodle update
6. am tidy

WHO DOES WHAT.
1. THE STRONGEST MODEL, ONCE: the hand-over scripts, the baton,
   the timers, the take-over.
2. THE EXPERT: Moodle updates; anything after a refusal that
   the plain sentence did not solve.
3. THE WORKHORSE: runs status, the stick, the tidy list.
4. NIR: the two icons; the word TAKEOVER; the stick, once a
   week.

DONE MEANS.
1. One switch in each direction, with the golden Level live:
   the counts match, a score made before the switch is there
   after it, and test T7 of Part 08 holds.
2. ON refuses while the other PC's baton says "serving", and
   the other three websites still start.
3. A DRILL: the serving PC is switched off without OFF. The
   other PC takes over from the nightly export, and the site
   answers.
4. An export with one changed byte is refused.
5. The nightly export has run by itself, and the baton names
   it.
6. A change pushed from the other PC appears on the site
   within ten minutes, with no agent.
7. The stick holds a copy, and that copy has been loaded once
   on the other PC as a test.
8. The seven facts "from memory" of 9.2 are confirmed, or
   corrected here with a notice.

WORDS ADDED TO THE GLOSSARY.
1. BATON -- the file that says which PC holds Moodle's data.
2. EXPORT -- Moodle's database as one file, with a
   fingerprint.
3. NIGHTLY EXPORT -- the export a serving PC makes every night.
4. SAFETY COPY -- a PC's own data, kept before a load.
5. COUNTS -- accounts, paid accounts and scores, compared after
   a load.
6. TAKE-OVER -- serving from the newest nightly export after
   the other PC died.
7. THE MISSING DAY -- what happened between the nightly export
   and the crash.
8. SELF-CHECK -- the serving PC fetching its own public
   address.
9. AMBACKUP -- the second USB stick.

================================================================================
END OF PART 09
================================================================================
