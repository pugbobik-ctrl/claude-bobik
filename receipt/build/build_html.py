"""Render every strip in spec.py to receipt/<name>.html.

    python3 receipt/build/build_html.py
"""
import html
import json
import pathlib
import re

from spec import STRIPS, STYLES, FLOW_UNIT, LINEUP, BROWN, CREAM

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent
A = json.loads((HERE / "assets.json").read_text())


def fmt(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


def bearing(ch, weight, side):
    b = A["bearings"][str(weight)].get(ch)
    return b[0 if side == "l" else 1] if b else 0


def esc(s):
    return html.escape(s, quote=False)


def runs(s):
    """**bold** markup -> <b>"""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc(s))


def colon(s, style, cls="colon"):
    # the colon sits at x-height; between lining figures at display sizes lift it to the cap middle
    if STYLES[style][0] >= 8:
        return re.sub(r"(?<=\d):(?=\d)", f'<span class="{cls}">:</span>', s)
    return s


def optical(text, style, side):
    """Pull large type out by its first/last glyph's side bearing so the ink lines up with the column."""
    size, weight, _, tr, caps = STYLES[style]
    if size < 8 or not text:
        return 0
    ch = text[0] if side == "l" else text[-1]
    if caps:
        ch = ch.upper()
    return bearing(ch, weight, side)


def style_css():
    out = []
    for name, (size, weight, lh, tr, caps) in STYLES.items():
        out.append(f"  .s-{name} {{ font-size: calc({fmt(size)}cqw * var(--k)); font-weight: {weight}; "
                   f"line-height: {fmt(lh)}; --tr: {fmt(tr)}em;{' text-transform: uppercase;' if caps else ''} }}")
    return "\n".join(out)


def wordmark(orient, width, align="center", extra=""):
    ratio = A["wm_ratio"]
    if orient == "v":
        vb, d = f"0 0 100 {fmt(100 * ratio)}", A["wm_v"]
    else:
        vb, d = f"0 0 {fmt(100 * ratio)} 100", A["wm_h"]
    margin = "auto" if align == "center" else "0"
    return (f'<svg class="wm" viewBox="{vb}" role="img" aria-label="Dinner" '
            f'style="width: {fmt(width)}%; margin-inline: {margin};{extra}">'
            f'<path fill="currentColor" fill-rule="evenodd" d="{d}"/></svg>')


def barcode(b):
    rects = "".join(f'<rect x="{x}" width="{w}" height="{h if b["digits"] else 60}"/>' for x, w, h in A["bars"])
    style = f'width: {fmt(b["width"])}%;'
    if b["height"]:
        style += f' height: {fmt(b["height"])}cqw;'
    if b["digits"]:
        e = A["ean"]
        nums = (f'<text x="-3" y="66" text-anchor="end">{e[0]}</text>'
                f'<text x="24" y="66" text-anchor="middle">{e[1:7]}</text>'
                f'<text x="70" y="66" text-anchor="middle">{e[7:]}</text>')
        return (f'<svg class="barcode" viewBox="-11 0 117 70" style="{style}" role="img" aria-label="Barcode {e}">'
                f'<g fill="currentColor">{rects}{nums}</g></svg>')
    return (f'<svg class="barcode" viewBox="0 0 95 60" preserveAspectRatio="none" style="{style}" role="img" '
            f'aria-label="Barcode {A["ean"]}"><g fill="currentColor">{rects}</g></svg>')


def qr(b):
    d = []
    for y, row in enumerate(A["qr"]):
        for m in re.finditer(r"1+", row):
            d.append(f"M{m.start()} {y}h{len(m.group())}v1h-{len(m.group())}z")
    n = len(A["qr"])
    return (f'<svg class="qr" viewBox="0 0 {n} {n}" style="width: {fmt(b["width"])}%; margin-top: {fmt(b["mt"])}cqw" '
            f'role="img" aria-label="QR code"><path fill="currentColor" d="{"".join(d)}"/></svg>')


def mt(b):
    return f' style="margin-top: {fmt(b["mt"])}cqw"' if b.get("mt") else ""


def block(b):
    t = b["t"]
    if t == "text":
        style, align = b["style"], b["align"]
        lines = []
        for ln in b["lines"]:
            css = ""
            if align == "left":
                o = optical(ln, style, "l")
                css = f' style="margin-left: -{fmt(o)}em"' if o else ""
            lines.append(f'<span class="ln"{css}>{colon(esc(ln), style)}</span>')
        return f'<p class="s-{style} a-{align}"{mt(b)}>{"".join(lines)}</p>'
    if t == "row":
        style = b["style"]
        o = optical(b["right"], style, "r")
        tr = STYLES[style][3]
        rcss = f' style="margin-right: {fmt(-(o + tr))}em"' if o else ""
        css = []
        if b.get("mt"):
            css.append(f"margin-top: {fmt(b['mt'])}cqw")
        if b.get("indent"):
            css.append(f"padding-left: {fmt(b['indent'])}cqw")
        st = f' style="{"; ".join(css)}"' if css else ""
        return (f'<div class="row s-{style}"{st}><span>{colon(esc(b["left"]), style)}</span>'
                f'<span{rcss}>{colon(esc(b["right"]), style)}</span></div>')
    if t == "rule":
        return f'<div class="rule rule-{b["kind"]}" style="margin-block: {fmt(b["mt"])}cqw {fmt(b["mb"])}cqw"></div>'
    if t == "wordmark":
        css = f' margin-top: {fmt(b["mt"])}cqw;' if b["mt"] else ""
        return wordmark(b["orient"], b["width"], b["align"], css)
    if t == "collab":
        return (f'<p class="collab s-{b["style"]}"{mt(b)}><span>Colorblock</span>'
                f'<span class="x s-body">×</span><span>DNA</span></p>')
    if t == "barcode":
        return f'<div{mt(b)}>{barcode(b)}</div>' if b.get("mt") else barcode(b)
    if t == "qr":
        return qr(b)
    if t == "list":
        cls = ["list", f"s-{b['style']}"]
        if b["numbered"]:
            cls.append("numbered")
        if b["ruled"]:
            cls.append("ruled")
        items = []
        for i, it in enumerate(b["items"], 1):
            num = f'<span class="num s-{b["num_style"]}">{i:02d}</span>' if b["numbered"] else ""
            pre = f'<span class="pre">{esc(b["prefix"])}</span>' if b["prefix"] else ""
            q = f'<span class="qty">{esc(b["qty"])}</span>' if b["qty"] else ""
            items.append(f"<li>{num}{pre}<span>{esc(it)}</span>{q}</li>")
        return f'<ol class="{" ".join(cls)}"{mt(b)}>\n      ' + "\n      ".join(items) + "\n    </ol>"
    if t == "flow":
        unit = runs(FLOW_UNIT)
        return f'<p class="flow s-flow"{mt(b)}>{unit * b["repeat"]}</p>'
    if t == "hero":
        side = "".join(f'<span class="{"x s-sub" if s == "×" else ""}">{s}</span>' for s in b["side"])
        return (f'<div class="hero" style="grid-template-columns: {fmt(b["wm_width"])}% 1fr">\n      '
                f'{wordmark("v", 100)}\n      <p class="side s-side">{side}</p>\n    </div>')
    if t == "vtext":
        return (f'<div class="vtext s-{b["style"]}"{mt(b)}>'
                + "".join(f"<p>{colon(esc(l), b['style'], 'colon-v')}</p>" for l in b["lines"]) + "</div>")
    if t == "columns":
        groups = "\n".join('        <div class="group">' + "".join(block(x) for x in g) + "</div>" for g in b["right"])
        return (f'<div class="columns" style="grid-template-columns: {fmt(b["left"])}% 1fr; gap: {fmt(b["gap"])}cqw">\n'
                f'      {wordmark("v", 100)}\n      <div class="col">\n{groups}\n      </div>\n    </div>')
    raise ValueError(t)


SWIRL_CSS = """
  /* the poster's spin-blurred caramel, as rings around a point off the top-left */
  .swirl {{
    background:
      url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .22 0'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)'/%3E%3C/svg%3E"),
      radial-gradient(circle at -45% -6%, {rings});
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
"""

TORN = """
  .paper {
    --z: 3.2cqw; /* torn-edge tooth */
    -webkit-mask:
      conic-gradient(from -45deg at bottom, #0000, #000 1deg 89deg, #0000 90deg) bottom / var(--z) 51% repeat-x,
      conic-gradient(from 135deg at top, #0000, #000 1deg 89deg, #0000 90deg) top / var(--z) 51% repeat-x;
    mask:
      conic-gradient(from -45deg at bottom, #0000, #000 1deg 89deg, #0000 90deg) bottom / var(--z) 51% repeat-x,
      conic-gradient(from 135deg at top, #0000, #000 1deg 89deg, #0000 90deg) top / var(--z) 51% repeat-x;
  }
"""

STUBS = """
  /* tear-off stubs: punched notches at every perforation */
  .paper {
    --r: 3.4cqw;
    position: relative;
    -webkit-mask:
      radial-gradient(circle at 0 0, #0000 var(--r), #000 calc(var(--r) + .5px)) 0 0 / 51% 51% no-repeat,
      radial-gradient(circle at 100% 0, #0000 var(--r), #000 calc(var(--r) + .5px)) 100% 0 / 51% 51% no-repeat,
      radial-gradient(circle at 0 100%, #0000 var(--r), #000 calc(var(--r) + .5px)) 0 100% / 51% 51% no-repeat,
      radial-gradient(circle at 100% 100%, #0000 var(--r), #000 calc(var(--r) + .5px)) 100% 100% / 51% 51% no-repeat;
    mask:
      radial-gradient(circle at 0 0, #0000 var(--r), #000 calc(var(--r) + .5px)) 0 0 / 51% 51% no-repeat,
      radial-gradient(circle at 100% 0, #0000 var(--r), #000 calc(var(--r) + .5px)) 100% 0 / 51% 51% no-repeat,
      radial-gradient(circle at 0 100%, #0000 var(--r), #000 calc(var(--r) + .5px)) 0 100% / 51% 51% no-repeat,
      radial-gradient(circle at 100% 100%, #0000 var(--r), #000 calc(var(--r) + .5px)) 100% 100% / 51% 51% no-repeat;
  }
  .paper + .paper::before {
    content: "";
    position: absolute;
    top: 0;
    left: var(--r);
    right: var(--r);
    height: .6cqw;
    background: radial-gradient(circle, currentColor 40%, transparent 45%) 0 50% / 2.4cqw 100% repeat-x;
    opacity: .5;
  }
"""

BASE = """<html lang="{lang}">
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Wix+Madefor+Display:wght@400;500;600;700;800&display=swap">
<!-- generated by receipt/build/build_html.py from spec.py; edit the spec, not this file -->
<style>
  :root {{
    --table: #d8d7d2;
    --font: "Wix Madefor Display", "Helvetica Neue", Arial, sans-serif;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{ --table: #1b1b1a; }}
  }}
  :root[data-theme="dark"] {{ --table: #1b1b1a; }}

  html, body {{ background: var(--table); margin: 0; }}
  body {{
    min-height: 100vh;
    display: grid;
    justify-items: center;
    align-items: start;
    padding: 40px 16px 64px;
    box-sizing: border-box;
  }}

  /* {mm} mm roll; every size is in cqw, a percent of the paper width */
  .roll {{
    width: min(100%, {px}px);
    container-type: inline-size;
    filter: drop-shadow(0 18px 24px rgba(0, 0, 0, .18)) drop-shadow(0 2px 3px rgba(0, 0, 0, .12));
  }}
  .paper {{
    --k: {k};
    padding: {pt}cqw {px_}cqw {pb}cqw;
    background:
      linear-gradient(90deg, rgba(0, 0, 0, .035), transparent 6%, transparent 94%, rgba(0, 0, 0, .035)),
      {paper};
    color: {ink};
    font-family: var(--font);
    font-weight: 500;
    /* the font ships kern only (no tnum, no case): kerning on, nothing synthesised */
    font-kerning: normal;
    font-feature-settings: "kern" 1;
    font-synthesis: none;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
  }}
  .paper p, .paper ol {{ margin: 0; padding: 0; }}

  /* type scale, shared with the Illustrator script */
{styles}
  [class*="s-"] {{ letter-spacing: var(--tr); }}
  .ln {{ display: block; }}
  .a-center {{ text-align: center; }}
  .a-right {{ text-align: right; }}
  /* tracking trails the last glyph; give it back so centred and right-set lines sit true */
  .a-center, .a-right {{ margin-right: calc(var(--tr) * -1); }}
  .colon {{ position: relative; top: -.1em; }}
  .colon-v {{ position: relative; left: .1em; }} /* same lift, in a column turned clockwise */

  .row {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 3cqw;
  }}
  .row > :last-child {{ text-align: right; white-space: nowrap; margin-right: calc(var(--tr) * -1); }}

  .collab {{
    display: flex;
    justify-content: center;
    align-items: baseline;
    gap: .55em;
    margin-right: calc(var(--tr) * -1);
  }}
  .collab .x, .side .x {{ letter-spacing: 0; }}

  .rule {{ height: .7cqw; }}
  .rule-dash {{ background: repeating-linear-gradient(90deg, currentColor 0 2.2cqw, transparent 2.2cqw 3.6cqw); }}
  .rule-double {{ height: 2cqw; border-block: .55cqw solid; box-sizing: border-box; }}
  .rule-thin {{ height: .35cqw; background: repeating-linear-gradient(90deg, currentColor 0 1.4cqw, transparent 1.4cqw 2.4cqw); }}
  .rule-thinDouble {{ height: 1.4cqw; border-block: .35cqw dashed; box-sizing: border-box; }}

  .wm, .barcode, .qr {{ display: block; }}
  .barcode, .qr {{ margin-inline: auto; }}
  .barcode text {{ font: 500 8.4px var(--font); letter-spacing: .02em; }}

  .list {{ list-style: none; }}
  .list li {{ display: flex; align-items: baseline; }}
  .list li > span:not(.num):not(.pre):not(.qty) {{ flex: 1; }}
  .list .num {{ flex: 0 0 7.5cqw; }}
  .list .pre {{ flex: 0 0 1.6em; }}
  .list li {{ white-space: nowrap; }}
  .list li + li {{ margin-top: .1em; }}
  .ruled {{ border-block: 1.2cqw solid; }}
  .ruled li {{ padding: 2.4cqw 0; }}
  .ruled li + li {{ margin: 0; border-top: .4cqw solid; }}

  /* the runner's long middle: flush left with a considered rag, never hyphenated */
  .flow {{ text-wrap: pretty; hyphens: manual; }}
  .flow b {{ font-weight: 800; }}

  .hero {{ display: grid; }}
  .side {{
    writing-mode: vertical-rl;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-block: 18% 6%;
  }}
  .side span:last-child {{ font-weight: 800; letter-spacing: -.02em; font-size: 1.2em; }}
  .vtext {{ writing-mode: vertical-rl; }}

  .columns {{ display: grid; }}
  .col {{ display: flex; flex-direction: column; justify-content: space-between; min-width: 0; }}
{extra}
  @media print {{
    @page {{ margin: 0; }}
    html, body {{ background: #fff; }}
    body {{ display: block; min-height: 0; padding: 0; }}
    .roll {{ width: {print_mm}mm; margin: 0 auto; filter: none; }}
    .paper {{ -webkit-mask: none; mask: none; }}
  }}
</style>

<main class="roll">
{body}</main>
"""


def render(name, s):
    rings = ", ".join(f"{c} {p}px" for c, p in A["rings"])
    extra = TORN if s["edge"] == "torn" else STUBS
    if s.get("paper") == "swirl" or any(st.get("paper") == "swirl" for st in s.get("stubs", [])):
        extra += SWIRL_CSS.format(rings=rings)
    label = 'aria-label="Colorblock × DNA Dinner, 10 October 2026"'

    def article(blocks, paper, ink, extra_cls=""):
        cls = "paper" + (" swirl" if paper == "swirl" else "") + extra_cls
        style = ""
        if paper != "swirl" and paper != s["paper"]:
            style += f" background: {paper};"
        if ink != s["ink"]:
            style += f" color: {ink};"
        st = f' style="{style.strip()}"' if style else ""
        inner = "\n    ".join(block(b) for b in blocks)
        return f'  <article class="{cls}" {label}{st}>\n    {inner}\n  </article>\n'

    if s["edge"] == "stubs":
        body = "".join(article(st["blocks"], st.get("paper", s["paper"]), st.get("ink", s["ink"]),
                               " short" if st.get("short") else "") for st in s["stubs"])
        extra += "  .short { padding-block: 6cqw; }\n"
    else:
        body = article(s["blocks"], s["paper"], s["ink"])

    pt, px_, pb = s["pad"]
    page = BASE.format(
        lang=s.get("lang", "en"), title=s["title"], mm=s["width_mm"], px=s["width_px"],
        k=fmt(s.get("scale", 1)), pt=fmt(pt), px_=fmt(px_), pb=fmt(pb),
        paper="transparent" if s["paper"] == "swirl" else s["paper"],
        ink=s["ink"], styles=style_css(), extra=extra, body=body,
        print_mm=s["width_mm"] - 8,
    )
    (OUT / f"{name}.html").write_text(page)


if __name__ == "__main__":
    for name, s in STRIPS.items():
        render(name, s)
        print("wrote", name)
