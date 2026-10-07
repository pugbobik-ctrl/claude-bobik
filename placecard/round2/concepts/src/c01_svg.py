from lib import *
import c01_calc as K, c01_build as B
from shapely.geometry import box, Polygon
from shapely import affinity

hp = B.holes_plate_coords(); hc = B.to_card(hp)
CW, CH = B.CARD_W, B.CARD_H
s = S()
s.header('01', 'LIT', 'The lamp writes the name on your plate. A stencil card that only means something under the table lamp.')

cam = FCam(ymax=520, az=-24, el=36, s=0.74, ox=330, oy=570)
W = cam.p
# cloth
cloth(s, cam, -210, 210, -50, 500, 0)
# lamp (at y=0)
lamp(s, cam, (0, 0), 0, 300, 70, 95)
# glow cone hint
# card panel (vertical at y=YC) + foot
Y = K.YC
def cp(xc, zc): return W(xc, Y, zc)
panel = [cp(-CW/2, 0), cp(CW/2, 0), cp(CW/2, CH), cp(-CW/2, CH)]
# foot (slotted, flat) 96 x 50 centred on panel line
foot = [W(-CW/2, Y-25, 0), W(CW/2, Y-25, 0), W(CW/2, Y+25, 0), W(-CW/2, Y+25, 0)]
s.poly(foot, LEMON_D, INK, 1.4)
# back face visible? viewer is on guest side so we see the guest face (front). draw panel
s.poly(panel, LEMON, INK, 1.6)
# holes in card face (as the guest sees it)
holes_path = geom_path(hc, lambda p: W(p[0], Y + 0.2, p[1]))
s.path(holes_path, '#2c2a26', 'none', 0, extra='fill-rule="evenodd"')
# shadow of card on cloth beyond the plate region + on plate
def shadow_poly(zplane):
    lam_top = (K.LAMP[2]-zplane)/(K.LAMP[2]-CH)
    lam_bot = (K.LAMP[2]-zplane)/(K.LAMP[2]-max(zplane, 0))
    pts = [(-CW/2*lam_bot, Y*lam_bot), (CW/2*lam_bot, Y*lam_bot), (CW/2*lam_top, Y*lam_top), (-CW/2*lam_top, Y*lam_top)]
    return Polygon(pts)
sh_cloth = shadow_poly(0)
disc = Polygon([(K.PLATE_C[0]+K.PLATE_R*math.cos(a/36*2*math.pi), K.PLATE_C[1]+K.PLATE_R*math.sin(a/36*2*math.pi)) for a in range(36)])
outside = sh_cloth.difference(disc)
for p in geom_polys(outside):
    s.poly([W(x, y, 0) for x, y in p.exterior.coords], '#cfccc0', 'none', 0)
# plate
plate(s, cam, K.PLATE_C, K.PLATE_R, 0, 14)
# plate surface z = 14 (rim top) -> we draw lit letters on the plate well at ZP=12
sh_pl = shadow_poly(K.ZP).intersection(disc.buffer(-1))
for p in geom_polys(sh_pl):
    s.poly([W(x, y, 12) for x, y in p.exterior.coords], '#a9a69b', 'none', 0)
# lit letters = holes mapped to plate (hp)
s.path(geom_path(hp, lambda p: W(p[0], p[1], 12.2)), '#fffdf2', 'none', 0, extra='fill-rule="evenodd"')
# lit region glow rays (dashed) from lamp rim through the band
for (xx, zz) in [(-38, 88), (38, 88), (-38, 112), (38, 112)]:
    pl = K.card_to_plate(xx, zz)
    s.line(W(0, 0, 295), W(xx, Y, zz), '#d6a800', 0.9, dash='3 4')
    s.line(W(xx, Y, zz), W(pl[0], pl[1], 12), '#d6a800', 0.9, dash='3 4')
# labels
s.leader(cp(-CW/2, CH*0.55), (110, 470), ['stencil card, 96 x 124 mm', 'name cut in, flipped'], 'r')
s.leader(W(60, 290, 12), (620, 470), ['the name lands here:', 'lit letters inside the', 'card\'s own shadow'], 'r')
s.leader(W(60, 0, 270), (600, 250), ['lamp, bulb at 300 mm'], 'r')

# ---- card front panel (as guest sees it), right column ----
fx, fy, sc = 840, 150, 2.55
s.text((fx, fy - 12), 'CARD FRONT (flat, guest side), 1:1 x 2.55', 12, 700, GREY, ls=1)
s.poly([(fx, fy), (fx + CW*sc, fy), (fx + CW*sc, fy + CH*sc), (fx, fy + CH*sc)], LEMON, INK, 1.8)
s.path(geom_path(hc, lambda p: (fx + (p[0] + CW/2)*sc, fy + (CH - p[1])*sc)), INK, 'none', 0, extra='fill-rule="evenodd"')
# dims
s.line((fx, fy + CH*sc + 18), (fx + CW*sc, fy + CH*sc + 18), GREY, 1); s.text((fx + CW*sc/2, fy + CH*sc + 34), '96', 12, 600, GREY, 'middle')
s.line((fx - 18, fy), (fx - 18, fy + CH*sc), GREY, 1); s.text((fx - 24, fy + CH*sc/2), '124', 12, 600, GREY, 'end')
s.note((fx, fy + CH*sc + 62), ['Reads as a vertically flipped stencil.', 'Bridges (1.5 mm) hold every counter.', 'Foot: separate 96 x 50 slotted piece.'], 13, 500)

# ---- side section ----
sx0, sy0, k = 50, 850, 0.52     # x: y world (0..520) -> horizontally ; z up
def SP(y, z): return (sx0 + y*k, sy0 - z*k)
s.text((sx0, 650), 'SIDE SECTION (mm, to scale)', 12, 700, GREY, ls=1)
s.line(SP(0, 0), SP(520, 0), INK, 1.6)
s.circle(SP(0, 300), 5, '#d6a800', INK, 1.2)
cone_pts = [SP(0, 0), SP(0, 0)]
s.poly([SP(-70, 205), SP(70, 205), SP(10, 300), SP(-10, 300)], INK, INK, 1)
s.line(SP(0, 0), SP(0, 205), INK, 3)
s.line(SP(Y, 0), SP(Y, CH), INK, 3)
s.line(SP(K.PLATE_C[1]-K.PLATE_R, 12), SP(K.PLATE_C[1]+K.PLATE_R, 12), GREY, 3)
for zz in (84, 114):
    pl = K.card_to_plate(0, zz)
    s.line(SP(0, 300), SP(pl[1], 12), '#d6a800', 1.2)
    s.circle(SP(Y, zz), 2.6, INK, INK, 1)
s.line(SP(0, 300), SP(Y, CH), '#d6a800', 1, dash='4 4')
s.line(SP(Y, CH), SP(K.card_to_plate(0, CH)[1], 12), '#d6a800', 1, dash='4 4')
s.text(SP(Y + 6, CH + 14), 'card', 12, 600)
s.text(SP(0, 316), 'lamp', 12, 600, anchor='middle')
s.text(SP(K.PLATE_C[1], 40), 'plate', 12, 600, anchor='middle')
s.text(SP(Y-4, 128), 'band z 85..114', 11, 500, GREY, 'end')

# ---- computed top views ----
x0 = 330
s.text((x0 + 10, 672), 'COMPUTED: TOP VIEW OF THE PLATE, THREE LIGHT SOURCES (ray-traced)', 12, 700, GREY, ls=1)
labs = [('c01_shadow_point.png', 'point source', 'sharp'), ('c01_shadow_led5mm.png', 'LED filament bulb, 5 mm', 'reads'), ('c01_shadow_bulb25mm.png', 'opal bulb, 25 mm', 'does not read')]
for i, (f, a, b) in enumerate(labs):
    ix = x0 + 10 + i * 275
    s.raw(f'<image href="{b64img("../calc/" + f)}" x="{ix}" y="708" width="262" height="160" preserveAspectRatio="xMidYMin slice" clip-path="inset(0)"/>')
    s.poly([(ix, 708), (ix+262, 708), (ix+262, 868), (ix, 868)], 'none', GREY_L, 1)
    s.text((ix, 696), a, 12, 700, INK if i < 2 else RED)
    s.text((ix + 262, 696), b, 12, 500, GREY, 'end')
s.save('../svg/01_lit.svg')
