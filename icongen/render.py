"""Shared harness: turn PIL silhouette drawings into dot-grid icons.

An icon module is a file `icons_<theme>.py` in this directory exposing:
    ICONS = [(name:str, n:int, draw_fn), ...]
where draw_fn(d, S) draws ONE black silhouette on a white SxS PIL image
(d is an ImageDraw). Solid filled shapes read best. Keep ~8-12% margin.

Sampling: the SxS image is area-averaged down to n x n; each cell's ink
coverage (0..1) maps to a dot level 0..6. So a filled cell -> big dot,
empty -> tiny dot, edges -> mid (the soft "flowy" halftone look).
"""
import os, json, math, importlib.util
from PIL import Image, ImageDraw, ImageFont

STEPS = 6
S = 480                      # high-res canvas for crisp anti-aliased edges
BG = (231, 227, 216)        # CTS paper
DOT = (92, 83, 71)          # CTS ink

def sample_grid(draw_fn, n, s=S):
    img = Image.new("L", (s, s), 255)      # white bg, black ink
    d = ImageDraw.Draw(img)
    draw_fn(d, s)
    small = img.resize((n, n), Image.BOX)  # area-average -> coverage
    px = small.load()
    grid = []
    for y in range(n):
        for x in range(n):
            frac = (255 - px[x, y]) / 255.0
            lv = round(frac * STEPS)
            grid.append(max(0, min(STEPS, lv)))
    return grid

def render_dots(grid, n, cell=26, bg=BG, dot=DOT, base=0.16):
    size = n * cell
    img = Image.new("RGB", (size, size), bg)
    dr = ImageDraw.Draw(img)
    for y in range(n):
        for x in range(n):
            lv = grid[y * n + x]
            frac = base + (lv / STEPS) * (1 - base)
            r = frac * cell / 2
            cx = (x + 0.5) * cell
            cy = (y + 0.5) * cell
            dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=dot)
    return img

def _font(sz=13):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", sz)
    except Exception:
        return ImageFont.load_default()

def preview(icons, outpath, title="", cols=5, tile=150):
    """Render a labeled contact sheet of dot-icons for visual QA."""
    rows = math.ceil(len(icons) / cols)
    PAD, LBL = 8, 18
    W = cols * tile + (cols + 1) * PAD
    H = rows * (tile + LBL + PAD) + PAD + (24 if title else 0)
    page = Image.new("RGB", (W, H), (40, 40, 40))
    pd = ImageDraw.Draw(page)
    y0 = 0
    if title:
        pd.text((PAD, 5), title, fill=(255, 255, 255), font=_font(15)); y0 = 24
    for i, (name, n, draw_fn) in enumerate(icons):
        grid = sample_grid(draw_fn, n)
        dots = render_dots(grid, n).resize((tile, tile), Image.LANCZOS)
        c, r = i % cols, i // cols
        x = PAD + c * (tile + PAD)
        yy = y0 + PAD + r * (tile + LBL + PAD)
        page.paste(dots, (x, yy))
        pd.text((x + 2, yy + tile + 2), f"{name} [n{n}]", fill=(230, 230, 230), font=_font(12))
    page.save(outpath)
    return outpath

def _load_modules():
    here = os.path.dirname(os.path.abspath(__file__))
    mods = []
    for f in sorted(os.listdir(here)):
        if f.startswith("icons_") and f.endswith(".py"):
            spec = importlib.util.spec_from_file_location(f[:-3], os.path.join(here, f))
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            for tup in getattr(m, "ICONS", []):
                mods.append((f[:-3],) + tuple(tup))
    return mods

def preview_grids(items, outpath, title="", cols=6, tile=150):
    """items: list of dicts with name,n,grid. Renders a labeled contact sheet."""
    rows = math.ceil(len(items) / cols)
    PAD, LBL = 8, 18
    W = cols * tile + (cols + 1) * PAD
    H = rows * (tile + LBL + PAD) + PAD + (24 if title else 0)
    page = Image.new("RGB", (W, H), (40, 40, 40))
    pd = ImageDraw.Draw(page)
    y0 = 24 if title else 0
    if title:
        pd.text((PAD, 5), title, fill=(255, 255, 255), font=_font(15))
    for i, d in enumerate(items):
        dots = render_dots(d["grid"], d["n"]).resize((tile, tile), Image.LANCZOS)
        c, r = i % cols, i // cols
        x = PAD + c * (tile + PAD)
        yy = y0 + PAD + r * (tile + LBL + PAD)
        page.paste(dots, (x, yy))
        lab = f"{i}. {d['name']}"
        pd.text((x + 2, yy + tile + 2), lab, fill=(230, 230, 230), font=_font(12))
    page.save(outpath)
    return outpath

def build_all():
    items = _load_modules()
    out = []
    for theme, name, n, draw_fn in items:
        out.append({"name": name, "theme": theme, "n": n, "steps": STEPS,
                    "grid": sample_grid(draw_fn, n)})
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "icons.json"), "w") as f:
        json.dump(out, f)
    preview_grids(out, "/tmp/icons_contact.png", title=f"{len(out)} icon candidates")
    print(f"built {len(out)} icons -> icons.json + /tmp/icons_contact.png")
    return out

if __name__ == "__main__":
    build_all()
