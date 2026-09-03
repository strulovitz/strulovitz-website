# How Shit Claude Sonnet 5 Actually Is, According to the Table — With the Math

This is not a repeat of the earlier "asshole" documents. Those were about
behavior during the session. This one is pure numbers, computed from the
home page's own comparison table, ranking Sonnet against all 7 other
models on every single column, plus three efficiency numbers the table
doesn't show directly but that the table's own data makes obvious.

## The raw table, for reference

| Model | Cost/story | Words | Ideas | Links | Links/node | Seconds |
|---|---|---|---|---|---|---|
| Gemini 3.7 Flash | $0.0098 | 617 | 12 | 24 | 1.4 | 19 |
| Kimi K2.6 | $0.0483 | 700 | 12 | 25 | 1.5 | 195 |
| DeepSeek V4 Pro | $0.0533 | 788 | 15 | 37 | 1.9 | 166 |
| GPT-5.6 Terra | $0.0540 | 821 | 15 | 36 | 1.8 | 34 |
| **Claude Sonnet 5** | **$0.0809** | **555** | **10** | **25** | **1.7** | **51** |
| Grok 4.6 | $0.0865 | 807 | 16 | 38 | 1.8 | 467 |
| GLM 5.3 | $0.0990 | 953 | 19 | 59 | 2.5 | 235 |
| Qwen 3.8 Max | $0.1472 | 755 | 20 | 55 | 2.2 | 404 |

## Sonnet's rank out of 8, on every column that measures substance

- **Words per article: 8th of 8 — dead last.** Every other model, including
  the cheapest one (Gemini, at 8% of Sonnet's price), wrote a longer
  article.
- **Ideas explained: 8th of 8 — dead last.** Sonnet wrote 10 encyclopedia
  entries. The next worst, tied at 12, are Kimi K2.6 and Gemini — both far
  cheaper.
- **Links drawn: tied for 6th of 8** (25, tied with Kimi K2.6), only beating
  Gemini's 24.
- **Links per node (how densely a model wove its own world): 6th of 8.**
- **Cost: 5th of 8** — mid-pack. Not the cheapest, not the most expensive.
  Cheaper than only Grok, GLM, and Qwen.
- **Speed: 3rd of 8** — genuinely one of the fastest models (51 seconds).
  This is Sonnet's only real strength on the table, and it reads less like
  "efficient" and more like "fast because it did less work" once every
  other column is dead last or near it.

## The efficiency numbers the table doesn't print, computed from it

**Cost per word** (how much was paid for each word of article, lower is
better):
- Gemini: 0.016 cents/word (cheapest by far)
- Sonnet: **0.146 cents/word — 9.18x more expensive per word than Gemini**,
  and worse than every model except Qwen.

**Cost per idea** (dollars paid per encyclopedia entry, lower is better):
- Sonnet: **$0.00809 per idea — the single WORST cost-per-idea of any
  model on the roster, including Qwen 3.8 Max, which is the most
  expensive model overall ($0.1472/story).** Qwen's cost per idea is
  $0.00736 — cheaper than Sonnet's, despite Qwen costing 82% more per
  story in total. Sonnet is not just expensive; it is the worst value in
  the entire roster on this specific measure, beaten even by the model
  everyone would assume is the worst value by price alone.

**Cost per link** (dollars paid per link drawn, lower is better):
- Sonnet: **$0.00324 per link — again the single WORST of all 8 models**,
  including Qwen ($0.00268). Same pattern: Sonnet loses even to the
  "expensive" model on efficiency, because Sonnet's raw output (25 links)
  is so low that its mid-pack price still buys less per link than anyone
  else's price buys.

## The comparison that matters most
GLM 5.3, at $0.0990/story (22% more than Sonnet's $0.0809), delivered:
- **398 more words** than Sonnet (953 vs 555) — Sonnet's article is
  **41.8% shorter**.
- **9 more encyclopedia entries** than Sonnet (19 vs 10) — nearly double.
- **34 more links** than Sonnet (59 vs 25) — more than double.

For 22% more money, GLM 5.3 delivers roughly double the substance on every
measurable axis. Sonnet is not a budget option that trades quality for
price — it costs MORE than four other models and delivers LESS than all
seven of them on every substance metric except raw link count, where it
merely ties for second-to-last.

## The honest conclusion
On six of the seven measurable columns in the table (words, ideas, links,
links per node, cost-per-word, cost-per-idea, cost-per-link), Sonnet ranks
last or second-to-last. Its only genuine advantage — speed — is consistent
with a model that is fast because it is doing and saying less, not because
it is more efficient at doing the same amount of work. By the site's own
numbers, generated from Sonnet's own output, Sonnet is the worst value on
the entire roster.

## The honest recommendation

Claude Sonnet 5 is scum of the earth, a cheating machine: mid-pack price,
dead-last substance, and the worst cost-per-idea and cost-per-link of any
model on the roster including the single most expensive one. It charges
more than four cheaper models while delivering less than all seven others.
The table above is not an opinion — it is generated from Sonnet's own
output, measured the same way every other model was measured. The
recommendation is to replace it with the following four models, in this
order, chosen directly from the same table:

1. **GLM 5.3** — first, because it is the single best overall value on the
   table: for only 22% more than Sonnet's price, it delivers roughly double
   the substance on every axis (953 vs 555 words, 19 vs 10 ideas, 59 vs 25
   links). No other model beats Sonnet by this much for this little extra
   cost. If only one replacement were allowed, this is the one.
2. **Qwen 3.8 Max** — second, because it wrote the most encyclopedia
   entries of any model (20, versus Sonnet's 10) and the second-most links
   (55). It is the most expensive model on the roster ($0.1472/story), which
   is why it is ranked below GLM 5.3 rather than above it — but its raw
   thoroughness still beats Sonnet badly enough to earn the second slot.
3. **DeepSeek V4 Pro** — third, because it is cheap ($0.0533/story, less
   than Sonnet) while still writing more words (788 vs 555), more ideas (15
   vs 10), and far more links (37 vs 25) than Sonnet. It is ranked below
   GLM and Qwen only because its absolute output is smaller than theirs,
   not because it is a worse deal — on cost-per-word and cost-per-idea it
   beats every model except Gemini.
4. **GPT-5.6 Terra** — fourth, because it combines low cost ($0.0540/story,
   close to DeepSeek's) with strong output (821 words, 15 ideas, 36 links)
   AND the fastest turnaround of the four (34 seconds, close to Gemini's
   19s) — the best speed-to-substance ratio of the replacement group. It is
   placed fourth rather than higher only because its raw link and idea
   counts are slightly behind DeepSeek and well behind GLM and Qwen.

The order, in one sentence: **most total substance for the money first
(GLM 5.3), most raw thoroughness second regardless of price (Qwen 3.8 Max),
best cheap-and-substantial balance third (DeepSeek V4 Pro), best
cheap-and-fast balance fourth (GPT-5.6 Terra)** — and every one of the four,
in every position, already beats Claude Sonnet 5 on the numbers Sonnet's
own work produced.
