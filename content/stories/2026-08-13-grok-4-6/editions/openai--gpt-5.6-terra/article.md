# Grok 4.6 targets coding and workplace tasks at lower token prices

*xAI's Grok 4.6 arrives with stronger coding results, lower listed token prices and mixed early hands-on tests.*

xAI has released Grok 4.6, an update to Grok 4.5 aimed squarely at coding and other work usually done at a computer. The central claim is not that it introduces a wholly new kind of AI, but that it moves xAI much closer to the leading models from OpenAI and Anthropic while charging less for generated text.

All three early video assessments agree on the broad direction: Grok 4.6 is a substantial step up from 4.5. They also agree that xAI is emphasizing software engineering, technical reasoning and general knowledge work—the drafting, research, analysis and production tasks that make up much office work. The more difficult question is whether benchmark charts translate into dependable work. The early evidence is encouraging, but uneven.

## What the charts do—and do not—say

The reviewers cite xAI's published evaluations, where the model performs competitively against top rivals. Matthew Berman highlights a leading score on GDPval, an evaluation intended to test work-like tasks, as well as large gains over Grok 4.5 on Terminal Bench and other measures. He also notes that Grok 4.6 remains behind some competitors on DeepSWE, a coding benchmark.

That distinction matters. A benchmark is a controlled test: useful for spotting progress, but not a guarantee that a model will behave well in a messy real project. Wes Roth explicitly cautions that developers have seen models score well on benchmarks while failing ordinary tasks once people use them.

The first practical tests give both sides of that argument. Roth used Grok Build to make a small portal-based 3D puzzle. After some steering, he found it produced functioning portals, reflections and momentum effects in a few hours. He also used it to assemble a prototype that connected a game emulator, text-to-speech and a chat interface, though the prototype was still getting stuck in play.

Bijan Bowen ran a wider collection of build tests. Grok 4.6 created interactive web pages, browser-style interfaces, simple 3D games and a three-piece engine model that he actually printed. Some results had impressive finishing touches—working traffic lights, environmental details and interactive 3D product views. Others showed the ordinary fragility of generated software: cars initially moved sideways, character heads appeared far above their bodies, a skateboard was not independent of its rider, and some gameplay was rudimentary. In one case, the model corrected reported problems during a further pass.

So the useful reading of these demos is neither “the charts are fake” nor “the model can now make finished games on request.” Grok 4.6 appears able to produce ambitious prototypes quickly, but still needs human testing, clear requests and correction.

## Price, speed and the training story

The listed API price is $2 per million input tokens and $6 per million output tokens. Input tokens are the pieces of text sent to a model; output tokens are the pieces it generates. A faster variant costs twice as much, according to the sources. That price matters, but it is not the whole bill: a model that takes more attempts or produces more text can cost more to finish a task even with a lower per-token rate.

Berman points to an analysis estimating that Grok 4.6 costs more per task than Grok 4.5 while delivering a higher capability score. In his account, it nevertheless sits below a comparable rival in cost for a similar overall score. These are estimates, not a universal price tag; the task, the tool setup and the amount of back-and-forth all change the final cost.

The sources describe 4.6 as an extended training and post-training run built on the same 1.5-trillion-parameter base cited for 4.5. They say xAI used curated, model-generated material for reasoning and technical subjects, engineering data, and improved training methods. Berman describes Grok 4.5 helping generate training examples for 4.6—a common approach in which one model's outputs are filtered and used to teach another.

The videos also connect the release to Cursor, a coding-tool company they say was acquired and whose data helped strengthen Grok. That claim is central to their explanation of the rapid improvement, but it comes through the commentators' accounts rather than an independently supplied acquisition record.

## From model to colleague-like software

Alongside the model, Roth and Berman discuss Grok Bot, an agent product designed to keep working in cloud-based virtual machines. Rather than answering only in a chat window, it can create sub-agents, follow routines and return later with results. Roth describes assigning it to monitor posts on X three times daily for ten days.

That is a meaningful shift in product design: the promise is not merely better answers, but delegated work that continues after the user leaves. It also raises the stakes of mistakes. Roth recounts a separate agent accidentally sending a message while trying to search one. A system that can browse, use tools and act over time needs limits, review and carefully granted access—not just a strong benchmark score.

Grok 4.6 therefore looks less like a final verdict on xAI's position than a sharper competitive offer: capable enough to deserve serious testing, priced to encourage it, and packaged for work that must still be supervised.
