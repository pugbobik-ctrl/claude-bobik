from lib import *
import c03_calc as K
s = S()
s.header('03', 'DECODER RING', 'The napkin ring is the key. A lemon card of swoops looks like abstract calligraphy until a mirror ring stands on it.')
def img(f, x, y, w, h, label, sub, c=INK):
    s.raw(f'<image href="{b64img("../calc/" + f)}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>')
    s.poly([(x, y), (x+w, y), (x+w, y+h), (x, y+h)], 'none', GREY_L, 1)
    s.text((x, y - 10), label, 12, 700, GREY, ls=1); s.text((x, y + h + 20), sub, 12, 500, c)
img('c03_print_crop.png', 48, 150, 340, 274, 'THE CARD ALONE', 'what arrives at the seat: swoops', INK)
img('c03_view_seat.png', 410, 150, 340, 272, 'RING STANDING ON IT, SEEN FROM THE SEAT', 'ray-traced: name resolves in the mirror')
img('c03_view_side.png', 772, 150, 380, 272, 'SAME RING FROM THE NEXT SEAT', 'tilts and slides away: a seat-specific trick')
# side section
sx0, sy0, k = 60, 870, 0.52
def SP(y, z): return (sx0 + (y + 450) * k, sy0 - z * k)
s.text((48, 560), 'SIDE SECTION, guest at the left (true geometry, mm)', 12, 700, GREY, ls=1)
s.line(SP(-450, 0), SP(110, 0), INK, 2)
eye = (-450, 430)
s.circle(SP(*eye), 6, INK, INK, 1); s.text((SP(*eye)[0] + 12, SP(*eye)[1] + 4), 'eye 430 up, 450 away', 12, 600)
s.poly([SP(-K.R, 0), SP(K.R, 0), SP(K.R, K.H), SP(-K.R, K.H)], '#d3d6da', INK, 1.5)
import numpy as np
for z, col in ((8, '#c8281e'), (42, '#1d6fb8')):
    phi = np.array([0.0]); P, Q = K.reflect_to_card(phi, np.array([float(z)]))
    q = Q[0]; p = P[0]
    s.line(SP(*eye), SP(q[1], q[2]), col, 1.3); s.line(SP(q[1], q[2]), SP(p[1], p[2]), col, 1.3)
    s.circle(SP(p[1], p[2]), 3.5, col, col, 1)
    s.text((SP(p[1], p[2])[0] + (-18 if z>20 else 18), SP(p[1], p[2])[1] + 20), f'{p[1]:.0f}', 11, 600, col, 'middle')
s.text(SP(40, 20), 'mirror ring', 12, 600); s.text(SP(-330, 18), 'card (lemon, printed)', 12, 600, GREY)
s.note((420, 590), ['Reflect the eye ray off the cylinder: where it lands on the card', 'is where that letter of the name must be printed.', 'Bottom of the ring (red) lands 34 mm in front of it, the top', '(blue) 72 mm, so letters fan out into arcs.', '1500 x 500 rays computed; ring r 26, h 50.'], 13)
# net of ring
nx, ny, ns = 420, 720, 2.0
s.text((nx, ny - 14), 'THE RING, FLAT (mirror board, 2 x 12 tab, 50 high)', 12, 700, GREY, ls=1)
Wn = 2 * math.pi * K.R
s.poly([(nx, ny), (nx + Wn*ns, ny), (nx + Wn*ns, ny + K.H*ns), (nx, ny + K.H*ns)], '#d3d6da', INK, 1.6)
s.poly([(nx + Wn*ns, ny + 6), (nx + (Wn+12)*ns, ny + 12), (nx + (Wn+12)*ns, ny + (K.H-12)*ns), (nx + Wn*ns, ny + (K.H-6)*ns)], '#d3d6da', INK, 1.6)
s.text((nx + 8, ny + 26), 'mirror side out; lemon inside', 12, 500, INK)
s.line((nx, ny + K.H*ns + 18), (nx + Wn*ns, ny + K.H*ns + 18), GREY, 1); s.text((nx + Wn*ns/2, ny + K.H*ns + 34), '163', 12, 600, GREY, 'middle')
s.note((810, 750), ['Guest rolls the napkin through the ring,', 'sets it on the card: name appears in the metal.', 'Card 160 x 130 mm, rounded.', 'Name: 5.7 mm cap height in the mirror.'], 13)
s.save('../svg/03_decoder_ring.svg')
