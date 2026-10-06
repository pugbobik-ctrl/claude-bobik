"""Shared helpers for the three place-card dielines (all units: mm)."""
import base64, math, os
import numpy as np
from fontTools.ttLib import TTFont
from shapely.geometry import Polygon, LineString, MultiPolygon, box
from shapely.ops import unary_union

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = ROOT
FONT_DIR = os.path.join(os.path.dirname(ROOT), 'fonts')   # shared with v1: dielines/fonts

# ------------------------------------------------------------------ colours
YELLOW = '#feed95'
INK = '#111111'
C_CUT = '#e2007a'      # magenta  : cut
C_CREASE = '#0072ce'   # blue     : crease / fold (dashed)
C_SLOT = '#8a2be2'     # violet   : slot / slit
C_BLEED = '#00a3a3'    # teal     : bleed
C_SAFE = '#1a9850'     # green    : safe area for the name
C_DIM = '#777777'

BOARD_T = 0.50         # mm, 400 g/m2 uncoated board, caliper
SLOT_W = 0.70          # mm, = steel-rule 2 pt (0.71) ; clearance 0.20 on 0.50 board
BLEED = 3.0
SEC = 4.9                # secondary text size: cap height 3.5 mm
INK_REV = '#111111'

# ------------------------------------------------------------------ font metrics
_fonts = {}
def _font(w):
    if w not in _fonts:
        f = TTFont(os.path.join(FONT_DIR, f'WixMadeforText-{w}.ttf'))
        _fonts[w] = (f.getBestCmap(), f['hmtx'], f['head'].unitsPerEm)
    return _fonts[w]

def text_em(s, weight=500, tracking=0.0):
    """advance width of s in em (no kerning; kerning in GPOS only shrinks it slightly)"""
    cm, hm, upm = _font(weight)
    w = sum(hm[cm.get(ord(c), cm[ord('?')])][0] for c in s) / upm
    return w + tracking * len(s)

def text_w(s, size, weight=500, tracking=0.0):
    return text_em(s, weight, tracking) * size

CAP = 0.715   # cap-height / em of Wix Madefor Text
XH = 0.497

def fit_size(s, avail, max_size, weight=500):
    return min(max_size, avail / text_em(s, weight))

# ------------------------------------------------------------------ path with true arcs
def _circ(p0, pm, p1):
    ax, ay = p0; bx, by = pm; cx, cy = p1
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    return (ux, uy), math.hypot(ax - ux, ay - uy)

class Path:
    """Polyline/arc path in SVG coordinates (y down). Arcs are defined by 3 points."""
    def __init__(self, start):
        self.segs = [('M', tuple(start))]
        self.cur = tuple(start)

    def L(self, p):
        self.segs.append(('L', tuple(p))); self.cur = tuple(p); return self

    def A3(self, pm, p1):
        p0 = self.cur
        c, r = _circ(p0, pm, p1)
        a0 = math.atan2(p0[1] - c[1], p0[0] - c[0])
        am = math.atan2(pm[1] - c[1], pm[0] - c[0])
        a1 = math.atan2(p1[1] - c[1], p1[0] - c[0])
        two = 2 * math.pi
        inc = ((am - a0) % two) < ((a1 - a0) % two)       # increasing angle (svg sweep=1)
        da = ((a1 - a0) % two) if inc else -((a0 - a1) % two)
        large = 1 if abs(da) > math.pi else 0
        self.segs.append(('A', tuple(p1), r, large, 1 if inc else 0, c, a0, da, tuple(pm)))
        self.cur = tuple(p1); return self

    def Z(self):
        self.segs.append(('Z',)); return self

    def xform(self, fn):
        """rigid transform (rotation/translation/reflection) of every point; returns new Path"""
        q = None
        for s in self.segs:
            if s[0] == 'M': q = Path(fn(s[1]))
            elif s[0] == 'L': q.L(fn(s[1]))
            elif s[0] == 'A': q.A3(fn(s[8]), fn(s[1]))
            else: q.Z()
        return q

    def d(self, nd=3):
        f = lambda v: ('%.*f' % (nd, v)).rstrip('0').rstrip('.')
        out = []
        for s in self.segs:
            if s[0] == 'M': out.append(f'M{f(s[1][0])} {f(s[1][1])}')
            elif s[0] == 'L': out.append(f'L{f(s[1][0])} {f(s[1][1])}')
            elif s[0] == 'A': out.append(f'A{f(s[2])} {f(s[2])} 0 {s[3]} {s[4]} {f(s[1][0])} {f(s[1][1])}')
            else: out.append('Z')
        return ' '.join(out)

    def pts(self, step=1.0):
        """sampled polyline (list of (x,y)), arc sampled every ~step mm"""
        out = []
        for s in self.segs:
            if s[0] in 'ML': out.append(s[1])
            elif s[0] == 'A':
                _, p1, r, large, sw, c, a0, da, _pm = s
                n = max(2, int(abs(da) * r / step))
                for i in range(1, n + 1):
                    a = a0 + da * i / n
                    out.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
                out[-1] = p1
        return out

    def poly(self, step=0.5):
        return Polygon(self.pts(step))

def sample_arc3(p0, pm, p1, step=0.5):
    return Path(p0).A3(pm, p1).pts(step)

def poly_d(poly_or_pts, nd=3):
    pts = list(poly_or_pts.exterior.coords) if hasattr(poly_or_pts, 'exterior') else poly_or_pts
    f = lambda v: ('%.*f' % (nd, v)).rstrip('0').rstrip('.')
    return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + ' Z'

def polys_d(g, nd=3):
    """shapely (Multi)Polygon with holes -> path d (use fill-rule evenodd)"""
    geoms = g.geoms if hasattr(g, 'geoms') else [g]
    out = []
    for p in geoms:
        out.append(poly_d(list(p.exterior.coords), nd))
        for h in p.interiors: out.append(poly_d(list(h.coords), nd))
    return ' '.join(out)

# ------------------------------------------------------------------ svg building
def _font_face_css():
    css = ''
    for w, name in ((500, 'sub-500.ttf'), (700, 'sub-700.ttf')):
        b = base64.b64encode(open(os.path.join(FONT_DIR, name), 'rb').read()).decode()
        css += ("@font-face{font-family:'Wix Madefor Text';font-weight:%d;"
                "src:url(data:font/ttf;base64,%s) format('truetype');}\n" % (w, b))
    return css

_FF = None
def svg_doc(w, h, body, title, desc='', bg=None, extra_css=''):
    global _FF
    if _FF is None: _FF = _font_face_css()
    bgrect = f'<rect id="paper" x="0" y="0" width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            f'width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">\n'
            f'<title>{title}</title>\n<desc>{desc}</desc>\n'
            f'<style>{_FF}\n'
            f"text{{font-family:'Wix Madefor Text','Helvetica Neue',Arial,sans-serif;font-weight:500;}}\n"
            f".ui{{font-family:'Wix Madefor Text','Helvetica Neue',Arial,sans-serif;font-weight:500;fill:#333;}}\n"
            f'{extra_css}</style>\n{bgrect}\n{body}\n</svg>\n')

def layer(id_, label, content, extra=''):
    return (f'<g id="{id_}" inkscape:groupmode="layer" inkscape:label="{label}" {extra}>\n'
            f'{content}\n</g>')

def f2(v): return ('%.3f' % v).rstrip('0').rstrip('.')

def txt(x, y, s, size, anchor='middle', weight=500, fill=INK, tracking=0, extra='', rot=0):
    tr = f' letter-spacing="{f2(tracking * size)}"' if tracking else ''
    rt = f' transform="rotate({f2(rot)} {f2(x)} {f2(y)})"' if rot else ''
    s = s.replace('&', '&amp;')
    return (f'<text x="{f2(x)}" y="{f2(y)}" font-size="{f2(size)}" text-anchor="{anchor}" '
            f'font-weight="{weight}" fill="{fill}"{tr}{rt} {extra}>{s}</text>')

def ui(x, y, s, size=2.6, anchor='start', fill='#333', weight=500, rot=0):
    return txt(x, y, s, size, anchor, weight, fill, 0, 'class="ui"', rot)

def cut_style(w=0.25): return f'fill="none" stroke="{C_CUT}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
def crease_style(w=0.25, dash='2.4 1.2', cap='butt'): return f'fill="none" stroke="{C_CREASE}" stroke-width="{w}" stroke-dasharray="{dash}" stroke-linecap="{cap}"'
def slot_style(w=0.12): return f'fill="{C_SLOT}" fill-opacity="0.35" stroke="{C_SLOT}" stroke-width="{w}" stroke-linejoin="miter"'
def bleed_style(w=0.15): return f'fill="none" stroke="{C_BLEED}" stroke-width="{w}" stroke-dasharray="0.8 0.8"'
def safe_style(w=0.2): return f'fill="none" stroke="{C_SAFE}" stroke-width="{w}" stroke-dasharray="0.5 1.0" stroke-linecap="round"'

def legend(x, y, items, title='Legend', width=70):
    """items: list of (kind, label) kind in cut/crease/slot/bleed/safe/mtn/vly"""
    out = [ui(x, y, title.upper(), 2.4, fill='#555', weight=700)]
    yy = y + 4.2
    for kind, label in items:
        if kind == 'cut': out.append(f'<line x1="{x}" y1="{yy-0.9}" x2="{x+9}" y2="{yy-0.9}" {cut_style(0.3)}/>')
        elif kind == 'crease': out.append(f'<line x1="{x}" y1="{yy-0.9}" x2="{x+9}" y2="{yy-0.9}" {crease_style(0.3)}/>')
        elif kind == 'valley': out.append(f'<line x1="{x}" y1="{yy-0.9}" x2="{x+9}" y2="{yy-0.9}" {crease_style(0.3, "0.2 1.0", "round")}/>')
        elif kind == 'slot': out.append(f'<rect x="{x}" y="{yy-1.9}" width="9" height="2" {slot_style(0.2)}/>')
        elif kind == 'bleed': out.append(f'<line x1="{x}" y1="{yy-0.9}" x2="{x+9}" y2="{yy-0.9}" {bleed_style(0.25)}/>')
        elif kind == 'safe': out.append(f'<line x1="{x}" y1="{yy-0.9}" x2="{x+9}" y2="{yy-0.9}" {safe_style(0.3)}/>')
        elif kind == 'art': out.append(f'<rect x="{x}" y="{yy-1.9}" width="9" height="2" fill="{YELLOW}" stroke="#999" stroke-width="0.15"/>')
        out.append(ui(x + 11.5, yy, label, 2.3))
        yy += 3.9
    return '\n'.join(out)

def dim_h(x0, x1, y, label, off=0, size=2.2, ext=None):
    """horizontal dimension line from x0 to x1 at height y"""
    s = (f'<g stroke="{C_DIM}" stroke-width="0.12" fill="none">'
         f'<line x1="{f2(x0)}" y1="{f2(y)}" x2="{f2(x1)}" y2="{f2(y)}"/>'
         f'<line x1="{f2(x0)}" y1="{f2(y-1.2)}" x2="{f2(x0)}" y2="{f2(y+1.2)}"/>'
         f'<line x1="{f2(x1)}" y1="{f2(y-1.2)}" x2="{f2(x1)}" y2="{f2(y+1.2)}"/></g>')
    s += ui((x0 + x1) / 2, y - 1.0 + off, label, size, 'middle', C_DIM)
    return s

def dim_v(x, y0, y1, label, size=2.2, side=1):
    s = (f'<g stroke="{C_DIM}" stroke-width="0.12" fill="none">'
         f'<line x1="{f2(x)}" y1="{f2(y0)}" x2="{f2(x)}" y2="{f2(y1)}"/>'
         f'<line x1="{f2(x-1.2)}" y1="{f2(y0)}" x2="{f2(x+1.2)}" y2="{f2(y0)}"/>'
         f'<line x1="{f2(x-1.2)}" y1="{f2(y1)}" x2="{f2(x+1.2)}" y2="{f2(y1)}"/></g>')
    s += ui(x + side * 1.2, (y0 + y1) / 2 + 0.8, label, size, 'start' if side > 0 else 'end', C_DIM)
    return s

# ------------------------------------------------------------------ axonometric helper
class Axo:
    """orthographic axonometric: world x right, y depth (+ away from viewer), z up.
    yaw rotates the scene about z; elev is camera elevation."""
    def __init__(self, yaw_deg=-28, elev_deg=28, ox=0, oy=0, k=1.0):
        self.psi = math.radians(yaw_deg); self.E = math.radians(elev_deg)
        self.ox, self.oy, self.k = ox, oy, k

    def __call__(self, p):
        x, y, z = p
        c, s = math.cos(self.psi), math.sin(self.psi)
        x1 = x * c - y * s
        y1 = x * s + y * c
        X = x1
        Yup = z * math.cos(self.E) + y1 * math.sin(self.E)
        return (self.ox + self.k * X, self.oy - self.k * Yup)

    def depth(self, p):
        x, y, z = p
        c, s = math.cos(self.psi), math.sin(self.psi)
        y1 = x * s + y * c
        return y1 * math.cos(self.E) - z * math.sin(self.E)   # larger = farther

    def matrix(self, o3, u3, v3):
        """affine matrix mapping local (u,w) -> screen, where local point = o3 + u*u3 + w*v3
        (u3,v3 are 3D unit vectors; w measured along v3, SVG local y is downward so pass -v3 if y-down)."""
        o = self(o3)
        pu = self((o3[0] + u3[0], o3[1] + u3[1], o3[2] + u3[2]))
        pv = self((o3[0] + v3[0], o3[1] + v3[1], o3[2] + v3[2]))
        a, b = pu[0] - o[0], pu[1] - o[1]
        c, d = pv[0] - o[0], pv[1] - o[1]
        return f'matrix({a:.5f} {b:.5f} {c:.5f} {d:.5f} {o[0]:.4f} {o[1]:.4f})'

def face_d(axo, pts3):
    return 'M' + ' L'.join('%.3f %.3f' % axo(p) for p in pts3) + ' Z'

def shadow_pts(pts3, lx=0.55, ly=-0.35):
    """project 3D points to ground z=0 along a light direction"""
    return [(x + z * lx, y + z * ly, 0.0) for x, y, z in pts3]

def centroid3(pts3):
    a = np.array(pts3, float); return a.mean(axis=0)
