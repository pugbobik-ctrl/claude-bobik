"""D3 v2 - One sheet for the whole table: 12 skewed straight-cut tents, long-grain SRA3 (landscape), one heavy line across all."""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from shapely.geometry import Point, box, LineString

T = BOARD_T
SHEET_W, SHEET_H = 450.0, 320.0          # SRA3 landscape: long grain runs along x = parallel to all creases
NCOL, NROW = 4, 3
COLW, PITCH = 106.0, 101.0
ALPHA = math.radians(72.0)
F_LEN = 34.5
B_LEN, FLAP_LEN = 20.0, 12.0
TAB_W, TAB_RISE, TAB_FO = 18.0, 3.0, 3.5
TAB_L = TAB_RISE + TAB_FO                # 6.5
SLIT_L = 19.5
assert abs(B_LEN + 2 * F_LEN + FLAP_LEN - PITCH) < 1e-9
BASE_B = 2 * F_LEN * math.cos(ALPHA)
X_PIN = BASE_B - FLAP_LEN
H_TENT = F_LEN * math.sin(ALPHA)
Y_KB, Y_RIDGE, Y_FF, Y_BOT = B_LEN, B_LEN + F_LEN, B_LEN + 2 * F_LEN, PITCH
Y_FO = Y_BOT + TAB_RISE
Y_SLIT = Y_KB - X_PIN
X0 = (SHEET_W - NCOL * COLW) / 2          # 13  (>= 10 mm gripper on the short edge)
Y0 = (SHEET_H - (NROW * PITCH + TAB_L)) / 2
# divider inclinations in degrees (x shifts by tan(a) per mm of y), pivot at the row mid line
ANG = [(6.0, 9.0, 12.0), (-10.0, -7.0, -12.0), (8.0, 12.0, 7.0)]
NAMES = ['Sophia Zhuravkova', 'Ivan Petrov', 'Alexandra Vorontsova', 'Mila Orlova', 'Tim Gerasimov',
         'Nadezhda Kuznetsova', 'Oleg Sidorov', 'Anna Li', 'Maximilian Kovalev', 'Daria Belova', 'Pavel Arkhipov', 'Elena Smirnova']
TABLE = '4'
LINE_S = 28.0                              # heavy line: distance from the table edge of K (s), stroke width
LINE_W = 2.4
def name_size(n): return fit_size(n, 80.0, 7.2)

def ytop(r): return Y0 + PITCH * r
def ymid(r): return ytop(r) + PITCH / 2

def xdiv(r, j, y):
    """x of divider j (0..NCOL-2) in row r at height y"""
    return X0 + COLW * (j + 1) + math.tan(math.radians(ANG[r][j])) * (y - ymid(r))

def xl(r, c, y): return X0 if c == 0 else xdiv(r, c - 1, y)
def xr(r, c, y): return X0 + NCOL * COLW if c == NCOL - 1 else xdiv(r, c, y)

def x_tab(r, c):
    """x of the tab (and of the slit) of piece (r,c): centre of the overlap of its bottom edge and the top edge of (r+1,c)"""
    y1 = ytop(r) + PITCH
    a, b = xl(r, c, y1), xr(r, c, y1)
    if r + 1 < NROW:
        a, b = max(a, xl(r + 1, c, y1)), min(b, xr(r + 1, c, y1))
    return (a + b) / 2

def piece_poly(r, c):
    y0 = ytop(r); y1 = y0 + PITCH
    pts = [(xl(r, c, y0), y0)]
    if r > 0:
        xt = x_tab(r - 1, c)
        pts += [(xt - TAB_W / 2, y0), (xt - TAB_W / 2, y0 + TAB_L), (xt + TAB_W / 2, y0 + TAB_L), (xt + TAB_W / 2, y0)]
    pts.append((xr(r, c, y0), y0)); pts.append((xr(r, c, y1), y1))
    xt = x_tab(r, c)
    pts += [(xt + TAB_W / 2, y1), (xt + TAB_W / 2, y1 + TAB_L), (xt - TAB_W / 2, y1 + TAB_L), (xt - TAB_W / 2, y1)]
    pts.append((xl(r, c, y1), y1))
    return Polygon(pts)

def band_poly(r, c, a, b):
    y0 = ytop(r); return piece_poly(r, c).intersection(box(0, y0 + a, SHEET_W, y0 + b))

def cut_network():
    lines = []
    xa, xb = X0, X0 + NCOL * COLW
    for rb in range(NROW + 1):
        y = Y0 + PITCH * rb
        p = Path((xa, y))
        if rb > 0:
            for c in range(NCOL):
                xt = x_tab(rb - 1, c)
                p.L((xt - TAB_W / 2, y)).L((xt - TAB_W / 2, y + TAB_L)).L((xt + TAB_W / 2, y + TAB_L)).L((xt + TAB_W / 2, y))
        p.L((xb, y)); lines.append(p)
    lines.append(Path((xa, Y0)).L((xa, Y0 + NROW * PITCH))); lines.append(Path((xb, Y0)).L((xb, Y0 + NROW * PITCH)))
    for r in range(NROW):
        for j in range(NCOL - 1):
            lines.append(Path((xdiv(r, j, ytop(r)), ytop(r))).L((xdiv(r, j, ytop(r) + PITCH), ytop(r) + PITCH)))
    return lines

# ---------------------------------------------------------------- artwork
def piece_art(r, c, idx, ink=INK, dx=0.0, dy=0.0):
    y0 = ytop(r) + dy
    name = NAMES[idx % len(NAMES)]; s = name_size(name); seat = '%02d' % (idx + 1)
    fb = band_poly(r, c, Y_RIDGE, Y_FF); kb = band_poly(r, c, Y_KB, Y_RIDGE)
    cF, cK = fb.centroid.x + dx, kb.centroid.x + dx
    o = txt(cF, y0 + Y_FF - 14.0, name, s, fill=ink)
    o += txt(cF, y0 + Y_FF - 25.0, f'TABLE {TABLE}  ·  SEAT {seat}', SEC, weight=700, tracking=0.05, fill=ink)
    o += txt(cK, y0 + Y_KB + 10.0, name, s, rot=180, fill=ink)
    o += txt(cK, y0 + Y_KB + 19.0, 'DINNER  ·  10.10.2026', SEC, weight=700, tracking=0.05, rot=180, fill=ink)
    return o

def heavy_line_path(ox=0, oy=0):
    """one continuous serpentine: row0 left->right, margin loop right, row1 right->left, margin loop left, row2 left->right"""
    xa, xb = X0, X0 + NCOL * COLW
    mr, ml = xb + 6.5, xa - 6.5
    ys = [ytop(r) + Y_KB + LINE_S for r in range(NROW)]
    pts = [(xa, ys[0]), (xb, ys[0]), (mr, ys[0]), (mr, ys[1]), (xb, ys[1]), (xa, ys[1]), (ml, ys[1]), (ml, ys[2]), (xa, ys[2]), (xb, ys[2])]
    return 'M' + ' L'.join(f'{x+ox:.3f} {y+oy:.3f}' for x, y in pts)

def features(r, c):
    y0 = ytop(r); xt = x_tab(r, c)
    cre = [((xl(r, c, y0 + off), y0 + off), (xr(r, c, y0 + off), y0 + off)) for off in (Y_KB, Y_RIDGE, Y_FF)]
    cre.append(((xt - TAB_W / 2, y0 + Y_BOT), (xt + TAB_W / 2, y0 + Y_BOT)))
    rev = ((xt - TAB_W / 2, y0 + Y_FO), (xt + TAB_W / 2, y0 + Y_FO))
    slit = (xt - SLIT_L / 2, y0 + Y_SLIT - SLOT_W / 2, SLIT_L, SLOT_W)
    return cre, rev, slit

def slit_svg(slit):
    x, y, w, h = slit
    return f'<rect x="{x:.3f}" y="{y:.3f}" width="{w}" height="{h}" {slot_style(0.15)}/>'

def line_svg(a, b, style): return f'<line x1="{a[0]:.3f}" y1="{a[1]:.3f}" x2="{b[0]:.3f}" y2="{b[1]:.3f}" {style}/>'
REV_STYLE = crease_style(0.25, '4 0.8 0.3 0.8')

# ================================================================= sheet
def build_sheet():
    W, H = SHEET_W, SHEET_H + 22
    art = f'<rect x="{X0-BLEED}" y="{Y0-BLEED}" width="{NCOL*COLW+2*BLEED}" height="{NROW*PITCH+TAB_L+2*BLEED}" fill="{YELLOW}"/>'
    bleedp = f'<rect x="{X0-BLEED}" y="{Y0-BLEED}" width="{NCOL*COLW+2*BLEED}" height="{NROW*PITCH+TAB_L+2*BLEED}" {bleed_style(0.2)}/>'
    cre = ''; slits = ''
    for r in range(NROW):
        for c in range(NCOL):
            idx = r * NCOL + c
            art += piece_art(r, c, idx)
            cs, rv, sl = features(r, c)
            for a, b in cs: cre += line_svg(a, b, crease_style(0.25))
            cre += line_svg(*rv, REV_STYLE); slits += slit_svg(sl)
    line = f'<path d="{heavy_line_path()}" fill="none" stroke="{INK}" stroke-width="{LINE_W}" stroke-linejoin="miter"/>'
    cut = ''.join(f'<path d="{p.d()}" {cut_style(0.3)}/>' for p in cut_network())
    furn = (f'<rect x="0" y="0" width="{W}" height="{SHEET_H}" fill="none" stroke="#999" stroke-width="0.3"/>'
            f'<rect x="0" y="0" width="10" height="{SHEET_H}" fill="#000" fill-opacity="0.06"/>' + ui(5, SHEET_H / 2, 'GRIPPER', 2.2, 'middle', '#666', rot=-90))
    for (cx, cy) in [(4, 4), (4, SHEET_H - 4), (W - 4, 4), (W - 4, SHEET_H - 4)]:
        furn += (f'<circle cx="{cx}" cy="{cy}" r="1.5" fill="none" stroke="#000" stroke-width="0.2"/><line x1="{cx-3}" y1="{cy}" x2="{cx+3}" y2="{cy}" stroke="#000" stroke-width="0.15"/><line x1="{cx}" y1="{cy-3}" x2="{cx}" y2="{cy+3}" stroke="#000" stroke-width="0.15"/>')
    furn += ui(X0, SHEET_H + 7, 'D3 v2  SRA3 landscape 450 x 320, LONG GRAIN along x = parallel to every crease. 12 tents, mosaic 424 x 303 (+6.5 tabs). All 5 creases per piece scored from the BACK.', 2.4, 'start', '#222', 700)
    furn += ui(X0, SHEET_H + 12, 'Heavy line (2.4 mm) runs over the rear leaf of all 12 pieces and joins in the trim margin: the full line shows only when the pieces are collected.', 2.4)
    furn += ui(X0, SHEET_H + 17, 'Pre-coloured lemon board, no bleed. Through-cut (no nicks), deliver in a tray. Creases 1-4 mountain, 5 (fold-over, hidden) against its score.', 2.4)
    body = (layer('bleed', 'bleed (only if flood-printed)', bleedp) + layer('artwork', 'artwork - lemon + black type', art) + layer('line', 'artwork - heavy black line', line) +
            layer('cut', 'cut', cut) + layer('crease', 'crease (all scored from the back)', cre) + layer('slot', 'slot (lock slits)', slits) + layer('sheet', 'sheet', furn))
    return svg_doc(W, H, body, 'D3 v2 SRA3 dieline 1:1 (mm)', '12 skewed tents, long grain', bg='#ffffff')

# ================================================================= single piece
def uih(x, y, t, size=2.4, anchor='start', fill='#333', weight=500):
    return txt(x, y, t, size, anchor, weight, fill, 0, 'class="ui" stroke="#ffffff" stroke-width="1.4" paint-order="stroke" stroke-linejoin="round"')

def build_piece():
    r, c = 1, 1
    W, H = 330, 262
    ox, oy = 52.0, 22.0
    p0 = piece_poly(r, c); minx = p0.bounds[0]
    dx = ox - minx; dy = oy - ytop(r)
    sh = lambda pts: [(x + dx, y + dy) for x, y in pts]
    nb = ''
    for rr in range(max(0, r - 1), min(NROW, r + 2)):
        for cc in range(max(0, c - 1), min(NCOL, c + 2)):
            if (rr, cc) == (r, c): continue
            nb += f'<path d="{poly_d(sh(list(piece_poly(rr, cc).exterior.coords)))}" fill="none" stroke="{C_CUT}" stroke-opacity="0.3" stroke-width="0.2"/>'
    mine = sh(list(p0.exterior.coords))
    art = f'<path d="{poly_d(mine)}" fill="{YELLOW}"/>' + f'<g transform="translate({dx} {dy})">{piece_art(r, c, 5)}</g>'
    y0 = ytop(r) + dy
    ln = f'<g transform="translate({dx} {dy})"><path d="M{xl(r,c,ytop(r)+Y_KB+LINE_S)-30:.2f} {ytop(r)+Y_KB+LINE_S:.2f} L{xr(r,c,ytop(r)+Y_KB+LINE_S)+30:.2f} {ytop(r)+Y_KB+LINE_S:.2f}" stroke="{INK}" stroke-width="{LINE_W}" fill="none"/></g>'
    cs, rv, sl = features(r, c)
    cre = ''.join(line_svg((a[0]+dx, a[1]+dy), (b[0]+dx, b[1]+dy), crease_style(0.3)) for a, b in cs)
    cre += line_svg((rv[0][0]+dx, rv[0][1]+dy), (rv[1][0]+dx, rv[1][1]+dy), crease_style(0.3, '4 0.8 0.3 0.8'))
    slit = (sl[0] + dx, sl[1] + dy, sl[2], sl[3])
    xrb = max(x for x, y in mine)
    labx = xrb + 6
    marks = [(Y_KB, '2  K-B crease: B folds under (mountain)'), (Y_RIDGE, '1  ridge F / K (mountain)'), (Y_FF, '3  F-flap crease: flap folds under (mountain)'),
             (Y_BOT, '4  tab hinge (mountain)'), (Y_FO, '5  tab fold-over: AGAINST the score, hidden, 3.0 mm after crease 4')]
    lab = ''.join(uih(labx, y0 + off + 0.8, t, 2.4, 'start', C_CREASE) for off, t in marks)
    lab += uih(labx, y0 + Y_SLIT + 0.8, f'slit {SLIT_L} x {SLOT_W} (tab of the flap goes through)', 2.4, 'start', C_SLOT)
    lab += uih(labx, y0 + 2.5, 'notch: takes the tab of the piece above', 2.4, 'start', C_CUT)
    lab += uih(labx, y0 + Y_KB + LINE_S + 0.8, 'heavy line 2.4 mm (on K, outside)', 2.4, 'start', '#111', 700)
    minx_ = min(x for x, y in mine)
    for off, t in (((0 + Y_KB) / 2, 'B  base  20'), ((Y_KB + Y_RIDGE) / 2, 'K  rear leaf  34.5'), ((Y_RIDGE + Y_FF) / 2, 'F  front leaf  34.5'), ((Y_FF + Y_BOT) / 2, 'flap  12')):
        lab += uih(minx_ - 5, y0 + off + 0.8, t, 2.5, 'end', '#333', 700)
    # inclination callouts
    angl = f'{ANG[r][c-1]:+.0f} deg left edge, {ANG[r][c]:+.0f} deg right edge (to the vertical)'
    lab += uih(minx_ + 40, y0 + PITCH + TAB_L + 9, angl, 2.5, 'start', '#111', 700)
    sx, sy = 10.0, 148.0
    nm = NAMES[5]
    lines = [('SPEC', 700),
             ('Board: PRE-COLOURED lemon, 400 g/m2 (0.50) - or 350 g (0.44, slit 0.60) if the digital press tops out at 300-350 g. Grain along the creases.', 500),
             (f'Tent: leaf {F_LEN} at {math.degrees(ALPHA):.0f} deg -> height {H_TENT:.1f}, depth {BASE_B:.2f}; closure {BASE_B:.2f} = flap {FLAP_LEN:.0f} + pin {X_PIN:.2f}', 500),
             (f'Slit {SLIT_L} x {SLOT_W}; tab {TAB_W} wide, {TAB_L} long = riser {TAB_RISE} + fold-over {TAB_FO}. Crease pitch >= 3.0 mm everywhere (20 / 54.5 / 89 / 101 / 104).', 500),
             (f'Name {name_size(nm):.1f} mm Wix Madefor Text Medium ("{nm}" {text_w(nm, name_size(nm)):.0f} mm). Table/seat + date {SEC} mm = 3.5 mm caps. Name 14-19 mm up the leaf (13-18 mm above the table).', 500),
             ('Print: black on lemon; for lemon type on black swap colours (same die).', 500),
             ('Side edges of every piece are straight and inclined 6-12 deg (see the callout); neighbours share the cut line, tab and notch nest: zero waste.', 500)]
    spec = ''; yy = sy
    for i, (t, w_) in enumerate(lines):
        spec += ui(sx, yy, t, 2.8 if i == 0 else 2.4, 'start', '#555' if i == 0 else '#222', w_); yy += 4.4
    leg = legend(sx, 184, [('cut', 'Cut, shared with neighbours'), ('crease', 'Crease, scored from the BACK (mountain)'), ('valley', 'Crease 5, folded against its score'),
                           ('slot', 'Slit 0.70'), ('safe', 'Safe area'), ('art', 'Board colour #feed95')], 'Legend')
    leg = leg.replace('stroke-dasharray="0.2 1.0"', 'stroke-dasharray="4 0.8 0.3 0.8"')
    body = (layer('neighbours', 'neighbour pieces', f'<clipPath id="nbc"><rect x="0" y="0" width="330" height="140"/></clipPath><g clip-path="url(#nbc)">{nb}</g>') +
            layer('artwork', 'artwork', art + f'<clipPath id="pc"><path d="{poly_d(mine)}"/></clipPath><g clip-path="url(#pc)">{ln}</g>') +
            layer('cut', 'cut', f'<path d="{poly_d(mine)}" {cut_style(0.3)}/>') + layer('crease', 'crease', cre) + layer('slot', 'slot', slit_svg(slit)) +
            layer('annotations', 'labels + legend', lab + spec + leg))
    return svg_doc(W, H, body, 'D3 v2 single piece 1:1 (mm)', 'skewed tent piece with neighbours', bg='#ffffff')

# ================================================================= 3D
def tent_faces(r, c, ax, off, idx, side='front'):
    y0 = ytop(r)
    fb = band_poly(r, c, Y_RIDGE, Y_FF); X0c = fb.centroid.x
    ca, sa = math.cos(ALPHA), math.sin(ALPHA)
    yKb, yFb = F_LEN * ca, -F_LEN * ca
    ox, oy = off
    F = lambda X, Y: (X - X0c + ox, oy - (Y - (y0 + Y_RIDGE)) * ca, H_TENT - (Y - (y0 + Y_RIDGE)) * sa)
    K = lambda X, Y: (X - X0c + ox, oy + ((y0 + Y_RIDGE) - Y) * ca, H_TENT - ((y0 + Y_RIDGE) - Y) * sa)
    Bm = lambda X, Y: (X - X0c + ox, oy + yKb - ((y0 + Y_KB) - Y), 0.5)
    Fl = lambda X, Y: (X - X0c + ox, oy + yFb + (Y - (y0 + Y_FF)), 0.0)
    pl = lambda g, f: [f(x, y) for x, y in list(g.exterior.coords)[:-1]]
    f_pts, k_pts = pl(fb, F), pl(band_poly(r, c, Y_KB, Y_RIDGE), K)
    b_pts, fl_pts = pl(band_poly(r, c, 0, Y_KB), Bm), pl(band_poly(r, c, Y_FF, Y_BOT), Fl)
    shadows = ''.join(f'<path d="{face_d(ax, shadow_pts(pts, 0.5, -0.3))}" fill="#000" fill-opacity="0.07"/>' for pts in (f_pts, k_pts))
    name = NAMES[idx % len(NAMES)]; s = name_size(name); seat = '%02d' % (idx + 1)
    # F art
    MF = ax.matrix(F(0.0, 0.0), (1, 0, 0), (0, -ca, -sa))
    tF = (txt(X0c, y0 + Y_FF - 14.0, name, s) + txt(X0c, y0 + Y_FF - 25.0, f'TABLE {TABLE}  ·  SEAT {seat}', SEC, weight=700, tracking=0.05))
    clipF = f'<clipPath id="cf{r}{c}{side}"><path d="{poly_d([(x, y) for x, y in fb.exterior.coords])}"/></clipPath>'
    svgF = (f'<path d="{face_d(ax, f_pts)}" fill="{YELLOW}" stroke="#222" stroke-width="0.35" stroke-linejoin="round"/>'
            f'<g transform="{MF}">{tF}</g>')
    # K art (outer face) incl. heavy line segment
    MK = ax.matrix(K(0.0, 0.0), (1, 0, 0), (0, -ca, sa))
    cK = band_poly(r, c, Y_KB, Y_RIDGE).centroid.x
    yl = y0 + Y_KB + LINE_S
    tK = (txt(cK, y0 + Y_KB + 10.0, name, s, rot=180) + txt(cK, y0 + Y_KB + 19.0, 'DINNER  ·  10.10.2026', SEC, weight=700, tracking=0.05, rot=180) +
          f'<path d="M{xl(r,c,yl)-5:.2f} {yl:.2f} L{xr(r,c,yl)+5:.2f} {yl:.2f}" stroke="{INK}" stroke-width="{LINE_W}"/>')
    kb = band_poly(r, c, Y_KB, Y_RIDGE)
    clipK = f'<clipPath id="ck{r}{c}{side}"><path d="{poly_d(list(kb.exterior.coords))}"/></clipPath>'
    svgK = (f'<path d="{face_d(ax, k_pts)}" fill="{YELLOW}" stroke="#222" stroke-width="0.35" stroke-linejoin="round"/>'
            f'<g transform="{MK}" clip-path="url(#ck{r}{c}{side})">{tK}</g>')
    inner = (f'<path d="{face_d(ax, fl_pts)}" fill="#eadb86" stroke="#222" stroke-width="0.2" stroke-linejoin="round"/>'
             f'<path d="{face_d(ax, b_pts)}" fill="#f1e08f" stroke="#222" stroke-width="0.2" stroke-linejoin="round"/>')
    inner_K = f'<path d="{face_d(ax, k_pts)}" fill="#f3e08a" stroke="#222" stroke-width="0.3" stroke-linejoin="round"/>'
    defs = clipF + clipK
    if side == 'front':
        return defs, shadows, inner_K + inner + svgF
    return defs, shadows, inner + (f'<path d="{face_d(ax, f_pts)}" fill="#f3e08a" stroke="#222" stroke-width="0.3" stroke-linejoin="round"/>') + svgK

def build_assembled():
    W, H = 300, 430
    out = ui(10, 12, 'D3 v2  ONE SHEET FOR THE WHOLE TABLE  -  assembled', 4.0, 'start', '#111', 700)
    out += ui(10, 17.8, 'Four of the twelve tents: skewed outlines, same mechanism. Top: guest side. Middle: seen from behind (name rotated, heavy line fragment).', 2.5)
    picks = [(0, 0, 0), (1, 2, 6), (2, 1, 9), (0, 3, 3)]
    offs = [(-62, 30), (62, 30), (-62, -30), (62, -30)]
    defs_all = ''
    for sidx, (side, yaw, oy) in enumerate((('front', -30, 78), ('back', 150, 190))):
        ax = Axo(yaw_deg=yaw, elev_deg=26, ox=150, oy=oy, k=0.74)
        order = sorted(zip(picks, offs), key=lambda t: -ax.depth((t[1][0], t[1][1], 0)))
        out += f'<path d="{face_d(ax, [(-135,-80,-0.5),(135,-80,-0.5),(135,80,-0.5),(-135,80,-0.5)])}" fill="#ecebe4"/>'
        sh_all = ''; sc_all = ''
        for (r, c, i), off in order:
            d_, sh, sc = tent_faces(r, c, ax, off, i, side)
            defs_all += d_; sh_all += sh; sc_all += sc
        out += sh_all + sc_all
    # section + lock detail
    k = 3.4; sx0, sz0 = 40.0, 405.0
    P = lambda y, z: (sx0 + k * (y + F_LEN * math.cos(ALPHA)), sz0 - k * z)
    ca, sa = math.cos(ALPHA), math.sin(ALPHA)
    yKb, yFb = F_LEN * ca, -F_LEN * ca
    sec = f'<line x1="{sx0-10}" y1="{sz0}" x2="{sx0+k*BASE_B+60}" y2="{sz0}" stroke="#222" stroke-width="0.5"/>'
    def seg(a, b, w=T, col='#222'):
        pa, pb = P(*a), P(*b); return f'<line x1="{pa[0]:.2f}" y1="{pa[1]:.2f}" x2="{pb[0]:.2f}" y2="{pb[1]:.2f}" stroke="{col}" stroke-width="{k*w:.2f}"/>'
    ypin = yFb + FLAP_LEN
    sec += seg((yFb, 0), (0, H_TENT)) + seg((0, H_TENT), (yKb, 0)) + seg((yKb, 1.5 * T + T / 2), (yKb - B_LEN, 1.5 * T + T / 2), col='#555') + seg((yFb, T / 2), (ypin, T / 2), col='#777')
    sec += seg((ypin, T / 2), (ypin, T / 2 + TAB_RISE + T), col='#c00') + seg((ypin, T / 2 + TAB_RISE + T), (ypin + TAB_FO, T / 2 + TAB_RISE + T), col='#c00')
    sec += ui(10, 290, 'SECTION THROUGH THE TENT  3.4:1', 2.6, 'start', '#555', 700)
    sec += ui(P(0, H_TENT)[0] + 3, P(0, H_TENT)[1] + 1, f'ridge, height {H_TENT:.1f}', 2.3, 'start', '#444')
    sec += dim_h(P(yFb, 0)[0], P(yKb, 0)[0], sz0 + 9, f'{BASE_B:.2f} depth') + dim_h(P(yFb, 0)[0], P(ypin, 0)[0], sz0 + 15, f'flap {FLAP_LEN:.0f}') + dim_h(P(ypin, 0)[0], P(yKb, 0)[0], sz0 + 15, f'{X_PIN:.2f}')
    sec += ui(P(yKb, 20)[0] + 14, P(yKb, 20)[1], f'leaf {F_LEN} mm at {math.degrees(ALPHA):.0f} deg', 2.3, 'start', '#555')
    kk = 14.0; dx0, dz0 = 215.0, 405.0
    Q = lambda y, z: (dx0 + kk * (y - ypin), dz0 - kk * z)
    def rect(y0_, y1_, z0_, z1_, fill, stroke='#222'):
        a_, b_ = Q(y0_, z1_), Q(y1_, z0_); return f'<rect x="{a_[0]:.2f}" y="{a_[1]:.2f}" width="{b_[0]-a_[0]:.2f}" height="{b_[1]-a_[1]:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="0.25"/>'
    det = f'<line x1="{dx0-60}" y1="{dz0}" x2="{dx0+66}" y2="{dz0}" stroke="#222" stroke-width="0.5"/>'
    det += rect(ypin - 4.2, ypin, 0, T, '#e8d98a') + rect(ypin - 4.2, ypin - SLOT_W / 2, T, 2 * T, '#f4e49a') + rect(ypin + SLOT_W / 2, ypin + 3.6, T, 2 * T, '#f4e49a')
    det += rect(ypin - T / 2, ypin + T / 2, 0, TAB_RISE, '#d33', '#900') + rect(ypin - T / 2, ypin + TAB_FO, TAB_RISE - T, TAB_RISE, '#d33', '#900')
    det += ui(dx0 - 55, dz0 - 55, 'LOCK DETAIL  14:1', 2.6, 'start', '#555', 700) + ui(dx0 - 55, dz0 - 50, f'flap under, B over, slit {SLOT_W}, tab riser {TAB_RISE} + fold-over {TAB_FO}', 2.2, 'start', '#444')
    det += dim_h(Q(ypin - SLOT_W / 2, 0)[0], Q(ypin + SLOT_W / 2, 0)[0], dz0 + 8, '0.70')
    return svg_doc(W, H, f'<defs>{defs_all}</defs>' + out + sec + det, 'D3 v2 assembled', 'front + back views, section', bg='#ffffff')

# ================================================================= scaling
def build_scaling():
    W, H = 300, 205
    out = ui(10, 12, 'D3 v2  HOW IT SCALES', 4.0, 'start', '#111', 700)
    out += ui(10, 17.8, 'One SRA3 (landscape, long grain) = one table of 12 seats; seat 01-12 in reading order = the table plan. The heavy line completes only when the 12 pieces are back together.', 2.4)
    sc = 0.105; x = 10
    for guests, sheets in ((12, 1), (24, 2), (36, 3), (48, 4), (60, 5)):
        for s in range(sheets):
            sx, sy = x + s * 3.0, 30 + s * 3.0
            out += f'<rect x="{sx}" y="{sy}" width="{SHEET_W*sc}" height="{SHEET_H*sc}" fill="{YELLOW}" stroke="#222" stroke-width="0.3"/>'
            if s == sheets - 1:
                for r in range(NROW):
                    for c in range(NCOL):
                        out += f'<path d="{poly_d([(sx + px*sc, sy + py*sc) for px, py in piece_poly(r, c).exterior.coords])}" fill="none" stroke="{C_CUT}" stroke-width="0.2"/>'
                out += f'<path d="{heavy_line_path(0,0).replace("M","M").replace(" L"," L")}" fill="none" stroke="none"/>'
        out += ui(x, 30 + SHEET_H * sc + sheets * 3 + 7, f'{guests} guests', 3.0, 'start', '#111', 700) + ui(x, 30 + SHEET_H * sc + sheets * 3 + 11.5, f'{sheets} sheet{"s" if sheets > 1 else ""}', 2.5)
        x += 55
    ty = 100
    out += ui(10, ty, 'Rules of thumb', 3.0, 'start', '#111', 700)
    lines = ['sheets = ceil(guests / 12).  20 guests -> 2 sheets (4 spare); 40 -> 4 (8 spare); 60 -> 5 (0 spare).',
             'By table: one sheet per table of 12. Table of 8: use rows 1-2 (8 pieces; the die already cuts them apart) and keep row 3 as spares. Tables of 6 / 10: same tile, cut-down die (3 x 2 / 5 x 2).',
             'Tooling: ONE steel-rule die with creasing rules on ONE side (all creases scored from the back), through-cut, no nicks; deliver in a tray. Names printed digitally BEFORE die-cutting.',
             'Digital press weight: many stop at 300-350 g. Use 350 g (0.44) + slit 0.60, or litho / screen for 400 g.',
             'Assembly: 5 folds per tent; estimate 40-60 s for the first dozen, 25-30 s later. Pre-assembled tents are 33 mm high (no longer flat): assemble at the venue.',
             'Other formats: the same 106 x 101 tile on B2 (500 x 707) gives 4 x 6 = 24 per sheet (long grain along 707). Laser: kerf 0.2 on shared lines = 0.2 gap and edge scorch on lemon; plotter needs >= 5 knife passes and an oscillating knife.',
             'At the end of the night the 12 pieces are collected and laid back into the sheet outline: the heavy line is whole again (it is also the staff\'s reason to count the cards back).']
    yy = ty + 5.5
    for t in lines:
        out += ui(10, yy, t, 2.4, 'start', '#222'); yy += 5.2
    return svg_doc(W, H, out, 'D3 v2 scaling', 'sheet counts', bg='#ffffff')

# ================================================================= verification
def verify():
    out = ['=== D3 v2 verification ==='] ; ok = True
    def chk(c, m):
        nonlocal ok
        out.append(('PASS ' if c else 'FAIL ') + m); ok &= bool(c)
    polys = {(r, c): piece_poly(r, c) for r in range(NROW) for c in range(NCOL)}
    keys = list(polys)
    maxov = max(polys[keys[i]].intersection(polys[keys[j]]).area for i in range(len(keys)) for j in range(i + 1, len(keys)))
    chk(maxov < 1e-6, f'no overlaps (max pairwise {maxov:.2e} mm2)')
    uni = unary_union(list(polys.values()))
    mosaic = box(X0, Y0, X0 + NCOL * COLW, Y0 + NROW * PITCH)
    chk(mosaic.difference(uni).area < 1e-6, f'no gaps: uncovered mosaic area {mosaic.difference(uni).area:.2e} mm2')
    extra = uni.difference(mosaic).area
    chk(abs(extra - NCOL * TAB_W * TAB_L) < 1e-6, f'only protrusion = the {NCOL} tabs of the last row ({extra:.1f} mm2)')
    b = uni.bounds
    chk(b[0] >= 10 and b[2] <= SHEET_W - 4 and b[1] >= 4 and b[3] <= SHEET_H - 4, f'inside the sheet; left margin {b[0]:.1f} (gripper >= 10), others >= 4; bounds {tuple(round(v,1) for v in b)}')
    chk(abs(SHEET_W - 450) < 1e-9 and Y_KB > 0, 'creases run along x = the 450 mm side = long grain of a standard SRA3 (grain parallel to creases)')
    # distinct shapes: normalise by centroid, round
    sigs = set()
    for p in polys.values():
        cx, cy = p.centroid.x, p.centroid.y
        sigs.add(tuple(sorted((round(x - cx, 1), round(y - cy, 1)) for x, y in list(p.exterior.coords)[:-1])))
    chk(len(sigs) == 12, f'12 pieces = {len(sigs)} distinct outlines (no two congruent by translation)')
    angs = [abs(a) for row in ANG for a in row]
    chk(min(angs) >= 6 and max(angs) <= 12, f'divider inclinations {sorted(set(angs))} deg (6-12)')
    out.append('INFO inclinations per row (left->right dividers): ' + '; '.join(str(a) for a in ANG))
    # widths
    minw = 1e9
    for (r, c), p in polys.items():
        for a, bb in ((Y_RIDGE, Y_FF), (Y_KB, Y_RIDGE)):
            band = band_poly(r, c, a, bb)
            for y in np.linspace(band.bounds[1] + 0.2, band.bounds[3] - 0.2, 20):
                minw = min(minw, LineString([(0, y), (SHEET_W, y)]).intersection(band).length)
    chk(minw >= 92.0, f'narrowest F / K leaf width {minw:.1f} mm (name safe 80 + 2 x 6)')
    # tab / notch fit
    mc = 1e9
    for r in range(NROW - 1):
        for c in range(NCOL):
            xt = x_tab(r, c); y1 = ytop(r) + PITCH
            lo, hi = xl(r + 1, c, y1), xr(r + 1, c, y1)
            mc = min(mc, xt - TAB_W / 2 - lo, hi - xt - TAB_W / 2 - 0)
            lo2, hi2 = xl(r, c, y1), xr(r, c, y1)
            mc = min(mc, xt - TAB_W / 2 - lo2, hi2 - (xt + TAB_W / 2))
    chk(mc >= 6.0, f'every tab / notch is >= {mc:.1f} mm from the side edges of both pieces')
    ms = 1e9
    for (r, c) in polys:
        yb = ytop(r) + Y_SLIT; xt = x_tab(r, c)
        ms = min(ms, xt - SLIT_L / 2 - xl(r, c, yb), xr(r, c, yb) - (xt + SLIT_L / 2))
    chk(ms >= 20, f'slit ends >= {ms:.1f} mm from the sides')
    # closure and clearances
    chk(abs(BASE_B - (FLAP_LEN + X_PIN)) < 1e-9, f'closure: depth {BASE_B:.3f} = flap {FLAP_LEN} + pin {X_PIN:.3f}')
    chk(B_LEN < BASE_B - 1.0, f'B ({B_LEN}) ends {BASE_B-B_LEN:.2f} mm short of the F foot')
    clr = (B_LEN - TAB_L) - X_PIN - SLOT_W / 2
    chk(clr >= 3.0, f'slit clears the notch bottom by {clr:.2f} mm')
    chk(B_LEN > X_PIN + SLOT_W / 2 + 3, f'B ear beyond the slit {B_LEN-X_PIN-SLOT_W/2:.2f} mm')
    chk(TAB_RISE > 2 * T and TAB_FO >= 3, f'riser {TAB_RISE} > B + flap ({2*T}); fold-over {TAB_FO}')
    offs = sorted([Y_KB, Y_RIDGE, Y_FF, Y_BOT, Y_FO]); gaps = [round(offs[i + 1] - offs[i], 2) for i in range(4)]
    chk(min(gaps) >= 3.0, f'crease pitches {gaps} mm (>= 3.0 for a 0.71 rule + counter)')
    chk(SLOT_W >= T + 0.1, f'slit {SLOT_W} for one board layer (clearance {SLOT_W-T:.2f})')
    # text
    chk(CAP * SEC >= 3.45, f'secondary type {SEC} mm -> caps {CAP*SEC:.2f} mm (table / seat / date)')
    chk(Y_FF - 25.0 - (Y_FF - 14.0 - 0) < 0 and (25.0 + CAP * SEC) < F_LEN - 5, f'F: name baseline s=14, caption s=25 (cap top {25+CAP*SEC:.1f}) leaves {F_LEN-25-CAP*SEC:.1f} to the ridge; name 13-18 mm above the table')
    ln_lo, ln_hi = LINE_S - LINE_W / 2, LINE_S + LINE_W / 2
    chk(19.0 + CAP * SEC < ln_lo - 2 and ln_hi < F_LEN - 3, f'K: date cap top {19+CAP*SEC:.1f} < heavy line {ln_lo:.1f}..{ln_hi:.1f} < ridge at {F_LEN}')
    for nm in NAMES + ['Mikhail Terentyev-Z']:
        assert text_w(nm, name_size(nm)) <= 80.01
    chk(True, 'all names (+ a 19-char one) fit the 80 mm safe width at <= 7.2 mm')
    # stability
    ca, sa = math.cos(ALPHA), math.sin(ALPHA)
    yKb, yFb = F_LEN * ca, -F_LEN * ca
    r, c = 1, 1
    parts = [(band_poly(r, c, Y_RIDGE, Y_FF).area, -F_LEN / 2 * ca, H_TENT - F_LEN / 2 * sa), (band_poly(r, c, Y_KB, Y_RIDGE).area, F_LEN / 2 * ca, H_TENT - F_LEN / 2 * sa),
             (band_poly(r, c, 0, Y_KB).area, yKb - B_LEN / 2, 0.5), (band_poly(r, c, Y_FF, Y_BOT).area, yFb + FLAP_LEN / 2, 0.0)]
    m = sum(p[0] for p in parts); ycom = sum(p[0] * p[1] for p in parts) / m; zcom = sum(p[0] * p[2] for p in parts) / m
    chk(yFb < ycom < yKb, f'COM y {ycom:.2f}, z {zcom:.1f} between the feet {yFb:.2f}..{yKb:.2f}; tip-over {math.degrees(math.atan2(min(ycom-yFb, yKb-ycom), zcom)):.0f} deg')
    out.append(f'INFO tent height {H_TENT:.1f} (v1 34.2), depth {BASE_B:.2f}; mosaic {NCOL*COLW:.0f} x {NROW*PITCH:.0f} on 450 x 320 = {100*NCOL*COLW*NROW*PITCH/(SHEET_W*SHEET_H):.1f} %')
    out.append(f'INFO cut network {len(cut_network())} straight paths; odd nodes 10 -> 5 passes min on a plotter; die / laser: one hit')
    out.append('RESULT ' + ('ALL PASS' if ok else 'SOME FAIL'))
    return '\n'.join(out)

if __name__ == '__main__':
    open(os.path.join(OUT, 'd3_dieline_SRA3.svg'), 'w').write(build_sheet())
    open(os.path.join(OUT, 'd3_piece_detail.svg'), 'w').write(build_piece())
    open(os.path.join(OUT, 'd3_assembled.svg'), 'w').write(build_assembled())
    open(os.path.join(OUT, 'd3_scaling.svg'), 'w').write(build_scaling())
    rep = verify(); open(os.path.join(OUT, 'd3_verify.txt'), 'w').write(rep + '\n'); print(rep)
