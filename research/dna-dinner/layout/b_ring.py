import sys, math; sys.path.insert(0, '.')
from ui import *
F = load('flat'); G = load('gear'); C = load('cutlery')
D = F['letters'][0]          # D fragment: bbox 110,111,237,293; counter 186..278 x 189..327
VW, VH = 720, 350
AX = -38.8                   # vertical object turned onto the poster's 51.2° axis
def d_ring(x, y, s, rot, name, fid='sh'):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s}) translate(-232 -258)">'
            f'<path d="{D["d"]}" fill="{Y}" filter="url(#{fid})"/>'
            f'<rect x="100" y="255.5" width="90" height="5" fill="{BG}"/>'
            f'<text x="229" y="379" text-anchor="middle" font-family="Inter" font-weight="600" font-size="32" fill="{DARK}" letter-spacing="-0.3">{name}</text>'
            f'</g>')
def ring_a():
    r = d_ring(88, 104, 0.55, -9, 'Tanya') + d_ring(250, 112, 0.55, 12, 'Igor') + d_ring(168, 258, 0.55, 3, 'Sasha')
    gx, gy = 560, 26
    glass = (f'<g transform="translate({gx} {gy})" fill="none" stroke="rgba(246,231,200,.8)" stroke-width="2.4">'
             f'<path d="M -62 0 C -66 76 -36 124 0 126 C 36 124 66 76 62 0"/><ellipse cx="0" cy="0" rx="62" ry="9"/>'
             f'<ellipse cx="0" cy="292" rx="66" ry="12"/></g>')
    ring_on = (f'<g transform="translate({gx} {gy+286}) scale(1 .3)"><g transform="scale(0.52) translate(-232 -258)">'
               f'<path d="{D["d"]}" fill="{Y}"/><rect x="100" y="255.5" width="90" height="5" fill="{BG}"/>'
               f'<text x="229" y="379" text-anchor="middle" font-family="Inter" font-weight="600" font-size="32" fill="{DARK}">Andrey</text></g></g>')
    stem = f'<line x1="{gx}" y1="{gy+126}" x2="{gx}" y2="{gy+286}" stroke="rgba(246,231,200,.8)" stroke-width="3"/>'
    return (f'<svg width="{VW}" height="{VH}" viewBox="0 0 {VW} {VH}"><defs>{shadow_filter("sh", 0, 5, 5, .55)}</defs>'
            + r + glass + ring_on + stem + '</svg>')
def gear_ring(x, y, s, key, name, rot=0):
    # mm units, R = 45; stem hole r 8, slit at the top dent
    arc = f'M -19 0 A 19 19 0 0 0 19 0'
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<path d="{G[key]} M 8 0 A 8 8 0 1 0 -8 0 A 8 8 0 1 0 8 0 Z" fill="{Y}" fill-rule="evenodd" filter="url(#sh2)"/>'
            f'<rect x="-0.45" y="-46" width="0.9" height="39" fill="{BG}"/>'
            f'<path id="ga{name}" d="{arc}" fill="none"/>'
            f'<text font-family="Inter" font-weight="600" font-size="5.6" fill="{DARK}" letter-spacing=".1"><textPath href="#ga{name}" startOffset="50%" text-anchor="middle">{name}</textPath></text>'
            f'</g>')
def ring_b():
    W, H = F['W'], F['H']
    src = (f'<g transform="translate(6 236) scale(0.15)"><path d="{F["base"]}" fill="{Y}" opacity=".9"/>'
           f'<path d="{G["edge"]}" fill="none" stroke="{CAR}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></g>')
    note = (f'<text x="22" y="328" font-family="Inter" font-size="13" fill="{MUTE}">край букв I–N–N–E → край кольца</text>')
    rings = gear_ring(110, 112, 2.2, 'g1', 'Sasha', -20) + gear_ring(352, 168, 2.75, 'g2', 'Tanya Andrianova') + gear_ring(600, 126, 2.25, 'g3', 'Igor Zotov', 14)
    return (f'<svg width="{VW}" height="{VH}" viewBox="0 0 {VW} {VH}"><defs>{shadow_filter("sh2", 0, 1.6, 1.6, .55)}</defs>'
            + src + note + rings + '</svg>')
def steel():
    return ('<linearGradient id="st" x1="0" x2="1"><stop offset="0" stop-color="#9F9A92"/><stop offset=".45" stop-color="#F3F1EC"/>'
            '<stop offset=".7" stop-color="#C9C5BD"/><stop offset="1" stop-color="#8E8981"/></linearGradient>')
def cutlery(ul, fill, x, y, s, rot, pivot=(900, 900), echoes=()):
    px, py = pivot
    g = f'<g transform="translate({x} {y}) scale({s}) translate({-px} {-py})">'
    for ang, col in echoes:
        g += f'<path d="{C[ul]}" fill="{col}" filter="url(#sh3)" transform="rotate({ang} {px} {py})"/>'
    g += f'<g transform="rotate({rot} {px} {py})"><path d="{C[ul]}" fill="{fill}" filter="url(#sh3)"/>'
    g += f'<path d="{C["fork"]}" fill="url(#st)" filter="url(#sh4)"/><path d="{C["knife"]}" fill="url(#st)" filter="url(#sh4)"/></g></g>'
    return g
def underlay_a():
    surf = (f'<clipPath id="ca"><rect x="0" y="0" width="{VW}" height="{VH}" rx="3"/></clipPath>'
            f'<g clip-path="url(#ca)"><image href="bun_print.jpg" x="-120" y="-420" width="960" height="1200" preserveAspectRatio="xMidYMid slice"/></g>')
    g = cutlery('dough', Y, 360, 178, 0.215, AX, pivot=(900, 900))
    return (f'<svg width="{VW}" height="{VH}" viewBox="0 0 {VW} {VH}"><defs>{steel()}{shadow_filter("sh3",0,5,5,.55)}{shadow_filter("sh4",1,3,2,.5)}</defs>'
            + surf + g + '</svg>')
def underlay_b():
    surf = f'<rect x="0" y="0" width="{VW}" height="{VH}" rx="3" fill="#EFE4CF"/>'
    steps = [0, AX*0.25, AX*0.5, AX*0.75]
    ech = list(zip(steps, [DARK, CRUST, CAR, '#E9C27A']))
    g = cutlery('plain', Y, 430, 318, 0.19, AX, pivot=(900, 1560), echoes=ech)
    return (f'<svg width="{VW}" height="{VH}" viewBox="0 0 {VW} {VH}"><defs>{steel()}{shadow_filter("sh3",0,4,4,.35)}{shadow_filter("sh4",1,3,2,.45)}</defs>'
            + surf + g + '</svg>')
body = header('COLORBLOCK × DNA · Dinner 10.10.2026 · место гостя', 'Бокал и приборы',
              'Кольцо на ножку бокала (реф. 8) и подложка по силуэту прибора (реф. 9). Форма берётся из контура DINNER, цвет — жёлтый афиши и тона булки, движение — вращение и шлейф, как смаз на фото.')
grid = '<div class="grid two">'
grid += idea('А', 'Кольцо — буква D из афиши', ring_a(),
             'Берём D прямо из леттеринга. Её «дырка» надевается на ножку, разрез идёт по спинке. Имя гостя набрано гротеском афиши по низу буквы. Как кольцо-шестерёнка в реф. 8, только форма наша.',
             'Режем: жёлтый картон 300 г, шаблон по контуру D, высота 70 мм. Снимаем: скальпель идёт по контуру буквы.',
             [(CLIENT[8], 'клиент · 8'), (POSTER, 'афиша · D')])
grid += idea('Б', 'Кольцо с вмятинами букв', ring_b(),
             'Шестерёнки из реф. 8, но зубцы не геометрические: это верхний край букв I–N–N–E, свёрнутый в круг. Мягкие бугры и V-вмятины те же, что у DINNER. Имя идёт по кругу вокруг ножки.',
             'Режем: жёлтый картон 300 г, Ø 90 мм, отверстие Ø 16 мм, разрез по вмятине. Три шаблона с разным числом зубцов.',
             [(CLIENT[8], 'клиент · 8'), (POSTER, 'афиша · край букв')])
grid += idea('В', 'Подложка с краем букв', underlay_a(),
             'Силуэт вилки и ножа с отступом 7 мм, как синяя подложка в реф. 9. По краю идут те же вмятины, что у DINNER. Приборы лежат вдоль диагонали афиши, на скатерти с фото булки.',
             'Режем: жёлтая бумага 160 г, шаблон по приборам DNA Kitchen. Снимаем: прибор ложится в свой силуэт.',
             [(CLIENT[9], 'клиент · 9'), (ref_img('DHDZ6aZtJS6')[0], '@kulu__club'), (POSTER, 'афиша · 51°')])
grid += idea('Г', 'Подложка-шлейф', underlay_b(),
             'Та же подложка в пяти слоях, от тёмной корки до жёлтого. Слои повёрнуты вокруг конца ручки от вертикали до диагонали афиши. Получается смаз вращения, собранный из бумаги.',
             'Режем: 5 тонов бумаги 160 г, один шаблон. Снимаем: раскладываем веер сверху камерой.',
             [(CLIENT[9], 'клиент · 9'), (ref_img('Dd8JXhly3G8')[0], '@limbatrip'), (POSTER, 'афиша · смаз')])
grid += '</div>'
open('board_ring.html', 'w').write(page(body + grid))
print('ok')
