STAGE 2 -- EXPERT TO WORKER (Moodle, in order)
date: 2026-11-28

Nir's order: Moodle at www, now. The Bible's own path (Part 08, 8.5 and Part
11, 11.5) is the plan; nothing else is added to it.

Execute in this order, one card at a time, each with its proof shown before the
next: 2-01 files and checksum, 2-02 database, 2-03 config.php and tables (Nir
types his own admin password in his own terminal), 2-04 PHP as Nir, 2-05 the
Caddy door and a reload, then 2-07 AT ONCE (D85: www is pointed at 8084 as soon
as the door answers -- nobody visits the old site, so there is nothing to
protect and no waiting), then 2-06 limits and a clean environment on the real
address, then 2-08 logs, clock and a guest front page.

D85 retires the "keep www on the old site until Moodle is finished" rule: it
protected nobody. The old site stays at pre.strulovitz.org.

Two facts settled from the makers' own pages on 2026-11-28, so nobody guesses:
- Moodle 5.3 requires MariaDB 11.4 or newer (public/admin/environment.xml), and
  this PC has 11.8.10.
- reverseproxy is NOT set from memory: setuplib.php refuses when reverseproxy is
  true and the request Host equals wwwroot's host. The request headers through
  the tunnel decide it, in 2-03 step 2.

Nir's acts, and only these: type the admin password (2-03), and change the
www Service URL at Cloudflare to localhost:8084 (2-07). Nothing else needs him.

Report after each card, and stop on any failure with the exact line, rather than
working around it.
