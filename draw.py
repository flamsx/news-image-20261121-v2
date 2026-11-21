#!/usr/bin/env python3
"""Draw the Saturday 21 November 2026 world-news front page.

Fresh build for news-image-20261121 v2. Renders one 1024x1024 PNG
(entry.png) with PIL only. Deterministic: no randomness, no clock,
no network. Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(HERE, "fonts", "Lexend.ttf")
W, H = 1024, 1024

PAPER = (247, 241, 227)
INK = (22, 22, 22)
RED = (178, 38, 28)
NAVY = (26, 42, 74)
TEAL = (14, 106, 90)
GOLD = (172, 120, 26)
GREY = (96, 90, 78)
SEA = (196, 219, 228)
LAND = (231, 213, 176)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
SKY = (16, 24, 54)

_fonts = {}


def F(weight, size):
    key = (weight, size)
    if key not in _fonts:
        f = ImageFont.truetype(FONT_PATH, size)
        f.set_variation_by_axes([weight])
        _fonts[key] = f
    return _fonts[key]


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(d, x, y, text, font, fill, track=-3):
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += d.textlength(ch, font=font) + track
    return cx - x


def fit_size(d, text, weight, start, max_w):
    size = start
    while size > 40 and d.textlength(text, font=F(weight, size)) > max_w:
        size -= 2
    return size


# ---------------------------------------------------------------- data
STATS = [
    ("3", "missiles downed over Riyadh"),
    ("146", "people safe after Davao jet landing"),
    ("6.7", "Peru quake magnitude"),
    ("$7.25bn", "Roundup settlement approved"),
    ("600", "women killed in South Africa in 3 months"),
    ("19\u00bd", "years in US Sikh plot case"),
]

# num, kicker, headline, body, source, accent, illustration
CARDS = [
    (1, "RIYADH \u2022 WAR",
     "Three missiles downed over Riyadh",
     "The Saudi-led coalition says three ballistic missiles fired at the "
     "capital early today were destroyed.",
     "Al Jazeera", NAVY, "riyadh"),
    (2, "KYIV \u2022 WAR",
     "Russia strikes Kyiv again at dawn",
     "A fresh missile attack set two homes ablaze in the Podil district "
     "before dawn today, Kyiv officials say.",
     "Kyiv Post", RED, "kyiv"),
    (3, "ANTALYA \u2022 CLIMATE",
     "Climate talks run into overtime",
     "COP31 missed its Friday close with no deal. A third draft is due "
     "today; the text drops fossil fuels.",
     "Al Jazeera, AP", TEAL, "cop"),
    (4, "JUN\u00cdN \u2022 QUAKE",
     "Magnitude 6.7 quake shakes Peru",
     "The quake struck at 00:09 GMT, felt in Lima. Peru\u2019s institute "
     "reports no deaths and no tsunami risk.",
     "USGS", GOLD, "quake"),
    (5, "WELLINGTON \u2022 CRICKET",
     "Rahul hits a century in Wellington",
     "First Indian opener with Test tons in all four SENA countries. "
     "India 344 for 2 at tea, replying to 368.",
     "IANS", (34, 110, 58), "cricket"),
    (6, "WASHINGTON \u2022 TECHNOLOGY",
     "Trump vows tax on data centres abroad",
     "The president threatens penalties for US firms building AI data "
     "centres overseas.",
     "AP, BBC", NAVY, "datacentre"),
    (7, "KYIV \u2022 DIPLOMACY",
     "Zelensky calls Putin a killer",
     "Ukraine\u2019s president hit back after Donald Trump called the "
     "Russian leader a friend.",
     "BBC", (36, 72, 140), "podium"),
    (8, "COPENHAGEN \u2022 SECURITY",
     "Denmark accuses Russia of murder plot",
     "Danish authorities say Russia plotted to kill a US-Ukrainian "
     "rapper on Danish soil.",
     "BBC, AP", (12, 84, 96), "magnifier"),
]

# num, text (city + headline + short source)
BRIEFS = [
    (9, "Davao \u2014 Air Niugini jet lands safely after engine-fire alert (CAAP)"),
    (10, "Warsaw \u2014 NATO chief Rutte heads here for talks today (BBC)"),
    (11, "New York \u2014 Mamdani plans to close Rikers Island by 2032 (BBC)"),
    (12, "New York \u2014 19\u00bd years in Sikh murder plot case (AP)"),
    (13, "The Hague \u2014 Sanctions urged after Myanmar genocide ruling (AP)"),
    (14, "Jericho \u2014 Woman, 72, shot dead in settler clashes (AP)"),
    (15, "Washington \u2014 Trump seeks a \u201creal deal\u201d with Iran (AP)"),
    (16, "Washington \u2014 Trump warns on China\u2019s nuclear build-up (AP)"),
    (17, "Paris \u2014 de Villepin launches French presidential bid (AP)"),
    (18, "Sydney \u2014 Man charged over car-bomb plot (AP)"),
    (19, "Seoul \u2014 First cholera case in 10 years (AP)"),
    (20, "London \u2014 US declassifies more UFO footage (BBC)"),
    (21, "Los Angeles \u2014 Palisades fire starter convicted (BBC)"),
    (22, "Missouri \u2014 $7.25bn Roundup settlement approved (BBC)"),
    (23, "Johannesburg \u2014 ANC fights to hold key cities (BBC)"),
    (24, "Johannesburg \u2014 600 women killed in three months (BBC)"),
    (25, "Buenos Aires \u2014 Milei moves to end primaries (Buenos Aires Times)"),
    (26, "Bras\u00edlia \u2014 Bolsonaro in hospital with abdominal pain (AP)"),
    (27, "Antalya \u2014 EU warns talks risk a \u201cfossil summit\u201d (Al Jazeera)"),
    (28, "Paris \u2014 Police sentenced over Zecler beating (BBC)"),
    (29, "London \u2014 Britain seeks closer EU ties, minister says (BBC)"),
    (30, "Kryvyi Rih \u2014 City hit again overnight; drone fire (Ukrinform)"),
    (31, "Turin \u2014 Medvedev meets Zverev in semi-final tonight (ATP)"),
    (32, "Las Vegas \u2014 Grand Prix grid decided tonight (Formula 1)"),
    (33, "Hong Kong \u2014 Satwik-Chirag exit Open semi-finals (MyKhel)"),
    (34, "London \u2014 AI \u201csolved maths\u2019 greatest riddle\u201d, lab says (AFP)"),
    (35, "Munich \u2014 Bayern confirm Kane out for months (BBC)"),
    (36, "Mercury \u2014 BepiColombo due to reach Mercury tonight (ESA)"),
    (37, "Washington \u2014 Trump floats chief of staff for 2028 (AP)"),
    (38, "London \u2014 Cost-of-living protests sweep Europe (BBC)"),
]

PINS = {  # card number -> (lon, lat)
    1: (46.7, 24.7), 2: (30.5, 50.5), 3: (30.7, 36.9), 4: (-76.0, -11.0),
    5: (174.8, -41.3), 6: (-77.0, 38.9), 7: (32.0, 49.0), 8: (12.6, 55.7),
}
PIN_DISPLAY = {3: (24.0, 33.0), 7: (40.0, 46.0)}  # nudge apart, leader line to true spot
DOTS = [  # brief cities (lon, lat)
    (125.6, 7.1), (21.0, 52.2), (-74.0, 40.7), (4.3, 52.1), (35.5, 31.9),
    (2.35, 48.9), (151.2, -33.9), (127.0, 37.5), (-0.1, 51.5), (-118.2, 34.1),
    (28.0, -26.2), (-58.4, -34.6), (-47.9, -15.8), (33.4, 47.9), (7.7, 45.1),
    (-115.1, 36.2), (114.2, 22.3), (11.6, 48.1), (-92.5, 38.5),
]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-95, 80), (-80, 73), (-65, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 30), (-90, 21),
     (-95, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-168, 66)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-40, -10), (-35, -15),
     (-40, -25), (-50, -30), (-60, -35), (-65, -45), (-70, -55),
     (-75, -50), (-75, -35), (-80, -20), (-80, -5), (-80, 10)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29),
     (25, -34), (18, -35), (12, -18), (8, 4), (-8, 5), (-17, 15)],
    [(30, 70), (45, 68), (60, 70), (80, 73), (100, 76), (120, 73),
     (140, 72), (160, 70), (178, 65), (170, 60), (160, 55), (150, 50),
     (140, 45), (130, 42), (127, 40), (122, 38), (120, 30), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 10),
     (75, 8), (70, 20), (65, 25), (60, 25), (55, 26), (50, 28), (48, 30),
     (45, 30), (40, 35), (35, 36), (30, 36), (30, 42), (35, 45),
     (40, 50), (45, 55), (50, 60), (45, 65), (40, 68), (30, 70)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68),
     (45, 60), (40, 50), (35, 45), (30, 42), (28, 40), (23, 36),
     (19, 40), (12, 44), (8, 44), (3, 42), (-2, 37), (-9, 37), (-10, 36)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)],
]


# ---------------------------------------------------------------- pictures
def burst(d, cx, cy, r, fill):
    for a in range(0, 360, 30):
        import math
        x2 = cx + r * math.cos(math.radians(a))
        y2 = cy + r * math.sin(math.radians(a))
        d.line([(cx, cy), (x2, y2)], fill=fill, width=3)
    d.ellipse([cx - r // 3, cy - r // 3, cx + r // 3, cy + r // 3], fill=fill)


def illo(d, kind, x, y, w, h):
    if kind == "riyadh":
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        for bx, bw, bh in [(0, 26, 34), (30, 18, 46), (52, 30, 28), (86, 20, 52),
                           (110, 26, 36), (140, 18, 44), (162, 28, 30), (194, 22, 48)]:
            d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(8, 12, 30))
            for wy in range(y + h - bh + 5, y + h - 4, 9):
                for wx in range(x + bx + 4, x + bx + bw - 3, 8):
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        for sx, sy in [(28, 14), (120, 10), (196, 18)]:
            burst(d, x + sx, y + sy, 9, (255, 196, 66))
        d.line([(x + 20, y + 46), (x + 60, y + 22), (x + 100, y + 30)],
               fill=(255, 214, 90), width=2)
    elif kind == "kyiv":
        d.rectangle([x, y, x + w, y + h], fill=(58, 44, 66))
        d.rectangle([x, y + h - 22, x + w, y + h], fill=(24, 20, 30))
        for bx, bw in [(8, 30), (44, 22), (72, 34), (112, 24), (142, 30), (178, 26)]:
            d.rectangle([x + bx, y + h - 22 - 26, x + bx + bw, y + h - 22],
                        fill=(16, 14, 22))
        burst(d, x + 118, y + 26, 16, (255, 122, 40))
        d.ellipse([x + 108, y + 16, x + 128, y + 36], fill=(255, 190, 80))
    elif kind == "cop":
        d.rectangle([x, y, x + w, y + h], fill=(214, 238, 226))
        d.ellipse([x + 12, y + 8, x + 76, y + 56], fill=(46, 130, 190))
        d.ellipse([x + 26, y + 18, x + 44, y + 32], fill=(90, 190, 120))
        d.ellipse([x + 46, y + 34, x + 62, y + 48], fill=(90, 190, 120))
        d.rectangle([x + 92, y + 12, x + 100, y + 44], fill=(220, 60, 40))
        d.ellipse([x + 86, y + 40, x + 106, y + 58], fill=(220, 60, 40))
        d.ellipse([x + 128, y + 10, x + 172, y + 54], outline=INK, width=3)
        d.line([(x + 150, y + 32), (x + 150, y + 18)], fill=INK, width=3)
        d.line([(x + 150, y + 32), (x + 162, y + 38)], fill=INK, width=3)
    elif kind == "quake":
        d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
        d.polygon([(x + 8, y + h), (x + 48, y + 14), (x + 88, y + h)],
                  fill=(150, 110, 70))
        d.polygon([(x + 70, y + h), (x + 120, y + 22), (x + 170, y + h)],
                  fill=(120, 86, 52))
        pts = [(x + 4, y + 34), (x + 30, y + 34), (x + 42, y + 18),
               (x + 54, y + 48), (x + 66, y + 26), (x + 78, y + 40),
               (x + 96, y + 14), (x + 108, y + 44), (x + 122, y + 30),
               (x + 150, y + 30), (x + 162, y + 12), (x + 174, y + 46),
               (x + 190, y + 34), (x + 212, y + 34)]
        d.line(pts, fill=RED, width=3)
    elif kind == "cricket":
        d.rectangle([x, y, x + w, y + h], fill=(52, 130, 72))
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(34, 96, 52))
        d.rectangle([x + 96, y + 14, x + 122, y + 52], fill=(222, 184, 120))
        d.rectangle([x + 100, y + 10, x + 118, y + 16], fill=(222, 184, 120))
        d.line([(x + 150, y + 52), (x + 178, y + 52)], fill=WHITE, width=3)
        d.line([(x + 154, y + 52), (x + 154, y + 40)], fill=WHITE, width=3)
        d.line([(x + 164, y + 52), (x + 164, y + 40)], fill=WHITE, width=3)
        d.line([(x + 174, y + 52), (x + 174, y + 40)], fill=WHITE, width=3)
        d.ellipse([x + 28, y + 18, x + 44, y + 34], fill=RED)
        d.ellipse([x + 186, y + 12, x + 198, y + 24], fill=WHITE)
    elif kind == "datacentre":
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        for i, bx in enumerate([14, 66, 118, 170]):
            d.rectangle([x + bx, y + 10, x + bx + 34, y + h - 8], fill=(38, 58, 96))
            for ry in range(y + 16, y + h - 12, 11):
                d.rectangle([x + bx + 5, ry, x + bx + 29, ry + 5],
                            fill=(90, 220, 160) if i % 2 == 0 else (255, 214, 90))
        d.rectangle([x + 84, y + 4, x + 134, y + 30], fill=RED)
        d.text((x + 92, y + 6), "AI", font=F(800, 18), fill=WHITE)
    elif kind == "podium":
        d.rectangle([x, y, x + w, y + h], fill=(36, 72, 140))
        d.rectangle([x, y, x + w // 2, y + h], fill=(38, 92, 180))
        d.rectangle([x + w // 2, y, x + w, y + h], fill=(250, 204, 0))
        d.rectangle([x + 78, y + 34, x + 138, y + h], fill=(70, 48, 30))
        d.ellipse([x + 98, y + 8, x + 118, y + 28], fill=(232, 190, 150))
        d.rectangle([x + 92, y + 26, x + 124, y + 38], fill=(30, 30, 30))
        d.line([(x + 92, y + 30), (x + 76, y + 18)], fill=INK, width=3)
        d.ellipse([x + 70, y + 12, x + 80, y + 22], fill=INK)
    elif kind == "magnifier":
        d.rectangle([x, y, x + w, y + h], fill=(12, 84, 96))
        d.ellipse([x + 58, y + 6, x + 128, y + 56], outline=WHITE, width=5)
        d.line([(x + 112, y + 46), (x + 152, y + 62)], fill=WHITE, width=6)
        d.text((x + 82, y + 14), "?", font=F(800, 30), fill=WHITE)
        d.ellipse([x + 150, y + 8, x + 168, y + 26], fill=(255, 214, 90))
        d.ellipse([x + 30, y + 38, x + 48, y + 56], fill=(255, 214, 90))


# ---------------------------------------------------------------- build
def draw_card(d, x, y, w, h, num, kicker, headline, body, source, accent, kind):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=(200, 192, 172))
    d.rectangle([x, y, x + w, y + 21], fill=accent)
    d.text((x + 8, y + 3), str(num), font=F(800, 13), fill=WHITE)
    d.text((x + 26, y + 3), kicker, font=F(700, 12), fill=WHITE)
    illo(d, kind, x + 4, y + 25, w - 8, 58)
    hy = y + 88
    for i, ln in enumerate(wrap(d, headline, F(800, 19), w - 16)[:2]):
        d.text((x + 8, hy + i * 23), ln, font=F(800, 19), fill=INK)
    by = hy + 48
    for i, ln in enumerate(wrap(d, body, F(400, 12), w - 16)[:3]):
        d.text((x + 8, by + i * 15), ln, font=F(400, 12), fill=(52, 48, 40))
    d.text((x + 8, y + h - 15), "Source: " + source, font=F(600, 10),
           fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 28
    CW = W - 2 * MX

    # top bar
    d.text((MX, 6), "THE WORLD IN ONE DAY", font=F(800, 14), fill=RED)
    right = "38 STORIES \u2022 6 CONTINENTS"
    d.text((W - MX - d.textlength(right, font=F(700, 14)), 6), right,
           font=F(700, 14), fill=INK)
    d.line([(MX, 26), (W - MX, 26)], fill=INK, width=2)

    # giant date
    date = "Saturday 21 November 2026"
    size = fit_size(d, date, 800, 76, CW)
    tw = tracked(d, MX, 34, date, F(800, size), INK, track=-3)
    # centre it
    img2 = Image.new("RGB", (W, H), PAPER)
    d2 = ImageDraw.Draw(img2)
    d2.text((MX, 6), "THE WORLD IN ONE DAY", font=F(800, 14), fill=RED)
    d2.text((W - MX - d2.textlength(right, font=F(700, 14)), 6), right,
            font=F(700, 14), fill=INK)
    d2.line([(MX, 26), (W - MX, 26)], fill=INK, width=2)
    x0 = MX + max(0, (CW - tw) // 2)
    tracked(d2, x0, 34, date, F(800, size), INK, track=-3)
    d = d2
    img = img2
    y = 34 + size + 8

    # subhead
    sub = ("Missiles downed over Riyadh \u2022 Quake shakes Peru \u2022 "
           "Climate talks run past deadline")
    d.text((MX, y), sub, font=F(500, 18), fill=(64, 58, 48))
    y += 30
    d.line([(MX, y), (W - MX, y)], fill=INK, width=1)
    y += 8

    # stat strip
    sw = (CW - 5 * 6) // 6
    for i, (num, label) in enumerate(STATS):
        sx = MX + i * (sw + 6)
        d.rectangle([sx, y, sx + sw, y + 66], fill=WHITE,
                    outline=(200, 192, 172))
        d.rectangle([sx, y, sx + sw, y + 4], fill=RED)
        d.text((sx + 8, y + 7), num, font=F(800, 30),
               fill=RED if i % 2 == 0 else NAVY)
        for j, ln in enumerate(wrap(d, label, F(500, 11), sw - 16)[:2]):
            d.text((sx + 8, y + 39 + j * 13), ln, font=F(500, 11), fill=GREY)
    y += 74

    # cards: 4 x 2
    cw = (CW - 3 * 10) // 4
    ch = 200
    for r in range(2):
        for c in range(4):
            card = CARDS[r * 4 + c]
            draw_card(d, MX + c * (cw + 10), y + r * (ch + 8), cw, ch,
                      card[0], card[1], card[2], card[3], card[4], card[5],
                      card[6])
    y += 2 * ch + 8 + 10

    # briefs
    d.text((MX, y), "ALSO ON SATURDAY 21 NOVEMBER \u2014 30 MORE STORIES",
           font=F(800, 16), fill=RED)
    y += 24
    bw = (CW - 16) // 2
    for col in range(2):
        for row in range(15):
            b = BRIEFS[col * 15 + row]
            bx = MX + col * (bw + 16)
            by = y + row * 15
            d.text((bx, by), str(b[0]), font=F(800, 13), fill=RED)
            txt = b[1]
            while (d.textlength(txt, font=F(400, 13)) > bw - 26 and len(txt) > 4):
                txt = txt[:-2]
            if txt != b[1]:
                txt = txt.rstrip() + "\u2026"
            d.text((bx + 24, by), txt, font=F(400, 13), fill=INK)
    y += 15 * 15 + 8

    # map
    d.text((MX, y), "WHERE IT HAPPENED", font=F(800, 16), fill=RED)
    d.text((W - MX - d.textlength("Red pins mark the eight lead stories",
                                   font=F(500, 11)), y + 3),
           "Red pins mark the eight lead stories", font=F(500, 11), fill=GREY)
    y += 22
    mh = 1024 - y - 22
    d.rectangle([MX, y, W - MX, y + mh], fill=SEA, outline=(200, 192, 172))

    def proj(lon, lat):
        px = MX + (lon + 180) / 360 * CW
        py = y + (72 - lat) / 132 * mh
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lo, la) for lo, la in poly], fill=LAND,
                  outline=(190, 170, 130))
    for lon, lat in DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=TEAL)
    for num, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        if num in PIN_DISPLAY:
            dx, dy = proj(*PIN_DISPLAY[num])
            d.line([(px, py), (dx, dy)], fill=RED, width=1)
            px, py = dx, dy
        d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED,
                  outline=WHITE, width=2)
        t = str(num)
        d.text((px - d.textlength(t, font=F(800, 12)) / 2, py - 8), t,
               font=F(800, 12), fill=WHITE)
    y += mh + 6

    # footer
    foot = ("Every story here happened, or was first reported, on Saturday "
            "21 November 2026. Sources named beside each story. "
            "Original drawings.")
    d.text((MX, y), foot, font=F(400, 11), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
