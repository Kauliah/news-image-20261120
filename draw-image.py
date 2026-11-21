#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261120.

One image summing up 20 November 2026's world news: a dark navy masthead
with the date, then six panels (2 columns x 3 rows), each with a small
geometric icon drawn from PIL shapes, a region/field kicker, a bold
two-line headline and a short grey sub-line. Footer states the day.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (245, 240, 230)          # warm off-white
NAVY = (27, 42, 74)           # masthead + headline colour
INK = (27, 42, 74)
GREY = (88, 96, 110)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def fit_font(draw, text, start, min_size, max_w, max_lines=2):
    """Largest bold size (start down to min_size) wrapping to max_lines."""
    for size in range(start, min_size - 1, -1):
        fnt = font(BOLD, size)
        if len(wrap(draw, text, fnt, max_w)) <= max_lines:
            return fnt, size
    return font(BOLD, min_size), min_size


def fit_body(draw, text, start, min_size, max_w, max_lines=4):
    """Largest regular size (start down to min_size) wrapping to max_lines."""
    for size in range(start, min_size - 1, -1):
        fnt = font(REG, size)
        if len(wrap(draw, text, fnt, max_w)) <= max_lines:
            return fnt, size
    return font(REG, min_size), min_size


def draw_spaced(draw, cx, y, text, fnt, fill, spacing=6):
    """Draw text centred on cx with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + spacing
    """Draw text centred on cx with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + spacing


# ---------------------------------------------------------------- icons
def icon_bridge(d, x, y, s, c):
    # Two bridge arches over a river line.
    d.line([(x, y + s * 0.62), (x + s, y + s * 0.62)], fill=c, width=7)
    d.arc([x + s * 0.05, y + s * 0.10, x + s * 0.48, y + s * 0.75],
          180, 360, fill=c, width=7)
    d.arc([x + s * 0.52, y + s * 0.10, x + s * 0.95, y + s * 0.75],
          180, 360, fill=c, width=7)
    d.line([(x + s * 0.50, y + s * 0.05), (x + s * 0.50, y + s * 0.62)],
           fill=c, width=7)
    d.line([(x, y + s * 0.82), (x + s, y + s * 0.82)], fill=c, width=5)
    d.line([(x + s * 0.08, y + s * 0.95), (x + s * 0.92, y + s * 0.95)],
           fill=c, width=5)


def icon_rings(d, x, y, s, c):
    # Two interlocking rings: UK and EU coming together.
    d.ellipse([x, y + s * 0.12, x + s * 0.58, y + s * 0.70],
              outline=c, width=8)
    d.ellipse([x + s * 0.42, y + s * 0.30, x + s, y + s * 0.88],
              outline=(201, 162, 39), width=8)
    d.ellipse([x + s * 0.24, y + s * 0.36, x + s * 0.40, y + s * 0.52],
              fill=c)


def icon_chart(d, x, y, s, c):
    # A falling market line with a down arrow.
    pts = [(x, y + s * 0.15), (x + s * 0.28, y + s * 0.35),
           (x + s * 0.50, y + s * 0.28), (x + s * 0.72, y + s * 0.60),
           (x + s * 0.95, y + s * 0.85)]
    d.line(pts, fill=c, width=8, joint="curve")
    d.polygon([(x + s * 0.95, y + s * 0.85), (x + s * 0.72, y + s * 0.82),
               (x + s * 0.92, y + s * 0.62)], fill=c)
    d.line([(x, y + s * 0.95), (x + s, y + s * 0.95)], fill=c, width=4)


def icon_sun_leaf(d, x, y, s, c):
    # Sun with rays above a leaf: climate talks.
    cx, cy, r = x + s * 0.50, y + s * 0.32, s * 0.20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(201, 162, 39))
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        x1 = cx + math.cos(a) * (r + 4)
        y1 = cy + math.sin(a) * (r + 4)
        x2 = cx + math.cos(a) * (r + s * 0.16)
        y2 = cy + math.sin(a) * (r + s * 0.16)
        d.line([(x1, y1), (x2, y2)], fill=(201, 162, 39), width=5)
    d.pieslice([x + s * 0.12, y + s * 0.58, x + s * 0.88, y + s * 1.02],
               180, 360, fill=c)
    d.line([(x + s * 0.50, y + s * 0.62), (x + s * 0.50, y + s * 0.98)],
           fill=BG, width=4)


def icon_flags(d, x, y, s, c):
    # Two flags on poles: a diplomatic visit.
    d.line([(x + s * 0.18, y + s * 0.05), (x + s * 0.18, y + s * 0.95)],
           fill=c, width=6)
    d.line([(x + s * 0.72, y + s * 0.05), (x + s * 0.72, y + s * 0.95)],
           fill=c, width=6)
    d.polygon([(x + s * 0.18, y + s * 0.08), (x + s * 0.62, y + s * 0.20),
               (x + s * 0.18, y + s * 0.34)], fill=c)
    d.polygon([(x + s * 0.72, y + s * 0.08), (x + s, y + s * 0.22),
               (x + s * 0.72, y + s * 0.38)], fill=(201, 162, 39))
    d.ellipse([x + s * 0.05, y + s * 0.82, x + s * 0.31, y + s * 0.98],
              fill=c)
    d.ellipse([x + s * 0.59, y + s * 0.82, x + s * 0.85, y + s * 0.98],
              fill=(201, 162, 39))


def icon_house(d, x, y, s, c):
    # A simple house under a roof line.
    d.polygon([(x, y + s * 0.45), (x + s * 0.50, y + s * 0.08),
               (x + s, y + s * 0.45)], fill=c)
    d.rectangle([x + s * 0.12, y + s * 0.45, x + s * 0.88, y + s * 0.95],
                fill=c)
    d.rectangle([x + s * 0.42, y + s * 0.66, x + s * 0.58, y + s * 0.95],
                fill=BG)
    d.rectangle([x + s * 0.20, y + s * 0.55, x + s * 0.33, y + s * 0.68],
                fill=BG)


# ---------------------------------------------------------------- panels
PANELS = [
    dict(color=(169, 50, 38), kicker="EUROPE · WAR",
         headline="RUSSIA HITS KYIV BRIDGES, 8 KILLED",
         sub="400 drones and 110 missiles in one of the war's biggest "
             "attacks; Russian weapons also enter Poland.",
         icon=icon_bridge),
    dict(color=(46, 90, 136), kicker="EUROPE · DIPLOMACY",
         headline="UK AND EU AGREE BREXIT RESET",
         sub="Food checks to end, 100,000 youth visas a year, UK back in "
             "Erasmus; deal worth £17bn, London says.",
         icon=icon_rings),
    dict(color=(185, 119, 14), kicker="ASIA · MARKETS",
         headline="ASIAN STOCKS PLUNGE ON AI DOUBTS",
         sub="Nikkei −4.8% to a seven-month low; Kospi −5.3%, Taiwan "
             "−5.6% after Anthropic's debut fails to calm tech fears.",
         icon=icon_chart),
    dict(color=(30, 122, 52), kicker="CLIMATE · ANTALYA",
         headline="COP31 TALKS RUN INTO OVERTIME",
         sub="Antalya summit deadlocks over a draft that drops every "
             "mention of fossil fuels.",
         icon=icon_sun_leaf),
    dict(color=(108, 52, 131), kicker="ASIA · DIPLOMACY",
         headline="PAKISTAN MINISTER VISITS INDIA",
         sub="Musadik Malik lands in New Delhi for an SCO forum, the "
             "first such visit since the May 2025 war.",
         icon=icon_flags),
    dict(color=(74, 101, 114), kicker="MIDDLE EAST · WAR",
         headline="SIX KILLED IN GAZA STRIKES",
         sub="Israeli attacks hit central Gaza despite the ceasefire, as "
             "the UN warns winter floods deepen the crisis.",
         icon=icon_house),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, W, 128], fill=NAVY)
    f_date = font(BOLD, 68)
    d.text((W / 2, 12), "20 NOVEMBER 2026", font=f_date, fill=WHITE,
           anchor="ma")
    f_sub = font(REG, 24)
    draw_spaced(d, W / 2, 92, "FRIDAY · THE WORLD IN ONE IMAGE",
                f_sub, (170, 190, 220), spacing=7)

    # Grid: 2 columns x 3 rows.
    gx, gy = 16, 142
    gw, gh, gap = 490, 272, 10
    f_kick = font(BOLD, 19)

    for i, p in enumerate(PANELS):
        col, row = i % 2, i // 2
        x0 = gx + col * (gw + gap)
        y0 = gy + row * (gh + gap)
        c = p["color"]

        d.rectangle([x0, y0, x0 + gw, y0 + gh], fill=CARD,
                    outline=(210, 203, 188), width=2)
        d.rectangle([x0, y0, x0 + gw, y0 + 8], fill=c)

        # Icon on the left.
        p["icon"](d, x0 + 20, y0 + 30, 88, c)

        # Text block on the right.
        tx = x0 + 122
        tw = gw - 122 - 16
        d.text((tx, y0 + 26), p["kicker"], font=f_kick, fill=c)
        f_head, head_size = fit_font(d, p["headline"], 32, 26, tw)
        lines = wrap(d, p["headline"], f_head, tw)
        hy = y0 + 56
        for ln in lines:
            d.text((tx, hy), ln, font=f_head, fill=INK)
            hy += head_size + 7
        f_body, body_size = fit_body(d, p["sub"], 21, 18, tw)
        sub_lines = wrap(d, p["sub"], f_body, tw)
        sy = hy + 8
        for ln in sub_lines:
            d.text((tx, sy), ln, font=f_body, fill=GREY)
            sy += body_size + 5

    # Footer.
    f_foot = font(REG, 20)
    d.text((W / 2, 992), "Every story above happened or was first reported "
           "on 20 November 2026.", font=f_foot, fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
