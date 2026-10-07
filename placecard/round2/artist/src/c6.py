from lib import *

def mirror(x, y, r, shine=True):
    s = C(x, y, r, fill="url(#mir)", stroke=INK, sw=2)
    if shine:
        s += P(f"M{x-r*0.55},{y-r*0.1} Q{x-r*0.4},{y-r*0.6} {x+r*0.1},{y-r*0.7}", stroke="#fff", sw=max(2, r*0.1))
    return s

def ray(pts, glow=True, w=2.2, arrow_end=True):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    s = ""
    if glow:
        s += f'<path d="{d}" fill="none" stroke="#fff3a0" stroke-width="{w*4.2}" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>'
    s += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}" stroke-dasharray="7 5" stroke-linecap="round" stroke-linejoin="round"/>'
    return s

def mirror_card(x, yb, n1="Sophia", n2="Zhuravkova", w=136, h=124, lean=-6, fs=19, r=27, with_ceiling=False):
    g = tent(x, yb, w, h, depth=9)
    g += mirror(x, yb - h + 20 + r + 6, r)
    g += T(x, yb - 32, n1, fs, 700, "middle") + T(x, yb - 10, n2, fs - 1, 700, "middle")
    return f'<g transform="rotate({lean} {x} {yb})">{g}</g>'

def lit_face(x, y, r=34):
    s = f'<circle cx="{x}" cy="{y}" r="{r*2.3}" fill="url(#sun)" opacity=".95"/>' + f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fffdf0" stroke="{INK}" stroke-width="2"/>'
    s += f'<circle cx="{x-r*0.35}" cy="{y-r*0.15}" r="{r*0.07}" fill="{INK}"/><circle cx="{x+r*0.35}" cy="{y-r*0.15}" r="{r*0.07}" fill="{INK}"/>'
    s += f'<ellipse cx="{x}" cy="{y+r*0.42}" rx="{r*0.2}" ry="{r*0.14}" fill="{INK}"/>'
    return s

def scene():
    xs = (180, 565, 950)
    s = scene_base(xs, head_y=118, base=232)
    # speaker Andrey lit
    s += lit_face(950, 118)
    s += lamp(372, 292, 92, 38, 120)
    # rays
    s += ray([(392, 224), (565, 262)])
    s += ray([(565, 262), (930, 140)])
    s += arrow(900, 150, 925, 140, sw=2.5, head=9)
    # cards
    s += mirror_card(180, 300, "Igor", "Zotov", fs=19, lean=-4)
    s += mirror_card(565, 300, lean=-14)
    s += mirror_card(950, 300, "Andrey", "Lee", fs=19, lean=-3)
    for x in xs:
        s += plate(x, 362, 100) + napkin(x - 40, 348, 66, 28) + glass(x + 142, 352, 112)
    s += callout(565, 252, 590, 468, [], 1) if False else ""
    s += TL(80, 52, ["зеркальный картон в круглом окне", "карточки — и маленькие прожекторы"], 19, 24, 600)
    s += TL(640, 52, ["тому, кто говорит, нужен свет:", "сосед ловит лампу и дарит её ему"], 19, 24, 600)
    s += arrow(380, 72, 490, 252, sw=1.8, curve=14, head=9) if False else ""
    s += TL(560, 452, ["лампа — одна, свет у каждого свой: кто-то держит наклон карточки,", "кто-то говорит — и лицо у него светится"], 17, 22, 600, "middle")
    return s

def flat():
    sc = 2.9; tw, th = 110*sc, 50*sc
    ox, oy = 22, 54
    s = R(ox, oy, tw, 2*th, fill=LEM, stroke=INK, sw=2.5)
    ry = oy + th
    cx, cy = ox + tw/2, oy + 62
    s += R(cx - 28*sc*0.5, cy - 28*sc*0.5, 28*sc, 28*sc, fill="none", stroke=INK, sw=1.2, extra='stroke-dasharray="4 4" opacity=".0"')
    s += C(cx, cy, 22.5*sc*0.5*1.0 + 0, fill="url(#mir)", stroke=INK, sw=2)
    s += T(cx, oy + th - 52 + 52 - 6 + 14, "", 1)
    s += T(cx, oy + 120, "Sophia Zhuravkova", 21, 700, "middle")
    s += T(cx, oy + 24, "", 1)
    s += T(ox + tw + 8, oy + 40, "окно Ø 45", 12, 600) + L(cx + 33, cy, ox + tw + 4, cy, sw=1) if False else T(ox + tw + 6, cy - 4, "← окно Ø45", 12, 600)
    s += L(ox - 8, ry, ox + tw + 8, ry, dash="10 6", sw=2) + T(ox + tw + 6, ry + 4, "ребро", 12, 600)
    low = T(cx, ry + 26, "Sophia Zhuravkova", 13, 600, "middle", extra='opacity=".75"')
    low += TL(cx, ry + 62, ["Тому, кто говорит, нужен свет.", "Поймай лампу — и подари её ему.", "Только не в глаза."], 14.5, 20, 600, "middle")
    s += rot(low, 180, cx, ry + th/2)
    s += T(ox, oy + 2*th + 18, "110×100 мм · зеркальный картон 56×56 — клеится изнутри", 12.5, 600)
    # side view
    ox2, oy2 = 40, 410
    s += T(ox2 - 18, oy2 - 20, "как стоит и ловит свет (вид сбоку)", 13, 600)
    s += L(ox2 - 18, oy2 + 100, ox2 + 500, oy2 + 100, sw=2)
    # lamp
    s += P(f"M{ox2+10},{oy2+30} L{ox2+60},{oy2+30} L{ox2+80},{oy2+60} L{ox2-10},{oy2+60} Z", fill=INK, stroke=INK)
    s += L(ox2 + 35, oy2 + 60, ox2 + 35, oy2 + 100, sw=4)
    # tent leaning
    s += P(f"M{ox2+250},{oy2+100} L{ox2+290},{oy2+14} L{ox2+330},{oy2+100} Z", fill=LEM, stroke=INK, sw=2)
    s += L(ox2 + 272, oy2 + 53, ox2 + 284, oy2 + 30, sw=7, stroke="#8f9aa1")
    s += ray([(ox2 + 70, oy2 + 62), (ox2 + 276, oy2 + 42)], w=1.8)
    s += ray([(ox2 + 276, oy2 + 42), (ox2 + 440, oy2 - 4)], w=1.8)
    s += f'<circle cx="{ox2+470}" cy="{oy2-6}" r="26" fill="url(#sun)"/>' + C(ox2 + 470, oy2 - 6, 11, fill="#fffdf0", stroke=INK, sw=1.6)
    s += T(ox2 + 470, oy2 + 40, "лицо", 12, 600, "middle")
    return s

def storyboard():
    BG = R(0, 30, 410, 380, fill=CLOTH, stroke="none")
    # 1: arrival -- mirror reflects ceiling
    P1 = BG + plate(205, 345, 100)
    P1 += mirror_card(205, 312, "Sophia", "Zhuravkova", w=210, h=168, lean=-8, fs=24, r=48)
    P1 += P("M190,160 L205,178 L220,160 Z", fill=INK, stroke=INK) if False else ""
    P2 = BG + silhouette(70, base=252, head_y=170, s=0.75) + silhouette(340, base=252, head_y=170, s=0.75)
    P2 += R(0, 252, 410, 160, fill=CLOTH, stroke=INK, sw=2)
    P2 += lit_face(340, 170, 24)
    P2 += lamp(205, 318, 72, 26, 90, glow=False)
    P2 += mirror_card(95, 345, "", "", w=100, h=84, lean=-12, fs=1, r=20)
    P2 += ray([(222, 262), (95, 296)], w=1.8) + ray([(95, 296), (318, 190)], w=1.8)
    P2 += T(205, 395, "говорит — значит, его надо подсветить", 15, 600, "middle")
    # 3: several mirrors on one face
    P3 = BG + silhouette(205, base=170, head_y=120, s=0.9)
    P3 += lit_face(205, 120, 30)
    xs = [50, 130, 280, 360]
    for x in xs:
        P3 += mirror_card(x, 345, "", "", w=64, h=62, lean=-10 if x < 205 else 10, fs=1, r=14)
    for x in xs:
        P3 += ray([(x, 300), (205, 140)], w=1.5)
    P3 += T(205, 394, "четыре зайчика на одной щеке", 15, 600, "middle")
    # 4: finale: all to one point on the ceiling
    P4 = BG
    P4 += f'<circle cx="205" cy="90" r="80" fill="url(#sun)"/>' + C(205, 90, 14, fill="#fff", stroke=INK, sw=1.6)
    xs = [40, 125, 205, 285, 370]
    for x in xs:
        P4 += mirror_card(x, 345, "", "", w=64, h=62, lean=(205 - x) / 14, fs=1, r=14)
        P4 += ray([(x, 295), (205, 100)], w=1.5)
    P4 += T(205, 394, "тост: все карточки — в одну точку", 15, 600, "middle")
    return [("Приход", ["зеркальное окно смотрит", "куда придётся — на потолок"], P1),
            ("За разговором", ["сосед ловит лампу", "и дарит её говорящему"], P2),
            ("Горячее", ["кому-то везёт больше всех:", "сразу четыре огонька"], P3),
            ("Тост", ["все карточки — в одну точку:", "общий маленький свет"], P4)]

caps = [
    "На столе — карточка с круглым зеркалом. Гостья вертит её, зайчик бежит по потолку. Первая улыбка.",
    "Кто говорит — тому нужно лицо. Сосед поворачивает карточку к лампе и направляет свет на говорящего.",
    "Свет — подарок и игра: интереснее всех рассказывает тот, кого видно. За вечер светятся все по очереди.",
    "На последнем тосте все наклоняют карточки в одну точку над столом. Уходя, гость забирает зеркало с именем.",
]
spec = "Домик 110×50 мм · лимонный картон 350 г/м² · окно Ø45 мм · зеркальный картон (металлизированный, ламинат) 56×56 мм, клей изнутри · 1 цвет"

def build():
    return sheet(6, "Подсвети говорящего", "Light the Speaker — a mirror place card that gives the lamp away",
                 ["карточка с зеркалом: пока один говорит,", "сосед светит ему лампой со стола"],
                 scene(), flat(), storyboard(), caps, spec)

if __name__ == "__main__":
    open("../c6.svg", "w").write(build())
