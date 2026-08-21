--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - INTRODUCTION TO PART 01 (not law)
--------------------------------------------------------------------------------

THANK YOU Nir!!! :-) Here is Part 01 — Architecture and Machines. This is the Part that tells every agent WHERE everything lives and WHO does what, so nobody ever installs a database on the wrong machine or tries to make your Dreamhost server "smart." Everything inside one copy-paste-safe fence, as the law demands.

================================================================================
AI PANORAMA — THE BIBLE — PART 01 OF 13
ARCHITECTURE AND MACHINES
Version 1.0 — August 2026
Obeys: Part 00 (Vision and Invariants). If anything here seems to conflict
with Part 00, Part 00 wins and the conflict must be reported to Nir.
================================================================================

--------------------------------------------------------------------------------
1.0 PURPOSE OF THIS PART
--------------------------------------------------------------------------------

This Part defines the physical and logical architecture: which machine runs
what, how data flows from a raw source URL all the way to a Meta Quest 3
headset, how deployment works, and what an agent may and may not install.
Any agent about to run, install, or build ANYTHING reads this Part first.

The architecture in one sentence: everything smart happens at home (THE
KITCHEN), everything public is dumb files on a rented shelf (THE SHELF),
and the two are connected by exactly one human ritual: Nir dragging a
folder in FileZilla.

--------------------------------------------------------------------------------
1.1 THE TWO WORLDS: KITCHEN AND SHELF
--------------------------------------------------------------------------------

THE KITCHEN is Nir's two home Linux PCs. It contains: the Neo4j database
(the single permanent source of truth), the Python pipeline, the layout
computation, image generation (ComfyUI), speech-to-text (Whisper), all AI
agents (OpenCode, OpenClaw), and all secrets. The kitchen may be messy,
powerful, and complicated, because only agents and Nir ever touch it.

THE SHELF is the Dreamhost VPS serving https://www.strulovitz.org/ . It
contains ONLY static files: HTML, JavaScript, CSS, JSON, binary data files,
images, fonts. It has no database, no server-side code, no SSH access in
our workflow, nothing to update, nothing to hack in the usual ways, and
nothing that can crash at 3 AM. Per LAW 4 (Part 00), no agent ever proposes
making the shelf smarter. The shelf's job is to hand files to browsers.

THE BRIDGE between kitchen and shelf is FileZilla over FTP, operated by
Nir's hands. The pipeline's final output is always one folder that mirrors
the website structure file-for-file (see 1.9). Nir drags it. That is the
entire deployment technology, by design: it cannot break, and Nir fully
understands and controls it.

Why this split is strong and not a compromise: the site's heavy work
(3D/4D rendering, graph queries, search, filtering) happens in the
VISITOR'S browser or headset, which is a more powerful computer than most
web servers anyway. The shelf never computes; it only serves. This makes
the public site effectively unbreakable and free of maintenance, which
serves LAW 11 (the 45-minute law) and the Madie clause (longevity).

--------------------------------------------------------------------------------
1.2 THE MACHINES AND THEIR ROLES
--------------------------------------------------------------------------------

MACHINE A — "ATLAS" (the desktop): Lenovo Legion desktop, Intel CPU, 64 GB
RAM, NVIDIA RTX 4070 Ti with 12 GB VRAM, dual-boot Windows 11 + Linux Mint
22. Project work happens ONLY on the Linux side.
ROLE: the LIBRARY AND FACTORY. Runs Neo4j (the source of truth), the
Python pipeline (ingestion, claims, synthesis calls via OpenRouter,
verification, graph analytics, layout, export), the job ledger, and the
export builder. Atlas is the machine that must be ON for a weekly build.

MACHINE B — "FORGE" (the laptop): Lenovo Legion laptop, Intel CPU, 64 GB
RAM, NVIDIA RTX 5090 with 24 GB VRAM, dual-boot Windows 11 + Debian 13.
Project work happens ONLY on the Linux side.
ROLE: the GPU WORKSHOP. Runs ComfyUI (all image generation, per LAW 6
images are the only local generation), and local Whisper for YouTube
subtitle transcription (large-v3 or the current best; the 5090 makes this
fast). Forge also serves as the development machine for the website (Vite
dev server) and, being portable, as the demo machine.

Division of labor rule: DATABASE AND TRUTH live on Atlas; GPU AND PIXELS
live on Forge. Agents never run a second Neo4j on Forge; if Forge needs
data, it asks Atlas over Tailscale. This prevents the deadly "two sources
of truth" disease.

Naming: agents use the names Atlas and Forge in all scripts, logs, docs,
and Telegram messages, so Nir always knows which physical machine is
involved. (Nir: Atlas carries the world; Forge makes things in fire.)

BOTH machines: check-before-install discipline. Before installing anything
(ComfyUI may already exist on one machine), an agent runs a discovery pass,
reports to the job ledger what is already present and which versions, and
only then installs what is missing. No agent ever reinstalls or upgrades a
working component without a ledger entry stating why.

THE HEADSET: Meta Quest 3, the reference VR device. It is a CLIENT, not
part of the kitchen: it only ever opens the website (local dev URL over
the LAN/Tailscale during development, the public site in production).
Nothing is ever installed on the headset; the entire VR experience is
WebXR through the Quest browser, per the stack in 1.6.

--------------------------------------------------------------------------------
1.3 NETWORK TOPOLOGY AND CONTROL
--------------------------------------------------------------------------------

1. TAILSCALE connects Atlas, Forge, and Nir's other devices into one
   private network. All kitchen-internal traffic (Forge asking Atlas's
   Neo4j, agents on one machine driving the other) goes over Tailscale.
   Nothing in the kitchen is ever exposed to the public internet: Neo4j
   listens only on localhost and the Tailscale interface, never 0.0.0.0
   on a public route. Same for ComfyUI and any dev servers.

2. OPENCODE is the hands: agents running in OpenCode on each machine do
   the actual building and script-running.

3. OPENCLAW + TELEGRAM is the control room: Nir supervises, approves, and
   receives alerts through Telegram. Three message disciplines, defined
   once here and used by all Parts:
   - GREEN/RED daily canary message (pipeline health, see Part 06).
   - DECISION REQUESTS: "A / B / C" options, one plain sentence each,
     with a recommendation (per Part 00, section 0.3).
   - ALERTS: spend cap warnings, failed builds, backup failures. An alert
     always says WHAT happened, WHICH machine, and WHAT the agent will do
     next, in plain language.

4. The vote/feedback write-path (arena, v2) also routes through the
   Telegram bot per LAW 4 — the shelf never receives writes. Details in
   Part 10.

--------------------------------------------------------------------------------
1.4 THE SOURCE OF TRUTH: NEO4J ON ATLAS
--------------------------------------------------------------------------------

Neo4j (Community Edition, latest LTS) on Atlas holds EVERYTHING the project
knows, permanently and growing for years:

1. Every source ever ingested (URL, type, fetch date, raw text location,
   simhash for dedup).
2. Every claim (verbatim span, locator, evidence class — schema in
   Part 02).
3. Every event node, canon node, entity, alias, tag, typed edge, influence
   edge.
4. Every edition's outputs and every faithfulness-scoreboard result.
5. Every weekly benchmark/price snapshot (Part 09).
6. Importance/prominence scores with version stamps (Part 08).
7. The job ledger (Part 12) — every pipeline run, its inputs hash, its
   outputs, its cost.

Why a real graph database and not files: the project's core operations ARE
graph operations — k-hop neighborhoods, typed-edge traversals, centrality
for importance, community detection for clusters, alias resolution,
supersession chains. At year-five scale (tens of thousands of nodes,
hundreds of thousands of edges, millions of claims) these must stay
instant and queryable in one line, and the same database must be able to
power bigger things later without migration. Neo4j's Graph Data Science
(GDS) library is used for community detection and centrality (Part 08).

Neo4j is INTERNAL ONLY. Per LAW 4 the public site never talks to it. Per
LAW 12 it is dumped weekly and the dump goes off-site (ritual in Part 12;
the dump travels to a PRIVATE, non-web-accessible folder on Dreamhost via
the same FileZilla ritual Nir already performs, plus a second copy kept on
Forge — two machines, two locations, zero new tools).

Access discipline: pipeline code talks to Neo4j through ONE shared Python
module (`pipeline/lib/db.py`) so that schema changes happen in one place.
Agents never scatter raw Cypher across scripts without going through this
module's helpers.

--------------------------------------------------------------------------------
1.5 THE PIPELINE: PYTHON ON ATLAS
--------------------------------------------------------------------------------

Language and tooling: Python 3.12+, managed with `uv` (fast, reproducible,
one `uv sync` recreates the environment). One repository, one lockfile.

Key libraries (agents pin exact versions in the lockfile):
1. `yt-dlp` — fetch YouTube audio/metadata (audio goes to Whisper on Forge
   for transcription; see Part 06 for why we transcribe ourselves).
2. `trafilatura` — extract clean article text from web pages.
3. `httpx` — all API calls, including OpenRouter.
4. `neo4j` — official driver, used only via `pipeline/lib/db.py`.
5. `networkx` — analytics that are more convenient in Python than GDS.
6. Layout & math: the canon-skeleton force layout and alignment (the
   agents implement per Part 03; whether the force step uses a Python
   library or a small Node.js helper with ngraph is an implementation
   detail the agents choose and document — the OUTPUT contract is fixed
   in Part 03).
7. `simhash` (or equivalent) — syndication dedup.
8. Local NLI / verification helpers as specified in Part 06.

Iron rules restated for the pipeline (details in later Parts):
1. Model names are parameters, never hardcoded (LAW 6). Every LLM call
   goes through one module (`pipeline/lib/llm.py`) which enforces spend
   caps, logging to the ledger, and the hostile-input delimiting of LAW 8.
2. Every stage is idempotent and resumable, keyed by content hash +
   idempotency key (LAW 12).
3. Every stage reads and writes THROUGH Neo4j; files on disk are caches
   and exports, never truth.
4. The pipeline always ends by building the EXPORT FOLDER (1.9). It never
   half-writes into a previous export.

Stage names (defined fully in Part 06; listed here so agents share
vocabulary): INGEST, TRANSCRIBE, DEDUP, EXTRACT (claims), RESOLVE
(entities/aliases), SYNTHESIZE, VERIFY, CANONIZE, SCORE (Part 08), LAYOUT
(Part 03), IMAGERY (ComfyUI on Forge), EXPORT.

--------------------------------------------------------------------------------
1.6 THE WEBSITE STACK
--------------------------------------------------------------------------------

1. Vanilla JavaScript + Vite. NO frameworks (no React, no Vue, no
   Angular). Reason: fewer moving parts for weaker agents to break during
   grunt work, faster loads, and nothing to become obsolete. Vite gives
   `npm run dev` for development and `npm run build` for the static
   bundle.
2. Three.js (pinned version, upgraded deliberately, never automatically)
   for all 3D rendering, with WebXR for VR. ONE codebase renders both
   versions demanded by LAW 1: the flat-screen 3D version and the Quest 3
   VR 4D version. The 4D mathematics (rotation planes, projection,
   slicing) lives in our own small module `site/src/lib/fourd.js`,
   specified precisely in Part 03 and Part 05.
3. Data on the site is PRIMITIVES, not pre-baked answers: the graph ships
   as compact typed-array binaries (positions, importance, tag bitsets,
   adjacency in CSR form — exact formats in Part 02 section on export
   schemas), plus small per-node JSON/HTML for text content, plus ONE
   pre-baked exception: the panorama landing file (Part 08). A client
   query layer (`site/src/lib/query.js`) answers everything else locally:
   ego neighborhoods, k-hop, importance thresholds, tag filters, the lens.
   No server queries exist, per LAW 4.
4. Every node also exists as a REAL static HTML page (the 2D fallback and
   the actual product for search engines, assistants, previews, and
   accessibility — Part 11). The 3D/4D atlas and the HTML kingdom are
   built from the same data in the same export.
5. Performance budgets and rendering discipline are LAW-adjacent and live
   in Part 04 (draw calls under 100 in VR, instancing strategy, label
   atlases, 72 fps on Quest 3, and the rest).

--------------------------------------------------------------------------------
1.7 REPOSITORY LAYOUT
--------------------------------------------------------------------------------

One Git repository, named `ai-panorama`, kept on Atlas, mirrored to Forge,
backed up to GitHub (backup and documentation ONLY, per LAW 4 — nothing
runs from GitHub and the project must survive GitHub being unreachable).

    ai-panorama/
    ├── bible/                  # Parts 00-13. The law. Plain text/markdown.
    ├── pipeline/               # Python. Runs on Atlas.
    │   ├── lib/                # db.py, llm.py, shared helpers
    │   ├── stages/             # one file per stage (ingest.py, extract.py, ...)
    │   ├── golden/             # golden-set fixtures + expected outputs (Part 06)
    │   └── pyproject.toml      # + uv lockfile
    ├── site/                   # the website. Vite project.
    │   ├── src/lib/fourd.js    # 4D math (Part 03/05 spec)
    │   ├── src/lib/query.js    # client query layer over typed arrays
    │   ├── src/scenes/         # graph scene, comparison scenes, w-gym
    │   ├── src/vr/             # WebXR session, controllers, holotable
    │   └── public/             # static assets that ship as-is
    ├── comfy/                  # ComfyUI workflows (JSON), style bible, prompts. Runs on Forge.
    ├── exports/                # build outputs. NEVER edited by hand.
    │   └── v2026-08-20-a/      # one versioned folder per build (see 1.9)
    ├── ops/                    # runbooks (plain language), backup scripts,
    │                           # snapshot cron scripts, validators, perftest
    └── schemas/                # JSON schemas + one example file per schema

Rules: every schema has an example file next to it (Part 00, section 0.3).
`exports/` contents are reproducible artifacts; they are gitignored except
for the manifest of the currently-live version. Secrets live in `.env`
files that are NEVER committed; a `.env.example` always documents every
variable (Part 07).

--------------------------------------------------------------------------------
1.8 DATA FLOW, END TO END (THE WALKTHROUGH)
--------------------------------------------------------------------------------

From a YouTube URL to a reader's hand in VR, numbered:

1. Nir (or a scheduled watcher) gives source URLs to the pipeline on
   Atlas, usually via a Telegram message to OpenClaw ("ingest these
   three").
2. INGEST fetches article text (trafilatura) on Atlas; for videos, Atlas
   asks Forge over Tailscale to run yt-dlp + Whisper and return the
   transcript. All raw text is stored, hashed, deduped (simhash), and
   recorded in Neo4j with fetch dates.
3. EXTRACT pulls claims (verbatim spans + locators + evidence class) via
   OpenRouter calls under LAW 8 delimiting (no tools enabled). RESOLVE
   links claims to entities/aliases in the registry.
4. SYNTHESIZE writes the combined article, TLDR, tag proposals, and image
   prompt FROM THE CLAIM SET ONLY (never from raw prose — Part 06), per
   edition where applicable (Part 10).
5. VERIFY runs a different model plus deterministic checks (every number,
   date, proper noun must exist in the claim set), then the faithfulness
   scoring where editions are involved. Failures loop back or flag Nir.
6. CANONIZE updates canon nodes, lifecycle states, supersession chains.
   SCORE recomputes importance/prominence (Part 08). LAYOUT recomputes
   analytic placements and, on epoch boundaries, the canon skeleton
   (Part 03).
7. IMAGERY: Atlas sends prompts to Forge's ComfyUI (fixed seeds, one
   render per image-model per node), Forge returns labeled images.
8. EXPORT builds one new versioned folder: binaries, JSON, HTML pages,
   images, feeds, the panorama file, the manifest with content hashes,
   and validates EVERYTHING against `schemas/` before declaring success.
9. Telegram tells Nir: "Build v2026-08-20-a ready. 14 new nodes, 3
   updated, all checks green. Drag exports/v2026-08-20-a to the server,
   then drag pointer.json." 
10. Nir performs the FileZilla ritual (1.9). The site flips atomically.
11. A visitor's browser downloads the pointer, then the manifest, then
    the panorama file (instant first view), then lazily the typed-array
    graph and whatever nodes they approach. In VR, the same site enters
    WebXR; the Quest renders the 4D graph per Parts 03/04/05.

--------------------------------------------------------------------------------
1.9 THE EXPORT FOLDER AND THE DEPLOYMENT RITUAL
--------------------------------------------------------------------------------

The contract that makes FTP deployment safe and atomic:

1. Every build produces a COMPLETE, self-contained versioned folder:
   `exports/vYYYY-MM-DD-x/` (x = a, b, c for same-day builds). Nothing
   inside a previous version's folder is ever modified. Large unchanged
   assets (images) may be shared via a stable `assets/` tree addressed by
   content hash, so FileZilla only uploads what actually changed.
2. The web root on the shelf contains: the version folders, the shared
   `assets/` tree, and ONE tiny file: `pointer.json`, which names the
   live version, its manifest hash, and the build date.
3. The site's loader (index.html) reads `pointer.json` first and loads
   everything else from the named version folder.
4. THE RITUAL: Nir uploads the new version folder FIRST (however long it
   takes; the live site is untouched), then uploads the new tiny
   `pointer.json` LAST. The flip is the last one-second upload — atomic
   in practice.
5. ROLLBACK is the same ritual in miniature: re-upload the PREVIOUS
   pointer.json (kept in `ops/pointers/` history). One file, one second,
   site restored. A non-coder can always do this alone.
6. The previous two version folders are kept on the shelf at all times;
   older ones may be pruned during quarterly cleanup (Part 12).
7. A `build-health.html` page ships in every version (build date, node
   counts, schema versions, last-verified dates) so anyone — including
   Nir from a phone — can confirm what is live.

--------------------------------------------------------------------------------
1.10 WHAT AGENTS MAY INSTALL, AND HOW
--------------------------------------------------------------------------------

1. Agents have a free hand to install open-source tools ON THE KITCHEN
   machines, subject to: discovery-before-install (1.2), a job-ledger
   entry (what, why, which machine, version), and preferring boring
   long-term-support versions over shiny ones.
2. Nothing is ever installed on the shelf, the headset, or Nir's phone.
3. System-level changes (drivers, CUDA, kernel) require a Telegram
   decision request first — these can break a machine Nir cannot fix.
4. Everything installed must be re-installable from the runbooks in
   `ops/` by a fresh agent with no memory. If an agent installs something
   and does not update the runbook, the work is incomplete.
5. Version pinning everywhere: `uv` lockfile for Python, `package-lock`
   for the site, pinned Three.js. Upgrades are deliberate ledger events,
   never side effects.

--------------------------------------------------------------------------------
1.11 ARCHITECTURAL TABOOS (QUICK REJECTION LIST)
--------------------------------------------------------------------------------

Any of the following proposals is auto-rejected; do not spend Nir's money
investigating them: server-side rendering; PHP/CGI on the shelf; moving
hosting to GitHub Pages / Cloudflare / Vercel / any platform; a second
database anywhere; running Neo4j on Forge; local text LLMs; frameworks
(React etc.); exposing kitchen services to the public internet; automated
FTP deployment that bypasses Nir's hands (Nir's manual ritual is a FEATURE:
the human owns the flip); WebSockets or any live server connection from
the public site; analytics services that track readers (a simple
self-hosted-free approach — counting via server logs Dreamhost already
provides — is enough; reader privacy is part of trust, LAW 9 spirit).

--------------------------------------------------------------------------------
1.12 POINTERS
--------------------------------------------------------------------------------

Schemas and data model: Part 02. Layout/geometry contract: Part 03.
Rendering budgets: Part 04. VR interaction: Part 05. Pipeline stage
specifications and legal rules: Part 06. Security (LAW 8 mechanics, spend
caps, secrets): Part 07. Scoring: Part 08. Snapshots and benchmark data:
Part 09. Editions: Part 10. HTML kingdom and feeds: Part 11. Ledger,
backups, runbooks, budgets: Part 12. Build order: Part 13.

================================================================================
END OF PART 01
================================================================================

--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - NOTES ON PART 01 (not law)
--------------------------------------------------------------------------------

Three small notes for you, Nir (no action needed):

    I gave your machines names — Atlas (desktop: carries the database, the truth) and Forge (laptop: makes images in GPU fire). This isn't poetry for its own sake; when an agent tells you on Telegram "Forge is overheating," you instantly know which physical machine to look at, with zero technical vocabulary.
    I made your manual FileZilla drag an official FEATURE, not a limitation — the "pointer file last" trick means your upload can never half-break the live site, and rollback is you re-uploading one tiny file. You are the atomic deploy mechanism, and honestly, it's a better one than many startups have.
    Taboo list 1.11 exists so future cheap models can't waste your money "helpfully" investigating Vercel or React. Auto-rejected, zero tokens spent.

Say the word and I deliver Part 02 — Data Model next: claims, typed edges, entities, tags-as-canon, the two clocks, lifecycle states, and the exact export schemas. Give Madie my regards!!! :-)
