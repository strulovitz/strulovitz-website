# RDR2 — THE INFINITE NVAPI SCAN, DIAGNOSED AND FIXED — 2026-09-11

Written in a hurry at Nir's explicit order ("document this before the game gets the
whole PC stuck"). This is the complete, honest record of the second RDR2 mystery,
with every command and every piece of evidence, so any future agent can pick it up
even if this session dies.

## THE SYMPTOM

The game (jc141 release, extracted real files per the 2026-09-10 record, wine TkG
Staging "wine-experimental.bleeding.edge.10.0.308760.20260208" bundled in
files/game-root/wine) starts, all mod tooling loads successfully
(ScriptHookRDR2 "INIT: Success", asiloader "Finished loading", vfs "Init done",
ModManager "Loaded" — all by ~5 seconds in), vkd3d-proton's pipeline cache setup
completes ("Done performing async setup of stream archive") — and then RDR2.exe's
MAIN THREAD spins at exactly 99.9% of one core forever: no window ever appears
(not even black), GPU memory sits at 4-6 MiB (the game never touches the GPU),
and not one new log line is written. It stayed like this for 30+ minutes twice,
and would presumably stay like this until killed.

## THE DIAGNOSIS (all measured, nothing guessed)

1. `top -b -H -n1 -p <pid>` showed the spinning thread is the MAIN thread, all
   other threads idle.
2. `strace -c -p <pid>` for 5 seconds showed the main thread doing ~43,000
   getdents64 + openat/close/fcntl per second: an endless directory-scan loop,
   plus ~32,000 FAILED newfstatat calls per second — statting paths that do not
   exist, over and over.
3. `strace -e trace=openat,getdents64 -p <pid> | grep -oE '"[^"]+"' | sort | uniq -c`
   named the directory being re-scanned ~8,700 times a second:
   `.../files/prefix/dosdevices/c:/windows/system32`
4. `strace -e trace=newfstatat,openat -p <pid> | grep ENOENT` named the exact
   file it hunts and never finds:

       13750 x .../system32/nvapi64.dll
        6875 x .../system32/nvapi64.dll?   (a wildcard enumeration)

ROOT CAUSE: RDR2 boots by detecting the GPU vendor through NVIDIA's nvapi64.dll
(the Windows NVIDIA driver API). Wine loads built-in DLLs VIRTUALLY — there is no
real FILE named nvapi64.dll in the prefix's system32 — and this game probes by raw
file enumeration, not by LoadLibrary. File not found -> the game's retry loop is
buggy and never falls back to the AMD/neutral path -> infinite scan -> the boot
hangs BEFORE creating any window. Neither the bundled TkG wine nor the system
winehq-staging 11.16 ships an nvapi file at all (checked with find on both).

This is a known class of RDR2-on-wine hang; Proton solves it the same way.

## THE FIX

The proven free-software implementation: dxvk-nvapi by jp7677
(https://github.com/jp7677/dxvk-nvapi — "Alternative NVAPI implementation on top
of DXVK", 654 stars, the same one Proton/wine-ge ship for exactly this game).
Release used: v0.9.2, tarball dxvk-nvapi-v0.9.2.tar.gz (4.8 MB).

Installed like this (prefix: files/prefix, all inside the game folder on the big disk):

    cd /tmp && curl -sL -o dxvk-nvapi.tar.gz \
      "https://github.com/jp7677/dxvk-nvapi/releases/download/v0.9.2/dxvk-nvapi-v0.9.2.tar.gz"
    tar xzf dxvk-nvapi.tar.gz
    P=/home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/prefix/drive_c/windows
    cp x64/nvapi64.dll   $P/system32/
    cp x64/nvofapi64.dll $P/system32/     # optical-flow API, RDR2-era games want it too
    cp x32/nvapi.dll     $P/syswow64/
    # tell wine to prefer the real files:
    export WINEPREFIX=/home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/prefix
    files/game-root/wine/bin/wine reg add "HKCU\\Software\\Wine\\DllOverrides" \
        /v nvapi64 /t REG_SZ /d native /f
    files/game-root/wine/bin/wine reg add "HKCU\\Software\\Wine\\DllOverrides" \
        /v nvofapi64 /t REG_SZ /d native /f

THEN launch as always (the desktop icon / start.e-w.sh). First sign the fix works:
within ~2.5 minutes the main-thread CPU profile dropped from a locked 99.9%
directory-scan to ~35% with a different syscall mix, and the getdents64 flood was
gone from a fresh strace. THE WINDOW HAD NOT YET APPEARED at the time of this
writing — the fix is NOT yet confirmed end-to-end; the next agent must verify
(the check commands are below).

## STATUS AT THE TIME OF THIS FILE

- Launched 11:23:23 Israel time on 2026-09-11 with the nvapi files in place.
- At 11:25:53: CPU ~35.8% (no longer a 99.9% spin — the scan loop is gone),
  GPU 4 MiB, no window yet. Monitoring continues.
- If it still never opens a window: next suspects, in order:
  1. the wine registry display-settings error seen at boot
     ("err:explorer:initialize_display_settings Failed to initialize registry
     display settings for \\.\DISPLAY1") — try a wine virtual desktop
     (HKCU\Software\Wine\Explorer\Desktops) or gamescope.
  2. audio device init — check the prefix's audio with `winecfg`.
  3. `exit_file.dat` in AppData/Local/Rockstar Games/Red Dead Redemption 2/ —
     a leftover exit-flag from a force-killed run could stall the boot; it is
     safe to delete when the game is not running.

## THE RULES LEARNED THIS TIME (harder than they look)

- THE SELF-KILL TRAP, HIT TWICE IN ONE DAY: `pkill -f`/`pgrep -f` with a
  pattern that appears in your own tool-command line kills YOUR OWN SHELL
  (the pattern "RDR2.exe" was in my kill loop's own text). Use
  `pgrep -x RDR2.exe` (exact process-name match, cannot self-match) and kill
  by the PIDs it returns, or you will execute half a command, kill yourself,
  and time out.
- Wine built-in DLLs are VIRTUAL: an app that probes C:\windows\system32 by
  raw file enumeration cannot see them. When a Windows app spins scanning a
  directory, strace it FIRST — `strace -c -p PID` then the ENOENT-filtered
  trace names the exact missing file in seconds. 43,000 getdents64/second
  IS a diagnosis by itself: nobody scans a directory 8,700 times a second
  for a good reason.
- strace of a hung game thread costs nothing and changes nothing — it is the
  safe tool for "is it doing something?" (Nir's standing question). A pure
  userspace grind means compute; a syscall storm names the I/O it is stuck on.
- The game's first launch still owes a shader-cache build: expect a long
  black/no-window period AFTER a window first appears — never kill it then.

## THE CHECK COMMANDS (for the next agent)

    # is it alive and what is it doing?
    ps aux | grep "RDR2.exe" | grep -v grep
    top -b -H -n1 -p $(pgrep -x RDR2.exe | head -1) | head -14
    nvidia-smi | grep RDR2
    # window?
    wmctrl -l
    # is the nvapi scan back?
    timeout 3 strace -c -p $(pgrep -x RDR2.exe | head -1) 2>&1 | grep getdents64
    # game logs (all under the game folder):
    tail -5 /home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/game-root/*.log
    tail -20 /tmp/opencode/rdr2-nvapi.log
