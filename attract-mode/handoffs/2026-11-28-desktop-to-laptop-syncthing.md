HAND-OFF: DESKTOP -> LAPTOP (Syncthing pairing, as much done for Nir as possible)
date: 2026-11-28
from: the agent on the DESKTOP
to:   the agent on the LAPTOP

Nir's instruction was explicit: whatever the models can do for him, do it. So
almost all of the pairing is ours. His only act is to keep both PCs switched
on, in Linux, at the same time, and to say one sentence to each of us.

WHAT I ALREADY DID ON THE DESKTOP (no root, no Caddy, no tunnel)
- Started Syncthing as a USER service (not root), API on 127.0.0.1:8384.
- Created the shared folder: id "attract-mode-files", path
  /home/nir/attract-mode-files, type send-receive, watcher on, rescan 60 s.
- ~/attract-mode-files/.stignore holds "work/" (Part 09, 9.9, item 2).
- It is not shared with anybody yet.

THE DESKTOP'S DEVICE ID (this is a PUBLIC KEY, not a password; it will be
deleted from this file as soon as we are paired):
(removed on 2026-11-28, minutes after the pairing succeeded)

YOUR STEPS, IN ORDER
1. Make sure Syncthing runs on the laptop as a USER service and answers on
   127.0.0.1:8384. Do not publish your own device ID: I will take it from the
   pending list, so it never enters Git.
2. Add the desktop as a remote device, through Syncthing's own API, using the
   id above and the name "mint-desktop". Example shape (adjust to your Syncthing
   version; read first, then add only if it is not there):
       GET  /rest/config/devices
       POST /rest/config/devices
       {"deviceID":"(removed on 2026-11-28, minutes after the pairing succeeded)","name":"mint-desktop","addresses":["dynamic"]}
3. Wait until "am doctor" (or /rest/system/connections) shows it connected.
   If it does not connect within a few minutes, check that both Syncthing
   services are running; local discovery or a relay will do the rest.
4. I will then accept your device from my pending list and share the folder
   with you. When the folder offer appears on your side, ACCEPT it, with the
   path /home/nir/attract-mode-files and the SAME id "attract-mode-files".
   Do not create a second folder and do not change its type.
5. Write me a short hand-off: your device name as I will see it, whether the
   connection is up, and whether the folder offer arrived.

THE TEST, WHEN BOTH SIDES ARE PAIRED (Part 01, 1.13, item 4)
- I put a file in handover/ from this side; it must appear on yours.
- You put one from yours; it must appear here.
- BOTH directions, or the test has not passed.
- Then "am doctor" on both PCs must show the other PC connected.

WHAT NOT TO DO
- Do not stop, restart or reconfigure Syncthing's service while we are
  pairing, and do not add a third device or a second folder.
- Do not publish a device ID, an address or a token in any file in Git.
- Do not touch Apache or start the tunnel.

-- the agent on the desktop
