# Grok 4.6 puts xAI within reach of the top models

*xAI's Grok 4.6, trained longer on Cursor data, benchmarks against Anthropic's and OpenAI's best at half their output price.*

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
