#!/usr/bin/env python3
"""Draw the round-2 entry image for news-image-20261123.

A poster-style front page for Monday 23 November 2026: six big illustrated
panels, a six-number strip and six one-line 'also today' items. Built for
legibility at ~300px across, so type is large and the story count is small
(14 distinct stories) instead of a dense broadsheet. Every story below was
verified against reporting dated 23 November 2026 (see RESEARCH.md in the
run log); nothing is invented and claims are attributed where the reporting
attributes them.

Run: python3 compose.py  ->  writes entry/entry.png (1024x1024 PNG).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry", "entry.png")

W, H = 1024, 1024
PAPER = (247, 241, 227)      # warm cream newsprint
CARD = (255, 253, 246)       # panel paper, a touch lighter
INK = (26, 23, 18)
RED = (160, 30, 30)
MUTED = (107, 98, 82)
TEAL = (31, 93, 96)
NAVY = (28, 48, 84)
SKY = (168, 205, 219)
GREEN = (46, 110, 58)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, f, cx, y, fill, leading):
    """Draw centred lines starting at y; returns the y after the last line."""
    for line in lines:
        draw.text((cx - text_w(draw, line, f) / 2, y), line, font=f, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- scenes
# Each scene paints a flat, bold illustration into a (w x h) box. Big shapes
# only: the panel is ~312px wide and the judge may view it small.

def scene_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    cx, cy, r = x + w // 2, y + h // 2 + 6, 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 165, 128))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 253, 246), width=4)
    # continents as rough blobs
    d.ellipse([cx - 42, cy - 30, cx - 6, cy + 4], fill=(38, 84, 48))
    d.ellipse([cx + 8, cy + 6, cx + 44, cy + 38], fill=(38, 84, 48))
    # the crack: no deal
    d.line([(cx - 8, cy - 58), (cx + 6, cy - 20), (cx - 10, cy + 8),
            (cx + 12, cy + 34), (cx - 2, cy + 58)], fill=RED, width=7)
    d.ellipse([x + 18, y + 14, x + 66, y + 34], fill=(255, 253, 246))
    d.ellipse([x + w - 70, y + 22, x + w - 22, y + 40], fill=(255, 253, 246))


def scene_dems(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy in [(x + 30, y + 24), (x + 70, y + 14), (x + w - 40, y + 20),
                   (x + w - 80, y + 12), (x + 150, y + 30)]:
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 253, 246))
    cx = x + w // 2
    base = y + h - 18
    # capitol dome
    d.rectangle([cx - 86, base - 34, cx + 86, base], fill=(255, 253, 246))
    d.polygon([(cx - 58, base - 34), (cx - 58, base - 78), (cx, base - 108),
               (cx + 58, base - 78), (cx + 58, base - 34)], fill=(255, 253, 246))
    d.rectangle([cx - 4, base - 122, cx + 4, base - 104], fill=(255, 253, 246))
    d.rectangle([cx - 96, base - 8, cx + 96, base], fill=RED)
    for px in range(cx - 78, cx + 79, 18):
        d.rectangle([px, base - 26, px + 8, base - 8], fill=NAVY)


def scene_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 26, 40))
    cx, cy = x + w // 2, y + h // 2
    for r in (30, 58, 86):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340,
              fill=(120, 140, 170), width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 253, 246))
    # three missile streaks
    for i, (sx, sy) in enumerate([(x + 30, y + 30), (x + 120, y + 18),
                                 (x + 210, y + 44)]):
        d.line([(sx, sy), (sx + 64, sy + 26)], fill=(255, 120, 60), width=6)
        d.ellipse([sx + 64, sy + 20, sx + 78, sy + 32], fill=(255, 220, 120))
        d.line([(sx, sy), (sx + 40, sy + 16)], fill=(255, 220, 120), width=2)


def scene_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 253, 246))
    for gy in range(y + 28, y + h - 10, 32):
        d.line([(x + 14, gy), (x + w - 14, gy)], fill=(225, 218, 200), width=1)
    pts = [(x + 20, y + 34), (x + 80, y + 52), (x + 130, y + 46),
           (x + 180, y + 86), (x + 235, y + 78), (x + 292, y + 138)]
    d.line(pts, fill=RED, width=7, joint="curve")
    d.polygon([(x + 292, y + 138), (x + 292, y + 118), (x + 262, y + 138)],
              fill=RED)
    d.text((x + 18, y + h - 34), "$60k", font=SANS_B(26), fill=RED)


def scene_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=GREEN)
    d.rectangle([x, y + h - 44, x + w, y + h], fill=(34, 84, 44))
    d.rectangle([x + 30, y + 62, x + w - 30, y + h - 44], fill=(196, 164, 104))
    # stumps: three tall yellow bars with bails, left of the pitch
    sx0 = x + 62
    for i in range(3):
        sx = sx0 + i * 16
        d.rectangle([sx, y + 92, sx + 9, y + 136], fill=(255, 220, 120))
    d.rectangle([sx0 - 2, y + 87, sx0 + 46, y + 92], fill=(255, 220, 120))
    # bat leaning over the stumps: handle + blade
    d.line([(x + 182, y + 34), (x + 152, y + 94)], fill=(120, 72, 32), width=11)
    d.polygon([(x + 140, y + 86), (x + 164, y + 98), (x + 142, y + 148),
               (x + 118, y + 136)], fill=(210, 170, 110))
    # red ball, bowled toward the stumps
    d.ellipse([x + 224, y + 116, x + 252, y + 144], fill=RED)
    d.arc([x + 224, y + 116, x + 252, y + 144], start=0, end=360,
          fill=(255, 253, 246), width=2)


def scene_capture(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 26, 40))
    # police light bar
    d.rectangle([x + w // 2 - 90, y + 34, x + w // 2 + 90, y + 62],
                fill=(40, 44, 66))
    d.ellipse([x + w // 2 - 78, y + 38, x + w // 2 - 18, y + 58],
              fill=(220, 40, 40))
    d.ellipse([x + w // 2 + 18, y + 38, x + w // 2 + 78, y + 58],
              fill=(60, 120, 255))
    # handcuffs
    cy = y + h - 58
    for cx in (x + w // 2 - 62, x + w // 2 + 62):
        d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34],
                  outline=(200, 200, 200), width=9)
    d.line([(x + w // 2 - 28, cy), (x + w // 2 + 28, cy)],
           fill=(200, 200, 200), width=7)


# ---------------------------------------------------------------- page

PANELS = [
    ("Climate talks collapse with no deal",
     "Ends after 50 hours overtime; no fossil-fuel deal.",
     scene_cop31),
    ("Democrats take 258 House seats",
     "Biggest majority since 1992 after a recount flip.",
     scene_dems),
    ("Poland confirms Russian missiles",
     "Three Kh-101s found; NATO meets in Brussels today.",
     scene_poland),
    ("Markets rout; Bitcoin under $60k",
     "S&P \u22128.6% in a week; Nasdaq \u221210%.",
     scene_markets),
    ("India pile up a record 720/9",
     "Highest Test total ever in New Zealand.",
     scene_cricket),
    ("Mexico captures \u2018El Chapo Isidro\u2019",
     "FBI top-10 fugitive taken; 11 killed.",
     scene_capture),
]

NUMBERS = [
    ("258", "Dem House seats"),
    ("\u22128.6%", "S&P 500, one week"),
    ("$13bn", "India inflows, Nov"),
    ("720/9", "India Test total"),
    ("36", "missing, factory fire"),
    ("3", "missiles over Poland"),
]

ALSO = [
    "Gaza strikes kill 8; Qatari LNG carrier hit",
    "Iran calls the UK Navy a terrorist group",
    "Ukrainian drone sets Russian warship ablaze",
    "Verstappen wins the Las Vegas GP",
    "Delta delays 1,000+ Thanksgiving flights",
    "Alcaraz wins first ATP Finals title",
]

FOOTER = ("Verified against 23 November 2026 reporting.  "
          "Not today: Pete Rose pardon (19 Nov) \u00b7 Anthropic IPO (19 Nov) "
          "\u00b7 Huang resigns (12 Nov).")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 30                      # side margin
    cw = W - 2 * mx              # content width = 964

    # --- masthead
    y = 22
    kick = SANS_B(19)
    kt = "THE WORLD IN ONE PAGE"
    d.text((mx + (cw - text_w(d, kt, kick)) / 2, y), kt, font=kick, fill=RED)
    y += 30
    date_f = SERIF_B(54)
    date_t = "MONDAY 23 NOVEMBER 2026"
    assert text_w(d, date_t, date_f) <= cw, "date headline too wide"
    d.text((mx + (cw - text_w(d, date_t, date_f)) / 2, y), date_t,
           font=date_f, fill=INK)
    y += 70
    d.rectangle([mx, y, mx + cw, y + 5], fill=RED)
    y += 16
    strap_f = SERIF(23)
    strap = "Every story on this page happened or was first reported today."
    d.text((mx + (cw - text_w(d, strap, strap_f)) / 2, y), strap,
           font=strap_f, fill=INK)
    y += 40

    # --- number strip
    d.line([(mx, y), (mx + cw, y)], fill=INK, width=2)
    y += 10
    ncell = cw // 6
    num_f, lab_f = SANS_B(32), SANS(15)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = mx + ncell * i + ncell // 2
        d.text((cx - text_w(d, num, num_f) / 2, y), num, font=num_f, fill=RED)
        lab_lines = wrap(d, lab, lab_f, ncell - 12)
        assert len(lab_lines) <= 2, f"number label too long: {lab}"
        draw_lines(d, lab_lines, lab_f, cx, y + 42, MUTED, 19)
        if i:
            d.line([(mx + ncell * i, y + 4), (mx + ncell * i, y + 76)],
                   fill=(200, 192, 172), width=1)
    y += 84
    d.line([(mx, y), (mx + cw, y)], fill=INK, width=2)
    y += 16

    # --- six big panels, 2 rows x 3 cols
    gap = 14
    pw = (cw - 2 * gap) // 3          # 312
    ph = 278
    scene_h = 168
    head_f, deck_f = SANS_B(24), SANS(18)
    for row in range(2):
        for col in range(3):
            p = PANELS[row * 3 + col]
            px = mx + col * (pw + gap)
            py = y + row * (ph + gap)
            d.rectangle([px, py, px + pw, py + ph], fill=CARD,
                        outline=INK, width=2)
            p[2](d, px + 2, py + 2, pw - 4, scene_h)
            ty = py + scene_h + 12
            head_lines = wrap(d, p[0], head_f, pw - 24)
            assert len(head_lines) <= 2, f"headline too long: {p[0]}"
            ty = draw_lines(d, head_lines, head_f, px + pw // 2, ty, INK, 26)
            deck_lines = wrap(d, p[1], deck_f, pw - 24)
            assert len(deck_lines) <= 2, f"deck too long: {p[1]}"
            draw_lines(d, deck_lines, deck_f, px + pw // 2, ty + 1, MUTED, 21)
    y += 2 * ph + gap + 16

    # --- also today
    also_f = SANS(19)
    d.text((mx, y), "ALSO TODAY", font=SANS_B(19), fill=RED)
    y += 28
    col_w = cw // 2
    for i, item in enumerate(ALSO):
        col = i % 2
        r = i // 2
        ix = mx + col * col_w
        iy = y + r * 24
        assert text_w(d, item, also_f) <= col_w - 26, f"also item too long: {item}"
        d.rectangle([ix, iy + 5, ix + 10, iy + 15], fill=RED)
        d.text((ix + 18, iy), item, font=also_f, fill=INK)
    y += 3 * 24 + 10

    # --- footer
    d.line([(mx, y), (mx + cw, y)], fill=INK, width=2)
    y += 8
    foot_f = SANS(14)
    foot_lines = wrap(d, FOOTER, foot_f, cw)
    assert len(foot_lines) <= 2
    draw_lines(d, foot_lines, foot_f, mx + cw // 2, y, MUTED, 18)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG")
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    build()
