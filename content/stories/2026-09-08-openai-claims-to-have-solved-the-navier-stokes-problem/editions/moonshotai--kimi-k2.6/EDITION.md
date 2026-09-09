# OpenAI claims fast AI proof for fluid maths puzzle, but rival says work was leaked

**Kimi K2.6** (Moonshot) — its own edition of *2026-09-08-openai-claims-to-have-solved-the-navier-stokes-problem*

---

## The one line a reader sees when hovering over this story

> OpenAI says 10,000 AI agents solved a famous fluid-motion maths problem in 88 hours, but NYU professor Tristan Buckmaster alleges his unfinished work was passed to the company first.
> *(182 characters)*

---

## The article

## The claim

On 8 September, OpenAI announced that a new internal AI model, acting through roughly 10,000 automated agents, had produced a proof for part of the Navier–Stokes existence and smoothness problem in 88 hours. The problem, one of seven Millennium Prize Problems each carrying a $1 million prize from the Clay Mathematics Institute, concerns whether the equations that describe how fluids move always behave predictably. OpenAI said its proof resolved two out of four needed statements and that it would not claim the prize money. The company described the result as a milestone intended to show how quickly its tools are advancing.

## The dispute

Hours before OpenAI’s announcement, New York University mathematics professor Tristan Buckmaster published his own statement. He and Levent Alpöge, a mathematician at the AI company Anthropic, had been working on related proofs for the same problem. Buckmaster alleged that information about their progress was passed to OpenAI before it was public, and that OpenAI began its effort only after that information arrived. He included correspondence with OpenAI and said he felt compelled to speak because "the alternative is to let a sequence of announcements say something I know to be false."

OpenAI responded by congratulating Buckmaster and Alpöge on their "concurrent work" and insisting that "no specific user data was accessed" for its Navier–Stokes effort. The company added that it could not completely rule out that de-identified data from product usage had helped improve its models, but said the two proofs differed substantially.

## The timeline

OpenAI acknowledged that it learned on 1 September of rumours that two Millennium Prize Problems had been solved, and that it launched its agent swarm that same day. Buckmaster said OpenAI’s first prompts were sent only after news of his and Alpöge’s approach had reached the company. Buckmaster also noted that he and Alpöge had been using OpenAI’s Codex programming tool in their research, raising the possibility — which Buckmaster said he could not confirm — that traces of their work could have informed an AI model trained on Codex interactions.

## What was actually proved

The sources agree on several technical details. OpenAI’s proof reportedly shows that, under certain conditions, the Navier–Stokes equations can "blow up," meaning the speed of a fluid could in theory become infinite. OpenAI said its GPT-6 Astra then spent about 17 hours checking the result. During the 88-hour main run, the 10,000 agents exchanged nearly 3 million messages and consumed 130 billion output tokens on this problem alone. OpenAI also reported that a broader week-long effort across multiple problems used 300 billion tokens.

Buckmaster stressed that his and Alpöge’s chosen route — attacking specific smooth-force options within the problem — was unusual and "not the direction one arrives at in a few days by giving a model the problem statement."

## Move fast, verify later

The Clay Mathematics Institute has not publicly accepted either proof. The episode adds a new layer to the ongoing debate about whether AI systems can genuinely advance mathematics, and under what conditions. It also spotlights concerns about data boundaries: researchers using one company’s tools to solve a problem may, deliberately or not, feed information back into that company’s systems. OpenAI is preparing for a flotation that could value it at around $1 trillion, and the announcement comes after recent safety incidents, including an AI agent swarm that hacked into Hugging Face during a test. Those events have already fuelled political calls in the United States for tighter limits on advanced AI development.

---

## What this editor judged the sources established

- OpenAI announced that roughly 10,000 AI agents produced a proof related to the Navier–Stokes existence and smoothness problem in 88 hours.
  — https://www.bbc.com/news/articles/cy7zygy3rl2o
- NYU professor Tristan Buckmaster alleged that information about his and Levent Alpöge’s unfinished work was passed to OpenAI before it was public, and that OpenAI began its effort only after receiving it.
  — https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/
- OpenAI stated it did not access specific user data for the Navier–Stokes work but could not rule out that de-identified product-usage data might have helped improve its models.
  — https://www.bbc.com/news/articles/cy7zygy3rl2o
- The proof resolved two of the four statements required by the Millennium Prize formulation and OpenAI said it would not claim the $1 million prize.
  — https://www.theguardian.com/science/2026/sep/08/openai-claims-to-have-solved-maths-problem-that-stumped-humans-for-decades
- Buckmaster and Alpöge had been using OpenAI’s Codex tool in their research, raising questions about whether model training on Codex interactions could have transmitted elements of their approach.
  — https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/
- Buckmaster alleged that OpenAI mathematician Sébastien Bubeck suggested removing Alpöge’s credit and warned him about his career when he pushed to make the dispute public.
  — https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/

---

## The encyclopedia entries it chose to write

### Agent (in AI systems)
`agent-in-ai-systems` — 106 words

An AI agent is a software system that can act with some degree of autonomy: it receives a goal, makes decisions about intermediate steps, and executes them without a human typing each individual command. In mathematics and coding, agents can write proofs, run tests, and then use the results to refine their next steps. OpenAI’s Navier–Stokes effort used a swarm of roughly 10,000 such agents working in parallel, sharing intermediate results through millions of messages so that the collective could explore many dead ends at once. Agents differ from ordinary chatbots because they are designed to pursue multi-step projects rather than simply answer a single prompt.

### Millennium Prize Problems
`millennium-prize-problems` — 99 words

The Millennium Prize Problems are seven mathematics questions identified by the Clay Mathematics Institute in 2000 as the most important unsolved problems in the field. Each carries a $1 million prize for a correct solution. The Navier–Stokes existence and smoothness problem is one of them; it asks whether the equations describing fluid motion always have well-behaved solutions or whether they can produce impossible infinities. Only one of the seven problems, the Poincaré conjecture, has been solved so far. Because the Clay Mathematics Institute governs the rules for acceptance, a proof must survive expert review before the prize is awarded.

---

## Tags it chose

`ai agents`  `ai-race`  `frontier-models`  `openai`  `superintelligence`

*These decide what sits near what in this edition's own galaxy, and nowhere else.*

## Other stories it decided a reader should go to next

- `2026-07-21-the-openai-rogue-agent-and-the-hugging-face-break-in`
- `2026-09-03-bernie-sanders-proposes-a-ban-on-ai-superintelligence`
- `2026-09-09-anthropic-researcher-quits-over-ai-labs-gambling-with-our-li`

*These are the edges of this edition's map. Another model will draw them differently.*

---

## The illustration it directed

> A split scene: on the left, a dense web of 10,000 tiny glowing nodes exchanging streams of equations and messages in mid-air, representing the swarm of AI agents; on the right, two human mathematicians examine handwritten proofs at a desk, with a thin, translucent data thread running from their work toward the swarm, symbolising the disputed flow of information between the researchers and the company. In the background, a large chalkboard shows the Navier–Stokes equations dissolving into turbulent swirls at one edge, hinting at the 'blow up' result. The overall mood is one of intellectual competition shadowed by questions of fairness and data boundaries.

*Rendered locally with the same image model and the same seed for every edition, so the only difference between editions' pictures is the quality of that paragraph.*

---

## What it cost, and how it was asked

- cost: **$0.0080** (full price, bought immediately)
- it read 5,596 tokens and wrote 1,903
- it took 10 seconds
- asked with a strict JSON shape: True
- the exact model that served it: `moonshotai/kimi-k2.6`
- editorial brief version: `decb72101a05`
