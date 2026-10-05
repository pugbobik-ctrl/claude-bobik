"""Write receipt/illustrator/dinner-receipts.jsx: the engine plus every strip from spec.py.

    python3 receipt/build/build_jsx.py
"""
import copy
import json
import pathlib

from spec import STRIPS, STYLES, FLOW_UNIT, ORDER, INK, PAPER, BROWN, CREAM

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "illustrator" / "dinner-receipts.jsx"
A = json.loads((HERE / "assets.json").read_text())


def bearing(ch, weight, side):
    b = A["bearings"][str(weight)].get(ch)
    return b[0 if side == "l" else 1] if b else 0


def optical(text, style, side):
    size, weight, _, _, caps = STYLES[style]
    if size < 8 or not text:
        return 0
    ch = text[0] if side == "l" else text[-1]
    return bearing(ch.upper() if caps else ch, weight, side)


def prep(blocks):
    """Bake the optical-margin offsets (em) into the blocks, as build_html does in CSS."""
    for b in blocks:
        if b["t"] == "text" and b["align"] == "left":
            b["ol"] = [optical(ln, b["style"], "l") for ln in b["lines"]]
        if b["t"] == "row":
            b["or"] = optical(b["right"], b["style"], "r")
        if b["t"] == "columns":
            for g in b["right"]:
                prep(g)
    return blocks


strips = copy.deepcopy(STRIPS)
for s in strips.values():
    if "blocks" in s:
        prep(s["blocks"])
    for st in s.get("stubs", []):
        prep(st["blocks"])

data = dict(
    styles={k: list(v) for k, v in STYLES.items()},
    strips=strips, order=ORDER, flow=FLOW_UNIT,
    colors=dict(ink=INK, paper=PAPER, brown=BROWN, cream=CREAM),
    wm_v=A["wm_v"], wm_h=A["wm_h"], wm_ratio=A["wm_ratio"],
    ean=A["ean"], bars=A["bars"], qr=A["qr"], rings=A["rings"], px=380,
)
engine = (HERE / "engine.jsx").read_text()
OUT.parent.mkdir(exist_ok=True)
# ExtendScript has no JSON object, but JSON is a valid object literal; \\u escapes keep the file ASCII
OUT.write_text(engine.replace("__DATA__", json.dumps(data, ensure_ascii=True, separators=(",", ":"))))
print("wrote", OUT, OUT.stat().st_size // 1024, "KB")
