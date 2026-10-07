"""Concept 03 DECODER RING - cylindrical mirror anamorphosis. x right, y away from guest, z up (mm).
Mirror cylinder radius R height H standing at the origin on the card. Eye E=(0,-450,430)."""
import numpy as np, math, cv2
from PIL import Image, ImageDraw
from lib import *
R, H = 26.0, 50.0
E = np.array([0., -450., 430.])
PHI = math.radians(72)          # visible half-arc used
# image (what the guest should read in the mirror): u across, v up; mm on the mirror surface projection
UX = R * math.sin(PHI)
PPM_I = 20
def make_mask():
    W = int(2 * UX * PPM_I); Hh = int(H * PPM_I)
    im = Image.new('L', (W, Hh), 0); d = ImageDraw.Draw(im)
    lines = [('Sophia', 8.6, 30.0), ('Zhuravkova', 8.6, 18.0)]
    for t, size, base in lines:
        g, w = text_shape(t, size * (UX * 2 * 0.86 / 8.6 / 11.2 if False else 1), 700)
    # fit: width of Zhuravkova to 0.92 * 2UX
    sz = (2 * UX * 0.92) / (text_width('Zhuravkova', 10, 700) / 10)
    for t, base in (('Sophia', 29.0), ('Zhuravkova', 17.0)):
        g, w = text_shape(t, sz, 700)
        for p in geom_polys(g):
            for ring, col in [(p.exterior, 255)] + [(r, 0) for r in p.interiors]:
                d.polygon([((x + UX) * PPM_I, (H - (y + base)) * PPM_I) for x, y in ring.coords], fill=col)
    return np.array(im) > 127, sz
MASK, FSIZE = make_mask()

def reflect_to_card(phi, z):
    Q = np.stack([R * np.sin(phi), -R * np.cos(phi), z], -1)
    n = np.stack([np.sin(phi), -np.cos(phi), np.zeros_like(phi)], -1)
    d = Q - E; d /= np.linalg.norm(d, axis=-1, keepdims=True)
    dp = d - 2 * np.sum(d * n, -1, keepdims=True) * n
    t = -Q[..., 2] / dp[..., 2]
    P = Q + dp * t[..., None]
    return P, Q

def build_print(ppm=8, ext=(-210, 210, -300, 120)):
    x0, x1, y0, y1 = ext
    W = int((x1 - x0) * ppm); Hh = int((y1 - y0) * ppm)
    canvas = np.zeros((Hh, W), np.uint8)
    nphi, nz = 1500, 500
    phis = np.linspace(-PHI, PHI, nphi + 1); zs = np.linspace(0.2, H - 0.2, nz + 1)
    PH, ZZ = np.meshgrid(phis, zs)
    P, Q = reflect_to_card(PH, ZZ)
    px = (P[..., 0] - x0) * ppm; py = (y1 - P[..., 1]) * ppm
    # ink at cell centres: image coords (u = Qx, v = z)
    uc = (Q[:-1, :-1, 0] + Q[1:, 1:, 0]) / 2; vc = (ZZ[:-1, :-1] + ZZ[1:, 1:]) / 2
    ix = np.round((uc + UX) * PPM_I).astype(int); iz = np.round((H - vc) * PPM_I).astype(int)
    ok = (ix >= 0) & (ix < MASK.shape[1]) & (iz >= 0) & (iz < MASK.shape[0])
    ink = np.zeros(uc.shape, bool); ink[ok] = MASK[iz[ok], ix[ok]]
    for j in range(nz):
        for i in range(nphi):
            if not ink[j, i]: continue
            quad = np.array([[px[j, i], py[j, i]], [px[j, i + 1], py[j, i + 1]], [px[j + 1, i + 1], py[j + 1, i + 1]], [px[j + 1, i], py[j + 1, i]]], np.float32)
            cv2.fillConvexPoly(canvas, np.round(quad * 16).astype(np.int32), 255, shift=4)
    return canvas > 127, ext, ppm, P

def render_mirror_view(canvas, ext, ppm, eye=E, target=(0, -20, 28), fov=9, size=(700, 560), ss=2):
    x0, x1, y0, y1 = ext
    eye = np.array(eye, float); target = np.array(target, float)
    f = target - eye; f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1.]); r /= np.linalg.norm(r); u = np.cross(r, f)
    W, Hh = size[0] * ss, size[1] * ss; t = math.tan(math.radians(fov) / 2)
    xs = (np.arange(W) + .5) / W * 2 - 1; ys = 1 - (np.arange(Hh) + .5) / Hh * 2
    X, Y = np.meshgrid(xs * t * (W / Hh), ys * t)
    D = f + X[..., None] * r + Y[..., None] * u; D /= np.linalg.norm(D, axis=-1, keepdims=True)
    col = np.zeros((Hh, W, 3)); cloth = np.array([236, 233, 222.]); lemon = np.array([254, 237, 149.]); ink = np.array([20, 20, 20.])
    def card_color(P):
        ix = np.round((P[..., 0] - x0) * ppm).astype(int); iy = np.round((y1 - P[..., 1]) * ppm).astype(int)
        inside = (ix >= 0) & (ix < canvas.shape[1]) & (iy >= 0) & (iy < canvas.shape[0])
        # lemon card extends over canvas ext, round to disc radius 190 centred at (0,-90)
        c = np.where(inside[..., None], lemon, cloth)
        k = np.zeros(P.shape[:-1], bool); k[inside] = canvas[iy[inside], ix[inside]]
        c[k] = ink
        return c
    # direct table hit
    tt = -eye[2] / D[..., 2]; P = eye + D * tt[..., None]
    col[:] = card_color(P)
    # cylinder hit
    ox, oy = eye[0], eye[1]; dx, dy = D[..., 0], D[..., 1]
    a = dx**2 + dy**2; b = 2 * (ox * dx + oy * dy); c = ox**2 + oy**2 - R**2
    disc = b * b - 4 * a * c; hit = disc > 0
    t1 = np.where(hit, (-b - np.sqrt(np.where(hit, disc, 0))) / (2 * a), np.inf)
    Qz = eye[2] + D[..., 2] * t1
    hit &= (t1 > 0) & (Qz >= 0) & (Qz <= H)
    Q = eye + D * np.where(hit, t1, 0)[..., None]
    n = np.stack([Q[..., 0], Q[..., 1], np.zeros_like(Q[..., 0])], -1) / R
    dp = D - 2 * np.sum(D * n, -1, keepdims=True) * n
    tr = np.where(hit, -Q[..., 2] / np.where(dp[..., 2] == 0, 1e-9, dp[..., 2]), 0)
    Pr = Q + dp * tr[..., None]
    mc = card_color(Pr)
    # mirror: slightly cool, with a vertical sheen band
    sheen = 1 - 0.12 * np.abs(Q[..., 0] / R)
    mc = mc * sheen[..., None]
    mc = np.where(((mc[..., 0] > 200))[..., None], mc * np.array([0.95, 0.97, 1.0]), mc)
    col[hit] = mc[hit]
    # top rim of cylinder (thin dark line): ignore
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).resize(size, Image.LANCZOS)
    return im

if __name__ == '__main__':
    canvas, ext, ppm, P = build_print()
    print('font size', round(FSIZE, 2), 'cap', round(FSIZE * .715, 2))
    print('card footprint of print: x', P[..., 0].min().round(1), P[..., 0].max().round(1), ' y', P[..., 1].min().round(1), P[..., 1].max().round(1))
    Image.fromarray(np.where(canvas, 20, 254).astype(np.uint8)).save('../calc/c03_print_mask.png')
    render_mirror_view(canvas, ext, ppm).save('../calc/c03_view_seat.png')
    render_mirror_view(canvas, ext, ppm, eye=(0, -450, 430), target=(0, -80, 0), fov=26, size=(700, 560)).save('../calc/c03_view_card.png')
    render_mirror_view(canvas, ext, ppm, eye=(260, -380, 430), target=(0, -20, 28), fov=9).save('../calc/c03_view_side.png')
    np.save('../calc/c03_canvas.npy', canvas)
