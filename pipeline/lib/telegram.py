#!/usr/bin/env python3
"""
THE ONE PLACE THAT IS ALLOWED TO TALK TO TELEGRAM
=================================================

WHAT THIS IS, IN ONE SENTENCE
A tiny helper that sends Nir a Telegram message, written once here so that no
other file in the project ever has to touch the bot token itself.

WHY IT IS ITS OWN FILE (bible/part-07.md, secrets; part-01.md, one door rule)
The Bible's habit is: anything dangerous gets exactly ONE door, and everything
else walks through that door. The database will get pipeline/lib/db.py. The
control room gets this file. That way, if the rules around secrets ever change,
there is one file to fix, not twenty.

RULES THIS FILE OBEYS
1. The token is read from the .env file at the top of the repository and is
   NEVER printed, NEVER logged, and NEVER included in an error message. If
   something goes wrong, the error says "Telegram refused" and shows the
   description Telegram gave, with the token stripped out of any URL.
2. Messages go ONLY to TELEGRAM_OWNER_USER_ID, Nir's own numeric id. There is
   deliberately no way to pass a different recipient in: a bug can therefore
   never message a stranger (bible/part-07.md 7.8.1).
3. Standard library only. No installed packages. A script that must still work
   in five years should depend on as little as possible.
4. If the network is down it fails quietly with a printed message and a
   non-zero exit code, so a timer can retry later. It never crashes the caller
   with a wall of technical noise.

HOW TO USE IT FROM ANOTHER SCRIPT
    from lib.telegram import send
    send("Good morning. Everything is healthy.")
"""

from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

# The repository root is two folders up from this file: pipeline/lib/ -> repo.
REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = REPO_ROOT / ".env"

TELEGRAM_API = "https://api.telegram.org"


class TelegramNotConfigured(RuntimeError):
    """Raised when .env is missing, or still holds the dummy placeholders."""


def _read_env_file(path: Path) -> dict[str, str]:
    """
    Read a .env file into a dictionary.

    Deliberately simple: KEY=VALUE lines, '#' starts a comment, blank lines
    ignored, surrounding quotes stripped. No shell expansion, because we never
    want a value in .env to be able to run anything.
    """
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def _credentials() -> tuple[str, str]:
    """
    Return (token, owner_user_id).

    Real environment variables win over the .env file, so that a future
    systemd unit or container can inject them without editing files.
    """
    from_file = _read_env_file(ENV_FILE)
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or from_file.get("TELEGRAM_BOT_TOKEN", "")
    owner = os.environ.get("TELEGRAM_OWNER_USER_ID") or from_file.get("TELEGRAM_OWNER_USER_ID", "")

    # These are the exact placeholder values shipped in .env.example. Catching
    # them by name gives a clear human error instead of a confusing Telegram
    # rejection.
    if not token or "REPLACE-ME" in token:
        raise TelegramNotConfigured(
            "No real TELEGRAM_BOT_TOKEN found. Copy .env.example to .env and "
            "put the token from @BotFather into it."
        )
    if not owner or owner == "000000000" or not owner.isdigit():
        raise TelegramNotConfigured(
            "No real TELEGRAM_OWNER_USER_ID found in .env. It must be Nir's "
            "numeric Telegram user id."
        )
    return token, owner


def _scrub(text: str, token: str) -> str:
    """Remove the token from any text before it is shown to a human or a log."""
    return text.replace(token, "<token hidden>") if token else text


def send(text: str, *, quiet_failure: bool = True) -> bool:
    """
    Send one message to Nir. Returns True if Telegram accepted it.

    text          the message, plain text, no formatting markup. Telegram's
                  limit is 4096 characters; longer text is cut with a note,
                  because a truncated warning is better than no warning.
    quiet_failure True (the default) means network trouble prints one plain
                  line and returns False. False means it raises, for callers
                  that want to handle the problem themselves.
    """
    token, owner = _credentials()

    if len(text) > 4000:
        text = text[:3960] + "\n\n(Message was too long and was cut here.)"

    payload = json.dumps({
        "chat_id": owner,
        "text": text,
        "disable_web_page_preview": True,
    }).encode("utf-8")

    request = urllib.request.Request(
        f"{TELEGRAM_API}/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        # Default certificate verification, explicitly created so nobody can
        # later "fix" a certificate error by turning verification off.
        context = ssl.create_default_context()
        with urllib.request.urlopen(request, timeout=30, context=context) as response:
            answer = json.loads(response.read().decode("utf-8"))
        if answer.get("ok"):
            return True
        raise RuntimeError("Telegram refused the message: " + str(answer.get("description")))
    except Exception as problem:  # noqa: BLE001 - one honest catch-all on purpose
        message = "Could not send the Telegram message: " + _scrub(str(problem), token)
        if quiet_failure:
            print(message, file=sys.stderr)
            return False
        raise RuntimeError(message) from None


if __name__ == "__main__":
    # Running this file directly sends a test message. Useful after moving the
    # project to a new machine: it proves the .env is correct before anything
    # else is built on top of it.
    ok = send("Test message from the desktop computer, Linux side. If you can "
              "read this, the control room works.")
    print("Sent." if ok else "Not sent. See the error above.")
    sys.exit(0 if ok else 1)
