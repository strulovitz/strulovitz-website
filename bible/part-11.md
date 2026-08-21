================================================================================
AI PANORAMA — THE BIBLE — PART 11 OF 13
PUBLISHING AND DISCOVERY
Version 1.0 — August 2026
Obeys: Part 00 (Vision and Invariants), Part 01 (Architecture),
Part 02 (Data Model), Part 08 (Advantage 0), Part 10 (Editions).
================================================================================

--------------------------------------------------------------------------------
11.0 PURPOSE OF THIS PART
--------------------------------------------------------------------------------

This Part defines everything the world can find, link, cite, embed,
subscribe to, and download: the static HTML page per node (the real
website, as far as search engines and AI assistants are concerned), the
feeds, the stable citation system, the monthly ISSUE and its cover
disc, the published datasets, and the zero-budget discovery strategy.

The strategic truth (fusion-settled, 6/6): A 3D/4D SITE IS INVISIBLE.
Google cannot crawl a tesseract. Link previews cannot screenshot a
WebXR session. AI assistants — increasingly the way people find
things — read text, not shaders. Therefore every piece of knowledge in
the project exists FIRST as an honest, fast, beautiful plain HTML page,
and the 4D atlas is the crown experience layered on top. The kingdom
pays for the crown, and the crown makes the kingdom unforgettable.

--------------------------------------------------------------------------------
11.1 THE HTML KINGDOM: ONE REAL PAGE PER NODE
--------------------------------------------------------------------------------

1. EVERY publishable node (event, canon, arc, standing question,
   benchmark card set, scoreboard issue, comparison template) ships as
   a static HTML page in the export: `html/<id>/index.html` (Part 02,
   2.10.8). Server-side nothing; hand-written nothing; ALL generated
   by the export builder from the same data as the atlas.
2. PAGE ANATOMY (event example): headline; TLDR; the prose with
   PROVENANCE HOVER (each sentence carries its claim ids as data
   attributes; hovering/tapping a sentence highlights its claims in
   the source list below — the claim-level provenance UI, rendered in
   plain accessible HTML+JS); the conflicts section; the image (with
   generating-model label per LAW 7); ELI5 concept links; the full
   source list with locator deep links (paragraph anchors, YouTube
   timestamp links — the exact-second citations, Part 02, 2.3.4);
   lifecycle badge + last-verified date; the cite key; and ONE
   prominent button: "OPEN THIS NODE IN THE ATLAS (3D / VR)" — the
   doorway from kingdom to crown, deep-linking the exact node
   (Part 05, 5.8.6).
3. MACHINE SURFACES on every page: OpenGraph + Twitter cards (the
   node's image + TLDR — link previews in Telegram/WhatsApp/Discord
   are the project's true front page); JSON-LD structured data
   (Article/Dataset/FAQ as appropriate); canonical URLs (flagship
   edition canonical, others noindex per Part 10, 10.5.4).
4. ASSISTANT SURFACES (fusion-settled: "assistants reading you is the
   new backlink"): `llms.txt` at the site root (a plain-text map of
   the site's structure and top content, maintained by the export
   builder); and a MARKDOWN MIRROR of every HTML page
   (`html/<id>/index.md`) — clean, attribution-preserving, trivially
   ingestible. When a reader asks their assistant "what changed in AI
   this month?", the assistant that found our changelog page quotes
   us — with our cite keys attached. That is discovery in 2026.
5. ACCESSIBILITY: the HTML kingdom is the accessible version by
   design: semantic headings, alt text on all images (generated from
   the image prompt + claims), keyboard navigation, no reliance on
   color (LAW 2's cousin: information never lives in hue alone),
   readable at any zoom. The atlas is an ENHANCEMENT; no knowledge is
   VR-gated. This is both ethics and reach.
6. PERFORMANCE: every page under 100 KB before images (plain HTML + a
   tiny shared CSS/JS bundle); images lazy-loaded WebP; zero
   third-party requests (Part 07, 7.3.2). The kingdom loads instantly
   on a phone in a field in Romania. That sentence is a test case.

--------------------------------------------------------------------------------
11.2 CITATION INFRASTRUCTURE
--------------------------------------------------------------------------------

1. CITE KEYS: every published node carries its permanent key
   (AP-YYYY-NNNN, Part 02, 2.1.1), displayed on the page with a
   one-tap copy in three formats: plain text, BibTeX, and CSL-JSON.
   URLs are permanent: `strulovitz.org/ap/AP-2026-0142` redirects
   (client-side map, static per LAW 4) to the current canonical page.
2. VERSIONED CITATIONS: canon nodes (mutable, versioned per Part 02)
   support citing a SPECIFIC REVISION: `AP-can-agentic-coding@v7` —
   the revision history page shows every version with diffs. An
   encyclopedia that can be cited stably at a moment in time is rare
   and academically precious.
3. THE ERRATA FEED: all Correction records (Part 02, 2.6) publish to
   a dedicated page + RSS feed. Prominently linked from the footer of
   every page: "We publish our mistakes." Nobody else leads with
   that; it is the cheapest trust signal in existence and it is
   entirely honest.
4. MERGED/RENAMED nodes: permanent client-side redirect entries
   (Part 02, 2.4 merge rules) — a cite key, once issued, resolves
   forever.

--------------------------------------------------------------------------------
11.3 FEEDS AND SUBSCRIPTIONS
--------------------------------------------------------------------------------

All static files, rebuilt each export (LAW 4-compatible by nature):

1. RSS/Atom: the firehose (all new/updated nodes); the WEEKLY DIGEST
   (changelog summary, the flagship feed for humans); per-community
   feeds (safety, open-weights, policy...); the errata feed; the
   scoreboard feed (new edition results).
2. THE CHANGELOG PAGES (Part 08, 8.5.1): `/changed/this-week/`,
   `/changed/this-month/`, `/changed/since/<date>/` (client-side
   rendering of the diff data for arbitrary dates) — the pages that
   answer the most valuable query in the field: "what did I miss?"
   These pages are expected to be the top external entry point after
   the panorama itself, and they are heavily cross-linked.
3. THE TELEGRAM CHANNEL (public, read-only; distinct from the control
   bot, Part 07, 7.8): auto-posts the weekly digest + the weekly diff
   video (Part 08, 8.5.3). Zero human minutes; one more surface where
   a share can happen.

--------------------------------------------------------------------------------
11.4 THE MONTHLY ISSUE (THE HOMAGE MADE REAL)
--------------------------------------------------------------------------------

The PC Format spirit, expressed without imitating anyone's trade dress
(Part 00, 0.9.6):

1. THE ISSUE: each month, the export builder assembles a magazine-
   shaped artifact: COVER (flagship edition's cover art + the month's
   defining headline); CONTENTS (the month's stories by community,
   with page-style numbering for charm); THE GUIDED WALK (a curated
   path through the atlas — 10 nodes with narrative connective text,
   readable as an article AND replayable as a trail in 3D/VR via its
   share-URL); the month's changelog; the scoreboard summary; the
   hindsight check-in (what last year's issue got right/wrong); and
   the panorama POSTER (a rendered still of this month's map,
   suitable for printing — readers hang the field on their wall).
2. FORMATS: an HTML issue page + a print-faithful PDF (generated at
   export from the same content). The PDF is the SHAREABLE OBJECT —
   the thing that travels through email and chat groups where links
   die, carrying the site's name on every footer.
3. THE COVER DISC (fusion-adopted from GLM, the beloved joke made
   useful): each issue offers a ZIP download of the ENTIRE static
   site as of that issue — the whole magazine, atlas included, works
   offline from a local folder (the site is static files; it RUNS
   from a folder by design, LAW 4's gift). Uses: offline reading,
   archival ("the field as it stood in August 2026"), classrooms
   without reliable internet, and the pure PC-Format-cover-CD grin of
   it. The disc page is also the project's cleanest SPONSOR SLOT
   (LAW 9: "this month's disc sponsored by X", clearly marked, zero
   influence on content — sponsoring the DISTRIBUTION of the
   magazine, never its judgment).
4. ISSUE CALENDAR (the cadence that drives Parts 06/10/12): story-set
   freeze on the 25th; edition runs overnight next; scoreboard +
   assembly by the 28th; Nir's review tap; publish with the month's
   final export. The monthly rhythm is the project's heartbeat —
   weekly builds keep the site alive; monthly issues give people a
   REASON TO TELL SOMEONE ("did you see this month's AI PANORAMA?").

--------------------------------------------------------------------------------
11.5 PUBLISHED DATASETS (THE INBOUND-LINK ENGINES)
--------------------------------------------------------------------------------

Per the fusion consensus: datasets earn better inbound links than
articles. All CC-BY-4.0, versioned, with DOIs (Zenodo), mirrored on
HuggingFace datasets, each with a plain README and a citation block:

1. THE PRICE/SPEC HISTORY ARCHIVE (Part 09, 9.4.3): weekly OpenRouter
   snapshots from August 2026 onward. Uniquely ours with every week
   that passes.
2. THE FAITHFULNESS SCOREBOARD (Part 10, 10.4): longitudinal, real-
   work, per-metric, per-model. The academically citable one.
3. THE CLAIM CORPUS (curated subsets): claims with spans, locators,
   evidence classes, and SAME_FACT_AS/CONTRADICTS clusters — a
   grounding/verification research resource harvested from our own
   pipeline (sources credited per LAW 7; only license-compatible
   material included).
4. THE HINDSIGHT RECORD (Part 08, 8.7): durability predictions and
   their gradings — a dataset about forecasting news importance that
   simply does not exist elsewhere.
Each dataset page on the site links its DOI, its HuggingFace mirror,
and the methodology; each external mirror links BACK to the site.
Researchers citing the data cite the magazine (Madie clause:
reputation compounds).

--------------------------------------------------------------------------------
11.6 EMBEDS AND OUTBOUND ARTIFACTS
--------------------------------------------------------------------------------

1. COMPARISON EMBEDS (Part 09, 9.7.2): iframe widgets for bloggers
   and newsletters, each carrying the corner mark and a deep link.
2. EGO-GRAPH EMBEDS (fusion-adopted from GLM): an iframe rendering a
   node's 1-hop neighborhood in interactive 3D (non-VR) — "here is
   this story's place in the field", embeddable under any external
   article that cites us.
3. STILL EXPORTS with baked attribution margins (Part 09, 9.7.3) for
   posts and slides.
4. THE WEEKLY DIFF VIDEO (Part 08, 8.5.3) — natively shareable proof
   of life.
5. ALL embeds and stills are generated from export data and served as
   static files (LAW 4) — an embed is just our site in a smaller
   window.

--------------------------------------------------------------------------------
11.7 THE DISCOVERY STRATEGY (ZERO BUDGET, WRITTEN DOWN)
--------------------------------------------------------------------------------

No ads, no promotion spend, no growth hacks. The strategy is: BE THE
MOST LINKABLE OBJECT IN THE FIELD, then let compounding do the work.
The mechanisms, ranked by expected yield:

1. THE CHANGELOG PAGES + WEEKLY DIGEST — the recurring utility that
   turns one visit into a habit ("what did I miss?" has one good
   answer on the internet, and it is ours).
2. LINK PREVIEWS — every OG card is designed to be worth a tap: node
   image, sharp TLDR, the cite key. Most sharing happens in private
   chats; the preview IS the ad we never pay for.
3. DATASETS + DOIs (11.5) — researcher citations are permanent,
   high-authority links.
4. ASSISTANT INGESTION (11.1.4) — llms.txt + markdown mirrors make us
   the easiest high-quality source to quote; assistants propagate our
   cite keys.
5. EMBEDS (11.6) — every embed is a doorway on someone else's page.
6. THE MONTHLY ISSUE PDF + COVER DISC — artifacts that travel where
   links do not.
7. THE VR WOW — the crown's role in discovery: nobody else HAS a 4D
   VR encyclopedia; every demo at a meetup, every short screen-
   capture of a hyper-rotation, every "you have to put on the headset
   for this" moment is unreplicable word-of-mouth. The atlas converts
   the curious into the loyal; the kingdom converts the loyal into
   linkers.
8. PATIENCE AS POLICY: no engagement mechanics, no clickbait (banned
   by Part 06, 6.6.1), no growth theater. The project's growth curve
   is expected to be slow, then sudden — trust compounds exactly like
   the citation inflow of Part 08: quietly, then all at once.

--------------------------------------------------------------------------------
11.8 EXPORT CONTRACT AND VALIDATION
--------------------------------------------------------------------------------

The export builder ships, per Part 02, 2.10 and this Part: all HTML +
markdown mirrors, llms.txt, all feeds, changelog pages, the issue
artifacts (HTML/PDF/ZIP on issue months), dataset export files,
redirect maps, sitemap.xml, robots.txt (welcoming, with a note that
the site is fully static and crawl-friendly). The validator (Part 12)
checks: every node has its HTML + markdown pair; every internal link
and redirect resolves; every page carries OG tags, JSON-LD, cite key,
canonical/noindex correctness per edition rules; feeds parse; the ZIP
opens and runs from a local folder. A kingdom page that fails
validation blocks the build exactly like a broken binary — the HTML
is not a second-class citizen; it is the citizenry.

--------------------------------------------------------------------------------
11.9 POINTERS
--------------------------------------------------------------------------------

Changelog data source: Part 08. Scoreboard content: Part 10.
Comparison embeds' data: Part 09. The atlas deep links that kingdom
pages open: Part 05, 5.8.6. Sponsor rules the disc slot obeys: LAW 9,
Part 00. Issue calendar operations and the validator: Part 12. The
security rules all pages obey (CSP, escaping, no third-party):
Part 07, 7.3.

================================================================================
END OF PART 11
================================================================================
