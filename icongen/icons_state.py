"""Statecraft & Government icon silhouettes for the dot-grid harness.
Each draw_fn(d, S) draws ONE black silhouette on a white SxS canvas.
Solid fills, thick strokes (>= S*0.06), ~10% margin, centered.
"""
import math
from PIL import ImageDraw


def capitol(d, S):
    cx = S * 0.5
    # dome
    d.pieslice([cx - S * 0.20, S * 0.10, cx + S * 0.20, S * 0.50], 180, 360, fill=0)
    # cupola / finial on top
    d.rectangle([cx - S * 0.03, S * 0.05, cx + S * 0.03, S * 0.15], fill=0)
    # base drum under dome
    d.rectangle([cx - S * 0.20, S * 0.30, cx + S * 0.20, S * 0.40], fill=0)
    # entablature above columns
    d.rectangle([S * 0.13, S * 0.40, S * 0.87, S * 0.48], fill=0)
    # columns
    ncol = 6
    top, bot = S * 0.48, S * 0.74
    x0, x1 = S * 0.16, S * 0.84
    cw = S * 0.065
    for i in range(ncol):
        cxx = x0 + (x1 - x0) * i / (ncol - 1)
        d.rectangle([cxx - cw / 2, top, cxx + cw / 2, bot], fill=0)
    # steps (widening base)
    d.rectangle([S * 0.13, S * 0.74, S * 0.87, S * 0.80], fill=0)
    d.rectangle([S * 0.09, S * 0.80, S * 0.91, S * 0.86], fill=0)
    d.rectangle([S * 0.06, S * 0.86, S * 0.94, S * 0.92], fill=0)


def scales(d, S):
    cx = S * 0.5
    # central post
    d.rectangle([cx - S * 0.035, S * 0.16, cx + S * 0.035, S * 0.80], fill=0)
    # base
    d.polygon([(cx - S * 0.20, S * 0.90), (cx + S * 0.20, S * 0.90),
               (cx + S * 0.07, S * 0.80), (cx - S * 0.07, S * 0.80)], fill=0)
    d.rectangle([cx - S * 0.24, S * 0.90, cx + S * 0.24, S * 0.95], fill=0)
    # top knob
    d.ellipse([cx - S * 0.06, S * 0.10, cx + S * 0.06, S * 0.22], fill=0)
    # beam
    by = S * 0.24
    d.rectangle([S * 0.14, by - S * 0.025, S * 0.86, by + S * 0.025], fill=0)
    # hanging strings + pans
    for px in (S * 0.20, S * 0.80):
        d.line([(px, by), (px - S * 0.09, S * 0.50)], fill=0, width=int(S * 0.012))
        d.line([(px, by), (px + S * 0.09, S * 0.50)], fill=0, width=int(S * 0.012))
        # pan (shallow bowl = chord)
        d.chord([px - S * 0.11, S * 0.44, px + S * 0.11, S * 0.62], 0, 180, fill=0)


def ballot_box(d, S):
    # box body
    d.rectangle([S * 0.20, S * 0.48, S * 0.80, S * 0.90], fill=0)
    # lid (wider) with clear slot
    d.rectangle([S * 0.16, S * 0.44, S * 0.84, S * 0.54], fill=0)
    # slot (white) cut through lid
    d.rectangle([S * 0.38, S * 0.46, S * 0.62, S * 0.52], fill=255)
    # ballot: an upright white paper sticking up out of the slot with a black border
    # black paper backing
    d.rectangle([S * 0.40, S * 0.14, S * 0.60, S * 0.50], fill=0)
    # white inner so it reads as a sheet of paper
    d.rectangle([S * 0.435, S * 0.17, S * 0.565, S * 0.46], fill=255)
    # check mark (black) on the white ballot
    d.line([(S * 0.46, S * 0.30), (S * 0.49, S * 0.35)], fill=0, width=int(S * 0.03))
    d.line([(S * 0.49, S * 0.35), (S * 0.55, S * 0.23)], fill=0, width=int(S * 0.03))


def flag(d, S):
    # pole
    d.rectangle([S * 0.18, S * 0.08, S * 0.255, S * 0.92], fill=0)
    # finial
    d.ellipse([S * 0.17, S * 0.04, S * 0.265, S * 0.12], fill=0)
    # waving flag (two arcs forming a wavy banner)
    top = S * 0.12
    bot = S * 0.46
    left = S * 0.255
    right = S * 0.86
    pts = []
    # top edge L->R with wave
    n = 20
    for i in range(n + 1):
        t = i / n
        x = left + (right - left) * t
        y = top + S * 0.05 * math.sin(t * 2 * math.pi)
        pts.append((x, y))
    # right edge down
    pts.append((right, top + (bot - top) + S * 0.05 * math.sin(2 * math.pi)))
    # bottom edge R->L with wave
    for i in range(n + 1):
        t = 1 - i / n
        x = left + (right - left) * t
        y = bot + S * 0.05 * math.sin(t * 2 * math.pi)
        pts.append((x, y))
    d.polygon(pts, fill=0)


def gavel(d, S):
    # Upright gavel: horizontal head at top, vertical handle, sound block at base.
    cx = S * 0.5
    # head (thick horizontal cylinder) near top, tilted slightly
    hcx, hcy = S * 0.5, S * 0.26
    hl, hw = S * 0.22, S * 0.10
    d.rectangle([hcx - hl, hcy - hw, hcx + hl, hcy + hw], fill=0)
    # rounded end caps
    d.ellipse([hcx - hl - hw, hcy - hw, hcx - hl + hw, hcy + hw], fill=0)
    d.ellipse([hcx + hl - hw, hcy - hw, hcx + hl + hw, hcy + hw], fill=0)
    # bands (white) near each end to read as a mallet head
    d.rectangle([hcx - hl * 0.62, hcy - hw, hcx - hl * 0.50, hcy + hw], fill=255)
    d.rectangle([hcx + hl * 0.50, hcy - hw, hcx + hl * 0.62, hcy + hw], fill=255)
    # handle straight down from head
    d.rectangle([cx - S * 0.045, hcy + hw, cx + S * 0.045, S * 0.70], fill=0)
    # sound block (base)
    d.rounded_rectangle([S * 0.26, S * 0.78, S * 0.74, S * 0.90], radius=S * 0.03, fill=0)
    # block top lip
    d.rectangle([S * 0.30, S * 0.72, S * 0.70, S * 0.78], fill=0)


def bank(d, S):
    cx = S * 0.5
    # pediment (triangle)
    d.polygon([(S * 0.10, S * 0.34), (cx, S * 0.12), (S * 0.90, S * 0.34)], fill=0)
    # architrave
    d.rectangle([S * 0.12, S * 0.34, S * 0.88, S * 0.42], fill=0)
    # columns
    ncol = 4
    top, bot = S * 0.42, S * 0.80
    x0, x1 = S * 0.18, S * 0.82
    cw = S * 0.085
    for i in range(ncol):
        cxx = x0 + (x1 - x0) * i / (ncol - 1)
        d.rectangle([cxx - cw / 2, top, cxx + cw / 2, bot], fill=0)
    # base / steps
    d.rectangle([S * 0.10, S * 0.80, S * 0.90, S * 0.88], fill=0)
    d.rectangle([S * 0.06, S * 0.88, S * 0.94, S * 0.94], fill=0)


def globe(d, S):
    cx, cy = S * 0.5, S * 0.5
    r = S * 0.40
    # sphere
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=0)
    # lat/long curves carved white — thick so they survive downsampling
    w = int(S * 0.035)
    # equator
    d.line([(cx - r, cy), (cx + r, cy)], fill=255, width=w)
    # one latitude above, one below
    for dyr in (-0.5, 0.5):
        yy = cy + r * dyr
        half = math.sqrt(max(0, r * r - (yy - cy) ** 2))
        d.line([(cx - half, yy), (cx + half, yy)], fill=255, width=w)
    # central meridian (vertical)
    d.line([(cx, cy - r), (cx, cy + r)], fill=255, width=w)
    # two curved meridians flanking the center
    d.arc([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r], 90, 270, fill=255, width=w)
    d.arc([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r], 270, 90, fill=255, width=w)


def people(d, S):
    # three overlapping figures: two back, one front center
    def fig(cx, hy, hr, bw, btop, bbot, color=0):
        d.ellipse([cx - hr, hy, cx + hr, hy + 2 * hr], fill=color)
        d.rounded_rectangle([cx - bw, btop, cx + bw, bbot], radius=bw * 0.7, fill=color)

    # back two (slightly higher, smaller)
    fig(S * 0.26, S * 0.18, S * 0.115, S * 0.155, S * 0.38, S * 0.86)
    fig(S * 0.74, S * 0.18, S * 0.115, S * 0.155, S * 0.38, S * 0.86)
    # white halo to separate front figure from the back two
    fig(S * 0.50, S * 0.26, S * 0.175, S * 0.225, S * 0.50, S * 0.94, color=255)
    # front center (larger, lower)
    fig(S * 0.50, S * 0.28, S * 0.14, S * 0.19, S * 0.52, S * 0.90)


def institution(d, S):
    cx = S * 0.5
    # flat roof slab
    d.rectangle([S * 0.10, S * 0.20, S * 0.90, S * 0.30], fill=0)
    # small flag on top
    d.rectangle([cx - S * 0.01, S * 0.08, cx + S * 0.01, S * 0.20], fill=0)
    d.polygon([(cx + S * 0.01, S * 0.09), (cx + S * 0.12, S * 0.12),
               (cx + S * 0.01, S * 0.15)], fill=0)
    # building body
    d.rectangle([S * 0.14, S * 0.30, S * 0.86, S * 0.82], fill=0)
    # windows (white grid)
    for wy in (0.40, 0.56):
        for wx in (0.24, 0.40, 0.56, 0.72):
            d.rectangle([S * wx, S * wy, S * (wx + 0.07), S * (wy + 0.09)], fill=255)
    # door (white)
    d.rectangle([cx - S * 0.06, S * 0.70, cx + S * 0.06, S * 0.82], fill=255)
    # base
    d.rectangle([S * 0.08, S * 0.82, S * 0.92, S * 0.90], fill=0)


def document(d, S):
    # paper as a black-bordered white sheet (so it reads as a page, not a blob)
    left, right = S * 0.22, S * 0.78
    top, bot = S * 0.08, S * 0.92
    fold = S * 0.18
    # black outline shape (with folded top-right corner)
    d.polygon([(left, top), (right - fold, top), (right, top + fold),
               (right, bot), (left, bot)], fill=0)
    # white interior (inset) — thin border so the page reads as a solid sheet
    bi = S * 0.025  # border thickness
    fi = fold
    d.polygon([(left + bi, top + bi), (right - fi - bi * 0.3, top + bi),
               (right - bi, top + fi + bi * 0.3), (right - bi, bot - bi),
               (left + bi, bot - bi)], fill=255)
    # folded corner triangle (black) for the dog-ear
    d.polygon([(right - fi, top), (right - fi, top + fi), (right, top + fi)], fill=0)
    # text lines (black, bold) on the white page
    lw = int(S * 0.03)
    for ly in (0.24, 0.33, 0.42):
        d.line([(left + S * 0.07, S * ly), (right - S * 0.10, S * ly)], fill=0, width=lw)
    # seal (bold black disc with white center) bottom-center
    sx, sy, sr = S * 0.41, S * 0.65, S * 0.12
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=0)
    d.ellipse([sx - sr * 0.40, sy - sr * 0.40, sx + sr * 0.40, sy + sr * 0.40], fill=255)
    # ribbon tails below seal
    d.polygon([(sx - sr * 0.6, sy + sr * 0.55), (sx - sr * 0.0, sy + sr * 0.55),
               (sx - sr * 0.3, S * 0.85)], fill=0)
    d.polygon([(sx + sr * 0.0, sy + sr * 0.55), (sx + sr * 0.6, sy + sr * 0.55),
               (sx + sr * 0.3, S * 0.85)], fill=0)


ICONS = [
    ("Capitol", 21, capitol),
    ("Scales", 21, scales),
    ("BallotBox", 17, ballot_box),
    ("Flag", 17, flag),
    ("Gavel", 17, gavel),
    ("Bank", 19, bank),
    ("Globe", 19, globe),
    ("People", 17, people),
    ("Institution", 19, institution),
    ("Document", 19, document),
]
