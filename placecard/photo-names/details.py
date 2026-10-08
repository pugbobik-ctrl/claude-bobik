"""Small type in the poster's style: a label, event lines and the COLORBLOCK × DNA lockup.

    from details import render_details
    rgba, svg = render_details(spec, W, H)     # RGBA layer at W x H and an SVG fragment (live text)

spec (output px):
{"x": 54, "y": 1180, "align": "left", "color": "#000000", "size": 28,
 "label": "Line-up", "lines": ["Dinner", "10 oct 2026, 18:00", "DNA Kitchen, Samokatnaya 4s53"],
 "lockup": 34, "leading": 1.25, "gap": 0.9, "rot": 0}
Poster rules: Wix Madefor Text SemiBold, mixed case, tracking +10/1000 em; label at 0.76 × size;
lockup COLORBLOCK and DNA Bold, × SemiBold at 0.7 × lockup, gaps 0.55 em. `y` is the first baseline.
`rot` (90 or -90) sets the whole block vertically about (x, y).
"""
import pathlib
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont

FONTS = pathlib.Path(__file__).resolve().parent.parent / "fonts"
TRACK = 0.010


def _font(w, size):
    return ImageFont.truetype(str(FONTS / f"WixMadeforText-{w}.ttf"), round(size))


def _width(text, f, size, track):
    return sum(f.getlength(c) for c in text) + track * size * max(0, len(text) - 1)


def _runs(spec):
    """Every piece of text with its weight, size, x offset and baseline offset (block-local)."""
    s = spec.get("size", 28)
    lead = spec.get("leading", 1.25) * s
    runs, y = [], 0.0
    if spec.get("label"):
        ls = 0.76 * s
        runs.append(dict(t=spec["label"], w=600, size=ls, dx=0, dy=y))
        y += lead * 1.15
    for line in spec.get("lines", []):
        runs.append(dict(t=line, w=600, size=s, dx=0, dy=y))
        y += lead
    if spec.get("lockup"):
        L = spec["lockup"]
        y += (spec.get("gap", 0.9) - 1) * lead + L * 1.05
        fb, fs = _font(700, L), _font(600, 0.7 * L)
        x = 0.0
        for t, w, sz, f in (("COLORBLOCK", 700, L, fb), ("×", 600, 0.7 * L, fs), ("DNA", 700, L, fb)):
            runs.append(dict(t=t, w=w, size=sz, dx=x, dy=y - (0.06 * L if t == "×" else 0), track=0.0))
            x += _width(t, f, sz, 0.0) + 0.55 * L
    for r in runs:
        r.setdefault("track", TRACK)
        r["width"] = _width(r["t"], _font(r["w"], r["size"]), r["size"], r["track"])
    return runs


def render_details(spec, W, H):
    runs = _runs(spec)
    right = spec.get("align", "left") == "right"
    # lockup pieces move together: align on the widest line
    lock = [r for r in runs if r["track"] == 0.0]
    lock_w = (lock[-1]["dx"] + lock[-1]["width"]) if lock else 0
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    big = max(W, H) * 2
    tmp = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    ox, oy = big // 2, big // 2
    col = spec.get("color", "#000000")
    svg = []
    for r in runs:
        f = _font(r["w"], r["size"])
        is_lock = r["track"] == 0.0
        x = r["dx"] - (lock_w if (right and is_lock) else (r["width"] if right else 0))
        cx = x
        for c in r["t"]:
            d.text((ox + cx, oy + r["dy"]), c, font=f, fill=col, anchor="ls")
            cx += f.getlength(c) + r["track"] * r["size"]
        svg.append((x, r["dy"], r))
    rot = spec.get("rot", 0)
    if rot:
        tmp = tmp.rotate(-rot, center=(ox, oy), resample=Image.BICUBIC)
    layer.alpha_composite(tmp.crop((ox - spec["x"], oy - spec["y"], ox - spec["x"] + W, oy - spec["y"] + H)))
    tr = f' transform="translate({spec["x"]} {spec["y"]}){f" rotate({rot})" if rot else ""}"'
    body = "".join(
        f'<text x="{x:.1f}" y="{dy:.1f}" font-family="Wix Madefor Text" font-weight="{r["w"]}" font-size="{r["size"]:.1f}" '
        f'letter-spacing="{r["track"] * r["size"]:.2f}" fill="{col}">{escape(r["t"])}</text>'
        for x, dy, r in svg)
    return layer, f'<g id="details"{tr}>{body}</g>'


if __name__ == "__main__":
    spec = {"x": 54, "y": 1150, "size": 28, "label": "Line-up", "lines": ["Dinner", "10 oct 2026, 18:00", "DNA Kitchen, Samokatnaya 4s53"], "lockup": 34}
    im, s = render_details(spec, 1080, 1350)
    bg = Image.new("RGBA", (1080, 1350), (240, 240, 236, 255)); bg.alpha_composite(im); bg.convert("RGB").save("/tmp/details_test.png")
    print(s[:200])
