# Grok 4.6 puts xAI within reach of OpenAI and Anthropic at half the price

*xAI's Grok 4.6 matches or trails the best OpenAI and Anthropic models depending on the benchmark, at roughly half the price.*

For roughly two years the front of the AI race has had two runners, OpenAI and Anthropic. On 13 August 2026, three reviewers published same-day verdicts on a model they say changes that: Grok 4.6, released by Elon Musk's lab xAI within about a day of their videos. All three call it an incremental upgrade rather than a fresh design, and all three call the jump unusually large. Matthew Berman put it bluntly: "We now have a third major US AI lab."

## How it was built, and why Cursor mattered

By every account, Grok 4.6 was not trained from scratch. Wes Roth says he and others who follow xAI believe 4.5 and 4.6 share one base — a 1.5-trillion-parameter model (parameters are the adjustable settings that training settles on; the count is a rough proxy for capacity). What changed is the finish: a much longer "supplemental training run", extra coaching layered onto that base with better data, much of it from Cursor, the AI coding-tool company bought by Musk's side in April. The transcripts disagree on the buyer — Roth says xAI, Berman says SpaceX — but agree on what the deal delivered. Berman frames it as a merger of gaps: Cursor had a mountain of coding data and no data centre; xAI had built a cluster of 200,000 GPUs in 122 days and a model few people wanted. xAI also says it used Grok 4.5 itself to "regenerate the SFT trajectories" for 4.6 — the previous model helped write the worked examples the next one studied, a practice Berman calls "recursive self-improvement" and notes is now common across labs.

## What the benchmarks say

A benchmark is a fixed test a model sits, like an exam: same questions, published scores, a leaderboard. Here the picture is mixed. On GPT Val — OpenAI's benchmark of real tasks from real jobs, in fields from engineering to finance to travel, graded by humans — Grok 4.6 High placed first, ahead of OpenAI's GPT 5.6 Soul and Anthropic's Fable 5 Max. On Cursor's internal benchmark it essentially tied Fable 5 Max. On DeepSWE, a software-engineering benchmark Berman rates as a close guide to how a coding model actually feels to use, it came third at 65.9, behind GPT 5.6 Soul Max (73) and Fable 5 (70). Between Grok versions it rose from 15% to 26% on Terminal Bench, and it dominated a legal-work benchmark, 15.8% against 2.5% and 11.3% for the Soul and Fable models. On Artificial Analysis's combined intelligence index it sits behind Claude Opus 5 and Fable 5, tied with GPT 5.6 Soul.

On that evidence the reviewers part ways. Roth calls the model "neck to neck" with the best of OpenAI and Anthropic — a first for Grok on release day — and says that despite his usual wariness about gamed benchmarks, his hours with it matched the charts. Bowen is cooler: not Fable 5 or GPT 5.6 level at coding, "but it's closer", and if the 4.5-to-4.6 leap repeats, the next model could pass them.

## Half the price, but dearer per job

Models are bought by the token — a small chunk of text — quoted per million. Grok 4.6 costs $2 per million tokens in, $6 per million out, with a faster variant at double. For comparison, Bowen cites Anthropic's Sonnet 5 at $2 in and $10 out, and OpenAI's GPT 5.6 at $2 and $12. Berman adds a subtler yardstick, cost per finished task, which folds in how much a model reasons on the way: Grok 4.5 High ran about 36 cents a task; 4.6 runs about 83, on an index score that rose from roughly 55 to 60. Smarter, but no longer cheap in quite the same way — and the value corner of his chart belonged to OpenAI's GPT 5.6 Luna Max, at roughly five cents a task. Cursor and Grok Build users get double usage for launch week, and the model is also on the API, OpenRouter, Vercel and Cloudflare.

## In practice

Roth's opening test was a working clone of a Portal 2 test chamber. Two to three hours later he had portals you can see through and walk through, conserved momentum and a solvable puzzle — in his words, "a beast". Bowen ran a battery: a fake desktop operating system in 26 minutes; a C++ skate game that fixed its floating heads and sideways cars when told; an engine model whose 3D-printed parts actually fitted together; and a marketing site for a two-decade-old iPod Mini with faithful, 3D-spinning colours. His favourite was a wedding site whose "holographic" couple could be spoken to and moved along a timeline. The failures were real too — the skateboard never moved independently of its rider — and in Berman's single-card design test, GPT 5.6 Soul won comfortably, Fable 5 flopped and Grok was respectable but sloppy at the edges. The shared conclusion: unusually strong on visual front-end work, close behind at code.

## Grok Bot

The day before the model, xAI shipped the product meant to carry it beyond programmers. Grok Bot is a set of always-on agents, each with its own virtual machine in the cloud, so work continues when your laptop closes. There are desktop apps for macOS, Windows and Linux, with Android promised, plus a "teach a task" button that records your screen so an agent learns a skill by demonstration. No code appears; even the model's name is hidden. One disagreement sits inside: Berman says Grok 4.6 powers Grok Bot, while Roth ran checks and did not believe 4.6 was live in it yet when he recorded.

## What's next

Musk posted that Grok 4.7 is "significantly better than 4.6", that its initial training is complete, that "a massive amount of SpaceX company data" is being added in supplemental training, and that it should be ready in three to four weeks. Roth relays, and clearly flags as unverified, a rumour of a 2.1-trillion-parameter model, and reports Grok 5 is targeted before the end of the year, with xAI reorganised to ship a major update every two to three weeks. Whether this leap repeats is the open question; that a credible third competitor arrived at roughly half the price is already a fact.
