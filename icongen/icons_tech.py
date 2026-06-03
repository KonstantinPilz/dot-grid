"""Technology & Hardware dot-grid icons.
Each draw_fn(d, S) draws ONE black silhouette on a white SxS canvas.
Solid fills, thick strokes (>= S*0.055), ~10% margin, centered.
"""
import math
from PIL import ImageDraw


def _pins(d, S, x0, y0, x1, y1, count, plen, pw, sides="all"):
    """Draw chunky pins sticking out of a body box."""
    bw = x1 - x0
    bh = y1 - y0
    for i in range(count):
        cx = x0 + bw * (i + 1) / (count + 1)
        cy = y0 + bh * (i + 1) / (count + 1)
        if sides in ("all", "tb"):
            d.rectangle([cx - pw / 2, y0 - plen, cx + pw / 2, y0], fill=0)        # top
            d.rectangle([cx - pw / 2, y1, cx + pw / 2, y1 + plen], fill=0)        # bottom
        if sides in ("all", "lr"):
            d.rectangle([x0 - plen, cy - pw / 2, x0, cy + pw / 2], fill=0)        # left
            d.rectangle([x1, cy - pw / 2, x1 + plen, cy + pw / 2], fill=0)        # right


def microchip(d, S):
    m = S * 0.31
    x0, y0, x1, y1 = m, m, S - m, S - m
    plen = S * 0.18
    pw = S * 0.06
    _pins(d, S, x0, y0, x1, y1, 3, plen, pw, sides="all")
    d.rectangle([x0, y0, x1, y1], fill=0)


def cpu(d, S):
    m = S * 0.32
    x0, y0, x1, y1 = m, m, S - m, S - m
    plen = S * 0.17
    pw = S * 0.075
    _pins(d, S, x0, y0, x1, y1, 3, plen, pw, sides="all")
    d.rectangle([x0, y0, x1, y1], fill=0)
    # inner square (white core)
    im = S * 0.085
    d.rectangle([x0 + im, y0 + im, x1 - im, y1 - im], fill=255)


def gpu(d, S):
    # board
    bx0, by0, bx1, by1 = S * 0.10, S * 0.26, S * 0.90, S * 0.70
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=S * 0.04, fill=0)
    # fan circle (white) on the board
    cx, cy = S * 0.42, S * 0.48
    fr = S * 0.16
    d.ellipse([cx - fr, cy - fr, cx + fr, cy + fr], fill=255)
    d.ellipse([cx - S * 0.04, cy - S * 0.04, cx + S * 0.04, cy + S * 0.04], fill=0)  # hub
    # bracket on the left edge
    d.rectangle([S * 0.04, S * 0.22, S * 0.10, S * 0.74], fill=0)
    # output ports (white slots in bracket)
    d.rectangle([S * 0.055, S * 0.30, S * 0.10, S * 0.36], fill=255)
    d.rectangle([S * 0.055, S * 0.42, S * 0.10, S * 0.48], fill=255)
    # connector pins along bottom
    for i in range(5):
        px = bx0 + S * 0.10 + i * S * 0.14
        d.rectangle([px, by1, px + S * 0.06, by1 + S * 0.08], fill=0)


def server(d, S):
    x0, x1 = S * 0.16, S * 0.84
    h = S * 0.18
    gap = S * 0.045
    top = S * 0.16
    for r in range(3):
        y0 = top + r * (h + gap)
        y1 = y0 + h
        d.rounded_rectangle([x0, y0, x1, y1], radius=S * 0.02, fill=0)
        # indicator dots (white) on left
        dy = y0 + h / 2
        for i in range(2):
            dx = x0 + S * 0.07 + i * S * 0.075
            dr = S * 0.025
            d.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=255)
        # slot bar (white) on right
        d.rectangle([x1 - S * 0.22, dy - S * 0.018, x1 - S * 0.05, dy + S * 0.018], fill=255)


def robot(d, S):
    # antenna
    d.rectangle([S * 0.485, S * 0.10, S * 0.515, S * 0.22], fill=0)
    ar = S * 0.045
    d.ellipse([S * 0.5 - ar, S * 0.07 - ar, S * 0.5 + ar, S * 0.07 + ar], fill=0)
    # head box
    x0, y0, x1, y1 = S * 0.20, S * 0.22, S * 0.80, S * 0.80
    d.rounded_rectangle([x0, y0, x1, y1], radius=S * 0.06, fill=0)
    # eyes (white)
    ey = S * 0.44
    er = S * 0.075
    for ex in (S * 0.37, S * 0.63):
        d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=255)
    # mouth (white bar)
    d.rectangle([S * 0.33, S * 0.62, S * 0.67, S * 0.685], fill=255)


def satellite(d, S):
    cx, cy = S * 0.5, S * 0.52
    # body
    bw, bh = S * 0.12, S * 0.22
    d.rounded_rectangle([cx - bw, cy - bh, cx + bw, cy + bh], radius=S * 0.03, fill=0)
    # connecting arms
    arm = S * 0.03
    d.rectangle([cx - bw - S * 0.07, cy - arm, cx - bw, cy + arm], fill=0)
    d.rectangle([cx + bw, cy - arm, cx + bw + S * 0.07, cy + arm], fill=0)
    # solar panels (rectangular wings, separated from body)
    pw, ph = S * 0.22, S * 0.20
    lx = cx - bw - S * 0.07
    rx = cx + bw + S * 0.07
    d.rectangle([lx - pw, cy - ph, lx, cy + ph], fill=0)
    d.rectangle([rx, cy - ph, rx + pw, cy + ph], fill=0)
    # white grid lines on panels
    for fx in (lx - pw * 0.5,):
        d.line([(fx, cy - ph), (fx, cy + ph)], fill=255, width=int(S * 0.02))
    for fx in (rx + pw * 0.5,):
        d.line([(fx, cy - ph), (fx, cy + ph)], fill=255, width=int(S * 0.02))
    # dish/antenna on top
    dr = S * 0.085
    d.ellipse([cx - dr, cy - bh - dr * 1.6, cx + dr, cy - bh + dr * 0.4], fill=0)


def rocket(d, S):
    cx = S * 0.5
    bw = S * 0.16
    # nose cone
    d.polygon([(cx, S * 0.09), (cx - bw, S * 0.34), (cx + bw, S * 0.34)], fill=0)
    # body
    d.rounded_rectangle([cx - bw, S * 0.31, cx + bw, S * 0.70],
                        radius=S * 0.05, fill=0)
    # fins
    d.polygon([(cx - bw, S * 0.54), (cx - S * 0.30, S * 0.76),
               (cx - bw, S * 0.70)], fill=0)
    d.polygon([(cx + bw, S * 0.54), (cx + S * 0.30, S * 0.76),
               (cx + bw, S * 0.70)], fill=0)
    # window (white)
    wr = S * 0.065
    d.ellipse([cx - wr, S * 0.44 - wr, cx + wr, S * 0.44 + wr], fill=255)
    # flame
    d.polygon([(cx - S * 0.11, S * 0.70), (cx + S * 0.11, S * 0.70),
               (cx, S * 0.93)], fill=0)


def network(d, S):
    cx, cy = S * 0.5, S * 0.5
    cr = S * 0.11
    outer = []
    R = S * 0.34
    for i in range(6):
        ang = -math.pi / 2 + i * math.pi / 3
        outer.append((cx + R * math.cos(ang), cy + R * math.sin(ang)))
    # thick links first (so nodes sit on top)
    for ox, oy in outer:
        d.line([(cx, cy), (ox, oy)], fill=0, width=int(S * 0.045))
    # outer nodes
    orr = S * 0.075
    for ox, oy in outer:
        d.ellipse([ox - orr, oy - orr, ox + orr, oy + orr], fill=0)
    # central node
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=0)


def database(d, S):
    cx = S * 0.5
    rx = S * 0.30
    ry = S * 0.09
    top = S * 0.18
    bot = S * 0.82
    # body rectangle
    d.rectangle([cx - rx, top, cx + rx, bot], fill=0)
    # bottom rounded
    d.ellipse([cx - rx, bot - ry, cx + rx, bot + ry], fill=0)
    # top ellipse
    d.ellipse([cx - rx, top - ry, cx + rx, top + ry], fill=0)
    # band lines (white ellipse arcs separating drums)
    for frac in (0.36, 0.64):
        by = top + (bot - top) * frac
        d.arc([cx - rx, by - ry, cx + rx, by + ry], 0, 180, fill=255, width=int(S * 0.03))


def monitor(d, S):
    # screen
    x0, y0, x1, y1 = S * 0.12, S * 0.16, S * 0.88, S * 0.66
    d.rounded_rectangle([x0, y0, x1, y1], radius=S * 0.04, fill=0)
    # inner display (white)
    im = S * 0.06
    d.rectangle([x0 + im, y0 + im, x1 - im, y1 - im], fill=255)
    # stand neck
    d.rectangle([S * 0.45, y1, S * 0.55, S * 0.80], fill=0)
    # base
    d.rounded_rectangle([S * 0.30, S * 0.80, S * 0.70, S * 0.88], radius=S * 0.02, fill=0)


ICONS = [
    ("Microchip", 21, microchip),
    ("CPU", 21, cpu),
    ("GPU", 19, gpu),
    ("Server", 17, server),
    ("Robot", 17, robot),
    ("Satellite", 19, satellite),
    ("Rocket", 19, rocket),
    ("Network", 21, network),
    ("Database", 17, database),
    ("Monitor", 17, monitor),
]
