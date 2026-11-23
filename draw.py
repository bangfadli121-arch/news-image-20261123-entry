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
DARKBLUE = (18, 52, 96)
TEAL    = (40, 110, 130)
SMOKE_D = (88, 86, 82)
SMOKE_L = (192, 188, 180)
FLAME_R = (198, 38, 18)
FLAME_O = (238, 118, 20)
FLAME_Y = (250, 198, 60)
FLAME_W = (255, 244, 190)
TAN     = (198, 164, 110)
BROWN   = (122, 84, 52)

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


def lerp(c1, c2, t):
    """Interpolate two RGB colors."""
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))


def vgrad(d, box, top, bottom):
    """Fill box with a vertical gradient from top color to bottom color."""
    x0, y0, x1, y1 = box
    hh = max(1, y1 - y0)
    for yy in range(y0, y1):
        t = (yy - y0) / hh
        d.line([(x0, yy), (x1, yy)], fill=lerp(top, bottom, t))


def rgrad(d, cx, cy, r, inner, outer):
    """Fill a disc with a radial gradient (inner color at the center)."""
    for rr in range(r, 0, -1):
        t = rr / r
        col = lerp(inner, outer, t)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)


def flame_tongue(d, bx, by, wdt, hgt):
    """A layered flame tongue rising from base point (bx, by)."""
    # outer red flame
    d.polygon([(bx - wdt, by), (bx - wdt * 0.55, by - hgt * 0.55),
               (bx - wdt * 0.15, by - hgt * 0.75), (bx, by - hgt),
               (bx + wdt * 0.15, by - hgt * 0.7),
               (bx + wdt * 0.55, by - hgt * 0.5), (bx + wdt, by)],
              fill=FLAME_R)
    # mid orange flame
    d.polygon([(bx - wdt * 0.65, by), (bx - wdt * 0.3, by - hgt * 0.45),
               (bx, by - hgt * 0.72), (bx + wdt * 0.3, by - hgt * 0.4),
               (bx + wdt * 0.65, by)], fill=FLAME_O)
    # inner yellow flame
    d.polygon([(bx - wdt * 0.38, by), (bx - wdt * 0.15, by - hgt * 0.35),
               (bx, by - hgt * 0.5), (bx + wdt * 0.15, by - hgt * 0.3),
               (bx + wdt * 0.38, by)], fill=FLAME_Y)
    # hot core
    d.ellipse([bx - wdt * 0.16, by - hgt * 0.22, bx + wdt * 0.16, by],
              fill=FLAME_W)


def smoke_plume(d, bx, by, rise, n=6, top=None):
    """A rising smoke plume: overlapping puffs, dark at base, pale aloft.
    If top is given, no puff rises above that y (stays inside the panel)."""
    import math
    for i in range(n):
        t = i / max(1, n - 1)
        px = bx + int(math.sin(i * 1.7) * 6) - int(t * 6)
        py = by - int(t * rise)
        rr = int(5 + t * 7)
        if top is not None:
            py = max(py, top + rr)
        col = lerp(SMOKE_D, SMOKE_L, t)
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=col)
        d.ellipse([px - rr // 2, py - rr // 2, px + rr // 2, py + rr // 2],
                  fill=lerp(col, WHITE, 0.25))


# ---- hero art ------------------------------------------------------------
# Each hero art panel is drawn in a box (x, y, w, h) on the given ImageDraw.

def art_cop31(d, x, y, w, h):
    """A parched, cracked globe under a harsh sun: the COP31 collapse."""
    import math
    # dusty sky gradient, hot and dry
    vgrad(d, [x, y, x + w, y + h], (250, 234, 196), (238, 206, 150))
    # harsh sun, top right, rays kept inside the panel
    sx, sy, sr = x + w - 48, y + 30, 13
    rgrad(d, sx, sy, sr + 10, (255, 244, 190), (244, 200, 110))
    for ang in range(0, 360, 24):
        a = math.radians(ang)
        x1 = sx + int(math.cos(a) * (sr + 12))
        y1 = sy + int(math.sin(a) * (sr + 12))
        x2 = sx + int(math.cos(a) * (sr + 22))
        y2 = sy + int(math.sin(a) * (sr + 22))
        if y1 >= y + 2 and y2 >= y + 2:
            d.line([(x1, y1), (x2, y2)], fill=(232, 196, 100), width=3)
    # distant dry hills at the bottom
    d.polygon([(x, y + h), (x, y + h - 12), (x + 70, y + h - 22),
               (x + 150, y + h - 10), (x + 230, y + h - 20),
               (x + w, y + h - 8), (x + w, y + h)], fill=(214, 178, 128))
    # globe: shaded sphere, light from top-left, sized to fit the panel
    cx, cy, r = x + w // 2 - 16, y + h // 2 + 2, 48
    rgrad(d, cx - 7, cy - 9, r + 3, (150, 200, 232), (52, 108, 162))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    # ocean shading: darker crescent bottom-right for depth
    d.pieslice([cx - r + 5, cy - r + 5, cx + r - 2, cy + r - 2], 300, 60,
               fill=(44, 92, 142))
    # continents: recognizable landmasses, green with tan dry patches
    # Americas (left)
    d.polygon([(cx - 40, cy - 24), (cx - 26, cy - 30), (cx - 19, cy - 19),
               (cx - 26, cy - 7), (cx - 36, cy - 5)], fill=GREEN)
    d.polygon([(cx - 33, cy + 2), (cx - 22, cy + 0), (cx - 19, cy + 12),
               (cx - 26, cy + 24), (cx - 35, cy + 15)], fill=(96, 140, 88))
    # Africa (center)
    d.polygon([(cx - 5, cy - 15), (cx + 10, cy - 19), (cx + 17, cy - 7),
               (cx + 10, cy + 7), (cx - 2, cy + 10), (cx - 9, cy - 2)],
              fill=GREEN)
    d.ellipse([cx + 2, cy - 10, cx + 12, cy + 2], fill=TAN)
    # Eurasia (right)
    d.polygon([(cx + 15, cy - 26), (cx + 34, cy - 27), (cx + 41, cy - 15),
               (cx + 31, cy - 7), (cx + 19, cy - 12)], fill=GREEN)
    d.ellipse([cx + 24, cy - 22, cx + 36, cy - 12], fill=TAN)
    # Australia (lower right)
    d.ellipse([cx + 19, cy + 19, cx + 34, cy + 27], fill=(96, 140, 88))
    # cloud wisps across the globe
    for cxx, cyy, cw in ((cx - 26, cy - 34, 14), (cx + 7, cy - 29, 10),
                         (cx + 21, cy + 10, 12), (cx - 15, cy + 26, 10)):
        d.ellipse([cxx - cw, cyy - 3, cxx + cw, cyy + 3],
                  fill=(240, 244, 248))
    # jagged main crack with branches
    crack = [(cx - 34, cy - 41), (cx - 21, cy - 26), (cx - 29, cy - 10),
             (cx - 12, cy + 2), (cx - 21, cy + 15), (cx - 5, cy + 29),
             (cx + 2, cy + 43)]
    d.line(crack, fill=(90, 40, 30), width=4, joint="curve")
    d.line([(cx - 21, cy - 26), (cx - 7, cy - 33), (cx + 3, cy - 26)],
           fill=(90, 40, 30), width=2, joint="curve")
    d.line([(cx - 12, cy + 2), (cx + 2, cy + 7), (cx + 10, cy + 2)],
           fill=(90, 40, 30), width=2, joint="curve")
    # red NO-DEAL slash across the globe
    d.line([(cx - r - 3, cy + r + 1), (cx + r + 3, cy - r - 1)],
           fill=RED, width=7)
    # cracked dry earth strip at the very bottom
    for exx in (x + 30, x + 120, x + 250):
        d.line([(exx, y + h - 6), (exx + 8, y + h - 2),
                (exx + 16, y + h - 6)], fill=BROWN, width=2)


def art_iran(d, x, y, w, h):
    """A tanker burning on a sunset sea under a missile arc."""
    import math
    # sunset sky gradient
    vgrad(d, [x, y, x + w, y + int(h * 0.62)], (250, 196, 130),
          (252, 228, 178))
    # low sun disc, left
    rgrad(d, x + 34, y + 26, 20, (255, 238, 170), (244, 180, 90))
    # thin clouds
    for cxx, cyy, cw in ((x + 120, y + 16, 34), (x + 210, y + 30, 28),
                         (x + 260, y + 12, 22)):
        d.ellipse([cxx - cw, cyy - 3, cxx + cw, cyy + 3],
                  fill=(252, 226, 190))
    # missile arc with a smoke trail + missile body
    pts = []
    for t in range(0, 101, 4):
        px = x + 24 + t * (w - 48) / 100.0
        py = y + 62 - math.sin(math.radians(t * 1.8)) * 46
        pts.append((px, py))
    for i, (px, py) in enumerate(pts[::3]):
        rr = max(2, 6 - i // 4)
        d.ellipse([px - rr, py - rr, px + rr, py + rr],
                  fill=lerp(SMOKE_L, WHITE, i / 12.0))
    d.line(pts, fill=(80, 80, 88), width=2)
    mx, my = pts[-1]
    d.polygon([(mx, my - 5), (mx + 18, my), (mx, my + 5)], fill=(50, 50, 58))
    d.polygon([(mx - 4, my - 7), (mx + 6, my), (mx - 4, my + 7)],
              fill=(120, 120, 128))
    # sea: gradient + lively waves with whitecaps
    sea_y = y + int(h * 0.62)
    vgrad(d, [x, sea_y, x + w, y + h], (110, 165, 200), (60, 110, 160))
    for wy, amp in ((0.68, 5), (0.78, 6), (0.88, 7), (0.96, 5)):
        yy = y + int(h * wy)
        for xx in range(x + 8, x + w - 8, 26):
            d.arc([xx, yy - amp, xx + 26, yy + amp], 180, 360,
                  fill=(200, 225, 240), width=2)
    # burning oil reflection under the ship
    for rx in range(x + 90, x + 230, 14):
        d.line([(rx, sea_y + 26), (rx + 8, sea_y + 26)],
               fill=FLAME_O, width=3)
    # tanker hull with waterline stripe, bow and deck line
    hx, hy = x + 44, sea_y
    d.polygon([(hx, hy), (hx + 224, hy), (hx + 204, hy + 30),
               (hx + 14, hy + 30)], fill=(46, 46, 54))
    d.polygon([(hx + 2, hy + 22), (hx + 206, hy + 22), (hx + 202, hy + 30),
               (hx + 14, hy + 30)], fill=(140, 40, 34))
    d.line([(hx + 4, hy + 4), (hx + 220, hy + 4)], fill=(90, 90, 100),
           width=2)
    # container stacks, corrugated, in varied colors
    stacks = [(hx + 28, (178, 52, 44), 40), (hx + 74, (200, 150, 50), 40),
              (hx + 120, (58, 108, 70), 40), (hx + 166, (52, 96, 140), 34)]
    for sx0, col, sw in stacks:
        d.rectangle([sx0, hy - 24, sx0 + sw, hy], fill=col, outline=INK,
                    width=1)
        for ly in (hy - 16, hy - 8):
            d.line([(sx0, ly), (sx0 + sw, ly)], fill=lerp(col, INK, 0.35),
                   width=1)
    # bridge superstructure with windows + funnel
    d.rectangle([hx + 204, hy - 32, hx + 228, hy], fill=(235, 235, 228),
                outline=INK, width=1)
    for wy in (hy - 26, hy - 18):
        for wx in (hx + 208, hx + 215, hx + 222):
            d.rectangle([wx, wy, wx + 4, wy + 4], fill=NAVY)
    d.rectangle([hx + 196, hy - 26, hx + 203, hy], fill=(178, 52, 44))
    d.rectangle([hx + 196, hy - 30, hx + 203, hy - 26], fill=INK)
    # mast on the bow
    d.line([(hx + 12, hy), (hx + 12, hy - 22)], fill=INK, width=2)
    d.line([(hx + 12, hy - 22), (hx + 22, hy - 18)], fill=INK, width=2)
    # layered flames over the containers (kept short so smoke fits above)
    for fx, fh, fw in ((hx + 48, 18, 12), (hx + 94, 24, 14),
                       (hx + 140, 20, 12), (hx + 183, 15, 10)):
        flame_tongue(d, fx, hy - 24, fw, fh)
    # embers rising
    for exx, eyy, er in ((hx + 60, hy - 52, 2), (hx + 108, hy - 58, 3),
                         (hx + 152, hy - 54, 2), (hx + 196, hy - 48, 2)):
        d.ellipse([exx - er, eyy - er, exx + er, eyy + er], fill=FLAME_O)
    # smoke plumes, clamped inside the panel top
    smoke_plume(d, hx + 200, hy - 34, 12, n=4, top=y + 2)
    smoke_plume(d, hx + 94, hy - 50, 8, n=4, top=y + 2)


def art_benghazi(d, x, y, w, h):
    """A warship hit by sea drones: a fireball over Benghazi harbour."""
    import math
    # warm harbour sky gradient + clouds
    vgrad(d, [x, y, x + w, y + int(h * 0.58)], (252, 226, 178),
          (246, 200, 150))
    for cxx, cyy, cw in ((x + 60, y + 14, 30), (x + 180, y + 24, 26),
                         (x + 270, y + 12, 22)):
        d.ellipse([cxx - cw, cyy - 3, cxx + cw, cyy + 3],
                  fill=(250, 238, 210))
    # distant shoreline + buildings silhouette
    d.rectangle([x, y + int(h * 0.46), x + w, y + int(h * 0.58)],
                fill=(196, 178, 148))
    for bx0, bh in ((x + 16, 12), (x + 44, 18), (x + 250, 14),
                    (x + 282, 10)):
        d.rectangle([bx0, y + int(h * 0.58) - bh, bx0 + 20,
                     y + int(h * 0.58)], fill=(150, 132, 108))
    # harbour cranes, detailed
    for cxp in (x + 30, x + 72):
        d.line([(cxp, y + 34), (cxp, y + int(h * 0.58))], fill=(90, 84, 76),
               width=4)
        d.line([(cxp, y + 34), (cxp + 36, y + 48)], fill=(90, 84, 76),
               width=3)
        d.line([(cxp + 36, y + 48), (cxp + 36, y + 62)], fill=(90, 84, 76),
               width=2)
        d.rectangle([cxp + 32, y + 62, cxp + 40, y + 68], fill=(90, 84, 76))
    # sea gradient + waves + foam
    sea_y = y + int(h * 0.58)
    vgrad(d, [x, sea_y, x + w, y + h], (104, 158, 194), (58, 106, 150))
    for wy, amp in ((0.66, 5), (0.76, 6), (0.88, 6), (0.96, 5)):
        yy = y + int(h * wy)
        for xx in range(x + 8, x + w - 8, 26):
            d.arc([xx, yy - amp, xx + 26, yy + amp], 180, 360,
                  fill=(200, 225, 240), width=2)
    # warship hull with bow, waterline stripe and portholes
    hx, hy = x + 92, y + int(h * 0.62)
    d.polygon([(hx, hy), (hx + 196, hy), (hx + 178, hy + 26),
               (hx + 12, hy + 26)], fill=(82, 90, 100))
    d.polygon([(hx + 4, hy + 18), (hx + 182, hy + 18), (hx + 178, hy + 26),
               (hx + 12, hy + 26)], fill=(140, 40, 34))
    d.line([(hx + 4, hy + 3), (hx + 194, hy + 3)], fill=(120, 128, 138),
           width=2)
    for px in range(hx + 30, hx + 180, 18):
        d.ellipse([px, hy + 9, px + 4, hy + 13], fill=(40, 44, 52))
    # gun turret on the foredeck
    d.rectangle([hx + 22, hy - 12, hx + 52, hy], fill=(96, 104, 114),
                outline=INK, width=1)
    d.line([(hx + 52, hy - 8), (hx + 74, hy - 12)], fill=(70, 76, 86),
           width=4)
    # superstructure with bridge windows
    d.rectangle([hx + 62, hy - 26, hx + 124, hy], fill=(104, 112, 122),
                outline=INK, width=1)
    for wx in (hx + 68, hx + 78, hx + 88, hx + 98, hx + 108):
        d.rectangle([wx, hy - 20, wx + 6, hy - 13], fill=(30, 42, 58))
    # funnel with cap + mast with radar and antennae
    d.rectangle([hx + 130, hy - 20, hx + 146, hy], fill=(96, 104, 114),
                outline=INK, width=1)
    d.rectangle([hx + 130, hy - 24, hx + 146, hy - 20], fill=INK)
    d.line([(hx + 96, hy - 26), (hx + 96, hy - 44)], fill=(70, 76, 86),
           width=3)
    d.line([(hx + 84, hy - 42), (hx + 108, hy - 42)], fill=(70, 76, 86),
           width=3)
    d.ellipse([hx + 92, hy - 48, hx + 100, hy - 40], fill=(200, 200, 205))
    d.line([(hx + 96, hy - 44), (hx + 96, hy - 52)], fill=(70, 76, 86),
           width=2)
    # small flag on the mast
    d.polygon([(hx + 96, hy - 52), (hx + 112, hy - 49),
               (hx + 96, hy - 46)], fill=RED)
    # helicopter deck marking on the aft deck
    d.ellipse([hx + 152, hy - 4, hx + 188, hy + 2], outline=(200, 210, 220),
              width=1)
    # irregular fireball: offset overlapping orbs + flame tongues + core
    ex, ey = hx + 100, hy - 30
    for ox, oy, orr, col in ((ex - 12, ey + 6, 17, FLAME_R),
                             (ex + 10, ey + 8, 15, FLAME_R),
                             (ex, ey - 8, 19, FLAME_O),
                             (ex - 8, ey - 2, 12, FLAME_O),
                             (ex + 8, ey - 4, 11, FLAME_Y),
                             (ex, ey, 7, FLAME_W)):
        d.ellipse([ox - orr, oy - orr, ox + orr, oy + orr], fill=col)
    flame_tongue(d, ex - 16, ey - 14, 8, 15)
    flame_tongue(d, ex + 16, ey - 12, 7, 13)
    # short smoke cap above the fireball, clamped inside the panel top
    smoke_plume(d, ex + 4, ey - 20, 6, n=3, top=y + 2)
    # debris fragments flying out
    for dxx, dyy, dx2, dy2 in ((ex - 30, ey - 6, ex - 44, ey - 14),
                               (ex + 30, ey - 2, ex + 46, ey - 10),
                               (ex - 24, ey + 12, ex - 38, ey + 20),
                               (ex + 26, ey + 10, ex + 40, ey + 18)):
        d.line([(dxx, dyy), (dx2, dy2)], fill=(60, 50, 44), width=2)
        d.ellipse([dx2 - 2, dy2 - 2, dx2 + 2, dy2 + 2], fill=(60, 50, 44))
    # fire glow reflected on the water under the blast
    for rx in range(hx + 60, hx + 150, 12):
        d.line([(rx, hy + 30), (rx + 8, hy + 30)], fill=FLAME_O, width=3)
    # sea drones: low hulls with mast, sensor dome and wake
    for dxp in (x + 14, x + 48):
        dy = y + int(h * 0.80)
        d.polygon([(dxp, dy + 4), (dxp + 26, dy + 4), (dxp + 22, dy + 10),
                   (dxp + 4, dy + 10)], fill=(36, 38, 46))
        d.line([(dxp + 13, dy + 4), (dxp + 13, dy - 6)], fill=(36, 38, 46),
               width=2)
        d.ellipse([dxp + 10, dy - 9, dxp + 16, dy - 3], fill=(200, 60, 40))
        d.line([(dxp, dy + 7), (dxp - 12, dy + 12)], fill=(220, 235, 245),
               width=2)
        d.line([(dxp, dy + 7), (dxp - 12, dy + 2)], fill=(220, 235, 245),
               width=2)


# ---- mini art for the 10 small cards (drawn in an s x s box) -----------
# All coordinates are fractions of s so the icons scale.

def mini_chart_down(d, x, y, s):
    # a market chart crashing: axes, grid, steep red fall, arrow, candle
    d.rectangle([x, y, x + s, y + s], fill=(250, 238, 226))
    for gy in (0.28, 0.52, 0.76):
        d.line([(x + 0.13 * s, y + gy * s), (x + 0.90 * s, y + gy * s)],
               fill=(220, 205, 190), width=1)
    d.line([(x + 0.13 * s, y + 0.13 * s), (x + 0.13 * s, y + 0.87 * s)],
           fill=INK, width=2)
    d.line([(x + 0.13 * s, y + 0.87 * s), (x + 0.90 * s, y + 0.87 * s)],
           fill=INK, width=2)
    # red candlestick
    d.rectangle([x + 0.30 * s, y + 0.30 * s, x + 0.40 * s, y + 0.48 * s],
                fill=RED)
    d.line([(x + 0.35 * s, y + 0.24 * s), (x + 0.35 * s, y + 0.54 * s)],
           fill=RED, width=2)
    pts = [(x + 0.16 * s, y + 0.24 * s), (x + 0.35 * s, y + 0.34 * s),
           (x + 0.52 * s, y + 0.30 * s), (x + 0.70 * s, y + 0.56 * s),
           (x + 0.84 * s, y + 0.74 * s)]
    d.line(pts, fill=RED, width=3, joint="curve")
    d.polygon([(x + 0.84 * s, y + 0.74 * s), (x + 0.84 * s, y + 0.58 * s),
               (x + 0.68 * s, y + 0.74 * s)], fill=RED)


def mini_capitol(d, x, y, s):
    # the US Capitol: dome, flag, columns, steps, blue check
    d.rectangle([x, y, x + s, y + s], fill=(226, 236, 248))
    d.line([(x + 0.5 * s, y + 0.13 * s), (x + 0.5 * s, y + 0.26 * s)],
           fill=INK, width=2)
    d.polygon([(x + 0.5 * s, y + 0.13 * s), (x + 0.62 * s, y + 0.16 * s),
               (x + 0.5 * s, y + 0.20 * s)], fill=RED)
    d.pieslice([x + 0.30 * s, y + 0.24 * s, x + 0.70 * s, y + 0.62 * s],
               180, 360, fill=NAVY)
    d.rectangle([x + 0.26 * s, y + 0.60 * s, x + 0.74 * s, y + 0.66 * s],
                fill=NAVY)
    for cxx in (0.32, 0.44, 0.56, 0.68):
        d.line([(x + cxx * s, y + 0.66 * s), (x + cxx * s, y + 0.80 * s)],
               fill=NAVY, width=3)
    d.rectangle([x + 0.24 * s, y + 0.80 * s, x + 0.76 * s, y + 0.86 * s],
                fill=NAVY)
    # blue check badge
    d.ellipse([x + 0.68 * s, y + 0.68 * s, x + 0.88 * s, y + 0.88 * s],
              fill=BLUE, outline=WHITE, width=1)
    d.line([(x + 0.72 * s, y + 0.78 * s), (x + 0.76 * s, y + 0.82 * s),
            (x + 0.84 * s, y + 0.72 * s)], fill=WHITE, width=2,
           joint="curve")


def mini_truck(d, x, y, s):
    # an aid truck hit by a blast: cab, cargo, wheels, explosion, smoke
    d.rectangle([x, y, x + s, y + s], fill=(238, 232, 220))
    # explosion flash above the cargo
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        ex0, ey0 = x + 0.36 * s, y + 0.24 * s
        ex1 = ex0 + int(math.cos(a) * 0.13 * s)
        ey1 = ey0 + int(math.sin(a) * 0.13 * s)
        d.line([(ex0, ey0), (ex1, ey1)], fill=FLAME_O, width=2)
    d.ellipse([x + 0.30 * s, y + 0.18 * s, x + 0.42 * s, y + 0.30 * s],
              fill=YELLOW)
    # cargo box + cab
    d.rectangle([x + 0.10 * s, y + 0.45 * s, x + 0.56 * s, y + 0.71 * s],
                fill=(120, 90, 60), outline=INK, width=1)
    d.line([(x + 0.10 * s, y + 0.54 * s), (x + 0.56 * s, y + 0.54 * s)],
           fill=(90, 66, 44), width=1)
    d.rectangle([x + 0.59 * s, y + 0.52 * s, x + 0.80 * s, y + 0.71 * s],
                fill=(90, 110, 140), outline=INK, width=1)
    d.rectangle([x + 0.63 * s, y + 0.55 * s, x + 0.72 * s, y + 0.62 * s],
                fill=(200, 225, 240))
    # wheels with hubcaps
    for wx in (0.22, 0.62):
        d.ellipse([x + wx * s, y + 0.68 * s, x + (wx + 0.13) * s,
                   y + 0.81 * s], fill=INK)
        d.ellipse([x + (wx + 0.04) * s, y + 0.72 * s,
                   x + (wx + 0.09) * s, y + 0.77 * s], fill=(200, 200, 200))
    # small smoke wisp
    d.ellipse([x + 0.78 * s, y + 0.30 * s, x + 0.88 * s, y + 0.40 * s],
              fill=SMOKE_L)


def mini_satellite(d, x, y, s):
    # a satellite with a nuclear trefoil: panels, dish, stars, red core
    d.rectangle([x, y, x + s, y + s], fill=(20, 26, 40))
    for sx in (0.06, 0.16, 0.26, 0.36, 0.46, 0.56, 0.66, 0.76, 0.86):
        for sy in (0.08, 0.22, 0.38, 0.54, 0.70, 0.84):
            d.ellipse([x + sx * s, y + sy * s, x + (sx + 0.03) * s,
                       y + (sy + 0.03) * s], fill=(200, 210, 220))
    # solar panels with grid lines
    d.rectangle([x + 0.13 * s, y + 0.42 * s, x + 0.32 * s, y + 0.58 * s],
                fill=(70, 110, 170), outline=(150, 190, 230), width=1)
    d.rectangle([x + 0.68 * s, y + 0.42 * s, x + 0.87 * s, y + 0.58 * s],
                fill=(70, 110, 170), outline=(150, 190, 230), width=1)
    for px in (0.19, 0.25, 0.74, 0.81):
        d.line([(x + px * s, y + 0.42 * s), (x + px * s, y + 0.58 * s)],
               fill=(150, 190, 230), width=1)
    # body + dish
    d.rectangle([x + 0.38 * s, y + 0.38 * s, x + 0.62 * s, y + 0.62 * s],
                fill=(200, 200, 200), outline=INK, width=1)
    d.pieslice([x + 0.42 * s, y + 0.62 * s, x + 0.58 * s, y + 0.78 * s],
               0, 180, fill=(180, 180, 185))
    # red radiation trefoil
    d.ellipse([x + 0.44 * s, y + 0.44 * s, x + 0.56 * s, y + 0.56 * s],
              fill=RED)
    for ang in (90, 210, 330):
        import math
        a = math.radians(ang)
        d.pieslice([x + 0.42 * s, y + 0.42 * s, x + 0.58 * s,
                    y + 0.58 * s], ang - 28, ang + 28, fill=RED)


def mini_chip(d, x, y, s):
    # an AI chip with pins, circuit traces and a green rise arrow
    d.rectangle([x, y, x + s, y + s], fill=(226, 248, 226))
    # circuit traces from the die outward
    for tx, ty in ((0.30, 0.30), (0.70, 0.30), (0.30, 0.70), (0.70, 0.70)):
        d.line([(x + 0.5 * s, y + 0.5 * s), (x + tx * s, y + ty * s)],
               fill=(34, 120, 60), width=1)
    # pins on all four sides
    for fx in (0.32, 0.45, 0.58):
        d.line([(x + fx * s, y + 0.10 * s), (x + fx * s, y + 0.24 * s)],
               fill=INK, width=2)
        d.line([(x + fx * s, y + 0.76 * s), (x + fx * s, y + 0.90 * s)],
               fill=INK, width=2)
        d.line([(x + 0.10 * s, y + fx * s), (x + 0.24 * s, y + fx * s)],
               fill=INK, width=2)
        d.line([(x + 0.76 * s, y + fx * s), (x + 0.90 * s, y + fx * s)],
               fill=INK, width=2)
    d.rectangle([x + 0.24 * s, y + 0.24 * s, x + 0.76 * s, y + 0.76 * s],
                fill=(34, 120, 60), outline=INK, width=2)
    d.rectangle([x + 0.38 * s, y + 0.38 * s, x + 0.62 * s, y + 0.62 * s],
                fill=(20, 80, 40), outline=(120, 220, 140), width=1)
    # green rise arrow over the die
    d.line([(x + 0.5 * s, y + 0.58 * s), (x + 0.5 * s, y + 0.42 * s)],
           fill=(120, 230, 120), width=3)
    d.polygon([(x + 0.5 * s, y + 0.36 * s), (x + 0.44 * s, y + 0.45 * s),
               (x + 0.56 * s, y + 0.45 * s)], fill=(120, 230, 120))


def mini_cuffs(d, x, y, s):
    # handcuffs with a chain and a star badge: the arrest
    d.rectangle([x, y, x + s, y + s], fill=(238, 238, 238))
    # chain links between the cuffs
    d.line([(x + 0.42 * s, y + 0.50 * s), (x + 0.58 * s, y + 0.50 * s)],
           fill=INK, width=3)
    d.ellipse([x + 0.45 * s, y + 0.45 * s, x + 0.55 * s, y + 0.55 * s],
              outline=INK, width=2)
    # two rings, double outline, with keyholes
    for cx0 in (0.14, 0.56):
        d.ellipse([x + cx0 * s, y + 0.32 * s, x + (cx0 + 0.30) * s,
                   y + 0.68 * s], outline=INK, width=3)
        d.ellipse([x + (cx0 + 0.05) * s, y + 0.37 * s,
                   x + (cx0 + 0.25) * s, y + 0.63 * s],
                  outline=(150, 150, 150), width=1)
        d.ellipse([x + (cx0 + 0.13) * s, y + 0.47 * s,
                   x + (cx0 + 0.17) * s, y + 0.51 * s], fill=INK)
    # small star badge, bottom right
    import math
    bx, by, br = x + 0.76 * s, y + 0.76 * s, 0.11 * s
    star = []
    for i in range(10):
        a = math.radians(i * 36 - 90)
        rr = br if i % 2 == 0 else br * 0.45
        star.append((bx + int(math.cos(a) * rr), by + int(math.sin(a) * rr)))
    d.polygon(star, fill=GOLD, outline=INK)


def mini_robot(d, x, y, s):
    # an AI robot head struck by a judge's gavel: the lawsuit
    d.rectangle([x, y, x + s, y + s], fill=(250, 232, 232))
    # gavel behind the head, diagonal
    d.line([(x + 0.16 * s, y + 0.84 * s), (x + 0.84 * s, y + 0.16 * s)],
           fill=(120, 80, 40), width=3)
    d.rectangle([x + 0.70 * s, y + 0.10 * s, x + 0.88 * s, y + 0.26 * s],
                fill=(90, 60, 30), outline=INK, width=1)
    # robot head
    d.rounded_rectangle([x + 0.22 * s, y + 0.26 * s, x + 0.74 * s,
                         y + 0.76 * s], radius=6, fill=(200, 210, 220),
                        outline=INK, width=2)
    d.line([(x + 0.48 * s, y + 0.26 * s), (x + 0.48 * s, y + 0.16 * s)],
           fill=INK, width=2)
    d.ellipse([x + 0.44 * s, y + 0.11 * s, x + 0.52 * s, y + 0.19 * s],
              fill=RED)
    d.ellipse([x + 0.31 * s, y + 0.40 * s, x + 0.44 * s, y + 0.53 * s],
              fill=RED)
    d.ellipse([x + 0.56 * s, y + 0.40 * s, x + 0.69 * s, y + 0.53 * s],
              fill=RED)
    # mouth grille
    for gx in (0.34, 0.42, 0.50, 0.58):
        d.line([(x + gx * s, y + 0.62 * s), (x + gx * s, y + 0.70 * s)],
               fill=INK, width=2)
    # red verdict stamp corner
    d.line([(x + 0.12 * s, y + 0.86 * s), (x + 0.30 * s, y + 0.86 * s)],
           fill=RED, width=2)


def mini_cap(d, x, y, s):
    # a graduation cap, tassel, book and a resignation paper
    d.rectangle([x, y, x + s, y + s], fill=(232, 232, 248))
    # book at the bottom
    d.rectangle([x + 0.16 * s, y + 0.66 * s, x + 0.60 * s, y + 0.82 * s],
                fill=(90, 60, 120), outline=INK, width=1)
    d.line([(x + 0.38 * s, y + 0.66 * s), (x + 0.38 * s, y + 0.82 * s)],
           fill=WHITE, width=1)
    # mortarboard
    d.polygon([(x + 0.12 * s, y + 0.40 * s), (x + 0.50 * s, y + 0.20 * s),
               (x + 0.88 * s, y + 0.40 * s), (x + 0.50 * s, y + 0.60 * s)],
              fill=NAVY, outline=INK, width=1)
    d.rectangle([x + 0.32 * s, y + 0.46 * s, x + 0.68 * s, y + 0.62 * s],
                fill=(60, 60, 90))
    # tassel
    d.line([(x + 0.82 * s, y + 0.40 * s), (x + 0.82 * s, y + 0.58 * s)],
           fill=GOLD, width=2)
    d.ellipse([x + 0.78 * s, y + 0.56 * s, x + 0.86 * s, y + 0.64 * s],
              fill=GOLD)
    # resignation paper with a red X
    d.rectangle([x + 0.64 * s, y + 0.66 * s, x + 0.86 * s, y + 0.86 * s],
                fill=WHITE, outline=INK, width=1)
    d.line([(x + 0.68 * s, y + 0.70 * s), (x + 0.82 * s, y + 0.82 * s)],
           fill=RED, width=2)
    d.line([(x + 0.82 * s, y + 0.70 * s), (x + 0.68 * s, y + 0.82 * s)],
           fill=RED, width=2)


def mini_mic(d, x, y, s):
    # a microphone under a red ban circle: the silenced plot
    d.rectangle([x, y, x + s, y + s], fill=(248, 238, 226))
    # mic head with grille lines
    d.ellipse([x + 0.30 * s, y + 0.14 * s, x + 0.70 * s, y + 0.56 * s],
              fill=(70, 70, 80), outline=INK, width=1)
    for gy in (0.24, 0.32, 0.40, 0.48):
        d.arc([x + 0.30 * s, y + gy * s, x + 0.70 * s, y + (gy + 0.10) * s],
              0, 180, fill=(160, 160, 170), width=1)
    # mic body + stand
    d.arc([x + 0.26 * s, y + 0.40 * s, x + 0.74 * s, y + 0.80 * s], 0, 180,
          fill=INK, width=3)
    d.line([(x + 0.5 * s, y + 0.78 * s), (x + 0.5 * s, y + 0.88 * s)],
           fill=INK, width=3)
    d.line([(x + 0.38 * s, y + 0.88 * s), (x + 0.62 * s, y + 0.88 * s)],
           fill=INK, width=3)
    # red ban circle + slash over the mic
    d.ellipse([x + 0.14 * s, y + 0.10 * s, x + 0.86 * s, y + 0.82 * s],
              outline=RED, width=3)
    d.line([(x + 0.22 * s, y + 0.74 * s), (x + 0.78 * s, y + 0.18 * s)],
           fill=RED, width=3)
    # small crosshair target, top right
    d.ellipse([x + 0.70 * s, y + 0.08 * s, x + 0.88 * s, y + 0.26 * s],
              outline=RED, width=2)
    d.line([(x + 0.79 * s, y + 0.05 * s), (x + 0.79 * s, y + 0.29 * s)],
           fill=RED, width=1)
    d.line([(x + 0.67 * s, y + 0.17 * s), (x + 0.91 * s, y + 0.17 * s)],
           fill=RED, width=1)


def mini_building(d, x, y, s):
    # a struck building: roof, lit windows, door, crack, blast, smoke
    d.rectangle([x, y, x + s, y + s], fill=(240, 234, 222))
    # blast starburst at the roof corner
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        ex0, ey0 = x + 0.70 * s, y + 0.20 * s
        ex1 = ex0 + int(math.cos(a) * 0.12 * s)
        ey1 = ey0 + int(math.sin(a) * 0.12 * s)
        d.line([(ex0, ey0), (ex1, ey1)], fill=FLAME_O, width=2)
    d.ellipse([x + 0.65 * s, y + 0.15 * s, x + 0.75 * s, y + 0.25 * s],
              fill=YELLOW)
    # smoke wisp
    d.ellipse([x + 0.78 * s, y + 0.08 * s, x + 0.88 * s, y + 0.18 * s],
              fill=SMOKE_L)
    # building body + roof
    d.polygon([(x + 0.16 * s, y + 0.34 * s), (x + 0.50 * s, y + 0.22 * s),
               (x + 0.84 * s, y + 0.34 * s)], fill=(120, 100, 80))
    d.rectangle([x + 0.19 * s, y + 0.34 * s, x + 0.81 * s, y + 0.84 * s],
                fill=(150, 140, 120), outline=INK, width=1)
    # lit and dark windows
    for wy, lit in ((0.42, True), (0.55, False), (0.68, True)):
        for wx in (0.27, 0.44, 0.61):
            col = (255, 220, 120) if lit else (60, 60, 70)
            d.rectangle([x + wx * s, y + wy * s, x + (wx + 0.09) * s,
                         y + (wy + 0.08) * s], fill=col, outline=INK,
                        width=1)
    # door
    d.rectangle([x + 0.45 * s, y + 0.74 * s, x + 0.55 * s, y + 0.84 * s],
                fill=(60, 50, 40))
    # big zigzag crack down the wall
    d.line([(x + 0.52 * s, y + 0.34 * s), (x + 0.44 * s, y + 0.48 * s),
            (x + 0.56 * s, y + 0.62 * s), (x + 0.46 * s, y + 0.76 * s),
            (x + 0.52 * s, y + 0.84 * s)], fill=DARKRED, width=3,
           joint="curve")


# ---- world map -----------------------------------------------------------
# Continents redrawn from lon/lat (x = (lon+180)/360*330, y = (90-lat)/150*210)
# in a 330 x 210 map space, so shapes read as a real world map.

CONTINENTS = [
    # North America (Alaska, Canada, US, Mexico, Central America)
    [(11, 34), (23, 27), (46, 28), (92, 39), (110, 49), (115, 59),
     (96, 73), (91, 88), (82, 95), (69, 98), (62, 87), (53, 73),
     (46, 53), (87, 109), (92, 113)],
    # Greenland
    [(124, 25), (142, 28), (147, 20), (115, 17), (112, 31)],
    # South America (full size: Brazil bulge, tapering to Patagonia)
    [(96, 112), (106, 112), (115, 118), (133, 137), (121, 157),
     (114, 172), (106, 189), (103, 202), (99, 182), (94, 140),
     (92, 129), (94, 120)],
    # Europe (UK, Iberia, Scandinavia, Italy, Greece, Turkey)
    [(163, 50), (157, 73), (160, 76), (179, 67), (186, 73), (192, 70),
     (197, 42), (187, 45), (174, 48), (174, 42), (183, 31), (170, 40)],
    # Africa (bulge, Horn, Madagascar)
    [(160, 81), (170, 84), (194, 84), (194, 104), (202, 112),
     (211, 119), (200, 129), (197, 134), (200, 147), (188, 168),
     (179, 161), (177, 143), (176, 129), (151, 112), (154, 109),
     (149, 105)],
    [(208, 151), (212, 158), (206, 164), (203, 156)],
    # Asia (Middle East, India, SE Asia, China, Siberia, Japan, Korea)
    [(194, 73), (206, 84), (211, 98), (215, 81), (225, 87), (231, 95),
     (236, 115), (246, 95), (247, 92), (252, 98), (256, 105), (263, 109),
     (266, 95), (275, 81), (282, 73), (293, 73), (312, 49), (312, 35),
     (266, 25), (229, 63), (202, 42)],
    # SE Asia islands (Sumatra, Borneo, Java, New Guinea, Philippines)
    [(256, 126), (269, 126), (293, 133), (275, 129), (266, 136),
     (277, 109)],
    # Australia + Tasmania
    [(270, 171), (277, 151), (285, 143), (299, 154), (303, 174),
     (298, 179), (291, 175), (270, 174)],
    [(300, 185), (304, 188), (298, 190)],
    # New Zealand
    [(325, 179), (319, 188), (322, 184)],
]

# (label, mx, my) story locations on the map, placed by lon/lat
MAP_DOTS = [
    ("Antalya", 193, 74), ("Bahrain", 211, 89), ("Benghazi", 183, 81),
    ("Kyiv", 193, 55), ("Seoul", 282, 74), ("Washington", 94, 72),
    ("Gaza", 197, 82), ("Mexico", 74, 99), ("Copenhagen", 177, 48),
    ("Dhaka", 248, 93), ("Ituri", 192, 124), ("Barbados", 110, 107),
    ("Banten", 262, 135), ("Brussels", 169, 55),
]


def draw_map(d, x, y, w, h):
    """Draw the world map with story dots."""
    # ocean: soft vertical gradient
    vgrad(d, [x, y, x + w, y + h], (216, 234, 242), (196, 220, 234))
    # graticule
    for gx in range(x + 40, x + w, 40):
        d.line([(gx, y), (gx, y + h)], fill=(178, 202, 220), width=1)
    for gy in range(y + 40, y + h, 40):
        d.line([(x, gy), (x + w, gy)], fill=(178, 202, 220), width=1)
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
