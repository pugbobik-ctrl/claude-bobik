from lib import *
import c02_calc as K
s = S()
s.header('02', 'SIT DOWN', 'A name that only assembles from your own seat. From anywhere else the card is a folded bird of fragments.')
# row of renders
views = [('seat', 'FROM YOUR SEAT', 'eye 430 mm up, 450 mm away: whole name', INK),
         ('neighbourR', 'FROM THE NEXT SEAT', '330 mm to the side: half hides in the fold', INK),
         ('walkby', 'WALKING PAST', 'grazing: a sliver of shards', INK),
         ('across', 'ACROSS THE TABLE', 'sees the back: seat number goes here', INK)]
x = 48
for k, a, b, c in views:
    s.raw(f'<image href="{b64img("../calc/c02_view_" + k + ".png")}" x="{x}" y="150" width="262" height="202" preserveAspectRatio="xMidYMid slice"/>')
    s.poly([(x, 150), (x+262, 150), (x+262, 352), (x, 352)], 'none', GREY_L, 1)
    s.text((x, 140), a, 12, 700, GREY, ls=1)
    s.text((x, 372), b, 12, 500, INK)
    x += 278
# plan diagram
px0, py0, k = 235, 440, 0.24
def PP(xm, ym): return (px0 + xm * k, py0 + ym * k)
s.text((48, 412), 'PLAN, guest at the bottom', 12, 700, GREY, ls=1)
s.line(PP(-700, 0), PP(400, 0), GREY_L, 1, dash='4 4'); s.text(PP(400, -6), 'image plane', 11, 500, GREY, 'end')
a = K.ALPHA; L = K.WL
for sg in (-1, 1):
    s.line(PP(0, 0), PP(sg * L * math.sin(a), L * math.cos(a)), INK, 5)
s.circle(PP(0, 0), 3, INK, INK, 1)
eyes = [((0, 450), 'seat', INK), ((330, 350), 'next seat', GREY), ((-700, 150), 'walking past', GREY)]
for (ex, ey), lab, c in eyes:
    s.line(PP(ex, ey), PP(0, 0), c, 1, dash='5 4')
    s.circle(PP(ex, ey), 6, c, c, 1)
    s.text((PP(ex, ey)[0] + 10, PP(ex, ey)[1] + 4), lab, 12, 600, c)
s.text(PP(-14, 120), '450 mm', 12, 600, GREY, 'end')
s.text(PP(46, 40), '90 deg', 11, 600, INK)
# object render
s.text((470, 412), 'THE OBJECT (two leaves, 82 mm each)', 12, 700, GREY, ls=1)
s.raw(f'<image href="{b64img("../calc/c02_view_object.png")}" x="470" y="424" width="300" height="231" preserveAspectRatio="xMidYMid slice"/>')
s.poly([(470, 424), (770, 424), (770, 655), (470, 655)], 'none', GREY_L, 1)
s.note((800, 450), ['Top edge climbs from 38 mm at the crease', 'to 88 mm at the free ends. Seen from the', 'seat that slope is eaten by perspective and', 'the card reads as one level banner.', '', 'Both leaves are printed, the name is cut', 'across the crease, stretched 1.4x.'], 13)
# flat net
nx, ny, ns = 48, 668, 2.2
s.text((nx, ny - 12), 'FLAT PRINT, AS CUT (164 x 88 mm)', 12, 700, GREY, ls=1)
s.raw(f'<image href="{b64img("../calc/c02_net.png")}" x="{nx}" y="{ny}" width="{int(2*K.WL*ns)}" height="{int(K.HH*ns)}"/>')
s.line((nx + K.WL*ns, ny - 4), (nx + K.WL*ns, ny + K.HH*ns + 4), RED, 1.2, dash='6 4')
s.text((nx + K.WL*ns + 6, ny + K.HH*ns + 18), 'valley fold', 11, 600, RED)
s.note((480, 720), ['Why it works: each leaf is a different distance', 'and angle from your eye, so the print is pre-stretched', 'leaf by leaf (ray from the eye through the name, hit the leaf).', 'Move 330 mm sideways and one leaf turns edge-on.', '', 'Back of the card, seen from across the table: the', 'seat number, big. Finding your seat = sitting down.'], 13)
s.save('../svg/02_sit_down.svg')
