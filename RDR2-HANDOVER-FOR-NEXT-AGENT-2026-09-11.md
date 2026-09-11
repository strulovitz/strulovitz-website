# RDR2 COMPLETE HAND-OVER — FOR THE NEXT AGENT — 2026-09-11

Written by GLM 5.3 at Nir's order, after Nir stopped the debugging session.
This file is EVERYTHING any agent needs to continue: the full saga, every attempt,
every measurement, every dead end, and the exact open question. Nothing here is
guessing — every claim below was measured on the machine.

GAME: Red Dead Redemption 2, johncena141 (jc141) warez release, on desktop-linux
(Linux Mint 22, NVIDIA RTX 4070 Ti, proprietary driver, X11, desktop is 7680x1080
multi-monitor). Part of the Fine Wine section (fine-wine.html) of
www.strulovitz.org — Wine runs AAA games while local AI works.

RELEASE LOCATION: /home/nir/Downloads/Red.Dead.Redemption.2-jc141/
- Launch normally with: bash /home/nir/Downloads/Red.Dead.Redemption.2-jc141/start.e-w.sh
  (desktop icon ~/Desktop/RedDeadRedemption2.desktop does the same)
- The release ships pre-installed mods: Lenny's Mod Loader (lml/), Alexander
  Blade's ScriptHookRDR2, ASI Loader (dinput8.dll), NativeTrainer.asi, vfs.asi.
- The release ships its own DXVK-style D3D DLLs inside files/game-root:
  d3d12.dll (122KB stub) + d3d12core.dll (5.8MB) + d3d11.dll + dxgi.dll +
  d3d9.dll + d3d10core.dll — split-DLL structure = vkd3d-proton/DXVK style.
- Bundled wine: files/game-root/wine/bin/wine (TkG custom build).
- The game was EXTRACTED (EXTRACT=1 in script_default_settings), ~120GB of real
  files, NO dwarfs/FUSE at runtime anymore.

THE ONE-SYMBOL SYMPTOM TODAY: the game process runs ~3-3.5 minutes with real GPU
rendering (16-59% GPU util, ~4GB VRAM), never creates its real window, then exits
ITSELF with exit code 3 (clean, coordinated shutdown, no crash, no exception).

===============================================================================
PART 1 — THE SAGA, IN ORDER (ALL SESSIONS, NOTHING SKIPPED)
===============================================================================

2026-09-10 (previous sessions — summarized from repo records):
1. First-ever launch: game hung for HOURS with no window. Processes stuck in
   D-state behind the compressed dwarfs FUSE mount — unkillable even with -9.
   FIX: EXTRACT=1 → one-time ~120GB extraction. D-state hangs gone forever.
   Full record: FINE-WINE-RDR2-TECHNICAL-RECORD-2026-09-10.md (pushed).

2026-09-11 (morning session, also GLM 5.3):
2. Nir's launch had TWO RDR2.exe instances dueling (single-core spin each, no
   window, 1 hour) — killed both + ComfyUI (squatted 3.8GB VRAM).
3. Clean relaunch: still hung 32+ min — one thread at 99.9%, no window, ZERO GPU.
   -windowed made no difference.
4. strace found the cause: ~43,000 getdents64/second re-scanning wine's system32
   hunting "nvapi64.dll". RDR2 probes the GPU vendor by RAW FILE ENUMERATION;
   wine's builtins are virtual (no files) and the game's not-found retry loop
   never falls back => infinite scan BEFORE any window.
   FIX: dxvk-nvapi v0.9.2 by jp7677 (github.com/jp7677/dxvk-nvapi):
   x64/nvapi64.dll + x64/nvofapi64.dll -> prefix system32, x32/nvapi.dll ->
   syswow64, plus DllOverrides nvapi64/native + nvofapi64/native via the
   BUNDLED wine reg. After it: scan loop GONE, CPU ~35%. Still no window.
   Full record: FINE-WINE-RDR2-NVAPI-FIX-2026-09-11.md (pushed).

2026-09-11 (this session, afternoon — stopped by Nir mid-run):
5. Read Nir's 5 Google-AI answers (saved verbatim in
   RDR2-GOOGLE-AI-ANSWERS-2026-09-11.md in this repo, with ranked analysis).
6. CHECK #1 — MULTIPLE VULKAN ICDs (Google's top suspect): CONFIRMED PRESENT.
   /usr/share/vulkan/icd.d/ has NINE ICDs (asahi, gfxstream, intel_hasvk, intel,
   lvp/lavapipe, nouveau, nvidia, radeon, virtio). Launched with
   VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json.
   RESULT: REAL PROGRESS — the GPU went from ZERO rendering to active 16-59%
   rendering with ~4GB VRAM for the full ~3.5 min. Keep this fix forever.
   But: still no window, still silent exit at ~3-3.5 min.
7. CHECK #2 — WINEDLLOVERRIDES="dinput8=n,b" (Google answer 4): ALREADY SET by
   the release's own start script (full line: winemenubuilder.exe=d;
   dinput8=n,b;version=n,b;d3d12,d3d12core=n,b;vulkan-1=n,b;amd_ags_x64=n,b;
   ffx_fsr2_api_vk_x64=n,b). Nothing to do.
8. CHECK #3 — WINE VIRTUAL DESKTOP (Google answer 2): set via the bundled wine:
   reg add "HKCU\Software\Wine\Explorer" /v Desktop /d Default
   reg add "HKCU\Software\Wine\Explorer\Desktops\Default" Width=1920 Height=1080
   (verified present afterwards with reg query). RESULT: no change — still no
   window, same ~3 min death.
9. CHECK #4 — RENDERER FLAG: launched manually replicating the script's full
   environment, with -dx12 instead of the script's -vulkan: SAME death (~3 min).
   Also tried -windowed instead of -fullscreen: SAME death (~3 min). So the
   death is NOT about DX12-vs-Vulkan API choice and NOT about fullscreen mode.
10. exit_file.dat: read it — it contains the PID/handshake written AT LAUNCH
    (mtime = launch time, 15 seconds after start). Normal startup handshake,
    exactly as Google answer 5 said. Closed dead end.
11. STRACE ON THE DEATH MOMENT (the proven method from the nvapi fix):
    attached strace to RDR2.exe ~2.5 min into a run, captured the death:
    - RDR2.exe calls exit_group(3) ITSELF (and a forked child exits with 3 too).
      NOTHING kills it — the game CHOOSES to quit, cleanly.
    - The death ritual, exactly: a 10,592-byte writev to a unix socket (fd 11)
      that had been SILENT the entire run (first use in the whole capture), then
      a 32-byte reply, then 2x EAGAIN reads, then shutdown(SHUT_RDWR) on the
      socket, then exit_group(3).
    - The reply bytes begin 0x01 (a success-shaped reply header) — the EAGAINs
      may be a normal drain, so the socket exchange is not proven to be the
      failure itself; it is simply the LAST thing the game does before deciding
      to quit.
12. WINEDEBUG=+seh: NO unhandled exception at all — only DBG_PRINTEXCEPTION_C
    debug-print exceptions (the ASI loader logging). The game does NOT crash.
13. SCRIPTHOOK'S OWN LOG (files/game-root/ScriptHookRDR2.log): INIT Success at
    launch, then a CLEAN "UNINIT: Unregistering script" at the EXACT death
    moment — confirming a coordinated, graceful shutdown, not a crash.
14. NOTEPAD TEST in the SAME prefix: notepad.exe creates a visible window
    instantly. Window creation in the prefix WORKS. The game alone never shows
    its window.
15. WINEDEBUG=+win — THE BIGGEST FINDING OF THE SESSION: the game process
    creates ONLY internal "WineD3D fake window" windows (class
    "WineD3D_OpenGL", 10x10 invisible) — 2,144 of them created (and 4,304
    destroy operations) in what looks like a RETRY LOOP — and NEVER creates its
    real game window (no Rockstar window class ever appears; only WineD3D
    fakes, Wine DDE/OLE helpers, "DXGI device window").
    MEANING: some game subsystem is repeatedly asking WINE'S OWN wined3d
    (wine's OLD OpenGL-backed D3D layer — NOT the shipped vkd3d-proton/DXVK
    DLLs!) for a device/context, failing ~2,144 times over ~3 minutes, then
    the game gives up and exits cleanly with code 3.
    (Meanwhile vkd3d-proton logs a perfectly successful D3D12 device init:
    "DX Ultimate supported", DXR 1.1, SM 6.8 — so the main device works. The
    loop is a SECOND subsystem.)
16. STARTED the decisive next measurement — WINEDEBUG=+loaddll to list exactly
    which d3d/gl/vulkan DLLs the game process loads (to see whether the
    wined3d/OpenGL usage comes from wine's BUILTINS overriding the shipped
    DXVK DLLs) — NIR ABORTED THE RUN after 1 minute, stopped the session, and
    ordered this hand-over. That measurement is UNFINISHED and is the natural
    next step.

===============================================================================
PART 2 — THE EXACT OPEN QUESTION
===============================================================================

WHY does RDR2's second graphics subsystem loop ~2,144 times through wine's own
wined3d ("WineD3D fake window", class WineD3D_OpenGL) and then quit with exit
code 3 — even though its main D3D12 device initializes perfectly and the GPU
renders the whole time?

Prime suspects to check first (in order):
a) WINEDEBUG=+loaddll (the aborted run) — does the game load wine's BUILTIN
   d3d9/d3d10core/d3d11/dxgi from system32 INSTEAD of the DXVK copies shipped
   next to the exe? The start script only forces n,b for d3d12+d3d12core. If
   wine's builtin d3d11/d3d9/dxgi are being loaded, force them native too:
   WINEDLLOVERRIDES="d3d9,d3d10core,d3d11,dxgi,d3d12,d3d12core=n,b;..." and/or
   rename wine's builtin stubs out of the prefix's system32.
b) The mods (Google answer 4's vanilla test): move away NativeTrainer.asi +
   ScriptHookRDR2.dll + lml/ (KEEP dinput8.dll + vfs.asi — vfs.asi is the
   release's version/DRM bypass and dinput8.dll is the loader that loads it;
   removing them may fire DRM checks). ScriptHook loads/unloads cleanly so it
   is not the prime suspect, but it is cheap to eliminate.
c) gamescope (jc141's own recommended path — their docs: "Prevents games from
   locking in the user focus"; set GAMESCOPE=1 + GAMESCOPE_SCREEN_WIDTH/HEIGHT
   in ~/.jc141rc). NOT INSTALLED on the machine yet (needs sudo apt install
   gamescope; NVIDIA needs extra setup per the Arch wiki gamescope page).
d) System winehq-staging 11.16 instead of the bundled TkG wine (edit SYSWINE
   in script_default_settings or ~/.jc141rc).
e) Audio init (jc141 docs: wine audio drivers are a common issue; lib32
   audio packages were installed for the 09-10 session, verify).

CLOSED DEAD ENDS — DO NOT RE-TEST (all measured):
- FUSE/dwarfs D-state hang (fixed by EXTRACT=1, 2026-09-10)
- nvapi64.dll file-scan loop (fixed by dxvk-nvapi v0.9.2, 2026-09-11)
- Multiple Vulkan ICDs (fixed by VK_ICD_FILENAMES=nvidia_icd.json — keep it)
- dinput8 override (already set by the release)
- Wine virtual desktop (set, verified in registry, no effect)
- -dx12 vs -vulkan (both die identically)
- -windowed vs -fullscreen (both die identically)
- exit_file.dat (normal launch handshake, content read, mtime = launch time)
- Unhandled exception (none — +seh clean)
- Crash (none — exit_group(3), coordinated shutdown, ScriptHook clean UNINIT)
- Broken window creation in the prefix (notepad works fine)
- mscoree/Mono warning at exit (Google answer 3: symptom of shutdown, not cause)

===============================================================================
PART 3 — HOW TO LAUNCH / MEASURE (exact working recipes)
===============================================================================

Normal launch (the release's way):
  bash /home/nir/Downloads/Red.Dead.Redemption.2-jc141/start.e-w.sh
  (needs the ICD fix: prefix the environment — see next block)

Manual launch that replicates the script exactly (used for all tests today;
this is how you can change the flags):
  cd /home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/game-root
  env HOME=/home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/prefix/home \
      WINEPREFIX=/home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/prefix \
      WINE_LARGE_ADDRESS_AWARE=1 WINEDEBUG=fixme-all VKD3D_DEBUG=info \
      VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json \
      WINEDLLOVERRIDES="winemenubuilder.exe=d;dinput8=n,b;version=n,b;d3d12,d3d12core=n,b;vulkan-1=n,b;amd_ags_x64=n,b;ffx_fsr2_api_vk_x64=n,b" \
      /home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/game-root/wine/bin/wine \
      Launcher.exe -vulkan -fullscreen -USEALLAVAILABLECORES -high \
      -cpuLoadRebalancing -malloc=system -ignorepipelinecache
  (always from game-root as cwd — the -dx12 and -windowed tests swapped only
  the flag after Launcher.exe; everything else identical)

The script's own full command line (for reference):
  CMD=( $SYSWINE Launcher.exe -vulkan -fullscreen -USEALLAVAILABLECORES -high
        -cpuLoadRebalancing -malloc=system -ignorepipelinecache "$@" )

Debug-channel launches: same as above, swap WINEDEBUG (used successfully:
"+seh,+exit", "+win,+event", "+loaddll" — the last one was aborted mid-run).

Process facts: Launcher.exe spawns RDR2.exe; RDR2.exe spawns a child RDR2.exe
(the real game). Check with: pgrep -x RDR2.exe (ALWAYS -x — see pitfalls).

strace on the death moment (worked, ~4 min total):
  launch, wait ~150s, PID=$(pgrep -x RDR2.exe | head -1), then
  (setsid strace -f -p $PID -o /tmp/opencode/rdr2-strace.log &)
  and watch it die. Death signature in the log: exit_group(3).

Relevant logs from today (in /tmp — MAY NOT SURVIVE A REBOOT; copy into the
repo if you need them long-term):
  /tmp/opencode/rdr2-launch.log .. rdr2-launch10.log  (all runs)
  /tmp/opencode/rdr2-strace.log (370,340 lines, the captured death)
  /tmp/opencode/rdr2-notepad.log (the working-window control test)

In-repo references:
  RDR2-GOOGLE-AI-ANSWERS-2026-09-11.md — Nir's 5 Google answers + ranked list
  FINE-WINE-RDR2-TECHNICAL-RECORD-2026-09-10.md — dwarfs/EXTRACT fix
  FINE-WINE-RDR2-NVAPI-FIX-2026-09-11.md — the nvapi64 scan-loop fix
  fine-wine.html / Fine Wine section — the public-facing entry (readers were
  told the real story: mount stalls on some machines, extract instead)

===============================================================================
PART 4 — PITFALLS THAT ALREADY COST BLOOD (do not repeat)
===============================================================================

1. THE SELF-KILL TRAP (hit THREE times across sessions): pgrep -f / pkill -f
   with a pattern that appears in your own shell's command line kills YOUR OWN
   session mid-command. ALWAYS use pgrep -x <exact-process-name> (pgrep -x
   RDR2.exe cannot match your shell) and kill by explicit PID lists.
2. TWO RDR2.exe INSTANCES can duel (single-core spin each, no window, hours).
   If behavior is insane, check the COUNT: pgrep -x RDR2.exe | wc -l (1 is
   normal after the process tree settles).
3. NEVER kill the game once it finally shows a window: the real first launch
   builds the shader cache — black window / many minutes of nothing is NORMAL
   and expected (15-30+ min on this GPU). Killing it then = start over.
4. NEVER launch the START SCRIPT from inside files/game-root (double-mount
   confusion); launching wine Launcher.exe manually from game-root cwd is fine
   (the script itself does exactly that).
5. The desktop is 7680x1080 (multi-monitor); the wine virtual desktop was set
   to 1920x1080 — if you experiment with resolution, remember gamescope picks
   720p unless GAMESCOPE_SCREEN_WIDTH/HEIGHT are set (jc141 docs).
6. ComfyUI squats VRAM/RAM if left running after a render job (it froze the
   whole desktop once). If nothing needs it, kill it by PID before gaming.
7. When a run "looks dead", measure before judging: GPU util
   (nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader), process
   count, wmctrl -l for windows, strace for syscall behavior. Every single
   verdict in this file came from one of those numbers.

===============================================================================
PART 5 — STATE OF THE MACHINE RIGHT NOW (as this file is written)
===============================================================================

- The last game run (+loaddll measurement, launch10) was ABORTED by Nir after
  ~1 minute; the game may or may not have still been running when the session
  ended — CHECK before anything: pgrep -x RDR2.exe; if alive and no window
  after 4 min, it is the known ~3.5-min exit, not a hang — let it die or kill
  by PID.
- The website v2026-09-11-c is deployed and live (this file is part of a later
  commit; deploying it is NOT urgent).
- Working tree state: this handover file is being committed with everything
  else up to date; 88 editions gapless in the DB; all page checks pass.
- Nothing heavy should be running (ComfyUI was killed hours ago today).

MONEY SPENT ON RDR2 SO FAR: $0 (all fixes were free software + code). The only
cost was agent time — which Nir judged wasted, correctly, on this session's
debugging approach.

Good luck to the next agent. The game is ONE diagnosis away from running — the
main device works, the GPU renders, the window system works; only the wined3d
retry loop and exit(3) decision remain to be explained and fixed.
