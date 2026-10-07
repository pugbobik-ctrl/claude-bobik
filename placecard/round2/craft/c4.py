import math, base64, io
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from lib import *

CW, CH, CT = 118.0, 64.0, 1.4      # card
PITCH, DEPTH = 0.5, 0.20
PPM = 16                           # raster px per mm (simulation)
FONT_MM = 16.0

def mask_name():
    W, H = int(CW * PPM), int(CH * PPM)
    im = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONTDIR + "WixMadeforText-700.ttf", int(FONT_MM * PPM))
    for txt, ybase in (("Sophia", 35.0), ("Zhuravkova", 53.0)):
        wmm = tw(txt, FONT_MM, 700)
        x = (CW - wmm) / 2 * PPM
        dr.text((x, ybase * PPM), txt, font=f, fill=255, anchor="ls")
    return np.array(im) > 127

def height(mask):
    H, W = mask.shape
    ys = (np.arange(H) / PPM)[:, None]
    xs = (np.arange(W) / PPM)[None, :]
    def tri(u):  # 0..1 triangle
        u = u % 1.0
        return 1 - np.abs(2 * u - 1)
    hg = DEPTH * tri(ys / PITCH) * np.ones_like(xs)   # ridges along x (ground)
    hl = DEPTH * tri(xs / PITCH) * np.ones_like(ys)   # ridges along y (letters)
    return np.where(mask, hl, hg)

def shade(h, el_deg, az_deg, ambient=0.12):
    gy, gx = np.gradient(h, 1 / PPM)
    n = np.dstack([-gx, -gy, np.ones_like(h)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    e = math.radians(el_deg); a = math.radians(az_deg)
    # az: direction the light comes FROM, measured in image plane (0 = from the right, 90 = from the top of the card, 180 = from the left)
    l = np.array([math.cos(e) * math.cos(a), -math.cos(e) * math.sin(a), math.sin(e)])
    return ambient + (1 - ambient) * np.clip(n @ l, 0, None)

def render(mask, h, el, az, name):
    s = shade(h, el, az)
    # normalise so flat card at this light = 1.0 for the yellow
    sb = gaussian_filter(s, PPM * PITCH * 0.9)
    img = np.clip(sb / sb.mean() * 0.95, 0, 1.0)
    base = np.array([0xfe, 0xed, 0x95], float) / 255
    rgb = img[..., None] * base[None, None, :]
    rgb = np.clip(rgb, 0, 1)
    im = Image.fromarray((rgb * 255).astype(np.uint8)).resize((int(CW * 6), int(CH * 6)), Image.LANCZOS)
    return im, s

def contrast(mask, s):
    # ignore a 0.8 mm band around the letter edges
    from PIL import ImageFilter
    m = Image.fromarray((mask * 255).astype(np.uint8))
    er = np.array(m.filter(ImageFilter.MinFilter(13))) > 127
    inv = ~mask
    di = np.array(Image.fromarray((inv * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(13))) > 127
    L = s[er].mean(); G = s[di].mean()
    return L, G

def b64(im):
    b = io.BytesIO(); im.save(b, "PNG", optimize=True)
    return base64.b64encode(b.getvalue()).decode()

def run():
    mask = mask_name(); h = height(mask)
    cases = [("A  diffuse light from every side", 80, 0, "diffuse"),
             ("B  lamp low at the LEFT, 15 deg", 15, 180, "left"),
             ("C  lamp low at the FAR EDGE, 15 deg", 15, 90, "top")]
    out = []; res = []
    # diffuse: average of 8 azimuths at 45 deg elevation
    ims = []
    s_d = np.mean([shade(h, 45, a) for a in range(0, 360, 45)], axis=0)
    flat_d = 0.12 + 0.88 * math.sin(math.radians(45))
    sbd = gaussian_filter(s_d, PPM * PITCH * 0.9)
    imgd = np.clip(sbd / sbd.mean() * 0.95, 0, 1)
    base = np.array([0xfe, 0xed, 0x95], float) / 255
    rgbd = np.clip(imgd[..., None] * base, 0, 1)
    imd = Image.fromarray((rgbd * 255).astype(np.uint8)).resize((int(CW * 6), int(CH * 6)), Image.LANCZOS)
    L, G = contrast(mask, s_d)
    res.append(("diffuse (8 lamps, 45 deg)", L, G))
    ims.append(imd)
    for lab, el, az, key in cases[1:]:
        im, s = render(mask, h, el, az, key)
        L, G = contrast(mask, s)
        res.append((lab, L, G)); ims.append(im)
    return ims, res

def verify(res):
    o = ["C4 RAKING LIGHT geometry + lighting check",
         f"card {CW} x {CH} x {CT} mm board; grating pitch {PITCH}, depth {DEPTH}, triangle profile -> flank slope atan(2d/p) = {math.degrees(math.atan(2*DEPTH/PITCH)):.1f} deg",
         f"letters: Wix Madefor Bold {FONT_MM} mm: 'Zhuravkova' {tw('Zhuravkova', FONT_MM, 700):.1f} mm wide; stem ~ {0.16*FONT_MM:.1f} mm = {0.16*FONT_MM/PITCH:.1f} grating periods (>= 4 needed to read the orientation)",
         "Lambert simulation of the real height field (numpy, 16 px/mm, gradient normals, clamp at 0), mean brightness inside letters vs ground:"]
    for lab, L, G in res:
        o.append(f"  {lab:40s} letters {L:.3f}   ground {G:.3f}   Weber contrast {(L-G)/G*100:+.0f} %")
    # analytic cross-check at 15 deg
    sl = math.atan(2 * DEPTH / PITCH); e = math.radians(15)
    n1 = math.cos(math.radians(90) - e - sl) if False else None
    # flank toward the lamp: normal tilted by sl toward the lamp; lamp direction angle from vertical = 90-e
    ang_t = (math.pi / 2 - e) - sl; ang_a = (math.pi / 2 - e) + sl
    perp = 0.5 * (max(0, math.cos(ang_t)) + max(0, math.cos(ang_a)))
    par = math.sin(e) * math.cos(sl)
    o.append(f"analytic 15 deg: ridges across the beam {perp:.3f}  ridges along the beam {par:.3f}  ratio {perp/par:.2f}; flat card {math.sin(e):.3f}")
    o.append("Contrast flips sign when the lamp moves 90 deg round: letters bright in B, dark in C. Diffuse light: ~0 -> the name vanishes.")
    o.append("detectability: human contrast threshold on a plain surface ~ 2-3 %; here >> that at 15 deg (see numbers); at 45 deg lamp it falls (see run).")
    # sensitivity: elevation
    mask = mask_name(); hh = height(mask)
    for el in (10, 15, 25, 35, 45, 60):
        s = shade(hh, el, 180); L, G = contrast(mask, s)
        o.append(f"  lamp from the left, elevation {el:2d} deg: letters {L:.3f} ground {G:.3f}  Weber {(L-G)/G*100:+.0f} %")
    o.append("Production: polymer (relief) plate per name, blind impression 0.2 mm on 1.4 mm cotton-rich board; 8 names ganged on an A4 plate -> 5 plates for 40 guests.")
    open("c4_verify.txt", "w").write("\n".join(o) + "\n")
    print("\n".join(o))

def assembled(ims, res):
    W, H = 380, 205
    d = Doc(0, 0, W, H, scale=4.4)
    d.title(10, 13, "04  RAKING LIGHT — assembled (three simulated lightings of the same card)",
            "Height field of the real design lit by a Lambert model (see c4_verify.txt). The name is tone-on-tone relief; only 'Dinner' and the date are inked black.")
    labs = ["A  diffuse (room light, flash): name invisible", "B  candle low at the LEFT: name bright", "C  lamp at the FAR edge: name dark"]
    for i, im in enumerate(ims):
        x = 8 + i * 124
        y = 28
        d.add(f'<rect x="{x+1}" y="{y+1.4}" width="{CW}" height="{CH}" rx="3" fill="#000" opacity=".16"/>')
        d.add(f'<clipPath id="cc{i}"><rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="3"/></clipPath>')
        d.add(f'<image x="{x}" y="{y}" width="{CW}" height="{CH}" href="data:image/png;base64,{b64(im)}" clip-path="url(#cc{i})"/>')
        d.add(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="3" fill="none" stroke="#6d5a10" stroke-width=".25"/>')
        # black print
        d.text(x + 6, y + 10.5, "Dinner", 8, 700, INK)
        d.text(x + CW - 6, y + 10.5, "10.10.2026", 3.6, 500, INK, "end")
        d.text(x + 6, y + CH - 5, "Colorblock × DNA Kitchen · Moscow", 2.5, 500, INK)
        d.text(x + CW - 6, y + CH - 5, "S.Zh.", 2.5, 700, INK, "end")
        d.note(x, y + CH + 7, labs[i], 2.8, INK, weight=600)
        # lamp arrow
        if i == 1:
            d.add(f'<g stroke="#e0a000" stroke-width=".6" fill="#e0a000"><line x1="{x-6}" y1="{y+CH/2}" x2="{x-1}" y2="{y+CH/2}"/><polygon points="{x-1},{y+CH/2-1.2} {x+1.4},{y+CH/2} {x-1},{y+CH/2+1.2}"/></g>')
        if i == 2:
            d.add(f'<g stroke="#e0a000" stroke-width=".6" fill="#e0a000"><line x1="{x+CW/2}" y1="{y-6}" x2="{x+CW/2}" y2="{y-1}"/><polygon points="{x+CW/2-1.2},{y-1} {x+CW/2},{y+1.4} {x+CW/2+1.2},{y-1}"/></g>')
        lab, L, G = res[i]
        d.note(x, y + CH + 11.5, f"mean brightness letters {L:.2f} / ground {G:.2f}  ->  {(L-G)/G*100:+.0f} %", 2.5, GREY)
    gx, gy = 14, 112
    d.text(gx, gy, "Cross-section of the relief, true proportions (1 mm = 48 units, depth 0.2 / pitch 0.5)", 3, 600, INK)
    ku = 48.0
    base_y = gy + 30
    d.add(f'<rect x="{gx}" y="{base_y}" width="{5*PITCH*ku}" height="3.2" fill="{LEMON_D}" stroke="#6d5a10" stroke-width=".2"/>')
    pts_ = []
    for i in range(0, 5):
        x0 = gx + i * PITCH * ku
        pts_ += [(x0, base_y), (x0 + PITCH * ku / 2, base_y - DEPTH * ku), (x0 + PITCH * ku, base_y)]
    d.add(f'<polyline points="{pts(pts_)}" fill="{LEMON}" stroke="#6d5a10" stroke-width=".4"/>')
    # lamp rays at 15 deg from the left
    for i in range(4):
        yy = base_y - 22 + i * 3.2
        xx = gx - 6
        d.add(f'<line x1="{xx}" y1="{yy}" x2="{xx+30}" y2="{yy+30*math.tan(math.radians(15))}" stroke="#e0a000" stroke-width=".35"/>')
    d.note(gx + 5 * PITCH * ku + 3, base_y - 8, "lamp 15 deg above the board, beam across the ridges:", 2.5, INK)
    d.note(gx + 5 * PITCH * ku + 3, base_y - 4.6, "flank facing the lamp is lit, the far flank is in its own shadow", 2.5, GREY)
    d.note(gx + 5 * PITCH * ku + 3, base_y - 1.2, "beam along the ridges: both flanks equal, ~2x darker (see c4_verify.txt)", 2.5, GREY)
    d.notes(14, 160, [
        "How it reads at the table",
        "- Daylight / ceiling light: a quiet lemon slab with 'Dinner'.",
        "- A candle or the phone torch held low and tilted:",
        "  the name lights up; turn the card 90 deg and it inverts.",
        "- Fingertip: the letters feel like corduroy against velvet.",
        "- 'S.Zh.' in black is a find-aid for the seat in daylight.",
    ], 2.7, 1.5, INK)
    d.save("c4_assembled.svg")
    for i, im in enumerate(ims):
        im.save(f"png/c4_sim_{i}.png")

def dieline():
    W, H = 330, 215
    d = Doc(0, 0, W, H, scale=5.0)
    d.title(10, 13, "04  RAKING LIGHT — dieline and relief map",
            "1:1 (mm). 118 x 64 x 1.4 board, corner radius 3. Plate 1: black (Dinner, date, event, find-aid). Plate 2: blind relief, name in vertical lines on a ground of horizontal lines.")
    ox, oy = 18, 30
    d.rect(ox, oy, CW, CH, "cut", LEMON, rx=3)
    # relief map : ground horizontal hatch (drawn at 4x pitch = 2 mm... to show), letters vertical hatch
    mask = mask_name()
    # vectorise name via text, clipped pattern
    d.defs.append(f'<pattern id="hg" width="2" height="2" patternUnits="userSpaceOnUse"><line x1="0" y1="1" x2="2" y2="1" stroke="{EMB}" stroke-width=".22"/></pattern>')
    d.defs.append(f'<pattern id="hv" width="2" height="2" patternUnits="userSpaceOnUse"><line x1="1" y1="0" x2="1" y2="2" stroke="{EMB}" stroke-width=".22"/></pattern>')
    d.defs.append(f'<clipPath id="card"><rect x="{ox}" y="{oy}" width="{CW}" height="{CH}" rx="3"/></clipPath>')
    d.add(f'<rect x="{ox+3}" y="{oy+3}" width="{CW-6}" height="{CH-6}" fill="url(#hg)" clip-path="url(#card)"/>')
    for txt, yb in (("Sophia", 35.0), ("Zhuravkova", 53.0)):
        d.add(f'<text x="{ox+CW/2}" y="{oy+yb}" font-size="{FONT_MM}" font-weight="700" text-anchor="middle" fill="#ffffff" stroke="#ffffff" stroke-width="0.4">{txt}</text>')
        d.add(f'<text x="{ox+CW/2}" y="{oy+yb}" font-size="{FONT_MM}" font-weight="700" text-anchor="middle" fill="url(#hv)">{txt}</text>')
    d.text(ox + 6, oy + 10.5, "Dinner", 8, 700, INK)
    d.text(ox + CW - 6, oy + 10.5, "10.10.2026", 3.6, 500, INK, "end")
    d.text(ox + 6, oy + CH - 5, "Colorblock × DNA Kitchen · Moscow", 2.5, 500, INK)
    d.text(ox + CW - 6, oy + CH - 5, "S.Zh.", 2.5, 700, INK, "end")
    d.note(ox, oy - 3, "front (relief map drawn at 4x the real 0.5 mm pitch so it can be seen)", 2.5, GREY)
    d.line(ox, oy + CH + 5, ox + CW, oy + CH + 5, "dim"); d.note(ox + CW / 2, oy + CH + 9, "118", 2.6, INK, "middle")
    d.line(ox - 5, oy, ox - 5, oy + CH, "dim"); d.add(f'<text transform="translate({ox-8} {oy+CH/2}) rotate(-90)" font-size="2.6" text-anchor="middle" fill="{INK}">64</text>')
    d.rect(ox + 3, oy + 3, CW - 6, CH - 6, "emb", "none", extra='stroke-dasharray=".8 .8"')
    d.note(ox + 4, oy + 1.9 - 0.0, "", 2)
    d.note(ox + 3, oy + CH + 15, "dashed: relief field, 3 mm inside the edge (edge stays flat for the die-cut)", 2.4, GREY)
    # reverse
    rx = ox + CW + 22
    d.rect(rx, oy, CW, CH, "cut", LEMON, rx=3)
    d.note(rx, oy - 3, "back: plain, or a one-line black menu / seating note", 2.5, GREY)
    d.text(rx + CW / 2, oy + CH / 2 - 3, "Sophia Zhuravkova", 6.0, 600, INK, "middle")
    d.text(rx + CW / 2, oy + CH / 2 + 3.5, "table 1, long side", 2.8, 500, INK, "middle")
    d.note(rx + CW / 2, oy + CH / 2 + 9, "(optional: the name in plain ink, face down as a fallback)", 2.3, GREY, "middle")
    # zoom window
    zx, zy = 18, 130
    d.text(zx, zy - 3, "Zoom 12 x 7 mm at the edge of an 'h' stem (x6 of real size, true pitch 0.5)", 3, 600, INK)
    z = 7.0
    zw, zh = 40, 24   # mm real
    d.add(f'<clipPath id="zc"><rect x="{zx}" y="{zy}" width="{12*z}" height="{7*z}"/></clipPath>')
    d.rect(zx, zy, 12 * z, 7 * z, "thin", LEMON)
    g = []
    for i in range(0, int(7 / PITCH) + 1):
        yy = zy + i * PITCH * z
        g.append(f'<line x1="{zx}" y1="{f2(yy)}" x2="{zx+6.1*z}" y2="{f2(yy)}" stroke="{EMB}" stroke-width=".35"/>')
    for i in range(0, int(6 / PITCH) + 1):
        xx = zx + 6.0 * z + i * PITCH * z
        g.append(f'<line x1="{f2(xx)}" y1="{zy}" x2="{f2(xx)}" y2="{zy+7*z}" stroke="{EMB}" stroke-width=".35"/>')
    d.add(f'<g clip-path="url(#zc)">{"".join(g)}</g>')
    d.add(f'<line x1="{zx+6*z}" y1="{zy}" x2="{zx+6*z}" y2="{zy+7*z}" stroke="{CUT}" stroke-width=".5" stroke-dasharray="1 1"/>')
    d.note(zx + 3 * z, zy + 7 * z + 4, "ground: horizontal lines", 2.5, INK, "middle")
    d.note(zx + 9 * z, zy + 7 * z + 4, "letter: vertical lines", 2.5, INK, "middle")
    d.notes(130, 130, [
        "PLATE DATA",
        "relief lines 0.25 wide on 0.50 pitch (50 %), line angle 0 deg ground / 90 deg letters",
        f"impression depth {DEPTH} mm (0.15-0.25 workable) into 1.4 mm board (about 14 %)",
        "no registration needed between the two plates: the blind relief is not trimmed to the ink",
        "name outline = Wix Madefor Text Bold 16 mm, set solid, no outline stroke",
        "one polymer plate per guest, 8-up on A4 plates; die-cut after embossing (corner radius 3)",
        "",
        "Text widths:  Sophia " + f"{tw('Sophia', FONT_MM, 700):.1f}" + " mm,  Zhuravkova " + f"{tw('Zhuravkova', FONT_MM, 700):.1f}" + " mm  (field 112 wide)",
    ], 2.7, 1.5, INK)
    d.legend(130, 185, [("cut", "die cut, R3"), ("emb", "relief field boundary (blind)"), ("swatch_lemon", "board: 1.4 mm lemon (duplex 2 x 700 g or solid 1.4 mm)")])
    d.save("c4_dieline.svg")

if __name__ == "__main__":
    ims, res = run()
    verify(res)
    assembled(ims, res)
    dieline()
