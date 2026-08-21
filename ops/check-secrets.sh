#!/usr/bin/env bash
# ============================================================================
# THE SECRET SCANNER
# ============================================================================
#
# WHAT IT DOES, IN ONE SENTENCE
# It looks for passwords and API keys that are about to be saved into git, and
# it stops you before that happens.
#
# WHY IT EXISTS
# A leaked key can be used by a stranger to spend Nir's money. Once a secret
# is committed to git it is in the history forever, even if you delete the
# line afterwards. So the only real defence is never letting it in.
# See bible/part-07.md section 7.4.2.
#
# HOW TO USE IT
#   ops/check-secrets.sh                 checks whatever git is about to commit
#   ops/check-secrets.sh some/file.txt   checks specific files instead
#
# WHAT IT PRINTS
# The file name, the line number, and WHAT KIND of secret it thinks it found.
# It never prints the secret itself, because that would just move the leak
# into your terminal history and your logs.
#
# EXIT CODES
#   0 = clean, nothing suspicious found
#   1 = something suspicious found, and it is named in the output
#   2 = the script could not run properly (for example, not a git repository)
# ============================================================================

set -uo pipefail

# ----------------------------------------------------------------------------
# The patterns we look for. Each one is a name, then a regular expression.
# Add new ones here as new services get used; keep the name plain English.
# ----------------------------------------------------------------------------
PATTERN_NAMES=(
  "an OpenRouter API key"
  "an OpenAI-style API key"
  "an Anthropic API key"
  "a Telegram bot token"
  "an Amazon access key"
  "a Google API key"
  "a GitHub token"
  "a Slack token"
  "a private key file header"
  "a password or token being assigned a long value"
  "a database connection string with a password in it"
)

PATTERN_REGEXES=(
  'sk-or-v1-[A-Za-z0-9_-]{16,}'
  'sk-[A-Za-z0-9]{20,}'
  'sk-ant-[A-Za-z0-9_-]{16,}'
  '[0-9]{8,10}:[A-Za-z0-9_-]{30,}'
  'AKIA[0-9A-Z]{16}'
  'AIza[0-9A-Za-z_-]{30,}'
  'gh[pousr]_[A-Za-z0-9]{30,}'
  'xox[baprs]-[A-Za-z0-9-]{10,}'
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  '(password|passwd|secret|token|api[_-]?key|apikey|access[_-]?key)[[:space:]]*[:=][[:space:]]*.?[A-Za-z0-9/+_-]{16,}'
  '(bolt|neo4j|postgres|postgresql|mysql|mongodb|redis|ftp|ftps|sftp)://[^:@[:space:]]+:[^@[:space:]]+@'
)

# ----------------------------------------------------------------------------
# Files we deliberately do NOT complain about.
# .env.example is a documentation file full of obvious fake values.
# This script itself contains the patterns, so it would always match itself.
# ----------------------------------------------------------------------------
is_exempt() {
  case "$1" in
    *.env.example|.env.example) return 0 ;;
    *ops/check-secrets.sh) return 0 ;;
    *) return 1 ;;
  esac
}

# ----------------------------------------------------------------------------
# Work out which files to look at.
# With arguments: exactly those files.
# Without arguments: the files git is about to commit (the staged ones).
# ----------------------------------------------------------------------------
FILES=()
if [ "$#" -gt 0 ]; then
  FILES=("$@")
  echo "Secret scanner: checking ${#FILES[@]} file(s) given on the command line."
else
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Secret scanner ERROR: this is not a git repository, and no files were named." >&2
    echo "Either run it inside the project folder, or pass file names to check." >&2
    exit 2
  fi
  # -z plus a null-delimited read handles file names containing spaces safely.
  while IFS= read -r -d '' staged_file; do
    FILES+=("$staged_file")
  done < <(git diff --cached --name-only --diff-filter=ACM -z)
  echo "Secret scanner: checking ${#FILES[@]} file(s) that git is about to commit."
fi

if [ "${#FILES[@]}" -eq 0 ]; then
  echo "Secret scanner: nothing to check. CLEAN."
  exit 0
fi

# ----------------------------------------------------------------------------
# The actual scan.
# ----------------------------------------------------------------------------
FINDINGS=0

for file in "${FILES[@]}"; do
  [ -f "$file" ] || continue
  if is_exempt "$file"; then
    continue
  fi
  # Skip anything that is not text (images, zip files, compiled things).
  if ! grep -Iq . "$file" 2>/dev/null; then
    continue
  fi

  index=0
  while [ "$index" -lt "${#PATTERN_REGEXES[@]}" ]; do
    regex="${PATTERN_REGEXES[$index]}"
    name="${PATTERN_NAMES[$index]}"
    # -n gives the line number. We print ONLY the number, never the content.
    while IFS= read -r line_number; do
      [ -n "$line_number" ] || continue
      echo "  POSSIBLE SECRET: $file line $line_number looks like $name"
      FINDINGS=$((FINDINGS + 1))
    done < <(grep -n -E -i -o "$regex" "$file" 2>/dev/null | cut -d: -f1 | sort -un)
    index=$((index + 1))
  done

  # A .env file should never be committed at all, whatever is inside it.
  case "$(basename "$file")" in
    .env|.env.local|.env.production|.env.pipeline)
      echo "  FORBIDDEN FILE: $file is a real secrets file and must never be committed"
      FINDINGS=$((FINDINGS + 1))
      ;;
  esac
done

echo
if [ "$FINDINGS" -gt 0 ]; then
  echo "SECRET SCANNER: STOPPED. $FINDINGS suspicious item(s) found above."
  echo
  echo "What to do now, in plain words:"
  echo "  1. Open each file listed and look at the line named."
  echo "  2. If it really is a password or key, take it out of the file and put"
  echo "     it in the .env file instead, which git never touches."
  echo "  3. If it is a harmless false alarm (an example, a test value), you can"
  echo "     commit anyway by adding --no-verify to the git commit command."
  echo "     Do that only when you are certain."
  exit 1
fi

echo "SECRET SCANNER: CLEAN. No passwords or keys found in what you are committing."
exit 0
