"""Artist name over a photo, in the melted DINNER lettering.

    python3 overlay.py LAYOUT.json [--out DIR]

LAYOUT.json (all coordinates in output pixels, 1080 x 1350 for a 4:5 post):
{
  "photo": "in/andrey_lee.jpg",            # relative to the layout file
  "crop": [0, 0, 1334, 1667.5],            # x, y, w, h in source pixels (aspect = out aspect)
  "out": [1080, 1350],
  "color": "#000000",                     # name colour (black or lemon #feed95)
  "behind": true,                          # the person covers the name (segmentation mask)
  "melt": {"sigma": 0.10, "thr": 0.27, "track": 0.03, "stretch": 0.9},   # DINNER logo fit, light tracking
  "lines": [{"text": "ANDREY", "x": 40, "y": 60, "cap": 190, "align": "left", "rot": 0}, ...],
  "effects": {"shadow": {"dx": 14, "dy": 10, "blur": 9, "opacity": 0.3},   # optional, all of them
              "texture": 0.5, "blur": 1.2, "grain": 6}
}
A line may give "quad": [[x,y] TL, TR, BR, BL] instead of x/y/align to lie in perspective on a plane.
`x` is the left, right or centre edge for align left/right/center; `y` is the top of the caps.
`rot` turns the line about its anchor (degrees, clockwise), for vertical names.

Writes <name>.png (out size), <name>@src.png (crop at source resolution), <name>.svg (editable:
photo layer, name as vector paths, the person as a clipped photo copy on top), <name>.json (placement)
and <name>_check.png (name mask, person mask and margins drawn over the photo).
Needs the person mask from mask.py next to the photo (<photo stem>_mask.png).
"""
import base64
import io
import json
import math
import os
import pathlib
import sys

import cv2
import numpy as np
import potrace
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
FONT = os.environ.get("WIX_DISPLAY_700", "/tmp/claude-0/-home-user-claude-bobik/6a3dcf92-132a-5018-88ad-a2068c46056a/scratchpad/wix700.ttf")
SS = 2          # supersampling for the name raster


def render(text, cap, stretch, track):
    f = ImageFont.truetype(FONT, size=int(cap / 0.715), layout_engine=ImageFont.Layout.RAQM)
    pad = int(cap * 0.8)
    w = int(f.getlength(text) + track * cap * len(text)) + 2 * pad
    h = int(cap * 1.4) + 2 * pad
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    x = pad
    for ch in text:
        d.text((x, pad + cap * 1.1), ch, font=f, fill=255, anchor="ls")
        x += f.getlength(ch) + track * cap
    a = np.asarray(im, np.float32) / 255
    if stretch != 1.0:
        a = cv2.resize(a, (int(a.shape[1] * stretch), a.shape[0]), interpolation=cv2.INTER_AREA)
    return a


def melted_line(text, cap, m):
    """Melted line cropped to its cap box: (mask, top offset of caps inside the mask)."""
    a = render(text, cap, m.get("stretch", 0.9), m.get("track", 0.03))
    b = cv2.GaussianBlur(a, (0, 0), m.get("sigma", 0.10) * cap)
    mk = (b > m.get("thr", 0.27)).astype(np.uint8)
    ys, xs = np.nonzero(mk)
    return mk[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def name_mask(layout, W, H):
    """Full-frame name mask at SS x output size."""
    canvas = np.zeros((H * SS, W * SS), np.uint8)
    boxes = []
    for ln in layout["lines"]:
        mk = melted_line(ln["text"], ln["cap"] * SS, layout.get("melt", {}))
        h, w = mk.shape
        x = ln["x"] * SS
        x0 = x if ln.get("align", "left") == "left" else x - w if ln["align"] == "right" else x - w / 2
        y0 = ln["y"] * SS
        rot = ln.get("rot", 0)
        if ln.get("quad"):
            # perspective: the line's ink box goes onto four points (TL, TR, BR, BL) on a plane in the photo
            src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
            dst = np.float32(ln["quad"]) * SS
            P = cv2.getPerspectiveTransform(src, dst)
            warped = cv2.warpPerspective(mk * 255, P, (W * SS, H * SS), flags=cv2.INTER_LINEAR)
        else:
            M = np.float32([[1, 0, x0], [0, 1, y0]])
            if rot:
                R = cv2.getRotationMatrix2D((x, y0), -rot, 1.0)
                M = (np.vstack([R, [0, 0, 1]]) @ np.vstack([M, [0, 0, 1]]))[:2].astype(np.float32)
            warped = cv2.warpAffine(mk * 255, M, (W * SS, H * SS), flags=cv2.INTER_LINEAR)
        canvas = np.maximum(canvas, warped)
        ys, xs = np.nonzero(warped)
        if len(xs):
            boxes.append([xs.min() / SS, ys.min() / SS, xs.max() / SS, ys.max() / SS])
    return canvas > 127, boxes


def trace(mask, scale, turd=4):
    """Binary mask -> SVG path d (scaled), even-odd."""
    bm = potrace.Bitmap(~mask.astype(bool))       # potracer traces the False pixels
    paths = bm.trace(turdsize=turd, alphamax=1.0, opticurve=True, opttolerance=0.2)
    f = lambda p: f"{p.x * scale:.2f},{p.y * scale:.2f}"
    out = []
    for c in paths:
        s = [f"M{f(c.start_point)}"]
        for seg in c.segments:
            if seg.is_corner:
                s.append(f"L{f(seg.c)}L{f(seg.end_point)}")
            else:
                s.append(f"C{f(seg.c1)} {f(seg.c2)} {f(seg.end_point)}")
        out.append("".join(s) + "Z")
    return "".join(out)


def jpeg_b64(im, q=92):
    b = io.BytesIO()
    im.save(b, "JPEG", quality=q)
    return base64.b64encode(b.getvalue()).decode()


def main(path, outdir=None):
    path = pathlib.Path(path)
    L = json.loads(path.read_text())
    outdir = pathlib.Path(outdir) if outdir else path.parent / "out"
    outdir.mkdir(parents=True, exist_ok=True)
    stem = path.stem
    W, H = L.get("out", [1080, 1350])
    src = Image.open(path.parent / L["photo"]).convert("RGB")
    cx, cy, cw, ch = L["crop"]
    photo = src.resize((W, H), Image.LANCZOS, box=(cx, cy, cx + cw, cy + ch))
    photo_hi = src.crop((round(cx), round(cy), round(cx + cw), round(cy + ch)))
    mpath = (path.parent / L["photo"]).with_name(pathlib.Path(L["photo"]).stem + "_mask.png")
    pm = Image.open(mpath).convert("L").resize((W, H), Image.LANCZOS, box=(cx, cy, cx + cw, cy + ch))
    person = np.asarray(pm, np.float32) / 255

    nm, boxes = name_mask(L, W, H)
    fx = L.get("effects", {})
    col = np.array(Image.new("RGB", (1, 1), L.get("color", "#000000")))[0, 0].astype(np.float32)

    def composite(base_img, person_a, scale):
        """Name over the photo at one resolution; effect sizes are given at output size and scaled."""
        Wc, Hc = base_img.size
        alpha = cv2.resize(nm.astype(np.float32), (Wc, Hc), interpolation=cv2.INTER_AREA)
        if fx.get("blur"):                                   # match the photo's depth of field
            alpha = cv2.GaussianBlur(alpha, (0, 0), fx["blur"] * scale)
        base = np.asarray(base_img, np.float32)
        # the person's edge pixels mix in the background: tuck the ink a pixel under them, no light fringe
        r = max(1, round(1.2 * scale))
        hard = cv2.erode((person_a > 0.5).astype(np.uint8), np.ones((2 * r + 1, 2 * r + 1), np.uint8)).astype(np.float32)
        keep = (1 - cv2.GaussianBlur(hard, (0, 0), 0.6 * scale)) if L.get("behind", True) else 1.0
        comp = base.copy()
        sh = fx.get("shadow")
        if sh:                                               # cast shadow on the surface behind the name
            sa = np.roll(np.roll(alpha, int(sh.get("dy", 12) * scale), 0), int(sh.get("dx", 12) * scale), 1)
            sa = cv2.GaussianBlur(sa, (0, 0), sh.get("blur", 10) * scale) * sh.get("opacity", 0.35) * keep
            comp = comp * (1 - sa[..., None])
        alpha = alpha * keep
        ink = np.broadcast_to(col, base.shape).copy()
        if fx.get("texture"):                                # ink takes the surface: folds, light falloff
            lum = cv2.cvtColor(base.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
            detail = lum - cv2.GaussianBlur(lum, (0, 0), 12 * scale)
            shade = cv2.GaussianBlur(lum, (0, 0), 60 * scale)
            shade = shade / max(1.0, float(np.percentile(shade, 95)))
            t = fx["texture"]
            ink = ink * (1 - t + t * np.clip(shade, 0.3, 1.2))[..., None] + (t * detail)[..., None]
        if fx.get("grain"):
            ink = ink + np.random.default_rng(7).normal(0, fx["grain"], base.shape[:2])[..., None]
        return comp * (1 - alpha[..., None]) + ink * alpha[..., None], alpha

    comp, alpha = composite(photo, person, 1.0)
    Image.fromarray(comp.clip(0, 255).astype(np.uint8)).save(outdir / f"{stem}.png")
    box_hi = (round(cx), round(cy), round(cx + cw), round(cy + ch))
    ph = np.asarray(Image.open(mpath).convert("L").crop(box_hi).resize(photo_hi.size), np.float32) / 255
    hi, _ = composite(photo_hi, ph, photo_hi.width / W)
    Image.fromarray(hi.clip(0, 255).astype(np.uint8)).save(outdir / f"{stem}@src.png")

    # editable SVG: photo, name paths, the person on top (photo clipped to the silhouette)
    d_name = trace(nm, 1 / SS)
    sil = cv2.GaussianBlur((person > 0.5).astype(np.float32), (0, 0), 1.0) > 0.5
    d_person = trace(sil, 1.0, turd=20)
    b64 = jpeg_b64(photo_hi)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><clipPath id="person-clip"><path d="{d_person}"/></clipPath></defs>
<g id="photo"><image width="{W}" height="{H}" preserveAspectRatio="none" xlink:href="data:image/jpeg;base64,{b64}"/></g>
<g id="name"><path d="{d_name}" fill="{L.get('color', '#000000')}" fill-rule="evenodd"/></g>
''' + (f'''<g id="person-over-name" clip-path="url(#person-clip)"><image width="{W}" height="{H}" preserveAspectRatio="none" xlink:href="data:image/jpeg;base64,{b64}"/></g>
''' if L.get("behind", True) else "") + "</svg>\n"
    (outdir / f"{stem}.svg").write_text(svg)

    # check image: name, person outline (red), 5 % margins (blue), the profile grid's 3:4 crop (green), name boxes (orange)
    chk = Image.fromarray(comp.clip(0, 255).astype(np.uint8)).convert("RGB")
    dr = ImageDraw.Draw(chk)
    cnts, _ = cv2.findContours((person > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        if len(c) > 10:
            dr.line([tuple(p[0]) for p in c] + [tuple(c[0][0])], fill=(255, 0, 90), width=2)
    m = round(W * 0.05)
    dr.rectangle([m, m, W - m, H - m], outline=(0, 160, 255), width=2)
    g = (W - H * 3 / 4) / 2                        # the profile grid shows a 3:4 centre crop
    dr.rectangle([g, 0, W - g, H - 1], outline=(0, 200, 120), width=2)
    for b in boxes:
        dr.rectangle(b, outline=(255, 140, 0), width=2)
    chk.save(outdir / f"{stem}_check.png")

    hidden = 1 - (alpha.sum() / max(1, cv2.resize(nm.astype(np.float32), (W, H), interpolation=cv2.INTER_AREA).sum()))
    info = {"layout": str(path), "boxes": boxes, "name_hidden_by_person": round(float(hidden), 3),
            "outputs": [f"{stem}.png", f"{stem}@src.png", f"{stem}.svg"]}
    (outdir / f"{stem}.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[a.index("--out") + 1] if "--out" in a else None)
