# HANDOVER — 2026-09-11 afternoon session end (Nir closing OpenCode to save context)

NEXT SESSION BOOT SEQUENCE:
1. Read /home/nir/AGENTS.md (latest entry at the bottom).
2. git -C /home/nir/strulovitz-website pull
3. Read THIS file + FINE-WINE-RDR2-NVAPI-FIX-2026-09-11.md
4. THE FIRST THING: Nir has answers from Google AI search to the 5 questions
   at the bottom of this file (he pasted them there or will paste in chat).
   Use them to fix RDR2. He expects this FIRST, before anything else.
5. Keep replies SHORT (one screen, important thing last) — locked rule.

STATE OF THE WEBSITE (all done, live, verified):
- v2026-09-11-b is live. The GPT galaxy clump is FIXED (ISLAND RULE in
  pipeline/stages/layout.py, commit 05fa7ef). The 7 healthy galaxies are
  bit-identical to what Nir liked. Deployed + verified over the internet.
- PENDING DECISION FOR NIR (do NOT spend without asking): Qwen's nvidia +
  anthropic editions were cut mid-JSON by token ceilings (31998 at 32k,
  63998 at 64k — Qwen writes monster answers). Fix = paid re-asks, about
  $0.20-0.45 each, ~$0.50 total. The DB has 86 editions, disk has 88.

STATE OF RDR2 (Fixed so far, NOT yet playable):
- DONE: EXTRACT=1 extraction (no FUSE, D-state gone forever).
- DONE: TWO dueling instances killed; ComfyUI no longer squatting VRAM.
- DONE (this session): the infinite nvapi64.dll scan diagnosed by strace and
  fixed with dxvk-nvapi v0.9.2 (nvapi64.dll + nvofapi64.dll into the prefix's
  system32, native overrides). Full record: FINE-WINE-RDR2-NVAPI-FIX-2026-09-11.md.
- CURRENT BEHAVIOR after the nvapi fix: the game boots MUCH further — vkd3d
  fully initializes the GPU ("DX Ultimate supported!", DXR, SM 6.8) — runs
  ~3 minutes 5 seconds WITHOUT ever showing a window, then exits POLITELY
  (ScriptHook "UNINIT" clean unregistration, no crash logs, "game unmounted").
  The "err:mscoree:expect_no_runtimes Process exited with a Mono runtime
  loaded" line appears at exit.
- TOP SUSPECTS (in order):
  1. The mod tooling running .NET on wine-mono inside the game:
     ModManager.log shows "ModManager.Core.UnmanagedHost" loading INTO the
     game; LML is .NET. Test = rename files/game-root/NativeTrainer.asi and
     files/game-root/lml out of the way, keep vfs.asi (possible essential
     version bypass) and 1911.dll + bink2w64.dll (the crack), relaunch.
  2. A missing plain-wine requirement (esync limits, /dev/shm, virtual desktop).
  3. Launcher handshake / exit_file.dat protocol.
- KILL PROCESSES SAFELY: pgrep -x RDR2.exe / pgrep -x Launcher.exe, kill by
  PID list. NEVER pkill -f with a pattern from your own command line (hit
  twice this session, kills your own shell).
- The game's first REAL successful launch will still owe a shader-cache
  build: window may be black 15-30+ min AFTER it appears — never kill it then.

THE 5 GOOGLE QUESTIONS NIR TOOK (his answers come first thing next session):
1. jc141 Red Dead Redemption 2 Linux wine starts without any window and
   exits after about 3 minutes silently how to fix
2. RDR2 under plain wine (not Proton) closes itself silently at boot, vkd3d
   initializes the GPU fine but no window is ever created — known requirements
   (nvapi, wine-mono, virtual desktop, esync)?
3. wine "err:mscoree:expect_no_runtimes Process exited with a Mono runtime
   loaded" — does this cause a game to exit, and should wine-mono be disabled?
4. Do ScriptHookRDR2 and Lenny's Mod Manager (lml) work under wine, or do they
   crash RDR2 at boot? Should I remove NativeTrainer.asi and the lml folder
   to test vanilla?
5. RDR2 exit_file.dat in AppData Local Rockstar Games — normal handshake file
   or does the game exit when the launcher writes it?

MONEY TODAY (2026-09-11): $0 spent. Only potential spend = the Qwen re-asks,
NOT approved yet. Website deploys were free (SFTP), fixes were code + free software.
