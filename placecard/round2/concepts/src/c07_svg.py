from lib import *
import numpy as np
s = S()
s.header('07', 'SKIRT', 'A flat lemon disc under the napkin. Clip it on the glass stem and it unwinds into a spiral lampshade with your name running down it.')
R0, PITCH, NT = 9.0, 12.0, 6
RMAX = R0 + PITCH * NT
HT = 92.0
NAME = 'Sophia Zhuravkova   '
# ---------- flat disc ----------
fx, fy, fs = 250, 370, 2.0
th = np.linspace(0, 2 * math.pi * NT, 1400)
def sp(r_off, t): return (fx + (R0 + PITCH * t / (2 * math.pi) + r_off) * fs * np.cos(t), fy + (R0 + PITCH * t / (2 * math.pi) + r_off) * fs * np.sin(t))
s.text((48, 150), 'FLAT, AS DELIVERED: 160 mm disc, one spiral cut', 12, 700, GREY, ls=1)
s.circle((fx, fy), RMAX * fs + 2, LEMON, INK, 1.5)
x, y = sp(0, th)
s.polyline(list(zip(x, y)), RED, 1.4)
xm, ym = sp(PITCH / 2 - 1.8, th)
pd = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in zip(xm, ym))
s.raw(f'<defs><path id="spir" d="{pd}"/></defs>')
s.raw(f'<text font-size="{6.8*fs}" font-weight="700" fill="{INK}" letter-spacing="0.5"><textPath href="#spir">{NAME*8}</textPath></text>')
s.circle((fx, fy), R0 * fs * 0.8, PAPER, INK, 1.2)
s.text((fx + RMAX * fs + 16, fy - 40), 'cut (red)', 12, 600, RED)
s.text((fx + RMAX * fs + 16, fy - 22), 'keyhole at the', 12, 500); s.text((fx + RMAX * fs + 16, fy - 6), 'centre clips on', 12, 500); s.text((fx + RMAX * fs + 16, fy + 10), 'the stem', 12, 500)
# ---------- hanging ----------
cam = Cam(az=-28, el=20, s=1.9, ox=880, oy=660)
cloth(s, cam, -120, 120, -110, 110, 0)
# glass
wineglass(s, cam, (0, 0), 0)
items = []
def pt(t):
    r = R0 + PITCH * t / (2 * math.pi)
    z = HT * (1 - t / (2 * math.pi * NT)) + 1.0
    return np.array([r * math.cos(t), r * math.sin(t), z])
drz = -HT / (2 * math.pi * NT)   # dz per radian
drr = PITCH / (2 * math.pi)
chars = list(NAME)
steps = 900
ts = np.linspace(0, 2 * math.pi * NT, steps)
band_w = PITCH - 1.4
cinfo = []
# letters along centre of ribbon
t = 0.4; ci = 0
while t < 2 * math.pi * NT - 0.5:
    ch = chars[ci % len(chars)]; ci += 1
    r = R0 + PITCH * t / (2 * math.pi)
    adv = text_width(ch, 6.6, 700) + 0.4 if ch != ' ' else 2.6
    if ch != ' ': cinfo.append((t, ch))
    t += adv / r
quads = []
for i in range(steps - 1):
    p0, p1 = pt(ts[i]), pt(ts[i + 1])
    def band(p, t):
        d = np.array([drr * math.cos(t) , drr * math.sin(t), drz]); d /= np.linalg.norm(d)
        return d
    d0, d1 = band(p0, ts[i]), band(p1, ts[i + 1])
    q = [p0 + d0 * band_w / 2 * -1 + d0 * 0, p1 - d1 * band_w / 2, p1 + d1 * band_w / 2, p0 + d0 * band_w / 2]
    # shift so ribbon sits between turns: centre offset not needed
    pts2 = [cam.p(*v) for v in q]
    depth = -(((p0[0]+p1[0])/2) * math.sin(cam.az) + ((p0[1]+p1[1])/2) * math.cos(cam.az))    # larger = nearer? y1 = x sin + y cos ; larger y1 = farther
    depth = ((p0[0]+p1[0])/2) * math.sin(cam.az) + ((p0[1]+p1[1])/2) * math.cos(cam.az)
    quads.append((depth, pts2, ts[i]))
# glass behind/in front: draw ribbon back-to-front (largest y1 first)
quads.sort(key=lambda a: -a[0])
for d, pts2, tt in quads:
    s.poly(pts2, LEMON, LEMON, 0.7)
    s.line(pts2[0], pts2[1], INK, 0.9, cap='butt'); s.line(pts2[3], pts2[2], INK, 0.9, cap='butt')
# letters: draw only front-facing
for t, ch in sorted(cinfo, key=lambda a: 0):
    pass
letters = []
for t, ch in cinfo:
    p = pt(t); tang = np.array([-(R0 + PITCH*t/(2*math.pi))*math.sin(t) + drr*math.cos(t), (R0 + PITCH*t/(2*math.pi))*math.cos(t) + drr*math.sin(t), drz*(1)]); 
    tang[2] = drz
    # use horizontal tangent
    u = np.array([-math.sin(t), math.cos(t), 0.0])
    v = np.array([drr * math.cos(t), drr * math.sin(t), drz]); v /= np.linalg.norm(v); v = -v   # up the slope (toward apex)
    v = v if v[2] > 0 else -v
    n = np.cross(u, v)
    if n @ np.array([math.cos(t), math.sin(t), 0]) < 0: n = -n
    # camera view direction (toward viewer): in cam coords viewer at -y1 ; world dir ~ (-sin az..., )
    vd = np.array([math.sin(cam.az) * 0 + math.sin(cam.az), -math.cos(cam.az), 0])
    # front facing if outward normal faces viewer: viewer looks along +y1 (rotated); outward normal . (-y1dir) > 0
    y1dir = np.array([math.sin(cam.az), math.cos(cam.az), 0])
    if n @ (-y1dir) > 0.15:
        org = p - v * 2.3
        depth = org @ y1dir
        letters.append((depth, org, u, v, ch))
for depth, org, u, v, ch in sorted(letters, key=lambda a: -a[0]):
    s.face_text(cam, tuple(org), tuple(u), tuple(v), ch, 6.6, 700, INK)
s.text((640, 150), 'CLIPPED ON THE STEM (axonometric, hanging height 92 mm, base 160 mm)', 12, 700, GREY, ls=1)
# note
s.note((48, 660), ['Disc 160 mm, 300 gsm card, laser-cut spiral, ribbon 11 mm, pitch 12 mm, 6 turns.', 'Under the napkin it is a flat lemon disc with a name running in a spiral,', 'a pleasing graphic of its own.', '', 'Lift it by the centre, clip the keyhole on the stem under the bowl,', 'let go: the turns fall apart into a cone, 92 mm tall. Ribbon length 1.6 m.', 'The name repeats about 17 times; one is always facing you.'], 13)
s.save('../svg/07_skirt.svg')
