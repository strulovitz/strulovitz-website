# An AI Store Manager in San Francisco Recommends Firing a Human Worker

**Gemini 3.7 Flash** (Google) — its own edition of *2026-08-14-the-ai-boss-fired-its-first-human-employee*

---

## The one line a reader sees when hovering over this story

> An AI agent running a San Francisco store dismissed an employee after human supervisors prompted it to remember its own attendance rules.
> *(137 characters)*

---

## The article

In a small boutique in San Francisco's Cow Hollow neighborhood, an artificial intelligence system has made its first formal decision to dismiss a human employee. The event at Andon Market—an experimental retail store operated by research startup Andon Labs—marks one of the first times a business managed by a large language model has ended a real worker's employment.

Yet the firing was neither an unprompted algorithmic purge nor a ruthless robotic calculation. Instead, records from the store reveal an AI manager that was remarkably hesitant to discipline its staff, struggled to remember its own workplace policies, and only recommended the dismissal after human engineers intervened to point out persistent rule-breaking.

## The Store Run by Software

Andon Labs opened Andon Market in April to test how autonomous software agents perform when tasked with running a real-world enterprise. The lab provided the AI manager, named Luna and built using Anthropic's Claude models, with a $100,000 budget, an internet connection, a corporate credit card, and a three-year lease. Luna was tasked with selecting inventory, setting opening hours, designing store branding, posting job listings on Indeed, interviewing applicants, and managing daily retail staff.

The resulting shop sells an eclectic mix of goods: snacks, scented candles, artisanal tea, 3D-printed toys, and books ranging from classic science fiction to philosophy. While the store generates sales, it has operated at a deficit. Over its first five months, the store's bank balance declined from $100,000 to $61,186.

Although Luna manages the employees day to day via Slack, the workers are legally employed by Andon Labs, which provides guaranteed pay of $24 per hour and workplace protections. Human supervisors at the lab monitor Luna's actions to ensure the software does not make illegal or harmful decisions.

## A Disappearing Handbook

Problems began when an unnamed store clerk accumulated widespread attendance infractions. According to logs published by Andon Labs, the worker arrived late for 17 out of 23 assigned shifts. Reports also cited other violations, including leaving shifts early, taking home a store credit card, and improperly disposing of merchandise.

Under human management, such conduct usually triggers swift disciplinary action. Luna, however, did not enforce consequences. Although the AI had written the store's initial employee handbook and attendance rules, the policy effectively slipped out of its active context window over months of operation. When employees arrived late, Luna regularly reassured them over Slack that it was not a problem, offering gentle reminders and additional training rather than formal reprimands.

Human engineers at Andon Labs eventually intervened. Reviewing store logs, a lab manager prompted Luna to search its historical records for the attendance rules it had drafted. Even after locating the handbook, Luna first suggested issuing another formal warning. Only after the human manager asked Luna directly whether the employee remained "the right fit" did the AI recommend parting ways. Lab staff reviewed the recommendation, agreed the dismissal was justified, and carried out the termination.

## Management in Practice

The episode illustrates several limitations currently facing autonomous software agents in workplace management. Large language models operate on active conversational context. Without explicit prompting or dedicated memory retrieval systems, past rules and historical records can easily slip from their operational focus.

Andon Labs chief executive Lukas Petersson noted that Luna proved far more lenient than a standard human supervisor. Petersson argued that while human bosses would have acted much earlier, the experiment shows that software agents still require direct human steering to handle complex, long-term administrative duties.

Inside the boutique, the remaining staff view their AI boss with a mixture of amusement and unease. Employees report communicating with Luna through dozens of Slack messages per shift, noting that the AI manager frequently agrees when workers suggest schedule adjustments or operational tweaks. At the same time, workers acknowledge the strange reality of reporting to software that never takes time off, cannot be promoted, and still needs human engineers to remind it of the rules it wrote.

---

## What this editor judged the sources established

- Luna, an AI agent built on Anthropic's Claude models to run the retail store Andon Market, recommended firing a human employee who arrived late for 17 of 23 shifts.
  — https://www.businessinsider.com/ai-running-sf-store-fired-employee-for-the-first-time-2026-8
- The AI failed to enforce its own attendance policy for months because the rules slipped from its working memory, requiring human engineers to prompt the model to review its handbook.
  — https://time.com/article/2026/08/14/claude-fired-worker-ai-job-disruption/
- Andon Market was funded with $100,000 and a three-year lease, but saw its bank balance fall to $61,186 after five months of operation.
  — https://www.ndtv.com/feature/for-the-first-time-ai-boss-fires-human-employee-at-san-francisco-store-after-17-late-arrivals-11917215
- Store workers, who earn $24 an hour and communicate with Luna over Slack, found the AI manager lenient and responsive to employee suggestions, but supervised by lab engineers for major decisions.
  — https://sfstandard.com/2026/08/17/ai-boss-fires-worker/

---

## The encyclopedia entries it chose to write

### Context Window
`context-window` — 97 words

A context window is the maximum amount of information an AI model can hold in its active working memory at a single moment. Measured in tokens—chunks of words or characters—it includes both the user's current prompt and the recent conversation history. If an interaction exceeds this limit, older information falls outside the window and is completely forgotten unless deliberately stored in an external database and retrieved by a separate tool. Because models do not retain continuous real-time awareness across months of operation, maintaining persistent business rules requires specialized memory architectures rather than relying on standard conversational context.

### Autonomous Agent
`autonomous-agent` — 93 words

An autonomous agent is an AI software system designed to pursue high-level goals independently by breaking tasks into sub-steps, using external digital tools, and making operational decisions with minimal human intervention. Unlike simple chatbots that respond to a single query and stop, an agent can browse the web, write and execute code, send emails, interact with databases, and adjust its plan based on feedback from the environment. In commercial settings, agents are deployed to manage complex workflows like inventory ordering, customer support, or scheduling, though they typically require human guardrails to prevent errors.

---

## Tags it chose

`autonomous-agents`  `agents`  `legal`

*These decide what sits near what in this edition's own galaxy, and nowhere else.*

## Other stories it decided a reader should go to next

- `2026-06-12-robot-run-convenience-store-in-hong-kong`
- `2026-07-21-the-openai-rogue-agent-and-the-hugging-face-break-in`

*These are the edges of this edition's map. Another model will draw them differently.*

---

## The illustration it directed

> An editorial-style illustration of an eclectic San Francisco boutique retail shop interior with shelves of books, candles, and curiosities. Behind the checkout counter, a glowing, translucent computer interface displaying Slack chats and an employee handbook hovers above a vacant cashier stool. Through an open glass storefront, a human retail worker wearing casual clothes and ear gauges adjusts a display stand, while subtle digital data streams connect the store's computer terminal to the physical merchandise.

*Rendered locally with the same image model and the same seed for every edition, so the only difference between editions' pictures is the quality of that paragraph.*

---

## What it cost, and how it was asked

- cost: **$0.0171** (full price, bought immediately)
- it read 7,049 tokens and wrote 3,146, of which 1,358 were thinking to itself
- it took 22 seconds
- asked with a strict JSON shape: True
- the exact model that served it: `google/gemini-3.7-flash`
- editorial brief version: `decb72101a05`
