from lib import *
from c2 import topplate, topglass, toplamp

PROMPTS = ["первое впечатление", "цвет", "подарок", "недосказанное", "пожелание"]

def slip(x, y, w, h, name=None, filled=2, ang=0, glow=False, dashed=False, prompts=False, fs=11, hl=False):
    """slip centred at x,y"""
    x0, y0 = -w/2, -h/2
    g = ""
    if glow: g += R(x0 - 8, y0 - 8, w + 16, h + 16, fill="#fff7c4", stroke="none", rx=6)
    dash = 'stroke-dasharray="6 5"' if dashed else ""
    g += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{LEM if not dashed else "#fff8cf"}" stroke="{INK}" stroke-width="{2 if hl else 1.6}" {dash}/>'
    if name:
        n1, n2 = name
        g += T(0, y0 + fs + 5, n1, fs, 700, "middle") + T(0, y0 + 2*fs + 6, n2, fs*0.9, 700, "middle")
    ty = y0 + 2*fs + 18 if name else y0 + 16
    step = (y0 + h - 8 - ty) / 5
    for i in range(5):
        yy = ty + i * step + step*0.7
        if prompts:
            g += T(x0 + 5, yy - 3, PROMPTS[i], fs*0.72, 500, extra='opacity=".75"')
        g += L(x0 + 5, yy, x0 + w - 5, yy, sw=1.0, stroke="#444")
        if i < filled:
            g += scribble(x0 + 8, yy - 3, w * (0.4 + 0.12 * ((i * 3) % 4)), amp=2, sw=1.3)
    return f'<g transform="translate({x},{y}) rotate({ang})" {dash and ""}>{g}</g>'

def guest_top(x, y=462, name=None):
    s = E(x, y + 40, 66, 28, fill=GHOST, stroke="none") + C(x, y, 24, fill=GHOST, stroke="none")
    return s

def tent_top(x, y, name, w=130, h=26, slot=True):
    s = R(x - w/2, y - h/2, w, h, fill=LEM, stroke=INK, sw=2)
    s += L(x - w/2, y, x + w/2, y, stroke=INK, sw=1, dash="3 3", extra='opacity=".5"')
    s += T(x - 8 if slot else x, y + 5, name, 13, 700, "middle")
    if slot:
        s += R(x + w/2 - 30, y - h/2 + 3, 20, h - 6, fill="#fff", stroke=INK, sw=1.3, extra='stroke-dasharray="3 2"')
    return s

NAMES = [("Tanya", "Andrianova"), ("Igor", "Zotov"), ("Andrey", "Lee"), ("Sasha", "Chernikov"), ("Sophia", "Zhuravkova")]

def scene():
    s = R(0, 0, 1120, 515, fill=WALL, stroke="none")
    xs = [130, 345, 560, 775, 990]
    for x in xs: s += guest_top(x)
    s += R(0, 30, 1120, 395, fill=CLOTH, stroke=INK, sw=2.5)
    for x in (237, 452, 667, 882): s += toplamp(x, 92)
    for x, nm in zip(xs, NAMES):
        s += tent_top(x, 92, nm[0] + " " + nm[1].split()[0][:1] + ".", slot=True) if False else tent_top(x, 92, nm[0], slot=True)
        s += topplate(x, 222, 60) + topglass(x + 88, 205, 18)
    # slips: current positions (after two hands)
    s += slip(130, 350, 64, 106, ("Andrey", "Lee"), 3)
    s += slip(345, 350, 64, 106, ("Sasha", "Chernikov"), 3)
    s += slip(560, 350, 64, 106, ("Sophia", "Zhuravkova"), 2, glow=True, hl=True)
    s += slip(775, 350, 64, 106, None, 1, dashed=False)
    s += slip(990, 350, 64, 106, None, 0, dashed=False)
    # ghosts of Sophia's slip path
    s += arrow(940, 300, 828, 300, sw=3, curve=-20) + arrow(725, 300, 614, 300, sw=3, curve=-20)
    s += T(884, 275, "перемена 1", 14, 600, "middle") + T(670, 275, "перемена 2", 14, 600, "middle")
    s += pencil(580, 382, -30, 80)
    # callouts
    s += TL(560, 440, ["её полоска у Андрея: он только что записал цвет"], 16, 20, 600, "middle") if False else ""
    s += TL(565, 484, ["полоска Софии после двух передач: она уже у Андрея"], 17, 22, 600, "middle")
    s += T(565, 150, "гнёзда в домиках пусты — полоски ушли гулять", 16, 600, "middle")
    s += T(130, 52, "гнёзда пусты —", 15, 600, "middle") + T(130, 70, "полоски ушли гулять", 15, 600, "middle") if False else ""
    s += TL(237, 160, ["гнёзда в", "домиках пусты"], 15, 18, 600, "middle") if False else ""
    s += T(1060, 46, "→ влево", 15, 700, "end", extra='opacity="0"')
    return s

def flat():
    sc = 2.55; tw, th = 120*sc, 50*sc
    ox, oy = 18, 60
    s = R(ox, oy, tw, 2*th, fill=LEM, stroke=INK, sw=2.5)
    ry = oy + th
    s += L(ox - 8, ry, ox + tw + 8, ry, dash="10 6", sw=2) + T(ox + 5, ry - 7, "ребро / биговка", 11, 600)
    s += T(ox + tw/2, oy + 30, "Dinner · 10.10.2026", 12, 500, "middle", extra='opacity=".7"')
    s += T(ox + tw/2, oy + 70, "Sophia Zhuravkova", 22, 700, "middle")
    s += R(ox + tw/2 - 36, oy + 96, 72, 8, fill="#fff", stroke=INK, sw=1.4, extra='stroke-dasharray="4 3"')
    s += T(ox + tw/2, oy + 120, "прорезь 54 мм", 11, 600, "middle", extra='opacity=".75"')
    low = T(ox + tw/2, ry + 30, "Sophia Zhuravkova", 15, 600, "middle")
    low += TL(ox + tw/2, ry + 58, ["После каждой перемены передай", "полоску соседу слева. Допиши на", "ней одно слово по подсказке."], 11.5, 16, 500, "middle")
    low += TL(ox + tw/2, ry + 112, ["В конце найди хозяина — и вручи."], 11.5, 16, 600, "middle")
    s += rot(low, 180, ox + tw/2, ry + th/2)
    s += TL(ox, oy + 2*th + 24, ["домик 120×50 мм (сложен),", "картон 350 г/м², биговка по ребру"], 12.5, 17, 600)
    sc2 = 3.0; sw_, sh = 50*sc2, 120*sc2
    sx = 380
    s += R(sx, 60, sw_, sh, fill=LEM, stroke=INK, sw=2.5)
    s += T(sx + sw_/2, 92, "Sophia", 21, 700, "middle") + T(sx + sw_/2, 117, "Zhuravkova", 18, 700, "middle")
    for i, p in enumerate(PROMPTS):
        yy = 152 + i * 47
        s += T(sx + 8, yy, p, 12, 600)
        s += L(sx + 8, yy + 24, sx + sw_ - 8, yy + 24, sw=1.2)
    s += L(sx + 20, 60 + sh, sx + 20, 60 + sh + 24, sw=0)
    s += TL(sx - 40, 60 + sh + 22, ["полоска 50×120 мм, 350 г/м²;", "нижний язычок входит в прорезь"], 12, 16, 600)
    return s

def storyboard():
    BG = R(0, 30, 410, 380, fill=CLOTH, stroke="none")
    def small_tent(x, yb, w=190, h=70, empty=False):
        s = tent(x, yb, w, h, depth=8)
        s += T(x, yb - h + 28, "Sophia", 22, 700, "middle") + T(x, yb - 14, "Zhuravkova", 22, 700, "middle")
        return s
    # 1 arrival: tent with slip standing in slot
    P1 = BG + plate(205, 345, 100)
    P1 += slip(205, 215, 70, 130, ("Sophia", "Zhuravkova"), 0, prompts=False, fs=12)
    P1 += small_tent(205, 310, 200, 66)
    # 2: slip lies in front of neighbour, pencil
    P2 = BG + plate(205, 320, 96)
    P2 += slip(205, 255, 150, 76, None, 0, ang=0, fs=11) if False else ""
    P2 += R(95, 120, 220, 170, fill="none", stroke="none")
    P2 += slip(205, 215, 100, 190, ("Sophia", "Zhuravkova"), 1, prompts=True, fs=15, hl=True)
    P2 += pencil(240, 222, -35, 120)
    # 3: hops along the row
    P3 = BG
    for i in range(5):
        xx = 48 + i * 78
        P3 += plate(xx, 300, 30, shadow=False) if False else E(xx, 300, 31, 31, fill="#fff", stroke=INK, sw=1.6)
    P3 += R(0, 365, 410, 30, fill="none", stroke="none")
    for i, (xx, filled) in enumerate([(48 + 4*78, 0), (48 + 3*78, 1), (48 + 2*78, 2), (48 + 1*78, 3), (48, 4)]):
        P3 += slip(xx, 215 if False else 230, 44, 88, ("S.", "") if False else None, filled, fs=8, dashed=(filled < 3 and False), hl=(i == 2)) 
    P3 += arrow(330, 160, 112, 160, sw=2.5, curve=-24) if False else ""
    P3 += T(205, 140, "◀  против часовой: влево  ◀", 14, 700, "middle") if False else ""
    for i in range(4):
        P3 += arrow(48 + (4 - i) * 78 - 12, 150, 48 + (3 - i) * 78 + 12, 150, sw=2, curve=-14, head=7)
    P3 += TL(205, 345, ["одна и та же полоска: слово за словом", "пять соседей — пять строк"], 15, 19, 600, "middle")
    # 4: delivery
    P4 = BG + silhouette(95, base=250, head_y=130, s=0.9) + silhouette(315, base=250, head_y=130, s=0.9)
    P4 += R(0, 255, 410, 160, fill=CLOTH, stroke=INK, sw=2)
    P4 += slip(205, 190, 80, 150, ("Sophia", "Zhuravkova"), 5, fs=12, hl=True, glow=True)
    P4 += arrow(160, 110, 125, 150, sw=0.1, stroke="none")
    P4 += arrow(180, 300, 255, 300, sw=3, curve=-14)
    P4 += T(205, 342, "вручить хозяйке", 17, 700, "middle")
    return [("Приход", ["имя на домике, полоска", "стоит в гнезде"], P1),
            ("После первого блюда", ["полоска уходит влево; сосед", "пишет первое впечатление"], P2),
            ("Середина вечера", ["по кругу — каждый дописывает", "по одному слову"], P3),
            ("Уход", ["полоска возвращается", "к хозяйке — портрет стола"], P4)]

caps = [
    "Домик с именем остаётся на месте. Полоска с её же именем стоит в нём — до первой перемены.",
    "С каждой переменой полоски едут по кругу: сосед пишет по одному слову под печатную подсказку.",
    "К десерту у полоски пять строк чужого почерка. Чужие слова про тебя — самое личное за вечер.",
    "Перед уходом каждый находит хозяина полоски и вручает её. Гость забирает не имя — а портрет.",
]
spec = "Домик 120×50 мм · полоска 50×120 мм · лимонный картон 350 г/м² · 1 цвет · одна прорезь · на место короткий чёрный карандаш"

def build():
    return sheet(4, "Круговая порука", "The Travelling Portrait — the card stays, her name goes round the table",
                 ["домик держит место; полоска с именем", "ходит по кругу и собирает слова стола"],
                 scene(), flat(), storyboard(), caps, spec)

if __name__ == "__main__":
    open("../c4.svg", "w").write(build())
