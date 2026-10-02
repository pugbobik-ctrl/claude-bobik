"""Fork and knife silhouettes (top view, mm grid) and underlays: plain offset like ref 9,
and an offset whose edge carries the dents of the DINNER top edge."""
import sys; sys.path.insert(0, '.')
from lib import *
PX = 6                          # px per mm
def canvas(wmm, hmm): return np.zeros((int(hmm*PX), int(wmm*PX)), np.float32)
def poly(img, pts):
    cv2.fillPoly(img, [np.round(np.array(pts)*PX).astype(np.int32)], 1.0)
def smooth(img, s=1.2):
    return (cv2.GaussianBlur(img, (0, 0), s*PX) > 0.5).astype(np.float32)
def knife(cx, y0):
    """vertical table knife, tip at y0, length ~232 mm"""
    k = canvas(300, 330)
    blade = np.zeros_like(k)
    cv2.ellipse(blade, (int(cx*PX), int((y0+14)*PX)), (int(9*PX), int(14*PX)), 0, 180, 360, 1.0, -1)
    poly(blade, [(cx-9, y0+14), (cx+9, y0+14), (cx+9, y0+100), (cx-9, y0+100)])
    # spine slopes toward the tip: shave the upper left
    cut = np.zeros_like(k)
    poly(cut, [(cx-30, y0-5), (cx-1, y0-5)] + [(cx-1 - 8.5*np.sin(t*np.pi/2), y0 + 70*t) for t in np.linspace(0, 1, 40)] + [(cx-30, y0+70)])
    blade = blade * (1 - cut)
    k = np.maximum(k, blade)
    poly(k, [(cx-9, y0+99), (cx+9, y0+99), (cx+5, y0+113), (cx-5, y0+113)])   # bolster
    poly(k, [(cx-5, y0+112), (cx+5, y0+112), (cx+7.4, y0+180), (cx+7.0, y0+224), (cx-7.0, y0+224), (cx-7.4, y0+180)])
    cv2.circle(k, (int(cx*PX), int((y0+224)*PX)), int(7.0*PX), 1.0, -1)
    return smooth(k, 0.7)
def fork(cx, y0):
    f = canvas(300, 330)
    # head
    hw = 13.0
    head = [(cx-hw, y0+34), (cx+hw, y0+34), (cx+hw-1, y0+50), (cx+6, y0+64), (cx+4.2, y0+82), (cx-4.2, y0+82), (cx-6, y0+64), (cx-hw+1, y0+50)]
    poly(f, head)
    tw = 4.4; gap = (2*hw - 4*tw)/3
    for i in range(4):
        x = cx - hw + i*(tw+gap)
        poly(f, [(x, y0+4), (x+tw, y0+4), (x+tw, y0+40), (x, y0+40)])
        cv2.ellipse(f, (int((x+tw/2)*PX), int((y0+4)*PX)), (int(tw/2*PX), int(3*PX)), 0, 0, 360, 1.0, -1)
    # neck and handle
    poly(f, [(cx-4.2, y0+80), (cx+4.2, y0+80), (cx+7.6, y0+168), (cx+7.2, y0+200), (cx-7.2, y0+200), (cx-7.6, y0+168)])
    cv2.circle(f, (int(cx*PX), int((y0+199)*PX)), int(7.3*PX), 1.0, -1)
    f = smooth(f, 0.45)
    return f
K = knife(185, 34); Fk = fork(115, 52)
both = np.clip(K + Fk, 0, 1)
dist = cv2.distanceTransform((1 - (both > 0.5)).astype(np.uint8), cv2.DIST_L2, 5) / PX   # mm
plain = (dist <= 7).astype(np.float32)
plain = smooth(cv2.morphologyEx(plain, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (16*PX+1, 16*PX+1))), 1.0)
# dough edge: modulate the offset with the DINNER top-edge profile running along the contour
F = load('flat'); top = np.array(F['top'], np.float32)
prof = top[347:955]; prof = (prof - prof.min()) / (prof.max() - prof.min())   # 0 = bulge top, 1 = dent bottom
cnts, _ = cv2.findContours((plain > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
dough = np.zeros_like(plain)
period = 150.0                                                      # mm of contour per copy of the I-N-N-E edge
for cn in cnts:
    c = cn[:, 0, :].astype(np.float32)
    seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))] / PX
    tg = np.roll(c, -10, axis=0) - np.roll(c, 10, axis=0)
    nrm = np.stack([tg[:, 1], -tg[:, 0]], 1); nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-6
    test = c + nrm*4
    inside = np.array([plain[int(min(max(y,0),plain.shape[0]-1)), int(min(max(x,0),plain.shape[1]-1))] for x, y in test])
    if inside.mean() > 0.5: nrm = -nrm
    idx = ((seg % period) / period * (len(prof) - 1)).astype(int)
    disp = (0.3 - prof[idx]) * 7.5                                   # mm; V-dents go inward
    k = int(0.8*PX)*3; disp = np.convolve(np.r_[disp[-k:], disp, disp[:k]], cv2.getGaussianKernel(2*k+1, 0.8*PX).ravel(), 'same')[k:-k]
    pts = c + nrm * disp[:, None] * PX
    cv2.fillPoly(dough, [np.round(pts).astype(np.int32)], 1.0)
dough = smooth(dough, 0.35)
out = {'px': PX, 'w': both.shape[1], 'h': both.shape[0],
       'knife': trace(K, 'knife', scale=1, smooth=0.3), 'fork': trace(Fk, 'fork', scale=1, smooth=0.3),
       'plain': trace(plain, 'u_plain', scale=1, smooth=0.3), 'dough': trace(dough, 'u_dough', scale=1, smooth=0.3)}
save('cutlery', out)
viz = np.dstack([plain*120 + dough*60, dough*200, both*255]).astype(np.uint8)
cv2.imwrite(os.path.join(GEN, 'cutlery.png'), viz)
print(out['w'], out['h'])
