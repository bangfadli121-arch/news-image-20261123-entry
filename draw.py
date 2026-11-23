#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026.

Everything here is drawn from scratch in this session with Pillow
vector shapes and system fonts. No photos, no network, no copied art.
The image is 1024x1024 and fully deterministic.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette -------------------------------------------------------------
PAPER   = (246, 241, 231)   # warm newsprint
INK     = (26, 26, 26)
RED     = (179, 38, 30)     # newspaper red
DARKRED = (140, 28, 22)
BLUE    = (30, 79, 143)
NAVY    = (24, 38, 64)
GOLD    = (201, 162, 39)
LGREY   = (232, 226, 212)   # light panel
MGREY   = (210, 203, 188)
WHITE   = (255, 255, 255)
SKY     = (178, 214, 235)
SEA     = (120, 170, 205)
LAND    = (214, 206, 184)
GREEN   = (74, 124, 74)
ORANGE  = (224, 122, 26)
YELLOW  = (240, 196, 66)

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF_B  = os.path.join(FONT_DIR, "NotoSerif-Bold.ttf")
SERIF_R  = os.path.join(FONT_DIR, "NotoSerif-Regular.ttf")
SANS_B   = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
SANS_R   = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill=INK, leading=None, align="left"):
    """Draw a list of lines starting at xy. Returns y after the last line."""
    x, y = xy
    if leading is None:
        leading = int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def center_block(draw, cx, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for ln in lines:
        w = draw.textlength(ln, font=fnt)
        draw.text((cx - w / 2, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def panel(draw, box, fill=WHITE, outline=INK, width=1):
    draw.rectangle(box, fill=fill, outline=outline, width=width)


# ---- hero art ------------------------------------------------------------
# Each hero art panel is drawn in a box (x, y, w, h) on the given ImageDraw.

def art_cop31(d, x, y, w, h):
    """A cracked globe over a broken conference table: the COP31 collapse."""
    # sky
    d.rectangle([x, y, x + w, y + h], fill=(233, 224, 205))
    # sun rays behind globe
    cx, cy, r = x + w // 2, y + h // 2 + 6, 62
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        x2 = cx + int(math.cos(a) * (r + 26))
        y2 = cy + int(math.sin(a) * (r + 26))
        d.line([(cx, cy), (x2, y2)], fill=(226, 200, 120), width=5)
    # globe
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(88, 150, 196),
              outline=NAVY, width=3)
    # continents (simple blobs)
    d.ellipse([cx - 42, cy - 34, cx - 8, cy - 2], fill=GREEN)
    d.ellipse([cx + 2, cy + 6, cx + 40, cy + 34], fill=GREEN)
    d.ellipse([cx - 18, cy + 22, cx + 12, cy + 44], fill=(96, 140, 88))
    # jagged crack through the globe
    crack = [(cx - 46, cy - 52), (cx - 22, cy - 28), (cx - 34, cy - 4),
             (cx - 8, cy + 12), (cx - 20, cy + 30), (cx + 4, cy + 52)]
    d.line(crack, fill=DARKRED, width=5, joint="curve")
    # red NO-DEAL slash across the globe
    d.line([(cx - r - 6, cy + r + 6), (cx + r + 6, cy - r - 6)],
           fill=RED, width=7)


def art_iran(d, x, y, w, h):
    """A tanker on burning water under a missile arc: the Iran war widens."""
    # sky gradient bands
    d.rectangle([x, y, x + w, y + h], fill=(250, 214, 170))
    d.rectangle([x, y, x + w, y + int(h * 0.55)], fill=(244, 190, 140))
    # missile arc + missile
    import math
    pts = []
    for t in range(0, 101, 5):
        px = x + 20 + t * (w - 40) / 100.0
        py = y + 58 - math.sin(math.radians(t * 1.8)) * 44
        pts.append((px, py))
    d.line(pts, fill=(90, 90, 96), width=3)
    mx, my = pts[-1]
    d.polygon([(mx, my - 5), (mx + 16, my), (mx, my + 5)], fill=(60, 60, 66))
    # sea
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=SEA)
    for wy in (int(h * 0.68), int(h * 0.80), int(h * 0.92)):
        d.arc([x + 6, y + wy - 8, x + w - 6, y + wy + 8], 0, 180,
              fill=(90, 140, 180), width=3)
    # tanker hull
    hx, hy = x + 46, y + int(h * 0.62)
    d.polygon([(hx, hy), (hx + 220, hy), (hx + 200, hy + 34),
               (hx + 16, hy + 34)], fill=(52, 52, 58))
    d.rectangle([hx + 30, hy - 22, hx + 70, hy], fill=(140, 40, 36))
    d.rectangle([hx + 80, hy - 22, hx + 120, hy], fill=(200, 150, 50))
    d.rectangle([hx + 130, hy - 22, hx + 170, hy], fill=(60, 110, 70))
    d.rectangle([hx + 180, hy - 30, hx + 210, hy], fill=(230, 230, 225))
    # flames on the tanker
    for fx, fh in ((hx + 96, 26), (hx + 140, 34), (hx + 176, 22)):
        d.polygon([(fx - 12, hy - 22), (fx, hy - 22 - fh),
                   (fx + 12, hy - 22)], fill=ORANGE)
        d.polygon([(fx - 6, hy - 22), (fx, hy - 22 - fh + 12),
                   (fx + 6, hy - 22)], fill=YELLOW)
    # smoke puffs
    for sx, sy, sr in ((hx + 96, hy - 62, 12), (hx + 140, hy - 74, 15),
                       (hx + 176, hy - 58, 11)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 118, 112))


def art_benghazi(d, x, y, w, h):
    """A warship hit by sea drones: a fireball over Benghazi harbour."""
    # sky + sea
    d.rectangle([x, y, x + w, y + int(h * 0.58)], fill=(252, 226, 178))
    d.rectangle([x, y + int(h * 0.58), x + w, y + h], fill=(96, 152, 190))
    # distant harbour cranes
    for cxp in (x + 30, x + 70):
        d.line([(cxp, y + 52), (cxp, y + int(h * 0.58))], fill=(90, 84, 76),
               width=4)
        d.line([(cxp, y + 52), (cxp + 34, y + 66)], fill=(90, 84, 76),
               width=3)
    # warship hull
    hx, hy = x + 96, y + int(h * 0.62)
    d.polygon([(hx, hy), (hx + 190, hy), (hx + 172, hy + 24),
               (hx + 14, hy + 24)], fill=(74, 82, 92))
    d.rectangle([hx + 60, hy - 24, hx + 120, hy], fill=(96, 104, 114))
    d.rectangle([hx + 128, hy - 14, hx + 158, hy], fill=(96, 104, 114))
    d.line([(hx + 90, hy - 24), (hx + 90, hy - 40)], fill=(74, 82, 92),
           width=4)
    d.polygon([(hx + 90, hy - 40), (hx + 116, hy - 33), (hx + 90, hy - 29)],
              fill=RED)
    # fireball above the ship (kept inside the box)
    ex, ey = hx + 96, hy - 34
    d.ellipse([ex - 24, ey - 24, ex + 24, ey + 24], fill=(200, 60, 30))
    d.ellipse([ex - 17, ey - 17, ex + 17, ey + 17], fill=ORANGE)
    d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=YELLOW)
    d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 240, 180))
    # sea drones approaching in the water
    for dxp in (x + 16, x + 50):
        dy = y + int(h * 0.78)
        d.ellipse([dxp, dy, dxp + 26, dy + 8], fill=(40, 40, 46))
        d.line([(dxp + 26, dy + 4), (dxp + 42, dy - 2)], fill=(40, 40, 46),
               width=2)


# ---- mini art for the 10 small cards (drawn in an s x s box) -----------
# All coordinates are fractions of s so the icons scale.

def mini_chart_down(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(250, 238, 226))
    pts = [(x + 0.13 * s, y + 0.22 * s), (x + 0.35 * s, y + 0.35 * s),
           (x + 0.55 * s, y + 0.29 * s), (x + 0.74 * s, y + 0.55 * s),
           (x + 0.87 * s, y + 0.74 * s)]
    d.line(pts, fill=RED, width=3, joint="curve")
    d.polygon([(x + 0.87 * s, y + 0.74 * s), (x + 0.87 * s, y + 0.58 * s),
               (x + 0.71 * s, y + 0.74 * s)], fill=RED)


def mini_capitol(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(226, 236, 248))
    d.pieslice([x + 0.22 * s, y + 0.29 * s, x + 0.78 * s, y + 0.71 * s],
               180, 360, fill=NAVY)
    d.rectangle([x + 0.16 * s, y + 0.65 * s, x + 0.84 * s, y + 0.84 * s],
                fill=NAVY)
    d.rectangle([x + 0.45 * s, y + 0.65 * s, x + 0.55 * s, y + 0.84 * s],
                fill=WHITE)


def mini_truck(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(238, 232, 220))
    d.rectangle([x + 0.13 * s, y + 0.45 * s, x + 0.58 * s, y + 0.71 * s],
                fill=(120, 90, 60))
    d.rectangle([x + 0.61 * s, y + 0.52 * s, x + 0.81 * s, y + 0.71 * s],
                fill=(90, 110, 140))
    d.ellipse([x + 0.23 * s, y + 0.68 * s, x + 0.35 * s, y + 0.81 * s],
              fill=INK)
    d.ellipse([x + 0.61 * s, y + 0.68 * s, x + 0.74 * s, y + 0.81 * s],
              fill=INK)
    d.polygon([(x + 0.29 * s, y + 0.42 * s), (x + 0.39 * s, y + 0.19 * s),
               (x + 0.48 * s, y + 0.42 * s)], fill=ORANGE)


def mini_satellite(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(20, 26, 40))
    d.rectangle([x + 0.16 * s, y + 0.42 * s, x + 0.32 * s, y + 0.58 * s],
                fill=(70, 110, 170))
    d.rectangle([x + 0.68 * s, y + 0.42 * s, x + 0.84 * s, y + 0.58 * s],
                fill=(70, 110, 170))
    d.rectangle([x + 0.39 * s, y + 0.39 * s, x + 0.61 * s, y + 0.61 * s],
                fill=(200, 200, 200))
    d.ellipse([x + 0.44 * s, y + 0.44 * s, x + 0.56 * s, y + 0.56 * s],
              fill=RED)
    d.line([(x + 0.5 * s, y + 0.61 * s), (x + 0.5 * s, y + 0.77 * s)],
           fill=(200, 200, 200), width=2)
    d.ellipse([x + 0.44 * s, y + 0.74 * s, x + 0.56 * s, y + 0.86 * s],
              fill=YELLOW)


def mini_chip(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(226, 248, 226))
    d.rectangle([x + 0.26 * s, y + 0.26 * s, x + 0.74 * s, y + 0.74 * s],
                fill=(34, 120, 60))
    d.rectangle([x + 0.39 * s, y + 0.39 * s, x + 0.61 * s, y + 0.61 * s],
                fill=(20, 80, 40))
    for fx in (0.32, 0.45, 0.58):
        d.line([(x + fx * s, y + 0.13 * s), (x + fx * s, y + 0.26 * s)],
               fill=INK, width=2)
        d.line([(x + fx * s, y + 0.74 * s), (x + fx * s, y + 0.87 * s)],
               fill=INK, width=2)


def mini_cuffs(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(238, 238, 238))
    d.ellipse([x + 0.16 * s, y + 0.35 * s, x + 0.45 * s, y + 0.65 * s],
              outline=INK, width=3)
    d.ellipse([x + 0.55 * s, y + 0.35 * s, x + 0.84 * s, y + 0.65 * s],
              outline=INK, width=3)
    d.line([(x + 0.45 * s, y + 0.5 * s), (x + 0.55 * s, y + 0.5 * s)],
           fill=INK, width=3)


def mini_robot(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(250, 232, 232))
    d.rounded_rectangle([x + 0.23 * s, y + 0.23 * s, x + 0.77 * s,
                         y + 0.77 * s], radius=6, fill=(200, 210, 220),
                        outline=INK, width=2)
    d.ellipse([x + 0.32 * s, y + 0.42 * s, x + 0.45 * s, y + 0.55 * s],
              fill=RED)
    d.ellipse([x + 0.55 * s, y + 0.42 * s, x + 0.68 * s, y + 0.55 * s],
              fill=RED)
    d.line([(x + 0.32 * s, y + 0.68 * s), (x + 0.68 * s, y + 0.68 * s)],
           fill=INK, width=2)
    d.line([(x + 0.19 * s, y + 0.19 * s), (x + 0.81 * s, y + 0.81 * s)],
           fill=RED, width=3)


def mini_cap(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(232, 232, 248))
    d.polygon([(x + 0.13 * s, y + 0.42 * s), (x + 0.5 * s, y + 0.23 * s),
               (x + 0.87 * s, y + 0.42 * s), (x + 0.5 * s, y + 0.61 * s)],
              fill=NAVY)
    d.rectangle([x + 0.32 * s, y + 0.48 * s, x + 0.68 * s, y + 0.65 * s],
                fill=(60, 60, 90))
    d.line([(x + 0.71 * s, y + 0.29 * s), (x + 0.71 * s, y + 0.48 * s)],
           fill=GOLD, width=2)
    d.ellipse([x + 0.66 * s, y + 0.45 * s, x + 0.76 * s, y + 0.55 * s],
              fill=GOLD)


def mini_mic(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(248, 238, 226))
    d.ellipse([x + 0.32 * s, y + 0.16 * s, x + 0.68 * s, y + 0.58 * s],
              fill=(70, 70, 80))
    d.arc([x + 0.26 * s, y + 0.35 * s, x + 0.74 * s, y + 0.77 * s], 0, 180,
          fill=INK, width=3)
    d.line([(x + 0.5 * s, y + 0.77 * s), (x + 0.5 * s, y + 0.87 * s)],
           fill=INK, width=3)
    d.line([(x + 0.23 * s, y + 0.23 * s), (x + 0.77 * s, y + 0.77 * s)],
           fill=RED, width=3)


def mini_building(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(240, 234, 222))
    d.rectangle([x + 0.19 * s, y + 0.32 * s, x + 0.81 * s, y + 0.84 * s],
                fill=(150, 140, 120))
    for wy in (0.42, 0.55, 0.68):
        for wx in (0.29, 0.45, 0.61):
            d.rectangle([x + wx * s, y + wy * s, x + (wx + 0.10) * s,
                         y + (wy + 0.08) * s], fill=(60, 60, 70))
    d.line([(x + 0.48 * s, y + 0.32 * s), (x + 0.39 * s, y + 0.52 * s),
            (x + 0.55 * s, y + 0.65 * s), (x + 0.42 * s, y + 0.84 * s)],
           fill=DARKRED, width=3)


# ---- world map -----------------------------------------------------------
# Simplified continents in map-local coordinates (map box w x h).

CONTINENTS = [
    # North America
    [(18, 48), (60, 30), (95, 28), (118, 40), (110, 62), (88, 78),
     (70, 95), (48, 88), (28, 72)],
    # Greenland
    [(118, 18), (138, 14), (146, 26), (130, 34)],
    # South America
    [(88, 108), (112, 102), (128, 120), (124, 160), (108, 196),
     (96, 168), (86, 130)],
    # Europe
    [(168, 38), (196, 28), (212, 40), (206, 58), (188, 66), (172, 58)],
    # Africa
    [(172, 74), (200, 70), (222, 82), (228, 108), (214, 150),
     (196, 158), (182, 128), (170, 100)],
    # Asia
    [(212, 30), (260, 22), (300, 34), (312, 58), (296, 84), (272, 96),
     (252, 84), (236, 66), (218, 52)],
    # SE Asia islands
    [(278, 116), (290, 112), (296, 122), (284, 128)],
    # Australia
    [(272, 158), (300, 152), (312, 166), (296, 182), (276, 176)],
]

# (label, mx, my) story locations on the map
MAP_DOTS = [
    ("Antalya", 206, 60), ("Bahrain", 232, 84), ("Benghazi", 192, 82),
    ("Kyiv", 200, 42), ("Seoul", 292, 52), ("Washington", 72, 56),
    ("Gaza", 210, 74), ("Mexico", 30, 76), ("Copenhagen", 188, 32),
    ("Dhaka", 258, 76), ("Ituri", 200, 128), ("Barbados", 92, 96),
    ("Banten", 282, 128), ("Brussels", 182, 42),
]


def draw_map(d, x, y, w, h):
    """Draw the simplified world map with story dots."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    # graticule
    for gx in range(x + 40, x + w, 40):
        d.line([(gx, y), (gx, y + h)], fill=(190, 210, 225), width=1)
    for gy in range(y + 40, y + h, 40):
        d.line([(x, gy), (x + w, gy)], fill=(190, 210, 225), width=1)
    sx = w / 330.0
    sy = h / 210.0
    for poly in CONTINENTS:
        pts = [(x + px * sx, y + py * sy) for px, py in poly]
        d.polygon(pts, fill=LAND, outline=(150, 140, 118))
    for label, mx, my in MAP_DOTS:
        px, py = x + mx * sx, y + my * sy
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=WHITE, width=1)
    return


# ---- content -------------------------------------------------------------

HEROES = [
    {
        "kicker": "CLIMATE  ·  ANTALYA, TURKEY",
        "headline": "COP31 COLLAPSES",
        "body": ("Longest climate talks in history end with no deal. "
                 "The EU and 130 nations reject a text that never mentions "
                 "fossil fuels — the first full COP collapse since "
                 "Copenhagen 2009."),
        "source": "CNN · REUTERS",
        "art": art_cop31,
    },
    {
        "kicker": "THE IRAN WAR  ·  BAHRAIN",
        "headline": "IRAN HITS BAHRAIN, TANKERS BURN",
        "body": ("A Saturday strike hits a civilian plant in Bahrain, "
                 "injuring two. The IRGC fires missiles and drones at US "
                 "positions. At least 3 tankers are hit in the Strait "
                 "of Hormuz."),
        "source": "REUTERS · AL JAZEERA",
        "art": art_iran,
    },
    {
        "kicker": "UKRAINE  ·  BENGHAZI, LIBYA",
        "headline": "UKRAINE SINKS A RUSSIAN WARSHIP — IN LIBYA",
        "body": ("Seven sea drones sink the corvette Merkury in Benghazi, "
                 "2,400 km from the front. A Ka-27 helicopter is destroyed "
                 "and the cargo ship MV Angara is hit."),
        "source": "CNN · AP",
        "art": art_benghazi,
    },
]

NUMBERS = [
    ("258", "Democrats' House seats — best since 1992"),
    ("-5.8%", "Kospi intraday plunge, Seoul"),
    ("11,762", "Ebola cases in DR Congo"),
    ("34", "workers missing in Indonesia fire"),
    ("404", "flights cancelled in Belgium"),
    ("7", "sea drones sank the Merkury"),
]

REGIONS = [("Europe", 8), ("Asia", 7), ("Middle East", 5), ("Africa", 3),
           ("Americas", 8), ("Global", 4)]

SMALL = [
    ("RUSSIA STRIKES UKRAINE",
     "Kryvyi Rih: boy, 7, and paramedic, 20, killed. Dymer: 11 dead. "
     "Poland: 3 Russian objects crossed in; NATO meets.",
     "REUTERS", mini_building),
    ("KOSPI PLUNGES",
     "Seoul's index fell as much as 5.8% and closed -3.3% at 4,708. "
     "Samsung -3.1%, SK Hynix -2.5% as AI doubts spread.",
     "AL JAZEERA", mini_chart_down),
    ("DEMOCRATS WIN 258 SEATS",
     "Best House result since 1992. The 258th seat fell Sunday as Chuck "
     "Hubbard beat Virginia Foxx. +44 seats.",
     "AP", mini_capitol),
    ("GAZA TRUCK HIT, 3 DEAD",
     "Israeli forces hit a truck in Gaza on Saturday. PM-elect "
     "Eisenkot calls settler arson 'Jewish terrorism'.",
     "REUTERS", mini_truck),
    ("RUSSIA'S SPACE NUKE",
     "NATO intel: Moscow plans to launch a nuclear-armed satellite, "
     "Sputnik-S, this year — possibly as early as December.",
     "REUTERS", mini_satellite),
    ("HUANG IS BACK",
     "Nvidia's board reinstates Jensen Huang as CEO, 11 days after he "
     "quit. Shares jump about a third.",
     "REUTERS", mini_chip),
    ("'CHAPO ISIDRO' CAUGHT",
     "Mexican troops capture Sinaloa boss Fausto Isidro Meza Flores, "
     "an FBI Top 10 fugitive, in Guasave. 11 killed.",
     "DOJ", mini_cuffs),
    ("TWO STATES SUE SPACEX",
     "Oregon and Virginia sue Musk's SpaceX over Grok AI making child "
     "sexual abuse images and nonconsensual deepfakes.",
     "REUTERS", mini_robot),
    ("KOREA MINISTER QUITS",
     "Education chief Choi Kyo-jin resigns over an AI-cheating scandal "
     "in the Suneung exam. 111 device cases found.",
     "GUARDIAN", mini_cap),
    ("DENMARK: RUSSIA PLOT",
     "Copenhagen says Russian intel plotted to kill rapper Kyivstoner "
     "at a concert. Russia's defence attaché is expelled.",
     "WSJ", mini_mic),
]

ALSO = [
    ("Tajikistan quits the ICC", "4th country to start leaving since the US push to 'dismantle' the court.", "REUTERS"),
    ("Bangladesh vows to jail Hasina", "if she returns from India; she faces a death sentence.", "REUTERS"),
    ("Ebola workers trapped", "fighting in Ituri, DR Congo, pins responders in a hospital ward for 24 hours.", "UN NEWS"),
    ("Guterres: rein in AI", "UN chief at a Barbados summit calls for a global AI risk framework.", "UN NEWS"),
    ("Indonesia factory fire", "34 workers missing after a candy plant blaze in Banten; at least 3 dead.", "AP"),
    ("Belgium grinds to a halt", "anti-austerity strike cancels 404 flights; 50,000 passengers hit.", "AP"),
    ("Mt Fuji warning", "China warns citizens off off-season climbs as a missing hiker's family offers $75,000.", "EMBASSY"),
    ("US stocks rebound", "Nasdaq +6%, S&P 500 +4% as Nvidia's return lifts the AI trade.", "REUTERS"),
    ("Sparta II ablaze", "Russian cargo ship hit by drones in the Baltic drifts into Finnish waters.", "WSJ"),
    ("Maltese ship hit", "hours after Benghazi, another sea drone strikes a commercial vessel off Libya.", "AP"),
    ("Kharg convoy", "14+ Iranian tankers mass at Kharg Island, ready to test the US blockade.", "GULF NEWS"),
    ("US hits Qeshm", "a US jet strikes a Revolutionary Guard missile site on Qeshm Island in retaliation.", "AP"),
    ("Poland finds missile debris", "Kh-101 cruise missile parts found at three sites in eastern Poland.", "ANSA"),
    ("NATO meets on Poland", "the North Atlantic Council holds an emergency session in Brussels.", "JUST SECURITY"),
    ("Trump: Iran deal 'not acceptable'", "'We want a real deal, not a fake deal,' he said on Friday.", "JUST SECURITY"),
    ("EU answers Denmark plot", "von der Leyen condemns the foiled killing and pledges a European response.", "EU"),
    ("Penny's last day", "Trump signs the Common Cents Act, ending the US penny after 232 years.", "FBT"),
    ("Delta outage", "a systems failure delays 1,600+ Delta flights from Atlanta as Thanksgiving travel starts.", "FAA"),
    ("Belgrade floods", "record rainfall floods Serbia's capital; the weather agency faces scrutiny.", "NEXUS"),
    ("Alice Huang and China's spies", "US intel says she kept contact with China's security ministry.", "FBT"),
    ("Iran vows 'every means'", "Tehran threatens to use 'every means' against the US naval blockade.", "REUTERS"),
    ("COP31's missing $120bn", "the failed draft dropped a pledge of $120bn a year in adaptation finance by 2035.", "IPS"),
]


# ---- main layout ---------------------------------------------------------

def build_image():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead --------------------------------------------------------
    f_top = font(SANS_B, 13)
    d.text((20, 10), "THE WORLD IN ONE PAGE", font=f_top, fill=INK)
    right = "MONDAY  ·  23 NOVEMBER 2026"
    d.text((W - 20 - d.textlength(right, font=f_top), 10), right,
           font=f_top, fill=INK)
    hline(d, 20, W - 20, 32, fill=INK, width=2)

    # ---- giant date headline --------------------------------------------
    f_date = font(SERIF_B, 54)
    center_block(d, W // 2, 38, ["Monday 23 November 2026"], f_date)
    f_sub = font(SANS_R, 13)
    sub = "One day. Every story that mattered.  35 stories, all verified."
    center_block(d, W // 2, 110, [sub], f_sub)
    hline(d, 20, W - 20, 130, fill=INK, width=2)

    # ---- hero row --------------------------------------------------------
    hy, hh = 138, 224
    for i, hero in enumerate(HEROES):
        hx = 20 + i * 332
        panel(d, [hx, hy, hx + 320, hy + hh], fill=WHITE, outline=INK,
              width=1)
        hero["art"](d, hx + 1, hy + 1, 318, 104)
        hline(d, hx + 1, hx + 319, hy + 105, fill=INK, width=1)
        f_kick = font(SANS_B, 10)
        d.text((hx + 10, hy + 112), hero["kicker"], font=f_kick, fill=RED)
        f_head = font(SERIF_B, 18)
        lines = wrap(d, hero["headline"], f_head, 300)[:2]
        y = text_block(d, (hx + 10, hy + 128), lines, f_head, leading=21)
        f_body = font(SANS_R, 10)
        blines = wrap(d, hero["body"], f_body, 300)[:3]
        text_block(d, (hx + 10, hy + 172), blines, f_body, leading=12)
        f_src = font(SANS_B, 9)
        d.text((hx + 10, hy + 208), hero["source"], font=f_src,
               fill=(140, 130, 110))

    # ---- six big numbers -------------------------------------------------
    ny, nh = 370, 52
    panel(d, [20, ny, W - 20, ny + nh], fill=LGREY, outline=INK, width=1)
    for i, (num, label) in enumerate(NUMBERS):
        cx = 20 + i * 164 + 82
        f_num = font(SANS_B, 22)
        nw = d.textlength(num, font=f_num)
        d.text((cx - nw / 2, ny + 4), num, font=f_num, fill=RED)
        f_lab = font(SANS_R, 8)
        ll = wrap(d, label, f_lab, 152)
        center_block(d, cx, ny + 30, ll[:2], f_lab, leading=10)

    # ---- region bar ------------------------------------------------------
    ry = 428
    d.rectangle([20, ry, W - 20, ry + 26], fill=NAVY)
    f_reg = font(SANS_B, 11)
    reg = "WHERE THE NEWS WAS   ·   " + "   ·   ".join(
        f"{name} {n}" for name, n in REGIONS)
    rw = d.textlength(reg, font=f_reg)
    d.text(((W - rw) / 2, ry + 6), reg, font=f_reg, fill=(246, 241, 231))

    # ---- ten small cards -------------------------------------------------
    sy0 = 460
    for idx, (head, body, source, artfn) in enumerate(SMALL):
        row, col = divmod(idx, 5)
        cx = 20 + col * 198
        cy = sy0 + row * 106
        panel(d, [cx, cy, cx + 190, cy + 98], fill=WHITE, outline=INK,
              width=1)
        artfn(d, cx + 6, cy + 6, 44)
        f_h = font(SANS_B, 11)
        hl = wrap(d, head, f_h, 128)[:2]
        text_block(d, (cx + 56, cy + 6), hl, f_h, leading=13)
        f_b = font(SANS_R, 9)
        bl = wrap(d, body, f_b, 178)[:3]
        text_block(d, (cx + 6, cy + 56), bl, f_b, leading=11)
        f_s = font(SANS_B, 8)
        d.text((cx + 6, cy + 88), source, font=f_s, fill=(140, 130, 110))

    # ---- bottom: map + also + date check --------------------------------
    by = 670
    # map panel
    panel(d, [20, by, 352, 990], fill=WHITE, outline=INK, width=1)
    f_sec = font(SANS_B, 13)
    d.text((28, by + 8), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    hline(d, 28, 344, by + 28, fill=INK, width=1)
    draw_map(d, 28, by + 36, 316, 234)
    f_leg = font(SANS_R, 9)
    leg = ("Each red dot is a place in today's news — from Antalya to "
           "Benghazi, Bahrain to Seoul. The war in Ukraine reached "
           "Libya; the climate talks collapsed in Turkey.")
    ll = wrap(d, leg, f_leg, 316)
    text_block(d, (28, by + 278), ll[:3], f_leg, leading=12)

    # also column
    d.text((368, by + 8), "ALSO ON MONDAY...", font=f_sec, fill=INK)
    hline(d, 368, 1004, by + 28, fill=INK, width=1)
    f_a = font(SANS_R, 9)
    f_an = font(SANS_B, 9)
    ay = by + 36
    for n, (lead, detail, src) in enumerate(ALSO, 1):
        num = f"{n}. "
        nw = d.textlength(num, font=f_an)
        d.text((368, ay), num, font=f_an, fill=RED)
        txt = lead + " — " + detail
        if src:
            txt += f" ({src})"
        d.text((368 + nw, ay), txt, font=f_a, fill=INK)
        ay += 10

    # date check box
    dy = 934
    d.rectangle([368, dy, 1004, 990], fill=(255, 240, 238),
                outline=RED, width=2)
    f_dc = font(SANS_B, 10)
    d.text((378, dy + 6), "DATE CHECK", font=f_dc, fill=RED)
    f_dct = font(SANS_R, 9)
    dct = ("NOT IN TODAY'S PAPER: Trump, Xi and Putin met in Shenzhen on "
           "19 Nov and signed a 'Path to Peace' declaration. Four days "
           "before this paper — so it is not in it.")
    dl = wrap(d, dct, f_dct, 616)
    text_block(d, (378, dy + 22), dl[:2], f_dct, leading=12)

    # ---- footer ----------------------------------------------------------
    f_f = font(SANS_R, 9)
    foot = ("Every story here happened, or was first reported, on Monday "
            "23 November 2026.  All drawings are original.  Sources: "
            "Reuters · AP · CNN · Al Jazeera · UN News · WSJ · The Guardian")
    fw = d.textlength(foot, font=f_f)
    d.text(((W - fw) / 2, 998), foot, font=f_f, fill=INK)
    return img


def main():
    img = build_image()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
