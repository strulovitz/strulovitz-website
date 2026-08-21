SESSION STATE - AI PANORAMA - START HERE AFTER A RESTART
=======================================================

Written: 2026-08-21, by Claude Opus 5 in OpenCode on the desktop (Linux Mint
22). This file exists so that a fresh agent with no memory can carry on
without Nir having to explain anything.

Keep this file up to date at the END of every session. It is the handover.


HOW TO TALK TO NIR (read this first, it matters more than the code)

1. He is Nir. Never call him "boss".
2. Use lots of emojis. Be warm.
3. HE CANNOT SCROLL UP in OpenCode on Linux. So every message must be
   SHORTER THAN ONE SCREEN, and the important part must be at the END.
4. He does not read or write code and does not wish to. Plain language only.
5. Never use quiz or multiple-choice question tools. Plain text questions.
6. Expensive model for hard things, cheap model for simple things - see the
   grunt agent below.


WHAT THIS PROJECT IS

AI PANORAMA: a free, open-source four-dimensional VR encyclopedia-magazine
about artificial intelligence, published at https://www.strulovitz.org/ .

The law is the Bible: bible/part-00.md through bible/part-13.md in this
repository, fourteen files. Part 00 outranks everything. READ THE PARTS YOUR
TASK TOUCHES BEFORE TOUCHING ANYTHING. If an instruction conflicts with the
Bible, stop and tell Nir in plain words; never resolve it yourself.

Nir's own rulings that differ from the Bible's letter are recorded in
DECISIONS.md in this repository. Read that together with Part 00. Do not edit
the Bible.


THE MACHINES (DECISIONS.md decision 7: plain names, no codenames)

desktop-linux is the desktop's Linux side. Linux Mint 22.2, Intel i9-13900KF,
62 GB RAM, NVIDIA RTX 4070 Ti with 12 GB. This is the machine you are on. Its
job is the database and the pipeline: the library and the factory.

laptop-linux is the laptop's Linux side. Debian 13, Intel Core Ultra 9 275HX,
62 GB RAM, NVIDIA RTX 5090 Laptop with 24 GB. Its job is the graphics card
work: images through ComfyUI, and speech-to-text through Whisper.

Nir also has Windows 11 on both machines. Those Windows sides are NOT used for
the magazine's machinery, but Nir does want an agent able to talk to him from
each of them, so they get their own names and bots: desktop-windows and
laptop-windows.

The laptop cannot be left running day and night. The desktop can be, but Nir
prefers not to, so that it lasts longer.

NIR HAS AN OLD SPARE COMPUTER. IT IS NOT PART OF THIS PROJECT. He expects it
to stop working before long, he will not leave it running, and nothing may be
built to depend on it. Do not propose using it. See DECISIONS.md, decision 4.
This is why the weekly snapshot timer uses catch-up: it makes the archive
survive the desktop being switched off, without needing another machine.

THE DISK RULE, WHICH INSTALLERS WILL TRY TO BREAK:
On the desktop (Linux), the system partition has about 46 GB free. /home has
1.7 TB with about 1.2 TB free. Every folder that grows - the Neo4j database,
frozen source text, images, exports, caches, model files - MUST live under
/home/nir/ . Never accept a package's default location under /var without
checking which partition it lands on. Planned home for project data:
/home/nir/ai-panorama-data/ .

There is also an external 3.6 TB drive at /media/nir/EXTERNAL12, but it is
88 percent full and formatted for Windows, so it is not suitable for the
database.


WHICH MODEL DOES WHICH WORK (Nir is paying, so this matters)

Claude Opus 5 keeps: the four-dimensional mathematics, layout and
projection code, the Neo4j data model, security wrapping, prompt design,
and anything touching an Iron Law.

Claude Sonnet 5 takes: installing software, writing runbooks, boilerplate
HTML and CSS, moving files, schema example files, formatting passes.

The Sonnet helper is configured as a subagent named "grunt" at
/home/nir/.config/opencode/agent/grunt.md . Call it with the task tool using
subagent_type "grunt". NOTE: it only exists after OpenCode has been
restarted, because OpenCode reads its configuration once at startup.
/home/nir/.config/opencode/opencode.jsonc also sets small_model to Sonnet
for OpenCode's own little internal jobs.


WHAT IS ALREADY DONE AND WORKING (do not redo any of this)

1. THE PRICE HISTORY ARCHIVE IS RUNNING. This was the urgent item, because
   past prices cannot be recovered later.
   Script: pipeline/stages/snapshot_openrouter.py
   Data: pipeline/snapshots/openrouter/YYYY-MM-DD.json plus index.json
   First snapshot: 2026-08-21, 419 models, 414 of them with a price.
   It needs no API key (the OpenRouter models endpoint is public), is safe
   to run many times a day, and refuses to overwrite an existing archive
   file unless forced.
   Schedule: a systemd USER timer on the desktop (Linux), Mondays about
   09:00, with
   Persistent=true so it catches up if the machine was switched off.
   Files: /home/nir/.config/systemd/user/ai-panorama-snapshot.service
   and .timer . Check it with:
       systemctl --user list-timers ai-panorama-snapshot.timer
   Runbook: ops/runbooks/weekly-openrouter-snapshot.md

2. THE SECRET GUARD IS INSTALLED. ops/check-secrets.sh runs automatically
   before every commit through .git/hooks/pre-commit . It blocks passwords
   and API keys from entering git history, prints only the file and line
   number and never the secret itself, and has been tested in both
   directions. Emergency bypass is git commit --no-verify .
   Runbook: ops/runbooks/install-the-secret-scanner.md
   Note: git hooks do not travel with the repository. On a new machine the
   hook must be installed again by hand, once.

3. .env.example lists every secret the project will need, with dummy
   values. The real .env does not exist yet.

4. The repository folder skeleton exists per bible/part-01.md section 1.7:
   pipeline/ site/ comfy/ exports/ ops/ schemas/ config/ .

5. Python is set up in pipeline/ with uv. Only one dependency so far,
   httpx, pinned by pipeline/uv.lock . Run things with:
       cd /home/nir/strulovitz-website/pipeline && uv run <script>

6. The existing website pages were not touched: index.html, hive/, ghost/,
   images/, style.css are exactly as they were.

Already installed on the desktop (Linux): Python 3.12.3, uv 0.12.0, node 24,
git, ffmpeg, OpenJDK 21, Neo4j Community 2026.07.1.
NOT installed on the desktop (Linux) yet: Tailscale, Docker or Podman,
OpenClaw.

7. THE TELEGRAM CONTROL ROOM WORKS, BOTH WAYS.
   Bot: display name "Desktop Linux", address t.me/NirAtlasDesktop_bot . The
   address still carries the old word because a Telegram bot address is
   permanent once created (DECISIONS.md decision 7); Nir only ever sees the
   display name "Desktop Linux" when a message arrives.
   Created 2026-08-21. The token and Nir's numeric user id are in .env, which
   git is forbidden to touch. The real usernames of all four planned bots are
   recorded in DECISIONS.md decision 6, because the tidy names from decision 5
   were already taken by strangers.
   The one place allowed to send a message: pipeline/lib/telegram.py . It can
   only ever message Nir - there is deliberately no way to pass another
   recipient in. Test it with: cd pipeline && uv run lib/telegram.py
   LESSON LEARNED: set the bot's display name yourself with the setMyName API
   call. Do not ask Nir to type it into BotFather; that is how the first bot
   ended up named "@AtlasDesktopBot" with a stray @ sign.

8. THE DAILY HEARTBEAT RUNS AT 10:30 EVERY MORNING (Nir chose the time; he is
   not an early bird). It sends ONE short Telegram message saying whether
   the desktop (Linux) is healthy: the price archive's freshness, the
   database's state, free space on both disks, and whether anything is
   unsaved.
   Script: pipeline/stages/heartbeat.py . Try it without sending anything:
       cd pipeline && uv run stages/heartbeat.py --dry-run
   Timer: systemd USER units ai-panorama-heartbeat.service and .timer, with
   Persistent=true so a switched-off morning is caught up later.
   First real message delivered 2026-08-21 at 10:31. Runbook:
   ops/runbooks/daily-heartbeat.md
   Silence therefore MEANS something: the desktop was off. That is the point.

9. NEO4J IS INSTALLED AND RUNNING ON THE DESKTOP (LINUX) - the project's
   permanent library.
   Community Edition 2026.07.1 from Neo4j's own apt repository, on OpenJDK 21.
   ALL of its growing folders are under /home/nir/ai-panorama-data/neo4j per
   DECISIONS.md decision 3; the package's /var defaults were commented out,
   not deleted, so the change stays visible in /etc/neo4j/neo4j.conf .
   It listens on localhost ONLY (verified with ss: 127.0.0.1 on 7474 and
   7687). Never expose it; later only the private Tailscale address may be
   added (LAW 4, part-07.md 7.6.1).
   Permissions trick worth remembering: /home/nir is private, so instead of
   adding the neo4j service user to Nir's group, a single ACL lets it WALK
   THROUGH the folder without reading it: sudo setfacl -m u:neo4j:x /home/nir
   Runbook: ops/runbooks/neo4j-on-the-desktop.md
   Exact settings, for rebuilding from scratch:
   config/neo4j-desktop-linux-settings.md
   (/etc/neo4j/neo4j.conf is a system file and is NOT in git, which is why
   that record exists. On a package upgrade, KEEP the local config.)

10. THE ONE DOOR TO THE DATABASE EXISTS: pipeline/lib/db.py . No other file
    may import the neo4j driver (bible/part-01.md 1.4). It holds connect(),
    ensure_schema(), log_job(), read_jobs(), already_done() for idempotency,
    and health() for the heartbeat. Look inside the database safely, writing
    nothing, with: cd pipeline && uv run lib/db.py

11. THE JOB LEDGER IS ALIVE (bible/part-12.md 12.1). Every install, config
    change and stage run becomes one immutable JobLedgerEntry, and the
    mandatory plain_words sentence is ENFORCED IN PYTHON: "done", "ok" and
    "ran the stage" are refused, tested. It is refused in Python rather than
    by the database because property-existence constraints are a paid
    Enterprise feature; job_id uniqueness IS enforced by the database.
    Seven entries already describe the work of 2026-08-21. Append only:
    corrections are NEW entries naming the job_id they correct.


WHAT TO DO NEXT, IN ORDER (the rest of Milestone 0, bible/part-13.md 13.1)

STEP A. DONE - the Telegram control room and the daily heartbeat, see items 7
and 8 above. What REMAINS of it: three more bots when Nir wants them
(laptop-linux, and the two Windows sides), each created the same way, with
the token for the laptop-linux bot living in the .env on the laptop (Linux)
and never on the desktop (Linux). Also still outstanding: OpenClaw itself is
not installed, so Nir can be TOLD things but cannot yet TALK BACK and give
approvals by Telegram. That is the next piece of the control room, and
Milestone 0 wants approvals to work.

STEP B. DONE - Neo4j and pipeline/lib/db.py and the job ledger, see items 9,
10 and 11 above.

STEP C. Feed the price snapshots into Neo4j as immutable rows, keeping the
JSON files as the frozen evidence. Also add the matching schema file plus an
example file in schemas/ (bible/part-02.md 2.8). Use already_done() from
lib/db.py so re-running is harmless, and log_job() for every run.

STEP D. Tailscale on the desktop (Linux) and the laptop (Linux), so the two
machines can talk privately, and so the Quest 3 headset can reach a
development server later. Needs Nir's password. When it is done, Neo4j's
listen address may gain the Tailscale address, and nothing else, ever.

STEP E. The discovery report. Inventory both machines and write it to the job
ledger with plain-language wording Nir actually understands. The desktop
(Linux) is already inventoried in this file; the laptop still needs doing,
and it is a different machine, so it means working there or over Tailscale.

STEP F. Deploy a placeholder page to strulovitz.org through the full ritual:
a versioned folder plus a tiny pointer.json uploaded LAST
(bible/part-01.md 1.9). Nir does the FileZilla dragging by hand. This proves
the deployment path before anything depends on it. Nir has not yet given the
FTP details, and by design no agent ever gets the FTP password.

MILESTONE 0 IS DONE WHEN: Nir has done one complete deploy ritual, the first
weekly snapshot exists in Neo4j as well as in the repository, the Telegram
heartbeat has run three mornings in a row, and the ledger shows every
install in words Nir understands. Do not start Milestone 1 before that.
Progress as of 2026-08-21: the heartbeat has run once (one morning of three),
the ledger requirement is met, the snapshot is not yet in Neo4j, and the
deploy ritual has not been attempted.

AFTER MILESTONE 0 comes Milestone 1, "Hello, Tesseract": true
four-dimensional rotation in VR on the Quest 3, built on fake data, before
any content pipeline exists. Its definition of done includes five human test
sessions and, formally, Nir smiling. See bible/part-13.md section 13.2.


THINGS NIR STILL OWES THE PROJECT (ask, do not nag)

1. His administrator password, at the moment Tailscale gets installed. He
   gave it once on 2026-08-21 for the Neo4j install; it was used and never
   written into any file. Ask again rather than assuming it is remembered.
2. An OpenRouter API key, when the article pipeline starts. Not needed yet.
3. The Dreamhost FTP host and username, for the first deployment. The
   password stays in his FileZilla and never comes to us.
4. Rewriting the Space Colonization page in his own words - his own task,
   noted in TODO.md, to be done when he is rested.
5. Tokens for the three remaining Telegram bots, whenever he wants them. He
   only ever pastes a token; the agent sets the name itself.


A REMINDER, NOT AN OPEN IDEA

Do not propose moving any task onto the old spare computer, and do not propose
leaving any machine running day and night. Both were considered and ruled out
by Nir on 2026-08-21. The weekly snapshot already survives the desktop being
switched off, because its timer catches up on the next boot.
