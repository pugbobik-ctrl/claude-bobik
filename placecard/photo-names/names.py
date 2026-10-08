"""Artist names as vector lettering in the DINNER logo's melt.

    python3 names.py OUT_DIR

How the logo is built (measured on logo.pdf): one fused black mass, letters joined over 0.46–0.72 of
the height, shallow V notches top and bottom (0.06–0.27 of the height) where letters meet, counters as
rounded bays (E) or a big bowl (D), a pinhole where the melt nearly closes (R).
The names follow that recipe:
  1. letters set with an equal optical gap (outline to outline), so every pair fuses the same way;
  2. one melt over the whole word (Gaussian 0.10 × cap, threshold 0.27: the logo fit);
  3. each letter's own counters and bays carved back, from a lightly melted copy of the letter, so the
     melt fills the joins but not the letters' insides;
  4. per-name corrections (PAIRS, OPEN) checked by eye against the logo.
Writes per artist: <slug>_2line.svg, <slug>_1line.svg, <slug>_first.svg, <slug>_last.svg (vector,
black, one even-odd path per word), PDFs of the same, and names_sheet.png with DINNER for comparison.
"""
import json
import os
import pathlib
import sys

import cv2
import numpy as np
import potrace
from PIL import Image, ImageDraw, ImageFont

FONT = os.environ.get("WIX_DISPLAY_700", "/tmp/claude-0/-home-user-claude-bobik/6a3dcf92-132a-5018-88ad-a2068c46056a/scratchpad/wix700.ttf")
CAP = 400                  # working cap height in px
STRETCH = 0.9
SIGMA, THR = 0.10, 0.27    # the logo fit
GAP = 0.20                 # mean white between letters per row, × cap (optical spacing, tuned against DINNER)
MINGAP = 0.095             # never closer than this at any row, × cap
LEAD = 0.10                # space between the two lines, × cap (after melt)

ARTISTS = [("Tanya Andrianova", "tanya-andrianova"), ("Igor Zotov", "igor-zotov"), ("Andrey Lee", "andrey-lee"),
           ("Sasha Chernikov", "sasha-chernikov"), ("Sophia Zhuravkova", "sophia-zhuravkova")]
# hand corrections: extra space for a pair (× cap, + = looser), and how far a letter's counters reopen
PAIRS = {"TA": 0.05, "EY": 0.02, "AN": 0.0, "NY": 0.06, "YA": 0.04, "EE": 0.10, "LE": 0.02, "RE": 0.02,
         "PH": 0.05, "HI": 0.02, "IA": 0.03, "OP": 0.02, "AV": 0.0, "VK": 0.06, "KO": 0.05, "RA": 0.02,
         "UR": 0.02, "ZH": 0.02, "RI": 0.04, "NI": 0.0, "IK": 0.0, "RN": 0.02, "ER": 0.02, "NO": 0.02}
OPEN = {"A": 1.15, "R": 1.1, "O": 1.0, "D": 1.0, "P": 1.3, "E": 2.6, "B": 1.0, "G": 1.0, "Y": 1.6, "V": 1.3, "K": 1.3}


def glyph(ch, cap):
    f = ImageFont.truetype(FONT, size=int(cap / 0.715))
    pad = int(cap * 0.6)
    w = int(f.getlength(ch)) + 2 * pad
    h = int(cap * 1.2) + 2 * pad
    im = Image.new("L", (w, h), 0)
    ImageDraw.Draw(im).text((pad, pad + cap), ch, font=f, fill=255, anchor="ls")
    a = np.asarray(im, np.float32) / 255
    a = cv2.resize(a, (int(w * STRETCH), h), interpolation=cv2.INTER_AREA)
    return a, pad + cap      # glyph image and its baseline row


def edges(g, cap):
    """Right and left ink edge per row over the cap band (NaN where the row is empty)."""
    rows = range(int(0.68 * cap), int(1.52 * cap))     # glyph(): cap top at 0.6 cap, baseline at 1.6 cap
    R, L = [], []
    for y in rows:
        r = np.nonzero(g[y] > 0.5)[0]
        R.append(r.max() if len(r) else np.nan); L.append(r.min() if len(r) else np.nan)
    return np.array(R), np.array(L)


def min_gap(a_r, b_l, shift):
    ok = ~np.isnan(a_r) & ~np.isnan(b_l)
    return np.min(b_l[ok] + shift - a_r[ok]) if ok.any() else 1e9


def white_area(a_r, b_l, shift, cap, depth=0.28):
    """Optical gap: the white between two letters per row, each side's open space clipped at depth × cap."""
    d = depth * cap
    ar = np.where(np.isnan(a_r), np.nanmax(a_r) - d, np.maximum(a_r, np.nanmax(a_r) - d))
    bl = np.where(np.isnan(b_l), np.nanmin(b_l) + d, np.minimum(b_l, np.nanmin(b_l) + d))
    return np.clip(bl + shift - ar, 0, None).mean()


def set_word(word, cap):
    """Place glyphs with an equal outline gap plus pair corrections; returns canvas and per-letter masks."""
    gl = [glyph(c, cap) for c in word]
    H = max(g[0].shape[0] for g in gl)
    gl = [np.pad(g[0], ((0, H - g[0].shape[0]), (0, 0))) for g in gl]
    xs = [0]
    for i in range(1, len(word)):
        prev = gl[i - 1]
        target = (GAP + PAIRS.get(word[i - 1:i + 1], 0.0)) * cap
        pr, _ = edges(prev, cap)
        _, nl = edges(gl[i], cap)
        # optical spacing: equal white area between letters, but never closer than MINGAP at any row
        def solve(metric, goal):
            lo, hi = -prev.shape[1], prev.shape[1] * 2
            for _ in range(40):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if metric(mid) < goal else (lo, mid)
            return hi
        hi = max(solve(lambda m: white_area(pr, nl, m, cap), target),
                 solve(lambda m: min_gap(pr, nl, m), MINGAP * cap))
        xs.append(xs[-1] + int(round(hi)))
    W = xs[-1] + gl[-1].shape[1]
    canvas = np.zeros((H, W), np.float32)
    letters = []
    for x, g in zip(xs, gl):
        canvas[:, x:x + g.shape[1]] = np.maximum(canvas[:, x:x + g.shape[1]], g)
        m = np.zeros((H, W), np.float32); m[:, x:x + g.shape[1]] = g
        letters.append(m)
    return canvas, letters


def cleanup(M, cap, hole=0.012, speck=0.01):
    """Fill enclosed holes smaller than hole × cap² and drop ink specks smaller than speck × cap²."""
    M = M.astype(np.uint8)
    inv = 1 - M
    n, lab, st, _ = cv2.connectedComponentsWithStats(inv, 8)
    H, W = M.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x > 0 and y > 0 and x + w < W and y + h < H:
            region = lab == i
            thin = cv2.distanceTransform(region.astype(np.uint8), cv2.DIST_L2, 3).max() < 0.02 * cap
            if a < hole * cap * cap or thin:          # pinholes and hairline crescents
                M[region] = 1
    n, lab, st, _ = cv2.connectedComponentsWithStats(M, 8)
    for i in range(1, n):
        if st[i, 4] < speck * cap * cap:
            M[lab == i] = 0
    return M.astype(bool)


def melt_word(word, cap=CAP):
    canvas, letters = set_word(word, cap)
    pad = int(cap * 0.6)
    canvas = np.pad(canvas, pad); letters = [np.pad(l, pad) for l in letters]
    M = cv2.GaussianBlur(canvas, (0, 0), SIGMA * cap) > THR
    k = int(0.32 * cap) | 1
    close_k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    union_light = cv2.dilate((cv2.GaussianBlur(canvas, (0, 0), 0.02 * cap) > 0.5).astype(np.uint8),
                             cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.05 * cap) | 1,) * 2))
    for ch, L in zip(word, letters):
        o = OPEN.get(ch, 0.7)
        light = (cv2.GaussianBlur(L, (0, 0), 0.045 * cap) > 0.42).astype(np.uint8)
        if ch in "EF":                      # DINNER's E: wide round bays, taken from the drawn letter itself
            light = (cv2.GaussianBlur(L, (0, 0), 0.02 * cap) > 0.5).astype(np.uint8)
        ck = close_k if ch not in "EF" else cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.6 * cap) | 1,) * 2)
        conc = cv2.morphologyEx(light, cv2.MORPH_CLOSE, ck) & (1 - light)     # E/F: the whole bay, as in DINNER
        # keep only the letter's own insides: concavities inside its bounding columns
        e = int(round((1.0 - o) * 0.05 * cap + 0.02 * cap))    # OPEN > 1 widens the counter past the light melt
        if e > 0:
            conc = cv2.erode(conc, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * e + 1, 2 * e + 1)))
        elif e < 0:
            conc = cv2.dilate(conc, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (-2 * e + 1, -2 * e + 1))) & (1 - light)
        if ch in "EF":                      # keep the bays' mouths open toward the next letter, as in DINNER
            k = int(0.16 * cap)
            ext = conc.copy()
            for dx in range(1, k + 1, 2):
                ext[:, dx:] |= conc[:, :-dx]
            conc = ext & (1 - union_light)
        M = M & ~conc.astype(bool)
    # clean-up: no pinholes, no stray specks, no sharp nicks; carved edges melt like the rest
    M = cleanup(M, cap)
    # white features thinner than 0.035 cap (slits, hairlines, needle-sharp notch tips) are filled
    white = 1 - M.astype(np.uint8)
    kw = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.035 * cap) | 1,) * 2)
    M = (M.astype(np.uint8) | (white & (1 - cv2.morphologyEx(white, cv2.MORPH_OPEN, kw))))
    M = cv2.morphologyEx(M, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.04 * cap) | 1,) * 2))
    M = cv2.GaussianBlur(M.astype(np.float32), (0, 0), 0.035 * cap) > 0.5
    M = cleanup(M, cap)
    ys, xs = np.nonzero(M)
    return M[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def trace_path(mask, scale=1.0, dx=0.0, dy=0.0):
    bm = potrace.Bitmap(~mask.astype(bool))            # potracer traces the False pixels
    f = lambda p: f"{p.x * scale + dx:.2f},{p.y * scale + dy:.2f}"
    d = []
    for c in bm.trace(turdsize=8, alphamax=1.1, opticurve=True, opttolerance=0.25):
        s = [f"M{f(c.start_point)}"]
        for seg in c.segments:
            s.append(f"L{f(seg.c)}L{f(seg.end_point)}" if seg.is_corner else f"C{f(seg.c1)} {f(seg.c2)} {f(seg.end_point)}")
        d.append("".join(s) + "Z")
    return "".join(d)


def svg_of(words_masks, gap_rows, unit=1 / CAP * 100):
    """Stack word masks (left aligned) into one SVG; units: cap height = 100."""
    paths, y, W = [], 0.0, 0.0
    for i, (word, m) in enumerate(words_masks):
        paths.append(f'<path id="{word.lower()}" d="{trace_path(m, unit, 0, y)}" fill="#000000" fill-rule="evenodd"/>')
        W = max(W, m.shape[1] * unit)
        y += m.shape[0] * unit + (gap_rows * unit if i < len(words_masks) - 1 else 0)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {y:.2f}" width="{W * 3:.0f}" height="{y * 3:.0f}">'
            + "".join(paths) + "</svg>\n"), (W, y)


def main(out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    meta = {}
    sheet_rows = []
    for name, slug in ARTISTS:
        first, last = name.upper().split()
        mf, ml = melt_word(first), melt_word(last)
        one = melt_word(first + " " + last) if False else None
        files = {}
        for key, words, gap in (("2line", [(first, mf), (last, ml)], LEAD * CAP),
                                ("first", [(first, mf)], 0), ("last", [(last, ml)], 0)):
            svg, size = svg_of(words, gap)
            (out / f"{slug}_{key}.svg").write_text(svg)
            files[key] = size
        # one line: the two words on one baseline with a word space of 0.35 cap
        H = max(mf.shape[0], ml.shape[0]); sp = int(0.35 * CAP)
        line = np.zeros((H, mf.shape[1] + sp + ml.shape[1]), bool)
        line[H - mf.shape[0]:, :mf.shape[1]] = mf
        line[H - ml.shape[0]:, mf.shape[1] + sp:] = ml
        svg, size = svg_of([(first + "-" + last, line)], 0)
        (out / f"{slug}_1line.svg").write_text(svg)
        files["1line"] = size
        meta[slug] = {"name": name, "files": {k: f"{slug}_{k}.svg" for k in files}, "size_cap100": files}
        sheet_rows.append((name, mf, ml))
    (out / "names.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    # comparison sheet with the logo
    logo = os.environ.get("DINNER_PNG", "/tmp/claude-0/-home-user-claude-bobik/6a3dcf92-132a-5018-88ad-a2068c46056a/scratchpad/logo/horiz.png")
    s = 0.25
    rows = []
    if os.path.exists(logo):
        a = np.asarray(Image.open(logo).convert("L")) < 128
        ys, xs = np.nonzero(a); a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        a = cv2.resize(a.astype(np.uint8) * 255, (int(a.shape[1] * mf.shape[0] / a.shape[0] * s), int(mf.shape[0] * s)), interpolation=cv2.INTER_AREA)
        rows.append(a)
    for _, mf, ml in sheet_rows:
        for m in (mf, ml):
            rows.append(cv2.resize(m.astype(np.uint8) * 255, (int(m.shape[1] * s), int(m.shape[0] * s)), interpolation=cv2.INTER_AREA))
    Wd = max(r.shape[1] for r in rows) + 40
    Hd = sum(r.shape[0] + 40 for r in rows) + 40
    sheet = np.full((Hd, Wd), 255, np.uint8)
    y = 20
    for i, r in enumerate(rows):
        sheet[y:y + r.shape[0], 20:20 + r.shape[1]] = 255 - r
        y += r.shape[0] + (40 if i % 2 == 0 else 18)
        if y > Hd - 10: break
    Image.fromarray(sheet).save(out / "names_sheet.png")
    print("wrote", len(meta), "names to", out)


if __name__ == "__main__":
    main(sys.argv[1])
