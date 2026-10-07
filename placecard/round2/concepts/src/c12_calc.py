"""Concept 12 THROUGH THE GLASS - a water-filled tumbler is a cylindrical lens. 2D (plan) ray trace, vertical axis.
Eye at y=-450 (x=0). Glass axis at origin, water radius A. Card plane y=D behind the glass."""
import numpy as np, math
from PIL import Image, ImageDraw
from lib import *
A = 36.0; N = 1.333; D = 120.0; EYE = 450.0

def trace(theta):
    """theta: array of view angles (rad) -> x on card plane y=D ; nan if ray misses glass handled separately"""
    o = np.array([0.0, -EYE]); out = np.zeros_like(theta); inside = np.zeros(theta.shape, bool)
    for i, th in enumerate(theta):
        d = np.array([math.sin(th), math.cos(th)])
        # intersect circle
        b = o @ d; c = o @ o - A * A; disc = b * b - c
        if disc <= 0:
            t = (D - o[1]) / d[1]; out[i] = o[0] + t * d[0]; continue
        t1 = -b - math.sqrt(disc); P = o + t1 * d; nrm = P / A
        # refract in (air->water)
        cos_i = -d @ nrm; sin_t = math.sqrt(max(0, 1 - cos_i**2)) / N; cos_t = math.sqrt(1 - sin_t**2)
        d2 = (d / N) + (cos_i / N - cos_t) * nrm; d2 /= np.linalg.norm(d2)
        b2 = P @ d2; t2 = -b2 + math.sqrt(max(0, b2 * b2 - (P @ P - A * A))); P2 = P + t2 * d2
        n2 = -P2 / A  # inward normal reversed: pointing toward water centre; for exit use outward normal -> flip
        nout = P2 / A
        cos_i2 = d2 @ nout; sin_o = N * math.sqrt(max(0, 1 - cos_i2**2))
        if sin_o >= 1: out[i] = np.nan; continue
        cos_o = math.sqrt(1 - sin_o**2)
        d3 = N * d2 + (cos_o - N * cos_i2) * nout; d3 /= np.linalg.norm(d3)
        t = (D - P2[1]) / d3[1]; out[i] = P2[0] + t * d3[0]; inside[i] = True
    return out, inside

if __name__ == '__main__':
    th = np.linspace(-A / EYE * 0.98, A / EYE * 0.98, 41)
    xc, ins = trace(th)
    xg = EYE * np.tan(th)
    print('through glass: view position at glass plane (mm) -> card x (mm)')
    for a, b in list(zip(xg, xc))[::5]: print(f'  {a:7.1f} -> {b:8.1f}')
    # linear fit slope near centre (magnification, negative = inverted)
    m = np.polyfit(xg[15:26], xc[15:26], 1)[0]
    print('centre slope dxcard/dxview =', round(m, 3), ' (direct would be', round((EYE + D) / EYE, 3), ')')
    # print: mirrored text. view coordinate xv in [-30,30] (glass plane) ; card x = f(xv). Build print mask by sampling image rows
    PPM = 12; XW = 120; ZH = 60
    W = XW * 2 * PPM; H = ZH * PPM
    sz = 56 / (text_width('Zhuravkova', 10, 700) / 10)
    img = Image.new('L', (W * 1, H), 0)
    # text mask in view coords
    VW = 80; vm = Image.new('L', (VW * PPM, H), 0); d = ImageDraw.Draw(vm)
    for t, base in (('Sophia', 36.0), ('Zhuravkova', 18.0)):
        g, w = text_shape(t, sz, 700)
        for p in geom_polys(g):
            for ring, col in [(p.exterior, 255)] + [(r, 0) for r in p.interiors]:
                d.polygon([((x + VW / 2) * PPM, (ZH - (y + base)) * PPM) for x, y in ring.coords], fill=col)
    vmask = np.array(vm) > 127
    # build mapping view->card for fine theta
    thf = np.linspace(-A / EYE * 0.98, A / EYE * 0.98, 2000); xcf, insf = trace(thf); xgf = EYE * np.tan(thf)
    printm = np.zeros((H, W), bool)
    for j in range(len(xgf)):
        ix_v = int(round((xgf[j] + VW / 2) * PPM))
        ixc = int(round((xcf[j] + XW) * PPM))
        if 0 <= ix_v < vmask.shape[1] and 0 <= ixc < W and not np.isnan(xcf[j]):
            col = vmask[:, ix_v]
            jn = j + 1 if j + 1 < len(xcf) else j
            ixc2 = int(round((xcf[jn] + XW) * PPM)) if not np.isnan(xcf[jn]) else ixc
            lo, hi = sorted((ixc, ixc2)); hi = max(hi, lo + 1)
            printm[:, max(lo, 0):min(hi + 1, W)] |= col[:, None]
    Image.fromarray(np.where(printm, 20, 254).astype(np.uint8)).save('../calc/c12_print.png')
    # render views: view columns across +-60 mm at glass plane
    VX = 70; cols = int(VX * 2 * PPM); thv = np.arctan((np.arange(cols) / PPM - VX + 0.5 / PPM) / EYE)
    xcv, insv = trace(thv)
    # cap: columns inside glass use xcv; outside use direct
    view = np.zeros((H, cols, 3), np.uint8); view[:] = (254, 237, 149)
    for c in range(cols):
        x = xcv[c]
        ix = int(round((x + XW) * PPM))
        if 0 <= ix < W and not np.isnan(x): 
            m = printm[:, ix]; view[m, c] = (20, 20, 20)
    # glass outline overlay
    im = Image.fromarray(view); dd = ImageDraw.Draw(im)
    gx0 = (-A + VX) * PPM; gx1 = (A + VX) * PPM
    # darken outside-of-glass slightly? draw glass edges
    dd.line([(gx0, 0), (gx0, H)], fill=(120, 140, 150), width=3); dd.line([(gx1, 0), (gx1, H)], fill=(120, 140, 150), width=3)
    # empty glass version: view with direct mapping everywhere
    thd = thv; xd = (EYE + D) * np.tan(thd) 
    v2 = np.zeros((H, cols, 3), np.uint8); v2[:] = (254, 237, 149)
    for c in range(cols):
        ix = int(round((xd[c] + XW) * PPM))
        if 0 <= ix < W: v2[printm[:, ix], c] = (20, 20, 20)
    Image.fromarray(v2).save('../calc/c12_view_empty.png'); im.save('../calc/c12_view_full.png')
    print('print width mm', xcf[~np.isnan(xcf)].min(), xcf[~np.isnan(xcf)].max(), 'font size', sz)
