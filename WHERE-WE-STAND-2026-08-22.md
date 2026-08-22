# WHERE THE EDITIONS MACHINE STANDS — 2026-08-22

This file supersedes `HANDOVER-EDITIONS-MACHINE-2026-08-21.md`, which was written
at midnight when the work was unfinished. That file is still worth reading for
the reasoning behind every design choice; this one is the current truth.

Written by Claude Opus 5 on desktop-linux at Nir's request, so that next month —
when there is money again — work resumes without him having to explain anything
to anybody.

**Read in this order:** this file, then `DECISIONS.md` decisions 12 to 20, then
`NIRS-PARKED-QUESTIONS-2026-08-21.md`.

**The git branch is `master`, not `main`.** GitHub links with `/main/` give a 404.

---

## 1. IT IS FINISHED, AND IT IS LIVE

**https://www.strulovitz.org/** — live version `v2026-08-22-b`, published
2026-08-22, verified over the real internet and not merely locally.

Anyone in the world can now read five AI news stories, each written from scratch
**eight separate times over by eight different AI models**, and fly through
**each model's own four-dimensional world** — a world whose shape that model
alone decided, by choosing its own tags and its own links.

Nobody else has published that. Not the eight-fold rewriting, not the
per-editor galaxy, and certainly not the two together.

### The measured totals

| | |
|---|---|
| stories | 5, all chosen by Nir |
| editions | **40 of 40 written**, every one understood the required shape |
| words of article written | 29,994 |
| encyclopedia entries written | 120 |
| illustration prompts written | 38 of 40 |
| illustrations actually rendered | **0** — the biggest gap |
| **total cost of everything** | **$2.8950** |
| cost per story across all eight editions | about **46 cents**, or **23 cents in batch** |

### What the first real comparison shows

| model | $ per story | words per article | ideas explained | links per node | seconds each |
|---|---|---|---|---|---|
| Gemini 3.7 Flash | **0.0098** | 617 | 12 | 1.4 | **19** |
| Kimi K2.6 | 0.0483 | 700 | 12 | 1.5 | 195 |
| DeepSeek V4 Pro | 0.0533 | 788 | 15 | 1.9 | 166 |
| GPT-5.6 Terra | 0.0540 | 821 | 15 | 1.8 | 34 |
| Claude Sonnet 5 | 0.0809 | **555** | **10** | 1.7 | 51 |
| Grok 4.6 | 0.0865 | 807 | 16 | 1.8 | **467** |
| GLM 5.3 | 0.0990 | **953** | 19 | **2.5** | 235 |
| Qwen 3.8 Max | **0.1472** | 755 | **20** | 2.2 | 404 |

Real differences, from identical frozen sources: **GLM wove a world 1.7 times
more densely connected than Gemini's** and wrote nearly twice as many words as
Sonnet. **Grok took 467 seconds to think where Gemini took 19.** **Gemini costs
one cent an edition and is not embarrassed** by company fifteen times the price.
And **Claude Sonnet 5 twice declined to write an illustration prompt at all** —
which is a result about Sonnet, recorded and not patched over.

On the AI-designed-viruses story, **GPT wrote an encyclopedia entry on *DNA
synthesis screening*** — the actual regulatory choke point of the biosecurity
argument — **and Gemini did not.** All eight independently agreed that virus
design has nothing to do with Kimi K3 or Grok 4.6, and drew no link. Unanimous
restraint, which is itself informative.

---

## 2. WHAT A VISITOR SEES

**The home page** carries the eight edition buttons and that comparison table,
with a paragraph above it and a paragraph below it — and **every word of it is
generated from the editions on disk** by `pipeline/stages/build_home.py`. Nothing
is typed. Add a ninth model or a sixth story and the table rewrites itself,
including the sentence underneath that names which model wove the densest world.
This matters because of Nir's standing instruction: *"you Opus will not be with
me in the future!!!"*

**Each world** is entered from those buttons or from the switcher in the top bar
of the 4-D page. Hovering a node gives the headline, the one-line summary, the
tags, and whether it is *a story that happened* or *an explanation written to
last*. **W and S swim the slab** from raw news towards the settled encyclopedia.
Cream-coloured, slightly larger nodes are encyclopedia entries, and an idea
explained by more stories sits deeper towards bedrock, because it earned it. The
floating region names are that model's **own tags** — its own vocabulary.

**In VR** it is the same page: press Enter VR on the Quest 3, or serve it over
https with `./ops/look-at-the-site.sh headset`.

---

## 3. THE MACHINE, FILE BY FILE

### The parts Nir edits, which are deliberately not code
- **`content/inbox.txt`** — where stories come from. Paste links, one story per
  `STORY` heading. Nothing else decides what gets covered.
- **`config/editions.toml`** — the roster. Eight models, one per company, each
  with Nir's own reason in his own words. The site's default face is one line.
- **`config/editorial-brief.md`** — **the most important text in the project.**
  The instructions every model receives, word for word, identically. Change this
  and you change how the whole magazine is written.

### The pipeline
- **`pipeline/lib/llm.py`** — the one door to the AI models. Model names are
  always parameters; every cent is recorded in the ledger; source text is fenced
  as hostile data; secrets are redacted; answers are cached so nothing is bought
  twice; the batch path (half price, 24-hour wait) is implemented and proven.
- **`pipeline/lib/sources.py`** — fetches and freezes news articles
  (`trafilatura`) and YouTube subtitles (`yt-dlp`), with error messages that say
  what to do about each failure.
- **`pipeline/lib/db.py`** — the one door to Neo4j, and the job ledger.
- **`pipeline/stages/make_story.py`** — inbox to frozen evidence. Refuses any
  story with fewer than two working sources.
- **`pipeline/stages/render_edition.py`** — one model does every role for one
  story. Also `--reparse`, which re-reads answers already on disk for nothing.
- **`pipeline/stages/layout.py`** — builds each edition's own galaxy: a force
  layout for x, y, z, a semantic fourth dimension, and the Procrustes alignment
  that stops one edition's own map silently becoming a different map.
- **`pipeline/stages/build_home.py`** — generates the home page's results
  section from the editions themselves.

### The site
- **`site/src/scenes/galaxy.js`** — loads a real galaxy in the exact shape the
  placeholder world used, names regions with the model's own tags, and escapes
  every word a model wrote before it touches the page.
- **`site/src/vr/main.js`**, **`panorama.js`** — both bodies, screen and headset.
  A scene now supplies its own band names and its own home position along the
  fourth dimension, so a reader never arrives to an empty world.
- **`site/index.html`**, **`site/tesseract.html`** — the home page with its
  generated section, and the 4-D page with the edition switcher.

### Publishing
- **`ops/build-export.py`** — builds a dated folder. It now ships `data/` too;
  it did not, and the first export would have gone live with empty worlds.
- **`ops/deploy.sh`** — **one command that publishes.** Asks for the password at
  the keyboard, hides it as you type, stores it nowhere, and uploads in the only
  safe order: the dated folder first, the root pages second, `pointer.json`
  **last**, which is the instant it flips. Rollback is re-uploading an older
  pointer from `ops/pointers/`.

### The tests, which must both pass after any change
- `node site/src/lib/fourd.selftest.js` — **64 checks**
- `python3 ops/test-the-4d-page.py` — **113 checks** in a real browser

---

## 4. EVERY COMMAND

```bash
cd /home/nir/strulovitz-website/pipeline

# ADD STORIES: paste links into content/inbox.txt, then
uv run stages/make_story.py

# WRITE THE EDITIONS. --batch is HALF PRICE with a 24-hour wait; use it.
uv run stages/render_edition.py --all --all-models --batch
uv run lib/llm.py                        # batches in flight; costs nothing

# ADD A MODEL: add a [[model]] block to config/editions.toml, then
uv run stages/render_edition.py --all --model <the new id> --batch

# AFTER ANY NEW EDITION, in this order
uv run stages/layout.py                  # rebuild the galaxies
uv run stages/build_home.py              # rewrite the home page's table

# RE-READ ANSWERS ALREADY ON DISK. Calls nobody, costs nothing.
uv run stages/render_edition.py --all --all-models --reparse

# LOOK AT IT
cd .. && ./ops/look-at-the-site.sh       # http://localhost:8080/
./ops/look-at-the-site.sh headset        # https, for the Quest 3

# PUBLISH
python3 ops/build-export.py && ./ops/deploy.sh
```

---

## 5. WHAT STILL NEEDS DOING, IN ORDER

### Free. No model is called, not one cent.

1. **THE ILLUSTRATIONS.** 38 image prompts written, none rendered. Nir cares
   about the pictures more than almost anything and said so explicitly: *"this is
   very important to me the images."* His decision: **local ComfyUI on this
   desktop's RTX 4070 Ti**, free and unlimited, with **the same image model and
   the same seed for every edition**, so the only difference between editions'
   pictures is how well each model directed the artist. ComfyUI is at
   `/home/nir/ai-art/ComfyUI` with RealVisXL, Juggernaut and ZavyChroma
   checkpoints; **the server is not running and needs starting.** Save each
   picture beside the text it accompanies — he asked for that specifically.
   Stage to write: `pipeline/stages/images.py`.
2. **THE READING PAGES.** Clicking a node opens nothing, because
   `stories/<slug>/<model>.html` does not exist. Each page needs: headline,
   TLDR, picture, article, key points with their source links, the encyclopedia
   entries, tags, every source linked prominently, and the edition switcher.
   **Symmetrical folders — GPT gets no privileged position**; the home page
   merely links to the default model's copy. Stage to write:
   `pipeline/stages/build_pages.py`.
3. **DIM THE TESSERACT.** Nir's parked question 2, and he is right: the white
   frame shouts while his stories whisper. Do not delete it — without it a 4-D
   turn stops being teachable and the lessons depend on it. **Ask him how dim,
   and whether it should fade with motion.** He has not answered that yet.
4. **THE STEM-VERSUS-MESH QUESTION.** Nir's parked question 3, the real design
   question: should nodes hang off a trunk rather than link to each other? Three
   options are written up in `NIRS-PARKED-QUESTIONS-2026-08-21.md`. **Do not pick
   one for him.**
5. **HOVER CARDS IN VR.** In the headset a node highlights and buzzes but says
   nothing readable. Item 3 of the remaining Milestone 1 list.
6. **`run.py`** — the single command that inspects the whole grid, works out
   every missing cell, and fills only those. All the pieces exist; this ties them
   together.
7. **EMBED THE FROZEN SOURCES** into Neo4j's vector index, for private search on
   this machine only. Reader-facing search must use our **own** edition prose
   instead, which we wrote and own. That was Nir's legal reasoning and he is
   right.
8. **THE BENCHMARK GRAPHS.** Decision 14: we invent no benchmark. We take the
   ones the world already publishes — GDPval, SWE-bench and the rest — and let a
   reader combine several into three and four dimensions instead of the
   one-dimensional bar chart everybody else prints. Nothing has been built here
   yet; the price and usage snapshots in `pipeline/snapshots/` are the first real
   data and 419 model proposals are waiting in Neo4j as `(:EntityProposal)` with
   status `pending`. **They must not be bulk-approved without him.**

### Costs money
9. **More stories.** 23 cents each across all eight editions, in batch.
10. **More models**, at the same price per story each.

---

## 6. THINGS THAT WILL BITE THE NEXT AGENT

1. **The branch is `master`.** Links with `/main/` 404.
2. **Nir cannot scroll back in OpenCode on Linux.** ONE SCREEN per message. If
   it is longer, write a file, push it, and give him a `master` link.
3. **NEVER choose something that is his to choose.** He was angry, and right:
   *"what the fuck is 'let me pick', why don't i get to pick?!"* Present the real
   options with real prices and let him decide. Every single choice he then made
   was better than the one I would have made.
4. **He WANTS many design questions, before any building.** *"it's much smarter
   than assuming, working, spending time and money and then me being angry."*
5. **Never a one-off hand-fix.** Everything must be general code in the
   repository: *"you Opus will not be with me in the future!!!"*
6. **NEVER edit a model's output.** Not a typo, not a better sentence, not the
   best of two attempts. Retry only when nothing arrived at all, and record why.
   This is decision 16 and it is the soul of the project.
7. **When a model looks like it failed, check our own code first.** GLM 5.3 wrote
   perfect JSON and `llm.py` threw all five of its editions away unparsed,
   because parsing was gated on having asked for a strict schema. Fixed, and
   rescued from disk for nothing with `--reparse`.
8. **`ops/build-export.py` must ship every folder the browser reads.** It did not
   ship `data/`, and the first export would have gone live showing empty worlds.
   If a new folder of data is ever added, add it to `SHIPPING_VERSIONED`.
9. **`uv run` is required** for anything importing `neo4j`. Bare `python3` fails.
10. **Python buffers output**, so a long run's log looks empty. Use `python -u`
    or watch the files appearing.
11. **A bash tool call that times out can kill the background job it started, or
    leave a stale one running.** A stale `--again` process nearly overwrote the
    GLM editions that had just been rescued. Start long jobs with
    `setsid nohup ... &` and check for strays with `ps aux | grep`.
12. **Chrome caches ES modules hard.** Reload with `ignoreCache: true` over the
    debugging protocol or you will test yesterday's code and believe it.
13. **The placeholder world still exists and still matters.**
    `?world=placeholder` forces it; the 113 checks depend on it and so do the
    lessons when the magazine is empty. Do not delete it.
14. **`openai.com` and `cybernews.com` block our fetcher** (HTTP 403). Some
    sources must be pasted by hand or swapped.

---

## 7. SECURITY, HONESTLY

- **Nir's OpenRouter key was pasted in chat on 2026-08-21** and lives only in
  `.env`, which git cannot touch. To rotate: **create a new key first, give it to
  the agent, and only then delete the old one.** That order, or the machine goes
  dead.
- **The DreamHost SFTP password was pasted in chat on 2026-08-22** and used from
  an environment variable, written to no file. **Nir was told to change it
  immediately afterwards.** `ops/deploy.sh` exists precisely so it never has to
  be pasted into a conversation again.
- **No spending limit is set on the OpenRouter key.** That is the backstop which
  survives our own bugs, and only Nir can set it, on their website. Worth
  mentioning to him once.
- The ledger in Neo4j records every call, its cost and its purpose in plain
  English. `cd pipeline && uv run lib/db.py` shows it and writes nothing.
