// Validate every candidate pattern and render a contact sheet HTML of SVG thumbnails.
const fs = require('fs');
const path = require('path');
const dir = path.join(__dirname, 'patterns');
const files = ['waves.json','blobs.json','spirals.json','drapes.json','flow.json'];

function renderSVG(p, eval_fn, px) {
  const n = p.n, s = p.steps;
  const pad = 0.5;
  const view = n + pad * 2;
  const base = 0.18; // base diameter fraction for thumbnail
  let circles = '';
  let levelsSeen = new Set();
  let bad = null;
  for (let y = 0; y < n; y++) {
    for (let x = 0; x < n; x++) {
      let lv;
      try { lv = eval_fn(x, y, n, s); } catch (e) { bad = 'throw: ' + e.message; lv = 0; }
      if (typeof lv !== 'number' || !isFinite(lv)) { bad = 'nonfinite'; lv = 0; }
      lv = Math.max(0, Math.min(s, Math.round(lv)));
      levelsSeen.add(lv);
      const frac = base + (lv / s) * (1 - base);
      const cx = pad + x + 0.5, cy = pad + y + 0.5, r = frac / 2;
      circles += `<circle cx="${cx.toFixed(3)}" cy="${cy.toFixed(3)}" r="${r.toFixed(3)}"/>`;
    }
  }
  return { svg: `<svg viewBox="0 0 ${view} ${view}" width="${px}" height="${px}"><rect width="${view}" height="${view}" fill="#e7e3d8"/><g fill="#5c5347">${circles}</g></svg>`,
           spread: levelsSeen.size, bad };
}

let items = [];
for (const f of files) {
  const arr = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
  const theme = f.replace('.json','');
  for (const p of arr) {
    let fn;
    try { fn = eval('(' + p.code + ')'); } catch (e) { items.push({ ...p, theme, bad: 'parse: '+e.message, spread:0, svg:'' }); continue; }
    const r = renderSVG(p, fn, 150);
    items.push({ ...p, theme, ...r });
  }
}

// report
const flagged = items.filter(i => i.bad || i.spread < 3);
console.log(`Total candidates: ${items.length}`);
console.log(`Flagged (error or spread<3): ${flagged.length}`);
flagged.forEach(i => console.log(`  [${i.theme}] ${i.name}: ${i.bad || 'spread='+i.spread}`));

// contact sheet
const cards = items.map((i, idx) => `
  <div class="card${(i.bad||i.spread<3)?' flag':''}">
    ${i.svg || '<div class=err>ERR</div>'}
    <div class="lbl"><b>${idx}</b> ${i.name} <span class="th">${i.theme} · n${i.n} · sp${i.spread}</span></div>
  </div>`).join('');

const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{margin:0;background:#3a3a3a;font-family:system-ui;padding:16px}
.grid{display:grid;grid-template-columns:repeat(8,1fr);gap:10px}
.card{background:#fff;border-radius:8px;overflow:hidden;border:3px solid transparent}
.card.flag{border-color:#e63946}
.card svg{display:block;width:100%;height:auto}
.lbl{font-size:11px;padding:4px 6px;color:#222;line-height:1.3}
.lbl b{color:#888;margin-right:4px}
.th{display:block;color:#999;font-size:9px}
.err{height:150px;display:flex;align-items:center;justify-content:center;color:red}
</style></head><body><div class="grid">${cards}</div></body></html>`;

fs.writeFileSync(path.join(__dirname, 'contact.html'), html);
console.log('Wrote contact.html');
