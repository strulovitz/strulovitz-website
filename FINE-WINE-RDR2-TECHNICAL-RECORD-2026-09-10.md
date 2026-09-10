# FINE WINE — RDR2 TECHNICAL RECORD — 2026-09-10
The problem, the hunt, and the fix. Written by the agent, by Nir's order, so
that no future session ever has to re-diagnose this.

## THE SETUP (what worked immediately)
Linux Mint 22, NVIDIA RTX 4070 Ti (Vulkan via driver 595.84), Wine 11.16
staging from the WineHQ noble repository, 32-bit audio libs, GStreamer
plugins, fuse-overlayfs. The jc141 release of Red Dead Redemption 2 needs
no installation: start.e-w.sh mounts its compressed dwarfs image on launch
and runs the game from the mount. The wine prefix is created inside the
game folder (files/prefix) on the big 1.7TB home disk, which is a separate
disk from the 92GB OS disk - filling home cannot choke Linux.

## THE PROBLEM (what did NOT work)
Launch #1 (12:04): the prefix built, wine-mono installed, Launcher.exe
handed off to RDR2.exe, vkd3d initialized full DX12 Ultimate on the GPU -
and then nothing, forever. No window, no black screen, no crash. Two hours
of "running" at 3% GPU. Relaunches hung earlier and earlier (Launcher.exe
frozen at 0% CPU, RDR2.exe never spawning), with these tells in the logs:
- wine processes stuck in D STATE (uninterruptible sleep - waiting on I/O
  that never completes). D-state processes CANNOT be killed, not even with
  kill -9; a zombie winedevice survived every kill for two hours.
- "The explorer process failed to start"
- "Failed to find monitor with path DISPLAY\Default_Monitor"
- the fuse mounts refusing to unmount ("Device or resource busy") until
  every last holder died.

## THE DIAGNOSIS
RDR2.exe was frozen mid-READ from the game files - and the game files live
behind the dwarfs FUSE mount, which is a userspace helper decompressing
everything on the fly. The helper stalls under the game's heavy reads (and
it competed all day with the overnight FLUX render on the same machine):
the I/O queue jams, every process that touches the mount freezes in D
state, and even wine's own desktop helper can no longer start. The game,
wine, the GPU and the machine were all healthy - the compressed disc was
the problem.

## THE FIX (jc141's own option, one word)
In the release's script_default_settings file, change:
    #EXTRACT=0
to
    EXTRACT=1
(don't just uncomment - replace the line with EXTRACT=1). The next launch
EXTRACTS the whole ~120GB game once, to real files inside files/game-root
on the big disk (1.1TB free), and from then on the game runs from real
files: no FUSE daemon, no decompression, nothing left to stall. Extraction
took roughly half an hour at ~9% per 8 minutes on this machine.

## THE RULES LEARNED (for any future Fine Wine entry)
1. When processes hang in D state, the fix is not "kill them harder" -
   kill -9 cannot reach a process waiting on I/O. Find the USERSPACE helper
   behind the mount (dwarfs, fuse-overlayfs) and kill THAT; the holders
   then die and the mount unmounts.
2. A stuck FUSE mount refuses fusermount3 -u while anything holds it open.
   fuser -v <mountpoint> names the holders. Kill them by PID (never
   pkill -f with a pattern that appears in your own shell's command line
   - that kills your own session, the oldest trap in this repo).
3. Before blaming wine or the game, check WHERE the frozen read lives:
   prefix = real disk (fine), game-root = the mount (suspect #1).
4. jc141 releases ship EXTRACT=1 for exactly this class of machine. On a
   fast big disk, extraction is the boring, robust answer - the museum
   plays best from a real disc, not a decompressing ghost of one.

## STATUS
2026-09-10 ~14:38: extraction started. After it completes the start script
continues automatically into the game launch. First launch still pays the
one-time shader-cache build (a black window or no window for many minutes
is NORMAL - do not kill it; later launches are fast).
