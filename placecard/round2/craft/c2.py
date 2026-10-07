import math
from lib import *

# ---------------- parameters ----------------
C = 170.0            # ring circumference (slot centre to tongue base)
N = 16               # ribbons per row
p = C / N            # ribbon width = column pitch
Rb = C / (2 * math.pi)   # belt radius
BELT, B, SL, FOOT = 22.0, 4.0, 18.0, 8.0
H = BELT + B + SL + B + SL + B + FOOT      # 78
X0, X1 = 10.0, 10.0 + C   # ring spans x in [X0, X1] on the flat strip
L = 194.0                  # strip length (tongue 14 beyond X1)
F = 5.0                    # outward bulge of each ribbon (sagitta) at the pre-crease
seg = SL / 2
hc = 2 * math.sqrt(seg ** 2 - F ** 2)       # compressed chord of one ribbon
dz = SL - hc
Hc = H - 2 * dz
ALPHA = math.radians(21)

def verify():
    o = []
    o.append("C2 LANTERN LATTICE geometry check (mm)")
    o.append(f"strip {L:.0f} x {H:.0f}; ring circumference C = {C:.0f} -> belt radius {Rb:.2f} (dia {2*Rb:.1f})")
    o.append(f"{N} ribbons per row, ribbon width p = {p:.3f}; slit length {SL}, bridge {B}")
    o.append(f"rows: belt {BELT} | {B} | slit row A {SL} | {B} | slit row B {SL} | {B} | foot {FOOT}  = {H} mm")
    o.append(f"ribbon creased at its middle (mountain, outward); two {seg:.0f} mm segments; bulge (sagitta) F = {F}")
    o.append(f"compressed chord per ribbon = 2*sqrt({seg}^2 - {F}^2) = {hc:.2f} -> shortening {dz:.2f} per row ({100*dz/SL:.0f} %)")
    o.append(f"lantern height {H:.0f} -> {Hc:.1f} mm; ribbon end angle from vertical = {math.degrees(math.asin(F/seg)):.1f} deg")
    # sine-buckle comparison (no pre-crease)
    f_sine = 2 / math.pi * math.sqrt(SL * dz)
    o.append(f"check, un-creased sine buckle with same shortening: f = (2/pi) sqrt(L dz) = {f_sine:.2f} (creased kink gives {F}); the crease forces the lower-energy bulge to the OUTSIDE")
    Rm = Rb + F
    o.append(f"belt-ring radius {Rb:.2f}; bulge radius {Rm:.2f}; circumference at the bulge {2*math.pi*Rm:.1f} vs ribbons {N*p:.1f}")
    gap = (2 * math.pi * Rm - N * p) / N
    o.append(f"-> gaps open between neighbouring ribbons: {gap:.2f} mm each (ribbons splay; they must not overlap: gap > 0 OK)")
    # ribbon edge clearance in the offset row
    o.append(f"row B is offset by p/2 = {p/2:.2f}; ribbons of A and B cross at the bridge bands -> brick/diamond pattern")
    # ribbon bending strain
    t = 0.40
    o.append(f"crease: 350 g/m2 board t = {t}; kink radius ~ 1.0 -> fold OK; ribbon bending strain at crease ~ t/(2r) = {t/2:.2f} (scored) fine")
    # name arcs
    for nm, sz, w in (("Zhuravkova", 8.0, 600), ("Sophia Zhuravkova (one line)", 8.0, 600)):
        s = tw(nm if "one" not in nm else NAME, sz, w)
        o.append(f"{nm}: {s:.1f} mm wide at {sz} mm; on the belt = {math.degrees(s/Rb):.0f} deg of arc; at the edges of that arc it is foreshortened to cos(half-arc) = {math.cos(s/Rb/2):.2f}")
    o.append(f"belt text zone: 2 lines of 8 mm type (cap-h {capheight(600)*8:.1f}) in {BELT} mm; leading 9.6, margins {(BELT-9.6-capheight(600)*8)/2:.1f}")
    o.append(f"SRA3 320 x 450: strips {L:.0f} x {H:.0f} -> {int(450//L)} across x {int(320//H)} down = {int(450//L)*int(320//H)} per sheet; 40 guests = {math.ceil(40/(int(450//L)*int(320//H)))} sheets")
    open("c2_verify.txt", "w").write("\n".join(o) + "\n")
    print("\n".join(o))

# ---------------- dieline ----------------
def dieline():
    W, Hh = 330, 250
    d = Doc(0, 0, W, Hh, scale=5.0)
    d.title(10, 13, "02  LANTERN LATTICE — kirigami cylinder that pops into a double barrel",
            "Dieline 1:1 (mm). One strip 194 x 78, 350 g lemon board, black print. Knife-cut slits (zero width), 32 mid-creases, slot and tongues.")
    ox, oy = 18, 40
    X = lambda x: ox + x
    Y = lambda y: oy + y
    # outline with tongues
    tong_top = [(Y(3), Y(11)), (Y(13), Y(21))]
    # outline polygon
    d.rect(X(0), Y(0), L, H, "cut", LEMON)
    # lattice zone: material outside x in [0,X0) and (X1, L] in lattice rows is cut away -> draw white notches
    zone_y0 = BELT
    zone_y1 = H - FOOT
    d.rect(X(0), Y(zone_y0), X0, zone_y1 - zone_y0, "cut", "#ffffff")
    d.rect(X(X1), Y(zone_y0), L - X1, zone_y1 - zone_y0, "cut", "#ffffff")
    # tongues: shapes at right end limited to tongues; cut away the rest of belt end
    # belt right end region [X1,L]: keep two tongues of 8 mm, remove the rest
    for (a, b) in [(0, 3), (11, 13), (21, BELT)]:
        d.rect(X(X1), Y(a), L - X1, b - a, "cut", "#ffffff")
    # foot tongue 4mm tall centred in foot
    fy0 = H - FOOT
    d.rect(X(X1), Y(fy0), L - X1, 2, "cut", "#ffffff")
    d.rect(X(X1), Y(fy0 + 6), L - X1, 2, "cut", "#ffffff")
    # slots at left (for tongues), x = X0 .. +1 wide  (tongue thickness 0.4 -> slot 0.8 wide)
    for (a, b) in tong_top:
        d.rect(X(X0 - 0.4), Y(a - 0.0), 0.8, b - a, "cut", "#ffffff")
    d.rect(X(X0 - 0.4), Y(fy0 + 2), 0.8, 4, "cut", "#ffffff")
    # slits: row A y in [BELT+B, +SL], row B next. x = X0 + k*p (A: k=1..N-1) ; B offset p/2 (k=0..N-1)
    yA0 = BELT + B; yB0 = yA0 + SL + B
    for k in range(1, N):
        x = X0 + k * p
        d.line(X(x), Y(yA0), X(x), Y(yA0 + SL), "cut")
    for k in range(0, N):
        x = X0 + (k + 0.5) * p
        d.line(X(x), Y(yB0), X(x), Y(yB0 + SL), "cut")
    # mid creases (mountain, from outside) - ribbons
    for k in range(0, N):
        xa0 = X0 + k * p; xa1 = xa0 + p
        d.line(X(xa0 + 0.6), Y(yA0 + SL / 2), X(xa1 - 0.6), Y(yA0 + SL / 2), "mtn")
        xb0 = X0 + (k - 0.5) * p; xb1 = xb0 + p
        a0 = max(xb0, X0) + 0.6; a1 = min(xb1, X1) - 0.6
        if a1 > a0:
            d.line(X(a0), Y(yB0 + SL / 2), X(a1), Y(yB0 + SL / 2), "mtn")
    # belt valley fold lines at belt/lattice junction? (none) -- show ring bridge lines as thin guide
    for y in (BELT, BELT + B, yA0 + SL, yA0 + SL + B, yB0 + SL, yB0 + SL + B):
        d.line(X(0 if y < zone_y0 or y > zone_y1 else X0), Y(y), X(L if y < zone_y0 or y > zone_y1 else X1), Y(y), "thin", extra='stroke-dasharray=".6 1.4"')
    # print: four quarters around the ring
    ink = INK
    def two(cx, l1, l2, sz=8.0, w=600):
        d.text(X(cx), Y(8.4), l1, sz, w, ink, "middle")
        d.text(X(cx), Y(8.4 + 9.6), l2, sz, w, ink, "middle")
    q = C / 4
    cxs = [X0 + q * 0.75 + q * i for i in range(4)]  # 0.75 q offset so name centres sit 32 off slot
    # name A, Dinner, name B, event
    two(cxs[0], "Sophia", "Zhuravkova")
    d.text(X(cxs[1]), Y(12.0), "Dinner", 10.5, 700, ink, "middle")
    d.text(X(cxs[1]), Y(18.6), "10.10.2026", 3.6, 500, ink, "middle")
    two(cxs[2], "Sophia", "Zhuravkova")
    d.text(X(cxs[3]), Y(9.6), "Colorblock × DNA Kitchen", 2.9, 500, ink, "middle")
    d.text(X(cxs[3]), Y(14.0), "Moscow", 2.9, 500, ink, "middle")
    d.text(X(cxs[3]), Y(18.4), "10 Oct 2026", 2.9, 500, ink, "middle")
    # dimensions
    d.line(X(0), Y(H + 6), X(L), Y(H + 6), "dim"); d.note(X(L / 2), Y(H + 10), f"{L:.0f}", 2.6, INK, "middle")
    d.line(X(L + 5), Y(0), X(L + 5), Y(H), "dim"); d.add(f'<text transform="translate({f2(X(L+9))} {f2(Y(H/2))}) rotate(90)" font-size="2.6" fill="{INK}" text-anchor="middle">{H:.0f}</text>')
    d.line(X(X0), Y(H + 14), X(X1), Y(H + 14), "dim"); d.note(X((X0 + X1) / 2), Y(H + 18), f"ring {C:.0f} = {N} x {p:.3f}", 2.6, INK, "middle")
    # callouts
    d.note(X(X1 + 1), Y(-3), "tongues 14 x 8 (belt)", 2.4, GREY)
    d.note(X(X0 - 9), Y(-3), "slots 0.8 x 8 at x = 10", 2.4, GREY)
    
    d.note(X(1), Y(zone_y0 + 22), "notch: lattice", 2.2, GREY)
    d.note(X(1), Y(zone_y0 + 25.5), "ends butt", 2.2, GREY)
    # detail: ribbon geometry
    gx, gy = 18, 168
    d.text(gx, gy, "Ribbon in flat and pressed states (side section, to scale)", 3.0, 600, INK)
    ax, ay = gx + 18, gy + 8
    d.line(ax, ay, ax, ay + SL, "dim")
    d.note(ax + 2, ay + 4, "flat 18", 2.4, GREY)
    bx = ax + 50
    pts_ = [(bx, ay), (bx + F, ay + dz / 2 + hc / 4 + 0.0), (bx, ay + dz + hc)]
    pts_ = [(bx, ay + dz / 2), (bx + F, ay + dz / 2 + hc / 2), (bx, ay + dz / 2 + hc)]
    d.add(f'<polyline points="{pts(pts_)}" class="ink" fill="none"/>')
    d.line(bx, ay, bx, ay + SL, "thin", extra='stroke-dasharray="1 1"')
    d.note(bx + F + 2, ay + SL / 2, f"pressed: chord {hc:.2f}, bulge {F}", 2.4, GREY)
    d.note(bx + F + 2, ay + SL / 2 + 3.6, f"(each row loses {dz:.2f} mm)", 2.4, GREY)
    # numbers for rows
    d.notes(18, 202, [
        "ASSEMBLY (30 s)",
        "1  Roll the strip with the print outside; pass the two belt tongues through the slots from the outside and fold them flat inside;",
        "    the 4 mm foot tongue the same way. Ring = 170 mm = 54 mm diameter.",
        "2  Stand it on the table and press the belt down 7 mm: the 32 pre-creased ribbons kink and bulge outward; the staggered rows interlock into a lattice.",
        "3  Optional: LED tealight inside; light leaks through the lattice, the belt stays dark-printed and reads front and back.",
    ], 2.7, 1.5, INK)
    d.legend(190, 168, [("cut", "knife cut / outline (zero-width slits; slots 0.8)"),
                         ("mtn", "mountain crease (score from print side, so crease bulges out)"),
                         ("thin", "bridge-band guide (no score)"),
                         ("swatch_lemon", "350 g lemon board, print black, one side")])
    d.save("c2_dieline.svg")

# ---------------- assembled ----------------
def proj(r, phi, z, ox, oy, s, alpha=ALPHA):
    X = r * math.sin(phi); Y = -r * math.cos(phi)     # Y<0 toward viewer
    return (ox + s * X, oy - s * (z * math.cos(alpha) + Y * math.sin(alpha)))

def lantern(d, ox, oy, s, f, name=True, tag=None):
    seg_ = SL / 2
    hcl = 2 * math.sqrt(seg_ ** 2 - f ** 2)
    # z of each part from bottom
    z = 0
    zf0, zf1 = 0, FOOT
    zb3 = (zf1, zf1 + B)
    zrB = (zb3[1], zb3[1] + hcl)
    zb2 = (zrB[1], zrB[1] + B)
    zrA = (zb2[1], zb2[1] + hcl)
    zb1 = (zrA[1], zrA[1] + B)
    zbelt = (zb1[1], zb1[1] + BELT)
    Htot = zbelt[1]
    def band(z0, z1, front=True, fill=LEMON, steps=40, shade=True):
        rng = range(0, steps) 
        for i in rng:
            p1 = -math.pi / 2 + math.pi * i / steps if front else math.pi / 2 + math.pi * i / steps
            p2 = -math.pi / 2 + math.pi * (i + 1) / steps if front else math.pi / 2 + math.pi * (i + 1) / steps
            a = proj(Rb, p1, z0, ox, oy, s); b = proj(Rb, p2, z0, ox, oy, s)
            c_ = proj(Rb, p2, z1, ox, oy, s); d_ = proj(Rb, p1, z1, ox, oy, s)
            m = (p1 + p2) / 2
            sh = 0.78 + 0.22 * math.cos(m) if front else 0.7
            col = shade_col(fill, sh)
            d.add(f'<polygon points="{pts([a,b,c_,d_])}" fill="{col}" stroke="{col}" stroke-width=".15"/>')
    def shade_col(hexc, k):
        r = int(hexc[1:3], 16); g = int(hexc[3:5], 16); b = int(hexc[5:7], 16)
        k = max(0, min(1.12, k))
        return "#%02x%02x%02x" % (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * (0.9 + 0.1 * k) * min(k, 1))))
    # inside back wall + top opening
    top_ellipse = [proj(Rb, 2 * math.pi * i / 72, Htot, ox, oy, s) for i in range(72)]
    # 1 back bands & belt back half (dark)
    for (z0, z1) in (zf0 and (0, 0) or (zf0, zf1), zb3, zb2, zb1, zbelt):
        band(z0, z1, front=False, fill=LEMON_D)
    # back ribbons
    def ribbons(row_offset, za, zb, front):
        # za = z of lower end, zb = z of upper end
        zm = (za + zb) / 2
        polys = []
        for k in range(N):
            th = (k + row_offset) * 2 * math.pi / N
            cth = math.cos(th)
            is_front = math.cos(th) > 0
            # th measured from front direction (phi=0 front), convert
            if is_front != front: continue
            w2 = p / 2
            def e(r, zz, sgn):
                X = r * math.sin(th) + sgn * w2 * math.cos(th)
                Yd = -r * math.cos(th) + sgn * w2 * math.sin(th) * (-1) * 0  # keep ribbon planar approx
                Yd = -r * math.cos(th) + sgn * w2 * math.sin(th)
                return (ox + s * X, oy - s * (zz * math.cos(ALPHA) + Yd * math.sin(ALPHA)))
            if f > 1e-6:
                L_ = [e(Rb, za, -1), e(Rb + f, zm, -1), e(Rb, zb, -1)]
                R_ = [e(Rb, zb, 1), e(Rb + f, zm, 1), e(Rb, za, 1)]
                # two facets
                lo = [e(Rb, za, -1), e(Rb + f, zm, -1), e(Rb + f, zm, 1), e(Rb, za, 1)]
                hi = [e(Rb + f, zm, -1), e(Rb, zb, -1), e(Rb, zb, 1), e(Rb + f, zm, 1)]
                polys.append((abs(cth), lo, hi, th))
            else:
                lo = [e(Rb, za, -1), e(Rb, zb, -1), e(Rb, zb, 1), e(Rb, za, 1)]
                polys.append((abs(cth), lo, None, th))
        # draw sorted by |cos| ascending (edge ones first)
        for c_, lo, hi, th in sorted(polys, key=lambda t: t[0]):
            base = LEMON if front else LEMON_D
            sh = (0.80 + 0.2 * c_) if front else 0.72
            col_lo = shade_col(base, sh * 0.93); col_hi = shade_col(base, sh * 1.03)
            d.add(f'<polygon points="{pts(lo)}" fill="{col_lo}" class="edge"/>')
            if hi: d.add(f'<polygon points="{pts(hi)}" fill="{col_hi}" class="edge"/>')
    # row A (upper) offset 0.5, row B (lower) offset 0
    ribbons(0.5, zrA[0], zrA[1], False); ribbons(0.0, zrB[0], zrB[1], False)
    # front bands
    for (z0, z1) in (zf0 and (0, 0) or (zf0, zf1), zb3, zb2, zb1):
        band(z0, z1, front=True)
    ribbons(0.5, zrA[0], zrA[1], True); ribbons(0.0, zrB[0], zrB[1], True)
    # belt front
    band(zbelt[0], zbelt[1], front=True)
    # top rim ellipse
    d.add(f'<polygon points="{pts(top_ellipse)}" fill="#efdc85" class="edge"/>')
    front_rim = [proj(Rb, -math.pi / 2 + math.pi * i / 60, Htot, ox, oy, s) for i in range(61)]
    d.add(f'<polyline points="{pts(front_rim)}" fill="none" class="edge"/>')
    # text on belt
    sz = 8.0
    def glyphs(txt, centre_phi, zbase, size, w=600):
        total = tw(txt, size, w)
        s0 = -total / 2
        for ch in txt:
            cw = tw(ch, size, w)
            sc = s0 + cw / 2
            phi = centre_phi + sc / Rb
            if math.cos(phi) <= 0.05:
                s0 += cw; continue
            X, Yy = Rb * math.sin(phi), -Rb * math.cos(phi)
            px = ox + s * X
            py = oy - s * (zbase * math.cos(ALPHA) + Yy * math.sin(ALPHA))
            a = math.cos(phi) * s; b = -math.sin(phi) * math.sin(ALPHA) * s
            dd = math.cos(ALPHA) * s
            d.add(f'<text transform="matrix({f2(a)} {f2(b)} 0 {f2(dd)} {f2(px)} {f2(py)})" font-size="{f2(size)}" font-weight="{w}" fill="{INK}" text-anchor="middle">{ch}</text>')
            s0 += cw
    if name:
        zt = zbelt[1]
        glyphs("Sophia", 0.0, zt - 8.4, sz)
        glyphs("Zhuravkova", 0.0, zt - 8.4 - 9.6, sz)
    return Htot

def plan(d, cx, cy, s, f):
    Rm = Rb + f
    d.circle(cx, cy, s * Rb, "thin", "none", extra='stroke-dasharray="1 1"')
    gap = (2 * math.pi * Rm - N * p) / N
    for row, off, dash in ((0, 0.5, ""), (1, 0.0, 'stroke-dasharray="1.6 .8"')):
        for k in range(N):
            th = (k + off) * 2 * math.pi / N
            for sgn in (-1,):
                pass
            x0 = cx + s * (Rm * math.sin(th) - p / 2 * math.cos(th)); y0 = cy - s * (Rm * math.cos(th) + p / 2 * math.sin(th))
            x1 = cx + s * (Rm * math.sin(th) + p / 2 * math.cos(th)); y1 = cy - s * (Rm * math.cos(th) - p / 2 * math.sin(th))
            d.add(f'<line x1="{f2(x0)}" y1="{f2(y0)}" x2="{f2(x1)}" y2="{f2(y1)}" stroke="{INK if row==0 else MTN}" stroke-width="{0.5 if row==0 else 0.35}" {dash}/>')
    return gap

def assembled():
    W, Hh = 360, 250
    d = Doc(0, 0, W, Hh, scale=4.6)
    d.title(10, 13, "02  LANTERN LATTICE — assembled", "As shipped (ring closed, ribbons straight) and pressed (ribbons kinked at the crease, bulging 5 mm). Three-quarter view from 21 deg above, and plan.")
    s = 1.55
    ground = 205
    for ox in (68, 178):
        d.add(f'<ellipse cx="{ox}" cy="{ground}" rx="{(Rb+ (F if ox>100 else 0))*s*1.06}" ry="{(Rb+(F if ox>100 else 0))*s*math.sin(ALPHA)*1.06}" fill="#000" opacity=".12"/>')
    lantern(d, 68, ground, s, 0.0)
    lantern(d, 178, ground, s, F)
    d.note(68, ground + 22, f"as shipped: {H:.0f} mm tall, {2*Rb:.0f} mm dia", 2.8, INK, "middle")
    d.note(178, ground + 22, f"pressed: {Hc:.1f} mm tall, {2*(Rb+F):.0f} mm dia at the bulge", 2.8, INK, "middle")
    gap = plan(d, 290, 80, 1.15, F)
    d.note(290, 80 + (Rb + F) * 1.15 + 8, "plan at the bulge", 2.8, INK, "middle")
    d.note(290, 80 + (Rb + F) * 1.15 + 12.5, f"gaps {gap:.1f} mm; row A black, row B red", 2.4, GREY, "middle")
    d.notes(250, 160, [
        "On the table:",
        "- belt: NAME front and back;",
        "  'Dinner / date' on one side,",
        "  event line on the other",
        "- 2 rows x 16 ribbons, offset",
        "  half a pitch (brick lattice)",
        "- LED tealight optional",
    ], 2.7, 1.5, INK)
    d.save("c2_assembled.svg")

if __name__ == "__main__":
    verify(); dieline(); assembled()
