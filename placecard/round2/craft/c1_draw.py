import math
import c1_sim as c
from lib import *

S = 200.0
YS = 78.4
C4 = 79.9
QX = 66.0
C1 = -41.0
PACK_ACT = (120, 70, 12)   # napkin pack w, h, thickness
PACK = (132, 82)           # effective footprint (+ thickness)
c.S = S; c.R = S / math.sqrt(2); R = c.R

P = dict(c1=C1, xs=R - YS, qx=QX, c4=C4)

def states():
    """return list of (label, layers) after each step"""
    base = c.Layer("base", [(0, R), (-R, 0), (0, -R), (R, 0)], list(c.REF), 0, 0)
    st = [("0 Napkin pack on printed (lining) face", [base])]
    L = c.fold([base], (0, C1), (1, 0), flap_left=False, tag="/F1")
    st.append(("1 Bottom corner up", L))
    Pr = (R - YS, YS); Qr = (QX, C1)
    L = c.fold(L, Pr, (Qr[0] - Pr[0], Qr[1] - Pr[1]), flap_left=True, tag="/F2")
    st.append(("2 Right lapel in", L))
    Pl = (-(R - YS), YS); Ql = (-QX, C1)
    L = c.fold(L, Pl, (Ql[0] - Pl[0], Ql[1] - Pl[1]), flap_left=False, tag="/F3")
    st.append(("3 Left lapel over right", L))
    L = c.finish_apex(L, C4)
    st.append(("4 Apex flap down = closed", L))
    return st

def edge_hits(p, d):
    """intersection segment of infinite line with diamond"""
    pts_ = []
    V = [(0, R), (-R, 0), (0, -R), (R, 0)]
    for i in range(4):
        a, b = V[i], V[(i + 1) % 4]
        ex, ey = b[0] - a[0], b[1] - a[1]
        den = d[0] * ey - d[1] * ex
        if abs(den) < 1e-12: continue
        t = ((a[0] - p[0]) * ey - (a[1] - p[1]) * ex) / den
        u = ((a[0] - p[0]) * d[1] - (a[1] - p[1]) * d[0]) / den
        if -1e-9 <= u <= 1 + 1e-9:
            pts_.append((p[0] + t * d[0], p[1] + t * d[1]))
    pts_.sort()
    return pts_[0], pts_[-1]

def sheet_art(d, back=False):
    """name etc. in sheet coords (y-up), text drawn upright via scale(1,-1)"""
    cap = capheight(600)
    def T(x, y, s, size, w=600, anchor="middle", fill=INK, ls=0):
        d.add(f'<g transform="translate({f2(x)} {f2(-y)})"><text x="0" y="0" font-size="{f2(size)}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text></g>')
    # y-up sheet coordinates mapped to svg by caller with scale(1,-1)? here we directly give svg coords (y flipped)
    T(0, 88, "Sophia", 13.5, 600)
    T(0, 70, "Zhuravkova", 13.5, 600)
    T(0, 56.5, "Dinner · Colorblock × DNA Kitchen · Moscow · 10 Oct 2026", 2.5, 500)

def draw_state(d, layers, ox, oy, k, open_apex=False, label=None, show_art=True, cord=None, pack=True, step=None):
    """draw folded state. final coords (y-up) -> svg (ox + k x, oy - k y)"""
    def tp(q): return (ox + k * q[0], oy - k * q[1])
    if pack and step is not None and step >= 1:
        # napkin pack (effective footprint outline + actual rectangle)
        pw, ph = PACK_ACT[0], PACK_ACT[1]
        d.rect(ox - k * PACK[0] / 2, oy - k * PACK[1] / 2, k * PACK[0], k * PACK[1], "thin", "none", extra='stroke-dasharray="1.2 1"')
    ls = sorted(layers, key=lambda l: l.z)
    cid = 0
    for l in ls:
        if open_apex and l.name.endswith("F4"):
            continue
        poly = [tp(q) for q in l.poly]
        cid += 1
        flips_odd = (l.flips % 2 == 1)
        fill = LEMON if not flips_odd else "#fbe684"
        if l.name == "base" and step is not None and step >= 1:
            pass
        # soft shadow
        d.add(f'<polygon points="{pts([(x+0.9,y+0.9) for x,y in poly])}" class="shadow"/>')
        d.add(f'<polygon points="{pts(poly)}" fill="{fill}" class="edge"/>')
    if open_apex:
        # apex flap returned to original position, print side up
        base = [l for l in ls if l.name == "base"]
    return

def draw_state_full(d, layers, ox, oy, k, step, open_apex=False, with_art=False):
    ls = sorted(layers, key=lambda l: l.z)
    def tp(q): return (ox + k * q[0], oy - k * q[1])
    # napkin pack under everything (but above base): draw after base layer only
    for l in ls:
        if open_apex and l.name.endswith("F4"):
            continue
        poly = [tp(q) for q in l.poly]
        odd = l.flips % 2 == 1
        fill = "#fbe684" if odd else LEMON
        d.add(f'<polygon points="{pts([(x+0.7,y+0.9) for x,y in poly])}" class="shadow"/>')
        d.add(f'<polygon points="{pts(poly)}" fill="{fill}" class="edge"/>')
        if l.name == "base" and step >= 1:
            # pack lies on base
            x0, y0 = tp((-PACK_ACT[0] / 2, PACK_ACT[1] / 2))
            d.add(f'<rect x="{f2(x0)}" y="{f2(y0)}" width="{f2(k*PACK_ACT[0])}" height="{f2(k*PACK_ACT[1])}" fill="#f4f1ea" stroke="#9c9688" stroke-width=".25"/>')
            for i in range(1, 6):
                yy = y0 + k * PACK_ACT[1] * i / 6
                d.add(f'<line x1="{f2(x0)}" y1="{f2(yy)}" x2="{f2(x0+k*PACK_ACT[0])}" y2="{f2(yy)}" stroke="#d9d4c6" stroke-width=".15"/>')
    return


NAME_A = (106, 12.0)   # baseline y, font size
NAME_B = (92, 12.0)
INFO_Y = 85.0

def build_dieline():
    W, H = 560, 500
    d = Doc(0, 0, W, H, scale=3.0)
    d.title(12, 14, "01  KOSODE — origata-style diagonal wrap, name under the V-flap",
            "Dieline + fold diagram. Print (lining) side shown. One 200 x 200 mm square sheet, 135 g lemon paper; folds only, no cuts, no glue.")
    cx, cy, k = 148, 250, 1.0
    def tp(q): return (cx + k * q[0], cy - k * q[1])
    V = [(0, R), (-R, 0), (0, -R), (R, 0)]
    d.poly([tp(q) for q in V], "cut", LEMON)
    x0, y0 = tp((-PACK_ACT[0] / 2, PACK_ACT[1] / 2))
    d.rect(x0, y0, PACK_ACT[0], PACK_ACT[1], "thin", "#f4f1ea", extra='stroke-dasharray="1.5 1"')
    d.rect(*tp((-PACK[0] / 2, PACK[1] / 2)), PACK[0], PACK[1], "thin", "none", extra='stroke-dasharray="0.6 1.2"')
    d.note(cx, cy + 1, "napkin pack 120 x 70 x 12", 2.6, GREY, "middle")
    d.note(cx, cy + 5, "(effective footprint 132 x 82)", 2.2, GREY, "middle")
    a, b = edge_hits((-R, C1), (1, 0)); d.line(*tp(a), *tp(b), "val")
    Pr = (R - YS, YS); Qr = (QX, C1)
    a, b = edge_hits(Pr, (Qr[0] - Pr[0], Qr[1] - Pr[1])); d.line(*tp(a), *tp(b), "val")
    Pl = (-(R - YS), YS); Ql = (-QX, C1)
    a, b = edge_hits(Pl, (Ql[0] - Pl[0], Ql[1] - Pl[1])); d.line(*tp(a), *tp(b), "val")
    a, b = edge_hits((-R, C4), (1, 0)); d.line(*tp(a), *tp(b), "val")
    cap = capheight(600)
    d.text(cx, cy - NAME_A[0], "Sophia", NAME_A[1], 600, INK, "middle")
    d.text(cx, cy - NAME_B[0], "Zhuravkova", NAME_B[1], 600, INK, "middle")
    d.text(cx, cy - INFO_Y, "Dinner · Colorblock × DNA Kitchen · Moscow · 10 Oct 2026", 2.4, 500, INK, "middle")
    def badge(q, n):
        x, y = tp(q); d.circle(x, y, 3.4, "thin", "#fff"); d.text(x, y + 1.3, str(n), 3.6, 700, INK, "middle")
    badge((0, C1 - 14), 1); badge((QX + 30, 8), 2); badge((-(QX + 30), 8), 3); badge((0, C4 + 4.5 - 12), 4)
    d.note(cx, cy + R + 8, "Shown corner-up, the way it is folded. Print file: the square sheet with the art turned 45 deg.", 2.5, GREY, "middle")
    nw = tw("Zhuravkova", NAME_B[1], 600)
    d.note(cx, cy + 14, f"name: Wix Madefor Text SemiBold 12 mm, cap-height {cap*NAME_A[1]:.1f} mm, 'Zhuravkova' {nw:.1f} mm wide", 2.3, GREY, "middle")
    # minis
    st = states()
    mk = 0.33
    px, py = 292, 30
    for i, (lab, L) in enumerate(st):
        col, row = i % 2, i // 2
        ox = px + 62 + col * 128
        oy = py + 52 + row * 106
        draw_state_full(d, L, ox, oy, mk, i)
        d.note(ox - 60, oy + 50, lab, 2.5, INK)
    ox, oy = px + 62 + 128, py + 52 + 2 * 106
    draw_state_full(d, st[-1][1], ox, oy, mk, 4)
    d.line(ox, oy - (C4 + 6) * mk, ox, oy + 48 * mk, "ink", extra='stroke-width=".9"')
    d.note(ox - 60, oy + 50, "5 Cord round the waist, bow on the flap", 2.5, INK)
    notes = [
        "FOLD SEQUENCE   napkin pack centred print-face-up, corner toward you",
        "1  Bottom corner up along y = -41 (pack's lower edge + half thickness).",
        "2  Right corner in along the line from shoulder (%.1f, %.1f) to (66, -41)." % (R - YS, YS),
        "3  Left corner in along the mirror line, OVER the right lapel (migi-mae, left-over-right):",
        "    lapel tips land at +/-11.4 mm past the centreline, so they overlap 22.8 mm.",
        "4  Apex down along y = %.1f; its tip lands at y = %.1f, covering the upper pack." % (C4, 2 * C4 - R),
        "5  2 mm black waxed cord round the short way (about 400 mm), bow on the V-flap.",
        "Guest: pull the bow, lift the V-flap; the name sits on its lining, upright toward the seat.",
    ]
    d.notes(292, 362, notes, 2.7, 1.5, INK)
    d.legend(292, 418, [("val", "valley fold toward you (all four folds), scored 0.4 mm on the print side"),
                        ("cut", "sheet edge (guillotine, no die)"),
                        ("thin", "napkin pack; dotted = effective footprint incl. thickness")])
    # back plate
    bx, by, kb = 490, 440, 0.30
    d.note(292, 444, "Reverse plate (optional duplex): 'Dinner' | date either side of the cord line.", 2.4, GREY)
    d.poly([(bx + kb * x, by - kb * y) for x, y in V], "thin", "#fff")
    d.line(bx - kb * (R - C4), by - kb * C4, bx + kb * (R - C4), by - kb * C4, "val")
    g = f'<g transform="rotate(180 {f2(bx)} {f2(by - kb*C4)})">'
    g += f'<text x="{f2(bx - 5*kb)}" y="{f2(by - kb*62)}" font-size="{f2(kb*10)}" font-weight="700" text-anchor="end" fill="{INK}">Dinner</text>'
    g += f'<text x="{f2(bx + 5*kb)}" y="{f2(by - kb*62)}" font-size="{f2(kb*5)}" font-weight="500" text-anchor="start" fill="{INK}">10.10.2026</text></g>'
    d.add(g)
    d.save("c1_dieline.svg")

def draw_closed_text(d, ox, oy, k=1.0):
    d.add(f'<text x="{f2(ox-5)}" y="{f2(oy-62)}" font-size="10" font-weight="700" text-anchor="end" fill="{INK}">Dinner</text>')
    d.add(f'<text x="{f2(ox+5)}" y="{f2(oy-62)}" font-size="5" font-weight="500" text-anchor="start" fill="{INK}">10.10.2026</text>')

def bow(d, ox, by, sc=1.0, w=1.6):
    d.path(f"M{ox},{by} C{ox-26},{by-20} {ox-32},{by+6} {ox},{by} C{ox+26},{by-20} {ox+32},{by+6} {ox},{by}", "ink", extra=f'stroke-width="{w}"')
    d.path(f"M{ox},{by} C{ox-8},{by+14} {ox-16},{by+22} {ox-24},{by+34}", "ink", extra=f'stroke-width="{w}"')
    d.path(f"M{ox},{by} C{ox+9},{by+14} {ox+15},{by+20} {ox+25},{by+30}", "ink", extra=f'stroke-width="{w}"')

def build_assembled():
    W, H = 560, 270
    d = Doc(0, 0, W, H, scale=3.0)
    d.title(12, 14, "01  KOSODE — assembled", "Top view on the place setting. Left: closed, as laid. Right: cord pulled, V-flap lifted (guest sits at the bottom of the picture).")
    st = states()
    Lc = st[-1][1]
    ox, oy = 134, 196
    draw_state_full(d, Lc, ox, oy, 1.0, 4)
    draw_closed_text(d, ox, oy)
    d.line(ox, oy - (C4 + 14), ox, oy + 52, "ink", extra='stroke-width="1.7"')
    bow(d, ox, oy - 38)
    ext_x = max(q[0] for l in Lc for q in l.poly); ext_y0 = min(q[1] for l in Lc for q in l.poly); ext_y1 = max(q[1] for l in Lc for q in l.poly)
    d.note(ox, oy + 76, f"CLOSED  {2*ext_x:.0f} x {ext_y1-ext_y0:.0f} mm footprint, about 14 mm tall", 2.8, INK, "middle")
    ox2, oy2 = 424, 196
    draw_state_full(d, Lc, ox2, oy2, 1.0, 4, open_apex=True)
    base = [l for l in st[3][1] if l.name == "base"][0]
    apex = clip_halfplane(base.poly, (0, C4), (1, 0), keep_left=True)
    ap = [(ox2 + x, oy2 - y) for x, y in apex]
    d.add(f'<polygon points="{pts([(x+.7,y+.9) for x,y in ap])}" class="shadow"/>')
    d.add(f'<polygon points="{pts(ap)}" fill="{LEMON}" class="edge"/>')
    d.add(f'<text x="{f2(ox2)}" y="{f2(oy2-NAME_A[0])}" font-size="{NAME_A[1]}" font-weight="600" text-anchor="middle" fill="{INK}">Sophia</text>')
    d.add(f'<text x="{f2(ox2)}" y="{f2(oy2-NAME_B[0])}" font-size="{NAME_B[1]}" font-weight="600" text-anchor="middle" fill="{INK}">Zhuravkova</text>')
    d.add(f'<text x="{f2(ox2)}" y="{f2(oy2-INFO_Y)}" font-size="2.4" font-weight="500" text-anchor="middle" fill="{INK}">Dinner · Colorblock × DNA Kitchen · Moscow · 10 Oct 2026</text>')
    d.path(f"M{ox2+84},{oy2+20} C{ox2+100},{oy2+2} {ox2+110},{oy2+44} {ox2+96},{oy2+62} S{ox2+68},{oy2+74} {ox2+54},{oy2+66}", "ink", extra='stroke-width="1.6"')
    d.note(ox2, oy2 + 76, "OPEN  flap hinged back; name reads toward the guest", 2.8, INK, "middle")
    d.save("c1_assembled.svg")

def verify():
    st = states(); Lc = st[-1][1]
    out = []
    out.append("C1 KOSODE geometry check (units mm; y up, sheet shown corner-up)")
    out.append(f"sheet {S:.0f} x {S:.0f}, half-diagonal R = {R:.2f}")
    out.append(f"napkin pack {PACK_ACT}, effective footprint {PACK} (thickness added once)")
    n = 0; ok = 0
    for ix in range(-int(PACK[0]/2 - 1.5), int(PACK[0]/2 - 1.5) + 1):
        for iy in range(-int(PACK[1]/2 - 1.5), int(PACK[1]/2 - 1.5) + 1):
            n += 1; ok += any(inside(l.poly, (ix, iy)) for l in Lc if l.name != "base")
    out.append(f"cover test (1 mm grid over the pack footprint inset 1.5 mm): {ok}/{n} points under at least one folded layer = {100*ok/n:.1f} %")
    f2m = min(q[0] for l in Lc if l.name == "base/F2" for q in l.poly)
    f3m = max(q[0] for l in Lc if l.name == "base/F3" for q in l.poly)
    out.append(f"right lapel tip reaches x = {f2m:.1f}, left lapel tip x = {f3m:.1f}  -> lapels overlap {f3m - f2m:.1f} mm (left over right)")
    top = max(max(q[1] for q in l.poly) for l in Lc if l.name not in ("base", "base/F4"))
    out.append(f"highest point of any lapel layer y = {top:.2f}; apex crease y = {C4:.2f}; clearance {C4 - top:.2f} mm (must be > 0 so the apex folds over nothing)")
    tip = min(q[1] for l in Lc if l.name.endswith("F4") for q in l.poly)
    out.append(f"apex flap height {R - C4:.1f}, width at crease {2*(R - C4):.1f}; lands with tip at y = {tip:.1f} (pack top 41, so flap covers {41 - tip:.1f} of the 82 mm pack height)")
    ex = max(q[0] for l in Lc for q in l.poly); y0 = min(q[1] for l in Lc for q in l.poly); y1 = max(q[1] for l in Lc for q in l.poly)
    out.append(f"closed footprint {2*ex:.1f} x {y1 - y0:.1f} mm")
    for nm in ("Sophia", "Zhuravkova"):
        out.append(f"{nm}: {tw(nm, 12.0, 600):.1f} mm wide at 12 mm SemiBold")
    for nm, y, sz in (("Zhuravkova", NAME_B[0], 12.0), ("Sophia", NAME_A[0], 12.0)):
        w = tw(nm, sz, 600); top_y = y + 0.78 * sz
        avail = 2 * (R - top_y)
        out.append(f"{nm}: top of ascenders at y = {top_y:.1f}; sheet width available there {avail:.1f} mm vs text {w:.1f} -> margin {(avail - w)/2:.1f} mm per side")
    girth = 2 * (PACK_ACT[1] + PACK_ACT[2])
    out.append(f"cord: girth round the pack's short way = 2 x (70 + 12) = {girth} mm; bow 2 x 45 loops + 2 x 60 tails -> cut length {girth + 90 + 120 + 20} mm (394, say 400)")
    out.append("flap walls: crease positions are offset by half the pack thickness (6 mm) so the paper closes tight without bulging.")
    open("c1_verify.txt", "w").write("\n".join(out) + "\n")
    print("\n".join(out))

if __name__ == "__main__":
    build_dieline(); build_assembled(); verify()
