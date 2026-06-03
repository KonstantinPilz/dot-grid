"""AI & abstract-concept icons as dot-grid silhouettes.
Each draw_fn(d, S) draws ONE black silhouette on a white SxS canvas.
Solid fills, thick strokes (>= S*0.06), ~10% margin, centered.
"""
import math
from PIL import ImageDraw


def brain(d, S):
    cx, cy = S * 0.5, S * 0.5
    # rounded brain blob (wider than tall)
    d.rounded_rectangle([S * 0.12, S * 0.20, S * 0.88, S * 0.80],
                        radius=S * 0.30, fill=0)
    # central vertical cleft (white) splitting hemispheres
    d.line([(cx, S * 0.22), (cx, S * 0.78)], fill=255, width=int(S * 0.05))
    # white fold curves, mirrored left/right
    w = int(S * 0.045)
    # left hemisphere folds
    d.arc([S * 0.16, S * 0.28, S * 0.46, S * 0.52], 30, 200, fill=255, width=w)
    d.arc([S * 0.16, S * 0.48, S * 0.46, S * 0.72], 160, 330, fill=255, width=w)
    # right hemisphere folds
    d.arc([S * 0.54, S * 0.28, S * 0.84, S * 0.52], 340, 150, fill=255, width=w)
    d.arc([S * 0.54, S * 0.48, S * 0.84, S * 0.72], 210, 20, fill=255, width=w)


def lightbulb(d, S):
    cx = S * 0.5
    # bulb (circle)
    br = S * 0.30
    d.ellipse([cx - br, S * 0.12, cx + br, S * 0.12 + 2 * br], fill=0)
    # neck connecting bulb to base
    d.rectangle([cx - S * 0.14, S * 0.62, cx + S * 0.14, S * 0.72], fill=0)
    # screw base
    d.rounded_rectangle([cx - S * 0.13, S * 0.70, cx + S * 0.13, S * 0.88],
                        radius=S * 0.03, fill=0)
    # base grooves (white lines)
    w = int(S * 0.018)
    for yy in (0.745, 0.79, 0.835):
        d.line([(cx - S * 0.13, S * yy), (cx + S * 0.13, S * yy)],
               fill=255, width=w)


def eye(d, S):
    cx, cy = S * 0.5, S * 0.5
    # almond outline: two arcs forming a thick lens, filled
    # build almond as union of two chords
    top = [S * 0.08, S * 0.12, S * 0.92, S * 0.88]
    bot = [S * 0.08, S * 0.12, S * 0.92, S * 0.88]
    d.chord(top, 180, 360, fill=0)   # upper lid
    d.chord(bot, 0, 180, fill=0)     # lower lid
    # white interior almond (smaller) to leave thick outline
    inset = S * 0.05
    ti = [S * 0.08 + inset, S * 0.12 + inset * 1.4,
          S * 0.92 - inset, S * 0.88 - inset * 1.4]
    d.chord(ti, 180, 360, fill=255)
    d.chord(ti, 0, 180, fill=255)
    # iris + pupil
    ir = S * 0.18
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=0)
    pr = S * 0.07
    d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=255)


def atom(d, S):
    cx, cy = S * 0.5, S * 0.5
    w = int(S * 0.05)
    # three elliptical orbits rotated
    rx, ry = S * 0.40, S * 0.16
    for ang in (0, 60, 120):
        # approximate rotated ellipse with a polygon outline (thick)
        pts = []
        a = math.radians(ang)
        for t in range(0, 361, 8):
            tr = math.radians(t)
            ex = rx * math.cos(tr)
            ey = ry * math.sin(tr)
            x = cx + ex * math.cos(a) - ey * math.sin(a)
            y = cy + ex * math.sin(a) + ey * math.cos(a)
            pts.append((x, y))
        d.line(pts, fill=0, width=w, joint="curve")
    # nucleus
    nr = S * 0.10
    d.ellipse([cx - nr, cy - nr, cx + nr, cy + nr], fill=0)


def gear(d, S):
    cx, cy = S * 0.5, S * 0.5
    teeth = 8
    Rout = S * 0.46
    Rin = S * 0.34
    # build toothed polygon: each tooth = flat-topped trapezoid
    pts = []
    per = 2 * math.pi / teeth
    tooth_w = 0.46   # fraction of the period the outer tooth occupies
    for i in range(teeth):
        base = i * per
        a0 = base - tooth_w / 2 * per
        a1 = base + tooth_w / 2 * per
        a2 = base + per - tooth_w / 2 * per
        # rise to tooth (outer), across top, fall to valley (inner)
        pts.append((cx + Rout * math.cos(a0), cy + Rout * math.sin(a0)))
        pts.append((cx + Rout * math.cos(a1), cy + Rout * math.sin(a1)))
        pts.append((cx + Rin * math.cos(a1), cy + Rin * math.sin(a1)))
        pts.append((cx + Rin * math.cos(a2), cy + Rin * math.sin(a2)))
    d.polygon(pts, fill=0)
    # solid body circle to clean center
    d.ellipse([cx - Rin, cy - Rin, cx + Rin, cy + Rin], fill=0)
    # center hole (white)
    hr = S * 0.14
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=255)


def lightning(d, S):
    # bold zigzag bolt
    pts = [
        (S * 0.56, S * 0.08),
        (S * 0.24, S * 0.54),
        (S * 0.46, S * 0.54),
        (S * 0.40, S * 0.92),
        (S * 0.78, S * 0.40),
        (S * 0.54, S * 0.40),
    ]
    d.polygon(pts, fill=0)


def cloud(d, S):
    cy = S * 0.58
    # several overlapping circles + base
    d.ellipse([S * 0.10, cy - S * 0.12, S * 0.42, cy + S * 0.20], fill=0)
    d.ellipse([S * 0.26, S * 0.26, S * 0.62, S * 0.62], fill=0)
    d.ellipse([S * 0.48, S * 0.34, S * 0.76, S * 0.62], fill=0)
    d.ellipse([S * 0.62, cy - S * 0.10, S * 0.90, cy + S * 0.20], fill=0)
    # flat base
    d.rounded_rectangle([S * 0.16, cy + S * 0.02, S * 0.84, cy + S * 0.20],
                        radius=S * 0.08, fill=0)


def shield(d, S):
    # heraldic shield silhouette
    pts = [
        (S * 0.5, S * 0.10),
        (S * 0.86, S * 0.22),
        (S * 0.86, S * 0.52),
        (S * 0.5, S * 0.90),
        (S * 0.14, S * 0.52),
        (S * 0.14, S * 0.22),
    ]
    d.polygon(pts, fill=0)
    # white checkmark
    w = int(S * 0.08)
    d.line([(S * 0.32, S * 0.48), (S * 0.45, S * 0.62),
            (S * 0.70, S * 0.30)], fill=255, width=w, joint="curve")


def padlock(d, S):
    cx = S * 0.5
    # shackle: thick arc
    w = int(S * 0.10)
    d.arc([cx - S * 0.22, S * 0.14, cx + S * 0.22, S * 0.58],
          180, 360, fill=0, width=w)
    # vertical legs of shackle down to body
    lx = cx - S * 0.22   # left arc centerline x
    rx = cx + S * 0.22   # right arc centerline x
    d.rectangle([lx - w / 2, S * 0.36, lx + w / 2, S * 0.50], fill=0)
    d.rectangle([rx - w / 2, S * 0.36, rx + w / 2, S * 0.50], fill=0)
    # body
    d.rounded_rectangle([cx - S * 0.30, S * 0.46, cx + S * 0.30, S * 0.88],
                        radius=S * 0.06, fill=0)
    # keyhole (white)
    kr = S * 0.06
    d.ellipse([cx - kr, S * 0.58, cx + kr, S * 0.58 + 2 * kr], fill=255)
    d.polygon([(cx - kr * 0.5, S * 0.66), (cx + kr * 0.5, S * 0.66),
               (cx + kr * 0.9, S * 0.80), (cx - kr * 0.9, S * 0.80)], fill=255)


def magnifier(d, S):
    # lens
    cx, cy = S * 0.42, S * 0.40
    rout = S * 0.28
    d.ellipse([cx - rout, cy - rout, cx + rout, cy + rout], fill=0)
    rin = S * 0.18
    d.ellipse([cx - rin, cy - rin, cx + rin, cy + rin], fill=255)
    # thick handle
    w = int(S * 0.14)
    d.line([(cx + rout * 0.72, cy + rout * 0.72),
            (S * 0.86, S * 0.86)], fill=0, width=w)


ICONS = [
    ("Brain", 17, brain),
    ("Lightbulb", 17, lightbulb),
    ("Eye", 17, eye),
    ("Atom", 21, atom),
    ("Gear", 19, gear),
    ("Lightning", 17, lightning),
    ("Cloud", 17, cloud),
    ("Shield", 17, shield),
    ("Padlock", 17, padlock),
    ("Magnifier", 17, magnifier),
]
