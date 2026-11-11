================================================================================
ATTRACT MODE -- THE BIBLE -- PART 08 OF 11
MOODLE
Version 1.0 -- 11 November 2026
Obeys Parts 00 to 07, with their notices and with section 8.2 below.
================================================================================

HOW TO READ THIS PART

Moodle is the website. This Part says how it is laid out, where
its installation goes wrong, how a parent pays, and how a
finished Level gets into it. Section 8.3 is the example. Read it
first.

The names of Moodle's settings are written from memory. The
EXPERT writes the exact clicks on the day, from what the screen
shows. Section 8.10 tests everything that matters.

This file is saved VERBATIM at: attract-mode/bible/part-08.md

--------------------------------------------------------------------------------
8.1 WHAT MOODLE DOES, AND WHAT IT NEVER DOES
--------------------------------------------------------------------------------

1. It shows everything: the front page, the departments, the
   Levels.
2. It keeps what only it can keep: accounts, payments, scores.
3. It is never the source. Every text, every film address and
   the whole layout come from the files in Git, put in by a
   script. Nobody types content into Moodle by hand.
4. No extra plugin and no extra theme.

--------------------------------------------------------------------------------
8.2 DECISIONS, CHANGES, FROM MEMORY
--------------------------------------------------------------------------------

Added to attract-mode/DECISIONS.md . All were chosen for Nir by
the author of this Part; Nir may reverse any of them.
D47. A department is one free Moodle course, open to guests. It
     appears when its first Level is live. A Level is one
     section of it.
D48. All Challenges are in ONE paid course. Its public name is
     Insert Coin.
D49. One family, one account. The parent's progress page is the
     Grades page of that account.
D50. A script builds everything in Moodle through Moodle's own
     functions. Nir drops in the two packages of each Level.
D51. A Challenge may be tried any number of times. The highest
     score counts.
D52. Badges wait.
D53. Nobody who bought can see who else bought.
D54. OPEN, Nir's: the price of Insert Coin, and whether it buys
     access for ever or for a number of days. Until he says:
     for ever.

CHANGES. Where an earlier Part disagrees, this section wins.
1. Part 04, section 4.1: the Attract, the Guide and the
   Walkthrough sit in the Level's section of its department.
   The Challenge, with the toy, sits in Insert Coin.
2. AM-LAW 11: Moodle is rebuilt from the files by one command,
   except for the packages, which Nir drops in.
3. AM-LAW 15: the public words also include Insert Coin.
4. Part 00, section 0.7: badges come later (Part 11).
THE NOTICE. The first agent adds to the notices at the top of
part-00.md and part-04.md one sentence: "Also changed by Part
08, section 8.2."

FROM MEMORY. Each is confirmed by a test of 8.10 or on the day.
1. Moodle's PayPal takes ONE payment. It cannot charge every
   month by itself.
2. "Enrolment on payment" can end access after a number of days.
3. A zip file dragged onto a course page in edit mode can be
   added as a SCORM package.
4. Behind a tunnel, Moodle's settings file needs the line
   sslproxy.
5. A section of a course has its own address.
6. Moodle turns a plain YouTube address into a player.
7. Moodle has its own age check at sign-up.
8. Replacing a package keeps the earlier scores, if the
   identifiers in its manifest stay the same.

--------------------------------------------------------------------------------
8.3 THE EXAMPLE: A STRANGER AND A PARENT
--------------------------------------------------------------------------------

A. A STRANGER. Maya, 15, gets a link from a friend:
   www.strulovitz.org/am/go/example . Her phone opens the
   Level's page. Nobody asks her to sign in. She sees:

       How does the puddle know what the sign looks like?
       [ the Attract, ready to play ]
       Guide
       [ the Walkthrough, ready to play ]
       The toy and the Challenge of this Level are in
       Insert Coin.

   She plays the clip, opens the Guide and presses Next.

B. A PARENT. Her father opens Insert Coin. He reads what is
   inside, and the price. He presses the pay button. Moodle asks
   him to make an account: his email, a password, a nickname for
   his daughter. He ticks: "I am an adult. This account is
   mine." An email arrives, and he presses its link. He pays
   with PayPal. The Challenges open at once.

C. Maya plays the toy and answers the eight questions: 6 of 8.

D. That evening the father signs in with the same account and
   opens Grades. One line for each Challenge, with its score.

E. WHAT NOBODY CAN DO: write to Nir through the site; see who
   else bought; find Maya's real name.

--------------------------------------------------------------------------------
8.4 THE LAYOUT
--------------------------------------------------------------------------------

THE FRONT PAGE, from the top:
1. The name Attract Mode, and the tagline.
2. The newest Level: its question and its Attract, ready to
   play.
3. The departments: Moodle's list of courses, each with one
   sentence and a picture.
4. Insert Coin.

THE MENU: Departments, All Levels, By school topic, Insert
Coin, Art, About Nir, The Prequels.

SITE PAGES, made by the script from files in Git:
1. All Levels -- every Level with its game, its question and
   its link. This is the door "by game".
2. By school topic -- the parent's door, from the topic cards
   (Part 02, 2.6).
3. About Nir -- his story (Part 00, 0.2).
4. Corrections -- from corrections.md (Part 07, 7.8).
5. Privacy -- what is kept (an email, a nickname, scores), that
   there is no advertising, and how to have an account deleted.

A DEPARTMENT. One free course. One section for each Level, each
on its own page. The section's title is the hook's question.
Inside, in this order: the Attract; the Guide; the Walkthrough;
one line that points to Insert Coin.

INSERT COIN. One paid course. One section for each department.
In it, one Challenge for each Level, named by the Level's
question. Its summary says what is inside and how many
Challenges there are today.

STUDIO WORDS. Moodle says "courses". With Moodle's own language
tool, the EXPERT renames the few words a visitor meets on the
way to a Level, for example "Available courses" to
"Departments". At most ten.

THE LOOK. Moodle's standard theme, with the colours of
look.css .

--------------------------------------------------------------------------------
8.5 INSTALLING: WHERE IT GOES WRONG
--------------------------------------------------------------------------------

The order is in Part 01, section 1.9, item 4. These are the
places where an installation behind a tunnel fails.

1. THE ADDRESS. Moodle is installed with
   https://www.strulovitz.org from the first minute.
2. THE TUNNEL. The visitor speaks https to Cloudflare. Caddy
   speaks plain http to Moodle. Moodle must be told, with the
   line sslproxy in its settings file. Without it the site
   turns in circles or loads without its styles.
3. THE VISITOR'S ADDRESS. Moodle must see the visitor's own
   address, which Cloudflare passes on. Otherwise every visitor
   looks like one person, and one wrong password locks out
   everybody.
4. THE WEB SERVER. Caddy answers /am/ itself. Everything else
   goes to Moodle's "public" folder, with PHP running as Nir's
   user. What matches no file goes to Moodle's router.
5. PHP. Moodle's own environment page must show no warning.
   Uploads of at least 20 MB are allowed.
6. THE DATABASE. Its own database and its own user, in full
   Unicode.
7. THE ADMIN PASSWORD. Nir chooses it and types it himself.
8. THE CLOCK. Moodle's clock runs every minute, on the serving
   PC only (Part 09).
9. English only.

--------------------------------------------------------------------------------
8.6 THE SETTINGS THAT MATTER
--------------------------------------------------------------------------------

GUESTS. A visitor is let in as a guest with no click. Every
department allows guests, with no password. In the departments
Moodle remembers nothing, for anybody. What is remembered is in
Insert Coin.

ACCOUNTS.
1. A parent makes the account, and confirms it by email.
2. The sign-up page says: "First name: a nickname for your
   teenager. Surname: one letter is enough."
3. To sign up, one box must be ticked: "I am an adult. This
   account is mine. The nickname is not a real name."
4. Moodle's own age check is switched on.
5. THE SIGN-UP PAGE IS GUARDED at Cloudflare by a challenge.
   Without it, robots use our sign-up to send our confirmation
   mail to strangers, and the mail service closes our account.

PRIVACY (AM-LAW 14).
1. Switched off: messages, forums, comments, blogs, notes, the
   mobile app's door, outside web services, badges.
2. NOBODY WHO BOUGHT CAN SEE WHO ELSE BOUGHT. In Insert Coin, a
   player may not see the list of participants or anybody
   else's profile.
3. Profiles are not public. Emails are hidden.
4. DELETING. A parent writes to the contact address. The agent
   deletes the account with Moodle's own privacy tool.

PACKAGES. Set once, for the whole site: a package opens in the
same window, at its first page, with no contents list and no
Moodle buttons inside it, at full width.

PROGRESS. In Insert Coin, each Challenge gets a tick when it
has a score. The Grades page lists the scores.

--------------------------------------------------------------------------------
8.7 EMAIL
--------------------------------------------------------------------------------

Moodle must send two kinds of mail: the confirmation, and the
forgotten password. A home connection cannot deliver mail.

1. An outside mail service sends it. The EXPERT proposes one,
   after a search that Nir carries: free or nearly free for a
   few hundred mails a month.
2. OWNER ACTS: Nir opens the account there; adds, at
   Cloudflare, the records the service asks for, so that mail
   from strulovitz.org is believed; and types the service's
   password into Moodle's mail settings.
3. The sender is no-reply@strulovitz.org . The contact address
   for parents is Nir's choice. It stands on the Privacy page.

--------------------------------------------------------------------------------
8.8 PAYPAL
--------------------------------------------------------------------------------

1. ONE PAYMENT. The price buys access for ever, or for a number
   of days. After that the parent may pay again (D54).
2. OWNER ACTS: in PayPal's pages for developers, Nir makes an
   "app" and gets two keys. He types them into Moodle's payment
   page himself.
3. The script adds "Enrolment on payment" to Insert Coin, with
   the price, the currency and the days from the configuration.
4. PRETEND MONEY FIRST. PayPal has a test mode. Then ONE real
   purchase by Nir, from a second account, and its refund.
5. A REFUND is given by Nir, in PayPal. Then the agent ends
   that account's access in Moodle. Neither happens by itself.
6. PayPal sends the receipt. Moodle keeps only who, when and
   how much.

--------------------------------------------------------------------------------
8.9 THE BUILDER, AND NIR'S UPLOAD
--------------------------------------------------------------------------------

"am moodle sync" makes Moodle match the files.

1. THE HANDS. Small PHP programs in line/moodle/ . Each does
   one thing, through Moodle's own functions: the same ones
   that Moodle's screens use. They never write into the
   database, and never copy files into Moodle's folders.
2. THE MARK. Everything the script makes carries an ID number
   that begins with "am-". The script touches only marked
   things. It never deletes: a retired Level is hidden, and its
   scores stay.
3. SAME TWICE. A second run changes nothing. With the word
   "dry", it only says what it would change.
4. IT BUILDS: the front page, the menu, the site pages, the
   departments and their sections, the film players, Insert
   Coin with its price, and the short links.
5. It runs on the serving PC only.

NIR'S UPLOAD, for one Level. This is step 16 of the line.
1. Sign in as admin. Open the department. Switch edit mode on.
2. Drag the Guide file from the packages folder onto the
   Level's section. Choose "Add a SCORM package".
3. Open Insert Coin. Drag the Challenge file onto the
   department's section. The same choice.
4. Say "uploaded".
Then the agent runs the sync. It knows each package by its
fingerprint, which must be that of the newest build. It gives
the package its public name, its place and its mark. The
Level's state becomes "live". Its short link is made. Last, the
Level's page is fetched as a guest.

A CORRECTION. Open the package's settings, drop the new file
over the old one, save, and say "uploaded". The packer keeps
the manifest's identifiers the same from build to build, so
that the scores stay.

LATER. If the uploads become a burden, the EXPERT can write one
more hand, which adds a package through Moodle's own functions.
Nir decides.

--------------------------------------------------------------------------------
8.10 FIRST THINGS TO TRY
--------------------------------------------------------------------------------

With the golden Level. On a phone, on mobile data, in a private
window.

T1. A guest opens the front page, a department, the Level, and
    turns the Guide's pages. No sign-in is asked.
    IF MOODLE REFUSES GUESTS: the Guide is also put under
    /am/guide/NAME/ as plain files, and the Level's page shows
    it in a frame. The package works without Moodle (Part 05,
    5.11).
T2. A new account without payment sees the price and the pay
    button, and cannot open a Challenge.
T3. A payment with pretend money opens the Challenges. A score
    of 6 of 8 arrives, and stands on the Grades page.
T4. A second account cannot see the first.
T5. The confirmation mail and the password mail arrive at two
    different mail providers, and not in the spam folder.
T6. A package is replaced by a new build. The old score is
    still there.
T7. Websites OFF, then ON at the other PC (Part 09). Everything
    above still holds.

"am moodle try" runs T1, T2, T4 and T6 by itself. T3, T5 and T7
need Nir, once.

--------------------------------------------------------------------------------
8.11 COMMANDS, ROLES, DONE
--------------------------------------------------------------------------------

COMMANDS, added to "am":
1. am moodle sync -- with the word "dry": only says.
2. am moodle try

WHO DOES WHAT.
1. THE STRONGEST MODEL, ONCE: the installation; the hands; the
   settings of 8.5 and 8.6.
2. THE WORKHORSE: runs the sync and the tests.
3. NIR, OWNER ACTS, each from a checklist written on the day:
   O4. The admin password.
   O5. The mail service and its records.
   O6. The PayPal keys.
   O7. The challenge on the sign-up page, at Cloudflare.
   And for each Level, the upload.

DONE MEANS.
1. www.strulovitz.org opens in Moodle, and the old site answers
   at pre.strulovitz.org (Switch Day, Part 01).
2. T1 to T7 hold.
3. The golden Level is live, and its short link works.
4. A second run of the sync changes nothing.

WORDS ADDED TO THE GLOSSARY.
1. DEPARTMENT (in Moodle) -- one free course.
2. INSERT COIN -- the one paid course, with all Challenges.
3. SITE PAGE -- a page of the site, made from a file in Git.
4. STUDIO WORDS -- the few Moodle words that are renamed.
5. THE HANDS -- the small programs that work inside Moodle.
6. THE MARK -- the ID number "am-" on everything the script
   made.
7. SYNC -- making Moodle match the files.

================================================================================
END OF PART 08
================================================================================
