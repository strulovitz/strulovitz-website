# Moonshot's Kimi K3 Matches Top US Models, Full Weights Due July 27

**Claude Sonnet 5** (Anthropic) — its own edition of *2026-07-17-kimi-k3*

---

## The one line a reader sees when hovering over this story

> Moonshot AI's 2.8-trillion-parameter Kimi K3 topped a major coding benchmark and rivals frontier US models, with full open weights due July 27, 2026.
> *(149 characters)*

---

## The article

On July 17, 2026, Chinese AI company Moonshot released Kimi K3, an open-weight model with 2.8 trillion parameters — the largest open-weight model announced to date. Moonshot says full weights will be downloadable from July 27, letting companies run and modify the model on their own servers instead of only through Moonshot's app.

What made the release notable wasn't just size. On Arena AI's front-end code arena, where developers ask models to build websites and interfaces and then vote on the results, K3 came in first. Source accounts of the exact numbers differ slightly: one report put K3 at 1,679 points against Claude Fable 5's 1,631 and GPT 5.6 Soul's 1,618, while another cited K3 at 76% success against Fable 5's 63%. Both agree K3 finished ahead of the leading US closed models, and that Moonshot's previous model, Kimi K2.6, had sat in 18th place. On Artificial Analysis's intelligence index, K3 scored 57, close to Claude Opus 4.8 (56) and GPT 5.6 Terra (55), with only Claude Fable 5 and GPT 5.6 Soul clearly ahead.

Moonshot doesn't claim K3 wins everything. The company says it still trails Fable 5 and GPT 5.6 Soul in overall user experience and some broader tasks. Reviewer Wes Roth found results varied sharply depending on how the model was accessed: prompts run through the kimi.com browser interface produced polished game demos, while the same prompts run through Moonshot's coding tool or API were noticeably weaker — suggesting the surrounding software, not just the model, still matters.

## Built for long jobs, not just chat

K3 is designed to work for hours largely unsupervised: inspecting code, planning changes, using tools, checking its own work, and continuing. Moonshot calls this ability to look at a screen and correct itself "vision in the loop." In demonstrations, K3 built a 3D open-world game in a browser, simulated China's Long March 10 rocket, built a Game Boy Advance emulator, and reportedly designed a computer chip in a 48-hour autonomous run using open-source tools — though reviewer Wes Roth noted the resulting chip was modest by commercial standards, more comparable to a strong student project than an industrial design. Moonshot also says K3 reproduced an astrophysics analysis, reviewing over 20 papers and writing more than 3,000 lines of code in about two hours, work the company says would normally take a team one to two weeks.

Technically, K3 uses a mixture-of-experts design with 896 specialized sections, only 16 of which activate for any given query, plus new attention mechanisms Moonshot calls Kimi Delta attention, which the company says make it 2.5 times more efficient to scale than its predecessor, Kimi K2. It was trained using lower-precision number formats (MXFP4 weights, MXFP8 activations) to ease hardware demands — though Moonshot still recommends at least 64 AI accelerators to run it, far beyond home computer capacity.

## Price and politics

K3 costs $3 per million input tokens uncached (30 cents cached) and $15 per million output tokens — roughly half GPT 5.6 Soul's output price and well below Claude Fable 5's roughly $10/$50. One benchmark tracker cited by Matthew Berman found K3's cost advantage partly offset because it uses about twice as many tokens to complete the same task as GPT 5.6 Soul, landing at similar effective cost.

The release rattled markets: shares in Chinese rivals Zhipu (

---

## What this editor judged the sources established

- Moonshot AI released Kimi K3, a 2.8 trillion parameter open-weight model, and said full weights would be released July 27, 2026.
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- K3 finished first on Arena AI's front-end code arena, ahead of Claude Fable 5 and GPT 5.6 Soul, with one source citing scores of 1,679 versus 1,631 and 1,618.
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- A separate account of the same benchmark reported Kimi K3 at 76% success versus Claude Fable 5's 63%.
  — https://www.youtube.com/watch?v=JrVPIy9AdfQ
- Artificial Analysis gave K3 an intelligence index score of 57, close to Claude Opus 4.8 (56) and GPT 5.6 Terra (55).
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- K3 is priced at $3 per million input tokens uncached, 30 cents cached, and $15 per million output tokens, undercutting Claude Fable 5's roughly $10/$50 pricing.
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- K3 uses a mixture-of-experts design with 896 experts and only 16 active at once, plus new Kimi Delta attention mechanisms Moonshot says make it 2.5 times more efficient than Kimi K2.
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- Moonshot demonstrated K3 autonomously designing a computer chip in a 48-hour run using open-source tools, though the chip was modest by commercial standards.
  — https://www.youtube.com/watch?v=4fPLsmJNaMI
- Shares of Chinese AI rivals fell after the release, with Zhipu (referred to as Jiepu) down 21.9% in Hong Kong and MiniMax down 13.8%.
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- Results with K3 varied significantly depending on interface: prompts run through kimi.com produced strong demos, while the same prompts through Moonshot's coding tool or API performed worse.
  — https://www.youtube.com/watch?v=4fPLsmJNaMI
- On a cost-versus-success benchmark, Kimi K3 Max matched GPT 5.6 Soul's effective price only because it used roughly twice as many tokens for the same task.
  — https://www.youtube.com/watch?v=JrVPIy9AdfQ
- Xi Jinping used the World Artificial Intelligence Conference in Shanghai to promote a Chinese-led global AI order, including a new World AI Cooperation Organization signed by 29 countries.
  — https://www.youtube.com/watch?v=V0RsocRqjIU

---

## The encyclopedia entries it chose to write

### Mixture of experts
`mixture-of-experts` — 185 words

Mixture of experts, or MoE, is a way of building a very large AI model without making every part of it work on every request. Instead of one huge network processing each word, the model is split into many smaller specialized sub-networks called experts. For any given piece of input, a routing mechanism selects only a handful of these experts to actually do the work, while the rest stay idle. Kimi K3, for example, contains 896 experts but activates only 16 for any single token it processes. This means a model can have an enormous total parameter count — the numbers that store what it has learned — while the actual computation needed to answer any one question stays much smaller than the full size would suggest. The appeal is efficiency: you get some of the capacity benefits of a huge model without paying the full computational cost every time. The tradeoff is complexity in training and routing, and the fact that headline parameter counts for MoE models can be misleading, since they measure total capacity rather than the effort spent on any single answer.

### Open-weight model
`open-weight-model` — 176 words

An open-weight model is an AI system whose trained parameters — the numerical values that encode everything it learned during training — are published for anyone to download, rather than kept locked inside a company's own servers. This differs from open-source software in the traditional sense, because the training data and exact code used to produce the model are often not released, only the finished weights. Once weights are public, anyone with sufficient computing hardware can run the model independently, modify it, fine-tune it for new purposes, or build products on top of it without paying the original company per use. This creates competitive pressure on companies that only offer closed access through paid APIs, since businesses can choose to self-host instead. It also raises harder questions: once weights are released, they cannot be recalled or shut off remotely, unlike a closed model accessed through a company's servers. This makes open-weight releases significant both commercially, as a competitive threat, and in debates about safety, since misuse-resistant restrictions can be removed by anyone who has the weights.

### Model distillation
`model-distillation` — 178 words

Distillation is a technique in which a smaller or newer AI model is trained partly by learning from the outputs of an existing, more capable model, rather than only from raw human-generated data. In practice this might mean generating large numbers of question-and-answer pairs from an established model and using them as training examples for a new one, letting the new model absorb some of the older model's patterns of reasoning more efficiently than training from scratch. It is a common and often legitimate technique in AI development. It becomes controversial when a company suspects a competitor has distilled from its own model without permission, effectively using the competitor's paid product to cheaply bootstrap a rival model, which some companies say violates their terms of service. Critics of this complaint point out that large AI models are themselves trained on vast amounts of publicly available text, images and code without individual permission from the original authors, making objections to distillation appear inconsistent to some observers. The dispute is likely to keep resurfacing as competition between AI labs intensifies.

### Context window
`context-window` — 167 words

A context window is the amount of text, code, or other input an AI model can consider at one time when generating a response. It is typically measured in tokens, which are small chunks of text roughly corresponding to parts of words; a million tokens is roughly comparable to hundreds of thousands of words. A larger context window lets a model take in more material at once — an entire codebase, a long research paper, or a lengthy project history — without losing track of information mentioned earlier in the conversation. This matters for tasks that unfold over long stretches of work, such as software development on large projects, where earlier decisions and code need to remain accessible much later in the process. A large context window does not by itself guarantee that a model will use that information well; some models handle long contexts more reliably than others, and performance can still degrade on very long or complex inputs even when the window itself is large.

---

## Tags it chose

`kimi-k3`  `moonshot-ai`  `open-weight-models`  `china-ai-race`  `ai-benchmarks`  `mixture-of-experts`

*These decide what sits near what in this edition's own galaxy, and nowhere else.*

## Other stories it decided a reader should go to next

- `2026-08-13-grok-4-6`

*These are the edges of this edition's map. Another model will draw them differently.*

---

## The illustration it directed

> An editorial illustration of a vast, dim hall of countless identical machine looms stretching into the distance, only a small cluster of them lit and working at any moment while the rest sit dark and still, rendered in a restrained, cool palette; in the far background, two rows of server-building silhouettes face each other, one row with wide open doors spilling warm light outward, the other row with doors shut tight, suggesting a contrast between open and closed systems without any text, screens, logos, faces, glowing brains, or circuit-board patterns.

*Rendered locally with the same image model and the same seed for every edition, so the only difference between editions' pictures is the quality of that paragraph.*

---

## What it cost, and how it was asked

- cost: **$0.1090** (full price, bought immediately)
- it read 22,164 tokens and wrote 6,472, of which 2,493 were thinking to itself
- it took 74 seconds
- asked with a strict JSON shape: True
- the exact model that served it: `anthropic/claude-sonnet-5`
- editorial brief version: `ba9b08ec7e56`
