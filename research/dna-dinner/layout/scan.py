"""Barrier-grid (scanimation) frames for the mezzanine panel: DINNER melting, vertical slits."""
import sys; sys.path.insert(0, '.')
from lib import *
fr = [cv2.imread(os.path.join(GEN, f'melt{k}.png'), 0).astype(np.float32)/255 for k in range(1, 5)]
x0, x1, y0, y1 = 70, 1420, 70, 760
fr = [f[y0:y1, x0:x1] for f in fr]
h, w = fr[0].shape
Y = np.array([0xFE, 0xED, 0x95][::-1], np.float32); D = np.array([0x2B, 0x14, 0x0A][::-1], np.float32)
s = 9                                     # stripe width in px of this image
cols = (np.arange(w) // s) % 4
inter = np.zeros((h, w), np.float32)
for k in range(4): inter[:, cols == k] = fr[k][:, cols == k]
def rgb(a, fg=Y, bg=D): return (bg*(1-a[..., None]) + fg*a[..., None]).astype(np.uint8)
cv2.imwrite(os.path.join(GEN, 'scan_inter.png'), rgb(inter))
for k in range(4):
    view = inter.copy(); bar = cols != k
    img = rgb(view); img[:, bar] = (np.array([0x5A, 0x2F, 0x1B][::-1])).astype(np.uint8)  # barrier: crust card
    cv2.imwrite(os.path.join(GEN, f'scan_view{k}.png'), img)
    cv2.imwrite(os.path.join(GEN, f'scan_frame{k}.png'), rgb(fr[k]))
print(h, w)
