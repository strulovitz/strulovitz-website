#!/usr/bin/env bash
# READ-ONLY SURVEY of THIS PC -- Part 01, section 1.5.
#
# Run it on the PC being surveyed, as the normal user, with no sudo:
#     bash attract-mode/machines/laptop-survey.sh
# Then copy everything it printed and give it back to the agent, which writes
# attract-mode/machines/<pc>.md from it.
#
# It installs nothing, changes nothing, asks for no password, and prints
# NO address, no token and no password: only port numbers, program names and
# version lines.
set -u

say() { printf '%s\n' "$*"; }
hdr() { printf '\n== %s ==\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

[ -r /etc/os-release ] && . /etc/os-release

hdr "1. THIS PC"
say "name:     $(hostname)"
say "system:   ${PRETTY_NAME:-unknown} (ID ${ID:-?} ${VERSION_ID:-?})"
say "kernel:   $(uname -r)"
say "user:     $(id -un)"
df -Pk / 2>/dev/null | awk 'NR==2 {printf "disk /:    %.1f GB free of %.1f GB (%s)\n", $4/1048576, $2/1048576, $5}'
df -Pk "$HOME" 2>/dev/null | awk 'NR==2 {printf "disk home: %.1f GB free of %.1f GB (%s)\n", $4/1048576, $2/1048576, $5}'

hdr "2. PROGRAMS AND VERSIONS"
ver() {
    name="$1"; shift
    if ! have "$1"; then say "$(printf '%-13s' "$name") NOT installed"; return; fi
    first="$("$@" 2>&1 | head -1)"
    say "$(printf '%-13s' "$name") $first"
}
ver git         git --version
ver caddy       caddy version
ver cloudflared cloudflared --version
ver php         php --version
ver mariadb     mariadb --version
ver syncthing   syncthing --version
ver uv          uv --version
ver python3     python3 --version
ver ffmpeg      ffmpeg -version
ver latex       latex --version
ver obsidian    obsidian --version
if ! have obsidian; then
    found=$(ls -d "$HOME"/Applications/*[Oo]bsidian* /opt/*[Oo]bsidian* "$HOME"/.local/bin/*[Oo]bsidian* 2>/dev/null | head -1)
    [ -n "$found" ] && say "$(printf '%-13s' obsidian) installed outside PATH"
fi

hdr "3. PORTS"
for p in 8081 8082 8083 8084 3306 8384 22 80 443; do
    if ss -ltnH 2>/dev/null | awk '{print $4}' | grep -q ":$p\$"; then say "port $p: LISTENING"; else say "port $p: free"; fi
done
say "8084 free (Part 01, 1.4 asks): $(ss -ltnH 2>/dev/null | awk '{print $4}' | grep -q ':8084$' && echo 'NO - something is using it' || echo yes)"
say "all listening ports, numbers only: $(ss -ltnH 2>/dev/null | awk '{print $4}' | sed 's/.*://' | sort -n -u | tr '\n' ' ')"

hdr "4. WHAT IS RUNNING: WEB SERVER, PHP, DATABASE"
running=$(ps -eo comm= 2>/dev/null | sort -u | grep -E '^(php|php[0-9.]+|php-fpm[0-9.]*|mariadbd|mysqld|apache2|httpd|nginx|caddy|cloudflared|syncthing)$' | tr '\n' ' ')
say "processes: ${running:-none of them}"
for s in apache2 httpd nginx mariadb mysql php8.3-fpm php8.4-fpm caddy; do
    st=$(systemctl is-active "$s" 2>/dev/null || true)
    [ -n "$st" ] && [ "$st" != "inactive" ] && [ "$st" != "unknown" ] && say "service $s: $st"
done
say "(Apache is NOT ours: Part 01, 1.8. Never touch it.)"

hdr "5. THE TUNNEL"
if [ -f "$HOME/.cloudflared/config.yml" ]; then
    n=$(grep -c 'hostname:' "$HOME/.cloudflared/config.yml" 2>/dev/null || echo 0)
    say "local file: yes, with $n hostname entries (contents NOT printed)"
else
    say "local file: none found (the tunnel may be managed at Cloudflare instead)"
fi
st=$(systemctl --user is-active site-tunnel 2>/dev/null || true)
say "site-tunnel service: ${st:-not present}"

hdr "6. WHAT 'WEBSITES ON' TOUCHES"
if [ -r hosting/bin/sites-on ]; then
    say "services it names: $(grep -oE 'site-[a-z-]+\.service' hosting/bin/sites-on | sort -u | tr '\n' ' ')"
    say "lines in the script: $(wc -l < hosting/bin/sites-on)"
else
    say "hosting/bin/sites-on not found here"
fi

hdr "7. WOULD A CHANGE UNDER attract-mode/ REBUILD THE AI PANORAMA EXPORT?"
hits=$(grep -rl "attract-mode" ops 2>/dev/null | head -5 | tr '\n' ' ')
say "files under ops/ that mention attract-mode: ${hits:-none}"
say "user timers: $(systemctl --user list-timers --all --no-pager 2>/dev/null | sed -n '2,4p' | awk '{print $NF}' | tr '\n' ' ')"

hdr "8. STUDIOS PRESENT (names only)"
for d in "$HOME/Apps" "$HOME/pinokio" "$HOME/ai-art" "$HOME/.unsloth" "$HOME/drama3" "$HOME/ComfyUI"; do
    [ -d "$d" ] && say "$(basename "$d")/: $(ls -1 "$d" 2>/dev/null | head -8 | tr '\n' ' ')"
done
say "desktop icons with start/stop: $(ls -1 "$HOME/Desktop" 2>/dev/null | grep -icE 'start|stop|launch')"

hdr "END OF SURVEY"
say "Copy everything above and give it back. Nothing was changed."
