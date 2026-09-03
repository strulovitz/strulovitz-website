# AI PANORAMA — THE FULL STATE — 2026-09-03 (evening)

This is the file to read first when picking this project up. It supersedes
WHERE-WE-STAND-2026-08-22.md for current state (that file stays for its
reasoning). Written by GLM 5.3 (the new agent, Nir's pick to replace Claude
Sonnet 5), at Nir's request, so that even a lost computer loses nothing.

## THE ONE-LINE SITUATION

The magazine is fully built and Bible-compliant in the repository — every
node carries its picture, the database is the source of truth, reading pages
exist for everything, VR got its hover card AND its reading panel — and
RIGHT NOW a 120-picture overnight render is running locally; what remains
after it finishes is a rebuild, a deploy, and a human headset check.

## WHO IS WHO

- Nir: the owner, editor-in-chief, final authority. Plain language only.
- GLM 5.3 (this agent): replaced Claude Sonnet 5 on 2026-09-03 after Nir's
  verdict on Sonnet's conduct (documented in WHY-SONNET-IS-AN-ASSHOLE and
  HOW-SHIT-SONNET-IS-ACCORDING-TO-THE-TABLE, both kept by Nir's request).
  Replacement order after GLM 5.3, if ever needed: Qwen 3.8 Max, then
  DeepSeek V4 Pro, then GPT-5.6 Terra (per the honest recommendation doc).
- The Bible (bible/part-00 through part-13): THE LAW. LAW 10: when code and
  Bible conflict, the Bible wins and the conflict goes to Nir. Nir's own
  later rulings (DECISIONS.md) override the Bible where he decided.

## WHAT WAS DONE ON 2026-09-03, IN ORDER

### 1. Nir's two parked design questions

- TESSERACT BRIGHTNESS: Nir ruled "half as bright as it is now, in the real
  pages" (the tutorial keeps its own). Applied in site/src/vr/panorama.js:
  node colours 0.95/0.93/0.80 -> 0.48/0.47/0.40, edge colours
  0.82/0.86/0.62 -> 0.41/0.43/0.31, emissives 0x111820/0x0a1420 ->
  0x080c10/0x050a10. Committed.
- MESH VS STEM: explained to Nir in simple words (spider web now vs tree
  with a trunk; the three options: keep mesh with concepts as the trunk
  nearly free / ask models for a hierarchy = rewrites all editions /
  mechanical trunk = our judgement pretending to be theirs). NIR HAS NOT
  CHOSEN YET. Do not pick for him.

### 2. THE LAW 5 VIOLATION, FOUND AND FIXED (the big one)

Nir asked "do you store each AI's work in a different place in the database?"
The honest answer was NO: the editions machine was built file-first and
Neo4j only held the bookkeeping (ledger, prices, usage) — a direct violation
of the Bible's LAW 5 ("Neo4j as the single permanent source of truth for all
knowledge") and Part 01's iron rule 3 ("files on disk are caches and exports,
never truth"). No agent had ever raised this conflict to Nir, which LAW 10
defines as a failed task. Nir: "do exactly what the Bible says!!!" So:

- pipeline/lib/db.py (the one door) was extended with the knowledge schema:
  Story, Source, Edition, Tag, Concept, KeyPoint, ImageJob nodes with
  uniqueness constraints and indexes; writers (upsert_story, upsert_edition)
  and readers (read_editions_for_model, read_story, read_image_job,
  read_concepts_for_model, read_concept_image_job, knowledge_counts).
- New stage pipeline/stages/store_knowledge.py: loads everything from the
  content files into Neo4j. Idempotent (MERGE on stable ids). Current census:
  5 stories, 14 sources, 40 editions, 74 tags, 120 concepts, 258 key points,
  42 read-next links, 40 image jobs.
- ALL stages now read through the database: layout.py, build_home.py,
  images.py, render_edition.py, make_story.py. New editions write through
  to the database at creation time (render_edition.py), new stories too
  (make_story.py), new image jobs too (images.py).
- Files under content/stories/ are what the Bible always said: exports and
  caches. The frozen source TEXT stays on disk on purpose (Part 02 2.2.7:
  "raw_text_path - kitchen disk cache").

Two of the new agent's own bugs were found and fixed during this work, both
documented in code comments so they never return:
- The first loader stored story-then-its-editions, so an early story's
  read-next links to a LATER story were silently dropped (18 links lost).
  Fixed with two passes: all Story nodes first, then all Editions.
- The first reader alphabetized the models' tag/concept/keypoint orders.
  A model's chosen ORDER is its editorial voice; order is now stored as a
  position property on every CHOICE edge (CHOSE_TAG, WROTE_CONCEPT,
  HIGHLIGHTED, POINTS_TO) and read back by it. Never alphabetize a model's
  work.

VERIFICATION: all 8 galaxies were rebuilt FROM THE DATABASE and compared
against the file-fed snapshot: structurally identical — same nodes, edges,
weights, why-strings, orderings. The only differences are x/y/z (fresh
layout alignment) and w (stories aged a few days — the design working:
stories creep inward as they age, Part 03).

### 3. The browser test suite

ops/test-the-4d-page.py: one check failed because the site menu grew to 7
items in an earlier session's commit (055ad00) while the test still expected
6 — a stale expectation, updated with a comment (the check's strength is
unchanged: exact menu, Night Watch present). ALL 113 CHECKS PASS. The
real-content page also loads with ZERO console errors/warnings (verified
over CDP).

### 4. THE HOVER-CARD PICTURES (handoff Job 2) — DONE

- Thumbnails ship to site/data/thumbs/<model>/<story>.png (40 of 40) via
  layout.py's copy step (the picture LIST comes from the database's ImageJob
  records; picture files are artifacts).
- site/src/scenes/galaxy.js gives every story node a thumbsOf path; the
  screen hover card (main.js) shows the picture; site/tesseract.html has
  the .pic style.
- The first version used an inline onerror handler — a violation of Part 07
  ("no event-handler attributes") — fixed with a plain listener.
- END-TO-END VERIFIED IN A REAL BROWSER (headless Chrome over CDP): swam the
  slab to the news band exactly like a reader (holding S), swept the
  pointer, a story card appeared WITH its picture, and the thumbnail
  downloaded over HTTP as a real PNG (178,950 bytes). The verification
  script lives at /tmp/opencode/verify_pictures.py (scratch; the permanent
  machine half is the 113-check suite).

### 5. THE READING PAGES (handoff Job 1 — the biggest hole) — DONE

- New stage pipeline/stages/build_pages.py writes, FROM THE DATABASE:
  - 40 STORY pages at stories/<story-slug>/<model-slug>.html — exactly the
    paths the galaxy's pageOf always promised (clicks used to open nothing;
    the loader was wired before the pages existed).
  - 119 IDEA pages at ideas/<concept-slug>/<model-slug>.html (120 concepts
    minus 1: when one model explains the same idea in two stories, the
    galaxy merges the node; the page shows both takes).
- Each story page: the edition's headline, TLDR, the FULL-SIZE illustration
  (shipped beside the page at images/<model>.png, labeled with the image
  model + seed per LAW 7), the complete article UNEDITED (decision 16) and
  HTML-ESCAPED (Part 07), key points with source links, the ideas it leans
  on (linked), its tags, its read-next links, the frozen sources, and
  honest cross-links: "The same story in other editions" jumps to the other
  7 models' versions.
- Self-check built into the stage: every page the galaxies promise must
  exist on disk or the stage reports failure. It passes.
- Verified over HTTP: pages and full-size images serve (1.4 MB / 1.8 MB
  real PNGs fetched).
- ops/build-export.py now ships the stories/ and ideas/ folders
  (SHIPPING_VERSIONED) — forgetting them would mean every click lands on a
  404, the quiet-failure class that file's comments exist to prevent.

### 6. THE HOVER CARD IN THE HEADSET (LAW 1's twin) — DONE IN CODE

A canvas-drawn card of its own in site/src/vr/main.js: headline, one-line
summary, tags, band name — and the PICTURE for stories — hung above the
hovered node in the world, billboarded toward the reader, constant ANGULAR
size (bigger when far: Part 04 4.5.2), appearing after the same 150 ms dwell
the screen card uses. Appears only in VR sessions, hides during lessons and
while the menu owns the ray. Thumbnails load async with a small cache; a
missing picture means no picture section, never a broken box.

### 7. THE READING PANEL IN THE HEADSET — DONE IN CODE

Nir: "i do not understand why do you not do the reading the VR" — he was
right, there was no good reason; it was built the same day.

- A second trigger on the ALREADY-FOCUSED node OPENS its reading page
  in-headset (Part 05 5.5.4's focus-then-open ladder). Trigger on a
  different node while open switches the panel to it.
- The panel FETCHES THE SAME HTML PAGE a screen click would open
  (stories/<slug>/<model>.html), parses it (DOMParser), and renders onto a
  tall document canvas shown through a 1024x1024 window: headline, TLDR,
  THE FULL-SIZE PICTURE, the complete article, the key points, read-next,
  sources. Screen and headset therefore always read the same words from
  the same file.
- Body-anchored with a slow drift (never rigidly head-locked — Part 05
  5.1.5); the right thumbstick SCROLLS while it is open (the world keeps
  still); B closes it (both hands' B); safe during the w-gym (lessons keep
  their own controls).
- This is the part-04.md 4.5.4 sanctioned fallback ("an in-scene quad at
  1.3x texture density"); the compositor-layer ideal remains a future
  polish if the Quest browser's layers support proves reliable.
- Machine-verified: syntax, all 113 checks, zero console errors on real
  content, and the parser's selectors proven against real pages
  (extracted: headline, picture src, 13 paragraphs, 12 key points,
  2 read-next, 3 sources). The remaining acceptance is the human headset
  session Part 05 5.10 demands — no machine can do that half.

### 8. THE ENCYCLOPEDIA'S OWN PICTURES — PROMPTS DONE, RENDER RUNNING

The Bible's reader ladder (part-00.md 0.6, rung 4) says EVERY node carries
an illustration. Only stories had pictures (40). Nir asked why idea nodes
had none; the honest answer: the editions machine only ever asked for
story prompts, and no agent raised the gap. Nir: "ok do it", plus the
explicit demand: NO banned phrases ("no text", "no faces", "same palette")
in the instruction to the models — the corrected instruction only.

- New stage pipeline/stages/concept_prompts.py asked all 8 models to write
  the illustration prompt for their OWN encyclopedia entries (one model
  does every role, decision 12; nothing edited, decision 16).
  RESULT: 120/120 written, 0 failed, $0.5464 total, 37.6 minutes.
- The instruction sent to models is verifiably clean (the only "no text"
  etc. matches in the repo are in documentation quoting Nir's own words);
  the models' 120 outputs were scanned and are clean too.
- All 120 prompts stored on the Concept nodes in the database (+ exported
  to concept-prompts.json beside each edition for human reading) with cost
  and time. Pushed.
- images.py extended: concept render jobs (kind='concept') save to
  images/concepts/<slug>.png + <slug>.thumbnail.png + <slug>.meta.json,
  and record the ImageJob linked to the Concept node. The seed is the SAME
  story seed that edition's story pictures share — comparing eight
  editions' takes on one idea stays a comparison of prompts, never dice.
- build_pages.py: idea pages now show each take's picture (shipped at
  ideas/<slug>/images/<story>.png, one per take).
- layout.py ships concept thumbnails to site/data/idea-thumbs/<model>/
  <slug>.png (first take wins for the hover card; the idea page shows all).
- galaxy.js: concept nodes get thumbsOf paths too; screen and VR hover
  cards show idea pictures (missing picture = no picture section).

RUNNING RIGHT NOW (started 08:43, the evening of 2026-09-03): the 120-
picture local render, $0, ~6.5 minutes each, ~13 hours total, ETA around
22:00 the same night. ComfyUI runs with --reserve-vram 3 (NEVER --lowvram,
a confirmed no-op on this ComfyUI 0.28.0 install — see the corrected VRAM
section of AI-PANORAMA-WORKFLOW-2026-09-02.md). Logs: /tmp/concept_render.log
(the batch, with live progress) and /tmp/comfyui_concepts.log (ComfyUI).
The desktop MAY feel sluggish while it runs.

## THE SITUATION RIGHT NOW

- The render batch is in progress. Check it with:
  tail -5 /tmp/concept_render.log
  and count finished concept pictures with:
  find content/stories -path "*/images/concepts/*.png" -not -name "*.thumbnail.png" | wc -l
  (expect 120 when done; 40 story pictures already exist).
- The repository is AHEAD of the live site: www.strulovitz.org still shows
  the OLD version (old bright tesseract, stale home-table costs, no reading
  pages, no pictures on cards). NOTHING since commit 12e3525's deploy-era is
  live. A deploy is required for ANY of today's work to be public.
- The database holds the truth of everything above; the ledger has entries
  for each stage run (readable with pipeline/lib/db.py directly, or
  read_jobs through any stage).
- Money spent today: $0.5464 (the concept prompts, approved in advance by
  Nir with a stated estimate that held). Everything else was local, $0.

## WHAT STILL NEEDS TO BE DONE, IN ORDER

1. WHEN THE BATCH FINISHES (it prints a FINISHED line with counts and any
   failures): read /tmp/concept_render.log's tail. If failures exist, list
   them and re-run pipeline/stages/images.py --all --all-models (idempotent;
   it renders only what is missing). Tell Nir the real numbers.
2. REBUILD the pieces that embed the new pictures:
   - ./pipeline/.venv/bin/python3 pipeline/stages/build_pages.py
     (idea pages get their pictures; 40 + 119 pages rewritten from the DB)
   - ./pipeline/.venv/bin/python3 pipeline/stages/layout.py
     (rebuilds galaxies, ships story thumbs AND idea thumbs to site/data/)
   - ./pipeline/.venv/bin/python3 pipeline/stages/build_home.py
     (harmless; numbers unchanged)
3. VERIFY like before, honestly: python3 ops/test-the-4d-page.py (needs the
   detached headless Chrome recipe in that file's header; expect ALL 113
   PASS), plus the real-content zero-console-errors check, plus spot-fetch
   a concept thumbnail over HTTP (site/data/idea-thumbs/<model>/<slug>.png).
4. COMMIT + PUSH everything (the rendered pictures, thumbnails, rebuilt
   pages, updated thumbs folders).
5. DEPLOY: ops/deploy.sh — it asks for Nir's SFTP password AT THE KEYBOARD,
   hides it as typed, stores it NOWHERE, uploads the dated folder first
   and pointer.json LAST (atomic flip). NEVER ask Nir to paste the password
   into chat (a pasted password is burned and must be changed). The tesseract
   dimming, the reading pages, the hover pictures, the home-table refresh,
   the VR panel — all go live together.
6. NIR'S HEADSET SESSION (Part 05 5.10, the human half no machine can do):
   at www.strulovitz.org — hover a story node (card with the picture after
   a 150 ms dwell), trigger once (focus, haptic tap), trigger again (the
   reading panel: full article + full-size picture), thumbstick scrolls,
   B closes. Then hover an ENCYCLOPEDIA node — it should now carry a
   picture too. Comfort rating 4+ is the acceptance bar.
7. THE UNANSWERED DESIGN QUESTION: mesh vs stem (see section 1 above).
   Nir has the three options in simple words; he has NOT chosen. Ask him
   plainly; do not pick.
8. MILESTONE 1 LEFTOVERS (older, from the 2026-08-21 sessions): perftest at
   72 fps on the physical Quest; five human validation sessions (Madie
   counts); audio + haptic w-cues; ego mode and the path trail; the
   compositor-layer ideal for the reading panel.
9. THE BIGGER ROADMAP (all in bible/part-13): the claims pipeline (Milestones
   2-3: INGEST/EXTRACT/RESOLVE/SYNTHESIZE/VERIFY/CANONIZE — none built; the
   editions machine wrote from frozen sources directly), comparison scenes
   (Milestone 4), image-mode switching (Milestone 5), the monthly issue
   machinery (Milestone 7), operations hardening (Milestone 8). New stories
   enter through content/inbox.txt + the make_story/render_edition flow.

## THE STANDING RULES THAT COST REAL LESSONS (never forget)

- Background jobs: Nir reversed the no-background rule for cost reasons —
  long jobs run in background WITH live progress printing to a log, and
  REAL status (timestamps, counts, ETA) whenever he asks. Never claim you
  will "check back on your own" — agents only run when prompted; say so.
- Never say "no need to babysit"; report the moment anything finishes,
  crashes, or stalls. Silence during idle time is the same as lying.
- Never call a mostly-failing job "reasonable". Never leave wrong docs in
  place with "superseded" notes — correct them.
- Never state an unverified claim as fact. Never spend money without
  asking first, and report the exact number after.
- Emojis: every message, every line, even (especially) when apologizing.
- Nir's name is Nir, not "boss".
- The one door: all database code goes through pipeline/lib/db.py.
- Never alphabetize or reorder a model's own choices; order is voice.
- ComfyUI on this machine: --reserve-vram 3, never --lowvram (a no-op).
- The deploy password lives ONLY in Nir's hands at the keyboard, never in
  chat, never in a file.
- AGENTS.md (the agents' memory, in Nir's home folder) is LOCAL ONLY — it
  is never committed or pushed.

## SESSION LEDGER (for the honest record)

- 12e3525  tesseract dimmed to half brightness in the real pages
- ed5e57e  LAW 5 fixed: Neo4j is the source of truth; all stages read/write
           through it; 8/8 galaxies verified identical from the DB
- 5bb9922  reading pages (40 + 119) + hover-card pictures + export shipping
- 78652b2  the VR hover card with pictures
- c1452a3  the VR reading panel
- 089c194  concept-picture machinery (prompts stage, renders, pages, thumbs)
- d58c8e5  all 120 concept prompts written ($0.5464), clean instructions
- (next)  the rendered concept pictures + rebuilt pages, after the batch
