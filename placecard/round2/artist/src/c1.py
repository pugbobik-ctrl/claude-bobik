from lib import *

NAME1, NAME2 = "Sophia", "Zhuravkova"

def tab(x, yb, w=46, h=60, written=True, tilt=0):
    s = f'<g transform="rotate({tilt} {x} {yb})">'
    s += tent(x, yb, w, h, depth=6)
    s += T(x, yb - h + 14, "нет:", 11, 600, "middle")
    if written:
        s += scribble(x - w/2 + 6, yb - h + 34, w - 12, amp=3, sw=1.6)
    s += '</g>'
    return s

def main_card(x, yb, torn=False, name=(NAME1, NAME2), size=30):
    """x=centre of whole object; torn = tab already gone"""
    h = 104; nw = 172; tw = 62
    s = ""
    if not torn:
        tot = nw + tw; x0 = x - tot/2
        s += tent(x - tot/2 + tw/2 + 0, yb, tw, h, depth=10)  # tab
        s += T(x0 + tw/2, yb - h + 34, "Кого здесь", 11, 600, "middle")
        s += T(x0 + tw/2, yb - h + 50, "нет?", 11, 600, "middle")
        s += L(x0 + 10, yb - 26, x0 + tw - 10, yb - 26, sw=1.5)
        s += tent(x0 + tw + nw/2, yb, nw, h, depth=10)
        s += L(x0 + tw, yb - h + 2, x0 + tw, yb - 2, sw=2.2, dash="2 5")
        cx = x0 + tw + nw/2
    else:
        s += tent(x, yb, nw, h, depth=10); cx = x
    s += T(cx, yb - h + 22, "Dinner · 10.10.26", 12, 500, "middle", extra='opacity=".75"')
    s += T(cx, yb - 50, name[0], size, 700, "middle")
    s += T(cx, yb - 16, name[1], size, 700, "middle")
    return s

def scene():
    xs = (180, 565, 950)
    s = scene_base(xs)
    s += lamp(372, 292, 92, 38, 120) + lamp(757, 292, 92, 38, 120)
    s += main_card(180, 300, torn=True, name=("Igor", "Zotov"), size=26)
    s += main_card(565, 300, torn=False, size=28)
    s += main_card(950, 300, torn=True, name=("Andrey", "Lee"), size=26)
    for x in xs:
        s += plate(x, 362, 100)
        s += napkin(x - 40, 348, 66, 28)
        s += glass(x + 140, 352, 112)
    s += tab(350, 330, tilt=-4) + tab(380, 334, tilt=3) + tab(408, 326, tilt=8)
    s += tab(740, 332, tilt=-2) + tab(774, 328, tilt=5)
    s += pencil(520, 408, -12, 100)
    s += callout(478, 238, 70, 48, ["отрывной язычок:", "«Кого здесь нет?»"], 20, frm=(170, 98), curve=-30)
    s += callout(640, 232, 700, 48, ["имя гостя — остаётся", "на своём месте"], 20, frm=(780, 100), curve=-25)
    s += callout(762, 330, 830, 470, ["…и лампа становится ещё", "одним местом за столом"], 19, frm=(880, 450), curve=-14)
    s += callout(380, 345, 110, 470, ["имена отсутствующих", "стоят у ламп"], 19, frm=(250, 452), curve=10)
    return s

def flat():
    sc = 3.4; mmw, mmh = 140, 90
    ox, oy = (570 - mmw*sc)/2, 62
    w, h = mmw*sc, mmh*sc
    s = R(ox, oy, w, h, fill=LEM, stroke=INK, sw=2.5)
    s += L(ox - 12, oy + h/2, ox + w + 12, oy + h/2, dash="10 6", sw=2)
    px = ox + 40*sc
    s += T(px + 10, oy + h/2 - 7, "биговка", 12, 600)
    s += L(px, oy - 14, px, oy + h + 14, dash="2 5", sw=3)
    s += T(px, oy - 20, "перфорация", 13, 600, "middle")
    nx = px + (w - 40*sc)/2
    s += T(nx, oy + 34, "Dinner · 10.10.2026", 13, 500, "middle", extra='opacity=".75"')
    s += T(nx, oy + 78, "Sophia", 38, 700, "middle")
    s += T(nx, oy + 118, "Zhuravkova", 38, 700, "middle")
    tx = ox + 20*sc
    s += T(tx, oy + 56, "Кого здесь", 16, 600, "middle") + T(tx, oy + 76, "нет?", 16, 600, "middle")
    s += L(ox + 12, oy + 128, px - 12, oy + 128, sw=1.6)
    low = T(nx, oy + h/2 + 36, "Sophia Zhuravkova", 16, 600, "middle")
    low += TL(nx, oy + h/2 + 66, ["Напиши на язычке имя того,", "кого за этим столом не хватает.", "Оторви. Поставь у лампы."], 14.5, 20, 500, "middle")
    low += TL(tx, oy + h/2 + 52, ["Мы о тебе", "думали."], 14.5, 20, 600, "middle")
    s += rot(low, 180, ox + w/2, oy + h*0.75)
    s += L(ox, oy + h + 34, ox + w, oy + h + 34, sw=1.4) + T(ox + w/2, oy + h + 54, "140 мм", 14, 600, "middle")
    s += L(ox + w + 14, oy, ox + w + 14, oy + h, sw=1.4) + T(ox + w + 20, oy + h/2 + 5, "90", 14, 600)
    s += TL(ox, oy + h + 96, ["Лимонный картон 300 г/м², один цвет (чёрный),", "высечка, биговка + перфорация (мост 3 мм).", "Нижняя половина — изнанка, печатается вверх ногами."], 15.5, 21, 500)
    return s

def storyboard():
    def small_card(x, yb, torn=False, size=22, h=88):
        nw = 150; tw = 64
        s = ""
        if not torn:
            tot = nw + tw; x0 = x - tot/2
            s += tent(x0 + tw/2, yb, tw, h, depth=8)
            s += T(x0 + tw/2, yb - h + 28, "Кого", 11, 600, "middle") + T(x0 + tw/2, yb - h + 42, "здесь нет?", 11, 600, "middle")
            s += L(x0 + 8, yb - 20, x0 + tw - 8, yb - 20, sw=1.4)
            s += tent(x0 + tw + nw/2, yb, nw, h, depth=8)
            s += L(x0 + tw, yb - h + 2, x0 + tw, yb - 2, sw=2.2, dash="2 5")
            cx = x0 + tw + nw/2
        else:
            s += tent(x, yb, nw, h, depth=8); cx = x
        s += T(cx, yb - 54, "Dinner · 10.10.26", 11, 500, "middle", extra='opacity=".7"')
        s += T(cx, yb - 36, "Sophia", size, 700, "middle") + T(cx, yb - 10, "Zhuravkova", size, 700, "middle")
        return s
    P1 = mini(215) + lamp(335, 290, 80, 30, 100) + plate(205, 340, 100) + small_card(205, 292)
    P2 = mini(215) + plate(205, 345, 105) + tent(205, 335, 210, 150, depth=10)
    P2 += T(205, 215, "Здесь не хватает:", 19, 600, "middle")
    P2 += scribble(120, 262, 170, amp=5, sw=2.4) + scribble(120, 300, 110, amp=5, sw=2.4)
    P2 += pencil(262, 312, -25, 120)
    P3 = mini(235) + lamp(205, 305, 100, 44, 150)
    for dx, dy, tl in [(-84, 8, -6), (-30, 24, 2), (28, 26, -3), (84, 8, 6)]:
        P3 += tab(205 + dx, 346 + dy, 56, 76, True, tl)
    P4 = mini(330)
    Q = R(70, 20, 140, 270, fill=INK, stroke=INK, rx=18)
    Q += R(79, 40, 122, 230, fill=LEM, stroke="none", rx=6)
    Q += lamp(140, 215, 62, 28, 80, glow=False)
    Q += tab(112, 245, 30, 42, True) + tab(164, 247, 30, 42, True)
    Q += T(140, 70, "Мы о тебе", 13, 600, "middle") + T(140, 87, "думали", 13, 600, "middle")
    Q += arrow(225, 150, 300, 110, sw=3, curve=-24)
    Q += P("M300,90 L350,76 L332,122 L320,106 Z", fill=LEM, stroke=INK, sw=2.2)
    Q += T(300, 185, "ему / ей", 24, 700, "middle") + TL(300, 215, ["тому, чьё имя", "на язычке"], 16, 20, 500, "middle")
    P4 += G(Q, 0, 62)
    return [("Приход", "одно имя — и один вопрос", P1), ("Перемена 1–2", "одно имя — не про тех, кто за столом", P2), ("Середина вечера", "язычок — к лампе; имена копятся", P3), ("Уход", "снимок лампы уходит адресату", P4)]

caps = [
    "Гостья находит своё имя — и рядом язычок с вопросом. Сидеть можно и так, но…",
    "Между блюдами она пишет имя того, кого нет за столом: друга в другом городе, ушедшего, никого.",
    "Язычки ставят у ламп. К десерту у каждой лампы своя тихая компания отсутствующих.",
    "На выходе — фото своей лампы, отправленное тому, кого ждали: «Мы за этим столом о тебе думали».",
]
spec = "Размер 140×90 мм, в сложенном виде 140×45 · лимонный картон 300 г/м² · 1 цвет · перфорация · по короткому чёрному карандашу на место"

def build():
    pan = storyboard()
    return sheet(1, "Для тех, кого нет", "The Absent Guest — a seat for someone who isn't here",
                 ["лампа — это место за столом,", "которое гости отдают отсутствующему"],
                 scene(), flat(), pan, caps, spec)

if __name__ == "__main__":
    open("../c1.svg", "w").write(build())
