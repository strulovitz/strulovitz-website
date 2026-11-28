MACHINE FILE -- LAPTOP (laptop-linux)

The survey of Part 01, section 1.5. Read-only: nothing was installed,
changed or touched. Nothing inside Windows was read. Written 2026-11-28
on the laptop itself, from machines/laptop-survey.sh plus the usual
read-only system commands.

This file is PUBLIC. It holds no passwords, no tokens and no IP addresses.


--------------------------------------------------------------------------------
WARNING -- FREE SPACE (the rule of section 1.5)
--------------------------------------------------------------------------------

The system disk ( / ) has 1.1 TB free of 1.8 TB (621 GB used, 37% used).
Section 1.5 says: if less than 60 GB is free on either PC, stop and tell
Nir. Here the rule passes with a wide margin. There is no second big
partition: / and /home are the same filesystem on this PC.


--------------------------------------------------------------------------------
1. LINUX, THE USER, THE SPACE
--------------------------------------------------------------------------------

Linux:   Debian GNU/Linux 13 (trixie), kernel 6.12.94+deb13-amd64, x86_64.
Machine: LENOVO Legion Pro 7 16IAX10H (chassis: laptop).
User:    nir. Home folder: /home/nir.
Host:    deb-server.

Where Linux lives: an EXTERNAL USB disk, /dev/sda "P40 Game Drive" (1.8 TB):
  sda1    16 MB  (reserved)
  sda2   488 MB  vfat   (EFI)
  sda3    61 GB  swap   [SWAP]
  sda4   1.8 TB  ext4   /        <- the system disk AND /home
The internal NVMe disk (1.9 TB, SK Hynix) holds Windows 11 (NTFS) and its
EFI partition. It was not read and not touched.

Two more external disks are attached and are Nir's media storage:
  /dev/sdb  3.6 TB  NTFS  mounted at /media/nir/1E42FC3E42FC1BE9
  /dev/sdc  3.6 TB  NTFS  mounted at /media/nir/T7 Shield
They are NOT ours. Do not read, write or index them.

Free space:
  /      1.1 TB free of 1.8 TB   (the rule of section 1.5 passes)

Hardware:
  RAM  62 GiB (about 51 GiB free, 6 GiB in use at the survey)
  CPU  Intel Core Ultra 9 275HX, 24 threads
  GPU  NVIDIA GeForce RTX 5090 Laptop GPU, 24463 MiB (24 GB), driver 580.95.05

This confirms the KNOWN FACTS of section 1.5 for the laptop (Lenovo Legion,
RTX 5090 with 24 GB, 64 GB of memory, Debian 13 on its own external USB
drive).


--------------------------------------------------------------------------------
2. SOFTWARE -- INSTALLED OR NOT, AND WHICH VERSION
--------------------------------------------------------------------------------

git           installed    2.47.3            /usr/bin/git
caddy         installed    v2.11.4           /home/nir/.local/bin/caddy
cloudflared   installed    2026.9.3          /usr/bin/cloudflared
php           NOT installed
mariadb       NOT installed (no mysql either)
syncthing     NOT installed
uv            installed    0.12.1            /home/nir/.local/bin/uv
python3       installed    3.13.5            /usr/bin/python3
ffmpeg        installed    7.1.5-0+deb13u1   /usr/bin/ffmpeg
latex         NOT installed (no pdflatex; D36 says TeX Live is not installed)
obsidian      NOT installed

Note: caddy and uv are in the user's own bin folder, not in the system.
Note: Python 3.13.5 is the system Python. The line's own Python (pinned
3.13.14) is built by uv inside the project and is not the system one.

TWO PIN MISMATCHES TO SETTLE BEFORE "am doctor" CAN PASS (reported to the
desktop in the hand-off):
  uv       the pin is 0.12.0; this PC has 0.12.1.
  ffmpeg   the pin is 6.1.1; this PC has 7.1.5 (Debian 13's own version).
Both are real numbers, not guesses. Only the EXPERT may change a pin, with
the reason written beside it (Part 01, section 1.8).


--------------------------------------------------------------------------------
3. LISTENING PORTS, AND WHETHER 8084 IS FREE
--------------------------------------------------------------------------------

Listening now (local or loopback):
  22      OpenSSH
  80      Apache (see part 4 -- NOT ours)
  443     Apache, and a secure local service
  631     CUPS (printing)
  1716    a local program
  7474    Neo4j (AI Panorama's database), loopback only
  7687    Neo4j Bolt, loopback only
  11434   Ollama (local language models), loopback only
  18789   OpenClaw (a local Node program), loopback only
  plus a few short-lived loopback ports used by OpenClaw, the desktop and
  the browser.

THE PORTS THAT MATTER TO THIS PROJECT:
  8081  FREE   (the existing strulovitz website -- nothing serving now)
  8082  FREE   (learnime.com -- nothing serving now)
  8083  FREE   (peaktogether.me -- nothing serving now)
  8084  FREE   <-- the new Attract Mode port. Free, as section 1.4 hopes.

Also free: 3306 (MariaDB) and 8384 (Syncthing's own window).

IMPORTANT: 8081-8083 being free means the three websites are NOT being
served from this PC at this moment. Do not assume they are running.


--------------------------------------------------------------------------------
4. IS A DATABASE OR PHP ALREADY RUNNING, AND WHAT USES IT
--------------------------------------------------------------------------------

PHP:     not installed, no process, no service. Nothing uses PHP.
MariaDB: not installed, no process, port 3306 free.

APACHE IS RUNNING on port 80. It belongs to something else on this laptop
(Part 01, section 1.8). It is NOT ours: never touch, stop, reconfigure or
reuse it. The survey found it active and left it alone.

Databases and servers that ARE running, but belong to OTHER projects
(not Attract Mode, do not touch them):
  Neo4j   on 127.0.0.1:7474 and 127.0.0.1:7687 -- AI Panorama's knowledge
          database (a Java process).
  Ollama  on 127.0.0.1:11434 -- the local language-model server.
  OpenClaw on 127.0.0.1:18789 -- a local Node program.

No Moodle, no PHP and no database for this project is running.


--------------------------------------------------------------------------------
5. HOW THE TUNNEL LEARNS ITS ADDRESSES, AND IS IT THE SAME TUNNEL
--------------------------------------------------------------------------------

The three websites' tunnel is started by site-tunnel.service with a token:
    cloudflared tunnel --no-autoupdate run --token-file <token file>
The token file lives at ~/.config/site-hosting/tunnel-token, outside the
repository, with permission 600. It exists.

Because the tunnel is run with a TOKEN and not with a local configuration
file, its hostnames and routes live in the CLOUDFLARE DASHBOARD, not in a
file on this PC. To see or change them, open the Cloudflare dashboard.

There is no ~/.cloudflared/config.yml on this PC (the script found none).
Which projects it listed on the desktop is in machines/desktop.md.

Same tunnel on both PCs: hosting/README.md says the two PCs take turns and
each keeps the same tunnel's token privately on its own disk. This PC cannot
see the desktop, so "the same tunnel" is confirmed only by the written
documentation, not measured here.


--------------------------------------------------------------------------------
6. WHAT "WEBSITES ON" DOES, STEP BY STEP (from hosting/bin/sites-on)
--------------------------------------------------------------------------------

1. Prints the reminder: run sites-off on the OTHER computer first; never
   host from both at the same time.
2. Checks the tunnel token file (~/.config/site-hosting/tunnel-token, mode
   600) and that cloudflared exists. If either is missing: stops, starts
   nothing.
3. For each of six repositories -- strulovitz-website, Anime,
   peaktogether-website, second-opinion, demoscene-museum, crystal-balls --
   runs "git pull --ff-only" (or "git clone" if the folder is missing).
   A failure prints a loud warning, and the other sites still start.
4. Rebuilds the Strulovitz website export only if the newest commit that
   touched "site/" or "ops/build-export.py" differs from the stamp in
   exports/.built-from. The build is "python3 ops/build-export.py"; then
   the stamp is written.
5. Reads the live version name from exports/pointer.json, checks that its
   folder exists, and points exports/current at it.
6. Creates exports/2nd-opinion as a link to ~/second-opinion/site if it is
   missing.
7. Starts three user services: site-caddy.service, site-nosleep.service,
   site-tunnel.service.
8. Waits 3 seconds, then runs sites-check: it asks the local server for
   every menu link and every served folder and prints each one that is not
   200; it also lists served files that git ignores or has not pushed.
   Warnings are printed if any repository had a problem.

"Websites OFF" (sites-off) stops these three services and leaves Apache
alone. No hand-over of Moodle's data exists yet (that is Part 09).

Today all three user services are "enabled=linked" but INACTIVE. The
websites are OFF on this PC.


--------------------------------------------------------------------------------
7. WOULD A CHANGE UNDER attract-mode/ REBUILD THE AI PANORAMA EXPORT
--------------------------------------------------------------------------------

NO. The rebuild decision (step 4 above) looks only at the last commit
that touched "site/" or "ops/build-export.py". A commit that touches only
attract-mode/ leaves the stamp unchanged, so no rebuild happens.

The only way an attract-mode change triggers a rebuild is if the same
commit also touches site/ or ops/build-export.py.

The survey found no file under ops/ that mentions attract-mode. The only
user timers listed belong to desktop support (drkonqi), not to AI Panorama.


--------------------------------------------------------------------------------
8. VOICE MODELS AND ART STUDIOS UNDER LINUX (NAMES ONLY)
--------------------------------------------------------------------------------

Studios with Start/Stop scripts and Desktop icons:
  ACE-Step 1.5   ~/ace-step    soundtrack (songs)
  Ruach (YuE2)   ~/ruach       soundtrack (songs)
  VoxCPM2        ~/voxcpm2     voice (clones a voice; speaks Hebrew)
  LatentSync 1.6 ~/latentsync  voice / lip-sync (needs about 20 GB of VRAM)

Other AI programs seen:
  Unsloth Studio (in ~/.unsloth, with llama.cpp and whisper.cpp)
  Ollama (local language models)
  OpenClaw and Moltbot (local agent programs)
  Blender (if installed for this user; not surveyed in depth)

Not present in this user's home: Voicebox, Drama 3, Zonos, ComfyUI, Pinokio,
Obsidian, LaTeX. (The Android/Linux notes may list some of these on the
desktop; they were NOT found on this laptop.)

Desktop icons with start/stop: 4 sets (ace-step, latentsync, ruach,
voxcpm2), each with Start, End, Folder, Guide and Outputs.


--------------------------------------------------------------------------------
9. OTHER FACTS A NEXT AGENT SHOULD KNOW
--------------------------------------------------------------------------------

The Apache web server is active on this PC and is not ours. Leave it alone.

The three Attract Mode services are inactive, and there is no Attract Mode
timer. The "am" command exists in the repository but has not been run on
this PC yet.

The folders of the attract-mode/ tree are the ones that arrive by git pull.
Place 3 (/home/nir/attract-mode-files/) was created on 2026-11-28 by this
agent (card 0-05), with its nine folders. Its exact path, needed by
Syncthing, is:

    /home/nir/attract-mode-files

Inside it, voice/ has mode 700. work/ is never copied (Part 09, 9.9).


--------------------------------------------------------------------------------
10. WHAT THIS SURVEY DID NOT COVER
--------------------------------------------------------------------------------

- The desktop. Its file is attract-mode/machines/desktop.md.
- Anything inside Windows (forbidden by section 1.6).
- Installing or changing anything (this survey is read-only).
