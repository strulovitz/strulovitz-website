# xAI's Grok 4.6 lands near the frontier, built on Cursor's coding data

*Grok 4.6 ties or nears GPT-5.6 and Claude Opus 5 on several benchmarks at roughly half their price, powered largely by Cursor's coding data.*

xAI released Grok 4.6 on August 13, 2026, and across three independent tests it landed in roughly the same tier as the best models from OpenAI and Anthropic — a first for the company, whose earlier Grok releases had fallen well behind.

All three sources agree Grok 4.6 is not a new model built from scratch. It's an "iterative" update to Grok 4.5, sharing the same roughly 1.5-trillion-parameter base model (sometimes called V9), but with a much longer supplemental training run. According to Matthew Berman, xAI's blog post says Grok 4.5 itself was used to help generate the training data for 4.6 — regenerating reasoning trajectories across coding, STEM and knowledge-work domains, a form of models training their successors. Wes Roth adds that this data included curated, model-generated material on reasoning and technical concepts plus "high-quality engineering data," alongside an improved optimizer and training recipe.

## Where the coding data came from

All three sources trace the leap to xAI's connection with Cursor, the AI coding tool. Berman explains that SpaceX acquired Cursor in April 2026, giving xAI access to a large store of real coding data that Cursor lacked the computing power to use — while xAI, having built 200,000 GPUs in 122 days, lacked a model good enough to attract users. Combining the two, he argues, produced the jump from Grok 4.5 to 4.6.

## The benchmarks, and their disagreements

On GDPval, a benchmark that tests models against real projects from working professionals and has humans grade the results, Berman says Grok 4.6 High scored highest, ahead of GPT-5.6 and Claude Opus 5 Max; Roth also cites GDPval as a strength. But the sources diverge on coding-specific tests. Berman reports Grok 4.6 placed third on DeepSWE (65.9%, versus 73% for GPT-5.6 Soul Max and 70% for Opus 5), while Bowen describes the jump on a version he calls 
