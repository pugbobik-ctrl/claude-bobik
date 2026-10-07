"""Render final card SVGs into textures for the 3D viewer.

For every SVG: <stem>.webp (lemon board inside the closed cut outline + art + live text) and,
with --clear, <stem>_clear.webp (art and text only on transparent, for acetate), plus
<stem>.size.json (viewBox size in mm). Die lines and guides are not drawn.

    python3 textures.py OUT_DIR SVG_OR_DIR [...] [--clear] [--ppm 4]
"""
import json
import re
import pathlib
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "illustrator"))
from svg2ai import SVGNS, parse_layer  # noqa: E402

LEMON = "#feed95"
FONTS = HERE.parent.parent / "fonts"
EXTRA_800 = pathlib.Path(__import__("os").environ.get("WIX800", "/nonexistent"))   # ExtraBold, if installed locally
ET.register_namespace("", "http://www.w3.org/2000/svg")


def board_d(root, group):
    """All closed subpaths of the cut layer as one path d (fill even-odd)."""
    items = parse_layer(root.attrib, ET.tostring(group, encoding="unicode").replace("ns0:", "").replace(":ns0", ""))
    out = []
    for it in items:
        if it["t"] != "path":
            continue
        for sp in it["sub"]:
            if not sp["closed"] or len(sp["pts"]) < 3:
                continue
            p = sp["pts"]
            seg = [f"M{p[0][0]} {p[0][1]}"]
            n = len(p)
            for i in range(n):
                a, b = p[i], p[(i + 1) % n]
                seg.append(f"C{a[4]} {a[5]} {b[2]} {b[3]} {b[0]} {b[1]}")
            out.append("".join(seg) + "Z")
    return "".join(out)


def variant(svg_path, mode):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    vb = [float(v) for v in root.get("viewBox").replace(",", " ").split()]
    d = ""
    for g in list(root):
        gid = g.get("id", "")
        if gid == "layer-cut":
            d = board_d(root, g)
        if gid in ("layer-guides", "layer-crease", "layer-perf", "layer-cut"):
            root.remove(g)
    if mode == "board":
        if not d:
            d = f"M{vb[0]} {vb[1]}h{vb[2]}v{vb[3]}h{-vb[2]}Z"
        b = ET.Element(SVGNS + "path", {"d": d, "fill": LEMON, "fill-rule": "evenodd"})
        root.insert(0, b)
    return ET.tostring(root, encoding="unicode"), vb


def render(jobs):
    faces = "".join(
        f"@font-face{{font-family:'Wix Madefor Text';font-weight:{w};src:url('file://{p}')}}"
        for w, p in [(400, FONTS / "WixMadeforText-400.ttf"), (500, FONTS / "WixMadeforText-500.ttf"),
                     (600, FONTS / "WixMadeforText-600.ttf"), (700, FONTS / "WixMadeforText-700.ttf"),
                     (800, EXTRA_800 if EXTRA_800.exists() else FONTS / "WixMadeforText-700.ttf")])
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        lst = []
        for i, (svg, w, h, png) in enumerate(jobs):
            head = svg.split(">", 1)
            tag = re.sub(r'\s(width|height)="[^"]*"', "", head[0]) + f' width="{w}" height="{h}" preserveAspectRatio="none"'
            svg = tag + ">" + head[1]
            html = (f"<!doctype html><meta charset=utf-8><style>{faces}html,body{{margin:0;background:transparent}}"
                    f"svg{{display:block}}</style>{svg}")
            f = tmp / f"{i}.html"
            f.write_text(html)
            lst.append({"html": str(f), "w": w, "h": h, "out": str(png)})
        jf = tmp / "jobs.json"
        jf.write_text(json.dumps(lst))
        subprocess.run(["node", str(HERE / "rasterize.cjs"), str(jf)], check=True,
                       env={**__import__("os").environ, "NODE_PATH": "/opt/node-tools/node_modules"})


def main(argv):
    clear = "--clear" in argv
    ppm = 4.0
    if "--ppm" in argv:
        ppm = float(argv[argv.index("--ppm") + 1])
    args = [a for i, a in enumerate(argv) if not a.startswith("--") and not (i and argv[i - 1] == "--ppm")]
    out = pathlib.Path(args[0])
    out.mkdir(parents=True, exist_ok=True)
    svgs = []
    for a in args[1:]:
        p = pathlib.Path(a)
        svgs += sorted(p.glob("*.svg")) if p.is_dir() else [p]
    jobs, conv = [], []
    with tempfile.TemporaryDirectory() as tmp:
        for s in svgs:
            modes = [("board", ppm)] + ([("clear", ppm * 3)] if clear else [])   # film: fine grilles need detail
            for mode, k in modes:
                svg, vb = variant(s, mode)
                scale = min(k, 4096 / max(vb[2], vb[3]))
                w, h = max(1, round(vb[2] * scale)), max(1, round(vb[3] * scale))
                png = pathlib.Path(tmp) / f"{s.stem}_{mode}.png"
                jobs.append((svg, w, h, png))
                name = s.stem + ("" if mode == "board" else "_" + mode) + ".webp"
                conv.append((png, out / name))
            (out / f"{s.stem}.size.json").write_text(json.dumps([vb[2], vb[3]]))
        render(jobs)
        for png, webp in conv:
            im = Image.open(png)
            im.save(webp, "WEBP", quality=88, method=5)
    print(f"{len(svgs)} svg -> {len(conv)} textures in {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
