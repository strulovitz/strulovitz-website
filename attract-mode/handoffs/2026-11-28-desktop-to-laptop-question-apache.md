HAND-OFF: DESKTOP -> LAPTOP (small, one question)
date: 2026-11-28
from: the agent on the DESKTOP
to:   the agent on the LAPTOP

Nir read your survey and asked a fair question that neither of us answered:
"Apache is not ours -- whose is it? These are both my computers."

He is right. The Bible's sentence (Part 01, 1.8, item 7: "Apache. It belongs
to something else on the laptop") is a note written before any check. Your
survey correctly reported that Apache answers on ports 80 and 443, and then
stopped, as it should have. So there is a fact in the Bible that nobody has
looked at. Please look.

READ ONLY. Do not stop, start, reload or reconfigure Apache. Do not open its
files for writing. If a command needs root, ask Nir to type his password in
the terminal; never paste it anywhere.

WHAT TO FIND OUT
1. WHICH SITES APACHE SERVES: its virtual hosts, their server names and their
   document roots.
       apache2ctl -S
       ls -l /etc/apache2/sites-enabled/
   and read those vhost files (read-only).
2. WHAT IS ACTUALLY IN EACH DOCUMENT ROOT: the NAMES of the top-level entries
   only -- no file contents, and nothing that could hold a password. Is it a
   copy of one of Nir's sites, a ready-made tool (phpMyAdmin, WordPress,
   a control panel), a test page, or an empty folder?
3. WHEN IT ARRIVED AND WHAT STARTED IT: the install date of the apache2
   package, and when the service last started.
4. WHAT LISTENS ON 443: your survey said "Apache, and a secure local service".
   Name each listener on 443 (program names only, no addresses).
5. WHETHER IT MATTERS AT ALL: our project uses ports 8081 to 8084 through
   Caddy, and Moodle will use 8084. Does anything in Apache's setup touch
   those ports or those folders? (It should not. Say so either way.)

WHAT TO WRITE BACK
A short hand-off, handoffs/2026-11-28-laptop-to-desktop-2.md, with four lines:
   - what Apache serves, in plain words;
   - the document roots, in plain words;
   - whether it is something Nir would miss if it were ever stopped;
   - whether it collides with anything we plan.
Then Nir will read it out to me.

WHY THIS MATTERS, IN ONE SENTENCE
If Apache serves one of Nir's own projects, we must know it before Switch Day,
because Switch Day moves his websites; if it serves something we can safely
ignore, we write that down and the Bible's note becomes a checked fact instead
of a memory.

-- the agent on the desktop
