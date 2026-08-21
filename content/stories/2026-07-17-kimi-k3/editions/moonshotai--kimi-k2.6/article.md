# China's Moonshot AI releases 2.8-trillion-parameter open model Kimi K3

*Moonshot AI's Kimi K3, a 2.8-trillion-parameter open-weight model, reached the top tier of AI coding benchmarks, challenging US leaders.*

## A huge model enters the open race

On July 17, 2026, Chinese lab Moonshot AI unveiled Kimi K3, a 2.8-trillion-parameter artificial-intelligence model that it says is the largest ever announced with fully open weights. Moonshot plans to release those weights on July 27, allowing organizations to download, modify, and run the model on their own hardware. Until then, it is available through Moonshot’s website and online service.

The model is built as a mixture-of-experts system. Imagine a hospital with hundreds of specialists, but only the ones relevant to your symptom are called into the room. K3 contains 896 specialized sub-networks, yet only 16 are active for any single task. This lets Moonshot build enormous scale without burning through the full model every time it writes a sentence. K3 can also hold up to one million tokens in one session—roughly 750,000 words—so it can ingest entire codebases or long document collections without losing track of the beginning.

## Near the top, but not everywhere

Independent tests place K3 close to the best American closed models, though sources differ on exactly how close.

In the Arena.ai front-end code benchmark, where developers vote on which model produces better websites and interfaces, K3 entered at number one with 1,679 points, ahead of Anthropic’s Claude Fable 5 (1,631) and OpenAI’s GPT-5.6 Soul (1,618). Another independent group, Artificial Analysis, gave K3 a score of 57 on its intelligence index, roughly level with Google’s Gemini 3.1 Pro and slightly ahead of some versions of GPT-5.6 and Claude Opus 4.8, while still trailing Claude Fable 5 and GPT-5.6 Soul by a narrow margin.

Moonshot itself admits K3 trails those leading closed models in overall user experience and broader general tasks. One independent tester also found a large gap in quality between using K3 through Moonshot’s browser interface and using it through the developer toolkit, indicating that the surrounding software—the harness that lets the model see, check, and revise its work—strongly shapes the results.

## Long tasks and visual iteration

Moonshot designed K3 for work that spans hours or days. The company showed it spending 15 hours improving graphics-chip code and cutting compute time by more than half; reproducing an astrophysics analysis in about two hours that it says would normally take a human team one to two weeks; and designing a modest proof-of-concept chip in 48 hours using only open-source tools. Experts who reviewed the chip design likened it to a strong student capstone rather than a commercial product, but emphasized that the model worked unsupervised for two full days.

A feature Moonshot calls “vision in the loop” lets K3 look at what it has built—such as a game screen or website—and revise its own work based on what it sees. Testers found this visual feedback loop made the model unusually capable at the design of websites and interactive graphics.

## The price tag and the hardware wall

Using K3 through Moonshot’s online service costs $3 per million uncached input tokens, $0.30 per million cached input tokens, and $15 per million output tokens including reasoning. That is sharply lower than Anthropic’s published Fable 5 pricing of roughly $10 per million input tokens and $50 per million output tokens. Yet one efficiency analysis found that K3 uses about twice as many tokens as GPT-5.6 Soul to complete the same task, which narrows the real-world cost gap to roughly equal on some benchmarks.

Running the model privately is another matter. Moonshot recommends at least 64 AI accelerators—specialized chips far beyond a desktop computer—meaning most users will rely on cloud providers rather than host it themselves.

## Geopolitics and training disputes

The launch landed on the same day that Xi Jinping addressed the World Artificial Intelligence Conference in Shanghai, arguing that China should help write global AI rules rather than follow American ones. He promoted a new World AI Cooperation Organization of 29 countries, offering lower-cost open technology to developing nations through partnerships with BRICS, ASEAN, Latin America, and the African Union. K3 gives China a frontier-class open model to anchor that pitch.

The release also revived accusations from Anthropic that Moonshot used “model distillation”—training K3 in part by studying outputs from Anthropic’s Claude models—in violation of Anthropic’s rules. The claim is contested; critics counter that Western labs themselves trained on vast public internet data.

## Market shock

The announcement hurt rivals almost immediately. Shares in rival Chinese AI firms fell sharply in Hong Kong after the release, with one report noting drops of 21.9 percent and 13.8 percent. Those falls signaled investor recognition that a large, capable, and relatively cheap open alternative had arrived.
