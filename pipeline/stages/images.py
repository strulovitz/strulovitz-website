#!/usr/bin/env python3
"""
RENDERING ONE EDITION'S ILLUSTRATION
=====================================

WHAT THIS IS, IN ONE SENTENCE
The stage that turns the illustration paragraph a model already wrote for its
own edition into an actual picture, using local ComfyUI (FLUX.2-dev) on this
machine's RTX 4070 Ti - free, unlimited, and nothing sent to any AI company.

WHY THIS MATTERS TO NIR, IN HIS OWN WORDS
"this is very important to me the images." All 40 illustration prompts were
written by the eight models in WHERE-WE-STAND-2026-08-22.md #1. None were
rendered until this file existed. Do not treat this as a minor finishing touch.

THE SAME MODEL, THE SAME SEED WITHIN A STORY, A DIFFERENT SEED PER STORY
Nir's decision: one image model, and a fixed seed shared by all eight editions
of the SAME story, so that comparing two editions' pictures on one story is
comparing two paragraphs, never two different dice rolls. But that seed is
NOT the same across every story - each story gets its own seed, derived from
its slug (see seed_for_story() below). Nir, correctly: "if the GLM work is
better in seed 42 and in seed 99, then he is better" - a model that only wins
under one lucky seed is suspicious; a model that keeps winning under several
different seeds across several stories is real evidence, so freezing the same
single number forever would have thrown that evidence away.

WHERE EACH PICTURE GOES (WHERE-WE-STAND-2026-08-22.md #1, decision 22)
    content/stories/<story>/editions/<company--model>/images/
        article.png     the full-size illustration, shown at the top of the
                         article page
        thumbnail.png    a small derived copy, shown inside that story's hover
                         card next to the one-line TLDR. Never downloaded on
                         its own - always derived from article.png so a hover
                         card never has to fetch a full-size file.
        meta.json        which model made the picture, the seed, the prompt,
                         when, and how long it took - the same honesty every
                         other stage keeps.

NOTHING IS EVER CHECKED OR IMPROVED (decision 16, same rule as the words)
If FLUX.2-dev draws something odd from a model's own paragraph, that oddity is
published exactly as drawn. This file never retries because a picture "looks
wrong" - only because ComfyUI itself failed to produce one at all.

HOW TO RUN IT
    ComfyUI must already be running on 127.0.0.1:8188 (see
    AI-PANORAMA-WORKFLOW-2026-09-02.md for how to start it if it is not).

    cd pipeline && uv run stages/images.py --story <slug> --model <id>
    cd pipeline && uv run stages/images.py --story <slug> --all-models
    cd pipeline && uv run stages/images.py --all --all-models
Nothing already rendered is redone unless --again is given.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import httpx
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.db import connect, log_job  # noqa: E402
from lib.llm import Model, model_by_id, roster  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
STORIES = REPO_ROOT / "content" / "stories"

COMFY_HOST = "127.0.0.1"
COMFY_PORT = 8188
COMFY_URL = f"http://{COMFY_HOST}:{COMFY_PORT}"

# ONE SEED PER STORY, SHARED BY ALL 8 MODELS' EDITIONS OF THAT STORY.
#
# Within a single story, every model's picture must use the identical seed -
# that is the part that has to be fixed, so that comparing Grok's picture
# against GPT's picture on the SAME story is comparing two paragraphs, never
# two different dice rolls.
#
# Nir, correctly, on why the seed must NOT also be frozen across every story
# forever: "if the GLM work is better in seed 42 and in seed 99, then he is
# better." A model that only wins under one specific lucky seed is suspicious.
# A model that keeps winning under several different seeds, across several
# stories, is real evidence. So each story gets its OWN seed - different from
# every other story's - and that seed is derived from the story's own slug so
# it is still exactly reproducible if this stage is ever run again.
def seed_for_story(slug: str) -> int:
    import hashlib
    return int(hashlib.sha256(slug.encode("utf-8")).hexdigest()[:8], 16)

IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024
STEPS = 28
GUIDANCE = 4.0

THUMBNAIL_MAX_SIDE = 400

# The exact models installed and verified working on this machine, per
# AI-PANORAMA-WORKFLOW-2026-09-02.md. If these files move, only this dict
# needs to change.
UNET_NAME = "flux2-dev-Q4_K_M.gguf"
CLIP_NAME = "Mistral-Small-3.2-24B-Instruct-2506-Q4_K_M.gguf"
VAE_NAME = "flux2-vae.safetensors"


# ------------------------------------------------------------------------------
# Talking to ComfyUI
# ------------------------------------------------------------------------------

def build_workflow(prompt_text: str, filename_prefix: str, seed: int) -> dict:
    """
    The exact ComfyUI API-format graph proven working on 2026-09-02:
    UnetLoaderGGUF -> CLIPLoaderGGUF -> CLIPTextEncode -> FluxGuidance (positive)
    + ConditioningZeroOut (negative, no second encode pass) -> KSampler (cfg=1)
    -> VAEDecode -> SaveImage.

    FluxGuidance + ConditioningZeroOut instead of a real second CLIPTextEncode
    for an empty negative prompt is not a style choice - encoding twice with
    the 24B Mistral text encoder overflows this GPU's 12GB VRAM. See the
    workflow doc for the full story of that bug.
    """
    return {
        "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": UNET_NAME}},
        "2": {"class_type": "CLIPLoaderGGUF",
              "inputs": {"clip_name": CLIP_NAME, "type": "flux2"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VAE_NAME}},
        "4": {"class_type": "CLIPTextEncode",
              "inputs": {"text": prompt_text, "clip": ["2", 0]}},
        "10": {"class_type": "FluxGuidance",
               "inputs": {"conditioning": ["4", 0], "guidance": GUIDANCE}},
        "11": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["4", 0]}},
        "6": {"class_type": "EmptyLatentImage",
              "inputs": {"width": IMAGE_WIDTH, "height": IMAGE_HEIGHT, "batch_size": 1}},
        "7": {"class_type": "KSampler",
              "inputs": {
                  "model": ["1", 0], "positive": ["10", 0], "negative": ["11", 0],
                  "latent_image": ["6", 0], "seed": seed, "steps": STEPS,
                  "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple",
                  "denoise": 1.0,
              }},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["3", 0]}},
        "9": {"class_type": "SaveImage",
              "inputs": {"images": ["8", 0], "filename_prefix": filename_prefix}},
    }


class ComfyNotRunning(RuntimeError):
    pass


class ComfyFailed(RuntimeError):
    pass


def comfy_alive(client: httpx.Client) -> bool:
    try:
        return client.get(f"{COMFY_URL}/", timeout=5).status_code == 200
    except httpx.HTTPError:
        return False


def vram_free_bytes(client: httpx.Client) -> int:
    """Ask ComfyUI itself how much VRAM is actually free right now."""
    stats = client.get(f"{COMFY_URL}/system_stats", timeout=10).json()
    return stats["devices"][0]["vram_free"]


def force_clean_vram(client: httpx.Client, *, min_free_gb: float = 10.5,
                      timeout_s: float = 60.0) -> float:
    """
    Unload every model and WAIT UNTIL VRAM IS ACTUALLY VERIFIED FREE, before
    every single image - not just after a failure.

    CORRECTED 2026-09-02, RUN 2, after Nir's explicit instruction: the first
    version of this file only cleared memory reactively, after a job had
    already crashed with an out-of-memory error, on the reasoning that
    reloading before every job would cost extra time. Nir's response, in his
    own words, was that this reasoning was worthless: "of course it needs to
    be done properly... clean each time." He is right - this is a free,
    unlimited, background job with no deadline, so trading some speed for
    never crashing at all is the correct trade, not a debatable one.

    This function does not trust a fixed sleep - it polls ComfyUI's own
    `/system_stats` endpoint (real numbers straight from the GPU driver, not
    a guess) until VRAM is genuinely back above `min_free_gb`, or gives up
    after `timeout_s` and proceeds anyway (a job that still OOMs after this
    will simply be reported as a real failure, never silently retried).
    """
    client.post(f"{COMFY_URL}/free",
                json={"unload_models": True, "free_memory": True}, timeout=10)
    started = time.monotonic()
    while time.monotonic() - started < timeout_s:
        free_gb = vram_free_bytes(client) / (1024 ** 3)
        if free_gb >= min_free_gb:
            return free_gb
        time.sleep(1.0)
    return vram_free_bytes(client) / (1024 ** 3)


def generate(client: httpx.Client, prompt_text: str, filename_prefix: str, seed: int,
             *, poll_every: float = 2.0, timeout_s: float = 900.0) -> tuple[bytes, float]:
    """
    Submit one image job to ComfyUI and wait for it, returning the PNG bytes
    and how many seconds it took. Raises ComfyFailed if ComfyUI reports an
    error or the job never appears in history within timeout_s.

    Caller (render_one, below) always calls force_clean_vram() first, so this
    function itself never retries - a failure here is real and reported as
    real, not silently patched over (decision 16 still applies to pictures;
    this function never sees or judges a successful picture at all, only
    whether ComfyUI itself finished the job).
    """
    workflow = build_workflow(prompt_text, filename_prefix, seed)
    started = time.monotonic()
    response = client.post(f"{COMFY_URL}/prompt", json={"prompt": workflow}, timeout=30)
    response.raise_for_status()
    prompt_id = response.json()["prompt_id"]

    while True:
        elapsed = time.monotonic() - started
        if elapsed > timeout_s:
            raise ComfyFailed(f"ComfyUI did not finish prompt {prompt_id} within {timeout_s:.0f}s.")
        try:
            history = client.get(f"{COMFY_URL}/history/{prompt_id}", timeout=30).json()
        except httpx.TimeoutException:
            # DISCOVERED 2026-09-02, RUN 3: under --lowvram, ComfyUI streams
            # weights from RAM more aggressively, and every so often a single
            # /history poll takes longer than expected to answer even though
            # the job itself is fine and keeps running server-side (same
            # underlying lesson as Trap 1 - the server doesn't care whether
            # the client is still listening). A single slow poll must never
            # be treated as a failure; just poll again.
            time.sleep(poll_every)
            continue
        entry = history.get(prompt_id)
        if entry:
            status = entry.get("status", {})
            if status.get("status_str") == "error" or any(
                m[0] == "execution_error" for m in status.get("messages", [])
            ):
                raise ComfyFailed(f"ComfyUI reported an error for {prompt_id}: {status}")
            outputs = entry.get("outputs", {})
            images = outputs.get("9", {}).get("images", [])
            if images:
                image_info = images[0]
                image_response = client.get(
                    f"{COMFY_URL}/view",
                    params={"filename": image_info["filename"],
                            "subfolder": image_info.get("subfolder", ""),
                            "type": image_info.get("type", "output")},
                    timeout=30,
                )
                image_response.raise_for_status()
                return image_response.content, time.monotonic() - started
        time.sleep(poll_every)


# ------------------------------------------------------------------------------
# Editions: prompts and story lists come from THE DATABASE, not files
# (Nir, 2026-09-03: "do exactly what the Bible says." Part 01 1.5 iron rule 3:
# every stage reads through Neo4j. The store_knowledge stage put every
# edition's image prompt and every story into the database; the .txt files
# under content/stories are human-readable exports, no longer the source.)
# ------------------------------------------------------------------------------

def all_story_slugs() -> list[str]:
    with connect() as db:
        with db.session() as session:
            rows = session.run("MATCH (s:Story) RETURN s.slug AS slug ORDER BY s.slug").data()
    return [r["slug"] for r in rows]


def edition_folder(slug: str, model: Model) -> Path:
    return STORIES / slug / "editions" / model.slug


def image_prompt_for(slug: str, model: Model) -> str | None:
    with connect() as db:
        with db.session() as session:
            record = session.run(
                "MATCH (e:Edition {story_slug: $slug, model_slug: $model}) "
                "RETURN e.image_prompt AS prompt",
                slug=slug, model=model.slug,
            ).single()
    if not record:
        return None
    text = (record["prompt"] or "").strip()
    return text or None


@dataclass
class Job:
    slug: str
    model: Model
    prompt_text: str
    seed: int


def missing_jobs(slugs: list[str], models: list[Model], *, again: bool) -> list[Job]:
    jobs: list[Job] = []
    for slug in slugs:
        seed = seed_for_story(slug)
        for model in models:
            prompt_text = image_prompt_for(slug, model)
            if prompt_text is None:
                continue
            article_path = edition_folder(slug, model) / "images" / "article.png"
            if article_path.exists() and not again:
                continue
            jobs.append(Job(slug=slug, model=model, prompt_text=prompt_text, seed=seed))
    return jobs


# ------------------------------------------------------------------------------
# Doing one job
# ------------------------------------------------------------------------------

def make_thumbnail(article_path: Path, thumbnail_path: Path) -> None:
    """
    A small derived copy for the hover card, made from the full-size file that
    was just written - a hover card must never download the full illustration.
    """
    with Image.open(article_path) as full:
        full = full.convert("RGB")
        full.thumbnail((THUMBNAIL_MAX_SIDE, THUMBNAIL_MAX_SIDE), Image.LANCZOS)
        full.save(thumbnail_path, "PNG", optimize=True)


def render_one(client: httpx.Client, job: Job, *, actor: str) -> dict:
    folder = edition_folder(job.slug, job.model) / "images"
    folder.mkdir(parents=True, exist_ok=True)
    filename_prefix = f"{job.slug}--{job.model.slug}"

    free_gb = force_clean_vram(client)
    png_bytes, seconds = generate(client, job.prompt_text, filename_prefix, job.seed)

    article_path = folder / "article.png"
    article_path.write_bytes(png_bytes)
    make_thumbnail(article_path, folder / "thumbnail.png")

    meta = {
        "story": job.slug,
        "model_id": job.model.id,
        "model_slug": job.model.slug,
        "image_model": "flux2-dev",
        "quantization": "Q4_K_M",
        "seed": job.seed,
        "steps": STEPS,
        "guidance": GUIDANCE,
        "width": IMAGE_WIDTH,
        "height": IMAGE_HEIGHT,
        "prompt": job.prompt_text,
        "rendered_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "seconds_waited": round(seconds, 1),
        "vram_free_gb_before_start": round(free_gb, 2),
    }
    (folder / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    # THE DATABASE IS THE TRUTH (Nir, 2026-09-03: "do exactly what the Bible
    # says." LAW 5 + Part 12 12.2.4: image FILES are artifacts, but the image
    # JOB - which model, which seed, how long - is knowledge, and it is
    # stored in the database the moment it happens, through the one door.
    with connect() as db:
        with db.session() as session:
            session.run(
                "MERGE (i:ImageJob {key: $key}) SET i = $meta, i.key = $key "
                "WITH i MATCH (e:Edition {story_slug: $slug, model_slug: $model}) "
                "MERGE (e)-[:RENDERED_IMAGE]->(i)",
                key=f"edn-{job.slug}--{job.model.slug}", meta=meta,
                slug=job.slug, model=job.model.slug,
            )
    return meta


# ------------------------------------------------------------------------------
# Command line
# ------------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render illustrations for editions.")
    parser.add_argument("--story", help="one story slug")
    parser.add_argument("--all", action="store_true", help="every story")
    parser.add_argument("--model", help="one model id from the roster")
    parser.add_argument("--all-models", action="store_true", help="every model on the roster")
    parser.add_argument("--again", action="store_true",
                        help="render even where an image already exists")
    parser.add_argument("--actor", default="claude-sonnet-5")
    args = parser.parse_args(argv)

    slugs = all_story_slugs() if args.all else ([args.story] if args.story else [])
    models = roster() if args.all_models else ([model_by_id(args.model)] if args.model else [])
    if not slugs or not models:
        parser.error("say which stories (--story SLUG or --all) and which models "
                     "(--model ID or --all-models).")

    with httpx.Client() as client:
        if not comfy_alive(client):
            print(f"ComfyUI is not answering at {COMFY_URL}. Start it first - see "
                  f"AI-PANORAMA-WORKFLOW-2026-09-02.md for the exact command.")
            return 1

        jobs = missing_jobs(slugs, models, again=args.again)
        if not jobs:
            print("Nothing missing - every requested cell already has an image.")
            return 0

        story_count = len({job.slug for job in jobs})
        print(f"{len(jobs)} illustrations to render across {story_count} "
              f"stor{'y' if story_count == 1 else 'ies'} (ComfyUI, FLUX.2-dev, "
              f"one seed per story, shared by all editions of that story).")
        done: list[str] = []
        failed: list[str] = []
        started_all = time.monotonic()
        start_clock = datetime.now().strftime("%H:%M:%S")
        total = len(jobs)

        # LIVE PROGRESS, ALWAYS, FOREVER (locked 2026-09-02, Nir's explicit
        # instruction): every long-running process must show, continuously,
        # what it is doing right now, how many done out of how many total,
        # the percent complete, when it started, and an estimate of when it
        # will finish - never rely on someone polling a silent process.
        for index, job in enumerate(jobs, start=1):
            elapsed_all = time.monotonic() - started_all
            avg_so_far = elapsed_all / (index - 1) if index > 1 else None
            remaining = (total - index + 1) * avg_so_far if avg_so_far else None
            eta = (f", ETA ~{remaining / 60:.0f} min" if remaining else "")
            percent = (index - 1) / total * 100
            print(f"[{index}/{total} = {percent:4.0f}% done | started {start_clock}"
                  f"{eta}] cleaning VRAM, then rendering {job.slug} / "
                  f"{job.model.short_name} ...")
            label = f"{job.slug} / {job.model.short_name}"
            try:
                meta = render_one(client, job, actor=args.actor)
                print(f"  [{index}/{total}] {label:<70} OK  {meta['seconds_waited']:6.0f}s "
                      f"(VRAM free before start: {meta['vram_free_gb_before_start']:.1f} GB)")
                done.append(f"{job.slug}/{job.model.slug}")
            except (ComfyFailed, httpx.HTTPError) as problem:
                print(f"  [{index}/{total}] {label:<70} FAILED: "
                      f"{type(problem).__name__}: {problem}")
                failed.append(f"{job.slug}/{job.model.slug}: {type(problem).__name__}")

        total_seconds = time.monotonic() - started_all
        print("\n" + "=" * 78)
        print(f"FINISHED: rendered {len(done)}/{total} illustrations "
              f"({len(done) / total * 100:.0f}%), {len(failed)} failed, "
              f"{total_seconds / 60:.1f} minutes total, "
              f"started {start_clock}, finished {datetime.now().strftime('%H:%M:%S')}. "
              f"Cost: $0 (local).")
        for note in failed:
            print(f"  failed: {note}")

        try:
            with connect() as db:
                log_job(
                    db, action_type="stage_run", actor=args.actor,
                    verdict="partial" if failed else "ok",
                    cost_usd=0.0,
                    plain_words=(
                        f"Rendered {len(done)} edition illustrations locally with FLUX.2-dev "
                        f"(one fixed seed per story, shared by every model's edition of that "
                        f"story, but a different seed from story to story), "
                        f"{len(failed)} failed, at zero cost since generation runs on this "
                        f"machine's own GPU."),
                    outputs=done,
                )
        except Exception as problem:  # noqa: BLE001
            print(f"(could not write to the ledger: {type(problem).__name__})")

    return 1 if failed and not done else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
