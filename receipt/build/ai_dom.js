// A small stand-in for Illustrator's scripting DOM, just enough to run engine.jsx in node.
// build_svg.js uses it to lay the strips out exactly as the Illustrator script does and then
// writes what was built as plain SVG. Text is measured with the font's advance widths.
const fs = require('fs');
const path = require('path');
const ADV = JSON.parse(fs.readFileSync(path.join(__dirname, 'advances.json')));

const E = (names) => Object.fromEntries(names.map(n => [n, n]));
global.DocumentColorSpace = E(['RGB', 'CMYK']);
global.ColorModel = E(['PROCESS', 'SPOT']);
global.AutoKernType = E(['AUTO', 'OPTICAL', 'NOAUTOKERN']);
global.FontCapsOption = E(['ALLCAPS', 'NORMALCAPS']);
global.Justification = E(['LEFT', 'RIGHT', 'CENTER']);
global.FirstBaselineType = E(['FIXED', 'ASCENT', 'LEADING']);
global.ElementPlacement = E(['PLACEATBEGINNING', 'PLACEATEND']);
global.Transformation = E(['DOCUMENTORIGIN']);
global.PointType = E(['SMOOTH', 'CORNER']);
global.StrokeCap = E(['ROUNDENDCAP']);
global.RGBColor = function () { this.red = 0; this.green = 0; this.blue = 0; };
global.SpotColor = function () { this.spot = null; this.tint = 100; };
const calls = { effects: 0 };

function hex(c) {
  if (!c) return 'none';
  if (c.spot) c = c.spot.color;
  const h = (v) => ('0' + Math.round(v).toString(16)).slice(-2);
  return '#' + h(c.red) + h(c.green) + h(c.blue);
}

class Font { constructor(name) { this.name = name; this.weight = { Regular: 400, Medium: 500, SemiBold: 600, Bold: 700, ExtraBold: 800 }[name.split('-')[1]]; } }
const fontsOK = true;

class Container {
  constructor(parent) {
    this.parent = parent; this.children = [];
    const self = this;
    this.textFrames = {
      pointText: (pt) => self.add(new TextFrame(self, 'point', pt)),
      areaText: (path) => { const t = new TextFrame(self, 'area', [path.left, path.top]); t.textPath = path; path.remove(); t.textPath.parent = null; return self.add(t); },
    };
    this.pathItems = {
      add: () => self.add(new PathItem(self)),
      rectangle: (top, left, w, h) => { const p = new PathItem(self); p.setEntirePath([[left, top], [left + w, top], [left + w, top - h], [left, top - h]]); p.closed = true; p.filled = true; return self.add(p); },
      ellipse: (top, left, w, h) => { const p = new PathItem(self); p.ellipse = [left, top, w, h]; p.filled = true; return self.add(p); },
    };
    this.compoundPathItems = { add: () => self.add(new Compound(self)) };
    this.groupItems = { add: () => self.add(new Group(self)) };
  }
  add(c) { this.children.unshift(c); c.parent = this; return c; } // new items go on top
  get pageItems() { return this.children; }
}
class Item {
  constructor(parent) { this.parent = parent; this.opacity = 100; }
  remove() { if (this.parent) this.parent.children = this.parent.children.filter(c => c !== this); this.parent = null; }
  move(target, where) { this.remove(); this.parent = target; if (where === 'PLACEATEND') target.children.push(this); else target.children.unshift(this); }
  applyEffect(xml) { this.blur = parseFloat(/blur ([\d.]+)/.exec(xml)[1]); calls.effects++; }
}
class Group extends Container { constructor(p) { super(p); this.opacity = 100; this.kind = 'group'; } }
Object.getOwnPropertyNames(Item.prototype).forEach(k => { if (k !== 'constructor') Group.prototype[k] = Item.prototype[k]; });
class Layer extends Container { constructor(p) { super(p); this.kind = 'layer'; } remove() { doc.layers.list = doc.layers.list.filter(l => l !== this); } }

class Pt {
  constructor(a) { this.anchor = a; this.leftDirection = a; this.rightDirection = a; }
}
class PathItem extends Item {
  constructor(p) { super(p); this.kind = 'path'; this.points = []; this.stroked = false; this.filled = false; }
  setEntirePath(a) { this.points = a.map(x => new Pt(x)); }
  get pathPoints() { return this.points; }
  bounds() {
    if (this.ellipse) { const [l, t, w, h] = this.ellipse; return [l, t, l + w, t - h]; }
    const xs = this.points.map(p => p.anchor[0]), ys = this.points.map(p => p.anchor[1]);
    return [Math.min(...xs), Math.max(...ys), Math.max(...xs), Math.min(...ys)];
  }
  get left() { return this.bounds()[0]; } get top() { return this.bounds()[1]; }
  get height() { const b = this.bounds(); return b[1] - b[3]; }
  set height(h) { const b = this.bounds(); const top = b[1]; this.points.forEach(p => { if (Math.abs(p.anchor[1] - top) > 1e-6) p.anchor = [p.anchor[0], top - h]; p.leftDirection = p.rightDirection = p.anchor; }); }
  get width() { const b = this.bounds(); return b[2] - b[0]; }
  d() {
    if (this.ellipse) return null;
    const P = this.points; if (!P.length) return '';
    let s = `M${P[0].anchor[0]} ${-P[0].anchor[1]}`;
    const seg = (a, b) => `C${a.rightDirection[0]} ${-a.rightDirection[1]} ${b.leftDirection[0]} ${-b.leftDirection[1]} ${b.anchor[0]} ${-b.anchor[1]}`;
    for (let i = 1; i < P.length; i++) s += seg(P[i - 1], P[i]);
    if (this.closed) s += seg(P[P.length - 1], P[0]) + 'Z';
    return s;
  }
}
class Compound extends Item {
  constructor(p) { super(p); this.kind = 'compound'; const self = this; this.paths = []; this.pathItems = { add: () => { const q = new PathItem(self); self.paths.push(q); return q; } }; }
}

const ATTR_KEYS = ['textFont', 'size', 'leading', 'tracking', 'capitalization', 'fillColor', 'baselineShift'];
class TextFrame extends Item {
  constructor(p, kind, at) {
    super(p); this.kind = 'text'; this.tkind = kind; this.at = at; this._contents = ''; this.base = {}; this.per = []; this.just = 'LEFT'; this.rot = 0; this.dx = 0; this.dy = 0;
    const self = this;
    this.textRange = { get characterAttributes() { return self.attrProxy(null); }, paragraphAttributes: { set justification(j) { self.just = j; }, get justification() { return self.just; } } };
  }
  set contents(s) { this._contents = s; this.per = [...s].map(() => ({})); }
  get contents() { return this._contents; }
  attrProxy(idx, len = 1) {
    const self = this;
    return new Proxy({}, {
      set(_, k, v) { if (idx === null) { self.base[k] = v; self.per.forEach(o => delete o[k]); } else for (let i = idx; i < idx + len; i++) self.per[i][k] = v; return true; },
      get(_, k) { return idx === null ? self.base[k] : (self.per[idx][k] ?? self.base[k]); },
    });
  }
  get characters() {
    const self = this;
    return new Proxy({ length: this.per.length }, {
      get(t, k) {
        if (k === 'length') return self.per.length;
        const i = +k; let len = 1;
        const r = { start: i, get length() { return len; }, set length(v) { len = v; }, get characterAttributes() { return self.attrProxy(i, len); } };
        return r;
      },
    });
  }
  attr(i, k) { return this.per[i] && this.per[i][k] !== undefined ? this.per[i][k] : this.base[k]; }
  weight(i) { const f = this.attr(i, 'textFont'); return f ? f.weight : 400; }
  adv(i) {
    let ch = this._contents[i]; if (this.attr(i, 'capitalization') === 'ALLCAPS') ch = ch.toUpperCase();
    const a = (ADV[this.weight(i)][ch] ?? 600) / 1000 * this.attr(i, 'size');
    return a + (this.attr(i, 'tracking') || 0) / 1000 * this.attr(i, 'size');
  }
  textWidth(a = 0, b = this._contents.length) { let w = 0; for (let i = a; i < b; i++) w += this.adv(i); return w; }
  wrap() {
    const W = this.textPath.width, s = this._contents, lines = []; let start = 0, lastBreak = -1, w = 0;
    for (let i = 0; i < s.length; i++) {
      if (s[i] === ' ') lastBreak = i;
      w += this.adv(i);
      if (w > W && lastBreak > start) { lines.push([start, lastBreak]); start = lastBreak + 1; i = start - 1; w = 0; lastBreak = -1; }
    }
    lines.push([start, s.length]);
    return lines;
  }
  get lines() { return { length: this.wrap().length }; }
  get width() { return this.rot ? this.size() * 1.0 : this.textWidth(); }
  get height() { return this.rot ? this.textWidth() : this.size() * 1.26; }
  size() { return this.base.size || 12; }
  // bounds for point text: x from anchor depending on justification
  hbounds() {
    const w = this.textWidth(), x = this.at[0] + this.dx, y = this.at[1] + this.dy;
    let l = x; if (this.just === 'RIGHT') l = x - w; if (this.just === 'CENTER') l = x - w / 2;
    if (this.rot) return [x - 0.252 * this.size(), y, x + 1.008 * this.size(), y - w];
    return [l, y + 1.008 * this.size(), l + w, y - 0.252 * this.size()];
  }
  get left() { return this.hbounds()[0]; } set left(v) { this.dx += v - this.hbounds()[0]; }
  get top() { return this.hbounds()[1]; } set top(v) { this.dy += v - this.hbounds()[1]; }
  rotate(a) { this.rot = a; }
  translate(x, y) { this.dx += x; this.dy += y; }
}

class Style {
  constructor(name) { this.name = name; this.characterAttributes = {}; this.paragraphAttributes = {}; }
  applyTo(range, clear) {
    // range is either a frame's textRange or a characters[] range
    if (range.characterAttributes && range.start !== undefined) { const ca = range.characterAttributes; for (const k in this.characterAttributes) ca[k] = this.characterAttributes[k]; return; }
    const ca = range.characterAttributes; for (const k in this.characterAttributes) ca[k] = this.characterAttributes[k];
  }
}
const coll = () => { const list = []; return { list, add: (n) => { const s = new Style(n); list.push(s); return s; }, getByName: (n) => { const s = list.find(x => x.name === n); if (!s) throw new Error('no ' + n); return s; } }; };

let doc;
global.app = {
  documents: { add: () => {
    doc = { rulerOrigin: null, spots: { add: () => ({ name: '', color: null }) }, paragraphStyles: coll(), characterStyles: coll(), artboardsList: [],
      layers: null };
    const layers = []; layers.add = () => { const l = new Layer(null); layers.unshift(l); return l; };
    Object.defineProperty(layers, 'list', { get: () => layers, set: (v) => { layers.length = 0; v.forEach(x => layers.push(x)); } });
    doc.layers = layers; layers.add();
    const abs = [{ artboardRect: [0, 0, 100, -100], name: '' }]; abs.add = (r) => { const a = { artboardRect: r, name: '' }; abs.push(a); return a; };
    doc.artboards = abs;
    return doc;
  } },
  textFonts: Object.assign([], { getByName: (n) => { if (!fontsOK) throw new Error('missing'); return new Font(n); } }),
  executeMenuCommand: () => {},
};

if (process.env.VARFONT) VARFONTS.forEach(f => app.textFonts.push(f));
if (process.env.BREAK) {
  // simulate an Illustrator that rejects some calls
  Item.prototype.applyEffect = () => { throw new Error('no live effects'); };
  Group.prototype.applyEffect = Item.prototype.applyEffect;
  const add = TextFrame.prototype.rotate; TextFrame.prototype.rotate = function (a, ...rest) { if (rest.length) throw new Error('bad rotate args'); return add.call(this, a); };
}

function runEngine(src) {
  const logs = [];
  global.alert = (m) => logs.push(m);
  new Function(src.replace(/^#target.*$/m, ''))();
  return { doc, logs };
}

module.exports = { runEngine, hex, ADV };
