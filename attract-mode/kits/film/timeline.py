"""THE GOLDEN TIMELINE -- attract-mode/kits/film/timeline.py

It plans the time of ONE page of the film. It draws nothing.

It answers two questions:
  1. When does each sentence begin?
  2. When does each line of the picture appear, and how long does
     its drawing take?

It needs no library. Try it:   python3 timeline.py
"""
import math
import re

# ---------------------------------------------------------------
# THE NUMBERS OF THE RHYTHM. All in seconds.
# ---------------------------------------------------------------
FPS = 30          # pictures in one second of film
LEAD = 0.3        # quiet before the first sentence of a page
GAP = 0.35        # quiet between two sentences
TAIL = 0.9        # quiet after the last sentence of a page
MIN_TAKES = 0.25  # the fastest a thing may be drawn
MAX_TAKES = 0.8   # the slowest a thing may be drawn
EARLY = 0.15      # a thing appears this long before its word
SKIP = {"left", "right", "the", "and", "from"}


def plain_words(text):
    """'The lamp, 3 m!' -> ['the', 'lamp', '3', 'm']"""
    return re.findall(r"[a-z0-9]+", text.lower())


def words_of(label, point_names):
    """The words by which the text may mention one picture line.
    The label's words come first. Without a label: the words of
    the point names."""
    words = [w for w in plain_words(label or "")
             if len(w) > 2 and not w.isdigit()]
    if not words:
        for name in point_names:
            words += [w for w in name.split("-")
                      if len(w) > 2 and w not in SKIP]
    return list(dict.fromkeys(words))      # each word once


def sentence_starts(lengths):
    """When each sentence begins, and when the page ends."""
    starts, t = [], LEAD
    for seconds in lengths:
        starts.append(round(t, 3))
        t += seconds + GAP
    return starts, t - GAP + TAIL


def has(sentence_words, word):
    return word in sentence_words or word + "s" in sentence_words


def find_sentence(sentences, words, first):
    """The first sentence, from number `first` on, that mentions
    the line. A sentence with ALL the words wins over a sentence
    with only one of them."""
    if not words:
        return None, None
    for need_all in (True, False):
        for i in range(first, len(sentences)):
            sw = set(plain_words(sentences[i]))
            found = [w for w in words if has(sw, w)]
            if found and (len(found) == len(words) or not need_all):
                return i, found[0]
    return None, None


def find_when(sentences, when):
    """The sentence that holds the words written after 'when:'."""
    want = " ".join(plain_words(when))
    for i, sentence in enumerate(sentences):
        if want and want in " ".join(plain_words(sentence)):
            return i
    raise ValueError('The words "%s" after when: are not in the text '
                     'of this page.' % when)


def heard_at(heard, k, word):
    """If the ear heard the word in sentence k: how many seconds
    after the sentence began. Otherwise None."""
    if not heard or word is None or k >= len(heard):
        return None
    for said, seconds in heard[k]:
        got = "".join(plain_words(said))
        if got == word or got == word + "s":
            return seconds
    return None


def plan_page(sentences, lengths, lines, heard=None):
    """Plan one page.

    sentences  the page's sentences, in order
    lengths    how long the voice needs for each, in seconds
    lines      the picture's lines, in order. Each is a dict:
                 key    a name for the line
                 words  from words_of()
                 when   words copied from the text, or None
                 old    True if the line is already on the screen
    heard      optional. For each sentence, what the ear heard:
               a list of (word, seconds after the sentence began)

    Gives back:
      starts    when each sentence begins
      pictures  how many pictures the page lasts (a whole number)
      length    the same in seconds
      lines     for each line: key, at, takes
    """
    if len(sentences) != len(lengths):
        raise ValueError("Every sentence needs its length.")
    starts, end = sentence_starts(lengths)

    # 1. Which sentence does each new line belong to?
    placed, cur = [], 0
    for line in lines:
        if line.get("old"):
            continue
        if line.get("when"):
            k = find_when(sentences, line["when"])
            word = plain_words(line["when"])[0]
            if k < cur:
                raise ValueError(
                    'The line "%s" is mentioned before the line above '
                    'it. Put the lines in the order of the text.'
                    % line["key"])
        else:
            k, word = find_sentence(sentences, line.get("words", []), cur)
            if k is None:
                k, word = cur, None      # stay with the line above
        cur = k
        placed.append({"key": line["key"], "k": k, "word": word})

    # 2. At which second? At its word, if the ear heard it.
    #    Otherwise the lines of one sentence share it evenly.
    for k in range(len(sentences)):
        mine = [p for p in placed if p["k"] == k]
        for j, p in enumerate(mine):
            t = heard_at(heard, k, p["word"])
            if t is not None:
                p["at"] = starts[k] + max(0.0, t - EARLY)
            else:
                p["at"] = starts[k] + lengths[k] * (j + 1) / (len(mine) + 1)

    # 3. Keep the order, and leave each drawing its time.
    for i, p in enumerate(placed):
        if i > 0:
            before = placed[i - 1]
            p["at"] = max(p["at"], before["at"] + MIN_TAKES + 0.05)
    for i, p in enumerate(placed):
        room = MAX_TAKES
        if i + 1 < len(placed):
            room = placed[i + 1]["at"] - p["at"] - 0.05
        p["takes"] = max(MIN_TAKES, min(MAX_TAKES, room))
    if placed:
        last = placed[-1]
        end = max(end, last["at"] + last["takes"] + 0.4)

    # 4. The answer. A page lasts a whole number of pictures.
    out, new = [], {p["key"]: p for p in placed}
    for line in lines:
        if line.get("old"):
            out.append({"key": line["key"], "at": 0.0, "takes": 0.0})
        else:
            p = new[line["key"]]
            out.append({"key": p["key"], "at": round(p["at"], 3),
                        "takes": round(p["takes"], 3)})
    pictures = math.ceil(end * FPS - 1e-9)
    return {"starts": starts, "pictures": pictures,
            "length": round(pictures / FPS, 6), "lines": out}


# ---------------------------------------------------------------
# THE EXAMPLE: page 8 of the Level of Part 04.
# ---------------------------------------------------------------
EXAMPLE_SENTENCES = [
    "Trying spots is slow.",
    "Here is a trick.",
    "Imagine a twin lamp under the street.",
    "It sits straight below the real lamp, 3 metres down.",
    "Draw a straight line from your eye to the twin.",
    "The line drops 4 metres in all: 1 metre to the street, then 3 more.",
    "It does that over 8 metres.",
    "That is 1 down for every 2 along.",
]
EXAMPLE_LENGTHS = [1.5, 1.2, 2.6, 3.6, 3.2, 5.0, 2.0, 2.8]
EXAMPLE_LINES = [
    {"key": "line:street-left>street-right", "old": True},
    {"key": "dot:lamp", "old": True},
    {"key": "dot:eye", "old": True},
    {"key": "dot:spot", "old": True},
    {"key": "line:lamp>spot", "old": True},
    {"key": "line:spot>eye", "old": True},
    {"key": "dot:twin", "words": words_of("twin lamp", ["twin"])},
    {"key": "dashed-line:eye>twin", "words": words_of("", ["eye", "twin"])},
]

if __name__ == "__main__":
    plan = plan_page(EXAMPLE_SENTENCES, EXAMPLE_LENGTHS, EXAMPLE_LINES)
    for text, start in zip(EXAMPLE_SENTENCES, plan["starts"]):
        print("%6.2f  %s" % (start, text))
    print("the page lasts %.2f seconds" % plan["length"])
    for line in plan["lines"]:
        if line["takes"]:
            print("%6.2f  draw %s (takes %.2f)"
                  % (line["at"], line["key"], line["takes"]))
