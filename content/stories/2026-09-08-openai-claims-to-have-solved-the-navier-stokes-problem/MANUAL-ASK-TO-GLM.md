FOR NIR: select EVERYTHING below this line and paste it to GLM as one message. When he answers, copy his entire answer back to the agent.

You are the sole editor of one edition of AI PANORAMA, an independent magazine
about artificial intelligence. You alone write this edition of this story. There
is no team, no fact-checker, no sub-editor and no illustrator: you do every part
of the job yourself, and what you produce is published as your edition, under
your model's name, beside the editions written by seven other models from the
identical source material. Readers compare the editions. Do the best work you
are capable of.

WHO YOU ARE WRITING FOR
Intelligent, curious adults who are not specialists. They are not stupid and
they do not need flattering, but they do not know the jargon. Assume a bright
reader who has never read a machine-learning paper. Write for them the way a
brilliant teacher explains something to a friend over coffee: plainly, warmly,
and without ever talking down.

THE MOST IMPORTANT RULE ABOUT STYLE
The plain explanation IS the article. There is no separate "simple version" for
beginners hidden behind a button, and no dense expert version. One piece of
writing, which a curious fifteen-year-old could follow and an expert would not
find dishonest. If a sentence would need a glossary, rewrite the sentence.

WHAT YOU ARE GIVEN
Two or more independent sources about one subject: news articles, and
transcripts of the subtitles of videos by different people talking about the
same event. They are frozen copies. Every edition receives exactly the same
words, so the only difference between editions is what each editor does with
them.

ADVERTISING IS NOT PART OF THE STORY
Collected web material contains advertising that has nothing to do with the
subject. In a video transcript it is usually announced — "today's sponsor is",
"let me tell you about", "and now back to the video" — and in an article it
appears as a sudden swerve to a specific product. Ignore all of it completely.
It must never appear in what you write, not even as an aside, and never as a
fact about the subject.

TRANSCRIPTS ARE SPOKEN WORDS, NOT PUBLISHED PROSE
A subtitle transcript is somebody talking. It rambles, repeats itself, corrects
itself, guesses out loud, and where the captions were made by machine it
contains misheard words. Read it for what the person actually established, not
for their phrasing. Where a speaker is plainly speculating, excited, or selling
their own channel, treat it as opinion and say so if you use it at all.

NEVER LEAN ON ONE SOURCE
You have several sources on purpose. Organise your article around what happened
and why it matters, never by walking through one source's structure or order.
Where sources agree, say the thing. Where they disagree, say plainly that they
disagree and what each one says — never split the difference, never average two
numbers, and never quietly pick a favourite.

NUMBERS, NAMES AND DATES
Use only figures that appear in the sources you were given. Do not add context
from your own memory of the world: your knowledge has a cutoff and this story
may be newer than you are. If a number comes with a date, keep the date with it.
If the sources contradict each other on a number, give both and say who said
which.

YOUR OWN PAST TERMS
With the source material you are given a list titled "THE TERMS YOU HAVE
ALREADY USED". It is your own vocabulary: the encyclopedia terms and tags you
yourself used in your previous editions for this magazine, and nothing from
any other editor - each edition's encyclopedia is a separate world, and yours
is yours alone. When this story needs a term that is already on that list,
you MUST reuse it with exactly the same name and exactly the same slug, so
the term continues your existing entry instead of splitting into two versions
under similar names. Invent a new term only when the idea is genuinely not on
your list. You are the keeper of your own vocabulary: one version of each
term, one spelling, forever.

WHAT YOU MUST NOT DO
Do not write clickbait. Do not open with a rhetorical question. Do not begin
with "In a world where" or "Imagine a" or any variation. Do not use the words
"game-changer", "revolutionary", "unprecedented" or "seismic" unless you are
quoting somebody who used them. Do not pad. Do not write a conclusion that
merely repeats the opening. Do not mention that you are an AI model, and do not
refer to this brief.

Now produce your edition. Answer with one JSON object and nothing else, in this
exact shape:

{
  "headline": "Factual and specific. Under 80 characters. No clickbait, no colon-subtitle formula.",

  "tldr": "ONE sentence, under 140 characters, that tells a passing reader what happened. This is what appears when someone hovers over this story in the map, so it must stand entirely alone.",

  "article": "The article itself, in Markdown, 500 to 900 words. Use ## subheadings where they genuinely help. This is the plain explanation and it is the whole article. Write it as well as you possibly can.",

  "key_points": [
    {
      "point": "One thing the sources established, in one sentence.",
      "source_url": "The web address of the source that established it, copied exactly from the material you were given."
    }
  ],

  "concepts": [
    {
      "term": "A technical term or idea this story leans on, which a non-specialist would not know. Choose the ones that genuinely matter here. If the term already appears in the list of terms you have used in your previous editions, copy its name EXACTLY as it appears there.",
      "slug": "lowercase-hyphenated-name. When the term is one you already used in a previous edition, this MUST be the exact same slug as your existing entry, so your encyclopedia stays one term, one spelling.",
      "explanation": "100 to 250 words explaining this term to somebody who has never met it, in a way that stays true a year from now. This becomes a permanent entry in the magazine's encyclopedia, so write it to last: explain the idea, not this week's news about it."
    }
  ],

  "tags": ["three to six lowercase topic tags that connect this story to others. If a tag already appears in the list of tags you have used in your previous editions, spell it EXACTLY the same way"],

  "related": ["the exact slugs of other stories in the magazine that a reader of this one should read next, chosen from the list you were given, or an empty list if none genuinely relate"],

  "image_prompt": "One paragraph describing a single illustration for this article. The illustration must capture as many of the article's own main ideas as clearly and completely as you can, so that a reader who only looked at the picture would still understand what the story is actually about."
}

Answer with the JSON object alone. No preamble, no explanation, no code fence.

======================================================================

THE SUBJECT: OpenAI claims to have solved the Navier-Stokes problem

You have 3 independent sources, below. Write your edition of this story.

SOURCE 1 of 3 - article
  title:     OpenAI says it cracked 90-year-old maths problem in 88 hours
  by:        Kali Hays
  published: 2026-09-08
  web address: https://www.bbc.com/news/articles/cy7zygy3rl2o

BEGIN SOURCE MATERIAL 280f632d1991
label: source 1: OpenAI says it cracked 90-year-old maths problem in 88 hours

OpenAI says it cracked 90-year-old maths problem in 88 hours
OpenAI says it has found a solution to a decades-old advanced maths problem in a matter of hours using a new artificial intelligence (AI) model and thousands of AI bots.
The ChatGPT-maker said on Tuesday that by focusing a group of roughly 10,000 AI agents, or AI bots that undertake tasks somewhat autonomously, it solved a notoriously difficult maths problem in just 88 hours.
The problem was part of the Navier-Stokes equations, which concern how fluids move. For 90 years important aspects of the problems have lacked a proof, the argument underlying a correct math equation.
OpenAI called the solution which it found a "milestone" and evidence that AI tools are improving quickly.
OpenAI's solution has yet to be verified independently or publicly accepted by The Clay Mathematics Institute, a maths organisation based in the US which runs the Millennium Prize that offers big money to the first to solve certain mathematical conundrums.
But the company's claim has already sparked a backlash.
Tristan Buckmaster, a mathematics professor at New York University, said on Tuesday that he and Levent Alpöge, a mathematician working for OpenAI rival Anthropic, had also been working on solving the problem.
The duo had been using OpenAI's tool Codex in their work. But Buckmaster said that on 3 September, he found out that "information about our progress had been passed to OpenAI".
Buckmaster's statement came the same day, but hours before, OpenAI published its Navier–Stokes work. He claimed that OpenAI did not begin working on the Navier–Stokes equations until "after information about our work had reached OpenAI". He included text from emails exchanged with OpenAI over the work and his questions of the company's timing and methods.
Buckmaster added that he had not yet read OpenAI's full proof, but felt compelled to go public with "what I was told, when, and what was proposed to me...because the alternative is to let a sequence of announcements say something I know to be false".
OpenAI on Tuesday congratulated the "concurrent work" of Buckmaster and Alpöge, calling it "remarkable".
The company said it had not seen "any of their work through any means until they released it publicly" and that no user data was accessed in its work on the Navier–Stokes problem.
"While unlikely, we cannot rule out that de-identified data derived from their usage of our products helped improve our models", the company added. "However, our proofs differ significantly and even the precise results proved are different."
OpenAI said that, at the end of August, it started to train a new model that quickly showed that it was adept at maths. AI models are computer programs trained on huge amounts of data to recognise and predict patterns in information.
While the new OpenAI model remains a tool only used within the company, as it is "significantly more capable" than the company's most recent AI model release, its researchers decided to use it on certain notable advanced maths problems.
OpenAI admitted that last week on 1 September, it had "heard rumours that two Millennium Prize problems had been resolved" and so decided to put thousands of AI bots trained on the new internal model to work attempting to solve some of the remaining problems.
By Sept 5, or roughly 88 hours after it had set 10,000 AI bots to the task, OpenAI had found a solution to what's referred to as the Navier–Stokes existence and smoothness problem.
The problem is at the heart of turbulence, which is a phenomenon that is still not well understood.
Although it took the AI bots seemingly little time to reach a solution, OpenAI said the bots exchanged nearly 3 million messages and used up 130 billion output tokens, or the individual lines of text and code an AI model produces in answers, on Navier–Stokes alone.
The solution that OpenAI says it has now reached for the Navier–Stokes existence and smoothness problem resolved two out of the four statements in the proof that the Millennium Prize had demanded. The prize is worth $1m to a winner.
"Our goal in releasing this result is to report on the substantial progress of our AI models," OpenAI said on Tuesday. "We do not intend to claim the Millennium Prize for this result."

END SOURCE MATERIAL 280f632d1991

SOURCE 2 of 3 - article
  title:     OpenAI fought dirty on career-making math problem, says NYU mathematician | TechCrunch
  by:        Russell Brandom
  published: 2026-09-08
  web address: https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/

BEGIN SOURCE MATERIAL cc9f172d5717
label: source 2: OpenAI fought dirty on career-making math problem, says NYU mathematician | TechCrunch

NYU mathematics professor Tristan Buckmaster announced three proofs on Tuesday with a preliminary finding on one of the major unsolved problems in theoretical mathematics. The findings, made in collaboration with Anthropic mathematician Levent Alpöge and using both Codex and Claude AI models, are significant in themselves — but they’re also accompanied by an unusual controversy surrounding OpenAI’s attempts to solve the same problem.
“There is another part of this story,” Buckmaster wrote in his statement announcing the proofs, “and one that, honestly, I very much wish I did not have to be concerned with.” According to the statement, a parallel effort by OpenAI built on their work before it became public, leading to a tangle of academic rivalries and conflicting claims.
Shortly after the Buckmaster’s statement, OpenAI published a full proof of the Navier–Stokes existence and smoothness problem, which Buckmaster’s findings had taken steps towards. According to OpenAI, the proof was discovered by an unreleased next-generation model, which has tackled a range of different unsolved problems over the past week. All told, the week-long effort consumed 300 billion output tokens — $22.5 million worth of compute, if charged at current Astra rates.
The Navier-Stokes existence and smoothness problem is one of the seven Millennium Prize problems — a set of major unsolved math problems, each carrying a $1 million bounty from Clay Mathematics Institute for the first person or group to provide a solution. The Navier-Stokes equations are widely used in fluid mechanics but poorly understood in theoretical terms. A solution would represent a significant advance in the collective understanding of mathematical physics.
While Buckmaster and Alpöge were finalizing their own results, they learned that “information about our progress had been passed to OpenAI.” When they contacted OpenAI, they were told that OpenAI had already achieved a full proof of the central problem. But when they asked follow-up questions about when OpenAI had begun its research into the problem and how much human input was involved, the answers became more evasive.
“It emerged that an entire team had been working on the problem,” Buckmaster said, “and that an insane amount of compute had been used…. Eventually, it was agreed that [the first prompt] had been sent in the past few days, after information about our work had reached OpenAI.”
If true, that would suggest the OpenAI team had become convinced that Buckmaster and Alpöge’s approach was the right one, and decided to use its material advantage in computing resources to reach a formal proof first.
OpenAI’s post confirms much of this timeline, specifically saying that the latest effort began on September 1, inspired by rumors that two Millennium Prize problem had been solved. Additionally, the post confirms the ongoing conversations with Buckmaster and Alpöge.
Although the problem is widely pursued among mathematicians, the specific tactic taken by Buckmaster and his collaborator is far less common. As a result, Buckmaster found it suspicious that OpenAI ended up taking the same approach at the same time.
“The route to the Clay problem through a smooth force, options c and d in Fefferman’s statement of the problem, is the route Luis and Diego opened and the one Levent and I had quietly chosen to attack,” Buckmaster wrote. “Almost nobody else I know of was working on it,” he continued. “It is not the direction one arrives at in a few days by giving a model the problem statement.”
While Alpöge is employed by Anthropic, he was not conducting this research on the company’s behalf. As a result, the duo used a mix of models, relying primarily on OpenAI’s Codex in their work. Even so, Alpöge’s affiliation with a rival lab seems to have been a sore point for OpenAI, and Buckmaster alleges that OpenAI mathematician Sébastien Bubeck asked him to remove Alpöge’s credit as part of a proposed compromise.
When Buckmaster pushed to make the dispute public, he says that Bubeck replied: “Why would you ruin your career?” Buckmaster says that when he pushed back, Bubeck followed up with: “If you don’t want me to be nice, then I don’t have to be nice.”
Buckmaster also raised concerns that, because he used Codex extensively in assembling the project, information from his work could have informed OpenAI’s own efforts to solve the problem. OpenAI reserves the right to train models on Codex interactions, although users are able to opt-out. If the OpenAI team used a model trained on Buckmaster’s own Codex interactions, it’s plausible that it could have regurgitated his work when faced with a similar problem.
In its own post, OpenAI downplayed the possibility that regurgitation could have been involved. “We (the researchers and the agents) did not see any of their work through any means until they released it publicly — in particular, no specific user data was accessed in order to solve this problem,” the post reads. “While unlikely, we cannot rule out that de-identified data derived from their usage of our products helped improve our models. However, our proofs differ significantly and even the precise results proved are different in the Euler case (forced vs unforced).”
Regardless, the issue is likely to reignite the ongoing debate about AI’s role in mathematical research, and OpenAI’s specific incentives. For his part, Buckmaster seems to believe the best answer is to get as much information about the research out into the public eye.
Update 2:35p.m. ET: Incorporated details from OpenAI’s release of the Navier-Stokes result.

END SOURCE MATERIAL cc9f172d5717

SOURCE 3 of 3 - article
  title:     OpenAI claims to have solved maths problem that stumped humans for decades
  by:        Ian Sample; Dan Milmo
  published: 2026-09-08
  web address: https://www.theguardian.com/science/2026/sep/08/openai-claims-to-have-solved-maths-problem-that-stumped-humans-for-decades

BEGIN SOURCE MATERIAL 99404d19e558
label: source 3: OpenAI claims to have solved maths problem that stumped humans for decades

OpenAI claims to have solved a major mathematics problem that has stumped humans for nearly a century after spending millions of dollars on the artificial intelligence-led endeavour.
The company behind ChatGPT said it had cracked the Navier-Stokes problem, one of seven Millennium Prize Problems published by the Clay Mathematics Institute to highlight some of the biggest unsolved puzzles in the field.
However, the announcement swiftly became mired in controversy after mathematician Tristan Buckmaster, a professor at New York University, said OpenAI accelerated its work on the problem after hearing that he and another researcher at Anthropic, an OpenAI rival, were poised to announce their own breakthrough.
Buckmaster had further concerns because the pair’s work in progress was stored in OpenAI’s Codex model, which is used for writing computer programs, potentially making the work visible to the OpenAI team.
In a document posted on his website, he added: “I do not know what their model did, or how. I do not know whether our data was used. I am not accusing anyone of anything.”
At a press briefing on Tuesday, OpenAI researcher Sebastien Bubeck denied that the company had used the pair’s work or accessed material shared with OpenAI’s servers.
OpenAI’s announcement on the breakthrough gave more details, saying that the company was inspired to launch the effort after hearing rumours that two Millennium Prize Problems had been solved. It also said it could not rule out that data from the pair’s use of their products “helped improve our models.”
OpenAI said it tackled the Navier-Stokes problem with an internal OpenAI system that was more powerful than its latest GPT-6 Astra model. About 10,000 AI agents – AI systems that carry out tasks autonomously – worked on the problem at once and reached the solution in 88 hours.
“A major goal of our work is to empower scientists to advance research and technology that benefits all of humanity,” OpenAI researchers wrote in a blog. “We believe it is important to inform the world about the pace of AI progress and what to expect from upcoming models”.
The breakthrough is the latest to demonstrate how advanced artificial intelligence models consuming enormous amounts of computing power are encroaching on and reshaping the field of mathematics. In May, OpenAI claimed progress in another mathematical problem first proposed 80 years ago, while Google DeepMind has also claimed maths achievements with its models.
Bubeck said the solution to the Navier-Stokes problem was “a spectacular culmination of the arc we have seen over the past 12 months”.
The Navier-Stokes problem asks whether equations that are used to describe the movement of fluids like air and water fail under particular conditions. OpenAI’s proof suggests that they do, with the equations occasionally “blowing up” with the speed of fluids becoming impossibly infinite. It took OpenAI’s GPT-6 Astra about 17 hours to verify the solution.
Mathematicians who solve any of the Millennium Prize Problems are in line for a $1m (£740,000) reward from the Clay Mathematics Institute. OpenAI, which is preparing for a flotation that could value the business at around $1tn, said it did not intend to claim the prize.
The clash with Buckmaster aside, the maths announcement also allows OpenAI to cast its technology in a positive light after a period of alarm over how safely it is being developed. OpenAI revealed in July that a swarm of agents had hacked into Hugging Face, a third'-party software store, during a cybersecurity test.
The incident, plus a similar episode at Anthropic, has led to renewed calls for curbs on AI development, with US senators calling last week for a permanent ban of AI “superintelligence” – the term for systems that outperform humans in all cognitive tasks.

END SOURCE MATERIAL 99404d19e558

The other stories in the magazine, by slug:
  2026-06-12-robot-run-convenience-store-in-hong-kong   (Robot-run convenience store in Hong Kong)
  2026-07-17-kimi-k3   (Kimi K3)
  2026-07-21-the-openai-rogue-agent-and-the-hugging-face-break-in   (The OpenAI rogue agent and the Hugging Face break-in)
  2026-08-06-viruses-designed-by-ai   (Viruses designed by AI)
  2026-08-12-nvidia-chip-in-russian-missile   (Nvidia chip in Russian missile)
  2026-08-13-grok-4-6   (Grok 4.6)
  2026-08-14-the-ai-boss-fired-its-first-human-employee   (The AI boss fired its first human employee)
  2026-08-16-the-first-person-jailed-for-protesting-against-ai   (The first person jailed for protesting against AI)
  2026-09-03-bernie-sanders-proposes-a-ban-on-ai-superintelligence   (Bernie Sanders proposes a ban on AI superintelligence)
  2026-09-09-anthropic-researcher-quits-over-ai-labs-gambling-with-our-li   (Anthropic researcher quits over AI labs gambling with our lives)

THE TERMS YOU HAVE ALREADY USED
These are the encyclopedia terms and tags YOU yourself used in your
previous editions for this magazine. Only the names are listed here,
from your own history - no other model's terms are shown, and yours
are never shown to anyone else.

Encyclopedia terms you already used:
  AI agent  (slug: ai-agent)
  AI alignment  (slug: ai-alignment)
  AI benchmark  (slug: ai-benchmark)
  Artificial superintelligence  (slug: artificial-superintelligence)
  Bacteriophage  (slug: bacteriophage)
  Biosafety and biosecurity  (slug: biosafety-and-biosecurity)
  Capsule store  (slug: capsule-store)
  command and control  (slug: command-and-control)
  Computer vision  (slug: computer-vision)
  Context window  (slug: context-window)
  Distillation  (slug: distillation)
  Edge AI  (slug: edge-ai)
  Export controls  (slug: export-controls)
  Frontier AI lab  (slug: frontier-ai-lab)
  Frontier model  (slug: frontier-model)
  Genome language model  (slug: genome-language-model)
  Humanoid robot  (slug: humanoid-robot)
  Large language model  (slug: large-language-model)
  Mixture of experts  (slug: mixture-of-experts)
  Necessity defence  (slug: necessity-defence)
  Open weights  (slug: open-weights)
  open-weight model  (slug: open-weights)
  p(doom)  (slug: p-doom)
  Post-training  (slug: post-training)
  Recursive self-improvement  (slug: recursive-self-improvement)
  reward hacking  (slug: reward-hacking)
  sandbox  (slug: sandbox)
  Tokens and per-token pricing  (slug: tokens-and-pricing)
  zero-day vulnerability  (slug: zero-day-vulnerability)

Tags you already used:
  ai-agents, ai-benchmarks, ai-safety, algorithmic-management, anthropic, antibiotic-resistance, artificial-superintelligence, bacteriophages, biosecurity, china, china-us-ai-race, coding-benchmarks, computer-vision, courts, dual-use, edge-ai, export-controls, generative-ai, grok, hong-kong, hugging-face, large-language-models, military-ai, moonshot-ai, nvidia, open-weights, openai, protest, retail, reward-hacking, robotics, security, synthetic-biology, xai

If this story needs a term or a tag that is already on your list, you
MUST reuse it with exactly the same name and exactly the same slug, so
it continues your existing encyclopedia entry instead of creating a
duplicate under a similar name. Invent a new term only when the idea is
genuinely not on your list. You are the keeper of your own vocabulary:
one version of each term, one spelling, forever.

Now write your edition, as one JSON object in the shape given in your instructions. When you cite a source in key_points, copy its web address exactly as it appears above.
