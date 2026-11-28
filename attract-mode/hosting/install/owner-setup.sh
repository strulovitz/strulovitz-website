#!/usr/bin/env bash
#
# attract-mode/hosting/install/owner-setup.sh
#
# THE ONE SETUP SCRIPT -- Part 01, section 1.9.
#
# Nir runs this himself, once on each PC, and types his Linux password when
# the terminal asks. An agent never runs it and never asks for the password.
#
# It is SAFE TO RUN TWICE: every piece is checked first and skipped if it is
# already there.
#
# It installs ONLY the Stage 0 pieces (Part 11, section 11.4):
#     PHP (with the extensions Moodle asks for) and MariaDB.
#     Syncthing too, but only when its version is pinned in config/pins.
#
# It does NOT install Moodle. The Bible says "NOT YET: Moodle" for Stage 0;
# Moodle comes on the desktop at Stage 2 and on the laptop at Stage 3.
#
# It does NOT touch Caddy, the three live websites, Apache, or any file of
# the running site. Not one line of the live hosting changes here.
#
# Every version comes from attract-mode/config/pins. Never "latest".
# A piece whose pin says OPEN is skipped and named in the final summary.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AM_ROOT="$(cd "$HERE/../.." && pwd)"
PINS="$AM_ROOT/config/pins"

# No package may ever stop to ask a question: the script runs without a person
# at the keyboard (D78), and a question with nobody to answer it waits forever.
# MariaDB asks about an anonymous feedback plugin exactly like that, and it hung
# a real run on 2026-11-28. Every apt call below says noninteractive for this
# reason.
say()  { printf '%s\n' "$*"; }
step() { printf '\n== %s ==\n' "$*"; }
warn() { printf 'NOTE: %s\n' "$*"; }
die()  { printf '\nSTOPPED: %s\n' "$*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

# The version of one piece, read from the pins file. Empty means OPEN.
pin_of() {
    # A pins line is: name, TWO OR MORE spaces, value, two or more spaces and
    # the reason. Splitting on $2 is wrong, because a name may hold a space
    # ("PHP (desktop)"). So the gaps are collapsed into tabs first.
    awk -v want="$1" '
        /^[ \t]/ { next }
        {
            line = $0
            gsub(/  +/, "\t", line)
            split(line, f, "\t")
            if (f[1] == want) {
                v = f[2]
                gsub(/^ +| +$/, "", v)
                if (v == "OPEN") v = ""
                print v
                exit
            }
        }
    ' "$PINS" 2>/dev/null || true
}

# sudo on this PC refuses to set DEBIAN_FRONTEND itself ("sorry, you are not
# allowed to set the following environment variables"), so it is set inside the
# shell that sudo runs. Without it a package may stop to ask a question forever
# (D78: nobody is at the keyboard).
apt_refresh() {
    sudo sh -c 'DEBIAN_FRONTEND=noninteractive apt-get update'
}

apt_install() {
    sudo sh -c 'DEBIAN_FRONTEND=noninteractive apt-get install -y "$@"' sh "$@"
}

# ---------------------------------------------------------------------------
step "BEFORE ANYTHING: WHO AND WHERE"
# ---------------------------------------------------------------------------

if [ "$(id -u)" -eq 0 ]; then
    die "Run this as Nir, not as root. It asks for the password itself."
fi

[ -r "$PINS" ] || die "Cannot read the pins file: $PINS"
[ -r /etc/os-release ] || die "Cannot read /etc/os-release. This is not a Linux this script knows."
. /etc/os-release

case "${ID:-unknown}" in
    linuxmint|ubuntu) FAMILY=ubuntu ;;
    debian)           FAMILY=debian ;;
    *) die "This script knows Linux Mint, Ubuntu and Debian. This PC says: ${ID:-unknown}. Nothing was changed." ;;
esac

case "$FAMILY" in
    ubuntu) PCLABEL=desktop ;;   # Linux Mint 22 is Ubuntu 24.04
    debian) PCLABEL=laptop ;;    # Debian 13
esac
# The pins own the number (Part 01, 1.8). This is only the fallback used before
# the pins are read, so that the first report lines are never empty.
case "$PCLABEL" in
    desktop) PHP_WANT=8.3 ;;
    laptop)  PHP_WANT=8.4 ;;
esac

# MariaDB's own repository script detects the OS from /etc/os-release, and
# Linux Mint calls itself "linuxmint", which that script does not know. Mint 22
# is Ubuntu 24.04 underneath, so on Mint we tell the script the truth about its
# base. Without this, the database cannot be installed on this PC at all.
MARIADB_OS_FLAGS=""
# That script wants the codename of the base system, not its number:
# --os-version=noble, not 24.04. Mint 22 carries UBUNTU_CODENAME=noble.
case "${UBUNTU_CODENAME:-}" in
    noble|jammy) MARIADB_OS_FLAGS="--os-type=ubuntu --os-version=${UBUNTU_CODENAME}" ;;
esac

say "PC:            $(hostname)"
say "System:        ${PRETTY_NAME:-$ID}"
say "Family:        $FAMILY"
say "PHP wanted:    $PHP_WANT   (from the pins; PHP 8.5 is not supported)"
say "Pins file:     $PINS"

# ---------------------------------------------------------------------------
step "THE PLAN -- this is everything that will happen"
# ---------------------------------------------------------------------------

cat <<'PLAN'
1. Read the versions from config/pins. Never "latest".
2. Refresh the list of available packages (apt update).
3. Install PHP for the website, with the extensions Moodle asks for.
4. Install MariaDB, the database (version 11.8 series on both PCs).
5. Install Syncthing ONLY if its pin is a real number; if the pin says
   OPEN, Syncthing is skipped and named in the summary.
6. Print the version of each piece, so "am doctor" can compare the PCs.

THIS SCRIPT WILL NOT:
  - install Moodle            (Stage 2 on the desktop, Stage 3 on the laptop)
  - touch Caddy or the live websites
  - touch Apache
  - store any password anywhere
  - change any file of the running site
PLAN

printf '\nType yes to continue, anything else stops here: '
read -r answer
[ "$answer" = "yes" ] || die "You did not type yes. Nothing was changed."

# ---------------------------------------------------------------------------
step "1. THE PINS"
# ---------------------------------------------------------------------------

MOODLE_PIN="$(pin_of 'Moodle')"
PHP_PIN="$(pin_of "PHP ($PCLABEL)")"
[ -n "$PHP_PIN" ] && PHP_WANT="$PHP_PIN"
MARIADB_PIN="$(pin_of 'MariaDB')"
SYNCTHING_PIN="$(pin_of 'Syncthing')"

say "Moodle pin:     ${MOODLE_PIN:-OPEN}   (not installed now, on purpose)"
say "PHP pin:        ${PHP_PIN:-OPEN}"
say "MariaDB pin:    ${MARIADB_PIN:-OPEN}"
say "Syncthing pin:  ${SYNCTHING_PIN:-OPEN}"

[ -n "$PHP_PIN" ]     || die "The PHP pin is OPEN. Fill it in config/pins first. Nothing was changed."
[ -n "$MARIADB_PIN" ] || die "The MariaDB pin is OPEN. Fill it in config/pins first. Nothing was changed."

case "$MARIADB_PIN" in
    11.8*) ;;
    *) die "The MariaDB pin is '$MARIADB_PIN' but this script installs the 11.8 series. Nothing was changed." ;;
esac

# ---------------------------------------------------------------------------
step "2. REFRESH THE PACKAGE LIST"
# ---------------------------------------------------------------------------

say "RUNNING: refresh the package list"
apt_refresh

# ---------------------------------------------------------------------------
step "3. PHP $PHP_WANT (the website's language)"
# ---------------------------------------------------------------------------

# The extensions Moodle 5.3 asks for, as Ubuntu/Debian package names.
PHP_PKGS=(
    "php$PHP_WANT-cli"
    "php$PHP_WANT-fpm"
    "php$PHP_WANT-mysql"
    "php$PHP_WANT-curl"
    "php$PHP_WANT-gd"
    "php$PHP_WANT-mbstring"
    "php$PHP_WANT-xml"
    "php$PHP_WANT-zip"
    "php$PHP_WANT-intl"
    "php$PHP_WANT-bcmath"
    "php$PHP_WANT-opcache"
)

if have "php$PHP_WANT"; then
    say "PHP $PHP_WANT is already here: $(php"$PHP_WANT" -r 'echo PHP_VERSION;' 2>/dev/null || echo '?')"
    say "Checking that every extension package is present (this is safe to repeat)."
else
    say "PHP $PHP_WANT is not here yet."
fi

say "RUNNING: install ${PHP_PKGS[*]}"
apt_install "${PHP_PKGS[@]}"

if have "php$PHP_WANT"; then
    say "PHP now: $(php"$PHP_WANT" -r 'echo PHP_VERSION;')"
else
    say "PHP now: $(php -r 'echo PHP_VERSION;' 2>/dev/null || echo 'not found')"
fi

# ---------------------------------------------------------------------------
step "4. MARIADB $MARIADB_PIN SERIES (the database)"
# ---------------------------------------------------------------------------

if [ "$FAMILY" = "ubuntu" ]; then
    # Ubuntu 24.04 ships MariaDB 10.11, which is too old for Moodle 5.3
    # (Part 01, section 1.8, fact 3). The 11.8 series comes from MariaDB's
    # own package repository.
    if dpkg -s mariadb-server >/dev/null 2>&1 && mariadb --version 2>/dev/null | grep -q '11\.8'; then
        say "MariaDB 11.8 is already here."
    else
        say "Ubuntu's own MariaDB is too old, so MariaDB's own repository is added first."
        say "RUNNING: MariaDB's official repo setup, series 11.8 ${MARIADB_OS_FLAGS}"
        curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup \
            | sudo bash -s -- --mariadb-server-version=11.8 $MARIADB_OS_FLAGS
    fi
else
    say "Debian 13 already ships the 11.8 series."
fi

say "RUNNING: install mariadb-server"
apt_install mariadb-server

if have mariadb; then
    say "MariaDB now: $(mariadb --version)"
else
    say "MariaDB now: $(mysql --version 2>/dev/null || echo 'not found')"
fi

# ---------------------------------------------------------------------------
step "5. SYNCTHING (the folder copied between the two PCs)"
# ---------------------------------------------------------------------------

if [ -z "$SYNCTHING_PIN" ]; then
    warn "The Syncthing pin is OPEN, so Syncthing is NOT installed."
    warn "The Bible says: never 'latest'. A real number goes into config/pins first."
    SYNCTHING_RESULT="skipped (pin is OPEN)"
else
    # The two distributions ship two different old versions (Mint/Ubuntu
    # 1.27.2, Debian 1.29.5). The pins rule needs ONE number on both PCs,
    # so Syncthing comes from its own repository. The channel follows the
    # major version of the pin.
    case "$SYNCTHING_PIN" in
        1.*) SYNC_CHANNEL="stable" ;;
        2.*) SYNC_CHANNEL="stable-v2" ;;
        *) die "The Syncthing pin '$SYNCTHING_PIN' is neither 1.x nor 2.x. Nothing was changed." ;;
    esac

    say "Syncthing comes from Syncthing's own repository, channel $SYNC_CHANNEL, so both PCs match."

    if [ ! -f /etc/apt/keyrings/syncthing-archive-keyring.gpg ]; then
        say "RUNNING: download Syncthing's signing key"
        sudo mkdir -p /etc/apt/keyrings
        curl -L --max-time 60 -o /tmp/syncthing-archive-keyring.gpg https://syncthing.net/release-key.gpg
        sudo mv /tmp/syncthing-archive-keyring.gpg /etc/apt/keyrings/syncthing-archive-keyring.gpg
        sudo chmod 644 /etc/apt/keyrings/syncthing-archive-keyring.gpg
    else
        say "Syncthing's signing key is already here."
    fi

    if ! grep -qs "apt.syncthing.net" /etc/apt/sources.list.d/syncthing.list; then
        say "RUNNING: add the Syncthing repository ($SYNC_CHANNEL)"
        printf 'deb [signed-by=/etc/apt/keyrings/syncthing-archive-keyring.gpg] https://apt.syncthing.net/ syncthing %s\n' "$SYNC_CHANNEL" \
            | sudo tee /etc/apt/sources.list.d/syncthing.list >/dev/null
        say "RUNNING: refresh the package list (to see the new repository)"
        apt_refresh
    else
        say "The Syncthing repository is already here."
    fi

    say "RUNNING: install syncthing=$SYNCTHING_PIN"
    apt_install "syncthing=$SYNCTHING_PIN"

    INSTALLED_SYNC="$(syncthing --version 2>/dev/null | awk '{print $2}' | sed 's/^v//' | head -1 || true)"
    SYNCTHING_RESULT="installed, version ${INSTALLED_SYNC:-unknown}"
    if [ "$INSTALLED_SYNC" = "$SYNCTHING_PIN" ]; then
        say "Syncthing matches the pin exactly: $INSTALLED_SYNC"
    else
        warn "Installed Syncthing is '${INSTALLED_SYNC:-unknown}' but the pin says $SYNCTHING_PIN."
    fi
fi

# ---------------------------------------------------------------------------
step "DONE -- THE PLAIN SUMMARY"
# ---------------------------------------------------------------------------

cat <<SUMMARY

PHP $PHP_WANT:      $(have "php$PHP_WANT" && php"$PHP_WANT" -r 'echo PHP_VERSION;' || echo 'not found')
MariaDB:         $(mariadb --version 2>/dev/null || echo 'not found')
Syncthing:       $SYNCTHING_RESULT
Moodle:          not installed (on purpose: Stage 2 on the desktop, Stage 3 on the laptop)
Caddy:           not touched
Live websites:   not touched
Apache:          not touched

Nothing else was changed. It is safe to run this script again at any time.
The next check is "am doctor", which compares this PC with the pins and
with the other PC.
SUMMARY
