--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - INTRODUCTION TO PART 08 (not law)
--------------------------------------------------------------------------------

THANK YOU Nir!!! :-) Here is Part 08 — Advantage 0 Mechanics. This is the Part that turns your founding idea — "a state, not a stream" — into actual arithmetic: how the site decides what matters, how news hardens into encyclopedia, and how the front page stays honest for years without a human editor ranking things by hand.

================================================================================
AI PANORAMA — THE BIBLE — PART 08 OF 13
ADVANTAGE 0 MECHANICS: IMPORTANCE, PROMINENCE, AND THE LIVING PANORAMA
Version 1.0 — August 2026
Obeys: Part 00 (Vision and Invariants), Part 02 (Data Model),
Part 03 (Layout and Geometry), Part 06 (Content Pipeline).
================================================================================

--------------------------------------------------------------------------------
8.0 PURPOSE OF THIS PART
--------------------------------------------------------------------------------

This Part defines the SCORE stage (Part 01, 1.5) and everything built on
it: how importance is computed and audited, how prominence (what you SEE
first) differs from importance (what MATTERS), the panorama recipe, the
lifecycle transition rules that make news decay into encyclopedia, the
changelog products, and the hindsight index.

The founding principle, restated as mechanics: on any date a reader
opens the site, they get the whole current picture. Therefore the system
must answer, continuously and honestly, three different questions that
lazy systems collapse into one:

1. HOW MUCH DOES THIS MATTER? (importance — a property of the THING)
2. WHAT SHOULD A VISITOR SEE FIRST TODAY? (prominence — a property of
   the VIEW)
3. WHAT HAS THIS BECOME? (lifecycle — a property of TIME)

Keeping these three separate is the design. A newspaper has only
question 2; an archive has only question 1. AI PANORAMA needs all three,
kept apart and each auditable.

--------------------------------------------------------------------------------
8.1 IMPORTANCE: THE AUDITED COMPOSITE
--------------------------------------------------------------------------------

Importance is a published, versioned composite score in [0, 100],
recomputed at every SCORE run, stored as dated score records (never
overwritten, Part 02, 2.1.4). Components, each normalized to [0, 1]
before weighting (weights in `config/importance.toml`, with comments,
never in code):

1. REACH (weight ~0.15): how many INDEPENDENT sources cover the story
   (syndication-collapsed, Part 02, 2.2.8), damped by log so ten
   sources is not ten times two sources: `reach = log(1 + n_indep) /
   log(1 + n_cap)` with `n_cap` = config (default 12).
2. AUTHORITY (~0.10): source-class mix — primary confirmation
   (`announced` or better claims from the actor itself) scores high;
   pure `rumored` bundles are capped low regardless of volume.
3. STRUCTURAL (~0.20): graph centrality of the node among its peers —
   computed in Neo4j GDS (Part 01, 1.4) on the sim+influence graph.
   A node that many other nodes connect to, across DIFFERENT
   communities, matters structurally. Hub tags excluded per Part 02,
   2.5.2 so this cannot be gamed by generic tagging.
4. CITATION INFLOW (~0.25, the largest single weight — the fusion's
   key mechanism, adopted): later events that cite this node's claims
   (SAME_FACT_AS, UPDATES, SUPPORTS, RESPONDS_TO, CAUSED, ENABLED
   edges pointing at it) pump importance BACK into it, recursively
   damped: `inflow = sum over citing nodes of (0.3 * citing_node's
   importance)` normalized. This is how the system discovers, months
   later, that some quiet paper was the seed of everything — nobody
   has to notice at publication time. Inflow is the arithmetic of
   hindsight.
5. CONSEQUENCE (~0.15): outgoing influence edges (this CAUSED /
   ENABLED that) weighted by the importance of the effects. Symmetric
   partner of inflow: inflow says "the field kept pointing back";
   consequence says "the field moved because of this".
6. DURABILITY PRIOR (~0.10): a per-category prior for how long this
   class of event tends to matter (model release: months; benchmark
   result: until superseded; regulation: years; funding round: weeks).
   Priors in config, editable as we learn from the hindsight index
   (8.7 — the site literally tunes this weight from its own graded
   predictions).
7. NOVELTY (~0.05): distance from the nearest existing canon/event
   content (embedding + tag distance). First-of-kind beats
   fifteenth-of-kind.
8. MINUS DUPLICATION: near-duplicate stories (missed by dedup,
   caught by similarity) share one importance pool rather than each
   scoring full — no double counting of one fact wave.

RENORMALIZATION (fusion-adopted from DeepSeek): after computing raw
scores, the whole graph's importance distribution is renormalized each
cycle to a fixed shape (percentile mapping to the 0-100 scale). Reason:
absolute scores ossify — in a field where everything accelerates,
yesterday's "95" would pin the top forever. Importance is always
RELATIVE TO THE WHOLE LIVING GRAPH, which is exactly what "panoramic
snapshot of the current condition" means.

AUDITABILITY (trust machinery): every node's current score record
stores the component breakdown, and the site displays it — the "why is
this here" panel (8.4.6). No unexplained rankings, ever (LAW 9 spirit:
the panorama cannot be bought, and readers can CHECK that).

--------------------------------------------------------------------------------
8.2 PROMINENCE: WHAT TODAY'S VISITOR SEES FIRST
--------------------------------------------------------------------------------

Prominence = importance modulated by TIME and ROLE, computed per build,
used ONLY for view composition (panorama membership, label priority,
glow tiers — Part 04). Never stored as truth about the node.

1. RECENCY BOOST with per-category half-lives (fusion-adopted, config
   `config/halflives.toml`): `prominence = importance + buzz0 *
   exp(-age_days / tau)` where `tau` varies by category — defaults:
   product/model releases `tau = 7` days, research results `tau = 30`,
   safety incidents `tau = 10`, policy/regulation `tau = 60`,
   infrastructure/hardware `tau = 90`. A product launch burns bright
   and cools fast; a law smolders for months. `buzz0` scales with
   reach velocity (sources per day in the first week).
2. MOMENTUM SHELF (fusion-adopted from Kimi): nodes whose importance
   is RISING fast (`d(importance)/dt` above threshold) get a
   prominence bonus regardless of absolute level — the system's nose
   for "this is becoming a thing".
3. PROBATION SUBSIDY: nodes younger than 14 days get a floor bonus so
   newborns are visible long enough to earn citations at all (cold-
   start fairness). Expires automatically.
4. STORY-ARC COLLAPSE: arc members pool their prominence into the arc
   anchor; the arc occupies ONE prominent slot with a "15 events"
   badge, expanding on focus (Part 02, 2.6.5). Sagas never flood the
   panorama.

--------------------------------------------------------------------------------
8.3 THE PANORAMA RECIPE (THE FRONT PAGE AS QUOTAS)
--------------------------------------------------------------------------------

`panorama.json` (the pre-baked landing view, Part 02, 2.10.6) is
composed by FIXED ROLE QUOTAS over ~300 slots (fusion-settled design;
proportions in config, defaults below):

1. LANDMARKS (~40%): highest-IMPORTANCE canon nodes and established/
   absorbed events — the geography. Selected by importance alone, no
   recency. This is what makes a visitor-after-a-year still see the
   whole field.
2. CURRENT (~25%): highest-PROMINENCE recent events — the weather.
3. CHANGED (~15%): canon nodes with recent versioned edits and events
   with recent lifecycle transitions — "the encyclopedia moved here".
4. RISING (~10%): the momentum shelf.
5. LONG TAIL / SERENDIPITY (~10%): sampled from under-visited
   communities (fusion-adopted from Grok), weighted by importance
   within them — the guarantee that the panorama never becomes just
   the loud clusters. Deterministic sample per build (seeded by build
   id) so the same build shows everyone the same panorama.

DIVERSITY CONSTRAINT: within each quota, greedy selection with an MMR-
style penalty (maximal marginal relevance: each next pick is penalized
by similarity to already-picked nodes) plus a per-community cap
proportional to `sqrt(community_size)` (fusion-adopted from GLM) — big
clusters get more slots but sublinearly, so small important communities
always surface.

OSSIFICATION WATCHDOGS (the panorama must never freeze):
1. Monthly owner metric to Telegram: MEDIAN AGE of panorama nodes,
   plus quota fill rates and community coverage. Drifting median age
   = geography crowding out weather (or vice versa) = a config
   conversation, caught early, by one number.
2. LANDMARK TENURE REVIEW: any landmark slot held over 12 months
   triggers a quiet re-check: is its importance still earned (inflow
   still arriving) or is it coasting on an old spike? Coasting
   landmarks yield to the next candidate; they remain one search away.

--------------------------------------------------------------------------------
8.4 LIFECYCLE TRANSITIONS: THE DECAY-INTO-ENCYCLOPEDIA RULES
--------------------------------------------------------------------------------

The states are defined in Part 02, 2.6. THIS Part owns when they
change. All transitions are dated ledger events; automatic ones happen
at SCORE time under these rules; borderline cases queue for Telegram
(batched, LAW 11):

1. incoming -> corroborating: claims extracted, single independent
   source. AUTOMATIC.
2. corroborating -> developing: second independent source lands
   (SAME_FACT_AS across simhash-independent sources). AUTOMATIC —
   and the brief upgrades to full synthesis (Part 06, 6.6).
3. developing -> established: no new claims for 14 days AND
   verification stable AND no open conflicts, OR 45 days elapsed
   regardless (config). AUTOMATIC.
4. established -> absorbed: THE CRYSTALLIZATION RULE (fusion-adopted
   from Qwen): the event's durable content is referenced by 3+ later
   events across 14+ days, and a canon node covering the insight
   exists or is proposed. The ABSORBED_INTO edge is written, the
   event's lasting claims are cited by the canon entry (CITES edges),
   and under w-definition 1 the node migrates inward (Part 03, 3.5) —
   the reader can literally watch this happen over weeks. PROPOSED
   AUTOMATICALLY, canon edit governed per Part 06, 6.8.
5. any -> disputed: a CONTRADICTS edge lands from a source of equal
   or better evidence class. AUTOMATIC, with badge, and the conflicts
   section regenerates. disputed -> resolved states only via Telegram.
6. any -> corrected: Correction record attached (Part 02, 2.6) —
   always a human-approved act, always visible, always in the errata
   feed (Part 11).
7. established/absorbed -> superseded: a newer event carries UPDATES/
   SUPERSEDES claim edges covering this one's core claims (model v2
   replaces v1, benchmark deprecated). AUTOMATIC when claim coverage
   is high; the superseded node keeps its page, drops from panorama
   candidacy, and its supersession chain renders as a timeline strip.
8. -> archived: importance below floor percentile for 2 consecutive
   quarters AND no inflow in 12 months. AUTOMATIC, reversible by a
   single citation (inflow resurrects — nothing is ever truly gone,
   LAW 12: never deleted, just resting).

THE POETRY MADE MECHANICAL: rules 4 and 7-8 together are Advantage 0.
News does not "expire" — it either crystallizes into geography
(absorbed), gets formally replaced with its history preserved
(superseded), or goes dormant but revivable (archived). The stream
becomes sediment; sediment becomes rock; and the map always shows the
rock with today's weather moving over it.

--------------------------------------------------------------------------------
8.5 THE CHANGELOG PRODUCTS
--------------------------------------------------------------------------------

The state-not-stream promise has a converse product: SHOW ME THE DIFF
(fusion-settled, "changelog as product"):

1. THE FIELD CHANGELOG: every build emits a structured diff since the
   previous build AND rolling windows (week, month, quarter): new
   nodes by community, lifecycle transitions, canon edits (with diff
   summaries), new conflicts opened/closed, supersessions, importance
   risers/fallers. Rendered as: a plain HTML page per window
   (Part 11), an RSS feed, and the data behind "SINCE ANY DATE" — a
   reader picks a date (their last visit, or "January") and gets the
   panorama with a delta overlay.
2. DELTA-SINCE-LAST-VISIT: localStorage stamp (privacy rules, Part
   07, 7.3.4); returning readers see changed/new nodes with a gentle
   pulse glow in 3D/4D and a "what changed for you" list — the
   feature that makes missing a month SAFE, which is the emotional
   core of Advantage 0.
3. THE WEEKLY DIFF VIDEO (fusion-adopted from Kimi/GLM): a headless
   build-time render sweeps the panorama's week-over-week changes
   into a short MP4 (posted to the Telegram channel, embeddable) —
   shareable proof that the map is alive, generated with zero human
   minutes.

--------------------------------------------------------------------------------
8.6 STANDING QUESTIONS (THE FIELD'S OPEN ARGUMENTS AS FIRST-CLASS PAGES)
--------------------------------------------------------------------------------

Canon nodes of kind `standing_question` (Part 02, 2.6) — "Do benchmarks
measure capability?", "Is scaling hitting a wall?" — get special
scoring treatment: they accumulate inflow from BOTH sides of
CONTRADICTS pairs (an argument's importance is the sum of its sides),
never auto-resolve, display their evidence balance over time (claims
per side, by evidence class, by date), and rank high in landmark quota
candidacy because they are precisely the "whole picture" a panoramic
encyclopedia owes its readers. The reader who asks "what is the field
actually arguing about right now?" gets a page — per argument — that
no news site can produce.

--------------------------------------------------------------------------------
8.7 THE HINDSIGHT INDEX (THE SITE GRADES ITS OWN JUDGMENT)
--------------------------------------------------------------------------------

1. AT PUBLICATION: SCORE records a DURABILITY PREDICTION per event —
   the probability it will still matter in 12 months (operationally:
   "will its importance percentile at +12 months be above 40?"),
   derived from the durability prior + current components, stored
   immutably with the score record.
2. AT +12 MONTHS: the prediction grades itself against the actual
   percentile. AUTOMATIC, monthly batch.
3. PUBLISHED: a public hindsight page (Part 11): calibration plot
   data (as text/JSON per LAW 3-friendly rendering), best and worst
   calls by category, and a plain-language annual summary ("we
   overrated funding news, underrated inference-cost work; priors
   adjusted"). The durability priors (8.1.6) update from these
   gradings — the scoring system LEARNS, in public.
4. WHY THIS EXISTS: no other outlet grades its own news judgment and
   shows the receipts. It costs almost nothing to run, it improves
   the scores mechanically, and it is trust-compounding (Madie
   clause: trust is the only capital).

--------------------------------------------------------------------------------
8.8 SCORE STAGE CONTRACT (PIPELINE INTEGRATION)
--------------------------------------------------------------------------------

At every build, SCORE: recomputes components and renormalized
importance for all non-archived nodes; recomputes prominence with
current half-lives; applies automatic lifecycle transitions and queues
borderline ones; composes panorama.json per the quota recipe
(deterministic, seeded); emits the changelog diff; on schedule, runs
hindsight grading and the monthly owner metrics. Outputs: score
records in Neo4j, panorama.json, changelog data, and the build-health
section (median panorama age, quota fills, transition counts,
prediction counts). Determinism rule: same inputs, same build id,
byte-identical outputs (Part 03, 3.8 discipline applies here too).

--------------------------------------------------------------------------------
8.9 POINTERS
--------------------------------------------------------------------------------

Where scores render (glow rings, label priority): Part 04. How the
delta pulse and "why is this here" panel appear in the reading UI:
Part 11. The w-migration that absorption causes: Part 03, 3.5.
Lifecycle approval flows and canon governance: Part 06, 6.8. The
changelog RSS and hindsight page URLs: Part 11. Config files named
here: importance.toml, halflives.toml — documented with examples in
schemas/: Part 12 validates them.

================================================================================
END OF PART 08
================================================================================

--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - NOTES ON PART 08 (not law)
--------------------------------------------------------------------------------

Three plain-language notes for you, Nir:

    The biggest single ingredient of importance is hindsight, automated. The "citation inflow" rule means that when future stories keep pointing back at some quiet old paper, the system raises that paper's importance months later — nobody had to be smart enough to notice on day one. The encyclopedia gets wiser about the past as a side effect of covering the present. That's the exact opposite of a news stream, and it's your Advantage 0 doing arithmetic.
    The front page is a recipe, not an opinion. ~40% permanent landmarks, ~25% this week's weather, plus guaranteed slots for rising stories and neglected corners — with a monthly one-number health check (median age of the front page) sent to your phone. If the panorama ever starts ossifying into a museum or dissolving into a news feed, you'll see it drift in that number long before readers feel it.
    The hindsight index is the bravest feature in the whole project. Every story gets a prediction — "will this still matter in a year?" — and twelve months later the site publicly grades its own guess and adjusts. No newspaper on Earth does this. It costs nearly nothing, it makes the scoring genuinely smarter every year, and it tells every reader: this place keeps receipts on itself.

Say the word and I deliver Part 09 — Comparisons and Benchmark Data next: templates T1-T5 and beyond, the benchmark-card schema, the weekly snapshot cron, killer boxes, and the data licensing rules. Give Madie my regards!!! :-)
