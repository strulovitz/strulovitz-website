# RDR2 COMPLETE HAND-OVER — FOR THE NEXT AGENT — 2026-09-11

Rewritten in plain words at Nir's order. No unexplained jargon. Every folder
named. Written by GLM 5.3; the debugging was handed over by Nir to a new agent.

===============================================================================
PART 0 — WHERE EVERYTHING IS (folders, files, how to start the game)
===============================================================================

THE GAME IN ONE LINE: Red Dead Redemption 2, downloaded release by "johncena141"
(jc141), running on Nir's desktop PC (Linux Mint 22, NVIDIA RTX 4070 Ti, real
NVIDIA driver, three-monitor desktop, total width 7680x1080).

MAIN FOLDER OF THE GAME:
  /home/nir/Downloads/Red.Dead.Redemption.2-jc141/

Inside that folder:
  start.e-w.sh              <- THE launcher script. Starting the game = running
                              this. (Desktop icon does the same.)
  script_default_settings   <- per-game settings file. Important line inside:
                              EXTRACT=1 (see "the story", step 1).
  ~/.jc141rc                <- global settings for all jc141 games (in Nir's
                              home folder). Network-blocking and sandbox are
                              OFF; wine = system wine by default, but the
                              game's own settings file overrides it.
  readme.txt                <- short: the game is moddable, mods are included.
  documentation/            <- the RELEASE'S OWN help texts:
       setup-guide.txt      <- their install/setup guide (packages, gamescope,
                               gstreamer for movies, etc.)
       scripts.and.configs.txt <- explains every setting of the start scripts.

THE ACTUAL GAME FILES (unpacked, ~120 GB of real files):
  /home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/game-root/
  Inside game-root live: Launcher.exe, RDR2.exe, the game's own graphics files
  (d3d12.dll, d3d12core.dll, d3d11.dll, dxgi.dll, d3d9.dll, d3d10core.dll),
  the mods (dinput8.dll, NativeTrainer.asi, ScriptHookRDR2.dll, vfs.asi, lml/
  folder), and ALSO the game's own private copy of wine (see next).

THE WINDOWS-EMULATOR (wine) THAT RUNS THE GAME:
  /home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/game-root/wine/bin/wine
  (a custom "wine-tkg" build that came bundled inside the release)

THE GAME'S PRIVATE FAKE C: DRIVE (called the "wine prefix"):
  /home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/prefix/
  This is the game's own little Windows world: fake C:\, fake registry, fake
  user folders. The game can't see Nir's real files, only this.

HOW NIR NORMALLY STARTS THE GAME:
  the desktop icon "Red Dead Redemption 2" (= runs start.e-w.sh)

WHERE OUR OWN DOCUMENTATION LIVES (this repo, all pushed):
  FINE-WINE-RDR2-TECHNICAL-RECORD-2026-09-10.md  (the extraction fix)
  FINE-WINE-RDR2-NVAPI-FIX-2026-09-11.md         (the NVIDIA-file fix)
  RDR2-GOOGLE-AI-ANSWERS-2026-09-11.md           (Nir's 5 Google answers + ranks)
  fine-wine.html                                  (the public page about it)

WHERE TODAY'S TEST LOGS ARE (TEMPORARY — deleted on reboot!):
  /tmp/opencode/rdr2-launch.log ... rdr2-launch10.log   (each test run)
  /tmp/opencode/rdr2-strace.log                        (the captured death, big)
  Copy them into the repo if you want them to survive.

===============================================================================
PART 1 — THE STORY SO FAR, IN PLAIN WORDS, IN ORDER
===============================================================================

WHAT THE GAME IS: it came as one giant compressed file. The release's script
"mounts" it like a virtual disk when you press play.

STEP 1 (2026-09-10) — THE GAME FROZE THE COMPUTER-SIDE, UNKILLABLE.
  First launch: no window for hours, and the game's processes got stuck in
  what Linux calls "D-state" — that means a program is frozen forever waiting
  on a broken virtual disk, and even "kill -9" cannot end it. The broken part
  was the compression-mounting software (dwarfs + fuse).
  FIX THAT WORKED: we set EXTRACT=1 in script_default_settings. On the next
  launch the release unpacked the whole ~120 GB into REAL files (that's why
  files/game-root is huge now). No virtual disk at runtime anymore, the
  freeze-forever problem is gone permanently.

STEP 2 (2026-09-11 morning) — THE GAME SPUN AT 100% CPU, NO WINDOW, NO GPU.
  Two game processes were fighting each other (killed both), and even a clean
  start just spun one thread at 100% forever.
  CAUSE FOUND BY MEASUREMENT (strace = a tool that records every file/request a
  program makes): the game was re-scanning its fake C:\ drive ~43,000 times
  PER SECOND, forever, looking for a file called "nvapi64.dll" — that's an
  NVIDIA driver file. The game checks "is this an NVIDIA computer?" by looking
  for that FILE, wine (the Windows emulator) normally has no such file, and
  the game's search loop never gives up.
  FIX THAT WORKED: we put real nvapi files into the game's fake C: drive
  (downloaded from github.com/jp7677/dxvk-nvapi, version 0.9.2 — the same
  thing Steam's Proton uses). The 100% CPU spin stopped. CPU dropped to ~35%.

STEP 3 (2026-09-11, this session) — THE GAME RUNS 3.5 MINUTES, THEN QUITS
  BY ITSELF. STILL NO WINDOW EVER. This is the current, unsolved problem.

  3a. NINE GRAPHICS DRIVERS. Linux keeps a folder of graphics drivers
      (/usr/share/vulkan/icd.d/). This PC had NINE listed — the real NVIDIA
      one plus eight others (fake software ones, nouveau, intel, virtio...).
      Google's answer (saved in RDR2-GOOGLE-AI-ANSWERS file) said: too many
      drivers can make the game pick a wrong path and give up silently.
      FIX THAT HELPED (real progress!): we launch the game with a line that
      says "only show the game the NVIDIA driver". Result: the GPU went from
      doing NOTHING to actively rendering the whole time (16-59% GPU use,
      4 GB of GPU memory) for the first time ever. KEEP THIS FIX FOREVER.
      ...but the game still never opens a window and still quits after
      ~3-3.5 minutes.

  3b. THINGS WE TESTED THAT CHANGED NOTHING (all measured, do not re-test):
      - a fake "second desktop inside the desktop" for the game (wine virtual
        desktop, set to 1920x1080) — no change
      - starting the game with the DX12 graphics mode instead of Vulkan —
        same death
      - starting the game in windowed mode instead of fullscreen — same death
      - the file exit_file.dat in the game's fake AppData — it is a normal
        "I started" note written at launch, not a cause (Google said so, we
        read the file and its timestamps confirmed it)
      - the "Mono runtime" warning at the end of the log — a symptom of the
        game closing, not a cause (Google answer 3)

  3c. WHAT THE DEATH ACTUALLY LOOKS LIKE (measured, not guessed):
      - The game does NOT crash. It quits POLITELY, by its own decision,
        with "exit code 3" (its own "I give up" signal). No error, no crash
        dump, no exception anywhere (checked with wine's exception log).
      - Even the mod (ScriptHook) says goodbye cleanly at the exact second
        the game quits — the game tells everything to shut down and leaves.
      - The last thing the game does before quitting: sends one ~10 KB
        message to a connection it had opened at the start and never used
        all game long, gets a short reply, then closes the connection and
        quits. (Captured with strace.)
      - Notepad (a trivial Windows app) opens a window INSTANTLY in the same
        game environment — so windows CAN be made; the game alone refuses.

  3d. THE BIGGEST DISCOVERY (the clue for whoever continues):
      With wine's window-logging turned on, we saw that the game NEVER even
      TRIES to open its real window. Instead, it creates and destroys a tiny
      invisible helper window ~2,144 TIMES in a loop, over the whole ~3
      minutes, then quits. Those helper windows belong to wine's OLD
      built-in graphics library (called "wined3d", backed by OpenGL) — NOT
      the modern translation layer the game is supposed to use (the
      vkd3d-proton/DXVK files that sit next to the game's exe, which DO
      initialize perfectly: the log shows the graphics device coming up with
      every modern feature).
      IN PLAIN WORDS: the game's main graphics engine works fine, but some
      second part of the game keeps asking wine's oldest, wrong graphics
      library over and over, ~2,144 times, gets nowhere, and after ~3
      minutes the game says "forget it", closes everything politely, and
      quits with code 3. NOBODY has yet answered WHY that second part asks
      the wrong library.

  3e. WHERE WE STOPPED: the very next measurement (a log listing exactly
      which graphics library files the game loads — to see whether the
      game is accidentally loading wine's built-in old ones instead of the
      modern files that sit right next to the game's exe) was STARTED and
      ABORTED after one minute when Nir stopped the session. It is the
      natural first step for the next agent. Recipe below.

===============================================================================
PART 2 — WHAT THE NEXT AGENT SHOULD TRY, IN ORDER
===============================================================================

1. THE ABORTED MEASUREMENT (start here): run the game with
   WINEDEBUG=+loaddll (recipe in Part 3) and read which d3d/dxgi/opengl files
   get loaded and from WHERE. If wine's built-in old graphics files load
   instead of the modern ones sitting next to the game exe, force the modern
   ones with the dll-overrides line (recipe below).

2. THE VANILLA TEST (Google answer 4, cheap): the release ships with mods
   pre-installed (Lenny's Mod Loader + ScriptHook + NativeTrainer). Temporarily
   move away: NativeTrainer.asi, ScriptHookRDR2.dll, and the lml folder.
   KEEP dinput8.dll and vfs.asi — vfs.asi is what bypasses the game's DRM and
   dinput8.dll is what loads it; removing THOSE may make the game refuse to
   start at all. (ScriptHook loads and unloads cleanly, so it is probably
   innocent — but this test is cheap and eliminates it.)

3. GAMESCOPE (the release's own recommendation, never tried yet): a wrapper
   that gives the game its own private screen so it always gets focus. Their
   own docs say it "prevents games from locking in user focus". Not installed
   on this PC yet (needs: sudo apt install gamescope, plus extra NVIDIA
   setup; and in ~/.jc141rc set GAMESCOPE=1 and GAMESCOPE_SCREEN_WIDTH=1920
   GAMESCOPE_SCREEN_HEIGHT=1080, otherwise it defaults to 720p).

4. SYSTEM WINE INSTEAD OF THE BUNDLED WINE: the release bundles its own
   custom wine (inside files/game-root/wine), and the system also has
   winehq-staging 11.16 installed. Swapping is one line: point SYSWINE in
   script_default_settings to "$(command -v wine)".

5. AUDIO: the release's docs warn that wine audio problems break many games;
   the 32-bit audio packages were installed once for this, worth verifying
   if nothing else pans out.

CLOSED DEAD ENDS — DO NOT RE-TEST (all already measured):
  the compressed-disk freeze (fixed by unpacking, step 1);
  the endless NVIDIA-file search (fixed by real nvapi files, step 2);
  the nine-drivers problem (fixed by "NVIDIA only" line — keep it);
  dinput8 override (already set by the release itself);
  wine virtual desktop (set, verified, no effect);
  DX12-vs-Vulkan flag (both identical);
  windowed-vs-fullscreen (both identical);
  exit_file.dat (normal startup note);
  Mono warning (symptom, not cause);
  "maybe windows can't be created" (notepad opens one instantly);
  "maybe it's a crash" (it is a clean, polite self-quit, exit code 3).

===============================================================================
PART 3 — EXACT RECIPES (copy-paste, all used successfully today)
===============================================================================

NORMAL LAUNCH (with the NVIDIA-only fix that must be kept):
  VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json \
  bash /home/nir/Downloads/Red.Dead.Redemption.2-jc141/start.e-w.sh

MANUAL LAUNCH that copies everything the script does (use this to change
flags — this exact form worked all day today):
  cd /home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/game-root
  env HOME=/home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/prefix/home \
      WINEPREFIX=/home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/prefix \
      WINE_LARGE_ADDRESS_AWARE=1 WINEDEBUG=fixme-all VKD3D_DEBUG=info \
      VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json \
      WINEDLLOVERRIDES="winemenubuilder.exe=d;dinput8=n,b;version=n,b;d3d12,d3d12core=n,b;vulkan-1=n,b;amd_ages_x64=n,b" \
      /home/nir/Downloads/Red.Dead.Redemption.2-jc141/files/game-root/wine/bin/wine \
      Launcher.exe -vulkan -fullscreen -USEALLAVAILABLECORES -high \
      -cpuLoadRebalancing -malloc=system -ignorepipelinecache
  (to change graphics mode: swap -vulkan for -dx12; windowed: swap -fullscreen
  for -windowed — both were tested, same result)

THE FULL OVERRIDE LINE THE SCRIPT USES (for reference, already correct):
  winemenubuilder.exe=d;dinput8=n,b;version=n,b;d3d12,d3d12core=n,b;vulkan-1=n,b;amd_ags_x64=n,b;ffx_fsr2_api_vk_x64=n,b
  (candidate addition from suspect 1: put d3d9,d3d10core,d3d11,dxgi in front of
  =n,b too — but ONLY after the +loaddll log proves which files load)

DEBUG LOGGING (swap into WINEDEBUG in the manual launch):
  "+loaddll"     -> lists every dll loaded, with full path (THE NEXT STEP)
  "+win"         -> every window created/destroyed (found the 2,144 loop)
  "+seh"         -> every exception (proved: none)

WATCHING A RUN (30-second heartbeat used all day):
  pgrep -x RDR2.exe | wc -l                          (1 = alive, 0 = it quit)
  nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader
  wmctrl -l                                        (list visible windows)

STRACE ON THE DEATH MOMENT (worked; death is at ~3-3.5 min, attach at ~2:30):
  (setsid strace -f -p $(pgrep -x RDR2.exe | head -1) -o /tmp/opencode/rdr2-strace.log &)
  The death signature in the log: a line containing exit_group(3)

===============================================================================
PART 4 — TRAPS THAT ALREADY COST BLOOD (do not repeat)
===============================================================================

1. THE SELF-KILL TRAP (happened THREE times): pgrep -f / pkill -f with a
   pattern that appears in your own command line kills YOUR OWN terminal
   session mid-command. ALWAYS use pgrep -x RDR2.exe (exact name only) and
   kill by explicit PID numbers, never by text pattern.
2. TWO game processes can fight each other (each spinning one core, no
   window, for hours). If things look insane, count them:
   pgrep -x RDR2.exe | wc -l — 1 is normal once settled.
3. NEVER kill the game once it finally shows a window: the first REAL launch
   builds the graphics cache — a black window for 15-30+ minutes is NORMAL
   on this GPU. Killing it then throws that work away.
4. Do not run the start script from inside files/game-root (confuses it);
   running wine Launcher.exe manually with game-root as the current folder
   is fine (the script itself does exactly that).
5. The desktop is 7680 pixels wide (three monitors) — if you experiment with
   resolutions, remember gamescope defaults to 720p unless told otherwise.
6. ComfyUI (the AI image tool) hogs memory/VRAM if left running and once
   froze the whole desktop during gaming. If nothing needs it, close it.
7. Measure before judging: every conclusion above came from a number (GPU
   percent, process count, window list, syscall log), never from a feeling.

===============================================================================
PART 5 — STATE OF THE MACHINE AS THIS FILE IS WRITTEN
===============================================================================

- The last test run was stopped by Nir after ~1 minute. Check before
  anything: pgrep -x RDR2.exe — if a process is alive with no window after
  ~4 minutes, that is the known polite self-quit, not a freeze; let it
  finish or kill by PID.
- The website v2026-09-11-c is live; the magazine is complete (88 editions,
  no gaps); all page checks pass.
- Money spent on this game so far: $0 (every fix was free software).

THE ONE-SENTENCE SUMMARY FOR WHOEVER CONTINUES:
The game's main graphics engine works and the GPU renders the whole time, but
a second part of the game asks wine's oldest graphics library ~2,144 times,
never succeeds, and after ~3 minutes the game politely quits with exit code 3
without ever opening its window — explain that, and the game runs.
