from lib import *

FR = [("Tanya", "Andrianova", ["Пусть этот стол"]),
      ("Igor", "Zotov", ["будет длиннее,", "чем мы рассчитывали,"]),
      ("Andrey", "Lee", ["а свет над ним —", "ниже, чем нужно,"]),
      ("Sasha", "Chernikov", ["чтобы нам пришлось", "придвинуться."]),
      ("Sophia", "Zhuravkova", ["За тех, кто", "сидит рядом."])]
FULL = ["Пусть этот стол будет длиннее, чем мы", "рассчитывали, а свет над ним — ниже, чем", "нужно, чтобы нам пришлось придвинуться.", "За тех, кто сидит рядом."]

def name_tent(x, yb, n1, n2, w=170, h=84, fs=22):
    s = tent(x, yb, w, h, depth=9)
    s += T(x, yb - h + 18, "Dinner · 10.10.26", 10.5, 500, "middle", extra='opacity=".7"')
    s += T(x, yb - 40, n1, fs, 700, "middle") + T(x, yb - 14, n2, fs, 700, "middle")
    return s

def scene():
    xs = [112, 336, 560, 784, 1008]
    s = scene_base(xs, head_y=132, base=232)
    s += lamp(448, 292, 92, 38, 116) + lamp(896, 292, 92, 38, 116)
    # toast band
    s += R(0, 14, 1120, 70, fill=LEM, stroke=INK, sw=2)
    for i, (n1, n2, fr) in enumerate(FR):
        x = xs[i]
        if i: s += L(x - 112, 14, x - 112, 84, sw=1.6, dash="2 5")
        s += TL(x, 44 if len(fr) == 2 else 55, fr, 17, 22, 700, "middle")
        s += L(x, 88, x, 200, sw=1.3, dash="3 5", extra='opacity=".6"')
    s += arrow(212, 49, 232, 49, sw=0.1, stroke="none")
    for i, (n1, n2, fr) in enumerate(FR):
        x = xs[i]
        s += name_tent(x, 300, n1, n2, 170, 84, 21)
        s += plate(x, 362, 78) + napkin(x - 30, 350, 56, 24) + glass(x + 112, 354, 100)
    s += TL(560, 450, ["каждая карточка — одна строка тоста (напечатана с обратной стороны, со стороны гостя);", "все пять вместе — одна фраза, которую никто не знает целиком"], 17, 22, 600, "middle")
    s += T(560, 500, "порядок рассадки = порядок фразы", 20, 700, "middle")
    return s

def flat():
    sc = 2.6; tw, th = 110*sc, 60*sc
    ox, oy = 14, 54
    s = R(ox, oy, tw, th, fill=LEM, stroke=INK, sw=2.5)
    s += T(ox + tw/2, oy + 28, "Dinner · 10.10.2026", 12, 500, "middle", extra='opacity=".7"')
    s += T(ox + tw/2, oy + 78, "Sophia", 34, 700, "middle") + T(ox + tw/2, oy + 118, "Zhuravkova", 34, 700, "middle")
    s += T(ox + tw + 8, oy + 18, "лицо", 12, 700) + T(ox + tw + 8, oy + 34, "(к столу)", 11, 500)
    s += L(ox - 8, oy + th, ox + tw + 8, oy + th, dash="10 6", sw=2)
    s += T(ox + tw + 14, oy + th + 4, "ребро", 12, 600)
    oy2 = oy + th
    s += R(ox, oy2, tw, th, fill=LEM, stroke=INK, sw=2.5)
    low = T(ox + tw/2, oy2 + 24, "Sophia Zhuravkova", 12, 600, "middle", extra='opacity=".75"')
    low += TL(ox + tw/2, oy2 + 78, ["За тех, кто", "сидит рядом."], 30, 38, 700, "middle")
    s += rot(low, 180, ox + tw/2, oy2 + th/2)
    s += T(ox + tw + 8, oy2 + 18, "изнанка", 12, 700) + T(ox + tw + 8, oy2 + 34, "(к гостю,", 11, 500) + T(ox + tw + 8, oy2 + 48, "вверх ногами)", 11, 500)
    s += T(ox, oy + 2*th + 22, "110 × 120 мм, домик 110×60", 13, 600)
    s += L(ox, oy + 2*th + 40, ox + tw, oy + 2*th + 40, sw=0)
    s += TL(ox, oy + 2*th + 58, ["Полный тост, который за столом никто", "не видел целиком:"], 12.5, 17, 500) if False else ""
    s += TL(ox, oy + 2*th + 50, ["Тост целиком (читается", "только по порядку мест):"], 12.5, 16, 600) if False else ""
    s += TL(ox, 466, FULL, 14, 18, 600) if False else ""
    s += TL(ox, 454, ["«Пусть этот стол будет длиннее, чем мы рассчитывали,", "а свет над ним — ниже, чем нужно, чтобы нам пришлось", "придвинуться. За тех, кто сидит рядом.»"], 13.5, 18, 600)
    s += T(ox, 440, "ТОСТ ЦЕЛИКОМ (на 5 мест; на большее число — припев)", 11, 700, extra='opacity=".7"')
    return s

def bubble(x, y, lines, w=130, fs=14, tail=(0, 30), emph=False):
    h = len(lines) * fs * 1.3 + 14
    s = R(x - w/2, y - h/2, w, h, fill=LEM if not emph else "#fff", stroke=INK, sw=1.8, rx=12)
    s += P(f"M{x-8},{y+h/2-1} L{x+tail[0]},{y+h/2+tail[1]} L{x+10},{y+h/2-1}", fill=LEM if not emph else "#fff", stroke=INK, sw=1.8)
    s += TL(x, y - h/2 + fs + 5, lines, fs, fs*1.3, 700, "middle")
    return s

def storyboard():
    BG = R(0, 30, 410, 380, fill=CLOTH, stroke="none")
    # 1: from guest side
    P1 = BG + plate(205, 335, 100)
    P1 += R(95, 120, 220, 150, fill=LEM, stroke=INK, sw=2.2)
    P1 += P("M95,120 L103,108 L323,108 L315,120 Z", fill=LEMD, stroke=INK, sw=1.6)
    P1 += T(205, 148, "Sophia Zhuravkova", 13, 600, "middle", extra='opacity=".75"')
    P1 += TL(205, 200, ["За тех, кто", "сидит рядом."], 28, 34, 700, "middle")
    P1 += T(205, 300, "(вид со стороны стула)", 13, 500, "middle", extra='opacity=".0"')
    # 2: dessert, first line
    P2 = BG
    for x in (70, 205, 340): P2 += silhouette(x, base=262, head_y=176, s=0.7)
    P2 += R(0, 262, 410, 160, fill=CLOTH, stroke=INK, sw=2)
    P2 += bubble(120, 112, ["Пусть этот", "стол…"], 124, 17, tail=(-30, 22))
    P2 += glass(52, 250, 70, wine=True, rim=14)
    P2 += T(300, 140, "…", 34, 700, "middle", extra='opacity=".6"') + T(250, 124, "?", 1, 500) 
    for x in (70, 205, 340):
        P2 += plate(x, 335, 50) + glass(x + 50, 326, 62, rim=14)
    P2 += T(205, 392, "один встал и постучал по бокалу", 15, 600, "middle")
    # 3: chain
    P3 = BG
    ys = [86, 134, 182, 230, 288]
    for i, (n1, n2, fr) in enumerate(FR):
        yy = 104 + i * 52
        P3 += R(14, yy - 21, 382, 42, fill=LEM if i < 4 else "#fff", stroke=INK, sw=1.6, rx=8)
        P3 += T(26, yy + 5, n1, 13, 600, extra='opacity=".6"')
        P3 += T(110, yy + 6, " ".join(fr), 15 if len(" ".join(fr)) < 34 else 13, 700)
        if i < 4: P3 += arrow(205, yy + 21, 205, yy + 31, sw=2, head=6)
    P3 += T(205, 366, "каждый — своя строка, по очереди", 15, 600, "middle")
    # 4: shuffle
    P4 = BG
    pos = [(70, 150, -8), (190, 120, 6), (320, 160, -4), (110, 270, 5), (270, 275, -9)]
    for (x, y, a), (n1, n2, fr) in zip(pos, FR):
        P4 += f'<g transform="rotate({a} {x} {y})">' + R(x - 52, y - 32, 104, 64, fill=LEM, stroke=INK, sw=1.8) + T(x, y - 4, n1, 16, 700, "middle") + T(x, y + 18, n2, 12, 600, "middle") + '</g>'
    P4 += arrow(200, 205, 235, 235, sw=2.5, curve=14) + arrow(235, 205, 200, 235, sw=2.5, curve=-14)
    P4 += T(205, 362, "смелый хозяин: карточки не по порядку", 15, 600, "middle")
    return [("Приход", ["она читает только свою строку:", "тост начинается не с неё"], P1),
            ("Десерт", ["кто-то встаёт и начинает —", "дальше каждый знает свою часть"], P2),
            ("Тост", ["строка за строкой — и стол", "говорит одной фразой"], P3),
            ("Вариант", ["карточки не по порядку: гости", "рассаживаются «по смыслу»"], P4)]

caps = [
    "Имя смотрит на стол, а с её стороны напечатана одна строка. Что за тост — никто не знает.",
    "К десерту кто-то встаёт и произносит первую строку. Все смотрят в свои карточки.",
    "Каждый читает свою строку по очереди — получается одна фраза на всех. Последняя достаётся ей: «За тех, кто сидит рядом».",
    "Опция: карточки раздаются вперемешку. Гости читают строки и рассаживаются по смыслу — это и есть рассадка.",
]
spec = "Домик 110×60 мм · лимонный картон 300 г/м² · 1 цвет · на большее число гостей — тост с припевом: каждая пятая карточка «Все: за нас!»"

def build():
    return sheet(5, "Один тост на всех", "One Toast — the table speaks a single sentence, one guest at a time",
                 ["имя смотрит на стол, строка тоста — на гостя;", "порядок мест и есть порядок фразы"],
                 scene(), flat(), storyboard(), caps, spec)

if __name__ == "__main__":
    open("../c5.svg", "w").write(build())
