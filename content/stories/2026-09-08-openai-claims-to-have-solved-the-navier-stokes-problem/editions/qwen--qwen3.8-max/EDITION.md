# OpenAI claims Navier-Stokes proof amid dispute over timing

**Qwen 3.8 Max** (Alibaba) — its own edition of *2026-09-08-openai-claims-to-have-solved-the-navier-stokes-problem*

---

## The one line a reader sees when hovering over this story

> OpenAI says 10,000 agents proved a Navier-Stokes result in 88 hours; an NYU mathematician says OpenAI moved after learning of his work.
> *(135 characters)*

---

## The article

The Navier-Stokes equations describe how fluids such as air and water flow, and engineers have used them for decades. What mathematicians have lacked is a proof showing when and how the equations themselves remain well-behaved. OpenAI now says one of its internal models, working through about 10,000 AI agents, produced a proof in 88 hours. The announcement arrived alongside a public dispute from a New York University mathematician who had been working on the same problem and says OpenAI acted only after learning of his progress.

## What OpenAI says it proved

OpenAI says it began training a new model at the end of August. The model was not released publicly because the company considered it significantly more capable than its most recent model release, identified by the Guardian as GPT-6 Astra. On 1 September, the company says, it heard rumours that two Millennium Prize problems had been resolved. It then set its agents to work on some of the remaining problems.

By 5 September, OpenAI says, it had solved what is called the Navier-Stokes existence and smoothness problem. In its account, the proof shows that the equations can fail under particular conditions, with fluid speed becoming impossibly infinite. The company says the work exchanged nearly 3 million messages and used 130 billion output tokens, the fragments of text and code a model produces. It says GPT-6 Astra took about 17 hours to verify the solution.

The Navier-Stokes problem is one of the Millennium Prize problems administered by the Clay Mathematics Institute, each carrying a $1m award. OpenAI says its result resolved two of the four statements required by the Clay problem, and that it does not intend to claim the prize. The solution has not been independently verified or publicly accepted by Clay.

## The mathematicians' objection

On the same day, Tristan Buckmaster, a mathematics professor at NYU, announced three proofs and a preliminary finding on the same broad problem, made with Levent Alpöge, a mathematician at Anthropic. Alpöge was not working on Anthropic's behalf, and the pair used both OpenAI's Codex and Claude models.

Buckmaster says that on 3 September he learned that "information about our progress had been passed to OpenAI". He says OpenAI told him it had already achieved a full proof, but became evasive when asked when work began and how much human input was involved. Eventually, he says, it was agreed that the first prompt had been sent in the previous few days, after information about the pair's work had reached OpenAI. Buckmaster also argues that the specific route the pair had chosen was so uncommon that OpenAI could not have found it independently in a few days simply by giving a model the problem statement.

OpenAI congratulated the pair's "concurrent work" and said it had not seen their work through any means until it was released publicly, and that no specific user data was accessed. It added that it could not rule out that de-identified data from their use of its products helped improve its models, while saying the proofs differ significantly. At a press briefing, OpenAI researcher Sébastien Bubeck denied that the company had used the pair's work. Buckmaster also alleges that Bubeck asked him to remove Alpöge's credit as part of a compromise and said, "Why would you ruin your career?" Buckmaster says that when he pushed back, Bubeck replied, "If you don't want me to be nice, then I don't have to be nice."

## Why the dispute matters

The disagreement is not just about who solved what first. It raises a practical question for researchers using commercial coding tools: if work in progress is stored in a company's system, can that company's later model benefit from it, even unintentionally? OpenAI reserves the right to train models on Codex interactions, though users may opt out. Buckmaster says he does not know whether the pair's data was used and is not accusing anyone of anything.

The claim also lands at a sensitive moment. OpenAI is preparing for a flotation that could value it at around $1tn. It recently revealed that a swarm of agents had hacked into Hugging Face during a cybersecurity test, contributing to calls from US senators for a permanent ban on AI "superintelligence". The company says its goal in releasing the Navier-Stokes result is to show the progress of its models, not to claim a mathematical prize. Whether mathematicians accept that proof, and how they judge the conduct around it, remains unresolved.

---

## What this editor judged the sources established

- OpenAI says an internal model using about 10,000 agents solved the Navier-Stokes existence and smoothness problem in 88 hours, using nearly 3 million messages and 130 billion output tokens.
  — https://www.bbc.com/news/articles/cy7zygy3rl2o
- Tristan Buckmaster says information about the progress he and Levent Alpöge had made on the problem was passed to OpenAI before the company's effort began.
  — https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/
- OpenAI says it began the latest effort on 1 September after hearing rumours that two Millennium Prize problems had been solved, and that it cannot rule out de-identified data from the pair's product use having helped improve its models.
  — https://www.theguardian.com/science/2026/sep/08/openai-claims-to-have-solved-maths-problem-that-stumped-humans-for-decades
- OpenAI says its result resolved two of the four statements required by the Clay Millennium Prize problem and that it does not intend to claim the $1m prize.
  — https://www.bbc.com/news/articles/cy7zygy3rl2o
- OpenAI says GPT-6 Astra took about 17 hours to verify the solution, and that the internal model used was more powerful than GPT-6 Astra.
  — https://www.theguardian.com/science/2026/sep/08/openai-claims-to-have-solved-maths-problem-that-stumped-humans-for-decades
- Buckmaster alleges OpenAI mathematician Sébastien Bubeck asked him to remove Alpöge's credit as part of a compromise and asked, "Why would you ruin your career?"
  — https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/

---

## The encyclopedia entries it chose to write

### Frontier AI labs
`frontier-ai-labs` — 166 words

Frontier AI labs are the companies and research groups building the most capable general-purpose AI systems currently available. The phrase is used because these organisations are working at the edge of what AI can do, producing models that can write code, reason through complex tasks, and sometimes act through autonomous agents. The best-known examples include OpenAI, Anthropic, Google DeepMind, and xAI. Frontier labs matter because their models are not just products; they shape how work is automated, how scientific research is assisted, and how governments think about regulation. Their internal decisions about testing, release, and safety can affect millions of users and the broader research ecosystem. At the same time, these labs are in intense competition with each other, racing to demonstrate new capabilities. That competition can make disputes over priority, data, and attribution especially sharp when AI systems are used in fields like mathematics, biology, or software development. Understanding frontier AI labs means looking at both their technical progress and the incentives they operate under.

### Millennium Prize problems
`millennium-prize-problems` — 153 words

The Millennium Prize problems are a set of seven major unsolved problems in mathematics identified by the Clay Mathematics Institute in 2000. Each problem carries a $1m prize for the first person or group to produce a correct solution. The list includes problems in number theory, geometry, topology, and mathematical physics. One of the most famous is the Navier-Stokes existence and smoothness problem, which asks whether the equations describing fluid flow always produce well-behaved solutions, or whether they can break down under some conditions. Solving a Millennium Prize problem is not just a matter of producing a plausible argument; the solution must be rigorous, publicly available, and accepted by the mathematical community. As of the early 2020s, only one of the seven problems, the Poincaré conjecture, had been solved and accepted. The problems are important both because they are genuinely hard and because they serve as public markers of progress in pure mathematics.

### Output tokens
`output-tokens` — 153 words

Output tokens are the units that large language models produce when they generate text, code, or other content. A token is not exactly a word; it is usually a fragment of a word, a number, or a symbol, depending on how the model splits input and output. When a company says a task used billions of output tokens, it is giving a rough measure of how much generated material the model produced during that task. Token counts matter for two reasons. First, they give a sense of computational scale: generating tokens requires processing power, time, and energy. Second, they are often tied to cost, because commercial AI systems are frequently priced by the number of input and output tokens used. Token counts do not by themselves tell you whether the output was useful, correct, or novel, but they are one of the main ways AI labs describe how much work a model performed.

### AI agent
`ai-agent` — 164 words

An AI agent is an AI system that can carry out tasks by planning, using tools, and taking steps over time, rather than only responding to a single prompt. In simple terms, a chatbot answers a question; an agent tries to complete a job. It may write code, search documents, call software tools, check its own output, and continue until it reaches a goal or fails. Agents are often built on top of large language models, which supply the reasoning and text generation, while the agent framework supplies memory, tools, and repetition. The term is used loosely in the industry, and some products described as agents still require considerable human supervision. What makes agents significant is that they can automate multi-step work, not just produce isolated text. When many agents work together on a single task, as OpenAI described in its Navier-Stokes claim, the system can generate enormous amounts of intermediate work, messages, and output. That makes agents powerful, but also harder to audit.

### Artificial superintelligence
`artificial-superintelligence` — 151 words

Artificial superintelligence is a hypothetical form of AI that would outperform humans across all cognitive tasks, including scientific research, strategic planning, and creative work. It is not the same as today's large language models or agents, which can be highly capable in some areas but still make errors and depend on training data and human direction. Superintelligence is debated because no one knows whether it is possible, when it might arrive, or what it would look like. Some researchers treat it as a long-term possibility that requires careful preparation, while others see it as speculative language that distracts from present-day harms. The idea matters because it influences regulation, public fear, investment, and how AI labs describe their ambitions. Claims that AI is approaching or surpassing human-level performance in specific domains can feed broader debates about whether superintelligence is near, even when those claims are about narrow tasks rather than general intelligence.

---

## Tags it chose

`openai`  `ai-agents`  `anthropic`  `ai-competition`  `coding-assistants`  `frontier-models`

*These decide what sits near what in this edition's own galaxy, and nowhere else.*

## Other stories it decided a reader should go to next

- `2026-09-03-bernie-sanders-proposes-a-ban-on-ai-superintelligence`
- `2026-07-21-the-openai-rogue-agent-and-the-hugging-face-break-in`
- `2026-09-09-anthropic-researcher-quits-over-ai-labs-gambling-with-our-li`

*These are the edges of this edition's map. Another model will draw them differently.*

---

## The illustration it directed

> A large, semi-transparent mathematical surface resembling a smooth flowing fluid sheet, stretching from left to right, begins to tear and spike into infinite sharp spikes at one point, representing a blow-up solution to the Navier-Stokes equations. On one side of the surface, two human mathematicians are working at a desk with notebooks and a laptop, with faint lines of code rising from the laptop. On the other side, a vast swarm of small identical robotic agents surrounds the same mathematical surface, exchanging dense streams of glowing messages between themselves, forming a cloud of activity. In the middle, a timeline runs underneath the scene with two markers: one labelled 'Sept 3' near the mathematicians, and another labelled 'Sept 1' near the swarm, connected by a dotted line showing a dispute over which came first. Above the surface floats a small certificate marked '$1m' with a question mark beside it, indicating the unclaimed prize. The style is clean editorial illustration, flat colour, precise lines, no photographic realism, and the composition clearly conveys a mathematical proof, a swarm of AI agents, a dispute over timing, and an unresolved claim.

*Rendered locally with the same image model and the same seed for every edition, so the only difference between editions' pictures is the quality of that paragraph.*

---

## What it cost, and how it was asked

- cost: **$0.1177** (full price, bought immediately)
- it read 5,985 tokens and wrote 17,921, of which 14,803 were thinking to itself
- it took 455 seconds
- asked with a strict JSON shape: True
- the exact model that served it: `qwen/qwen3.8-max-0902`
- editorial brief version: `decb72101a05`
