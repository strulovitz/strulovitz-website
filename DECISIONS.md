NIR'S DECISIONS
===============

WHAT THIS FILE IS

The Bible (bible/part-00.md through part-13.md) is the law. Bible LAW 10 says
that when the code and the Bible disagree, the Bible wins, and that no agent
may silently "fix" the Bible. So when Nir makes a ruling that differs from
something the Bible says, the ruling is recorded HERE, dated, in plain words,
and the Bible text itself is left exactly as written.

Every agent working on this project reads this file together with Part 00.


DECISION 1 - THE REPOSITORY AND THE WEBSITE ARE ONE
Date: 2026-08-21
Decided by: Nir
Ruling: This repository keeps its name, strulovitz-website. It is not renamed
and no separate repository is created.

Nir's reasoning, in his own words: "ai-panorama" is the name of the MAGAZINE,
not the name of a repository. He does not have a separate website. This IS his
website, and it is now turning into this magazine. The site also carries links
to his other projects: the ones that live as pages on this same domain (the
Hive and the Ghost), and the ones that live on other domains (PeakTogether and
Learnime).

Which Bible text this touches: bible/part-01.md section 1.7 opens with the
words "One Git repository, named ai-panorama". Read that sentence as "one Git
repository, which is strulovitz-website". Everything else in section 1.7 - the
folder layout, the mirroring to the laptop, the GitHub-is-backup-only rule -
stands unchanged and is being followed exactly.

What this means in practice:
1. The magazine's machinery (bible, pipeline, site, comfy, exports, ops,
   schemas, config) lives in folders inside this existing repository.
2. The existing pages (index.html, hive/, ghost/, images/, style.css) are not
   touched, not moved, and not broken by any of this work.
3. strulovitz.org remains one website, whose front door leads both to the
   magazine and to Nir's other projects.


DECISION 2 - WHICH AI MODEL DOES WHICH WORK
Date: 2026-08-21
Decided by: Nir
Ruling: Expensive models are for hard and important work only. Simple work
goes to a cheaper model to save money.

How this is arranged: a helper agent called "grunt" is configured at
/home/nir/.config/opencode/agent/grunt.md and runs on Claude Sonnet 5. Its
instructions carry the parts of the Bible it is most likely to break by
accident. Claude Opus 5 keeps the design work: the four-dimensional
mathematics, the layout and projection code, the database model, the security
wrapping, prompt design, and anything touching an Iron Law.

This decision is not a compromise. Bible part-12.md section 12.5.3 already
demands it as the project's economics: a cheaper model that passes the quality
gate has earned the job.


DECISION 3 - EVERYTHING BIG LIVES ON THE HOME PARTITION
Date: 2026-08-21
Decided by: Nir
Ruling: Large and growing things go on the big disk.

The facts on Atlas, the desktop: the system partition has about 92 GB in total
with roughly 46 GB free. The /home partition has 1.7 TB with roughly 1.2 TB
free. There is also an external 3.6 TB drive that is 88 percent full and
formatted for Windows, which makes it unsuitable for the database.

Therefore every data folder that grows - the Neo4j database, the frozen source
text and transcripts, generated images, build exports, caches, model files -
is placed under /home/nir/ and never left at a package's default location
under /var. This is written into every runbook and into the grunt agent's
standing instructions, because installers will quietly try to do the wrong
thing.


HOW TO ADD TO THIS FILE

Append a new numbered decision. Never edit or delete an existing one; if Nir
changes his mind, add a new decision that says so and names the one it
replaces. Same discipline as the archive itself: history is added to, never
rewritten.


DECISION 4 - THE OLD SPARE COMPUTER IS NOT PART OF THIS PROJECT
Date: 2026-08-21
Decided by: Nir
Ruling: Nothing is to depend on the old spare computer, at all.

Nir's reasoning, in his own words: it is very old, he expects it to just stop
working soon, and he does not want to leave it on day and night. He does not
want to rely on it for anything.

An earlier suggestion to move the weekly price snapshot onto it, so that the
archive would not depend on the desktop being switched on, is WITHDRAWN. The
machine gets no name, no Telegram bot, and no job.

Why this costs us nothing: the weekly snapshot timer on Atlas is set with
catch-up turned on, so if the desktop was switched off on Monday the snapshot
runs as soon as it is next switched on. No week is lost, and no second machine
is needed to guarantee that.

Standing instruction to every future agent: do not propose using that
computer, and do not propose leaving any machine running day and night. Both
ideas were considered and ruled out here.


DECISION 5 - FOUR MACHINE NAMES, FOUR TELEGRAM BOTS
Date: 2026-08-21
Decided by: Nir
Ruling: The names are approved. Four bots, one for each operating system Nir
actually works in:

1. Atlas - Desktop Linux    @AtlasDesktopBot   (Linux Mint 22, the magazine's
                                                control room)
2. Forge - Laptop Linux     @ForgeLaptopBot    (Debian 13, the graphics card)
3. Atlas - Desktop Windows  @AtlasWindowsBot   (Windows 11 on the desktop)
4. Forge - Laptop Windows   @ForgeWindowsBot   (Windows 11 on the laptop)

Plus one separate PUBLIC read-only channel for readers, which is not a bot:
suggested @AIPanorama .

The name Beacon, proposed for the old spare computer, is dropped along with
the machine itself. See decision 4.

Why one bot per computer rather than one shared bot: a Telegram token can only
be listened to by one program at a time, so two machines sharing a token would
steal each other's messages. Full explanation and the two-minute creation
steps are in ops/TELEGRAM-BOTS.md .


DECISION 6 - THE REAL BOT USERNAMES (correcting decision 5's placeholders)
Date: 2026-08-21
Decided by: reality, accepted by Nir
Ruling: The plain usernames wanted in decision 5 were already taken by
strangers on Telegram, because a bot username must be unique across the whole
world. The real usernames therefore carry Nir's name in front, which also makes
them recognisably his. The DISPLAY NAMES stay the short friendly ones.

1. Atlas - Desktop Linux   display name "Atlas Desktop"   @NirAtlasDesktop_bot
   Created 2026-08-21, token stored in .env on Atlas, description set, live.
2. Forge - Laptop Linux    display name "Forge Laptop"    @NirForgeLaptop_bot
   Not created yet. Its token belongs in the .env on FORGE, not on Atlas.
3. Atlas - Desktop Windows display name "Atlas Windows"   @NirAtlasWindows_bot
   Not created yet.
4. Forge - Laptop Windows  display name "Forge Windows"   @NirForgeWindows_bot
   Not created yet.

Rule for whoever creates the remaining three: if a username is taken, append
digits (for example @NirForgeLaptop26_bot) and record the real one here. The
display name is set by the agent afterwards with the setMyName call, never by
asking Nir to type it, because that is exactly how the first bot ended up named
"@AtlasDesktopBot" with a stray @ sign.


DECISION 7 - PLAIN MACHINE NAMES. "ATLAS" AND "FORGE" ARE ABOLISHED
Date: 2026-08-21
Decided by: Nir
Ruling: The machines are named after what they plainly are. The poetic names
Atlas and Forge are dropped everywhere: in Telegram, in Tailscale, in the
runbooks, in the code comments, and in every message written to Nir.

Nir's reasoning, in his own words: "for me the atlas shit and forge shit is
meaningless. i only understand things like desktop and laptop, linux and
windows."

THE FOUR NAMES, AND THEY ARE THE SAME IN EVERY PLACE:
1. desktop-linux    the Linux Mint side of the desktop computer. The library
                    and the factory: Neo4j, the pipeline, the price archive.
2. desktop-windows  the Windows 11 side of the same desktop computer.
3. laptop-linux     the Debian side of the laptop. The graphics card work:
                    images through ComfyUI, speech-to-text through Whisper.
4. laptop-windows   the Windows 11 side of the same laptop.

Already applied on 2026-08-21: the Tailscale name of this computer, and the
Telegram bot's display name, are both now "desktop-linux" / "Desktop Linux".

WHAT CANNOT BE CHANGED, AND WHY IT DOES NOT MATTER: a Telegram bot's ADDRESS
is permanent once created, so the first bot keeps the address
@NirAtlasDesktop_bot even though it now displays as "Desktop Linux". Nir sees
the display name in every message; the address only appears when adding the
bot. If he ever wants the address to match too, the fix is to create a fresh
bot (for example @NirDesktopLinux_bot), paste its token, and abandon the old
one. His choice, not an agent's.

Which Bible text this touches: bible/part-01.md section 1.2 names the machines
ATLAS and FORGE, and later Parts use those words. The Bible text is NOT edited
(LAW 10). Read every "Atlas" in the Bible as "desktop-linux" and every "Forge"
as "laptop-linux".

STANDING INSTRUCTION TO EVERY AGENT: never invent a nickname, a codename, or a
metaphor for a machine, a script, or a folder that Nir has to learn. Name
things after what they plainly are. Nir does not read code and did not ask for
poetry; he asked for a magazine.


DECISION 8 - THE BOTS WERE REBUILT WITH PLAIN ADDRESSES
Date: 2026-08-21
Decided by: Nir
Ruling: All bots created earlier that day were deleted and are being rebuilt so
that the ADDRESS matches the plain machine name too, not only the display name.
Decision 6's usernames are therefore history; these are the real ones.

1. Desktop Linux    @NirDesktopLinux_bot     created 2026-08-21, live, its
                                             token is in .env on desktop-linux.
2. Laptop Linux     @NirLaptopLinux_bot      not created yet. Its token belongs
                                             in the .env on the LAPTOP only.
3. Desktop Windows  @NirDesktopWindows_bot   not created yet.
4. Laptop Windows   @NirLaptopWindows_bot    not created yet.

How this happened, recorded honestly because the lesson matters more than the
tidiness: an agent explained how to delete the old bot and put the words "make
the new one FIRST, then delete the old one" at the BOTTOM of the message. Nir
acts immediately and in the order written, so he deleted every bot he had. See
the communication rules at the top of SESSION-STATE-AI-PANORAMA.md, rule 4:
the important thing goes FIRST. This decision exists partly as a monument to
that rule.

WHO MAY COMMAND THIS COMPUTER: only Nir's numeric Telegram id, and nothing
else, ever (bible/part-07.md 7.8.1). Not a username, which can be given up and
claimed by a stranger; not a display name, which can be copied exactly. The
check lives in one function, is_owner() in pipeline/lib/telegram.py, and every
future listening ear must call it. A stranger gets SILENCE, never a refusal,
because a refusal advertises that something worth attacking is here.
As of 2026-08-21 nothing listens for incoming messages at all, so no one can
command the computer over Telegram - not even Nir. That ear arrives with
OpenClaw, and the guard is already waiting for it.


DECISION 9 - NO ARCHAEOLOGY. A PRICE LIST IS NOT A LEADERBOARD
Date: 2026-08-21
Decided by: Nir, after catching an agent publishing nonsense
Ruling: The magazine never presents a raw maximum, minimum or ranking taken
straight from a seller's catalogue. Every comparison must first be reduced to
what a reader could sensibly use TODAY.

What happened, recorded honestly because the lesson is the valuable part: an
agent asked the fresh price archive for "the most expensive models" and "the
biggest context windows" and repeated the answers to Nir as if they were news.
Nir immediately spotted that they were museum pieces and asked: "are you
building an archeology magazine for AI?" He was right. The data itself was
genuine and current - it contained Claude Fable at 10 dollars in and 50 out,
GPT-5.6 Sol Pro at 2.50 and 15, Grok 4.6, and Kimi K3 with a million-token
context, all correct. The QUESTION was defective, not the archive.

What the catalogue of 419 listings actually contained:
1. Five entries that are not models at all but ROUTERS which forward a request
   to whichever model they choose. Two of them advertise a two-million-token
   context that belongs to nothing you can point at.
2. Sixty-one "(batch)" entries, which are the same model at half price for
   slow work. They are a discount, not a model, and they double-count every
   family they appear in.
3. Fifty-four listings first published in 2024 or earlier, still purchasable,
   including o1-pro at 600 dollars per million words out - by far the most
   expensive number in the file, and completely irrelevant to a reader.
4. Superseded generations still on sale next to their successors, for example
   Grok 4.20 sitting beside Grok 4.6 while advertising a bigger context than
   the newer model. A date filter alone does not catch this; only knowing
   which listing is the current member of its family does.

THE RULES THAT FOLLOW, AND THEY APPLY TO EVERY COMPARISON THE SITE EVER SHOWS:
1. Routers, aliases and "auto" entries are never ranked against models. They
   are a separate kind of thing and get their own label.
2. Batch and discount variants never appear as separate competitors. They may
   appear as a second price attached to their own model.
3. Superseded models are shown as HISTORY, in the price-history view where they
   are genuinely interesting, and never in a "biggest" or "most expensive"
   list.
4. Every leaderboard states in plain words which listings it excluded and why.
   A number without its exclusions is not honest.
5. Nothing derived is ever written back over the archive. The archive keeps
   every listing forever, including the museum pieces: they are needed for the
   price-history dataset and they cost nothing to keep. The filtering happens
   when a question is asked, not when data is stored (LAW 12).

Which Bible text this reinforces: part-00.md ADVANTAGE 2, which already says
that one-dimensional benchmark reporting "hides the truths that matter", and
part-08.md, which separates IMPORTANCE from PROMINENCE. This decision is that
principle applied to the seller's catalogue, which is the first real data the
project ever touched.

STANDING INSTRUCTION: no agent may show Nir, or the public, a figure taken
straight from a source's list. State what was excluded, or do not publish the
figure.


DECISION 10 - ADVERTISING AND AFFILIATE LINKS ARE ALLOWED
Date: 2026-08-21
Decided by: Nir
Ruling: Advertising and affiliate links are allowed. Nir marks them clearly and
points them out honestly. The footer line about licences and "no advertising,
ever" is deleted from the site, with no replacement.

Nir's reasoning: "how do you say in the next line that this is to take care of
my girlfriend's future if you take away the main way of making money from this
project?"

This overrides part-00.md LAW 9's forbidden-income list. Two things from LAW 9
still stand, because they are what keeps the money coming: say plainly where a
link pays us, and never let money move a ranking or a benchmark number.

Agents: never add licence text or "no advertising" boasts to a page, and do not
add advertising either until Nir says so.


DECISION 11 - NIGHT WATCH COMES AFTER THE MAGAZINE
Date: 2026-08-21
Decided by: Nir
Ruling: The magazine itself gets built first. Night Watch comes afterwards.
NIGHT-WATCH.md stays as the written design and is not acted on. Its menu entry
and page stay, tagged "planned" rather than "soon", because nobody has promised
a date. No agent proposes starting it; Nir will say when.
