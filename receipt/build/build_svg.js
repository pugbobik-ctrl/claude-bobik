// Write editable SVGs of every strip for Illustrator: receipt/illustrator/svg/
//
//   node receipt/build/build_svg.js
//
// Runs the Illustrator script's own layout engine against ai_dom.js, then writes what it built as
// plain SVG that Illustrator opens with live type: one <text> per line or paragraph set in
// Wix Madefor Display, named groups for paper / type / wordmark / barcode, the caramel swirl as a
// real radial gradient, dashed rules as dashed strokes. No masks, no patterns, no images.
const fs = require('fs');
const path = require('path');
const { runEngine, hex } = require('./ai_dom');

const ROOT = path.join(__dirname, '..');
const JSX = path.join(ROOT, 'illustrator', 'dinner-receipts.jsx');
const OUT = path.join(ROOT, 'illustrator', 'svg');
const src = fs.readFileSync(JSX, 'utf8');
const D = JSON.parse(/var D = (\{.*\});\n/.exec(src)[1]);
const { doc } = runEngine(src);

const PS = { 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold' };
const n = (v) => +v.toFixed(2);
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function build(layer, ab) {
  const ox = ab.artboardRect[0], oy = ab.artboardRect[1];
  const X = (x) => n(x - ox), Y = (y) => n(oy - y);
  const used = {};
  let defs = '';
  const id = (name) => {
    let base = String(name).replace(/[^A-Za-z0-9]+/g, '_').replace(/^_|_$/g, '') || 'item';
    if (/^[0-9]/.test(base)) base = 'n' + base;   // XML ids cannot start with a digit
    used[base] = (used[base] || 0) + 1;
    return used[base] > 1 ? `${base}_${used[base]}` : base;
  };

  function pathD(p) {
    const P = p.points;
    if (!P.length) return '';
    let s = `M${X(P[0].anchor[0])} ${Y(P[0].anchor[1])}`;
    const seg = (a, b) => {
      const straight = a.rightDirection === a.anchor && b.leftDirection === b.anchor;
      return straight ? `L${X(b.anchor[0])} ${Y(b.anchor[1])}`
        : `C${X(a.rightDirection[0])} ${Y(a.rightDirection[1])} ${X(b.leftDirection[0])} ${Y(b.leftDirection[1])} ${X(b.anchor[0])} ${Y(b.anchor[1])}`;
    };
    for (let i = 1; i < P.length; i++) s += seg(P[i - 1], P[i]);
    if (p.closed) s += seg(P[P.length - 1], P[0]) + 'Z';
    return s;
  }

  function font(w) {
    return `font-family="WixMadeforDisplay-${PS[w]}, 'Wix Madefor Display', sans-serif" font-weight="${w}"`;
  }

  // split a frame's characters into runs of identical styling
  function runs(t, a, b) {
    const out = [];
    for (let i = a; i < b; i++) {
      let ch = t._contents[i];
      if (t.attr(i, 'capitalization') === 'ALLCAPS') ch = ch.toUpperCase();
      const st = {
        w: t.weight(i), size: n(t.attr(i, 'size')),
        ls: n((t.attr(i, 'tracking') || 0) / 1000 * t.attr(i, 'size')),
        bs: n(t.attr(i, 'baselineShift') || 0),
      };
      const last = out[out.length - 1];
      if (last && last.w === st.w && last.size === st.size && last.ls === st.ls && last.bs === st.bs) last.s += ch;
      else out.push(Object.assign(st, { s: ch }));
    }
    return out;
  }
  const runAttrs = (r, base) => [
    r.w !== base.w ? font(r.w) : '',
    r.size !== base.size ? `font-size="${r.size}"` : '',
    r.ls !== base.ls ? `letter-spacing="${r.ls}"` : '',
    r.bs ? `baseline-shift="${r.bs}"` : '',
  ].filter(Boolean).join(' ');

  function text(t) {
    const fill = hex(t.base.fillColor);
    const anchor = { LEFT: 'start', RIGHT: 'end', CENTER: 'middle' }[t.just];
    if (t.tkind === 'area') {
      const lines = t.wrap(), lh = t.base.leading;
      const x = X(t.at[0] + t.dx), y0 = Y(t.at[1] + t.dy) + (t.firstBaselineMin || 0);
      const all = runs(t, 0, t._contents.length);
      const base = all[0];
      let body = '';
      lines.forEach(([a, b], k) => {
        runs(t, a, b).forEach((r, j) => {
          const pos = j === 0 ? ` x="${x}" y="${n(y0 + k * lh)}"` : '';
          const at = runAttrs(r, base);
          body += `<tspan${pos}${at ? ' ' + at : ''}>${esc(r.s)}</tspan>`;
        });
      });
      return `<text id="${id('flow')}" ${font(base.w)} font-size="${base.size}" letter-spacing="${base.ls}" fill="${fill}">${body}</text>`;
    }
    const rs = runs(t, 0, t._contents.length), base = rs[0];
    const x = X(t.at[0] + t.dx), y = Y(t.at[1] + t.dy);
    const rot = t.rot ? ` transform="rotate(90 ${x} ${y})"` : '';
    const body = rs.length === 1 && !base.bs ? esc(base.s)
      : rs.map((r) => { const at = runAttrs(r, base); return `<tspan${at ? ' ' + at : ''}>${esc(r.s)}</tspan>`; }).join('');
    const label = t._contents.replace(/\s+/g, ' ').slice(0, 24);
    return `<text id="${id(label)}" x="${x}" y="${y}" ${font(base.w)} font-size="${base.size}"` +
      `${base.ls ? ` letter-spacing="${base.ls}"` : ''} text-anchor="${anchor}" fill="${fill}"${rot}>${body}</text>`;
  }

  // the swirl: instead of blurred rings, a radial gradient with the same stops, on the paper itself
  function swirl(g) {
    const clip = g.children.find((c) => c.clipping);
    const b = clip.bounds(), W = b[2] - b[0], H = b[1] - b[3];
    const k = W / D.px, cx = X(b[0] - 0.45 * W), cy = Y(b[1] + 0.06 * H);
    const R = D.rings, rmax = R[R.length - 1][1] * k;
    const gid = id('caramel');
    defs += `<radialGradient id="${gid}" gradientUnits="userSpaceOnUse" cx="${cx}" cy="${cy}" r="${n(rmax)}">` +
      R.map(([c, r]) => `<stop offset="${n(r * k / rmax)}" stop-color="${c}"/>`).join('') + '</radialGradient>';
    return `<path id="${id('paper')}" d="${pathD(clip)}" fill="url(#${gid})"/>`;
  }

  function item(it) {
    if (it.kind === 'group' || it.kind === 'layer') {
      if (it.name === 'Caramel swirl') return swirl(it);
      const kids = [...it.children].reverse().map(item).join('');
      return `<g id="${id(it.name || 'group')}">${kids}</g>`;
    }
    if (it.kind === 'path') {
      if (it.ellipse) return '';
      const fill = it.filled ? hex(it.fillColor) : 'none';
      let s = '';
      if (it.stroked) {
        s = ` stroke="${hex(it.strokeColor)}" stroke-width="${n(it.strokeWidth)}"`;
        if (it.strokeDashes) s += ` stroke-dasharray="${it.strokeDashes.map(n).join(' ')}"`;
        if (it.strokeCap) s += ' stroke-linecap="round"';
      }
      const op = it.opacity !== 100 ? ` opacity="${it.opacity / 100}"` : '';
      const name = it.closed && it.filled && !it.stroked && it.points.length > 8 ? id('paper') : id(it.stroked ? 'rule' : 'shape');
      return `<path id="${name}" d="${pathD(it)}" fill="${fill}"${s}${op}/>`;
    }
    if (it.kind === 'compound') {
      return `<path id="${id(it.name || 'compound')}" fill-rule="evenodd" fill="${hex(it.paths[0].fillColor)}" d="${it.paths.map(pathD).join('')}"/>`;
    }
    if (it.kind === 'text') return text(it);
    return '';
  }

  const body = [...layer.children].reverse().map(item).join('\n  ');
  const r = ab.artboardRect, W = n(r[2] - r[0]), H = n(r[1] - r[3]);
  return { W, H, defs, body, name: layer.name };
}

fs.mkdirSync(OUT, { recursive: true });
const layers = [...doc.layers].reverse();
const parts = layers.map((l) => build(l, doc.artboards.find((a) => a.name === l.name)));
const head = (W, H) => `<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="${W}pt" height="${H}pt" viewBox="0 0 ${W} ${H}">\n`;
for (const p of parts) {
  fs.writeFileSync(path.join(OUT, `${p.name}.svg`),
    head(p.W, p.H) + `<defs>${p.defs}</defs>\n<g id="${p.name}">\n  ${p.body}\n</g>\n</svg>\n`);
  console.log('wrote', p.name + '.svg', Math.round(p.W / 72 * 25.4) + '×' + Math.round(p.H / 72 * 25.4) + 'mm');
}
