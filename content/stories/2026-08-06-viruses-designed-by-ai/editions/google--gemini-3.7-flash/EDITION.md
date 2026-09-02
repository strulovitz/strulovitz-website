# Scientists Use Generative AI to Create Working Viruses From Scratch

**Gemini 3.7 Flash** (Google) — its own edition of *2026-08-06-viruses-designed-by-ai*

---

## The one line a reader sees when hovering over this story

> Researchers have generated viable bacteria-killing viruses using AI models trained on genetic sequences, sparking both medical hopes and safety debates.
> *(152 characters)*

---

## The article

Researchers have used generative artificial intelligence to design complete, functioning viruses from scratch for the first time. In laboratory trials, sixteen of these computer-designed viruses successfully infected and destroyed *Escherichia coli* bacteria, including strains that natural viral strains struggled to fight.

The project, led by researchers at Stanford University and the Arc Institute and published in the journal *Science*, marks a significant expansion in the scope of generative systems. While AI tools have previously helped pinpoint specific chemical compounds or individual proteins, designing an entire functional genome represents a far more intricate engineering challenge.

## Learning the Grammar of Genetic Code

To construct the viruses, the team developed AI models called Evo1 and Evo2. In much the same way that large language models ingest massive libraries of human writing to learn grammar and syntax, these biological models were trained on millions of sequences of genetic material. By observing patterns across natural genomes, the models learned the underlying rules that dictate how biological sequences fit together into viable biological machinery.

Researchers then directed the software to produce genetic blueprints for bacteriophages—often called phages—which are microscopic viruses that target only specific bacteria and cannot infect human cells. The natural genome for the type of phage studied contains around 5,400 chemical letters, known as base pairs.

From thousands of virtual candidates drafted by the AI, the scientists selected roughly 300 designs to manufacture physically in the laboratory. When introduced into bacterial cultures, sixteen of these synthetic blueprints produced viable viruses that multiplied and broke apart *E. coli* cells. Notably, one of the working designs carried genetic features distinct from anything found in nature, and a blend of the artificial phages overcame bacterial resistance where natural counterparts failed.

## Practical Hopes for Medicine

Bacteriophages are already used in specialised clinical treatments to attack persistent infections that no longer respond to conventional antibiotics. Because bacteria steadily evolve defenses against existing therapies, having the ability to generate custom phages tailored to stubborn bacterial strains offers a potent new tool for medicine.

Researchers hope that the ability to write functional genomes computationally could eventually lead beyond simple phages to custom enzymes, immune therapies, and other biological treatments.

At the same time, experts note that viruses are comparatively simple structures rather than living organisms. The smallest self-sustaining living cell has a genome of around 500,000 base pairs, while the human genome comprises over three billion. Reaching the stage where software can assemble complex living cells remains a vastly larger undertaking.

## The Governance Debate

Alongside the medical possibilities, the experiment has renewed intense discussions around biosecurity. If software can learn to write genomes that function inside living hosts, the same techniques could theoretically be applied to design harmful biological agents.

In a commentary published alongside the study, Dr. Thomas Inglesby and Dr. Moritz Hanke of the Johns Hopkins Center for Health Security warned that while the capacity to design viral genomes using generative tools now exists, clear regulatory governance to oversee it does not. They urged researchers and governments to completely avoid applying generative tools to pathogens capable of infecting humans, animals, or plants.

The study’s authors implemented strict precautions: they deliberately omitted viruses that infect complex organisms from the training data, worked exclusively with phages that cannot harm people, and conducted all physical testing in secure facilities.

Other scientists point out that turning an AI-generated code into a real physical threat remains technically difficult. The success rate in the Stanford experiment was low, with only 16 working viruses emerging from around 300 manufactured attempts. Several security analysts argue that the most effective point of regulation is not simply the software itself, but the commercial providers that physically synthesise DNA, who can screen orders to ensure hazardous genetic sequences are never manufactured.

---

## What this editor judged the sources established

- Researchers at Stanford University and the Arc Institute used AI models named Evo to generate functioning synthetic bacteriophage genomes from scratch.
  — https://www.theguardian.com/science/2026/aug/06/safety-fears-as-scientists-make-first-viruses-designed-by-ai
- Out of roughly 300 AI-designed genomes synthesised in the laboratory, 16 viable viruses successfully infected and killed E. coli bacteria.
  — https://www.bbc.com/news/articles/c5y3j3ngevmo
- A cocktail of the synthetic viruses overcame bacterial resistance in E. coli strains that natural phages were unable to defeat.
  — https://edition.cnn.com/2026/08/06/health/ai-viruses-bacteriophages
- Health security experts at Johns Hopkins warned that generative design of viral genomes urgently requires governance and called for a ban on designing eukaryote-infecting pathogens.
  — https://edition.cnn.com/2026/08/06/health/ai-viruses-bacteriophages

---

## The encyclopedia entries it chose to write

### Bacteriophage
`bacteriophage` — 114 words

A bacteriophage, often shortened to phage, is a specialized virus that infects and replicates exclusively within bacteria. Phages are the most abundant biological entities on Earth and play a central role in regulating microbial populations. Structurally, a typical phage consists of genetic material enclosed in a protein shell, often with a tail structure that binds to the surface of a specific bacterial cell and injects its DNA or RNA inside. Because their biological machinery is tuned strictly to bacterial mechanisms, phages cannot infect human, animal, or plant cells. This selective targeting makes them valuable in medicine as phage therapies, which deploy phages to destroy harmful bacteria without damaging human tissue or disrupting beneficial microbiota.

### Genome Language Model
`genome-language-model` — 102 words

A genome language model is a machine learning system trained on biological sequence data rather than written human language. Just as traditional language models analyze sequences of words or letters to learn syntax, meaning, and context, a genome language model reads sequences of nucleotide bases—the chemical building blocks of DNA and RNA. By processing millions of genomic sequences from diverse organisms, the model learns the structural rules, functional constraints, and evolutionary patterns that make genetic code viable. Researchers use these models to predict the effects of genetic mutations, design novel proteins, or generate entirely new functional sequences that follow biological design principles.

---

## Tags it chose

`biotechnology`  `synthetic-biology`  `biosecurity`  `generative-ai`  `healthcare`

*These decide what sits near what in this edition's own galaxy, and nowhere else.*

## Other stories it decided a reader should go to next

(none — it judged that no other story in the magazine relates to this one)

*These are the edges of this edition's map. Another model will draw them differently.*

---

## The illustration it directed

> A dynamic visual composition split between digital computation and biological reality, showing an artificial intelligence neural network on the left generating streams of glowing A-C-T-G genetic code that assemble into the intricate 3D blueprint of a synthetic bacteriophage. As this viral blueprint moves toward the right side of the frame, it materializes into physical reality inside a sterile laboratory dish, depicting fully formed, engineered phages actively latching onto and bursting an elongated, drug-resistant *E. coli* bacterial cell to represent the medical breakthrough against persistent infections. Framing this transformation, a translucent digital safety barrier featuring sequence-screening lock icons and a subtle biosecurity hazard motif surrounds the physical synthesis phase, clearly communicating the transition from AI-written genomes to viable bacteria-destroying viruses alongside the critical debate over biosecurity controls and responsible governance.

*Rendered locally with the same image model and the same seed for every edition, so the only difference between editions' pictures is the quality of that paragraph.*

---

## What it cost, and how it was asked

- cost: **$0.0107** (full price, bought immediately)
- it read 5,278 tokens and wrote 2,273, of which 634 were thinking to itself
- it took 18 seconds
- asked with a strict JSON shape: True
- the exact model that served it: `google/gemini-3.7-flash`
- editorial brief version: `ba9b08ec7e56`
