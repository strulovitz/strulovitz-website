RUNBOOK: THE DAILY MORNING HEARTBEAT
=====================================

WHAT THIS IS, AND WHY IT EXISTS

Every morning at about 10:30, Atlas (the desktop) looks itself over and
sends Nir one short Telegram message. It checks three things: the price
archive, the free disk space, and whether any work is sitting unsaved on
this computer instead of on GitHub.

A GREEN message ("Everything is healthy") means IGNORE ME. You do not need
to do anything, you do not need to read it carefully, you can just glance
and move on.

A RED message ("SOMETHING NEEDS YOU") means one of those three checks found
a real problem, and the message itself tells you which line to worry about.

SILENCE IS ALSO INFORMATION. If no message arrives some morning, it almost
always means the desktop was switched off at 10:30. It will catch up and
send the message as soon as the machine is next switched on (see the
Persistent=true explanation below). It is not an emergency by itself - but
if several days go by with total silence AND the machine has clearly been
on, that is worth mentioning to your agent.

Owned by: bible/part-12.md (operations) and bible/part-00.md LAW 11.
The script itself: pipeline/stages/heartbeat.py - read its own top comment
for the full reasoning, this runbook only covers how to live with it.


WHAT THE MESSAGE MEANS, LINE BY LINE

Line 1, the headline: either "Everything is healthy" or "SOMETHING NEEDS
YOU". This is the only line you strictly need to read.

"Price archive: ..." - how many snapshots of AI model prices have been
saved, and how long ago the newest one was taken. This is the single most
important check in the whole project, because a missed week of prices can
never be recovered later. If this line says "TOO OLD", the weekly snapshot
timer may be broken - tell your agent.

"System disk: ... GB free." and "Big home disk: ... GB free." - how much
storage is left on the two disks. If either says "LOW", something is
filling up a disk it should not be on. See DECISIONS.md decision 3: nothing
that grows is supposed to live on the small system disk.

"Repository: ..." - a gentle note, never an error by itself, about whether
there is work on this computer that has not yet been pushed to GitHub.

The last line is just the date and time the check was made.


HOW TO TEST IT WITHOUT SENDING A TELEGRAM MESSAGE

    cd /home/nir/strulovitz-website/pipeline && uv run stages/heartbeat.py --dry-run

This prints the exact message to the screen instead of sending it. Safe to
run as many times as you like, any time of day - it changes nothing.


HOW TO CHANGE THE TIME IT SENDS

1. Open /home/nir/.config/systemd/user/ai-panorama-heartbeat.timer
2. Change the OnCalendar line, for example to 08:00:
       OnCalendar=*-*-* 08:00:00
3. Tell systemd to notice the change:
       systemctl --user daemon-reload
4. Check the new time took effect:
       systemctl --user list-timers ai-panorama-heartbeat.timer


HOW TO TURN IT OFF

    systemctl --user disable --now ai-panorama-heartbeat.timer

This stops the daily message. Nothing else is affected - no data is
touched, no files are deleted.


HOW TO TURN IT BACK ON

    systemctl --user enable --now ai-panorama-heartbeat.timer
    systemctl --user list-timers ai-panorama-heartbeat.timer

The second command confirms when the next message will actually go out.


WHERE THE TELEGRAM TOKEN LIVES

The bot token and Nir's Telegram user id live in the .env file at the top
of the repository (/home/nir/strulovitz-website/.env). That file is never
committed to git - it is listed in .gitignore on purpose, and a pre-commit
secret scanner also blocks it if anyone ever tries. This runbook, like
every file in this project, never quotes the actual token or user id
anywhere. If the heartbeat ever reports it cannot send a message, check
that .env still exists and still holds real values, not the dummy
placeholders from .env.example - but do this by opening the file yourself,
never by asking an agent to print its contents.


IF IT FAILS

Symptom: the dry-run prints a normal-looking message, but no Telegram
message ever arrives at the scheduled time.
    Check the token as described above. Also check:
        systemctl --user status ai-panorama-heartbeat.service
        journalctl --user -u ai-panorama-heartbeat.service -n 40
    The Restart=on-failure / RestartSec=10min setting means it will quietly
    try again ten minutes later on its own if Telegram was briefly down.

Symptom: the message says the price archive is "TOO OLD".
    See ops/runbooks/weekly-openrouter-snapshot.md - that is a separate,
    more urgent problem, because a missed week of prices cannot be
    recovered.

Symptom: a disk says "LOW".
    Something is writing to the wrong place. See DECISIONS.md decision 3:
    everything that grows belongs under /home/nir/, never under /var or on
    the small system disk.

Symptom: several mornings pass with total silence and you know the machine
was on the whole time.
    That is not the normal "desktop was off" case. Tell your agent to run
    the dry-run by hand and read the journalctl output above.


ROLLBACK

There is nothing to roll back in the usual sense. This script only ever
reads - the snapshot folder, the disk, and the repository's own status -
and sends one message. It never writes, deletes, or changes anything.

To remove the schedule entirely:
    systemctl --user disable --now ai-panorama-heartbeat.timer
    rm /home/nir/.config/systemd/user/ai-panorama-heartbeat.timer
    rm /home/nir/.config/systemd/user/ai-panorama-heartbeat.service
    systemctl --user daemon-reload

This does not touch the script itself (pipeline/stages/heartbeat.py) or
anything it checked - it only removes the daily schedule.


ONE IMPORTANT LIMITATION - SYSTEMD UNITS DO NOT TRAVEL WITH GIT

The two files that make this run automatically live in
/home/nir/.config/systemd/user/ - NOT inside the strulovitz-website
repository. Git never sees them, and a "git pull" on a new machine will
never create or update them.

This means: if the project is ever set up on a new machine, these two
files (ai-panorama-heartbeat.service and ai-panorama-heartbeat.timer) must
be created again BY HAND, from scratch, exactly the same way the
pre-commit secret scanner hook has to be reinstalled by hand on a new
machine (see ops/runbooks/install-the-secret-scanner.md for that other
example of the same limitation). The content to use is not a secret and
can simply be copied from this runbook or from the working files on Atlas.
