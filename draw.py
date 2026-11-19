#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Thursday 19 November 2026.

Everything on the page is drawn with Pillow: no photographs, no downloaded
assets. The page is one 1024x1024 PNG, laid out top to bottom as a masthead,
a dateline strip, a lead story with a skyline illustration, two mid-page
stories, three short columns and a briefs strip.

Run:  python3 draw.py        (writes entry.png next to this file)
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (253, 244, 222)      # warm newsprint
INK = (17, 17, 17)           # near-black text
SOFT_INK = (60, 55, 45)      # body copy
RED = (176, 30, 30)          # kickers, dateline accent
RULE = (30, 30, 30)          # horizontal rules
FAINT = (150, 140, 120)      # footer grey
SKY = (205, 224, 240)        # illustration sky
SLATE = (46, 64, 87)         # skyline buildings
LIT = (250, 214, 110)        # lit windows
SUN = (232, 163, 61)         # sun disc
SEA = (31, 78, 121)          # cyclone blue
LEAF = (31, 120, 70)         # market green

PAGE = 1024
MARGIN = 36
RIGHT = PAGE - MARGIN

LIB = "/usr/share/fonts/truetype/liberation/"
SERIF = LIB + "LiberationSerif-Regular.ttf"
SERIF_BOLD = LIB + "LiberationSerif-Bold.ttf"
SANS = LIB + "LiberationSans-Regular.ttf"
SANS_BOLD = LIB + "LiberationSans-Bold.ttf"

_cache = {}


def typeface(path, size):
    """Load (and memoise) a TrueType face at the requested size."""
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap_lines(pen, text, face, max_w):
    """Greedy word wrap; honours explicit newlines in the source text."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            out.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if pen.textlength(trial, font=face) <= max_w:
                line = trial
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def draw_para(pen, text, face, x, y, max_w, leading, colour=SOFT_INK):
    """Draw wrapped paragraph text; return the y just below the last line."""
    for line in wrap_lines(pen, text, face, max_w):
        pen.text((x, y), line, font=face, fill=colour)
        y += leading
    return y


def kicker(pen, label, x, y, size=19):
    """Small red uppercase section label, e.g. 'GULF · CONFLICT'."""
    face = typeface(SANS_BOLD, size)
    pen.text((x, y), label, font=face, fill=RED)
    return y + size + 8


def headline(pen, text, face, x, y, max_w, leading):
    """Draw a wrapped bold serif headline; return y below it."""
    return draw_para(pen, text, face, x, y, max_w, leading, colour=INK)


def hrule(pen, y, weight=2):
    """A full-width horizontal rule at height y."""
    pen.line([(MARGIN, y), (RIGHT, y)], fill=RULE, width=weight)
    return y + weight


def skyline_scene(pen, x0, y0, x1, y1):
    """A stylised Shenzhen skyline at dusk: pale sky, amber sun, towers
    with lit windows, and a tall spired tower in the middle."""
    pen.rectangle([x0, y0, x1, y1], fill=SKY)
    pen.ellipse([x1 - 78, y0 + 18, x1 - 18, y0 + 78], fill=SUN)
    # (left, width, height) for each tower, tallest near the centre.
    towers = [
        (0.00, 0.13, 0.42), (0.14, 0.10, 0.58), (0.25, 0.12, 0.50),
        (0.38, 0.14, 0.86), (0.53, 0.11, 0.62), (0.65, 0.12, 0.46),
        (0.78, 0.10, 0.66), (0.89, 0.11, 0.54),
    ]
    span = x1 - x0
    base = y1
    for frac_x, frac_w, frac_h in towers:
        bx = x0 + int(frac_x * span)
        bw = int(frac_w * span)
        bh = int(frac_h * (y1 - y0))
        pen.rectangle([bx, base - bh, bx + bw, base], fill=SLATE)
        # Spire on the tallest tower.
        if frac_h > 0.8:
            pen.polygon([(bx + bw // 2 - 8, base - bh),
                         (bx + bw // 2 + 8, base - bh),
                         (bx + bw // 2, base - bh - 34)], fill=SLATE)
        # Lit windows in a loose grid.
        cols = max(1, bw // 16)
        rows = max(1, bh // 22)
        for r in range(rows):
            for c in range(cols):
                if (r * 7 + c * 3) % 4 == 0:
                    wx = bx + 5 + c * 16
                    wy = base - bh + 8 + r * 22
                    pen.rectangle([wx, wy, wx + 6, wy + 8], fill=LIT)


def flag(pen, x, y, w, h, country):
    """Draw a tiny simplified flag: 'us', 'cn' or 'ru'."""
    if country == "us":
        for i in range(13):
            pen.rectangle([x, y + i * h // 13, x + w, y + (i + 1) * h // 13],
                          fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
        pen.rectangle([x, y, x + int(w * 0.4), y + int(h * 0.54)], fill=(60, 59, 110))
        for r in range(5):
            for c in range(6):
                pen.ellipse([x + 4 + c * 7, y + 3 + r * 5,
                             x + 7 + c * 7, y + 6 + r * 5], fill=(255, 255, 255))
    elif country == "cn":
        pen.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        pen.ellipse([x + 6, y + 5, x + 18, y + 17], fill=(255, 222, 0))
        for sx, sy in [(30, 6), (36, 12), (36, 20), (30, 26)]:
            pen.ellipse([x + sx, y + sy, x + sx + 6, y + sy + 6], fill=(255, 222, 0))
    else:  # ru — white over blue over red
        third = h // 3
        pen.rectangle([x, y, x + w, y + third], fill=(255, 255, 255))
        pen.rectangle([x, y + third, x + w, y + 2 * third], fill=(0, 57, 166))
        pen.rectangle([x, y + 2 * third, x + w, y + h], fill=(213, 0, 50))
    pen.rectangle([x, y, x + w, y + h], outline=(120, 110, 95), width=1)


def rising_chart(pen, x0, y0, x1, y1):
    """A small boxed line chart trending upward, left to right."""
    pen.rectangle([x0, y0, x1, y1], outline=(140, 130, 110), width=1)
    pen.line([(x0, y1 - 14), (x1, y1 - 14)], fill=(200, 190, 170), width=1)
    # Hand-picked points: flat, then a steady climb with a small dip.
    pts = [0.78, 0.76, 0.77, 0.72, 0.70, 0.66, 0.60, 0.58,
           0.55, 0.50, 0.44, 0.40, 0.34, 0.30, 0.22, 0.16]
    n = len(pts)
    coords = []
    for i, frac in enumerate(pts):
        px = x0 + 8 + i * (x1 - x0 - 16) // (n - 1)
        py = y0 + 8 + int(frac * (y1 - y0 - 22))
        coords.append((px, py))
    pen.line(coords, fill=LEAF, width=3, joint="curve")
    pen.ellipse([coords[-1][0] - 4, coords[-1][1] - 4,
                 coords[-1][0] + 4, coords[-1][1] + 4], fill=LEAF)


def storm_swirl(pen, cx, cy, outer):
    """Concentric broken arcs suggesting a cyclone seen from above."""
    for ring in range(4):
        r = outer - ring * (outer // 4)
        start = 20 + ring * 55
        pen.arc([cx - r, cy - r, cx + r, cy + r],
                start=start, end=start + 265, fill=SEA, width=5)
    pen.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=SEA, width=4)


def story_column(pen, x, y, width, label, head, deck,
                 head_size=27, head_lead=32, deck_size=20, deck_lead=26):
    """Kicker + headline + deck stacked in one column; return bottom y."""
    y = kicker(pen, label, x, y, size=18)
    y = headline(pen, head, typeface(SERIF_BOLD, head_size),
                 x, y, width, head_lead)
    y += 6
    y = draw_para(pen, deck, typeface(SERIF, deck_size),
                  x, y, width, deck_lead)
    return y


def brief_line(pen, tag, text, y):
    """One brief: red tag on the left, sentence on the right."""
    pen.text((MARGIN, y), tag, font=typeface(SANS_BOLD, 18), fill=RED)
    pen.text((MARGIN + 88, y), text, font=typeface(SERIF, 18), fill=SOFT_INK)
    return y + 22


def build_page():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    pen = ImageDraw.Draw(page)

    # ---------------------------------------------------------- masthead
    name = "THE WORLD TODAY"
    face = typeface(SERIF_BOLD, 68)
    w = pen.textlength(name, font=face)
    pen.text(((PAGE - w) / 2, 12), name, font=face, fill=INK)

    y = 96
    y = hrule(pen, y, weight=4)
    y = hrule(pen, y + 4, weight=1)

    # ---------------------------------------------------------- dateline
    y += 10
    pen.text((MARGIN, y), "THURSDAY 19 NOVEMBER 2026",
             font=typeface(SANS_BOLD, 21), fill=INK)
    tag = "ONE DAY  ·  ONE PICTURE"
    tw = pen.textlength(tag, font=typeface(SANS_BOLD, 21))
    pen.text((RIGHT - tw, y), tag, font=typeface(SANS_BOLD, 21), fill=RED)
    y += 28
    y = hrule(pen, y, weight=1)

    # ---------------------------------------------------------- lead story
    lead_w = 560
    art_x = MARGIN + lead_w + 28
    y_lead = y + 14
    y_lead = kicker(pen, "SHENZHEN  ·  DIPLOMACY", MARGIN, y_lead, size=18)
    y_lead = headline(pen, "TRUMP, XI AND\nPUTIN MEET",
                      typeface(SERIF_BOLD, 50), MARGIN, y_lead, lead_w, 56)
    y_lead += 8
    y_lead = draw_para(
        pen,
        "The leaders of the US, China and Russia sit down together for the "
        "first time \u2014 nuclear arms, Ukraine and the Gulf war on the table.",
        typeface(SERIF, 20), MARGIN, y_lead, lead_w, 26)
    y_lead += 10
    y_lead = draw_para(
        pen,
        "Donald Trump landed in Shenzhen on Wednesday for the APEC summit. "
        "On Thursday he joins Xi Jinping and Vladimir Putin for a three-way "
        "meeting no sitting presidents of the three powers have held before.",
        typeface(SERIF, 20), MARGIN, y_lead, lead_w, 26)

    # Lead illustration: skyline, caption, three flags.
    skyline_scene(pen, art_x, y + 14, RIGHT, y + 180)
    cy = y + 188
    pen.text((art_x, cy), "THREE POWERS, ONE TABLE",
             font=typeface(SANS_BOLD, 18), fill=SOFT_INK)
    fy = cy + 28
    fw, fh = 74, 44
    for i, nation in enumerate(["us", "cn", "ru"]):
        flag(pen, art_x + i * (fw + 14), fy, fw, fh, nation)
    pen.text((art_x, fy + fh + 8), "US  ·  CHINA  ·  RUSSIA",
             font=typeface(SANS_BOLD, 16), fill=INK)

    y = max(y_lead, fy + fh + 34) + 6
    y = hrule(pen, y, weight=2)

    # ---------------------------------------------------------- mid stories
    mid_y = y + 14
    half = (RIGHT - MARGIN - 28) // 2
    left_x = MARGIN
    right_x = MARGIN + half + 28

    bottom_left = story_column(
        pen, left_x, mid_y, half,
        "MARKETS  ·  TECHNOLOGY",
        "NVIDIA DOUBLES TO $115.8BN",
        "Revenue doubled in the first results since Jensen Huang resigned; "
        "interim chief Colette Kress led the call.",
        head_size=26, head_lead=30, deck_size=19, deck_lead=23)
    # Market chart under the Nvidia deck, labelled with the after-hours move.
    pen.text((left_x, bottom_left + 6), "NVIDIA  +3% AFTER HOURS",
             font=typeface(SANS_BOLD, 17), fill=LEAF)
    rising_chart(pen, left_x, bottom_left + 28, left_x + half, bottom_left + 76)

    bottom_right = story_column(
        pen, right_x, mid_y, half,
        "WEATHER  ·  BAY OF BENGAL",
        "CYCLONE AKVAN NEARS INDIA",
        "Red alerts and school closures on India\u2019s east coast as the "
        "severe storm bears down; landfall is due on Friday.",
        head_size=26, head_lead=30, deck_size=19, deck_lead=23)
    storm_swirl(pen, right_x + half - 62, bottom_right + 44, 40)

    y = max(bottom_left + 82, bottom_right + 92) + 8
    y = hrule(pen, y, weight=2)

    # ---------------------------------------------------------- three columns
    col_w = (RIGHT - MARGIN - 56) // 3
    col_y = y + 14
    c1 = MARGIN
    c2 = MARGIN + col_w + 28
    c3 = MARGIN + 2 * (col_w + 28)
    pen.line([(c2 - 14, col_y), (c2 - 14, col_y + 150)], fill=(190, 180, 160), width=1)
    pen.line([(c3 - 14, col_y), (c3 - 14, col_y + 150)], fill=(190, 180, 160), width=1)

    end1 = story_column(
        pen, c1, col_y, col_w,
        "GULF  ·  CONFLICT",
        "IRAN WIDENS STRIKES TO KUWAIT",
        "Iran hit a US base in Kuwait and sites in Bahrain, after US jets "
        "struck Qeshm Island.",
        head_size=24, head_lead=28, deck_size=18, deck_lead=22)
    end2 = story_column(
        pen, c2, col_y, col_w,
        "CULTURE  ·  GAMES",
        "GTA VI ARRIVES AFTER 13 YEARS",
        "Rockstar\u2019s long-awaited game launches today on PlayStation 5 "
        "and Xbox. Metacritic: 99.",
        head_size=24, head_lead=28, deck_size=18, deck_lead=22)
    end3 = story_column(
        pen, c3, col_y, col_w,
        "THE HAGUE  ·  LAW",
        "ICJ RULES ON ROHINGYA CASE",
        "The world court rules today in The Gambia\u2019s case against "
        "Myanmar, seven years on.",
        head_size=24, head_lead=28, deck_size=18, deck_lead=22)

    y = max(end1, end2, end3) + 10
    y = hrule(pen, y, weight=2)

    # ---------------------------------------------------------- briefs
    y += 12
    y = brief_line(pen, "FED",
                   "Fed minutes show most officials expect further interest-rate rises.", y)
    y = brief_line(pen, "SPORT",
                   "Ben Duckett\u2019s 133 puts England on top in the third ODI in Australia.", y)
    y = brief_line(pen, "SPACE",
                   "Voyager 1 reaches one light-day from Earth; NASA confirms it today.", y)

    # ---------------------------------------------------------- footer
    foot = ("Thursday 19 November 2026  ·  All stories reported on "
            "19 November 2026  ·  Drawn, not photographed")
    face = typeface(SANS, 13)
    fw = pen.textlength(foot, font=face)
    pen.text(((PAGE - fw) / 2, PAGE - 18), foot, font=face, fill=FAINT)

    return page


if __name__ == "__main__":
    build_page().save("entry.png", optimize=True)
    print("wrote entry.png")
