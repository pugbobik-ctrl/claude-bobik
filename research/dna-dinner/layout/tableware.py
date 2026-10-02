"""Flat paper doubles of the table (side views, like client ref 6): glass, carafe, cup, bowl, bun,
plus a plate whose rim carries the DINNER dents. Units: mm, PX px per mm."""
import sys; sys.path.insert(0, '.')
from lib import *
PX = 5
def cv(w, h): return np.zeros((int(h*PX), int(w*PX)), np.float32)
def P(pts): return np.round(np.array(pts)*PX).astype(np.int32)
def sm(img, s=0.8): return (cv2.GaussianBlur(img, (0, 0), s*PX) > 0.5).astype(np.float32)
def lathe(profile, w, h, cx=None, soft=0.0):
    """profile: list of (y, halfwidth) top->bottom; mirrored around cx; soft = smoothing in mm"""
    img = cv(w, h); cx = w/2 if cx is None else cx
    ys = np.arange(profile[0][0], profile[-1][0] + 0.01, 0.25)
    hw = np.interp(ys, [p[0] for p in profile], [p[1] for p in profile])
    if soft:
        k = int(soft*4*4); g = cv2.getGaussianKernel(2*k+1, soft*4).ravel()
        hw = np.convolve(np.r_[np.full(k, hw[0]), hw, np.full(k, hw[-1])], g, 'same')[k:-k]
    pts = [(cx + a, y) for y, a in zip(ys, hw)] + [(cx - a, y) for y, a in zip(ys[::-1], hw[::-1])]
    cv2.fillPoly(img, [P(pts)], 1.0); return img
out = {}
# wine glass, 210 mm tall
g = lathe([(8, 38), (30, 41), (60, 40), (85, 33), (102, 18), (110, 4), (112, 3.2), (178, 3.2), (186, 10), (192, 34), (197, 36), (200, 0.1)], 100, 210)
out['glass'] = sm(g, 0.6)
# carafe, 260 mm
c = lathe([(10, 16), (14, 17), (18, 14.5), (44, 14), (72, 24), (110, 50), (160, 63), (205, 60), (236, 49), (250, 42), (252, 0.1)], 150, 262, soft=6)
out['carafe'] = sm(c, 1.0)
# cup with handle, side view
cp = cv(150, 110)
cv2.fillPoly(cp, [P([(20, 16), (110, 16), (104, 80), (92, 96), (38, 96), (26, 80)])], 1.0)
cv2.ellipse(cp, (int(116*PX), int(48*PX)), (int(20*PX), int(24*PX)), 0, 0, 360, 1.0, -1)
cv2.ellipse(cp, (int(116*PX), int(48*PX)), (int(10*PX), int(14*PX)), 0, 0, 360, 0.0, -1)
cv2.fillPoly(cp, [P([(14, 100), (116, 100), (110, 106), (20, 106)])], 1.0)
out['cup'] = sm(cp, 0.8)
# bowl, side view
b = lathe([(10, 70), (13, 72), (30, 68), (46, 56), (58, 38), (63, 26), (64, 22), (66, 25), (71, 25), (72, 0.1)], 160, 80, soft=3)
out['bowl'] = sm(b, 0.8)
# bun, top view: soft round loaf like the photo on the poster, cut from the printed bun
bn = cv(170, 150); yy, xx = np.mgrid[0:bn.shape[0], 0:bn.shape[1]] / PX
th = np.arctan2(yy - 75, xx - 85); rr = np.hypot((xx - 85)/1.12, yy - 75)
bn = (rr <= 62 + 4*np.sin(3*th + 0.6) + 2.5*np.sin(5*th + 1.3)).astype(np.float32)
out['bun'] = sm(bn, 1.2)
# plate, top view: rim with DINNER dents (I-N-N-E top edge, wrapped 3 times around)
F = load('flat'); top = np.array(F['top'], np.float32)
prof = top[347:955]; prof = (prof - prof.min())/(prof.max() - prof.min())
S = 290; pl = cv(S, S); yy, xx = np.mgrid[0:pl.shape[0], 0:pl.shape[1]] / PX
dx, dy = xx - S/2, yy - S/2; r = np.hypot(dx, dy); th = (np.arctan2(dy, dx) + np.pi) / (2*np.pi)
idx = ((th*3) % 1 * (len(prof)-1)).astype(int)
R = 132 - prof[idx]*11
out['plate'] = sm((r <= R).astype(np.float32), 0.4)
res = {'px': PX}
for k, v in out.items():
    res[k] = {'d': trace(v, 'tw_' + k, scale=1, smooth=0.25), 'w': v.shape[1]/PX, 'h': v.shape[0]/PX}
    cv2.imwrite(os.path.join(GEN, 'tw_' + k + '.png'), (v*255).astype(np.uint8))
save('tableware', res)
print({k: (round(v['w']), round(v['h'])) for k, v in res.items() if k != 'px'})
