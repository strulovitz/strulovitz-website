# Grok 4.6 puts xAI within reach of the top models

**Qwen 3.8 Max** (Alibaba) — its own edition of *2026-08-13-grok-4-6*

---

## The one line a reader sees when hovering over this story

> xAI's Grok 4.6, trained longer on Cursor data, benchmarks against Anthropic's and OpenAI's best at half their output price.
> *(123 characters)*

---

## The article

On 13 August 2026, xAI released Grok 4.6, the latest in its Grok line of large language models. The significance is not just that it is good. It is that, after years in which OpenAI and Anthropic were the only two labs considered truly competitive at the frontier, a third company has now produced a model that several independent reviewers say sits in the same conversation, at a noticeably lower price.

## What Grok 4.6 is

Grok 4.6 is not a ground-up rebuild. According to the material reviewed by reviewers, it is built on the same foundation as Grok 4.5: a base model of roughly 1.5 trillion parameters, referred to internally as the V9 base. The main difference is that 4.6 went through a much longer supplemental training run than 4.5, using curated data, model-generated reasoning examples, high-quality engineering material, and an improved training recipe.

Much of that data appears to come from Cursor, the AI coding tool company that xAI acquired earlier in the year. Reviewers Matthew Berman and Wes Roth both argue this acquisition is the key to understanding Grok's sudden improvement: Cursor brought a large body of real coding interaction data, and xAI had a large amount of GPU capacity. Together, they gave xAI what it had been missing.

## How it performs

Benchmark results vary by test, but the overall picture is consistent: Grok 4.6 is in the top tier, though not always at the very top.

Matthew Berman reported that on GDPval, a benchmark measuring performance on real knowledge-work tasks, Grok 4.6 High scored highest among the models compared, ahead of both GPT 5.6 Soul and Fable 5 Max. On Harvey Lab's legal reasoning benchmark, it also led at 15.8%. On the DeepSWE coding benchmark, however, it came third at 65.9%, behind Fable 5 Max at 70% and GPT 5.6 Soul Max at 73%.

Wes Roth described it as "neck to neck" with the best models from OpenAI and Anthropic at release, and said his hands-on tests, including generating a playable replica of a Portal-style game level, matched that impression. Bijan Bowen ran a series of creative and technical generation tasks, including a 3D-printable engine model and a detailed frontend website, and concluded it was a genuinely competitive frontier model, though he stopped short of calling it the best.

All three reviewers caution that benchmarks alone are an incomplete picture. Berman specifically noted that cost per task matters as much as raw quality, and that Grok 4.6 is more expensive per task than Grok 4.5 was, though still cheaper than the most capable competitors.

## Pricing and availability

Grok 4.6 costs $2 per million input tokens and $6 per million output tokens. A fast variant runs at twice that price but with faster responses. Berman noted this makes it roughly half the output-token cost of comparable OpenAI and Anthropic frontier models.

It is available through the xAI API, Cursor, Grok Build, and several third-party platforms. During launch week, Cursor and Grok Build users receive double their normal usage allowance.

## Grok Bot

Alongside the model, xAI released Grok Bot, a desktop agent application for macOS, Windows, and Linux, with Android versions planned. Unlike a standard chatbot, Grok Bot is designed as a persistent agent that runs in a cloud virtual machine around the clock. Users can set up a lead agent, which then creates and delegates tasks to sub-agents.

Roth tested it by having it build an automated Pokémon-playing livestream setup and an agent that monitors X for news. Berman noted that Grok Bot hides all code and model selection from the user, presenting results as documents and presentations instead, making it aimed at a broader, less technical audience than typical coding tools.

## What comes next

Elon Musk said on X that Grok 4.7, expected within three to four weeks, is significantly better than 4.6 and will include SpaceX company data in its training. All three reviewers referenced this claim, though none treated it as confirmed. Berman also noted that xAI has reorganised its engineering team to ship major updates every two to three weeks, with Grok 5 targeted before the end of the year.

Whether that pace is sustainable, and whether Grok 4.6's benchmark numbers hold up in wider use, remain open questions. But the consensus among these three independent reviewers, all publishing on the same day, was clear: xAI is now a serious third competitor in a race that had, until this week, looked like a two-horse one.

---

## What this editor judged the sources established

- Grok 4.6 is built on the same 1.5 trillion parameter V9 base as Grok 4.5, with the key improvement being a longer supplemental training run using curated Cursor and engineering data.
  — https://www.youtube.com/watch?v=VB39bHByHuU
- On the GDPval knowledge-work benchmark, Grok 4.6 High scored highest among compared models, ahead of GPT 5.6 Soul and Fable 5 Max, while on DeepSWE coding it placed third behind both.
  — https://www.youtube.com/watch?v=rdYBjpylJUQ
- Grok 4.6 costs $2 per million input tokens and $6 per million output tokens, making it roughly half the output price of comparable OpenAI and Anthropic frontier models.
  — https://www.youtube.com/watch?v=rdYBjpylJUQ
- Grok Bot, released alongside Grok 4.6, is a persistent desktop agent that runs in a cloud virtual machine and delegates tasks to sub-agents without exposing code or model selection to the user.
  — https://www.youtube.com/watch?v=rdYBjpylJUQ
- Elon Musk said Grok 4.7 is expected in three to four weeks and will include SpaceX company data in supplemental training, though reviewers noted this is not yet officially confirmed.
  — https://www.youtube.com/watch?v=rdYBjpylJUQ
- Bijan Bowen tested Grok 4.6 on creative generation tasks including a 3D-printable engine model and a frontend website, and concluded it was a genuinely competitive frontier model though not the best.
  — https://www.youtube.com/watch?v=PtdI0KZRTLU

---

## The encyclopedia entries it chose to write

### Benchmark
`benchmark` — 96 words

A benchmark is a standardised test used to compare the abilities of AI models. Think of it as an exam that every model sits under the same conditions. Benchmarks can measure coding ability, reasoning, knowledge work, or specific tasks like legal analysis. They are useful for quick comparisons but have well-known limits: models can be trained specifically to perform well on particular tests without being generally better, and a high benchmark score does not always translate into better real-world performance. This is why reviewers often combine benchmark results with their own hands-on testing before drawing conclusions.

### Supplemental training run
`supplemental-training-run` — 96 words

After a large language model is first trained on a broad body of text, it can be trained further on more specific or carefully selected data to improve particular abilities. This additional phase is called supplemental training. It does not rebuild the model from scratch; instead it refines what is already there, much like a specialist course taken after a general degree. In the case of Grok 4.6, the supplemental run was longer than for its predecessor and used data from Cursor's coding tool, which is credited with much of the model's improvement in technical tasks.

### Persistent AI agent
`persistent-ai-agent` — 96 words

Most AI tools respond only when you actively use them, and stop when you close the window. A persistent agent is designed to keep running in the background, continuing tasks over hours or days without needing the user's computer to stay on. It typically runs on a remote server rather than the user's own machine. This allows it to monitor events, complete long-running projects, or hand work back to the user when they return. Grok Bot is an example: each agent it creates operates in its own cloud environment and can continue working around the clock.

### Recursive model training
`recursive-model-training` — 97 words

Recursive model training refers to using one generation of an AI model to help produce the training data for the next generation. Rather than relying entirely on human-written examples, the older model generates responses, corrections, or reasoning traces that are then used to teach the newer model. This does not mean the AI is improving itself autonomously in the science-fiction sense; humans still design the process and curate the data. But it does mean that as models get better, they can contribute to making the next version better, potentially accelerating the pace of improvement across successive releases.

---

## Tags it chose

`large-language-models`  `xai`  `coding-assistants`  `ai-agents`  `benchmarking`

*These decide what sits near what in this edition's own galaxy, and nowhere else.*

## Other stories it decided a reader should go to next

- `2026-07-17-kimi-k3`

*These are the edges of this edition's map. Another model will draw them differently.*

---

## The illustration it directed

> A single wide illustration should show a frontier AI race that has changed from two leaders to three, with xAI Grok 4.6 as a sleek robotic runner or vehicle surging into the same lane as OpenAI and Anthropic. Grok 4.6 should be visibly powered by a stream of Cursor coding interfaces, engineering documents, and model-generated reasoning examples flowing from a Cursor vault into a large GPU training furnace, showing that longer supplemental training on acquired Cursor data drove the improvement. Around the scene, transparent benchmark gauges for knowledge work, legal reasoning, and coding should show Grok leading in some tests and close behind the best models in others, while a prominent price comparison shows Grok at $2 per million input tokens and $6 per million output tokens, roughly half the output price of the rival frontier models. In the foreground, a Grok Bot desktop window should spawn persistent cloud sub-agents that produce documents, websites, a playable game level, and monitoring feeds, making the picture communicate that xAI is now a serious third frontier competitor offering top-tier performance, lower cost, and agent-based products, even though the race is not yet won.

*Rendered locally with the same image model and the same seed for every edition, so the only difference between editions' pictures is the quality of that paragraph.*

---

## What it cost, and how it was asked

- cost: **$0.2029** (full price, bought immediately)
- it read 18,445 tokens and wrote 25,772, of which 23,454 were thinking to itself
- it took 512 seconds
- asked with a strict JSON shape: True
- the exact model that served it: `qwen/qwen3.8-max`
- editorial brief version: `ba9b08ec7e56`
