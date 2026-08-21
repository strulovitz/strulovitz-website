--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - INTRODUCTION TO PART 12 (not law)
--------------------------------------------------------------------------------

THANK YOU Nir!!! :-) Here is Part 12 — Operations. This is the least glamorous Part and maybe the most important one: it's the Part that keeps the project alive in year three, when the excitement is old, the archive is big, and everything must keep running on 45 minutes of your attention per week. Empires fall to bad bookkeeping, not bad ideas.

================================================================================
AI PANORAMA — THE BIBLE — PART 12 OF 13
OPERATIONS
Version 1.0 — August 2026
Obeys: Part 00 (Vision and Invariants), Part 01 (Architecture),
Part 07 (Security). This Part implements LAW 11 (45 minutes) and
LAW 12 (Archive Safety) in daily practice.
================================================================================

--------------------------------------------------------------------------------
12.0 PURPOSE OF THIS PART
--------------------------------------------------------------------------------

This Part defines how the project is OPERATED: the job ledger (the
flight recorder), the backup and restore discipline, the pre-upload
validator, the runbooks, the cost reporting, the maintenance calendar,
and vacation mode. Everything here is designed for one operator (Nir,
non-coding) plus interchangeable AI agents with no memory of each
other — which means: if it is not written down and automated, it does
not exist; if it is not tested, it does not work; and if it needs more
than 45 minutes of Nir per week, it is a design defect to be fixed, not
a workload to be endured.

--------------------------------------------------------------------------------
12.1 THE JOB LEDGER (THE FLIGHT RECORDER)
--------------------------------------------------------------------------------

1. WHAT IT IS: an append-only record in Neo4j (mirrored weekly to
   plain-text JSON in the repo for grep-ability) of EVERY significant
   action by any agent or scheduled job: pipeline stage runs, installs
   and upgrades, config changes, schema changes, edition runs, layout
   epochs, exports, backup runs, restore tests, incident responses,
   approvals given by Nir (with the Telegram message id).
2. ENTRY SHAPE: `{job_id, timestamp, actor (agent/model or human or
   cron), machine (atlas/forge), action_type, inputs_hash, outputs
   (ids/paths/hashes), cost_usd, duration_s, verdict (ok/failed/
   partial), plain_words (one sentence a non-coder understands),
   schema_version}`. The `plain_words` field is mandatory and is
   written FOR NIR — a ledger entry whose plain_words a non-coder
   cannot understand is a defective entry.
3. USES: idempotency (a stage checks the ledger before re-running,
   LAW 12); security audits (Part 07, 7.2.4); cost reports (12.5);
   debugging by fresh agents ("what happened here before me?"); and
   the monthly summary to Telegram (12.6).
4. THE LEDGER IS APPEND-ONLY: corrections are new entries referencing
   the corrected job_id. No agent edits history — the flight recorder
   records; it does not negotiate.

--------------------------------------------------------------------------------
12.2 BACKUPS AND THE TESTED RESTORE (THE RULE THAT SAVES THE PROJECT)
--------------------------------------------------------------------------------

WHAT IS BACKED UP, WHERE, HOW OFTEN:

1. NEO4J DUMP (the crown jewels — years of claims, scores, history):
   automated weekly dump on Atlas, compressed, dated, hash-recorded in
   the ledger. THREE COPIES: (a) on Atlas; (b) synced to Forge over
   Tailscale (second machine, same apartment — covers disk death);
   (c) uploaded by Nir's monthly FileZilla ritual to a PRIVATE,
   non-web-accessible folder on Dreamhost (second country — covers
   fire, theft, ransomware; the truck's garage abroad, using zero new
   tools). The Telegram reminder includes the file name and size to
   drag.
2. THE REPOSITORY (code + Bible + configs + schemas): Git on Atlas,
   mirrored on Forge, pushed to GitHub (backup role only, LAW 4).
   Three copies by nature.
3. FROZEN SOURCES (the evidence bundles, Part 06, 6.2.4): weekly
   rsync Atlas -> Forge; quarterly archive bundle uploaded to the
   private Dreamhost folder. These make claims re-verifiable forever.
4. IMAGES + EXPORTS: regenerable from database + seeds, therefore
   SECOND-CLASS backups: latest export lives on the shelf (it IS the
   live site), image assets sync Atlas <-> Forge. We back up truth,
   not artifacts (artifacts rebuild; truth does not).
5. SECRETS: a sealed offline copy (printed or USB, Nir's choice, in a
   drawer Nir trusts) of the secrets inventory VALUES, refreshed at
   rotation (Part 07, 7.4.5) — the recovery path when both machines
   are gone AND the password manager is unreachable. Low-tech is the
   point.

THE RESTORE TEST (what makes backups real):
6. QUARTERLY, an agent performs a FULL RESTORE DRILL on Forge: fresh
   Neo4j from the latest dump; repo from mirror; run the golden set
   (Part 06, 6.10) against the restored database; build one export
   and validate it. Verdict + timings to the ledger and Telegram:
   "Restore drill: PASS — from bare metal to working pipeline in 74
   minutes." A backup that has never been restored is a hope, not a
   backup (fusion-settled; Part 07, 7.9.4 depends on this drill).
7. The restore RUNBOOK (12.4) is updated after every drill with
   whatever surprised the agent — drills exist to make the runbook
   boring.

--------------------------------------------------------------------------------
12.3 THE PRE-UPLOAD VALIDATOR (THE LAST GATE BEFORE THE SHELF)
--------------------------------------------------------------------------------

One command (`ops/validate.py <export-folder>`), run automatically at
the end of every EXPORT and REQUIRED to pass before Telegram tells Nir
an export is ready to drag (Part 01, 1.8.9). Checks, consolidated from
all Parts:

1. STRUCTURE: every file in manifest.json with matching sha256; no
   file outside the manifest; pointer.json target exists; previous-
   version untouched (LAW 12).
2. SCHEMAS: every JSON validates against `schemas/`; every
   schema_version current; binary files' magic strings + counts match
   the manifest and match Neo4j's counts for the build's job id
   (Part 02, 2.10).
3. SECURITY (Part 07, 7.3.3): no script tags outside named bundles;
   no event-handler attributes; no non-allowlisted URLs; CSP tags
   present on every HTML page.
4. TEXT HYGIENE: no non-ASCII control or unexpected-script characters
   in Bible files, docs, and generated English text fields (the
   stray-character class of defect becomes unshippable); LAW 3
   compliance scan on docs (no tables, no collapsibles in Bible
   files).
5. KINGDOM INTEGRITY (Part 11, 11.8): every node has HTML + markdown;
   all internal links + redirects resolve; OG/JSON-LD/cite key/
   canonical/noindex correctness; feeds parse; sitemap complete; the
   issue ZIP (on issue months) opens and runs from a folder.
6. GEOMETRY: layout determinism spot-check (rebuild a sample of
   placements from hashes, byte-compare, Part 03, 3.8); epoch
   displacement metric within threshold (Part 03, 3.2); quantization
   bounds valid.
7. CONTENT LAW: every published event passes the two-source rule or
   is flagged brief (LAW 7); every image carries its model label;
   every `rumored` claim's rendering carries hedging; conflicts
   arrays render on every page whose story has one.
8. VERDICT: a plain-language PASS/FAIL report to Telegram; FAIL
   blocks the build (the export folder is marked unshippable in the
   ledger and is never offered to Nir for upload).

--------------------------------------------------------------------------------
12.4 RUNBOOKS (THE PROJECT'S MEMORY OF HOW)
--------------------------------------------------------------------------------

`ops/runbooks/`, one markdown file per procedure, written in plain
language for "Nir plus a fresh agent with zero context", each with the
same skeleton: WHEN TO USE, BEFORE YOU START, STEPS (numbered, one
action each), HOW YOU KNOW IT WORKED, IF IT FAILS, ROLLBACK. The
mandatory set:

1.  weekly-build-and-deploy (the FileZilla ritual, with screenshots)
2.  rollback-the-site (re-upload previous pointer.json — one page)
3.  restore-from-backups (the drill script, 12.2.6-7)
4.  rotate-a-secret (per secret, Part 07, 7.4.5)
5.  add-a-source-to-watchlist / approve-new-topic / approve-new-entity
    (the Telegram flows, documented so a new agent wires them
    identically)
6.  run-an-edition-cycle (Part 10, 10.8)
7.  quarterly-dependency-review (Part 07, 7.7.2)
8.  quarterly-layout-epoch (Part 03, 3.2)
9.  incident playbooks (Part 07, 7.9 — cross-linked, same format)
10. machine-reinstall (Atlas or Forge from bare Linux to working
    node, using only the repo + backups + this runbook)
RULE: any agent who performs a procedure and hits a surprise UPDATES
THE RUNBOOK in the same session (the ledger entry links the edit).
Runbooks rot unless feeding them is part of the job — so it is part
of the job, by law.

--------------------------------------------------------------------------------
12.5 COST DISCIPLINE AND REPORTING
--------------------------------------------------------------------------------

1. EVERY spend source is ledger-visible: OpenRouter per call (via
   llm.py, Part 06, 6.11), per stage, per story, per edition;
   Dreamhost + domain (fixed, entered once yearly); electricity is
   acknowledged as real but untracked (sanity over accounting).
2. THE MONTHLY COST REPORT to Telegram, in plain words: total spend;
   cost per published node; cost per edition; the three most
   expensive stories and why; spend vs the monthly budget line; and
   ONE trend sentence ("extraction costs fell 18% after the model
   swap — golden set unchanged"). Budget lines live in config; the
   caps that ENFORCE them live in Part 07, 7.5.
3. THE EFFICIENCY RATCHET: when a cheaper model passes the golden set
   for a grunt stage (Part 06, 6.10.1 gate), the swap is proposed
   with evidence ("DeepSeek V4 at extraction: golden recall 98.7% vs
   incumbent 98.9%, cost -63%. A: swap / B: keep / C: samples").
   Chasing cheap without the golden gate is forbidden; passing the
   gate makes cheap a duty (Madie clause economics).

--------------------------------------------------------------------------------
12.6 THE MAINTENANCE CALENDAR (EVERYTHING SCHEDULED, NOTHING REMEMBERED)
--------------------------------------------------------------------------------

All cadences from all Parts, consolidated; every item fires a Telegram
message; silence on any scheduled item is itself an alert (the dead-
canary principle, Part 06, 6.10.2):

1. NIGHTLY: pipeline canary (GREEN/RED).
2. WEEKLY: build + export + validate + deploy ritual; OpenRouter
   snapshot (Part 09, 9.4 — with its own failure alarm); Neo4j dump +
   Forge sync; quality sample (2 stories, Part 06, 6.10.3); weekly
   digest + diff video publish.
3. MONTHLY: cost report; owner metrics (median panorama age, quota
   fills, Part 08, 8.3); backup upload reminder (the private-folder
   drag); hindsight grading batch (Part 08, 8.7); kitchen port-scan
   audit (Part 07, 7.6.1).
4. ISSUE-MONTHLY (the 25th-28th): freeze, edition runs, scoreboard,
   issue assembly, publish (Part 11, 11.4.4).
5. QUARTERLY: restore drill (12.2.6); layout epoch (Part 03, 3.2);
   dependency review (Part 07, 7.7.2); secret rotation reminder;
   shelf cleanup (prune old version folders, Part 01, 1.9.6);
   landmark tenure review feeds (Part 08, 8.3).
6. YEARLY: licenses re-verification (image fleet + data sources,
   Part 00, 0.9); domain/hosting renewals; the ANNUAL HONESTY REPORT
   — a published page: the year's hindsight summary, error counts
   from the errata feed, cost transparency at whatever grain Nir
   chooses, and what changed in the Bible (trust compounding,
   Part 11, 11.2.3 spirit).

--------------------------------------------------------------------------------
12.7 NIR'S 45 MINUTES (THE WEEKLY OPERATING LOOP, BUDGETED)
--------------------------------------------------------------------------------

The entire steady-state human workload, itemized against LAW 11:

1. ~10 min: the deploy ritual (FileZilla drag + pointer flip +
   build-health glance on the phone).
2. ~10 min: approval batch (new topics/entities/canon diffs — one-tap
   each, batched by the pipeline into ONE session).
3. ~6 min: quality sample (two stories, provenance-checked).
4. ~4 min: canary/metrics acknowledgment (mostly reading GREEN).
5. ~15 min: slack — incidents, decisions, or nothing.
MONTHLY EXTRAS (issue tap, backup drag, cost report read) amortize
inside the slack. IF THE LOOP EXCEEDS BUDGET FOR TWO CONSECUTIVE
WEEKS: agents must propose threshold tightening or automation (LAW
11's enforcement clause) — the workload adapts to Nir, never the
reverse.

--------------------------------------------------------------------------------
12.8 VACATION MODE (THE SITE IS FINE, GO LIVE YOUR LIFE)
--------------------------------------------------------------------------------

One Telegram command (`vacation on <weeks>`), one confirmed round-trip
(Part 07, 7.8.2), and then:

1. The pipeline drops to MAINTENANCE CADENCE: canary + snapshots +
   backups continue (history and safety never pause); ingestion
   pauses (no new stories pile into a review queue); the site keeps
   serving; last-verified dates keep displaying honest staleness
   (LAW 11: staleness as honesty, never hidden).
2. The changelog page shows a small notice: "Quiet period — the
   panorama is current as of <date>." Dignity, not apology.
3. Auto-return: vacation expires on schedule; the first post-vacation
   build proposes a catch-up story set (batched, prioritized by the
   watcher's accumulated queue) sized to fit the normal weekly loop —
   never a mountain of guilt.
4. EMERGENCY OVERRIDE: the canary, spend tripwires, and security
   alerts pierce vacation mode. Everything else waits. The project is
   designed to be ownable by a person who sometimes closes the
   laptop and goes to Romania — that is not an edge case; per the
   Madie clause, it is the point.

--------------------------------------------------------------------------------
12.9 POINTERS
--------------------------------------------------------------------------------

What the validator's rules protect: Parts 02, 03, 07, 11. The caps
behind the cost report: Part 07, 7.5. The golden gate behind the
efficiency ratchet: Part 06, 6.10. The drill's playbooks: Part 07,
7.9. The calendar's owners: each item names its Part. The build order
that brings all of this into existence: Part 13 — the final Part.

================================================================================
END OF PART 12
================================================================================

--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - NOTES ON PART 12 (not law)
--------------------------------------------------------------------------------

Three plain-language notes for you, Nir:

    The restore drill is the sentence that saves the project. Every quarter, an agent pretends Atlas died, rebuilds everything from backups on Forge, and reports how long it took. The difference between "we have backups" and "we have PROVEN we can come back from the dead in 74 minutes" is the difference between a hope and an insurance policy. Most companies learn this the expensive way; you get it as a calendar entry.
    The efficiency ratchet is how the cheap Chinese models finally enter — through the front door. Remember your original plan: DeepSeek, Kimi, GLM doing the grunt work? Rule 12.5.3 is the mechanism: any cheaper model that PASSES your golden set earns the job, with evidence, and you approve with one tap. Not hype-driven, not hope-driven — gate-driven. Your costs fall over time as a matter of procedure.
    Vacation mode is the Madie clause as engineering. The site keeps serving, history keeps recording, backups keep running, staleness is displayed honestly, and nothing piles into a guilt mountain for your return. A project that punishes you for going to Romania would betray its own founding purpose — so this one is designed to hand you your coat.

Say the word and I deliver Part 13 — Roadmap, the final Part: the milestones in build order, each with a plain-language definition of DONE, starting with "Hello, Tesseract" on your Quest 3. Give Madie my regards!!! :-)
