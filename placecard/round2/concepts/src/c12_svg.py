from lib import *
import c12_calc as K
import numpy as np, math
s = S()
s.header('12', 'POUR', 'The name is unreadable until you pour. A tumbler of water is a lens; the card is printed for it.')
def img(f, x, y, w, h, label, sub, c=INK):
    s.raw(f'<image href="{b64img("../calc/" + f)}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>')
    s.poly([(x, y), (x+w, y), (x+w, y+h), (x, y+h)], 'none', GREY_L, 1)
    s.text((x, y - 10), label, 12, 700, GREY, ls=1); s.text((x, y + h + 20), sub, 12, 500, c)
img('c12_view_empty_c.png', 48, 150, 372, 207, 'EMPTY GLASS (or no glass)', 'mirror-image smudge: reads as a pattern')
img('c12_view_full_c.png', 440, 150, 372, 207, 'GLASS FILLED WITH WATER', 'ray-traced: the lens flips and magnifies 3x')
img('c12_print_lemon.png', 832, 150, 320, 207, 'THE PRINT ON THE CARD (60 mm wide)', 'mirrored, uneven: tight at the middle')
# plan view with refraction
ox, oy, k = 600, 880, 1.05      # eye at bottom (y=-450 -> screen)
def PL(x, y): return (ox + x * k * 3.0 if False else ox + x * 3.0, 700 - (y) * 0.55)
# plan scaled: x scale 3, y scale 0.55 would distort; draw schematic instead with uniform scale on a zoom
zx = 2.3
def Z(x, y): return (270 + x * zx, 740 - y * zx)     # zoomed plan around glass, y up = away from eye
s.text((48, 412), 'PLAN, zoomed at the glass (mm, true shape; eye is 450 mm below the page)', 12, 700, GREY, ls=1)
s.circle(Z(0, 0), K.A * zx, '#cfe3ea', INK, 1.6, extra='fill-opacity="0.7"')
s.line(Z(-70, K.D), Z(70, K.D), INK, 4); s.text((Z(74, K.D)[0], Z(74, K.D)[1] + 4), 'card', 12, 600)
for xo in (-26, -14, -5, 5, 14, 26):
    th = math.atan2(xo, 450) if False else math.asin(xo / math.hypot(xo, 450.))
    # ray from eye aimed so it is at x=xo at glass plane
    o = np.array([0.0, -K.EYE]); d = np.array([xo, K.EYE]); d /= np.linalg.norm(d)
    b = o @ d; c = o @ o - K.A**2; disc = b * b - c
    t1 = -b - math.sqrt(disc); P = o + t1 * d; nrm = P / K.A
    cos_i = -d @ nrm; sin_t = math.sqrt(1 - cos_i**2) / K.N; cos_t = math.sqrt(1 - sin_t**2)
    d2 = d / K.N + (cos_i / K.N - cos_t) * nrm; d2 /= np.linalg.norm(d2)
    b2 = P @ d2; t2 = -b2 + math.sqrt(b2 * b2 - (P @ P - K.A**2)); P2 = P + t2 * d2
    nout = P2 / K.A; cos_i2 = d2 @ nout; sin_o = K.N * math.sqrt(1 - cos_i2**2); cos_o = math.sqrt(1 - sin_o**2)
    d3 = K.N * d2 + (cos_o - K.N * cos_i2) * nout; d3 /= np.linalg.norm(d3)
    t = (K.D - P2[1]) / d3[1]; X = P2 + t * d3
    back = P - 14 * d
    s.polyline([Z(*back), Z(*P), Z(*P2), Z(*X)], '#1d6fb8', 1.3)
    s.circle(Z(*X), 3, '#1d6fb8', '#1d6fb8', 1)
s.text((Z(60, -K.A - 6)[0], Z(60, -K.A - 6)[1]), 'to the eye, 450 mm', 12, 600, GREY)
s.text((Z(K.A + 6, -4)[0], Z(K.A + 6, -4)[1]), 'water, n 1.33', 12, 600)
s.note((620, 470), ['Rays that enter left of centre land on the card right of centre:', 'the image through the glass is mirrored.', 'Near the middle the card region seen per mm of view is 0.43 mm,', 'against 1.27 mm for the bare line of sight: 3x magnified.', '', 'Printing = run the rays backwards for every letter edge.', '', 'Caveats: the glass must be a straight tumbler, not a tulip;', 'wine is tinted but optically the same; glass wall ignored.'], 13)
s.note((620, 740), ['Card stands 120 mm behind the glass on a slotted foot,', '60 mm print band, 160 x 90 mm card, one sheet.'], 13)
s.save('../svg/12_pour.svg')
