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
   SHORTER THAN ONE SCREEN.
4. THE IMPORTANT THING GOES FIRST. Nir's own instruction, 2026-08-21, after an
   agent put "create the new bot before deleting the old one" at the BOTTOM of
   a message and he had already deleted it: "next time if something is
   important please write it FIRST". So: warnings, and the ORDER in which steps
   must be done, come in the first line. Never bury a consequence under
   pleasantries. If a step is irreversible, say so before the step.
5. HE DOES THINGS IN THE ORDER WRITTEN, immediately and literally. Numbered
   steps are followed exactly as numbered. Therefore never write a numbered
   list whose safe order is different from its printed order.
6. He does not read or write code and does not wish to. Plain language only.
7. Never use quiz or multiple-choice question tools. Plain text questions.
8. Expensive model for hard things, cheap model for simple things - see the
   grunt agent below.


WHAT THIS PROJECT IS

AI PANORAMA: a free, open-source four-dimensional VR encyclopedia-magazine
about artificial intelligence, published at https://www.strulovitz.org/ .

THERE IS NO "OLD WEBSITE". Nir had to correct this twice on 2026-08-21. The
magazine IS the site and lives at the ROOT of the domain; his other projects are
LINKS IN ITS MENU, never the other way round. The menu, in order: AI Panorama,
Night Watch, Hive, Ghost, Learnime, Peak Together. Full list with what each one
is: PROJECTS-AND-MENU.md . Never put the magazine in a subfolder.

TWO DOCUMENTS SIT AFTER THE BIBLE and are Nir's decisions, not law:
PROJECTS-AND-MENU.md (the menu and every project) and NIGHT-WATCH.md (the
design of Night Watch, his cyber-security project: Eunuch and Golden Man, and
the magazine's do-it-yourself workshop feature whose first project it is).
Read NIGHT-WATCH.md before writing a line of Night Watch code; the "castrated"
limited mandate of Eunuch is the product's main feature and an agent that
"improves" it by giving it more power has destroyed the thing.

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

STEP C. DONE - the price archive is now in the library as well as on disk.
Stage: pipeline/stages/load_snapshots.py . Safe to run any number of times:
the database refuses two rows for the same model on the same day at the same
seller, and the stage also asks the ledger whether a file was already loaded.
Use --dry-run to look, --force to reload. Tested three ways on 2026-08-21.
The weekly timer now does BOTH steps by itself: the snapshot service has an
ExecStartPost line that runs the loader after the dated file is written.
Shape files, as bible/part-02.md 2.8 demands: schemas/price-snapshot.schema.json
and schemas/price-snapshot.example.json (three real rows chosen to teach that
zero means free while null means nobody published the number).
IMPORTANT EDITORIAL RULE, ALREADY ENFORCED IN CODE: a model appearing in a
price list does NOT become an entity. It waits as an (:EntityProposal) with
status 'pending' until Nir approves it, because bible/part-02.md 2.4 says
"unresolved mentions never silently create entities; near-duplicate entities
are the disease that killed many knowledge bases". 419 models were waiting as
of 2026-08-21, and NOTHING can approve them yet: that needs the Telegram
one-tap approval flow, which needs OpenClaw. Do not shortcut it by approving
them in bulk without asking Nir.

STEP D. Tailscale. PARTLY DONE 2026-08-21: installed here and joined as
"desktop-linux" at 100.118.103.61 . Nir's private network also holds his two
Windows machines, which he is renaming to desktop-windows and laptop-windows,
and an old machine called ilan that has no job here (decision 4).
STILL TO DO: install it on the laptop's Linux and join as "laptop-linux"; and
ask Nir to disable key expiry on each machine in the Tailscale admin console,
otherwise Tailscale logs them out after six months and the machines stop
talking silently. Only once the laptop is on the private network may Neo4j's
listen address gain the Tailscale address - and nothing else, ever.

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


================================================================================
NIR'S COURSE CORRECTION, 2026-08-21, AND WHAT THE NEXT AGENT MUST DO FIRST
================================================================================

READ THIS BEFORE PLANNING ANYTHING. Nir stopped the session and said, correctly:
"we were supposed to be doing the serious stuff, how to do the fucking 4D
Virtual Reality, and also the 3D is not easy, but 4D even harder. and how to
make the mechanism for automation so that cheap models will be able to do
editions of the website ... it seems to me you are drowning in irrelevant shit."

He is right, and the Bible agrees with him: part-13.md makes Milestone 1 "Hello,
Tesseract" precisely because the hardest risk must die first, while it is cheap.
An agent that keeps building comfortable plumbing instead is avoiding the real
work. Do not do that.

THE TWO THINGS THAT MATTER, IN THIS ORDER:

1. FOUR-DIMENSIONAL VR (LAW 1, the crown law; part-03.md geometry, part-05.md
   interaction, part-13.md 13.2 for the definition of done). Build "Hello,
   Tesseract": a genuine 4D structure, rotated in real time by hand
   controllers on a Meta Quest 3 over WebXR, on fake data, before any content
   exists. Also its flat-screen 3D twin, because no feature ships without both.
   Remember LAW 2: the fourth dimension is NEVER colour.
   STARTED AND WORKING, 2026-08-21 (Claude Opus 5). See the section
   "MILESTONE 1: WHAT NOW EXISTS" at the very bottom of this file.

2. THE EDITIONS MACHINE (part-10.md, part-06.md). Cheap models - Chinese
   open-weight models and the like, through OpenRouter - take the articles and
   YouTube links Nir supplies and produce the TLDRs, the ELI5 explanations, the
   tags, the graphs and the images, with Nir approving by Telegram.
   ARCHITECTURE ANSWER NIR ASKED FOR, so nobody re-litigates it: this needs
   plain Python calling the OpenRouter API through one module
   (pipeline/lib/llm.py, not yet written) with the model name as a parameter
   (LAW 6), plus OpenClaw for the Telegram approvals. It does NOT need OpenCode.
   OpenCode is the workshop the humans and agents build IN; it is not part of
   the running machine, and nothing in production should depend on it.
   NOT STARTED.

WHAT WAS BUILT ON 2026-08-21, AND WHY IT SHOULD NOT BE REDONE OR MOURNED:
the Telegram bot, the daily heartbeat, Neo4j on the big disk, the one database
door with the job ledger, the weekly price archive, and the weekly usage
archive. All of it runs by itself and costs no attention. The ONLY part of it
that was genuinely urgent was the price and usage archive: a week not recorded
can never be recovered. The rest was groundwork that is now done and must not
be expanded further until the two things above exist.

DO NOT, IN THE NEXT SESSION: write more runbooks, add more decisions files,
polish the heartbeat, or refine the model filters. Those are finished. If the
next agent finds itself writing prose instead of a rotating tesseract, it has
made the same mistake this session made.

STILL GENUINELY OUTSTANDING, BUT SMALL AND CHEAP, DO ONLY IF ASKED:
1. Wire the usage snapshot into the weekly timer, the same way the price
   snapshot already has an ExecStartPost line. One line of configuration.
2. Batch 2 of the "which models are current" search prompts (Google, DeepSeek,
   Moonshot, Z.ai, Qwen, Meta, Mistral) for Nir to paste into a web search.
3. Three more Telegram bots, if Nir wants them.
4. The laptop joining the private network as laptop-linux.
5. Nir disabling key expiry on his Tailscale machines.

THE STANDING LESSON FROM THIS SESSION, FOR EVERY FUTURE AGENT:
Nir cannot read code and will not check it, so an agent is trusted to choose
what matters. He measures the project by whether the impossible part is getting
closer, not by how tidy the repository is. When in doubt, build the hard thing.

================================================================================
MILESTONE 1: WHAT NOW EXISTS, 2026-08-21 (Claude Opus 5, desktop-linux)
================================================================================

HOW TO SEE IT, WITHOUT ANY BUILD STEP:
    ./ops/look-at-the-site.sh              then open http://localhost:8080/
    ./ops/look-at-the-site.sh headset      then open the printed https address
                                           in the Quest's own browser
Virtual Reality refuses to start over a plain connection, which is the only
reason the second mode exists. The homemade certificate makes the headset show
one scary warning: Advanced, then Proceed.

THE FILES, AND WHAT EACH ONE IS FOR:
1. site/src/lib/fourd.js  --  ALL the four-dimensional mathematics. One 4x4
   matrix Q is the only orientation state in the whole program, which is why
   Undo is a stack pop and Reset is one line. Six planes of rotation, three of
   them the hyper-rotations. Gram-Schmidt after every compose, so a long
   session cannot let the map slowly shear. The projection is the Bible's
   normalised form, s = (d - w_min) / (d - w), which cannot divide by zero.
   Pure arithmetic: no browser, no three.js, testable by plain node.
2. site/src/lib/fourd.selftest.js  --  49 checks. Run: node site/src/lib/
   fourd.selftest.js . Any change to the maths must keep them all passing.
   They test the properties that MATTER perceptually, not code coverage.
3. site/src/scenes/synthetic.js  --  the fake world: a real tesseract, plus 200
   placeholder nodes in the six w bands of w-definition 1. Positions come from
   a hash of each node's id, never from a random number, so the same node lands
   in the same place forever on every machine. NOTHING in it is real content.
4. site/src/vr/panorama.js  --  the picture: holotable, dithered slab with
   ghosts, drop-stems over a fixed floor grid, the tesseract, cluster labels
   that never change size. Colour means identity and nothing else.
5. site/src/vr/main.js  --  one state machine, two bodies: mouse and keyboard,
   and the Quest 3 controllers. Comfort cap of 25 degrees per second, no
   inertia anywhere, the wrist w-gauge, and the hand menu whose first two items
   are Undo and Reset.
6. site/index.html and site/tesseract.html  --  a plain no-JavaScript landing
   page offering Screen or VR entry, and the application itself.
7. site/vendor/  --  three.js 0.185.1, MIT, kept locally on purpose so the live
   site never depends on anyone else's server (LAW 4).
8. ops/build-export.py  --  the deployment ritual: dated folder first, tiny
   pointer.json LAST, rollback pointers kept in ops/pointers/.
9. ops/look-at-the-site.sh  --  local viewing, and https for the headset.

HOW IT WAS PROVEN, so nobody has to take an agent's word for it: a headless
Chrome test drives the real page with real key events and checks 30 things,
including zero console errors, that something is actually drawn, that the
promised keys do what the landing page says, that the slab really changes which
nodes are solid, and that four quarter-turns return the LIVE view matrix to the
identity to within a millionth. The test now lives in the repository at ops/test-the-4d-page.py and has grown to
36 checks. Run it after ANY change to rotation, projection or comfort code
(part-05.md 5.10 makes that protocol repeat). It found two real faults already,
which is the point of having it.

TWO TESTING TRAPS worth knowing, both commented in that script: three.js turns
matrixAutoUpdate OFF for XR controllers, so a test that places them by hand must
turn it back on; and Object3D.lookAt aims an ordinary object's PLUS Z at the
target, while a controller points along MINUS Z, so an aimed controller must
then be turned around.

TWO TRAPS THAT COST TIME HERE. Both are commented in the code, do not undo the
fixes: (1) three.js draws instanced objects BLACK if a material has
vertexColors switched on and the geometry has no per-vertex colour attribute;
panorama.js now adds a white one automatically. (2) `pkill -f <pattern>` in a
tool-driven shell matches the shell's own command line and kills the session.

WHAT MILESTONE 1 STILL NEEDS BEFORE IT CAN BE CALLED DONE (part-13.md 13.2):
0. NOTE FROM NIR'S FIRST HEADSET SESSION, 2026-08-21: everything worked and he
   liked it, with one fault. He saw the instrument on his left forearm, tried to
   touch it with his right hand and then tried to point the laser at it, and
   nothing happened, because it had been built as a dial with nothing to press.
   FIXED THE SAME DAY: reaching for it, by pointing or by touching, now opens
   the hand menu, and the instrument brightens and prints what to do. THE
   LESSON, worth more than the fix: when a person reaches for a thing, the thing
   must answer. Check every other panel and instrument added in future against
   that.
1. THE W-GYM IS BUILT, and revised once after Nir's first real session:
   site/src/scenes/wgym.js , five lessons, replayable from the loud gold button
   in the top bar or the key L or the hand menu.
   FOUR LESSONS LEARNED FROM WATCHING HIM USE IT, all now enforced by tests:
   (a) NOTHING MAY ADVANCE BY ITSELF. His words: "the lessons are going to the
       next one without the user being aware, he just drops into a new lesson
       because the software decided the previous lesson was through". A finished
       lesson now says what happened and waits for Next; there is a Back button.
   (b) SAY WHAT JUST HAPPENED. "I pressed W and it turned to more full colour
       and I do not understand what happened." Every lesson now has a plain
       sentence explaining its own success.
   (c) A SINGLE LETTER NEEDS A SQUARE CANVAS. Labels were drawn on a canvas
       eight times wider than tall, so one letter was too small to read and he
       was asked to follow a bead F that he could not find. makeTextSprite now
       takes { square: true }.
   (d) MEASURE THE LAYOUT, DO NOT EYEBALL IT. Two letters were printed on top of
       each other. Bead positions are now chosen by measuring their screen
       separation, and a test fails if any two get closer than 0.12.
   Also: every lesson but the first resets the view when it begins, because a
   stray turn made at the end of one lesson was quietly ruining the next.
   TWO MORE FROM HIS SECOND SESSION, also enforced by tests:
   (e) MEASURE WHAT THE PERSON EXPERIENCES, NOT WHAT THE CODE DOES. Lesson 1
       asked him to resize the object and watched graph.scale for it, but on a
       flat screen the wheel dollies the CAMERA and scale never changes, so it
       read "resized 0%" however much he scrolled. It now measures APPARENT
       size, which covers both the headset's two-handed stretch and the wheel.
   (f) ANYTHING THAT CAN BE MOVED MUST BE RESETTABLE. Scrolling forward flew the
       camera through the object into blank space with no way back, and the
       lessons button did not rescue him either. The camera is now clamped
       between MIN_VIEW_DISTANCE and MAX_VIEW_DISTANCE in main.js, resetting
       restores camera, panning, scale AND rotation via resetEverything(), the
       gold lessons button calls it, and there is now a visible "Reset view"
       button beside it because the Home key is useless to somebody who does not
       know it exists.
   TWO MORE FROM HIS THIRD SESSION:
   (g) MESSAGES MUST BE READABLE. "In every place that there is like a message
       box it appears for a split second and disappears immediately, I cannot
       read it." Time on screen now depends on the length of the text, and when
       it expires the message DIMS instead of vanishing, so looking away does
       not lose it.
   (h) LESSON 5 WAS HONESTLY BROKEN, and his diagnosis was exactly right: "the
       dragging with the mouse just rotates the cube normally, like not in 4D".
       One plane at a time leaves two of the four coordinates untouched, so it
       IS an ordinary turn to the eye. A diagonal Shift-drag now turns a
       hyper-plane AND its partner plane at once (xw+yz, yw+xz, zw+xy), which is
       a DOUBLE ROTATION: the one motion with no three-dimensional imitation,
       because in three dimensions any two turns share an axis and add up to
       one. All four coordinates move, and the shape never repeats. This is the
       flat screen's honest equivalent of the two-handed twist, and PARTNER_PLANE
       in main.js is where it lives.
   (i) DO NOT MEASURE A QUANTITY THAT TWO GESTURES BOTH DISTURB. Sliding the
       object about was creeping into lesson 1's RESIZING count, because
       apparent size was measured as the camera's distance to the object, and
       panning changes that distance too. Resizing is now COUNTED when a
       resizing gesture happens (apparentSizeTravel in main.js: the wheel, and
       the two-handed stretch), so sliding contributes exactly nothing. Nir:
       "the moving is NOT resizing".
   FOUR MORE FROM HIS FIRST HEADSET SESSION, which found faults no flat-screen
   test could see. Everything else in VR he reported as working well.
   (j) A FEATURE MUST NOT BE LOCKED DURING THE LESSON THAT TEACHES IT. The
       two-handed twist was gated on tier2Enabled, which is only true AFTER
       graduating, so in lesson 5 both grips fell through to plain scaling and
       nothing happened. Both bodies now use doubleRotationAllowed().
   (k) DO NOT `continue` OUT OF AN INPUT LOOP. The gym's bead-picking branch
       ended in `continue`, which skipped the rest of the right hand including
       the A button, so carrying on from lesson 4 took several presses. Use a
       flag and skip only the part you mean to skip.
   (l) EVERY CONTROL ON THE SCREEN MUST EXIST IN THE HEADSET. There was no way
       to skip, go back, or leave the lessons in VR. The hand menu is now built
       fresh whenever it opens (buildMenu in main.js) and carries the lesson's
       own controls while a lesson is running. The headset panel also always
       prints "A = carry on, Y = menu: back, skip, or leave".
   (m) IF A GESTURE LOOKS DEAD, SAY WHY. He squeezed both grips and "moved his
       hands in all directions" with no effect, because the twist needs the
       WRISTS to turn; two closed fists sliding through the air is a rotation of
       nothing. Holding both grips for 1.4 seconds with no turning now prints
       "turn your WRISTS against each other, like opening a stiff jar".
2. Hover cards and a reading panel in VR. On the flat screen the hover card
   exists as plain HTML; in the headset there is only a highlight and a haptic
   tap so far.
3. Ego mode, the path trail, and Back and Forward along it (part-05.md 5.6).
4. The audio cue package (5.3.4) and the density haptics while swimming.
5. The perftest scene and the ?perftest=1 route (part-04.md), measured on the
   physical Quest 3 rather than on a software renderer.
6. Nir's five test sessions with the tasks from part-05.md 5.10, and Nir
   personally rotating a tesseract in ZW, watching it turn inside out, and
   smiling. That smile is a formal acceptance criterion; an agent cannot tick
   it.
7. THE DEPLOY IS DONE, 2026-08-21: the magazine is live at the ROOT,
   https://www.strulovitz.org/ . The old /ai-panorama/ subfolder was my mistake
   and is now just a one-line redirect to the root. Nir's previous home page and
   stylesheet were downloaded to ops/server-backup/ before anything was
   overwritten, and his originals also remain in this repository at ./index.html
   and ./style.css (stale now: they are NOT what the domain serves).
   HOW THE ROOT STAYS CLEAN AND STILL DEPLOYS ATOMICALLY: index.html and
   night-watch.html sit at the root and are hand-written pages. All the code
   lives in a dated folder. The root page reads pointer.json and aims its two
   entry buttons at whichever dated folder is live, with the live version also
   baked into the links so it works without JavaScript, and falling back to a
   neighbouring tesseract.html when there is no pointer at all, which is what
   makes ops/look-at-the-site.sh work with no build step. The web root on the server is strulovitz.org/ and
   the connection is SFTP on port 22 to vps68338.dreamhostps.com as dh_ptax3d.
   NOTE ON THE RULE: the Bible says Nir uploads by hand in FileZilla and that no
   agent ever holds the password (LAW 4, and part-01.md 1.9). Nir gave the
   password in chat and asked for the upload, and Nir outranks the Bible. It was
   used from an environment variable, written to no file, and Nir was told
   first thing to change it. If a future agent is asked again: ask Nir whether
   he wants to keep doing it this way, and never store the password anywhere.

THE EDITIONS MACHINE (the second thing that matters) IS STILL NOT STARTED.
pipeline/lib/llm.py does not exist yet. The architecture answer stands: plain
Python calling OpenRouter through that one module with the model name always a
parameter, plus OpenClaw for the Telegram approvals. It does not need OpenCode.

================================================================================
SITUATION AT THE END OF 2026-08-21. READ THIS SECTION FIRST.
================================================================================
Written by Claude Opus 5 on desktop-linux, at Nir's request, so that a fresh
agent with an empty memory can carry on without him explaining anything.

WHERE THINGS STAND, IN ONE PARAGRAPH

The hardest and most doubtful part of the whole project now works, and Nir has
confirmed it with his own hands and his own eyes, on a flat screen and on his
Quest 3: "everything works great". www.strulovitz.org IS the magazine now, at
the root of the domain, and a visitor can turn a genuinely four-dimensional
object, swim a slice from fresh news toward settled knowledge, and be taught to
follow an object through a turn that has no three-dimensional equivalent. There
is no real content yet, on purpose. Milestone 1 is substantially built; what
remains of it is listed below, and most of it is small.

WHAT IS LIVE, AND HOW IT GOT THERE

1. The site is served from the root of strulovitz.org. Root files: index.html
   (the landing page, with the menu) and night-watch.html. All the code lives in
   a dated folder, and pointer.json names which folder is live. Currently
   v2026-08-21-l.
2. Deploying: `python3 ops/build-export.py` writes exports/ , then the dated
   folder is uploaded FIRST and pointer.json LAST, which is what makes the flip
   instant. Rollback is re-uploading an old pointer from ops/pointers/ .
3. THE FTP SITUATION, said plainly: the Bible has Nir uploading by hand in
   FileZilla, with no agent ever holding the password (LAW 4, part-01.md 1.9).
   On 2026-08-21 Nir gave the SFTP password in chat and asked for the upload to
   be done for him, and Nir outranks the Bible. It was used from an environment
   variable, written to no file, and he was told first thing to change it.
   HE STILL NEEDS TO CHANGE THAT PASSWORD. Connection: SFTP, port 22,
   vps68338.dreamhostps.com, user dh_ptax3d, web root strulovitz.org/ .
   A future agent must ASK him for it rather than assume, and store it nowhere.
4. His previous personal home page was downloaded to ops/server-backup/ before
   anything was overwritten, and remains in this repository at ./index.html and
   ./style.css (stale: NOT what the domain serves). His Hive and Ghost pages on
   the server were never touched.

THE CODE, FILE BY FILE

site/src/lib/fourd.js         all the four-dimensional maths and nothing else:
                              one 4x4 matrix Q, six planes, Gram-Schmidt after
                              every compose, the normalised projection
                              s = (d - w_min) / (d - w), the pivot rule, the
                              undo stack, and the two-handed twist as a pair of
                              quaternion multiplication matrices.
site/src/lib/fourd.selftest.js  64 checks. Run: node site/src/lib/fourd.selftest.js
site/src/scenes/synthetic.js  the fake world: a tesseract and 200 placeholder
                              nodes in six w bands, placed by hashing their own
                              ids so positions never move between machines.
site/src/scenes/wgym.js       the five lessons.
site/src/vr/panorama.js       the holotable, the dithered slab and its ghosts,
                              drop-stems over a fixed floor grid, labels that
                              never change size, and registerPointSet so extra
                              objects join the ONE projection pass.
site/src/vr/main.js           both bodies: mouse and keyboard, and the Quest 3.
                              Also the wrist gauge, the hand menu, the flash
                              messages, and resetEverything().
site/index.html               the root landing page with the menu.
site/night-watch.html         honest that Night Watch does not exist yet.
site/vendor/                  three.js 0.185.1, MIT, kept locally on purpose.
ops/build-export.py           the deployment ritual.
ops/look-at-the-site.sh       local viewing; "headset" mode serves https so a
                              Quest on the same wi-fi can open it.
ops/test-the-4d-page.py       113 checks driving the real page in a real
                              browser. RUN IT AFTER ANY CHANGE to rotation,
                              projection, comfort or the lessons: part-05.md
                              5.10 makes that protocol repeat. It needs Chrome
                              started detached first; the command is in the
                              file's own header.

WHAT REMAINS BEFORE MILESTONE 1 CAN BE CALLED DONE (part-13.md 13.2)

1. The five human test sessions of part-05.md 5.10, with the five tasks, and
   comfort scored 1 to 5. Nir has effectively done his own, several times over,
   and reported comfort as fine and the experience as good. Madie counts as a
   session; friends count. Results go in the ledger as plain text.
2. The perftest scene and the ?perftest=1 route (part-04.md), measured on the
   physical Quest 3 rather than on a software renderer. Nothing has been
   measured on real hardware yet; the numbers in the debug HUD came from a
   software renderer at 20 to 50 frames per second, which proves nothing about
   the 72 the Quest needs.
3. Hover cards and a reading panel in the headset. On the flat screen the hover
   card is plain HTML; in VR there is only a highlight and a haptic tap.
4. Ego mode, the path trail, and Back and Forward along it (part-05.md 5.6).
5. The audio cue package (5.3.4) and the density haptics while swimming (5.3.5).
6. Nir's formal smile. Arguably already given: "everything works great :-)".

AFTER THAT, THE SECOND THING THAT MATTERS: THE EDITIONS MACHINE

Still not started. pipeline/lib/llm.py does not exist. The architecture answer,
so nobody re-litigates it: plain Python calling OpenRouter through that one
module with the model name always a parameter (LAW 6), plus OpenClaw for the
Telegram approvals. It does NOT need OpenCode; OpenCode is the workshop we build
in, never part of the running machine. Nir will need to provide an OpenRouter
API key when this starts.

SMALL THINGS STILL OUTSTANDING, DO ONLY IF ASKED

1. Wire the usage snapshot into the weekly timer, the way the price snapshot
   already has an ExecStartPost line. One line of configuration.
2. Batch 2 of the "which models are current" search prompts for Nir to paste.
3. Three more Telegram bots, if he wants them.
4. The laptop joining the private network as laptop-linux.
5. Nir disabling key expiry on his Tailscale machines.
6. The 419 model proposals waiting in Neo4j as (:EntityProposal) with status
   'pending'. Nothing can approve them until the Telegram approval flow exists,
   and they must NOT be bulk-approved without him.

BOOT SEQUENCE FOR THE NEXT AGENT

1. Read this file's last section, which is this one, and the accumulated list of
   lessons above it. Then read DECISIONS.md and bible/part-00.md.
2. git -C /home/nir/strulovitz-website pull
3. node site/src/lib/fourd.selftest.js   (64 checks, takes a second)
4. Greet Nir briefly and warmly, with emojis, and ask what he wants next rather
   than assuming. Do not re-explain the state to him; he lived it.
5. If he reports a fault: reproduce it, fix the CAUSE, add a check to
   ops/test-the-4d-page.py that would have caught it, deploy, and tell him in
   plain words what was wrong. Every single fault he reported today was real,
   and none of them would have been found by an agent testing its own work.
