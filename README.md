# Dot Grid

Interactive dot-grid art tool, inspired by the Center for Technology & Statecraft logo.
Live: https://konstantinpilz.github.io/dot-grid/

## What it does
- Square grid of equidistant dots (default 6×6, set 1–40 per side).
- Click a dot to grow it one equal step; at the final step dots touch their neighbors; one more click resets.
- Shift-click shrinks a dot one step.
- Black/white toggle, independent dot + background colour pickers, 8 preset palettes.
- Sliders: board size, base dot size, touch gap, margin. Square-dot mode.
- Clear / Fill / Random, plus SVG and 2000px PNG export.

## Pattern library
A curated gallery of 20 abstract, flowing patterns (waves, blobs, spirals, drapes, marble/smoke).
Click a thumbnail to load it; the grid auto-sizes and you can then tweak individual dots.

Each pattern is a deterministic function `(x,y,n,steps) -> level`. The 20 shipped in `index.html`
were curated from ~110 candidates generated across five families. Source candidates and the
build/curation scripts:
- `patterns/*.json` — all 110 candidate generators (waves, blobs, spirals, drapes, flow)
- `compute-grids.js` — evaluates every generator to a level grid
- `montage.py` — renders candidate contact sheets (PIL)
- `extract.js` — pulls the curated 20 into `selected.json`

Everything is a single self-contained `index.html` (no build step, no dependencies).

Drafted by an Opus 4.8 agent team for Konstantin.
