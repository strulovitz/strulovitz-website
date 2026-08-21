/*
================================================================================
 synthetic.js  --  FAKE DATA FOR MILESTONE 1 ("HELLO, TESSERACT")
================================================================================

 bible/part-13.md 13.2 build item 7 asks for exactly this: one tesseract plus
 about two hundred fake nodes sitting in fake w bands, so that the fourth
 dimension can be proven on the Quest 3 BEFORE any content pipeline exists.

 NOTHING IN THIS FILE IS REAL. No real article, model or company is described
 here. The names are deliberately generic placeholders so that nobody, ever,
 mistakes this scene for published content (that would violate LAW 7, the
 attribution law). When the real pipeline exists it will produce the same
 arrays, and this file gets deleted or kept only as a test fixture.

 THREE DESIGN RULES THIS FILE OBEYS

 1. DETERMINISM. Positions come from a hash of the node's own id, never from
    Math.random(). The same node lands in the same place on every machine, in
    every rebuild, forever, with nothing stored (bible/part-03.md 3.3.3). Run
    it twice, get byte-identical numbers. This is the habit the real layout
    stage must keep.

 2. THE MEANING OF w. The fourth coordinate here follows w-definition 1,
    ABSTRACTION (bible/part-03.md 3.5): low w is raw fresh news, high w is the
    settled encyclopedia. So swimming along w is watching news condense into
    knowledge. Even in fake data, the axis MEANS something, because a
    meaningless fourth axis teaches the reader nothing.

 3. COLOUR IS IDENTITY, NEVER w (LAW 2). Each cluster gets one fixed colour and
    keeps it. Nothing in this file may ever compute a colour from w.
================================================================================
*/

// -----------------------------------------------------------------------------
// A tiny deterministic hash, so this file needs no dependencies.
// -----------------------------------------------------------------------------

/**
 * FNV-1a over a string, returning a 32-bit unsigned integer. Small, ancient,
 * boring and perfectly adequate: we only need "the same input always gives the
 * same spread-out number".
 */
function hashString(text) {
  let h = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h >>> 0;
}

/** Turn a hash plus a salt into a number from 0 to 1. Deterministic. */
function unit(id, salt) {
  return (hashString(`${id}:${salt}`) >>> 8) / 0x01000000;
}

/** Deterministic number from -1 to +1. */
function signedUnit(id, salt) {
  return unit(id, salt) * 2 - 1;
}


// -----------------------------------------------------------------------------
// THE TESSERACT
// -----------------------------------------------------------------------------

/**
 * The sixteen corners of a four-dimensional cube, and the thirty-two edges
 * joining them.
 *
 * Why sixteen and thirty-two, in plain words: a square has 4 corners and 4
 * edges, a cube has 8 corners and 12 edges, and a tesseract has 16 corners and
 * 32 edges. The pattern for corners is doubling, because each new dimension
 * copies the whole shape and shifts the copy sideways. Two corners are joined
 * by an edge when they differ in exactly ONE coordinate.
 *
 * This is the object Nir must be able to rotate in the ZW plane, watch turn
 * inside out, and smile at. That smile is a formal acceptance criterion of
 * Milestone 1 (bible/part-13.md 13.2).
 */
export function buildTesseract(halfSize = 0.34) {
  const vertices = [];
  for (let i = 0; i < 16; i++) {
    vertices.push([
      (i & 1) ? halfSize : -halfSize,
      (i & 2) ? halfSize : -halfSize,
      (i & 4) ? halfSize : -halfSize,
      (i & 8) ? halfSize : -halfSize,
    ]);
  }
  const edges = [];
  for (let a = 0; a < 16; a++) {
    for (let bit = 0; bit < 4; bit++) {
      const b = a ^ (1 << bit);
      // Only add each edge once, from the lower index to the higher one.
      if (b > a) edges.push([a, b]);
    }
  }
  return { vertices, edges };
}


// -----------------------------------------------------------------------------
// THE FAKE KNOWLEDGE GRAPH
// -----------------------------------------------------------------------------

/**
 * The clusters. In the real project these are the "cities" of the map: a few
 * hundred canon concept nodes laid out once by a physics simulation, with news
 * items placed instantly between the concepts they are about
 * (bible/part-03.md 3.2 and 3.3). Here there are eight of them, placed by hand
 * on a rough sphere so the fake world has recognisable neighbourhoods to build
 * spatial memory against.
 *
 * The colour is the cluster's IDENTITY and never changes. It is not derived
 * from w and never may be (LAW 2).
 */
export const CLUSTERS = [
  { id: 'safety',      label: 'Safety',           colour: 0xff8a5c, centre: [-0.80,  0.34, -0.28] },
  { id: 'openweights', label: 'Open weights',     colour: 0x6ec6ff, centre: [ 0.82,  0.12,  0.34] },
  { id: 'benchmarks',  label: 'Benchmarks',       colour: 0xffd166, centre: [ 0.14, -0.62,  0.62] },
  { id: 'hardware',    label: 'Hardware',         colour: 0xa0e7a0, centre: [-0.40, -0.58, -0.66] },
  { id: 'policy',      label: 'Policy',           colour: 0xd8a0ff, centre: [ 0.52,  0.70, -0.46] },
  { id: 'agents',      label: 'Agents',           colour: 0x7ee8d8, centre: [-0.84, -0.14,  0.60] },
  { id: 'images',      label: 'Image models',     colour: 0xff9ec4, centre: [ 0.20,  0.72,  0.70] },
  { id: 'economics',   label: 'Money and costs',  colour: 0xc2b280, centre: [ 0.80, -0.52, -0.58] },
];

/**
 * The six w bands of w-definition 1 (bible/part-03.md 3.5), with the plain
 * one-sentence explanation each definition is legally required to have, and
 * which the wrist gauge shows the reader.
 */
export const W_BANDS = [
  { w: -1.0, name: 'Incoming',   plain: 'Just arrived, barely checked yet.' },
  { w: -0.5, name: 'Developing', plain: 'A story still moving.' },
  { w:  0.0, name: 'Established', plain: 'The settled news record. You start here.' },
  { w:  0.4, name: 'Absorbed',   plain: 'Old news whose lesson is already in the encyclopedia.' },
  { w:  0.7, name: 'Canon',      plain: 'Encyclopedia topics and explainers.' },
  { w:  1.0, name: 'Bedrock',    plain: 'The most time-tested ideas of the whole field.' },
];

// Harmless placeholder words. They exist only so hover cards have something to
// show and so the w-gym task "find the node called X" has a name to say.
const FAKE_SUBJECTS = [
  'Alpha', 'Beacon', 'Cascade', 'Dovetail', 'Ember', 'Foundry', 'Gradient',
  'Harbour', 'Ingot', 'Jetty', 'Kestrel', 'Lantern', 'Mosaic', 'Nimbus',
  'Orchard', 'Pennant', 'Quarry', 'Ribbon', 'Sextant', 'Thicket', 'Umbra',
  'Vellum', 'Willow', 'Xenon', 'Yardarm', 'Zephyr',
];
const FAKE_VERBS = [
  'report', 'review', 'measurement', 'comparison', 'explainer', 'note',
  'follow-up', 'correction', 'summary', 'briefing',
];

/**
 * Build the whole fake scene.
 *
 * Returns an object whose shape deliberately matches what the real exporter
 * will produce, so the renderer never has to change when real data arrives:
 *
 *   count      how many nodes there are
 *   points4    Float64Array, 4 numbers per node: x, y, z, w
 *   colours    Float32Array, 3 numbers per node: red, green, blue from 0 to 1
 *   radii      Float32Array, the BASE radius of each node before projection
 *   labels     array of strings, one per node
 *   bandOf     Int32Array, which w band each node sits in
 *   clusterOf  Int32Array, which cluster each node belongs to
 *   edges      Int32Array pairs of node indices
 *   tesseract  the 16 vertices and 32 edges, as its own little object
 */
export function buildSyntheticScene(nodeCount = 200) {
  const points4 = new Float64Array(nodeCount * 4);
  const colours = new Float32Array(nodeCount * 3);
  const radii = new Float32Array(nodeCount);
  const bandOf = new Int32Array(nodeCount);
  const clusterOf = new Int32Array(nodeCount);
  const labels = [];
  const ids = [];

  for (let i = 0; i < nodeCount; i++) {
    // The id is the ONLY source of randomness. Same id, same node, forever.
    const id = `fake-node-${String(i).padStart(4, '0')}`;
    ids.push(id);

    const clusterIndex = Math.floor(unit(id, 'cluster') * CLUSTERS.length) % CLUSTERS.length;
    const cluster = CLUSTERS[clusterIndex];
    clusterOf[i] = clusterIndex;

    // Scatter around the cluster centre, the way real event nodes are placed
    // analytically around the concepts they belong to (part-03.md 3.3).
    const spread = 0.17;
    const x = cluster.centre[0] + signedUnit(id, 'x') * spread;
    const y = cluster.centre[1] + signedUnit(id, 'y') * spread;
    const z = cluster.centre[2] + signedUnit(id, 'z') * spread;

    // Pick a w band, then jitter gently INSIDE the band, so motion along w is
    // continuous rather than stepped (part-03.md 3.5, w-definition 1).
    const bandIndex = Math.floor(unit(id, 'band') * W_BANDS.length) % W_BANDS.length;
    bandOf[i] = bandIndex;
    const w = W_BANDS[bandIndex].w + signedUnit(id, 'wjitter') * 0.08;

    const b = i * 4;
    // Keep everything inside the unit box, which the whole geometry assumes.
    points4[b] = Math.max(-1, Math.min(1, x));
    points4[b + 1] = Math.max(-1, Math.min(1, y));
    points4[b + 2] = Math.max(-1, Math.min(1, z));
    points4[b + 3] = Math.max(-1, Math.min(1, w));

    colours[i * 3] = ((cluster.colour >> 16) & 255) / 255;
    colours[i * 3 + 1] = ((cluster.colour >> 8) & 255) / 255;
    colours[i * 3 + 2] = (cluster.colour & 255) / 255;

    // Base radius varies a little so the crowd does not look machine-made.
    // NOTE, and this matters: the size a reader actually SEES is this number
    // multiplied by the projection scale, and by nothing else. Importance is
    // never shown by size (part-03.md 3.7.5).
    radii[i] = 0.011 + unit(id, 'radius') * 0.006;

    const subject = FAKE_SUBJECTS[Math.floor(unit(id, 'subject') * FAKE_SUBJECTS.length)];
    const verb = FAKE_VERBS[Math.floor(unit(id, 'verb') * FAKE_VERBS.length)];
    labels.push(`${subject} ${verb}`);
  }

  // A few fake edges, only between nodes of the same cluster, so the picture
  // shows structure instead of soup. Capped at six per node exactly like the
  // real export prunes edges for legibility (part-03.md 3.4.1).
  const edgeList = [];
  for (let i = 0; i < nodeCount; i++) {
    let made = 0;
    for (let attempt = 0; attempt < 24 && made < 3; attempt++) {
      const j = Math.floor(unit(ids[i], `edge${attempt}`) * nodeCount) % nodeCount;
      if (j <= i) continue;
      if (clusterOf[j] !== clusterOf[i]) continue;
      edgeList.push(i, j);
      made++;
    }
  }

  return {
    count: nodeCount,
    points4,
    colours,
    radii,
    labels,
    ids,
    bandOf,
    clusterOf,
    edges: new Int32Array(edgeList),
    tesseract: buildTesseract(),
  };
}

/**
 * A histogram of how much content lives at each w, for the density silhouette
 * on the wrist gauge (bible/part-05.md 5.3.2). Plain counting, no cleverness.
 */
export function wHistogram(points4, count, buckets = 32) {
  const histogram = new Float32Array(buckets);
  for (let i = 0; i < count; i++) {
    const w = points4[i * 4 + 3];
    let bucket = Math.floor(((w + 1) / 2) * buckets);
    if (bucket < 0) bucket = 0;
    if (bucket >= buckets) bucket = buckets - 1;
    histogram[bucket]++;
  }
  let peak = 0;
  for (let i = 0; i < buckets; i++) peak = Math.max(peak, histogram[i]);
  if (peak > 0) for (let i = 0; i < buckets; i++) histogram[i] /= peak;
  return histogram;
}
