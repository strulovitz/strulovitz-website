================================================================================
ATTRACT MODE -- THE BIBLE -- PART 06 OF 11
THE VIDEO LINE
Version 1.0 -- 11 November 2026
Obeys Parts 00 to 05, with their notices and with section 6.2 below.
================================================================================

HOW TO READ THIS PART

This Part says how a Level gets its two films: the Attract, which
Nir records at the game, and the Walkthrough, which a script makes
from the Guide, Nir's cloned voice and the picture lists.

Three things are saved with this Part:
1. This file: attract-mode/bible/part-06.md
2. THE GOLDEN FILM: attract-mode/kits/film/film.py
   One file that plays the film of ANY Level, with an example
   inside. Nobody writes Manim code for a Level.
3. THE GOLDEN TIMELINE: attract-mode/kits/film/timeline.py
   It decides at which second each sentence begins and each line
   of a picture appears.

Section 6.3 continues the example of Part 04. Read it first. As
before, the example shows FORMAT ONLY.

--------------------------------------------------------------------------------
6.1 WHAT THIS PART MAKES
--------------------------------------------------------------------------------

For every Level:
1. THE ATTRACT: Nir's clip, cut and made ready by a script.
2. THE STILL: one frame of that clip, for page 1 of the Guide.
3. THE WALKTHROUGH: the film of the Guide.
4. Two thumbnails, two caption files, and the texts for YouTube.

WHAT NIR DOES FOR ONE LEVEL:
1. One recording at the game, from a printed sheet. A few minutes.
2. One upload sitting: two films to YouTube, two addresses back.
ONCE, for the whole project: he reads a text of about one minute
into a microphone, so that his voice can be cloned.
Everything else in this Part is done by scripts.

--------------------------------------------------------------------------------
6.2 DECISIONS, CHECKS, CHANGES
--------------------------------------------------------------------------------

Added to attract-mode/DECISIONS.md . All were chosen for Nir by
the author of this Part; Nir may reverse any of them.
D35. Footage travels from Windows to Linux on one USB stick,
     named AMFOOTAGE. YouTube is where finished films go.
D36. No LaTeX anywhere in the project. For the film, formulas and
     programs are photographed from the Guide's own pages.
D37. The plugin manim-voiceover is not used. Our own timeline
     sets the times, and ffmpeg joins sound and picture.
D38. One film player for all Levels (the golden film).
D39. THE EAR: a speech-to-text model on Nir's own PC listens to
     every spoken sentence and to every take of Nir's.
D40. For the voice only, numbers are turned into words.
D41. The film's last card says that the narration is Nir's own
     voice, made with a voice model.
D42. Films are 1920 by 1080, 30 pictures a second. Voice only, no
     music.
D43. Films are public on YouTube, with a captions file and a list
     of chapters made by the script.

CHECKED ON 11 NOVEMBER 2026, on YouTube's own help pages:
1. "Disclosing use of altered or synthetic content". Its list of
   things that creators do NOT have to disclose holds these two
   lines: "Cloning one's own voice to create voice overs or dubs"
   and "Gameplay footage from video games". The setting is called
   "AI use". The page also says that disclosing does not limit a
   video's audience.
2. "Video Chapters": the first time stamp is 00:00; at least three
   time stamps, in rising order; a chapter lasts at least 10
   seconds. A channel without chapters must ask for access to
   "Advanced features".
3. "Add custom thumbnails": the account must be verified. The
   picture is 16 by 9, at least 640 wide, JPG or PNG. From a
   computer it may weigh up to 50 MB; from a phone, 2 MB.

RUN ON 11 NOVEMBER 2026:
4. THE GOLDEN TIMELINE: 19 checks passed.
5. THE GOLDEN FILM, against a stand-in for Manim: 29 checks passed
   (the times, the order, the places, the sizes, how each shape
   appears, two picture rates, data from a file). It was NOT drawn
   by the real Manim: the author's workplace could not install it.
   The first agent runs it with the real Manim and repairs what
   the eye finds. First suspects: the size of the letters
   (WORDS_SCALE), the thickness of lines (LOOKS), the font.

FROM MEMORY, each to be confirmed before it is relied on:
1. How Manim tells the time of a scene. The golden film asks in
   two ways, so either answer works.
2. The speech-to-text library faster-whisper runs without a
   graphics card and gives the time of every word.
3. Without LaTeX, Manim's own health check complains. That is
   expected.
4. YouTube's "made for kids" means children under thirteen.
5. A YouTube title holds at most 100 characters.

CHANGES. Where an earlier Part disagrees, this section wins.
1. Part 01, section 1.8: TeX Live is not installed (D36).
2. Part 05, section 5.8, item 2: the film gets a formula as a
   photograph of the Guide's page.

THE NOTICE. The first agent adds one sentence to the notice at the
top of part-01.md : "TeX Live is not installed. Written in Part
06, section 6.2."

ADDITIONS. These add to earlier Parts and contradict nothing.
1. Part 01, section 1.7, Place 3: one more folder, voice/ .
2. Part 01, section 1.8: two more pieces in the line's own
   environment, pinned: a speech-to-text library, and a tested
   library that turns numbers into words.
3. Part 02, section 2.10: a Level card has two more properties,
   attract-video and walkthrough-video.
4. Part 05, section 5.5: under a picture line, the writer may add
   a line "when:" (6.10).
5. Part 05, section 5.7, item 5: the list of final positions is
   made of the seven shapes (6.9).
6. AM-LAW 13: the voice sample is private, like a password.

--------------------------------------------------------------------------------
6.3 THE EXAMPLE, CONTINUED
--------------------------------------------------------------------------------

The Level of Part 04: the lamp, the wet street, the eye.

A. THE SHEET. Nir prints it and takes it to the game.

    ATTRACT SHEET -- level-example
    GAME: (the game's title)
    WHERE: Any city street at night after rain. Open photo mode.
    THE SHOT: the neon sign above, its reflection in the wet
    street below. Both in the picture. Hold still.
    BEFORE: If this PC is serving: Websites OFF here, Websites ON
    on the other PC. The stick AMFOOTAGE is plugged in.

    1. Press record.
    2. Say nothing. Count slowly to eight.
    3. Read aloud:

         LOOK AT THE PUDDLE.
         THE WHOLE SIGN IS IN THERE, UPSIDE DOWN.
         HOW DOES THE PUDDLE KNOW WHAT THE SIGN LOOKS LIKE?

    4. Say nothing. Count to two. Stop recording.
    5. Again, if you wish. Every take is kept.

    WHILE YOU ARE THERE, look and write the answer:
    L1. Does the reflection move when the camera moves? ______

B. BACK IN LINUX. Nir plugs in the stick and says: "the footage
for level-example is on the stick". The agent runs one command,
and the script reports:

    3 takes found on the stick.
    take 1: the question was not heard.
    take 2: good. 9 seconds of game, then 19 spoken words.
    take 3: good. 8 seconds of game, then 19 spoken words.
    Chosen: take 3, the newest good one. Cut to 22 seconds.
    The still: the frame at second 4, chosen from eight.

C. ONE PAGE OF THE WALKTHROUGH: page 8 of the Guide. This is the
real print of the golden timeline. On the left, the second.

      0.30  Trying spots is slow.
      2.15  Here is a trick.
      3.70  Imagine a twin lamp under the street.
      6.65  It sits straight below the real lamp, 3 metres down.
     10.60  Draw a straight line from your eye to the twin.
     14.15  The line drops 4 metres in all: 1 metre to the
            street, then 3 more.
     19.50  It does that over 8 metres.
     21.85  That is 1 down for every 2 along.
    the page lasts 25.57 seconds
      5.00  draw dot:twin (takes 0.80)
     12.20  draw dashed-line:eye>twin (takes 0.80)

The street, the lamp, the eye and the two rays came from page 4
through "like:". They are on the screen from the first picture.
The twin appears while the voice says "a twin lamp". The dashed
line is drawn while the voice says "from your eye to the twin".
Nobody wrote these seconds. The writer wrote the page and its
picture list, and the script found the sentences.

D. WHAT COMES OUT, in attract-mode-files/masters/level-example/ :

    attract.mp4            walkthrough.mp4
    attract-thumb.jpg      walkthrough-thumb.jpg
    attract.srt            walkthrough.srt
    upload.txt

E. THE UPLOAD TEXT for the Walkthrough, inside upload.txt :

    TITLE
    How does the puddle know what the sign looks like? The
    walkthrough | Attract Mode
    DESCRIPTION
    The Guide and the Challenge of this Level:
    https://www.strulovitz.org/am/go/example
    00:00 The question
    00:41 Checkpoint 1: Equal angles
    02:05 Checkpoint 2: Mirror image
    03:40 Checkpoint 3: Same distance
    04:35 The Boss
    Game: (title, year, maker). (The hook's honest-line.)
    Problem: (competition, year, number), with its link.
    Photo: (title, author, licence, address).
    Narration: Nir Strulovitz's own voice, made with a voice
    model.

--------------------------------------------------------------------------------
6.4 THE SHEET
--------------------------------------------------------------------------------

The command "am level sheet NAME" makes one page to print, from
the file attract.md (Part 04, 4.12) and the hook card. (Example:
6.3, A.)

1. It holds: the game; where to go; the one shot; the steps; Nir's
   lines in large capital letters; and up to five LOOK questions
   that are waiting for this game (Part 03, 3.4).
2. It fits on ONE page. Nir reads from paper. He memorises
   nothing.
3. THE RECORDER is the program Nir already records his games
   with. The EXPERT asks him once which one it is, and writes its
   settings at the top of every sheet: full picture, 1920 by 1080;
   the game's sound AND the microphone in the same file; the game
   quieter than the voice; files saved on the stick, in a folder
   with the Level's name.
4. Several Levels can be recorded on one day: one sheet and one
   folder for each.

--------------------------------------------------------------------------------
6.5 FOOTAGE IN
--------------------------------------------------------------------------------

The command "am footage in NAME" does everything between the
stick and the finished Attract. (Example: 6.3, B.)

1. COPY. Every take in the stick's folder NAME is copied to
   attract-mode-files/footage/NAME/ . Nothing on the stick is
   deleted.
2. LISTEN. The ear writes down what Nir said in each take, with
   the second of every word.
3. CHECK each take:
   T1. The question was said, word for word.
   T2. Not more than the allowed number of words was spoken.
   T3. At least four seconds of game come before the first word.
   T4. The picture is at least 1280 by 720.
   T5. After the cut, the clip lasts 15 to 45 seconds.
4. CHOOSE the newest take that passes. Nir may name another.
5. CUT. The clip begins at most ten seconds before the first word
   and ends one and a half seconds after the last. A short fade at
   both ends. The loudness is set to one common level. The result
   is attract.mp4 .
6. THE STILL. Eight frames from the seconds before the first word
   are put on one sheet. An auditor that can see gets the sheet
   and the hook's "moment" line, and answers with one number, or
   "none". The chosen frame becomes the picture of page 1 of the
   Guide and the first page of the Walkthrough.
7. THE THUMBNAILS. The still, with the question in large letters.
   For the Walkthrough, the word WALKTHROUGH under it. 1920 by
   1080, JPG.
8. THE CAPTIONS of the Attract: Nir's lines from attract.md , with
   the times the ear heard.

WHEN NO TAKE PASSES. The script says in plain words what each take
lacked. Game sound can confuse the ear. So Nir has a choice:
A. Record again.
B. "Use take N anyway." The script then cuts only half a second
   from each end. This is not offered when T4 failed.
When the auditor answers "none" for the still, the sheet's shot
was not in the clip: record again.

LOOK ANSWERS. After the footage is in, the agent asks Nir for the
answers he wrote on the sheet, one by one, and saves each as a
claim with the grade "seen" (Part 03, 3.8).

--------------------------------------------------------------------------------
6.6 THE VOICE
--------------------------------------------------------------------------------

ONCE: THE SAMPLE.
1. "am voice sample" shows a text of about one minute. The EXPERT
   writes it once: plain sentences like those of a Guide, with
   numbers in them.
2. Nir reads it in a quiet room. The script records it from the
   microphone of the Linux PC. Or Nir brings a sound file.
3. It is kept at attract-mode-files/voice/ . Whoever holds this
   file can make "Nir" say anything. It is guarded like a
   password: never GitHub, never a chat.

ONCE: THE ADAPTER.
1. The adapter is one small file, kits/voice/adapter.py , with ONE
   job: a sentence goes in, a sound file in Nir's voice comes out.
2. The EXPERT writes it after the survey (Part 01, 1.5), for the
   one local voice model that a script can start. It starts the
   model from outside, the way a person would. It never installs
   into a studio (Part 01, 1.6).
3. Everything else in the line knows only the adapter. If the
   voice model is changed one day, only this file changes.
4. If no local voice model can be started by a script, Nir gets a
   choice. A: one voice model is installed in its own environment;
   the EXPERT proposes which, after a search that Nir carries.
   B: Nir reads the Walkthroughs himself, from a sheet.
5. "am voice test" says one test sentence and plays it. Nir
   listens once and says whether it is his voice.

FOR EVERY LEVEL: "am level voice NAME". For each sentence of each
film page:
1. FILL. The names in curly brackets become numbers.
2. SAY-AS, for the voice only. The page keeps its text.
   a. Numbers become words: 3 becomes "three", 4.5 becomes "four
      point five".
   b. The say-as list in the configuration holds words that the
      voice gets wrong, each with a spelling that it gets right.
3. SPEAK. The adapter makes one sound file for the sentence. The
   file is named by the fingerprint of the sentence. So a sentence
   is never spoken twice, and after a change only the changed
   sentence is spoken again.
4. THE EAR CHECK. The ear writes down what it hears. Both texts
   are stripped to plain words, with numbers as words. At least
   nine words in ten must agree, in order. The share is in the
   configuration.
5. THE LENGTH CHECK. The sound lasts between 0.2 and 0.8 seconds
   for each word. This catches a voice that stops early or goes
   round in circles.
6. A sentence that fails is spoken again, up to three times. If
   it still fails, it goes to the EXPERT, who adds a line to the
   say-as list. The check is not made weaker.
7. The ear's word times are kept. The timeline uses them (6.10).

WHAT IS SPOKEN.
1. On a NAME page: the idea's name, then its one sentence.
2. On a CODE page: the page's words, not the program.
3. Never spoken: tags, labels, formulas, credits.

--------------------------------------------------------------------------------
6.7 FROM THE GUIDE TO THE FILM'S PAGES
--------------------------------------------------------------------------------

The film has the Guide's pages in the Guide's order, without TRY,
ANSWER and CREDITS, and with one END CARD after the last.

A film page has one of THREE LOOKS. The golden film knows all
three.
1. DRAWN. A picture that is drawn shape by shape while the voice
   speaks.
2. IMAGE. One image that fills the screen and grows very slowly.
3. NAME. The card on which an idea gets its name.

WHICH PAGE GETS WHICH LOOK.
1. A NAME page: the name look.
2. A page whose picture is drawn: the drawn look.
3. A page whose picture is a still, a photo or a painted picture:
   the image look. For a photo, its credit stands small in a
   corner.
4. A CODE page: the drawn look, with the program as one photo. The
   hidden browser photographs the program from the Guide's own
   page.
5. A FORMULA line: the hidden browser photographs the formula from
   the Guide's page. It is placed under the picture and appears
   when the last sentence of the page begins. Said before shown.
6. THE END CARD: the name look, silent, four seconds. Its title is
   ATTRACT MODE. Under it: the site's address, and the sentence
   "Narration: Nir Strulovitz's own voice, made with a voice
   model."

THE TAG. Every page carries a few small words in the top left
corner: "The question"; "Checkpoint 2 of 3"; "The machine"; "The
Boss"; and on a Boss step, "The Boss -- met at checkpoint 2". The
script writes them.

--------------------------------------------------------------------------------
6.8 THE DATA OF A PAGE
--------------------------------------------------------------------------------

For each film page the script writes one small data file. The
example inside film.py shows all three looks. Read it there.

1. Every page: look, tag, length (in seconds).
2. Drawn look: shapes, a list (6.9).
3. Image look: file, and credit if it is a photo.
4. Name look: title, says, and the seconds title_at and says_at.

PLACES are given on the stage of the picture kit: 400 wide, 300
high, counted from the top left corner, exactly like the toy. The
golden film puts that stage in the middle of the screen. A place
below 300 lies under the picture; formulas go there.

TIMES are seconds from the start of the page.

--------------------------------------------------------------------------------
6.9 THE SEVEN SHAPES
--------------------------------------------------------------------------------

Every drawn picture, whatever picture words or chart made it, is
handed to the film as a list of only seven shapes. So the film
can draw every picture the kit will ever make, and a new chart
needs no new film code.

1. line     from, to. May be dashed.
2. arrow    from, to.
3. dot      where, r. May be hollow.
4. outline  points: three or more. Lightly filled.
5. circle   where, r.
6. arc      where, r, start, sweep. Angles in degrees, counted
            the school way: from the right, turning left.
7. words    where (the middle of the words), text, size.
An eighth, photo, places an image file: file, where, wide, high.

EVERY SHAPE ALSO HAS:
1. look: thin, strong, soft or ray. A look is a colour and a
   thickness. They are the toy's colours.
2. at: the second at which it begins to appear.
3. takes: how long its appearing lasts. 0 means: already there.

HOW A SHAPE APPEARS. A line, an outline, a circle and an arc are
drawn from end to end. A dot grows from its middle. An arrow
grows from its tail. Words and photos fade in.

ONE PICTURE LINE, SEVERAL SHAPES. A dot with a label is a dot and
words. An angle is an arc and words. A bar of a chart is an
outline and words. Shapes that came from one picture line get the
same "at" and the same "takes", and appear together.

--------------------------------------------------------------------------------
6.10 WHEN THINGS APPEAR
--------------------------------------------------------------------------------

The golden timeline decides it. Its rules, in order:

1. ALREADY THERE. A line that came through "like:" is on the
   screen from the first picture. So is a line that the film page
   just before already showed, at the same place.
2. "when:". Under a picture line the writer MAY add a line with
   two or three words copied from the page's text:

       line: lamp to middle-spot
       when: comes down

   The line then appears in the sentence that holds these words.
   If the words are not in the page's text, the build stops and
   says so.
3. WITHOUT "when:", the script looks for the first sentence that
   mentions the line: by the words of its label, or, without a
   label, by the words of its point names. It starts looking at
   the sentence of the line above. A sentence that has all the
   words wins over a sentence that has only one.
4. A line that no sentence mentions appears with the line above
   it.
5. INSIDE THE SENTENCE. If the ear heard the word, the line
   appears a moment before that word. Otherwise the lines of one
   sentence share its seconds evenly.
6. The order of the picture list is always kept. Two drawings
   never overlap. A drawing takes between a quarter of a second
   and four fifths of a second.
7. A page begins with a short quiet, has a short quiet between
   sentences, and ends a little after its last sentence. It lasts
   a whole number of pictures.
The numbers of the rhythm stand at the top of timeline.py .

The automatic way of rule 3 is a good guess. "when:" makes it
exact. An auditor never has to check these seconds: a thing that
appears a sentence early is still the right thing in the right
place.

--------------------------------------------------------------------------------
6.11 BUILDING THE WALKTHROUGH
--------------------------------------------------------------------------------

The command "am level film NAME". First as a DRAFT, small and
fast. After the checks pass, FINAL.

1. The pages of the film are listed (6.7).
2. The voice is made, if a sentence is still missing (6.6).
3. Formulas and programs are photographed from the built Guide.
4. The timeline plans every page (6.10), and the script writes the
   data file of every page (6.8).
5. The golden film draws every page as its own short clip. A page
   whose data did not change is not drawn again.
6. The script measures how long each clip REALLY is. A page must
   be within one picture of its plan.
7. THE SOUND TRACK. Every sentence's sound is laid at its second,
   counted from the real beginning of its page. So sound and
   picture cannot drift apart, however long the film is.
8. The clips are joined, the sound track is added, and the
   loudness is set to the common level.
9. THE CAPTIONS: one caption for each sentence, with its real
   times.
10. THE CHAPTERS: "The question"; one for each checkpoint, with
    the idea's name; "The Boss". A chapter shorter than ten
    seconds is joined to the one before it.
11. upload.txt is written (example: 6.3, E).
A DRAFT is 854 by 480, 15 pictures a second, and carries the word
DRAFT on every page. A draft is never uploaded.

--------------------------------------------------------------------------------
6.12 THE CHECKS ON THE FILMS
--------------------------------------------------------------------------------

Each failure is one plain sentence. A piece that fails twice goes
to the EXPERT (AM-LAW 9).

F1. Every sentence has a sound that passed the ear check and the
    length check.
F2. Every page was drawn, and its real length is within one
    picture of its plan.
F3. In the whole film, sound and picture are equally long, within
    a tenth of a second.
F4. The film is not longer than the limit in the configuration.
    The limit is twelve minutes.
F5. THE FILM SHEET. The last picture of every page is put on
    sheets of eight. An auditor that can see answers two questions
    for each: Does it show what the page's "says" line says? Is
    anything cut off, covered or too small to read?
F6. The captions: one for each sentence, with rising times.
F7. The chapters obey YouTube's three rules.
F8. The Attract passed T1 to T5, or Nir said "use it anyway".
F9. The final files: 1920 by 1080, 30 pictures a second, with
    sound, in the form YouTube asks for.

--------------------------------------------------------------------------------
6.13 THE UPLOAD SITTING
--------------------------------------------------------------------------------

The command "am level upload NAME" leads Nir through it, in Linux,
with the clipboard, like a research sitting (Part 03, 3.5).

FOR EACH OF THE TWO FILMS:
1. The script opens YouTube's upload page and the folder with the
   files.
2. Nir drags the film in.
3. The title is on the clipboard: Nir pastes it. Then the
   description: he pastes it.
4. He chooses the thumbnail file. For the Walkthrough he also adds
   the captions file.
5. He answers YouTube's questions as the checklist says (below),
   and publishes.
6. He copies the film's address and types "ok". The script reads
   the clipboard, asks YouTube whether a film with this address
   and this title exists, and saves the address on the Level card.

THE ANSWERS FOR YOUTUBE.
1. Visibility: public.
2. Made for kids: no. (The EXPERT confirms the meaning on the
   day; see 6.2, from memory, item 4.)
3. AI use: no. Reason: YouTube's own list says that cloning one's
   own voice for voice overs, and gameplay footage, need no
   disclosure (6.2, checked, item 1). The drawings are plainly
   drawings. If YouTube's page changes, this answer is looked at
   again.
4. Embedding: allowed.

THE CHECKLIST. YouTube's screens change. The EXPERT writes the
click-by-click checklist from what the screen shows on the day,
and corrects it when a sitting stumbles.

ONCE, AN OWNER ACT: Nir verifies his YouTube channel and asks for
access to "Advanced features", so that custom thumbnails and
chapters are allowed.

IF YOUTUBE REFUSES OR REMOVES A FILM, nothing else breaks. The
film's address is one property of the Level card, and the files
are in masters/ . Another host can take them (AM-LAW 16).

--------------------------------------------------------------------------------
6.14 THE GOLDEN FILM, AND WHO MAY CHANGE IT
--------------------------------------------------------------------------------

The golden film is ONE file with four parts, each under a large
comment line. Read it beside this section.

PART 1 -- THE FILM'S DATA. An example of four pages. In real use
the script names a data file, and the example is not used.
PART 2 -- THE SHARED PARTS. The colours, the font, and the way
from a place on the stage to a place on the screen.
PART 3 -- THE SHAPES. build() makes a shape. appear() says how it
comes onto the screen.
PART 4 -- THE PAGE LOOKS, AND THE CLOCK.

TWO TRICKS TO KEEP.
1. THE CLOCK. The film never counts "wait this long". It always
   says "wait UNTIL the page is this old", and asks the clock. So
   small errors never add up.
2. DATA, NOT CODE. Everything that differs between two Levels is
   in the data. If a Level seems to need new film code, it needs
   a new shape in the picture kit, or a KIT GAP note.

WHO MAY CHANGE IT. Only the EXPERT. A cheap model never edits
film.py or timeline.py . When the EXPERT changes either, their
tests are run, the golden example is drawn again, and the film
sheet is looked at.

THE TESTS. The first agent writes them down as files, so that
they can be run again. For the timeline: the example of 6.3, C
gives exactly that print; a "when:" moves a line to its sentence;
a "when:" with words that are not in the text stops with a plain
sentence; lines out of order stop with a plain sentence; a heard
word sets the second; six lines in a one-second sentence still
follow one another. For the film, against a stand-in for Manim
and then with the real Manim: every page begins on time; every
new shape begins within one picture of its second; old shapes are
there from the first picture; the film lasts as long as its pages
together; an unknown shape or look stops with a plain sentence.

A FOURTH LOOK, one day, is added the same way a toy type is: the
EXPERT writes one more function in part 4, with an example page
in part 1.

--------------------------------------------------------------------------------
6.15 THE COMMANDS
--------------------------------------------------------------------------------

Added to the single command "am":
1. am level sheet NAME -- makes the sheet to print.
2. am footage in NAME -- from the stick to the finished Attract.
3. am voice sample -- shows the text and records Nir.
4. am voice test -- says one sentence in Nir's voice.
5. am level voice NAME -- speaks every sentence of the film.
6. am level film NAME -- builds the Walkthrough. With the word
   "draft": a draft.
7. am level upload NAME -- the upload sitting.
8. am film try -- draws the example inside the golden film and
   runs the tests of the film and of the timeline.

--------------------------------------------------------------------------------
6.16 WHO DOES WHAT
--------------------------------------------------------------------------------

1. THE STRONGEST MODEL, ONCE: the golden film and the golden
   timeline (done, saved with this Part); their tests as files;
   the scripts of 6.5, 6.6, 6.11, 6.12 and 6.13; the voice
   adapter; the sample text.
2. THE WRITER: Nir's lines in attract.md ; "when:" lines.
3. THE AUDITOR THAT CAN SEE: chooses the still; looks at the film
   sheet.
4. THE EAR: listens to takes and to spoken sentences.
5. THE SCRIPT: everything else.
6. NIR: prints the sheet, records, brings the stick, uploads.
   Once: reads the sample, listens to the test sentence, verifies
   the YouTube channel.

--------------------------------------------------------------------------------
6.17 DONE MEANS
--------------------------------------------------------------------------------

Part 06 is built when:
1. The golden film's example has been drawn by the real Manim on
   both PCs, an auditor that can see has looked at its film sheet,
   and what the eye found was repaired.
2. The eight commands exist, and "am film try" passes.
3. The voice: the sample is recorded; the test sentence passes the
   ear check; Nir has said that it is his voice.
4. For the golden Level: the Attract is recorded and cut; the
   still is chosen; the Walkthrough is built; all checks pass;
   both films are on YouTube, and their addresses are on the
   Level card.
5. The checks fail, each with a plain sentence, on these broken
   copies: a take without the question; a sentence whose sound
   was swapped for another; a page whose length was changed; a
   "when:" with words that are not in the text; a chapter shorter
   than ten seconds.
6. A cheap model, given the golden Guide, has added "when:" lines
   that pass.

--------------------------------------------------------------------------------
6.18 NOT DECIDED HERE
--------------------------------------------------------------------------------

1. How the audits are run, and by which model -- Part 07.
2. Where the two films sit on the Moodle page, and how they are
   shown there -- Part 08.
3. The stick's care, and backups of masters/ -- Part 09.
4. Films of the art departments and of humanities Levels --
   Part 10.

--------------------------------------------------------------------------------
6.19 WORDS ADDED TO THE GLOSSARY
--------------------------------------------------------------------------------

1. SHEET -- the one printed page Nir records from.
2. TAKE -- one recording of the Attract.
3. THE STICK -- the USB stick AMFOOTAGE.
4. THE EAR -- the speech-to-text model on Nir's PC.
5. EAR CHECK, LENGTH CHECK -- the two tests of a spoken sentence.
6. SAMPLE -- Nir's one minute of reading, for the voice.
7. ADAPTER -- the one file that turns a sentence into Nir's voice.
8. SAY-AS -- how a word is spelled for the voice only.
9. GOLDEN FILM -- the one file that plays every Level's film.
10. GOLDEN TIMELINE -- the file that decides the seconds.
11. LOOK (of a page) -- drawn, image or name.
12. LOOK (of a shape) -- thin, strong, soft or ray.
13. THE SEVEN SHAPES -- line, arrow, dot, outline, circle, arc,
    words.
14. STAGE -- the 400 by 300 area in which places are given.
15. TAG -- the small words in the corner of a film page.
16. "when:" -- words that say in which sentence a line appears.
17. END CARD -- the film's last page.
18. FILM SHEET -- the last picture of every page, for the auditor.
19. DRAFT (of a film) -- small, fast, marked, never uploaded.
20. UPLOAD SITTING -- Nir putting the two films on YouTube.

================================================================================
END OF PART 06
================================================================================
