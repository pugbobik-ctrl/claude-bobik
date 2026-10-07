from lib import *
import numpy as np
s = S()
s.header('08', 'NOD', 'A tiny lamp that cannot fall over. Flick it and it nods to you, rocks for a few seconds, and settles facing you again.')
RB, HC = 30.0, 85.0
mh, mc, mw = 3.0, 4.0, 15.0
com = (-0.5 * RB * mh + (HC / 3) * mc - 24 * mw) / (mh + mc + mw)
g = 9810.0; k = 28.0
T = 2 * math.pi * math.sqrt((k**2 + (RB + com) ** 2) / (g * -com))
sc = 2.2
gy = 440
def pose(cx, th, label, name_on=True):
    # O at (cx - RB*th, RB); rotate shape by th (clockwise positive)
    def tf(x, y):  # shape coords: x right, y up from O
        c, sn = math.cos(th), math.sin(th)
        xr = x * c + y * sn; yr = -x * sn + y * c
        return (cx - RB * th + xr, RB + yr)
    def P(x, y):
        X, Y = tf(x, y); return (X * sc, gy - Y * sc)
    # cone body
    s.poly([P(-RB, 0), P(RB, 0), P(0, HC)], LEMON, INK, 2)
    # hemisphere
    arc = [P(RB * math.cos(a), -RB * math.sin(a)) for a in np.linspace(0, math.pi, 40)]
    s.poly(arc, LEMON_D, INK, 2)
    # weight and CoM
    wx = P(0, -24); s.circle(wx, 9, INK, INK, 1)
    cm = P(0, com); s.circle(cm, 4, RED, RED, 1)
    # name along axis
    X0, Y0 = P(0, 8); X1, Y1 = P(0, HC - 6)
    ang = math.degrees(math.atan2(Y1 - Y0, X1 - X0))
    s.raw(f'<text transform="translate({X0:.1f} {Y0:.1f}) rotate({ang:.1f})" x="0" y="0" font-size="{8.6*sc*0.62:.1f}" font-weight="700" fill="{INK}" dy="{3.3*sc*0.62:.1f}">Sophia Zhuravkova</text>') if False else None
    if ang < -90 or ang > 90:
        X0, Y0 = X1, Y1; ang += 180
    s.raw(f'<text transform="translate({X0:.1f} {Y0:.1f}) rotate({ang:.1f})" font-size="{8.2*sc*0.78:.1f}" font-weight="700" fill="{INK}" dy="{-3.3*sc*0.0:.1f}" text-anchor="start" dominant-baseline="middle">Sophia Zhuravkova</text>')
    # contact marker
    s.circle((cx * sc - RB * th * sc, gy), 2.5, INK, INK, 1)
    s.text((cx * sc - RB * th * sc, gy + 34), label, 12, 700, GREY, 'middle', ls=1)
s.line((40, gy), (760, gy), INK, 1.6)
pose(64, -0.45, 'FLICKED TOWARD YOU')
pose(182, 0.0, 'AT REST')
pose(300, 0.45, 'RECOIL')
s.text((800, 200), 'WHY IT RIGHTS ITSELF', 12, 700, GREY, ls=1)
# stability numbers
s.note((800, 225), [f'Centre of mass (red) sits {-com:.1f} mm below the ball centre,', 'so any tilt lifts it: it always rolls back.', f'Rocking period about {T:.2f} s, fading over 3 to 4 s.', f'Masses: shell 3 g, cone 4 g, steel weight 15 g.'], 13)
# flat pattern
s.text((48, 590), 'FLAT PARTS (mm)', 12, 700, GREY, ls=1)
Lsl = math.hypot(RB, HC); ang_s = 360 * RB / Lsl
fx, fy, fs = 190, 610, 1.3
a0 = math.radians(90 - ang_s / 2); 
pts = [(fx, fy)] + [(fx + Lsl * fs * math.cos(math.radians(90 - ang_s/2 + ang_s * i / 30)) , fy + Lsl * fs * math.sin(math.radians(90 - ang_s/2 + ang_s * i / 30))) for i in range(31)]
s.poly(pts, LEMON, INK, 1.8)
s.text((fx, fy + Lsl * fs + 22), f'cone: slant {Lsl:.0f}, sector {ang_s:.0f} deg, 8 mm glue lap', 12, 500, INK)
# gores
for i in range(3):
    gx = 520 + i * 44; gy0 = 620
    gl = math.pi * RB / 2
    left = [(gx - 15 * math.sin(math.pi * j / 20) * 0.62, gy0 + gl * 1.3 * j / 20) for j in range(21)]
    right = [(gx + 15 * math.sin(math.pi * j / 20) * 0.62, gy0 + gl * 1.3 * j / 20) for j in range(20, -1, -1)]
    s.poly(left + right, LEMON_D, INK, 1.2)
s.text((500, 620 + 47 * fs + 40), '6 gores for the ball (3 shown)', 12, 500, INK)
s.note((48, 790), ['Cone and ball are one lemon sheet. Cone: 85 mm, ball 60 mm across; name printed up the axis.', 'The weight is a 15 g steel washer stack glued in the ball. A fingertip flick sets it rocking;', 'with 6 on a table the room fills with small nodding lamps.', '', 'The table lamps are cones. These are the same cone, nodding.'], 13)
s.save('../svg/08_nod.svg')
