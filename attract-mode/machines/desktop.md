MACHINE FILE -- DESKTOP (desktop-linux)

The survey of Part 01, section 1.5. Read-only: nothing was installed,
changed or touched. Nothing inside Windows was read. Written 2026-11-28
on the desktop itself.

This file is PUBLIC. It holds no passwords, no tokens and no IP addresses.


--------------------------------------------------------------------------------
WARNING -- FREE SPACE (the rule of section 1.5)
--------------------------------------------------------------------------------

The system disk ( / ) has 31 GB free of 93.1 GB (66% used).
Section 1.5 says: if less than 60 GB is free on either PC, stop and tell
Nir. Nir was told on 2026-11-28.

The big home disk ( /home ) has 377 GB free of 1.7 TB.
PHP, MariaDB and Moodle would normally live on the system disk, not on
/home. This is why the warning matters for the kitchen (Stage 0).


--------------------------------------------------------------------------------
1. LINUX, THE USER, THE SPACE
--------------------------------------------------------------------------------

Linux:   Linux Mint 22.2 (Zara), kernel 7.0.0-30-generic, x86_64.
Machine: LENOVO Legion T7 34IRZ8 (product 90V7009WYS, board 376A).
User:    nir. Home folder: /home/nir.
Host:    mint-desktop.

Where Linux lives: an EXTERNAL USB disk, /dev/sda (1.8 TB):
  sda1  486 MB  vfat   boot
  sda2 93.1 GB  ext4   /        <- the system disk
  sda3   61 GB  swap
  sda4  1.7 TB  ext4   /home    <- the big disk
The internal NVMe disk (953.9 GB) holds Windows 11 (a BitLocker partition)
and the EFI partition. It was not read and not touched.

Free space:
  /      31 GB free of 93.1 GB   (see the warning above)
  /home 377 GB free of 1.7 TB

Hardware:
  RAM  62 GiB
  CPU  13th Gen Intel Core i9-13900KF, 32 threads
  GPU  NVIDIA GeForce RTX 4070 Ti, 12282 MiB (12 GB), driver 595.84

This confirms the KNOWN FACTS of section 1.5 for the desktop.


--------------------------------------------------------------------------------
2. SOFTWARE -- INSTALLED OR NOT, AND WHICH VERSION
--------------------------------------------------------------------------------

git           installed    2.43.0            /usr/bin/git
caddy         installed    v2.11.4           /home/nir/.local/bin/caddy
cloudflared   installed    2026.9.3          /usr/bin/cloudflared
php           NOT installed
mariadb       NOT installed (no mysql either)
syncthing     NOT installed
uv            installed    0.12.0            /home/nir/.local/bin/uv
python3       installed    3.12.3            /usr/bin/python3
ffmpeg        installed    6.1.1             /usr/bin/ffmpeg
latex         NOT installed (no pdflatex; D36 says TeX Live is not installed)
obsidian      NOT installed

Note: caddy and uv are in the user's own bin folder, not in the system.
Note: Python 3.12.3 is the system Python. The line's own Python is not
built yet (no attract-mode/line/ folder).


--------------------------------------------------------------------------------
3. LISTENING PORTS, AND WHETHER 8084 IS FREE
--------------------------------------------------------------------------------

Listening now (local or loopback):
  53      systemd-resolved, and a local virtual-network DNS
  443     the Tailscale interface
  631     CUPS (printing)
  7474    Neo4j (AI Panorama's database), loopback only
  7687    Neo4j Bolt, loopback only
  11434   Ollama (local language models), loopback only
  18789   OpenClaw (a local Node program), loopback only
  plus a few short-lived loopback ports used by OpenClaw and Tailscale

THE PORTS THAT MATTER TO THIS PROJECT:
  8081  FREE   (the existing strulovitz website -- nothing serving now)
  8082  FREE   (learnime.com -- nothing serving now)
  8083  FREE   (peaktogether.me -- nothing serving now)
  8084  FREE   <-- the new Attract Mode port. Free, as section 1.4 hopes.

Also free: 3306 (MariaDB), 5432 (PostgreSQL), 5000 (the other tunnel's
target, see part 5).

IMPORTANT: 8081-8083 being free means the three websites are NOT being
served from this PC at this moment. Do not assume they are running.


--------------------------------------------------------------------------------
4. IS A DATABASE OR PHP ALREADY RUNNING, AND WHAT USES IT
--------------------------------------------------------------------------------

PHP:     not installed, no process, no service. Nothing uses PHP.
MariaDB: not installed, no process, port 3306 free.

Databases and servers that ARE running, but belong to OTHER projects
(not Attract Mode, do not touch them):
  Neo4j   on 127.0.0.1:7474 and 127.0.0.1:7687 -- AI Panorama's knowledge
          database (a Java process).
  Ollama  on 127.0.0.1:11434 -- the local language-model server used by
          Crystal Balls.
  OpenClaw on 127.0.0.1:18789 -- a local Node program (pid 1765).

No Moodle, no web server, no PHP is running for this project.


--------------------------------------------------------------------------------
5. HOW THE TUNNEL LEARNS ITS ADDRESSES, AND IS IT THE SAME TUNNEL
--------------------------------------------------------------------------------

The three websites' tunnel is started by site-tunnel.service as:
    cloudflared tunnel --no-autoupdate run --token-file <token file>
The token file lives at ~/.config/site-hosting/tunnel-token, outside the
repository, with permission 600. It exists.

Because the tunnel is run with a TOKEN and not with a local configuration
file, its hostnames and routes live in the CLOUDFLARE DASHBOARD, not in a
file on this PC. To see or change them, open the Cloudflare dashboard.

A SECOND, DIFFERENT tunnel configuration exists at ~/.cloudflared/config.yml.
It lists only beehiveofai.com and www.beehiveofai.com, both pointing at
http://localhost:5000. That is a separate project. It is NOT the three
websites, and sites-on does not start it.

Same tunnel on both PCs: hosting/README.md says the two PCs take turns and
each keeps the same tunnel's token privately on its own disk. sites-on
prints a reminder to run sites-off on the other PC first. This PC cannot
see the laptop, so "the same tunnel" is confirmed only by the written
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


--------------------------------------------------------------------------------
7. WOULD A CHANGE UNDER attract-mode/ REBUILD THE AI PANORAMA EXPORT
--------------------------------------------------------------------------------

NO. The rebuild decision (step 4 above) looks only at the last commit
that touched "site/" or "ops/build-export.py". A commit that touches only
attract-mode/ leaves the stamp unchanged, so no rebuild happens.

The only way an attract-mode change triggers a rebuild is if the same
commit also touches site/ or ops/build-export.py.

(The last commit touching site/ or ops/build-export.py is f1a7f09,
"menu: add Demoscene Museum ...".)


--------------------------------------------------------------------------------
8. VOICE MODELS AND ART STUDIOS UNDER LINUX (NAMES ONLY)
--------------------------------------------------------------------------------

Voice studios (each has Start, Stop, Folder, Guide, Outputs icons):
  Drama 3
  VoxCPM2
  Zonos
  Voicebox (includes Whisper Large v3)

Art and AI programs:
  ComfyUI (inside ~/ai-art)
  Unsloth Studio
  Pinokio (runs WanGP video)
  Blender
  OpenClaw
  Moltbot

Folders seen: ~/drama3, ~/voxcpm2, ~/zonos, ~/voicebox, ~/ai-art, ~/Apps,
~/pinokio, ~/.unsloth.

Not present: Obsidian, LaTeX.


--------------------------------------------------------------------------------
9. OTHER FACTS A NEXT AGENT SHOULD KNOW
--------------------------------------------------------------------------------

The three user services site-caddy, site-tunnel and site-nosleep are
"enabled=linked" but INACTIVE. The websites are OFF on this PC.

User timers running for other projects:
  ai-panorama-heartbeat.timer  (daily, about 10:30)
  ai-panorama-snapshot.timer   (weekly)
  launchpadlib-cache-clean.timer
There is no Attract Mode timer and no "am" command yet.

The folders of the attract-mode/ tree that this survey found were:
  bible/  DECISIONS.md  handoffs/  kits/
The rest of the skeleton of section 1.7 does not exist yet.


--------------------------------------------------------------------------------
10. WHAT THIS SURVEY DID NOT COVER
--------------------------------------------------------------------------------

- The laptop. Its file is attract-mode/machines/laptop.md, written when an
  agent sits at that PC.
- Anything inside Windows (forbidden by section 1.6).
- Installing or changing anything (this survey is read-only).
