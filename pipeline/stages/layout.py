#!/usr/bin/env python3
"""
BUILDING EACH EDITION'S OWN GALAXY
==================================

WHAT THIS IS, IN ONE SENTENCE
The stage that turns one model's tags and links into one four-dimensional world
of its own, so that switching edition on the website rearranges the sky.

EIGHT EDITIONS MEANS EIGHT GALAXIES (DECISIONS.md decision 20)
Nothing is shared between editions except the frozen sources. Each model chose
its own tags, wrote its own encyclopedia entries and decided for itself which
stories a reader should go to next, and those choices are exactly what decides
where things sit and what they sit beside. Nir: "if one editor in Wikipedia is
dumb, and make dumb links, then this is also a test of intelligence that we
want." So a model that links unrelated things gets a visibly stranger galaxy,
and that is a result, not a fault to be fixed.

THE TWO KINDS OF NODE, AND WHAT THE FOURTH DIMENSION MEANS
1. STORY nodes: something that happened, tied to a date. Raw news.
2. CONCEPT nodes: the encyclopedia. "What a bacteriophage is." No date. Written
   to stay true a year from now.
The fourth coordinate, w, is the distance between those two things
(bible/part-03.md 3.5, W-DEFINITION 1): raw news at one end, settled knowledge
at the other. Slide the slab outward and you are reading this week; slide it
inward and you are reading the encyclopedia. A story drifts inward as it ages,
so a reader coming back in a month sees this week's weather hanging outside the
geography.

WHERE x, y AND z COME FROM (bible/part-03.md 3.2)
A force layout: nodes pull together when they share tags or a link, and push
apart otherwise, until the whole thing settles. The simulation owns only x, y
and z and NEVER touches w, because a simulated fourth coordinate is meaningless
residue while a chosen one is readable.

THE NO-JUMPING RULE, WITHIN AN EDITION (bible/part-03.md 3.2 alignment)
When a galaxy is rebuilt after new stories arrive, the new layout is rotated to
sit as close as possible to the old one, so a reader's map does not silently
become a different map. This applies WITHIN one edition over time. It is
deliberately NOT applied between editions: they are supposed to differ.

HOW TO RUN IT
    cd pipeline && uv run stages/layout.py                 (every edition)
    cd pipeline && uv run stages/layout.py --model <id>    (just one)
Safe to re-run: it recomputes from what is on disk and writes the result whole.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import networkx as nx
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.db import connect, log_job, read_editions_for_model  # noqa: E402
from lib.llm import Model, model_by_id, roster  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
STORIES = REPO_ROOT / "content" / "stories"
GALAXIES = REPO_ROOT / "content" / "galaxies"

# The layout is deterministic: the same tags and links always produce the same
# galaxy, on any machine, forever. That is what makes a rebuild trustworthy.
RANDOM_SEED = 20260821

# Where the two kinds of node live along the fourth axis. These are the anchors
# from bible/part-03.md 3.5, narrowed to the two kinds this magazine actually
# has. A story starts at the raw-news end and creeps inward as it ages; an
# encyclopedia entry sits at the settled end and does not move.
W_FRESH_NEWS = -1.0
W_SETTLED_NEWS = 0.0
W_ENCYCLOPEDIA = 0.7

# How long a story takes to drift from "raw news" to "part of the record", in
# days. Ninety days is a season: long enough that a story is still news when a
# reader comes back next month, short enough that a year-old story has clearly
# settled.
DAYS_TO_SETTLE = 90.0


def w_for_story(published: str, today: date | None = None) -> float:
    """
    How far along the news-to-knowledge axis a story sits, from its age.

    Smooth, not stepped, so a returning reader sees things MOVE rather than
    jump between shelves.
    """
    today = today or datetime.now(timezone.utc).date()
    try:
        when = date.fromisoformat(published[:10])
    except (ValueError, TypeError):
        return W_FRESH_NEWS
    days = max(0.0, (today - when).days)
    # A curve that moves quickly at first and then slows, so the difference
    # between "today" and "last week" is visible, and the difference between
    # "one year" and "two years" is not pretended to be large.
    settled = 1.0 - math.exp(-days / (DAYS_TO_SETTLE / 2.0))
    return W_FRESH_NEWS + (W_SETTLED_NEWS - W_FRESH_NEWS) * settled


def read_editions(model: Model) -> list[dict]:
    """
    Every rendering this model produced, in story order - READ FROM THE
    DATABASE, not from files. Nir, 2026-09-03: "do exactly what the Bible
    says." Part 01 1.5 iron rule 3: "Every stage reads and writes THROUGH
    Neo4j; files on disk are caches and exports, never truth." Until today
    this function read rendering.json files directly, which violated LAW 5
    - the same shapes flow through db.py's reader now (the reader was built
    to return this function's exact old output, so the switch was verified
    by rebuilding every galaxy and comparing it to the file-fed build).
    """
    with connect() as db:
        return read_editions_for_model(db, model.slug)


def build_graph(editions: list[dict]) -> tuple[nx.Graph, dict[str, dict]]:
    """
    Turn one model's choices into a graph.

    Nodes: one per story, plus one per encyclopedia entry it wrote. Where two
    stories produced an entry with the same slug, they become ONE node with two
    explanations, because that is the model saying the same idea matters twice.

    Edges, and what each one means:
      story  -> concept   this article leans on that idea (the strongest bond)
      story  -> story     this editor said read that one next
      story  -> story     they share tags (weaker, one edge per shared tag)
      concept-> concept   two ideas explained by the same article
    """
    graph = nx.Graph()
    nodes: dict[str, dict] = {}

    for edition in editions:
        produced = edition["produced"]
        story_id = f"story:{edition['story']}"
        nodes[story_id] = {
            "id": story_id,
            "kind": "story",
            "slug": edition["story"],
            "headline": produced.get("headline", ""),
            "tldr": produced.get("tldr", ""),
            "tags": [str(t).lower() for t in produced.get("tags") or []],
            "published": edition["story_published"],
            "w": w_for_story(edition["story_published"]),
            "story_title": edition["story_title"],
        }
        graph.add_node(story_id)

        for concept in produced.get("concepts") or []:
            slug = str(concept.get("slug") or "").strip().lower()
            if not slug:
                continue
            concept_id = f"concept:{slug}"
            if concept_id not in nodes:
                nodes[concept_id] = {
                    "id": concept_id, "kind": "concept", "slug": slug,
                    "headline": concept.get("term", slug),
                    "tldr": _first_sentence(concept.get("explanation", "")),
                    "tags": [], "published": "", "w": W_ENCYCLOPEDIA,
                    "explained_in": [],
                    "explanations": [],
                }
                graph.add_node(concept_id)
            nodes[concept_id]["explanations"].append({
                "from_story": edition["story"],
                "text": concept.get("explanation", ""),
            })
            nodes[concept_id]["explained_in"].append(edition["story"])
            graph.add_edge(story_id, concept_id, weight=3.0, why="leans on")

    # The editor's own "read this next" links, which are its strongest opinion
    # about how knowledge fits together.
    for edition in editions:
        story_id = f"story:{edition['story']}"
        for other in edition["produced"].get("related") or []:
            other_id = f"story:{str(other).strip()}"
            if other_id in nodes and other_id != story_id:
                graph.add_edge(story_id, other_id, weight=4.0, why="read next")

    # Shared tags: a weaker pull, but it is what stops a small magazine from
    # being a scatter of unconnected dots.
    stories = [n for n in nodes.values() if n["kind"] == "story"]
    for index, first in enumerate(stories):
        for second in stories[index + 1:]:
            shared = set(first["tags"]) & set(second["tags"])
            if shared:
                a, b = first["id"], second["id"]
                weight = 1.0 * len(shared)
                if graph.has_edge(a, b):
                    graph[a][b]["weight"] += weight
                    graph[a][b]["why"] += f", shares {'/'.join(sorted(shared))}"
                else:
                    graph.add_edge(a, b, weight=weight, why=f"shares {'/'.join(sorted(shared))}")

    # Two ideas explained by the same article belong near each other.
    for edition in editions:
        concept_ids = [f"concept:{str(c.get('slug','')).strip().lower()}"
                       for c in edition["produced"].get("concepts") or []]
        concept_ids = [c for c in concept_ids if c in nodes]
        for index, first in enumerate(concept_ids):
            for second in concept_ids[index + 1:]:
                if not graph.has_edge(first, second):
                    graph.add_edge(first, second, weight=1.5, why="explained together")

    return graph, nodes


def _first_sentence(text: str, limit: int = 140) -> str:
    """The opening sentence of an explanation, for the hover card."""
    cleaned = " ".join(str(text).split())
    cut = cleaned[:limit]
    stop = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
    return (cut[:stop + 1] if stop > 40 else cut).strip()


def place(graph: nx.Graph, nodes: dict[str, dict]) -> dict[str, tuple[float, float, float]]:
    """
    Settle the graph in three dimensions, then fit it into the unit box.

    Uses a spring layout: linked nodes pull together, everything pushes apart.
    Deterministic under RANDOM_SEED, so the same choices always make the same
    galaxy (bible/part-03.md 3.2, the layout contract).
    """
    if graph.number_of_nodes() == 0:
        return {}
    if graph.number_of_nodes() == 1:
        return {next(iter(graph.nodes)): (0.0, 0.0, 0.0)}

    raw = nx.spring_layout(
        graph, dim=3, weight="weight", seed=RANDOM_SEED,
        iterations=400, k=1.4 / math.sqrt(graph.number_of_nodes()),
    )
    points = np.array([raw[node] for node in graph.nodes], dtype=float)

    # Centre it, then scale the widest axis to fill the box. Scaling all three
    # axes by the SAME factor matters: scaling them separately would stretch the
    # shape and quietly lie about how far apart things are.
    points -= points.mean(axis=0)
    widest = float(np.abs(points).max()) or 1.0
    points *= 0.92 / widest

    return {node: tuple(float(v) for v in points[index])
            for index, node in enumerate(graph.nodes)}


def align_to_previous(model: Model, placed: dict[str, tuple[float, float, float]]
                      ) -> dict[str, tuple[float, float, float]]:
    """
    Rotate a freshly-built galaxy to sit as close as possible to its own
    previous version, so a reader's map does not secretly become a new map
    (bible/part-03.md 3.2, the no-jumping rule).

    This is the classic orthogonal Procrustes fit: find the rotation that
    minimises the total squared distance between the shared nodes' old and new
    positions, and refuse any solution that MIRRORS the world, because a
    mirrored map wrecks spatial memory without looking wrong.
    """
    previous_path = GALAXIES / f"{model.slug}.json"
    if not previous_path.exists():
        return placed
    try:
        previous = json.loads(previous_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return placed

    old = {n["id"]: (n["x"], n["y"], n["z"]) for n in previous.get("nodes", [])}
    shared = [node for node in placed if node in old]
    if len(shared) < 4:
        return placed

    before = np.array([old[node] for node in shared], dtype=float)
    after = np.array([placed[node] for node in shared], dtype=float)
    before -= before.mean(axis=0)
    after -= after.mean(axis=0)

    u, _, vt = np.linalg.svd(after.T @ before)
    rotation = u @ vt
    if np.linalg.det(rotation) < 0:  # a mirror flip: forbid it
        u[:, -1] *= -1
        rotation = u @ vt

    everything = np.array([placed[node] for node in placed], dtype=float)
    centre = everything.mean(axis=0)
    turned = (everything - centre) @ rotation.T + centre
    return {node: tuple(float(v) for v in turned[index]) for index, node in enumerate(placed)}


def build_galaxy(model: Model) -> dict | None:
    """One model's whole world, ready for the browser."""
    editions = read_editions(model)
    if not editions:
        return None

    graph, nodes = build_graph(editions)
    settle_concepts(nodes)
    placed = align_to_previous(model, place(graph, nodes))

    for node_id, (x, y, z) in placed.items():
        nodes[node_id].update(x=x, y=y, z=z)

    edges = [
        {"from": a, "to": b, "weight": round(float(data.get("weight", 1.0)), 3),
         "why": data.get("why", "")}
        for a, b, data in graph.edges(data=True)
    ]

    stories = [n for n in nodes.values() if n["kind"] == "story"]
    concepts = [n for n in nodes.values() if n["kind"] == "concept"]
    return {
        "model_id": model.id,
        "model_slug": model.slug,
        "short_name": model.short_name,
        "company": model.company,
        "built_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "layout_seed": RANDOM_SEED,
        "w_meaning": "raw news at -1, part of the record at 0, the encyclopedia at +0.7",
        "counts": {"stories": len(stories), "concepts": len(concepts), "links": len(edges)},
        "nodes": sorted(nodes.values(), key=lambda n: (n["kind"], n["slug"])),
        "edges": edges,
    }


def settle_concepts(nodes: dict[str, dict]) -> None:
    """
    Spread the encyclopedia along the last stretch of the fourth dimension.

    Every idea starts at the encyclopedia anchor, but they must not all sit at
    exactly the same depth: fifteen nodes in one infinitely thin shell is a
    wall, not a world, and a reader sliding the slab would hit all of them at
    once and nothing in between.

    So an idea explained by MORE stories sits deeper, towards the bedrock end.
    That is not decoration: an idea this editor keeps needing to explain has
    earned its place further from the weather. An idea mentioned once stays
    just inside the encyclopedia's edge.
    """
    concepts = [n for n in nodes.values() if n["kind"] == "concept"]
    if not concepts:
        return
    most = max(len(n.get("explained_in") or []) for n in concepts)
    for concept in concepts:
        times = len(concept.get("explained_in") or [])
        # From the encyclopedia anchor towards, but never reaching, +1.0, which
        # bible/part-03.md 3.5 reserves for the most time-tested ideas of the
        # whole field - and a magazine three days old has none of those yet.
        share = 0.0 if most <= 1 else (times - 1) / (most - 1)
        concept["w"] = round(W_ENCYCLOPEDIA + share * 0.22, 4)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build each edition's own galaxy.")
    parser.add_argument("--model", help="one model id; the default is every model")
    parser.add_argument("--actor", default="claude-opus-5")
    args = parser.parse_args(argv)

    models = [model_by_id(args.model)] if args.model else roster()
    GALAXIES.mkdir(parents=True, exist_ok=True)

    built: list[str] = []
    print(f"{'MODEL':<20}{'STORIES':>8}{'IDEAS':>7}{'LINKS':>7}   the shape of its world")
    for model in models:
        galaxy = build_galaxy(model)
        if galaxy is None:
            print(f"{model.short_name:<20}{'-':>8}{'-':>7}{'-':>7}   nothing written yet")
            continue
        (GALAXIES / f"{model.slug}.json").write_text(
            json.dumps(galaxy, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        counts = galaxy["counts"]
        density = counts["links"] / max(1, counts["stories"] + counts["concepts"])
        print(f"{model.short_name:<20}{counts['stories']:>8}{counts['concepts']:>7}"
              f"{counts['links']:>7}   {density:.1f} links per node")
        built.append(model.slug)

    write_index()
    copy_to_site()

    if built:
        try:
            with connect() as db:
                log_job(db, action_type="layout", actor=args.actor,
                        plain_words=(
                            f"Built a separate four-dimensional world for each of {len(built)} "
                            f"editions, from nothing but that model's own tags, its own "
                            f"encyclopedia entries and its own opinion about which story a "
                            f"reader should go to next. Nothing is shared between them except "
                            f"the frozen sources, so switching edition on the website "
                            f"rearranges the sky. The fourth dimension is the distance from "
                            f"raw news to settled knowledge, and a story creeps inward as it "
                            f"ages."),
                        outputs=built)
        except Exception as problem:  # noqa: BLE001
            print(f"(could not write to the ledger: {type(problem).__name__})")
    return 0


def write_index() -> Path:
    """
    The list of editions that exist, so the switcher on the website builds
    itself. Adding a model tomorrow makes it appear with no page edited
    (DECISIONS.md decision 18).
    """
    from lib.llm import settings as grid_settings

    default = grid_settings().default_model
    editions = []
    for model in roster():
        path = GALAXIES / f"{model.slug}.json"
        if not path.exists():
            continue
        galaxy = json.loads(path.read_text(encoding="utf-8"))
        editions.append({
            "model_id": model.id,
            "model_slug": model.slug,
            "short_name": model.short_name,
            "company": model.company,
            "counts": galaxy["counts"],
            "is_default": model.id == default,
            "built_at_utc": galaxy["built_at_utc"],
        })
    index = {
        "built_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "default_model_slug": next((e["model_slug"] for e in editions if e["is_default"]),
                                   editions[0]["model_slug"] if editions else ""),
        "editions": editions,
    }
    path = GALAXIES / "index.json"
    path.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    return path


def copy_to_site() -> int:
    """
    Copy the galaxies to where the website can fetch them.

    content/galaxies is the TRUTH; site/data/galaxies is a build artifact that
    the browser reads (bible/part-01.md 1.9: files on disk are caches and
    exports, never truth). Copied whole rather than edited, so the two can
    never drift apart in some partial way.
    """
    import shutil

    destination = REPO_ROOT / "site" / "data" / "galaxies"
    destination.mkdir(parents=True, exist_ok=True)
    copied = 0
    for path in GALAXIES.glob("*.json"):
        shutil.copy2(path, destination / path.name)
        copied += 1
    return copied


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
