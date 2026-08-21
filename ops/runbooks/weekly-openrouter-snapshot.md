RUNBOOK: THE WEEKLY OPENROUTER PRICE AND SPEC SNAPSHOT
======================================================

WHY THIS IS THE MOST TIME-SENSITIVE THING IN THE WHOLE PROJECT

Release dates are public history that anybody can look up in five years.
Prices are not. Nobody archives what a model cost on a random Tuesday, so
that information is simply gone the moment the provider changes the number.

This means the sentence "this model is getting thirty percent cheaper every
quarter" can only ever be said by someone who quietly saved the Tuesdays.
From today onward, we are that someone.

A missing week is permanent damage. It cannot be filled in later, by anyone,
at any price. That is why this runs before anything else in the project
exists, and why a failure gets a loud alert instead of a quiet retry.

Owned by: bible/part-09.md section 9.4.


WHEN TO USE THIS RUNBOOK

1. The automatic weekly run failed and you got an alert.
2. You want to take an extra snapshot by hand, because something big just
   happened (a major model launch or a price war). The Bible asks for an
   extra snapshot within 24 hours of a major release event.
3. You are setting the whole thing up again on a fresh machine.


BEFORE YOU START

1. You need to be on ATLAS, the desktop machine.
2. You need a working internet connection. Nothing else. In particular you
   do NOT need an API key, a password, or an account. The endpoint we use is
   public, on purpose: a script that must keep working for years should
   depend on as few secrets as possible.
3. The tool `uv` must be installed at /home/nir/.local/bin/uv .


STEPS: RUNNING IT BY HAND

1. Open a terminal.
2. Go to the pipeline folder:
       cd /home/nir/strulovitz-website/pipeline
3. Run the snapshot:
       uv run stages/snapshot_openrouter.py
4. Read the four lines it prints. They are written in plain English and are
   safe to paste into Telegram.
5. Save the new file into git history:
       cd /home/nir/strulovitz-website
       git add pipeline/snapshots
       git commit -m "Snapshot: OpenRouter prices and specs for <the date>"
       git push


HOW YOU KNOW IT WORKED

1. The first line says SNAPSHOT OK, followed by today's date and how many
   models were saved. Roughly four hundred is normal in August 2026.
2. A new file exists, named after today's date:
       pipeline/snapshots/openrouter/YYYY-MM-DD.json
3. The index file lists it:
       pipeline/snapshots/openrouter/index.json
4. From the second week onward, the third line tells you what changed since
   the previous snapshot: how many models appeared, disappeared, or changed
   price. That line is the interesting one, and it is the whole reason the
   archive exists.

If it says SNAPSHOT ALREADY DONE, that is also success. It means today is
already saved and the script refused to overwrite an archive file. Running
the script five times in one day is completely safe.


STEPS: THE AUTOMATIC WEEKLY SCHEDULE (ALREADY INSTALLED)

The schedule is handled by two small files, already in place on Atlas:

    /home/nir/.config/systemd/user/ai-panorama-snapshot.service
    /home/nir/.config/systemd/user/ai-panorama-snapshot.timer

It is set to run every Monday at about nine in the morning.

The important setting inside the timer is `Persistent=true`. It means: if the
computer was switched off on Monday, the snapshot runs as soon as the machine
is switched on again. So a weekend away, or a holiday, does not cost a week
of history.

To check when it will next run:
    systemctl --user list-timers ai-panorama-snapshot.timer

To see what happened on the last run:
    systemctl --user status ai-panorama-snapshot.service
    journalctl --user -u ai-panorama-snapshot.service -n 40

To install it again from scratch on a new machine:
    systemctl --user daemon-reload
    systemctl --user enable --now ai-panorama-snapshot.timer

One honest limitation worth knowing: this kind of timer belongs to Nir's own
login session, so it runs while Nir is logged in to the desktop. Because of
the catch-up setting above, that is almost always good enough. If the machine
is ever left running for weeks with nobody logged in, the fix is a single
command that needs the administrator password:
    sudo loginctl enable-linger nir

That command is optional and has not been run, because it needs Nir's
password and the catch-up behaviour already covers normal life.


THE ALTERNATIVE, IF THE TIMER EVER BECOMES A PROBLEM

Cron does the same job with less cleverness. It does NOT catch up after the
machine was switched off, which is why it is the second choice, not the
first. To use it, run `crontab -e` and add this one line:

    0 9 * * 1 cd /home/nir/strulovitz-website/pipeline && /home/nir/.local/bin/uv run stages/snapshot_openrouter.py >> /home/nir/ai-panorama-data/logs/snapshot.log 2>&1

If you do this, disable the timer first so the work is not done twice:
    systemctl --user disable --now ai-panorama-snapshot.timer


IF IT FAILS

Symptom: the output says SNAPSHOT FAILED and mentions the network.
    The internet was down or OpenRouter was unreachable. Nothing was written.
    Wait a few minutes and run it again by hand. Getting it done on the SAME
    DAY matters much more than getting it done at the scheduled hour.

Symptom: the output says SNAPSHOT FAILED and mentions no usable records.
    OpenRouter changed the shape of its answer. This needs a human decision,
    because the script must not guess. Report it and stop: the archive is
    better with an honest gap than with invented numbers.

Symptom: the model count suddenly drops a lot, for example from four hundred
to forty.
    Do NOT overwrite anything. Take the snapshot as it came, then look at the
    comparison line to see which models disappeared. A real mass withdrawal is
    news; a broken answer is a bug. Both are worth knowing about, and both are
    easier to judge with the file saved than with it thrown away.

Symptom: the same day is already saved and you genuinely need to replace it.
    This should be rare, and it edits history. Think twice, then:
        uv run stages/snapshot_openrouter.py --force
    Record why you did it, because overwriting an archive file is exactly the
    kind of thing LAW 12 exists to make deliberate.


ROLLBACK

There is nothing to roll back in the usual sense. This script only ever adds
one new file and rewrites a small index. It changes no website, touches no
database, and spends no money.

If a bad snapshot file was written and you want it gone, delete that one dated
file and run the script again so the index is rebuilt from what is actually on
disk:

    rm pipeline/snapshots/openrouter/YYYY-MM-DD.json
    cd pipeline && uv run stages/snapshot_openrouter.py

To turn the whole thing off (not recommended, for the reason at the top of
this page):

    systemctl --user disable --now ai-panorama-snapshot.timer
