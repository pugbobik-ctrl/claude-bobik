"""Shared helpers: tiny axonometric camera, SVG writer, glyph outlines."""
import math, os
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, 'fonts')

LEMON = '#feed95'
LEMON_D = '#f3dd75'
LEMON_DD = '#e6c957'
INK = '#141414'
PAPER = '#f7f5ef'
CLOTH = '#ebe8de'
GREY = '#8d8a80'
GREY_L = '#cfccc2'
WHITE = '#ffffff'
RED = '#c8281e'   # only for dimension/annotation, never on the card

_fonts = {}
def font(w=700):
    if w not in _fonts:
        _fonts[w] = TTFont(os.path.join(FONTS, f'WixMadeforText-{w}.ttf'))
    return _fonts[w]


def _flatten(pen_value, n=10):
    """RecordingPen value -> list of contours (each list of (x,y))."""
    contours, cur = [], []
    last = None
    for op, args in pen_value:
        if op == 'moveTo':
            cur = [args[0]]; last = args[0]
        elif op == 'lineTo':
            cur.append(args[0]); last = args[0]
        elif op == 'qCurveTo':
            pts = list(args)
            # TrueType implied on-curve points
            offs, end = pts[:-1], pts[-1]
            if end is None: end = cur[0]
            seq = []
            for i, o in enumerate(offs):
                if i < len(offs) - 1:
                    nx = offs[i + 1]
                    on = ((o[0] + nx[0]) / 2, (o[1] + nx[1]) / 2)
                else:
                    on = end
                seq.append((o, on))
            p0 = last
            for c, on in seq:
                for k in range(1, n + 1):
                    t = k / n
                    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * on[0]
                    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * on[1]
                    cur.append((x, y))
                p0 = on
            last = end
        elif op == 'curveTo':
            p0 = last; c1, c2, e = args
            for k in range(1, n + 1):
                t = k / n
                x = (1-t)**3*p0[0]+3*(1-t)**2*t*c1[0]+3*(1-t)*t*t*c2[0]+t**3*e[0]
                y = (1-t)**3*p0[1]+3*(1-t)**2*t*c1[1]+3*(1-t)*t*t*c2[1]+t**3*e[1]
                cur.append((x, y))
            last = e
        elif op in ('closePath', 'endPath'):
            if cur: contours.append(cur)
            cur = []
    return contours


def text_contours(text, size, weight=700, tracking=0.0):
    """Return (contours, width) in mm-like units: y up, baseline y=0, x from 0.
    size = font size (em) in same units."""
    f = font(weight)
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); hmtx = f['hmtx']
    upm = f['head'].unitsPerEm
    sc = size / upm
    x = 0; out = []
    for ch in text:
        gn = cmap.get(ord(ch))
        if gn is None: x += 0.3 * size; continue
        pen = RecordingPen(); gs[gn].draw(pen)
        for c in _flatten(pen.value):
            out.append([(x + px * sc, py * sc) for px, py in c])
        x += hmtx[gn][0] * sc + tracking * size
    return out, x - tracking * size


def text_width(text, size, weight=700, tracking=0.0):
    return text_contours(text, size, weight, tracking)[1]


def contours_to_path(contours, tf=lambda p: p):
    d = []
    for c in contours:
        pts = [tf(p) for p in c]
        d.append('M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in pts) + 'Z')
    return ' '.join(d)


def hull(pts):
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in pts))
    if len(pts) < 3: return pts
    def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


class Cam:
    """Orthographic axonometric. World: x right, y away from viewer, z up (mm)."""
    def __init__(self, az=-28, el=32, s=1.0, ox=0, oy=0):
        self.az = math.radians(az); self.el = math.radians(el)
        self.s = s; self.ox = ox; self.oy = oy
    def p(self, x, y, z=0):
        ca, sa = math.cos(self.az), math.sin(self.az)
        x1 = x * ca - y * sa
        y1 = x * sa + y * ca
        sx = x1
        sy_up = z * math.cos(self.el) + y1 * math.sin(self.el)
        return (self.ox + self.s * sx, self.oy - self.s * sy_up)
    def vec(self, v):
        o = self.p(0, 0, 0); q = self.p(*v)
        return (q[0] - o[0], q[1] - o[1])


class S:
    def __init__(self, w=1200, h=900, bg=PAPER):
        self.w, self.h = w, h; self.e = []; self.bg = bg
        self.defs = []
    def add(self, s): self.e.append(s)
    def raw(self, s): self.e.append(s)
    def poly(self, pts, fill='none', stroke=INK, sw=1.5, op=None, dash=None, join='round', extra=''):
        d = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
        a = f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="{join}"'
        if op is not None: a += f' fill-opacity="{op}"'
        if dash: a += f' stroke-dasharray="{dash}"'
        self.e.append(a + f' {extra}/>')
    def path(self, d, fill='none', stroke=INK, sw=1.5, dash=None, extra='', cap='round'):
        a = f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="{cap}"'
        if dash: a += f' stroke-dasharray="{dash}"'
        self.e.append(a + f' {extra}/>')
    def line(self, a, b, stroke=INK, sw=1.5, dash=None, cap='round', extra=''):
        s = f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"'
        if dash: s += f' stroke-dasharray="{dash}"'
        self.e.append(s + f' {extra}/>')
    def polyline(self, pts, stroke=INK, sw=1.5, dash=None, fill='none', extra=''):
        d = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
        s = f'<polyline points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'
        if dash: s += f' stroke-dasharray="{dash}"'
        self.e.append(s + f' {extra}/>')
    def circle(self, c, r, fill='none', stroke=INK, sw=1.5, extra=''):
        self.e.append(f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{r:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
    def text(self, xy, t, size=14, weight=500, fill=INK, anchor='start', extra='', ls=None):
        t = t.replace('&', '&amp;').replace('<', '&lt;')
        s = f'<text x="{xy[0]:.2f}" y="{xy[1]:.2f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
        if ls is not None: s += f' letter-spacing="{ls}"'
        self.e.append(s + f' {extra}>{t}</text>')
    def note(self, xy, lines, size=13, weight=500, fill=INK, anchor='start', lh=1.35):
        if isinstance(lines, str): lines = [lines]
        for i, l in enumerate(lines):
            self.text((xy[0], xy[1] + i * size * lh), l, size, weight, fill, anchor)
    def leader(self, frm, to, label, side='r', size=13, lines=None, dot=True):
        """frm = point on object, to = label anchor"""
        self.line(frm, to, GREY, 1)
        if dot: self.circle(frm, 2.6, INK, INK, 0.5)
        anchor = 'start' if side == 'r' else 'end'
        dx = 6 if side == 'r' else -6
        self.note((to[0] + dx, to[1] + 4), label if isinstance(label, list) else [label], size, 500, INK, anchor)
    def face_text(self, cam, origin, u, v, t, size, weight=700, fill=INK, anchor='start', ls=None, dx=0, dy=0, extra=''):
        """Text lying in a 3D plane: origin (3D), u = unit vector along text (3D), v = up-in-face (3D)."""
        ux, uy = cam.vec(u); vx, vy = cam.vec(v); ox, oy = cam.p(*origin)
        m = f'matrix({ux:.4f} {uy:.4f} {-vx:.4f} {-vy:.4f} {ox:.2f} {oy:.2f})'
        t = t.replace('&', '&amp;')
        s = f'<text transform="{m}" x="{dx}" y="{-dy}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
        if ls is not None: s += f' letter-spacing="{ls}"'
        self.e.append(s + f' {extra}>{t}</text>')
    def header(self, num, name, tag):
        self.text((48, 78), num, 40, 700, INK)
        self.text((112, 78), name, 40, 700, INK)
        self.text((48, 108), tag, 16, 400, '#555')
    def footer(self, items):
        x = 48
        for k, v in items:
            self.text((x, self.h - 34), k, 11, 700, GREY, ls=1)
            self.text((x, self.h - 17), v, 13, 500, INK)
            x += max(150, 8.2 * max(len(v), len(k)) + 24)
    def save(self, path):
        css = ''.join(
            f"@font-face{{font-family:'Wix Madefor Text';font-weight:{w};src:url('../fonts/WixMadeforText-{w}.ttf') format('truetype');}}"
            for w in (400, 500, 600, 700))
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
                f"font-family=\"'Wix Madefor Text', sans-serif\">"
                f'<style>{css}</style>' + ''.join(self.defs) +
                f'<rect width="{self.w}" height="{self.h}" fill="{self.bg}"/>')
        open(path, 'w').write(head + '\n'.join(self.e) + '</svg>')


# ---------- 3D object helpers (draw into an S through a Cam) ----------
def circ3(c, r, z, n=72, a0=0, a1=360):
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)), z) for i in range(n + 1)]


def cloth(s, cam, x0, x1, y0, y1, z=0):
    pts = [cam.p(x0, y0, z), cam.p(x1, y0, z), cam.p(x1, y1, z), cam.p(x0, y1, z)]
    s.poly(pts, CLOTH, GREY_L, 1)


def plate(s, cam, c, r=135, z=0, h=18, fill=WHITE):
    # rim wall
    top = [cam.p(*p) for p in circ3(c, r, z + h)]
    bot = [cam.p(*p) for p in circ3(c, r * 0.62, z)]
    allp = [cam.p(*p) for p in circ3(c, r, z + h)] + bot
    s.poly(hull(allp), fill, GREY, 1.4)
    s.poly(top, fill, GREY, 1.4)
    well = [cam.p(*p) for p in circ3(c, r * 0.68, z + h * 0.55)]
    s.poly(well, '#f4f3ee', GREY_L, 1)


def cylinder(s, cam, c, r, z0, z1, fill=WHITE, stroke=INK, sw=1.5, n=48, topfill=None):
    pts = [cam.p(*p) for p in circ3(c, r, z0, n)] + [cam.p(*p) for p in circ3(c, r, z1, n)]
    s.poly(hull(pts), fill, stroke, sw)
    s.poly([cam.p(*p) for p in circ3(c, r, z1, n)], topfill or fill, stroke, sw)


def cone(s, cam, c, r, z0, z1, fill=INK, stroke=INK, sw=1.2, apex_r=0):
    pts = [cam.p(*p) for p in circ3(c, r, z0)] + [cam.p(*p) for p in circ3(c, apex_r, z1, 24)]
    s.poly(hull(pts), fill, stroke, sw)


def lamp(s, cam, c, z=0, h=300, shade_r=70, shade_h=95):
    """small black cone-shade table lamp: base disc, stem, cone shade"""
    cx, cy = c
    cylinder(s, cam, c, 34, z, z + 6, '#2a2a2a', INK, 1)
    s.line(cam.p(cx, cy, z + 6), cam.p(cx, cy, z + h - shade_h + 6), INK, 4)
    cone(s, cam, c, shade_r, z + h - shade_h, z + h, INK, INK, 1, apex_r=10)
    # opening rim ellipse (inside glow)
    s.poly([cam.p(*p) for p in circ3(c, shade_r, z + h - shade_h)], '#3a3a3a', INK, 1)


def wineglass(s, cam, c, z=0, stroke=INK, fill='#ffffff', op=0.55):
    cx, cy = c
    s.poly([cam.p(*p) for p in circ3(c, 33, z)], fill, GREY, 1.2)
    s.line(cam.p(cx, cy, z), cam.p(cx, cy, z + 85), GREY, 3)
    prof = [(0, 85), (20, 92), (34, 120), (36, 150), (30, 185), (22, 195)]
    pts = []
    for rr, zz in prof:
        pts += [cam.p(*p) for p in circ3(c, max(rr, 0.1), z + zz, 36)]
    s.poly(hull(pts), fill, GREY, 1.4, op=op)
    s.poly([cam.p(*p) for p in circ3(c, 22, z + 195, 36)], fill, GREY, 1.2, op=0.8)


def person_seat_eye(s, cam, pos, label=None):
    s.circle(cam.p(*pos), 6, INK, INK, 1)


# ---------- shapely glyph shapes ----------
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.ops import unary_union
from shapely import affinity


def _area(c):
    return 0.5 * sum(c[i][0] * c[(i + 1) % len(c)][1] - c[(i + 1) % len(c)][0] * c[i][1] for i in range(len(c)))


def text_shape(text, size, weight=700, tracking=0.0, center=True):
    """shapely geometry of the text, y UP, baseline at y=0. Returns (geom, width)."""
    cs, w = text_contours(text, size, weight, tracking)
    outers = [Polygon(c).buffer(0) for c in cs if _area(c) < 0]
    holes = [Polygon(c).buffer(0) for c in cs if _area(c) > 0]
    g = unary_union(outers).difference(unary_union(holes)) if holes else unary_union(outers)
    if center: g = affinity.translate(g, -w / 2, 0)
    return g, w


def geom_polys(g):
    if g.is_empty: return []
    if isinstance(g, Polygon): return [g]
    return [p for p in g.geoms if isinstance(p, Polygon)]


def geom_path(g, tf=lambda p: p):
    d = []
    for p in geom_polys(g):
        for ring in [p.exterior] + list(p.interiors):
            pts = [tf(q) for q in ring.coords]
            d.append('M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in pts[:-1]) + 'Z')
    return ' '.join(d)


def geom_map(g, f):
    """map every vertex through f(x,y)->(x,y); returns shapely geometry"""
    out = []
    for p in geom_polys(g):
        ext = [f(*q) for q in p.exterior.coords]
        ints = [[f(*q) for q in r.coords] for r in p.interiors]
        out.append(Polygon(ext, ints))
    return unary_union(out) if out else Polygon()


class FCam(Cam):
    """Same camera but world y runs TOWARD the viewer (guest side): y_cam = ymax - y."""
    def __init__(self, ymax=500, **kw):
        super().__init__(**kw); self.ymax = ymax
    def p(self, x, y, z=0):
        return super().p(x, self.ymax - y, z)
    def vec(self, v):
        return super().vec((v[0], -v[1], v[2]))


def b64img(path):
    import base64
    return 'data:image/png;base64,' + base64.b64encode(open(path, 'rb').read()).decode()
