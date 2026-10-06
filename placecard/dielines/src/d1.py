"""D1 v2 - Two plates on slots: raised name, short B, 0.6 gap, slot test strip, relieved slot ends. + 'sail' variant."""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from shapely.geometry import Point

T = BOARD_T
SW = SLOT_W                      # 0.70 net design width
CH = 0.6                         # lead-in chamfer (45 deg)
RELIEF_R = 0.7                   # slot-end relief circle (dia 1.4)
WA, HS, HC = 100.0, 34.0, 45.0
D_A = 11.0                       # slot depth in A
GAP_V = 0.60                     # vertical gap between the two slot ends
FLOOR_B = D_A - GAP_V            # 10.4
WB, BC = 64.0, 22.0              # plate B: width, height at the centre
sag = HC - HS
R = ((WA / 2) ** 2 + sag ** 2) / (2 * sag)
def z_dip(x): return BC + R - math.sqrt(R * R - x * x)
def z_dome(x): return HC - R + math.sqrt(R * R - x * x)
HB_END = z_dip(WB / 2)
NAME_Z = 27.0                    # name baseline on A (B never rises above 26.4)
EYE_Z = 35.3                     # table/seat line baseline on A
NAME = 'Sophia Zhuravkova'
SAMPLE_NAMES = ['Sophia Zhuravkova', 'Ivan Petrov', 'Alexandra Vorontsova', 'Mila Orlova', 'Tim Gerasimov',
                'Nadezhda Kuznetsova', 'Oleg Sidorov', 'Anna Li', 'Maximilian Kovalev', 'Daria Belova',
                'Pavel Arkhipov', 'Elena Smirnova', 'Kirill Volkov', 'Yulia Zakharova', 'Roman Fedorov']
def name_size(n, avail=80.0): return fit_size(n, avail, 7.2)

# ------------------------------------------------------------ slot with chamfer mouth + relief circle
def slot_path(ym, ye):
    """slot centred on x=0, mouth at local y=ym, end (tip of the relief circle) at y=ye. returns open Path"""
    d = 1 if ye > ym else -1
    L = abs(ye - ym); w = SW / 2; m = w + CH
    cs = L - RELIEF_R
    sw_ = cs - math.sqrt(RELIEF_R ** 2 - w ** 2)
    Y_ = lambda s: ym + d * s
    p = Path((m, Y_(0))).L((w, Y_(CH))).L((w, Y_(sw_))).A3((0, Y_(L)), (-w, Y_(sw_))).L((-w, Y_(CH))).L((-m, Y_(0)))
    return p

def A_local(depth=D_A):
    m = SW / 2 + CH
    cut = Path((m, 0)).L((WA / 2, 0)).L((WA / 2, -HS)).A3((0, -HC), (-WA / 2, -HS)).L((-WA / 2, 0)).L((-m, 0))
    slot = slot_path(0, -depth)
    outline = Path((-WA / 2, 0)).L((WA / 2, 0)).L((WA / 2, -HS)).A3((0, -HC), (-WA / 2, -HS)).Z()
    return dict(cut=cut, slot=slot, outline=outline)

def B_local():
    m = SW / 2 + CH
    zm = z_dip(m); zq = z_dip(WB / 4)
    cut = (Path((-m, -zm)).A3((-WB / 4, -zq), (-WB / 2, -HB_END)).L((-WB / 2, 0)).L((WB / 2, 0)).L((WB / 2, -HB_END)).A3((WB / 4, -zq), (m, -zm)))
    slot = slot_path(-zm, -FLOOR_B)
    outline = Path((-WB / 2, 0)).L((WB / 2, 0)).L((WB / 2, -HB_END)).A3((0, -BC), (-WB / 2, -HB_END)).Z()
    return dict(cut=cut, slot=slot, outline=outline)

def place(ox, oy, rot180=False):
    if rot180: return lambda p: (ox - p[0], oy - p[1])
    return lambda p: (ox + p[0], oy + p[1])

def a_texts(ox, oy, name, rot=0, ink=INK, seat='07'):
    s = name_size(name)
    def tx(x, z, *a, **k):
        X, Y_ = (ox + x, oy - z) if not rot else (ox - x, oy + z)
        return txt(X, Y_, *a, rot=rot, fill=ink, **k)
    return tx(0, NAME_Z, name, s) + tx(0, EYE_Z, f'TABLE 4  ·  SEAT {seat}', SEC, weight=700, tracking=0.05)

def b_texts(ox, oy, rot=0, ink=INK):
    def tx(x, z, *a, **k):
        X, Y_ = (ox + x, oy - z) if not rot else (ox - x, oy + z)
        return txt(X, Y_, *a, rot=rot, fill=ink, **k)
    return tx(-17, 8.0, 'DINNER', SEC, weight=700, tracking=0.05) + tx(17, 8.0, '10 OCT', SEC, weight=700, tracking=0.05)

def bleed_poly(outline_path, fn):
    return outline_path.xform(fn).poly(0.4).buffer(BLEED, join_style=1, resolution=24)

def slot_draw(slot_path_, fn):
    sp = slot_path_.xform(fn)
    pts = sp.pts(0.15)
    fill = f'<path d="{poly_d(pts)}" fill="{C_SLOT}" fill-opacity="0.35" stroke="none"/>'
    line = f'<path d="{sp.d()}" fill="none" stroke="{C_SLOT}" stroke-width="0.2" stroke-linejoin="miter"/>'
    return fill + line

def piece_layers(geo, fn, bleed, art, ink_fill=YELLOW):
    return dict(bleed=f'<path d="{poly_d(bleed)}" {bleed_style(0.18)}/>',
                art=f'<path d="{poly_d(bleed)}" fill="{ink_fill}"/>' + art,
                cut=f'<path d="{geo["cut"].xform(fn).d()}" {cut_style()}/>',
                slot=slot_draw(geo['slot'], fn))

# ================================================================= dieline (one set)
def build_dieline():
    W, H = 278, 222
    A_ox, A_by = 84.0, 74.0
    B_ox, B_by = 210.0, 74.0
    A = A_local(); B = B_local()
    fa, fb = place(A_ox, A_by), place(B_ox, B_by)
    la = piece_layers(A, fa, bleed_poly(A['outline'], fa), a_texts(A_ox, A_by, NAME))
    lb = piece_layers(B, fb, bleed_poly(B['outline'], fb), b_texts(B_ox, B_by))
    sz = name_size(NAME)
    safe = (f'<rect x="{A_ox-40}" y="{A_by-NAME_Z-CAP*sz-0.5}" width="80" height="{CAP*sz+0.25*sz+1:.1f}" {safe_style()}/>'
            f'<rect x="{A_ox-26}" y="{A_by-EYE_Z-3.5-0.5}" width="52" height="4.6" {safe_style()}/>'
            f'<rect x="{B_ox-30}" y="{B_by-13.5}" width="26" height="10.5" {safe_style()}/>'
            f'<rect x="{B_ox+4}" y="{B_by-13.5}" width="26" height="10.5" {safe_style()}/>')
    # B top line: where it is relative to the name
    ref = (f'<line x1="{A_ox-WA/2}" y1="{A_by-HB_END}" x2="{A_ox+WA/2}" y2="{A_by-HB_END}" stroke="#c00" stroke-width="0.15" stroke-dasharray="1 1"/>'
           + ui(A_ox + WA / 2 + 2, A_by - HB_END + 0.8, f'B max z {HB_END:.1f}', 2.0, 'start', '#c00'))
    d = [dim_h(A_ox - WA / 2, A_ox + WA / 2, A_by + 8, f'{WA:.0f}'),
         dim_v(A_ox - WA / 2 - 7, A_by - HS, A_by, f'{HS:.0f}', side=-1), dim_v(A_ox - WA / 2 - 16, A_by - HC, A_by, f'{HC:.0f}', side=-1),
         dim_v(A_ox - 8, A_by - D_A, A_by, f'slot {D_A:.1f}', side=-1),
         dim_h(B_ox - WB / 2, B_ox + WB / 2, B_by + 8, f'{WB:.0f}'),
         dim_v(B_ox + WB / 2 + 7, B_by - HB_END, B_by, f'{HB_END:.1f}'), dim_v(B_ox - WB / 2 - 7, B_by - BC, B_by, f'{BC:.0f}', side=-1),
         ui(A_ox, A_by + 16.5, f'dome R{R:.1f}  (B dip: same R{R:.1f})', 2.3, 'middle', C_DIM),
         ui(B_ox, B_by + 16.5, f'slot floor z = {FLOOR_B:.1f}  (depth {BC-FLOOR_B:.1f})', 2.3, 'middle', C_DIM)]
    labels = (ui(A_ox, 12, 'A  -  NAME PLATE', 3.4, 'middle', '#111', 700) + ui(A_ox, 16.6, 'slot opens from the BOTTOM edge', 2.3, 'middle') +
              ui(B_ox, 12, 'B  -  FIN', 3.4, 'middle', '#111', 700) + ui(B_ox, 16.6, 'slot opens from the TOP edge', 2.3, 'middle'))
    # slot detail x14
    k = 14.0; ix, iy = 30.0, 188.0
    sp = slot_path(0, -4.2).xform(lambda p: (ix + k * p[0], iy + k * p[1]))
    inset = (f'<line x1="{ix-24}" y1="{iy}" x2="{ix-(SW/2+CH)*k}" y2="{iy}" {cut_style(0.35)}/>'
             f'<line x1="{ix+(SW/2+CH)*k}" y1="{iy}" x2="{ix+24}" y2="{iy}" {cut_style(0.35)}/>'
             f'<path d="{poly_d(sp.pts(0.3))}" {slot_style(0.3)}/>' + dim_h(ix - SW / 2 * k, ix + SW / 2 * k, iy - 4.2 * k - 4, f'{SW:.2f}') +
             ui(ix, iy - 4.2 * k - 10.5, f'SLOT DETAIL  x{k:.0f}', 2.4, 'middle', '#555', 700) +
             ui(ix, iy + 5, f'chamfer {CH} x 45 deg ; end relief O{2*RELIEF_R:.1f}', 2.2, 'middle'))
    sx, sy = 84.0, 112.0
    sz = name_size(NAME)
    lines = [('SPEC', 700),
             (f'Board: PRE-COLOURED lemon #feed95, 400 g/m2, caliper {T:.2f} mm (or 350 g / 0.44 mm for a digital press: slot 0.60). No flood print, no bleed.', 500),
             (f'Digital presses mostly stop at 300-350 g: check; 400 g duplex = litho / screen / flat-bed digital.', 500),
             (f'Slot {SW:.2f} net = board + 0.20. A slot depth {D_A:.1f}; B floor {FLOOR_B:.1f} -> {GAP_V:.1f} mm bottoming gap (> die / laser tolerance 0.2). Play angle 1.0 deg.', 500),
             ('STEEL RULE: a single rule only slits (fibre springback leaves ~0.35-0.55): ask the die-maker for', 500),
             ('   (a) 3 pt (1.07) blunt slot rule or (b) two 2 pt rules at 0.70 clear gap with stripping pin; first article decides.', 500),
             ('LASER: draw 0.50 (kerf 0.20 -> 0.70 net); edge scorch is visible on lemon -> use a 2nd pass at low power or tumble.', 500),
             ('KNIFE PLOTTER: not suitable for a 0.7 slot (sliver stays in); use laser or die.', 500),
             ('Slot test strip: 0.60 / 0.70 / 0.80 / 0.90 on every sheet (see imposition) - pick the fit with the real board.', 500),
             (f'Name: Wix Madefor Text Medium {sz:.1f} mm, baseline z {NAME_Z:.0f} (cap top {NAME_Z+CAP*sz:.1f}), ABOVE B (max {HB_END:.1f}). Table/seat one line {SEC} mm = 3.5 mm caps, on A.', 500),
             (f'Footprint {WA:.0f} x {WB:.0f} mm (rhombus), height {HC:.0f}. Flat A {WA:.0f}x{HC:.0f}, B {WB:.0f}x{HB_END:.1f} fit C6 / DL.', 500)]
    spec = ''; yy = sy
    for i, (t, w_) in enumerate(lines):
        spec += ui(sx, yy, t, 2.8 if i == 0 else 2.4, 'start', '#555' if i == 0 else '#222', w_); yy += 4.3
    leg = legend(sx, 168, [('cut', 'Cut (solid)'), ('slot', 'Slot, cut (0.70 net)'), ('bleed', 'Bleed 3 mm (only if flood-printed)'),
                           ('safe', 'Safe area for text'), ('art', 'Board colour #feed95')], 'Legend')
    leg += ui(sx, 168 + 4.2 + 3.9 * 5 + 1.0, 'No creases: both plates are flat.', 2.3)
    body = (layer('bleed', 'bleed', la['bleed'] + lb['bleed']) + layer('artwork', 'artwork (lemon + black type)', la['art'] + lb['art']) +
            layer('safe', 'safe area', safe) + layer('cut', 'cut', la['cut'] + lb['cut']) + layer('slot', 'slot', la['slot'] + lb['slot']) +
            layer('crease', 'crease (none)', '') + layer('annotations', 'dimensions + legend', ''.join(d) + labels + ref + inset + spec + leg))
    return svg_doc(W, H, body, 'D1 v2 dieline 1:1 (mm)', 'cross-slot plates', bg='#ffffff')

# ================================================================= imposition
SHEET_W, SHEET_H = 320.0, 450.0
COL_X0, COL_PITCH, GRIP = 6.0, 104.0, 12.0
PAIR_H = HC + 4.5 + BC
ROW_PITCH = PAIR_H + 4.0
NCOL, NROW = 3, 5
TEST_W = [0.60, 0.70, 0.80, 0.90]

def pair_geometry(c, r):
    ox = COL_X0 + c * COL_PITCH + WA / 2
    top = GRIP + r * ROW_PITCH
    return dict(A=(ox, top + PAIR_H), B=(ox, top))

def coupon(x, y, w, label):
    """test coupon 56 x 26, slot of width w, depth 11, chamfer, relief; origin top-left"""
    cw, chh = 56.0, 26.0
    m = w / 2 + CH
    cut = Path((x + cw / 2 + m, y + chh)).L((x + cw, y + chh)).L((x + cw, y)).L((x, y)).L((x, y + chh)).L((x + cw / 2 - m, y + chh))
    # slot with variable width
    wh = w / 2; L = 11.0; cs = L - RELIEF_R; swl = cs - math.sqrt(max(RELIEF_R ** 2 - wh ** 2, 0.0))
    X_, Y_ = x + cw / 2, y + chh
    s = Path((X_ + m, Y_)).L((X_ + wh, Y_ - CH)).L((X_ + wh, Y_ - swl)).A3((X_, Y_ - L), (X_ - wh, Y_ - swl)).L((X_ - wh, Y_ - CH)).L((X_ - m, Y_))
    art = f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" fill="{YELLOW}"/>' + txt(x + cw / 2, y + 7.5, label, 5.5, weight=700) + txt(x + cw / 2, y + 12.5, 'mm', 2.6, weight=500)
    slot = f'<path d="{poly_d(s.pts(0.15))}" fill="{C_SLOT}" fill-opacity="0.35" stroke="none"/><path d="{s.d()}" fill="none" stroke="{C_SLOT}" stroke-width="0.2"/>'
    return art, f'<path d="{cut.d()}" {cut_style()}/>', slot, Polygon([(x, y), (x + cw, y), (x + cw, y + chh), (x, y + chh)])

def build_sheet():
    A = A_local(); B = B_local()
    bl, art, cut, slot = [], [], [], []; polys = []
    for r in range(NROW):
        for c in range(NCOL):
            g = pair_geometry(c, r); idx = r * NCOL + c
            name = SAMPLE_NAMES[idx % len(SAMPLE_NAMES)]
            (ax, ay), (bx, by) = g['A'], g['B']
            fa, fb = place(ax, ay), place(bx, by, True)
            la = piece_layers(A, fa, bleed_poly(A['outline'], fa), a_texts(ax, ay, name, seat='%02d' % (idx % 12 + 1)))
            lb = piece_layers(B, fb, bleed_poly(B['outline'], fb), b_texts(bx, by, rot=180))
            bl += [la['bleed'], lb['bleed']]; art += [la['art'], lb['art']]; cut += [la['cut'], lb['cut']]; slot += [la['slot'], lb['slot']]
            polys.append(('A%02d' % idx, A['outline'].xform(fa).poly(0.4))); polys.append(('B%02d' % idx, B['outline'].xform(fb).poly(0.4)))
    y_t = GRIP + NROW * ROW_PITCH - 4 + 7
    for i, w in enumerate(TEST_W):
        a_, c_, s_, p_ = coupon(COL_X0 + i * 60, y_t, w, '%.2f' % w)
        art.append(a_); cut.append(c_); slot.append(s_); polys.append(('T%d' % i, p_))
    furn = (f'<rect x="0" y="0" width="{SHEET_W}" height="{SHEET_H}" fill="none" stroke="#999" stroke-width="0.3"/>'
            f'<rect x="0" y="0" width="{SHEET_W}" height="{GRIP}" fill="#000" fill-opacity="0.06"/>' + ui(SHEET_W / 2, 7.5, 'GRIPPER EDGE 12 mm', 2.4, 'middle', '#666'))
    for (cx, cy) in [(3, GRIP + 3), (SHEET_W - 3, GRIP + 3), (3, SHEET_H - 6), (SHEET_W - 3, SHEET_H - 6)]:
        furn += (f'<circle cx="{cx}" cy="{cy}" r="1.6" fill="none" stroke="#000" stroke-width="0.2"/><line x1="{cx-3}" y1="{cy}" x2="{cx+3}" y2="{cy}" stroke="#000" stroke-width="0.15"/><line x1="{cx}" y1="{cy-3}" x2="{cx}" y2="{cy+3}" stroke="#000" stroke-width="0.15"/>')
    ny = y_t + 26 + 6
    note = (ui(6, ny, f'SRA3 320 x 450  -  {NCOL*NROW} sets (A + B) = {NCOL*NROW} guests per sheet + slot test strip (coupons 0.60 / 0.70 / 0.80 / 0.90).', 3.0, 'start', '#111', 700) +
            ui(6, ny + 5, f'B turned 180 deg and nested over the dome of A (same R{R:.0f}, 4.5 mm gap). Pitch {COL_PITCH:.0f} x {ROW_PITCH:.1f}, web 4 mm, long grain (450) = vertical on both plates.', 2.4) +
            ui(6, ny + 9.5, 'Pre-coloured lemon board: no bleed. Slip a scrap of the production board into each coupon slit and choose the width that holds without force.', 2.4))
    body = (layer('bleed', 'bleed', '\n'.join(bl)) + layer('artwork', 'artwork', '\n'.join(art)) + layer('cut', 'cut', '\n'.join(cut)) +
            layer('slot', 'slot', '\n'.join(slot)) + layer('sheet', 'sheet', furn + note))
    return svg_doc(SHEET_W, SHEET_H, body, 'D1 v2 SRA3 imposition 1:1', '15 sets + slot test strip', bg='#ffffff'), polys

# ================================================================= assembled
def build_assembled():
    W, H = 290, 232
    ax = Axo(yaw_deg=-24, elev_deg=26, ox=150, oy=122, k=1.25)
    def a_half(s):
        pts = [(0, 0), (s * WA / 2, 0), (s * WA / 2, HS)]
        for i in range(1, 25):
            x = s * WA / 2 * (1 - i / 24.0); pts.append((x, z_dome(abs(x))))
        return pts + [(0, D_A)]
    def b_half(s):
        pts = [(0, 0), (s * WB / 2, 0), (s * WB / 2, HB_END)]
        for i in range(1, 25):
            u = s * WB / 2 * (1 - i / 24.0); pts.append((u, z_dip(abs(u))))
        return pts + [(0, FLOOR_B)]
    faces = []
    for s in (-1, 1):
        faces.append(dict(kind='A', p3=[(u, 0.0, z) for u, z in a_half(s)])); faces.append(dict(kind='B', p3=[(0.0, u, z) for u, z in b_half(s)]))
    sh = ''.join(f'<path d="{face_d(ax, shadow_pts(f["p3"], 0.45, -0.30))}" fill="#000" fill-opacity="0.07"/>' for f in faces)
    faces.sort(key=lambda f: -ax.depth(centroid3(f['p3'])))
    body = ''; defs = ''
    for i, f in enumerate(faces):
        body += f'<path d="{face_d(ax, f["p3"])}" fill="{YELLOW}" stroke="#222" stroke-width="0.35" stroke-linejoin="round"/>'
        if f['kind'] == 'A':
            loc = [(u, -z) for (u, y, z) in f['p3']]; defs += f'<clipPath id="ca{i}"><path d="{poly_d(loc)}"/></clipPath>'
            M = ax.matrix((0, -T / 2 - 0.01, 0), (1, 0, 0), (0, 0, -1))
            body += f'<g transform="{M}" clip-path="url(#ca{i})">{a_texts(0, 0, NAME)}</g>'
        else:
            loc = [(u, -z) for (x, u, z) in f['p3']]; defs += f'<clipPath id="cb{i}"><path d="{poly_d(loc)}"/></clipPath>'
            M = ax.matrix((T / 2 + 0.01, 0, 0), (0, 1, 0), (0, 0, -1))
            body += f'<g transform="{M}" clip-path="url(#cb{i})">{b_texts(0, 0)}</g>'
    gr = f'<path d="{face_d(ax, [(-62,-58,0),(62,-58,0),(62,58,0),(-62,58,0)])}" fill="#ecebe4"/>'
    gx, gy = ax((0, -66, 0)); g2x, g2y = ax((0, -50, 0))
    defs += '<marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 Z" fill="#555"/></marker>'
    call = (f'<line x1="{gx:.2f}" y1="{gy:.2f}" x2="{g2x:.2f}" y2="{g2y:.2f}" stroke="#555" stroke-width="0.3" marker-end="url(#arr)"/>' + ui(gx, gy + 5, 'guest side', 2.6, 'middle', '#555', 700))
    lax, lay = ax((-52, 0, HS + 8)); lbx, lby = ax((0, 40, 0))
    call += ui(lax - 2, lay, 'A  name plate', 2.8, 'end', '#111', 700) + ui(lbx + 6, lby + 4, 'B  fin', 2.8, 'start', '#111', 700)
    scene = f'<defs>{defs}</defs>' + gr + sh + body + call
    # front elevation: guest's eye view (B edge-on, below the name)
    ex, ey = 62.0, 214.0
    elev = f'<path d="{A_local()["outline"].xform(lambda p: (ex + p[0], ey + p[1])).d()}" fill="{YELLOW}" stroke="#222" stroke-width="0.3"/>'
    elev += f'<rect x="{ex-T/2}" y="{ey-HB_END}" width="{T}" height="{HB_END}" fill="#555"/>'
    elev += f'<line x1="{ex}" y1="{ey-D_A}" x2="{ex}" y2="{ey}" stroke="{C_SLOT}" stroke-width="{SW}"/>'
    elev += a_texts(ex, ey, NAME)
    elev += ui(ex, ey + 8, 'FRONT, eye level: B is a hairline that stops at z 26.4, the name starts at 27', 2.2, 'middle', '#555', 700)
    plan_x, plan_y = 190.0, 205.0
    plan = (f'<rect x="{plan_x-WA/4}" y="{plan_y-T*0.5}" width="{WA*0.5}" height="{T}" fill="#222"/><rect x="{plan_x-T*0.5}" y="{plan_y-WB/4}" width="{T}" height="{WB*0.5}" fill="#222"/>'
            f'<path d="M{plan_x-WA/4} {plan_y} L{plan_x} {plan_y-WB/4} L{plan_x+WA/4} {plan_y} L{plan_x} {plan_y+WB/4} Z" fill="#00000010" stroke="#999" stroke-width="0.2" stroke-dasharray="1 1"/>'
            + ui(plan_x, plan_y + WB / 4 + 6, 'PLAN, support polygon 1:2', 2.4, 'middle', '#555', 700))
    sx, sy = 252.0, 214.0; z2y = lambda z: sy - z * 1.9
    joint = (f'<rect x="{sx-14}" y="{z2y(HC)}" width="12" height="{(HC-D_A)*1.9}" fill="{YELLOW}" stroke="#222" stroke-width="0.25"/>'
             f'<rect x="{sx+2}" y="{z2y(FLOOR_B)}" width="12" height="{FLOOR_B*1.9}" fill="#f6e27a" stroke="#222" stroke-width="0.25"/>'
             f'<line x1="{sx-16}" y1="{z2y(D_A)}" x2="{sx+16}" y2="{z2y(D_A)}" stroke="#c00" stroke-width="0.2"/>'
             + ui(sx - 8, z2y(HC) - 2, 'A', 2.2, 'middle') + ui(sx + 8, z2y(0) + 5, 'B', 2.2, 'middle') +
             ui(sx, sy + 9, 'COLUMN AT THE CROSSING', 2.4, 'middle', '#555', 700) + ui(sx, sy + 12.6, f'{GAP_V:.1f} mm gap: no bottoming-out', 2.2, 'middle'))
    title = ui(10, 12, 'D1 v2  TWO PLATES ON SLOTS  -  assembled', 4.0, 'start', '#111', 700) + ui(10, 17.5, f'cross footprint {WA:.0f} x {WB:.0f} mm, height {HC:.0f} mm; slide A down onto B.', 2.5)
    return svg_doc(W, H, title + scene + elev + plan + joint, 'D1 v2 assembled', 'axonometric + elevation', bg='#ffffff')

# ================================================================= SAIL variant
S_WA, S_HS, S_HC = 100.0, 28.0, 34.0
S_DA = 10.0; S_FLOOR = S_DA - GAP_V
S_TOE, S_REAR, S_H, S_HR = 18.0, 74.0, 72.0, 68.0          # B: toe length in front, rear arm, sail height at the front edge / end
S_NAME_Z = 13.5
S_R = ((S_WA / 2) ** 2 + (S_HC - S_HS) ** 2) / (2 * (S_HC - S_HS))
def sa_dome(x): return S_HC - S_R + math.sqrt(S_R ** 2 - x ** 2)

def sail_geo():
    m = SW / 2 + CH
    A_cut = Path((m, 0)).L((S_WA / 2, 0)).L((S_WA / 2, -S_HS)).A3((0, -S_HC), (-S_WA / 2, -S_HS)).L((-S_WA / 2, 0)).L((-m, 0))
    A_out = Path((-S_WA / 2, 0)).L((S_WA / 2, 0)).L((S_WA / 2, -S_HS)).A3((0, -S_HC), (-S_WA / 2, -S_HS)).Z()
    A_slot = slot_path(0, -S_DA)
    # B in (y,z): y to the right = rear. toe at the left, vertical front edge of the sail at y = SW/2+0.1
    yf = SW / 2 + 0.1
    # top edge: concave arc through (yf, S_H) ... (S_REAR, S_HR) with the same radius R
    # find a mid point on the circle of radius R through the two end points (concave: centre above)
    p0 = (yf, S_H); p1 = (S_REAR, S_HR)
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; ch = math.hypot(dx, dy)
    hh = math.sqrt(R * R - (ch / 2) ** 2)
    nx, ny = -dy / ch, dx / ch                       # normal; centre above the chord
    if ny < 0: nx, ny = -nx, -ny
    cx_, cy_ = mx + nx * hh, my + ny * hh
    mid = (cx_ - nx * R, cy_ - ny * R)               # point on the lower arc (bulging down)
    B_cut = Path((-S_TOE, 0)).L((S_REAR, 0)).L((S_REAR, -S_HR)).A3((mid[0], -mid[1]), (yf, -S_H)).L((yf, -S_FLOOR)).L((-S_TOE, -S_FLOOR)).Z()
    return A_cut, A_out, A_slot, B_cut

def build_sail():
    W, H = 300, 252
    A_cut, A_out, A_slot, B_cut = sail_geo()
    a_ox, a_by = 62.0, 62.0
    fa = lambda p: (a_ox + p[0], a_by + p[1])
    bx0, by0 = 150.0, 104.0
    fb = lambda p: (bx0 + p[0], by0 + p[1])
    bl_a = A_out.xform(fa).poly(0.4).buffer(BLEED, join_style=1, resolution=16)
    nm_s = name_size(NAME)
    artA = f'<path d="{poly_d(bl_a)}" fill="{YELLOW}"/>' + txt(a_ox, a_by - S_NAME_Z, NAME, nm_s) + txt(a_ox, a_by - 24.0, 'DINNER  ·  10.10.2026', SEC, weight=700, tracking=0.05)
    Bpoly = B_cut.xform(fb).poly(0.3)
    bl_b = Bpoly.buffer(BLEED, join_style=1, resolution=16)
    nsz = 55.0 / CAP                                  # numeral cap height 55 mm
    artB = (f'<path d="{poly_d(bl_b)}" fill="{YELLOW}"/>' + txt(bx0 + 32, by0 - 6.0, "4", nsz, weight=700) +
            txt(bx0 + 29, by0 - 2 * 0 - 0, '', 2) )
    cut = f'<path d="{A_cut.xform(fa).d()}" {cut_style()}/><path d="{B_cut.xform(fb).d()}" {cut_style()}/>'
    slot = slot_draw(A_slot, fa)
    d = [dim_h(a_ox - S_WA / 2, a_ox + S_WA / 2, a_by + 8, f'{S_WA:.0f}'), dim_v(a_ox + S_WA / 2 + 7, a_by - S_HC, a_by, f'{S_HC:.0f}'),
         dim_v(a_ox - S_WA / 2 - 7, a_by - S_HS, a_by, f'{S_HS:.0f}', side=-1),
         dim_h(bx0 - S_TOE, bx0 + S_REAR, by0 + 8, f'{S_TOE + S_REAR:.0f}  (toe {S_TOE:.0f} + rear {S_REAR:.0f})'),
         dim_v(bx0 + S_REAR + 7, by0 - S_H, by0, f'{S_H:.0f}'), dim_v(bx0 - S_TOE - 7, by0 - S_FLOOR, by0, f'{S_FLOOR:.1f}', side=-1)]
    lab = (ui(a_ox, 12, 'A  LOW NAME PLATE (slot from the bottom)', 3.0, 'middle', '#111', 700) +
           ui(bx0 + 20, 16, 'B  SAIL: tall fin behind the name (no slot on B: A rests against its front edge, toe in front)', 3.0, 'middle', '#111', 700))
    # assembled sketch
    ax = Axo(yaw_deg=-42, elev_deg=24, ox=95, oy=212, k=1.0)
    # A halves + B
    def a_poly():
        pts = [(-S_WA / 2, 0), (S_WA / 2, 0), (S_WA / 2, S_HS)]
        for i in range(1, 25):
            x = S_WA / 2 * (1 - 2 * i / 24.0); pts.append((x, sa_dome(abs(x))))
        pts.append((-S_WA / 2, S_HS)); return pts
    Apts = [(u, 0.0, z) for u, z in a_poly()]
    Bp = B_cut.pts(0.8); Bpts = [(0.0, y, -z) for y, z in Bp]
    # (sail on the +y side = behind the plate, guest at -y)
    sh = ''.join(f'<path d="{face_d(ax, shadow_pts(p, 0.45, -0.3))}" fill="#000" fill-opacity="0.07"/>' for p in (Apts, Bpts))
    order = sorted([('A', Apts), ('B', Bpts)], key=lambda t: -ax.depth(centroid3(t[1])))
    sc = ''; df = ''
    for kind, pts in order:
        sc += f'<path d="{face_d(ax, pts)}" fill="{YELLOW}" stroke="#222" stroke-width="0.35" stroke-linejoin="round"/>'
        if kind == 'A':
            M = ax.matrix((0, -T / 2 - 0.01, 0), (1, 0, 0), (0, 0, -1))
            sc += f'<g transform="{M}">{txt(0, -S_NAME_Z, NAME, nm_s) if False else txt(0, 0 - S_NAME_Z, NAME, nm_s)}</g>'
        else:
            M = ax.matrix((T / 2 + 0.01, 0, 0), (0, 1, 0), (0, 0, -1))
            sc += f'<g transform="{M}">{txt(32, -6.0, "4", nsz, weight=700)}</g>'
    gnd = f'<path d="{face_d(ax, [(-62,-50,0),(62,-50,0),(62,70,0),(-62,70,0)])}" fill="#ecebe4"/>'
    # stability
    from shapely.geometry import Polygon as P_
    Ap = Polygon([(x, z) for x, _, z in Apts]); Bpoly_yz = Polygon([(y, -z) for y, z in Bp])
    aA, zA = Ap.area, Ap.centroid.y
    aB, yB, zB = Bpoly_yz.area, Bpoly_yz.centroid.x, Bpoly_yz.centroid.y
    ycom = aB * yB / (aA + aB); zcom = (aA * zA + aB * zB) / (aA + aB)
    hull = Polygon([(-S_WA / 2, 0), (0, -S_TOE), (S_WA / 2, 0), (0, S_REAR)])
    dmin = hull.exterior.distance(Point(0, ycom)); tip = math.degrees(math.atan2(dmin, zcom))
    notes = [f'Sail variant (sketch, not tooled). Footprint {S_WA:.0f} x {S_TOE + S_REAR:.0f} mm (kite), height {S_H:.0f}.',
             f'Numeral: cap height 55 mm = {nsz:.0f} mm type, readable along the table from the door; seat/name stay on the low plate A.',
             f'COM y {ycom:.1f} mm behind A, z {zcom:.1f}; nearest hull edge {dmin:.1f} mm -> tip-over {tip:.0f} deg (a little under the main D1; heavier sail raises the COM).',
             'A is held against falling backwards by the sail face (gap 0.2) and forwards by its lean + the 2 mm toe step: weakest joint, test first.',
             'Slot in A 10.0 deep, toe/floor of B 9.4 (0.6 gap). Same slot test strip, same pre-coloured lemon board, 400 g.',
             'Sail top edge keeps the dip arc R119.1 (dome / dip echo stays). Nests on SRA3: ~7 sails + 7 plates per sheet (estimate, not drawn).']
    nt = ''.join(ui(150, 150 + i * 4.6, t, 2.4, 'start', '#222') for i, t in enumerate(notes))
    body = (layer('artwork', 'artwork', artA + artB) + layer('cut', 'cut', cut) + layer('slot', 'slot', slot) +
            layer('annotations', 'dims + notes', ''.join(d) + lab + nt) + layer('assembled', 'assembled sketch', gnd + sh + sc))
    return svg_doc(W, H, body, 'D1 sail variant', 'tall fin with table numeral', bg='#ffffff'), dict(tip=tip, ycom=ycom, zcom=zcom, dmin=dmin)

# ================================================================= verification
def verify():
    out = ['=== D1 v2 verification ==='] ; ok = True
    def chk(c, m):
        nonlocal ok
        out.append(('PASS ' if c else 'FAIL ') + m); ok &= bool(c)
    chk(SW >= T + 0.1 and SW <= T + 0.3, f'slot {SW} net for board {T}: clearance {SW-T:.2f}')
    bd = BC - FLOOR_B
    out.append(f'INFO slot depth A {D_A:.1f}, B {bd:.1f}; play angle B in A {math.degrees((SW-T)/D_A):.2f} deg, A in B {math.degrees((SW-T)/bd):.2f} deg; A top sways {HC*math.tan((SW-T)/bd):.2f} mm')
    zs = np.linspace(0, 60, 6001)
    a_mat = (zs >= D_A) & (zs <= HC); b_mat = (zs <= FLOOR_B)
    chk(not np.any(a_mat & b_mat) and abs((D_A - FLOOR_B) - GAP_V) < 1e-9, f'no material overlap at the crossing line; gap {D_A-FLOOR_B:.2f} mm (>= 0.6)')
    sz = name_size(NAME)
    chk(HB_END < NAME_Z, f'B never rises above the name: B max {HB_END:.2f} < name baseline {NAME_Z}')
    chk(NAME_Z + CAP * sz < z_dome(40) - 5, f'name cap top {NAME_Z+CAP*sz:.1f} vs dome at x=40 {z_dome(40):.1f} (margin {z_dome(40)-NAME_Z-CAP*sz:.1f})')
    for nm in (NAME, 'Alexandra Vorontsova', 'Mikhail Terentyev-Z'):
        s = name_size(nm); w = text_w(nm, s)
        chk(w / 2 <= 40 and NAME_Z + CAP * s < z_dome(w / 2) - 4, f'"{nm}" {s:.1f} mm, {w:.1f} wide: cap top {NAME_Z+CAP*s:.1f} < dome at its edge {z_dome(w/2):.1f} - 4')
    ew = text_w('TABLE 4  ·  SEAT 07', SEC, 700, 0.05); et = EYE_Z + CAP * SEC
    chk(et < z_dome(ew / 2) - 3, f'table/seat line {ew:.1f} wide, cap top {et:.1f} < dome at its edge {z_dome(ew/2):.1f} - 3')
    chk(CAP * SEC >= 3.45, f'secondary type {SEC} mm -> cap {CAP*SEC:.2f} mm >= 3.5')
    chk(EYE_Z - (NAME_Z + CAP * sz) >= 2.5, f'line spacing name / eyebrow {EYE_Z-NAME_Z-CAP*sz:.1f} mm')
    chk(text_w('DINNER', SEC, 700, 0.05) <= 26 and text_w('10 OCT', SEC, 700, 0.05) <= 26, 'B texts fit the 26 mm arm zones')
    # tip over
    A = A_local(); B = B_local()
    pa = A['outline'].poly(0.2); pb = B['outline'].poly(0.2)
    aA, zA = pa.area, -pa.centroid.y; aB, zB = pb.area, -pb.centroid.y
    zc = (aA * zA + aB * zB) / (aA + aB)
    hull = Polygon([(-WA / 2, 0), (0, -WB / 2), (WA / 2, 0), (0, WB / 2)])
    dd = hull.exterior.distance(Point(0, 0)); tip = math.degrees(math.atan2(dd, zc))
    chk(tip >= 55, f'COM z {zc:.1f}; rhombus inradius {dd:.1f} mm -> tip-over {tip:.1f} deg (>= 55; v1 61 deg with B 88 wide)')
    chk(pa.bounds[2] - pa.bounds[0] <= 110 and pb.bounds[2] - pb.bounds[0] <= 110, 'A and B fit C6 / DL flat')
    svg, polys = build_sheet()
    minD = min(polys[i][1].distance(polys[j][1]) for i in range(len(polys)) for j in range(i + 1, len(polys)))
    chk(minD >= 3.9, f'min distance between any two pieces / coupons on the sheet {minD:.2f} mm')
    ub = unary_union([p for _, p in polys]).bounds
    chk(ub[0] >= 5.9 and ub[2] <= SHEET_W - 5.9 and ub[1] >= GRIP and ub[3] <= SHEET_H - 5, f'all inside the usable area {tuple(round(b,1) for b in ub)}')
    tot = sum(p.area for _, p in polys[:-4])
    out.append(f'INFO utilisation {100*tot/(SHEET_W*SHEET_H):.1f} % ; 15 sets + 4 test coupons per SRA3')
    _, st = build_sail()
    chk(st['tip'] >= 45, f'sail variant (sketch, relaxed limit 45): COM y {st["ycom"]:.1f}, z {st["zcom"]:.1f}, hull distance {st["dmin"]:.1f} -> tip-over {st["tip"]:.0f} deg')
    out.append('RESULT ' + ('ALL PASS' if ok else 'SOME FAIL'))
    return '\n'.join(out)

if __name__ == '__main__':
    open(os.path.join(OUT, 'd1_dieline.svg'), 'w').write(build_dieline())
    open(os.path.join(OUT, 'd1_sheet_SRA3.svg'), 'w').write(build_sheet()[0])
    open(os.path.join(OUT, 'd1_assembled.svg'), 'w').write(build_assembled())
    open(os.path.join(OUT, 'd1_sail_variant.svg'), 'w').write(build_sail()[0])
    rep = verify(); open(os.path.join(OUT, 'd1_verify.txt'), 'w').write(rep + '\n'); print(rep)
