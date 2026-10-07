"""Concept 01 LIT - geometry proof. Lamp point source -> stencil card -> plate.
Coordinates: x right (guest's right), y from lamp foot toward guest, z up. mm."""
import numpy as np, json, math
from PIL import Image, ImageDraw
from scipy import ndimage
from lib import *

LAMP = np.array([0., 0., 300.]); ZP = 12.0          # lamp, plate surface height
YC = 195.0                                          # card plane distance from lamp axis
PLATE_C = (0., 360.); PLATE_R = 135.
SIZE = 22.0; LEAD = 24.5; TOPPY = 262.0             # text on plate: font size, line pitch, cap-top of line 1
BRIDGE = 2.1                                        # stencil bridge on the plate (mm)

def plate_to_card(px, py):
    t = YC / py
    return (px * t, LAMP[2] - (LAMP[2] - ZP) * t)    # (xc, zc)
def card_to_plate(xc, zc):
    lam = (LAMP[2] - ZP) / (LAMP[2] - zc)
    return (lam * xc, lam * YC)

def build_text_polys(slice_frac):
    polys = []
    cap = 0.715 * SIZE; xh = 0.503 * SIZE
    for i, line in enumerate(['Sophia', 'Zhuravkova']):
        cs, w = text_contours(line, SIZE, 700)
        base = TOPPY + cap + i * LEAD
        for c in cs:
            polys.append([(x - w / 2, base - y) for x, y in c])
        # bridge band at slice_frac of x-height for this line (py coords)
        polys_band = (base - slice_frac * xh)
        yield_band = (polys_band - BRIDGE / 2, polys_band + BRIDGE / 2)
        polys.append(('band', yield_band, w))
    return polys

def raster(polys, x0, x1, y0, y1, ppm=8):
    W = int((x1 - x0) * ppm); H = int((y1 - y0) * ppm)
    m = np.zeros((H, W), bool)
    for p in polys:
        if p and p[0] == 'band': continue
        im = Image.new('1', (W, H), 0)
        ImageDraw.Draw(im).polygon([((x - x0) * ppm, (y - y0) * ppm) for x, y in p], fill=1)
        m ^= np.array(im, bool)       # even-odd
    return m

def holes_mask(slice_frac, ppm=8):
    polys = build_text_polys(slice_frac)
    x0, x1, y0, y1 = -80, 80, TOPPY - 6, TOPPY + 56
    m = raster(polys, x0, x1, y0, y1, ppm)
    for p in polys:
        if p and p[0] == 'band':
            _, (a, b), w = p
            ya = int((a - y0) * ppm); yb = int((b - y0) * ppm)
            m[ya:yb, :] = False
    return m, (x0, x1, y0, y1)

if __name__ == '__main__':
    for sf in (0.35, 0.45, 0.5, 0.55, 0.65):
        m, _ = holes_mask(sf)
        solid = ~m
        lab, n = ndimage.label(solid)
        print('slice', sf, 'solid components in text box:', n, [int((lab == k).sum()) for k in range(1, n + 1)])
