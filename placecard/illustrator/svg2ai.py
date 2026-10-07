"""Turn layered card SVGs into one Illustrator script (place-cards.jsx).

Each input SVG is one flat card for one artist, in mm (viewBox 1 unit = 1 mm), with top-level
groups id="layer-cut | layer-crease | layer-perf | layer-art | layer-text | layer-guides".
The script lays every card on its own artboard at 1:1, sorted into Illustrator layers by
function, with live text, die lines as spot colours and the guides layer set to non-printing.

    python3 svg2ai.py OUT.jsx DIR_OR_SVG [DIR_OR_SVG ...]
"""
import json
import math
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

from svgelements import (SVG, Arc, Close, CubicBezier, Line, Move, Path, QuadraticBezier, Shape,
                         Text)

HERE = pathlib.Path(__file__).parent
LAYERS = ["cut", "crease", "perf", "art", "text", "guides"]
SVGNS = "{http://www.w3.org/2000/svg}"


def r(v):
    return round(float(v), 3)


def subpaths(path):
    """svgelements Path -> list of {pts: [[ax, ay, lx, ly, rx, ry], ...], closed}."""
    out, cur = [], None

    def start(p):
        nonlocal cur
        cur = {"pts": [[r(p.x), r(p.y)] * 3], "closed": False}
        out.append(cur)

    for seg in path:
        if isinstance(seg, Move):
            start(seg.end)
        elif isinstance(seg, Close):
            if cur:
                cur["closed"] = True
                a, z = cur["pts"][0], cur["pts"][-1]
                if len(cur["pts"]) > 1 and abs(a[0] - z[0]) < 1e-3 and abs(a[1] - z[1]) < 1e-3:
                    a[2], a[3] = z[2], z[3]      # merge the duplicate end point into the start
                    cur["pts"].pop()
        else:
            if cur is None:
                start(seg.start)
            curves = []
            if isinstance(seg, Line):
                curves = [("L", seg.end)]
            elif isinstance(seg, CubicBezier):
                curves = [("C", seg.control1, seg.control2, seg.end)]
            elif isinstance(seg, QuadraticBezier):
                p0, q, p1 = seg.start, seg.control, seg.end
                c1 = (p0.x + 2 / 3 * (q.x - p0.x), p0.y + 2 / 3 * (q.y - p0.y))
                c2 = (p1.x + 2 / 3 * (q.x - p1.x), p1.y + 2 / 3 * (q.y - p1.y))
                curves = [("Cq", c1, c2, p1)]
            elif isinstance(seg, Arc):
                curves = [("C", c.control1, c.control2, c.end) for c in seg.as_cubic_curves()]
            for c in curves:
                prev = cur["pts"][-1]
                if c[0] == "L":
                    e = c[1]
                    cur["pts"].append([r(e.x), r(e.y)] * 3)
                else:
                    c1, c2, e = c[1], c[2], c[3]
                    c1x, c1y = (c1.x, c1.y) if hasattr(c1, "x") else c1
                    c2x, c2y = (c2.x, c2.y) if hasattr(c2, "x") else c2
                    prev[4], prev[5] = r(c1x), r(c1y)
                    cur["pts"].append([r(e.x), r(e.y), r(c2x), r(c2y), r(e.x), r(e.y)])
    return [s for s in out if len(s["pts"]) > 1]


def colour(c):
    if c is None or c.value is None or getattr(c, "alpha", 255) == 0:
        return None
    return "#%02x%02x%02x" % (c.red, c.green, c.blue)


def parse_layer(root_attrs, group_xml):
    """Parse one layer group on its own so its id is known for everything inside it."""
    attrs = " ".join(f'{k}="{v}"' for k, v in root_attrs.items() if k in ("width", "height", "viewBox"))
    doc = f'<svg xmlns="http://www.w3.org/2000/svg" {attrs}>{group_xml}</svg>'
    svg = SVG.parse(__import__("io").StringIO(doc), reify=True, ppi=25.4)
    items = []
    for el in svg.elements():
        if isinstance(el, Text):
            if not (el.text or "").strip():
                continue
            m = el.transform
            x, y = m.point_in_matrix_space((el.x, el.y)) if m is not None else (el.x, el.y)
            ang = math.degrees(math.atan2(m.b, m.a)) if m is not None else 0.0
            scale = math.sqrt(abs(m.a * m.d - m.b * m.c)) if m is not None else 1.0
            size = float(el.font_size or 3.36) * scale
            ls = el.values.get("letter-spacing", "0")
            try:
                ls = float(re.sub(r"[a-z]+$", "", str(ls))) * scale
            except ValueError:
                ls = 0.0
            items.append({"t": "text", "s": el.text, "x": r(x), "y": r(y), "size": r(size),
                          "weight": int(re.sub(r"\D", "", str(el.font_weight or 600)) or 600),
                          "anchor": el.anchor or "start", "ls": r(ls), "rot": r(ang),
                          "fill": colour(el.fill) or "#000000"})
        elif isinstance(el, Shape):
            p = Path(el)
            if len(p) == 0:
                continue
            sub = subpaths(p)
            if not sub:
                continue
            dash = el.values.get("stroke-dasharray")
            dash = [r(v) for v in re.split(r"[ ,]+", dash.strip())] if dash and dash != "none" else None
            items.append({"t": "path", "sub": sub, "fill": colour(el.fill), "stroke": colour(el.stroke),
                          "sw": r(el.stroke_width or 0.25) if el.stroke is not None else 0, "dash": dash})
    return items


def parse_card(path):
    tree = ET.parse(path)
    root = tree.getroot()
    if root.find(f".//{SVGNS}image") is not None:
        raise SystemExit(f"{path}: contains a raster <image>; final files must be vector + live text only")
    vb = [float(v) for v in re.split(r"[ ,]+", root.get("viewBox").strip())]
    card = {"file": path.name, "w": r(vb[2]), "h": r(vb[3]), "layers": {}}
    for g in root.iter(f"{SVGNS}g"):
        gid = g.get("id", "")
        if gid.startswith("layer-") and gid[6:] in LAYERS:
            xml = ET.tostring(g, encoding="unicode").replace("ns0:", "").replace(":ns0", "")
            items = parse_layer(root.attrib, xml)
            if items:
                card["layers"].setdefault(gid[6:], []).extend(items)
    return card


def collect(inputs):
    cards = []
    for inp in inputs:
        p = pathlib.Path(inp)
        files = sorted(p.glob("*.svg")) if p.is_dir() else [p]
        meta = {}
        idx = (p if p.is_dir() else p.parent) / "index.json"
        if idx.exists():
            raw = json.loads(idx.read_text())
            for e in (raw if isinstance(raw, list) else raw.get("files", raw.get("cards", []))):
                meta[pathlib.Path(e.get("file", "")).name] = e
        group = p.parent.name if p.is_dir() and p.name == "final" else p.name
        for f in files:
            c = parse_card(f)
            m = meta.get(f.name, {})
            c["design"] = m.get("design") or m.get("variant") or f.stem.rsplit("_", 2)[0]
            c["artist"] = m.get("artist") or ""
            c["group"] = group
            if c["layers"]:
                cards.append(c)
            else:
                print("skipped (no layer-* groups):", f)
    return cards


if __name__ == "__main__":
    out, inputs = sys.argv[1], sys.argv[2:]
    cards = collect(inputs)
    engine = (HERE / "engine.jsx").read_text()
    data = json.dumps({"cards": cards}, ensure_ascii=True, separators=(",", ":"))
    pathlib.Path(out).write_text(engine.replace("__DATA__", data))
    by = {}
    for c in cards:
        by.setdefault((c["group"], c["design"]), 0)
        by[(c["group"], c["design"])] += 1
    print(f"wrote {out}: {len(cards)} cards", by)
