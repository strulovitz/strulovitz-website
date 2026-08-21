RUNBOOK: NEO4J, THE PROJECT'S LIBRARY, ON THE DESKTOP (LINUX)
==============================================================

WHAT NEO4J IS, IN PLAIN WORDS

Neo4j is the database that holds the project's permanent memory. It is the
one and only place where facts get written down for good: the job ledger
(what every install, every config change, every pipeline run did, in plain
words Nir can read), and later, the content of the magazine itself. Nothing
in this project is allowed to talk to it directly except one file,
pipeline/lib/db.py. Think of Neo4j as the project's filing cabinet, and
db.py as the one clerk who is allowed to open the drawer.

It was installed on the desktop (Linux) on 2026-08-21, version 1:2026.07.1,
Community Edition, from Neo4j's own official software source. The exact
settings that were changed to get it running safely on this machine are
written down in config/neo4j-desktop-linux-settings.md, in this same
repository.
Read that file if you ever need to rebuild this from scratch.


HOW TO CHECK IT IS RUNNING

    systemctl is-active neo4j

This prints "active" if it is up and answering, or something else if not.
For more detail:

    systemctl status neo4j

It runs as a normal system service, under its own user account called
"neo4j", not as Nir. It is enabled, meaning it starts by itself every time
the desktop boots. Nobody needs to remember to turn it on.


HOW TO START, STOP, AND RESTART IT

    sudo systemctl start neo4j
    sudo systemctl stop neo4j
    sudo systemctl restart neo4j

Stopping it is safe. Nothing is lost; it simply becomes unreachable until it
is started again. Restarting is the normal fix after a settings change.


HOW TO LOOK INSIDE IT WITHOUT BREAKING ANYTHING

    cd /home/nir/strulovitz-website/pipeline && uv run lib/db.py

This is the safe, read-only way to check the library. It prints how many
things the database is holding, the newest entry in the job ledger, and the
last several ledger entries in plain words. It writes nothing. It is safe
to run at any time, as often as you like, including while a pipeline stage
is working.


WHERE EVERY FOLDER IS, AND WHY IT IS ON THE BIG DISK

Decision 3 in DECISIONS.md is the rule: on the desktop (Linux), the system
disk has only
about 46 GB free, while /home has about 1.2 TB free. Anything that grows
must live under /home/nir/, never at a package's default location under
/var. Neo4j's own defaults pointed at /var, so those lines were commented
out (left visible, not deleted) and replaced. The folders now are:

    /home/nir/ai-panorama-data/neo4j/data
        The database itself: every node, every relationship, every ledger
        entry.

    /home/nir/ai-panorama-data/neo4j/data/transactions
        The database's write-ahead log. This lives inside the data folder
        on purpose, and the setting for it is written as a full, absolute
        path rather than a short relative one. See the wart below for why.

    /home/nir/ai-panorama-data/neo4j/logs
        Neo4j's own log files, the ones you read when something goes wrong
        (see "if it will not start" below).

    /home/nir/ai-panorama-data/neo4j/import
        A drop-box folder for bulk imports later. Empty for now.

    /home/nir/ai-panorama-data/backups
        Empty for now. This is where future database dumps will go.

A small permissions detail worth knowing: /home/nir itself is private
(only Nir can look inside it), so the neo4j service user could not reach
the ai-panorama-data folder by default. Rather than adding the neo4j
account to Nir's own group, which would let it read everything else Nir
owns in his home folder too, a single narrow permission was added that
only lets the neo4j user WALK THROUGH /home/nir on its way to the one
folder it needs, without being able to read or list anything else inside
it. Nir keeps his own full access to ai-panorama-data as well. This is the
smaller, safer change: one exact door, instead of a master key.


HOW TO PROVE IT IS NOT EXPOSED TO THE INTERNET

The Bible (LAW 4, and part-07.md 7.6.1) is absolute about this: the
database must never be reachable from outside this computer. Two commands
prove it is not:

    ss -ltnp | grep -E '7474|7687'

Both lines must show the address as 127.0.0.1 (or the equivalent
[::ffff:127.0.0.1]), never 0.0.0.0 and never a real public IP address.
7474 is the browser interface's port; 7687 is the one the pipeline code
actually talks to.

    sudo grep -n "listen_address" /etc/neo4j/neo4j.conf

The line that matters is server.default_listen_address=localhost. If that
line ever says 0.0.0.0, or if it is missing, something is badly wrong and
must be reported before doing anything else. Later, and only later, the
private Tailscale address may be added alongside localhost. Nothing else,
ever.


IF IT WILL NOT START

Look in two places, in this order:

    ls -la /home/nir/ai-panorama-data/neo4j/logs
    (then read the newest file in there, usually neo4j.log or debug.log)

    journalctl -u neo4j -n 100 --no-pager

Between the two, the actual reason is almost always visible in plain
English near the bottom: a permissions problem, a full disk, a bad setting
in the config file. Do not guess and do not restart it repeatedly hoping
it fixes itself; read what it says first.


THE BROWSER INTERFACE (OPTIONAL, NIR NEVER NEEDS THIS)

Nir can, if he is ever curious, open a normal web browser and go to
http://localhost:7474 while sitting at the desktop (Linux). It will ask for
a username and password: the username is neo4j, and the password is the
one in the .env file. This is completely optional. Nir never needs to do
this for the magazine to work; it exists only as a way to peek inside the
filing cabinet by hand, if he ever wants to.


WARNINGS FOR EVERY FUTURE AGENT

No agent may ever, for any reason:

1. Change server.default_listen_address away from localhost, or add
   0.0.0.0, or open this database to the public internet. That is an Iron
   Law (LAW 4), not a preference.

2. Move the data, logs, transactions, or import folders back to /var or
   to any location on the small system disk. That breaks Decision 3.

3. Delete, edit, or "clean up" anything already written into the job
   ledger. It is append-only by design (LAW 12). A mistake is corrected by
   writing a NEW entry, never by touching an old one.

4. Read, print, log, or write the database password anywhere. It lives
   only in the .env file, which git is forbidden to touch.
