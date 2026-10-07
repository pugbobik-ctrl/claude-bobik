import sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE,'pylib'))
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.ops import unary_union
from shapely import affinity

FONTDIR='/tmp/claude-0/-home-user-claude-bobik/6a3dcf92-132a-5018-88ad-a2068c46056a/scratchpad/dielines/fonts/'
LEMON='#feed95'; INK='#111111'
NAME='Sophia Zhuravkova'
OUT=os.path.join(HERE,'out')

_fonts={}
def font(w=700):
    if w not in _fonts: _fonts[w]=TTFont(FONTDIR+f'WixMadeforText-{w}.ttf')
    return _fonts[w]

class FlatPen(BasePen):
    def __init__(self, gs, n=10):
        super().__init__(gs); self.contours=[]; self.cur=None; self.n=n
    def _moveTo(self,p): self.cur=[p]
    def _lineTo(self,p): self.cur.append(p)
    def _curveToOne(self,a,b,c):
        p0=self.cur[-1]
        for t in np.linspace(0,1,self.n+1)[1:]:
            u=1-t
            self.cur.append((u**3*p0[0]+3*u*u*t*a[0]+3*u*t*t*b[0]+t**3*c[0],
                             u**3*p0[1]+3*u*u*t*a[1]+3*u*t*t*b[1]+t**3*c[1]))
    def _qCurveToOne(self,a,b):
        p0=self.cur[-1]
        for t in np.linspace(0,1,self.n+1)[1:]:
            u=1-t
            self.cur.append((u*u*p0[0]+2*u*t*a[0]+t*t*b[0], u*u*p0[1]+2*u*t*a[1]+t*t*b[1]))
    def _closePath(self):
        if self.cur and len(self.cur)>2: self.contours.append(self.cur)
        self.cur=None
    _endPath=_closePath

def text_poly(text, cap_mm, weight=700, tracking=0.0, anchor='l'):
    """shapely geometry of text, baseline at y=0, x from 0, y up, mm. cap height = cap_mm."""
    f=font(weight); gs=f.getGlyphSet(); cmap=f.getBestCmap()
    s=cap_mm/f['OS/2'].sCapHeight
    x=0; polys=[]
    for ch in text:
        gn=cmap[ord(ch)]
        pen=FlatPen(gs); gs[gn].draw(pen)
        g=None
        for c in pen.contours:
            p=Polygon(c)
            if not p.is_valid: p=p.buffer(0)
            g=p if g is None else g.symmetric_difference(p)
        if g is not None and not g.is_empty:
            g=affinity.translate(g,x,0); polys.append(g)
        x+=gs[gn].width+tracking*f['head'].unitsPerEm
    G=unary_union(polys) if polys else Polygon()
    G=affinity.scale(G,s,s,origin=(0,0))
    if anchor=='c':
        b=G.bounds; G=affinity.translate(G,-(b[0]+b[2])/2,0)
    return G

def geom_path(g, flipy=False):
    """SVG path data (even-odd) for shapely polygon(s), coordinates mm."""
    polys=[g] if isinstance(g,Polygon) else list(g.geoms)
    d=[]
    sy=-1 if flipy else 1
    for p in polys:
        for ring in [p.exterior]+list(p.interiors):
            pts=list(ring.coords)
            d.append('M'+' L'.join(f'{x:.3f},{sy*y:.3f}' for x,y in pts)+' Z')
    return ' '.join(d)

def svg_head(w,h,vb=None,bg='#ffffff'):
    vb=vb or f'0 0 {w} {h}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w*4}" height="{h*4}" '
            f'font-family="Wix Madefor Text, sans-serif">\n<defs><style>@font-face{{font-family:"Wix Madefor Text";font-weight:700;src:url("file://{FONTDIR}WixMadeforText-700.ttf");}}'
            f'@font-face{{font-family:"Wix Madefor Text";font-weight:400;src:url("file://{FONTDIR}WixMadeforText-400.ttf");}}'
            f'@font-face{{font-family:"Wix Madefor Text";font-weight:500;src:url("file://{FONTDIR}WixMadeforText-500.ttf");}}</style></defs>\n'
            f'<rect x="-10000" y="-10000" width="20000" height="20000" fill="{bg}"/>\n')
