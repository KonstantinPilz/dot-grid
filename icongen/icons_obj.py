"""Everyday objects & symbols — dot-grid icon module.
Each draw_fn(d, S) draws ONE black silhouette on a white SxS canvas.
Solid fills, thick strokes (>= S*0.06), ~10% margin, centered.
"""
import math
from PIL import ImageDraw


def heart(d, S):
    cx = S * 0.5
    # two top lobes + bottom point, built as polygon + two circles
    r = S * 0.20
    ly = S * 0.34
    d.ellipse([cx - 2 * r, ly - r, cx, ly + r], fill=0)
    d.ellipse([cx, ly - r, cx + 2 * r, ly + r], fill=0)
    # bottom triangle down to the point
    d.polygon([(cx - 2 * r, ly + r * 0.1),
               (cx + 2 * r, ly + r * 0.1),
               (cx, S * 0.86)], fill=0)


def house(d, S):
    # square body + triangular roof + door
    bx0, bx1 = S * 0.22, S * 0.78
    by0, by1 = S * 0.48, S * 0.86
    d.rectangle([bx0, by0, bx1, by1], fill=0)
    # roof wider than body
    d.polygon([(S * 0.12, by0), (S * 0.5, S * 0.16), (S * 0.88, by0)], fill=0)
    # door (white cut-out)
    dw = S * 0.12
    d.rectangle([S * 0.5 - dw, S * 0.60, S * 0.5 + dw, by1], fill=255)


def document(d, S):
    # page with folded corner + text lines
    x0, x1 = S * 0.26, S * 0.74
    y0, y1 = S * 0.12, S * 0.88
    fold = S * 0.22
    # page body as polygon with cut top-right corner
    d.polygon([(x0, y0), (x1 - fold, y0), (x1, y0 + fold),
               (x1, y1), (x0, y1)], fill=0)
    # folded corner triangle (white)
    d.polygon([(x1 - fold, y0), (x1, y0 + fold),
               (x1 - fold, y0 + fold)], fill=255)
    # text lines (white, chunky)
    lw = S * 0.07
    tx0 = x0 + S * 0.07
    tx1 = x1 - S * 0.07
    for i in range(3):
        ty = S * 0.45 + i * S * 0.13
        d.rectangle([tx0, ty, tx1, ty + lw], fill=255)


def envelope(d, S):
    x0, x1 = S * 0.12, S * 0.88
    y0, y1 = S * 0.24, S * 0.76
    d.rectangle([x0, y0, x1, y1], fill=0)
    # flap triangle (white V cut deep into top)
    vy = S * 0.58
    d.polygon([(x0, y0), (S * 0.5, vy), (x1, y0)], fill=255)
    # thick black outline of flap edges to keep the V crisp
    w = int(S * 0.045)
    d.line([(x0, y0), (S * 0.5, vy)], fill=0, width=w)
    d.line([(x1, y0), (S * 0.5, vy)], fill=0, width=w)


def key(d, S):
    # round bow (left) + shaft + teeth (right)
    bx, by = S * 0.28, S * 0.5
    br = S * 0.18
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=0)
    # hole (white)
    hr = S * 0.07
    d.ellipse([bx - hr, by - hr, bx + hr, by + hr], fill=255)
    # shaft
    sh = S * 0.13
    sx0 = bx + br * 0.4
    sx1 = S * 0.90
    d.rectangle([sx0, by - sh / 2, sx1, by + sh / 2], fill=0)
    # teeth (chunky downward stubs near the end)
    tw = S * 0.09
    th = S * 0.15
    for tx in (sx1 - S * 0.10, sx1 - S * 0.26):
        d.rectangle([tx, by + sh / 2, tx + tw, by + sh / 2 + th], fill=0)


def sun(d, S):
    cx, cy = S * 0.5, S * 0.5
    R = S * 0.27      # disc radius (dominant)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=0)
    # triangular rays: short, fat stubs poking out of the disc
    rin = R * 0.95
    rout = S * 0.47
    half = S * 0.10
    for i in range(8):
        a = i * math.pi / 4
        tip = (cx + rout * math.cos(a), cy + rout * math.sin(a))
        pa = a + math.pi / 2
        b1 = (cx + rin * math.cos(a) + half * math.cos(pa),
              cy + rin * math.sin(a) + half * math.sin(pa))
        b2 = (cx + rin * math.cos(a) - half * math.cos(pa),
              cy + rin * math.sin(a) - half * math.sin(pa))
        d.polygon([tip, b1, b2], fill=0)


def tree(d, S):
    # trunk + round canopy
    cx = S * 0.5
    tw = S * 0.10
    d.rectangle([cx - tw / 2, S * 0.58, cx + tw / 2, S * 0.88], fill=0)
    cr = S * 0.30
    d.ellipse([cx - cr, S * 0.14, cx + cr, S * 0.14 + 2 * cr], fill=0)


def clock(d, S):
    cx, cy = S * 0.5, S * 0.5
    R = S * 0.40
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=0)
    # white face
    fr = R * 0.82
    d.ellipse([cx - fr, cy - fr, cx + fr, cy + fr], fill=255)
    # two hands (black, chunky)
    w = int(S * 0.045)
    d.line([(cx, cy), (cx, cy - fr * 0.72)], fill=0, width=w)          # minute up
    d.line([(cx, cy), (cx + fr * 0.55, cy + fr * 0.15)], fill=0, width=w)  # hour
    # center hub
    hr = S * 0.04
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=0)


def camera(d, S):
    x0, x1 = S * 0.12, S * 0.88
    y0, y1 = S * 0.30, S * 0.82
    # viewfinder bump on top
    d.rectangle([S * 0.34, S * 0.22, S * 0.56, y0 + S * 0.02], fill=0)
    d.rounded_rectangle([x0, y0, x1, y1], radius=S * 0.05, fill=0)
    # lens (white ring + black inner)
    cx, cy = S * 0.5, (y0 + y1) / 2 + S * 0.02
    lr = S * 0.17
    d.ellipse([cx - lr, cy - lr, cx + lr, cy + lr], fill=255)
    ir = S * 0.10
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=0)


def crown(d, S):
    x0, x1 = S * 0.14, S * 0.86
    base_top = S * 0.66
    base_bot = S * 0.80
    # zigzag crown body: base band + 5 points
    top = S * 0.24
    mid = S * 0.42
    pts = [
        (x0, base_top),
        (x0, top),
        (S * 0.32, mid),
        (S * 0.5, top - S * 0.04),
        (S * 0.68, mid),
        (x1, top),
        (x1, base_top),
    ]
    d.polygon(pts, fill=0)
    # base band
    d.rectangle([x0, base_top, x1, base_bot], fill=0)


ICONS = [
    ("Heart", 17, heart),
    ("House", 17, house),
    ("Document", 17, document),
    ("Envelope", 17, envelope),
    ("Key", 17, key),
    ("Sun", 17, sun),
    ("Tree", 17, tree),
    ("Clock", 17, clock),
    ("Camera", 17, camera),
    ("Crown", 17, crown),
]
