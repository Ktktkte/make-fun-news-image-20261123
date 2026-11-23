#!/usr/bin/env python3
"""Draw entry.png for news-image-20261123: newspaper front page, 1024x1024.
All facts verified live 2026-11-23; drawn scenes only, no borrowed photos.
Layout is flow-based: every block starts where the previous one ended."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
TEAL = (14, 94, 90)
GREY = (90, 88, 80)
RULE = (180, 175, 160)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, max_w, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y


def kicker(draw, x, y, label, color):
    draw.text((x, y), label, font=font(SANS_B, 26), fill=color)
    return y + 38


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- Masthead ----------
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((32, 12), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 62), fill=(255, 255, 255))
d.text((32, 76), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 36), fill=GOLD)
d.line([0, 118, W, 118], fill=GOLD, width=4)

# ---------- Hero: Iran war (y 126..520) ----------
hy = 126
d.rectangle([24, hy, 1000, 520], outline=RULE, width=2)
y = kicker(d, 44, hy + 14, "WAR IN THE GULF  •  TOP STORY", RED)
y = text_block(d, 44, y + 4, "IRAN WAR WIDENS", font(SERIF_B, 58), INK, 560, leading=62)
y = text_block(d, 44, y + 8, "Bahrain hit, tankers attacked in the Strait of Hormuz",
               font(SANS_B, 32), INK, 560, leading=40)
y = text_block(d, 44, y + 10, "US bases targeted. Two people hurt in Bahrain. Trump: Iran wants a deal — but not an “acceptable” one.",
               font(SANS, 28), (60, 58, 52), 560, leading=35)

# Hero art: sea, tankers, missile arcs, smoke (right side, inside the panel)
ax0, ay0, ax1, ay1 = 640, hy + 56, 984, 508
d.rectangle([ax0, ay0, ax1, ay1], fill=(38, 68, 96))
d.rectangle([ax0, ay0 + 170, ax1, ay1], fill=(24, 48, 72))
d.ellipse([ax0 + 30, ay0 + 18, ax0 + 110, ay0 + 98], fill=(232, 120, 40))
for cx, cy, r in [(ax0 + 250, ay0 + 38, 44), (ax0 + 282, ay0 + 66, 56), (ax0 + 215, ay0 + 76, 38)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 118))
d.arc([ax0 + 40, ay0 - 40, ax0 + 260, ay0 + 170], start=200, end=340, fill=(255, 220, 120), width=5)
d.arc([ax0 + 120, ay0 - 10, ax0 + 330, ay0 + 190], start=210, end=330, fill=(255, 220, 120), width=5)
for tx in (ax0 + 20, ax0 + 140, ax0 + 252):
    d.rectangle([tx, ay0 + 268, tx + 80, ay0 + 296], fill=(40, 40, 44))
    d.rectangle([tx + 52, ay0 + 246, tx + 68, ay0 + 268], fill=(40, 40, 44))
    d.polygon([(tx + 14, ay0 + 296), (tx + 66, ay0 + 296), (tx + 58, ay0 + 310), (tx + 22, ay0 + 310)],
              fill=(150, 60, 30))

# ---------- Row 2: two panels (y 536..768) ----------
ry = 536
pw = (1000 - 24 - 16) // 2  # 480
# Panel A: COP31
d.rectangle([24, ry, 24 + pw, 768], outline=RULE, width=2)
y = kicker(d, 44, ry + 12, "CLIMATE", TEAL)
y = text_block(d, 44, y + 4, "CLIMATE TALKS COLLAPSE", font(SERIF_B, 38), INK, pw - 40, leading=42)
text_block(d, 44, y + 8, "COP31 ends with no deal — the longest summit ever.",
           font(SANS, 28), (60, 58, 52), pw - 40, leading=35)
# Panel B: Kyiv
bx = 24 + pw + 16
d.rectangle([bx, ry, bx + pw, 768], outline=RULE, width=2)
y = kicker(d, bx + 20, ry + 12, "UKRAINE", RED)
y = text_block(d, bx + 20, y + 4, "KYIV REGION HIT", font(SERIF_B, 38), INK, pw - 40, leading=42)
text_block(d, bx + 20, y + 8, "15 killed in Dymer strikes. Missiles enter Poland; NATO talks called.",
           font(SANS, 28), (60, 58, 52), pw - 40, leading=35)

# ---------- Row 3: three panels (y 784..1000) ----------
ry3 = 784
pw3 = (1000 - 24 - 32) // 3  # 314
panels = [
    ("WAR AT SEA", "RUSSIAN SHIP SUNK",
     "Drones sink the Mercury off Benghazi.", "ship"),
    ("WASHINGTON", "DEMOCRATS TAKE HOUSE",
     "258 seats — biggest majority in decades.", "house"),
    ("MARKETS", "MARKETS RALLY",
     "CrowdStrike buys Zscaler: $43.9B.", "chart"),
]
for i, (kick, head, body, kind) in enumerate(panels):
    x0 = 24 + i * (pw3 + 16)
    d.rectangle([x0, ry3, x0 + pw3, 1000], outline=RULE, width=2)
    y = kicker(d, x0 + 18, ry3 + 10, kick, NAVY)
    y = text_block(d, x0 + 18, y + 2, head, font(SERIF_B, 32), INK, pw3 - 36, leading=36)
    y = text_block(d, x0 + 18, y + 6, body, font(SANS, 24), (60, 58, 52), pw3 - 36, leading=30)
    # small icon strip near the bottom, below the text
    iy = ry3 + 186
    if kind == "ship":
        d.rectangle([x0 + 18, iy + 6, x0 + 118, iy + 18], fill=(40, 40, 44))
        d.rectangle([x0 + 70, iy - 6, x0 + 86, iy + 6], fill=(40, 40, 44))
        d.line([x0 + 18, iy + 22, x0 + 280, iy + 22], fill=(38, 68, 96), width=4)
    elif kind == "house":
        d.rectangle([x0 + 18, iy, x0 + 118, iy + 24], fill=(20, 33, 61))
        d.rectangle([x0 + 130, iy, x0 + 230, iy + 24], fill=(120, 118, 110))
        d.text((x0 + 24, iy + 1), "D 258", font=font(SANS_B, 21), fill=(255, 255, 255))
        d.text((x0 + 136, iy + 1), "4 OPEN", font=font(SANS_B, 21), fill=(255, 255, 255))
    else:
        pts = [(x0 + 18, iy + 18), (x0 + 70, iy + 13), (x0 + 120, iy + 16),
               (x0 + 170, iy + 6), (x0 + 220, iy + 8), (x0 + 270, iy - 1)]
        d.line(pts, fill=(14, 94, 90), width=5)
        d.polygon([(x0 + 270, iy - 1), (x0 + 259, iy + 2), (x0 + 270, iy + 7)], fill=(14, 94, 90))

d.line([24, 1012, 1000, 1012], fill=RULE, width=2)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
