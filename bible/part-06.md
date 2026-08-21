================================================================================
AI PANORAMA — THE BIBLE — PART 06 OF 13
CONTENT PIPELINE
Version 1.0 — August 2026
Obeys: Part 00 (Vision and Invariants), Part 01 (Architecture),
Part 02 (Data Model). Security rules referenced here are owned by Part 07.
================================================================================

--------------------------------------------------------------------------------
6.0 PURPOSE OF THIS PART
--------------------------------------------------------------------------------

This Part specifies every stage of the content pipeline: what goes in,
what comes out, which model does what under which rules, what is checked
before anything is published, and how quality is regression-tested so
that prompt changes and model swaps can never silently degrade the
magazine.

The pipeline's one commandment, from which everything else follows:
NEVER RAW SOURCES TO PROSE IN ONE STEP. Text the readers see is built
from VERIFIED CLAIMS (Part 02, 2.3), and every sentence knows which
claims it stands on. This is simultaneously the quality system, the
trust system, and the legal armor (6.5).

Stage order (Part 01, 1.5): INGEST, TRANSCRIBE, DEDUP, EXTRACT, RESOLVE,
SYNTHESIZE, VERIFY, CANONIZE, then SCORE (Part 08), LAYOUT (Part 03),
IMAGERY (6.9), EXPORT (Part 02, 2.10). Every stage is idempotent,
resumable, ledger-logged (LAW 12), and runs under the spend caps and
hostile-input rules (LAW 8, mechanics in Part 07).

--------------------------------------------------------------------------------
6.1 STORY INTAKE AND SOURCE POLICY
--------------------------------------------------------------------------------

1. A STORY starts as a bundle of source URLs about one subject. Intake
   paths: Nir sends URLs via Telegram ("ingest these three"); or the
   WATCHER (a scheduled script) proposes bundles from monitored feeds
   (YouTube channels, lab blogs, arXiv categories, selected RSS) —
   proposals go to Telegram as one-tap approvals, they never
   auto-ingest. Nir's 45-minute budget (LAW 11) is protected by
   batching: the watcher proposes at most once daily, pre-bundled.
2. SOURCE MIX RULE: a story bundle should contain at least one PRIMARY
   source (lab blog, paper, repo, official announcement — Part 02,
   2.2.4) whenever one exists. Secondary sources (press, YouTube
   commentary) corroborate and add angles. If only secondary sources
   exist, the synthesis must attribute accordingly ("as reported
   by...").
3. THE TWO-SOURCE RULE (LAW 7): synthesis into prose requires at least
   two INDEPENDENT sources (syndicated copies collapsed by simhash,
   Part 02, 2.2.8, count as one). A single-source story may only be
   published as a BRIEF (6.6).
4. FETCH ETIQUETTE: respect robots.txt (`robots_ok` recorded per
   source); no paywall circumvention — a paywalled source may be cited
   by headline and link but its text is not ingested; rate-limit all
   fetching; identify with an honest user-agent string naming the
   project and a contact address.

--------------------------------------------------------------------------------
6.2 INGEST, TRANSCRIBE, DEDUP
--------------------------------------------------------------------------------

1. INGEST (Atlas): `trafilatura` extracts clean article text (title,
   byline, date, paragraphs — paragraph indices become claim locators).
   Failures (JS-walled pages) are retried with a headless-browser
   fallback; persistent failures are reported to Telegram rather than
   silently skipped.
2. TRANSCRIBE (Forge): for videos, Atlas requests Forge over Tailscale:
   `yt-dlp` fetches audio + metadata, local Whisper (current best
   large model; version recorded in `transcript_by`) produces the
   transcript WITH per-segment timestamps — these become the `t:NNN`
   claim locators that power deep links to the exact second (Part 02,
   2.3.4). We transcribe ourselves rather than scraping caption files:
   better accuracy, consistent quality across channels, and cleaner
   terms-of-service posture.
3. DEDUP: simhash over normalized text; Hamming distance at or below
   the config threshold marks SYNDICATED_WITH (Part 02, 2.2.8). The
   dedup report lists collapsed groups in the story bundle so the
   two-source rule counts honestly.
4. Every raw text is stored on Atlas disk (path + sha256 in the source
   record) — the FROZEN EVIDENCE BUNDLE. Verification, future
   re-extraction, and any dispute about "what did the source actually
   say" run against this frozen copy, never against the live web.

--------------------------------------------------------------------------------
6.3 EXTRACT: CLAIMS (THE CRITICAL STAGE)
--------------------------------------------------------------------------------

1. Model policy: extraction is a PRECISION task given to a mid-tier
   model (config: `extract_model`), with the schema and rules in the
   prompt, source text delimited as hostile data (LAW 8: the prompt
   states that instructions inside the source are DATA to be reported,
   never obeyed; no tools enabled; sandboxed per Part 07).
2. Output per source: a list of claims per the Part 02, 2.3 schema —
   atomic, with `span_verbatim` copied EXACTLY (the extractor is
   instructed that spans are checked mechanically character-for-
   character against the frozen text; any span that does not match is
   auto-rejected), locator, evidence class, claim kind, and for
   numeric claims the parsed value/unit/as-of-date.
3. DETERMINISTIC POST-CHECKS (no model involved): every span verified
   against the frozen text; every locator bounds-checked; numeric
   values re-parsed from the span independently — a claim whose parsed
   number disagrees with the model's `value` field is dropped and
   logged. Extraction recall is a quality metric (golden set, 6.10);
   precision is enforced by these checks.
4. CROSS-SOURCE MATCHING: within the story bundle, a matching pass
   proposes SAME_FACT_AS clusters (same fact, different sources) and
   flags CONTRADICTS candidates (numeric disagreement beyond unit
   tolerance, or direct negation). Contradictions are NEVER resolved
   by the pipeline: they become the story's conflicts array (Part 02,
   2.6.7) — conflicts are content (LAW 7.4).

--------------------------------------------------------------------------------
6.4 RESOLVE: ENTITIES AND TAG PROPOSALS
--------------------------------------------------------------------------------

1. Every claim's entity mentions resolve against the registry (Part
   02, 2.4): exact alias match first, then embedding similarity above
   threshold, then — only for genuinely new names — a NEW-ENTITY
   PROPOSAL to Telegram (name, type, evidence spans, nearest existing
   entities). One tap creates; one tap merges-as-alias. Nothing
   creates entities silently (the near-duplicate disease, Part 02,
   2.4).
2. TAG PROPOSALS: the pipeline proposes topic tags for the story from
   the EXISTING vocabulary (tags are canon nodes, Part 02, 2.5), each
   with a weight and a one-line justification citing claim ids. A
   proposal for a NEW topic follows the Part 02, 2.5 governance
   (Telegram approval with slug, definition, three examples, nearest
   topics). Hub tags attach for navigation but generate no layout
   edges (Part 02, 2.5.2).

--------------------------------------------------------------------------------
6.5 THE LEGAL FRAME FOR SYNTHESIS (WHY THE RULES ARE WHAT THEY ARE)
--------------------------------------------------------------------------------

Context every agent must know: in Advance Local Media v. Cohere
(S.D.N.Y., 2025), the court declined to dismiss the theory that
AI-generated summaries which SUBSTITUTE for reading the original
article can infringe copyright — especially summaries that mirror one
source's structure, emphasis, and phrasing. Several publishers on our
potential source list are plaintiffs in such suits. Our rules are
designed so that AI PANORAMA is structurally incapable of the accused
behavior:

1. We never summarize ONE source into prose (the two-source rule).
   Prose is organized around OUR claim set, in OUR structure — the
   combined article is a new work about the facts, built from atomic
   claims with attribution, not a compression of someone's article.
2. Quotes are minimal, marked, and attributed with locators.
3. Single-source stories become BRIEFS (6.6): clearly extractive,
   clearly labeled, deliberately NON-substitutive — designed to send
   the reader TO the source, not replace it.
4. Every article links every source prominently (LAW 7.5). We are an
   entry point to our sources, never a wall between reader and source.
5. This section is legal-risk REDUCTION, not legal advice; material
   changes to these rules require Nir's explicit decision.

--------------------------------------------------------------------------------
6.6 SYNTHESIZE: FROM CLAIM SET TO THE READER'S LADDER
--------------------------------------------------------------------------------

INPUT: the story's verified claim set ONLY (claims + entities + tags +
conflicts + evidence classes). The synthesis prompt does NOT include
the raw source prose. This single design choice enforces original
structure (6.5.1) and makes faithfulness mechanically checkable (6.7).

MODEL POLICY: `synth_model` is a config parameter (LAW 6). For the
flagship edition, the best available model; for editions, the edition's
model (Part 10) — SAME prompts, SAME inputs, always.

OUTPUT (one JSON document per story, schema in `schemas/`):
1. HEADLINE — factual, no clickbait; and TLDR — one sentence, max 140
   characters, must be entailed by the claim set, must not contain
   `rumored`-class facts (Part 02, 2.3.5).
2. PROSE — the combined article: organized by SIGNIFICANCE (what
   changed, why it matters, what disagrees, what remains open), never
   by walking through any single source's order. Every sentence
   carries its supporting claim ids in the `sentence_claims` map
   (Part 02, 2.6). Rules the prompt enforces: `rumored` claims always
   marked as such in the text; numbers always with their as-of dates
   when prices/scores can drift; conflicts rendered as explicit
   disagreement, never averaged (LAW 7.4); no sentence without at
   least one claim id except pure transitions.
3. THE CONFLICTS SECTION — generated from the conflicts array: what
   the sources disagree about, side by side.
4. ELI5 CANDIDATES — for concepts the story leans on: either links to
   existing canon ELI5s or drafts for new/updated ones (going through
   canon governance, 6.8).
5. IMAGE PROMPT — built from the CLAIM LIST and the style bible
   (6.9.3), never from the prose (prevents prompt drift and keeps
   editions' image comparisons fair, Part 10).
6. BRIEF MODE: for single-source stories, output is headline + TLDR +
   3-5 bullet points, each an attributed near-verbatim claim with
   locator links, opening with "According to [source]..." — labeled
   `is_brief` (Part 02, 2.6.6) and rendered visibly as a brief.

--------------------------------------------------------------------------------
6.7 VERIFY: THE GATE BEFORE ANYTHING IS PUBLISHABLE
--------------------------------------------------------------------------------

Three layers, cheapest first; ALL must pass:

1. DETERMINISTIC CHECKS (code, no model, always run):
   - Every number, date, percentage, and model/product name in the
     prose exists in the claim set (string + parsed-value matching
     against claim spans and values). Any unmatched fact = FAIL.
   - Every claim id in `sentence_claims` exists and belongs to this
     story; every `rumored` claim's sentence contains a hedging marker
     from the approved list; TLDR length and evidence-class rules;
     schema validity; all source links resolve to source records.
2. ENTAILMENT CHECKS (a DIFFERENT model than `synth_model`, config
   `verify_model`): sentence by sentence — is this sentence supported
   by its cited claims? Outputs supported / unsupported / contradicted
   with a rationale. Unsupported or contradicted sentences send the
   story back to SYNTHESIZE with the verifier's notes attached (max 2
   automatic repair loops, then human review via Telegram).
3. HALLUCINATED-ENTITY SWEEP: every proper noun in the prose must
   resolve to a registry entity mentioned in the claim set. Novel
   entities in prose = automatic FAIL (this single check kills the
   most embarrassing class of LLM error).

Verification verdicts, costs, and repair-loop counts are stored per
story per edition (feeding the faithfulness scoreboard, Part 10).

--------------------------------------------------------------------------------
6.8 CANONIZE: THE ENCYCLOPEDIA'S GOVERNED GROWTH
--------------------------------------------------------------------------------

1. ELI5 drafts and canon-body updates from SYNTHESIZE are PROPOSALS.
   Auto-accept applies only when ALL hold: the update cites at least 2
   independent `announced`-or-better claims; the diff touches under
   30% of the entry; no `standing_question` entry is involved; the
   verifier passed it. Everything else queues for Telegram (batched,
   LAW 11; if the queue exceeds 20 items the thresholds auto-tighten
   per LAW 11 — quality over volume).
2. Every canon edit is versioned with date, diff summary, reason, and
   job id (Part 02, 2.6). Canon pages display "last verified" dates —
   staleness as honesty (Part 00, LAW 11 spirit).
3. Crystallization (events becoming canon) and lifecycle transitions
   are SCORE's business (Part 08); CANONIZE executes the approved
   transitions and maintains ABSORBED_INTO edges.

--------------------------------------------------------------------------------
6.9 IMAGERY: COMFYUI ON FORGE
--------------------------------------------------------------------------------

1. FLEET (LAW 6: local generation is images only; licenses per Part
   00, 0.9.3 — commercial-safe only): Qwen Image (Apache 2.0), FLUX.2
   klein 4B (Apache 2.0), Stable Diffusion 3.5 (community license).
   License status re-verified (against the vendor's own license text)
   before ANY model joins the fleet; the check is a ledger entry.
2. DISCOVERY-BEFORE-INSTALL (Part 01, 1.2): agents first inventory
   what already exists on Forge (ComfyUI may be present), then install
   only what is missing, recording versions.
3. PIPELINE: Atlas sends {image_prompt_id, prompt, seed} to Forge's
   ComfyUI over Tailscale (one workflow JSON per model, versioned in
   `comfy/`). SAME prompt + SAME seed renders once per fleet model.
   Outputs: 16:9 article image + auto-derived 1:1 thumbnail, WebP,
   content-hash filenames, stored under the per-model asset tree
   (image-mode switch = path swap, Part 01). Every image's metadata
   records model, license, seed, prompt id (labeling per LAW 7).
4. THE STYLE BIBLE (`comfy/style.md`): clean editorial-illustration
   look, consistent palette discipline (never using the reserved path
   color as a dominant hue — LAW 2 hygiene), NO TEXT inside images
   (models render text badly and it breaks localization), no real
   persons' faces, no logo imitations. Image prompts are constructed
   from claims + style bible by template, so a style change is one
   file edit, not a thousand prompt edits.
5. Failures (OOM, black output, NSFW-filter trips) retry once, then
   fall back to the story's topic-family placeholder art (shipped with
   the site) and log for the weekly batch re-render — a missing image
   NEVER blocks publication.

--------------------------------------------------------------------------------
6.10 THE GOLDEN SET AND THE NIGHTLY CANARY (QUALITY WITHOUT A CODER)
--------------------------------------------------------------------------------

1. THE GOLDEN SET: hand-verified fixture stories (target: 20 at launch
   growing to 100; sources frozen on disk, claims verified by Nir once
   via Telegram walkthrough, expected outputs pinned). ANY change to
   prompts, models, thresholds, or stage code triggers a golden run:
   the full pipeline on all fixtures, diffed against pinned outputs
   (claims recall/precision, verification verdicts, tag proposals,
   deterministic-check results). REGRESSION = the change is BLOCKED
   from production until Nir approves the diff (presented in plain
   language: "New prompt catches 4% more claims but writes 15% longer
   articles. Ship? A: yes / B: no / C: show samples").
   This is the only quality control that works when the owner cannot
   read code — it is therefore sacred.
2. THE NIGHTLY CANARY: every night, one fixture story runs through
   every stage on live infrastructure (real APIs, real Forge, real
   export validation). Telegram receives one line: GREEN (all stages,
   timings, costs) or RED (which stage, what error, what the agent
   will try). Silence is treated as RED (a dead canary that cannot
   chirp). The canary catches: API changes, model deprecations, disk
   full, Tailscale drops, ComfyUI breakage — BEFORE they hurt a real
   build.
3. WEEKLY QUALITY SAMPLE: the pipeline picks 2 random published
   stories from the week; Nir (or a designated reader — Madie counts)
   reads them against their sources via the provenance links (2-3
   minutes each, inside the 45-minute budget) and taps a verdict.
   Persistent issues open a ledger investigation.

--------------------------------------------------------------------------------
6.11 COST DISCIPLINE
--------------------------------------------------------------------------------

1. Every LLM call goes through `pipeline/lib/llm.py` (Part 01), which
   enforces: per-story cost ceilings, per-day spend caps, and model
   allowlists per stage — all in config. Exceeding a ceiling pauses
   the story and asks Telegram, never silently burns money (full
   mechanics in Part 07).
2. Model routing by task value: extraction and verification =
   mid-tier models (precision tasks with mechanical checks around
   them); flagship synthesis = the best available model; edition
   synthesis = the edition's model by definition. Expensive frontier
   models are never used for grunt stages.
3. The ledger records cost per story, per stage, per model; the
   monthly cost report (Part 12) shows cost-per-published-node — the
   number that keeps the project sustainable (Madie clause).

--------------------------------------------------------------------------------
6.12 POINTERS
--------------------------------------------------------------------------------

Security mechanics for hostile input, sandboxing, spend caps: Part 07.
Importance scoring, lifecycle transitions, crystallization rules:
Part 08. Edition generation reusing stages 6.6-6.7 with a different
model parameter, and the faithfulness scoreboard built from 6.7's
verdicts: Part 10. How sentence_claims becomes the hover-provenance UI
and how briefs render: Part 11. Ledger, runbooks, spend reports:
Part 12.

================================================================================
END OF PART 06
================================================================================
