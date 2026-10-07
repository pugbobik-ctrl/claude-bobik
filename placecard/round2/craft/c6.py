import math, io, base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from lib import *

A_W, ALPHA, BETA = 9.0, math.radians(18), math.radians(70)
B_W = A_W * math.sin(ALPHA) / math.sin(BETA)
PITCH = A_W * math.cos(ALPHA) + B_W * math.cos(BETA)
N = 13
STRIP_H = 34.0
TAB = 8.0
PPM = 24  # raster px per mm for the print file simulation

def apparent_A(theta): return A_W * math.cos(ALPHA + theta)
def apparent_B(theta): return B_W * math.cos(BETA - theta)

def facets():
    """list of (x0,z0,x1,z1,kind,k,u0,u1) ; u = developed length along the sheet from first A"""
    out = []; x = z = 0.0; u = 0.0
    for k in range(N):
        x1 = x + A_W * math.cos(ALPHA); z1 = z + A_W * math.sin(ALPHA)
        out.append((x, z, x1, z1, "A", k, u, u + A_W)); x, z, u = x1, z1, u + A_W
        x1 = x + B_W * math.cos(BETA); z1 = z - B_W * math.sin(BETA)
        out.append((x, z, x1, z1, "B", k, u, u + B_W)); x, z, u = x1, z1, u + B_W
    return out

def image_A():
    """name image: apparent width N*A_W*cos(ALPHA) at theta=0, height STRIP_H"""
    Wmm = N * A_W * math.cos(ALPHA)
    im = Image.new("L", (int(Wmm * PPM), int(STRIP_H * PPM)), 0)
    dr = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONTDIR + "WixMadeforText-600.ttf", int(12.0 * PPM))
    w = tw(NAME, 12.0, 600)
    dr.text(((Wmm - w) / 2 * PPM, 22.8 * PPM), NAME, font=f, fill=255, anchor="ls")
    return im, Wmm

def image_B():
    Wmm = N * B_W
    im = Image.new("L", (int(Wmm * PPM), int(STRIP_H * PPM)), 0)
    dr = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONTDIR + "WixMadeforText-700.ttf", int(11.0 * PPM))
    f2_ = ImageFont.truetype(FONTDIR + "WixMadeforText-500.ttf", int(4.4 * PPM))
    w = tw("Dinner", 11.0, 700)
    dr.text(((Wmm - w) / 2 * PPM, 10.5 * PPM), "Dinner", font=f, fill=255, anchor="ls")
    w2 = tw("10.10.2026", 4.4, 500)
    dr.text(((Wmm - w2) / 2 * PPM, 31.2 * PPM), "10.10.2026", font=f2_, fill=255, anchor="ls")
    return im, Wmm

def flat_print():
    """interleaved strips as one raster: width N*(A_W+B_W) mm"""
    ia, wa = image_A(); ib, wb = image_B()
    tot = N * (A_W + B_W)
    W = int(round(tot * PPM)); H = int(STRIP_H * PPM)
    im = Image.new("L", (W, H), 0)
    uA = A_W * math.cos(ALPHA)   # apparent width of one A slice
    for k in range(N):
        xs = k * (A_W + B_W)
        sl = ia.crop((int(round(k * uA * PPM)), 0, int(round((k + 1) * uA * PPM)), H)).resize((int(round(A_W * PPM)), H), Image.LANCZOS)
        im.paste(sl, (int(round(xs * PPM)), 0))
        sl2 = ib.crop((int(round(k * B_W * PPM)), 0, int(round((k + 1) * B_W * PPM)), H))
        im.paste(sl2, (int(round((xs + A_W) * PPM)), 0))
    return im

def view(theta_deg, flat):
    th = math.radians(theta_deg)
    F = facets()
    v = (math.sin(th), math.cos(th))
    # screen coordinate s = x cos th - z sin th ; depth d = x sin th + z cos th
    def sc(x, z): return x * math.cos(th) - z * math.sin(th)
    def dp(x, z): return x * math.sin(th) + z * math.cos(th)
    smin = min(min(sc(f[0], f[1]), sc(f[2], f[3])) for f in F); smax = max(max(sc(f[0], f[1]), sc(f[2], f[3])) for f in F)
    ds = 0.04
    S = np.arange(smin, smax, ds)
    cols = np.zeros((len(S),), dtype=int) - 1
    shade = np.ones(len(S))
    best = np.full(len(S), -1e9)
    sheetx = np.zeros(len(S))
    for (x0, z0, x1, z1, kind, k, u0, u1) in F:
        psi = ALPHA if kind == "A" else -BETA
        n = (-math.sin(psi), math.cos(psi))
        dot = n[0] * v[0] + n[1] * v[1]
        if dot <= 1e-9: continue
        sa, sb = sc(x0, z0), sc(x1, z1)
        lo, hi = min(sa, sb), max(sa, sb)
        idx = np.where((S >= lo) & (S <= hi))[0]
        if len(idx) == 0: continue
        t = (S[idx] - sa) / (sb - sa)
        d_ = dp(x0, z0) + t * (dp(x1, z1) - dp(x0, z0))
        better = d_ > best[idx]
        sel = idx[better]
        best[sel] = d_[better]
        sheetx[sel] = (k * (A_W + B_W) + (0 if kind == "A" else A_W)) + t[better] * (A_W if kind == "A" else B_W)
        shade[sel] = 0.80 + 0.20 * dot
        cols[sel] = 1
    W = int(len(S) * ds * PPM); Hh = flat.size[1]
    fl = np.array(flat).astype(float) / 255
    out = np.ones((Hh, W, 3))
    lemon = np.array([0xfe, 0xed, 0x95]) / 255
    for i in range(W):
        sidx = min(len(S) - 1, int(i / PPM / ds))
        if cols[sidx] < 0:
            out[:, i, :] = np.array([0.30, 0.28, 0.20])  # see-through gap (dark behind): shouldn't happen for a closed profile
            continue
        xi = min(fl.shape[1] - 1, int(sheetx[sidx] * PPM))
        ink = fl[:, xi]
        out[:, i, :] = (lemon[None, :] * shade[sidx]) * (1 - ink[:, None]) + 0.07 * ink[:, None]
    return out, (smax - smin), cols, sheetx, S

def contrast_text_visible(theta_deg):
    th = math.radians(theta_deg)
    A = max(0.0, apparent_A(th)) if math.cos(ALPHA + th) > 0 else 0
    Bv = apparent_B(th) if math.cos(BETA - th) > 0 else 0
    # B facet visible only if its normal faces viewer: normal angle: BETA from plane -> dot = cos(BETA - th) > 0 handled
    return A, Bv

def verify():
    o = ["C6 WALK-BY (agamograph pleat) geometry check",
         f"A facet {A_W} mm at +{math.degrees(ALPHA):.0f} deg, B facet at -{math.degrees(BETA):.0f} deg; planarity needs a sin(alpha) = b sin(beta) -> b = {B_W:.3f}",
         f"closure check: a sin a - b sin b = {A_W*math.sin(ALPHA) - B_W*math.sin(BETA):.2e} (zero = the strip returns to its baseline)",
         f"tooth pitch p = a cos a + b cos b = {A_W*math.cos(ALPHA):.3f} + {B_W*math.cos(BETA):.3f} = {PITCH:.3f}; {N} teeth -> panel {N*PITCH:.1f} mm wide; tooth depth {A_W*math.sin(ALPHA):.2f} mm",
         f"developed length per tooth {A_W + B_W:.2f}; strip {N*(A_W+B_W):.1f} + 2 x {TAB} tabs = {N*(A_W+B_W)+2*TAB:.1f} x {STRIP_H:.0f}",
         f"name image: Wix Madefor SemiBold 12 mm, '{NAME}' = {tw(NAME,12.0,600):.1f} mm in {N*A_W*math.cos(ALPHA):.1f} (apparent width at 0 deg); margin {(N*A_W*math.cos(ALPHA)-tw(NAME,12.0,600))/2:.1f}",
         f"B image: 'Dinner' 11 mm Bold = {tw('Dinner',11.0,700):.1f} mm in {N*B_W:.1f} (apparent width at {math.degrees(BETA):.0f} deg)",
         "",
         "what each viewing azimuth sees (theta from the card normal, + toward the side the B facets face):",
         " theta   A strip   B strip   B share   A share   verdict"]
    for t in (-40, -30, -18, -10, 0, 10, 20, 30, 40, 50, 60, 65, 70, 75, 80):
        th = math.radians(t)
        A = apparent_A(th) if math.cos(ALPHA + th) > 0 else 0
        Bv = apparent_B(th) if math.cos(BETA - th) > 0 else 0
        tot = A + Bv
        bs = Bv / tot if tot else 0; as_ = A / tot if tot else 0
        verdict = "NAME clean" if bs <= 0.12 else ("name readable, striped" if bs <= 0.25 else ("mixed - gibberish" if as_ > 0.25 else ("DINNER readable" if as_ > 0.10 else "DINNER clean")))
        o.append(f" {t:5d}   {A:7.2f}   {Bv:7.2f}   {100*bs:6.1f}%   {100*as_:6.1f}%   {verdict}")
    # thresholds
    th = np.radians(np.arange(-80, 90, 0.1))
    def bs_(t):
        A = A_W * math.cos(ALPHA + t) if math.cos(ALPHA + t) > 0 else 0
        Bv = B_W * math.cos(BETA - t) if math.cos(BETA - t) > 0 else 0
        return Bv / (A + Bv)
    t_name = max(t for t in th if bs_(t) <= 0.12); t_din = min(t for t in th if bs_(t) >= 0.90)
    o.append(f"name stays clean (B share <= 12 %) up to theta = {math.degrees(t_name):.0f} deg; 'Dinner' clean (A share <= 10 %) from theta = {math.degrees(t_din):.0f} deg")
    # walking geometry
    dist = 0.9
    o.append(f"walker passing the seat at lateral distance {dist} m sees the card at theta = atan(x/{dist}): x = 1.0 m -> {math.degrees(math.atan(1.0/dist)):.0f} deg, 2.0 m -> {math.degrees(math.atan(2.0/dist)):.0f}, 3.0 m -> {math.degrees(math.atan(3.0/dist)):.0f}, 0.3 m -> {math.degrees(math.atan(0.3/dist)):.0f}")
    t_ok = max(t for t in th if bs_(t) <= 0.25)
    o.append(f"-> from the B side: 'Dinner' shows only on cards >= {dist*math.tan(t_din):.1f} m away along the table ({math.degrees(t_din):.0f} deg); between {dist*math.tan(math.radians(25)):.1f} and {dist*math.tan(math.radians(65)):.1f} m the card shimmers (stripes); the name is readable (B share <= 25 %) inside theta <= {math.degrees(t_ok):.0f} deg = x <= {dist*math.tan(t_ok):.2f} m, i.e. when you are at your seat or looking from the other side (B hidden, clean for theta < 0)")
    o.append("B ink is confined to the top 12 mm ('Dinner') and bottom 6 mm (date) of the 34 mm strip; the name sits in y = 14..26: at theta = 0 the B facets add lemon slivers and dashes ABOVE and BELOW the name, never through it (see c6_assembled.png)")
    o.append("placement tip: turn the tent ~15 deg so the seat is at theta = -15 (B share 2 %), where the name is cleanest")
    # tent
    panel_h, apex = 50.0, math.radians(40)
    lean = apex / 2
    depth = 2 * panel_h * math.sin(lean); height = panel_h * math.cos(lean)
    o.append(f"tent: two panels {panel_h:.0f} high, apex angle 40 deg -> each leans {math.degrees(lean):.0f} deg; footprint depth {depth:.1f}, height {height:.1f}; tip-over (centre of mass at 40 % height, rough) = atan({depth/2:.1f}/{0.4*height:.1f}) = {math.degrees(math.atan((depth/2)/(0.4*height))):.0f} deg")
    o.append(f"tooth precision: A and B strips must register to the creases within +-0.3 mm; B strip is {B_W:.2f} mm wide so a 0.3 mm crease error shifts {100*0.3/B_W:.0f} % of a B strip (print scoring marks: 4 mm crop-style ticks on both edges)")
    o.append(f"SRA3: strip {N*(A_W+B_W)+2*TAB:.0f} x {STRIP_H:.0f} -> {int(450//(N*(A_W+B_W)+2*TAB))} x {int(320//STRIP_H)} = {int(450//(N*(A_W+B_W)+2*TAB))*int(320//STRIP_H)} per sheet; tent {136} x {2*panel_h:.0f} -> {int(320//136)} x {int(450//(2*panel_h))}")
    open("c6_verify.txt", "w").write("\n".join(o) + "\n")
    print("\n".join(o))

def b64png(arr, scale_px=None):
    im = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
    if scale_px:
        im = im.resize(scale_px, Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "PNG", optimize=True)
    return base64.b64encode(b.getvalue()).decode(), im

def dieline():
    W, H = 330, 250
    d = Doc(0, 0, W, H, scale=5.0)
    d.title(10, 13, "06  WALK-BY — a pleated name that turns into 'Dinner' as you walk past",
            "Dieline 1:1 (mm). 200 g lemon: pleated strip (print file with interleaved strips) + 300 g tent card. Black print.")
    ox, oy = 14, 40
    tot = N * (A_W + B_W)
    d.note(ox, oy - 5, f"1  PLEATED STRIP  {tot + 2*TAB:.1f} x {STRIP_H:.0f}   (13 x [A {A_W} + B {B_W:.2f}], tabs {TAB})", 2.8, INK, weight=600)
    d.rect(ox, oy, tot + 2 * TAB, STRIP_H, "cut", LEMON)
    # print content, strip by strip
    ia, wa = image_A(); ib, wb = image_B()
    uA = A_W * math.cos(ALPHA)
    # vector text per strip with clipPath
    cid = 0
    for k in range(N):
        xa = ox + TAB + k * (A_W + B_W)
        cid += 1
        d.add(f'<clipPath id="a{cid}"><rect x="{f2(xa)}" y="{oy}" width="{A_W}" height="{STRIP_H}"/></clipPath>')
        # name text: apparent coordinate u -> sheet x = xa + (u - k*uA) * (A_W/uA)
        sx = A_W / uA
        wtxt = tw(NAME, 12.0, 600)
        x_img = (wa - wtxt) / 2
        d.add(f'<g clip-path="url(#a{cid})"><g transform="translate({f2(xa - k*uA*sx)} {oy}) scale({f2(sx)} 1)"><text x="{f2(x_img)}" y="22.8" font-size="12" font-weight="600" fill="{INK}">{NAME}</text></g></g>')
        xb = xa + A_W
        cid += 1
        d.add(f'<clipPath id="b{cid}"><rect x="{f2(xb)}" y="{oy}" width="{f2(B_W)}" height="{STRIP_H}"/></clipPath>')
        wD = tw("Dinner", 11.0, 700); wd2 = tw("10.10.2026", 4.4, 500)
        d.add(f'<g clip-path="url(#b{cid})"><g transform="translate({f2(xb - k*B_W)} {oy})">'
              f'<text x="{f2((wb-wD)/2)}" y="10.5" font-size="11" font-weight="700" fill="{INK}">Dinner</text>'
              f'<text x="{f2((wb-wd2)/2)}" y="31.2" font-size="4.4" font-weight="500" fill="{INK}">10.10.2026</text></g></g>')
        # creases
        d.line(xa, oy, xa, oy + STRIP_H, "val")                # B->A valley (at start of A)
        d.line(xa + A_W, oy, xa + A_W, oy + STRIP_H, "mtn")    # A->B mountain
    # tab outline and slot guides
    d.line(ox + TAB, oy, ox + TAB, oy + STRIP_H, "thin")
    d.line(ox + TAB + tot, oy, ox + TAB + tot, oy + STRIP_H, "thin")
    d.note(ox + 1, oy + STRIP_H + 4, "tab 8", 2.3, GREY)
    # dims
    d.line(ox, oy + STRIP_H + 7, ox + tot + 2 * TAB, oy + STRIP_H + 7, "dim"); d.note(ox + (tot + 2 * TAB) / 2, oy + STRIP_H + 11, f"{tot + 2*TAB:.1f}", 2.6, INK, "middle")
    # tent
    tx, ty = 190, 40
    TW, TH = 136.0, 100.0
    d.note(tx - 0, ty - 5, "2  TENT CARD  136 x 100, 300 g", 2.8, INK, weight=600)
    # drawn at 0.9 scale? keep 1:1 -> too tall for panel: fits (100)
    d.rect(tx, ty, TW, TH, "cut", LEMON)
    d.line(tx, ty + TH / 2, tx + TW, ty + TH / 2, "val")
    d.note(tx + TW / 2, ty + TH / 2 - 1.5, "valley = tent top", 2.2, VAL, "middle")
    # front panel is the lower half (guest side) : y from ty+50 to ty+100 ; strip placed 8 mm from the bottom edge
    fy0 = ty + TH / 2
    sx0 = tx + (TW - N * PITCH) / 2
    d.rect(sx0, ty + TH - 8 - STRIP_H, N * PITCH, STRIP_H, "thin", "none", extra='stroke-dasharray="1 1"')
    d.note(sx0 + N * PITCH / 2, ty + TH - 8 - STRIP_H / 2 + 0.5, f"strip sits here: {N*PITCH:.1f} wide", 2.4, GREY, "middle")
    # slots for tabs (vertical slits) at the strip's two ends, 18 high, 0.7 wide
    for xx in (sx0, sx0 + N * PITCH):
        d.line(xx, ty + TH - 8 - STRIP_H / 2 - 9, xx, ty + TH - 8 - STRIP_H / 2 + 9, "cut")
    d.note(sx0 - 1.5, ty + TH - 8 - STRIP_H / 2 - 11, "slit 18 (tab 8 x 18 passes through)", 2.2, GREY)
    d.add(f'<g transform="rotate(180 {f2(tx + TW/2)} {f2(ty + TH/4)})"><text x="{f2(tx+TW/2)}" y="{f2(ty+TH/4-1)}" font-size="11" font-weight="700" text-anchor="middle" fill="{INK}">Dinner</text><text x="{f2(tx+TW/2)}" y="{f2(ty+TH/4+7)}" font-size="2.8" font-weight="500" text-anchor="middle" fill="{INK}">Colorblock × DNA Kitchen · Moscow · 10 Oct 2026</text></g>')
    d.note(tx + TW / 2, ty + 5, "(back panel, printed upside down so it reads for the person opposite)", 2.3, GREY, "middle")
    d.note(tx + TW / 2, ty + TH + 5, "guest side is the lower half; the tent is closed by its own fold", 2.4, GREY, "middle")
    d.notes(14, 150, [
        "MAKE (4 min each)",
        "1  Print the strip file (interleaved A / B slices) and the tent. B ink is confined to the top 12 and bottom 6 mm so it never crosses the name.",
        "2  Score the 26 vertical creases from the printed side with a 0.4 mm crease rule (digital cutter crease wheel).",
        "3  Pleat on a jig (two 1 mm corrugated boards with 18 deg / 70 deg wedge slots), or by hand from the left end: valley, mountain, valley ...",
        "4  Slide the two 8 mm tabs through the slits in the tent's front panel, fold flat behind, tape.",
        "5  Teeth: A faces the seat; short steep B faces the walker (right-hand side of the seat).",
    ], 2.7, 1.5, INK)
    d.legend(190, 160, [("cut", "cut / outline"), ("val", "valley"), ("mtn", "mountain"), ("thin", "tab line / strip position")])
    d.save("c6_dieline.svg")

def assembled(imgs):
    W, H = 380, 255
    d = Doc(0, 0, W, H, scale=4.4)
    d.title(10, 13, "06  WALK-BY — assembled: what the same card shows from five viewing angles",
            "Simulated from the real print file and the real tooth profile (c6.py); theta = angle from the card's normal, positive toward the side the short B teeth face.")
    labs = [(-18, "theta -18: name, cleanest"), (0, "theta 0: seated guest - name, 10 % B slivers"), (35, "theta 35: mixed stripes"), (55, "theta 55: Dinner emerging"), (70, "theta 70: walking up the table - Dinner")]
    y = 24
    for i, (t, lab) in enumerate(labs):
        arr, wapp, *_ = imgs[t]
        wmm = wapp
        b, im = b64png(arr)
        d.add(f'<rect x="12" y="{y}" width="124" height="{STRIP_H + 6}" fill="#e9e9e9"/>')
        px = 12 + (124 - wmm) / 2
        d.add(f'<image x="{f2(px)}" y="{y+3}" width="{f2(wmm)}" height="{STRIP_H}" preserveAspectRatio="none" href="data:image/png;base64,{b}"/>')
        d.note(142, y + 12, lab, 2.9, INK, weight=600)
        A = apparent_A(math.radians(t)) if math.cos(ALPHA + math.radians(t)) > 0 else 0
        Bv = apparent_B(math.radians(t)) if math.cos(BETA - math.radians(t)) > 0 else 0
        d.note(142, y + 17, f"A strips {A:.2f} mm + B strips {Bv:.2f} mm per tooth; B share {100*Bv/(A+Bv):.0f} %", 2.5, GREY)
        d.note(142, y + 21.5, f"card appears {wmm:.0f} mm wide (true {N*PITCH:.0f})", 2.5, GREY)
        y += 40
    # plan section of the sawtooth
    gx, gy = 232, 40
    s = 3.4
    d.text(gx - 10, gy - 8, "Plan section of the pleat (x3.4): 4 teeth", 3.0, 600, INK)
    F = facets()
    pts_ = [(gx + s * F[0][0], gy + 24 - s * F[0][1])]
    for f in F[:8]:
        pts_.append((gx + s * f[2], gy + 24 - s * f[3]))
    d.add(f'<polyline points="{pts(pts_)}" fill="none" stroke="#6d5a10" stroke-width=".5"/>')
    d.add(f'<line x1="{gx-2}" y1="{gy+24}" x2="{gx + s*4*PITCH + 2}" y2="{gy+24}" stroke="#aaa" stroke-width=".25" stroke-dasharray="1 1"/>')
    # viewer arrows
    for t, col, lab in ((-18, "#222", "-18"), (0, "#222", "0"), (70, "#e0a000", "+70")):
        th = math.radians(t)
        cx = gx + s * 2 * PITCH
        L = 36
        sx_, sy_ = cx + L * math.sin(th), gy + 24 - L * math.cos(th) - 0
        d.add(f'<line x1="{f2(sx_)}" y1="{f2(sy_ - 6)}" x2="{f2(cx)}" y2="{f2(gy+24-3)}" stroke="{col}" stroke-width=".4"/>')
        d.note(sx_, sy_ - 8, lab, 2.4, col, "middle")
    d.note(gx, gy + 34, "A = 9 mm at +18 deg faces the guest,", 2.6, INK)
    d.note(gx, gy + 38, f"B = {B_W:.2f} mm at -70 deg faces the walker", 2.6, INK)
    d.note(gx, gy + 42, f"tooth depth {A_W*math.sin(ALPHA):.2f} mm; pitch {PITCH:.2f}", 2.6, GREY)
    # tent elevation
    tx, ty = 250, 125
    ks = 1.35
    panel = 50 * ks; ap = math.radians(20)
    d.text(tx - 10, ty - 8, "Tent in profile (x1.35): guest on the left", 3.0, 600, INK)
    base_y = ty + 60
    apex_x, apex_y = tx + 40, base_y - panel * math.cos(ap)
    d.add(f'<polyline points="{pts([(apex_x - panel*math.sin(ap), base_y), (apex_x, apex_y), (apex_x + panel*math.sin(ap), base_y)])}" fill="none" stroke="#6d5a10" stroke-width=".8"/>')
    d.line(apex_x - 60, base_y, apex_x + 60, base_y, "thin")
    d.note(apex_x, base_y + 6, f"footprint 34 mm deep, 51.5 mm tall; 50 mm panels, 40 deg apex", 2.5, GREY, "middle")
    d.save("c6_assembled.svg")

if __name__ == "__main__":
    verify()
    flat = flat_print()
    imgs = {}
    for t in (-18, 0, 35, 55, 70):
        imgs[t] = view(t, flat)
    assembled(imgs)
    dieline()
