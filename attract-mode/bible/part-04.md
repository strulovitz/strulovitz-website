================================================================================
ATTRACT MODE -- THE BIBLE -- PART 04 OF 11
LEVEL DESIGN
Version 1.0 -- 11 November 2026
Obeys Parts 00 to 03, with their notices and with section 4.2 below.
================================================================================

HOW TO READ THIS PART

This Part says how one Level is designed. It is built around ONE
WHOLE EXAMPLE, in section 4.3. Read the example first. The rules
after it only say, in order, what the example already shows.

The example shows FORMAT ONLY. Its game and its competition problem
are placeholders, and nothing in it is a verified fact.

This file is saved VERBATIM at: attract-mode/bible/part-04.md

--------------------------------------------------------------------------------
4.1 WHAT A LEVEL IS MADE OF
--------------------------------------------------------------------------------

A Level is four things, side by side in one section of a Moodle
course.

1. THE ATTRACT. Nir's clip of the game moment, ending on the
   question. On YouTube. Free.
2. THE GUIDE. Pages of text that the visitor reads by pressing
   Next. One SCORM package. Free. THE GUIDE IS THE LEVEL:
   everything else leans on it, and it must work alone.
3. THE WALKTHROUGH. A film made with Manim: the Guide, drawn and
   spoken. On YouTube. Free.
4. THE CHALLENGE. One SCORM package with a fixed set of questions.
   Moodle saves the score. Where a toy exists, the Challenge opens
   with it. Paid.

Watching and reading are free. Doing and being scored are paid.

A Level goes LIVE when its Attract, Guide and Challenge exist and
pass their checks. The Walkthrough and the toy are added when they
pass theirs. A Level never waits for them.

Why this shape: the people who build Levels day by day are a cheap
model and a middle-priced model. Text is what they do reliably.
Pictures, films and toys are extras that may fail without taking
the Level down with them.

--------------------------------------------------------------------------------
4.2 WHAT WE DECIDED, AND WHAT IT CHANGES
--------------------------------------------------------------------------------

Added to attract-mode/DECISIONS.md :

Decided by Nir, 11 November 2026:
D13. The Guide and the Challenge are SCORM packages. Nir uploads
     them to Moodle.
D14. The text carries the Level. Pictures are extras. In a science
     Level, nothing is drawn by an image-generating model.
D15. Films stay outside the packages, on the course page.
D16. The Challenge has a fixed set of questions, the same for
     everyone. No shuffling, no question bank.
D17. There is no "break" switch.
D18. The work done for every Level must be within reach of a cheap
     model and a middle-priced model.

Chosen for Nir by the author of this Part; Nir may reverse any:
D19. Free: Attract, Guide, Walkthrough. Paid: Challenge, with the
     toy inside it.
D20. A Level goes live without waiting for its film or its toy.
D21. The public names are Guide and Challenge.
D22. The Walkthrough speaks the Guide's own text.
D23. Informatics Levels show no program code.

CHECKED ON 11 NOVEMBER 2026, in Moodle's own documentation: Moodle
supports SCORM version 1.2 and not SCORM 2004. Our packages are
SCORM 1.2.

CHANGES TO EARLIER PARTS. Where they disagree with this section,
this section wins.
1. Part 00, section 0.5: a Level's pieces are those of 4.1. The
   checkpoints live inside the Guide.
2. Part 00, section 0.7, and Part 01, section 1.2, item 2: what is
   free and what is paid is as in 4.1. Toys are no longer free.
3. AM-LAW 5 now reads: "EXAMPLE FIRST. Every idea is shown working
   on plain numbers before it is named. Every checkpoint ends with
   something to do."
4. AM-LAW 15: the public words also include Guide and Challenge.
5. Part 00, section 0.13: Part 05 is named "The Kits: pages,
   pictures and toys".
6. Part 01, section 1.4: the path /am/toy/ is not used. A toy
   lives inside its Challenge package.
7. Part 02, section 2.10: the line "picture:" holds the name of a
   ready picture, or "none". The line "do:" holds the try
   question.

THE NOTICES. In the notices at the top of part-00.md , part-01.md
and part-02.md , the first agent adds one sentence: "Also changed
by Part 04, section 4.2."

--------------------------------------------------------------------------------
4.3 THE WHOLE EXAMPLE
--------------------------------------------------------------------------------

One Level, from the competition problem to the questions. Game: a
city at night in the rain (placeholder). Boss: two villages and a
river (placeholder).

A. THE ROUTE. The published solution, retold in small steps. It
sits on the problem card (Part 02, 2.7).

    ## Statement
    Two villages, A and B, stand on the same side of a straight
    river. A pump is to be built on the bank, with a straight pipe
    to each village. Where must the pump stand so that the two
    pipes together are as short as possible?

    ## Route
    1. Put a twin of B across the river, as far behind the bank as B is in front. USES: [[m-mirror-image]]
    2. From any spot on the bank, the twin is exactly as far away as B. USES: [[m-same-distance]]
    3. (fill) So the two pipes together are as long as the path from A to the pump to the twin. USES: [[m-same-distance]]
    4. The shortest path from A to the twin is the straight line. USES: [[m-straight-is-shortest]]
    5. So the pump stands where that line crosses the bank. USES: [[m-straight-is-shortest]]

B. THE PLAN. One form, filled in. It decides everything.

    # PLAN level-example

    ## Bridge
    moment: A neon sign is reflected in a wet street at night.
    job: Find the spot on the street where light from the sign bounces into the eye.
    idea: [[m-mirror-image]]
    machine: Give every point of the sign a twin under the street, and draw the twins.

    ## Checkpoint 1
    idea: [[m-equal-angles]]
    reminds:
    told-by: steep in, steep out
    picture: bounce
    numbers: lamp 3 up, eye 1 up, 8 apart
    do: lamp 4 up, eye 2 up, 12 apart; where is the bounce spot?
    slip: choosing the middle
    new-words: bounce spot

    ## Checkpoint 2
    idea: [[m-mirror-image]]
    (the same eight lines)

    ## Checkpoint 3
    idea: [[m-same-distance]]
    (the same eight lines)

    ## Boss
    costume: The river bank is the mirror. Village B gets the twin.
    close: The puddle and the pump are the same trick.

    ## Extras
    toy: none

C. THE GUIDE. The pages as the visitor reads them. There is no
picture on any page, and none is needed.

    PAGE 1 -- QUESTION
    A wet street at night. A neon sign hangs above it. In the
    puddle you see the sign again, upside down. Nobody painted
    that puddle by hand. The game works it out, many times every
    second. How does the puddle know what the sign looks like?

    PAGE 2 -- JOB
    Make it smaller: one lamp instead of a whole sign. Light
    leaves the lamp, hits the wet street and bounces into your
    eye. The job is to find the spot on the street where the
    bounce happens. Do that for every point of the sign, and you
    have the reflection.

    PAGE 3 -- SEE (checkpoint 1)
    The lamp hangs 3 metres above the street. Your eye is 1 metre
    above the street. Along the street, they are 8 metres apart.
    Try a spot 4 metres from the lamp. The light comes down 3
    metres over 4 metres of street. Then it must climb only 1
    metre over the next 4. Steep in, flat out. Light does not
    bounce like that.

    PAGE 4 -- SEE (checkpoint 1)
    Try a spot 6 metres from the lamp. The light comes down 3
    metres over 6 metres of street. That is 1 down for every 2
    along. Then it climbs 1 metre over the last 2 metres. That is
    1 up for every 2 along. The same steepness in and out. This is
    the spot.

    PAGE 5 -- NAME (checkpoint 1)
    EQUAL ANGLES
    Light leaves a flat mirror at the same angle it arrived.

    PAGE 6 -- TRY (checkpoint 1)
    A lamp hangs 4 metres up. An eye is 2 metres up. They are 12
    metres apart. How far from the lamp is the bounce spot? Think
    first. Then press Next.

    PAGE 7 -- ANSWER (checkpoint 1)
    8 metres. Down 4 over 8 is 1 for every 2. Up 2 over the last 4
    is 1 for every 2.

    PAGE 8 -- SEE (checkpoint 2)
    Trying spots is slow. Here is a trick. Imagine a twin lamp
    under the street. It sits straight below the real lamp, 3
    metres down. Draw a straight line from your eye to the twin.
    The line drops 4 metres in all: 1 metre to the street, then 3
    more. It does that over 8 metres. That is 1 down for every 2
    along.

    PAGE 9 -- SEE (checkpoint 2)
    So the line reaches the street after 2 metres. That is 6
    metres from the lamp. The same spot as before, and nothing was
    tried.

    PAGE 10 -- NAME (checkpoint 2)
    MIRROR IMAGE
    A thing in front of a flat mirror appears as far behind the
    mirror as it really is in front.

    PAGES 11 AND 12 -- TRY and ANSWER (checkpoint 2)

    PAGE 13 -- MACHINE
    Now the whole sign. A sign is thousands of points of light.
    Give each point its twin under the street. Together the twins
    make the sign again, upside down. Reflections like this one
    can be made that way.

    PAGE 14 -- SEE (checkpoint 3)
    Draw the lamp, the street and the twin on paper. Fold the
    paper along the street. The twin lands exactly on the lamp. So
    from any spot on the street, the way to the twin is as long as
    the way to the lamp.

    PAGE 15 -- NAME (checkpoint 3)
    SAME DISTANCE
    From any spot on a flat mirror, a thing and its twin are
    equally far away.

    PAGES 16 AND 17 -- TRY and ANSWER (checkpoint 3)

    PAGE 18 -- BOSS: PROBLEM
    Now a problem from a real competition. (Its name, year and
    number.) Two villages, A and B, stand on the same side of a
    straight river. One pump will be built on the bank, with a
    straight pipe to each village. Where must the pump stand so
    that the pipes together are as short as possible? You can stop
    here and look for the idea yourself.

    PAGE 19 -- BOSS: STEP 1 (met at checkpoint 2)
    Treat the river bank as a mirror. Give village B a twin across
    the river, as far behind the bank as B is in front.

    PAGE 20 -- BOSS: STEP 2 (met at checkpoint 3)
    From any spot on the bank, the twin is exactly as far away as
    B.

    PAGE 21 -- BOSS: STEP 3 (met at checkpoint 3)
    So the two pipes together are always as long as the path from
    A to the pump to the twin.

    PAGE 22 -- BOSS: STEP 4
    The shortest path from A to the twin is a straight line.

    PAGE 23 -- BOSS: STEP 5
    Build the pump where that line crosses the bank. The puddle
    and the pump are the same trick. Every idea in this solution
    was met at a checkpoint.

    PAGE 24 -- CREDITS

In the file, the writer does not type "3 metres". It types
"{lamp-up} metres", and a script fills in the number (4.10).

D. THE CHALLENGE. Three of its eight questions.

    QUESTION 1 -- NUMBER (checkpoint 1)
    A lamp hangs 2 metres up. An eye is 1 metre up. They are 9
    metres apart. How far from the lamp is the bounce spot, in
    metres?
    Right answer: 6

    QUESTION 3 -- PICK (checkpoint 2)
    A lamp hangs 3 metres above a puddle. How far below the puddle
    is its twin?
    A. 3 metres. (Right.)
    B. 6 metres. "That is the distance from the lamp to its twin."
    C. 1.5 metres. "That is half the height. The twin is as deep
       as the lamp is high."
    D. 0 metres. "That is the puddle itself. The twin lies below."

    QUESTION 7 -- SPOT (Boss)
    Step 2 says that the twin is as far from the bank as village B
    is. Which idea is that?
    A. Equal angles.  B. Mirror image.  C. Same distance. (Right.)
    D. Straight is shortest.

--------------------------------------------------------------------------------
4.4 WHO DOES WHAT
--------------------------------------------------------------------------------

ONCE, for the whole project. This is worth a few sittings of the
strongest model Nir can afford:
1. The forms: the shapes of the plan, the Guide and the Challenge.
2. One golden example of each, complete and checked.
3. The scripts and the checks.
4. For each field, its FREE LIST (4.5, rule 4).

FOR EVERY LEVEL:
1. THE PLANNER. The EXPERT role; on a normal day, a middle-priced
   model. It fills in the plan and writes the numbers file.
2. THE WRITER. The WORKHORSE role; a cheap model. It writes the
   Guide, the Challenge and Nir's lines, from the plan.
3. THE AUDITOR. Another cheap model, never the one that wrote.
4. THE SCRIPT. Fills in numbers, builds the packages, runs the
   checks.
5. NIR. Nothing in design.

THREE PROMISES TO THE WRITER. It never types a number. It never
draws. It never writes code. It writes sentences into a form.

ONE RULE FOR THE WRITER. If it finds that it must DECIDE something
(which number, which example, which order), the plan is
incomplete. It stops and sends the plan back.

--------------------------------------------------------------------------------
4.5 THE ROUTE
--------------------------------------------------------------------------------

A route is the published solution, cut into smaller steps and told
in our own words. It is never a new solution. (Example: 4.3, A.)

Before starting, the command "am route brief ID" gathers the
pictures of the pages, the typed statement and the list of the
field's ideas. The published solution is read from the picture.

1. OWN WORDS. No sentence is copied from the published solution.
2. ONE STEP IS ONE MOVE: one sentence of at most 25 words.
3. EVERY STEP NAMES ITS IDEAS. It ends with USES: and the links.
   At most two. If a step needs three, it is two steps.
4. THE FREE LIST. Counting, and the four operations on whole
   numbers and decimals, need no card. Each field has its free
   list in the configuration. Everything else is an idea.
5. NO SKIPPED MOVE. Published solutions say "clearly" and jump. We
   do not. A route never contains: clearly, obviously, it follows,
   similarly, easy to see.
6. A step that we added, because the published solution skipped
   it, begins with (fill). Mistakes hide in fills.
7. The last step states the published answer.
8. THE KEY is the one idea that, told to a stuck solver, lets them
   finish with routine moves.
9. Where the answer can be tested by calculation, the card says
   how, under "Script check".

THE DESCENT. Every idea in the route needs a card. For each one:
find it with "am vault find"; if it is not there, create it as
"proposed"; then ask what a person must already hold for it to
make sense. Those are its needs. Repeat until everything rests on
ground or on the free list. STOP when a fifth idea above ground
appears: the problem is too big for a Boss, and its state becomes
set-aside (Part 02, 2.13).

A ROUTE IS AUDITED WHEN:
1. FAITHFUL. An auditor that can see the page compares route and
   published solution. Every step without (fill) matches a
   published move, and the answer is the same.
2. NO GAPS. A second auditor gets only the statement, the route,
   the free list and each linked idea's one sentence. It is told
   to use nothing else. For each step it answers FOLLOWS, or NEEDS
   and what. A NEEDS means one more step or one more idea.
3. THE SCRIPT AGREES, where there is a script check.

--------------------------------------------------------------------------------
4.6 THE PLAN
--------------------------------------------------------------------------------

The plan is one form (example: 4.3, B). The command
"am level brief NAME" first writes ONE file with everything the
planner needs: the hook, the lines of the dossier about this
moment, the Boss with its route, every idea under it with its
sentence and its slips, the ledger of those ideas, and the golden
plan.

THE BRIDGE. Four lines lead from the game to the idea:
1. moment -- what is on the screen.
2. job -- what somebody, or some machine, must DO for that moment
   to exist. One sentence starting with a verb. For a story link
   it is nature's or history's job.
3. idea -- the headline idea, which is how the job gets done.
4. machine -- how the idea, repeated, makes the moment.
If the planner cannot write the job in one sentence, the idea is
not at the heart of the moment. Then the hook is a stretch, and
the plan says so; or the chain is refused (4.13).

THE CHECKPOINTS.
1. Three to five. Each teaches ONE idea.
2. Checkpoint 1 teaches a ground idea that the job leans on.
3. Every idea above ground that the Boss needs gets a checkpoint,
   lowest first. (Part 02, checks V13 and V14.)
4. For each checkpoint the planner fills eight lines: idea,
   reminds, told-by, picture, numbers, do, slip, new-words.
5. told-by and numbers must differ from earlier Levels. The ledger
   says what was used (Part 02, 2.15).
6. At most two new words in a checkpoint.
7. "picture" is the name of a ready picture, or none (4.8).

THE BOSS. Two lines: costume (where the headline idea hides in the
problem) and close (one honest sentence).

EXTRAS. "toy:" names a ready toy from the kit, or none (Part 05).

A STRETCH IS SAID ONCE. If the hook's heart score is 1 (Part 02,
2.9), the plan adds one light sentence for the MACHINE page,
saying that this idea is a side door into the scene.

--------------------------------------------------------------------------------
4.7 THE GUIDE
--------------------------------------------------------------------------------

The Guide is the file guide.md : a list of pages. Each page has a
KIND. The kinds come in a fixed order (example: 4.3, C).

1. QUESTION. One page. The moment in words, ending with the hook's
   question.
2. JOB. One page. The job, made small.
3. For each checkpoint, in order:
   SEE -- one or two pages. The idea at work on plain numbers.
   NAME -- one page. The idea's name and its one sentence, put in
           by SCRIPT from the idea card, word for word.
   TRY -- one page. One question. "Think first. Then press Next."
   ANSWER -- one page. The answer and its working.
4. MACHINE. One page, right after the checkpoint of the headline
   idea. How the idea, repeated, makes the game moment.
5. BOSS: PROBLEM. One page. Where the problem comes from; the
   statement; the offer to stop and think.
6. BOSS: STEP. One page for each step of the route, in the route's
   order, worded for a reader. The SCRIPT adds the tag that says
   at which checkpoint its idea was met.
7. The last STEP page ends with the plan's "close" sentence.
8. CREDITS. Made by SCRIPT: the game; the hook's honest-line; the
   problem with its link; the sources; the licence; the "report a
   mistake" link.

A shaky ground idea (Part 02, 2.11) is refreshed in one or two
sentences on the SEE page that first uses it.

THE TEXT STANDS ALONE.
T1. The Guide must be understood with every picture removed.
T2. Say where things are in numbers and plain directions: above,
    below, along, left, right.
T3. The text never points at a picture. It never says: as shown,
    in the picture, the figure, the diagram. It never names
    something by its colour.
T4. A page has at most 80 words and one thought.
T5. A sentence has at most 20 words.

THE VOICE.
V1. Nir's voice says "I" and "you": one curious person talking to
    another.
V2. Never said: obviously, clearly, simply, just, easy, trivial,
    of course, as you know.
V3. No school words: lesson, class, homework, exercise, student.
V4. From its NAME page on, an idea is called by its name only.
V5. Numbers before letters: show a rule twice with plain numbers
    before writing it once with a letter.
V6. Honest praise only. We never say "you solved it" to somebody
    who read, and we never call anything easy.
V7. Nothing from above: no word about what advanced students do.
V8. "Like this": we say how effects like this are made. We say
    what this game does only where a maker claim says so.
V9. In maths, "tried" is not "proved". Trying many cases is called
    trying.

--------------------------------------------------------------------------------
4.8 PICTURES
--------------------------------------------------------------------------------

A picture is an extra. There are two kinds, and no third.

1. A READY PICTURE. The kit (Part 05) holds a small list of
   pictures that a script draws from numbers: for example a number
   line, a grid, a triangle, a bounce. The planner writes the name
   of one. The script draws it from the Level's numbers, so its
   lines are exactly where the numbers say.
2. A PHOTO from Wikimedia Commons. It is copied into the package,
   with its author, its licence and its address written in the
   Credits. It is found through research (Part 03).

NEVER, in a science Level: a picture made by an image-generating
model. Such a model paints what looks right. A diagram must BE
right. Nir's own laser experiment showed it: the painted bounce
could not be trusted, and the computed one was exact.

If no ready picture fits, the page has no picture. If a picture
fails its check, it is left out. The Level does not wait.

A picture never holds information that the text lacks.

--------------------------------------------------------------------------------
4.9 THE CHALLENGE
--------------------------------------------------------------------------------

The Challenge is the file challenge.md : a fixed list of questions
(example: 4.3, D).

1. HOW MANY. Two for each checkpoint, and two for the Boss. The
   numbers are in the configuration.
2. THREE KINDS.
   NUMBER -- type a number.
   PICK -- choose one of four.
   SPOT -- a Boss step is shown; which idea does it use? The
   SCRIPT makes these from the cards.
3. A checkpoint's questions ask the teenager to USE its idea on
   fresh numbers. They never ask about the game.
4. We never ask the teenager to solve the Boss.
5. EVERY RIGHT ANSWER is worked out by the numbers file.
6. WRONG ANSWERS ARE SLIPS. In a PICK, each wrong answer is what
   one slip from the idea card would give. Its sentence says
   kindly what happened: "That is what you get if you ..." The
   word "wrong" is not used.
7. THE SCORE is the number of right answers out of all. It goes to
   Moodle. How often it may be retried is Part 08's business.
8. THE TOY. If the plan names a ready toy, it is the first page of
   the Challenge, to play with before the questions. It has no
   score.

--------------------------------------------------------------------------------
4.10 NUMBERS
--------------------------------------------------------------------------------

Every number a visitor sees is worked out by a script.

1. The planner writes ONE numbers file, numbers.py , for the
   Level. It holds the numbers chosen in the plan and works out
   everything that follows from them, down to "1 down for every 2
   along".
2. Every number gets a NAME. The script prints the list: name,
   value, meaning.
3. The writer types names in curly brackets, like {lamp-up} . A
   check refuses any digit typed in the Guide or the Challenge.
4. FRIENDLY FIRST. At checkpoint 1, small whole numbers with whole
   results.
5. NO LUCKY NUMBERS. The file also works out what each slip would
   give. If a slip gives the right answer by luck, other numbers
   are chosen.
6. The Boss's answer in the file equals the published answer.
7. TWICE COMPUTED. An auditor writes its own small program from
   the plan alone, without seeing the numbers file. A script
   compares the two results. Two models, two programs, one answer.

--------------------------------------------------------------------------------
4.11 THE ATTRACT AND THE WALKTHROUGH
--------------------------------------------------------------------------------

THE ATTRACT. Its plan is the file attract.md : where to go in the
game, the one shot to capture, and Nir's lines.
1. First the moment plays with the game's own sound.
2. Nir says one or two sentences that point at the screen.
3. Nir asks the hook's question, word for word. Cut.
4. At most 40 spoken words. No school word, no name of an idea, no
   hint of the answer.
5. Nir does not pretend to play well.

THE WALKTHROUGH. It speaks the Guide's own text: the same pages,
without TRY and ANSWER. No second text is written. Part 06 owns
how it is drawn and voiced.

--------------------------------------------------------------------------------
4.12 THE FIELDS
--------------------------------------------------------------------------------

MATHS. SEE pages try small cases. Script check: many cases.
Bosses: first problems of early years, and junior olympiads.

PHYSICS. Every number carries its unit. What is left out (air,
friction) is said in one sentence. Route: what is asked, what is
given, which law, the calculation, the answer with its unit.
Bosses are often one part of a long problem.

CHEMISTRY. SEE pages count atoms. Script check: atoms and charges
are equal on both sides. Bosses: calculation and balancing.

BIOLOGY. Every fact is a claim with grade standard (Part 03).
Bosses: reasoning with ratios, growth, tables and graphs.

INFORMATICS. SEE pages have the reader BE the computer, carrying
out a small procedure by hand. Procedures are written as plain
numbered steps, with no program code. Script check: the procedure
as a program, run on the official tests where they are published.

IN CHEMISTRY AND BIOLOGY, a question that only asks for a
remembered fact is never a Boss.

HUMANITIES. Part 10.

--------------------------------------------------------------------------------
4.13 WHEN A CHAIN CANNOT BE DESIGNED
--------------------------------------------------------------------------------

The pairing is a calculation and cannot see everything. If the
planner finds that no job can be named, or that the ideas cannot
be shown on plain numbers, it does not force the Level. It writes
five lines saying what fails. Nir then gets a choice:
A. Retire this Level card. The game, the idea and the Boss are
   free again.
B. Keep the game and the idea, and ask the pairing for another
   Boss.
The planner recommends one. Nothing is built until Nir answers.

--------------------------------------------------------------------------------
4.14 FILES, COMMANDS AND CHECKS
--------------------------------------------------------------------------------

THE WORKSHOP of a Level is the folder attract-mode/levels/NAME/ :
1. brief.md      made by SCRIPT.
2. plan.md       the planner.
3. numbers.py    the planner.
4. guide.md      the writer.
5. challenge.md  the writer.
6. attract.md    the writer.
7. audits/       Part 07.
The two packages for Nir to upload are built by SCRIPT (Part 05).

The six lines that the Level card holds for each checkpoint (Part
02, 2.10) are typed once, in the plan. "am level sync" copies
them.

COMMANDS, added to the single command "am":
1. am route brief ID
2. am level new NAME -- creates the workshop from the golden one.
3. am level brief NAME
4. am level sync NAME
5. am level check NAME
6. am level status NAME -- says in plain words what exists and
   what passes.

THE CHECKS of "am level check". Each failure is one plain
sentence.
1. The plan has every line of the form.
2. The Level card equals the plan, and the checks of Part 02 pass.
3. The Guide's pages are of the right kinds, in the right order.
4. No digit is typed. Every name in curly brackets exists.
5. Page and sentence lengths (T4, T5).
6. The forbidden words (T3, V2, V3).
7. No new word appears before its checkpoint.
8. The Boss has one STEP page for each step of the route.
9. The Challenge has the right number of questions, and every
   wrong answer names its slip.
10. No slip gives the right answer.
11. The Boss's answer equals the published answer.
The rules that a script cannot test (T1, T2, V5 to V9) are tested
by an auditor (Part 07).

--------------------------------------------------------------------------------
4.15 DONE MEANS
--------------------------------------------------------------------------------

Part 04 is built when:
1. The six commands exist.
2. The free list for maths exists.
3. One golden route exists and has passed its three audits.
4. One golden workshop exists, for a game that Nir named: plan,
   numbers file, Guide, Challenge and Attract, and
   "am level check" passes.
5. The check fails, with a plain sentence, on each of a set of
   deliberately broken copies.
6. A cheap model, given the golden workshop and a new plan, has
   written a Guide and a Challenge that pass.
7. A middle-priced model, given the golden plan and a new brief,
   has written a plan that passes.
If 6 or 7 fails twice, the forms and the golden example are made
simpler. The checks are not made weaker.

--------------------------------------------------------------------------------
4.16 NOT DECIDED HERE
--------------------------------------------------------------------------------

1. How guide.md and challenge.md become SCORM packages; the ready
   pictures; the ready toys -- Part 05.
2. The film, the voice, the recording -- Part 06.
3. How the audits are run -- Part 07.
4. Where the four things sit in Moodle; the upload steps; retries
   -- Part 08.
5. Humanities Levels -- Part 10.

--------------------------------------------------------------------------------
4.17 WORDS ADDED TO THE GLOSSARY
--------------------------------------------------------------------------------

1. GUIDE -- the free text pages of a Level.
2. CHALLENGE -- the paid, scored questions of a Level.
3. PAGE KIND -- QUESTION, JOB, SEE, NAME, TRY, ANSWER, MACHINE,
   BOSS: PROBLEM, BOSS: STEP, CREDITS.
4. ROUTE -- the published solution in our own small steps.
5. FILL -- a step we added where the published solution jumped.
6. FREE LIST -- what is so basic that it needs no card.
7. DESCENT -- following an idea's needs down to ground.
8. FAITHFUL, NO GAPS -- the two audits of a route.
9. PLAN -- the form that decides everything about a Level.
10. BRIDGE -- moment, job, idea, machine.
11. PLANNER, WRITER -- who fills the plan; who writes the words.
12. SLIP -- a common mistake, listed on the idea card.
13. NUMBERS FILE -- the one program that works out a Level's
    numbers.
14. READY PICTURE, READY TOY -- made once in the kit, then only
    filled with numbers.
15. NUMBER, PICK, SPOT -- the three kinds of question.
16. WORKSHOP -- the folder where one Level is made.

================================================================================
END OF PART 04
================================================================================
