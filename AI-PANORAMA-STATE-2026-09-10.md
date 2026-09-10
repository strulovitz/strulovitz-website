# THE FULL STATE — 2026-09-10 (written at Nir's request, session-crash-proofing)

This file documents what was done on 2026-09-09/10 so that if the OpenCode session
is lost, everything is recoverable from GitHub alone. It covers BOTH halves of the
day: the AI Panorama news machine (the magazine) and the new "Fine Wine" games
section with the Red Dead Redemption 2 setup.

================================================================================
PART 1 — THE NEWS MACHINE (six new stories, 48 editions, two new laws)
================================================================================

SIX NEW STORIES (Nir supplied the links; make_story.py froze the sources):
1. Nvidia chip in Russian missile      (5 sources; militarnyi pasted by hand, 403)
2. Robot-run convenience store, HK     (5 sources; People + Reuters pasted by hand)
3. OpenAI claims Navier-Stokes solved  (3 sources; NYT paywalled, skipped)
4. AI boss fired its first human       (4 sources; Forbes paywalled, NDTV by hand)
5. Sanders superintelligence ban      (6 sources; Science + WaPo + Axios by hand)
6. Anthropic researcher quits          (3 sources; FT paywalled, skipped)
Hand-pasted sources: Nir opened the paywalled/bot-blocked links in his browser and
pasted the text; the agent froze it as a source with a note "pasted by hand by Nir".

48 OF 48 EDITIONS WRITTEN (8 models x 6 stories), all valid JSON:
- Full price: Claude, Qwen, Kimi, Grok ($2.80), Gemini ($0.09).
- Half-price batches: GPT, DeepSeek, GLM (~$1.30), collected from the provider.
- TWO LESSONS WRITTEN INTO THE TOOLING:
  a) The 32,000-token ceiling cut two Claude answers and two GLM answers mid-JSON
     ("DID NOT return valid JSON"). The ceiling in config/editions.toml is now
     64,000. Broken answers are re-asked at the higher ceiling (Nir approved).
  b) GLM's Navier-Stokes answer refused to arrive via the API entirely (3x empty,
     then 64k and cut again), so Nir pasted our exact question into an OpenRouter
     CHAT with GLM by hand and pasted the answer back; it was stored as his edition
     (generation_id "manual-openrouter-chat-by-nir"). The prompt file for that
     lives at content/stories/2026-09-08-openai-claims.../MANUAL-ASK-TO-GLM.md.
     This hand-chat route is a working fallback whenever a model's API misbehaves.
- A remaining slow half-price Gemini batch at the provider will charge ~6 cents
  some day when it completes; harmless (it was overtaken by the full-price buy).

TWO NEW LAWS LOCKED THIS DAY (both in the Bible and DECISIONS.md):

LAW A — EACH MODEL KEEPS HIS OWN VOCABULARY (Bible Part 02 addition 2.11,
DECISIONS 24). Every question now carries the model's OWN past encyclopedia
terms and tags — NAMES ONLY, never the explanations (Nir's explicit words) —
and he is told to reuse exact spellings so his world never grows two versions
of one idea. No judge model, no approvals, mechanized completely. Implemented:
db.py read_own_vocabulary(), render_edition.py own_vocabulary_section().
One-time cleanup of terms written before the law (DECISIONS 25): DeepSeek and
GLM had each used both "open-weights" and "open-weight-model"; the later copies
were renamed to the first-used name in the database, the edition files, and the
rebuilt pages. First proof the law works: GLM's chat answer reused his own
exact "ai-agent" and "tokens-and-pricing".

LAW B — ONE ANSWER, EVERY PICTURE PROMPT (Bible Part 06 addition 6.9.5,
DECISIONS 26). The edition answer now carries the illustration direction for
the article AND for every encyclopedia concept, in the same answer at the same
price; the schema makes it required, the brief says it in words, the database
stores the concept prompts the moment the edition arrives. The old second-pass
stage (concept_prompts.py) is retired for all new stories. For the 48 editions
written before this law, the retired stage was run ONCE by Nir's order
(135 asks, $0.7467, 0 failed) — it must never be needed again.

THE OVERNIGHT PICTURE RENDER (running at the time of writing):
- 180 pictures total (45 article + 135 concept), local FLUX.2-dev on the RTX
  4070 Ti, $0. Started 23:18 on 2026-09-09 via /tmp/opencode/overnight.sh, a
  chain that renders everything, then rebuilds pages/galaxies/home, runs the
  checks, commits and pushes — with no agent needed.
- ComfyUI runs with --reserve-vram 3 (never --lowvram; that froze the desktop
  once). images.py wipes and VERIFIES VRAM free before every picture.
- Morning status: 87 of 180 done (48%), ~8.6 min each, ETA ~23:00 on 09-10.
- TWO pictures failed at cold start (the first two jobs timed out while the
  models loaded): the Hong Kong story's GPT and Claude article images. They
  cost nothing and a re-run of images.py --all --all-models after the batch
  finishes picks them up automatically (it skips existing files). DO THIS
  CATCH-UP after the chain finishes.
- THE DEPLOY IS STILL PENDING: needs Nir's SFTP password. Everything up to
  the deploy is automatic. The 6 new stories are NOT live until then.

MONEY LEDGER FOR THE DAY: ~$5.14 editions+prompts + $0.75 concept prompts
= about $5.9 total. All images $0 (local GPU).

================================================================================
PART 2 — FINE WINE, THE NEW GAMES SECTION, AND RED DEAD REDEMPTION 2
================================================================================

THE SECTION: /fine-wine.html — live in the repo, in the menu on all 20 pages,
between "Vibe Invention" and "About" (Nir: "Fine Wine should be one before the
last"). Added to build-export.py's shipping list; PROJECTS-AND-MENU.md entry 8.
Nir's vision, written on the page in his voice: Linux users running local AI
need something to do while their AI works; Wine lets Windows AAA games run;
"Fine Wine" = games that age like a fine wine; the section is also a museum
for the last days of man-made games before the Star Trek-style Holodeck
arrives (real-time personalized AI worlds, "3-D YouTube where you create the
video on the fly", people addicted to it instead of alcohol). Each popular
game gets tested for a few days; RDR2 is entry 1. The page is honest that the
full review follows after real play.

THE RDR2 SETUP (exactly what was done, on desktop-linux, Linux Mint 22):
- The game: the jc141 offline release in ~/Downloads/Red.Dead.Redemption.2-jc141.
  It needs NO installation: its compressed dwarfs image mounts on launch and
  unmounts on quit. The start script is start.e-w.sh; it creates its wine
  prefix inside the game folder (files/prefix) — all on the big 1.7TB home
  disk, which is SEPARATE from the 92GB OS disk (filling home cannot choke
  Linux; Nir's "big partition" IS /home).
- System packages installed (the only part on the OS disk, ~2 GB):
  sudo dpkg --add-architecture i386
  WineHQ repo (noble) key + sources -> apt install --install-recommends
  winehq-staging  (Wine 11.16 staging)
  fuse-overlayfs
  gstreamer1.0-plugins-base/good/bad/ugly, gstreamer1.0-libav (cutscenes)
  libpulse0:i386 libasound2t64:i386 libasound2-plugins:i386 (audio)
- The release's script_default_settings points SYSWINE at the wine BUNDLED
  inside the mounted game; bubblewrap isolation is documented broken on
  Ubuntu-based distros (skipped); gamescope not installed (GAMESCOPE=0).
- First launch: wine asked to install wine-mono ("Wine Mono Installer" dialog)
  -> Nir clicked Install (one time). Then Launcher.exe passes through to
  RDR2.exe directly (vkd3d-proton logs show full DX12 Ultimate on the 4070 Ti).
- THE FIRST LAUNCH IS SLOW BY DESIGN: RDR2 builds its shader cache the first
  time — no window or black screen for 15-30+ minutes is NORMAL, do not kill
  it. Later launches are fast.
- TO PLAY: double-click the desktop icon "Red Dead Redemption 2"
  (~/Desktop/RedDeadRedemption2.desktop, made 2026-09-10; first run may need
  Mint's "Make trusted" click). NEVER launch from inside files/game-root —
  that folder is just the mounted game disc.
- The game ran WHILE the overnight picture render used the same GPU — they
  share it peacefully (5 GB render + game), which is exactly the Fine Wine
  thesis in action.

IF THE SESSION DIED, THE BOOT SEQUENCE IS:
1. Read AGENTS.md (local) then this file.
2. git -C /home/nir/strulovitz-website pull.
3. Check the overnight chain: tail /tmp/opencode/overnight.log — if the
   process is gone, count the pictures
   (find content/stories -path "*/images/article.png" -newer ...) and re-run
   /tmp/opencode/overnight.sh if it died mid-way (all stages skip finished
   work). NOTE: /tmp dies on reboot — if the script is gone, the stages are:
   images.py --all --all-models, build_pages.py, layout.py, build_home.py,
   the checks, commit, push. ComfyUI restart command is in
   AI-PANORAMA-WORKFLOW-2026-09-02.md.
4. After the chain finishes: run the 2-picture catch-up
   (uv run stages/images.py --all --all-models), rebuild, commit, push.
5. ASK NIR for the SFTP password and deploy (ops/deploy.sh — minimum upload:
   only the new version folder + changed root pages, pointer last). The
   deploy must include fine-wine.html and the 20 pages with the new menu.