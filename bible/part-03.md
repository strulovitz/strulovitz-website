--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - INTRODUCTION TO PART 03 (not law)
--------------------------------------------------------------------------------

THANK YOU Nir!!! :-) Here is Part 03 — Layout and Geometry. This is the Part that answers "WHERE is every node in space, and WHY is it there?" — the map-making law of the project. It contains the most mathematics of any Part, all written as plain code-style text per LAW 3, with explanations a weaker model can follow step by step.

================================================================================
AI PANORAMA — THE BIBLE — PART 03 OF 13
LAYOUT AND GEOMETRY
Version 1.0 — August 2026
Obeys: Part 00 (Vision and Invariants), Part 01 (Architecture),
Part 02 (Data Model).
================================================================================

--------------------------------------------------------------------------------
3.0 PURPOSE OF THIS PART
--------------------------------------------------------------------------------

This Part defines how every publishable node gets its position in
four-dimensional space `(x, y, z, w)`, how those positions stay STABLE
across weeks and years (the no-jumping rule), what the fourth coordinate
MEANS, and the exact projection mathematics the renderer uses to turn 4D
into what the reader sees — in VR (LAW 1: the crown) and on flat screens.

The design in one paragraph: the force simulation lays out only the CANON
SKELETON (a few hundred concept nodes — the "cities" of the map), rarely,
in 3D. Every event node (the "houses") is placed INSTANTLY by a formula
from the cities it belongs to — no simulation, no randomness, stable
forever. The fourth coordinate `w` is never a simulation residue: it is a
SEMANTIC axis with a chosen meaning, default = abstraction level, so that
swimming along `w` in VR travels from fresh news to settled encyclopedia —
Advantage 0 made into a literal direction in space.

Vocabulary reminder (Part 00 glossary): an EPOCH is one frozen layout
computation. Positions change only between epochs, and the change is
deliberately minimized and animated.

--------------------------------------------------------------------------------
3.1 COORDINATE SYSTEM AND UNITS
--------------------------------------------------------------------------------

1. World space is right-handed, `y` up, matching Three.js conventions:
   `x` right, `y` up, `z` toward the viewer, `w` the fourth axis with no
   spatial prejudice (its meaning is semantic, 3.5).
2. All published positions live inside the UNIT BOX: each coordinate in
   `[-1, +1]`. The renderer scales the unit box to comfortable physical
   size (the holotable, Part 05): default graph diameter about 1.6
   meters in VR, adjustable by the user's two-grip scale gesture.
3. Quantization (Part 02, 2.10): each coordinate is stored as uint16.
   Dequantize: `coord = (raw / 65535) * 2 - 1`. Precision is about
   0.00003 of the box — far below visual perception; agents never store
   float positions in exports.
4. The layout bounding box, epoch id, and w-definition id are recorded
   in `layout/epochs.json` with every build.

--------------------------------------------------------------------------------
3.2 THE CANON SKELETON: FORCE LAYOUT FOR CITIES ONLY
--------------------------------------------------------------------------------

WHAT IS LAID OUT: only canon nodes (Part 02, 2.6) that are not hubs
(`is_hub: false` — hubs get no edges and no layout influence, Part 02,
2.5), plus story-arc anchor nodes. Expected count: hundreds, at most a
few thousand after years. NEVER the full event population — that is what
makes weekly builds cheap and positions stable.

INPUT GRAPH: canon-to-canon `RELATED` edges weighted by `sim_weight`
aggregated from their events (Part 02, 2.7), pruned to the strongest
edges per node (top-k, default `k = 12`, config) so the simulation sees
structure, not soup.

METHOD:
1. The simulation runs in 3D and owns ONLY `(x, y, z)`. It does NOT
   produce `w` (3.5 owns `w`). Rationale (fusion-settled): a simulated
   fourth coordinate is meaningless residue; a semantic one is readable.
2. Algorithm: force-directed layout with repulsion approximated by
   Barnes-Hut (octree) so cost stays near `n log n`, attraction along
   weighted edges, plus a weak centering force. The agents implement
   with a well-maintained library of their choice (documented in the
   ledger) — the CONTRACT is only: deterministic under a fixed random
   seed, seed recorded in `layout/epochs.json`.
3. Convergence: run to low total displacement (config threshold), cap
   iterations, record final stress value in the build health page.
4. Cluster detection (for labels and the panorama): community detection
   (Louvain or Leiden via Neo4j GDS, Part 01) runs on the same input
   graph; each community gets a human-readable label proposed by the
   pipeline and approved by Nir once (ledger event). Community ids ship
   in `nodes.bin` flags region for the renderer's cluster labels.

WHEN IT RUNS (EPOCH POLICY):
1. A new epoch is computed ONLY when: (a) a calendar quarter has passed,
   or (b) canon membership changed by more than 10% since the last
   epoch, or (c) Nir asks for one. Weekly builds REUSE the current
   epoch's skeleton untouched.
2. Between epochs, NEW canon nodes are placed analytically like events
   (3.3) using their strongest RELATED neighbors, flagged
   `provisional: true`, and become simulated members at the next epoch.

ALIGNMENT (THE NO-JUMPING RULE):
1. After computing epoch `E+1`, align it to epoch `E` by orthogonal
   Procrustes: find the rotation matrix `R` minimizing the total squared
   distance between the new positions and the old positions of the
   SHARED canon nodes. Computation: `R = U * V_transpose` where
   `U, S, V_transpose = svd(B_transpose * A)`, `A` = old positions
   matrix, `B` = new positions matrix, both mean-centered; correct the
   sign so `det(R) = +1` (no mirror flips — a mirrored map would wreck
   every reader's spatial memory silently).
2. After rotation, apply uniform scale + translation fit to the shared
   nodes (full similarity transform).
3. Additionally PIN the top-20 highest-importance canon nodes: after
   Procrustes, any pinned node still displaced by more than `0.05` unit
   is snapped 80% back toward its old position and the simulation is
   given a short settle run with those pins as soft anchors. Landmarks
   must feel eternal.
4. BUILD METRIC: median displacement of shared canon nodes between
   epochs is computed and reported in build health. If it exceeds
   `0.10` units, the build FAILS for human review — the map is not
   allowed to secretly become a new map (protects Part 00, 0.7,
   invariant 3).
5. CROSSFADE: `layout/epochs.json` ships previous + current positions;
   the renderer animates nodes along straight lines over 800 ms the
   first time a returning visitor sees a new epoch. No teleporting
   geography.

--------------------------------------------------------------------------------
3.3 ANALYTIC PLACEMENT: EVERY EVENT NODE, INSTANTLY, FOREVER
--------------------------------------------------------------------------------

Event nodes never enter the simulation. Their `(x, y, z)` is a FORMULA:

1. Collect the event's non-hub topic edges `TAGGED {weight}` to canon
   nodes (Part 02) and its influence/claim-graph bonuses to other nodes
   already placed (Part 02, 2.7). Call these anchors `a_1 ... a_m` with
   weights `u_1 ... u_m`.
2. Weighted centroid: `p = sum(u_i * pos(a_i)) / sum(u_i)`.
3. Deterministic scatter: derive a pseudo-random offset from the event
   id — `h = sha256(event_id)`, map `h` to a unit vector `v` in 3D and
   a radius `r` in `[r_min, r_max]` (defaults: `r_min = 0.015`,
   `r_max = 0.06`, scaled by local anchor density so dense
   neighborhoods scatter tighter). Final: `pos(event) = p + r * v`.
   The hash makes placement REPRODUCIBLE: same event, same position, on
   every machine, in every rebuild, with no stored state.
4. Collision relief: if two events land within `0.008` units, the
   later-ingested one takes one extra hash round (`h = sha256(h)`) —
   deterministic re-scatter, at most 3 rounds, then accept overlap
   (the renderer's importance ordering keeps labels legible anyway).
5. Story-arc members tighten toward their arc anchor: blend
   `pos = 0.6 * pos + 0.4 * pos(arc_anchor)` so sagas read as braids,
   not scattered dust.

CONSEQUENCES (why this design is the law):
1. Placement is O(1) per event — a build with 10,000 new events costs
   nothing measurable.
2. Positions are STABLE across builds (no simulation jitter) and
   READABLE: an event sits between the concepts it is about, so "this
   node lives between the safety cluster and the open-weights cluster"
   is a fact about the CONTENT, not an accident of physics.
3. 100,000 nodes is a non-problem for layout (rendering budgets are
   Part 04's business).

--------------------------------------------------------------------------------
3.4 EDGE GEOMETRY
--------------------------------------------------------------------------------

1. Only edges above the render threshold ship: per node, top-k sim
   edges (default `k = 6` for events, `k = 12` for canon) AND all
   influence edges. The full edge set stays in Neo4j; the export prunes
   for legibility and budget (Part 04).
2. Edges render as instanced ribbons (never 1-pixel lines in VR, per
   fusion reject list). Influence edges are DIRECTED and render with a
   subtle flow animation toward the effect (CAUSED/ENABLED point
   forward in time of consequence).
3. Edges are never pickable (Part 05; picking is nodes-only, a
   performance and usability rule).

--------------------------------------------------------------------------------
3.5 THE FOURTH COORDINATE: SEMANTIC W
--------------------------------------------------------------------------------

`w` is NEVER produced by simulation and NEVER mapped to color (LAW 2).
`w` is a chosen, documented, per-view MEANING. The active w-definition
id ships in `layout/epochs.json` and the site's w-selector UI lets the
reader switch among the definitions exported for that build.

W-DEFINITION 1 — ABSTRACTION (default for the knowledge graph):
The axis from weather to geography. Fixed anchor values in `[-1, +1]`:
1. `w = -1.0` : incoming / corroborating events (the newest, rawest)
2. `w = -0.5` : developing events
3. `w =  0.0` : established events (the stable news record)
4. `w = +0.4` : absorbed events (their essence already in canon)
5. `w = +0.7` : canon topics and explainers (the encyclopedia)
6. `w = +1.0` : canon standing-questions and the most crystallized,
   time-tested concepts
Within each band, position interpolates smoothly by age-in-state and
corroboration count (config curves), so motion along w is continuous,
not stepped. READER EXPERIENCE: slicing at low w = "today's news";
sliding the slab toward high w = watching news condense into knowledge.
Advantage 0 as a hand motion. New events ENTER the world at low w and
MIGRATE inward over their lifecycle — returning visitors literally see
this week's weather hanging outside the geography.

W-DEFINITION 2 — TIME (`t_event`, normalized over the archive span,
log-compressed near the present so recent months get more room).
Used for story-arc exploration and the changelog views (Part 08).

W-DEFINITION 3 — VERIFICATION (evidence tier): rumored at `-1`,
reported at `-0.33`, announced at `+0.33`, benchmarked/established at
`+1`, computed from the event's claim mix. Slicing toward high w gives
the reader a "show me only what is solid" world — trust as geometry.

COMPARISON SCENES (Advantage 2, Part 09): `w` is simply the fourth
CHOSEN METRIC AXIS (e.g., context window). Native data axes, no
simulation, same projection machinery below.

RULE FOR ALL DEFINITIONS: every w-definition must be explainable to a
reader in one sentence, shown in the w-selector UI. If a proposed
w-definition cannot be explained in one sentence, it is rejected.

--------------------------------------------------------------------------------
3.6 4D ROTATION MATHEMATICS
--------------------------------------------------------------------------------

Rotation in 4D happens in PLANES, not around axes. There are exactly six
coordinate planes: `XY, XZ, YZ` (the familiar 3D rotations) and
`XW, YW, ZW` (the hyper-rotations that make 4D 4D).

A rotation by angle `theta` in a plane mixes those two coordinates and
leaves the other two untouched. Example, plane ZW:
    `z_new = z * cos(theta) - w * sin(theta)`
    `w_new = z * sin(theta) + w * cos(theta)`
(The same pattern applies to any plane — substitute the two letters.)

IMPLEMENTATION CONTRACT for `site/src/lib/fourd.js`:
1. The view's 4D orientation is ONE 4x4 orthonormal matrix `Q` (column-
   major, like Three.js). User input composes plane rotations onto `Q`:
   `Q = R_plane(theta) * Q`, then `Q` is re-orthonormalized (Gram-
   Schmidt) every compose to kill numeric drift.
2. Rotation is applied about the current PIVOT (the focused node, or
   the graph centroid if none — Part 05), never about the world origin:
   `p_rotated = Q * (p - pivot) + pivot`.
3. The expert two-handed rotation (Part 05) composes onto the same `Q`;
   there is only ever ONE orientation state, so undo/reset are trivial:
   undo pops a small history stack of `Q`; reset sets `Q = identity`
   (the canonical basis — a top-level control, fusion-settled).
4. Snap rotations: 90-degree plane rotations animate over 300 ms with
   ease-in-out; analog rotation rate is CAPPED at 25 degrees/second in
   VR (comfort law, Part 05 owns the full comfort rules).

--------------------------------------------------------------------------------
3.7 4D-TO-3D PROJECTION
--------------------------------------------------------------------------------

After rotation, each point `(x, y, z, w)` (coordinates now in the view
basis) is projected to 3D by perspective from a 4D eye on the w-axis:

1. NORMALIZED projection scale (fusion-adopted; nothing can explode):
   `s = (d - w_min) / (d - w)`
   where `d` is the 4D eye distance (default `d = 3.0`, config) and
   `w_min = -1` (the unit box floor). Since `w <= +1 < d`, the
   denominator is always positive; `s` ranges smoothly around 1.
2. Projected position: `(x_3d, y_3d, z_3d) = (s * x, s * y, s * z)`.
3. MEANING FOR THE READER: nodes with higher `w` appear LARGER and
   nearer (like the outer cube of the classic tesseract drawing); lower
   `w` appears smaller and nested within. Under w-definition 1 this is
   poetic and correct: the encyclopedia looms large and enclosing, the
   fresh news hangs small and outward — and a hyper-rotation visibly
   turns the structure inside out, which is exactly the honest
   experience of 4D.
4. THE ONE-PROJECTION RULE (red-letter, fusion correctness bug): the
   4D-to-3D projection is computed ONCE per frame, producing ONE 3D
   scene, which the VR compositor then renders in stereo for the two
   eyes. NEVER compute a separate 4D projection per eye — per-eye 4D
   projections create disparity the human brain cannot fuse. A
   regression test in the perftest scene asserts both eyes' scenes
   derive from a single projection pass (Part 04).
5. Node SIZE budget: the geometric radius of a node is
   `radius = base_radius * s` — projection owns size EXCLUSIVELY.
   Importance is shown by glow-ring and label priority, never by
   radius (GLM's collision rule, adopted; Part 04/05 implement).
6. The floor shadow + drop-stem system (the reader's w-anchors) and
   slice mode (slab at `w0` with fade and ghosting) consume `w` BEFORE
   projection; their exact behavior is interaction law, owned by
   Part 05.

FLAT-SCREEN VERSION (LAW 1's companion): identical mathematics — same
`Q`, same projection, same one-projection rule (trivially, one eye).
Mouse mappings for the six planes live in Part 05. The 3D screen version
is the same 4D world seen through a normal camera, so a URL-shared view
(Part 00, 0.7) opens identically on screen and in VR.

--------------------------------------------------------------------------------
3.8 PIPELINE INTEGRATION (THE LAYOUT STAGE CONTRACT)
--------------------------------------------------------------------------------

The LAYOUT stage (Part 01, 1.5) at every build:
1. Reuses or computes the epoch skeleton per 3.2's policy.
2. Computes analytic placements (3.3) for all new/changed events.
3. Computes `w` for every node under EVERY exported w-definition.
4. Quantizes to uint16, writes `nodes.bin`, `edges.csr.bin`,
   `layout/epochs.json` (with seed, stress, displacement metric,
   w-definition ids, previous positions for crossfade).
5. Emits the layout section of build-health: node count, edge count,
   epoch id, median displacement, stress, w-definition list.
Determinism rule: two runs of the same build inputs on any machine must
produce byte-identical layout files (fixed seeds, fixed hash scatter).
If they do not, that is a bug, not a curiosity.

--------------------------------------------------------------------------------
3.9 POINTERS
--------------------------------------------------------------------------------

Rendering the geometry at 72 fps, instancing, glow-rings, labels:
Part 04. Rotating, slicing, pivoting, comfort, onboarding: Part 05.
When lifecycle states change (which moves nodes along w-definition 1):
Part 08. Comparison-scene axes and templates: Part 09.

================================================================================
END OF PART 03
================================================================================

--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - NOTES ON PART 03 (not law)
--------------------------------------------------------------------------------

(One tiny note: I spotted a stray non-English character that slipped into section 3.8 line 1 — "at每 build" should read "at every build". Please tell the agent who commits this to fix that one word; everything else is clean.)

Three plain-language notes for you, Nir:

    The cities-and-houses idea is the heart of this Part. Only the few hundred "city" concept nodes ever get the expensive physics simulation, and every news "house" is placed instantly by formula — between the concepts it's about. So your map stays stable for years, builds cost nothing, and a node's position literally MEANS something.
    Your Advantage 0 became a direction you can swim. With the default meaning of the fourth axis, fresh news hangs at one end and the settled encyclopedia at the other — and in VR, pushing the slab through w is literally watching news condense into knowledge with your hand. No other website on Earth has that.
    The no-jumping rule has teeth. If a rebuild would secretly move the map more than a small amount, the build FAILS and a human looks at it. Your readers' memory of "where things live" is protected by law, not by hope.

Say the word and I deliver Part 04 — Rendering and Performance next: the 72-fps discipline, draw calls under 100, instancing, label atlases, the identity color palette, and the fallback ladder for weaker devices. Give Madie my regards!!! :-)
