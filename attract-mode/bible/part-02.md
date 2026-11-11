NOTICE, 11 November 2026: by Nir's decision the "clean" rule
and the age rating are removed, and problem cards gain a part
letter and one property. The changes are written in Part 03,
section 3.1, and they win over the text below. Also changed by Part 04,
section 4.2.
================================================================================
ATTRACT MODE -- THE BIBLE -- PART 02 OF 11
THE VAULT
Version 1.0 -- 11 November 2026
Status: FOUNDATIONAL. Obeys Part 00 (as changed in Part 01, section
1.2) and Part 01.
================================================================================

HOW TO READ THIS PART

Part 02 defines the project's memory: the folder attract-mode/vault/ .
It says what kinds of file live there, the exact shape of each, and
the calculations made from them. Part 03 says how facts ARRIVE in the
vault. Part 04 says how a Level is DESIGNED from it. This Part owns
the shapes and the sums.

Every example in this Part shows FORMAT ONLY. The facts inside the
examples were written from memory and are not verified. No example is
ever copied into the vault.

This file is saved VERBATIM at: attract-mode/bible/part-02.md

--------------------------------------------------------------------------------
2.1 WHAT THE VAULT IS FOR
--------------------------------------------------------------------------------

The vault answers five questions that no model can answer reliably
from its own head:
1. Which ideas does this Boss need, all the way down to what a
   14-year-old knows?
2. Which game goes with which idea, so that no game and no idea is
   used twice?
3. How was this idea explained before, so that this time it is
   explained differently?
4. Which Level comes next?
5. What is missing, and therefore what should Nir search for next?

The vault is KITCHEN ONLY. The visitor never sees it as a map or a
graph. The visitor sees only what is made from it: the Levels, the
"next Level" button and the parent's door by school topic.

There is ONE vault, with one folder per field. The fields stay apart
(2.5, rule 3). The games are shared by all fields, because one game
hosts one Level in the whole project.

--------------------------------------------------------------------------------
2.2 HOW THE VAULT GROWS: FROM TWO SIDES
--------------------------------------------------------------------------------

FROM THE BOSS SIDE. A published competition problem comes in. Its
published solution is cut into steps. Each step names the IDEAS it
uses. Each idea names the ideas IT needs, and so on downward, until
everything rests on GROUND.

FROM THE GAME SIDE. Nir names a game. Research produces its dossier
(Part 03). From the dossier come HOOKS: moments in the game, each
tied to one idea.

The two sides meet at the ideas. A Level can be built wherever a
complete CHAIN exists:

    GAME -- HOOK -- IDEA -- BOSS

Where a chain is broken, the vault reports exactly what is missing
(2.17), and that report becomes Nir's next search.

--------------------------------------------------------------------------------
2.3 FOLDERS
--------------------------------------------------------------------------------

Inside attract-mode/vault/ :
1. maths/ideas/ , maths/topics/ , maths/problems/
2. physics/ , chemistry/ , biology/ , informatics/ -- each with the
   same three sub-folders.
3. humanities/ -- empty until Part 10 says what goes there.
4. games/     one card per game.
5. hooks/     one card per hook.
6. levels/    one card per Level.
7. made/      files written by SCRIPT only. Never edited by hand.
              The first line of each says so.
8. examples/  one golden example of each kind of card, written once
              by the EXPERT.
9. .obsidian/ the viewer's settings (2.20).

FIELD LETTERS, used at the start of ids:
m maths, p physics, c chemistry, b biology, i informatics,
h humanities.
"Informatics" is computer science. It is named after its olympiad,
and its letter does not clash with chemistry.

--------------------------------------------------------------------------------
2.4 RULES FOR EVERY CARD
--------------------------------------------------------------------------------

A CARD is one text file ending in .md .

1. SHAPE. At the top, a PROPERTIES block between two lines of three
   hyphens. Under it, the BODY.
2. ID. The id is the file name without ".md". Lowercase English
   letters, digits and hyphens only. An id never changes once another
   card links to it. Names shown to people can change; ids cannot.
3. FLAT. A property is a text, a number, true or false, or a list of
   texts. Never a value inside a value. (The viewer cannot show
   nested values, and cheap models break them.)
4. LINKS. A link is the other card's id inside double square
   brackets. Inside the properties block it is also wrapped in double
   quotes: "[[m-divisor]]" . In the body there are no quotes.
5. LINES WITH A SHAPE. Things with several parts (the steps of a
   route, the checkpoints of a Level) are written in the body, in
   exactly the line shapes shown in this Part.
6. Every card has the properties id, kind and state.
7. NOTHING COMPUTED IS TYPED. Tiers, loads, pairings, the campaign
   and the ledger are worked out by SCRIPT and written into made/ .
   No model types them into a card. (AM-LAW 7.)
8. SOURCES. A card says only what its sources say. The property
   "sources" lists web addresses or paths of research files.
9. NO CARD IS DELETED. A card leaves by a change of state.
10. Cards are created only with the command "am vault new" (2.19),
    which copies the golden example of that kind.
11. Cards are kitchen notes in plain English. Text meant for the
    public is never written in a card. It lives in the Level's
    workshop folder (Part 04).
12. Other Parts may add properties (a video address, a Moodle
    course). The list of allowed properties for each kind lives in
    one file of the line, so adding one is a one-line change by the
    EXPERT.

--------------------------------------------------------------------------------
2.5 THE IDEA CARD
--------------------------------------------------------------------------------

An IDEA is one thing a teenager can use after one checkpoint.
Folder: FIELD/ideas/ . Id: the field letter, a hyphen, a short name.

PROPERTIES:
1. id, kind (idea), field.
2. name -- the fixed public name. If school has a name for it, use
   school's name. Otherwise a plain name of at most four words that
   says what the idea does. The name never varies between Levels;
   only the explanation varies.
3. says -- ONE plain sentence stating the idea. No "and".
4. also-called -- other wordings, so that a search finds this card.
5. topic -- link to exactly one topic card of the same field.
6. ground -- true or false (2.11).
7. shaky -- true or false. Only for ground ideas: true means that
   struggling students usually do not hold it firmly.
8. needs -- links to the ideas this one stands on.
9. state -- proposed, approved or merged.
10. merged-into -- only when state is merged: link to the survivor.
11. maybe-same-as -- optional link, when the writer suspects a twin.
12. sources.

BODY: two short sections, "Why it is true" and "Where people slip".

RULES:
1. needs may link to ideas of the SAME field, or to GROUND ideas of
   any field. Nothing else.
2. needs lists only the direct supports, not everything underneath.
3. THE FIELDS STAY APART. If physics needs a piece of maths that is
   above ground, physics gets its OWN card for it, with its own
   explanations. It is not borrowed from the maths folder.
4. No loops: an idea never ends up needing itself.

EXAMPLE (format only):

    ---
    id: m-divides-the-difference
    kind: idea
    field: maths
    name: Divides the difference
    says: A number that divides two numbers also divides their difference.
    also-called:
      - common divisor of a difference
    topic: "[[m-topic-factors-and-multiples]]"
    ground: false
    shaky: false
    needs:
      - "[[m-divisor]]"
    state: approved
    sources:
      - research/maths/ideas/divides-the-difference.md
    ---
    ## Why it is true
    If 7 goes into 35 and into 21, both are piles of sevens. Take one
    pile from the other and what is left is still a pile of sevens.

    ## Where people slip
    They think it works for any two numbers, not only for two numbers
    that the divisor already divides.

--------------------------------------------------------------------------------
2.6 THE TOPIC CARD
--------------------------------------------------------------------------------

A TOPIC is a chapter name that a parent recognises from school:
"Fractions", "Forces". It is the parent's door.
Folder: FIELD/topics/ . Id: field letter, "-topic-", short name.

PROPERTIES: id, kind (topic), field, name, parent-line (one sentence
a parent would nod at), state (approved), sources.

Topic names are taken from the headings of the school programmes
named in 2.11, so that they are school's own words.

A Level is listed under every topic that one of its checkpoint ideas
belongs to, earliest checkpoint first.

EXAMPLE (format only):

    ---
    id: m-topic-fractions
    kind: topic
    field: maths
    name: Fractions
    parent-line: Simplifying, comparing and calculating with fractions.
    state: approved
    sources:
      - research/maths/ground/england-ks3.md
    ---

--------------------------------------------------------------------------------
2.7 THE PROBLEM CARD
--------------------------------------------------------------------------------

A PROBLEM is one published competition problem: a Boss candidate.
Folder: FIELD/problems/ . Id: field letter, competition code, year,
number. The competition codes are listed in one configuration file,
which Part 03 fills.

PROPERTIES:
1. id, kind (problem), field.
2. competition, year, number.
3. statement-source -- where the official statement is.
4. solution-source -- where the PUBLISHED solution is: an address,
   or a book and page in the big-files folder. Without it the card
   cannot leave the state "candidate". (AM-LAW 7.)
5. key -- link to the ONE idea that cracks the problem.
6. state -- candidate, routed, audited or set-aside.

BODY, three sections:
1. "Statement" -- the problem. Part 03 says when it may be quoted in
   full and when it is only linked.
2. "Route" -- the solution in OUR OWN plain words, as numbered steps.
   Each step is one line and ends with the word USES: and the links
   of the ideas that step uses. Part 04 owns how a route is written.
3. "Script check" -- optional: how a SCRIPT can test the claim on
   many cases.

EXAMPLE (format only):

    ---
    id: m-imo-1959-1
    kind: problem
    field: maths
    competition: imo
    year: 1959
    number: 1
    statement-source: (address of the official page)
    solution-source: (address, or book and page)
    key: "[[m-divides-a-combination]]"
    state: audited
    ---
    ## Statement
    Prove that the fraction (21n+4)/(14n+3) is irreducible for every
    natural number n.

    ## Route
    1. Suppose a number d divides the top and the bottom. USES: [[m-divisor]]
    2. Then d divides 3 bottoms minus 2 tops. USES: [[m-divides-a-combination]]
    3. That amount is always exactly 1, so d is 1. USES: [[m-expanding-brackets]]

    ## Script check
    For n from 1 to 100000, the greatest common divisor of 21n+4 and
    14n+3 is 1.

--------------------------------------------------------------------------------
2.8 THE GAME CARD
--------------------------------------------------------------------------------

A GAME card exists because Nir named the game. (AM-LAW 2.) Agents
create one at his word and never on their own.
Folder: games/ . Id: "game-" and the game's short name.

PROPERTIES:
1. id, kind (game), title, year, maker.
2. single-player -- must be true.
3. photo-mode -- true or false: can the game freeze and let the
   camera fly?
4. age-rating -- as printed by the rating board, from the dossier.
5. dossier -- path of the research folder for this game (Part 03).
6. chosen -- the date Nir named it.
7. state -- named, researched or set-aside.
BODY: Nir's own words about what struck him in this game, if he
said any.

EXAMPLE (format only):

    ---
    id: game-cyberpunk-2077
    kind: game
    title: Cyberpunk 2077
    year: 2020
    maker: CD Projekt Red
    single-player: true
    photo-mode: true
    age-rating: PEGI 18
    dossier: research/games/cyberpunk-2077/
    chosen: 2026-11-11
    state: researched
    ---
    Nir: the city at night in the rain.

--------------------------------------------------------------------------------
2.9 THE HOOK CARD
--------------------------------------------------------------------------------

A HOOK is one proposed connection: one moment in one game, tied to
one idea. A game may have many hooks. Only one becomes its Level.
Folder: hooks/ . Id: "hook-", the game's short name, the idea's id.

PROPERTIES:
1. id, kind (hook), game (link), idea (link).
2. link -- tech or story. (AM-LAW 3.)
3. department -- one name from the list of departments in the
   configuration. It must belong to the idea's field.
4. moment -- one sentence: what is on the screen.
5. where -- how Nir reaches that moment without playing well.
6. question -- the "How did they do that?" of this moment, in the
   words of someone looking at the screen.
7. honest-line -- the one sentence for the Credits that says what
   kind of connection this is. If it is a stretch, it says so.
8. seen, true, heart, toy -- four scores from 0 to 3 (below).
9. clean -- true or false (below).
10. sources -- the research files that support it.
11. nir -- none, yes or no. Nir's own word on this hook.
12. state -- proposed, audited or rejected.

THE FOUR SCORES.
SEEN -- can a stranger see it?
3: visible in a still picture, or in 20 seconds, with no skill.
2: visible within 40 seconds after a setup that a script can
   describe.
1: needs skill at playing, or long progress in the game.
0: cannot be shown on a screen.
TRUE -- how firm is the connection?
3: the makers said it in public, and we hold the source.
2: it is the standard, documented way that effects like this are
   made, and we hold the source. For a story link: the real science
   or history is solid, and we hold the source.
1: one informal source only.
0: nobody says so except an AI.
HEART -- is the idea the heart of the moment?
3: without the idea, the moment could not exist.
2: the idea is one of the main things at work.
1: the idea is there, but at the side. This is the STRETCH. It is
   allowed, and the honest-line must say it.
0: no connection.
TOY -- can a 14-year-old play with the idea?
3: an obvious toy: one thing to drag, or one or two sliders.
2: a toy is possible but needs care.
1: only something close to a quiz.
0: no toy can be imagined.

CLEAN. True when 20 to 40 seconds of this moment can be shown with
no gore, no sex or nudity, no drugs and no strong language, in
picture or in sound. The audience is 14 to 17 and a parent is
watching. If false, another MOMENT in the same game is looked for.
This rule never refuses a game.

A HOOK IS USABLE when: state is audited; no score is 0; true is 2 or
3; clean is true; nir is not "no"; the idea's state is approved; the
game is not set aside.
THE HOOK SCORE is seen + true + heart + toy. The most is 12.

WHO SCORES. The WORKHORSE writes the hook and scores it. An AUDITOR,
a different model, scores it again without seeing the first scores.
The lower number stands. If two numbers differ by 2 or more, or the
two disagree about clean, the hook goes to the EXPERT.

EXAMPLE (format only):

    ---
    id: hook-cyberpunk-2077-m-mirror-image
    kind: hook
    game: "[[game-cyberpunk-2077]]"
    idea: "[[m-mirror-image]]"
    link: tech
    department: graphics
    moment: A neon sign is reflected in a wet street at night.
    where: Any city street at night after rain. Use photo mode.
    question: How does a puddle know what the sign above it looks like?
    honest-line: Reflections like this are made by following light backwards from the eye. We show the principle, not this game's code.
    seen: 3
    true: 2
    heart: 3
    toy: 3
    clean: true
    sources:
      - research/games/cyberpunk-2077/dossier.md
    nir: none
    state: audited
    ---

--------------------------------------------------------------------------------
2.10 THE LEVEL CARD
--------------------------------------------------------------------------------

A LEVEL card records one Level: which hook, which Boss, and which
ideas its checkpoints teach, in order. The making of the Level (its
texts, toy and scenes) lives in the workshop folder
attract-mode/levels/NAME/ (Part 04). The card is the truth about the
Level's LINKS; the workshop is the truth about its CONTENT.
Folder: levels/ . Id: "level-" and the game's short name. That short
name is also the Level's NAME in its short link (Part 01, 1.4).

PROPERTIES:
1. id, kind (level).
2. hook -- link. The game, the HEADLINE IDEA, the link type and the
   department are all read from the hook. They are not typed again.
3. boss -- link to a problem card.
4. state -- planned, built, live or retired.

BODY: one block per checkpoint, in order. Each block has a heading
"Checkpoint" with its number, then these lines:
1. idea: -- ONE link. The idea this checkpoint teaches.
2. reminds: -- links to shaky ground ideas that are briefly
   refreshed here. May be empty.
3. told-by: -- two or three words naming the comparison or story
   used to explain the idea this time.
4. picture: -- what is drawn.
5. numbers: -- the main numbers used.
6. do: -- the one thing the teenager does at the end.
Part 04 owns how these are chosen. This Part owns their shape and
the checks on them.

EXAMPLE (format only, first checkpoint of several):

    ---
    id: level-cyberpunk-2077
    kind: level
    hook: "[[hook-cyberpunk-2077-m-mirror-image]]"
    boss: "[[m-example-1970-2]]"
    state: planned
    ---
    ## Checkpoint 1
    idea: [[m-equal-angles]]
    reminds: [[m-measuring-angles]]
    told-by: torch and bathroom mirror
    picture: a lamp, a flat mirror, an eye
    numbers: 30, 45, 60 degrees
    do: drag the lamp until the ray reaches the eye

--------------------------------------------------------------------------------
2.11 GROUND
--------------------------------------------------------------------------------

GROUND is what a 14-year-old is taught at school. (AM-LAW 4.) It is
decided by documents, not by a model's feeling.

THE REFERENCE DOCUMENTS. Named here from memory; Part 03 has Nir
fetch them and confirms the names:
1. England: the national curriculum programmes of study for key
   stage 3 (ages 11 to 14), in mathematics, science and computing.
2. United States: the Common Core State Standards for Mathematics
   up to grade 8; the Next Generation Science Standards for middle
   school; the CSTA computer science standards for grades 6 to 8.
Nir may swap or add documents. The list is in the configuration.

THE RULE. An idea is ground only if BOTH documents teach it by age
14. The card's sources quote the line from each. An idea found in
only one of them is NOT ground. It will simply sit very low.

SEED, THEN GROW.
1. SEED. For each field the EXPERT writes, once, the topic cards and
   the ground cards that almost every route will touch.
2. GROW. When a route reaches something that seems to be school
   knowledge and has no card, the WORKHORSE may add a ground card,
   but only with the two quoted lines. An AUDITOR checks the quotes
   against the documents.

SHAKY. Some ground ideas are taught by 14 and still not held by the
teenagers we serve: fractions, negative numbers, ratio. The EXPERT
marks these shaky: true. A shaky idea is never just assumed: the
checkpoint that first uses it refreshes it in a sentence or two with
a picture (the line "reminds:").

MATHS UNDER EVERYTHING. A ground idea of any field may be needed by
an idea of any other field. So ground maths lies under physics,
chemistry, biology and informatics without being copied.

--------------------------------------------------------------------------------
2.12 ONE IDEA: HOW BIG, AND WHEN TWO ARE THE SAME
--------------------------------------------------------------------------------

HOW BIG.
1. It fits in one plain sentence without "and" (the property "says").
2. A teenager can use it after one checkpoint.
3. If one step of a route needs two sentences to justify it, that is
   two ideas, or two steps.
4. A whole chapter ("fractions") is never an idea. It is a topic.

THE SAME OR NOT. Before any new idea card:
1. Run "am vault find" with the important words.
2. If an existing card says the same thing in other words, USE IT,
   and add the new wording to its also-called list.
3. If unsure, create the card with state proposed and a
   maybe-same-as link. The EXPERT decides these in batches. Deciding
   sameness is EXPERT work, always. (Part 00, 0.8.)
4. A proposed idea may appear in routes and hooks. Nothing that
   contains a proposed idea can be paired or built.
5. When two cards are merged, the loser stays as a file with state
   merged and a merged-into link. The command "am vault tidy" then
   points every link at the survivor.

--------------------------------------------------------------------------------
2.13 WHAT THE SCRIPT WORKS OUT
--------------------------------------------------------------------------------

All of this is written into made/ and never typed by a model.

1. TIER of an idea. Ground ideas are tier 0. Any other idea is one
   more than the highest tier among the ideas it needs.
2. UNDER an idea: everything it needs, and everything those need,
   down to ground.
3. LOAD of a problem. Take every idea used in its route, and
   everything under them. Count the ones that are NOT ground. That
   number is the load: how many new ideas a teenager must be given
   before the Boss.
4. ELIGIBLE BOSS. A problem whose state is audited and whose load is
   at most the LOAD LIMIT. The limit is 4 and lives in the
   configuration. It follows from the Level's shape: checkpoint 1 is
   ground, each later checkpoint teaches one idea, and a Level has
   at most five checkpoints. A problem over the limit is not wrong;
   it is too big to be a Boss, and its state becomes set-aside.
5. TIER of a Level: the highest tier among its checkpoint ideas.

--------------------------------------------------------------------------------
2.14 THE PAIRING
--------------------------------------------------------------------------------

The pairing decides which game gets which idea and which Boss. It is
one calculation, done by SCRIPT, proposed to Nir and decided by Nir.

A CHAIN is: a game, a usable hook of that game, the hook's idea, and
an eligible Boss whose route contains that idea.

WHAT IS LEFT OUT BEFORE THE SUM.
1. FROZEN. Every Level card that is not retired keeps its game, its
   headline idea and its Boss forever. The pairing never moves them.
2. FORCED. A hook with nir: yes ties that game and that idea
   together. Only the Boss is still chosen.
3. REFUSED. A hook with nir: no is never proposed again.

WHAT THE SUM LOOKS FOR, in this order:
1. The LARGEST number of chains in which no game, no idea and no
   Boss appears twice.
2. Among those, the highest total of CHAIN SCORES.
3. Among those, the first in alphabetical order of ids, so that the
   same vault always gives the same answer.

THE CHAIN SCORE is: the hook score; plus 3 if the idea is the Boss's
key; plus the FIELD BONUS; minus one tenth of the Boss's load.

THE FIELD BONUS. The configuration holds the share of Levels that
Nir wants for each science field. The default is equal shares. A
field that has fewer Levels than its share gets a bonus of up to 3
points, larger the further behind it is. Together with rule 1, this
does by calculation what "do the hard fields first" does by hand: a
game that could serve maths or biology goes to biology when biology
is short.

THE METHOD. This is a standard minimum-cost flow: from the games,
through the ideas, to the Bosses, each used at most once. The EXPERT
writes it once, with a tested library, and proves it on the test
vault (2.19). No model ever does this sum in its head.

WHAT NIR GETS. The file made/pairing.md : one numbered line per
proposed chain, with the game, the question, the idea's name, the
Boss, the link type and the score. Under it, what was left over and
why. Nir answers in plain words: "all yes", or the numbers he
refuses, or a pair he wants instead.
1. Yes: the hook gets nir: yes, and a Level card is created with
   state planned. From that moment the chain is frozen.
2. No: the hook gets nir: no.
3. "Game X goes with idea Y", at any time: if that hook exists, it
   gets nir: yes. If it does not, the WORKHORSE first writes it
   honestly: a real moment, real sources, and an honest-line that
   says so if it is a stretch. The score "true" must still reach 2,
   because however far the bridge stretches, every fact on both
   sides is sourced. (AM-LAW 3.)

The pairing runs when an agent is asked to run it, after new games
or new problems have come in. It never runs by itself.

Humanities chains have no Boss card. Part 10 says what stands in its
place.

--------------------------------------------------------------------------------
2.15 THE VARIETY LEDGER
--------------------------------------------------------------------------------

AM-LAW 6: a basic idea is explained again, freshly, in every Level
that needs it. The ledger is how "freshly" is made certain.

1. The truth is in the Level cards: each checkpoint block records
   told-by, picture and numbers.
2. The SCRIPT gathers, for each idea, every earlier telling, newest
   first, into made/ledger/ , one file per idea. The command
   "am ledger" prints the same.
3. BEFORE designing a checkpoint, the designer reads the ledger of
   its idea and of every idea in its "reminds:" line.
4. THE RULE. told-by must differ from the last FIVE tellings of that
   idea. numbers must differ from EVERY earlier telling of it.
   picture should differ from the last telling.
5. An AUDITOR judges whether two told-by lines are the same
   comparison in different words.
6. The idea's NAME and its "says" sentence never vary. The teenager
   meets the same name each time, in a new story.

--------------------------------------------------------------------------------
2.16 THE CAMPAIGN (THE "NEXT LEVEL" BUTTON)
--------------------------------------------------------------------------------

In a single-player game, the CAMPAIGN is the order in which the
levels are played. Each field has one campaign: an order of all its
live Levels. The "next Level" button follows it. There is no menu of
"more of the same idea": one button, chosen by the vault, so that
the teenager meets mostly familiar ideas plus a little that is new.

HOW THE ORDER IS MADE, for one field:
1. Start with the Level of the lowest tier. If several, the one with
   the fewest ideas above ground.
2. Keep a list, KNOWN, of every idea met so far.
3. The next Level is, among those not yet placed, the one with the
   best number of ideas not in KNOWN. Best is exactly 1; then 0;
   then 2; then 3; and so on.
4. Ties: the Level that shares more ideas with the one just placed;
   then the lower tier; then alphabetical order of ids.
5. Repeat until every Level is placed. After the last Level, the
   button leads back to the studio.

The order is worked out again whenever a Level goes live. It is the
same for every visitor. A personal order, from a signed-in player's
saved progress, is a later improvement and is not built now.

--------------------------------------------------------------------------------
2.17 THE REPORT: WHAT IS MISSING
--------------------------------------------------------------------------------

The command "am vault report" writes made/report.md and prints it in
plain words. Fields that are furthest behind their share come first.

1. GAMES WITHOUT A USABLE HOOK. Next step: more research on that
   game (Part 03).
2. IDEAS WITH A BOSS BUT NO GAME. Next step: a search, carried by
   Nir, for games that show an effect made with this idea. The
   results are leads. Nir alone decides which, if any, become game
   cards.
3. IDEAS WITH A GAME BUT NO BOSS. Next step: a search for a
   published competition problem that uses this idea, starting with
   the easier competitions.
4. FIELDS BEHIND THEIR SHARE.
5. PROPOSED IDEAS WAITING FOR THE EXPERT.
6. HOOKS WAITING FOR A SOURCE (the score "true" is 1).
7. Problems that are audited and unused. This is not a fault. It is
   the stock.

Each of lines 1, 2, 3 and 6 is turned into a research request in the
form that Part 03 defines.

--------------------------------------------------------------------------------
2.18 THE CHECKS
--------------------------------------------------------------------------------

The command "am vault check" runs all of these. Each failure is one
plain sentence that names the card and says what to do. A check may
be changed only by the EXPERT. (AM-LAW 9.)

EVERY CARD.
V1. The file name equals the id. The kind fits the folder. Every
    required property is there, and no unknown one.
V2. Every link points to an existing card of the right kind.
V3. Nothing is nested. Links in the properties block are quoted.

IDEAS.
V4. needs links only to the same field or to ground. No loops.
V5. A ground card quotes both reference documents and needs nothing
    that is above ground.
V6. Exactly one topic, of the same field.
V7. The name is unique within the field. "says" is one sentence.

PROBLEMS.
V8. Every route step ends with USES: and at least one link. The key
    appears in the route. From the state "routed" on, the card has a
    solution-source. The competition code is in the configuration.

HOOKS.
V9. The four scores are whole numbers from 0 to 3. The honest-line
    is there. Every source is a file that exists or an address. The
    department belongs to the idea's field.

LEVELS.
V10. One Level per game. One Level per headline idea. One Level per
     Boss. (Retired Levels do not count.)
V11. The Boss's route contains the headline idea.
V12. Three to five checkpoints. The idea of checkpoint 1 is ground.
V13. THE ORDER CHECK. Everything that a checkpoint's idea needs is
     either ground or the idea of an EARLIER checkpoint of the same
     Level. A Level never leans on another Level.
V14. THE COVER CHECK. Every idea above ground that the Boss needs is
     the idea of some checkpoint. Nothing is used at the Boss that
     was not taught on the way.
V15. THE REMIND CHECK. Every shaky ground idea that the Level uses
     appears in a "reminds:" line at or before its first use.
V16. THE LEDGER CHECK. The rule of 2.15, item 4.
V17. The headline idea is the idea of one of the checkpoints.
V18. A Level can be "live" only if its hook is audited, its Boss is
     audited, and all its ideas are approved.

V13 and V14 together are what turn AM-LAW 4 and AM-LAW 6 from good
intentions into something a script can refuse.

--------------------------------------------------------------------------------
2.19 THE COMMANDS
--------------------------------------------------------------------------------

Added to the single command "am" (Part 01, 1.10):
1. am vault new KIND ID -- creates a card from the golden example.
2. am vault find WORDS -- searches names, "says" lines and
   also-called lists; prints the nearest cards.
3. am vault check -- runs the checks of 2.18.
4. am vault tidy -- repairs FORM only: quotes, order of properties,
   links to merged cards. It never changes meaning.
5. am vault report -- works out everything in 2.13, the ledger and
   the campaigns, writes made/ , and prints what is missing.
6. am pair -- works out the pairing and writes made/pairing.md .
7. am ledger ID -- prints the earlier tellings of one idea.

THE TEST VAULT. Inside the line's tests lives a tiny invented vault
of about twenty cards, with the right answers for tier, load,
pairing and campaign written beside it by the EXPERT. The scripts
must reproduce those answers exactly before they are trusted on the
real vault, and again after every change to them.

--------------------------------------------------------------------------------
2.20 THE VIEWER (OBSIDIAN)
--------------------------------------------------------------------------------

1. Obsidian opens the folder attract-mode/vault/ as it is. Checked
   on 11 November 2026 in Obsidian's own help: properties may be
   text, list, number, checkbox or date; a link inside a property
   must be in quotes; nested properties are not supported. Links in
   properties are reported to appear in the graph and in backlinks.
2. Its settings folder .obsidian/ is in Git, so that both PCs show
   the same colours: one colour per kind of card, by folder. The
   files that remember window positions are kept out of Git.
3. To see one field alone, type its folder in the graph's filter,
   for example path:maths .
4. No community plugins. Nothing in the line may depend on Obsidian.
   If it vanished tomorrow, nothing would break.
5. Nir LOOKS in Obsidian. Changes are made by agents, through the
   commands, so that the checks always run.

--------------------------------------------------------------------------------
2.21 WHO DOES WHAT
--------------------------------------------------------------------------------

1. EXPERT: the golden example cards; the scripts and the test vault;
   the topic cards and the seed of ground for each field; marking
   shaky; approving and merging ideas; the first routes of each
   field (Part 04); the checkpoints of each Level (Part 04);
   settling hook scores that the two scorers dispute.
2. WORKHORSE: game cards at Nir's word; hook cards from dossiers;
   candidate problem cards from intake (Part 03); later routes, from
   the golden ones (Part 04); new ground cards with their two quotes.
3. AUDITOR: second scoring of hooks; checking quotes of ground
   cards; judging sameness of told-by lines.
4. SCRIPT: everything in 2.13 to 2.19.
5. NIR: names the games; answers the pairing; may force or refuse
   any pair at any time.

--------------------------------------------------------------------------------
2.22 DONE MEANS
--------------------------------------------------------------------------------

Part 02 is built when all of these are true:
1. The folders of 2.3 exist, with a golden example of each of the
   six kinds of card in examples/ .
2. The seven commands exist and reproduce the test vault's answers.
3. For maths: the topic cards and the seed of ground exist, each
   ground card quoting both reference documents.
4. "am vault check" passes on the real vault, and fails, with a
   plain sentence, on each of a set of deliberately broken cards.
5. Obsidian opens the vault on both PCs with the same colours.
How many problems, games and Levels come first is Part 11's
business, not this Part's.

--------------------------------------------------------------------------------
2.23 NOT DECIDED HERE
--------------------------------------------------------------------------------

1. How facts, books, dossiers and problem statements arrive, and
   what may be quoted -- Part 03.
2. How a route is cut from a published solution, and how
   checkpoints are chosen -- Part 04.
3. The workshop folder of a Level -- Part 04.
4. The footage and the video address -- Part 06.
5. How Levels, departments and topics appear in Moodle -- Part 08.
6. Humanities cards -- Part 10.

--------------------------------------------------------------------------------
2.24 WORDS ADDED TO THE GLOSSARY
--------------------------------------------------------------------------------

1. CARD -- one text file in the vault.
2. TOPIC -- a school chapter name; the parent's door.
3. HOOK -- one moment in one game, tied to one idea.
4. CHAIN -- game, hook, idea and Boss that fit together.
5. ROUTE -- a published solution retold in our own numbered steps.
6. KEY -- the one idea that cracks a problem.
7. SHAKY -- a ground idea that is taught by 14 but not held firmly.
8. TIER -- how many layers of ideas lie between an idea and ground.
9. LOAD -- how many ideas above ground a problem needs.
10. THE PAIRING -- the calculation that proposes the chains.
11. FROZEN, FORCED, REFUSED -- the three ways a chain is fixed.
12. TELLING -- one explanation of one idea in one Level.
13. CAMPAIGN -- the order of a field's Levels.
14. TEST VAULT -- the tiny invented vault with known answers.

================================================================================
END OF PART 02
================================================================================
