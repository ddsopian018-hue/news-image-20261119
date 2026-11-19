#!/usr/bin/env python3
"""Draw the front page for Thursday 19 November 2026.

A newspaper-style summary of the day's world news, drawn entirely with
PIL shapes and text: no photos, no network. Run: python3 draw.py
Writes entry.png (1024x1024, under 1 MiB) next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (17, 17, 17)
RED = (176, 42, 32)
BLUE = (31, 78, 121)
GREEN = (28, 110, 60)
GREY = (90, 90, 86)
LIGHT = (233, 226, 208)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped text; return y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, text, color=RED):
    draw.text((x, y), text, font=font(SANSB, 19), fill=color)
    return y + 26


def rule(draw, y, x0=36, x1=988, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def flag_us(draw, x, y, w=62, h=40):
    for i in range(7):
        draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([x, y, x + int(w * 0.42), y + int(h * 0.55)], fill=(30, 50, 110))
    for r in range(3):
        for c in range(4):
            draw.ellipse([x + 4 + c * 8, y + 4 + r * 7, x + 7 + c * 8, y + 7 + r * 7],
                         fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_cn(draw, x, y, w=62, h=40):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    # one large star + four small stars, simplified
    cx, cy = x + 13, y + 11
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 222, 0))
    for sx, sy in [(34, 6), (42, 12), (42, 22), (34, 28)]:
        draw.ellipse([x + sx - 3, y + sy - 3, x + sx + 3, y + sy + 3],
                     fill=(255, 222, 0))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_ru(draw, x, y, w=62, h=40):
    draw.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
    draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def skyline(draw, x0, y0, x1, y1):
    """Shenzhen skyline at dusk with a sun."""
    draw.rectangle([x0, y0, x1, y1], fill=(214, 226, 236))
    draw.ellipse([x1 - 78, y0 + 12, x1 - 28, y0 + 62], fill=(232, 170, 60))
    # buildings, one tall tower with a spire
    heights = [0.42, 0.66, 0.52, 0.88, 0.58, 0.72, 0.46, 0.62]
    bw = (x1 - x0) // len(heights)
    for i, frac in enumerate(heights):
        bx = x0 + i * bw + 2
        top = y1 - int((y1 - y0) * frac)
        draw.rectangle([bx, top, bx + bw - 4, y1], fill=(52, 74, 96))
        if i == 3:
            draw.polygon([(bx + 8, top), (bx + bw // 2, top - 26),
                          (bx + bw - 12, top)], fill=(52, 74, 96))
        for wy in range(top + 10, y1 - 8, 16):
            for wx in range(bx + 6, bx + bw - 10, 12):
                draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(240, 220, 130))
    draw.rectangle([x0, y1 - 4, x1, y1], fill=(52, 74, 96))


def cyclone(draw, cx, cy, r):
    """Spiral storm: nested arcs in storm blue."""
    for k in range(5):
        rr = r - k * (r // 5)
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr],
                 start=40 + k * 55, end=300 + k * 55, fill=(31, 78, 121), width=5)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(248, 243, 230),
                 outline=(31, 78, 121), width=3)


def chart(draw, x0, y0, x1, y1):
    """Rising market line, green, with grid and axes."""
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=GREY, width=1)
    hh = y1 - y0
    for gy in (y0 + hh * 0.35, y0 + hh * 0.6, y0 + hh * 0.85):
        draw.line([(x0, gy), (x1, gy)], fill=(220, 220, 215), width=1)
    xs = [x0 + 8 + i * (x1 - x0 - 16) // 7 for i in range(8)]
    ys = [y0 + hh * f for f in (0.88, 0.82, 0.84, 0.72, 0.66, 0.58, 0.60, 0.50)]
    pts = list(zip(xs, ys))
    draw.line(pts, fill=GREEN, width=3, joint="curve")
    draw.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
                 fill=GREEN)
    draw.text((x0 + 8, y0 + 4), "NVIDIA  +3% AFTER HOURS", font=font(SANSB, 15),
              fill=GREEN)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.text((W // 2, 26), "THE WORLD TODAY", font=font(SERIF, 66),
           fill=INK, anchor="ma")
    rule(d, 104, width=3)
    d.text((36, 114), "THURSDAY 19 NOVEMBER 2026",
           font=font(SANSB, 21), fill=INK)
    d.text((988, 114), "ONE DAY  ·  ONE PICTURE",
           font=font(SANSB, 21), fill=RED, anchor="ra")
    rule(d, 142, width=2)

    # ---- Lead story: Trump-Xi-Putin in Shenzhen ----
    y = 156
    y = kicker(d, 36, y, "SHENZHEN  ·  DIPLOMACY")
    for ln in wrap(d, "TRUMP, XI AND PUTIN MEET", font(SERIF, 46), 590):
        d.text((36, y), ln, font=font(SERIF, 46), fill=INK)
        y += 54
    y += 6
    y = para(d, 36, y,
             "The leaders of the US, China and Russia sit down together "
             "for the first time — nuclear arms, Ukraine and the Gulf "
             "war on the table.",
             font(SANS, 21), 560, 27)
    y += 6
    y = para(d, 36, y,
             "Donald Trump landed in Shenzhen on Wednesday for the APEC "
             "summit. On Thursday he joins Xi Jinping and Vladimir "
             "Putin for a three-way meeting no sitting presidents of "
             "the three powers have held before.",
             font(SANS, 19), 560, 25)
    # illustration: skyline + three flags
    ix0, iy0, ix1, iy1 = 640, 158, 988, 330
    skyline(d, ix0, iy0, ix1, iy1)
    d.text((ix0, iy1 + 10), "THREE POWERS, ONE TABLE",
           font=font(SANSB, 16), fill=GREY)
    fx, fy = ix0, iy1 + 36
    for fn in (flag_us, flag_cn, flag_ru):
        fn(d, fx, fy)
        fx += 74
    d.text((ix0, fy + 48), "US  ·  CHINA  ·  RUSSIA",
           font=font(SANSB, 15), fill=INK)

    rule(d, 494, width=2)

    # ---- Row 2: Nvidia + cyclone ----
    y = 510
    # left: Nvidia
    y = kicker(d, 36, y, "MARKETS  ·  TECHNOLOGY")
    for ln in wrap(d, "NVIDIA DOUBLES TO $115.8BN", font(SERIF, 24), 460):
        d.text((36, y), ln, font=font(SERIF, 24), fill=INK)
        y += 30
    by = y + 6
    by = para(d, 36, by,
              "Revenue doubled in the first results since Jensen Huang "
              "resigned; interim chief Colette Kress led the call.",
              font(SANS, 18), 440, 23)
    chart(d, 36, by + 6, 480, 712)
    # right: cyclone
    y2 = 510
    y2 = kicker(d, 524, y2, "WEATHER  ·  BAY OF BENGAL")
    d.text((524, y2), "CYCLONE AKVAN NEARS INDIA", font=font(SERIF, 23), fill=INK)
    cy = y2 + 30
    cy = para(d, 524, cy,
              "Red alerts and school closures on India's east coast as "
              "the severe storm bears down; landfall is due on Friday.",
              font(SANS, 18), 300, 24)
    cyclone(d, 908, 640, 56)

    rule(d, 724, width=2)

    # ---- Row 3: three stories ----
    cols = [
        (36, "GULF  ·  CONFLICT", "IRAN WIDENS STRIKES TO KUWAIT",
         "Iran hit a US base in Kuwait and sites in Bahrain, after "
         "US jets struck Qeshm Island."),
        (362, "CULTURE  ·  GAMES", "GTA VI ARRIVES AFTER 13 YEARS",
         "Rockstar's long-awaited game launches today on PlayStation "
         "5 and Xbox. Metacritic: 99."),
        (688, "THE HAGUE  ·  LAW", "ICJ RULES ON ROHINGYA CASE",
         "The world court rules today in The Gambia's case against "
         "Myanmar, seven years on."),
    ]
    for x, kick, head, body in cols:
        yy = 738
        yy = kicker(d, x, yy, kick)
        for ln in wrap(d, head, font(SERIF, 23), 288):
            d.text((x, yy), ln, font=font(SERIF, 23), fill=INK)
            yy += 29
        yy += 6
        para(d, x, yy, body, font(SANS, 16), 288, 21)
        if x < 688:
            d.line([(x + 300, 738), (x + 300, 900)], fill=(200, 192, 172), width=1)

    rule(d, 912, width=2)

    # ---- Briefs strip ----
    by = 926
    d.text((36, by), "FED", font=font(SANSB, 17), fill=RED)
    d.text((118, by), "Fed minutes show most officials expect further interest-rate rises.",
           font=font(SANS, 17), fill=INK)
    by += 28
    d.text((36, by), "SPORT", font=font(SANSB, 17), fill=RED)
    d.text((118, by), "Ben Duckett's 133 puts England on top in the third ODI in Australia.",
           font=font(SANS, 17), fill=INK)
    by += 28
    d.text((36, by), "SPACE", font=font(SANSB, 17), fill=RED)
    d.text((118, by), "Voyager 1 reaches one light-day from Earth; NASA confirms it today.",
           font=font(SANS, 17), fill=INK)

    d.text((W // 2, 1004), "Thursday 19 November 2026  ·  All stories reported on 19 November 2026  ·  Drawn, not photographed",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
