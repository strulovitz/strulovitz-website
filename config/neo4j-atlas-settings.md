NEO4J ON ATLAS: THE EXACT SETTINGS, AND WHY EACH ONE IS THERE
==============================================================

WHY THIS FILE EXISTS

The real settings file is /etc/neo4j/neo4j.conf, which is a system file on
Atlas and is NOT, and must never be, tracked in git. This document is the
record of exactly what was changed in that system file and why, so that this
same machine could be rebuilt from scratch, or a second machine set up to
match it, without anyone having to guess or rediscover it by trial and error.

If a future apt upgrade of the neo4j package ever asks whether to keep the
existing (modified) configuration file or install the package's new default
one, the answer is always: KEEP THE LOCAL VERSION. The package's own default
would put everything back on the small system disk and re-open the listen
address question, both of which would break Decision 3 and Bible LAW 4.


WHAT WAS INSTALLED, AND FROM WHERE

1. Java, first, because Neo4j needs it:
       openjdk-21-jre-headless, version 21.0.11

2. Neo4j Community Edition, version 1:2026.07.1, from Neo4j's own official
   apt repository, not from any generic Linux distribution repository. The
   repository was added with these exact lines:

   Signing key saved at:
       /etc/apt/keyrings/neotechnology.gpg

   Repository listed at /etc/apt/sources.list.d/neo4j.list, containing this
   one line:
       deb [signed-by=/etc/apt/keyrings/neotechnology.gpg] https://debian.neo4j.com stable latest

   After that, the normal apt install of the neo4j package was run.


THE SETTINGS BLOCK ADDED TO THE END OF /etc/neo4j/neo4j.conf

The block below was appended verbatim to the end of the real config file, as
a clearly marked section titled "AI PANORAMA SETTINGS - added 2026-08-21".
It is reproduced here, as plain text lines, exactly as it appears there:

    server.directories.data=/home/nir/ai-panorama-data/neo4j/data
    server.directories.logs=/home/nir/ai-panorama-data/neo4j/logs
    server.directories.import=/home/nir/ai-panorama-data/neo4j/import
    server.directories.transaction.logs.root=/home/nir/ai-panorama-data/neo4j/data/transactions
    server.default_listen_address=localhost
    server.memory.heap.initial_size=4g
    server.memory.heap.max_size=4g
    server.memory.pagecache.size=4g

WHY EACH LINE IS THERE:

1. server.directories.data, server.directories.logs,
   server.directories.import
   Decision 3 in DECISIONS.md: everything that grows lives under
   /home/nir/, never under /var. Atlas's system disk has only about 46 GB
   free; /home has about 1.2 TB free. The package's own defaults for these
   three settings point at /var/lib/neo4j/... and /var/log/neo4j; those
   original lines were commented out near the top of the file (left
   visible, not deleted), so the change is easy to see and easy to undo if
   it were ever wrong.

2. server.directories.transaction.logs.root
   This one setting is written as a full, absolute path on purpose,
   instead of the shorter relative path "data/transactions" that the
   package's own commented-out example suggests. The wart that was found
   and fixed the same day: with the relative path, Neo4j resolves it
   underneath the data directory a second time, producing a doubled,
   nonsensical folder called data/data/transactions. This was caught
   before any real data existed, the setting was corrected to the full
   absolute path shown above, and the doubled folder was removed.

3. server.default_listen_address=localhost
   Bible LAW 4 and part-07.md section 7.6.1: this database must never be
   reachable from the open internet. The package's own default already
   only listens locally by default, but this line makes the intention
   explicit and permanent rather than accidental, so nobody mistakes the
   silence for "it just hasn't been configured yet". Verified afterwards
   with "ss -ltnp": ports 7474 and 7687 both listen only on 127.0.0.1.
   Later, and only later, the private Tailscale address may be added
   alongside localhost on this same line. Nothing else, ever.

4. server.memory.heap.initial_size, server.memory.heap.max_size,
   server.memory.pagecache.size
   Atlas has 62 GB of RAM in total, but it also has to run the desktop
   itself and, at times, the image generation software. 4 GB of working
   memory (the heap) plus 4 GB of page cache is far more than this
   database needs for years of the job ledger and the magazine's content,
   and it leaves the rest of the machine comfortable. Raise these numbers
   only if an actual measurement, not a guess, calls for it.


THE FOLDERS THEMSELVES: HOW THEY WERE CREATED

The folders were created directly under /home/nir/ai-panorama-data/, owned
by the neo4j system user (because that is the account the service runs
as), with permissions that keep them closed to everyone except that
account and Nir himself:

    /home/nir/ai-panorama-data/neo4j/data
    /home/nir/ai-panorama-data/neo4j/data/transactions
    /home/nir/ai-panorama-data/neo4j/logs
    /home/nir/ai-panorama-data/neo4j/import
    /home/nir/ai-panorama-data/backups   (created empty, for future dumps)

Ownership was set to the neo4j user and group. On top of that, an access
list (not the plain owner/group bits) was used so that Nir also keeps full
access to ai-panorama-data, without needing to be a member of the neo4j
group.


THE ONE PERMISSION ADDED OUTSIDE ai-panorama-data, AND WHY IT IS SAFE

/home/nir itself is private: only Nir can open it or list what is inside
it. That meant the neo4j service user, on its own, could not even reach
down into ai-panorama-data, because it could not get past the front door of
/home/nir at all.

The fix that was used is one single command:

    sudo setfacl -m u:neo4j:x /home/nir

This grants the neo4j account only the "x" (execute, meaning "may pass
through") permission on /home/nir itself. It does NOT grant "r" (read), so
neo4j still cannot list what else is inside Nir's home folder, and it does
NOT grant any access at all to any other folder inside /home/nir besides
the one it is specifically given access to further down. It is the
narrowest possible door: one account may walk through the hallway to reach
one room, and cannot open any other door along the way.

The alternative that was rejected on purpose was adding the neo4j account
to Nir's own Linux group. That would have been a much bigger key: it would
have given the database service the same broad access Nir's own group
membership carries across his entire home folder, including files that
have nothing to do with the database at all. One narrow ACL entry achieves
the one real requirement (reach ai-panorama-data) without any of that
side-effect.


A NOTE ON COMMUNITY EDITION'S LIMITS

Neo4j Community Edition cannot enforce "this property must always exist on
this kind of node" rules; that particular feature (a property existence
constraint) is only available in the paid Enterprise Edition. Because of
that, the requirement that every job ledger entry must carry a real,
readable plain_words sentence is enforced in Python instead, inside
pipeline/lib/db.py, which is the only code in the whole project allowed to
write to the database. What Community Edition CAN and does enforce on its
own is uniqueness: no two ledger entries may ever share the same job_id,
which is set up as a real database constraint.
