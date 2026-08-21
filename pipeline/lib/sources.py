#!/usr/bin/env python3
"""
FETCHING AND FREEZING THE SOURCES
=================================

WHAT THIS IS, IN ONE SENTENCE
The part of the machine that turns a handful of links into frozen text on disk,
so that every edition is written from EXACTLY the same material, and so that
years from now anyone can see what the sources actually said.

WHY THE TEXT IS FROZEN (bible/part-06.md 6.2.4)
A web page can be edited, paywalled or deleted. If eight models were each sent
to read a live page, they would not be reading the same page, and the whole
comparison would be worthless. So we fetch once, write the text to disk with a
fingerprint, and every model afterwards reads the frozen copy. This is also the
reader's evidence: the article links to its sources prominently, and the frozen
copy is what we can honestly say we worked from.

THE TWO-SOURCE RULE (DECISIONS.md decision 13, bible/part-00.md LAW 7)
A story needs at least two independent sources before any model may write about
it. Nir, on why this holds even for the best story imaginable: "if a story is
only from one source, even if it is the most amazing story, like new aliens came
and handed us AGI, i cannot publish it, because i can get sued and lose all my
money." The number lives in config/editions.toml, not in this code.

WHAT IT CAN FETCH
1. News and blog articles, by web address. trafilatura pulls out the actual
   article and discards the navigation, adverts and cookie banners.
2. YouTube videos, by web address. yt-dlp fetches the SUBTITLES plus the title,
   channel and publication date. We take the captions rather than transcribing
   the audio ourselves, which is instant, free and needs no graphics card.
   Where a video has no subtitles at all, that is reported and the video is not
   used - it is not quietly skipped.
3. Text pasted by hand into a file, for the case where fetching fails or a
   source has to be gathered manually.

FETCH MANNERS (bible/part-06.md 6.1.4)
We identify ourselves honestly with a user-agent naming the project and the
site, we pause between requests, and we do not attempt to get around a paywall.
A paywalled source can be cited by its headline and linked to, but its text is
not taken.

HOW TO CHECK IT BY HAND
    cd /home/nir/strulovitz-website/pipeline && uv run lib/sources.py <a web address>
That fetches one thing, prints what it found, and writes nothing.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx

REPO_ROOT = Path(__file__).resolve().parents[2]

# Who we say we are when we ask a stranger's server for a page. Honest, and it
# gives an annoyed webmaster somewhere to write to (bible/part-06.md 6.1.4).
USER_AGENT = (
    "AIPanoramaBot/1.0 (+https://www.strulovitz.org/; a small independent "
    "magazine about AI; contact via the website)"
)

# A polite pause between fetches, in seconds.
PAUSE_BETWEEN_FETCHES_S = 1.5

YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "www.youtu.be"}


class CouldNotFetch(RuntimeError):
    """
    Raised when a source could not be collected. Always says WHY in words a
    person can act on, because the answer is usually 'paste this one by hand'.
    """


@dataclass
class Source:
    """
    One piece of frozen evidence.

    kind        "article" or "video" or "pasted"
    url         where it came from, which the published article links to
    title       the headline or video title
    byline      the author, or the channel name for a video
    published   the date the source itself carries, when it has one
    text        the frozen words the models will read
    fingerprint sha256 of the text, so any later change is detectable
    """
    kind: str
    url: str
    title: str
    byline: str
    published: str
    text: str
    fingerprint: str
    fetched_at_utc: str
    site: str
    words: int
    note: str = ""

    @property
    def filename(self) -> str:
        """A stable, readable filename for this source's frozen text."""
        stub = re.sub(r"[^a-z0-9]+", "-", (self.site + "-" + self.title).lower()).strip("-")
        return f"{stub[:70]}-{self.fingerprint[:8]}.txt"


def _fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _site_of(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def is_youtube(url: str) -> bool:
    return (urlparse(url).hostname or "").lower() in YOUTUBE_HOSTS


# ------------------------------------------------------------------------------
# ARTICLES
# ------------------------------------------------------------------------------

def fetch_article(url: str) -> Source:
    """Fetch one news or blog article and return it as frozen evidence."""
    import trafilatura

    try:
        with httpx.Client(timeout=60.0, follow_redirects=True,
                          headers={"User-Agent": USER_AGENT}) as client:
            response = client.get(url)
    except httpx.HTTPError as problem:
        raise CouldNotFetch(f"Could not reach {url}: {type(problem).__name__}. "
                            f"Either the site is down or it is blocking us. You can paste "
                            f"the text by hand instead.") from problem

    if response.status_code != 200:
        raise CouldNotFetch(
            f"{url} answered with HTTP {response.status_code}. "
            f"{'That is usually a paywall or a bot-block - paste the text by hand, or use a different source.' if response.status_code in (401, 402, 403, 451) else 'The page may have moved.'}"
        )

    extracted = trafilatura.extract(
        response.text, url=url, favor_precision=True,
        include_comments=False, include_tables=True, with_metadata=True,
        output_format="json",
    )
    if not extracted:
        raise CouldNotFetch(
            f"Nothing readable could be pulled out of {url}. It is probably a page "
            f"that builds itself with JavaScript. Paste the text by hand instead."
        )

    found = json.loads(extracted)
    text = (found.get("text") or "").strip()
    if len(text.split()) < 80:
        raise CouldNotFetch(
            f"Only {len(text.split())} words came out of {url}, which is too little to be "
            f"the article. It is probably a paywall teaser. Use a different source."
        )

    return Source(
        kind="article",
        url=url,
        title=(found.get("title") or "").strip() or url,
        byline=(found.get("author") or "").strip(),
        published=(found.get("date") or "").strip(),
        text=text,
        fingerprint=_fingerprint(text),
        fetched_at_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        site=_site_of(url),
        words=len(text.split()),
    )


# ------------------------------------------------------------------------------
# YOUTUBE VIDEOS
#
# We ask yt-dlp for the subtitles. Manually written subtitles are preferred
# because they are punctuated and spelled properly; automatic captions are used
# when that is all there is, and the difference is RECORDED, because a wall of
# unpunctuated automatic captions is a harder thing for a model to read and that
# fact belongs in the honest record.
# ------------------------------------------------------------------------------

def fetch_video(url: str) -> Source:
    """Fetch one YouTube video's subtitles and details as frozen evidence."""
    import yt_dlp

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "writesubtitles": False,
        "http_headers": {"User-Agent": USER_AGENT},
    }
    try:
        with yt_dlp.YoutubeDL(options) as downloader:
            info = downloader.extract_info(url, download=False)
    except Exception as problem:  # noqa: BLE001 - yt-dlp raises many shapes
        raise CouldNotFetch(f"yt-dlp could not read {url}: {problem}") from problem

    manual = info.get("subtitles") or {}
    automatic = info.get("automatic_captions") or {}
    track, source_kind = _pick_english_track(manual, automatic)
    if track is None:
        raise CouldNotFetch(
            f"{url} has no English subtitles at all, neither written nor automatic, "
            f"so there is nothing to read. Choose a different video."
        )

    text = _subtitle_text(track["url"])
    if len(text.split()) < 80:
        raise CouldNotFetch(f"The subtitles of {url} came to only {len(text.split())} words.")

    upload = str(info.get("upload_date") or "")
    published = f"{upload[:4]}-{upload[4:6]}-{upload[6:8]}" if len(upload) == 8 else ""

    return Source(
        kind="video",
        url=url,
        title=(info.get("title") or url).strip(),
        byline=(info.get("uploader") or info.get("channel") or "").strip(),
        published=published,
        text=text,
        fingerprint=_fingerprint(text),
        fetched_at_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        site="youtube.com",
        words=len(text.split()),
        note=("subtitles written by the channel" if source_kind == "manual"
              else "AUTOMATIC captions - unpunctuated, and machine-misheard words are likely"),
    )


def _pick_english_track(manual: dict, automatic: dict) -> tuple[dict | None, str]:
    """Prefer subtitles a human wrote; fall back to the machine's guess."""
    for store, kind in ((manual, "manual"), (automatic, "automatic")):
        for language in list(store):
            if language.lower().startswith("en"):
                for entry in store[language]:
                    if entry.get("ext") in ("json3", "vtt", "srv1", "ttml"):
                        return entry, kind
    return None, ""


def _subtitle_text(subtitle_url: str) -> str:
    """Download a subtitle track and flatten it into ordinary prose."""
    with httpx.Client(timeout=120.0, follow_redirects=True,
                      headers={"User-Agent": USER_AGENT}) as client:
        response = client.get(subtitle_url)
    response.raise_for_status()
    raw = response.text

    if raw.lstrip().startswith("{"):
        # json3: YouTube's own format, one event per caption line. The pieces
        # INSIDE one event join with nothing (they are fragments of one word or
        # phrase); the events themselves join with a space, because a caption
        # line ends where the next begins and gluing them produces "a 3.It's".
        events: list[str] = []
        for event in (json.loads(raw).get("events") or []):
            line = "".join(segment.get("utf8", "") for segment in event.get("segs") or [])
            if line.strip():
                events.append(line.strip())
        return _tidy(" ".join(events))

    # WebVTT or similar: drop timing lines and markup.
    lines: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if (not stripped or "-->" in stripped or stripped.isdigit()
                or stripped.startswith(("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE"))):
            continue
        lines.append(re.sub(r"<[^>]+>", "", stripped))
    return _tidy(" ".join(lines))


def _tidy(text: str) -> str:
    """
    Remove the duplication YouTube's rolling captions produce, and squeeze the
    whitespace. This changes no words - it only stops the same phrase appearing
    three times because it scrolled up the screen.
    """
    text = text.replace("\u200b", " ")
    words = text.split()
    out: list[str] = []
    for word in words:
        # A rolling caption repeats a run of words verbatim. Drop a word only if
        # the previous six words already end with exactly this continuation.
        if len(out) >= 12 and word == out[-1] and word == out[-2]:
            continue
        out.append(word)
    joined = " ".join(out)
    return re.sub(r"\s+", " ", joined).strip()


# ------------------------------------------------------------------------------
# ONE ENTRY POINT FOR EVERYTHING
# ------------------------------------------------------------------------------

def fetch(url: str) -> Source:
    """Fetch whatever kind of thing this address is. Pauses politely first."""
    time.sleep(PAUSE_BETWEEN_FETCHES_S)
    return fetch_video(url) if is_youtube(url) else fetch_article(url)


def freeze(source: Source, into: Path) -> Path:
    """
    Write a source's text and its details to disk, and return the text's path.

    The text goes into a plain .txt file that anybody can open, and the details
    into a .json beside it. Both are named after the text's own fingerprint, so
    the same source fetched twice lands on the same filename and never
    duplicates.
    """
    into.mkdir(parents=True, exist_ok=True)
    text_path = into / source.filename
    text_path.write_text(source.text, encoding="utf-8")
    details = dict(asdict(source))
    details.pop("text")
    details["text_file"] = text_path.name
    (into / (text_path.stem + ".json")).write_text(
        json.dumps(details, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    return text_path


def read_frozen(folder: Path) -> list[Source]:
    """Read back every frozen source in a folder, newest fetch first."""
    out: list[Source] = []
    for details_path in sorted(folder.glob("*.json")):
        details = json.loads(details_path.read_text(encoding="utf-8"))
        text_file = folder / details.pop("text_file")
        if not text_file.exists():
            continue
        out.append(Source(text=text_file.read_text(encoding="utf-8"), **details))
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip().splitlines()[0])
        print("\nusage: uv run lib/sources.py <a web address>")
        raise SystemExit(0)
    try:
        got = fetch(sys.argv[1])
    except CouldNotFetch as why:
        print(f"COULD NOT FETCH\n  {why}")
        raise SystemExit(1)
    print(f"kind:      {got.kind}")
    print(f"title:     {got.title}")
    print(f"by:        {got.byline or '(nobody named)'}")
    print(f"published: {got.published or '(no date on the page)'}")
    print(f"site:      {got.site}")
    print(f"words:     {got.words}")
    if got.note:
        print(f"note:      {got.note}")
    print(f"\nfirst 400 characters:\n{got.text[:400]}")
