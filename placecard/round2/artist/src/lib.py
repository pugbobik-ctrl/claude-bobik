import html, textwrap
FONTDIR = "file:///tmp/claude-0/-home-user-claude-bobik/6a3dcf92-132a-5018-88ad-a2068c46056a/scratchpad/dielines/fonts/"
INK = "#111111"; LEM = "#feed95"; LEMD = "#e9d36c"; PAPER = "#f1efe8"; CLOTH = "#fbfaf5"; WALL = "#e7e4d8"; GREY = "#cfcabb"; GHOST = "#d9d5c6"

W, H = 1800, 1260

def esc(s): return html.escape(s, quote=False)

def T(x, y, s, size=20, w=500, anchor="start", fill=INK, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}" fill="{fill}" {extra}>{esc(s)}</text>'

def TL(x, y, lines, size=20, lh=None, w=500, anchor="start", fill=INK, extra=""):
    lh = lh or size * 1.28
    return "".join(T(x, y + i * lh, s, size, w, anchor, fill, extra) for i, s in enumerate(lines))

def R(x, y, w, h, fill=LEM, stroke=INK, sw=2, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def L(x1, y1, x2, y2, stroke=INK, sw=2, dash="", extra=""):
    d = f'stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" {d} {extra}/>'

def P(d, fill="none", stroke=INK, sw=2, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'

def E(cx, cy, rx, ry, fill="none", stroke=INK, sw=2, extra=""):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def C(cx, cy, r, fill="none", stroke=INK, sw=2, extra=""):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def G(content, tx=0, ty=0, extra=""):
    return f'<g transform="translate({tx},{ty})" {extra}>{content}</g>'

def scribble(x, y, w, amp=4, n=None, sw=2, stroke=INK):
    """handwriting-ish squiggle"""
    n = n or max(3, int(w / 9))
    d = f"M{x},{y}"
    step = w / n
    for i in range(n):
        d += f" q{step/4:.1f},{-amp * (1 if i % 2 == 0 else 1.6):.1f} {step/2:.1f},0 t{step/2:.1f},{(amp if i%3==0 else -amp*0.6):.1f}"
    return P(d, stroke=stroke, sw=sw)

def arrow(x1, y1, x2, y2, sw=2.5, stroke=INK, curve=0, head=11, dash=""):
    import math
    if curve:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy) or 1
        cx, cy = mx - dy / ln * curve, my + dx / ln * curve
        d = f"M{x1},{y1} Q{cx},{cy} {x2},{y2}"
        ang = math.atan2(y2 - cy, x2 - cx)
    else:
        d = f"M{x1},{y1} L{x2},{y2}"
        ang = math.atan2(y2 - y1, x2 - x1)
    a1 = ang + math.radians(155); a2 = ang - math.radians(155)
    hx1, hy1 = x2 + head * math.cos(a1), y2 + head * math.sin(a1)
    hx2, hy2 = x2 + head * math.cos(a2), y2 + head * math.sin(a2)
    da = f'stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" {da}/>'
            f'<path d="M{hx1:.1f},{hy1:.1f} L{x2},{y2} L{hx2:.1f},{hy2:.1f}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')

def callout(x, y, tx, ty, lines, size=19, anchor="start", curve=0, frm=None):
    """label at (tx,ty) with arrow to (x,y). frm = explicit arrow start"""
    t = TL(tx, ty, lines, size, anchor=anchor, w=500)
    if frm:
        sx, sy = frm
    else:
        sy = ty + (len(lines) - 1) * size * 1.28 + 8
        sx = tx + (0 if anchor == "start" else 0)
        if anchor == "start": sx = tx + 6
    return t + arrow(sx, sy, x, y, sw=1.8, curve=curve, head=9)

# ---------- scene pieces ----------
def silhouette(x, base=250, head_y=120, fill=GHOST, s=1.0):
    return (f'<circle cx="{x}" cy="{head_y}" r="{36*s}" fill="{fill}"/>'
            f'<path d="M{x-100*s},{base} C{x-100*s},{base-65*s} {x-55*s},{base-85*s} {x},{base-85*s} C{x+55*s},{base-85*s} {x+100*s},{base-65*s} {x+100*s},{base} Z" fill="{fill}"/>')

def plate(cx, cy, rx=105, shadow=True):
    ry = rx * 0.27
    s = E(cx + 4, cy + 7, rx, ry, fill="#00000018", stroke="none") if shadow else ""
    s += E(cx, cy, rx, ry, fill="#ffffff", stroke=INK, sw=2)
    s += E(cx, cy + 1, rx * 0.64, ry * 0.62, fill="#fbfbf8", stroke="#bdb8a8", sw=1.5)
    return s

def napkin(x, y, w=70, h=34):
    sk = 14
    s = P(f"M{x+sk},{y} L{x+w+sk},{y} L{x+w},{y+h} L{x},{y+h} Z", fill="#ffffff", stroke=INK, sw=2)
    s += L(x + sk * 0.5 + 6, y + h * 0.5, x + w + sk * 0.5 - 6, y + h * 0.5, stroke="#c9c4b4", sw=1.5)
    return s

def glass(x, yb, h=125, wine=True, rim=28):
    top = yb - h
    bowl = f"M{x-rim},{top} C{x-rim-3},{top+52} {x-14},{top+72} {x},{top+72} C{x+14},{top+72} {x+rim+3},{top+52} {x+rim},{top} Z"
    s = ""
    if wine:
        s += P(f"M{x-rim+2},{top+26} C{x-rim},{top+55} {x-14},{top+70} {x},{top+70} C{x+14},{top+70} {x+rim},{top+55} {x+rim-2},{top+26} Z", fill="#d8d0a0", stroke="none")
    s += P(bowl, fill="#ffffff55", stroke=INK, sw=2)
    s += E(x, top, rim, 6, fill="none", stroke=INK, sw=1.6)
    s += L(x, top + 72, x, yb - 4, sw=2.4)
    s += E(x, yb, 27, 6.5, fill="#ffffff", stroke=INK, sw=2)
    return s

def lamp(x, yb, shade_h=92, top_w=40, bot_w=130, glow=True):
    ytop = yb - 70 - shade_h
    ybot = ytop + shade_h
    s = ""
    if glow:
        s += f'<ellipse cx="{x}" cy="{yb+6}" rx="{bot_w*1.15}" ry="{bot_w*0.30}" fill="url(#glow)"/>'
    s += E(x, yb, 24, 6.5, fill=INK, stroke=INK)
    s += R(x - 3.5, ybot, 7, yb - ybot, fill=INK, stroke=INK, sw=1)
    s += P(f"M{x-top_w/2},{ytop} L{x+top_w/2},{ytop} L{x+bot_w/2},{ybot} L{x-bot_w/2},{ybot} Z", fill=INK, stroke=INK, sw=2)
    s += E(x, ytop, top_w / 2, 4, fill="#2a2a2a", stroke=INK, sw=1.5)
    s += E(x, ybot, bot_w / 2, 9, fill="#fff3b0", stroke=INK, sw=2)
    return s

def tent(x, yb, w, h, fill=LEM, extra_inside="", depth=10):
    """front face of a tent card seen from the front, slightly above. x = centre."""
    x0 = x - w / 2
    s = E(x + 5, yb + 3, w / 2 + 6, 8, fill="#00000020", stroke="none")
    s += P(f"M{x0},{yb} L{x0},{yb-h} L{x0+w},{yb-h} L{x0+w},{yb} Z", fill=fill, stroke=INK, sw=2)
    s += P(f"M{x0},{yb-h} L{x0+8},{yb-h-depth} L{x0+w+8},{yb-h-depth} L{x0+w},{yb-h} Z", fill=LEMD, stroke=INK, sw=1.6)
    s += extra_inside
    return s

def scene_base(xs=(), head_y=110, base=232, fills=None):
    """wall + ghost guests + table. local coords 1120x515"""
    s = R(0, 0, 1120, 515, fill=WALL, stroke="none")
    for i, x in enumerate(xs):
        s += silhouette(x, base=base, head_y=head_y, fill=(fills[i] if fills else GHOST))
    s += R(0, 232, 1120, 190, fill=CLOTH, stroke=INK, sw=2)
    s += R(0, 422, 1120, 93, fill="#f2f0e7", stroke=INK, sw=2)
    for xx in (140, 380, 620, 860, 1040):
        s += P(f"M{xx},424 C{xx+8},460 {xx-8},480 {xx},515", stroke="#d4d0c0", sw=1.5)
    return s

def rot(content, ang, cx, cy):
    return f'<g transform="rotate({ang} {cx} {cy})">{content}</g>'

DEFS = f'''<defs>
<style>
@font-face{{font-family:'Wix Madefor Text';font-weight:400;src:url('{FONTDIR}WixMadeforText-400.ttf')}}
@font-face{{font-family:'Wix Madefor Text';font-weight:500;src:url('{FONTDIR}WixMadeforText-500.ttf')}}
@font-face{{font-family:'Wix Madefor Text';font-weight:600;src:url('{FONTDIR}WixMadeforText-600.ttf')}}
@font-face{{font-family:'Wix Madefor Text';font-weight:700;src:url('{FONTDIR}WixMadeforText-700.ttf')}}
text{{font-family:'Wix Madefor Text',sans-serif}}
</style>
<radialGradient id="glow"><stop offset="0" stop-color="#fff4b8" stop-opacity=".95"/><stop offset=".6" stop-color="#feed95" stop-opacity=".45"/><stop offset="1" stop-color="#feed95" stop-opacity="0"/></radialGradient>
<linearGradient id="mir" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f8fafb"/><stop offset=".45" stop-color="#aab4ba"/><stop offset=".6" stop-color="#d9dfe3"/><stop offset="1" stop-color="#8f9aa1"/></linearGradient>
<radialGradient id="sun"><stop offset="0" stop-color="#ffffff" stop-opacity="1"/><stop offset=".35" stop-color="#feed95" stop-opacity=".9"/><stop offset="1" stop-color="#feed95" stop-opacity="0"/></radialGradient>
</defs>'''

def header(num, title_ru, title_en, pitch):
    s = R(0, 0, W, H, fill=PAPER, stroke="none")
    s += R(0, 0, W, 135, fill=LEM, stroke="none")
    s += L(0, 135, W, 135, sw=2)
    s += T(40, 92, str(num), 78, 700)
    s += T(130, 70, title_ru, 46, 700)
    s += T(130, 112, title_en, 26, 500)
    s += TL(W - 40, 62, pitch, 22, anchor="end", w=500)
    return s

def panel_frame(x, y, w, h, label, n):
    s = R(x, y, w, h, fill=WALL, stroke=INK, sw=2, rx=10)
    s += C(x + 30, y + 30, 18, fill=INK)
    s += T(x + 30, y + 37, str(n), 21, 700, "middle", LEM)
    s += T(x + 58, y + 37, label, 21, 600)
    return s

def sheet(num, title_ru, title_en, pitch, scene, flat, panels, captions, spec, scene_note=""):
    """scene: svg for 1120x515 area; flat: svg for 570x520 area; panels: list of 4 svg strings (410x350 local, frame excluded)"""
    out = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{DEFS}'
    out += header(num, title_ru, title_en, pitch)
    out += G(scene, 40, 160)
    out += R(40, 160, 1120, 515, fill="none", stroke=INK, sw=2.5)
    out += R(1190, 160, 570, 515, fill=CLOTH, stroke=INK, sw=2.5)
    out += G(flat, 1190, 160)
    out += T(1204, 186, "ПЕЧАТЬ / PRINT  ·  чёрный на лимонном #feed95", 15, 600, extra='opacity=".7"')
    for i, (label, heading, body) in enumerate(panels):
        x = 40 + i * 430
        out += panel_frame(x, 700, 410, 400, label, i + 1)
        out += f'<clipPath id="pc{i}"><rect x="0" y="-50" width="410" height="400" rx="10"/></clipPath>'
        out += G(R(0, 0, 410, 350, fill=WALL, stroke="none") + G(body, 0, -30), x, 750, f'clip-path="url(#pc{i})"') if False else ""
        out += G(G(body, 0, -30) + TL(205, 24, heading if isinstance(heading, list) else [heading], 17, 21, 600, "middle"), x, 750, f'clip-path="url(#pc{i})"')
        cap = captions[i] if isinstance(captions[i], list) else textwrap.wrap(captions[i], 40)
        out += TL(x + 6, 1128, cap, 18.5, 23, w=500)
    out += L(40, 1222, W - 40, 1222, sw=1.2, stroke="#00000055")
    out += T(40, 1246, spec, 17, 500, extra='opacity=".8"')
    out += '</svg>'
    return out

def pencil(x, y, ang=-40, ln=110):
    """tip at (x,y), body extends away at angle"""
    g = (f'<path d="M0,0 L16,-5 L16,5 Z" fill="#e8d9a8" stroke="{INK}" stroke-width="1.5"/>'
         f'<path d="M0,0 L5,-1.6 L5,1.6 Z" fill="{INK}"/>'
         f'<rect x="16" y="-5" width="{ln-16-12}" height="10" fill="{INK}" stroke="{INK}" stroke-width="1.5"/>'
         f'<rect x="{ln-12}" y="-5" width="12" height="10" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
    return f'<g transform="translate({x},{y}) rotate({ang})">{g}</g>'

def mini(y=215):
    return R(0, y, 410, 400 - y, fill=CLOTH, stroke="none") + L(0, y, 410, y, sw=2)
