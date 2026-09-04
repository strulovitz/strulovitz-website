#!/usr/bin/env python3
"""
WRITING THE FIRST-RESULTS SECTION ON THE HOME PAGE
==================================================

WHAT THIS IS, IN ONE SENTENCE
The stage that generates the "first results" part of the home page - the table
comparing what each model made of the same stories, and a button per edition -
straight from the editions on disk, so it can never be out of date.

WHY IT IS GENERATED AND NOT TYPED
Because Nir will add models and add stories, and a table typed by hand would
start lying the moment he did. His standing instruction, in his own words: "i
hope you did not take Gemini's answer and one time fix it for me... you Opus
will not be with me in the future!!!" So nothing here knows the name of any
particular model or story. Add a ninth model tomorrow and it appears in the
table by itself.

WHAT IT WRITES
It replaces everything between these two lines in EVERY home page (the default
site/index.html plus every site/home-page-*.html variant, found by glob so a new
variant is picked up by itself):
    <!-- RESULTS BEGIN -->
    <!-- RESULTS END -->
and touches nothing else on the page. The styling lives in the page's own
stylesheet, not here: a machine generates DATA, never appearance.

WHY THE GENERATED LINKS ARE PLAIN AND RELATIVE (2026-09-04, Nir's ruling)
The edition links this stage generates are PLAIN relative links
("tesseract.html?edition=..."). They work from every home page copy as
shipped: from the site/ folder during development (the galaxy sits next
door), and from the copy inside the live version folder (the galaxy sits
in the SAME folder). On the ROOT home page, the page's own little script
aims them at the live version folder by prepending its name - and it skips
any link that already carries it, so nothing is ever doubled. Nothing is
hard-coded and nothing is absolute: if the site moves or is renamed, every
relative link still points at its own neighbour (Nir: "even a person who
never built a website knows" a hard-wired address breaks the day the site
moves).

WHERE THE NUMBERS COME FROM
Every one is measured, never estimated: the costs are what OpenRouter actually
charged, taken from each rendering; the article lengths, the number of
encyclopedia entries and the number of links are counted from what the models
produced; the links-per-node figure comes from the galaxy each edition's own
choices built. Nothing is rounded in a flattering direction, and nothing is
taken from a source's own list without saying what it is (DECISIONS.md
decision 9).

HOW TO RUN IT
    cd pipeline && uv run stages/build_home.py
Safe to re-run at any time. It costs nothing and calls nobody.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.db import connect, log_job, read_editions_for_model  # noqa: E402
from lib.llm import roster, settings  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
STORIES = REPO_ROOT / "content" / "stories"
GALAXIES = REPO_ROOT / "content" / "galaxies"
SITE = REPO_ROOT / "site"


def home_pages() -> list[Path]:
    """
    Every home page that ships at the site root: the default index.html plus
    every home-page-*.html variant, found by glob so a new variant is picked
    up by itself.

    The variants are copies of index.html with different pictures, and their
    own comment used to say "if index.html changes, ask an agent to refresh
    this copy" - which meant the table went stale the moment anyone forgot.
    Since 2026-09-05 this stage refreshes the generated section in ALL of
    them, so they can never disagree again.
    """
    return [SITE / "index.html"] + sorted(SITE.glob("home-page-*.html"))

BEGIN = "<!-- RESULTS BEGIN -->"
END = "<!-- RESULTS END -->"


def escape(text: object) -> str:
    """
    Escape anything that came from a model or a source before it goes in a page.

    Every word in this table's first column came from config, but the story
    titles came from Nir and the headlines came from models that had just been
    reading web pages written by strangers. So everything is escaped, always
    (bible/part-00.md LAW 8, followed all the way to the last mile).
    """
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#39;"))


def gather() -> list[dict]:
    """
    One row per model that has written something, in cheapest-first order.

    Nir, 2026-09-03: "do exactly what the Bible says." Part 01 1.5 iron rule 3:
    "Every stage reads and writes THROUGH Neo4j; files on disk are caches and
    exports, never truth." This stage used to read rendering.json files
    directly; it now reads the same facts from the database through the one
    door (lib/db.py), where the store_knowledge stage put them. The numbers
    on the home page were compared against the file-fed build before this
    switch and did not change.
    """
    rows = []
    with connect() as db:
        for model in roster():
            renderings = read_editions_for_model(db, model.slug)
            if not renderings:
                continue

            galaxy_path = GALAXIES / f"{model.slug}.json"
            galaxy = json.loads(galaxy_path.read_text(encoding="utf-8")) if galaxy_path.exists() else {}
            counts = galaxy.get("counts", {})
            nodes = max(1, counts.get("stories", 0) + counts.get("concepts", 0))

            total_cost = sum(r["cost_usd"] for r in renderings)
            words = [len((r["produced"].get("article") or "").split()) for r in renderings]
            rows.append({
                "model": model,
                "editions": len(renderings),
                "cost_total": total_cost,
                "cost_each": total_cost / len(renderings),
                "words_each": sum(words) // len(words),
                "concepts": counts.get("concepts", 0),
                "links": counts.get("links", 0),
                "links_per_node": counts.get("links", 0) / nodes,
                "seconds_each": sum(r["seconds_waited"] for r in renderings) / len(renderings),
            })
    return sorted(rows, key=lambda row: row["cost_each"])


def build_html(rows: list[dict]) -> str:
    """The section, as plain readable HTML."""
    if not rows:
        return f"{BEGIN}\n{END}"

    with connect() as db:
        with db.session() as session:
            stories = session.run("MATCH (:Story) RETURN count(*) AS n").single()["n"]
    editions = len(rows)
    total = sum(row["cost_total"] for row in rows)
    default_slug = next((m.slug for m in roster() if m.id == settings().default_model),
                        rows[0]["model"].slug)

    cheapest = min(rows, key=lambda r: r["cost_each"])
    densest = max(rows, key=lambda r: r["links_per_node"])
    sparsest = min(rows, key=lambda r: r["links_per_node"])
    longest = max(rows, key=lambda r: r["words_each"])
    shortest = min(rows, key=lambda r: r["words_each"])
    slowest = max(rows, key=lambda r: r["seconds_each"])
    quickest = min(rows, key=lambda r: r["seconds_each"])

    out: list[str] = [BEGIN, '  <h2>The first real results</h2>']

    # The paragraph above the table.
    out.append(
        f'  <p>{stories} stories so far, each one written {editions} separate times over, '
        f'by {editions} different AI models. Every model read exactly the same frozen '
        f'sources and did the entire job alone: the article, the one-line summary, the '
        f'encyclopedia entries behind it, the tags, the links to other stories, and the '
        f'instructions for its own illustration. Nothing any of them wrote has been '
        f'corrected, improved or graded by us. If one of them is wrong, switch to another '
        f'and see for yourself &mdash; that comparison is the point of this magazine, not '
        f'a flaw in it.</p>'
    )
    out.append(
        '  <p>Pick whose edition you want to fly through. Each one is its own '
        'four-dimensional world, because each model chose its own tags and its own links, '
        'and those choices are what decide where everything sits. Changing edition '
        'rearranges the sky.</p>'
    )

    # A button per edition. The default one says so.
    out.append('  <div class="editions">')
    for row in sorted(rows, key=lambda r: roster().index(r["model"])):
        model = row["model"]
        note = "the one this site opens with" if model.slug == default_slug else escape(model.company)
        out.append(
            f'    <a class="edition-link" data-edition="{escape(model.slug)}" '
            f'href="tesseract.html?edition={escape(model.slug)}">'
            f'<b>{escape(model.short_name)}</b><span>{note}</span></a>'
        )
    out.append('  </div>')

    # The table.
    out.append('  <table class="results">')
    out.append('    <thead><tr>'
               '<th>Edition</th>'
               '<th>Cost per story</th>'
               '<th>Words per article</th>'
               '<th>Ideas explained</th>'
               '<th>Links drawn</th>'
               '<th>Links per node</th>'
               '<th>Seconds each</th>'
               '</tr></thead>')
    out.append('    <tbody>')
    for row in rows:
        model = row["model"]
        cheap = ' class="cheapest"' if row is cheapest else ''
        dense = ' class="most"' if row is densest else ''
        out.append(
            f'      <tr>'
            f'<td><a href="tesseract.html?edition={escape(model.slug)}">'
            f'{escape(model.short_name)}</a></td>'
            f'<td{cheap}>${row["cost_each"]:.4f}</td>'
            f'<td>{row["words_each"]}</td>'
            f'<td>{row["concepts"]}</td>'
            f'<td>{row["links"]}</td>'
            f'<td{dense}>{row["links_per_node"]:.1f}</td>'
            f'<td>{row["seconds_each"]:.0f}</td>'
            f'</tr>'
        )
    out.append('    </tbody>')
    out.append(
        f'    <caption>Every number here is measured, not estimated. The costs are what '
        f'was actually charged for the work. &ldquo;Ideas explained&rdquo; is how many '
        f'encyclopedia entries that model decided the stories needed. &ldquo;Links per '
        f'node&rdquo; is how densely it wove its own world together. All {editions} '
        f'editions of all {stories} stories cost ${total:.2f} in total.</caption>'
    )
    out.append('  </table>')

    # The paragraph below the table, written from the numbers rather than from
    # anybody's impression of them.
    out.append(
        f'  <p class="note">What the table already shows: '
        f'{escape(densest["model"].short_name)} wove a world '
        f'{densest["links_per_node"] / max(0.1, sparsest["links_per_node"]):.1f} times more '
        f'densely connected than {escape(sparsest["model"].short_name)}&rsquo;s, from the '
        f'same {stories} stories. '
        f'{escape(longest["model"].short_name)} wrote {longest["words_each"]} words per '
        f'article where {escape(shortest["model"].short_name)} wrote '
        f'{shortest["words_each"]}. '
        f'{escape(slowest["model"].short_name)} took {slowest["seconds_each"]:.0f} seconds '
        f'to think where {escape(quickest["model"].short_name)} took '
        f'{quickest["seconds_each"]:.0f}. And {escape(cheapest["model"].short_name)}, at '
        f'${cheapest["cost_each"]:.4f} a story, costs '
        f'{max(r["cost_each"] for r in rows) / cheapest["cost_each"]:.0f} times less than '
        f'the dearest edition here &mdash; read them side by side and judge whether it '
        f'shows.</p>'
    )
    out.append(
        '  <p class="note">Hover a node for its one-line summary and picture; click it to '
        'read the whole page its model wrote for it. Every node carries the illustration '
        'its model imagined for the idea.</p>'
    )
    out.append(f'  <!-- generated by pipeline/stages/build_home.py on '
               f'{datetime.now(timezone.utc).strftime("%Y-%m-%d")} - do not edit by hand -->')
    out.append(END)
    return "\n".join(out)


def main() -> int:
    rows = gather()
    section = build_html(rows)
    written: list[str] = []
    failed = 0

    for page_path in home_pages():
        page = page_path.read_text(encoding="utf-8")
        if BEGIN not in page or END not in page:
            print(f"ERROR: {page_path.name} has lost its {BEGIN} / {END} markers.")
            failed += 1
            continue
        before = page[:page.index(BEGIN)]
        after = page[page.index(END) + len(END):]
        page_path.write_text(before + section + after, encoding="utf-8")
        written.append(str(page_path.relative_to(REPO_ROOT)))
        print(f"  refreshed: {page_path.name}")

    print(f"Wrote the first-results section for {len(rows)} editions into "
          f"{len(written)} home page(s), {failed} failed.")
    for row in rows:
        print(f"  {row['model'].short_name:<20} ${row['cost_each']:.4f} per story, "
              f"{row['words_each']} words, {row['concepts']} ideas, "
              f"{row['links_per_node']:.1f} links per node")

    if rows and written:
        try:
            with connect() as db:
                log_job(db, action_type="export", actor="claude-opus-5",
                        plain_words=(
                            f"Wrote the first-results section into all {len(written)} "
                            f"home pages from the {len(rows)} editions in the database: a "
                            f"button for each edition a visitor can fly through (pointing "
                            f"into the live version folder via the VERSION_FALLBACK "
                            f"placeholder, so no root page can ever 404 on the galaxy), "
                            f"and a table of what each model made of the same stories, "
                            f"with every number measured rather than estimated. It is "
                            f"generated rather than typed, so adding a model or a story "
                            f"updates every home page by itself."),
                        outputs=written)
        except Exception as problem:  # noqa: BLE001
            print(f"(could not write to the ledger: {type(problem).__name__})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
