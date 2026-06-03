"""Example icon module — template for the silhouette contract.
Each draw_fn(d, S) draws ONE black silhouette on a white SxS canvas.
Use solid fills, thick strokes (>= S*0.05), ~10% margin. Centered.
"""
from PIL import ImageDraw

def person(d, S):
    cx = S * 0.5
    # head
    hr = S * 0.13
    d.ellipse([cx - hr, S * 0.13, cx + hr, S * 0.13 + 2 * hr], fill=0)
    # body (rounded shoulders + torso)
    bw = S * 0.30
    d.rounded_rectangle([cx - bw, S * 0.45, cx + bw, S * 0.92],
                        radius=S * 0.18, fill=0)

def chip(d, S):
    m = S * 0.28
    # body
    d.rounded_rectangle([m, m, S - m, S - m], radius=S * 0.04, fill=0)
    # pins: short black stubs on all four sides
    pin = S * 0.045
    plen = S * 0.10
    for i in range(3):
        off = m + (S - 2 * m) * (i + 1) / 4 - pin / 2
        d.rectangle([off, m - plen, off + pin, m], fill=0)            # top
        d.rectangle([off, S - m, off + pin, S - m + plen], fill=0)    # bottom
        d.rectangle([m - plen, off, m, off + pin], fill=0)           # left
        d.rectangle([S - m, off, S - m + plen, off + pin], fill=0)   # right
    # notch (white) to give chip identity
    nr = S * 0.05
    d.ellipse([m + S*0.04 - nr, m + S*0.04 - nr, m + S*0.04 + nr, m + S*0.04 + nr], fill=255)

def star(d, S):
    import math
    cx, cy = S * 0.5, S * 0.52
    R, r = S * 0.40, S * 0.16
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=0)

ICONS = [
    ("Person", 17, person),
    ("Chip", 17, chip),
    ("Star", 17, star),
]
