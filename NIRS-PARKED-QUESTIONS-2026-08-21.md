# NIR'S THREE QUESTIONS FROM 2026-08-21, PARKED ON PURPOSE

He asked these the first time he flew through a real edition, and then said to
stop rather than spend more. They are written down so that next month nobody has
to remember them, and so that whoever picks this up does not "improve" any of it
by guessing.

**None of the three costs money.** They are code, not model calls. Nothing here
requires a single API request. Only re-rendering editions costs anything, and
that is not needed for any of this.

---

## QUESTION 1 - IS IT AVAILABLE IN VR, IN 4D?

**Answered already: yes.** The same page carries both bodies. On the Quest 3,
press **Enter VR**, or serve it over https with `./ops/look-at-the-site.sh
headset` because a browser refuses to start VR over a plain connection. A real
edition loads in the headset exactly as it does on the screen; nothing about the
galaxy loader is screen-only.

**CLOSED IN CODE 2026-09-03, HUMAN CHECK PENDING:** the headset now has BOTH
halves. (1) A real hover card of its own - headline, one-line summary, and for
a story the PICTURE that edition made for it - drawn on a canvas, hung above
the hovered node, billboarded, constant angular size, 150 ms dwell like the
screen card. (2) The READING panel: a second trigger on a focused node opens
the node's whole reading page - headline, summary, full-size picture, the
complete article, key points, read-next links, sources - fetched from the
very same page a screen click opens, on a body-anchored panel that scrolls
with the thumbstick and closes with B (part-05.md 5.5.4, the part-04.md 4.5.4
sanctioned in-scene-quad fallback at high texture density). What remains is
the part no machine can do: a real headset session to confirm both feel right
(part-05.md 5.10's validation protocol is human sessions; the machine half -
zero console errors, all 113 checks green, selectors verified against the
real pages - passed 2026-09-03).

---

## QUESTION 2 - WHY IS THE TESSERACT THERE, AND SHOULD IT BE GREYED OUT?

**Why it is there:** it is the reference frame. A four-dimensional rotation
applied to a cloud of scattered dots looks like the dots sliding around at
random, because there is nothing rigid to compare them against. The tesseract is
a shape whose *correct* behaviour under a 4-D turn the eye can learn, so it makes
the rotation legible. It is also what the whole w-gym teaches against.

**His observation, and it is correct:** it is drawn as brightly as the content.
That is backwards. The frame should whisper and the news should shout. His own
words: "maybe it needs to be more greyed out, like not as prominent white as the
nodes and edges".

**Where the fix lives, for whoever does it:** `site/src/vr/panorama.js`, in the
tesseract's own material and in `updateTesseract`. Dim it, and consider making it
dim FURTHER while the reader is hovering or reading something, then come back
when they start rotating again - the frame is only needed while the view is
moving. Do not delete it: without it, a 4-D turn stops being teachable, and
bible/part-05.md's lessons depend on it.

**Not yet decided by Nir:** how dim, and whether it should fade in and out with
motion or simply sit quieter all the time. Ask him.

---

## QUESTION 3 - WHY ARE NODES CONNECTED TO EACH OTHER RATHER THAN BRANCHING OFF A STEM?

This is the real design question of the three, and it was deliberately NOT
answered in a rush.

**Why it currently looks the way it does:** the links between nodes ARE the
content. Each edition's model chose its own tags, wrote its own encyclopedia
entries and named which story a reader should go to next, and those three
choices are the only thing that decides what sits beside what. Comparing those
choices between editions is the entire point of the magazine (DECISIONS.md
decision 20: "if one editor in Wikipedia is dumb, and make dumb links, then this
is also a test of intelligence that we want"). A peer-to-peer web is the honest
picture of "this editor thinks these two things are related".

**What Nir is describing instead:** a hierarchy. A trunk, branches coming off
it, and leaves at the ends - "each node needs to be like a branch coming out of a
bigger branch (stem)". That is how an encyclopedia actually FEELS to use, and it
may well read better in four dimensions than a mesh of equal threads, because a
mesh has no natural place to start.

**The genuine tension, stated plainly so nobody papers over it:** a hierarchy
needs somebody to decide what the trunk IS. If we decide it, we are doing
editorial work the models are supposed to be doing, and the comparison stops
being purely theirs. If each model decides it, the brief has to ask for it,
which means the editorial brief changes and every existing edition would have to
be written again to stay comparable.

**Three ways it could go, none chosen:**
1. Keep the mesh, and make the encyclopedia visually the trunk it already half
   is - concepts sit deeper along the fourth dimension, and stories hang off
   them. This is nearly free: it is a change to edge drawing and to the layout's
   forces, no re-rendering, no brief change.
2. Ask each edition's model for a hierarchy explicitly - "which of your concepts
   is the parent of which" - which is honest and comparable, but changes the
   brief and therefore needs every edition rewritten.
3. Derive a trunk mechanically from what already exists, for instance by
   counting how many stories lean on each concept and treating the most-leaned-on
   as trunk. Free, no brief change, but it is OUR judgement wearing the model's
   coat, which is exactly the kind of quiet interference DECISION 16 forbids.

**Ask Nir which, and do not pick one for him.**

---

## WHAT IT ACTUALLY COST, SINCE MONEY IS WHY WE STOPPED

Measured, not estimated, from the renderings themselves:

| model | per edition |
|---|---|
| Gemini 3.7 Flash | $0.0098 |
| GPT-5.6 Terra | $0.0540 |
| Claude Sonnet 5 | $0.0809 |
| Grok 4.6 | $0.0934 |

Five stories written by all eight models comes to roughly **$2.30 in total**, at
full immediate price. In batch, which is the same models at half price with a
24-hour wait, the same work is about **$1.15**. One story across all eight
editions is about **46 cents**, or **23 cents** in batch.

That is worth knowing before deciding this is expensive.
