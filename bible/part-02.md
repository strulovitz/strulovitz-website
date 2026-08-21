================================================================================
AI PANORAMA — THE BIBLE — PART 02 OF 13
DATA MODEL
Version 1.0 — August 2026
Obeys: Part 00 (Vision and Invariants) and Part 01 (Architecture).
================================================================================

--------------------------------------------------------------------------------
2.0 PURPOSE OF THIS PART
--------------------------------------------------------------------------------

This Part defines every kind of record the project stores in Neo4j on
Atlas, every kind of relationship between records, and every format the
export builder writes for the website. If a stage of the pipeline (Part
06) or a scene of the website (Parts 03-05) needs data, the shape of that
data is defined HERE and only here.

Three principles govern the whole model:

1. CLAIMS ARE THE ATOMS. Articles are not made of source prose; they are
   made of verified claims, each traceable to an exact place in an exact
   source. Everything above claims (articles, canon, scores, editions) is
   built from them and can be re-derived from them.
2. EDGES CARRY MEANING. A link between two nodes always has a TYPE and a
   WEIGHT. "These two things are related somehow" is not a valid edge.
3. TRUTH LIVES IN ONE PLACE. Neo4j is the source of truth (LAW 5). Export
   files are derived, reproducible artifacts. If an export and the
   database disagree, the database is right and the export is rebuilt.

Terminology note: "node" in this Part means a Neo4j record. The VISUAL
nodes floating in 3D/4D space correspond to PUBLISHABLE nodes only (event
nodes, canon nodes, and comparison spheres) — sources, claims, and
entities are internal machinery and are never rendered as graph nodes.

--------------------------------------------------------------------------------
2.1 IDENTIFIERS, TIME, AND VERSIONING (RULES FOR ALL RECORDS)
--------------------------------------------------------------------------------

1. IDS. Every record has a permanent, human-readable id, never reused,
   never renamed:
   - Sources:   src-2026-0847        (year + counter)
   - Claims:    clm-2026-0847-013    (source id + claim counter)
   - Events:    evt-2026-0142        (these become public cite keys,
                                      shown on the site as AP-2026-0142)
   - Canon:     can-agentic-coding   (readable slug, chosen once)
   - Entities:  ent-anthropic, ent-claude-fable-5
   - Editions:  edn-2026-09-kimi-k3  (issue + model slug)
   - Jobs:      job-2026-08-20-0007  (ledger, Part 12)
   The public cite key AP-YYYY-NNNN (AP for AI PANORAMA) appears on every
   published page so humans and papers can cite stably (Part 11).

2. TWO CLOCKS. Every fact-bearing record carries two timestamps:
   - `t_event`     — when the thing HAPPENED in the world.
   - `t_knowledge` — when WE learned/recorded/last-revised it.
   Example: a price cut on March 3 ingested on March 7 has `t_event` =
   March 3, `t_knowledge` = March 7. Corrections update `t_knowledge`,
   never `t_event`. All "what changed since your visit" features (Part
   08) run on `t_knowledge`; all history/timeline features run on
   `t_event`. Confusing the two clocks is a bug.

3. SCHEMA VERSIONS. Every export file and every Neo4j record type carries
   `schema_version` (integer). The pre-upload validator (Part 12) rejects
   any file whose schema_version does not match the current `schemas/`
   definitions. Schema changes are ledger events with migration notes.

4. IMMUTABILITY RULES (LAW 12 applied):
   - Sources and claims: immutable after creation (a re-fetch that finds
     changed text creates a NEW source record linked to the old one).
   - Event nodes: immutable once published. Corrections are new records
     of type Correction linked to the event (2.6).
   - Canon nodes: mutable but VERSIONED — every revision stores a diff,
     a date, and the reason.
   - Scores: never overwritten; new score records with version stamps.

--------------------------------------------------------------------------------
2.2 SOURCES
--------------------------------------------------------------------------------

A Source is one fetched document: an article, a video transcript, a forum
thread, a README, an official blog post, a paper.

Properties:
1.  `id`, `schema_version`
2.  `url` (canonical), `fetched_url` (as actually fetched)
3.  `source_type`: one of `press`, `video`, `official_blog`, `paper`,
    `forum`, `repo`, `benchmark_report`, `social`
4.  `source_class`: `primary` or `secondary`. Primary = the actor speaks
    (lab blog, paper, repo, official announcement). Secondary = someone
    reports on the actor (press, YouTube commentary). LAW 7 practice:
    primary sources form the spine of synthesis; secondary sources
    corroborate and add angles (Part 06).
5.  `publisher` (entity id), `author` (free text), `title`
6.  `t_event` (publication date), `t_knowledge` (fetch date)
7.  `raw_text_path` (kitchen disk cache), `raw_text_hash` (sha256)
8.  `simhash` — 64-bit locality-sensitive hash of the text. Two sources
    whose simhash Hamming distance is at or below 3 are treated as
    SYNDICATED COPIES: they are linked `SYNDICATED_WITH` and count as ONE
    source for the two-source rule of LAW 7 and for reach counting
    (Part 08). Threshold lives in config, not code.
9.  `paywalled` (bool), `robots_ok` (bool) — fetch etiquette flags.
10. For videos: `video_id`, `channel` (entity id), `transcript_by`
    (whisper model + version), `duration_s`.

Relationships:
- `(Source)-[:PUBLISHED_BY]->(Entity)`
- `(Source)-[:SYNDICATED_WITH]-(Source)`
- `(Source)-[:SUPERSEDED_BY]->(Source)` (re-fetch with changed text)

--------------------------------------------------------------------------------
2.3 CLAIMS (THE ATOMS)
--------------------------------------------------------------------------------

A Claim is ONE atomic factual statement extracted from ONE source. Atomic
means: it asserts one thing, about identified entities, that could in
principle be true or false. "GLM 5.3 scored 84.5% on CyberGym" is one
claim. "GLM 5.3 beat Mythos 5 and is also cheaper" is two claims.

Properties:
1. `id`, `schema_version`
2. `text_normalized` — the claim in our neutral wording.
3. `span_verbatim` — the EXACT quoted characters from the source that
   ground this claim. Never paraphrased. This is the audit trail.
4. `locator` — where in the source:
   - articles: `para:14` (paragraph index) plus `char_start`, `char_end`
   - videos:   `t:583` (seconds from start; deep links jump to 9:43)
   - PDFs:     `page:6` plus paragraph
5. `evidence_class` — exactly one of:
   - `rumored`     (unnamed sources, leaks, speculation)
   - `reported`    (named secondary source states it)
   - `announced`   (the actor itself states it — primary)
   - `benchmarked` (a measurement with stated method/harness)
   Evidence class is displayed to readers and used by synthesis rules
   (Part 06): e.g., a `rumored` claim may never appear in prose without
   the word "reportedly" or similar, and never in a TLDR.
6. `claim_kind`: `numeric`, `event`, `quote`, `stance`, `method` —
   numeric claims carry parsed `value`, `unit`, `as_of_date` so the
   deterministic verifier (Part 06) can check every number in prose
   against the claim set mechanically.
7. `extracted_by` (model slug + prompt version), `t_knowledge`.

Relationships:
- `(Claim)-[:FROM_SOURCE]->(Source)`
- `(Claim)-[:ABOUT]->(Entity)` (one or more)
- `(Claim)-[:SAME_FACT_AS]-(Claim)` — cross-source corroboration link:
  two claims from independent sources asserting the same fact. The
  corroboration count of a fact = number of independent sources in its
  SAME_FACT_AS cluster (syndicated copies collapsed). This count drives
  the two-source rule and importance (Part 08).
- Typed claim-to-claim edges (THE CLAIM GRAPH, the deep structure):
  - `SUPPORTS`            (evidence in the same direction)
  - `CONTRADICTS`         (cannot both be true — fuels the conflicts
                           section; conflicts are content, LAW 7.4)
  - `UPDATES`             (newer figure replaces older figure)
  - `SUPERSEDES`          (formally replaces: v2 spec vs v1)
  - `REPLICATES`          (independent re-measurement agrees)
  - `FAILS_TO_REPLICATE`  (independent re-measurement disagrees)
  These edges are proposed by the pipeline with model + confidence and
  the important ones are surfaced for Nir's Telegram approval per the
  thresholds in Part 06.

--------------------------------------------------------------------------------
2.4 ENTITIES AND ALIASES (THE REGISTRY)
--------------------------------------------------------------------------------

An Entity is a real-world thing that claims are about: a company, a lab, a
model, a person, a product, a benchmark, a law/regulation, a dataset.

Properties:
1. `id`, `schema_version`, `entity_type`: `org`, `model`, `person`,
   `product`, `benchmark`, `regulation`, `dataset`, `event_series`
2. `name_canonical` — the one display name.
3. `wikidata_qid` — when one exists; anchors us to a public registry.
4. For models: `family` (entity id), `developer` (entity id),
   `release_date`, `weights_open` (bool), `license_slug`,
   `display_color` — THE fixed site-wide color of this model (LAW 2:
   color = identity). Assigned once from the palette in Part 04,
   never changed thereafter.

Aliases: `(Alias {text, lang})-[:ALIAS_OF]->(Entity)`. "GPT-5.6 Sol",
"gpt5.6-sol", "OpenAI's new Sol model" all resolve to one entity. The
RESOLVE stage (Part 06) matches claim mentions to entities via aliases
first, then embedding similarity, then — only for genuinely new names —
proposes a NEW entity for Nir's one-tap Telegram approval. Unresolved
mentions never silently create entities; near-duplicate entities are the
disease that killed many knowledge bases, and the registry is the cure.

Merging entities (discovered duplicates) is a ledger event: the loser id
becomes an alias, all edges re-point, and a `MERGED_INTO` record keeps
the history. Public HTML for a merged id redirects to the winner
(Part 11).

--------------------------------------------------------------------------------
2.5 TAGS ARE CANON NODES
--------------------------------------------------------------------------------

There is no separate "tag" table. A tag IS a canon node (2.6) with
`canon_kind: topic`. Tagging an event means creating an edge
`(Event)-[:TAGGED {weight}]->(Canon)`.

This unification (per the fusion consensus) means: the tag vocabulary is
governed exactly like the encyclopedia (versioned ELI5 text, approval
flow, supersession), the ego-view of a tag is just the neighborhood of a
canon node, and "tag pages" and "concept pages" are the same page.

Vocabulary governance:
1. The pipeline may PROPOSE new topics; only Nir's Telegram approval
   creates one (staged vocabulary). Proposals arrive with: suggested
   slug, one-sentence definition, three example events, and the nearest
   existing topics (to expose duplicates before they are born).
2. HUB TAGS: topics whose event-count exceeds the hub threshold (config;
   e.g., "LLMs") are marked `is_hub: true`. Hub tags still exist as
   pages, but they GENERATE NO GRAPH EDGES for layout and no similarity
   weight — otherwise everything connects to everything and the map
   collapses into a ball (the IDF principle, 2.7).
3. Topic hierarchy: `(Canon)-[:PARENT_TOPIC]->(Canon)` where sensible
   (e.g., "context-window-engineering" under "inference"). Used for
   cluster naming and the lens filters, not for layout.

--------------------------------------------------------------------------------
2.6 PUBLISHABLE NODES: EVENTS, CANON, AND THEIR LIFECYCLES
--------------------------------------------------------------------------------

EVENT NODE — an immutable published news item (Advantage 0's "weather").

Properties:
1.  `id` (public cite key derives from it), `schema_version`
2.  `headline`, `tldr` (max 140 chars — the ladder, Part 00 section 0.6)
3.  `t_event`, `t_knowledge`, `published_at`
4.  `lifecycle_state` — exactly one of:
    `incoming`      (ingested, claims extracted, not yet publishable)
    `corroborating` (single-source; publishable only as a BRIEF, LAW 7.2)
    `developing`    (published, still accumulating sources/claims)
    `established`   (stable, corroborated, part of the record)
    `absorbed`      (its lasting content now lives in canon nodes; the
                     event remains readable but yields prominence)
    `disputed`      (credible contradiction exists — shown with a badge)
    `corrected`     (a Correction record is attached)
    `superseded`    (a newer event replaces it; edge points forward)
    `archived`      (long-tail; excluded from panorama, never deleted)
    Transitions are proposed by pipeline rules (Part 08) and applied
    automatically when confidence is high, else queued for Telegram
    approval. Every transition is a dated ledger event.
5.  `story_arc_id` — optional; events in one saga (e.g., one lawsuit
    across months) share an arc. Arcs get ONE panorama slot (Part 08)
    and a timeline strip on their pages.
6.  `is_brief` (bool) — single-source extractive brief per LAW 7.2.
7.  `conflicts` — array of {topic, claim_id_a, claim_id_b, note} rendered
    as the "sources disagree" section. Conflicts are never averaged.
8.  `importance`, `prominence` — current scores (score RECORDS with
    history live separately; Part 08).
9.  `image_prompt_id`, per-image-model asset hashes (Part 06).
10. Position data: `xyz` (from layout, Part 03), `w_semantic` (from the
    active w-definition, Part 03), `layout_epoch`.

Relationships of events:
- `(Event)-[:BUILT_FROM]->(Claim)` — every event knows its atoms. Every
  sentence of the article prose stores the claim ids it rests on
  (sentence-to-claims map kept as a property blob `sentence_claims`),
  powering the hover-provenance UI (Part 11) and the verifier (Part 06).
- `(Event)-[:TAGGED {weight}]->(Canon)`
- `(Event)-[:PART_OF_ARC]->(StoryArc)`
- `(Event)-[:SUPERSEDED_BY]->(Event)`
- Influence edges (DIRECTED, the "why" of the field — from the fusion's
  best structural idea):
  - `(A)-[:CAUSED]->(B)`   (price cut CAUSED rival price cut)
  - `(A)-[:ENABLED]->(B)`  (paper ENABLED product)
  - `(A)-[:RESPONDS_TO]->(B)` (rebuttal, counter-launch, regulation)
  Influence edges require either an explicit claim asserting the link or
  Nir's approval; the pipeline may propose with confidence scores but
  never auto-commits low-confidence causality. On the site, influence
  edges render as directed streams the reader can follow ("what did this
  lead to?").

CANON NODE — a mutable, versioned encyclopedia entry (the "geography").

Properties:
1. `id`, `schema_version`, `canon_kind`: `topic`, `concept`, `explainer`,
   `standing_question` (an open question the field argues about — a
   first-class page type: "Do benchmarks measure capability?")
2. `title`, `eli5` (the explain-like-I-am-five text, versioned),
   `body` (the full living entry, versioned), `tldr`
3. `crystallized_from` — the event ids whose absorption built this entry
4. `revision_history` — array of {date, diff_summary, reason, job_id}
5. `is_hub`, `parent_topic`, position data as events.

Relationships:
- `(Canon)-[:CITES]->(Claim)` — canon text is claim-grounded like events.
- `(Canon)-[:RELATED {weight}]-(Canon)` — computed similarity (2.7).
- `(Event)-[:ABSORBED_INTO]->(Canon)` — the decay-into-encyclopedia edge;
  the mechanics of when this fires live in Part 08.

CORRECTION — `(Correction {date, what_was_wrong, what_is_right,
claim_ids})-[:CORRECTS]->(Event)`. Rendered prominently, listed in the
public errata feed (Part 11). We publish our mistakes (Part 00, 0.2).

--------------------------------------------------------------------------------
2.7 EDGE WEIGHTS FOR LAYOUT AND SIMILARITY
--------------------------------------------------------------------------------

The visual graph's springs (Part 03) use ONE combined similarity weight
per node pair, computed at SCORE time:

1. Shared-topic weight with IDF damping: a shared topic t contributes
   `idf(t) = 1 / log(1 + count(t))` where `count(t)` = number of events
   tagged t. Rare shared topics bind strongly; hubs bind at zero (2.5).
   Sum over shared topics.
2. Claim-graph bonus: any SUPPORTS / UPDATES / REPLICATES /
   SAME_FACT_AS connection between the nodes' claims adds `beta_claim`;
   CONTRADICTS adds `beta_conflict` (yes, conflicts attract — disputed
   things belong side by side so readers see the dispute).
3. Influence bonus: a CAUSED / ENABLED / RESPONDS_TO edge adds
   `beta_influence`, the strongest single bond.
4. Entity co-mention: shared non-hub entities add a small
   `beta_entity * idf(entity)` term.
All betas live in `config/weights.toml` with comments, never in code.
The result is `sim_weight` stored on `(A)-[:SIM {weight}]-(B)` edges,
recomputed at SCORE, consumed by LAYOUT (Part 03) which decides cutoffs.

--------------------------------------------------------------------------------
2.8 COMPARISON DATA: BENCHMARK CARDS AND SNAPSHOTS (SHAPE ONLY)
--------------------------------------------------------------------------------

Owned by Part 09; the SHAPES live here for one-stop schema reference.

BENCHMARK CARD (one measurement of one model on one benchmark):
`{schema_version, benchmark (entity id), model (entity id), score, unit,
higher_is_better, effort_level, harness, run_date, source (source id),
license_of_data, submitted_by, verified (bool)}`
Missing data is MISSING, never zero (rendered as absent, LAW-adjacent
honesty rule).

PRICE/SPEC SNAPSHOT (the weekly cron, Part 09):
`{schema_version, snapshot_date, provider, model (entity id),
usd_per_m_input, usd_per_m_output, context_tokens, max_output_tokens,
throughput_tps_median, latency_s_p50, source_api, license_of_data}`
Snapshots are immutable rows; the T4 view and price-history dataset are
derived entirely from them.

--------------------------------------------------------------------------------
2.9 EDITION RECORDS (SHAPE ONLY; MECHANICS IN PART 10)
--------------------------------------------------------------------------------

For each edition and each event in its issue scope:
`{schema_version, edition_id, event_id, model_slug, model_version_date,
prompt_version, prose, tldr, eli5_texts, tag_proposals, image_prompt,
idempotency_key, cost_usd, latency_s, faithfulness: {entailment_rate,
attribution_correct, numeric_fidelity, hallucinated_entities,
importance_coverage, conflict_preservation, schema_valid}}`
The idempotency key is `hash(event_id + edition_id + model_version_date +
prompt_version)` — LAW 12's guarantee that nothing is silently
regenerated. Graph structure, positions, and scores are edition-invariant
(Part 00, Advantage 3); ONLY the fields above vary.

--------------------------------------------------------------------------------
2.10 EXPORT FORMATS (WHAT THE WEBSITE ACTUALLY DOWNLOADS)
--------------------------------------------------------------------------------

The export builder (Part 01, 1.9) derives everything below from Neo4j.
All multi-byte numbers little-endian; all files carry a magic string +
schema_version in their first bytes; every file's sha256 appears in
`manifest.json`. Sizes assume year-3 scale (20k nodes, 200k sim edges) —
totals stay under ~1 MB gzipped for the whole structural layer.

1. `graph/nodes.bin` — one record per publishable node, sorted by
   IMPORTANCE DESCENDING (this ordering IS the level-of-detail system:
   the renderer reads a prefix — first N nodes = top-N important; no
   separate tier files). Per record:
   - `node_index` implicit; `node_kind` uint8 (event/canon/arc)
   - `xyz` 3 x uint16 (quantized to the layout bounding box)
   - `w` uint16 (quantized; per active w-definition)
   - `importance` uint8, `prominence` uint8
   - `lifecycle_state` uint8, `flags` uint8 (is_brief, disputed,
     has_conflicts, is_hub...)
   - `color_index` uint8 (palette index — identity colors, LAW 2)
   - `epoch_id` uint8
2. `graph/edges.csr.bin` — similarity + influence edges in CSR form
   (offsets array uint32, neighbor indices uint32, weight uint8,
   edge_type uint8). CSR = "compressed sparse row", the compact standard
   for adjacency; the client query layer (Part 01, 1.6) walks it
   directly for ego/k-hop/lens without ever inflating objects.
3. `graph/ids.json` — node_index to public id mapping + reverse.
4. `graph/tagsets.bin` — bitset per node over the topic vocabulary
   (vocabulary order in `graph/topics.json`) for instant lens filtering.
5. `nodes/<id>.json` — per-node payload fetched on demand: headline,
   tldr, prose (per edition via `editions/<edn>/<id>.json` overlay),
   sentence_claims map, conflicts, sources with locators, image asset
   hashes, cite key.
6. `panorama.json` — THE pre-baked exception (Part 08 owns its recipe):
   the landing view's node list, cluster labels, changelog delta anchors.
7. `search/index.bin` — compact client-side search index (id, title,
   tldr tokens), sharded hot/cold if it outgrows a few MB.
8. `html/<id>/index.html` — the real 2D page per node (Part 11).
9. `layout/epochs.json` — epoch metadata + the previous epoch's
   positions for the 800 ms crossfade (Part 03).
10. `pointer.json`, `manifest.json`, `build-health.html` — per Part 01.

Validator rule (Part 12): an export ships only if every file parses, all
cross-references resolve, all hashes match the manifest, and node/edge
counts match Neo4j's counts for the build's job id.

--------------------------------------------------------------------------------
2.11 WORKED EXAMPLE (END TO END, ABBREVIATED)
--------------------------------------------------------------------------------

The GLM 5.3 vs Mythos 5 story from the founding conversation, as data:

1. Sources: src-2026-0311 (AI Revolution video, `video`, secondary),
   src-2026-0312 (lab blog post, `official_blog`, primary),
   src-2026-0313 (press writeup, `press`, secondary; simhash shows NOT
   syndicated with 0312).
2. Claims include: clm-...-004 {text: "GLM 5.3 scored 84.5% on
   CyberGym", kind: numeric, value: 84.5, unit: "%", evidence:
   benchmarked, locator: t:73 of the video} with SAME_FACT_AS to the
   blog's matching claim (corroboration = 2); clm-...-009 {"Mythos 5
   scored 78.0% on ExploitBench"}; claim edges: the ExploitBench claims
   CONTRADICT nothing but SUPPORT the stance claim "detection and
   exploitation capability diverge".
3. Event: evt-2026-0142, headline "Finding bugs is not exploiting them:
   GLM 5.3 and Mythos 5 split the security pipeline", lifecycle
   `developing`, conflicts: [] (no contradiction — the two benchmarks
   measure different things, and the prose says exactly that, each
   sentence carrying its claim ids). TAGGED: can-security-evals (weight
   high, rare topic), can-open-weights (medium), can-benchmarks (hub —
   page link only, no layout edge).
4. Later: three more events cite its claims; citation inflow raises
   importance (Part 08); the durable insight crystallizes into canon
   node can-detection-vs-exploitation with ABSORBED_INTO edges; the
   event drifts to `absorbed`, keeps its page, its cite key AP-2026-0142,
   and its place in history.

--------------------------------------------------------------------------------
2.12 POINTERS
--------------------------------------------------------------------------------

How positions and w are computed: Part 03. How nodes.bin is rendered at
72 fps: Part 04. How claims are extracted and verified, and who approves
what: Part 06. How importance/prominence/lifecycle transitions are
scored: Part 08. Benchmark card governance and snapshot cron: Part 09.
Edition generation and the faithfulness scoreboard: Part 10. How
nodes/<id>.json becomes hover-provenance UI and real HTML pages: Part 11.

================================================================================
END OF PART 02
================================================================================
