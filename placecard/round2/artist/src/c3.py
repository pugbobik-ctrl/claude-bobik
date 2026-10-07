from lib import *

SHEETS = [
    ["Расскажи соседу слева,", "где был год назад."],
    ["Передай соль.", "Никто не просил."],
    ["Услышишь тишину —", "присоединись к ней."],
    ["Пересядь на 10 минут.", "Бокал возьми с собой."],
    ["Попрощайся, будто ужин", "только начинается."],
]
FINAL = ["Дальше —", "без инструкций."]

def pad_card(x, yb, stage, n1="Sophia", n2="Zhuravkova", w=214, hn=58, hp=104, ns=26, fs=13.5):
    """stage 0..4 = which sheet is on top; 5 = finished"""
    h = hn + hp
    x0 = x - w/2
    s = E(x + 5, yb + 3, w/2 + 6, 8, fill="#00000020", stroke="none")
    s += P(f"M{x0},{yb} L{x0},{yb-h} L{x0+w},{yb-h} L{x0+w},{yb} Z", fill=LEM, stroke=INK, sw=2)
    s += P(f"M{x0},{yb-h} L{x0+8},{yb-h-10} L{x0+w+8},{yb-h-10} L{x0+w},{yb-h} Z", fill=LEMD, stroke=INK, sw=1.6)
    s += T(x, yb - h + 16, "Dinner · 10.10.26", 11, 500, "middle", extra='opacity=".7"')
    s += T(x, yb - h + 42, f"{n1} {n2}", ns*0.62 if False else 19, 700, "middle")
    py = yb - hp
    s += L(x0, py, x0 + w, py, sw=1.5)
    if stage < 5:
        # pad stack
        left = 5 - stage
        for k in range(min(left - 1, 3), 0, -1):
            s += R(x0 + 3 + k*1.8, py + 3 + k*1.8, w - 6, hp - 8, fill="#f7e98a", stroke=INK, sw=1)
        s += R(x0 + 3, py + 3, w - 6, hp - 8, fill="#fff1a8", stroke=INK, sw=1.4)
        s += L(x0 + 3, py + 8, x0 + w - 3, py + 8, sw=1.4, dash="2 3")
        s += T(x0 + 12, py + 34, str(stage + 1), 20, 700)
        s += TL(x0 + 36, py + 36, SHEETS[stage], fs, 20, 600)
    else:
        s += TL(x, py + 46, FINAL, 17, 21, 700, "middle")
    return s

def loose_sheet(x, y, ang=0, w=60, h=30, txt=None):
    s = f'<g transform="rotate({ang} {x} {y})">' + R(x - w/2, y - h/2, w, h, fill="#fff1a8", stroke=INK, sw=1.3)
    if txt: s += scribble(x - w/2 + 6, y + 2, w - 12, amp=2, sw=1.2)
    s += '</g>'
    return s

def scene():
    xs = (180, 565, 950)
    s = scene_base(xs)
    s += lamp(372, 292, 92, 38, 120) + lamp(757, 292, 92, 38, 120)
    s += pad_card(180, 300, 3) + pad_card(565, 300, 0) + pad_card(950, 300, 5, "Andrey", "Lee")
    for x in xs:
        s += plate(x, 362, 100) + napkin(x - 40, 348, 66, 28) + glass(x + 140, 352, 112)
    # torn sheets on cloth
    for (x, y, a) in [(95, 408, -12), (150, 428, 8), (236, 418, -6), (300, 436, 15), (880, 410, 10), (940, 432, -9), (1030, 416, 20), (720, 440, -4), (470, 430, 6)]:
        s += loose_sheet(x, y, a)
    s += TL(565, 38, ["один листок — одна инструкция;", "следующий не виден"], 19, 24, 600, "middle")
    s += arrow(565, 84, 565, 118, sw=1.8, curve=0, head=9)
    s += TL(950, 38, ["листки кончились:", "«Дальше — без инструкций»"], 19, 24, 600, "middle")
    s += arrow(950, 84, 950, 118, sw=1.8, head=9)
    s += TL(180, 38, ["четвёртая перемена:", "«пересядь»"], 19, 24, 600, "middle")
    s += arrow(180, 84, 180, 118, sw=1.8, head=9)
    s += TL(560, 480, ["оторванные листки остаются на скатерти —", "лимонное конфетти исполненных поступков"], 19, 24, 600, "middle")
    s += arrow(420, 462, 300, 440, sw=1.8, head=9) + arrow(700, 462, 880, 430, sw=1.8, head=9)
    s += T(180, 140, "перемена 4", 15, 600, "middle", extra='opacity=".0"')
    return s

def flat():
    sc = 2.4; w, h = 100*sc, 86*sc
    ox, oy = 28, 54
    s = R(ox, oy, w, 2*h, fill=LEM, stroke=INK, sw=2.5)
    ry = oy + h
    s += L(ox - 10, ry, ox + w + 10, ry, dash="10 6", sw=2) + T(ox + 6, ry - 6, "ребро / биговка", 11, 600)
    # front (top): name + pad area
    s += T(ox + w/2, oy + 24, "Dinner · 10.10.2026", 12, 500, "middle", extra='opacity=".7"')
    s += T(ox + w/2, oy + 62, "Sophia Zhuravkova", 21, 700, "middle")
    py = oy + 80
    s += L(ox, py, ox + w, py, sw=1.5)
    s += TL(ox + w/2, py + 38, ["Дальше —", "без инструкций."], 19, 23, 700, "middle")
    s += R(ox + 8, py + 10, w - 16, h - 90, fill="none", stroke=INK, sw=1.3, extra='stroke-dasharray="6 4"')
    s += T(0,0,"",1)
    s += TL(ox + w/2, py + 100, ["сюда клеится блок", "из 5 листков"], 13, 16, 500, "middle") if False else ""
    # back (bottom, rotated)
    low = T(ox + w/2, ry + 30, "Sophia Zhuravkova", 15, 600, "middle")
    low += TL(ox + w/2, ry + 66, ["Меняют тарелки — рви листок.", "Исполнил — оставь на столе."], 13.5, 18, 500, "middle")
    low += TL(ox + w/2, ry + 126, ["Dinner · Colorblock × DNA Kitchen", "Москва, 10 октября 2026"], 12, 16, 500, "middle")
    s += rot(low, 180, ox + w/2, oy + h + h/2)
    s += T(ox, oy + 2*h + 22, "100 × 172 мм, биговка по ребру", 13, 600)
    # sheets column
    sx = 300; sc2 = 1.7; sw_, sh = 92*sc2, 44*sc2
    for i, ln in enumerate(SHEETS):
        yy = 62 + i * (sh + 6)
        s += R(sx, yy, sw_, sh, fill="#fff1a8", stroke=INK, sw=1.5)
        s += T(sx + 8, yy + 24, str(i + 1), 17, 700)
        s += TL(sx + 26, yy + 33, ln, 11.5, 16, 600) if False else TL(sx + 26, yy + 30, ln, 11, 15, 600)
    s += TL(sx, 62 + 5*(sh + 6) + 16, ["листки 92×44 мм · 100 г/м²,", "клей по верхнему краю"], 12.5, 16, 500)
    return s

def storyboard():
    BG = R(0, 30, 410, 380, fill=CLOTH, stroke="none")
    def card(x, yb, st, **k):
        return pad_card(x, yb, st, w=220, hn=58, hp=108, fs=14, **k)
    P1 = BG + lamp(365, 300, 80, 30, 90) + plate(205, 345, 100) + card(205, 310, 0)
    P2 = BG + plate(205, 345, 100) + card(205, 310, 1)
    P2 += loose_sheet(352, 262, 28, 84, 40) + T(352, 270, "1", 20, 700, "middle", extra='transform="rotate(28 352 262)"')
    P2 += arrow(318, 205, 346, 238, sw=2, curve=-16, head=8)
    P3 = BG
    for x in (70, 205, 340):
        P3 += silhouette(x, base=215, head_y=120, s=0.62, fill=GHOST)
        P3 += E(x + 40, 92, 22, 13, fill="#fff", stroke=INK, sw=1.6) + T(x + 40, 99, "…", 19, 700, "middle")
    P3 += R(0, 215, 410, 200, fill=CLOTH, stroke=INK, sw=2)
    for x in (70, 205, 340):
        P3 += plate(x, 340, 52) + tent(x, 295, 100, 66, depth=7)
        P3 += R(x - 44, 262, 88, 26, fill="#fff1a8", stroke=INK, sw=1.2)
        P3 += T(x, 280, "3", 15, 700, "middle")
    P3 += T(205, 376, "стол молчит минуту, сам собой", 15, 600, "middle")
    P4 = BG + plate(205, 345, 100) + card(205, 310, 5, n1="Sophia", n2="Zhuravkova")
    for (x, y, a) in [(60, 330, -12), (95, 372, 8), (340, 330, -6), (365, 366, 15), (310, 380, 9)]:
        P4 += loose_sheet(x, y, a)
    return [("Приход", ["имя и первый листок;", "про второй ты ещё не знаешь"], P1),
            ("Меняют тарелки", ["листок оторван, исполнен;", "под ним — следующий"], P2),
            ("Третья перемена", ["«Услышишь тишину —", "присоединись к ней»"], P3),
            ("Уход", ["последний листок исполнен;", "дальше — без инструкций"], P4)]

caps = [
    "Гостья видит имя и одну инструкцию, как на отрывном календаре. Дальше — только по очереди.",
    "Когда меняют тарелки, она рвёт листок и делает то, что в нём. Листок остаётся на скатерти.",
    "На третьей перемене кто-то первым рвёт «тишину». Остальные присоединяются, и стол замолкает сам.",
    "Под последним листком — печатная фраза. К полуночи на скатерти лимонные листки: след исполненного.",
]
spec = "Карточка-домик 100×86 (сложена) · 350 г/м² лимонный · блок из 5 листков 92×44, 100 г/м², склейка по верху · 1 цвет · под блоком напечатано «Дальше — без инструкций»"

def build():
    return sheet(3, "Партитура на пять перемен", "Score for Five Courses — a tear-off pad of instructions, Fluxus-style",
                 ["каждая смена тарелок — один листок,", "один маленький поступок за ужином"],
                 scene(), flat(), storyboard(), caps, spec)

if __name__ == "__main__":
    open("../c3.svg", "w").write(build())
