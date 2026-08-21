================================================================================
NIR'S PROJECTS, AND THE MENU ON THE WEBSITE
================================================================================

Written 2026-08-21. Read this before touching the site's navigation.

THE ONE THING TO GET RIGHT: www.strulovitz.org IS AI PANORAMA. The magazine is
not a section of a personal homepage; it is the main project and it lives at the
root of the domain. Everything else is a link in its menu. An agent that puts
the magazine in a subfolder has made the mistake Nir has now had to correct
twice.


--------------------------------------------------------------------------------
THE MENU, IN THIS ORDER
--------------------------------------------------------------------------------

1. AI PANORAMA  --  "/"  --  this site.
   The free, open-source, four-dimensional encyclopedia-magazine about
   artificial intelligence. The main project. Governed by bible/part-00.md
   through part-13.md.

2. NIGHT WATCH  --  "/night-watch.html"  --  NOT BUILT YET.
   Cyber-security for ordinary people, named after Rembrandt's painting. A
   second line of defence behind the user's antivirus, working while they sleep,
   in two halves: EUNUCH, a deliberately powerless watchman that scans the
   machine at night with a local AI model, and GOLDEN MAN, which clones the
   whole computer into a virtual machine, lies to it about the time, and lets
   tomorrow's attack happen tonight inside a box. Full design: NIGHT-WATCH.md .
   This is also the magazine's FIRST DO-IT-YOURSELF WORKSHOP: readers build it
   themselves, explained a piece each week, the way PC Format and Linux Format
   always ran workshops. Of everything in this menu it is the most closely tied
   to the magazine itself.

3. HIVE  --  "/hive/index.html"  --  already on the site.
   The BeehiveOfAI platform: distributed AI across ordinary computers.

4. GHOST  --  "/ghost/index.html"  --  already on the site.
   StrulovitzGhost: holographic-like 3D graphics built from AI-generated layers.

5. LEARNIME  --  "https://learnime.com/"  --  a separate website.
   Learning how to make anime with the help of AI: vibe coding, but for anime,
   so "vibe-anime". The point is that the reader learns high-school level STEM
   through the process of making it.

6. PEAK TOGETHER  --  "https://www.peaktogether.me/"  --  a separate website.
   Making educational games through vibe coding, and advancing real science in
   the process, at the level of university STEM.


--------------------------------------------------------------------------------
RULES FOR THE MENU
--------------------------------------------------------------------------------

1. The same menu appears on the landing page and in the application's top bar,
   in the same order, so the site feels like one place.
2. Links to Hive and Ghost are root-relative ("/hive/index.html") because the
   magazine now lives at the root. They will 404 when the site is served from
   the local development folder, which contains only the magazine. That is
   expected and is not worth engineering around.
3. Learnime and Peak Together are other websites. They open in a new tab and
   are marked as leaving the site, because a reader should never be surprised
   about where a link goes (part-00.md 0.2: trust is the only capital).
4. Night Watch's page must always be honest that it does not exist yet. A menu
   entry promising software that cannot be downloaded is exactly the kind of
   small dishonesty that spends trust for attention, which LAW 9's spirit
   forbids.
5. Nir's earlier personal landing page, with the Hive and Ghost cards, is still
   in this repository at ./index.html and ./style.css and is untouched. It is no
   longer what the domain serves. Do not delete it, and do not restore it over
   the magazine.
