================================================================================
ATTRACT MODE -- THE BIBLE -- PART 07 OF 11
QUALITY
Version 2.0, folded on 11 November 2026
Obeys Parts 00 to 06.
================================================================================

HOW TO READ THIS PART

Earlier Parts named many checks. This Part gathers the ones that
a MODEL must answer (the AUDITS), says how they are run cheaply,
what happens after a failure, and what happens after a Level is
live. It is short on purpose. It changes no earlier Part.

This file is saved VERBATIM at: attract-mode/bible/part-07.md

--------------------------------------------------------------------------------
7.1 THE IDEA
--------------------------------------------------------------------------------

1. SCRIPT FIRST. Whatever a script can test, a script tests (the
   checks of Parts 02 to 06). An audit runs only after those
   pass. No model is paid to read broken work.
2. SMALL CLOSED QUESTIONS. An auditor is never asked "is this
   good?". It gets a question with a fixed set of answers: YES or
   NO, a number, FOLLOWS or NEEDS. A cheap model does this well,
   and a script can read the answer.
3. YES MEANS GOOD. Every question is worded so that YES is the
   good answer.
4. ONLY WHAT IS ON THE TABLE. An auditor gets exactly the inputs
   listed for its audit, and nothing else.
5. NEVER THE MAKER. The configuration names two auditor roles:
   auditor-text, and auditor-eyes (a model that can see). A
   script refuses to run if either is the same model as the
   planner or the writer.
6. ONCE. Every result is saved with the fingerprint of its
   inputs. Unchanged work is never audited again.
7. TOGETHER. Small audits of the same kind are sent ten at a
   time in one call, numbered.

Added to attract-mode/DECISIONS.md , chosen for Nir by the author
of this Part; Nir may reverse any:
D44. An auditor model must pass the trap test (7.5).
D45. Audits are closed questions, and YES means good.
D46. Live Levels are watched by the counters and corrected in
     the open (7.8).

--------------------------------------------------------------------------------
7.2 THE AUDITS
--------------------------------------------------------------------------------

Fourteen audits. For each: who, what goes IN, what it ANSWERS.

A1  MEANING (text). IN: a claim's "says" line and its quote.
    Does the quote say this? YES / NO.
    (Part 03, 3.7. Also the quotes of ground cards.)
A2  COPY (eyes). IN: a typed problem statement, the picture of
    its page. Is the typed text the same as the page, sign for
    sign? YES / NO: where.  (Part 03, 3.13.)
A3  HOOK SCORES (text). IN: a hook card without its scores, its
    claims, the scoring table of Part 02, 2.9. ANSWERS: four
    numbers.
A4  NEW TELLING (text). IN: two told-by lines. Are these two
    different comparisons? YES / NO.  (Part 02, 2.15.)
A5  FAITHFUL (eyes). IN: the pictures of the published solution,
    the route. For each step that is not a fill: MATCH or NOT
    THERE. Last line: SAME ANSWER YES / NO.  (Part 04, 4.5.)
A6  NO GAPS (text). IN: the statement, the route, the free list,
    each linked idea's one sentence. For each step: FOLLOWS, or
    NEEDS: what.  (Part 04, 4.5.)
A7  SECOND SUM (text). IN: the plan only. OUT: a small program
    that prints the worked numbers. A script runs it and compares
    with the numbers file.  (Part 04, 4.11.)
A8  STANDS ALONE (text). IN: one page's text, without its
    picture. Can every thing on this page be placed from the
    words alone? YES / NO: which thing.  (Part 04, T1, T2.)
A9  VOICE (text). IN: one page's text, and rules V5 to V9 of
    Part 04, one line each. For each rule: YES / NO: the
    sentence that breaks it.
A10 PICTURE (eyes). IN: a picture, its "says" line, the page's
    text. Two questions (7.3).
A11 CHOOSE (eyes). IN: a sheet of up to eight numbered pictures,
    and one line saying what is wanted. ANSWERS: one number, or
    NONE.  (Photos, Part 05; the still, Part 06.)
A12 FILM SHEET (eyes). IN: the last picture of each film page,
    with its "says" line. For each, two questions: Does it show
    what "says" says? Is everything whole, uncovered and large
    enough to read? YES / NO.  (Part 06, F5.)
A13 TOY SCREEN (eyes). IN: a screenshot of each task of a new
    toy type, and its form. Does the screen show what the form
    says for this task? YES / NO.  (Part 05, 5.13.)
A14 SOURCED (text). IN: one page's sentences, and the Level's claims.
    For each sentence: the id of the claim it rests on, or NONE. A NONE
    sends the page back.  (Part 10, 10.8; humanities Levels.)

--------------------------------------------------------------------------------
7.3 THE AUDIT CARD
--------------------------------------------------------------------------------

Each audit is one file, kits/audits/ID.md : the fixed words of
the question, with blanks. A script fills the blanks, sends the
card, and reads the answer. An answer that is not in the allowed
form is asked for once more. After that it counts as a failure.

TWO GOLDEN CARDS. The EXPERT writes the other eleven by copying
these.

    AUDIT A6 -- NO GAPS
    You are checking a solution written for a 14-year-old.
    You may use ONLY what is written below: the statement, the
    free list, the ideas and the steps. Use nothing else that
    you know.
    For each step, answer on one line:
        N FOLLOWS
    or
        N NEEDS: (in a few words, what the step uses that is not
        written below)
    Write nothing else.
    STATEMENT: ____
    FREE LIST: ____
    IDEAS: ____
    STEPS: ____

    AUDIT A10 -- PICTURE
    Look at the picture. Answer in two lines and write nothing
    else.
        1 YES    or    1 NO: (what is missing or different)
        2 YES    or    2 NO: (what disagrees)
    Question 1: Does the picture show what this sentence says?
    SAYS: ____
    Question 2: Does everything in the picture agree with this
    text?
    TEXT: ____

--------------------------------------------------------------------------------
7.4 WHEN SOMETHING FAILS
--------------------------------------------------------------------------------

1. FIRST FAILURE. The work goes back to its maker with the
   auditor's one line. One more try.
2. SECOND FAILURE. Stop. A script writes an escalation note into
   the workshop's audits/ : what failed, both attempts, both
   answers. The Level's status becomes "waiting for the EXPERT".
3. THE EXPERT, a stronger model, does one of three things:
   a. Repairs the work.
   b. Repairs the form or the golden example, so that the cheap
      model stops failing in this way. This is the better
      repair: it helps every later Level.
   c. Tells Nir that the chain cannot be designed (Part 04,
      4.14).
4. NEVER: weakening a check; changing the auditor until one says
   yes; marking something as passed by hand.
5. WHEN THE AUDITOR WAS WRONG. The EXPERT says so in the note,
   and the case becomes a new trap (7.5).

--------------------------------------------------------------------------------
7.5 THE TRAP TEST
--------------------------------------------------------------------------------

A cheap auditor is only worth something if it catches mistakes.
That is measured, not hoped.

1. For each audit there is a folder of TRAPS,
   kits/audits/traps/ID/ : five good cases and ten broken ones,
   each with its right answer. First the golden Level is audited by the
   best model Nir can afford, before any trap exists. The traps are then
   made from it, by breaking one thing in each: a
   step removed from a route, a label moved in a picture, a
   quote changed by one word.
2. "am audit traps" runs every audit on its traps with the
   models now named in the configuration.
3. A model may serve an audit only if it catches at least nine
   of the ten broken cases and passes at least four of the five
   good ones. The numbers are in the configuration.
4. The test is run again whenever an auditor model is changed.
   The script refuses to audit with a model that has not passed.
5. If no cheap model passes a certain audit, that audit goes to
   a middle-priced model. This is where the money goes first.

Mistakes will still get through sometimes. Section 7.8 is for
those.

--------------------------------------------------------------------------------
7.6 THE GATE
--------------------------------------------------------------------------------

"am level audit NAME" runs every audit of the Level that has not
passed yet: text audits first, then the audits with eyes, which
cost more.

"am level status NAME" prints the five pieces (Attract, Guide,
Walkthrough, toy, Challenge), each with "passed" or with the one
sentence of what is missing.

A Level's state becomes "built" when all five have passed. It
becomes "live" in Part 08.

--------------------------------------------------------------------------------
7.7 THE LINE FOR ONE LEVEL
--------------------------------------------------------------------------------

The whole production of one Level, in order. Each step is one
command from Parts 04 to 06. A step is not started before the
one above it has passed.

1.  am level new NAME
2.  am level brief NAME
3.  The planner fills plan.md and numbers.py .
4.  am level sync NAME
5.  The writer writes guide.md , challenge.md , attract.md .
6.  am level check NAME
7.  am level pictures NAME
8.  am level sheet NAME -- Nir records; then am footage in NAME
9.  am level pack NAME draft ; am level try NAME
10. am level voice NAME
11. am level film NAME draft
12. am level audit NAME
13. am level pack NAME ; am level try NAME
14. am level film NAME
15. am level upload NAME -- Nir uploads the two films.
16. Part 08: Nir uploads the two packages to Moodle.

Steps 1 to 7 and 9 to 14 need no Nir. Several Levels can wait
together at step 8, and again at step 15.

--------------------------------------------------------------------------------
7.8 AFTER A LEVEL IS LIVE
--------------------------------------------------------------------------------

THE COUNTERS. The beacon (Part 01, 1.4) records which checkpoint
readers reach. "am report live" prints, for each Level, how many
opened it and what share reached each checkpoint.
1. A checkpoint is FLAGGED when at least fifty readers reached
   it and more than half of them went no further. The numbers
   are in the configuration.
2. A flagged checkpoint gets a new telling: the planner chooses
   another told-by and other numbers, the writer rewrites its
   pages, and the line runs again from step 4.
3. With few visitors, the counters say nothing. That is normal
   at the start.

MISTAKES. Every Credits page has a "report a mistake" link. It
opens a new issue in the GitHub repository, with the Level and
the page already filled in.
1. The WORKHORSE checks the report against the sources.
2. If the report is right: the file is fixed, the line runs
   again from the step that owns the file, and Nir uploads the
   new package or film.
3. One line is added to the file corrections.md : the date, the
   Level, what was wrong, what it is now. Part 08 shows this
   file as the Corrections page.
4. A mistake in an idea card or a route may touch several
   Levels. "am vault find" lists them, and each is rebuilt.
5. The case becomes a trap for the audit that should have caught
   it.

--------------------------------------------------------------------------------
7.9 COMMANDS, ROLES, DONE
--------------------------------------------------------------------------------

COMMANDS, added to "am":
1. am level audit NAME
2. am audit traps
3. am report live

WHO DOES WHAT.
1. THE STRONGEST MODEL, ONCE (read Part 11, 11.7): the fourteen audit
   cards, the traps, the scripts that fill, send and read.
2. AUDITOR-TEXT and AUDITOR-EYES: cheap models that passed the
   trap test.
3. THE EXPERT: escalations.
4. THE WORKHORSE: checks reports of mistakes.
5. NIR: nothing, except the uploads that a correction needs.

DONE MEANS.
1. The fourteen cards and their traps exist.
2. "am audit traps" has run, and the configuration names an
   auditor-text and an auditor-eyes that passed.
3. The golden Level has passed "am level audit".
4. A broken copy of the golden Level has gone through a first
   failure, a second failure and an escalation note.

WORDS ADDED TO THE GLOSSARY.
1. AUDIT -- a check that a model must answer.
2. AUDIT CARD -- the fixed words of one audit, with blanks.
3. AUDITOR-TEXT, AUDITOR-EYES -- the two auditor roles.
4. TRAP -- a case with a known answer, for testing an auditor.
5. ESCALATION NOTE -- what the EXPERT gets after two failures.
6. THE GATE -- "am level audit": everything must pass.
7. THE LINE -- the sixteen steps of 7.7.
8. FLAGGED -- a checkpoint where most readers stop.

================================================================================
END OF PART 07
================================================================================
