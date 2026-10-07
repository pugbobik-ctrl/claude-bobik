from lib import *
s = S()
s.header('06', 'THREE FACES', 'A hexagon the size of a coaster. Pinch and flex it: name, then the menu, then the evening. The card is the programme.')
SQ3 = math.sqrt(3)
def hexagon(cx, cy, a, fill=LEMON):
    return [(cx + a * math.cos(math.radians(60 * i)), cy + a * math.sin(math.radians(60 * i))) for i in range(6)]
a = 128
faces = [('FACE 1: YOU', ['Sophia', 'Zhuravkova', 'TABLE 4  SEAT 07']), ('FACE 2: THE MENU', ['I  cold', 'II  fire', 'III  sweet']), ('FACE 3: THE EVENING', ['Colorblock', 'x DNA Kitchen', '10 Oct 2026'])]
for i, (nm, lines) in enumerate(faces):
    cx = 200 + i * 400; cy = 300
    hx = hexagon(cx, cy, a)
    s.poly(hx, LEMON, INK, 2.2)
    for k in range(6):
        s.line((cx, cy), hx[k], '#d4be5c', 1, dash='3 4')
    if i == 0:
        s.text((cx, cy - 6), 'Sophia', 30, 700, INK, 'middle'); s.text((cx, cy + 26), 'Zhuravkova', 30, 700, INK, 'middle'); s.text((cx, cy + 56), 'TABLE 4   SEAT 07', 12, 600, INK, 'middle', ls=1.5)
    elif i == 1:
        for j, (r, t) in enumerate((('I', 'cold'), ('II', 'fire'), ('III', 'sweet'))):
            s.text((cx - 70, cy - 24 + j * 38), r, 20, 700, INK); s.text((cx - 22, cy - 24 + j * 38), t, 26, 700, INK)
    else:
        s.text((cx, cy - 22), 'Colorblock', 26, 700, INK, 'middle'); s.text((cx, cy + 8), 'x DNA Kitchen', 22, 600, INK, 'middle')
        s.text((cx, cy + 44), 'MOSCOW   10.10.2026', 12, 600, INK, 'middle', ls=1.5)
    s.text((cx, cy + a + 36), nm, 12, 700, GREY, 'middle', ls=1)
    if i < 2:
        x0 = cx + a + 28
        s.path(f'M{x0},{cy-12} q38,-34 76,0', 'none', INK, 1.8); s.polyline([(x0+76, cy-12), (x0+66, cy-16)], INK, 1.8); s.polyline([(x0+76, cy-12), (x0+72, cy-22)], INK, 1.8)
        s.text((x0 + 38, cy + 18), 'flex', 12, 600, GREY, 'middle')
# net
nx, ny, side = 60, 650, 78
h = side * SQ3 / 2
s.text((nx, ny - 20), 'THE STRIP: 9 triangles + glue tab, side 45 mm (drawn x1.7), folded on every dashed line', 12, 700, GREY, ls=1)
tris = []
for i in range(10):
    x = nx + i * side / 2
    if i % 2 == 0: pts = [(x, ny + h), (x + side, ny + h), (x + side/2, ny)]
    else: pts = [(x, ny), (x + side, ny), (x + side/2, ny + h)]
    pts = [(nx + i * side/2 + (0 if i % 2 == 0 else 0), 0)]
polys = []
for i in range(10):
    x = nx + i * side / 2
    if i % 2 == 0: pts = [(x, ny + h), (x + side, ny + h), (x + side / 2, ny)]
    else: pts = [(x + side/2, ny + h), (x, ny), (x + side, ny)]
    s.poly(pts, LEMON if i < 9 else LEMON_DD, INK, 1.6)
    c = (sum(p[0] for p in pts)/3, sum(p[1] for p in pts)/3)
    s.text(c, str(i + 1) if i < 9 else 'glue', 14 if i < 9 else 11, 700, GREY, 'middle', extra='dy="5"')
s.note((nx, ny + h + 40), ['Each triangle is printed both sides; 3 faces x 6 triangles = 18 = 9 x 2.', 'Face layout follows the standard trihexaflexagon template: mock it up in white paper before artwork.'], 13)
s.note((880, ny - 6), ['Hexagon 90 mm across, 350 gsm', 'lemon card, scored, no glue but the tab.', '', 'Lies flat beside the plate; faces 2 and 3', 'are found only by playing with it.'], 13)
s.save('../svg/06_three_faces.svg')
