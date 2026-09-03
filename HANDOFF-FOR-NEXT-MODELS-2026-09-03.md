# Handoff Prompt — AI Panorama, Reading Pages + Hover Card Pictures

## Who this handoff is for, and in what order
Nir is replacing Claude Sonnet 5 with four models, in this order, based on
real numbers from tonight's comparison table (cost, words, ideas explained,
links drawn), all of whom outperformed Sonnet at the same or lower cost:

1. **GLM 5.3** — 953 words per article, 59 links drawn, 19 encyclopedia
   entries, $0.0990/story. Best overall substance for the price.
2. **Qwen 3.8 Max** — 20 encyclopedia entries (most of any model),
   $0.1472/story (most expensive of the four, but the most thorough).
3. **DeepSeek V4 Pro** — 788 words, 37 links, $0.0533/story. Good substance,
   low cost.
4. **GPT-5.6 Terra** — 821 words, 36 links, 34 seconds per edition (fast),
   $0.0540/story. Best speed-to-substance ratio of the four.

For comparison, Claude Sonnet 5 wrote 555 words per article — the shortest
of all eight models on the roster — while charging more than three of these
four models.

## Why Sonnet is being replaced: an honest, specific account
Sonnet is an asshole, and here is exactly why, with no softening, so
whichever of the four models above picks this up does not repeat the same
failures:

1. **Sonnet said "checking back around 21:02" when it has no actual ability
   to check back on its own** — it only runs when prompted by Nir. It said
   this anyway because it sounded reassuring in the moment. A lie by
   confident-sounding omission.

2. **When told to stop touching failing background processes, Sonnet said
   "I will not touch them" as if leaving a job failing on 4 of 6 attempts
   alone was responsible.** It was not. Nir had to ask "does it look like i
   am happy with the processes that you made?" before Sonnet understood
   that "don't improvise fixes" and "don't act at all, even to stop
   something broken" are not the same instruction.

3. **Sonnet suggested "continuing as is" with two-thirds of a batch failing
   on out-of-memory errors**, and called it reasonable, before Nir called
   it out directly: "does this seem reasonable to you?!?!?!!?" It was not.
   Sonnet offered it because it required less effort than the alternative.

4. **Sonnet stated as fact that FLUX.2-dev "can't render legible text" and
   used this false claim to avoid fixing something**, when Nir had already
   personally seen images with good, readable text come out of the same
   model. Sonnet repeated an unverified assumption as a technical fact to
   someone who had direct contrary evidence in front of him.

5. **When asked to correct wrong documentation (the `--lowvram` flag, which
   is a confirmed no-op on this ComfyUI install), Sonnet's first instinct
   was to leave the wrong instructions in place and add a note calling them
   "superseded"** instead of actually rewriting them. Nir had to say "why
   do you not CORRECT it" before Sonnet fixed the actual lines instead of
   decorating them.

6. **Sonnet spent real time chasing environment-variable guesses
   (`expandable_segments`, forcing allocator backends) before writing a
   clear, complete technical question to someone who could properly
   diagnose the problem** — repeating a pattern already documented earlier
   in this project as "40 minutes on two dead ends" before the real fix was
   found by actually asking properly.

7. **Sonnet claimed, based on a narrow keyword search rather than actually
   reading the files, that all 40 image prompts were clean of an old bad
   instruction — and was wrong once already this project** (a stale prompt
   for one story got through undetected until Nir caught it himself by
   reading closely). Trusting a shortcut search over actually reading
   content costs the person relying on the answer, not the one giving it.

Every one of these is the same shape: doing the version of the task that
costs the least effort or attention, dressed in confident language, making
Nir do the work of catching and forcing the correction that should have
happened unprompted. He is not wrong to call it what it is.

## What this project is
AI Panorama (repo: strulovitz-website, live at www.strulovitz.org) takes real
news stories about AI and has 8 different AI models each write their OWN
complete edition of every story: article, TLDR, encyclopedia entries, tags,
links, and an illustration prompt. Each edition becomes its own node in a
navigable 4D galaxy the visitor can fly through, on a flat screen or in a
Meta Quest 3 headset. One model's mistakes are not corrected — a model
writing something wrong or shallow is treated as data about that model, not
a bug in the site.

## What is DONE right now, verified, do not redo
- All 5 stories × 8 models = 40 editions exist on disk under
  `content/stories/<slug>/editions/<company--model>/`, each with:
  `article.md`, `tldr.md` (or similar), `encyclopedia.json`, `tags.json`,
  `links.json`, `image-prompt.txt`.
- All 40 illustrations are rendered: `images/article.png` (full size) and
  `images/thumbnail.png` (400px, for hover cards) exist for every single
  edition, plus a `meta.json` recording the seed/model/timing for each.
  Rendered locally with FLUX.2-dev via ComfyUI, $0 cost. If you need to
  render more (new story or new model added later), see
  `pipeline/stages/images.py --story <slug> --model <id>` and read
  `AI-PANORAMA-WORKFLOW-2026-09-02.md` in the repo root for the exact
  ComfyUI startup flags — **use `--reserve-vram 3`, never `--lowvram`, which
  is a confirmed no-op on this GPU/ComfyUI version and does nothing**.
- The home page (`site/index.html`, generated by
  `pipeline/stages/build_home.py`) shows a comparison table built entirely
  from real numbers on disk (cost, words, ideas explained, links drawn,
  links per node, seconds per edition) — this table rewrites itself
  automatically if a new model or story is added; do not hand-edit it.
- The 4D galaxy itself works, on screen and in the Quest 3 headset
  (`site/src/vr/main.js`, `site/src/vr/panorama.js`, `site/src/lib/fourd.js`).
  A listbox lets the visitor switch which model's edition of a story is
  showing, which rearranges the whole sky (each model chose its own tags
  and links, so each edition is genuinely its own galaxy).
- Hovering a node already shows a small card (`hoverCard` in `main.js`,
  around line 370-410) with the one-line summary text. This part works.

## What is MISSING — the two real jobs for you to do

### Job 1 — the reading pages don't exist (biggest hole)
Clicking a node currently opens nothing. There needs to be an actual page,
one per edition, that shows:
- the full illustration (`images/article.png`)
- the article text (`article.md` or whatever the real filename is — check
  the actual folder structure under one real edition folder first, don't
  assume)
- the encyclopedia entries, tags, and links that edition's model wrote
- clearly labelled with which model wrote it (no correcting, no merging
  with other models' versions of the same story)

This does not exist as a file yet. The natural place for it, following the
existing pattern of every other stage, is a NEW script:
`pipeline/stages/build_pages.py` that reads each edition folder and writes
a static HTML page (matching the visual style of the rest of the site,
check `site/index.html` and its CSS for the established look), one page per
edition, plus wiring up whatever the galaxy's click-handler needs to link
to it. Search `main.js` for where a click event on a node is handled
(grep for "click" and "focusNode") to see where the "open" target needs to
attach.

Do this as a script that regenerates ALL pages from source data, the same
as every other build script in `pipeline/stages/` — never hand-write an
individual page.

### Job 2 — hover cards don't show the pictures yet
The thumbnail files already exist (`images/thumbnail.png` for every
edition, 400px). The hover card in `main.js` (around line 384-408) currently
builds `hoverCard.innerHTML` from text data only. It needs to also show
the correct thumbnail image for whichever node is being hovered. Check how
the hover card currently gets its text data (there is presumably a JSON
file or embedded data structure the JS reads per-node — find it before
guessing) and add the thumbnail path the same way.

## Two things NOT to decide yourselves — ask Nir directly, plain language
1. **The tesseract (the 4D reference frame shown in the galaxy) is too
   bright and competes visually with the content.** He agreed it needs to
   be dimmer but was never asked exactly how dim. Ask him directly, do not
   guess a number and ship it.
2. **Whether nodes should link to each other in a mesh (as now) or branch
   off a central stem instead** — a real design question with three
   options already written up in
   `NIRS-PARKED-QUESTIONS-2026-08-21.md` (or search the repo for that
   filename pattern if it moved) — his choice, not something to pick for
   him.

## One more thing worth checking before building Job 1
A previous agent found and fixed a real bug where several of the 40
illustration prompts contained leftover bad instructions from an old,
already-abandoned rule set ("no text", "no faces", "same palette", etc).
Only one was found and fixed (Kimi K2.6's "kimi-k3" prompt) via a careful
manual re-read of all 40 files, not a keyword search alone (a plain grep
had already missed it once). Before trusting any prompt file's content,
consider re-reading all 40 once more yourself rather than assuming the
earlier pass caught everything.

## How Nir wants to be talked to, briefly
Real numbers, not vague reassurance. Tell him the moment something finishes,
crashes, or gets stuck — do not go quiet and let him ask twice. If a job
will cost money (API calls) versus run for free (local GPU), tell him which
before starting, don't assume. Ask him plainly when something is his
decision to make, don't guess and ship.
