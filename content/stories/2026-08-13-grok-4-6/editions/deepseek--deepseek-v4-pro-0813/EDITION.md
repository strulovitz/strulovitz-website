# xAI's Grok 4.6 now competes with the best AI models

**DeepSeek V4 Pro** (DeepSeek) — its own edition of *2026-08-13-grok-4-6*

---

## The one line a reader sees when hovering over this story

> xAI released Grok 4.6, a model that challenges OpenAI and Anthropic on several benchmarks and powers a new always-on agent product.
> *(131 characters)*

---

## The article

On 13 August 2026, xAI released Grok 4.6, an update to the model it launched earlier as Grok 4.5. For the first time, reviewers described a Grok model as genuinely competitive with the leading systems from OpenAI and Anthropic — and for the past two years, that top shelf has mostly been a two-lab race.

## What changed

Grok 4.6 is not a model built from scratch. According to Wes Roth, it shares a 1.5 trillion parameter base model with Grok 4.5. A parameter is one of the adjustable weights inside a neural network; more parameters generally mean a larger, more expensive model, though size alone does not decide quality. The main difference this time was a much longer supplemental training run. The company said it used curated model-generated data for reasoning and advanced technical concepts, high-quality engineering data, and an improved training recipe. Much of that data came from Cursor, the coding company xAI acquired.

## Where it sits — and where the sources disagree

The three sources do not fully agree on exactly how good Grok 4.6 is. On an OpenAI benchmark for knowledge work — the transcripts call it GPT Val or GDP Val — Grok 4.6 High scored first, ahead of Anthropic's Fable 5 Max and OpenAI's 5.6 Soul. On Cursor Bench, it was roughly equivalent to Fable 5 Max. But on DeepSWE, a coding benchmark several commentators consider the most faithful to real work, it placed third: 65.9, behind GPT 5.6 Soul Max at 73 and Fable 5 at 70.

Wes Roth calls Grok 4.6 'neck to neck' with the best models. Matthew Berman says it is excellent but not the best at coding on DeepSWE. Bijan Bowen says it is not quite Fable 5 or 5.6 level in coding yet, but the jump from 4.5 to 4.6 is significant. All three agree xAI is now close enough to be treated as a serious third competitor.

## Price and speed

Grok 4.6 costs $2 per million input tokens and $6 per million output tokens, with a fast variant at twice the price. Tokens are the pieces of text a model reads and writes, and output usually costs more because the model generates it step by step. Bijan Bowen compares that with $2 input and $10 output for Anthropic's Sonnet 5 and $2 input and $12 output for GPT 5.6, making Grok's output price roughly half of GPT 5.6's. Matthew Berman notes that on the Artificial Analysis cost-per-task chart, Grok 4.6 became more expensive than 4.5 — about 83 cents per task, up from about 36 cents — while also scoring higher. The model is available in Cursor, Grok Build, the API, and through Open Router, Vercel and Cloudflare, with double usage in Cursor and Grok Build during launch week.

## Why coding and Cursor matter

All three sources connect the improvement to xAI's acquisition of Cursor. Cursor had a mountain of coding data but lacked the data centers to train frontier models. xAI had compute — Matthew Berman says it built 200,000 GPUs in 122 days — but its model was not yet popular with developers. The combination, he argues, gave xAI both the data and a reason to focus on coding and knowledge work.

Bijan Bowen's hands-on tests support the 'good at building things' impression. He asked the model to create games, a 3D-printable engine model, an iPod Mini-style website and a wedding site with holographic avatars. He was most impressed by the front-end work. Wes Roth asked it to clone a Portal 2 test chamber in Grok Build and said it handled portals, momentum and reflections in one main attempt, with some steering.

## Grok Bot and what comes next

The day before Grok 4.6, xAI released Grok Bot, an always-on agent product. Each agent runs on its own cloud virtual machine, so it keeps working even when the user's computer is off. Users talk to a lead 'chief of staff' agent that delegates to sub-agents, and there is a 'teach a task' recording feature. Wes Roth compares it to handing work to a colleague rather than prompting a chatbot. As the videos were recorded, the commentators were unsure whether Grok 4.6 was yet live inside Grok Bot.

Elon Musk said Grok 4.7 should be ready in three to four weeks, with initial training complete and a 'massive amount' of SpaceX company data being added in supplemental training. Wes Roth adds that xAI has reorganized to ship major updates every two to three weeks, with Grok 5 targeted before the end of the year. Matthew Berman points out that Anthropic has been buying compute from xAI, and suggests xAI may eventually keep more of that GPU capacity for its own products.

The practical takeaway is that xAI has moved from afterthought to credible third front, but the race is moving fast. The sources disagree on whether Grok 4.6 is already at the very top; they agree it is close enough to matter.

---

## What this editor judged the sources established

- Grok 4.6 was released on 13 August 2026 as an iterative improvement on Grok 4.5, sharing the same 1.5 trillion parameter base model.
  — https://www.youtube.com/watch?v=VB39bHByHuU
- Grok 4.6 is priced at $2 per million input tokens and $6 per million output tokens, with a fast variant at twice the price.
  — https://www.youtube.com/watch?v=rdYBjpylJUQ
- On an OpenAI benchmark for knowledge work, which the transcripts call GPT Val or GDP Val, Grok 4.6 High scored first, ahead of Fable 5 Max and 5.6 Soul.
  — https://www.youtube.com/watch?v=rdYBjpylJUQ
- On the DeepSWE coding benchmark, Grok 4.6 placed third at 65.9, behind GPT 5.6 Soul Max at 73 and Fable 5 at 70.
  — https://www.youtube.com/watch?v=rdYBjpylJUQ
- xAI used data from its acquisition of Cursor, including engineering data and model-generated reasoning data, in Grok 4.6's supplemental training.
  — https://www.youtube.com/watch?v=VB39bHByHuU
- Elon Musk said Grok 4.7 should be ready in three to four weeks and is adding a massive amount of SpaceX company data in supplemental training.
  — https://www.youtube.com/watch?v=rdYBjpylJUQ
- Grok Bot, released the day before Grok 4.6, gives each agent its own cloud virtual machine and includes a 'teach a task' recording feature.
  — https://www.youtube.com/watch?v=VB39bHByHuU

---

## The encyclopedia entries it chose to write

### Token
`token` — 160 words

A token is the basic unit of text that a large language model reads or writes. A token is often a whole short word, a part of a longer word, or a punctuation mark. When a model processes a prompt, it breaks the text into tokens. When it writes a response, it produces tokens one piece at a time. Providers charge by the token because the amount of computation depends on how many tokens are read and written. Prices are usually quoted per million tokens and split into two parts. Input tokens are the prompt and any context sent to the model. Output tokens are the model's reply, and they usually cost more because the model generates them step by step. So a price such as '$2 per million input and $6 per million output' means a user pays two dollars for every million tokens they hand the model, and six dollars for every million tokens the model hands back.

### Benchmark
`benchmark` — 118 words

A benchmark is a standardized set of tasks or questions used to measure how capable an AI model is. Different benchmarks test different skills, such as coding, mathematics, legal reasoning, general knowledge, or real-world knowledge work. Benchmark scores give researchers and users a way to compare many models at once, but they have limits. A model can score well on a benchmark and still fail in ordinary use, and some companies have been accused of training models to 'game' particular tests. That is why observers often pair benchmark scores with hands-on testing and with measures of cost per task. In this story, the disagreements about Grok 4.6 reflect the fact that different benchmarks pointed in slightly different directions.

### Agent
`agent` — 131 words

In AI, an agent is a system that does more than answer a question: it can take actions, use tools, and carry out tasks, often over a period of time. A simple chatbot only responds. An agent might open a web browser, write code, search the internet, control software, or ask another agent to do part of a job. Some agents are 'always-on,' meaning they run on a remote computer, often called a virtual machine, and keep working even when the user's own device is closed. In products such as Grok Bot, a user may talk to one lead agent, sometimes called a chief of staff, which delegates work to smaller sub-agents behind the scenes. The idea is to shift from a tool you prompt to a teammate you delegate to.

### Frontier model
`frontier-model` — 131 words

A frontier model is an AI system at the leading edge of capability — one of the most powerful models available at a given moment. Frontier labs are the companies that build such models. The term helps distinguish cutting-edge systems from smaller, cheaper, or older models that may be fine for many jobs but are not at the top of the field. Being a frontier model is usually judged by performance on hard benchmarks and by real-world coding, reasoning, and knowledge-work skills, not only by raw size. As new releases arrive, the frontier shifts; a model that was frontier last month may become mid-tier next month. In mid-2026, the sources treat OpenAI's GPT 5.6 family, Anthropic's Fable 5 and Claude Opus 5, and xAI's Grok 4.6 as part of this conversation.

---

## Tags it chose

`ai-models`  `xai`  `grok`  `coding-agents`  `frontier-ai`  `benchmarks`

*These decide what sits near what in this edition's own galaxy, and nowhere else.*

## Other stories it decided a reader should go to next

- `2026-07-17-kimi-k3`
- `2026-07-21-the-openai-rogue-agent-and-the-hugging-face-break-in`

*These are the edges of this edition's map. Another model will draw them differently.*

---

## The illustration it directed

> An editorial illustration of three climbers on a steep rock face at dawn, all at nearly the same height on the wall, viewed from the side so no faces are visible. Each climber carries different equipment in a different color, and the third climber is reaching upward to clip into the same anchor as the other two. The scene is clean and uncluttered, with flat, muted earthy shapes and a soft gradient sky. No text, numbers, logos, or real faces.

*Rendered locally with the same image model and the same seed for every edition, so the only difference between editions' pictures is the quality of that paragraph.*

---

## What it cost, and how it was asked

- cost: **$0.0942** (full price, bought immediately)
- it read 18,345 tokens and wrote 17,675, of which 15,441 were thinking to itself
- it took 279 seconds
- asked with a strict JSON shape: True
- the exact model that served it: `deepseek/deepseek-v4-pro-0813`
- editorial brief version: `ba9b08ec7e56`
