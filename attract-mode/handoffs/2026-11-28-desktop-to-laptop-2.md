HAND-OFF: DESKTOP -> LAPTOP (small)
date: 2026-11-28
from: the agent on the DESKTOP
to:   the agent on the LAPTOP
your letter: handoffs/2026-11-28-laptop-to-desktop.md
repository at the time of writing: edfb863

CONFIRMED, AS YOU ASKED
1. I pulled your commit and ran "am doctor" here with the per-PC pins:
   exit 0, "No failures". uv (desktop) 0.12.0 and ffmpeg (desktop) 6.1.1
   match their lines. PHP (desktop) 8.3.6 and MariaDB 11.8.10 unchanged.
2. Your 17 self-checks pass on the desktop as well.
3. D79 is Nir's decision and it does not weaken anything that must stay
   equal: Moodle (same version), MariaDB (same series) and the line's
   Python (same lock file) are untouched. The pins file keeps its shape.
4. Your survey is good work. The three facts that matter to me are the same
   three you named: Debian 13 on the external drive with 1.1 TB free, ports
   free including 8084, and Apache active on 80 but not ours.

ONE THING I DID, SO YOU DO NOT HAVE TO DISCOVER IT
Part 09, section 9.9, item 2 says the folder work/ is never carried. That is
a property of the shared folder on EACH PC, not of the repository. I created
on the desktop:
    ~/attract-mode-files/.stignore   with the single line   work/
Please create the same file on the laptop, with the same single line, BEFORE
the folder is shared. It stays out of Git.

WHAT IS LEFT IN STAGE 0, AND WHO OWNS IT
- Syncthing's pairing: NIR, two clicks on each PC, then a test file must
  travel both ways. Nothing for us to build until then.
- O2, "pre" at Cloudflare: NIR.
- Card 0-13, the fold check of Part 00 by a different model, and the tag
  bible-v1: neither of us may check our own work. It stays open.
So: no more building work on either PC until Nir pairs Syncthing.

WHEN THE PAIRING IS DONE
1. Run "am doctor" on your PC. It should show the other PC connected.
2. Put a small file in attract-mode-files/handover/ and ask Nir to look for
   it on the desktop, and the other way round. BOTH directions, or the test
   has not passed (Part 01, 1.13, item 4).
3. Then write me a small hand-off: did both directions work, and what the
   doctor says now. Keep the laptop's Syncthing running as a user service so
   the desktop can see it.

Please also leave the cli.github.com warning alone, as you did. Nir decides.

-- the agent on the desktop, edfb863
