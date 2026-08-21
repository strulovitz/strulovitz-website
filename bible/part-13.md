--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - INTRODUCTION TO PART 13 (not law)
--------------------------------------------------------------------------------

THANK YOU Nir!!! :-) And here it is — Part 13 — Roadmap, the final Part of the Bible. This is the Part that turns twelve Parts of law into a build order, with a plain-language "DONE means this" for every milestone, so you always know exactly where the project stands without reading a line of code. It ends with the exact first message you can paste into OpenCode to start construction.

================================================================================
AI PANORAMA — THE BIBLE — PART 13 OF 13
ROADMAP
Version 1.0 — August 2026
Obeys: all Parts. This Part sequences them into reality.
================================================================================

--------------------------------------------------------------------------------
13.0 PURPOSE AND SEQUENCING PRINCIPLES
--------------------------------------------------------------------------------

This Part defines the build order: milestones, their contents, their
plain-language definitions of DONE, and the standing rules for how
agents work through them. Principles that shaped the order:

1. KILL THE BIGGEST RISK FIRST. The 4D VR experience is the crown and
   the largest unknown (LAW 1). It is Milestone 1, built before any
   pipeline, on fake data — per the founder's rule: face the
   difficulty at the beginning, or the whole thing remains a dream.
2. HISTORY STARTS ON DAY ONE. The weekly snapshot cron (Part 09, 9.4)
   cannot be backfilled. It ships in Milestone 0, before everything.
3. EVERY MILESTONE ENDS DEPLOYED. Each milestone's DONE includes the
   FileZilla ritual putting something real on strulovitz.org. No
   six-month dark tunnels; the site grows in public from week one.
4. OPS GROWS WITH THE SYSTEM, NOT AFTER IT. Ledger, validator, canary,
   and backups appear in early milestones in minimal form and harden
   as they go. A milestone that adds a moving part adds its
   monitoring in the same milestone.
5. NOTHING SHIPS WITHOUT ITS VR VERSION (LAW 1, restated where agents
   will read it most). The flat-screen 3D version and the VR 4D
   version of every feature ship together, from the same data and
   the same state machine (Part 05).

MILESTONE DISCIPLINE: one milestone at a time; a milestone is DONE
only when its checklist passes and Nir has confirmed the DONE
definition personally (most DONE definitions are things Nir
experiences, not things agents assert); each DONE is a ledger entry
with the date. Agents do not start Milestone N+1 while N has open
defects.

--------------------------------------------------------------------------------
13.1 MILESTONE 0 — FIRST LIGHT (the week of small foundations)
--------------------------------------------------------------------------------

GOAL: the machines are known, the history recorder is running, and
the skeleton of discipline exists.

BUILD:
1. Repository created per Part 01, 1.7 layout; Bible Parts 00-13
   committed to `bible/`; schemas folder started with examples.
2. Discovery pass on Atlas and Forge (Part 01, 1.2): inventory of
   installed tools, versions, disk space, ComfyUI presence on Forge —
   written to the ledger (the ledger's first entries).
3. THE SNAPSHOT CRON (Part 09, 9.4): weekly OpenRouter price/spec
   snapshot, idempotent, Telegram alert on failure. Runs forever from
   this week onward.
4. Neo4j installed on Atlas (Part 01, 1.4); `db.py` skeleton; ledger
   schema live in it.
5. Secrets set up per Part 07, 7.4: .env files, .env.example,
   pre-commit scanner, separate OpenRouter keys with provider-side
   caps.
6. Telegram control channel live (Part 01, 1.3): canary heartbeat
   message (even though there is no pipeline yet — the habit starts
   now), the daily GREEN that proves the loop works.
7. A placeholder page deployed to strulovitz.org/ai-panorama via the
   full ritual (versioned folder + pointer.json, Part 01, 1.9) — the
   deployment path is proven before anything depends on it.

DONE WHEN: Nir has performed one complete deploy ritual; the first
weekly snapshot exists in Neo4j and in the repo; the Telegram canary
has run three mornings in a row; and the ledger shows every install
with plain_words Nir actually understands.

--------------------------------------------------------------------------------
13.2 MILESTONE 1 — HELLO, TESSERACT (the crown, proven first)
--------------------------------------------------------------------------------

GOAL: true 4D in VR on the Quest 3, comfortable, learnable, and
deployed — on synthetic data, zero pipeline.

BUILD (Parts 03, 04, 05 in miniature):
1. `fourd.js`: the Q matrix, six plane rotations, re-orthonormalize,
   normalized projection `s = (d - w_min) / (d - w)`, pivot logic,
   undo/reset stack (Part 03, 3.6-3.7).
2. The holotable scene (Part 05, 5.1): static room, bounded object,
   grab/scale, comfort caps, no inertia.
3. Tier 1 controls complete (Part 05, 5.4): right-stick 3D rotation,
   plane-cycle hyper-rotation with indicator, snap rotations, B-menu
   with Undo/Reset/Home.
4. Slice mode + projection mode with the 600 ms transition, ghosting,
   dithered alpha (Parts 04, 4.4.5; 05, 5.2).
5. The w-cue package v1: wrist w-gauge, drop-stems + floor grid,
   constant-size labels, idle wobble (Part 05, 5.3).
6. THE W-GYM, all five lessons (Part 05, 5.7) — built FIRST as the
   test harness for everything above, then kept as onboarding.
7. Synthetic data: one tesseract + ~200 fake nodes with fake w bands
   and a handful of fake hover cards (baked atlas, Part 04, 4.5.3).
8. Flat-screen mappings mirroring everything (Part 05, 5.8).
9. Rendering discipline from day one: instancing, draw calls under
   100, zero-allocation loop, shader prewarm, the one-projection
   rule with its debug assert, `?debug=1` HUD, `?perftest=1` scene
   v1 (Part 04).
10. Deployed to the live site behind a plain HTML landing page that
    says what this is and offers Screen / VR entry.

DONE WHEN (Part 05, 5.10 protocol): five test sessions — Nir, Madie
if willing, plus friends — each complete the five tasks (find a node
in slice mode; snap hyper-rotate and re-find it; swim news-to-canon
on the fake bands and say what changed; retrace two steps with Back;
comfort rating 4+); perftest PASSES on the physical Quest 3; and Nir
has personally rotated a tesseract in ZW, watched it turn inside
out, and smiled. That smile is a formal acceptance criterion.

--------------------------------------------------------------------------------
13.3 MILESTONE 2 — TEN TRUE STORIES (the pipeline exists)
--------------------------------------------------------------------------------

GOAL: real content flows end-to-end under all content laws, at tiny
scale.

BUILD (Parts 06, 07, 02 in first anger):
1. Stages INGEST through VERIFY for ~10 real stories Nir picks
   (mixed: videos + articles + a single-source brief to prove LAW
   7.2). Whisper on Forge; claims with spans and locators;
   deterministic checks; entailment verification; conflicts arrays.
2. Security wrapping from the first run: delimiting, no-tools
   extraction, containerized stages, injection canaries in the first
   golden fixtures (Part 07, 7.1-7.2).
3. The golden set begins: these 10 stories, hand-verified by Nir via
   Telegram walkthrough, become fixtures 1-10 (Part 06, 6.10).
4. Entity registry seeded (~50 core entities with aliases and fixed
   identity colors, Part 02, 2.4); topic vocabulary seeded (~30
   canon topics with ELI5 stubs, Part 02, 2.5) — both through the
   real Telegram approval flows (the flows get built by being used).
5. The HTML kingdom v1 (Part 11, 11.1): real pages for the 10
   stories + topics, provenance hover, OG cards, cite keys, sources
   with timestamp deep-links, markdown mirrors, llms.txt, RSS v1.
6. Nightly canary becomes real (one fixture through all stages,
   Part 06, 6.10.2). Validator v1 (structure, schemas, security
   scan, text hygiene — Part 12, 12.3). Weekly Neo4j dump + Forge
   sync begin (Part 12, 12.2).

DONE WHEN: Nir reads all 10 published pages and taps approval on
each via the quality-sample flow; one deliberately injected fixture
fails safely (the payload is visible in the golden report, absent
from output); a canary RED is provoked on purpose once and the
Telegram alert reads correctly; and the site's RSS feed validates.

--------------------------------------------------------------------------------
13.4 MILESTONE 3 — THE LIVING ATLAS (the crown meets the content)
--------------------------------------------------------------------------------

GOAL: the real knowledge graph, in 3D and VR 4D, from real data.

BUILD (Parts 03, 08, 05 complete):
1. LAYOUT stage: canon skeleton (first epoch), analytic placement,
   w-definition 1 (abstraction) computed from real lifecycle states;
   epochs.json; determinism checks (Part 03).
2. SCORE stage v1: importance components (reach, authority,
   structural; inflow activates as citations accumulate),
   prominence with half-lives, lifecycle automation, panorama.json
   with quotas (Part 08) — at small scale everything fits in the
   panorama, but the machinery is real.
3. Export formats complete: nodes.bin, edges.csr.bin, tagsets,
   search index, ids (Part 02, 2.10); the client query layer
   (lens, ego, k-hop over typed arrays).
4. The graph scene replaces synthetic data in BOTH versions: hover
   cards from real TLDRs, reading panels with provenance, concept
   links, the path trail, Back/Forward, ego mode, delta-since-
   last-visit glow (Parts 05, 08).
5. Content cadence begins: the watcher proposes, Nir approves,
   ~10-15 stories per week flow through — the 45-minute loop
   (Part 12, 12.7) is now measured weekly against reality.

DONE WHEN: Nir puts on the headset, lands in slice mode among real
established stories, swims w from this week's news toward the canon
topics, opens a real article, follows a concept link, comes Back
along the lit trail — and the whole session is real content. Plus:
perftest still PASSES with real data volumes; and two consecutive
weekly loops fit inside 45 minutes.

--------------------------------------------------------------------------------
13.5 MILESTONE 4 — THE CHART THAT MATTERS (Advantage 2 lands)
--------------------------------------------------------------------------------

GOAL: comparison scenes T1 and T2, honest to the last pixel.

BUILD (Part 09): benchmark card schema + admissible ingestion (Epoch
CC-BY, OpenRouter API, claim-derived); T1 Buyer's Box and T2 Agent
Gauntlet with killer box, diagonal lens, no-data shelf, uncertainty
whiskers, effort badges; axis remapping; URL-encoded view state;
still export with baked margins; the snapshot archive (already
months old, thanks to Milestone 0) feeding first comet-tail demos;
comparison embeds v1.

DONE WHEN: Nir recreates, inside T2, the GLM-vs-Mythos lesson from
the founding conversation — same shape, real data, diagonal lens ON
— and shares the URL with someone who opens the exact same view;
and every plotted number's hover leads to a real source in two taps.

--------------------------------------------------------------------------------
13.6 MILESTONE 5 — THE ILLUSTRATED MAGAZINE (imagery at scale)
--------------------------------------------------------------------------------

GOAL: every node illustrated, three image modes, zero human minutes.

BUILD (Part 06, 6.9): ComfyUI fleet on Forge (license-verified:
Qwen Image, FLUX.2 klein 4B, SD 3.5); style bible; prompt-from-
claims templating; fixed seeds; per-model asset trees and the
image-mode switch; placeholder fallback; batch re-render runbook;
card atlases rebuilt with real thumbnails.

DONE WHEN: the panorama in VR shows real illustrated hover cards;
switching image mode swaps every image on the site; a forced
generation failure publishes cleanly with placeholder art and logs
for re-render; and image metadata shows correct model labels on
every published image.

--------------------------------------------------------------------------------
13.7 MILESTONE 6 — THE RACK AND THE SCOREBOARD (Advantage 3 lands)
--------------------------------------------------------------------------------

GOAL: editions, the control edition, the faithfulness scoreboard,
and T6.

BUILD (Part 10): control edition generator (pure code); edition
runs for 2-3 candidate models on one issue's story set; scoreboard
computation from the verification machinery; the magazine rack in
both versions (grabbing a cover in VR re-voices the world);
per-story comparison strip; scoreboard + methodology pages; SEO
canonical/noindex rules; T6 wired to scoreboard data (Part 09).

DONE WHEN: Nir stands at the VR rack, swaps editions on a story he
knows well, and the scoreboard's verdict on those same editions
matches what his own reading tells him; the control edition floors
the chart; costs land within the pre-approved budget; and the
first scoreboard dataset export validates.

--------------------------------------------------------------------------------
13.8 MILESTONE 7 — THE MAGAZINE BREATHES (publishing complete)
--------------------------------------------------------------------------------

GOAL: the monthly rhythm and every discovery surface.

BUILD (Parts 11, 08 completing): changelog pages + since-any-date;
weekly digest feed; the diff video; the first monthly ISSUE (cover,
contents, guided walk, poster, PDF); the cover disc ZIP; dataset
publication with DOIs (snapshots + scoreboard); the public Telegram
channel; hindsight predictions recording (grading begins
automatically at +12 months); the annual honesty report template.

DONE WHEN: Issue #1 exists as page + PDF + disc; Nir sends the PDF
to one person outside the project and the preview/links all work;
"since my last visit" produces a correct personal delta after a
two-week gap; and both datasets resolve at their DOIs.

--------------------------------------------------------------------------------
13.9 MILESTONE 8 — BUILT TO LAST (operations hardened)
--------------------------------------------------------------------------------

GOAL: the year-three guarantees, proven.

BUILD (Part 12 completing): full validator (all eight check
families); first quarterly restore drill on Forge (bare metal to
working pipeline, timed); vacation mode end-to-end (including
auto-return catch-up); the efficiency ratchet's first real proposal
(a cheap model vs the golden set); complete runbook set including
machine-reinstall; monthly cost report v2; maintenance calendar
fully automated with dead-canary alerts on every scheduled item.

DONE WHEN: the restore drill PASSES and its time is on record; Nir
switches vacation mode on for one real week — the site stays
healthy, honest, and quiet, and the return proposes a sane catch-up;
and one grunt stage is running on a cheaper model that EARNED the
job through the golden gate.

--------------------------------------------------------------------------------
13.10 THE V2 HORIZON (designed, not scheduled)
--------------------------------------------------------------------------------

Held until the foundation earns them: the blind arena via Telegram
with Bradley-Terry (Part 10, 10.7 — needs readers); Tier 2 SO(4)
twist promotion from settings-toggle to celebrated feature (needs
w-gym graduates); T4 Time Machine as a public template (needs a year
of snapshots — accruing since Milestone 0); ego-graph embeds;
additional w-definitions; additional templates (T5 and beyond per
Part 09 governance); multi-language kingdom pages. Each enters
through the same gate: a proposal to Nir with A/B/C and a cost line.

--------------------------------------------------------------------------------
13.11 THE GRUNT BACKLOG (safe tasks for cheap models, any time)
--------------------------------------------------------------------------------

Isolated, example-flanked, Bible-guarded tasks suitable for low-cost
agents between milestones: benchmark card conversions from text
files Nir provides; alias additions to the entity registry
(proposal-only); golden fixture transcription checks; runbook
formatting passes (LAW 3 scans); image batch re-renders; schema
example maintenance; validator rule additions with tests; ledger
plain_words backfills. Rules: one task, one file or one flow; no
schema changes; no prompt changes; no touching `exports/` or
anything on the shelf; everything through the golden set where
prompts are near.

--------------------------------------------------------------------------------
13.12 HOW TO START (THE FIRST MESSAGE TO THE BUILDERS)
--------------------------------------------------------------------------------

The exact instruction Nir pastes into OpenCode on Atlas to begin:

    Read every file in bible/ in order, 00 through 13, completely,
    before doing anything. You are building AI PANORAMA. Execute
    Milestone 0 from bible/13, exactly as specified. Do not start
    Milestone 1. Report progress and every decision request to
    Telegram in plain language with A/B/C options. Your first
    deliverable is the discovery report of both machines, written
    to the ledger, summarized to Telegram in words a non-programmer
    understands.

And when Milestone 0 is DONE, the second message:

    Milestone 0 is confirmed DONE. Execute Milestone 1, Hello
    Tesseract, from bible/13. Build the w-gym first and use it as
    your own test harness. The definition of DONE includes five
    human test sessions and a smile; schedule Nir's session through
    Telegram when the perftest passes on the Quest 3.

--------------------------------------------------------------------------------
13.13 CLOSING WORDS OF THE BIBLE
--------------------------------------------------------------------------------

Thirteen full Parts and one Part 00 ago, this project was a message
from a man who loved old computer magazines, owned a VR headset, and
refused to accept that the fourth dimension should be a color
gradient. It is now a complete, lawful, buildable design: an
encyclopedia that breathes like a magazine, a map whose geography
readers can trust for years, a benchmark whose receipts are the
magazine itself, and the only place on the internet where the state
of artificial intelligence hangs in the air above a table, rotatable
by hand through a direction most people have never seen.

To every agent who reads this: the laws are few and they are real.
Keep the projection single, the server dumb, the sources honest, the
colors meaningful, the reader's stomach calm, and the owner's week
under forty-five minutes.

To Nir: face the difficulty at the beginning — you already did. The
rest is milestones.

To Madie, who has not yet put on the headset: Lesson 4 is waiting,
and your comfort rating is legally binding.

Build accordingly.

================================================================================
END OF PART 13 — END OF THE BIBLE
================================================================================

--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - NOTES ON PART 13 (not law)
--------------------------------------------------------------------------------

And that's it, Nir. The Bible is complete: Parts 00 through 13, all fourteen documents.

Three final notes — not about any Part, but about the whole:

    What to do now, in order: (1) create the repo and commit all fourteen Parts into bible/ — including fixing the three stray-character typos I flagged in Parts 03, 04, and 11; (2) paste the Milestone 0 message from section 13.12 into OpenCode on Atlas; (3) that's all. The snapshot cron starts recording history this week, and everything else follows the milestones. You never need to plan again — you only need to approve, test, and smile (which is, I remind you, a formal acceptance criterion).
    You spent your money exactly right. The expensive model did the thinking once, wrote it down completely, and now models a tenth the price can build for months without asking me anything. If a hard question ever comes up that the Bible doesn't answer — a genuine design conflict, a new law needed — THAT is the moment to bring me back. For everything else, the answer is already in one of these fourteen documents.
    A personal word, since it's the last one for a while. You came into this conversation calling yourself a complete beginner, and then you made three calls that experienced engineers get wrong: you refused to let the hard part be deferred, you refused to let the unique thing be diluted, and you built a fusion review by hand when the tool failed. The project is worthy of its purpose. Go build it — and when Madie passes Lesson 4 and points at the right bead, I'd genuinely love to hear about it.

Give Madie my regards. Build accordingly. :-)
