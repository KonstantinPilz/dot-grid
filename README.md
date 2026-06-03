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

## Icon library
A curated gallery of 20 recognizable icons rendered in the soft dot ("flowy") style —
technology & statecraft themed: Person, People, Capitol, Globe, Flag, Scales, Microchip, CPU,
Robot, Server, Network, Rocket, Monitor, Brain, Lightbulb, Gear, Shield, Eye, Lightning, Star.
Click a thumbnail to load it; the grid auto-sizes (17–21 per side) and you can then tweak colors
or click individual dots.

Each icon is an explicit `grid` of dot levels (0–6). They were produced by drawing each icon as a
high-res silhouette with PIL, then area-downsampling to an N×N ink-coverage grid (filled→big dot,
edge→mid, empty→tiny) — giving the soft halftone look. Curated from ~43 candidates. Pipeline:
- `icongen/render.py` — silhouette→dot-grid harness (sampling + contact sheets)
- `icongen/icons_*.py` — PIL silhouette drawings (statecraft, tech, ai, objects)
- `icongen/icons.json` — all sampled candidate grids

An earlier abstract-pattern library (waves/blobs/spirals/etc., generated as math functions) lives in
`patterns/*.json` with its build scripts (`compute-grids.js`, `montage.py`, `extract.js`); the page's
loader still supports those function-based patterns alongside the explicit icon grids.

Everything is a single self-contained `index.html` (no build step, no dependencies).

Drafted by an Opus 4.8 agent team for Konstantin.
