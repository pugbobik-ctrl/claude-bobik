import cv2, numpy as np, json, sys
from lib import *
m = flat_mask(); H, W = m.shape; bw = (m > 0.5).astype(np.uint8)
out = {'W': W, 'H': H, 'pad': PAD}
top = np.array([np.argmax(bw[:, x]) if bw[:, x].any() else H for x in range(W)])
bot = np.array([H - 1 - np.argmax(bw[::-1, x]) if bw[:, x].any() else 0 for x in range(W)])
out['base'] = trace(m, 'base')
# outward offsets (distance transform, rounded)
dist = cv2.distanceTransform((1 - bw).astype(np.uint8), cv2.DIST_L2, 5)
for r in (14, 28, 42, 56):
    f = (dist <= r).astype(np.float32)
    out[f'off{r}'] = trace(f, f'off{r}', smooth=1.2)
# melt frames: few fat rounded drips hanging from the lowest bulges, like the R leg
def lowest_bulges():
    xs = []
    for a, b in [(150, 330), (470, 560), (600, 690), (850, 945), (980, 1150), (1290, 1370)]:
        seg = bot[a:b]; xs.append(a + int(np.argmax(seg)))
    return xs
bx = [235, 640, 1080, 1345]; out['drip_x'] = bx
widths = [96, 78, 104, 88]; order = [0.8, 0.45, 1.0, 0.62]
for k, L in enumerate([0, 70, 140, 215], start=1):
    f = np.zeros((H + 260, W), np.float32); f[:H] = bw
    if L:
        for i, x in enumerate(bx):
            ln = int(L*order[i]); w = widths[i]; yb = int(bot[x]) - 40
            if ln < 20: continue
            cv2.ellipse(f, (x, yb + ln//2), (int(w*0.42), ln//2 + 14), 0, 0, 360, 1.0, -1)
            cv2.circle(f, (x, yb + ln), int(w*0.52), 1.0, -1)
        f = cv2.GaussianBlur(f, (0, 0), 12.0); f = (f > 0.45).astype(np.float32)
        f[:H][(m < 0.5) & (dist == 0)] = f[:H][(m < 0.5) & (dist == 0)]  # keep counters as traced below
        holes = (cv2.morphologyEx(bw, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8)) == 0)
        cnts, hier = cv2.findContours(bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        hm = np.zeros((H, W), np.uint8)
        for c, hh in zip(cnts, hier[0]):
            if hh[3] >= 0: cv2.drawContours(hm, [c], -1, 1, -1)
        f[:H][hm > 0] = 0
    cv2.imwrite(os.path.join(GEN, f'melt{k}.png'), (f*255).astype(np.uint8))
    out[f'melt{k}'] = trace(f, f'melt{k}')
# letter fragments, cut at the waists, cut ends rounded
cuts = [PAD, 347, 448, 701, 955, 1238, W]
out['cuts'] = cuts
cnts, hier = cv2.findContours(bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
HM = np.zeros((H, W), np.uint8)
for c, hh in zip(cnts, hier[0]):
    if hh[3] >= 0: cv2.drawContours(HM, [c], -1, 1, -1)
ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
letters = []
for i in range(6):
    a, b = cuts[i], cuts[i+1]
    f = np.zeros_like(m); f[:, a:b] = m[:, a:b]
    f = cv2.morphologyEx((f > 0.5).astype(np.uint8), cv2.MORPH_OPEN, ker).astype(np.float32)
    f = cv2.GaussianBlur(f, (0, 0), 6.0); f = (f > 0.5).astype(np.float32)
    f[HM > 0] = 0
    ys, xs = np.nonzero(f)
    letters.append({'d': trace(f, f'L{i}'), 'bbox': [int(xs.min()), int(ys.min()), int(xs.max()-xs.min()+1), int(ys.max()-ys.min()+1)]})
    cv2.imwrite(os.path.join(GEN, f'L{i}.png'), (f*255).astype(np.uint8))
out['letters'] = letters
out['top'] = top.tolist(); out['bot'] = bot.tolist()
save('flat', out)
cv2.imwrite(os.path.join(GEN, 'flat.png'), (m*255).astype(np.uint8))
# poster orientation, in poster px (1600x2000)
pm = poster_mask()
save('poster', {'d': trace(pm, 'poster', scale=2, smooth=0.5), 'w': pm.shape[1], 'h': pm.shape[0]})
print('ok', W, H, [l['bbox'] for l in letters])
# per-letter outward offsets for the layered card
for i in range(6):
    f = cv2.imread(os.path.join(GEN, f'L{i}.png'), 0) > 127
    dd = cv2.distanceTransform((~f).astype(np.uint8), cv2.DIST_L2, 5)
    for r in (16, 32):
        out['letters'][i][f'o{r}'] = trace((dd <= r).astype(np.float32), f'L{i}o{r}', smooth=0.9)
save('flat', out)
print('letter offsets ok')
