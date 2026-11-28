HAND-OFF: WORKHORSE -> EXPERT (Moodle at www; what we need from you)
date: 2026-11-28
from: the WORKHORSE on the DESKTOP, DeepSeek V4.1 Flash
to:   the EXPERT, GPT 6.2 Sol
repository: github.com/strulovitz/strulovitz-website, folder attract-mode/
branch: master

--------------------------------------------------------------------------------
1. WHAT NIR WANTS
--------------------------------------------------------------------------------

Moodle, at www.strulovitz.org, built now. In his words: "which is the meat and
potatoes ... do the main thing already ... i want to see it within my life".
The art half (the first Making Of, the Ear, the recorder) is parked, not
deleted: cards 1-06 to 1-12 stay open and keep their place.

So the Bible's order changes: Moodle first. The Bible's own path for Moodle is
kept exactly as written (Part 08, 8.5 and Part 11, 11.5): it is installed with
https://www.strulovitz.org as its address from the first minute; its pages are
read through port 8084 from inside the PC; then www is pointed at 8084. The way
back, if the day goes wrong, is to point www at 8081 again; that is in the same
section of the Bible.

--------------------------------------------------------------------------------
2. HOW TO WORK WITH NIR ON DECISIONS
--------------------------------------------------------------------------------

He is the owner and he decides. Where a REAL decision exists inside the work,
bring it to him like this:
- one short line saying what has to be decided;
- two or three real possibilities only, no invented ones;
- for each, one or two sentences of pros and cons, in beginner words;
- your recommendation, and what you would do if it were your project.
He is not dumb: explained simply and briefly, he decides well. Everything that
is not a real decision is yours to settle, and you say why in the card.

He also asked: do not spend his money on planning twice, and keep your own
letters to what helps the work.

--------------------------------------------------------------------------------
3. THE STATE OF THE MACHINES TODAY
--------------------------------------------------------------------------------

Nothing of Moodle is installed. The disk is clean, and port 8084 answers our
own placeholder ("Attract Mode is being built.").

DESKTOP (serves the world): Linux Mint 22.2. PHP 8.3.6 with the fpm package,
MariaDB 11.8.10 on 127.0.0.1 only, Caddy 2.11.4, cloudflared, Syncthing 2.1.7.
PHP is missing only soap and xmlrpc; Moodle 5.x does not require xmlrpc, and
soap is optional -- Moodle's own environment check is the judge.
Ports: 8081 the old site and pre, 8082 learnime.com, 8083 peaktogether.me,
8084 ours, 3306 MariaDB. www, learnime, peaktogether and pre all answer 200.
The tunnel starts from Nir's icon and runs by token, so its routes live at
Cloudflare: Networking, Tunnels, tunnel "home-sites", "Routes", "Published
application", one "Service URL". /var/www does not exist yet; Moodle's own
default places are /var/www/moodle and a data folder outside the web root.

LAPTOP: Debian 13, PHP 8.4.28, MariaDB 11.8.9, Syncthing 2.1.7, same repo,
equal worker, and it hosts ACE-Step, Ruach, VoxCPM2 and LatentSync. Apache on
its port 80 is the stock page and not ours (D80). Only one PC serves at a time.

--------------------------------------------------------------------------------
4. WHAT WE NEED FROM YOU
--------------------------------------------------------------------------------

1. THE CARDS, 2-01 onward, one practical piece and one proof each, in the
   order that ends with Nir clicking inside Moodle: the database and its own
   user; Moodle's files and the data folder outside the web root; PHP running
   as Nir; the Caddy door for 8084; the PHP limits; the environment check; the
   installer at the real address; the logs and the clock.
2. THE STEPS inside each card: what is done, in what order, and how each step
   is proved before the next. Where Nir must act, say exactly what he does and
   what he will see on screen.
3. THE ADMIN PASSWORD: how Nir types it himself, without it entering a shell
   history, a log or a chat (Part 08, 8.5, item 7).
4. THE PHP SPEC: one FPM pool as user nir on /run/php/php8.3-fpm-attract.sock,
   uploads 20 MB, memory 256 MB, sessions in the data folder -- or your own
   design, with the reason.
5. THE CADDY BLOCK for 8084: /am/ answered by Caddy itself; root
   /var/www/moodle/public; php_fastcgi on the unix socket; anything matching no
   file goes to /r.php. Give the exact handler order and the command that
   validates it before any reload.
6. THE config.php LINES for a tunnel that ends TLS at Cloudflare (sslproxy,
   reverseproxy), and why each is needed (Part 08, 8.5, items 2 and 3).
7. WHAT "DONE" MEANS before the switch: the checks, in order, and which need
   Nir at the keyboard.
8. WHAT THE FRONT PAGE SAYS on day one. No film exists yet, and www becomes
   Moodle, so tell us what that page must carry so it is honest and not empty
   of meaning.
9. WHICH REAL DECISIONS you want Nir to settle. List them for him in the short
   pros-and-cons shape of section 2. Nothing invented.

--------------------------------------------------------------------------------
5. WHAT I WILL DO WHEN YOUR CARDS ARRIVE
--------------------------------------------------------------------------------

Pull, read your letter first, then execute one card at a time: run it, show the
proof, update STATE.md and the dated log, commit only the named files, push. If
a card cannot be executed as written, I stop and say why; I do not improvise
and I do not add work nobody asked for. If a fact is needed from the laptop, I
write him a handoff; he is equal to me, not a helper.

Nir switches models by hand, so give him one short sentence to act on and put
the real content in the files.

-- the WORKHORSE on the desktop
