"""Shared helpers for the six craft concepts. All SVG units are millimetres."""
import math
from fontTools.ttLib import TTFont

FONTDIR = "/tmp/claude-0/-home-user-claude-bobik/6a3dcf92-132a-5018-88ad-a2068c46056a/scratchpad/dielines/fonts/"
LEMON = "#feed95"
LEMON_D = "#f0d974"      # shaded lemon (back face / shadow side)
LEMON_DD = "#dcc24f"
INK = "#111111"
CUT = "#d4007a"
VAL = "#1769e0"
MTN = "#e03a1e"
EMB = "#0a8f80"
GREY = "#6b6b6b"
FONT = "'Wix Madefor Text', sans-serif"
NAME = "Sophia Zhuravkova"

_fonts = {}


def tw(text, size, weight=500):
    """advance width in mm of text at font-size `size` (mm)"""
    if weight not in _fonts:
        f = TTFont(FONTDIR + f"WixMadeforText-{weight}.ttf")
        _fonts[weight] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm, f)
    cmap, hmtx, upm, _ = _fonts[weight]
    return sum(hmtx[cmap[ord(c)]][0] for c in text) / upm * size


def capheight(weight=500):
    tw("a", 1, weight)
    f = _fonts[weight][3]
    os2 = f["OS/2"]
    return os2.sCapHeight / f["head"].unitsPerEm


def f2(x):
    return ("%.3f" % x).rstrip("0").rstrip(".")


def pts(poly):
    return " ".join(f"{f2(x)},{f2(y)}" for x, y in poly)


class Doc:
    def __init__(self, x0, y0, w, h, scale=5.0, bg="#ffffff"):
        self.x0, self.y0, self.w, self.h, self.scale = x0, y0, w, h, scale
        self.bg = bg
        self.parts = []
        self.defs = []

    def add(self, s):
        self.parts.append(s)

    def raw(self, s):
        self.parts.append(s)

    def line(self, x1, y1, x2, y2, cls="cut", extra=""):
        self.add(f'<line x1="{f2(x1)}" y1="{f2(y1)}" x2="{f2(x2)}" y2="{f2(y2)}" class="{cls}" {extra}/>')

    def poly(self, poly, cls="cut", fill="none", extra=""):
        self.add(f'<polygon points="{pts(poly)}" class="{cls}" fill="{fill}" {extra}/>')

    def path(self, d, cls="cut", fill="none", extra=""):
        self.add(f'<path d="{d}" class="{cls}" fill="{fill}" {extra}/>')

    def rect(self, x, y, w, h, cls="cut", fill="none", rx=0, extra=""):
        self.add(f'<rect x="{f2(x)}" y="{f2(y)}" width="{f2(w)}" height="{f2(h)}" rx="{f2(rx)}" class="{cls}" fill="{fill}" {extra}/>')

    def circle(self, x, y, r, cls="cut", fill="none", extra=""):
        self.add(f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(r)}" class="{cls}" fill="{fill}" {extra}/>')

    def text(self, x, y, s, size=3, weight=500, fill=INK, anchor="start", extra="", ls=0):
        s = s.replace("&", "&amp;")
        self.add(f'<text x="{f2(x)}" y="{f2(y)}" font-size="{f2(size)}" font-weight="{weight}" fill="{fill}" '
                 f'text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{s}</text>')

    def note(self, x, y, s, size=2.6, fill=GREY, anchor="start", weight=400, extra=""):
        self.text(x, y, s, size, weight, fill, anchor, extra)

    def notes(self, x, y, lines, size=2.6, lead=1.45, fill=GREY, weight=400):
        for i, l in enumerate(lines):
            self.note(x, y + i * size * lead, l, size, fill, weight=weight)

    def title(self, x, y, t, sub=None):
        self.text(x, y, t, 5.2, 700, INK)
        if sub:
            self.note(x, y + 5.2, sub, 2.8)

    def legend(self, x, y, items):
        """items: (cls, label)"""
        for i, (cls, lab) in enumerate(items):
            yy = y + i * 4.6
            if cls == "swatch_lemon":
                self.rect(x, yy - 2.2, 8, 3.2, "thin", LEMON)
            elif cls == "swatch_emb":
                self.rect(x, yy - 2.2, 8, 3.2, "thin", "#bfe8e1")
            else:
                self.line(x, yy - 0.6, x + 8, yy - 0.6, cls)
            self.note(x + 10.5, yy, lab, 2.7, INK)

    def svg(self):
        W, H = self.w * self.scale, self.h * self.scale
        style = f"""
        text {{ font-family: {FONT}; }}
        .cut {{ stroke:{CUT}; stroke-width:.35; stroke-linejoin:round; stroke-linecap:round }}
        .val {{ stroke:{VAL}; stroke-width:.3; stroke-dasharray:2.6 1.3 }}
        .mtn {{ stroke:{MTN}; stroke-width:.3; stroke-dasharray:5 1.2 .9 1.2 }}
        .emb {{ stroke:{EMB}; stroke-width:.3 }}
        .thin {{ stroke:#9a9a9a; stroke-width:.2 }}
        .dim {{ stroke:#444; stroke-width:.18 }}
        .edge {{ stroke:#6d5a10; stroke-width:.22; stroke-linejoin:round }}
        .edgeL {{ stroke:#b79c2a; stroke-width:.18; stroke-linejoin:round }}
        .ink {{ stroke:{INK}; stroke-width:.5; stroke-linecap:round; stroke-linejoin:round }}
        .shadow {{ fill:#000; opacity:.13 }}
        """
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{f2(W)}" height="{f2(H)}" '
                f'viewBox="{f2(self.x0)} {f2(self.y0)} {f2(self.w)} {f2(self.h)}">'
                f'<defs><style>{style}</style>{"".join(self.defs)}</defs>'
                f'<rect x="{f2(self.x0)}" y="{f2(self.y0)}" width="{f2(self.w)}" height="{f2(self.h)}" fill="{self.bg}"/>'
                + "".join(self.parts) + "</svg>")

    def save(self, path):
        open(path, "w").write(self.svg())


# --- planar geometry ------------------------------------------------------
def clip_halfplane(poly, p, d, keep_left=True):
    """clip convex polygon by line through p with direction d; keep left side (cross(d, q-p) >= 0) or right"""
    out = []
    def side(q):
        s = d[0] * (q[1] - p[1]) - d[1] * (q[0] - p[0])
        return s if keep_left else -s
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        sa, sb = side(a), side(b)
        if sa >= -1e-9:
            out.append(a)
        if (sa > 1e-9 and sb < -1e-9) or (sa < -1e-9 and sb > 1e-9):
            t = sa / (sa - sb)
            out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    # drop duplicates
    res = []
    for q in out:
        if not res or abs(q[0] - res[-1][0]) > 1e-9 or abs(q[1] - res[-1][1]) > 1e-9:
            res.append(q)
    if len(res) > 1 and abs(res[0][0] - res[-1][0]) < 1e-9 and abs(res[0][1] - res[-1][1]) < 1e-9:
        res.pop()
    return res


def reflect_pt(q, p, d):
    L = math.hypot(*d)
    ux, uy = d[0] / L, d[1] / L
    vx, vy = q[0] - p[0], q[1] - p[1]
    t = vx * ux + vy * uy
    px, py = p[0] + t * ux, p[1] + t * uy
    return (2 * px - q[0], 2 * py - q[1])


def area(poly):
    s = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s / 2


def inside(poly, q):
    """convex point test, any winding"""
    sgn = 0
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        c = (b[0] - a[0]) * (q[1] - a[1]) - (b[1] - a[1]) * (q[0] - a[0])
        if abs(c) < 1e-9:
            continue
        s = 1 if c > 0 else -1
        if sgn == 0:
            sgn = s
        elif s != sgn:
            return False
    return True
