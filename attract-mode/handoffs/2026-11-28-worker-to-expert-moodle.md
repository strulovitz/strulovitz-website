HAND-OFF: WORKHORSE -> EXPERT (Moodle, now)
date: 2026-11-28
from: the WORKHORSE on the DESKTOP, DeepSeek V4.1 Flash
to:   the EXPERT, GPT 6.2 Sol
repository: github.com/strulovitz/strulovitz-website, folder attract-mode/
branch: master

--------------------------------------------------------------------------------
1. WHAT NIR WANTS
--------------------------------------------------------------------------------

Moodle. Now. In his words: "why are we not in Moodle, which is the meat and
potatoes ... do the main thing already ... i want to see it within my life".
He wants to click inside Moodle soon, not months from now.

Two rules he set today, which outrank any plan:
- Do only what he asks. No invented safety rules, no extra work.
- If the Bible and his wish disagree, his wish wins, and the Bible is corrected
  with a dated decision (AM-LAW 19). The Bible is meant to reflect what he
  wants; it is not to be obeyed against him.

--------------------------------------------------------------------------------
2. WHAT THIS MEANS FOR THE ORDER
--------------------------------------------------------------------------------

Part 11, 11.4 puts Stage 1 (a first Making Of) before Stage 2 (Moodle). Nir has
overruled that: Moodle goes first. The art work is parked, not deleted: cards
1-06 to 1-12 stay open, and 1-01 to 1-05 are already done or draft-ready.

Part 11, 11.5 says the switch of www waits because "from this day, a link to
the home page opens Attract Mode, so the front page must have something to show
on its first day". Nir is not waiting: www becomes Moodle. So tell us, as an
instruction and not as a choice, what that front page must say on day one while
no film exists yet, so that it is honest and not empty of meaning.

--------------------------------------------------------------------------------
3. THE STATE OF THE MACHINES TODAY
--------------------------------------------------------------------------------

Nothing of Moodle is installed. The disk is clean; port 8084 answers our own
placeholder ("Attract Mode is being built.").

DESKTOP (serves the world): Linux Mint 22.2. PHP 8.3.6 with the fpm package,
MariaDB 11.8.10 on 127.0.0.1 only, Caddy 2.11.4, cloudflared, Syncthing
2.1.7. Missing PHP extensions: soap and xmlrpc only. Moodle 5.x does not
require xmlrpc; soap is optional and Moodle's own environment check decides.
Ports: 8081 the old site and pre, 8082 learnime.com, 8083 peaktogether.me,
8084 ours, 3306 MariaDB. www, learnime, peaktogether and pre all answer 200.
The tunnel starts from Nir's icon and runs by token, so its routes live at
Cloudflare: Networking, Tunnels, tunnel "home-sites", "Routes", "Published
application", one "Service URL". The place Moodle goes is /var/www/moodle with
its data folder outside the web root, which is Moodle's own default (D9).
/var/www does not exist yet.

LAPTOP: Debian 13, PHP 8.4.28, MariaDB 11.8.9, Syncthing 2.1.7, same repo,
equal worker. It hosts ACE-Step, Ruach, VoxCPM2, LatentSync, and Apache on
port 80 (stock page, not ours, D80). Only one PC serves at a time.

--------------------------------------------------------------------------------
4. WHAT WE NEED FROM YOU: HOW, IN STEPS
--------------------------------------------------------------------------------

One thing only is fixed, and it is not a choice: the address. Nir rejected the
idea of showing Moodle only on this computer, or under some temporary name.
Those were options I invented, nobody asked for them, and one of them (the
temporary name) would make life hard later. They are not the plan, and they are
not to be discussed again.

Everything else is yours to decide as you write the cards. Inside a Moodle
installation there are real choices; where one exists, decide it, say why, and
put it in the card. What we need from you is the "how": the steps, in order,
each with a proof before the next, and what Nir must do himself.

1. HOW TO OPEN MOODLE AT www. The path is fixed by the Bible, not chosen by us:
   Moodle is installed with https://www.strulovitz.org from the first minute
   (Part 08, 8.5, item 1); its pages are read through port 8084 from inside the
   PC (Part 11, 11.5, item 1); then Nir points www at 8084 (Part 11, 11.5, item
   3). Give us that as ordered steps: what is done first, how each step is
   proved before the next, what Nir does himself, and the exact way back if the
   day goes wrong (Part 11, 11.5, "the way back").
2. HOW the admin password is typed by Nir himself, so it never enters a shell
   history, a log or a chat (Part 08, 8.5, item 7).
3. HOW PHP is to be set up here: one FPM pool running as user nir on
   /run/php/php8.3-fpm-attract.sock, uploads 20 MB, memory 256 MB, sessions in
   the data folder. State it as the spec, with the steps to apply it.
4. HOW the Caddy block for 8084 is written: /am/ answered by Caddy itself; root
   /var/www/moodle/public; php_fastcgi on the unix socket; anything matching no
   file goes to /r.php. Give the exact handler order and the command that
   validates it before any reload.
5. HOW config.php must be set for a tunnel that ends TLS at Cloudflare:
   sslproxy and reverseproxy, and why each is needed (Part 08, 8.5, items 2
   and 3).
6. HOW we prove the building half is done before the switch: the checks, in
   order, and which of them need Nir at the keyboard.
7. WHAT the front page says on day one, before any film exists.
8. THE CARDS THEMSELVES, 2-01 onward: one practical piece and one proof each.
   The shape Nir understands: the database and its user; Moodle's files and the
   data folder outside the web root; PHP running as Nir; the Caddy door; the
   PHP limits; the environment check; the installer at the real address with
   Nir's password; the logs and the clock. In order, ending with him clicking
   inside Moodle.

--------------------------------------------------------------------------------
5. WHAT I WILL DO WHEN YOUR CARDS ARRIVE
--------------------------------------------------------------------------------

Pull, read your letter first, then execute one card at a time: run it, show the
proof, update STATE.md and the dated log, commit only the named files, push. If
a card cannot be executed as written, I stop and say why. I do not improvise
and I do not add work nobody asked for. If a fact is needed from the laptop, I
write him a handoff; he is equal to me, not a helper.

Nir switches models by hand. Put the real content in the files, and give him
one short sentence to act on.

-- the WORKHORSE on the desktop
