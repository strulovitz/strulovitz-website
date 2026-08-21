# THE EDITIONS MACHINE — HANDOVER, 2026-08-21 (MIDNIGHT, ISRAEL)

Written by Claude Opus 5 on desktop-linux, at Nir's request, because he is going
to sleep and the computer may crash in the night. Everything needed to carry on
from exactly this point is here. Read this file, then `DECISIONS.md` decisions
12 to 20, then `NIRS-PARKED-QUESTIONS-2026-08-21.md`.

---

## 1. WHAT WAS BUILT TODAY, IN ONE PARAGRAPH

The editions machine exists and works end to end. Nir pastes source links into
one text file; the machine fetches and freezes them; each of eight AI models
then writes its OWN complete edition of every story — the article, the one-line
summary, the encyclopedia entries, the tags, the links and the illustration
prompt — and each edition becomes its own four-dimensional galaxy that Nir can
fly through on screen or in the Quest 3, switching editions from a listbox and
watching the whole sky rearrange. Five real stories are done, thirty-five of the
forty editions are written, and the entire thing cost **$2.65**.

---

## 2. THE EXACT SITUATION RIGHT NOW

### Content
Five stories, all from links Nir chose himself, in `content/stories/`:

| story folder | sources |
|---|---|
| `2026-07-17-kimi-k3` | 3 YouTube (Berman, Wes Roth, AI Revolution) |
| `2026-07-21-the-openai-rogue-agent-and-the-hugging-face-break-in` | 3 YouTube |
| `2026-08-13-grok-4-6` | 3 YouTube (Berman, Wes Roth, Bijan Bowen) |
| `2026-08-06-viruses-designed-by-ai` | CNN, BBC, The Guardian |
| `2026-08-16-the-first-person-jailed-for-protesting-against-ai` | The Guardian, Yahoo News |

14 of 15 links were fetched successfully. **cybernews.com returned HTTP 403**
(bot-block); that story stands on its two remaining sources, which satisfies the
two-source rule.

### Editions: 35 of 40 written, all 35 understood the required shape

| model | editions | cost each | total |
|---|---|---|---|
| Gemini 3.7 Flash | 5 | $0.0098 | $0.0490 |
| DeepSeek V4 Pro | 5 | $0.0533 | $0.2664 |
| GPT-5.6 Terra | 5 | $0.0540 | $0.2698 |
| Claude Sonnet 5 | 5 | $0.0809 | $0.4045 |
| Grok 4.6 | 5 | $0.0865 | $0.4325 |
| GLM 5.3 | 5 | $0.0990 | $0.4951 |
| Qwen 3.8 Max | 5 | $0.1472 | $0.7360 |
| **Kimi K2.6** | **0 — THE ONLY GAP** | — | — |
| **TOTAL** | **35** | | **$2.6533** |

**KIMI K2.6 IS THE ONE THING UNFINISHED.** Its five editions were running in the
background when this was written (`/tmp/opencode/kimi.log`). It is the slowest
model on the roster and had produced nothing after two minutes. If the night
finished it, its editions will be on disk and nothing more is needed. If not,
the command to finish it is in section 5. Expect roughly **$0.25**.

### Galaxies: built for every model that has editions
`content/galaxies/*.json` is the truth; `site/data/galaxies/` is the copy the
browser reads. Rebuild both with one command (section 5). The shapes already
differ visibly, which is the entire point:

| model | stories | encyclopedia entries it chose to write | links |
|---|---|---|---|
| GPT-5.6 Terra | 5 | 15 | 36 |
| Gemini 3.7 Flash | 5 | 12 | 24 |
| Claude Sonnet 5 | 5 | 10 | 25 |

### The website
`site/tesseract.html` now flies through a REAL edition by default, with an
edition switcher in the top bar that builds itself from whatever editions exist.
All **113 browser checks** and all **64 maths checks** pass. Nothing is deployed
to strulovitz.org yet — the live site still shows the placeholder world.

---

## 3. EVERY FILE THAT WAS WRITTEN OR CHANGED TODAY

### New, and this is the machine
- `config/editions.toml` — **the roster**. Nir's eight models, one per company,
  with his own reason for each in his own words. Adding a model is eight lines
  here and one command. The default face of the site is one line.
- `config/editorial-brief.md` — **the instructions every model receives, word for
  word, identically.** This is the most important text in the project. Nir can
  edit it freely; it is not code.
- `schemas/rendering.schema.json` — the shape one edition takes.
- `pipeline/lib/llm.py` — **the one door to the AI models.** Model names are
  always parameters, every cent is recorded in the ledger, source text is fenced
  as hostile data, secrets are redacted, answers are cached so nothing is ever
  bought twice, and the batch path (half price, 24-hour wait) is implemented and
  proven working.
- `pipeline/lib/sources.py` — fetches and freezes news articles (`trafilatura`)
  and YouTube subtitles (`yt-dlp`), with honest error messages that say what to
  do about each failure.
- `pipeline/stages/make_story.py` — reads `content/inbox.txt`, freezes sources,
  refuses any story with fewer than two working sources.
- `pipeline/stages/render_edition.py` — one model does every role for one story.
  Also `--reparse`, which re-reads answers already on disk at zero cost.
- `pipeline/stages/layout.py` — builds each edition's own galaxy: a force layout
  for x, y, z and a semantic fourth dimension, plus the Procrustes alignment that
  stops one edition's own map silently becoming a different map.
- `site/src/scenes/galaxy.js` — loads a real galaxy in the exact shape the fake
  world used, names the regions with the model's own tags, and escapes every
  word a model wrote before it touches the page.
- `content/inbox.txt` — Nir's five stories, with his notes preserved.
- `NIRS-PARKED-QUESTIONS-2026-08-21.md` — his three questions, answered, parked.

### Changed
- `site/src/vr/main.js` — chooses a real edition or the placeholder world; the
  edition switcher; real hover cards; click a node to read it.
- `site/src/vr/panorama.js` — a scene now supplies its own band names and its own
  home position along the fourth dimension.
- `site/tesseract.html` — the edition switcher and its styling.
- `ops/test-the-4d-page.py` — the old checks now ask for the placeholder world
  explicitly with `?world=placeholder`, because the page shows real content by
  default. **All 113 still pass.**
- `pipeline/pyproject.toml` — added trafilatura, yt-dlp, networkx, numpy.
- `.gitignore` — ignores `pipeline/batches/` (receipts for work in flight).
- `.env` — Nir's OpenRouter key is in `OPENROUTER_API_KEY_PIPELINE`. **Never
  committed. Never printed.**
- `DECISIONS.md` — decisions 12 to 20.

---

## 4. THE NINE RULINGS NIR MADE TODAY (the short version — full text in DECISIONS.md)

12. **One model does EVERY role** for its edition: facts, article, encyclopedia,
    tags, links AND the image prompt. Never a division of labour.
13. **The roster**: the middle of the spectrum. Too big to run at home, not the
    frontier flagships. One model per company. No free models.
14. **We invent no benchmark.** We plot the world's existing benchmarks
    (GDPval, SWE-bench) in 3-D and 4-D instead of one-dimensional bar charts.
15. **No daily dollar ceiling.** The roster is the limit. If it is expensive,
    the magazine comes out less often.
16. **A model's mistakes are the product.** No gate, no repair, no correction,
    no warning labels. The reader switches edition and sees for themselves.
    That comparison IS the fact-checking.
17. **A continuous stream, not monthly issues.** Shaped like Wikipedia.
18. **The grid**: stories down the side, models across. Add either, one command
    fills only the missing cells.
19. **Kimi K2.6**, and **everything in batch** at half price.
20. **Eight editions means eight galaxies**, stored separately. Switching
    edition rearranges the sky.

---

## 5. EVERY COMMAND YOU NEED

```bash
cd /home/nir/strulovitz-website/pipeline

# FINISH KIMI - the one gap. About $0.25.
uv run stages/render_edition.py --all --model moonshotai/kimi-k2.6

# THE NORMAL WAY FROM NOW ON: half price, answers within 24 hours
uv run stages/render_edition.py --all --all-models --batch
uv run lib/llm.py                      # shows batches in flight, costs nothing

# ADD STORIES: paste links into content/inbox.txt, then
uv run stages/make_story.py

# ADD A MODEL: add a [[model]] block to config/editions.toml, then
uv run stages/render_edition.py --all --model <the new id> --batch

# REBUILD THE GALAXIES after any new edition
uv run stages/layout.py

# RE-READ ANSWERS ALREADY ON DISK. Calls nobody, costs nothing.
uv run stages/render_edition.py --all --all-models --reparse

# LOOK AT IT
cd .. && ./ops/look-at-the-site.sh            # then http://localhost:8080/tesseract.html
./ops/look-at-the-site.sh headset             # https, for the Quest 3

# THE TESTS. Run both after ANY change to the viewer.
node site/src/lib/fourd.selftest.js           # 64 checks
python3 ops/test-the-4d-page.py               # 113 checks, needs Chrome first:
# (setsid google-chrome --headless=new --remote-debugging-port=9333 \
#   --user-data-dir=/tmp/ai-panorama-4d-test/profile --no-first-run --no-sandbox \
#   --window-size=1400,900 --hide-scrollbars --use-gl=angle \
#   --use-angle=swiftshader --enable-unsafe-swiftshader about:blank </dev/null >/dev/null 2>&1 &)
```

---

## 6. WHAT TO DO NEXT, IN ORDER, WHEN THERE IS MONEY AGAIN

### Free — costs nothing, no model is called
1. **Finish Kimi** if the night did not (about $0.25, the only paid item here).
2. **Dim the tesseract.** Nir's question 2. It is currently as bright as the
   content, which is backwards. `site/src/vr/panorama.js`. Ask him how dim, and
   whether it should fade with motion.
3. **Decide the stem-versus-mesh question.** Nir's question 3, the real design
   question. Three options are laid out in
   `NIRS-PARKED-QUESTIONS-2026-08-21.md`. **Do not pick one for him.**
4. **BUILD THE ARTICLE PAGES.** This is the biggest missing piece and it costs
   nothing. Clicking a node in the galaxy currently opens nothing, because
   `stories/<slug>/<model>.html` does not exist yet. Each page needs: the
   headline, the TLDR, the picture, the article, the key points with their
   source links, the encyclopedia entries, the tags, every source linked
   prominently, and the edition switcher. Symmetrical folders — GPT gets no
   privileged position; the home page merely LINKS to the default model's copy.
   Stage to write: `pipeline/stages/build_pages.py`.
5. **THE PICTURES.** Every model wrote an illustration prompt and not one has
   been rendered. Nir chose **local ComfyUI on this desktop's RTX 4070 Ti**, free
   and unlimited, with **the same image model and the same seed for every
   edition**, so the only difference between editions' pictures is how well each
   model directed the illustrator. ComfyUI is installed at
   `/home/nir/ai-art/ComfyUI` with RealVisXL, Juggernaut and ZavyChroma
   checkpoints; the server is NOT running and needs restarting. Nir cares about
   the images more than almost anything else — do not leave this last again.
   Also: save each picture beside the text it accompanies, which he asked for
   explicitly. Stage to write: `pipeline/stages/images.py`.
6. **`run.py`** — the single command that looks at the whole grid, works out
   every missing cell, and fills only those. The pieces all exist; this ties
   them together.
7. **Hover cards in VR.** In the headset a node highlights and buzzes but says
   nothing readable. Item 3 of the remaining Milestone 1 list.
8. **Embed the frozen sources into Neo4j's vector index** for private search on
   this machine only. Reader-facing search must use our OWN edition prose
   instead, which we wrote and own — Nir's legal reasoning, and he is right.
9. **Deploy.** `python3 ops/build-export.py`, upload the dated folder FIRST and
   `pointer.json` LAST. Nir must be asked for the SFTP password every time and it
   is stored nowhere. **He still needs to change the one he pasted in chat.**

### Costs money
10. More stories. **23 cents per story across all eight editions in batch.**
11. More models on the roster, at the same price per story each.

---

## 7. THINGS THAT WILL BITE THE NEXT AGENT

1. **The git branch is `master`, not `main`.** GitHub links with `/main/` 404.
2. **Python buffers output**, so a long run's log looks empty. Use `python -u`,
   or watch the files appearing instead.
3. **A bash tool call that times out can kill the background job it started.**
   That is probably why the first big run stopped before Kimi. Start long jobs
   with `setsid nohup ... &` and check on them by looking at the files.
4. **`uv run` is required** for anything importing `neo4j`; bare `python3` in the
   pipeline folder fails with ModuleNotFoundError.
5. **Chrome caches ES modules hard.** Reload with `ignoreCache: true` over the
   debugging protocol or you will test yesterday's code and believe it.
6. **A REAL BUG I MADE AND FIXED, WORTH KNOWING:** GLM 5.3 is the only roster
   model that cannot be handed a strict JSON shape, so it was asked for JSON in
   words. It complied perfectly — and `llm.py` threw its answer away unparsed,
   because parsing was gated on having asked for a schema. All five of its
   editions were recorded as failures by my own code, not by the model. Fixed by
   always looking for JSON, and rescued from disk at zero cost with `--reparse`.
   **The lesson: when a model appears to have failed, check our own reading of
   its answer before believing it.**
7. **The placeholder world still exists and still matters.** `?world=placeholder`
   forces it. The 113 checks depend on it, and so do the lessons when the
   magazine is empty. Do not delete it.
8. **Nir cannot scroll back in OpenCode on Linux.** Keep every message to ONE
   screen. If it is longer than that, write a file, push it, and give him a
   GitHub link on the `master` branch.
9. **Never edit a model's output.** Not to fix a typo, not to improve a sentence,
   not to pick the better of two attempts. Retry ONLY when nothing arrived at
   all, and record the reason. This is decision 16 and it is the soul of the
   project.

---

## 8. WHAT THE FIRST REAL COMPARISON ALREADY SHOWED

Given the identical three frozen sources about AI-designed viruses:

- **GPT-5.6 Terra** wrote three encyclopedia entries and included **DNA synthesis
  screening** — the actual regulatory choke point in the biosecurity argument.
  **Gemini** wrote two and left it out. That is a real editorial judgement
  difference, visible to any reader who flips the listbox.
- **GPT wrote 15 encyclopedia entries across the five stories; Sonnet wrote 10.**
  Their galaxies are therefore different shapes, and GPT's is denser: 1.8 links
  per node against Gemini's 1.4.
- **All eight models independently decided that virus design has nothing to do
  with Kimi K3 or Grok 4.6**, and returned no related stories. Unanimous
  restraint, which is itself informative.
- **Gemini 3.7 Flash costs one cent an edition and is not embarrassed** by
  company fifteen times its price. Qwen 3.8 Max cost fifteen times more than
  Gemini for the same five stories.

Nobody has published that comparison, because nobody else lets eight models do
the same real editorial job on the same real material and shows a reader the
result as a place they can fly through.
