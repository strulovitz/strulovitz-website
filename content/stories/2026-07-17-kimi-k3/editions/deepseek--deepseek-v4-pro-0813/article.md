# China's Kimi K3 tops a major coding benchmark as open weights near

*Moonshot AI's open-weights Kimi K3, with 2.8 trillion parameters, topped a front-end coding benchmark and intensified the US-China AI race.*

On 17 July, the Chinese company Moonshot AI announced Kimi K3, a large model that the company says contains 2.8 trillion parameters. That makes it the largest open-weights model announced so far, and Moonshot says the full weights are expected to be released on 27 July. In plain terms, a model's weights are its learned settings. Releasing them lets other companies and researchers download, inspect, modify, and run the model themselves, instead of only using it through a company's app.

The size is not what made the release land hard. What landed hard was evidence that an open model from China had caught up with, or in one benchmark passed, some of the best closed American systems.

## One striking benchmark

On Arena AI's front-end code arena, where developers ask models to build real websites and interfaces and then vote on the results, Kimi K3 entered in first place with 1,679 points. Anthropic's Fable 5 scored 1,631 and GPT-5.6 Soul scored 1,618, according to the AI Revolution video. K3 finished first in six of the seven areas tested. The jump was abrupt: Moonshot's previous model, Kimi K2.6, had been sitting in 18th place.

Artificial Analysis placed K3 at 57 on its intelligence index, just above Claude Opus 4.8 at about 56 and around Gemini 3.1 Pro. Only two models remained clearly ahead, by two or three points. This is not a clean sweep. Moonshot itself says K3 still trails the top American models in overall user experience and some broader tasks.

## Built for long, visual work

K3 is designed for long-running coding and knowledge work. It can take up to one million tokens in a session, roughly 750,000 words, so it can work with large codebases, long documents, and research papers without immediately losing track of what came earlier. It uses a mixture-of-experts design: the model contains 896 specialized sections, but only 16 activate at a time. That lets it be very large without running every part for every word it generates.

It also has a visual loop. The model writes code, screenshots the result, notices what is wrong, changes the code, and checks again. One reviewer's browser test produced a playable Matrix-style subway shooter, a miniature ring-world driving game, and a SimCity-like simulation, because the model kept looking at its own work and iterating.

Moonshot also showed grander claims: a Game Boy Advance emulator, a rocket simulation, a chip designed over 48 hours with open-source tools, and an astrophysics analysis written in more than 3,000 lines of Python. These are company demonstrations and need independent checking. One reviewer cautioned that the chip was a student-level proof of concept, not a rival to commercial chips.

## Price and caveats

Published prices are aggressive but not simple. K3 costs $3 per million input tokens when the input is uncached, 30 cents when cached, and $15 per million output tokens. That is far below Fable 5's $10 per million input and $50 per million output in the same video. But another analyst noted that K3 can be token-hungry and slow. When measured by cost per completed task rather than per token, it was about as expensive as GPT-5.6 Soul, because it may use more tokens to finish the same work.

The model is open, but not small. Moonshot recommends at least 64 AI accelerators, and reviewers joked about needing terabytes of VRAM. Early tests through the API and command-line tool felt weaker than the browser app, suggesting that quality depends heavily on the software harness around the model. Moonshot also warns that vague instructions can make K3 act on its own, so strict control requires clear rules.

## The politics around it

The release landed inside a political argument. On the same day, Chinese leader Xi Jinping told the World AI Conference in Shanghai that China would help write AI rules, spread its models to developing countries, and build a new AI order. He promoted a new World AI Cooperation Organization, which he said had signed up 29 countries the day before.

Meanwhile, Anthropic has accused Moonshot, DeepSeek, and MiniMax of using distillation, a technique in which one model helps train another, to copy capabilities from Claude. Critics answered that American labs trained on huge parts of the public internet and then complained when others learned from their models.

Markets noticed too. JIEPU shares fell 21.9 percent in Hong Kong and MiniMax dropped 13.8 percent. Investors read the release as pressure on both Chinese rivals and Western providers.

Kimi K3 does not win everything, and the top American labs may have newer models already in testing. But it changes the conversation. A Chinese lab now has a model that is open, near the frontier, and on one practical benchmark at the top. That is enough to make companies ask why they keep paying closed premium prices, and enough to make governments treat AI as a contest over who gets to set the rules.
