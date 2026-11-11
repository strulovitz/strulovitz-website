================================================================================
ATTRACT MODE -- THE BIBLE -- PART 05 OF 11
THE KITS: PACKAGES, PICTURES AND TOYS
Version 2.0, folded on 11 November 2026
Obeys Parts 00 to 04 and section 5.2 below.
This version replaces every earlier Part 05.
================================================================================

HOW TO READ THIS PART

Part 04 ended with a Level's text files: the plan, the numbers
file, the Guide and the Challenge. This Part says how those files
become things a visitor can open: pictures, a toy, and two closed
SCORM packages.

Two things are saved with this Part:
1. This file: attract-mode/bible/part-05.md
2. THE GOLDEN TOY: a finished, working toy for the example of
   Part 04. It is the file
   attract-mode/kits/toys/mirror-bounce/toy.html
   A double click opens it in a browser. Every later toy is made
   by copying it (5.13).

Section 5.3 continues the example of Part 04. Read it first. As
before, the example shows FORMAT ONLY.

--------------------------------------------------------------------------------
5.1 THE THREE KITS
--------------------------------------------------------------------------------

A KIT is a set of pieces that are BUILT ONCE, tested, and then
only FILLED with a Level's names and numbers.

1. THE PICTURE KIT turns the PICTURE blocks of the Guide into
   pictures. Folder: attract-mode/kits/pictures/ .
2. THE TOY KIT holds the toy types. Folder: attract-mode/kits/toys/ .
3. THE PACKAGE KIT holds the page player, the Challenge player,
   the packer and the robots. Folder: attract-mode/kits/pages/ .

--------------------------------------------------------------------------------
5.2 DECISIONS, CHANGES AND ADDITIONS
--------------------------------------------------------------------------------

Added to attract-mode/DECISIONS.md :

Decided by Nir, 11 November 2026:
D28. Every question of a Challenge is multiple choice. Nobody
     types an answer.
D29. The toy gets a real blueprint: one finished, working toy
     that the weaker models copy.

Chosen for Nir by the author of this Part; Nir may reverse any:
D30. A package is closed: it holds everything it needs.
D31. Formulas are typed the way people type on a calculator. A
     script sets them. They are shown, not spoken.
D32. A toy is one file of plain code, with no outside library. A
     library enters only when the EXPERT finds that a toy type
     cannot be built without it.
D33. The right answers travel inside the Challenge package.
     Somebody who wants to cheat can ask an AI anyway.
D34. Painted pictures are switched off until a script can start
     Nir's local image model by itself (5.10).

CHECKED ON 11 NOVEMBER 2026:
1. The SCORM 1.2 rules. The score is a number from 0 to 100. The
   bookmark holds up to 255 characters. The saved state holds up
   to 4096 characters. The status words are: passed, completed,
   failed, incomplete, browsed, not attempted.
2. Wikimedia Commons, asked by a program, returns for each photo
   its title, author, licence, the licence's address, its size
   and its kind. Wikimedia's rules require a script to name
   itself and give a way to reach its owner.
3. Formulas written in MathML are shown by all main browsers
   without any library, since January 2023.
4. THE GOLDEN TOY was run under Node against a stand-in for a
   browser page, with two sets of numbers. Its formulas, its
   three tasks, the finger, the keys, the buttons, the machine
   and the test hook behaved as written. It was NOT opened in a
   real browser there. The first agent opens it in the hidden
   browser and in a real one, and repairs what the eye finds.

CHANGES TO PART 04. Where Part 04 disagrees with this section,
this section wins.
1. Section 4.10, item 2: there are two kinds of question, PICK
   and SPOT. The kind NUMBER is removed. In section 4.3, D,
   question 1 is a PICK.
2. Section 4.10, item 6: a PICK has one right answer and three
   wrong ones. The wrong ones are slips first. If the idea has
   fewer than three slips, the numbers file fills up with NEAR
   ANSWERS (5.12).
3. Sections 4.3, B and 4.9: in the plan, the Toy section has one
   line for each thing the toy's form needs (5.13).

ADDITIONS. These add to earlier Parts and contradict nothing.
1. Part 01, section 1.7, Place 3: one more folder, packages/ .
2. Part 04, section 4.7: a page may carry FORMULA lines (5.8).
3. Part 04, section 4.11: the numbers file also gives scenes,
   lists, answers and toy tests (5.4).
4. Part 04, section 4.13: a line of a program has at most 48
   characters, so that it fits a phone.

--------------------------------------------------------------------------------
5.3 THE EXAMPLE, CONTINUED
--------------------------------------------------------------------------------

The Level of Part 04, section 4.3: the lamp, the wet street, the
eye.

A. WHAT THE NUMBERS FILE PRINTS.

    NUMBERS
    lamp-up      3   how high the lamp hangs, in metres
    eye-up       1   how high the eye is, in metres
    apart        8   from lamp to eye along the street, in metres
    spot-along   6   from the lamp to the bounce spot, in metres

    SCENE street
    street-left    -1 ,  0
    street-right    9 ,  0
    lamp            0 ,  3
    eye             8 ,  1
    middle-spot     4 ,  0
    spot            6 ,  0
    twin            0 , -3

    LIST sign
    2,2  2,3  2,4  3,4  4,4  4,3  4,2  3,2  5,2  6,3  5,4

    ANSWERS q1
    right   6
    slip    4.5   middle
    slip    3     from-the-eye
    near    5     one less

    TOY TESTS
    task 1, set 4:    done no,  lightAtEyeHeight 5.33
    task 1, set 6:    done yes, lightAtEyeHeight 8
    task 3, machine:  done yes, twins 11

B. ONE PICTURE. For page 8 the writer wrote:

    PICTURE
    kind: drawn
    like: page 4
    dot: twin "twin lamp"
    dashed-line: eye to twin
    says: The picture of page 4, with a twin lamp added straight
    below the real lamp, under the street. A dashed straight line
    runs from the eye to the twin and crosses the street at the
    bounce spot.

What the script does with it:
1. It takes the picture of page 4.
2. It adds the dot and the dashed line, at the places the numbers
   file gave.
3. It uses the frame of the scene "street". That frame is the
   same on every page, so the lamp stands at the same place on
   pages 3, 4 and 8. Nothing jumps.
4. It puts the words "twin lamp" beside the dot, where they cover
   nothing.
5. It writes two files: pictures/page-08.svg , the picture; and
   pictures/page-08.json , the same picture as a list of final
   positions. The film reads that list (Part 06).

C. THE TOY. This is the golden toy. What the visitor meets:

    TASK 1. A street, a lamp, an eye, and a ring on the street:
    the bounce spot. Light runs from the lamp to the ring and
    leaves as steeply as it came. Wherever the finger touches,
    the ring goes. Under the picture stands: "Bounce spot: 4 m
    from the lamp. The light misses the eye." At 6 the light runs
    into the eye, and the task line says "Done."

    TASK 2. The same, and now the twin lamp is drawn under the
    street, with a dashed line from the eye to it. The ring
    belongs where the dashed line crosses the street.

    TASK 3. The sign appears as eleven dots. One button: "Run the
    machine". Twin after twin appears under the street, each with
    its ray, until the whole sign stands there upside down.

For this toy the planner wrote only these lines in the plan:

    ## Toy
    type: mirror-bounce
    light: lamp
    eye: eye
    mirrorLeft: street-left
    mirrorRight: street-right
    sign: sign
    label light: lamp
    label eye: eye
    label twin: twin lamp
    unit: m
    task 1: Slide the spot until the light from the lamp reaches the eye.
    task 2: Now the twin lamp is shown. Find the spot in one move.
    task 3: Press the button. The machine does it for the whole sign.

D. THE TWO PACKAGES.

    level-example-guide.zip
        imsmanifest.xml
        index.html
        player.js
        look.css
        pictures/

    level-example-challenge.zip
        imsmanifest.xml
        index.html
        player.js
        look.css
        toy.html
        pictures/

E. THE ROBOT. Before Nir uploads anything, a robot opens the
Guide at the size of a phone and presses Next on every page. It
sets the toy's spot to 4, then to 6, and reads what the toy says.
It answers all the questions right, then all wrong. Each time it
reads what the package told a pretend Moodle. If anything is off,
it says so in one plain sentence.

--------------------------------------------------------------------------------
5.4 WHAT THE NUMBERS FILE GIVES
--------------------------------------------------------------------------------

The numbers file (Part 04, 4.11) gives six kinds of things. All
have NAMES: lowercase letters, digits and hyphens, unique inside
the Level. (Example: 5.3, A.)

1. NUMBERS. A name, a value, a meaning.
2. POINTS, in SCENES. A scene is a group of points that are drawn
   together: "street", "river". Each point has a place across and
   a place up, in the scene's own units. Every point belongs to
   exactly one scene. A new set of numbers, such as a TRY
   question's, gets its own scene.
3. LISTS. A named row of numbers, of words or of points.
4. RESULTS. In informatics: what each program printed.
5. ANSWERS. For each question of the Challenge: the right answer
   and three wrong ones (5.12).
6. TOY TESTS. A few settings of the toy, and for each, what the
   toy must then say (5.13).

The command "am level pictures" prints all six as plain lists.
The writer and the planner work from that print.

--------------------------------------------------------------------------------
5.5 DRAWN PICTURES: THE PICTURE WORDS
--------------------------------------------------------------------------------

A PICTURE LIST is made of these twelve words and of names of
points. (Example: 5.3, B.) POINT means the name of a point. Words
in quotes are a label.

1.  dot: POINT "label"
        a dot. The label may be left out.
2.  text: POINT "words"
        words at a place, without a dot.
3.  line: POINT to POINT
4.  dashed-line: POINT to POINT
5.  arrow: POINT to POINT
6.  shape: POINT, POINT, POINT
        a closed outline through three or more points, lightly
        filled.
7.  circle: POINT through POINT
        the centre, and one point on the rim.
8.  angle: POINT, POINT, POINT "label"
        the angle at the middle point.
9.  right-angle: POINT, POINT, POINT
        the small square that marks a right angle at the middle
        point.
10. length: POINT to POINT "label"
        a measuring mark beside that stretch, with its label.
11. same: POINT to POINT, POINT to POINT
        small ticks saying that these stretches are equally long.
12. like: page N
        start from the picture of page N and add to it.

HOW THE WRITER USES THEM.
1. A label holds words and names in curly brackets, like
   "{lamp-up} m". Never a typed digit.
2. All points of one picture belong to one scene. "like:" may
   point only to an earlier page with a picture of that scene.
3. Write the lines in the order in which the page's text mentions
   the things. The film draws them in that order.
4. At most twelve things in one picture, counting those that came
   through "like:". The limit is in the configuration.
5. Never write a place, a size or a colour. The script decides
   them.
6. If these words cannot say what the page needs, write one line,
   KIT GAP, saying what is missing. The EXPERT decides whether
   the list of words grows.
7. Under a picture line the writer MAY add a line "when:" with two or
   three words copied from the page's text. It says in which sentence
   the line appears (Part 06, 6.10).

--------------------------------------------------------------------------------
5.6 DRAWN PICTURES: THE CHARTS
--------------------------------------------------------------------------------

Some pictures are not made of points and lines. For those there
are CHARTS: ready drawings, each with a short form. The first set:

1. number-line -- a line with marks, some marked numbers, and
   jumps between them.
2. bars -- one bar for each number of a list, with names.
3. graph -- points, or a line through them, from two lists, with
   named axes.
4. table -- rows and columns of words and numbers.
5. grid -- squares in rows and columns. Some are filled, some are
   marked, and a path may run through them.
6. counters -- groups of small tokens of a few kinds: atoms,
   animals, coins.
7. boxes -- a row of boxes with a value in each, and a pointer.
   This is how a list in a computer's memory is shown.

EXAMPLE of a chart block (format only):

    PICTURE
    kind: drawn
    chart: bars
    values: rabbits-by-year
    names: years
    up-label: "rabbits"
    says: Five bars, one for each year. Each bar is twice as tall
    as the one before.

The form of each chart is the file kits/pictures/charts/NAME.md ,
with a filled example. The writer copies the example and changes
the names. A new chart is built by the EXPERT after a KIT GAP.

--------------------------------------------------------------------------------
5.7 HOW THE SCRIPT DRAWS
--------------------------------------------------------------------------------

1. THE FRAME of a picture is the frame of its SCENE: the smallest
   box that holds ALL the points of the scene, with a margin. The
   scale is the same across and up, so shapes and angles are
   true. Every picture of a scene has the same frame. (The golden
   toy does the same; its function makeFrame shows how.)
2. EVERY PICTURE HAS THE SAME OUTER SHAPE: four wide by three
   high. It is in the configuration.
3. LABELS are placed by the script. It tries the places around
   the point and takes the first where the label covers nothing.
4. THE LOOK is one file for the whole project: the thickness of
   lines, the size of letters, the colours. Nothing is told by
   colour alone: a dashed line is dashed, a strong line is thick.
5. OUTPUT. For each picture, two files in the workshop's folder
   pictures/ : the picture itself (SVG), and the list of final
   positions in drawing order, made of the seven shapes (Part 06, 6.9)
   (JSON). The Guide shows the first.
   The film reads the second.

THE SCRIPT'S CHECKS ON A DRAWN PICTURE.
1. Every word is a known picture word. Every name exists.
2. All points are in one scene.
3. Nothing lies outside the frame.
4. No label covers another label, a dot or a line's end.
5. On a screen 360 wide, the letters are at least 14 high.
6. No typed digit.
The script draws the picture in the hidden browser and measures
it there, so it checks what a visitor will really see.

Then the auditor that can see asks its two questions (Part 04,
4.8).

--------------------------------------------------------------------------------
5.8 FORMULAS
--------------------------------------------------------------------------------

The sentences of a page are spoken in the film. So sentences hold
words and numbers only. A formula goes on its own line, after the
page's text. It is shown and not spoken.

EXAMPLES (format only):

    FORMULA: ({top-a}*n + {top-b}) / ({bottom-a}*n + {bottom-b})
    FORMULA: {lamp-up} / {spot-along} = {eye-up} / {rest-along}
    FORMULA chem: 2 H2 + O2 -> 2 H2O

1. TYPED LIKE ON A CALCULATOR. Allowed: + - * / ^ ( ) sqrt( )
   = < > <= >= . Numbers are names in curly brackets. A single
   letter stands for a number we do not know yet.
2. THE SCRIPT SETS IT PROPERLY: a division as a fraction with a
   bar, a power raised, a multiplication sign where one is
   needed. On the pages it is shown by the browser itself, with
   no library. The film gets a formula as a photograph of the Guide's
   page (Part 06).
3. SAID BEFORE SHOWN. The text of the same page first says in
   words what the formula says.
4. At most two formula lines on a page.
5. THE EQUATION CHECK. If a formula has an equals sign and both
   sides hold only numbers, the script works out both sides. They
   must be equal, or the build stops.
6. CHEMISTRY. A line "FORMULA chem:" holds substances and an
   arrow. Digits are allowed here: they belong to a substance's
   name. A charge is typed with ^ , as in Na^+ . The script sets
   the small numbers low. It also counts the atoms and the
   charges on both sides, and they must be equal. A page that
   shows an unbalanced equation on purpose writes
   "FORMULA chem unbalanced:".
7. A formula that the script cannot read stops the build, with a
   plain sentence. The EXPERT may teach the reader more.

--------------------------------------------------------------------------------
5.9 PHOTOS
--------------------------------------------------------------------------------

A PHOTO block holds two lines, wanted: and says: (Part 04, 4.8).
The script and the auditor do the rest.

1. ASK. The script sends the main words of the "wanted" line to
   Wikimedia Commons and asks for photos only. It names itself
   and Nir's site, as Wikimedia's rules ask. It asks slowly: at
   most one request a second.
2. KEEP only candidates that pass all of these:
   a. The licence is on our list: public domain, CC0, CC BY,
      CC BY-SA. The list is in the configuration.
   b. An author is named, or the photo is in the public domain.
   c. It is a photo file, at least 800 wide.
3. SHEET. The script puts up to eight candidates on one sheet,
   with a number under each.
4. CHOOSE. An auditor that can see gets the sheet, the "wanted"
   line and the page's text. It answers with one number, or
   "none". One look instead of eight.
5. TAKE. The script fetches the chosen photo, makes it small
   enough (5.14), and stores it in the workshop's pictures/ .
6. CREDIT. The script writes down the photo's title, its author,
   its licence with the licence's address, the address of its
   page at Commons, and the word "resized". All of this appears
   in the Credits.
7. "NONE". The writer rewrites the "wanted" line once, with other
   words. After a second "none", Part 04, section 4.8, says what
   happens.

--------------------------------------------------------------------------------
5.10 PAINTED PICTURES
--------------------------------------------------------------------------------

Painted pictures are for imagined scenes only (Part 04, 4.8).

THEY ARE SWITCHED OFF AT THE START. Nir's image models live in
studios with their own windows. Until a script can start one by
itself, a painted picture would be one more thing for Nir to
carry. After the survey (Part 01, 1.5), the EXPERT finds out
whether one of the models can be started by a command. If so, it
switches painted pictures on in the configuration. Until then a
page gets a photo or a drawn picture.

THE FORM, for when they are on (format only):

    PICTURE
    kind: painted
    subject: a lighthouse on a rock
    place: a stormy sea
    light: dusk, one warm light at the top
    says: A lighthouse on a rock in a storm at dusk.

The script adds two fixed lines from the configuration: the
project's LOOK, and NEVER: no words, no letters, no numbers, no
logos, no real people.

The auditor that can see asks its two questions, and a third: is
there any writing or any number in the picture? If yes, it is
painted again.

--------------------------------------------------------------------------------
5.11 THE PAGE PLAYER (THE GUIDE PACKAGE)
--------------------------------------------------------------------------------

The page player is the small program inside every package that
shows one page at a time. It is built once, by the strongest
model, and it is the golden example of its kind.

1. One page at a time. Two large buttons at the bottom, Back and
   Next, within reach of a thumb. The arrow keys work too.
2. At the top: the Level's name, and where the reader is:
   "Checkpoint 2 of 3", and the page number.
3. On a phone the picture is above the text. On a wide screen
   they stand side by side. A tap on the picture makes it large.
4. Letters at least 18 high. The fonts are the device's own.
5. It works in a frame as small as 360 by 500, and on a full
   screen.
6. A NAME page looks different from every other page, so that the
   moment an idea gets its name is felt.
7. A CODE page uses letters of equal width and never scrolls
   sideways.
8. The "says" line of a picture is given to screen readers.
9. WITH MOODLE. It keeps a bookmark, so a signed-in player comes
   back to the same page. On the last page it tells Moodle
   "completed".
10. WITHOUT MOODLE. For a guest, or when the package is opened
    from the disk, everything works. Nothing is remembered and no
    error is shown.
11. THE BEACON. At each checkpoint reached, it asks for one tiny
    file under /am/beacon/ (Part 01, 1.4). If that fails, nothing
    happens.
12. THE LOOK is one file, look.css . Nir can ask for another look
    at any time. Every package gets it at its next build.

--------------------------------------------------------------------------------
5.12 THE CHALLENGE PLAYER
--------------------------------------------------------------------------------

The Challenge package uses the same player. Its first page is the
toy. Then comes one question on each page. Every question is four
large buttons. Nobody types.

HOW THE WRITER WRITES A QUESTION (format only):

    QUESTION 1 -- PICK (checkpoint 1)
    ask: A lamp hangs {q1-lamp-up} metres up. An eye is
    {q1-eye-up} metre up. They are {q1-apart} metres apart. How
    far from the lamp is the bounce spot?
    answers: q1
    after: metres
    slip middle: That is the middle between them. The spot lies
    nearer the eye, because the eye is lower.
    slip from-the-eye: That is the distance from the eye. The
    question asks for the distance from the lamp.

WHAT THE VISITOR SEES:

    A lamp hangs 2 metres up. An eye is 1 metre up. They are 9
    metres apart. How far from the lamp is the bounce spot?
    A. 3 metres
    B. 4.5 metres
    C. 5 metres
    D. 6 metres

The writer typed no number and no answer. The four answers come
from the numbers file (5.3, A: ANSWERS q1).

HOW IT WORKS.
1. TWO KINDS. PICK: four answers from the numbers file. SPOT: a
   step of the Boss is shown, and the four answers are names of
   ideas. The SCRIPT makes every SPOT question from the cards:
   the right idea, and three others of this Level. If the Level
   has fewer than four ideas, it takes ideas of the same topic.
2. THE WRONG ANSWERS of a PICK are worked out by the numbers
   file. Slips come first: what a named mistake would give. If
   fewer than three slips exist, NEAR ANSWERS fill up. A near
   answer is the first of these that is new and makes sense: one
   less, one more, the half, the double. The list is in the
   configuration.
3. THE SENTENCE after a wrong answer. For a slip, the writer
   writes it, kindly, beginning "That is ...". For a near answer
   it is fixed: "Not this one. Checkpoint N of the Guide shows
   the way." The word "wrong" is not used.
4. THE ORDER is set by the script, the same for everyone. Number
   answers stand from the smallest to the largest. Idea names
   stand in the order of the Guide.
5. The script checks that the four answers are all different.
6. AFTER AN ANSWER it is locked. The page shows the right answer
   and one sentence.
7. THE LAST PAGE shows the result as "6 of 8". For each missed
   question it names the idea and the checkpoint of the Guide
   that teaches it.
8. TO MOODLE it sends the score as a number from 0 to 100, and
   the word "completed". It never sends "failed".
9. A signed-in player's answers are saved as they are given.
   Closing the page in the middle loses nothing.
10. No clock.
How often a Challenge may be started again is Part 08's business.

--------------------------------------------------------------------------------
5.13 THE GOLDEN TOY, AND HOW TO COPY IT
--------------------------------------------------------------------------------

The golden toy is the file kits/toys/mirror-bounce/toy.html . It
is ONE file. It opens by a double click, with nothing else. Read
it beside this section: its comments use the same words.

THE FILE HAS FOUR PARTS, each under a large comment line.

PART 1 -- THE LEVEL'S DATA. One block named LEVEL, between two
marks. It holds the points, the lists, which point plays which
role, the labels, the unit and the task sentences. The packer
writes this block from the plan and the numbers file. In the
golden file it holds the example's numbers, so the file works by
itself.

PART 2 -- THE SHARED PARTS. The frame; the way from a place in
the scene to a place on the stage; the way from a finger to a
place in the scene; drawLine, drawDot, drawLabel; plain numbers;
the task line. It is the same in every toy type, letter for
letter. A script compares.

PART 3 -- THIS TOY TYPE. The only part that differs from toy to
toy. It has five pieces, A to E (below).

PART 4 -- START, AND THE TEST HOOK.

THE FIVE PIECES OF PART 3, and what they are in the golden toy.

A. THE GEOMETRY. Small functions that work things out from LEVEL
   and draw nothing. Golden: twinOf (the twin of a point),
   bounceSpotFor (where light must bounce to reach the eye),
   lightAtEyeHeight (where the bounced light is when it is as
   high as the eye).
B. THE STATE. The few things that can change. Golden: which task;
   where the spot is; how many twins are drawn.
C. THE TASKS. When a task is done, and what moves. Golden:
   taskDone, goToTask, moveSpot, machineStep, runMachine.
D. THE DRAWING. ONE function, draw. It wipes the stage and draws
   everything again from the state. It is called after every
   change. Nothing is drawn anywhere else.
E. WHAT THE FINGER DOES. The whole stage follows the finger:
   touch anywhere, and the spot goes under the finger.

FOUR TRICKS TO KEEP IN EVERY TOY.
1. DRAW EVERYTHING AGAIN. Never repair a picture bit by bit. So
   the picture can never disagree with the state.
2. THE MAGNET. When the finger is close enough to the right
   place, the thing jumps exactly onto it. So "done" is exact,
   and a thick finger can do it.
3. A key step is twice the magnet's reach. So a key can leave the
   magnet, and can never jump over the right place.
4. THE MACHINE HAS TWO SPEEDS. The button runs it slowly, on a
   timer, so the eye can follow. The test hook runs it at once,
   so a robot need not wait.

THE FORM of the golden toy type, the file form.md (format only):

    TOY TYPE mirror-bounce
    WHAT IT IS: light bounces off a flat mirror into an eye.
    USE IT WHEN: the job is to find where something bounces, or
    the shortest way that touches a straight line.
    NEEDS
      light        a point above the mirror
      eye          a point above the mirror
      mirrorLeft   a point: one end of the mirror
      mirrorRight  a point: the other end, at the same height
      sign         a list of points above the mirror
    LABELS: light, eye, twin
    UNIT: one short word, like m
    TASKS
      1  by hand: slide the spot until the light reaches the eye
      2  the twin is shown: set the spot in one move
      3  the machine: one button; it draws the twin of every
         point of the sign
    THE ROBOT CAN
      set(along)   put the spot that far from the light
      read()       along, lightAtEyeHeight, twins, done, says

HOW A LEVEL USES A TOY TYPE. The planner writes the Toy section
of the plan: one line for each NEED, each LABEL, the UNIT and
each TASK (example: 5.3, C). The packer turns those lines and the
numbers file into the LEVEL block, puts it between the two marks,
and writes the result into the Challenge package as toy.html .
The first page of the Challenge shows it in a frame.

A NEW TOY TYPE, STEP BY STEP. When the planner writes KIT GAP:
1. "am toy new TYPE" copies the golden folder under a new name.
2. Write form.md first: what it is, when to use it, what it
   needs, its tasks. The first task is the job by hand. The last
   task hands the job to the machine.
3. In part 1, write example data with friendly numbers.
4. Piece A. Write the geometry functions. Try them alone on the
   example numbers before anything is drawn.
5. Piece B. List the few things that can change.
6. Piece C. Say when each task is done. Keep the magnet.
7. Piece D. Write draw, using drawLine, drawDot and drawLabel.
   If the toy needs another shape, add ONE new drawing function
   to part 3. Never to part 2.
8. Piece E. Usually it stays as it is. Change only which thing
   the finger moves.
9. Part 4. Keep the four words of the test hook: task, set,
   machine, read. "read" gives back the toy's own values.
10. Do not touch part 2.
11. Run the toy robot. Then the auditor that can see gets one
    screenshot of each task, and the form. It answers: does the
    screen show what the form says?
The builder is the EXPERT role; on a normal day, a middle-priced
model. After two failures, the type goes to the strongest model.

HOW ANOTHER TOY FITS THE SAME FIVE PIECES (format only): a toy
type "balance", a beam with a weight on each side.
    A. geometry: the pull of a side is its weight times its
       distance from the middle.
    B. state: which task; where the right weight hangs.
    C. tasks: 1, slide the weight until the beam is level. 2, the
       two pulls are shown as numbers; set it in one move. 3, the
       machine levels five beams, one after another.
    D. drawing: the beam is a line, tilted by the difference of
       the pulls; the weights are dots; the middle is a label.
    E. finger: moves the right weight along the beam.

WHAT HOLDS FOR EVERY TOY.
1. It works with one finger on a screen 360 wide. Nothing depends
   on a mouse hovering.
2. The first touch does something that can be seen. The only
   instruction is the task's one sentence.
3. Things stand where the Guide's pictures showed them, because
   the toy draws from the same points.
4. No number is typed in part 3. Every value is worked out from
   LEVEL.
5. A "Next task" button is always there, so nobody is stuck.
6. No sound, no clock, no score.
7. One file. It calls no address outside itself.

THE TOY ROBOT. For each line of TOY TESTS in the numbers file
(5.3, A), the robot goes to that task, sets the toy through the
test hook, and reads it. What the toy says must equal what the
numbers file worked out. So the toy's formulas and the numbers
file's formulas are two programs that must agree. The robot also
opens the toy at phone size, looks for errors, drags a finger
across the stage and checks that the spot followed, and presses
every button.

--------------------------------------------------------------------------------
5.14 PACKING
--------------------------------------------------------------------------------

The command "am level pack NAME" builds the two packages into the
folder attract-mode-files/packages/NAME/ . The two PCs copy that
folder to each other, so Nir finds the packages on whichever PC
is serving. (Example: 5.3, D.)

1. CLOSED. A package holds everything it needs: the pages, the
   pictures, the player, the look, the toy. It calls no address
   outside itself, except the beacon and the links in the
   Credits.
2. ONE FILE OF PAGES. All pages are inside index.html , so the
   package also opens straight from the disk.
3. ITS OWN COPY OF THE KIT. When the kit changes later, an old
   Level keeps working exactly as it was built.
4. SCORM 1.2. One manifest, one item. Its title is the Level's
   public title and the word Guide or Challenge.
5. SAME IN, SAME OUT. The same files always give the same package,
   byte for byte.
6. THE STAMP. Each package carries a short fingerprint, shown
   small on its last page. "am level status" prints the
   fingerprint of the newest build. So anyone can tell whether
   the package in Moodle is the newest. The stamp of the newest build is
   also written into the workshop, so that it travels by Git.
7. SIZE. A package is at most 5 MB, and a picture at most 200 KB.
   The limits are in the configuration. Part 08 sets Moodle's
   upload limit above them.
8. DRAFT. "am level pack NAME draft" builds even when pieces are
   missing. Every page of a draft carries the word DRAFT. A draft
   never goes to Moodle.
9. A final build refuses to run if a piece is missing or a check
   fails.

--------------------------------------------------------------------------------
5.15 THE ROBOTS
--------------------------------------------------------------------------------

The command "am level try NAME" tests the built packages in a
hidden browser. Each failure is one plain sentence.

R1. THE MANIFEST is well formed and names the file to open. Every
    file it lists is there, and nothing else is.
R2. THE READER ROBOT turns every page, at three sizes: a phone
    (360 by 640), a small frame (360 by 500) and a desk screen
    (1280 by 800). No script error. Nothing scrolls sideways. No
    text is cut. Every picture is shown. The letters are large
    enough. No request leaves the package, except the beacon. It
    saves a screenshot of every page at phone size into the
    workshop's audits/ , for Part 07.
R3. THE PRETEND MOODLE is a test page that plays Moodle's part
    and writes down everything a package tells it.
    Guide: the bookmark is saved and brought back; the last page
    says "completed".
    Challenge: all right gives 100; all wrong gives 0; a known
    mix gives the expected number; "failed" is never sent; the
    saved state stays under 4096 characters; closing in the
    middle and opening again brings the answers back.
R4. NO MOODLE. Opened from the disk, everything works and no
    error is shown.
R5. THE TOY ROBOT (5.13).
R6. THE SIZES of 5.14.

--------------------------------------------------------------------------------
5.16 THE COMMANDS
--------------------------------------------------------------------------------

Added to the single command "am":
1. am kit list -- prints the picture words, the charts and the
   toy types with their forms. The brief of a Level includes this
   print.
2. am kit test -- runs the kits' own tests, and checks that part
   2 is the same in every toy type.
3. am toy new TYPE -- starts a new toy type from the golden one.
4. am toy open TYPE -- opens a toy type's file in the browser.
5. am level pictures NAME -- prints the lists of 5.4, draws,
   fetches photos, and runs the picture checks.
6. am level pack NAME -- builds the two packages. With the word
   "draft": a draft.
7. am level try NAME -- runs the robots.
8. am level open NAME -- opens the built Guide and Challenge in
   the browser of this PC, so that Nir can look at them.

--------------------------------------------------------------------------------
5.17 WHO DOES WHAT
--------------------------------------------------------------------------------

1. THE STRONGEST MODEL, ONCE (read Part 11, 11.7): the golden toy (done, saved with
   this Part); the drawer; the formula reader; the page player
   and the Challenge player; the packer; the robots and the
   pretend Moodle; the first charts.
2. THE EXPERT ROLE, when a KIT GAP appears (on a normal day, a
   middle-priced model): a new toy type, a new chart, a new
   picture word.
3. THE PLANNER: the Toy section of the plan; KIT GAP lines; the
   answers and the toy tests in the numbers file.
4. THE WRITER: PICTURE blocks, FORMULA lines, questions and slip
   sentences.
5. THE AUDITOR THAT CAN SEE: the two questions on every picture;
   choosing a photo from the sheet; the screenshots of a new toy
   type.
6. THE SCRIPT: drawing, fetching, setting formulas, packing, the
   robots.
7. NIR: looks, if he wishes, with "am level open". Uploads the
   packages (Part 08).

--------------------------------------------------------------------------------
5.18 DONE MEANS
--------------------------------------------------------------------------------

Part 05 is built when:
1. The golden toy has been opened in a real browser on a phone
   and on a PC, and what the eye found was repaired.
2. The eight commands exist, and "am kit test" passes on both
   PCs.
3. For the golden Level: every picture is drawn or fetched and
   has passed its checks; its toy passes the toy robot; both
   packages are built; all the robots pass.
4. The checks fail, each with a plain sentence, on these broken
   copies: a picture that names a missing point; two labels on
   top of each other; an equation that is false; a chemical
   equation that does not balance; a photo with a licence that is
   not on the list; a toy whose formula was changed; a question
   with two equal answers; a package that calls an outside
   address.
5. A cheap model, given the golden Guide and a new plan, has
   written PICTURE blocks and questions that pass.
6. A middle-priced model has built a second toy type from the
   golden one by the steps of 5.13, and the toy robot passes.
7. Nir has opened the golden Guide and Challenge with
   "am level open".
The test inside real Moodle is the "done" of Part 08: a guest
opens the Guide, and a signed-in player's score arrives.

--------------------------------------------------------------------------------
5.19 NOT DECIDED HERE
--------------------------------------------------------------------------------

1. The still from Nir's footage; how the film reads the picture
   lists; the voice -- Part 06.
2. How the audits are run, and by which model -- Part 07.
3. The upload steps; attempts and grades; the upload limit; how
   Moodle shows a package -- Part 08.
4. How the local image model is started by a script -- the EXPERT,
   after the survey; Part 10 owns the art studios.
5. Pictures for humanities Levels -- Part 10.

--------------------------------------------------------------------------------
5.20 WORDS ADDED TO THE GLOSSARY
--------------------------------------------------------------------------------

1. KIT -- pieces built once and then only filled.
2. SCENE -- a group of points that are drawn together, with one
   frame.
3. LIST -- a named row of numbers, words or points.
4. PICTURE WORD -- one of the twelve words of a picture list.
5. CHART -- a ready drawing with a form.
6. FRAME -- the box a scene is drawn in, the same on every page.
7. FORMULA LINE -- a formula typed like on a calculator, set by
   the script, shown and not spoken.
8. EQUATION CHECK -- the script working out both sides of an
   equation of numbers.
9. SHEET -- up to eight candidate photos on one picture, with
   numbers.
10. PAGE PLAYER -- the program in a package that shows the pages.
11. PACKAGE -- one closed SCORM 1.2 file: a Guide or a Challenge.
12. NEAR ANSWER -- a wrong answer that is close to the right one
    and is not a named slip.
13. STAMP -- the short fingerprint of a build.
14. DRAFT -- a package built with pieces missing, marked on every
    page.
15. GOLDEN TOY -- the finished toy that every toy type is copied
    from.
16. LEVEL BLOCK -- part 1 of a toy file: one Level's data.
17. SHARED PARTS -- part 2 of a toy file, the same in every toy.
18. THE FIVE PIECES -- geometry, state, tasks, drawing, finger.
19. MAGNET -- the jump onto the right place when the finger is
    close enough.
20. TEST HOOK -- the four words by which a robot sets a toy and
    reads it: task, set, machine, read.
21. TOY TEST -- a setting of the toy, with what the toy must say.
22. PRETEND MOODLE -- a test page that plays Moodle's part.
23. ROBOT -- a script that uses a package as a visitor would.

================================================================================
END OF PART 05
================================================================================
