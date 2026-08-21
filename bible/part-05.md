================================================================================
AI PANORAMA — THE BIBLE — PART 05 OF 13
4D INTERACTION
Version 1.0 — August 2026
Obeys: Part 00 (Vision and Invariants), Part 03 (Layout and Geometry),
Part 04 (Rendering and Performance).
================================================================================

--------------------------------------------------------------------------------
5.0 PURPOSE OF THIS PART
--------------------------------------------------------------------------------

This Part defines the reader's bodily experience of the fourth dimension:
the two viewing modes, the controller and mouse mappings, the comfort
rules that prevent motion sickness, the non-color cues that make `w`
readable (LAW 2), the onboarding room where newcomers learn 4D in about
one minute, and the red-letter correctness rules that keep the experience
perceptually honest.

Design philosophy in three sentences: the reader is a VISITOR IN A
WORKSHOP, not a passenger on a ride — the world never moves them; they
move the object. The fourth dimension is DISCOVERED, not imposed — the
first minute looks like familiar 3D, and `w` reveals itself through the
reader's own hand motions. Every control has an instant, visible,
reversible effect — nothing is hidden, nothing is irreversible, and the
way back is always one button.

The reference experience is VR on Meta Quest 3 (LAW 1: the crown). The
flat-screen version implements the SAME state machine with mouse and
keyboard (5.8) — one interaction model, two bodies.

--------------------------------------------------------------------------------
5.1 THE HOLOTABLE (THE STAGE AND THE COMFORT CONTRACT)
--------------------------------------------------------------------------------

1. The graph appears as an object floating above a HOLOTABLE: a bounded
   volume, default 1.6 meters diameter, centered at comfortable chest
   height, about 1.2 meters in front of the reader at session start.
2. THE WORLD NEVER ROTATES AROUND THE READER. All rotation (3D and
   hyper) applies to the graph object about its PIVOT (5.4). The room —
   a simple static environment with a floor, a horizon reference, and
   fixed distant landmarks — never moves. A stable peripheral rest
   frame is the single strongest defense against VR nausea, and it is
   non-negotiable.
3. LOCOMOTION: the reader either physically walks (room-scale) or moves
   the GRAPH, never themselves: one-hand grip = grab and reposition the
   graph object; two-hand grip = scale (stretch/squeeze) and yaw the
   graph between the hands. No artificial smooth locomotion, no
   teleport-flying through space in v1. Ego mode (5.6.4) is the
   exception, with its own comfort wrapper.
4. COMFORT CAPS (from Part 03, 3.6.4, restated as law): analog rotation
   rate capped at 25 degrees per second; NO rotational inertia (motion
   stops the instant input stops — drifting geometry is nauseating);
   snap rotations animate 300 ms with ease-in-out; the projection
   factor's rate of change is clamped (`ds/dt` limit) so nodes never
   "loom" explosively during fast hyper-rotation.
5. All UI panels (reading panel, menus, w-selector) are BODY-ANCHORED
   (positioned relative to the reader or their hands), never
   HEAD-LOCKED (glued to the view). Head-locked content fights the
   vestibular system and reads as smearing.

--------------------------------------------------------------------------------
5.2 THE TWO MODES: SLICE (HOME) AND PROJECTION (AWE)
--------------------------------------------------------------------------------

MODE 1 — SLICE (the default; every session starts here):
1. The reader sees the slab of the world at `w0 = 0` with thickness
   `epsilon` (default 0.25 in unit-box units; adjustable). Under
   w-definition 1 (Part 03, 3.5) this means: session starts among the
   ESTABLISHED events — a calm, familiar-looking 3D graph. No 4D
   confusion in the first seconds; the fourth dimension is a door, not
   a wall.
2. Nodes fade toward the slab edges using dithered alpha (Part 04,
   4.4.5). GHOSTING: nodes just OUTSIDE the slab (within `epsilon`
   beyond each face) render as faint wireframe ghosts — the reader
   always sees that MORE WORLD exists beyond the slab, and nothing ever
   just vanishes ("my article disappeared" is a design failure;
   fusion-adopted from Grok and GLM).
3. SWIMMING: holding LEFT TRIGGER, the left thumbstick's vertical axis
   moves `w0` smoothly through `[-1, +1]` — the MRI-scanner gesture.
   Under w-definition 1, pushing away from the body moves toward canon
   (the encyclopedia), pulling back moves toward fresh news. The motion
   is slow by default (full sweep in about 4 seconds) with a precision
   half-speed when the trigger is held deeper (analog trigger value).
4. The slab's floor projection (5.3.3) updates live, so the reader sees
   the shadow-map of the current slab on the table surface.

MODE 2 — PROJECTION (the whole 4D structure at once):
1. Toggled by the X button (left controller) or from the hand menu. The
   slab expands to the whole `w` range with a 600 ms animated
   transition (the ghosts inflate into solidity — the reader SEES that
   projection mode is "all slabs at once").
2. Now the projection scale `s = (d - w_min) / (d - w)` (Part 03, 3.7)
   does its full work: high-`w` structure looms large and enclosing,
   low-`w` hangs small and outward. Hyper-rotations visibly turn the
   structure inside out — the honest tesseract experience, and the
   mode readers will screenshot and share.
3. Projection mode is the AWE and OVERVIEW mode; reading and precise
   picking are expected to happen in slice mode. The UI gently nudges:
   opening a reading panel from projection mode offers "focus this
   node's slab" as the default action.
4. IDLE WOBBLE: after 5 seconds without input in projection mode, a
   tiny slow oscillation (amplitude under 2 degrees) in the XW plane
   begins. A static 4D projection is indistinguishable from a weird 3D
   object; the wobble supplies the motion parallax that makes the
   4D-ness continuously visible (fusion-adopted from Kimi). Any input
   pauses it; the LOD governor may pause it under load (Part 04,
   4.6.4).

--------------------------------------------------------------------------------
5.3 READING W WITHOUT COLOR (THE CUE PACKAGE, LAW 2 MACHINERY)
--------------------------------------------------------------------------------

Every cue below is active in both modes unless stated. None uses hue.

1. PROJECTION SIZE: `s` makes high-`w` bigger — automatic, from the
   math (Part 03, 3.7.5: radius is EXCLUSIVELY `base_radius * s`;
   importance uses glow rings, never size).
2. THE W-GAUGE: a physical instrument mounted on the LEFT FOREARM like
   a wristwatch (diegetic, not a floating HUD; fusion-adopted from GLM
   and Kimi). A vertical bar shows the full `w` range with: the current
   slab position and thickness (slice mode), the hovered/focused node's
   `w` as a bright tick, and small density marks showing how much
   content lives at each `w` (a histogram silhouette). Rendered via
   compositor layer for crispness (Part 04, 4.5.4). Glancing at your
   wrist to check "where am I in the fourth dimension" becomes a
   natural gesture within minutes.
3. DROP-STEMS AND FLOOR GRID: every detailed node drops a hairline stem
   to its shadow dot on the holotable surface, which carries a fixed
   grid whose CELL SIZE never changes. This disambiguates the projection:
   a node big-because-near-z sits far up its stem over a near grid
   cell; a node big-because-high-w shows a stem-length and grid
   position that do not match near-z (fusion-adopted from DeepSeek).
   Stems render only for the top ~300 visible nodes (budget, Part 04).
4. AUDIO: a soft ambient bed whose brightness follows the focused
   region's `w` — low-pass filtered (muffled) at low `w`, opening up
   toward high `w`; hover ticks are similarly filtered by the node's
   `|w - w0|` distance. Subtle, optional (settings), and genuinely
   informative with practice (fusion-adopted from Opus).
5. HAPTICS: while swimming `w0`, controller vibration pulses gently as
   the slab crosses density bands (the histogram from cue 2 made
   touchable). While hyper-rotating, a faint texture pulse marks each
   15 degrees — rotation you can count by feel.
6. LABELS DO NOT SCALE with `s` (constant angular size, Part 04,
   4.5.2) — text is the one thing exempted from the projection cue,
   because shimmering text destroys reading.

--------------------------------------------------------------------------------
5.4 ROTATION CONTROLS: TWO TIERS
--------------------------------------------------------------------------------

PIVOT RULE (both tiers): rotation happens about the FOCUSED NODE if one
is focused, else about the graph centroid (Part 03, 3.6.2). Focusing a
node (5.6.1) and then rotating means "turn the world around this
thing" — the natural gesture of inspection.

TIER 1 — GUIDED (default for everyone):
1. RIGHT THUMBSTICK: ordinary 3D rotation of the graph object (stick X
   = yaw, stick Y = pitch). Familiar, always available, no modes.
2. HYPER-ROTATION is explicit and single-plane: CLICKING the left
   thumbstick cycles the ACTIVE HYPER-PLANE through XW, YW, ZW (with a
   small three-segment indicator on the w-gauge arm showing which is
   active, and a one-word voice-over on first use: "X-W"). The LEFT
   THUMBSTICK's vertical axis then rotates in that plane, rate-capped
   per 5.1.4. One plane at a time, one axis of input — a newcomer
   cannot get lost, and every hyper-rotation is a deliberate act
   (fusion-adopted: Qwen's no-chording rule, DeepSeek's plane-cycle,
   Grok's explicit-mode principle).
3. SNAP: flicking the left stick horizontally while in hyper-mode
   performs a 90-degree snap rotation in the active plane (300 ms
   animated). Four flicks always return home — hyper-rotation with
   training wheels, great for the w-gym.
4. RESET AND UNDO (top-level, always): the B button opens the hand
   menu whose FIRST item is Undo Last Rotation and SECOND is Reset To
   Canonical View (`Q = identity`, slab to `w0 = 0`; Part 03, 3.6.3).
   Readers must never fear experimenting — the way home is two clicks,
   from anywhere, forever.

TIER 2 — THE TWIST (expert toggle, off by default; enable in settings
or by completing w-gym lesson 5):
1. Holding BOTH GRIPS enters twist mode: the two controllers' combined
   orientations drive a full free 4D rotation, composed continuously
   onto `Q` — the two-handed SO(4) gesture (`p' = l * p * r` in the
   quaternion-pair formulation; Part 03's `Q` machinery absorbs it, so
   undo/reset work identically). In plain words: your two hands
   together hold the four-dimensional object, and twisting them in
   opposite ways turns it through dimensions no single hand can reach.
2. Rate-limited by the same comfort caps; releasing either grip
   freezes the rotation instantly (no inertia, 5.1.4).
3. This is the mode for readers who want mastery — and the gesture the
   project may become known for. But TIER 1 IS THE PRODUCT; the twist
   is the reward.

--------------------------------------------------------------------------------
5.5 POINTING, HOVERING, OPENING (THE LADDER IN THE HAND)
--------------------------------------------------------------------------------

1. The RIGHT controller casts the pointing ray (a subtle line with a
   dot cursor; the ray bends slightly toward the nearest pickable node
   within a small cone — assisted aim, because free-hand rays at 1.5
   meters wobble by design of human arms). Picking runs against typed
   arrays, nodes only, never edges (Part 04, 4.7.3).
2. HOVER (ray dwells on a node): the node's glow ring brightens, its
   `w` tick lights on the w-gauge, and after 150 ms the HOVER CARD
   (headline, TLDR, thumbnail — Part 00, 0.6, ladder rung 1) fades in,
   anchored above the node, billboard, constant size. Prefetch of the
   full payload begins on the 250 ms debounce (Part 04, 4.7.4).
3. FOCUS (single TRIGGER click): the node becomes the pivot; its
   first-ring neighborhood highlights; its path-trail entry is
   recorded; the hover card pins. A second trigger click OPENS.
4. OPEN (trigger on a focused node): the READING PANEL slides up —
   body-anchored at comfortable reading distance, compositor-layer
   crisp (Part 04, 4.5.4), scrollable by stick or by grabbing the page
   edge. Content per the ladder: full synthesis, conflicts section,
   ELI5 concept links (opening one records the hop in the trail),
   sources with locator deep-links, cite key, image with generating
   model label. Closing (B or grab-fling down) returns to the graph
   with the node still focused.
5. THE HAND MENU (B button): appears AT THE HAND (Part 00, 0.7,
   invariant 2), items in fixed order: Undo Rotation, Reset View,
   Back, Forward, Home (panorama), Mode Toggle, w-Selector, Lens,
   Settings. Radial layout, thumb-selectable, dismisses on release —
   built for eyes-on-the-graph use.

--------------------------------------------------------------------------------
5.6 NAVIGATION: TRAIL, HISTORY, EGO MODE
--------------------------------------------------------------------------------

1. THE PATH TRAIL (Part 00, 0.7, invariant 1): every focused node joins
   the session trail, drawn as a lit ribbon threading the visited nodes
   in the reserved path color (Part 04, 4.3.4), fading with age but
   never disappearing during the session. The trail is the reader's
   spatial breadcrumb — MSTY-style history made walkable.
2. BACK/FORWARD walk the trail: Back refocuses the previous node
   (animating the pivot smoothly, 400 ms, the graph glides — the
   reader does not move), Forward re-advances. The trail forks like
   browser history: going back three and opening something new starts
   a new branch; old branches dim but remain visible.
3. SESSION PERSISTENCE: the trail (node ids + timestamps) saves to
   localStorage; returning within 7 days offers "resume your trail?"
   — and the delta-since-last-visit glow (Part 08) marks what changed
   since they left. Nothing leaves the device (Part 04, 4.9.5).
4. EGO MODE (the zoom-in exception to no-locomotion): trigger-holding
   a focused node for 600 ms "enters" it — the view transitions (fast
   fade through white, 250 ms, a comfort-safe cut, never a zoom-fly)
   to a small private scene: the node at center, its 1-hop
   neighborhood arranged on a sphere around the reader at fixed
   comfortable radius, edges as spokes. Stepping out (B) cuts back to
   the holotable exactly as it was. Ego mode is for READING a
   neighborhood; the holotable is for SEEING the world
   (fusion-adopted from Kimi).

--------------------------------------------------------------------------------
5.7 THE W-GYM (ONBOARDING, ~60 SECONDS, SKIPPABLE, REPLAYABLE)
--------------------------------------------------------------------------------

First VR session auto-offers the gym (skippable, always available from
Settings). Five lessons, each a single toy object on the holotable,
each gated on DOING, not reading (task-based validation,
fusion-adopted from GPT):

1. LESSON 1 — TABLE MANNERS (10 s): grab, move, scale a colored cube.
   Teaches: grips, the object-moves-not-you contract.
2. LESSON 2 — THE SLAB (15 s): a 4D ladder of five beads at different
   `w`. Task: swim the slab until the bright bead is solid. Teaches:
   left-trigger swim, ghosting, the w-gauge (the bead's tick visibly
   slides as the slab moves).
3. LESSON 3 — THE TESSERACT (15 s): a wireframe tesseract in
   projection mode. Task: snap-rotate XW four times and watch it turn
   inside out and come home. Teaches: hyper-rotation is a LOOP, not a
   fall; the inside-out motion is normal and reversible.
4. LESSON 4 — FIND IT AGAIN (15 s): six labeled beads; the gym
   hyper-rotates the object once, slowly; task: point at the bead that
   was previously focused. Teaches (and TESTS): tracking identity
   through a hyper-rotation — the core perceptual skill. Failing
   replays gently with a slower rotation; passing twice unlocks a
   quiet confidence.
5. LESSON 5 — THE TWIST (optional, 10 s): both grips, free-rotate the
   tesseract, then Reset. Completing it offers to enable Tier 2.
Graduation drops the reader onto the panorama in slice mode at
`w0 = 0` — among the established events, exactly where Part 5.2 starts
everyone.

--------------------------------------------------------------------------------
5.8 FLAT-SCREEN MAPPINGS (THE COMPANION BODY)
--------------------------------------------------------------------------------

Same state machine, same modes, same pivot rules, same reset/undo. The
mappings:
1. Left-drag: 3D rotation (yaw/pitch). Scroll: dolly zoom. Right-drag:
   pan the holotable.
2. Hyper-rotation mirrors Tier 1: TAB cycles the active hyper-plane
   (XW/YW/ZW, indicator in the corner w-gauge widget);
   SHIFT+left-drag rotates in the active plane; SHIFT+arrow keys snap
   90 degrees.
3. W / S keys (or CTRL+scroll): swim the slab (`w0`). E: toggle
   slice/projection. HOME: reset view. CTRL+Z: undo rotation.
4. Hover with mouse = hover card; click = focus; double-click = open;
   right-click = the context menu (same fixed order as the hand menu)
   AT THE CURSOR (Part 00, 0.7, invariant 2).
5. The corner w-gauge widget mirrors the wrist instrument: slab
   position, thickness, focused node tick, density histogram, active
   hyper-plane indicator.
6. URL state (Part 00, 0.7, invariant 4): `Q` (quantized), mode, `w0`,
   `epsilon`, pivot node, lens settings, active w-definition, edition
   — every view shareable; a Quest and a laptop opening the same link
   see the same sight.

--------------------------------------------------------------------------------
5.9 RED-LETTER CORRECTNESS RULES (VIOLATION = REJECTED WORK)
--------------------------------------------------------------------------------

1. ONE PROJECTION PER FRAME, both eyes consume the same 3D scene
   (Part 03, 3.7.4; asserted in debug builds, Part 04, 4.9.3).
2. THE WORLD NEVER MOVES THE READER: no camera animation in VR except
   the two sanctioned cuts (ego mode enter/exit), which are fades,
   never flights.
3. NO ROTATIONAL INERTIA anywhere in VR.
4. NOTHING VANISHES WITHOUT A TRACE: slice ghosting always on; any
   node removed by lens filters leaves a 400 ms fade so the reader
   sees WHERE it went; the hand menu's Lens item shows active filters
   as removable chips.
5. STEREO DISPARITY IS NEVER MANIPULATED as a w-cue; depth is real 3D
   depth only (fusion reject list).
6. `w` IS NEVER HUE (LAW 2 — restated here because this Part is where
   the temptation lives).
7. EVERY GESTURE REVERSIBLE: undo covers rotation; Back covers focus;
   Reset covers everything; and all three live on the first ring of
   the hand menu.
8. COMFORT SETTINGS (rotation rate, snap-only mode, wobble off, audio
   off, high-contrast rings) are honored EVERYWHERE, persisted in
   localStorage, and offered — not buried — at first session.

--------------------------------------------------------------------------------
5.10 VALIDATION PROTOCOL (HOW WE KNOW THE 4D WORKS)
--------------------------------------------------------------------------------

Before Milestone 1 is DONE (Part 13), five test sessions (Nir plus
anyone reachable — Madie counts, friends count) each complete, without
coaching beyond the w-gym: (1) find a named node in slice mode; (2)
perform one snap hyper-rotation and re-find the same node (the Lesson 4
skill in the wild); (3) swim from news to canon under w-definition 1
and say aloud roughly what changed; (4) use Back to retrace two steps;
(5) report comfort at session end (simple 1-5 scale, anything under 4
triggers a comfort review). Results go in the ledger as plain text.
This protocol repeats after any change to rotation, projection, or
comfort code.

--------------------------------------------------------------------------------
5.11 POINTERS
--------------------------------------------------------------------------------

The mathematics behind every gesture: Part 03. The rendering budget
every gesture must respect: Part 04. What the reading panel contains
and how provenance hover works inside it: Part 11 (with data from
Part 02). The delta-since-last-visit glow: Part 08. Comparison-scene
interaction variants (axis remapping, killer boxes): Part 09.
Milestone gates that cite this Part's validation protocol: Part 13.

================================================================================
END OF PART 05
================================================================================
