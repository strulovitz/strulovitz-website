#!/usr/bin/env bash
#
# deploy.sh -- put the built site onto www.strulovitz.org, in the right order
#
# WHAT THIS IS, IN ONE SENTENCE
# The one command that publishes the site, asking Nir for the server password
# each time and storing it nowhere.
#
# WHY THE PASSWORD IS TYPED EVERY TIME
# bible/part-07.md 7.4.4 keeps the website's password out of every file and out
# of every agent's hands, because an agent that cannot reach the live site can
# never break the live site. Nir overruled that once, on 2026-08-21, by giving
# the password in chat and asking for the upload; this script exists so that it
# never has to be pasted into a conversation again. It is read from the keyboard,
# held in one shell variable, and gone when the command finishes.
#
# WHY THE ORDER MATTERS, AND IT REALLY DOES
# The dated folder goes up FIRST and pointer.json goes up LAST. Until the
# pointer lands, every visitor is still being served the previous version, whole
# and working. The moment it lands, everyone gets the new one. So a slow or
# half-finished upload can never show anybody a broken site.
#
# GOING BACK
# Re-upload an older pointer from ops/pointers/. That is the entire rollback:
# one small file, one minute, from any computer.
#
# HOW TO RUN IT
#     python3 ops/build-export.py        # build first
#     ./ops/deploy.sh                    # then publish
#
# It will show exactly what it is about to do and wait for you to say yes.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXPORTS="$HERE/exports"
ENV_FILE="$HERE/.env"

# The server details live in .env. The PASSWORD deliberately does not.
HOST="$(grep -E '^FTP_HOST=' "$ENV_FILE" | cut -d= -f2-)"
USER="$(grep -E '^FTP_USER=' "$ENV_FILE" | cut -d= -f2-)"
WEB_ROOT="$(grep -E '^FTP_REMOTE_WEB_ROOT=' "$ENV_FILE" | cut -d= -f2-)"

if [[ -z "$HOST" || -z "$USER" || -z "$WEB_ROOT" || "$HOST" == *REPLACE-ME* ]]; then
  echo "The server details are missing from .env (FTP_HOST, FTP_USER, FTP_REMOTE_WEB_ROOT)."
  exit 1
fi

if [[ ! -f "$EXPORTS/pointer.json" ]]; then
  echo "There is nothing built yet. Run this first:"
  echo "    python3 ops/build-export.py"
  exit 1
fi

VERSION="$(python3 -c "import json;print(json.load(open('$EXPORTS/pointer.json'))['live'])")"

if [[ ! -d "$EXPORTS/$VERSION" ]]; then
  echo "pointer.json names '$VERSION' but exports/$VERSION does not exist."
  echo "Run python3 ops/build-export.py again."
  exit 1
fi

FILE_COUNT="$(find "$EXPORTS/$VERSION" -type f | wc -l)"

echo ""
echo "ABOUT TO PUBLISH TO THE REAL WEBSITE"
echo "  server      $USER@$HOST"
echo "  web root    $WEB_ROOT"
echo "  version     $VERSION  ($FILE_COUNT files)"
echo ""
echo "  step 1  upload the folder $VERSION            (visitors still see the old site)"
echo "  step 2  upload index.html and night-watch.html"
echo "  step 3  upload pointer.json                   <- THIS is the moment it flips"
echo ""
read -r -p "Type yes to go ahead: " AGREED
if [[ "$AGREED" != "yes" ]]; then
  echo "Nothing was uploaded."
  exit 0
fi

echo ""
echo "The password is read from the keyboard, kept in memory only, and written to"
echo "no file. It will not appear on screen as you type it."
read -r -s -p "SFTP password for $USER: " SFTP_PASSWORD
echo ""
echo ""

if ! command -v lftp >/dev/null 2>&1; then
  echo "lftp is not installed. Install it with:  sudo apt-get install -y lftp"
  exit 1
fi

# LFTP_PASSWORD is read by lftp from the environment, so the password never
# appears in the command line, where any other user on the machine could see it
# in the process list.
run_lftp() {
  LFTP_PASSWORD="$SFTP_PASSWORD" lftp -u "$USER",  --env-password \
    -e "set sftp:auto-confirm yes; set net:max-retries 3; set net:timeout 30; $1; bye" \
    "sftp://$HOST"
}

echo "STEP 1 of 3  uploading the folder $VERSION ..."
run_lftp "mirror --reverse --delete --verbose=1 --parallel=3 '$EXPORTS/$VERSION' '$WEB_ROOT/$VERSION'"

echo ""
echo "STEP 2 of 3  uploading the pages at the root ..."
run_lftp "cd '$WEB_ROOT'; put '$EXPORTS/index.html' -o index.html; put '$EXPORTS/night-watch.html' -o night-watch.html"

echo ""
echo "STEP 3 of 3  uploading pointer.json - this is the moment it goes live ..."
run_lftp "cd '$WEB_ROOT'; put '$EXPORTS/pointer.json' -o pointer.json"

unset SFTP_PASSWORD

echo ""
echo "PUBLISHED. $VERSION is live at https://www.strulovitz.org/"
echo ""
echo "Check it, and if anything is wrong, go back by uploading an older pointer"
echo "from ops/pointers/ - that is the whole rollback."
