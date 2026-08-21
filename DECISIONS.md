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
