import sys, math; sys.path.insert(0, '.')
from ui import *
F = load('flat'); L = F['letters']
NAMES = ['Anna Petrova', 'Mark Belov', 'Vera Lis', 'Lev Orlov', 'Nina Sokol', 'Oleg Rudin']
ANG = 51.2
def bbox(i): return L[i]['bbox']
def tent_row():
    W, H = 1472, 360
    cw, ch, gap = 196, 122, 59
    x0 = (W - (6*cw + 5*gap))/2; base = 318
    s = 0.6
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{shadow_filter("tsh", 0, 6, 6, .5)}</defs>']
    out.append(f'<line x1="0" y1="{base}" x2="{W}" y2="{base}" stroke="rgba(246,231,200,.25)" stroke-width="1.2"/>')
    for i in range(6):
        x = x0 + i*(cw + gap); top = base - ch
        bx, by, bw, bh = bbox(i)
        lx = x + cw/2 - (bx + bw/2)*s; ly = top - 0.7*bh*s - by*s
        out.append(f'<ellipse cx="{x+cw/2}" cy="{base+6}" rx="{cw*0.55}" ry="7" fill="#120600" opacity=".45"/>')
        out.append(f'<g transform="translate({lx:.1f} {ly:.1f}) scale({s})"><path d="{L[i]["d"]}" fill="{Y}" filter="url(#tsh)"/></g>')
        out.append(f'<clipPath id="tc{i}"><rect x="{x}" y="{top}" width="{cw}" height="{ch}"/></clipPath>')
        out.append(f'<g clip-path="url(#tc{i})"><rect x="{x}" y="{top}" width="{cw}" height="{ch}" fill="{CRUST}"/>'
                   f'<image href="bun_print.jpg" x="{x - 40 - (i*83) % 380}" y="{top - 260 - (i*57) % 360}" width="640" height="800" preserveAspectRatio="xMidYMid slice"/>'
                   f'<text transform="translate({x+20} {top+22}) rotate({ANG})" font-family="Inter" font-weight="600" font-size="15" fill="{Y}">{NAMES[i]}</text>'
                   f'<text transform="translate({x+cw-62} {top+18}) rotate({ANG})" font-family="Inter" font-weight="500" font-size="9.5" fill="{Y}" opacity=".85">10.10 · 18:00</text>'
                   f'</g>')
        out.append(f'<line x1="{x}" y1="{top}" x2="{x+cw}" y2="{top}" stroke="rgba(0,0,0,.25)" stroke-width="1"/>')
    out.append('</svg>')
    return ''.join(out)
def fold_card(cx, cy, rot, fill, back, li, s, text_fill, name, fid):
    w, h = 300, 176
    bx, by, bw, bh = bbox(li)
    # letter placed on the right half; hinge on its left edge
    lx = w*0.72 - (bx + bw/2)*s; ly = h/2 - (by + bh/2)*s
    hx = (bx)*s + lx
    letter = f'<g transform="translate({lx:.1f} {ly:.1f}) scale({s})"><path d="{L[li]["d"]}"/></g>'
    flap = (f'<g transform="translate({hx:.1f} 0) scale(-0.52 1) translate({-hx:.1f} 0)">'
            f'<g transform="translate({lx:.1f} {ly:.1f}) scale({s})"><path d="{L[li]["d"]}" fill="{back}" filter="url(#{fid})"/></g></g>')
    txt = (f'<g transform="translate(26 22) rotate({ANG - rot})" font-family="Inter" fill="{text_fill}">'
           f'<text font-weight="600" font-size="15">{name}</text>'
           f'<text y="18" font-weight="500" font-size="10">Dinner · 10.10.2026</text>'
           f'<text y="31" font-weight="500" font-size="10">DNA Kitchen · 18:00</text></g>')
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) translate({-w/2} {-h/2})">'
            f'<rect width="{w}" height="{h}" fill="{fill}" filter="url(#csh)"/>'
            f'<g fill="#140802">{letter}</g>{txt}{flap}</g>')
def fold_cards():
    W, H = 720, 360
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{shadow_filter("csh", 0, 6, 7, .5)}{shadow_filter("fsh", -6, 6, 5, .45)}</defs>'
            + fold_card(220, 96, -14, '#5A2F1B', '#6E3C25', 0, 0.42, Y, 'Lev Orlov', 'fsh')
            + fold_card(380, 172, -14, CAR, '#D59A5C', 2, 0.42, BG, 'Vera Lis', 'fsh')
            + fold_card(540, 248, -14, Y, '#FFF3B8', 5, 0.42, '#5A2F1B', 'Anna Petrova', 'fsh')
            + '</svg>')
def layer_card(cx, cy, rot, li, s, name):
    w, h = 300, 196
    bx, by, bw, bh = bbox(li)
    lx = w/2 - (bx + bw/2)*s + 30; ly = h/2 - (by + bh/2)*s
    def win(d): return f'<g transform="translate({lx:.1f} {ly:.1f}) scale({s})"><path d="{d}"/></g>'
    # window = rect minus offset contour (evenodd in one path is not possible across groups -> mask)
    def layer(col, d, mid):
        return (f'<mask id="m{mid}"><rect width="{w}" height="{h}" fill="#fff"/><g fill="#000">{win(d)}</g></mask>'
                f'<rect width="{w}" height="{h}" fill="{col}" mask="url(#m{mid})" filter="url(#lsh)"/>')
    k = f'{li}{int(cx)}'
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) translate({-w/2} {-h/2})">'
            f'<rect width="{w}" height="{h}" fill="{Y}" filter="url(#csh)"/>'
            + layer('#E2AE68', L[li]['d'], k + 'a') + layer(CAR, L[li]['o16'], k + 'b') + layer(CRUST, L[li]['o32'], k + 'c')
            + f'<g transform="translate(22 20) rotate({ANG - rot})" font-family="Inter" fill="{Y}"><text font-weight="600" font-size="15">{name}</text>'
              f'<text y="17" font-weight="500" font-size="10">Dinner · 10.10.2026</text></g>'
            + '</g>')
def layer_cards():
    W, H = 720, 360
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{shadow_filter("csh", 0, 6, 7, .5)}'
            f'<filter id="lsh" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="2.2" stdDeviation="2.2" flood-color="#1a0a03" flood-opacity=".7"/></filter></defs>'
            + layer_card(205, 150, -8, 0, 0.36, 'Mark Belov') + layer_card(500, 210, 7, 2, 0.36, 'Nina Sokol') + '</svg>')
body = header('COLORBLOCK × DNA · Dinner 10.10.2026 · место гостя', 'Карточки с именем',
              'Домик с фигурой над коньком (реф. 4) и плоская карточка с вырезом (реф. 5). В нашей версии фигура — это сама надпись DINNER: её куски, вырезы и слои. Имя набрано гротеском афиши и стоит по её диагонали.')
grid = '<div class="grid" style="grid-template-columns:1fr">'
grid += idea('А', 'Домик: над коньком кусок DINNER', tent_row(),
             'Домик как в реф. 4, только над коньком стоит не фигурка, а кусок надписи. Шесть мест подряд дают D-I-N-N-E-R, слово собирается вдоль стола. Лицевая сторона — фото булки с афиши, имя жёлтым под 51°, как лайн-ап.',
             'Режем: жёлтый картон 300 г, на лицевой стороне печать булки; буква вырезается из задней стенки, сгиб до неё не доходит. Снимаем: камера едет вдоль стола, и слово собирается.',
             [(CLIENT[4], 'клиент · 4'), (ref_img('DdjIhPjILvp')[0], '@kellianderson'), (POSTER, 'афиша')])
grid += '</div><div class="grid two" style="margin-top:46px">'
grid += idea('Б', 'Карточка с отогнутой буквой', fold_cards(),
             'Плоская карточка на тарелке, как билеты в реф. 5: буква вырезана с трёх сторон и отогнута, в проёме видна скатерть. Три цвета — жёлтый афиши и два тона булки. Текст идёт по диагонали афиши.',
             'Режем: картон 300 г трёх цветов, скальпель по контуру буквы, биговка по линии сгиба. Снимаем: гость отгибает букву.',
             [(CLIENT[5], 'клиент · 5'), (ref_img('DPMJkGNkbVK')[0], '@buildingblock'), (ref_img('DO-gCGxj3yJ')[0], '@bambra.bebold')])
grid += idea('В', 'Слоёная карточка', layer_cards(),
             'Буква прорезана в четырёх слоях бумаги, каждый следующий слой с отступом от контура. Внутри — жёлтая буква с мягкими ступенями, как слоёные круги Гилдерслива. Цвета идут от корки к мякишу и жёлтому.',
             'Режем: 4 листа 160 г, контур с отступом 0, 4 и 8 мм, склейка. Снимаем: слои ложатся один на другой.',
             [(ref_img('Dd3fvcfhqTP')[0], '@owengildersleeve'), (ref_img('DalGsc3gP61')[0], '@jessicadrenk'), (CLIENT[5], 'клиент · 5')])
grid += '</div>'
open('board_cards.html', 'w').write(page(body + grid))
print('ok')
