# Moonshot's Kimi K3 brings frontier-level coding to open-weight AI

*China's Moonshot AI released Kimi K3, a 2.8-trillion-parameter open-weight model that tops several coding benchmarks and undercuts US rivals on price.*

For years, the comfortable assumption in the West was that open-weight AI models — the kind anyone can download, modify, and run — trailed the best closed commercial systems by six months or more. Moonshot AI's Kimi K3 has made that assumption hard to keep.

The Chinese lab announced K3 as a 2.8-trillion-parameter model, the largest open-weight system ever announced, with its full weights expected to be released on July 27. On the LMArena front-end code leaderboard, which ranks models by how well developers rate the websites and interfaces they build, K3 entered at number one with 1,679 points, ahead of Anthropic's Claude Fable 5 at 1,631 and OpenAI's GPT 5.6 Soul at 1,618. Moonshot's previous model had sat in 18th place. One jump put K3 at the top, and LMArena's CEO called it potentially the biggest AI release of the year.

## What K3 can and cannot beat

K3 is not the overall champion. On Artificial Analysis's intelligence index it scored 57, roughly level with Google's Gemini 3.1 Pro and just above Claude Opus 4.8's 56, but two or three points behind Claude Fable 5 and GPT 5.6 Soul. Moonshot itself admits K3 trails those two models in overall user experience and broader tasks. In one independent writing benchmark, however, K3 reportedly jumped from 21st to first, displacing Fable 5.

Its particular strength is building software, especially front-end work where appearance matters. The model uses what Moonshot calls "vision in the loop": it writes code, takes a screenshot of the result, notices what looks wrong, edits, and checks again, repeating that cycle for hours. Several reviewers found this loop convincing in practice, watching K3 iterate through dozens of screenshots while building browser games. Matthew Berman also noted the model is slow and token-hungry, with one demonstration taking roughly 30 minutes to complete.

Moonshot's own demos are more eye-catching but unverified: K3 reportedly designed a modest chip in 48 hours using open-source tools, spent 15 hours improving GPU code and cut compute time by more than half, and reproduced an astrophysics analysis in about two hours that the company says would normally take an experienced team one to two weeks. The chip is explicitly an early proof of concept, not commercial silicon.

## Open, but not small

K3 uses a mixture-of-experts design: 896 specialised sections, of which only 16 activate for any given task. That lets a 2.8-trillion-parameter system run without using all of itself for every word. It handles up to one million tokens per session — roughly 750,000 words — and processes text, images, and video in the same model. Moonshot trained it with low-precision formats and says new attention methods make it about 2.5 times more efficient at scaling than its predecessor.

Nobody is running this at home. Moonshot recommends at least 64 AI accelerators. The point is that large companies can host it, keep their data private, and adapt it. At $3 per million uncached input tokens and $15 per million output tokens, it undercuts Fable 5's roughly $10 and $50, though GPT 5.6 Soul's input price is lower.

## A release with political weather

K3 arrived the same day China's leader used the World Artificial Intelligence Conference in Shanghai to argue that China should help write global AI rules rather than follow America's. A new World AI Cooperation Organization signed up 29 countries, and the timing gives that pitch a concrete artefact. The release also unsettled markets: shares in Chinese AI companies Zhipu and MiniMax fell sharply, and Bloomberg reported Moonshot is trying to raise $2 billion at a valuation of around $30 billion ahead of a possible Hong Kong listing.

Not everyone reads K3 as a true frontier arrival. Berman argues US labs likely have newer models in internal testing and remain eight to ten months ahead in practice. Others see the gap as days. Anthropic has also accused Moonshot, DeepSeek, and MiniMax of using distillation — training one model on the outputs of another — to copy Claude's capabilities, a dispute likely to intensify once the weights are public. K3's answer to that argument is to make itself downloadable, and impossible to switch off.
