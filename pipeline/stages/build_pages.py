#!/usr/bin/env python3
"""
THE READING PAGES: WHAT A CLICK ACTUALLY OPENS
==============================================

WHAT THIS IS, IN ONE SENTENCE
The stage that turns the database into the pages a reader lands on when they
click a node in the galaxy - one page per story per edition, and one page per
encyclopedia idea per edition - so the magazine finally has somewhere to READ.

WHY THESE EXACT PATHS
The site already promised these pages before this stage existed: the galaxy
loader (site/src/scenes/galaxy.js) gives every node a `pageOf` of
`stories/<story-slug>/<model-slug>.html` for a story and
`ideas/<concept-slug>/<model-slug>.html` for an encyclopedia idea, and clicking
a node opens exactly that file. Until this stage was written (2026-09-03),
every one of those clicks landed on nothing. This stage writes the files the
site has been asking for all along.

EVERYTHING COMES FROM THE DATABASE (bible/part-00.md LAW 5)
Nir, 2026-09-03: "do exactly what the Bible says." Every word on these pages
is read through pipeline/lib/db.py, the one door - the same truth the galaxy
builder reads. The files under content/stories/ are not consulted at all.
The PICTURES are artifacts, and are copied beside the pages they illustrate
(Part 12 12.2.4: image files are artifacts; the JOB that made them is truth,
and its label - model, seed - is printed on the page per LAW 7).

NO MODEL'S WORK IS EVER EDITED HERE (DECISIONS.md decision 16)
A model's headline, article, key points, tags, ideas and links are published
exactly as it wrote them. If it made a dumb link, the page shows the dumb
link - "this is also a test of intelligence that we want."

EVERY WORD IS ESCAPED (bible/part-07.md 7.3)
Everything a model wrote is HTML-escaped before it touches a page; the only
raw HTML on the page is the page's own skeleton, which this stage owns.

HOW TO RUN IT
    cd pipeline && uv run stages/build_pages.py
Safe to re-run: it rewrites the pages whole from the database (LAW 12).
"""

from __future__ import annotations

import html
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.db import (  # noqa: E402
    connect,
    log_job,
    read_editions_for_model,
    read_image_job,
)
from lib.llm import roster  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE = REPO_ROOT / "site"
GALAXIES = SITE / "data" / "galaxies"

# The page's own look: the root page's palette, kept in one place here so the
# reading pages feel like the same publication, not a different site.
STYLE = """
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body { margin: 0; background: #07090f; color: #dbe4f4;
         font: 17px/1.65 system-ui, -apple-system, Segoe UI, sans-serif; }
  a { color: #9fd0ff; }
  .sheet { max-width: 44rem; margin: 0 auto; padding: 2.2rem 1.4rem 4rem; }
  .crumbs { font-size: 0.86rem; color: #7f92b4; margin-bottom: 1.4rem; }
  .crumbs a { color: #9fd0ff; text-decoration: none; }
  .edition-note { border: 1px solid #1b2949; background: #0d1424;
                  border-radius: 9px; padding: 0.8rem 1rem; font-size: 0.9rem;
                  color: #a8bad8; margin-bottom: 1.8rem; }
  .edition-note strong { color: #fff; }
  h1 { font-size: 1.9rem; line-height: 1.25; margin: 0 0 0.5rem; }
  .tldr { font-size: 1.12rem; color: #ffd479; margin: 0 0 1.6rem; }
  figure { margin: 0 0 1.8rem; }
  figure img { width: 100%; height: auto; border-radius: 9px;
               border: 1px solid #1b2437; display: block; }
  figcaption { font-size: 0.82rem; color: #7f92b4; margin-top: 0.5rem; }
  .article p { margin: 0 0 1.1rem; }
  h2 { font-size: 1.2rem; border-bottom: 1px solid #1b2437;
       padding-bottom: 0.35rem; margin: 2rem 0 0.8rem; }
  ul.points { padding-left: 1.1rem; }
  ul.points li { margin-bottom: 0.5rem; }
  ul.points .src { color: #7f92b4; font-size: 0.85rem; }
  .tag { display: inline-block; border: 1px solid #38507d; border-radius: 6px;
         padding: 0.1rem 0.5rem; margin: 0 0.3rem 0.3rem 0; font-size: 0.85rem;
         color: #a8bad8; text-decoration: none; }
  .sources li { margin-bottom: 0.45rem; font-size: 0.95rem; }
  .sources .by { color: #7f92b4; }
  .next a { display: block; padding: 0.55rem 0.8rem; margin-bottom: 0.4rem;
            border: 1px solid #1b2437; border-radius: 8px; text-decoration: none; }
  .next a:hover { background: #16203a; }
  .next .where { color: #9fd0ff; }
  .others { font-size: 0.92rem; }
  .others a { margin-right: 0.7rem; }
"""


def esc(text: object) -> str:
    """Escape EVERYTHING a model wrote before it touches the page (LAW 8)."""
    return html.escape(str(text if text is not None else ""))


def head(title: str, description: str, image: str | None = None) -> str:
    """The page skeleton's top, with the preview tags every page carries."""
    og = (f'\n<meta property="og:image" content="{esc(image)}">' if image else "")
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{esc(title)}</title>\n"
        f'<meta name="description" content="{esc(description)}">\n'
        f'<meta property="og:title" content="{esc(title)}">\n'
        f'<meta property="og:description" content="{esc(description)}">{og}\n'
        f"<style>{STYLE}</style>\n"
        "</head>\n<body>\n<div class=\"sheet\">\n"
    )


FOOT = "\n</div>\n</body>\n</html>\n"


def crumbs(edition_link: str, edition_name: str) -> str:
    return (
        '<p class="crumbs"><a href="../../index.html">AI Panorama</a> &middot; '
        f'<a href="{esc(edition_link)}">fly through the {esc(edition_name)} edition</a></p>'
    )


def edition_note(short_name: str, company: str,
                 other_editions: list[tuple[str, str, str]]) -> str:
    """
    The banner that names whose edition this is, per LAW 7 kinship.
    other_editions: (short_name, story_slug, model_slug) for each OTHER
    model's edition of the SAME story - so a reader can jump straight to
    another model's version of what they are reading.
    """
    links = " ".join(
        f'<a href="../{esc(slug)}/{esc(page_model)}.html">{esc(name)}</a>'
        for name, slug, page_model in other_editions
    )
    others_html = (f'<br>The same story in other editions: <span class="others">{links}</span>'
                   if links else "")
    return (
        '<p class="edition-note">This page was written entirely by '
        f"<strong>{esc(short_name)}</strong> ({esc(company)}), as one of the "
        "magazine's editions - eight AI models each wrote their own version of "
        f"every story from the same frozen sources.{others_html}</p>"
    )


def story_page(db, model, edition: dict, other_editions: list[tuple]) -> str:
    """One edition's page for one story: the article, whole and unedited."""
    produced = edition["produced"]
    story_slug, model_slug = edition["story"], model.slug
    story_title = edition.get("story_title", story_slug)
    galaxy_link = f"../../tesseract.html?edition={esc(model_slug)}"

    image_job = read_image_job(db, story_slug, model_slug)
    picture = ""
    if image_job:
        picture = (
            f'<figure><img src="images/{esc(model_slug)}.png" '
            f'alt="Illustration for {esc(story_title)}">'
            "<figcaption>Illustrated locally by "
            f"{esc(image_job.get('image_model', 'an open image model'))}"
            f", seed {image_job.get('seed', '?')} - from this edition's own prompt. "
            "AI-generated image, labeled per the site's attribution rules.</figcaption></figure>"
        )

    points = "".join(
        f"<li>{esc(p['point'])}"
        + (f' <span class="src">&middot; <a href="{esc(p["source_url"])}" '
           'target="_blank" rel="noopener">source</a></span>' if p.get("source_url") else "")
        + "</li>"
        for p in produced.get("key_points") or []
    )
    points_html = f"<h2>The key points</h2><ul class=\"points\">{points}</ul>" if points else ""

    ideas = "".join(
        f'<a class="tag" href="../../ideas/{esc(c["slug"])}/{esc(model_slug)}.html">'
        f"{esc(c['term'])}</a>"
        for c in produced.get("concepts") or []
    )
    ideas_html = f"<h2>Ideas this story leans on</h2><p>{ideas}</p>" if ideas else ""

    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in produced.get("tags") or [])
    tags_html = f"<h2>Tags this edition chose</h2><p>{tags}</p>" if tags else ""

    related = "".join(
        f'<a href="../{esc(other)}/{esc(model_slug)}.html">'
        f'<span class="where">{esc(other)}</span></a>'
        for other in produced.get("related") or []
        if other != story_slug
    )
    related_html = f"<h2>Read next, says this edition</h2><div class=\"next\">{related}</div>" if related else ""

    sources = "".join(
        f"<li><a href=\"{esc(s['url'])}\" target=\"_blank\" rel=\"noopener\">{esc(s['title'])}</a>"
        + (f" <span class=\"by\">&middot; {esc(s['byline'])}, {esc(s['site'])}, {esc(s['published'])}</span>"
           if s.get("byline") else "")
        + "</li>"
        for s in edition.get("story_sources") or []
    )
    sources_html = f"<h2>The frozen sources</h2><ul class=\"sources\">{sources}</ul>" if sources else ""

    # The article body arrives as plain paragraphs from the model; escaped and
    # wrapped, never edited (decision 16).
    paragraphs = "".join(f"<p>{esc(p)}</p>"
                         for p in str(produced.get("article") or "").split("\n") if p.strip())

    return (
        head(f"{produced.get('headline', story_title)} - {model.short_name}'s edition",
             produced.get("tldr") or story_title,
             f"stories/{story_slug}/images/{model_slug}.png")
        + crumbs(galaxy_link, model.short_name)
        + edition_note(model.short_name, model.company, other_editions)
        + f"<h1>{esc(produced.get('headline', story_title))}</h1>\n"
        + f'<p class="tldr">{esc(produced.get("tldr", ""))}</p>\n'
        + picture
        + f'<div class="article">{paragraphs}</div>\n'
        + points_html + ideas_html + tags_html + related_html + sources_html
        + FOOT
    )


def idea_page(model, slug: str, term: str, takes: list[tuple[str, str]]) -> str:
    """
    One edition's page for one encyclopedia idea: every explanation this
    model wrote of it, across the stories that leaned on it, each linking
    back to the story it came from.
    """
    galaxy_link = f"../../tesseract.html?edition={esc(model.slug)}"
    sections = ""
    for story_slug, explanation in takes:
        sections += (
            f"<h2>As explained in "
            f'<a href="../{esc(story_slug)}/{esc(model.slug)}.html">{esc(story_slug)}</a></h2>\n'
            f"<p>{esc(explanation)}</p>\n"
        )
    return (
        head(f"{term} - {model.short_name}'s edition", f"What {model.short_name} wrote about {term}.")
        + crumbs(galaxy_link, model.short_name)
        + edition_note(model.short_name, model.company, [])
        + f"<h1>{esc(term)}</h1>\n"
        + '<p class="tldr">An encyclopedia idea, explained by this edition wherever '
        "the stories leaned on it.</p>\n"
        + sections
        + FOOT
    )


def main() -> int:
    started = time.monotonic()
    stories_written = 0
    ideas_written = 0

    with connect() as db:
        # Every model's editions once, up front - the cross-edition links need
        # to know what every OTHER model wrote about the same story, and
        # re-querying inside the loop would be both wasteful and messy.
        all_editions: dict[str, list[dict]] = {
            m.slug: read_editions_for_model(db, m.slug) for m in roster()
        }

        for model in roster():
            editions = all_editions[model.slug]
            if not editions:
                continue

            # Per model: every story's list of OTHER models' editions of that
            # same story, for the honest cross-links.
            others_by_story: dict[str, list[tuple]] = {}
            for other_model in roster():
                if other_model.slug == model.slug:
                    continue
                for other in all_editions[other_model.slug]:
                    others_by_story.setdefault(other["story"], []).append(
                        (other_model.short_name, other["story"], other_model.slug))

            # The idea pages want, per slug, every story that wrote it.
            ideas_by_slug: dict[str, list[tuple[str, str]]] = {}
            idea_terms: dict[str, str] = {}

            for edition in editions:
                story_slug = edition["story"]
                page = story_page(db, model, edition, others_by_story.get(story_slug, []))
                folder = SITE / "stories" / story_slug
                folder.mkdir(parents=True, exist_ok=True)
                (folder / f"{model.slug}.html").write_text(page, encoding="utf-8")
                stories_written += 1

                # Ship the full picture beside the page (artifacts, exported).
                image_job = read_image_job(db, story_slug, model.slug)
                if image_job:
                    source = (REPO_ROOT / "content" / "stories" / story_slug
                              / "editions" / model.slug / "images" / "article.png")
                    if source.exists():
                        images_dir = folder / "images"
                        images_dir.mkdir(exist_ok=True)
                        shutil.copy2(source, images_dir / f"{model.slug}.png")

                for concept in edition["produced"].get("concepts") or []:
                    slug = str(concept.get("slug") or "").strip().lower()
                    if not slug:
                        continue
                    ideas_by_slug.setdefault(slug, []).append(
                        (story_slug, concept.get("explanation", "")))
                    idea_terms[slug] = concept.get("term", slug)

            for slug, takes in ideas_by_slug.items():
                folder = SITE / "ideas" / slug
                folder.mkdir(parents=True, exist_ok=True)
                page = idea_page(model, slug, idea_terms[slug], takes)
                (folder / f"{model.slug}.html").write_text(page, encoding="utf-8")
                ideas_written += 1

        # SELF-CHECK (the Part 12 spirit: a build that ships broken links is
        # not a build): every page the galaxies promise must now exist.
        missing = []
        for path in sorted(GALAXIES.glob("*.json")):
            if path.name == "index.json":
                continue
            model_slug = path.name.removesuffix(".json")
            galaxy = json.loads(path.read_text(encoding="utf-8"))
            for node in galaxy.get("nodes") or []:
                page = (f"stories/{node['slug']}/{model_slug}.html" if node["kind"] == "story"
                        else f"ideas/{node['slug']}/{model_slug}.html")
                if not (SITE / page).exists():
                    missing.append(page)

        seconds = time.monotonic() - started
        verdict = "ok" if not missing else "partial"
        print(f"Reading pages built from the database: {stories_written} story pages, "
              f"{ideas_written} idea pages, in {seconds:.1f} seconds.")
        if missing:
            print(f"MISSING {len(missing)} pages the galaxies promise, for example: "
                  f"{missing[:3]}")

        log_job(
            db,
            action_type="stage_run",
            actor="glm-5.3",
            verdict=verdict,
            cost_usd=0.0,
            duration_s=seconds,
            plain_words=(
                f"Built the magazine's reading pages from the database: {stories_written} "
                f"story pages and {ideas_written} encyclopedia pages, one per edition, so "
                f"clicking a node in the galaxy finally opens something to read. "
                + ("Every page the galaxies promise exists." if not missing
                   else f"{len(missing)} promised pages are still missing.")
            ),
        )
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
