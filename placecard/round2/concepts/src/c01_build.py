import json, numpy as np, math, base64, io
from PIL import Image, ImageDraw, ImageFilter
from shapely.geometry import box, Polygon
from shapely import affinity
from lib import *
import c01_calc as K

LAMP = K.LAMP; ZP = K.ZP; YC = K.YC
CARD_W = 96.0; CARD_H = 124.0

def holes_plate_coords(slice_frac=0.45):
    geoms = []
    cap = 0.715 * K.SIZE; xh = 0.503 * K.SIZE
    for i, line in enumerate(['Sophia', 'Zhuravkova']):
        g, w = text_shape(line, K.SIZE, 700)          # y up
        base = K.TOPPY + cap + i * K.LEAD
        g = affinity.scale(g, 1, -1, origin=(0, 0))   # y down
        g = affinity.translate(g, 0, base)
        band = box(-100, base - slice_frac * xh - K.BRIDGE / 2, 100, base - slice_frac * xh + K.BRIDGE / 2)
        # extra bridge above ascenders? none needed (checked)
        geoms.append(g.difference(band))
    return unary_union(geoms)

def to_card(g, lamp=LAMP):
    return geom_map(g, lambda x, y: K.plate_to_card(x, y))

def simulate(holes_card, src_d=3.0, nsamp=61, lamp=LAMP, ppm_card=12, res=3.0):
    x0, x1, y0, y1 = -150, 150, 190, 520
    xs = np.arange(x0, x1, 1 / res); ys = np.arange(y0, y1, 1 / res)
    PX, PY = np.meshgrid(xs, ys)
    # card solid mask
    W = int(CARD_W * ppm_card); H = int(CARD_H * ppm_card)
    im = Image.new('L', (W, H), 255)      # 255 = solid (blocks)
    d = ImageDraw.Draw(im)
    for p in geom_polys(holes_card):
        for ring, col in [(p.exterior, 0)] + [(r, 255) for r in p.interiors]:
            d.polygon([((x + CARD_W / 2) * ppm_card, (CARD_H - z) * ppm_card) for x, z in ring.coords], fill=col)
    solid = np.array(im) > 127
    # source samples: Fermat spiral inside a disc of diameter src_d (horizontal)
    pts = [(0, 0)]
    if src_d > 0:
        for k in range(1, nsamp):
            r = (src_d / 2) * math.sqrt(k / nsamp); a = k * 2.399963
            pts.append((r * math.cos(a), r * math.sin(a)))
    lit = np.zeros(PX.shape)
    for sx, sy in pts:
        S = np.array([lamp[0] + sx, lamp[1] + sy, lamp[2]])
        lam = (YC - S[1]) / (PY - S[1])            # <1 when pixel is behind the card plane
        X = S[0] + lam * (PX - S[0]); Z = S[2] + lam * (ZP - S[2])
        ix = np.round((X + CARD_W / 2) * ppm_card).astype(int)
        iz = np.round((CARD_H - Z) * ppm_card).astype(int)
        inside = (ix >= 0) & (ix < W) & (iz >= 0) & (iz < H)
        blocked = np.zeros(PX.shape, bool)
        blocked[inside] = solid[iz[inside], ix[inside]]
        blocked &= (PY > YC)
        # table cut at z<0 : rays below the card base (Z<0) cannot occur on plate plane
        lit += (~blocked)
    return lit / len(pts), (x0, x1, y0, y1, res)

def render_top(lit, ext, name):
    x0, x1, y0, y1, res = ext
    H, W = lit.shape
    # shading: lit plate white, shadow = 0.22 of that
    amb = 0.30
    val = amb + (1 - amb) * lit
    img = np.zeros((H, W, 3))
    base = np.array([255, 253, 246])
    img[:] = base * val[..., None]
    yy, xx = np.mgrid[0:H, 0:W]
    px = x0 + xx / res; py = y0 + yy / res
    r = np.hypot(px - K.PLATE_C[0], py - K.PLATE_C[1])
    cloth = img.copy(); cloth *= np.array([0.93, 0.91, 0.86])
    out = np.where((r <= K.PLATE_R)[..., None], img, cloth)
    # plate rim line
    rim = (np.abs(r - K.PLATE_R) < 0.8) | (np.abs(r - K.PLATE_R * 0.68) < 0.5)
    out[rim] = out[rim] * 0.55
    # card footprint
    foot = (np.abs(px) < CARD_W / 2) & (py > YC - 25) & (py < YC + 25)
    out[foot] = np.array([254, 237, 149])
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(name)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

if __name__ == '__main__':
    hp = holes_plate_coords(); hc = to_card(hp)
    print('card hole bbox', [round(v, 1) for v in hc.bounds], 'plate text bbox', [round(v, 1) for v in hp.bounds])
    minb = min(r.width for r in [Polygon(p) for p in []]) if False else None
    lit_pt, ext = simulate(hc, src_d=0.0)
    render_top(lit_pt, ext, '../calc/c01_shadow_point.png')
    lit_led, ext = simulate(hc, src_d=5.0)
    render_top(lit_led, ext, '../calc/c01_shadow_led5mm.png')
    lit_big, ext = simulate(hc, src_d=25.0)
    render_top(lit_big, ext, '../calc/c01_shadow_bulb25mm.png')
    # sensitivity: lamp height / lateral error -> where does a letter-point land
    ref = np.array(K.card_to_plate(*K.plate_to_card(0, 282)))
    print('check roundtrip', ref)
    def land(lamp, xc, zc):
        S = np.array(lamp); C = np.array([xc, YC, zc]); lam = (ZP - S[2]) / (C[2] - S[2]); P = S + lam * (C - S); return P[:2]
    xc, zc = K.plate_to_card(0, 282)
    for name, lamp in [('nominal', LAMP), ('bulb 30 mm lower', (0, 0, 270)), ('bulb 30 mm higher', (0, 0, 330)), ('lamp 25 mm sideways', (25, 0, 300)), ('lamp 40 mm nearer card', (0, 40, 300)), ('lamp 40 mm farther', (0, -40, 300))]:
        P = land(lamp, xc, zc); print(f'{name:26s} text centre lands at x={P[0]:7.1f}  y={P[1]:7.1f}  (shift {P[0]-0:6.1f}, {P[1]-282:6.1f} mm)')
    # card hole stats
    print('holes area', hc.area, 'n polys', len(geom_polys(hc)))
