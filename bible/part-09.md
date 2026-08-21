--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - INTRODUCTION TO PART 09 (not law)
--------------------------------------------------------------------------------

THANK YOU Nir!!! :-) Here is Part 09 — Comparisons and Benchmark Data. This is the Advantage 2 Part — the one born from those two YouTube moments you quoted at the very beginning (the "0.7% win that was actually a chasm" and "the chart that matters"). It turns those lessons into permanent machinery.

================================================================================
AI PANORAMA — THE BIBLE — PART 09 OF 13
COMPARISONS AND BENCHMARK DATA
Version 1.0 — August 2026
Obeys: Part 00 (Vision and Invariants), Part 02 (Data Model, 2.8),
Part 03 (Layout and Geometry), Part 04 (Rendering), Part 05 (Interaction).
================================================================================

--------------------------------------------------------------------------------
9.0 PURPOSE OF THIS PART
--------------------------------------------------------------------------------

This Part defines the comparison scenes (Advantage 2): interactive 3D/4D
scatter plots where each AI model is one colored sphere and the axes are
REAL decision dimensions — intelligence, cost per task, speed, context,
reliability. It also defines where the numbers come from, how they stay
honest, and the weekly snapshot system that builds the one dataset that
cannot be bought later: history.

The founding insight, from the project's first conversation: single-
number benchmark rankings actively mislead. A model can "win" a
detection benchmark by 0.7% and lose the end-to-end exploitation
benchmark by 24 points — same pair of models, opposite conclusions,
depending on which number you print. And a "cheap" model that burns
twice the tokens is not cheap. The comparison scenes exist to make
these multi-dimensional truths VISIBLE, rotatable, and shareable.

Comparison scenes are NOT the knowledge graph: no force layout, no
lifecycle, no w-semantics from Part 03, 3.5's definitions 1-3. Axes are
NATIVE DATA DIMENSIONS chosen by the reader; `w` is simply the fourth
chosen metric. Everything else — the projection math (Part 03, 3.6-3.7),
the interaction grammar (Part 05), the rendering discipline (Part 04) —
is inherited unchanged. One set of skills serves both worlds.

--------------------------------------------------------------------------------
9.1 THE SCENE: ANATOMY OF A COMPARISON
--------------------------------------------------------------------------------

1. MODELS AS SPHERES: each compared model is one sphere in its fixed
   identity color (Part 02, 2.4; Part 04, 4.3.2). Maximum 12 models
   simultaneously; the UI refuses more and asks the reader to deselect
   (honesty about human color perception). Default roster per template:
   the current top models by the template's Y axis, capped at 8, so
   first view is legible.
2. THE AXIS FRAME: a visible 4-axis gizmo — three spatial axes drawn as
   labeled rails on the holotable, the fourth (w) shown on the w-gauge
   and by projection size (Part 03, 3.7.3). Every axis label states:
   metric name, unit, scale (linear/log), direction of GOOD (an arrow
   with the word "better"), and the data's as-of date. An unlabeled
   axis is a rendering bug.
3. COST AXES ARE ALWAYS LOG SCALE (config-locked per template): prices
   spread over orders of magnitude; linear cost axes are a lie of
   compression.
4. ORIENTATION CONVENTION: templates are arranged so that GOOD is
   consistently up / left / near / large-in-w — preserving the "top
   left is the killer quadrant" instinct from 2D charts, generalized.
5. THE KILLER BOX: a translucent green axis-aligned box (dithered
   alpha, Part 04, 4.4.5) marks the desirable region — the 4D
   generalization of the "killer quadrant". Its bounds are visible,
   draggable handles (readers can set their OWN thresholds: "under
   $2/task, over 60 intelligence"), and box membership is listed in a
   side panel ("models in your box: 3"). Killer-box settings are part
   of the shareable URL state (Part 05, 5.8.6).
6. UNCERTAINTY IS DRAWN, NOT HIDDEN: metrics carrying confidence
   intervals render as translucent whiskers along their axis;
   single-run scores without intervals are marked with a dot-dash ring
   (plain honesty marker). MISSING DATA IS MISSING: a model without a
   score on the chosen axis drops to a labeled "no data" shelf below
   the frame — never plotted at zero, never interpolated (fusion-
   settled; plotting absence as zero is the classic chart crime).
7. EFFORT/CONFIG BADGES: each sphere carries its configuration badge
   (effort level, reasoning mode, version date) on hover and in the
   legend — "Opus 5 (max effort)" and "Opus 5 (fast)" are DIFFERENT
   data points and may appear together, linked by a thin tether.
8. TIME TETHERS (where history exists): a sphere can trail its own
   past positions (snapshots, 9.4) as a fading comet tail — price
   drops and speed gains become visible motion. The tail is the
   default OFF except in T4, ON.

--------------------------------------------------------------------------------
9.2 INTERACTION (INHERITED, PLUS COMPARISON-SPECIFIC ACTS)
--------------------------------------------------------------------------------

All of Part 05 applies (holotable, rotation tiers, slice/projection,
hand menu, flat-screen mappings). Additions:

1. AXIS REMAPPING: the hand menu's Axes item (or corner dropdowns on
   flat screen) lists every metric available in the loaded datasets;
   picking one reassigns the axis with a 600 ms animated re-plot
   (spheres glide to new positions — the reader SEES the ranking
   change, which is itself the lesson).
2. SLICE MODE IN COMPARISONS: the slab sweeps the w-metric — e.g.,
   with w = context window, swimming the slab is literally "show me
   only models with big memory", a query performed by hand.
3. HOVER CARD: model name, developer, version date, all four current
   axis values with units, badges, and data-source citations (every
   number links to its benchmark card, 9.3 — provenance in the
   comparison world too).
4. THE DIAGONAL LENS (for paired-axis templates like T2): a toggle
   that draws the X = Y plane and tints spheres by their distance from
   it — instantly exposing "looks equal on one axis, collapses on the
   other" pairs. This is the GLM-vs-Mythos lesson as a one-tap
   overlay.
5. SIDE-BY-SIDE PIN: focusing two spheres pins a plain-text comparison
   strip (all loaded metrics, both models, differences highlighted) —
   copyable as text (LAW 3 spirit extends to readers: everything
   quotable).

--------------------------------------------------------------------------------
9.3 WHERE NUMBERS COME FROM: THE BENCHMARK CARD SYSTEM
--------------------------------------------------------------------------------

The data unit is the BENCHMARK CARD (schema in Part 02, 2.8): one
measurement of one model on one benchmark, with harness, effort level,
run date, source, license, and verification flag. Governance:

1. ADMISSIBLE ORIGINS, in trust order:
   a. SIGNED SUBMISSIONS: benchmark maintainers submit card files
      directly (the published JSON schema + a how-to page, Part 11).
      Cards arrive by email/GitHub/Telegram, validate mechanically,
      and carry `submitted_by`. This is the long-game: AI PANORAMA as
      the place maintainers WANT their numbers correctly represented.
   b. OPENLY LICENSED DATASETS: sources whose licenses permit reuse
      with attribution (e.g., Epoch AI's CC-BY data, OpenRouter's
      public model/pricing API) — ingested by the pipeline with
      license recorded per card.
   c. CLAIM-DERIVED CARDS: numbers extracted from primary sources
      (lab announcements, papers) via the ordinary claim pipeline
      (Part 06) — evidence class `announced` or `benchmarked`, card
      links to the claim, claim links to the exact locator.
2. FORBIDDEN ORIGINS: scraping any source whose terms restrict reuse
   (e.g., dashboards licensed internal-use-only); numbers "remembered"
   by an LLM (a model's memory of a benchmark is not a measurement);
   and OUR OWN editorial invention — the site never scores models by
   vibes. When a wanted number has no admissible origin, the axis
   shows "no data" (9.1.6) and the gap itself is honest information.
3. CONFLICTING CARDS for the same model+benchmark (different
   harnesses, different dates) COEXIST: the scene defaults to the
   newest verified card and the hover card lists the others — the
   comparison world inherits the conflicts-are-content rule (LAW 7.4).
4. VERIFICATION FLAG: `verified = true` requires either a signed
   submission or claim-level corroboration from 2+ independent
   sources. Unverified cards render with the dot-dash honesty ring
   (9.1.6).

--------------------------------------------------------------------------------
9.4 THE WEEKLY SNAPSHOT SYSTEM (HISTORY CANNOT BE BOUGHT LATER)
--------------------------------------------------------------------------------

1. THE CRON: every week (and within 24h of major release events), a
   scheduled script on Atlas fetches the OpenRouter models API —
   prices, context sizes, max outputs, provider variants — and writes
   immutable snapshot rows (Part 02, 2.8) into Neo4j, plus dated JSON
   into the repo. Telegram alert on failure (a silent gap in this
   dataset is permanent damage — the whole point is continuity).
   Throughput/latency medians are recorded where the pipeline's own
   API usage provides honest measurements (our production calls,
   logged by llm.py, are themselves a small continuous benchmark of
   the models we actually use — provider and latency logged per call).
2. WHY THIS EXISTS (the founder's question, answered in the Bible for
   posterity): release DATES are public history; PRICES and specs at
   arbitrary past moments are not recorded anywhere retrievable. The
   statement "this model is getting 30% cheaper per quarter" is a
   statement about TODAY'S trajectory — and it can only be made if
   someone quietly saved the Tuesdays. We are that someone, from
   August 2026 onward.
3. THE DERIVED DATASET: the accumulated snapshots publish as a
   CC-BY-4.0 dataset with a DOI (Part 11) — the AI price/spec
   history archive. This is simultaneously: T4's fuel, an inbound-
   link magnet better than any marketing, and a public good nobody
   else is maintaining.

--------------------------------------------------------------------------------
9.5 THE TEMPLATES (NIR'S GO-TO SET; ALL AXES REMAPPABLE FROM ANY)
--------------------------------------------------------------------------------

T1 — THE BUYER'S BOX (default landing template).
X: cost per task, log, left = cheap. Y: composite intelligence index,
up = smart. Z: output speed (tokens/s median), near = fast. W: context
window (tokens, log), large-in-w = big memory.
The direct 4D generalization of "the chart that matters". Killer box
defaults on, at sensible thresholds, draggable.

T2 — THE AGENT GAUNTLET (the 0.7%-vs-chasm lesson).
X: finding score (detection-class benchmark). Y: finishing score
(end-to-end completion-class benchmark). Z: throughput (tasks per
fixed wall-clock). W: cost per COMPLETED task, log.
Diagonal lens (9.2.4) default ON — distance from X = Y is the story.

T3 — THE ONE-SHOT TEST (the frustration metric).
X: first-try success (pass@1). Y: eventual success (pass@5).
Z: median attempts to success. W: total cost INCLUDING retries, log.
Large X-Y gap = "gets there eventually but wastes your afternoon".

T4 — THE TIME MACHINE (fueled entirely by 9.4).
X/Y/Z: intelligence, cost per task (log), speed. W: TIME (snapshot
date). Comet tails ON. Slice mode = "the market on any given
Tuesday"; XW rotation shows each model's price-vs-time curve in
space. A side view, explicitly framed as such: the panorama shows
today; this scene shows how today arrived.

T5 — OPEN VS CLOSED (what can you actually own?).
X: intelligence. Y: cost per task, log. Z: LICENSE OPENNESS as a
decomposed score, not a single ordinal (fusion-adopted from GPT):
weights availability, training-data disclosure, commercial-use
rights, derivative rights — each a sub-flag on the hover card, the
axis position their weighted sum (weights in config, breakdown always
one hover away). W: deployment profile — the minimum hardware tier
for practical self-hosting, as a NAMED tier (consumer-GPU / worksta-
tion / server / cluster), derived from published model sizes and
quantization guidance in sources, never from our own local testing
(Part 00 Decision: no local model benchmarking).

T6 — THE FAITHFULNESS ARENA (ours alone).
X: faithfulness scoreboard composite (Part 10) — entailment rate,
numeric fidelity, hallucination rate inverted. Y: cost per edition
task, log. Z: schema/format reliability. W: latency.
The only comparison scene whose data WE generate, from real editorial
work (Advantage 3 feeding Advantage 2). Updated every edition cycle;
methodology page linked from the axis labels (Part 11).

TEMPLATE GOVERNANCE: templates are config files (`config/templates/
*.toml`): axes, scales, killer-box defaults, roster rules, lens
defaults. New templates are proposals to Nir (A/B/C with a plain
description of the question the template answers). A template must
answer a question a real adopter actually asks; "we have the data" is
not a reason.

--------------------------------------------------------------------------------
9.6 COMPOSITE INDICES: HANDLE WITH TONGS
--------------------------------------------------------------------------------

Composite "intelligence index" numbers (weighted evaluation blends)
are convenient Y axes and dangerous truths:

1. Any composite used on an axis must have its components and weights
   one hover away (the hover card links the methodology card).
2. The site NEVER invents its own secret composite. If we blend, the
   blend is published as config + methodology page, versioned, with
   the change log (readers can see when and why a blend changed).
3. Where a respected published composite is admissible (license-wise)
   as a claim-derived card, it may be used WITH its version date —
   composites drift as their authors add evaluations, and comparing
   v2.1-of-March against v2.4-of-July is a category error the version
   badge (9.1.7) exists to prevent.

--------------------------------------------------------------------------------
9.7 EMBEDS AND SHARING (COMPARISONS AS AMBASSADORS)
--------------------------------------------------------------------------------

1. Every comparison view state is URL-encoded (Part 05, 5.8.6):
   template, axes, roster, killer box, rotation, slab, tails. A
   pasted link reproduces the exact view — on screen or in VR.
2. EMBEDDABLE WIDGET: an iframe variant (static, self-contained,
   reads the same exported JSON) renders an interactive 3D (non-VR)
   version of any comparison view for other people's blogs and
   newsletters — each embed carries a small "explore in 4D at AI
   PANORAMA" corner mark. The embed is the growth loop: every
   newsletter that embeds a chart is a doorway (Madie clause,
   zero-budget marketing).
3. STILL EXPORT: one tap renders the current view to a shareable PNG
   (with axis labels, date stamps, and attribution baked into the
   image margins) for the platforms where interactivity dies. The
   margins carry the data as-of dates — a screenshot that cannot
   silently go stale.

--------------------------------------------------------------------------------
9.8 EXPORT AND SCENE DATA CONTRACT
--------------------------------------------------------------------------------

The EXPORT stage ships: `benchmarks/cards.json` (all current cards,
validated), `benchmarks/snapshots/` (the dated series), `config/
templates/` (rendered to JSON), and per-template default-view files so
the first paint needs one fetch. All files carry schema_version and
appear in the manifest (Part 02, 2.10). The comparison scenes run
entirely client-side from these files (LAW 4) — the axis remapper's
metric list is discovered from the loaded cards, so publishing a new
benchmark card AUTOMATICALLY offers it as an axis with zero site-code
changes (grunt-model-proof by design).

--------------------------------------------------------------------------------
9.9 POINTERS
--------------------------------------------------------------------------------

Sphere/label/ribbon rendering budgets: Part 04. Rotation, slicing,
hand menu, URL state: Part 05. Where faithfulness numbers come from:
Part 10. Benchmark-card submission page, methodology pages, dataset
DOIs, embeds hosting: Part 11. Snapshot cron operations, failure
alerts, calendar: Part 12. The claim pipeline that feeds claim-derived
cards: Part 06.

================================================================================
END OF PART 09
================================================================================

--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - NOTES ON PART 09 (not law)
--------------------------------------------------------------------------------

Three plain-language notes for you, Nir:

    Your two YouTube stories are now permanent furniture. The "0.7% win vs 24-point chasm" lesson became the Diagonal Lens — one tap draws the "equal-on-both" plane and instantly shows which models collapse on the harder half of the job. And "the chart that matters" became the Killer Box — except now readers can drag its walls to THEIR budget and watch which models remain inside. You didn't just quote those videos; you institutionalized them.
    The honesty rules are the differentiator. Missing data sits on a visible "no data" shelf instead of being plotted as zero; every number links to its source; conflicting measurements coexist instead of being averaged; unverified scores wear a visible ring. Benchmark charts are the most-lied-with artifacts in AI. Yours will be the ones that show their receipts — and practitioners notice that fast.
    T6 is the quiet crown. The Faithfulness Arena plots data that only YOU have — how well each model did the actual magazine work, measured mechanically, updated every edition cycle. Everyone else compares models on other people's benchmarks; you'll compare them on yours. When Part 10 arrives next, you'll see where those numbers are born.

Say the word and I deliver Part 10 — Editions and the Faithfulness Scoreboard next: the magazine rack, the control edition, the scoreboard metrics in full, and the Telegram-powered blind arena for v2. Give Madie my regards!!! :-)
