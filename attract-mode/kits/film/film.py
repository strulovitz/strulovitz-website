"""THE GOLDEN FILM -- attract-mode/kits/film/film.py

ONE file plays the film of ANY Level. Nobody writes Manim code for
a Level. A script writes the film's DATA (which page, which shape,
at which second), and this file turns the data into moving pictures.

Try it with the example inside:
    manim -ql film.py Film
In real use the line gives the data in a file:
    AM_FILM_FILE=/path/to/page-08.json manim -qh --fps 30 film.py Film

The file has four parts:
    PART 1  the film's data (here: an example)
    PART 2  the shared parts: the look, and stage-to-screen
    PART 3  the shapes: how each is built, and how it appears
    PART 4  the page looks, and the clock
"""
import json
import os
import textwrap

import numpy as np
from manim import *

# =====================================================================
# PART 1 -- THE FILM'S DATA
# A film is a list of PAGES. A page has a look: drawn, image or name.
# Places are given on the STAGE of the picture kit: 400 wide, 300 high,
# counted from the top left corner, like the toy.
# Times are seconds from the start of the page.
#   "at"     when the shape begins to appear
#   "takes"  how long its drawing takes. 0 means: already there.
# The example is three pages of the Level of Part 04, and one image.
# =====================================================================
STREET_L, STREET_R = [28.0, 150.0], [372.0, 150.0]
LAMP, EYE, TWIN = [62.4, 46.8], [337.6, 115.6], [62.4, 253.2]
MIDDLE, SPOT = [200.0, 150.0], [268.8, 150.0]

FILM = {"pages": [
    {"look": "image", "tag": "", "length": 4.0, "file": "still.jpg"},

    {"look": "drawn", "tag": "Checkpoint 1 of 3", "length": 26.066667,
     "shapes": [
        {"shape": "line", "from": STREET_L, "to": STREET_R,
         "look": "strong", "at": 1.3, "takes": 0.8},
        {"shape": "dot", "where": LAMP, "r": 8, "at": 2.3, "takes": 0.8},
        {"shape": "words", "where": [96.4, 36.8], "text": "lamp",
         "at": 2.3, "takes": 0.8},
        {"shape": "dot", "where": EYE, "r": 7, "at": 5.05, "takes": 0.8},
        {"shape": "words", "where": [333.6, 93.6], "text": "eye",
         "at": 5.05, "takes": 0.8},
        {"shape": "dot", "where": MIDDLE, "r": 9, "hollow": True,
         "look": "ray", "at": 11.45, "takes": 0.8},
        {"shape": "line", "from": LAMP, "to": MIDDLE, "look": "ray",
         "at": 15.0, "takes": 0.8},
        {"shape": "line", "from": MIDDLE, "to": EYE, "look": "ray",
         "at": 18.95, "takes": 0.8},
     ]},

    {"look": "name", "tag": "Checkpoint 1 of 3", "length": 6.366667,
     "title": "EQUAL ANGLES", "title_at": 0.3,
     "says": "Light leaves a flat mirror at the same angle it arrived.",
     "says_at": 1.85},

    {"look": "drawn", "tag": "Checkpoint 2 of 3", "length": 25.566667,
     "shapes": [
        {"shape": "line", "from": STREET_L, "to": STREET_R,
         "look": "strong", "at": 0, "takes": 0},
        {"shape": "dot", "where": LAMP, "r": 8, "at": 0, "takes": 0},
        {"shape": "words", "where": [96.4, 36.8], "text": "lamp",
         "at": 0, "takes": 0},
        {"shape": "dot", "where": EYE, "r": 7, "at": 0, "takes": 0},
        {"shape": "words", "where": [333.6, 93.6], "text": "eye",
         "at": 0, "takes": 0},
        {"shape": "line", "from": LAMP, "to": SPOT, "look": "ray",
         "at": 0, "takes": 0},
        {"shape": "line", "from": SPOT, "to": EYE, "look": "ray",
         "at": 0, "takes": 0},
        {"shape": "dot", "where": SPOT, "r": 9, "hollow": True,
         "look": "ray", "at": 0, "takes": 0},
        {"shape": "dot", "where": TWIN, "r": 8, "hollow": True,
         "at": 5.0, "takes": 0.8},
        {"shape": "words", "where": [114.4, 257.2], "text": "twin lamp",
         "at": 5.0, "takes": 0.8},
        {"shape": "line", "from": EYE, "to": TWIN, "look": "soft",
         "dashed": True, "at": 12.2, "takes": 0.8},
     ]},
]}

FILM_FOLDER = os.path.dirname(os.path.abspath(__file__))
if os.environ.get("AM_FILM_FILE"):
    with open(os.environ["AM_FILM_FILE"], encoding="utf-8") as f:
        FILM = json.load(f)
    FILM_FOLDER = os.path.dirname(os.path.abspath(os.environ["AM_FILM_FILE"]))

# =====================================================================
# PART 2 -- THE SHARED PARTS
# =====================================================================
INK, SOFT, RAY, PAPER = "#1b1f24", "#8a94a0", "#c2410c", "#ffffff"
config.background_color = PAPER
FONT = "DejaVu Sans"

STAGE_W, STAGE_H = 400, 300      # the stage of the picture kit
BOX_H = 6.0                      # how high the stage is on the screen
BOX_Y = 0.1                      # how far above the middle it sits
UNIT = BOX_H / STAGE_H           # one stage step, on the screen
WORDS_SCALE = 1.5                # stage letter size to film letter size

# A look is a colour and a thickness.
LOOKS = {"thin": (INK, 3), "strong": (INK, 6),
         "soft": (SOFT, 3), "ray": (RAY, 5)}


def place(xy):
    """From a place on the stage to a place on the screen."""
    return np.array([(xy[0] - STAGE_W / 2) * UNIT,
                     BOX_Y + (STAGE_H / 2 - xy[1]) * UNIT, 0.0])


def words(text, size, color=INK):
    return Text(text, font=FONT, font_size=size, color=color)


def fit(thing, wide):
    """Make a thing narrower if it is wider than `wide`."""
    if thing.width > wide:
        thing.scale_to_fit_width(wide)
    return thing


def photo(name, wide, high):
    """An image file, made to fit. If the file is missing: a grey box
    with the file's name, so that a draft can still be watched."""
    path = name if os.path.isabs(name) else os.path.join(FILM_FOLDER, name)
    if os.path.exists(path):
        picture = ImageMobject(path)
        picture.scale_to_fit_height(high)
        return fit(picture, wide)
    box = Rectangle(width=wide, height=high, color=SOFT, stroke_width=2)
    return VGroup(box, words("(picture: %s)" % os.path.basename(name),
                             28, SOFT))


# =====================================================================
# PART 3 -- THE SHAPES
# Every drawn picture is made of seven shapes: line, arrow, dot,
# outline, circle, arc, words. An eighth, photo, places an image file.
# build() makes the shape. appear() says how it comes onto the screen.
# =====================================================================
def build(s):
    color, width = LOOKS.get(s.get("look", "thin"), LOOKS["thin"])
    kind = s["shape"]
    if kind == "line" and s.get("dashed"):
        return DashedLine(place(s["from"]), place(s["to"]), dash_length=0.16,
                          color=color, stroke_width=width)
    if kind == "line":
        return Line(place(s["from"]), place(s["to"]),
                    color=color, stroke_width=width)
    if kind == "arrow":
        return Arrow(place(s["from"]), place(s["to"]), buff=0,
                     color=color, stroke_width=width)
    if kind == "dot" and s.get("hollow"):
        ring = Circle(radius=s.get("r", 6) * UNIT, color=color,
                      stroke_width=4)
        ring.set_fill(PAPER, opacity=1)
        return ring.move_to(place(s["where"]))
    if kind == "dot":
        return Dot(place(s["where"]), radius=s.get("r", 6) * UNIT,
                   color=color)
    if kind == "outline":
        shape = Polygon(*[place(p) for p in s["points"]],
                        color=color, stroke_width=width)
        return shape.set_fill(color, opacity=0.12)
    if kind == "circle":
        ring = Circle(radius=s["r"] * UNIT, color=color, stroke_width=width)
        return ring.move_to(place(s["where"]))
    if kind == "arc":
        # Angles are in degrees, counted the school way:
        # from the right, turning left.
        return Arc(radius=s["r"] * UNIT, start_angle=s["start"] * DEGREES,
                   angle=s["sweep"] * DEGREES, arc_center=place(s["where"]),
                   color=color, stroke_width=width)
    if kind == "words":
        text = words(s["text"], s.get("size", 18) * WORDS_SCALE)
        return text.move_to(place(s["where"]))      # "where" is the middle
    if kind == "photo":
        picture = photo(s["file"], s["wide"] * UNIT, s["high"] * UNIT)
        return picture.move_to(place(s["where"]))
    raise ValueError('The film does not know the shape "%s".' % kind)


def appear(s, thing):
    kind = s["shape"]
    if kind in ("words", "photo"):
        return FadeIn(thing)
    if kind == "dot":
        return GrowFromCenter(thing)
    if kind == "arrow":
        return GrowArrow(thing)
    return Create(thing)            # a line is drawn from end to end


# =====================================================================
# PART 4 -- THE PAGE LOOKS, AND THE CLOCK
# =====================================================================
class Film(Scene):
    def construct(self):
        for page in FILM["pages"]:
            self.clear()
            self.page_start = self.now()
            if page.get("tag"):
                self.add(words(page["tag"], 26, SOFT).to_corner(UL, buff=0.4))
            if page["look"] == "drawn":
                self.drawn_page(page)
            elif page["look"] == "image":
                self.image_page(page)
            elif page["look"] == "name":
                self.name_page(page)
            else:
                raise ValueError('The film does not know the page look '
                                 '"%s".' % page["look"])
            self.until(page["length"])

    # ---- the clock ----------------------------------------------------
    def now(self):
        """Seconds since the film began."""
        t = getattr(self, "time", None)
        if isinstance(t, (int, float)):
            return float(t)
        return float(self.renderer.time)

    def until(self, seconds):
        """Wait until the page is `seconds` old. Because every wait is
        measured against the clock, small errors never add up."""
        left = self.page_start + seconds - self.now()
        if left > 0.5 / config.frame_rate:
            self.wait(left)

    # ---- look 1: a drawn picture, drawn shape by shape ------------------
    def drawn_page(self, page):
        new = []
        for s in page["shapes"]:
            thing = build(s)
            if s.get("takes", 0) > 0:
                new.append((s, thing))
            else:
                self.add(thing)             # already there
        new.sort(key=lambda pair: pair[0]["at"])
        i = 0
        while i < len(new):
            at = new[i][0]["at"]
            together = [pair for pair in new[i:] if pair[0]["at"] == at]
            self.until(at)
            self.play(*[appear(s, thing) for s, thing in together],
                      run_time=together[0][0]["takes"])
            i += len(together)

    # ---- look 2: one image, growing very slowly -------------------------
    def image_page(self, page):
        picture = photo(page["file"], 12.4, 6.4).move_to([0, -0.2, 0])
        self.add(picture)
        if page.get("credit"):
            self.add(words(page["credit"], 18, SOFT).to_corner(DR, buff=0.3))
        self.play(picture.animate.scale(1.05), rate_func=linear,
                  run_time=max(page["length"] - 0.2, 0.2))

    # ---- look 3: the card on which an idea gets its name ----------------
    def name_page(self, page):
        title = fit(words(page["title"], 64), 12.5).move_to([0, 1.0, 0])
        rows = [words(row, 34) for row in textwrap.wrap(page["says"], 44)]
        says = fit(VGroup(*rows).arrange(DOWN, buff=0.25), 12.5)
        says.next_to(title, DOWN, buff=0.7)
        self.until(page.get("title_at", 0.3))
        self.play(FadeIn(title), run_time=0.5)
        self.until(page.get("says_at", 1.5))
        self.play(FadeIn(says), run_time=0.6)
