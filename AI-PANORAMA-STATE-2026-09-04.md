# AI PANORAMA — THE FULL STATE — 2026-09-04 (night)

This is the file to read first when picking this project up. It supersedes
AI-PANORAMA-STATE-2026-09-03.md for current state (that file stays for its
reasoning and for the detailed history of the LAW 5 fix day).

## THE ONE-LINE SITUATION

Version v2026-09-04-a IS LIVE at www.strulovitz.org — Madie's home-page
changes verified live by Nir — but Nir has NOT YET SEEN the galaxy's new
pictures, almost certainly because of a broken edition-button link on the
home page (found and diagnosed, fix is tomorrow's first job). Also: Nir's
SFTP password was pasted in chat AGAIN (second time) and MUST be changed.

## WHO IS WHO

- Nir: the owner, editor-in-chief, final authority. Plain language only.
- Madie: Nir's girlfriend — her first design request (the home-page text
  changes) was implemented and is live. Her headset comfort rating is
  legally binding on the project (bible/part-05.md 5.10, "Madie counts").
- GLM 5.3: the working agent, Nir's pick to replace Claude Sonnet 5. It is
  served through OpenRouter — when Nir's OpenRouter credits ran out
  (2026-09-04 night), the agent's replies simply died mid-sentence until
  he bought more. Replacement order after GLM 5.3: Qwen 3.8 Max, then
  DeepSeek V4 Pro, then GPT-5.6 Terra.
- The Bible (bible/part-00..13): THE LAW. LAW 10: conflicts go to Nir.

## WHAT HAPPENED ON 2026-09-04, IN ORDER

### 1. The overnight render finished perfectly
All 120 concept illustrations: 120/120 rendered, 0 failed, 799.2 minutes
(08:43:11 -> 22:02:23), $0 local. Verified on disk: exactly 120.

### 2. The rebuild + one real bug caught in my own work
- Rebuilt: build_pages.py (idea pages embed each take's picture), layout.py
  (ships idea thumbs to site/data/idea-thumbs/, 119 of them), build_home.py.
- BUG I CAUGHT MYSELF: my first idea-page image naming used the story slug
  only, so eight models' pictures for the same idea OVERWOTE each other
  (GLM's page could have shown Qwen's picture). Fixed: images named
  <story>--<model>.png, verified 1:1 with the 120 jobs, stale 49 files
  removed. Rule now written in code: an edition's picture can never
  overwrite another edition's picture.
- All 113 checks pass; zero console errors on real content; concept thumb
  and full-size concept image verified over HTTP locally.

### 3. Everything pushed, then Madie's request
Madie asked (through Nir) for home-page text changes, applied to ALL 7
home-page versions (index.html + 6 model variants):
- The tsunami line "AI is like a tsunami wave 🌊 Strulovitz let you surf it
  instead of drowning 🛟" a LITTLE bigger than normal (1.25rem).
- The old combined line replaced by two lines:
  - normal size: "enjoy my revolutionary projects, scroll down for news,"
  - BIG BOLD below it: "or learn more in the "about" page!" with the link
    visible, bold and big.
All 113 checks pass; committed; pushed.

### 4. THE DEPLOY (Nir handed the SFTP credentials in chat - burned again)
Nir pasted host/user/password in chat (second time; first was 2026-08-21).
THE PASSWORD MUST BE CHANGED ON DREAMHOST - it is in the session log.
The deploy itself went perfectly:
- python3 ops/build-export.py -> version v2026-09-04-a, 498 files, 285MB.
- ops/deploy.sh (fed the confirmation and password on stdin): step 1 the
  versioned folder, step 2 root index.html + night-watch.html, step 3
  pointer.json LAST. ~4 minutes total. PUBLISHED.
- Verified LIVE over the real internet: Madie's three text changes on the
  live home page; 8 editions' galaxies index; a full reading page with its
  1.4MB picture; an idea page with its 1.4MB concept picture; the dimmed
  tesseract (0.48/0.47/0.40 colours live in src/vr/panorama.js); concept
  thumbnails serving. Everything under https://www.strulovitz.org/v2026-09-04-a/.
- Ledger entry written; pointer archived (ops/pointers/pointer-v2026-09-04-a.json)
  for the one-command rollback.

### 5. Nir's feedback + the found culprit
Nir: "i saw the changes that Madie asked for" ✅ "but i did not see the
changes that we made like with the pictures and so on."
Diagnosis started the same night:
- The root /tesseract.html is a 404 (good - no stale root galaxy).
- The home page's main entry buttons correctly point to
  v2026-09-04-a/tesseract.html.
- BUT the home page also contains links of the form
  "tesseract.html?edition=openai--gpt-5.6-terra" - RELATIVE links that
  resolve against the ROOT, where the file does not exist -> 404. These
  are the comparison-table edition buttons (and any other relative
  tesseract links) in build_home.py's generated section. If Nir clicked
  one, he landed on a dead page instead of the galaxy with pictures.
- The OTHER candidate explanation, to confirm with him tomorrow: he may
  have only looked at the home page, where the pictures do not appear -
  they live in the GALAXY (hover a node: card + picture; click/trigger:
  full reading page with the full-size picture).
- ALSO NOTE: he may have entered the galaxy and seen the DEFAULT view -
  the slab starts at the busiest band (the encyclopedia, w=+0.7), where
  hovering shows concept cards - which DO have pictures now, but story
  pictures need the slab swum toward the news band (hold S).

## THE SITUATION RIGHT NOW

- LIVE: v2026-09-04-a (everything: Madie's text, dimmed tesseract, reading
  pages, 160 illustrations on every node, hover pictures, VR panel).
- Nir's OpenRouter credits were topped up; the agent works again.
- Nir's SFTP password is burned (in chat, 2026-09-04) - CHANGE IT.
- Working tree clean, everything pushed through commit 2a5790c.

## WHAT STILL NEEDS TO BE DONE, IN ORDER

1. NIRMUST CHANGE THE DREAMHOST SFTP PASSWORD (top priority, security).
2. TOMORROW, FIRST: ask Nir exactly HOW he looked for the pictures, then:
   a. Fix the broken relative tesseract.html?edition=... links in
      build_home.py so every entry point points INTO the live version
      folder (read pointer.json's live version like the entry buttons do,
      or generate absolute versioned paths). Then rebuild home + redeploy.
   b. Walk Nir (and Madie!) into the galaxy the RIGHT way: from the home
      page's "Enter" buttons -> v2026-09-04-a/tesseract.html -> hover a
      story node (swim toward news with S if needed) -> picture on the
      card -> click opens the reading page with the full-size picture.
3. NIR'S HEADSET SESSION (bible/part-05.md 5.10, the human half): hover
   card with picture, trigger-twice reading panel, thumbstick scroll, B
   close, comfort 4+. Madie counts as one of the five sessions.
4. THE UNANSWERED DESIGN QUESTION: mesh vs stem (three options explained
   to Nir 2026-09-03, simple words; he has NOT chosen). Ask; never pick.
5. KNOWN SMALL POLISH: the reading panel's compositor-layer ideal
   (currently the Bible-sanctioned in-scene quad fallback); hover-card
   fade with rotation motion (parked-questions suggestion); the galaxy
   idea-node hover thumb shows the FIRST take's picture (the idea's own
   page shows all takes) - acceptable, documented.
6. MILESTONE 1 LEFTOVERS (older): perftest at 72fps on the physical
   Quest; five human validation sessions; audio + haptic w-cues; ego mode
   and the path trail.
7. THE BIGGER ROADMAP (bible/part-13): the claims pipeline (Milestones
   2-3, nothing built - editions were written straight from frozen
   sources), comparison scenes (Milestone 4), image-mode switching
   (Milestone 5), monthly issue machinery (Milestone 7), ops hardening
   (Milestone 8: restore drills, vacation mode, validator completion).
   New stories: content/inbox.txt -> make_story -> render_edition (both
   write through to the database now) -> concept_prompts -> images ->
   build_pages/layout/build_home -> deploy.

## MONEY LEDGER (2026-09-03 + 2026-09-04)

- Concept prompts: $0.5464 (120 asks, approved in advance, estimate held).
- Everything else: $0 (local GPU renders, all code, the deploy).
- Nir topped up OpenRouter credits on 2026-09-04 night after the agent
  went silent mid-reply (that is what "no credits" looks like from the
  agent side: the reply just dies).

## THE STANDING RULES (never forget; each one cost something real)

- Real numbers always; never "check back on my own" (agents run only when
  prompted - say so honestly); report the moment anything finishes,
  crashes, or stalls; never call a failing job reasonable; correct wrong
  docs directly, never "superseded" notes; never claim unverified things
  as fact; ask before spending money, report exact numbers after.
- Emojis every message, every line, even mid-apology. His name is Nir.
- One door to the database: pipeline/lib/db.py. Files are exports (LAW 5).
- Never reorder a model's own choices; order is editorial voice.
- ComfyUI here: --reserve-vram 3, never --lowvram (no-op on 0.28.0).
- Long jobs: background with live progress printing, real status on ask.
- The SFTP password: at the keyboard only. Nir has now pasted it twice
  (2026-08-21, 2026-09-04); both must be changed; never write it in a file.
- AGENTS.md (agents' memory, /home/nir/AGENTS.md) is LOCAL ONLY, never pushed.
- Madie's design opinions are treasured requests. :-)

## SESSION LEDGER

- c571eb1  120 concept pictures + thumbs + metas, idea pages rebuilt, fix
- a8b3d36  Madie's home-page changes in all 7 versions
- 2a5790c  deploy of v2026-09-04-a recorded, pointer archived
- LIVE     v2026-09-04-a at www.strulovitz.org (rollback: re-upload the
           pointer from ops/pointers/, one file, one minute)
