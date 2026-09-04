/*
================================================================================
A REAL GALAXY, LOADED FROM DISK
================================================================================

WHAT THIS IS, IN ONE SENTENCE
The scene that reads one edition's four-dimensional world out of a JSON file
and hands it to the renderer in exactly the shape the fake world used, so the
renderer never had to change when real content arrived.

WHY THERE IS ONE FILE PER MODEL, NOT ONE FOR THE MAGAZINE
Each edition is written entirely by one model, including its tags, its
encyclopedia entries and its opinion about which story a reader should go to
next - and those choices are what decide where things sit. So each edition has
its own map, and switching edition rearranges the sky (DECISIONS.md decision
20). A model that links unrelated things gets a visibly stranger galaxy. That
is the point of the magazine, not a fault in it.

THE TWO KINDS OF NODE
1. STORY nodes sit at the raw-news end of the fourth dimension and creep inward
   as they age.
2. CONCEPT nodes - the encyclopedia - sit at the settled-knowledge end and do
   not move.
So sliding the slab outward shows you this week, and sliding it inward shows you
what the field has already digested (bible/part-03.md 3.5).

COLOUR IS NEVER MEANING THAT MATTERS (bible/part-00.md LAW 2)
Colour here groups nodes by their leading tag so a crowd is readable at a
glance. Nothing important is EVER carried by colour alone: the kind of node,
its position along the fourth dimension and its title are all available in
words. Colour is decoration that helps, never the only way to know something.
================================================================================
*/

import { buildTesseract } from './synthetic.js';

/**
 * A small fixed palette. Tags are assigned a colour by hashing their own name,
 * so the same tag is always the same colour, on every machine, forever - and a
 * new tag appearing next month does not recolour everything that came before.
 */
const PALETTE = [
  0xff8a5c, 0x6ec6ff, 0xffd166, 0xa0e7a0, 0xd8a0ff,
  0x7ee8d8, 0xff9ec4, 0xc2b280, 0xb0c4ff, 0xffb3a7,
];

// The encyclopedia gets one reserved colour of its own, because "is this a news
// story or a permanent explanation" is the single most useful thing to see from
// a distance. It is also stated in words on every hover card.
const CONCEPT_COLOUR = 0xf2e8d5;

function hashString(text) {
  let hash = 2166136261;
  for (let i = 0; i < text.length; i++) {
    hash ^= text.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function colourFor(node) {
  if (node.kind === 'concept') return CONCEPT_COLOUR;
  const leadingTag = (node.tags && node.tags.length) ? node.tags[0] : node.slug;
  return PALETTE[hashString(leadingTag) % PALETTE.length];
}

/**
 * Which of the named w bands a node falls in. Used for the wrist gauge and the
 * hover card, so a reader is never shown a bare number without a word for it.
 */
export const GALAXY_BANDS = [
  { w: -1.00, name: 'Just happened', plain: 'Raw news. Days old at most.' },
  { w: -0.50, name: 'Still moving', plain: 'A story the field is still digesting.' },
  { w: 0.00, name: 'On the record', plain: 'Settled news. It happened, and we know what happened.' },
  { w: 0.70, name: 'The encyclopedia', plain: 'A permanent explanation, written to stay true.' },
];

function bandIndexFor(w) {
  let best = 0;
  let bestDistance = Infinity;
  for (let i = 0; i < GALAXY_BANDS.length; i++) {
    const distance = Math.abs(GALAXY_BANDS[i].w - w);
    if (distance < bestDistance) { bestDistance = distance; best = i; }
  }
  return best;
}

/**
 * Fetch the list of editions that exist, so the switcher can be built without
 * anything being hardcoded. Adding a model tomorrow makes it appear here with
 * no change to any page (DECISIONS.md decision 18).
 */
export async function loadEditionList(base = 'data/galaxies') {
  const response = await fetch(`${base}/index.json`, { cache: 'no-cache' });
  if (!response.ok) throw new Error(`No edition list at ${base}/index.json`);
  return response.json();
}

/**
 * Load one edition's galaxy and return it in the renderer's shape.
 *
 * The returned object carries the same fields the fake world did - count,
 * points4, colours, radii, labels, ids, bandOf, clusterOf, edges, tesseract -
 * plus the real content the hover card needs: what kind each node is, its
 * one-line summary, and where to read it.
 */
export async function loadGalaxy(modelSlug, base = 'data/galaxies') {
  const response = await fetch(`${base}/${modelSlug}.json`, { cache: 'no-cache' });
  if (!response.ok) throw new Error(`No galaxy for ${modelSlug}`);
  const galaxy = await response.json();

  const nodes = galaxy.nodes || [];
  const count = nodes.length;
  const points4 = new Float64Array(count * 4);
  const colours = new Float32Array(count * 3);
  const radii = new Float32Array(count);
  const bandOf = new Int32Array(count);
  const clusterOf = new Int32Array(count);
  const labels = [];
  const ids = [];
  const kinds = [];
  const summaries = [];
  const tagsOf = [];
  const pageOf = [];
  const thumbsOf = [];

  const indexOfId = new Map();

  /*
   * THE REGIONS OF THIS GALAXY, AND THEIR NAMES.
   *
   * A region is a tag this model chose. The floating words over the world are
   * therefore this editor's own vocabulary, which is worth seeing: two models
   * given the same five stories name the territory differently.
   *
   * Every node belongs to the region of its FIRST tag, because that is the tag
   * the model itself put first. The encyclopedia is its own region, since "news
   * or permanent explanation" is the most useful thing to see from a distance.
   */
  const tagCounts = new Map();
  for (const node of nodes) {
    const tag = (node.tags && node.tags.length) ? node.tags[0] : null;
    if (tag) tagCounts.set(tag, (tagCounts.get(tag) || 0) + 1);
  }
  const regionNames = [...tagCounts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([tag]) => tag);
  const clusters = regionNames.map((tag) => ({
    id: tag,
    label: tag.replace(/-/g, ' '),
    colour: PALETTE[hashString(tag) % PALETTE.length],
  }));
  const ENCYCLOPEDIA_REGION = clusters.length;
  clusters.push({ id: 'encyclopedia', label: 'the encyclopedia', colour: CONCEPT_COLOUR });
  const regionIndexOf = new Map(regionNames.map((tag, index) => [tag, index]));

  for (let i = 0; i < count; i++) {
    const node = nodes[i];
    indexOfId.set(node.id, i);
    ids.push(node.id);
    labels.push(node.headline || node.slug);
    kinds.push(node.kind);
    summaries.push(node.tldr || '');
    tagsOf.push(node.tags || []);
    // Where this node is READ. Every edition's pages live under its own model
    // folder, so nothing has a privileged position (DECISIONS.md decision 18).
    pageOf.push(node.kind === 'story'
      ? `stories/${node.slug}/${modelSlug}.html`
      : `ideas/${node.slug}/${modelSlug}.html`);
    // The little picture on the hover card. Every node carries an
    // illustration (part-00.md 0.6 rung 4): a story shows this edition's own
    // picture of that story; an encyclopedia idea shows this edition's own
    // take on that idea. If a picture has not been rendered yet (or failed),
    // the card quietly leaves the space out rather than showing a broken
    // box - the entry still reads fine without it.
    thumbsOf.push(node.kind === 'story'
      ? `data/thumbs/${modelSlug}/${node.slug}.png`
      : `data/idea-thumbs/${modelSlug}/${node.slug}.png`);

    const base4 = i * 4;
    points4[base4] = clamp(node.x);
    points4[base4 + 1] = clamp(node.y);
    points4[base4 + 2] = clamp(node.z);
    points4[base4 + 3] = clamp(node.w);

    const colour = colourFor(node);
    colours[i * 3] = ((colour >> 16) & 255) / 255;
    colours[i * 3 + 1] = ((colour >> 8) & 255) / 255;
    colours[i * 3 + 2] = (colour & 255) / 255;

    // The encyclopedia is drawn slightly larger, because a permanent
    // explanation is a landmark and news is weather. Size never means
    // importance-within-a-kind (bible/part-03.md 3.7.5).
    radii[i] = node.kind === 'concept' ? 0.017 : 0.013;

    bandOf[i] = bandIndexFor(points4[base4 + 3]);
    clusterOf[i] = node.kind === 'concept'
      ? ENCYCLOPEDIA_REGION
      : (regionIndexOf.get((node.tags || [])[0]) ?? ENCYCLOPEDIA_REGION);
  }

  // Which nodes are the ARTICLES. The magazine opens in their band (Nir,
  // 2026-09-04) - see homeBandOfArticles below.
  const storyIndices = [];
  for (let i = 0; i < count; i++) {
    if (kinds[i] === 'story') storyIndices.push(i);
  }

  const edgePairs = [];
  const edgeWhy = [];
  for (const edge of galaxy.edges || []) {
    const from = indexOfId.get(edge.from);
    const to = indexOfId.get(edge.to);
    if (from === undefined || to === undefined) continue;
    edgePairs.push(from, to);
    edgeWhy.push(edge.why || '');
  }

  return {
    count,
    homeW: homeBandOfArticles(points4, storyIndices),
    points4,
    colours,
    radii,
    labels,
    ids,
    bandOf,
    clusterOf,
    edges: new Int32Array(edgePairs),
    tesseract: buildTesseract(),
    // The named regions of this world, in this editor's own words.
    clusters,
    // Everything below is extra, and the renderer may ignore it.
    isReal: true,
    modelSlug,
    shortName: galaxy.short_name,
    company: galaxy.company,
    wMeaning: galaxy.w_meaning,
    counts: galaxy.counts,
    kinds,
    summaries,
    tagsOf,
    pageOf,
    thumbsOf,
    edgeWhy,
    bands: GALAXY_BANDS,
  };
}

function clamp(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return 0;
  return Math.max(-1, Math.min(1, number));
}


/**
 * The busiest place along the fourth dimension: where the most content lives.
 *
 * This is where a reader is put when the page opens, and the reason it is
 * computed rather than fixed is that a reader must NEVER arrive to an empty
 * world. In a young magazine almost everything is either brand-new news or an
 * encyclopedia entry, and the middle of the axis is the empty gap between the
 * two. Deliberately simple counting, no cleverness: slide a window the width of
 * the default slab across the axis and keep the fullest spot.
 */
/**
 * The band the magazine OPENS in - Nir's ruling, 2026-09-04, his words:
 * "the articles need to be closest to the user, not the concepts, when the
 * magazine opens." The old rule opened at the BUSIEST band, and because a
 * model writes far more encyclopedia entries than there are articles, the
 * busiest band was always the encyclopedia - so the reader landed among
 * the concepts and, in Nir's words, "never dreamed that the articles are
 * there." The home band is therefore the articles' own band, found among
 * the STORY nodes only (the encyclopedia then hangs in view as fog, and
 * never disappears - see slabVisibility's fog floor).
 */
function homeBandOfArticles(points4, storyIndices, window = 0.25) {
  if (!storyIndices.length) return 0;
  let bestW = 0;
  let bestCount = -1;
  for (let step = 0; step <= 40; step++) {
    const w = -1 + (step / 40) * 2;
    let here = 0;
    for (const i of storyIndices) {
      if (Math.abs(points4[i * 4 + 3] - w) <= window / 2) here++;
    }
    if (here > bestCount) { bestCount = here; bestW = w; }
  }
  return Math.round(bestW * 100) / 100;
}
