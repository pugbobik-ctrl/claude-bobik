from lib import *

def disc(cx, cy, r, n1, n2, fs=None, ang=0, arc=False, uid="a", opacity=1, stroke_dash=""):
    fs = fs or r * 0.34
    g = f'<circle cx="0" cy="0" r="{r}" fill="{LEM}" stroke="{INK}" stroke-width="1.6" {("stroke-dasharray=%s" % chr(34)+stroke_dash+chr(34)) if stroke_dash else ""}/>'
    g += f'<circle cx="0" cy="0" r="{r*0.9:.1f}" fill="none" stroke="{INK}" stroke-width="0.8" opacity=".5"/>'
    if arc:
        rr = r * 0.78
        g += f'<path id="arc{uid}" d="M{-rr},0 A{rr},{rr} 0 1,1 {rr},0 A{rr},{rr} 0 1,1 {-rr},0" fill="none"/>'
        g += f'<text font-size="{r*0.115:.1f}" font-weight="600" letter-spacing="{r*0.02:.2f}" fill="{INK}"><textPath href="#arc{uid}" startOffset="0">DINNER · 10.10.2026 · COLORBLOCK × DNA KITCHEN · </textPath></text>'
    g += T(0, -fs*0.1, n1, fs, 700, "middle") + T(0, fs*1.05, n2, fs*0.93, 700, "middle")
    return f'<g transform="translate({cx},{cy}) rotate({ang})" opacity="{opacity}">{g}</g>'

def topplate(cx, cy, r=100):
    s = C(cx + 4, cy + 6, r, fill="#00000015", stroke="none")
    s += C(cx, cy, r, fill="#ffffff", stroke=INK, sw=2)
    s += C(cx, cy, r * 0.66, fill="#fbfbf8", stroke="#bdb8a8", sw=1.5)
    return s

def topglass(cx, cy, r=24):
    return C(cx, cy, r, fill="#ffffffaa", stroke=INK, sw=2) + C(cx, cy, r*0.62, fill="#d8d0a0", stroke="none") + C(cx, cy, r*0.62, fill="none", stroke=INK, sw=1)

def toplamp(cx, cy):
    s = f'<circle cx="{cx}" cy="{cy}" r="95" fill="url(#glow)"/>'
    s += C(cx, cy, 36, fill="#3a3a3a", stroke=INK, sw=2) + C(cx, cy, 14, fill=INK, stroke=INK)
    return s

def topnapkin(x, y, w=64, h=46, ang=0):
    return f'<g transform="rotate({ang} {x+w/2} {y+h/2})">' + R(x, y, w, h, fill="#fff", stroke=INK, sw=2) + L(x, y+h*0.5, x+w, y+h*0.5, stroke="#c9c4b4", sw=1.4) + '</g>'

def cutlery(cx, cy, flip=1):
    s = L(cx - 128*flip, cy - 60, cx - 128*flip, cy + 60, sw=2.6, stroke="#9a968a")
    s += L(cx + 128*flip, cy - 60, cx + 128*flip, cy + 60, sw=2.6, stroke="#9a968a")
    return s

def food(cx, cy):
    s = P(f"M{cx-52},{cy+14} C{cx-60},{cy-20} {cx-20},{cy-40} {cx+10},{cy-22} C{cx+50},{cy-30} {cx+64},{cy+8} {cx+30},{cy+24} C{cx},{cy+34} {cx-36},{cy+32} {cx-52},{cy+14} Z", fill="#e9e3cf", stroke=INK, sw=1.6)
    s += C(cx - 12, cy - 6, 6, fill=INK, stroke="none") + C(cx + 16, cy + 6, 4, fill=INK, stroke="none") + C(cx + 30, cy - 8, 3, fill=INK, stroke="none")
    return s

def cup(cx, cy, r=62, letters=True):
    s = C(cx + 4, cy + 6, r * 1.38, fill="#00000015", stroke="none")
    s += C(cx, cy, r * 1.38, fill="#fff", stroke=INK, sw=2)
    s += C(cx, cy, r, fill="#fff", stroke=INK, sw=2.4)
    s += C(cx, cy, r * 0.86, fill="#e6c868", stroke=INK, sw=1.6)
    s += P(f"M{cx+r},{cy} C{cx+r+30},{cy-10} {cx+r+40},{cy+24} {cx+r+4},{cy+18}", stroke=INK, sw=2.4)
    if letters:
        import random
        random.seed(3)
        for i, ch in enumerate("Andrey"):
            a = random.uniform(-70, 70)
            s += T(cx - r*0.72 + i * r*0.3 + random.uniform(-3, 3), cy + random.uniform(-14, 14) + (i % 2) * 8, ch, max(14, r*0.3), 700, "middle", extra=f'transform="rotate({a*0.6:.0f} {cx-r*0.72+i*r*0.3} {cy})" opacity="{0.95 - i*0.1:.2f}"')
    return s

def scene():
    s = R(0, 0, 1120, 515, fill=WALL, stroke="none")
    s += R(0, 40, 1120, 430, fill=CLOTH, stroke=INK, sw=2.5)
    xs = (190, 565, 950)
    for x in (380, 757): s += toplamp(x, 255)
    R_ = 82
    for x, (a, b) in zip(xs[:2], [("Tanya", "Andrianova"), ("Sasha", "Chernikov")]):
        s += topplate(x, 135, R_) + topglass(x - 112, 150) + topnapkin(x + 98, 115, 46, 38, 90)
        s += disc(x, 135, 40, a, b, fs=12, ang=180, uid="b"+a)
    # seat A
    s += topplate(190, 375, R_) + topglass(190 + 112, 360) + topnapkin(190 - 142, 355, 46, 38, 90)
    s += disc(190, 375, 40, "Igor", "Zotov", fs=13, uid="fa")
    # seat B
    s += topplate(565, 375, R_) + food(565, 377) + topglass(565 + 112, 360)
    s += topnapkin(565 - 190, 340, 78, 62, -4)
    s += disc(565 - 150, 372, 40, "Sophia", "Zhuravkova", fs=12.5, uid="fb", ang=-4)
    # seat C
    s += topplate(950, 375, R_) + cup(950, 375, 40)
    s += topglass(950 + 112, 360) + disc(950 - 118, 392, 40, "Sophia", "Zhuravkova", fs=12.5, uid="fc", ang=8)
    s += TL(190, 252, ["имя на тарелке —", "как желток"], 16, 20, 600, "middle")
    s += TL(565, 252, ["диск переехал на салфетку,", "остаётся на столе луной"], 16, 20, 600, "middle")
    s += TL(950, 252, ["обмен дисками; чужое", "имя — в чашку"], 16, 20, 600, "middle")
    s += T(190, 495, "1  приход", 18, 700, "middle") + T(565, 495, "2  между блюдами", 18, 700, "middle") + T(950, 495, "3  к чаю", 18, 700, "middle")
    return s

def flat():
    cx, cy, r = 285, 215, 175
    s = f'<path id="bigarc" d="M{cx-r*0.8},{cy} A{r*0.8},{r*0.8} 0 1,1 {cx+r*0.8},{cy} A{r*0.8},{r*0.8} 0 1,1 {cx-r*0.8},{cy}" fill="none"/>'
    s += C(cx, cy, r, fill=LEM, stroke=INK, sw=2.5)
    s += C(cx, cy, r*0.9, fill="none", stroke=INK, sw=1, extra='opacity=".5"')
    s += f'<text font-size="18" font-weight="600" letter-spacing="2.2" fill="{INK}"><textPath href="#bigarc">DINNER · 10.10.2026 · COLORBLOCK × DNA KITCHEN · </textPath></text>'
    s += T(cx, cy - 8, "Sophia", 46, 700, "middle") + T(cx, cy + 40, "Zhuravkova", 42, 700, "middle")
    s += L(cx - r, cy + r + 24, cx + r, cy + r + 24, sw=1.4) + T(cx, cy + r + 46, "⌀ 130 мм", 15, 600, "middle")
    s += TL(40, 462, ["Вафельная бумага 0,3 мм, лимонная заливка, печать", "пищевым чёрным. Хранить плоско, класть за 20 мин.", "На лист А4 помещается 6 дисков."], 15.5, 21, 500)
    return s

def storyboard():
    BG = R(0, 30, 410, 380, fill=CLOTH, stroke="none")
    P1 = BG + topplate(205, 215, 108) + disc(205, 215, 58, "Sophia", "Zhuravkova", fs=17, uid="p1") + topglass(365, 160) + topnapkin(24, 190, 50, 44, 90)
    P2 = BG + topplate(250, 215, 108) + food(255, 220) + topglass(380, 150, 20) + topnapkin(8, 160, 76, 70, -4)
    P2 += disc(62, 190, 52, "Sophia", "Zhuravkova", fs=15, uid="p2", ang=-4)
    P3 = BG + disc(105, 210, 62, "Sophia", "Zhuravkova", fs=18, uid="p3a", ang=-10) + disc(305, 210, 62, "Andrey", "Lee", fs=19, uid="p3b", ang=8)
    P3 += arrow(150, 140, 262, 140, sw=3, curve=-26) + arrow(262, 285, 150, 285, sw=3, curve=-26)
    P4 = BG + cup(205, 215, 86) + T(205, 352, "жёлтое расплывается, имя всплывает", 15, 500, "middle")
    return [("Приход", ["диск лежит на тарелке,", "как желток"], P1),
            ("Между блюдами", ["переезжает на салфетку —", "и ждёт"], P2),
            ("К чаю", ["«Я съем твоё имя,", "ты — моё»"], P3),
            ("Уход", ["чужое имя растворяется", "в твоей чашке"], P4)]

caps = [
    "На тарелке — жёлтый диск с её именем. Есть ли его? Никто не спрашивает, все косятся.",
    "С первым блюдом официант переносит диск на салфетку. Он остаётся на столе луной.",
    "К чаю гости меняются дисками. Правило: съесть можно только чужое имя.",
    "Горячее размягчает вафлю, чёрные буквы плывут. Уходишь, унося внутри имя соседа.",
]
spec = "Диск ⌀130 мм · вафельная бумага 0,3 мм, лимонная · пищевой чёрный · допустима вариация: печать на сахарном листе · ИЗГОТОВИТЬ ЗА 1–2 ДНЯ, ХРАНИТЬ В КОРОБКЕ С СИЛИКАГЕЛЕМ"

def build():
    pan = storyboard()
    return sheet(2, "Съешь имя", "Eat the Name — a place card you finish by the end of dinner",
                 ["именная карточка — это еда:", "чужое имя ты проглатываешь, своё — отдаёшь"],
                 scene(), flat(), pan, caps, spec)

if __name__ == "__main__":
    open("../c2.svg", "w").write(build())
