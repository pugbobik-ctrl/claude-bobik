from lib import *
import numpy as np
s = S()
s.header('11', 'JACK', 'A folded napkin sits on the table. Lift it and a lemon card springs up from underneath, announcing the name.')
Lf, c, h, bx = 70.0, 55.0, 5.0, -38.0
def ell(psi):
    af = np.array([c * math.cos(psi) - h * math.sin(psi), c * math.sin(psi) + h * math.cos(psi)])
    return np.linalg.norm(af - np.array([bx, 0]))
psis = np.radians(np.arange(0, 150, 0.5)); ls = np.array([ell(p) for p in psis]); peq = math.radians(70.0)
print('eq angle', math.degrees(peq), 'len0', ls[0], 'len min', ls.min())
sc = 3.0
def state(x0, psi, napkin, label, sub):
    gy = 500
    P = lambda x, z: (x0 + x * sc, gy - z * sc)
    # table
    s.line((x0 - 70 * sc, gy), (x0 + 80 * sc, gy), INK, 1.4)
    # base card (extends behind hinge by 55, ahead 30)
    s.poly([P(-55, 0), P(30, 0), P(30, 1.2), P(-55, 1.2)], LEMON_D, INK, 1.4)
    # flap
    def F(u, v): return P(u * math.cos(psi) - v * math.sin(psi), u * math.sin(psi) + v * math.cos(psi) + 1.2)
    s.poly([F(0, 0), F(Lf, 0), F(Lf, 1.2), F(0, 1.2)], LEMON, INK, 1.6)
    # tab standoff
    s.line(F(c, 0), F(c, h), INK, 1.6)
    ab = P(bx, 1.2); af = F(c, h)
    s.line(ab, af, RED, 2.2)
    s.circle(ab, 3, RED, RED, 1); s.circle(af, 3, RED, RED, 1)
    s.circle(P(0, 1.2), 3.2, INK, INK, 1)
    sa = F(45, 0); sb = P(35, 1.2)
    slack = math.dist(sa, sb) < 46.6 * sc - 1
    s.line(sa, sb, INK, 1.4, dash='4 3' if slack else None)
    s.circle(sa, 2.6, INK, INK, 1); s.circle(sb, 2.6, INK, INK, 1)
    if napkin == 'on':
        s.path(f'M{P(-30,3)[0]},{P(-30,3)[1]} q-4,-4 0,-9 l 0,0 h {80*sc} q4,-3 0,-9 z', 'none', INK, 0)
        s.poly([P(-22, 1.5), P(66, 1.5), P(66, 14), P(-22, 14)], WHITE, GREY, 1.6)
        s.line(P(-22, 8), P(66, 8), GREY_L, 1)
        s.text(P(22, 22), 'napkin', 12, 600, GREY, 'middle')
    elif napkin == 'lift':
        s.poly([P(-45, 52), P(24, 61), P(30, 66), P(-38, 58)], WHITE, GREY, 1.4, dash='5 4')
        s.text(P(-5, 74), 'napkin lifted away', 12, 600, GREY, 'middle')
    s.text((x0 + 12 * sc, gy + 36), label, 13, 700, INK, 'middle')
    s.text((x0 + 12 * sc, gy + 56), sub, 12, 500, GREY, 'middle')
state(210, 0.0, 'on', 'IN THE KITCHEN', 'flap pinned flat by the napkin, band taut')
state(560, math.radians(32), 'lift', 'THE LIFT', 'band releases the flap')
state(900, peq, None, 'THE POP', f'strap goes taut at 70 deg: card stands')
s.text((48, 160), 'SIDE SECTION AT 3:1, base card on the table, the red line is the rubber band', 12, 700, GREY, ls=1)
# front view
fx, fy, fs = 70, 600, 2.4
s.text((fx, fy - 14), 'GUEST VIEW OF THE FLAP, 100 x 70 mm', 12, 700, GREY, ls=1)
s.poly([(fx, fy), (fx + 100 * fs, fy), (fx + 100 * fs, fy + 70 * fs), (fx, fy + 70 * fs)], LEMON, INK, 1.8)
s.text((fx + 50 * fs, fy + 34 * fs), 'Sophia', 11 * fs, 700, INK, 'middle'); s.text((fx + 50 * fs, fy + 50 * fs), 'Zhuravkova', 11 * fs, 700, INK, 'middle')
s.text((fx + 50 * fs, fy + 64 * fs), 'DINNER  10.10.2026', 4.6 * fs, 600, INK, 'middle', ls=1.5)
s.poly([(fx + 46 * fs, fy + 70 * fs - 12), (fx + 54 * fs, fy + 70 * fs - 12), (fx + 54 * fs, fy + 70 * fs - 6), (fx + 46 * fs, fy + 70 * fs - 6)], 'none', 'none', 0)
s.note((520, 650), [f'Band loop 2 mm wide: {ls[0]:.0f} mm stretched when flat, {ell(peq):.0f} mm when upright.', 'The anchor tab on the flap stands 5 mm off the card so the band', 'pulls the flap over the hinge the moment the weight is gone.', 'The napkin (about 40 g) is the weight. No spring steel, no glue,', 'one die-cut sheet, a 47 mm paper strap (black dot to dot) as the stop, one band.', '', 'Risk: the napkin must not be refolded on top by staff:', 'brief the floor, or print LIFT on the napkin band.'], 13)
s.save('../svg/11_jack.svg')
