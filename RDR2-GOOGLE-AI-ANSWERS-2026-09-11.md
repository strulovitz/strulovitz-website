# RDR2 — NIR'S GOOGLE AI SEARCH ANSWERS — 2026-09-11

The 5 questions I gave Nir, asked by him in Google AI search, pasted back verbatim
below. Saved at his order so the next session knows exactly what the outside world
says about our exact failure: the game boots (GPU fully initializes via vkd3d)
but never shows a window and exits politely at ~3 minutes.

MY QUICK READ OF THESE ANSWERS, ranked against OUR measured evidence:
1. ANSWER 2's "child window / multiple Vulkan ICDs" bug is a STRONG new suspect:
   RDR2 silently exits when it sees duplicate Vulkan ICDs (e.g. nvidia + swrast/
   lavapipe). CHECK NEXT: `ls /usr/share/vulkan/icd.d/` — if more than the
   nvidia one is there, launch with VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json
2. ANSWER 2 + 4: WINEDLLOVERRIDES="dinput8=n,b" — the ASI loader (dinput8.dll)
   should be explicitly native,builtin; we never set this override. The mods
   DID load (logs show ScriptHook INIT Success) so this is likely fine, but it
   is the standard checklist item.
3. ANSWER 2's wine VIRTUAL DESKTOP (winecfg Graphics tab, emulate 1920x1080)
   matches our own boot log's "Failed to initialize registry display settings
   for \\.\DISPLAY1" — worth one try if the ICD fix doesn't do it.
4. ANSWER 2's esync/fsync: our TkG wine is staging; check `ulimit -Hn` is high
   in the launching shell (RDR2 spawns enormous thread counts).
5. ANSWER 3 + 5 confirm: the mscoree Mono warning is a SYMPTOM not a cause, and
   exit_file.dat is a normal handshake file — so those two dead ends are closed.
6. ANSWER 2's NVAPI advice ("disable it") applies to the crash-after-detect case;
   OUR case was the opposite (the game spun forever scanning for the file), and
   our dxvk-nvapi install already fixed the scan and got the GPU initializing.
   Keep our nvapi files; do not remove them.
7. ANSWER 4 confirms the vanilla test procedure (remove NativeTrainer.asi, lml,
   and even dinput8.dll + vfs.asi) is a valid fallback — but note vfs.asi is
   the release's version bypass: if removing it makes the DRM checks fire,
   put it back and only remove NativeTrainer + lml.
8. ANSWER 1's DBG=1 bash start.w.sh debug flag is worth using on the next launch
   to see the wrapper's own output before the exit.

================================================================================
QUESTION 1: Red Dead Redemption 2 johncena141 jc141 release Linux wine starts
without any window and exits after about 3 minutes silently how to fix
================================================================================
When Red Dead Redemption 2 (especially a johncena141 / jc141 Linux wine-wrapped
release) starts silently without opening a window and terminates after a few
minutes, it is almost always caused by a missing dependencies environment, an
unextracted dwarfs storage container, or an absolute path formatting restriction
in the wrapper script. (reddit r/LinuxCrackSupport threads ydx0og, 11k0d3v)
Here is how you can isolate and fix the problem step by step:
1. Enable Debugging to See the Real Error. Johncena141 releases bundle a custom
startup script. Turn off silent mode to see exactly why it is exiting: launch
with: DBG=1 bash start.w.sh — look closely at the terminal output right before it
closes.
2. Check for "Dwarfs" Extraction Issues. Many jc141 releases use DwarFS high-
compression file system. If the system lacks fuse drivers or configuration, the
script spins out and exits silently. Run the built-in extractor helper
(./settings.sh extract-dwarfs) or extract manually. [NOTE FOR US: ALREADY DONE —
our EXTRACT=1 extraction completed 2026-09-10, no FUSE at runtime, the D-state
hang is gone.]
3. Check for the vulkan-1.dll Conflict. RDR2 relies heavily on Vulkan or DX12.
If the Wine prefix hardcodes or drops a generic Windows vulkan-1.dll into the
game directory, it will crash silently on Linux. Look inside the main game
directory (where RDR2.exe is); if a file explicitly named vulkan-1.dll exists,
rename it (vulkan-1.dll.bak). This forces Wine to use the native system Vulkan
drivers.
4. Provide Missing Media Foundation Files. Rockstar games require specific video
files (Media Foundation) for the intro cinematic; without them the game crashes
during its initial hidden black screen. Verify 32-bit and 64-bit Vulkan drivers
are installed (vulkan-icd-loader, lib32/mesa-vulkan-drivers:i386 on Debian/Ubuntu).
5. Bypass the Wrapper via Lutris/Steam. Point Lutris or Steam (non-Steam game)
directly at RDR2.exe inside the extracted directory, runner = recent GE-Proton /
Wine-GE, with the launch argument: -vulkan

================================================================================
QUESTION 2: RDR2 running under wine (not Proton) closes itself silently at boot,
vkd3d-proton initializes the GPU fine but no window is ever created, what are the
known requirements for RDR2 under plain wine (nvapi, wine-mono, virtual desktop,
esync)?
================================================================================
Running RDR2 under plain Wine requires specific environment variables and
configuration overrides that Proton usually handles automatically. When the game
initializes the GPU via vkd3d-proton but silently crashes before creating a
window, it is typically due to Vulkan surface creation failures, missing
specialized Windows dependencies, or Rockstar Games Launcher hooks.
1. The Child Window Rendering Bug (Crucial). RDR2 has a notorious behavior where
if it detects multiple Vulkan ICDs (or duplicate video adapters), it switches to
a code path that requires child window rendering. Plain Wine often fails here,
resulting in a silent exit or a vkCreateWin32SurfaceKHR error. Fix: explicitly
hide duplicate or integrated GPUs: VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json
(adjust for vendor). Also ensure no conflicting software Vulkan layers
(vulkan-swrast / lavapipe).
2. Wine Virtual Desktop. Highly Recommended. RDR2 frequently crashes when
attempting to query display modes or resize a borderless/fullscreen window on
boot. Fix: winecfg -> Graphics tab -> "Emulate a virtual desktop" at native
resolution (e.g. 1920x1080).
3. NVAPI (Nvidia users only). Must be disabled or explicitly configured. RDR2
checks for Nvidia-specific extensions; if it detects an Nvidia card via Wine but
can't properly negotiate NVAPI calls, it will crash. If you do not need DLSS,
disable NVAPI (PROTON_ENABLE_NVAPI=0 or dxgi.nvapiHack=False in dxvk.conf). If
you DO want DLSS, wine-nvapi must be properly installed in the prefix and
overridden as nvapi,nvapi64 = n,b in winecfg.
4. Wine-Mono vs. .NET Framework. The Rockstar Games Launcher often relies on
complex WPF/WCF features that wine-mono does not execute properly, causing a
silent crash before spawning the actual game. Safer: clean Wine prefix,
winetricks dotnet48, let it overwrite Wine-Mono.
5. Sync Framework (Esync/Fsync). Mandatory for performance. RDR2 spins up an
enormous number of concurrent worker threads; plain Wine's standard server
synchronization bottlenecks, stutters or deadlocks. Set open file limits high
(ulimit -Hn 524288) and launch with WINEESYNC=1 or WINEFSYNC=1 (staging builds).
6. The Default API Trap (Vulkan vs DX12). RDR2 may prefer its internal Vulkan
renderer; if vkd3d-proton logs success but nothing happens, the game might be
switching back to its internal Vulkan pipeline and failing. Check
Documents/Rockstar Games/Red Dead Redemption 2/Settings/system.xml — the <API>
tag: kSettingAPI_Vulkan vs kSettingAPI_DX12 must match the translation layer
you intend.

================================================================================
QUESTION 3: wine error "err:mscoree:expect_no_runtimes Process exited with a Mono
runtime loaded" — does this cause a game to exit and should wine-mono be disabled
or is it harmless?
================================================================================
No, this error usually does not cause a game to exit, and you should not disable
wine-mono by default. The message is a harmless CLEANUP warning: Wine prints it
when a .NET or Mono-based application closes down and a background thread or a
piece of the Mono runtime is still in memory while the process is terminating.
Because it triggers during or immediately after the process exit sequence, it is
typically a SYMPTOM of the game closing, not the cause. Disabling wine-mono will
likely break the game if it relies on .NET. If the game is crashing and this is
the last line, look slightly higher in the logs: the actual culprit (DirectX
failure, missing native DLL, page fault) is printed BEFORE this shutdown warning.

================================================================================
QUESTION 4: Do ScriptHookRDR2 and Lenny's Mod Manager (lml) work under wine on
Linux, or do they crash Red Dead Redemption 2 at boot? Should I remove
NativeTrainer.asi and the lml folder to test vanilla?
================================================================================
Yes, they work under Wine/Proton on Linux, but they cause a silent crash at boot
if you do not explicitly instruct Wine to load the custom modding files. By
default Wine may ignore custom libraries like dinput8.dll or version.dll. Steam
launch options fix: WINEDLLOVERRIDES="dinput8=n,b;version=n,b" %command% (or set
the native,builtin overrides in winecfg for a plain prefix). Removing for a
vanilla test is a good idea — but to truly go vanilla you must remove the loaders
too: the lml folder, the ModManager folder, NativeTrainer.asi, ScriptHookRDR2.dll,
vfs.asi, AND dinput8.dll / version.dll (the ASI loaders). For the Lenny's Mod
Manager UI, launch ModManager.UI.exe inside the game's own Wine prefix with
protontricks.

================================================================================
QUESTION 5: Red Dead Redemption 2 what is exit_file.dat in AppData Local Rockstar
Games — does the game exit if the launcher writes it or is it a normal handshake
file?
================================================================================
exit_file.dat is a completely normal handshake, diagnostics and telemetry file
used by the Rockstar Games Launcher and Social Club framework. Writing it does
NOT force the game to exit. It functions as a tracking and logging mechanism:
when the game session closes — clean exit or crash — the Rockstar ecosystem
generates/updates it to store the exit status. Launcher logs show:
[gamelaunch] Game exited with code 0x0 (0)
[crashdetection] Reading game exit file...
[crashdetection] Updating exit code: 0x00000000
[crashdetection] No additional error information found.
If the game crashes, the launcher reads exit_file.dat to determine the specific
exit code. It is a routine handshake file: if the game is closing immediately
after launching, the file is merely REPORTING a crash caused by something else
(driver conflict, permissions, corrupted cache).
