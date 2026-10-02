import sys, math; sys.path.insert(0, '.')
from ui import *
F = load('flat'); L = F['letters']; T = load('tableware'); C = load('cutlery'); G = load('gear')
ANG = 51.2; CA, SA = math.cos(math.radians(ANG)), math.sin(math.radians(ANG))
VW, VH = 720, 372
K = VW/2000                     # px per mm: 2 m of table across the panel
def svg_open(extra=''):
    return (f'<svg width="{VW}" height="{VH}" viewBox="0 0 {VW} {VH}"><defs>{shadow_filter("p", 0, 2.5, 2.5, .35)}{shadow_filter("pp", 0, 4, 4, .45)}'
            '<radialGradient id="gl" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#fff" stop-opacity=".75"/><stop offset=".5" stop-color="#fff" stop-opacity=".2"/><stop offset="1" stop-color="#fff" stop-opacity=".45"/></radialGradient>'
            '<linearGradient id="st" x1="0" x2="1"><stop offset="0" stop-color="#9F9A92"/><stop offset=".45" stop-color="#F3F1EC"/><stop offset=".7" stop-color="#C9C5BD"/><stop offset="1" stop-color="#8E8981"/></linearGradient>'
            f'{extra}</defs><g transform="translate(0 {(VH - 1000*K)/2}) scale({K})">')
def svg_close(): return '</g></svg>'
def table(fill='#EFE4CF', image=None):
    s = f'<rect x="0" y="0" width="2000" height="1000" fill="{fill}"/>'
    if image:
        s += f'<clipPath id="tbl"><rect x="0" y="0" width="2000" height="1000"/></clipPath><g clip-path="url(#tbl)"><image href="{image}" x="-200" y="-1100" width="2400" height="3000" preserveAspectRatio="xMidYMid slice"/></g>'
    return s
def setting(x, side, plate_under='', glass=True):
    """plate centre 210 mm from the edge; fork left, knife right; glass toward the centre"""
    y = 210 if side == 0 else 790
    flip = 1 if side == 0 else -1
    s = plate_under
    s += f'<circle cx="{x}" cy="{y}" r="135" fill="#FBF8F3" filter="url(#p)"/><circle cx="{x}" cy="{y}" r="96" fill="none" stroke="rgba(60,30,10,.08)" stroke-width="3"/>'
    cs = 1/C['px']
    for kind, dx in (('fork', -175), ('knife', 175)):
        # cutlery paths are drawn tip up; turn them so the tips point away from the guest's edge
        cx0 = 115*C['px'] if kind == 'fork' else 185*C['px']
        cy0 = 150*C['px']
        s += (f'<g transform="translate({x+dx} {y}) rotate({0 if side == 0 else 180}) scale({cs}) translate({-cx0} {-cy0})">'
              f'<path d="{C[kind]}" fill="url(#st)" filter="url(#p)"/></g>')
    if glass:
        gx, gy = x + 196, y + flip*128
        s += (f'<circle cx="{gx+4}" cy="{gy+6}" r="40" fill="rgba(20,8,2,.18)"/>'
              f'<circle cx="{gx}" cy="{gy}" r="40" fill="rgba(255,255,255,.16)" stroke="rgba(255,255,255,.85)" stroke-width="3"/>'
              f'<path d="M {gx-26} {gy-12} A 28 28 0 0 1 {gx-8} {gy-28}" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".8"/>'
              f'<circle cx="{gx}" cy="{gy}" r="6" fill="rgba(255,255,255,.5)"/>')
    return s
def tw(key, x, y, h, rot, fill, img=False, fid='pp'):
    t = T[key]; s = h/t['h']
    px = 1/T['px']
    pat = ''
    if img:
        pat = f'<pattern id="bp{key}{int(x)}" patternUnits="userSpaceOnUse" x="0" y="0" width="{t["w"]*T["px"]}" height="{t["h"]*T["px"]}"><image href="bun_print.jpg" x="-300" y="-500" width="{t["w"]*T["px"]*2.2}" height="{t["w"]*T["px"]*2.75}" preserveAspectRatio="xMidYMid slice"/></pattern>'
        fill = f'url(#bp{key}{int(x)})'
    return (pat + f'<g transform="translate({x} {y}) rotate({rot}) scale({s*px}) translate({-t["w"]*T["px"]/2} {-t["h"]*T["px"]/2})">'
            f'<path d="{t["d"]}" fill="{fill}" filter="url(#{fid})"/></g>')
def idea_a():
    s = svg_open() + table('#C99158')
    for i, x in enumerate((370, 1000, 1630)):
        for side in (0, 1):
            y = 210 if side == 0 else 790
            under = ''.join(tw('plate', x + k*CA*26, y + k*SA*26, 300, 0, col)
                            for k, col in ((2, CRUST), (1, '#E9C27A')))
            s += setting(x, side, under + tw('plate', x, y, 300, 0, Y))
    # flat doubles in the middle band, all turned onto the poster diagonal
    s += tw('carafe', 690, 500, 250, ANG - 90, DARK) + tw('glass', 860, 470, 200, ANG - 90, CRUST)
    s += tw('bun', 1120, 510, 150, 20, None, img=True) + tw('bowl', 1350, 480, 150, ANG - 90, Y)
    s += tw('cup', 1560, 520, 120, ANG - 90, CRUST) + tw('glass', 330, 500, 200, ANG - 90, Y) + tw('bun', 500, 470, 130, -30, None, img=True)
    return s + svg_close()
def letter(i, x, y, h, rot, fill, fid='pp'):
    bx, by, bw, bh = L[i]['bbox']; s = h/bh
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s}) translate({-(bx+bw/2)} {-(by+bh/2)})">'
            f'<path d="{L[i]["d"]}" fill="{fill}" filter="url(#{fid})"/></g>')
def idea_b():
    s = svg_open() + table('#EFE4CF')
    for x in (370, 1000, 1630):
        s += setting(x, 0) + setting(x, 1)
    # serving boards with rolls, and the letters lying among them like the hand and spoon in ref 7
    s += f'<ellipse cx="1600" cy="500" rx="140" ry="92" fill="#FBF8F3" filter="url(#p)"/>'
    s += tw('bun', 1560, 490, 88, 10, None, img=True) + tw('bun', 1645, 515, 78, -40, None, img=True)
    s += f'<circle cx="1880" cy="497" r="96" fill="#FBF8F3" filter="url(#p)"/><circle cx="1880" cy="497" r="60" fill="#E7D2B0"/>'
    for i, (x, y, rot, col) in enumerate([(190, 500, ANG - 4, Y), (390, 505, ANG + 6, CAR), (620, 500, ANG - 6, Y),
                                           (860, 505, ANG + 3, Y), (1105, 500, ANG - 8, CAR), (1330, 505, ANG + 5, Y)]):
        s += letter(i, x, y, 160, rot, col)
    return s + svg_close()
def idea_c():
    s = svg_open() + table(image='bun_print.jpg')
    # runner: DINNER and line-up lines on the poster diagonal, repeated along the table
    for k, x in enumerate((330, 830, 1330, 1830)):
        sc = 0.30
        s += (f'<g transform="translate({x} 500) rotate({ANG}) scale({sc}) translate(-745 -260)"><path d="{F["base"]}" fill="{Y}" filter="url(#pp)"/></g>')
        s += (f'<g transform="translate({x + 120} 330) rotate({ANG})" font-family="Inter" font-weight="500" font-size="30" fill="{Y}">'
              f'<text>COLORBLOCK × DNA</text><text y="40">10 oct 2026 · 18:00</text></g>')
    for x in (370, 1000, 1630):
        s += setting(x, 0) + setting(x, 1)
    return s + svg_close()
def idea_d():
    s = svg_open() + table(DARK)
    for x in (370, 1000, 1630):
        s += setting(x, 0) + setting(x, 1)
    sc = 0.56; steps = [('off56', DARK), ('off42', '#6A3A22'), ('off28', CRUST), ('off14', CAR), ('base', Y)]
    for k, (key, col) in enumerate(steps):
        sh = (k - 2)*14
        s += (f'<g transform="translate({1000 + sh*CA} {500 + sh*SA}) scale({sc}) translate(-745 -260)">'
              f'<path d="{F[key]}" fill="{col}" filter="url(#pp)"/></g>')
    return s + svg_close()
body = header('COLORBLOCK × DNA · Dinner 10.10.2026 · два длинных стола', 'Стол',
              'Плоские силуэты посуды (реф. 6) и бумажные фигуры среди еды (реф. 7). Вместо случайных форм — контур DINNER, тарелки с его вмятинами, фото булки и диагональ афиши, вдоль которой всё сдвинуто, как при смазе. Вид сверху, 2 м стола.')
grid = '<div class="grid two">'
grid += idea('А', 'Бумажный двойник сервировки', idea_a(),
             'Под каждой тарелкой бумажная тарелка с вмятинами DINNER и два её тона, сдвинутые по диагонали афиши, как смаз. По центру плоские силуэты графина, бокала, миски и булки из бумаги и печати — как сервировка в реф. 6.',
             'Режем: бумага 160 г четырёх тонов и печать булки, шаблоны тарелки и посуды. Снимаем: раскладываем силуэты сверху.',
             [(CLIENT[6], 'клиент · 6'), (ref_img('DZSL58rI-0W')[0], '@catarinaguerreiro'), (ref_img('DZ6m4WMNJJR')[0], '@daffodill.studios')])
grid += idea('Б', 'Буквы среди еды', idea_b(),
             'Куски DINNER лежат между блюдами, как синяя рука и жёлтая ложка в реф. 7. Все буквы смотрят по диагонали афиши, слово читается вдоль стола. Рядом булочки, завёрнутые в печать булки.',
             'Режем: жёлтый и карамельный картон 300 г, буквы 200 мм. Снимаем: руки раскладывают буквы между блюдами.',
             [(CLIENT[7], 'клиент · 7'), (POSTER, 'афиша · DINNER'), (ref_img('keltoto')[0], '@keltoto')])
grid += idea('В', 'Скатерть — это афиша', idea_c(),
             'Рулон бумаги с фото булки со смазом, как бумага-хлеб у Ippei Tsujio. По центру идут DINNER и строки афиши под 51°. Тарелки и приборы стоят прямо на фоне афиши.',
             'Печать на рулоне 1 м, по длине стола. Снимаем: раскатываем рулон по столу.',
             [(ref_img('keltoto')[0], '@keltoto'), (POSTER, 'афиша · фон'), (ref_img('Da7ats-om7T')[0], '@sessionsartsclub')])
grid += idea('Г', 'DINNER слоями по центру', idea_d(),
             'Пять контуров DINNER с отступом, от тёмной корки до жёлтого, сдвинуты по диагонали афиши. Получается рельеф, как слоёная бумага у Гилдерслива и Дренк, и шлейф, как смаз на фото.',
             'Режем: картон 1,5 мм, обтянутый бумагой пяти тонов, контуры с отступом 8 мм. Снимаем: слои собираем на столе.',
             [(ref_img('Dd3fvcfhqTP')[0], '@owengildersleeve'), (ref_img('DalGsc3gP61')[0], '@jessicadrenk'), (POSTER, 'афиша · контур')])
grid += '</div>'
open('board_table.html', 'w').write(page(body + grid))
print('ok')
