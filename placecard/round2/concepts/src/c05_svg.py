from lib import *
s = S()
s.header('05', 'SPIN', 'An empty plate on one side, your name on the other. Roll the threads between your fingers and the name lands on the plate.')
R = 150   # disc radius in px (70 mm -> 300 px)
def disc(cx, cy, mode, op=1.0, rot=0):
    s.circle((cx, cy), R, LEMON, INK, 2.4)
    s.circle((cx - R + 22, cy), 6, 'none', INK, 1.6); s.circle((cx + R - 22, cy), 6, 'none', INK, 1.6)
    g = f'<g transform="rotate({rot} {cx} {cy})" opacity="{op}">'
    s.raw(g)
    if mode in ('plate', 'both'):
        s.circle((cx, cy), 108, 'none', INK, 3); s.circle((cx, cy), 84, 'none', INK, 2)
        # fork (left) and knife (right)
        s.line((cx - 128, cy - 50), (cx - 128, cy + 62), INK, 4)
        for dx in (-8, 0, 8): s.line((cx - 122 + dx, cy - 56), (cx - 122 + dx, cy - 28), INK, 2.5)
        s.line((cx + 122, cy - 56), (cx + 122, cy + 62), INK, 4)
        s.path(f'M{cx+122},{cy-56} q18,18 0,52 z', INK, INK, 1)
    if mode in ('name', 'both'):
        s.text((cx, cy - 4), 'Sophia', 25, 700, INK, 'middle')
        s.text((cx, cy + 26), 'Zhuravkova', 25, 700, INK, 'middle')
    s.raw('</g>')
cy = 330
disc(220, cy, 'plate'); s.text((220, cy + R + 36), 'SIDE A', 12, 700, GREY, 'middle', ls=1)
s.text((220, cy + R + 56), 'empty plate, knife and fork', 13, 500, INK, 'middle')
disc(600, cy, 'name', rot=180); s.text((600, cy + R + 36), 'SIDE B  (printed upside-down)', 12, 700, GREY, 'middle', ls=1)
s.text((600, cy + R + 56), 'the name, in the plate\'s ring', 13, 500, INK, 'middle')
# merged
disc(980, cy, 'both', 1.0)
s.raw(f'<rect x="{980-R}" y="{cy-R}" width="{2*R}" height="{2*R}" fill="none"/>')
s.text((980, cy + R + 36), 'SPINNING: BOTH AT ONCE', 12, 700, GREY, 'middle', ls=1)
s.text((980, cy + R + 56), 'persistence of vision, 12 turns a second', 13, 500, INK, 'middle')
s.text((410, cy + 4), '+', 44, 400, GREY, 'middle'); s.text((790, cy + 4), '=', 44, 400, GREY, 'middle')
# threads detail
tx, ty = 220, 740
s.text((48, 660), 'HOW IT IS HELD', 12, 700, GREY, ls=1)
s.circle((tx, ty + 40), 48, LEMON, INK, 2)
s.line((tx - 48, ty + 40), (tx - 120, ty - 20), INK, 1.4); s.line((tx + 48, ty + 40), (tx + 120, ty - 20), INK, 1.4)
for sx in (-1, 1):
    s.raw(f'<ellipse cx="{tx + sx*128}" cy="{ty - 26}" rx="22" ry="12" fill="#e7dccb" stroke="{GREY}" stroke-width="1.5"/>')
s.text((tx - 128, ty - 48), 'thumb', 12, 600, GREY, 'middle'); s.text((tx + 128, ty - 48), 'finger', 12, 600, GREY, 'middle')
s.path(f'M{tx-30},{ty+108} q30,14 60,0', 'none', INK, 1.6); s.polyline([(tx+30, ty+108), (tx+38, ty+101)], INK, 1.6); s.polyline([(tx+30, ty+108), (tx+39, ty+113)], INK, 1.6)
s.text((tx, ty + 134), 'roll the threads', 12, 500, INK, 'middle')
s.note((420, 690), ['Disc 70 mm, 400 gsm lemon card, both sides printed, 2 holes,', '2 x 150 mm black cotton thread loops tied to the glass stem.', 'Spin it once and it is a toy; every disc is the same plate,', 'only the name changes: one artwork file, 40 names.', '', 'Variant: side B shows the menu course, so the dish lands on the plate.'], 13)
s.save('../svg/05_spin.svg')
