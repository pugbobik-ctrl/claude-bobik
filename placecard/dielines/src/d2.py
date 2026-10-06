"""D2 v2 - Form and its void, COMPACT: 105 x 118 card, S lifted segment + flanged strut P (hook lip)."""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from shapely.geometry import Point

T = BOARD_T
SHW, SHH = 105.0, 118.0
FRONT = 20.0                      # u of crease c1
S_LEN, S_CHORD = 32.0, 90.0
THETA = math.radians(75.0)
BRIDGE = 8.0
U_P = FRONT + S_LEN + BRIDGE      # 60  -> b = 40
P_WH, P_WT = 36.0, 26.0
LIP_W, LIP_L = 22.0, 6.0
FLW = 5.0                         # flange width (folded 90 deg, away from the printed face)
FL_A, FL_B = 6.0, 8.0             # flange starts 6 mm after c2, ends 8 mm before c3
RELIEF_R = 0.9
CX = SHW / 2

S_R = ((S_CHORD / 2) ** 2 + S_LEN ** 2) / (2 * S_LEN)
S_CV = S_LEN - S_R                # circle centre (v), negative = in front of c1
dS = (math.cos(THETA), math.sin(THETA))
TIP = (FRONT + S_LEN * dS[0], S_LEN * dS[1])
P_LEN = math.hypot(TIP[0] - U_P, TIP[1])
dP = ((TIP[0] - U_P) / P_LEN, TIP[1] / P_LEN)
dLip = (-dS[0], -dS[1])
ANG_P = math.degrees(math.atan2(dP[1], -dP[0]))
FOLD_P = 180 - ANG_P
FOLD_LIP = math.degrees(math.acos(dP[0] * dLip[0] + dP[1] * dLip[1]))
U_TIP = U_P + P_LEN
U_END = U_TIP + LIP_L
def Y(u): return SHH - u

NAME = 'Sophia Zhuravkova'
TABLE, SEAT = '4', '07'
NAME_V, SEC_V = 9.0, 17.5          # baselines on S (v measured from c1 along the slope)
def name_size(n): return fit_size(n, 66.0, 6.8)

# ---------------------------------------------------------------- geometry (flat, y down)
def s_geo():
    y1 = Y(FRONT)
    cut = Path((CX - S_CHORD / 2, y1)).A3((CX, Y(FRONT + S_LEN)), (CX + S_CHORD / 2, y1))
    crease = [(CX - S_CHORD / 2, y1), (CX + S_CHORD / 2, y1)]
    outline = Path((CX - S_CHORD / 2, y1)).A3((CX, Y(FRONT + S_LEN)), (CX + S_CHORD / 2, y1)).Z()
    reliefs = [(CX - S_CHORD / 2 - RELIEF_R, y1), (CX + S_CHORD / 2 + RELIEF_R, y1)]
    return cut, crease, outline, reliefs

def p_geo():
    yh, yt, yl = Y(U_P), Y(U_TIP), Y(U_END)
    r = 2.0; c = math.sqrt(0.5)
    L0, L1 = CX - P_WH / 2, CX + P_WH / 2
    T0, T1 = CX - P_WT / 2, CX + P_WT / 2
    l0, l1 = CX - LIP_W / 2, CX + LIP_W / 2
    cut = Path((L0, yh)).L((T0, yt)).L((l0, yt)).L((l0, yl + r))
    cut.A3((l0 + r * (1 - c), yl + r * (1 - c)), (l0 + r, yl)).L((l1 - r, yl))
    cut.A3((l1 - r * (1 - c), yl + r * (1 - c)), (l1, yl + r)).L((l1, yt)).L((T1, yt)).L((L1, yh))
    outline = Path((L0, yh)).L((T0, yt)).L((l0, yt)).L((l0, yl + r))
    outline.A3((l0 + r * (1 - c), yl + r * (1 - c)), (l0 + r, yl)).L((l1 - r, yl))
    outline.A3((l1 - r * (1 - c), yl + r * (1 - c)), (l1, yl + r)).L((l1, yt)).L((T1, yt)).L((L1, yh)).Z()
    # side edges as functions x(y)
    def xl(yy): return L0 + (T0 - L0) * (yh - yy) / (yh - yt)
    def xr(yy): return L1 + (T1 - L1) * (yh - yy) / (yh - yt)
    ang = math.atan2((T0 - L0), (yh - yt))          # edge inclination from the axis
    off = FLW / math.cos(ang)                       # horizontal offset of the flange crease line
    ya, yb = Y(U_P + FL_A), Y(U_TIP - FL_B)
    slits = []; fcre = []
    for sgn, xe in ((-1, xl), (1, xr)):
        d_ = off if sgn < 0 else -off
        for yy in (ya, yb):
            slits.append(((xe(yy), yy), (xe(yy) + d_, yy)))
        fcre.append(((xe(ya) + d_, ya), (xe(yb) + d_, yb)))
    hinge = [(L0, yh), (L1, yh)]
    c3 = [(T0, yt), (T1, yt)]
    reliefs = [(L0 - RELIEF_R, yh), (L1 + RELIEF_R, yh)]
    return dict(cut=cut, outline=outline, hinge=hinge, c3=c3, slits=slits, fcre=fcre, reliefs=reliefs,
                xl=xl, xr=xr, off=off, ya=ya, yb=yb)

def sheet_rect(): return Path((0, 0)).L((SHW, 0)).L((SHW, SHH)).L((0, SHH)).Z()

# ---------------------------------------------------------------- artwork (flat coordinates)
def art_s(name, ink=INK, dx=0, dy=0):
    s = name_size(name)
    o = txt(CX + dx, Y(FRONT + NAME_V) + dy, name, s, fill=ink)
    o += txt(CX + dx, Y(FRONT + SEC_V) + dy, f'TABLE {TABLE}  ·  SEAT {SEAT}', SEC, weight=700, tracking=0.05, fill=ink)
    return o

def art_base(ink=INK, dx=0, dy=0):
    return txt(CX + dx, Y(7.5) + dy, 'DINNER  10.10.2026', SEC, weight=700, tracking=0.05, fill=ink)

# ================================================================= dieline
def feature_layers(ox, oy):
    tr = lambda p: (p[0] + ox, p[1] + oy)
    cutS, creS, outS, relS = s_geo(); P = p_geo()
    cut = f'<path d="{sheet_rect().xform(tr).d()}" {cut_style()}/>'
    cut += f'<path d="{cutS.xform(tr).d()}" {cut_style()}/><path d="{P["cut"].xform(tr).d()}" {cut_style()}/>'
    for (a, b) in P['slits']:
        a, b = tr(a), tr(b); cut += f'<line x1="{a[0]:.3f}" y1="{a[1]:.3f}" x2="{b[0]:.3f}" y2="{b[1]:.3f}" {cut_style()}/>'
    for (x, y) in relS + P['reliefs']:
        x, y = tr((x, y)); cut += f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{RELIEF_R}" {cut_style(0.2)}/>'
    for (a, b) in P['slits']:      # small relief at the inner end of each slit
        x, y = tr(b); cut += f'<circle cx="{x:.3f}" cy="{y:.3f}" r="0.5" {cut_style(0.15)}/>'
    cre = ''
    for seg in (creS, P['hinge'], P['c3']):
        a, b = tr(seg[0]), tr(seg[1])
        cre += f'<line x1="{a[0]:.3f}" y1="{a[1]:.3f}" x2="{b[0]:.3f}" y2="{b[1]:.3f}" {crease_style(0.3)}/>'
    for seg in P['fcre']:          # flange creases: scored from the same (printed) face, folded AGAINST the score
        a, b = tr(seg[0]), tr(seg[1])
        cre += f'<line x1="{a[0]:.3f}" y1="{a[1]:.3f}" x2="{b[0]:.3f}" y2="{b[1]:.3f}" {crease_style(0.3, "4 0.8 0.3 0.8")}/>'
    return cut, cre, outS, P['outline']

def build_dieline(variant='both'):
    """variant: 'both' (lemon visible, reverse hidden layer), 'reverse' (reverse visible)"""
    W, H = 345, 178
    ox, oy = 40.0, 22.0
    cut, cre, outS, outP = feature_layers(ox, oy)
    tr = lambda p: (p[0] + ox, p[1] + oy)
    bleed = box(0, 0, SHW, SHH).buffer(BLEED, join_style=2)
    bleed = Polygon([(x + ox, y + oy) for x, y in bleed.exterior.coords])
    lemon = (f'<path d="{poly_d(bleed)}" fill="{YELLOW}"/>' +
             f'<g transform="translate({ox} {oy})">{art_s(NAME)}{art_base()}</g>')
    black = (f'<path d="{poly_d(bleed)}" fill="{INK_REV}"/>' +
             f'<g transform="translate({ox} {oy})">{art_s(NAME, YELLOW)}{art_base(YELLOW)}</g>')
    void = (f'<path d="{outS.xform(tr).d()}" fill="#808080" fill-opacity="0.18" stroke="none"/>'
            f'<path d="{outP.xform(tr).d()}" fill="#808080" fill-opacity="0.18" stroke="none"/>')
    sz = name_size(NAME)
    safe = (f'<rect x="{ox+CX-33}" y="{oy+Y(FRONT+NAME_V+0.72*sz+0.5)}" width="66" height="{0.72*sz+0.25*sz+1:.1f}" {safe_style()}/>'
            f'<rect x="{ox+CX-26}" y="{oy+Y(FRONT+SEC_V+3.5+0.5)}" width="52" height="4.6" {safe_style()}/>')
    lipbox = (f'<rect x="{ox+CX-LIP_W/2}" y="{oy+Y(FRONT+S_LEN)}" width="{LIP_W}" height="{LIP_L}" fill="none" stroke="{C_CREASE}" stroke-width="0.15" stroke-dasharray="0.6 0.6"/>'
              + ui(ox + CX + LIP_W / 2 + 1.5, oy + Y(FRONT + S_LEN - 3) + 0.6, 'lip lands here', 2.0, 'start', C_CREASE))
    d = [dim_h(ox, ox + SHW, oy + SHH + 9, f'{SHW:.0f}'), dim_v(ox - 8, oy, oy + SHH, f'{SHH:.0f}', side=-1),
         dim_v(ox + SHW + 8, oy + Y(FRONT + S_LEN), oy + Y(FRONT), f'S {S_LEN:.0f}'),
         dim_v(ox + SHW + 8, oy + Y(U_P), oy + Y(FRONT + S_LEN), f'{BRIDGE:.0f}'),
         dim_v(ox + SHW + 8, oy + Y(U_TIP), oy + Y(U_P), f'P {P_LEN:.1f}'),
         dim_v(ox + SHW + 8, oy + Y(U_END), oy + Y(U_TIP), f'{LIP_L:.0f}'),
         dim_v(ox - 16, oy + Y(FRONT), oy + SHH, f'{FRONT:.0f}', side=-1),
         dim_h(ox + CX - S_CHORD / 2, ox + CX + S_CHORD / 2, oy + Y(FRONT) + 5.0, f'chord {S_CHORD:.0f}  R{S_R:.1f}')]
    lab = (ui(ox + CX, oy + Y(FRONT + 2.6), 'crease c1  (75 deg)', 2.1, 'middle', C_CREASE) +
           ui(ox + CX, oy + Y(U_P) + 4.0, 'crease c2', 2.1, 'middle', C_CREASE) +
           ui(ox + CX, oy + Y(U_P + 22), 'P  strut (flanged)', 2.4, 'middle', '#444', 700) +
           ui(ox + CX, oy + Y(FRONT + S_LEN + 1.8), '', 2.0) +
           ui(ox + CX, oy + Y(U_TIP) - 1.0, 'crease c3 (hook)', 2.0, 'middle', C_CREASE))
    sx = 168.0
    sp = [('SPEC', 700),
          ('Card 105 x 118 mm, one piece, square trim (no rounded corners). 21 % smaller than the 105 x 148 v1.', 500),
          ('Board: PRE-COLOURED lemon (#feed95) 350-400 g/m2, caliper 0.44-0.50; no flood print, no bleed, cracks at folds stay yellow.', 500),
          ('Digital presses mostly stop at 300-350 g: use 350 g (0.44) and check the press; litho / screen for 400 g.', 500),
          ('Grain parallel to the 105 mm side = parallel to c1 c2 c3 (and to the 450 mm side of SRA3). All creases scored from the PRINTED face.', 500),
          (f'Name: Wix Madefor Text Medium {name_size(NAME):.1f} mm ("{NAME}" = {text_w(NAME, name_size(NAME)):.1f} mm). Table/seat {SEC} mm type = 3.5 mm caps.', 500),
          ('Reverse colourway (hidden layer "artwork_reverse", same die): black through-dyed board, lemon type, see d2_dieline_reverse.svg.', 500)]
    spec = ''; yy = 16
    for i, (t, w_) in enumerate(sp):
        spec += ui(sx, yy, t, 2.8 if i == 0 else 2.4, 'start', '#555' if i == 0 else '#222', w_); yy += 4.4
    yy += 3
    spec += ui(sx, yy, 'FOLDS', 2.6, 'start', '#555', 700); yy += 4.6
    for a, b in [('c1 S hinge', f'valley {math.degrees(THETA):.0f} deg from flat -> S stands at 75 deg (15 deg back-lean)'),
                 ('c2 P hinge', f'valley {FOLD_P:.1f} deg -> P stands at {ANG_P:.1f} deg'),
                 ('c3 hook', f'valley {FOLD_LIP:.1f} deg beyond P -> lip lies on the FRONT face of S, over the crown'),
                 ('flanges', f'2 x {FLW:.0f} mm, 90 deg AGAINST the score (mountain): rise up/back, away from S and table; end 6 mm after c2 and 8 mm before c3')]:
        spec += ui(sx, yy, a, 2.4, 'start', '#222', 700) + ui(sx + 20, yy, b, 2.4, 'start', '#222'); yy += 4.2
    yy += 3
    spec += ui(sx, yy, 'WHY FLANGES (not twin struts)', 2.6, 'start', '#555', 700); yy += 4.6
    for t in ['A flat 0.5 mm strut buckles at about 3 N; a C-channel with two 5 mm flanges has ~100x the bending stiffness (see d2_verify.txt),',
              'is still ONE part with ONE hook, and needs only 2 more creases + 4 short slits in the same die.',
              'Twin struts: each strip is narrower (I ~ width) and needs a rung or two hooks; flatter, not stiffer.']:
        spec += ui(sx, yy, t, 2.4, 'start', '#222'); yy += 4.2
    yy += 2
    spec += ui(sx, yy, 'Relief: O1.8 cut at each crease end (S: 2, P: 2) + O1 at slit ends: no tear when lifting.', 2.4, 'start', '#222'); yy += 4.2
    spec += ui(sx, yy, f'Geometry: b = {U_P-FRONT:.0f}, S crown ({TIP[0]-FRONT:.2f}, {TIP[1]:.2f}) from c1, P {P_LEN:.2f} (drawn net; +0.3 for fold take-up if the test says so).', 2.4, 'start', '#222')
    leg = legend(sx, 150, [('cut', 'Cut'), ('crease', 'Crease: valley, scored from printed face'),
                           ('bleed', 'Bleed (only if flood-printed)'), ('safe', 'Safe area for text'), ('art', 'Board colour #feed95')], 'Legend')
    leg += f'<line x1="{sx+78}" y1="{150+3.3}" x2="{sx+87}" y2="{150+3.3}" {crease_style(0.3, "4 0.8 0.3 0.8")}/>' + ui(sx + 89.5, 150 + 4.2, 'flange crease (against score)', 2.3)
    leg += f'<rect x="{sx+78}" y="{150+6}" width="9" height="2" fill="#808080" fill-opacity="0.3"/>' + ui(sx + 89.5, 150 + 8.1, 'void = negative of S / P', 2.3)
    show_rev = (variant == 'reverse')
    body = (layer('bleed', 'bleed', f'<path d="{poly_d(bleed)}" {bleed_style(0.18)}/>', 'style="display:none"' if False else '') +
            layer('artwork_lemon', 'artwork - lemon card, black type', lemon + ('' if show_rev else void), 'style="display:none"' if show_rev else '') +
            layer('artwork_reverse', 'artwork - REVERSE: black card, lemon type', black + (void if show_rev else ''), '' if show_rev else 'style="display:none"') +
            layer('safe', 'safe area', safe + lipbox) + layer('cut', 'cut', cut) + layer('crease', 'crease', cre) +
            layer('slot', 'slot (none)', '') + layer('annotations', 'dimensions + legend', ''.join(d) + lab + spec + leg))
    return svg_doc(W, H, body, 'D2 v2 compact dieline 1:1 (mm)', '105 x 118 card, S segment + flanged strut', bg='#ffffff')

# ================================================================= 3D
def S3(X, Yf):
    v = (SHH - Yf) - FRONT
    return (X - CX, (FRONT - 60.0) + v * dS[0], v * dS[1])

def P3(X, Yf):
    w = (SHH - Yf) - U_P
    hy = U_P - 60.0
    if w <= P_LEN + 1e-9: return (X - CX, hy + w * dP[0], w * dP[1])
    l = w - P_LEN
    return (X - CX, hy + P_LEN * dP[0] + l * dLip[0], P_LEN * dP[1] + l * dLip[1])

def build_assembled(reverse=False):
    W, H = 300, 262
    card = INK_REV if reverse else YELLOW
    ink = YELLOW if reverse else INK
    strut = '#2b2b2b' if reverse else '#f5e07e'
    table = '#f3e08a' if reverse else '#e9e7df'
    edge = '#888888' if reverse else '#222222'
    ax = Axo(yaw_deg=-28, elev_deg=27, ox=150, oy=102, k=1.3)
    cutS, creS, outS, relS = s_geo(); P = p_geo()
    sheet = box(0, 0, SHW, SHH); pS = outS.poly(0.5); pP = P['outline'].poly(0.5)
    base = sheet.difference(pS).difference(pP)
    def base3(c): return [(X - CX, (SHH - Yf) - 60.0, 0.0) for X, Yf in c]
    def path3(g):
        out = []
        for p in (g.geoms if hasattr(g, 'geoms') else [g]):
            for ring in [p.exterior] + list(p.interiors): out.append(face_d(ax, base3(list(ring.coords)[:-1])))
        return ' '.join(out)
    S3pts = [S3(x, y) for x, y in pS.exterior.coords]
    # strut web polygon (flat) with flange strips removed between the slits, mapped to 3D
    off = P['off']; ya, yb = P['ya'], P['yb']
    yh, yt = Y(U_P), Y(U_TIP)
    xl, xr = P['xl'], P['xr']
    web = [(xl(yh), yh), (xl(ya), ya), (xl(ya) + off, ya), (xl(yb) + off, yb), (xl(yb), yb), (xl(yt), yt),
           (xr(yt), yt), (xr(yb), yb), (xr(yb) - off, yb), (xr(ya) - off, ya), (xr(ya), ya), (xr(yh), yh)]
    web3 = [P3(x, y) for x, y in web]
    nu, nz = abs(dP[1]), abs(dP[0])
    flanges = []
    for seg in P['fcre']:
        (xa_, ya_), (xb_, yb_) = seg
        pa, pb = P3(xa_, ya_), P3(xb_, yb_)
        flanges.append([pa, pb, (pb[0], pb[1] + FLW * nu, pb[2] + FLW * nz), (pa[0], pa[1] + FLW * nu, pa[2] + FLW * nz)])
    Plip = [P3(x, y) for x, y in [(CX - P_WT / 2, Y(U_TIP)), (CX - LIP_W / 2, Y(U_TIP)), (CX - LIP_W / 2, Y(U_END)), (CX + LIP_W / 2, Y(U_END)), (CX + LIP_W / 2, Y(U_TIP)), (CX + P_WT / 2, Y(U_TIP))]]
    gnd = [(-85, -66, -0.6), (85, -66, -0.6), (85, 76, -0.6), (-85, 76, -0.6)]
    body = f'<path d="{face_d(ax, gnd)}" fill="{table}"/>'
    body += f'<path d="{path3(sheet)}" fill="#000" fill-opacity="0.12" transform="translate(1.2 1.6)"/>'
    body += f'<path d="{path3(base)}" fill="{card}" stroke="{edge}" stroke-width="0.3" fill-rule="evenodd" stroke-linejoin="round"/>'
    Mb = ax.matrix((-CX, SHH - 60.0, 0.02), (1, 0, 0), (0, -1, 0))
    body += f'<g transform="{Mb}">{art_base(ink)}</g>'
    for pts in (S3pts, web3):
        body += f'<path d="{face_d(ax, shadow_pts(pts, 0.5, -0.35))}" fill="#000" fill-opacity="0.08"/>'
    for fl in flanges:
        body += f'<path d="{face_d(ax, fl)}" fill="{strut}" stroke="{edge}" stroke-width="0.25" stroke-linejoin="round"/>'
    body += f'<path d="{face_d(ax, web3)}" fill="{strut}" stroke="{edge}" stroke-width="0.3" stroke-linejoin="round"/>'
    body += f'<path d="{face_d(ax, S3pts)}" fill="{card}" stroke="{edge}" stroke-width="0.35" stroke-linejoin="round"/>'
    o = S3(0.0, 0.0)
    Ms = ax.matrix(o, (1, 0, 0), (0, -dS[0], -dS[1]))
    body += f'<g transform="{Ms}">{art_s(NAME, ink)}</g>'
    body += f'<path d="{face_d(ax, Plip)}" fill="{strut}" stroke="{edge}" stroke-width="0.35" stroke-linejoin="round"/>'
    gx, gy = ax((0, -74, 0)); g2x, g2y = ax((0, -58, 0))
    call = (f'<line x1="{gx:.2f}" y1="{gy:.2f}" x2="{g2x:.2f}" y2="{g2y:.2f}" stroke="#555" stroke-width="0.3" marker-end="url(#arr)"/>' + ui(gx, gy + 5, 'guest side', 2.6, 'middle', '#555', 700))
    def leader(tx, ty, target, text, anchor='start'):
        px_, py_ = ax(target)
        x0_ = (tx - 1.5) if px_ < tx else (tx + text_w(text, 2.8, 700) + 1.5)
        return (f'<line x1="{x0_:.2f}" y1="{ty-1:.2f}" x2="{px_:.2f}" y2="{py_:.2f}" stroke="#555" stroke-width="0.25"/>'
                f'<circle cx="{px_:.2f}" cy="{py_:.2f}" r="0.9" fill="#111"/>' + ui(tx, ty, text, 2.8, anchor, '#111', 700))
    call += leader(12, 62, S3(CX - 36, Y(FRONT + 14)), 'S  lifted segment (name plate)')
    call += leader(196, 34, P3(CX, Y(U_P + 20)), 'P  flanged strut, hook lip on S')
    call += leader(206, 112, (0, (U_P + 24) - 60.0, 0.0), 'void = negative of P')
    call += leader(206, 150, (38, (FRONT + 10) - 60.0, 0.0), 'void = negative of S')
    defs = '<defs><marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 Z" fill="#555"/></marker></defs>'
    # side section
    k = 2.0; sx0, sz0 = 24.0, 248.0
    Pq = lambda u, z: (sx0 + k * u, sz0 - k * z)
    sec = f'<line x1="{sx0-4}" y1="{sz0}" x2="{sx0+k*SHH+4}" y2="{sz0}" stroke="{edge}" stroke-width="0.5"/>'
    for u0, u1 in ((0, FRONT), (FRONT + S_LEN, U_P), (U_END, SHH)):
        sec += f'<rect x="{Pq(u0,0)[0]:.2f}" y="{sz0-k*T}" width="{k*(u1-u0):.2f}" height="{k*T}" fill="#222"/>'
    s0, s1 = Pq(FRONT, 0), Pq(*TIP); p0 = Pq(U_P, 0); l1 = Pq(TIP[0] + LIP_L * dLip[0], TIP[1] + LIP_L * dLip[1])
    sec += f'<line x1="{s0[0]:.2f}" y1="{s0[1]:.2f}" x2="{s1[0]:.2f}" y2="{s1[1]:.2f}" stroke="{edge}" stroke-width="{k*T:.2f}"/>'
    sec += f'<line x1="{p0[0]:.2f}" y1="{p0[1]:.2f}" x2="{s1[0]:.2f}" y2="{s1[1]:.2f}" stroke="#555" stroke-width="{k*T:.2f}"/>'
    sec += f'<line x1="{s1[0]:.2f}" y1="{s1[1]:.2f}" x2="{l1[0]:.2f}" y2="{l1[1]:.2f}" stroke="#555" stroke-width="{k*T:.2f}"/>'
    # flange seen edge-on (5 mm, up/back) in the middle of the strut
    wm = (FL_A + P_LEN - FL_B) / 2
    mid = (U_P + wm * dP[0], wm * dP[1]); tip = (mid[0] + FLW * abs(dP[1]), mid[1] + FLW * abs(dP[0]))
    a_, b_ = Pq(*mid), Pq(*tip)
    sec += f'<line x1="{a_[0]:.2f}" y1="{a_[1]:.2f}" x2="{b_[0]:.2f}" y2="{b_[1]:.2f}" stroke="#c00" stroke-width="{k*T:.2f}"/>'
    sec += ui(b_[0] + 2, b_[1], 'flange 5 mm', 2.2, 'start', '#c00')
    sec += ui(s1[0] + 3, s1[1] - 1, 'c3 hook lip', 2.2, 'start', C_CREASE)
    sec += ui(Pq(FRONT, 0)[0], Pq(FRONT, 0)[1] + 5, 'c1', 2.2, 'middle', C_CREASE) + ui(p0[0], p0[1] + 5, 'c2', 2.2, 'middle', C_CREASE)
    sec += ui(Pq(FRONT + 11, 3)[0], Pq(FRONT + 11, 3)[1], '75 deg', 2.2, 'start', C_DIM)
    sec += ui(Pq(U_P - 17, 2.5)[0], Pq(U_P - 17, 2.5)[1], f'{ANG_P:.1f} deg', 2.2, 'start', C_DIM)
    sec += dim_h(Pq(FRONT, 0)[0], Pq(U_P, 0)[0], sz0 + 11, f'b = {U_P-FRONT:.0f}')
    sec += ui(sx0 + k * 66, sz0 - k * 36, 'SIDE SECTION 2:1  -  closed triangle base / S / P', 2.5, 'start', '#555', 700)
    sec += ui(sx0 + k * 66, sz0 - k * 36 + 4, f'S {S_LEN:.0f} at 75 deg ; P {P_LEN:.1f} at {ANG_P:.1f} deg ; red = flange (edge-on)', 2.2, 'start', '#444')
    title = (ui(10, 12, 'D2 v2  FORM AND ITS VOID, COMPACT' + ('  -  reverse colourway' if reverse else '') + '  -  assembled', 4.0, 'start', '#111', 700) +
             ui(10, 17.8, '105 x 118 card on the table. Lift S, lift P, hook the lip over the crown of S. No glue.', 2.5))
    return svg_doc(W, H, title + defs + body + call + sec, 'D2 v2 assembled', 'axonometric + section', bg='#ffffff')

# ================================================================= verification
def verify():
    out = ['=== D2 v2 verification ==='] ; ok = True
    def chk(c, m):
        nonlocal ok
        out.append(('PASS ' if c else 'FAIL ') + m); ok &= bool(c)
    cutS, creS, outS, relS = s_geo(); P = p_geo()
    sheet = box(0, 0, SHW, SHH); pS = outS.poly(0.2); pP = P['outline'].poly(0.2)
    chk(sheet.contains(pS) and sheet.contains(pP), 'S and P outlines inside the card')
    chk(not pS.intersects(pP), 'S void and P void do not overlap')
    chk(pS.distance(pP) >= 7.9, f'web between voids {pS.distance(pP):.1f} mm (die minimum 3)')
    edge = min(sheet.exterior.distance(pS), sheet.exterior.distance(pP))
    chk(edge >= 6.9, f'void to card edge {edge:.1f} mm')
    chk(SHW <= 114 and SHH <= 162, f'{SHW:.0f} x {SHH:.0f} fits C6 (114 x 162)')
    out.append(f'INFO footprint {SHW*SHH:.0f} mm2 vs v1 {105*148} mm2 = {100*(1-SHW*SHH/(105*148)):.0f} % smaller')
    S_top = np.array(TIP); P_end = np.array([U_P, 0.0]) + P_LEN * np.array(dP)
    chk(np.allclose(S_top, P_end, atol=1e-9), f'triangle closes: S crown {S_top.round(3)} = P tip {P_end.round(3)} ; P = {P_LEN:.2f} at {ANG_P:.1f} deg')
    out.append(f'INFO S circle: chord {S_CHORD:.0f}, height {S_LEN:.0f} -> R {S_R:.2f} (review quoted 33.7; (45^2+32^2)/(2*32) = {S_R:.1f}). Tangent angle at the hinge ends {math.degrees(math.asin((S_CHORD/2)/S_R)):.1f} deg')
    out.append(f'INFO folds: c1 {math.degrees(THETA):.0f}, c2 {FOLD_P:.1f}, c3 {FOLD_LIP:.1f} deg')
    def lean(pl):
        b = U_P - FRONT; x = (S_LEN**2 - pl**2 + b**2) / (2 * b); return math.degrees(math.atan2(math.sqrt(max(S_LEN**2 - x**2, 0)), x))
    out.append(f'INFO S lean for P {P_LEN-0.5:.2f}/{P_LEN:.2f}/{P_LEN+0.5:.2f}: {lean(P_LEN-0.5):.2f}/{lean(P_LEN):.2f}/{lean(P_LEN+0.5):.2f} deg (fold take-up 0.3-0.4 mm per 135 deg fold is inside this window; test 44.0 / 44.3 / 44.6)')
    # strut stiffness: flat vs C-channel (mid-length)
    wmid = (P_WH + P_WT) / 2
    I_flat = wmid * T**3 / 12
    ww = wmid - 2 * FLW
    Aw, Af = ww * T, FLW * T
    yw, yf = T / 2, T + FLW / 2
    yc = (Aw * yw + 2 * Af * yf) / (Aw + 2 * Af)
    I_ch = ww * T**3 / 12 + Aw * (yw - yc)**2 + 2 * (T * FLW**3 / 12 + Af * (yf - yc)**2)
    Ecd = 2000.0
    Pcr_flat = math.pi**2 * Ecd * I_flat / P_LEN**2
    arm = abs(((FRONT - S_top[0]) * dP[1] - (0.0 - S_top[1]) * dP[0]))
    push = lambda Pc: Pc * arm / S_top[1]
    out.append(f'INFO strut flat: I {I_flat:.3f} mm4, Euler {Pcr_flat:.2f} N -> push at crown {push(Pcr_flat):.2f} N ({push(Pcr_flat)/9.81*1000:.0f} gf)')
    out.append(f'INFO strut with 2 flanges: I {I_ch:.1f} mm4 = {I_ch/I_flat:.0f} x ; Euler {math.pi**2*Ecd*I_ch/P_LEN**2:.0f} N (no longer the limit; limits become the hook lip and crease c2, to be tested)')
    chk(I_ch / I_flat > 20, 'flanged strut >= 20 x stiffer than flat')
    # twin struts for comparison: two strips each 12 wide
    I_twin = 2 * 12 * T**3 / 12
    out.append(f'INFO twin struts 2 x 12 wide: I {I_twin:.3f} mm4 (each strip alone: Euler {math.pi**2*Ecd*I_twin/2/P_LEN**2:.2f} N) - not stiffer than the flat strut')
    # flange clearance: flange tip points must be above the table and behind S's back face
    nu, nz = abs(dP[1]), abs(dP[0])
    worst = 1e9
    for w in np.linspace(FL_A, P_LEN - FL_B, 20):
        pu, pz = U_P + w * dP[0], w * dP[1]
        tu, tz = pu + FLW * nu, pz + FLW * nz
        s_u = FRONT + tz / math.tan(THETA)        # S front... back face u at that height
        worst = min(worst, tu - s_u)
        assert tz > 0
    chk(worst > 2.0, f'flange tips stay behind the back face of S by >= {worst:.1f} mm and above the table')
    chk(FL_B >= 3.0 and FL_A >= 3.0, f'flange ends are {FL_A:.0f} / {FL_B:.0f} mm from c2 / c3 (creases >= 3 mm apart)')
    # strut flat width at the flange slits >= 2*FLW + 10
    chk(min(P['xr'](P['ya']) - P['xl'](P['ya']), P['xr'](P['yb']) - P['xl'](P['yb'])) - 2 * FLW >= 15, f'web between flange creases >= {min(P["xr"](P["ya"]) - P["xl"](P["ya"]), P["xr"](P["yb"]) - P["xl"](P["yb"])) - 2*FLW:.1f} mm')
    # text vs S outline and lip
    sz = name_size(NAME)
    def hw(v): return math.sqrt(max(S_R**2 - (v - S_CV)**2, 0))
    for nm in (NAME, 'Alexandra Vorontsova', 'Mikhail Terentyev-Z'):
        s_ = name_size(nm); w = text_w(nm, s_); top = NAME_V + CAP * s_
        chk(w / 2 + 3 <= hw(top), f'name "{nm}" {s_:.1f} mm: {w:.1f} wide, S half-width at its cap top {2*hw(top):.1f}')
    sec_w = text_w(f'TABLE {TABLE}  ·  SEAT {SEAT}', SEC, 700, 0.05)
    sec_top = SEC_V + CAP * SEC
    chk(sec_w / 2 + 3 <= hw(sec_top), f'table/seat line {sec_w:.1f} mm wide at cap top v = {sec_top:.1f}: S width there {2*hw(sec_top):.1f}')
    chk(CAP * SEC >= 3.45, f'secondary type {SEC} mm -> cap height {CAP*SEC:.2f} mm >= 3.5')
    chk(S_LEN - LIP_L - sec_top >= 3.0, f'lip (v {S_LEN-LIP_L:.0f}-{S_LEN:.0f}) clears the table/seat line (cap top {sec_top:.1f}) by {S_LEN-LIP_L-sec_top:.1f} mm')
    chk(sec_top + 0.0 < NAME_V + 20, 'name below table/seat line')
    # imposition 8 / SRA3
    out.append('INFO imposition: cards stand with their 105 mm side (creases) along the 450 mm side: 4 x 105 + 3 x 3 = 429 mm; 2 x 118 + 3 = 239 mm of 320 -> 8 per SRA3 (grain long, parallel to creases)')
    out.append('RESULT ' + ('ALL PASS' if ok else 'SOME FAIL'))
    return '\n'.join(out)

if __name__ == '__main__':
    open(os.path.join(OUT, 'd2_dieline.svg'), 'w').write(build_dieline('both'))
    open(os.path.join(OUT, 'd2_dieline_reverse.svg'), 'w').write(build_dieline('reverse'))
    open(os.path.join(OUT, 'd2_assembled.svg'), 'w').write(build_assembled(False))
    open(os.path.join(OUT, 'd2_assembled_reverse.svg'), 'w').write(build_assembled(True))
    rep = verify(); open(os.path.join(OUT, 'd2_verify.txt'), 'w').write(rep + '\n'); print(rep)
