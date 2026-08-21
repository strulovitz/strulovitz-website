--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - INTRODUCTION TO PART 04 (not law)
--------------------------------------------------------------------------------

THANK YOU Nir!!! :-) Here is Part 04 — Rendering and Performance. This is the Part that guarantees the VR experience is always smooth and comfortable — because in VR, a slow website isn't just annoying like on a screen, it can make the user physically sick. So this Part is written as a discipline with hard numbers, and every future agent gets measured against them.

================================================================================
AI PANORAMA — THE BIBLE — PART 04 OF 13
RENDERING AND PERFORMANCE
Version 1.0 — August 2026
Obeys: Part 00 (Vision and Invariants), Part 01 (Architecture),
Part 02 (Data Model), Part 03 (Layout and Geometry).
================================================================================

--------------------------------------------------------------------------------
4.0 PURPOSE OF THIS PART
--------------------------------------------------------------------------------

This Part defines the performance law of the renderer: the frame budgets,
the drawing techniques that meet them, the identity color palette (LAW 2
machinery), the degradation ladder for weaker devices, and the regression
tests that keep all of it true over years of agent turnover.

The one-sentence philosophy: in VR, PERFORMANCE IS A COMFORT AND SAFETY
FEATURE, not an optimization. A dropped frame on a screen is a stutter; a
dropped frame in a headset is a lurch in the reader's inner ear. The VR
reader (Part 00, 0.8, reader 4) is promised 72 frames per second, always.
Every technique in this Part exists to keep that promise with thousands
of nodes visible.

Reference device: Meta Quest 3, standalone, through its built-in browser
(WebXR). If it runs well there, it runs well everywhere we care about.

--------------------------------------------------------------------------------
4.1 THE BUDGETS (HARD NUMBERS, TESTED, NOT ASPIRATIONAL)
--------------------------------------------------------------------------------

VR (Quest 3, WebXR session):
1.  Frame rate: 72 fps sustained. Never below 72 for more than 3
    consecutive frames during normal interaction (rotation, slicing,
    hovering, opening panels).
2.  DRAW CALLS: under 100 per frame. This is THE binding constraint on
    mobile-class VR GPUs (per Meta's own guidance) — more binding than
    triangle count. The entire graph scene budget: nodes 16-32 calls,
    edges 8-16 calls, labels 4-8 calls, UI/panels/gauge 10-20 calls,
    environment 5-10 calls. Total target: 60-90.
3.  Visible detailed nodes: up to 1,500 (sphere + glow ring + potential
    label). Beyond that, the excess renders as points (4.6).
4.  Visible edge ribbons: up to 4,000 segments instanced.
5.  Texture memory: under 500 MB total. Textures for closed views are
    DISPOSED on scene switch, not cached forever.
6.  JavaScript per frame: under 4 ms on Quest 3 (the GPU needs the
    rest). ZERO allocations in the render loop (4.7).
7.  First-load to first interactive panorama view: under 8 seconds on
    Quest 3 over ordinary home Wi-Fi.

FLAT SCREEN (desktop/laptop browser):
1. 60 fps sustained on a mid-range laptop WITHOUT discrete GPU.
2. Up to 5,000 detailed nodes; same draw-call discipline applies (it is
   cheap to keep and makes the screen version effortless).

BUILD-TIME VERIFICATION: every export ships with the perftest scene
(4.9); the release checklist (Part 12) includes running it on the
physical Quest 3. "It worked on the desktop" is not a pass.

--------------------------------------------------------------------------------
4.2 NODES: INSTANCED RENDERING
--------------------------------------------------------------------------------

1. All node spheres render via InstancedMesh — one geometry (a low-poly
   sphere, about 80-120 triangles), thousands of instances, ONE draw
   call per mesh. Per-instance attributes: position (from the 4D
   projection each frame, 4.8), radius (`base_radius * s`, projection
   owns size EXCLUSIVELY per Part 03, 3.7), color index, flags.
2. SPATIAL SPLITTING: instances are packed into 16-32 InstancedMesh
   buckets by spatial region (octant of the unit box, subdivided by
   population). Reason: Three.js frustum-culls per MESH, not per
   instance — one giant InstancedMesh is always fully drawn even when
   90% is behind the reader. With 16-32 spatial buckets, looking at one
   cluster costs only that cluster's buckets. Bucket assignment is
   computed at export time from epoch positions and stored in
   `nodes.bin` flags; hyper-rotation can move nodes between spatial
   regions VISUALLY, but bucket membership follows the UNROTATED
   positions — good enough because culling is conservative, and
   reassignment every frame would cost more than it saves.
3. FRONT-PACKING: within each bucket, visible instances are packed to
   the front of the instance buffer and `mesh.count` is lowered to the
   visible count — instances beyond `count` cost nothing. The lens
   filters, slice mode, and importance cutoff all work by repacking
   counts, not by allocating new buffers.
4. GLOW RINGS (importance display, Part 03, 3.7 rule 5): a second
   InstancedMesh set (camera-facing quads with a ring texture) sharing
   the same bucket structure. Ring opacity/thickness encodes importance
   tiers. Ring color = the node's identity color. Budget: rings render
   only for the top ~300 visible nodes by importance (config).
5. Node color comes from a PALETTE TEXTURE indexed by `color_index`
   (Part 02, 2.10) — changing themes or editions never touches
   per-instance data, only the 256 x 1 palette texture.

--------------------------------------------------------------------------------
4.3 THE IDENTITY COLOR PALETTE (LAW 2 MACHINERY)
--------------------------------------------------------------------------------

1. Color encodes IDENTITY or PATH, never `w` (LAW 2). This section is
   the single place palette decisions live.
2. MODEL IDENTITY COLORS (comparison scenes, editions UI): a fixed
   roster of at most 12 maximally-distinguishable hues assigned to AI
   models in `entities` (Part 02, 2.4, `display_color`), chosen
   colorblind-aware (verified against deuteranopia and protanopia
   simulations at export time; the validator warns if any assigned pair
   collides). Beyond 12 simultaneously-compared models, the UI REFUSES
   to add more and asks the reader to deselect one — honesty about
   human perception (fusion-settled: color breaks past ~15; we stop at
   12 with margin).
3. TAG-FAMILY TINTS (knowledge graph): event/canon nodes tint by their
   dominant top-level topic family — a muted 8-color set, distinct from
   the vivid model roster so the two worlds never confuse.
4. PATH COLOR: one reserved vivid color (default warm amber) for the
   reader's lit trail and history; nothing else may use it.
5. STATE BADGES: disputed/corrected/brief render as small icon badges
   on the hover card and glow-ring notches — NEVER as node body colors
   (body color is identity, LAW 2 discipline).
6. All palette values live in `config/palette.toml` with plain-language
   comments; agents never hardcode a hex value in a shader or scene
   file.

--------------------------------------------------------------------------------
4.4 EDGES: INSTANCED RIBBONS
--------------------------------------------------------------------------------

1. Edges render as instanced flat ribbons (two triangles per segment,
   camera-facing shader billboarding), NEVER as 1-pixel GL lines —
   which are illegible and shimmer badly in VR (fusion reject list).
2. Ribbon width is constant ANGULAR size (a few arcminutes) clamped to
   a world-space minimum and maximum, so edges stay readable but never
   dominate.
3. Influence edges (directed, Part 03, 3.4) add a slow texture-scroll
   flow animation toward the effect node — one shared shader uniform
   (time), zero per-edge cost.
4. Edge visibility follows the LOD ladder (4.6): far view shows only
   canon-to-canon and influence edges; event sim edges fade in with
   proximity to their cluster. The lens can always force categories on
   or off (repacking, not reallocating, per 4.2.3).
5. Transparency uses DITHERED ALPHA (screen-door pattern in shader, a
   Bayer-matrix threshold against opacity), not sorted alpha blending:
   order-independent, one pass, no popping — this is the technique
   behind slab-fade and ghosting in slice mode (Part 05 owns behavior;
   this Part owns the method).

--------------------------------------------------------------------------------
4.5 TEXT AND LABELS
--------------------------------------------------------------------------------

Text is the classic VR performance killer; the discipline is baked
atlases, few live labels, and compositor layers for reading surfaces.

1. NODE LABELS: rendered from a build-time MSDF atlas (multi-channel
   signed distance field font atlas shipped in the export). At most
   40-64 labels visible simultaneously (config), chosen by LABEL
   PRIORITY = importance x proximity x facing. Labels render as
   instanced quads sampling the atlas — 1-2 draw calls total.
2. Labels keep CONSTANT ANGULAR SIZE (they do not scale with the
   projection factor `s` — text that breathes with hyper-rotation
   shimmers unreadably; fusion-adopted from Grok). Labels always face
   the reader (billboard) and never occlude their own node (offset
   above, leader dot beneath).
3. HOVER CARDS (TLDR + thumbnail, Part 00, 0.6): pre-baked at EXPORT
   time into per-cluster CARD ATLASES — each node's card is a
   pre-rendered texture tile (headline, TLDR text, thumbnail). Hovering
   swaps UV offsets on a single quad — ZERO runtime text layout, zero
   canvas rasterization hitches in-session (fusion-adopted from Kimi;
   superior to runtime SDF layout for fixed content).
4. READING PANELS (the full article, scrollable): rendered through the
   WebXR Layers API (a compositor quad layer) — the compositor samples
   the panel at full display resolution, making body text crisp
   without raising the whole scene's framebuffer scale. The w-gauge
   instrument (Part 05) uses the same mechanism. Fallback when Layers
   API is unavailable: an in-scene quad at 1.3x texture density.
5. FRAMEBUFFER SCALE: default 1.0. The "crisp text" temptation
   (framebufferScaleFactor 1.3-1.5) costs GPU quadratically; we spend
   compositor layers instead (they are free crispness for flat
   surfaces). Scale may rise to 1.2 ONLY in the sparse comparison
   scenes (few objects), never in the full graph.

--------------------------------------------------------------------------------
4.6 LEVEL OF DETAIL AND THE DEGRADATION LADDER
--------------------------------------------------------------------------------

The importance-sorted `nodes.bin` prefix IS the LOD system (Part 02,
2.10): rendering the first N records = rendering the N most important
nodes. The ladder, from best to worst conditions:

1. FULL: 1,500 detailed nodes, rings, 4,000 edge segments, 64 labels.
2. TRIMMED: labels drop to 24, rings to top 100, event sim edges hidden
   beyond focus cluster.
3. POINTS: nodes beyond the detailed budget render as a single
   THREE.Points cloud (one draw call, tens of thousands of points) —
   the honest fallback that keeps the WHOLE panorama visible as a
   starfield while detail concentrates where the reader looks/points.
4. FROZEN: if frame time still exceeds budget for more than 2 seconds,
   idle auto-wobble (Part 05) pauses and edge flow animations stop
   (static scenes cost less); a small "performance mode" notice appears.

Automatic stepping: a frame-time governor (rolling 120-frame median)
steps DOWN one rung when median frame time exceeds 13.5 ms in VR and
steps UP after 10 clean seconds. Steps are one-way per 5-second window
(no oscillation). The governor's current rung is visible in the debug
HUD (4.9) and logged to build-health telemetry counters (client-side
only, no reader tracking — Part 01, 1.11).

Quest-specific measures: `XRWebGLLayer.fixedFoveation` is set to 0.5 in the
graph scene (peripheral resolution is spent on nothing anyway) and 0.25
in reading contexts (DeepSeek-verified as available in browser WebXR).
AppSpaceWarp is NOT used — its motion extrapolation smears rotating
edges into ghosting (fusion reject, Grok).

--------------------------------------------------------------------------------
4.7 THE RENDER LOOP DISCIPLINE
--------------------------------------------------------------------------------

1. ZERO ALLOCATION during the frame: all vectors, matrices, arrays are
   pre-allocated and reused. No object spread, no closures created per
   frame, no array.map in the loop. A garbage-collection pause in VR is
   a guaranteed dropped-frame lurch. Code review rule: any `new` inside
   the render path is a defect.
2. The 4D pipeline per frame (Part 03 math): apply `Q` and projection
   to node positions in ONE typed-array pass (a tight loop over
   Float32Arrays, writing straight into instance attribute buffers,
   then one `needsUpdate`). At 20k nodes this is well under 1 ms on
   Quest 3's CPU. THE ONE-PROJECTION RULE (Part 03, 3.7.4): this pass
   runs ONCE per frame; both eyes consume the same projected scene.
3. PICKING: no THREE.Raycaster against scene objects (it walks the
   whole scene graph allocating hit records). Picking is a custom
   sphere-intersection test against the SAME typed arrays the
   projection pass writes, iterating only currently-visible instances,
   allocation-free, returning a node index. Edges are never pickable
   (Part 03, 3.4.3).
4. Hover work is BUDGETED: card-atlas UV swap and glow pulse only; any
   heavier response to hover (prefetching `nodes/<id>.json`, Part 01)
   happens on a debounce timer OFF the frame path (250 ms of stable
   hover), via fetch in an idle callback.
5. SHADER PREWARM: all scene shaders compile during the loading screen
   (renderer.compile + a hidden 1-frame render of every material
   variant) BEFORE the WebXR session starts. First-hyper-rotation
   shader compilation would otherwise freeze the world mid-gesture
   (fusion-settled, 3/6 convergence).
6. Scene transitions (graph to comparison to w-gym) PRELOAD the target
   scene's buffers, then swap in one frame; textures of the departed
   scene are disposed after the swap (4.1 budget 5).

--------------------------------------------------------------------------------
4.8 DATA LOADING AND MEMORY
--------------------------------------------------------------------------------

1. Load order (Part 01, 1.8.11): `pointer.json`, `manifest.json`,
   `panorama.json` (render immediately — the reader is INSIDE the
   panorama within seconds), then `nodes.bin` + `edges.csr.bin` +
   `tagsets.bin` streamed in the background, then on-demand per-node
   payloads.
2. All binary files parse directly into typed arrays (zero-copy views
   where alignment allows). No JSON for bulk structure (Part 02, 2.10).
3. Per-node payloads (`nodes/<id>.json`) and images load on approach/
   hover with an LRU cache (config: 200 payloads, 100 full images);
   eviction disposes GPU textures.
4. The site is a PWA with a service worker caching the current version
   folder for offline reading; the pointer.json fetch always bypasses
   the cache (network-first) so a rollback or new release is never
   pinned by a stale cache — and a cache-reset path exists in the
   settings UI (fusion-adopted from GPT).

--------------------------------------------------------------------------------
4.9 REGRESSION TESTING AND INSTRUMENTATION
--------------------------------------------------------------------------------

1. THE PERFTEST SCENE: `?perftest=1` loads a synthetic build (generated
   at export time: 20k nodes, 200k edges, deterministic layout) and
   runs a scripted 60-second tour: full rotation in all six planes,
   slice sweep, 50 hovers, 5 panel opens, LOD ladder walk. It records
   frame-time percentiles, draw calls, allocation counts, and worst
   frame, then displays a PASS/FAIL against the budgets in 4.1 and
   offers the report as copyable JSON text (LAW 3: pasteable into
   Telegram).
2. RELEASE RULE (enforced via Part 12's checklist): perftest must PASS
   on the physical Quest 3 for any release that touched `site/`.
   Failures attach the JSON report to the ledger.
3. THE ONE-PROJECTION ASSERT: in debug builds, the render loop asserts
   a single projection pass per frame and identical projected buffers
   consumed by both eyes' draws.
4. DEBUG HUD (`?debug=1`): frame time graph, draw calls, instance
   counts per bucket, LOD rung, memory, current `Q` matrix, active
   w-definition — all as plain text overlays, screenshot-friendly.
5. NO READER TELEMETRY leaves the device, ever (Part 01, 1.11). All
   instrumentation is local and visible to the person holding the
   headset.

--------------------------------------------------------------------------------
4.10 POINTERS
--------------------------------------------------------------------------------

What the reader DOES with all this speed (rotation, slicing, pivots,
comfort, onboarding): Part 05. Where card atlases and images come from
(export/imagery stages): Part 06 and Part 01. The panorama recipe:
Part 08. Comparison scenes' special rendering (axis gizmos, killer
boxes): Part 09. Release checklist and ledger: Part 12.

================================================================================
END OF PART 04
================================================================================

--------------------------------------------------------------------------------
AUTHOR'S COMMENTARY - NOTES ON PART 04 (not law)
--------------------------------------------------------------------------------

(Two stray characters slipped in again — section 4.6 "Quest-specific措施" should read "Quest-specific measures". Same cleanup instruction as last time for the committing agent: fix that one word, everything else is clean. I've noticed this happens occasionally in very long outputs; the pre-upload validator in Part 12 will also catch non-ASCII characters in Bible files as a rule.)

Three plain-language notes for you, Nir:

    The whole Part is really one promise: the headset never stutters. Everything else — the hundred-draw-call limit, the pre-baked text cards, the "starfield" fallback — is machinery for keeping that one promise even when the graph is huge. Stutter in VR isn't ugly, it's nauseating, and a reader who felt sick once never puts the headset back on.
    The hover cards trick is worth understanding: every node's little TLDR popup is pre-drawn as a picture at build time in your kitchen, so when a reader points the laser at a node, the headset just slides a ready-made picture into view — it never has to typeset text live. Your Atlas PC does the work once so a million future hovers cost nothing.
    The ?perftest=1 page is your quality inspector. Any time you want, you can open that address on the Quest and get a plain PASS or FAIL with numbers you can paste into Telegram. No agent can tell you "it's fast, trust me" — you can check yourself, without reading a line of code.

Say the word and I deliver Part 05 — 4D Interaction next: the controller mappings, slice and projection modes, the holotable comfort rules, the w-gym onboarding room, and the red-letter correctness rules — the crown jewel Part. Give Madie my regards!!! :-)
