import math
from lib import *

CWID, CLEN = 124.0, 88.0
FX0, FX1 = 12.0, 112.0      # flag x-extent (100 wide)
HY, FL = 20.0, 50.0         # hinge y, flag length
A_, LEG = 15.0, 30.0        # leg hinge distance on flag, leg length
PHI_F = math.radians(78)    # final flag angle
FONT = 15.5

def yfoot(phi):
    return HY + A_ * math.cos(phi) + math.sqrt(LEG ** 2 - (A_ * math.sin(phi)) ** 2)

def verify():
    o = ["C5 FLAG-UP (napkin-triggered pull-flag) mechanism check (mm)"]
    y0 = yfoot(0.0); y1 = yfoot(PHI_F)
    o.append(f"card {CWID:.0f} x {CLEN:.0f}; flag {FX1-FX0:.0f} x {FL:.0f} hinged at y = {HY:.0f}; leg hinge a = {A_}, leg l = {LEG}")
    o.append(f"foot start y_f(0) = {HY}+{A_}+{LEG} = {y0:.1f}  (< flag tip {HY+FL:.0f}, so the folded leg lies under the flag)")
    o.append("phi(deg)  foot y   stroke   P(y,z)            leg angle   flag tip height")
    for deg in (0, 10, 20, 30, 40, 50, 60, 70, 78, 85, 90):
        ph = math.radians(deg)
        yf = yfoot(ph)
        P = (HY + A_ * math.cos(ph), A_ * math.sin(ph))
        leg_ang = math.degrees(math.atan2(P[1], yf - P[0]))
        tip = FL * math.sin(ph)
        o.append(f"{deg:5d}   {yf:7.2f}  {y0-yf:6.2f}   ({P[0]:5.1f},{P[1]:5.1f})    {leg_ang:5.1f}      {tip:5.1f}")
    s_f = y0 - y1
    o.append(f"final stroke to phi = 78 deg: {s_f:.2f} mm (guest pulls the tail ~16 mm)")
    d_sh = y1 - 20.0
    o.append(f"stop: slider shoulder (16 wide) sits {d_sh:.1f} mm from the foot fold and meets the 12.6 mm channel mouth at y = 20 exactly when phi = 78 deg: {y1:.2f} - {d_sh:.2f} = 20")
    # beyond-stop
    ph = math.radians(90); o.append(f"without the stop the flag would run on to phi = 90 deg at stroke {y0 - yfoot(ph):.1f} mm and then fall toward the guest -> stop is mandatory")
    # forces (estimates)
    m_flag = 100 * 50 * 0.35e-3 * 1.0 / 100  # g (area cm2 * 0.035 g/cm2)
    area_cm2 = 100 * 50 / 100
    m = area_cm2 * 0.035
    o.append(f"flag mass = {area_cm2:.0f} cm2 x 0.035 g/cm2 = {m:.1f} g -> weight {m*9.81e-3*1000:.1f} mN, gravity torque at phi=0 : {m*9.81e-3*(FL/2):.2f} N.mm")
    Mc = 1.6
    ph = PHI_F
    P = (HY + A_ * math.cos(ph), A_ * math.sin(ph)); F = (yfoot(ph), 0)
    ux, uz = F[0] - P[0], F[1] - P[1]; L = math.hypot(ux, uz)
    fl = (math.cos(ph), math.sin(ph))
    cosang = (ux * fl[0] + uz * fl[1]) / L
    o.append(f"hold at 78 deg: crease spring-back est. M = {Mc} N.mm (350 g board, 0.4 caliper, scored) -> leg force {Mc/(A_*math.sqrt(1-cosang**2)):.2f} N ; friction alone unreliable -> latch tongue (>= 2 N) required")
    o.append("estimates (to confirm on a hand prototype): pull to erect 0.1-0.3 N; tear of the 8 mm tail perforation 1.0-1.5 N; latch holds > 2 N, so the sequence is erect -> latch -> tear -> napkin free")
    o.append(f"tail: slider reaches the edge (y=0) from F (y={y0:.0f}); outside the card 20 mm to the perforation, then 60 mm of tail to the napkin slot. Napkin travel needed = {s_f:.0f} mm")
    o.append(f"flag text: 'Zhuravkova' {tw('Zhuravkova', FONT, 600):.1f} mm at {FONT} mm in a {FX1-FX0:.0f} wide flag -> margin {(FX1-FX0-tw('Zhuravkova', FONT, 600))/2:.1f}; two lines leading 16.5, block centred on the flag")
    o.append("laminate: A 350 g (0.40) + C 900 um spacer (leg + slider doubled = 0.8) + B 350 g (0.40) = 1.7 mm card")
    o.append(f"A, B, C: {CWID:.0f} x {CLEN:.0f}; SRA3: {int(320//CWID)} x {int(450//CLEN)} = {int(320//CWID)*int(450//CLEN)} each of A, B, C -> 40 guests need {math.ceil(40/ (int(320//CWID)*int(450//CLEN)))} sheets per layer")
    open("c5_verify.txt", "w").write("\n".join(o) + "\n")
    print("\n".join(o))

def flagtext(d, x, y_of, anchor_y, sz=FONT):
    pass

def dieline():
    W, H = 420, 300
    d = Doc(0, 0, W, H, scale=4.0)
    d.title(10, 13, "05  FLAG UP — napkin-triggered pull-tab pop-up",
            "Dieline 1:1 (mm), guest edge at the bottom of every part. 4 parts: A top card, C spacer, B base, D leg-and-slider strip. Lemon board, black print.")
    def Y(oy, y): return oy + CLEN - y
    gap = 10
    ox = [10, 10 + CWID + gap, 10 + 2 * (CWID + gap)]
    oy = 30
    # ---- A ----
    x0 = ox[0]
    d.rect(x0, oy, CWID, CLEN, "cut", LEMON, rx=2)
    # U-cut: left, top, right; hinge crease along y = HY
    d.line(x0 + FX0, Y(oy, HY), x0 + FX0, Y(oy, HY + FL), "cut")
    d.line(x0 + FX1, Y(oy, HY), x0 + FX1, Y(oy, HY + FL), "cut")
    d.line(x0 + FX0, Y(oy, HY + FL), x0 + FX1, Y(oy, HY + FL), "cut")
    d.line(x0 + FX0, Y(oy, HY), x0 + FX1, Y(oy, HY), "val")
    # flag print : two lines centred
    cx = x0 + CWID / 2
    mid = HY + FL / 2
    d.text(cx, Y(oy, mid + 2.5 + 3.0), "Sophia", FONT, 600, INK, "middle")
    d.text(cx, Y(oy, mid + 2.5 + 3.0 - 16.5), "Zhuravkova", FONT, 600, INK, "middle")
    # latch window in lip
    d.rect(cx - 1.5, Y(oy, 11), 3, 3, "cut", "#ffffff")
    d.note(cx + 3, Y(oy, 9), "latch window 3 x 3", 2.2, GREY)
    # channel slit mark: slider is under the lip. show tail exit
    d.note(x0, oy - 3, "A  top card, 350 g  (flag is cut out of it)", 2.8, INK, weight=600)
    d.note(x0 + 2, Y(oy, 5), "guest edge", 2.2, GREY)
    d.note(x0 + CWID / 2, Y(oy, HY + FL + 5), "far edge", 2.2, GREY, "middle")
    d.note(x0 + FX0 + 1, Y(oy, HY) - 1.5, "hinge crease, valley, y = 20", 2.2, VAL)
    # glue zone border
    d.rect(x0 + 2.5, oy + 2.5, CWID - 5, CLEN - 5, "thin", "none", extra='stroke-dasharray=".8 1"')
    # reverse of the flag (printer's back plate, viewed from behind: mirrored in x only)
    rx0, ry0 = ox[0] + 8, oy + CLEN + 3.5
    d.note(ox[0], ry0 + 2.5, "A reverse (flag back, read by the person opposite):", 2.4, GREY)
    d.rect(rx0 + 2, ry0 + 5, 100, 28, "thin", LEMON)
    d.text(rx0 + 2 + 50, ry0 + 5 + 14.5, "Dinner", 15, 700, INK, "middle")
    d.text(rx0 + 2 + 50, ry0 + 5 + 21.5, "Colorblock × DNA Kitchen · Moscow · 10.10.2026", 3.0, 500, INK, "middle")
    # ---- C ----
    x0 = ox[1]
    d.rect(x0, oy, CWID, CLEN, "cut", LEMON, rx=2)
    # cutout: window area (flag + 2 margin) and channel to the edge
    d.rect(x0 + FX0 - 0.0, Y(oy, HY + FL + 0.0), FX1 - FX0, FL, "cut", "#ffffff")
    d.rect(x0 + CWID / 2 - 6.3, Y(oy, HY), 12.6, HY, "cut", "#ffffff")
    d.note(x0, oy - 3, "C  spacer, 0.9 mm board  (window + 12.6 mm channel)", 2.8, INK, weight=600)
    d.note(x0 + CWID / 2 + 8, Y(oy, 10), "channel 12.6 wide", 2.2, GREY)
    d.note(x0 + CWID / 2, Y(oy, HY + FL / 2), "window = flag 100 x 50", 2.4, GREY, "middle")
    d.note(x0 + CWID / 2, Y(oy, HY + FL / 2) + 3.5, "(shoulder stop = this edge, y = 20)", 2.4, GREY, "middle")
    d.rect(x0 + 2.5, oy + 2.5, CWID - 5, CLEN - 5, "thin", "none", extra='stroke-dasharray=".8 1"')
    # ---- B ----
    x0 = ox[2]
    d.rect(x0, oy, CWID, CLEN, "cut", LEMON, rx=2)
    d.note(x0, oy - 3, "B  base, 350 g  (solid black pit under the flag)", 2.8, INK, weight=600)
    d.rect(x0 + FX0, Y(oy, HY + FL), FX1 - FX0, FL, "thin", "none", extra='stroke-dasharray="1 1"')
    d.rect(x0 + FX0 - 1, Y(oy, HY + FL + 1), FX1 - FX0 + 2, FL + 2, "thin", INK)
    d.note(x0 + CWID / 2, Y(oy, HY + FL / 2) - 1, "solid black pit (bleeds 1 mm under C)", 2.6, "#ffffff", "middle")
    d.note(x0 + CWID / 2, Y(oy, HY + FL / 2) + 3, "the leg and the slider are lemon on black", 2.4, "#cfcfcf", "middle")
    d.rect(x0 + CWID / 2 - 6.3, Y(oy, HY), 12.6, HY, "thin", "none", extra='stroke-dasharray="1 1"')
    d.rect(x0 + 2.5, oy + 2.5, CWID - 5, CLEN - 5, "thin", "none", extra='stroke-dasharray=".8 1"')
    # ---- D ----
    dy = oy + CLEN + 50
    dx = 10
    # strip along x: from tail end (left) ... drawn horizontally; positions measured along strip from the tab end
    segs = [("tab (glued to flag back)", 8, None), ("leg", LEG, None), ("slider (to the edge of the card)", 65.0, None), ("outside the card", 20, None), ("tail", 60, None)]
    total = sum(s[1] for s in segs)
    kx = 1.9
    d.note(dx, dy - 8, "D  leg + slider strip, 12 wide, 350 g, one piece, doubled at the foot fold", 2.8, INK, weight=600)
    xcur = dx
    for name, ln, _ in segs:
        d.rect(xcur, dy, ln * kx * 0.0 + ln * kx / kx, 12, "cut", LEMON)
        xcur += ln
    # real scale: 1 unit = 1 mm already (ln mm). place creases
    d.line(dx + 8, dy, dx + 8, dy + 12, "val")           # P hinge
    d.line(dx + 8 + LEG, dy, dx + 8 + LEG, dy + 12, "mtn")  # foot U fold (mountain+return)
    d.note(dx + 8, dy + 15.5, "P hinge", 2.2, VAL, "middle")
    d.note(dx + 8 + LEG, dy + 15.5, "F fold 180 deg", 2.2, MTN, "middle")
    # shoulder (16 wide) at distance 29.3 from foot, on the slider
    sh0 = dx + 8 + LEG + 29.3
    d.rect(sh0, dy - 2, 6, 16, "cut", LEMON)
    d.note(sh0 + 3, dy - 3.5, "shoulder 16 x 6", 2.2, GREY, "middle")
    # latch tongue
    lt0 = dx + 8 + LEG + 41.3 - 0
    d.path(f"M{lt0},{dy+4.5} L{lt0+5},{dy+4.5} L{lt0+5},{dy+7.5} L{lt0},{dy+7.5}", "cut")
    d.note(lt0 + 2, dy + 19, "latch tongue 5 x 3, bent up 0.5", 2.2, GREY, "middle")
    # perforation
    px = dx + 8 + LEG + 65.0 + 20
    for k in range(6):
        d.line(px, dy + 1 + 2 * k, px, dy + 2 + 2 * k, "cut")
    d.note(px, dy + 15.5, "perforation (tear 1-1.5 N)", 2.2, GREY, "middle")
    # napkin slot at tail
    sx = dx + total - 14
    d.rect(sx, dy + 4.5, 10, 3, "cut", "#ffffff")
    d.note(sx + 5, dy + 15.5, "napkin slot 10 x 3", 2.2, GREY, "middle")
    d.note(dx, dy + 24, f"length {total:.0f} mm, drawn 1:1 (strip is folded back at F, so the doubled part is 30 mm long, slider is 65 + 20 + 60 beyond it)", 2.4, GREY)
    # assembly notes
    d.notes(10, dy + 31, [
        "BUILD ORDER",
        "1  Cut A, B, C, D. Print B (pit) and A (flag) black. Score A hinge y = 20 (valley, from the print side), D at P and F.",
        "2  Glue D's tab to the BACK of the flag at y = 27..35 (P hinge on y = 35 -> 15 mm from the card hinge). Flag lies flat, window closed.",
        "3  Fold D back 180 deg at F; drop the doubled leg + slider into the channel of C, shoulder inside the window zone, tail out the guest edge.",
        "4  Glue A + C + B at the 2.5 mm borders (A to C, C to B). Tongue on D must line up with the latch window in A when the stroke is complete.",
        "5  Table: thread the napkin's rolled corner through the 10 x 3 slot in the tail. Lift the napkin toward the lap: the flag stands, the latch clicks, the perforation tears.",
    ], 2.7, 1.5, INK)
    d.legend(230, dy + 55, [("cut", "cut"), ("val", "valley crease"), ("mtn", "mountain crease"), ("thin", "glue border 2.5 / 10 x 3 slot")])
    d.save("c5_dieline.svg")

def proj(Xc, Y, Z, ox, oy, s, alpha):
    return (ox + s * Xc, oy - s * (Z * math.cos(alpha) + Y * math.sin(alpha)))

def assembled():
    W, H = 420, 270
    d = Doc(0, 0, W, H, scale=4.0)
    d.title(10, 13, "05  FLAG UP — assembled", "Side sections at three flag angles (true scale, layers 3x thick; guest and napkin on the left), then the standing card from the guest's side and from across the table.")
    s = 0.95
    def section(ox, oy, deg, label):
        ph = math.radians(deg)
        yf = yfoot(ph); stroke = yfoot(0) - yf
        X = lambda y: ox + s * y
        Z = lambda z: oy - s * z
        k = 3.0
        d.line(X(-120), Z(-1.7), X(CLEN + 4), Z(-1.7), "thin")
        def layer(y0, y1, z0, z1, fill):
            d.add(f'<rect x="{f2(X(y0))}" y="{f2(Z(z1*k))}" width="{f2(s*(y1-y0))}" height="{f2(s*(z1-z0)*k)}" fill="{fill}" stroke="#6d5a10" stroke-width=".2"/>')
        layer(0, CLEN, -1.7, -1.3, "#222222")
        layer(0, HY, -1.3, -0.4, LEMON_DD); layer(HY + FL, CLEN, -1.3, -0.4, LEMON_DD)
        layer(0, HY, -0.4, 0.0, LEMON); layer(HY + FL, CLEN, -0.4, 0.0, LEMON)
        tip = (HY + FL * math.cos(ph), FL * math.sin(ph))
        d.add(f'<line x1="{f2(X(HY))}" y1="{f2(Z(-0.2*k))}" x2="{f2(X(tip[0]))}" y2="{f2(Z(tip[1]-0.2*k))}" stroke="#6d5a10" stroke-width="{f2(0.4*k*s)}"/>')
        d.add(f'<line x1="{f2(X(HY))}" y1="{f2(Z(-0.2*k))}" x2="{f2(X(tip[0]))}" y2="{f2(Z(tip[1]-0.2*k))}" stroke="{LEMON}" stroke-width="{f2(0.4*k*s*0.6)}"/>')
        P = (HY + A_ * math.cos(ph), A_ * math.sin(ph) - 0.4 * k)
        F = (yf, -0.9 * k)
        end = -80 - stroke
        d.add(f'<line x1="{f2(X(P[0]))}" y1="{f2(Z(P[1]))}" x2="{f2(X(F[0]))}" y2="{f2(Z(F[1]))}" stroke="{INK}" stroke-width=".9"/>')
        d.add(f'<line x1="{f2(X(F[0]))}" y1="{f2(Z(F[1]))}" x2="{f2(X(end))}" y2="{f2(Z(F[1]))}" stroke="{INK}" stroke-width=".9"/>')
        d.circle(X(F[0]), Z(F[1]), 1.1, "ink", "#fff"); d.circle(X(P[0]), Z(P[1]), 1.1, "ink", "#fff")
        # napkin pack moves with the tail
        nx0 = -120 - stroke
        d.add(f'<rect x="{f2(X(nx0))}" y="{f2(Z(10))}" width="{f2(s*58)}" height="{f2(s*12)}" rx="3" fill="#f4f1ea" stroke="#9c9688" stroke-width=".3"/>')
        d.note(X(nx0 + 29), Z(4.8), "napkin", 2.4, GREY, "middle")
        d.add(f'<line x1="{f2(X(end))}" y1="{f2(Z(F[1]))}" x2="{f2(X(end))}" y2="{f2(Z(9))}" stroke="{INK}" stroke-width=".5" stroke-dasharray="1 .8"/>')
        d.note(X(-18), Z(-9), "guest edge", 2.2, GREY, "middle")
        d.note(ox - 118 * s, oy + 14, label, 2.8, INK, weight=600)
        d.note(ox - 118 * s, oy + 18.5, f"foot y = {yf:.1f}, stroke {stroke:.1f} mm, flag tip {FL*math.sin(ph):.0f} mm high", 2.4, GREY)
    for i, (deg, lab) in enumerate(((0, "1  flat, napkin folded beside it"), (45, "2  napkin drawn 6 mm toward the lap"), (78, "3  stroke 15.7 mm: flag at 78 deg, latch clicks"))):
        section(142, 80 + i * 66, deg, lab)
    # 3/4 view
    alpha = math.radians(26)
    ox, oy = 322, 150
    s2 = 0.95
    def P3(X_, Y_, Z_): return proj(X_, Y_, Z_, ox, oy, s2, alpha)
    plate = [P3(-CWID/2, 0, 0), P3(CWID/2, 0, 0), P3(CWID/2, CLEN, 0), P3(-CWID/2, CLEN, 0)]
    d.add(f'<polygon points="{pts([(x+1.5,y+2.4) for x,y in plate])}" fill="#000" opacity=".14"/>')
    d.add(f'<polygon points="{pts(plate)}" fill="{LEMON}" class="edge"/>')
    d.add(f'<polygon points="{pts([P3(-CWID/2,0,0), P3(CWID/2,0,0), P3(CWID/2,0,-1.7), P3(-CWID/2,0,-1.7)])}" fill="{LEMON_D}" class="edge"/>')
    win = [P3(-50, HY, 0), P3(50, HY, 0), P3(50, HY + FL, 0), P3(-50, HY + FL, 0)]
    d.add(f'<polygon points="{pts(win)}" fill="#161616" class="edge"/>')
    ph = PHI_F
    Pp = (0, HY + A_ * math.cos(ph), A_ * math.sin(ph)); Ff = (0, yfoot(ph), 0.0)
    legq = [P3(-6, Pp[1], Pp[2]), P3(6, Pp[1], Pp[2]), P3(6, Ff[1], Ff[2]), P3(-6, Ff[1], Ff[2])]
    d.add(f'<polygon points="{pts(legq)}" fill="{LEMON_D}" class="edge"/>')
    tip = (HY + FL * math.cos(ph), FL * math.sin(ph))
    flag = [P3(-50, HY, 0), P3(50, HY, 0), P3(50, tip[0], tip[1]), P3(-50, tip[0], tip[1])]
    d.add(f'<polygon points="{pts([(x+1.2,y+1.5) for x,y in flag])}" fill="#000" opacity=".12"/>')
    d.add(f'<polygon points="{pts(flag)}" fill="{LEMON}" class="edge"/>')
    sc = math.sin(ph + alpha)
    mid = FL / 2
    for txt, tpos in (("Sophia", mid + 2.5 + 3.0), ("Zhuravkova", mid + 2.5 + 3.0 - 16.5)):
        Yt, Zt = HY + tpos * math.cos(ph), tpos * math.sin(ph)
        x, y = P3(0, Yt, Zt)
        d.add(f'<g transform="translate({f2(x)} {f2(y)}) scale({s2} {f2(s2*sc)})"><text x="0" y="0" font-size="{FONT}" font-weight="600" fill="{INK}" text-anchor="middle">{txt}</text></g>')
    d.add(f'<path d="M{P3(0,0,0)[0]},{P3(0,0,0)[1]} L{P3(0,-16,0)[0]},{P3(0,-16,0)[1]}" stroke="{INK}" stroke-width="2.6" fill="none"/>')
    d.add(f'<path d="M{P3(0,0,0)[0]},{P3(0,0,0)[1]} L{P3(0,-16,0)[0]},{P3(0,-16,0)[1]}" stroke="{LEMON}" stroke-width="1.8" fill="none"/>')
    d.note(ox, oy + 36, "standing card, from the guest's seat", 2.8, INK, "middle")
    d.note(ox, oy + 40.5, "black pit where the flag was; lemon leg", 2.4, GREY, "middle")
    # from across the table: flag back
    bx, by = 322, 238
    d.add(f'<rect x="{bx-47}" y="{by-47}" width="94" height="46" fill="{LEMON}" class="edge"/>')
    d.text(bx, by - 22, "Dinner", 15, 700, INK, "middle")
    d.text(bx, by - 11, "Colorblock × DNA Kitchen · Moscow · 10.10.2026", 2.9, 500, INK, "middle")
    d.note(bx, by + 7, "same flag from across the table", 2.6, INK, "middle")
    d.save("c5_assembled.svg")

if __name__ == "__main__":
    verify(); dieline(); assembled()
