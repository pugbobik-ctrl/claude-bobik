"""Concept 02 SIT DOWN - vertical V-fold anamorph. World: x right, y away from the guest, z up (mm).
Crease on the vertical axis x=0,y=0. Two leaves open toward the guest at +-ALPHA from the sight line.
Seat eye E=(0,-450,430); image plane y=0 (perpendicular to the sight line, through the crease)."""
import numpy as np, math
from PIL import Image, ImageDraw
from lib import *

E_SEAT = np.array([0., -450., 430.])
ALPHA = math.radians(45); WL = 82.0; Z0 = 38.0
def ztop(s):
    lam = 450.0 / (450.0 - s * math.cos(ALPHA)); return 430.0 - (430.0 - Z0) / lam
HH = ztop(WL)
SIZE = 17.0; PPM = 10
IX0, IX1, IZ0, IZ1 = -90, 90, -70, 60
def make_mask():
    W = (IX1 - IX0) * PPM; H = (IZ1 - IZ0) * PPM
    im = Image.new('L', (W, H), 0); d = ImageDraw.Draw(im)
    for line, base in (('Sophia', 21.0), ('Zhuravkova', 5.0)):
        g, w = text_shape(line, SIZE, 700)
        for p in geom_polys(g):
            for ring, col in [(p.exterior, 255)] + [(r, 0) for r in p.interiors]:
                d.polygon([((x - IX0) * PPM, (IZ1 - (y + base)) * PPM) for x, y in ring.coords], fill=col)
    return np.array(im) > 127
MASK = make_mask()

def ink_at(P):
    lam = (0 - E_SEAT[1]) / (P[..., 1] - E_SEAT[1])
    x = E_SEAT[0] + lam * (P[..., 0] - E_SEAT[0]); z = E_SEAT[2] + lam * (P[..., 2] - E_SEAT[2])
    ix = np.round((x - IX0) * PPM).astype(int); iz = np.round((IZ1 - z) * PPM).astype(int)
    ok = (ix >= 0) & (ix < MASK.shape[1]) & (iz >= 0) & (iz < MASK.shape[0])
    out = np.zeros(P.shape[:-1], bool); out[ok] = MASK[iz[ok], ix[ok]]
    return out

def leaf_point(side, s, z):
    sg = 1 if side == 'R' else -1
    return np.stack([sg * s * math.sin(ALPHA), -s * math.cos(ALPHA), z], -1)

def render_net(ppm=10):
    Wp = int(WL * ppm); Hp = int(HH * ppm)
    out = Image.new('RGB', (2 * Wp, Hp), (254, 237, 149))
    for i, side in enumerate(('L', 'R')):
        s = (np.arange(Wp) + .5) / ppm; z = HH - (np.arange(Hp) + .5) / ppm
        S_, Z_ = np.meshgrid(s if side == 'R' else s[::-1], z)   # L leaf: crease is at its right edge in the net
        P = leaf_point(side, S_, Z_)
        ink = ink_at(P)
        arr = np.zeros((Hp, Wp, 3), np.uint8); arr[:] = (254, 237, 149); arr[ink] = (20, 20, 20)
        zt = np.array([ztop(v) for v in S_[0]]); outside = Z_ > zt[None, :]
        arr[outside] = (247, 245, 239)
        out.paste(Image.fromarray(arr), (i * Wp, 0))
    return out

def render_view(eye, target, fov_deg=14, size=(520, 400), ss=2):
    eye = np.array(eye, float); target = np.array(target, float)
    f = target - eye; f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1.]); r /= np.linalg.norm(r); u = np.cross(r, f)
    W, H = size[0] * ss, size[1] * ss
    t = math.tan(math.radians(fov_deg) / 2)
    xs = (np.arange(W) + .5) / W * 2 - 1; ys = 1 - (np.arange(H) + .5) / H * 2
    X, Y = np.meshgrid(xs * t * (W / H), ys * t)
    D = f[None, None, :] + X[..., None] * r + Y[..., None] * u
    D /= np.linalg.norm(D, axis=-1, keepdims=True)
    best = np.full((H, W), np.inf); col = np.zeros((H, W, 3)); cloth = np.array([236, 233, 222.])
    tt = -eye[2] / D[..., 2]; m = tt > 0
    P = eye + D * np.where(m, tt, 1)[..., None]
    grid = ((np.floor(P[..., 0] / 40) + np.floor(P[..., 1] / 40)) % 2 == 0)
    col[:] = cloth * 0.97; col[m] = cloth; col[m & grid] = cloth * 0.965; best[m] = tt[m]
    for side in ('L', 'R'):
        sg = 1 if side == 'R' else -1
        dvec = np.array([sg * math.sin(ALPHA), -math.cos(ALPHA), 0.]); n = np.array([math.cos(ALPHA), sg * math.sin(ALPHA) * 1.0, 0.])
        n = np.array([sg * math.cos(ALPHA), math.sin(ALPHA), 0.])      # normal, perpendicular to dvec
        tt = -(n @ eye) / (D @ n); P = eye + D * tt[..., None]
        s = P @ dvec; ok = (tt > 0) & (s >= 0) & (s <= WL) & (P[..., 2] >= 0) & (P[..., 2] <= np.vectorize(ztop)(np.clip(s, 0, WL))) & (tt < best)
        facing = (D @ n) < 0     # camera sees the face whose normal points to it; both faces printed/blank
        ink = ink_at(P)
        # inside faces (toward the guest, +n side of a leaf?) printed; outside faces blank & darker
        inside = (eye - 0) @ n > 0
        side_front = (np.einsum('ij,j->i', np.zeros((1, 3)), n) if False else None)
        c_in = np.where(ink[..., None], np.array([20, 20, 20.]), np.array([254, 237, 149.]))
        c_out = np.array([236, 214, 120.])
        # printed face is the one seen from the guest side (y<0 side of the leaf plane contains the open V)
        printed = ((eye @ n) * (np.array([0., -450., 100.]) @ n)) > 0 if False else None
        # a leaf's printed face = the face the seat eye sees; test per-pixel by sign of (eye - P) . n vs seat eye side
        seat_side = np.sign((E_SEAT) @ n)
        cam_side = np.sign((eye) @ n)
        show = cam_side == seat_side
        cc = c_in if show else None
        if show: col[ok] = c_in[ok]
        else: col[ok] = c_out
        best[ok] = tt[ok]
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8))
    return im.resize(size, Image.LANCZOS)

if __name__ == '__main__':
    render_net().save('../calc/c02_net.png')
    tgt = (0, -30, 30)
    views = {'seat': E_SEAT, 'neighbourR': (330., -350., 430.), 'neighbourL': (-330., -350., 430.), 'walkby': (-700., -150., 430.), 'standing': (0., -450., 1150.), 'across': (0., 900., 430.)}
    for k, e in views.items():
        render_view(e, tgt, 14 if k != 'walkby' else 16).save(f'../calc/c02_view_{k}.png')
    ims = [Image.open(f'../calc/c02_view_{k}.png') for k in views]
    o = Image.new('RGB', (1560, 800))
    for i, im in enumerate(ims): o.paste(im, ((i % 3) * 520, (i // 3) * 400))
    o.save('../calc/_c02_cmp.png')
    render_view((-430., -520., 330.), (0, -30, 40), 9, (520, 400)).save('../calc/c02_view_object.png')
