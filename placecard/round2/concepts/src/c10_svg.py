from lib import *
s = S()
s.header('10', 'COLLAR', 'Four neighbours, four cards, one lamp. Each card slots into the next and together they build a collar around the lamp: a table of small lit rooms.')
cam = Cam(az=-24, el=26, s=1.55, ox=380, oy=770)
cloth(s, cam, -170, 170, -130, 130, 0)
H = 52; L = 160; HALF = 50; TH = 0.0
def panel(p0, p1, fill=LEMON, slots='top', slot_x=None):
    pts = [cam.p(*p0, 0), cam.p(*p1, 0), cam.p(*p1, H), cam.p(*p0, H)]
    s.poly(pts, fill, INK, 1.6)
def slot_line(a, b, z0, z1):
    s.line(cam.p(a[0], a[1], z0), cam.p(b[0], b[1], z1), INK, 2.4)
# back panel N (y=+50), runs along x
panel((-L/2, HALF), (L/2, HALF), LEMON_D)
# W (x=-50) and E (x=+50) run along y
panel((-HALF, -L/2), (-HALF, L/2), LEMON_D)
# lamp
lamp(s, cam, (0, 0), 0, 300, 70, 95)
# E panel
panel((HALF, -L/2), (HALF, L/2), LEMON)
# S panel front (y=-50) with names
panel((-L/2, -HALF), (L/2, -HALF), LEMON)
s.face_text(cam, (-L/4, -HALF - 0.1, 29), (1, 0, 0), (0, 0, 1), 'Sophia', 11, 700, INK, 'middle')
s.face_text(cam, (-L/4, -HALF - 0.1, 15), (1, 0, 0), (0, 0, 1), 'Zhuravkova', 11, 700, INK, 'middle')
s.face_text(cam, (L/4, -HALF - 0.1, 29), (1, 0, 0), (0, 0, 1), 'Anton', 11, 700, INK, 'middle')
s.face_text(cam, (L/4, -HALF - 0.1, 15), (1, 0, 0), (0, 0, 1), 'Vetrov', 11, 700, INK, 'middle')
# joints marks (corner slots)
for (cx, cy) in ((-HALF, -HALF), (HALF, -HALF)):
    s.line(cam.p(cx, cy, H), cam.p(cx, cy, H - 26), RED, 1.6)
s.leader(cam.p(HALF, -HALF, H), (800, 640), ['half-height slots,', 'one from the top, one from the bottom'], 'r')
s.leader(cam.p(L/2, 0, 30), (800, 720), ['east / west cards:', 'the table, the date'], 'r')
s.leader(cam.p(0, -HALF, 6), (520, 800), ['south: two guests, one lamp'], 'r') if False else None
# flat die lines
fx, fy, fs = 790, 220, 2.2
s.text((fx, fy - 20), 'DIE LINES, 160 x 52 mm (red = cut)', 12, 700, GREY, ls=1)
def card(y, slots_from_top, label):
    s.poly([(fx, y), (fx + L*fs, y), (fx + L*fs, y + H*fs), (fx, y + H*fs)], LEMON, INK, 1.4)
    for sx in (L/2 - 50 - 0.5, L/2 + 50 - 0.5):
        xx = fx + (L/2 + (sx - L/2)) * fs
        if slots_from_top: s.poly([(xx, y), (xx + 1.2*fs, y), (xx + 1.2*fs, y + 26*fs), (xx, y + 26*fs)], PAPER, RED, 1.2)
        else: s.poly([(xx, y + H*fs), (xx + 1.2*fs, y + H*fs), (xx + 1.2*fs, y + (H-26)*fs), (xx, y + (H-26)*fs)], PAPER, RED, 1.2)
    s.text((fx + 6, y + H*fs + 16), label, 12, 500)
card(fy, True, 'north / south: slots from the top, 26 deep')
card(fy + H*fs + 44, False, 'east / west: slots from the bottom')
s.note((790, 560), ['Printed both sides: guest face outward, lamp face inside.', 'Four to six cards per lamp; closes only when all sit.', 'Card 350 gsm, slot 1.2 mm for the paper thickness.'], 13)
s.save('../svg/10_collar.svg')
