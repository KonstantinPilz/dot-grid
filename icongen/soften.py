"""Regenerate icon grids with softer, more organic edges + gentle noise,
so icons feather into the dot field instead of sitting on a hard empty
background. Deterministic (no RNG) so the baked grids are stable.

Pipeline per icon:
  1. draw silhouette at high res, Gaussian-blur it -> soft coverage
  2. lift the empty background to a faint base so it carries small dots
  3. add smooth low-frequency "flow" noise + a little fine grain,
     damped inside the solid core to keep the shape readable
  4. round to levels 0..6
"""
import os, sys, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render

STEPS = 6
S = 480

def sample_cov(draw_fn, n, blur_frac=0.013):
    img = Image.new("L", (S, S), 255)
    d = ImageDraw.Draw(img)
    draw_fn(d, S)
    img = img.filter(ImageFilter.GaussianBlur(radius=S * blur_frac))
    small = img.resize((n, n), Image.BOX)
    arr = np.asarray(small, dtype=np.float64)
    return (255.0 - arr) / 255.0           # coverage 0..1, shape (n,n)

def noise_field(n):
    """Deterministic smooth noise ~[-1,1]: a few low-freq sinusoids (flow)
    plus one finer component (grain). Same for every icon, so the texture
    reads as a consistent 'paper'."""
    ys, xs = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    # (freq_x rad/cell, freq_y rad/cell, phase, weight)
    comps = [
        (0.42, 0.55, 0.0, 1.00),
        (0.70, -0.38, 1.7, 0.70),
        (-0.30, 0.85, 3.1, 0.55),
        (1.05, 0.95, 0.6, 0.40),
        (1.70, -1.45, 2.3, 0.22),   # finer grain
    ]
    f = np.zeros((n, n))
    wsum = 0.0
    for fx, fy, ph, w in comps:
        f += w * np.sin(xs * fx + ys * fy + ph)
        wsum += w
    return f / wsum                        # ~[-1,1]

def soften(cov, n, amp=0.11, bg=0.075, flow=0.55):
    nz = noise_field(n)
    # lift background: empty areas rise to ~bg, solid stays ~cov
    field = cov + bg * (1.0 - cov)
    # noise: full strength in background, damped in the solid core
    damp = 1.0 - 0.55 * cov
    field = field + nz * amp * damp
    # a touch of low-freq flow warps overall brightness for an organic feel
    field = field + (nz * flow * 0.04)
    field = np.clip(field, 0.0, 1.0)
    lv = np.rint(field * STEPS).astype(int)
    return np.clip(lv, 0, STEPS)

def build(amp=0.11, bg=0.075, preview_only=False):
    items = render._load_modules()
    out = []
    for theme, name, n, draw_fn in items:
        cov = sample_cov(draw_fn, n)
        lv = soften(cov, n, amp=amp, bg=bg)
        out.append({"name": name, "theme": theme, "n": n, "steps": STEPS,
                    "grid": lv.flatten().tolist()})
    if not preview_only:
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "icons.json"), "w") as f:
            json.dump(out, f)
    render.preview_grids(out, "/tmp/icons_soft.png",
                         title=f"softened (amp={amp}, bg={bg})", cols=5, tile=150)
    print(f"built {len(out)} softened icons -> /tmp/icons_soft.png"
          + ("" if preview_only else " + icons.json"))
    return out

if __name__ == "__main__":
    amp = float(sys.argv[1]) if len(sys.argv) > 1 else 0.11
    bg = float(sys.argv[2]) if len(sys.argv) > 2 else 0.075
    po = "--write" not in sys.argv
    build(amp=amp, bg=bg, preview_only=po)
