"""Concept 04 CHEERS - scanimation. Simulate a 4-frame barrier-grid animation: interlaced print + slotted sleeve."""
import numpy as np, math
from PIL import Image, ImageDraw, ImageFilter
PPM = 20           # px per mm
W_MM, H_MM = 100, 56
N = 3; PITCH = 2.1; SLICE = PITCH / N     # mm
W, H = int(W_MM * PPM), int(H_MM * PPM)

def glass(d, cx, face, y0, col=0):
    # tumbler silhouette: trapezoid (wider at top), face = +1 faces right, -1 left (tilted slightly)
    w_top, w_bot, hh = 15, 11, 26
    pts = [(cx - w_top/2, y0), (cx + w_top/2, y0), (cx + w_bot/2, y0 + hh), (cx - w_bot/2, y0 + hh)]
    d.polygon([(x * PPM, y * PPM) for x, y in pts], fill=255)
    # inner liquid line (cut out)
    pts2 = [(cx - w_top/2 + 2, y0 + 8), (cx + w_top/2 - 2, y0 + 8), (cx + w_bot/2 - 1.6, y0 + hh - 2), (cx - w_bot/2 + 1.6, y0 + hh - 2)]
    d.polygon([(x * PPM, y * PPM) for x, y in pts2], fill=0)

def frame(k):
    im = Image.new('L', (W, H), 0); d = ImageDraw.Draw(im)
    gap = [34, 14, 4][k]
    ya = 22
    glass(d, W_MM / 2 - gap / 2 - 7.5 + (0 if k < 2 else 1.5), 1, ya)
    glass(d, W_MM / 2 + gap / 2 + 7.5 - (0 if k < 2 else 1.5), -1, ya)
    if k == 2:     # clink sparks
        cx = W_MM / 2
        for a in (-60, -30, 0, 30, 60):
            ang = math.radians(-90 + a)
            x0, y0 = cx + 5 * math.cos(ang), 20 + 5 * math.sin(ang)
            x1, y1 = cx + 14 * math.cos(ang), 20 + 14 * math.sin(ang)
            d.line([(x0 * PPM, y0 * PPM), (x1 * PPM, y1 * PPM)], fill=255, width=int(1.6 * PPM))
    return np.array(im) > 127

frames = [frame(k) for k in range(N)]
# interlace: slice j of width SLICE shows frame j mod N
sl = int(round(SLICE * PPM))
inter = np.zeros((H, W), bool)
for x in range(W):
    j = (x // sl) % N
    inter[:, x] = frames[j][:, x]
def view(offset_slices):
    out = np.zeros((H, W, 3), np.uint8); out[:] = (20, 20, 20)       # black barrier
    vis = ((np.arange(W) // sl) % N) == (offset_slices % N)
    for x in np.nonzero(vis)[0]:
        out[:, x] = np.where(inter[:, x, None], np.array([20, 20, 20]), np.array([254, 237, 149]))
    return Image.fromarray(out)
if __name__ == '__main__':
    for k in range(N):
        view(k).save(f'../calc/c04_view{k}.png')
    # bar fill: what the guest perceives (slit gaps appear as lines through lemon); softened version = box blur to emulate eye
    Image.fromarray(np.where(inter, 20, 254).astype(np.uint8)).save('../calc/c04_interlaced.png')
    for k in range(N):
        im = view(k).filter(ImageFilter.GaussianBlur(sl * 0.9)).resize((W // 2, H // 2), Image.LANCZOS)
        # emulate lemon bars hiding: lemon barrier colour = background; eye averages 1/4 density. Contrast-stretch for illustration
        a = np.array(im).astype(float); a = np.clip(a * 1.9, 0, 255) if False else a
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(f'../calc/c04_eye{k}.png')
    print('slice', SLICE, 'mm; pitch', PITCH, 'mm; sleeve travel per frame', SLICE, 'mm')
