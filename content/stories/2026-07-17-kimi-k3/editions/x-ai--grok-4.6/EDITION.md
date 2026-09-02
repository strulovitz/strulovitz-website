# Moonshot AI releases 2.8-trillion-parameter Kimi K3

**Grok 4.6** (xAI) — its own edition of *2026-07-17-kimi-k3*

---

## The one line a reader sees when hovering over this story

> Moonshot AI’s Kimi K3, a 2.8-trillion-parameter open-weight model, matches or beats leading US systems on several coding tests.
> *(127 characters)*

---

## The article

Moonshot AI, a Chinese lab backed by Alibaba and Tencent, has unveiled Kimi K3, a 2.8-trillion-parameter model it calls the largest open-weight system yet announced and the first open model to approach the three-trillion mark. Full weights are expected on 27 July 2026, after which companies and researchers can download, modify, and run it on their own machines. The launch landed on the same day China’s leadership, speaking in Shanghai at the World Artificial Intelligence Conference, argued that China should help write global AI rules, spread lower-cost open models, and refuse an American monopoly on standards, chips, and access.

## Size and how it is built
K3 is a mixture-of-experts design: 896 specialised sections, with only 16 switched on for any given step. That is how Moonshot can claim 2.8 trillion parameters without running the whole network for every word. It can take in up to a million tokens in one session—about 750,000 words—and it handles text, images, and video in the same model. Moonshot says new attention methods, plus lower-precision training formats, make it about 2.5 times more efficient at scaling than Kimi K2. This is not a laptop model. The company recommends at least 64 AI accelerators; commentators joked about needing around two terabytes of video memory.

The product is aimed at long jobs, especially software. Moonshot describes a loop in which the model writes code, looks at the screen, notices what is wrong, and tries again—useful for websites, games, and design. Company demonstrations include a 3D browser game, a rocket simulation, a Game Boy emulator, a small GPU compiler, more than 15 hours spent speeding up GPU code, an astrophysics analysis in about two hours, and a 48-hour chip-design run with open-source tools. Those remain company demos. One reviewer who tried similar games found a large gap: on Moonshot’s website, where the model can screenshot its own work and keep iterating, results looked polished; through the API and a coding terminal, they often did not. Moonshot itself warns that if an agent fails to return its full reasoning history, performance drops, and that vague instructions can leave K3 deciding on its own.

## Scores, price, and what they do not prove
On Artificial Analysis’s intelligence index, K3 scored 57. Claude Opus 4.8 was around 56, GPT-5.6 Terra 55, and Gemini 3.1 Pro about level with K3. Only Claude Fable 5 and GPT-5.6 Soul stayed ahead, by two or three points. Moonshot says K3 can compete with Fable 5 on hard coding and still trails those two leaders on overall user experience.

The result that travelled farthest was Arena.ai’s front-end code arena, where people vote on websites and interfaces. One account put K3 first at 1,679 points, ahead of Fable 5 (1,631) and GPT-5.6 Soul (1,618), winning six of seven categories after Kimi K2.6 had sat eighteenth. Another account of the same kind of contest gave K3 76 percent against Fable 5’s 63 percent. Vercel’s founder said K3 led a Next.js engineering benchmark—the first time an open model had done so there. Testers also put it first on an internal writing ranking, a jump from 21st with the previous generation.

API prices are $3 per million uncached input tokens, 30 cents when cached, and $15 per million output tokens including reasoning, even at long context. Fable 5 is quoted around $10 in and $50 out; GPT-5.6 Soul around 50 cents in and $30 out. On a cost-per-task chart used by one reviewer, K3 Max sat near GPT-5.6 Soul at about $4.70 because it burned more tokens: cheaper per token, hungrier, and slower.

## Markets and the argument around it
Chinese rivals felt it first. JIEPU shares fell 21.9 percent in Hong Kong; MiniMax dropped 13.8 percent. MiniMax is said to be preparing a 2.7-trillion-parameter model as early as the third quarter of 2026. Bloomberg reported Moonshot seeking about $2 billion at a valuation around $30 billion.

Anthropic has accused Moonshot and other Chinese labs of distilling capabilities from Claude. US commentators argued that patchwork regulation and delayed American releases let China ship faster. Xi Jinping called open-source AI a historic chance, promoted a World AI Cooperation Organization that signed 29 countries, and spoke of keeping AI under human control. The conference runs 17–20 July 2026, just before government-level US–China AI talks. One American official called a Chinese model taking first on the front-end arena “concerning.” A Kimi engineer said the point was not winning a race but keeping a frontier-level open model available to everyone.

K3 does not have to win every category. If firms can run a near-frontier coding model themselves, keep data private, and pay less, closed US providers have a commercial problem. Once the weights are public, they cannot be recalled.

---

## What this editor judged the sources established

- Moonshot AI unveiled Kimi K3 as a 2.8-trillion-parameter model, described as the largest open-weight AI system yet announced, with full weights expected on 27 July 2026.
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- K3 uses a mixture-of-experts design with 896 experts and 16 active at a time, a million-token context window, and Moonshot recommends at least 64 AI accelerators to run it.
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- Artificial Analysis scored K3 at 57 on its intelligence index, with Claude Opus 4.8 around 56, GPT-5.6 Terra at 55, and only Claude Fable 5 and GPT-5.6 Soul a few points ahead.
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- On Arena.ai’s front-end code arena, K3 entered at number one with 1,679 points, ahead of Claude Fable 5 (1,631) and GPT-5.6 Soul (1,618), after Kimi K2.6 had been 18th.
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- API pricing is $3 per million uncached input tokens, $0.30 cached, and $15 per million output tokens including reasoning, compared with much higher output prices quoted for Fable 5 and GPT-5.6 Soul.
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- JIEPU shares fell 21.9% in Hong Kong and MiniMax dropped 13.8% after the release; Moonshot is backed by Alibaba and Tencent and, according to Bloomberg, is trying to raise about $2 billion at around a $30 billion valuation.
  — https://www.youtube.com/watch?v=V0RsocRqjIU
- Hands-on tests found a large gap between polished results in Moonshot’s browser app, where the model screenshots its own work and iterates, and weaker results via the API and coding terminal.
  — https://www.youtube.com/watch?v=4fPLsmJNaMI
- On a cost-per-task chart, K3 Max sat near GPT-5.6 Soul at about $4.70 because it used far more tokens, making sticker prices look cheaper than effective cost; the model was also described as slow.
  — https://www.youtube.com/watch?v=JrVPIy9AdfQ
- Vercel’s founder said K3 was the best-performing model on a Next.js web-engineering benchmark, the first time an open model led all proprietary ones there.
  — https://www.youtube.com/watch?v=JrVPIy9AdfQ
- Xi Jinping, speaking at the World Artificial Intelligence Conference in Shanghai (17–20 July 2026), promoted open-source AI and a World AI Cooperation Organization that signed 29 countries the day before.
  — https://www.youtube.com/watch?v=V0RsocRqjIU

---

## The encyclopedia entries it chose to write

### Mixture of experts
`mixture-of-experts` — 142 words

A mixture-of-experts model is a large neural network divided into many specialised sub-networks, called experts, plus a router that decides which few of them should handle each piece of input. Instead of waking the entire model for every word, only a small team of experts is switched on. That lets builders advertise a huge total parameter count—the sum of all experts—while the cost of generating each token stays closer to a much smaller dense model. The trade-off is engineering complexity: the router must choose well, unused experts can waste capacity, and serving the system still requires enough memory to hold the full set of weights even if most sit idle. The idea is older than today’s chat models, but it became the usual way to grow language models past the point where a fully dense network would be too expensive to run.

### Open weights
`open-weights` — 151 words

Open weights means a lab publishes the trained numerical parameters of a model so that other people can download them, run the model on their own computers, inspect it, and often fine-tune it. That is different from an API-only product, where you send prompts to a company’s servers and never see the model itself. It is also narrower than full open source, which would include training data, code, and a licence that lets you rebuild the system from scratch. Open weights matter because they change who is in control: a company cannot quietly switch the model off for you, change its behaviour overnight, or keep your data on its premises if you host it yourself. They also freeze a snapshot in public, so later restrictions cannot fully take it back. The practical catch is hardware. Frontier-sized open-weight models may be free to download and still require a data centre to run.

### Model distillation
`model-distillation` — 143 words

Distillation is a training method in which a smaller or newer model learns from the outputs of a larger or already-trained one, often called the teacher. The student is shown many prompts and the teacher’s answers—or its internal scores—and is trained to imitate them. Labs use this to compress a big model, to transfer a skill, or to cheaply bootstrap a new system. The technique is ordinary in machine learning. Conflict arises when the teacher is a rival’s commercial model and the student is trained by querying that model at scale, which many providers forbid in their terms of use. Critics call that copying; defenders note that almost every large model has already learned from public text produced by other people and other machines. The argument is now as much about contracts, export policy, and national competition as it is about the algorithm.

---

## Tags it chose

`kimi-k3`  `moonshot-ai`  `open-weights`  `china`  `coding-models`  `ai-policy`

*These decide what sits near what in this edition's own galaxy, and nowhere else.*

## Other stories it decided a reader should go to next

- `2026-08-13-grok-4-6`

*These are the edges of this edition's map. Another model will draw them differently.*

---

## The illustration it directed

> A panoramic digital painting shows a colossal moonlit Chinese dragon whose body is a 2.8-trillion-parameter mixture-of-experts lattice of 896 specialized modules with only 16 glowing at any moment, ingesting a million-token multimodal torrent of text, images and video while autonomously looping through screens that display a 3D browser game, GPU compiler, rocket simulation and 48-hour chip design; holographic leaderboards place Kimi K3 first on Arena.ai front-end coding and level with Claude and GPT, cheap-token price tags hover beside a 64-accelerator GPU farm, open-weight files cascade unrecallably toward global users, Shanghai’s World AI Conference podium and open-source banners stand left, locked US closed-model silhouettes look on right, and rival Chinese stock tickers plunge beneath the rising moon labeled Moonshot AI.

*Rendered locally with the same image model and the same seed for every edition, so the only difference between editions' pictures is the quality of that paragraph.*

---

## What it cost, and how it was asked

- cost: **$0.0866** (full price, bought immediately)
- it read 15,610 tokens and wrote 7,542, of which 4,796 were thinking to itself
- it took 544 seconds
- asked with a strict JSON shape: True
- the exact model that served it: `x-ai/grok-4.6`
- editorial brief version: `ba9b08ec7e56`
