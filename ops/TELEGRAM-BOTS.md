THE TELEGRAM BOTS: WHO IS WHO, AND WHY
======================================

Written 2026-08-21 for Nir, in plain language.


THE SHORT ANSWER TO NIR'S QUESTION

Yes. One bot per computer. Nir's instinct was right.


WHY IT HAS TO BE THAT WAY (a genuine technical limit, not a preference)

A Telegram bot token can only be listened to by ONE program at a time. If two
computers used the same token, they would steal each other's messages at
random: Nir would ask the desktop something and the laptop would answer, or
the message would simply vanish. Telegram calls this a conflict and refuses.

So because each machine runs its own OpenClaw and its own OpenCode, each
machine needs its own bot token.

There is a happy side effect. A bot is a machine's MOUTH. When a message
arrives, the NAME of the bot tells Nir instantly which physical computer is
talking, before reading a single word. The Bible already relies on this idea:
"when an agent tells you on Telegram that Forge is overheating, you instantly
know which physical machine to look at, with zero technical vocabulary"
(bible/part-01.md, section 1.2).


THE MACHINE NAMES

Two names come from the Bible and are already used in every log and script:

ATLAS is the desktop. Atlas carries the world: the database, the truth, the
factory. It is the machine that must be on for a weekly build.

FORGE is the laptop. Forge makes things in fire: the graphics card, images,
transcription. It cannot be left running day and night.

Three names are proposed here for the machines the Bible does not mention:

BEACON is the old spare computer. A beacon is not powerful; it is simply
always lit. This is the machine that can be left running day and night, so it
is the natural home for the small tasks that must never be missed.

ATLAS-WIN and FORGE-WIN are the Windows sides of the two gaming machines.
Same physical box, different world, so the name says so.


THE BOTS TO CREATE, WITH NAMES

Each bot in Telegram needs two things: a DISPLAY NAME, which can be anything
and can be changed later, and a USERNAME, which must be unique across all of
Telegram and must end in the letters "bot". If a username is already taken,
add a short suffix such as a number or the letters "nir" and try again.

BOT 1 - the desktop Linux machine. Create this one first; it is the one that
matters for the magazine.
    Display name:  Atlas - Desktop Linux
    Username:      AtlasDesktopBot
    Its job:       the AI PANORAMA control room. The daily green or red
                   health message, approval requests, alerts, the weekly
                   build being ready to upload.

BOT 2 - the laptop Linux machine.
    Display name:  Forge - Laptop Linux
    Username:      ForgeLaptopBot
    Its job:       image generation and transcription progress, and anything
                   that needs the big graphics card.

BOT 3 - the old always-on computer. Create this only when it is given a job.
    Display name:  Beacon - Always On
    Username:      BeaconAlwaysOnBot
    Its job:       the small tasks that must never be missed, such as the
                   weekly price snapshot, so that they no longer depend on a
                   gaming computer happening to be switched on.

BOT 4 and BOT 5 - the two Windows sides. Create these only if and when Nir
actually wants an agent talking to him from Windows.
    Display name:  Atlas - Desktop Windows
    Username:      AtlasWindowsBot
    Display name:  Forge - Laptop Windows
    Username:      ForgeWindowsBot

A NOTE ON THE ORDER. There is no need to create all five today. Bot 1 alone is
enough to finish Milestone 0. Each extra bot is two minutes of work whenever
it is wanted.


THE ONE THING THAT IS NOT A BOT

The magazine also needs a PUBLIC CHANNEL: a read-only noticeboard where the
weekly digest and the weekly change video are posted automatically for
readers. That is a channel, not a bot, and it is completely separate from the
private bots above. Nobody can reply to it and it never carries approvals.

    Suggested channel name:  AI Panorama
    Suggested address:       @AIPanorama  (or @AIPanoramaMagazine if taken)

Keeping the public channel and the private control bots apart is a security
rule, not tidiness (bible/part-07.md, section 7.8).


HOW TO CREATE A BOT (two minutes, inside Telegram)

1. In Telegram, search for the user @BotFather and open a chat with it.
2. Send: /newbot
3. It asks for a display name. Send one of the display names above, for
   example: Atlas - Desktop Linux
4. It asks for a username. Send the matching username above, for example:
   AtlasDesktopBot . If it says the name is taken, try AtlasDesktopNirBot or
   similar until it accepts one.
5. It replies with a long token that looks like a row of digits, then a colon,
   then a long jumble of letters. THAT is the secret. Paste it to the agent
   once, and it goes into the .env file which git never touches.
6. Optional but nice: send /setuserpic to give the bot a picture, and
   /setdescription to write one line about what it is for.

THEN, ONE MORE THING, ONCE ONLY:
7. In Telegram, search for @userinfobot and send it any message. It replies
   with a number: Nir's own numeric user id. Paste that too.
   Why it is needed: each bot is locked so that it answers ONLY that number
   and stays completely silent for any stranger who finds it
   (bible/part-07.md, section 7.8.1). Without the number, the lock cannot be
   set.


WHAT HAPPENS IF A TOKEN EVER LEAKS

Message @BotFather, send /revoke, choose the bot. The old token dies
instantly and a new one is issued. Nothing else is affected, and because each
machine has its own token, a leak on one machine never touches the others.
That containment is the second reason for one bot per computer.
