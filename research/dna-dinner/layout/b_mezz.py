import sys, math; sys.path.insert(0, '.')
from ui import *
F = load('flat'); P = load('poster')
ANG = 51.2
LINEUP = ['Tanya Andrianova', 'Igor Zotov', 'Andrey Lee', 'Sasha Chernikov', 'Sophia Zhuravkova']
def clip(x, top):
    return (f'<path d="M {x-7} {top} L {x-4} {top-15} M {x+7} {top} L {x+4} {top-15}" stroke="#cfc9bf" stroke-width="1.6" fill="none"/>'
            f'<rect x="{x-11}" y="{top-1}" width="22" height="13" rx="1.5" fill="#141210"/>')
def comp_strips():
    W, H = 1472, 430
    N = 24; ws = 52; gap = 8.0; x0 = (W - (N*ws + (N-1)*gap))/2
    rail = 26; top = rail + 16
    CW, CH = N*ws + (N-1)*gap, 470          # composition size
    # composition: bun print, three diagonal DINNERs, line-up lines between them (poster layout laid out wide)
    sc = 400/1133
    comp = [f'<image href="bun_print.jpg" x="0" y="-560" width="{CW}" height="{CW*1.25}" preserveAspectRatio="xMidYMid slice"/>']
    for k, cx in enumerate([250, 760, 1270]):
        comp.append(f'<g transform="translate({cx - 637*sc} {40 - 125*sc}) scale({sc})"><path d="{P["d"]}" fill="{Y}"/></g>')
    def lines(x, y, rows, size=17, w=500, op=1):
        t = ''.join(f'<text y="{i*size*1.16}" >{r}</text>' for i, r in enumerate(rows))
        return f'<g transform="translate({x} {y}) rotate({ANG})" font-family="Inter" font-weight="{w}" font-size="{size}" fill="{Y}" opacity="{op}">{t}</g>'
    comp.append(lines(520, 30, ['COLORBLOCK × DNA'], 26, 500))
    comp.append(lines(420, 120, ['Line-up'] + LINEUP, 17, 500))
    comp.append(lines(1040, 40, ['10 oct 2026', 'Samokatnaya 4s53', 'DNA Kitchen', '18:00'], 19, 500))
    comp.append(lines(960, 210, ['Line-up'] + LINEUP, 17, 500, .9))
    comp.append(lines(40, 250, ['10 oct 2026 · 18:00'], 19, 500))
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><g id="comp">{"".join(comp)}</g>'
           f'<filter id="ssh" x="-20%" y="-5%" width="140%" height="110%"><feDropShadow dx="3" dy="5" stdDeviation="4" flood-color="#0d0400" flood-opacity=".55"/></filter></defs>']
    out.append(f'<line x1="0" y1="{rail}" x2="{W}" y2="{rail}" stroke="#8d847a" stroke-width="3"/>')
    for i in range(N):
        x = x0 + i*(ws + gap)
        dy = 34*math.sin(2*math.pi*i/N*1.35 + 0.4)
        ln = min(330 + 48*math.sin(i*1.7) + 30*math.cos(i*0.6), H - top - 14)
        r = ws/2
        d = f'M {x} {top} L {x+ws} {top} L {x+ws} {top+ln-r} A {r} {r} 0 0 1 {x} {top+ln-r} Z'
        out.append(f'<clipPath id="sc{i}"><path d="{d}"/></clipPath>')
        out.append(f'<g filter="url(#ssh)"><g clip-path="url(#sc{i})"><use href="#comp" transform="translate({x0} {top - 20 + dy:.1f})"/></g></g>')
        out.append(clip(x + ws/2, top))
    out.append('</svg>')
    return ''.join(out)
def threads():
    W, H = 456, 400
    words = ['Tanya', 'DINNER', 'Igor', 'Zotov', 'COLORBLOCK', 'Andrey', 'Lee', 'Sasha', 'DNA', 'Sophia', '10.10']
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><line x1="0" y1="14" x2="{W}" y2="14" stroke="#8d847a" stroke-width="3"/>']
    n = len(words); step = (W - 40)/(n - 1)
    grad = [Y, '#FAE491', '#F4D686', '#EDC77C', '#E5B872', '#DCA968', '#D29A5E', CAR, '#BD8148', '#B57942']
    for i, wd in enumerate(words):
        x = 20 + i*step
        letters = list(wd)
        size = 30
        y = 40 + (i % 3)*14
        out.append(f'<line x1="{x}" y1="14" x2="{x}" y2="{y + len(letters)*size*1.02}" stroke="rgba(246,231,200,.35)" stroke-width="1"/>')
        for j, ch in enumerate(letters):
            ph = math.cos(j*0.9 + i*1.3)
            sx = 0.25 + 0.75*abs(ph)
            col = grad[min(len(grad)-1, int(j*len(grad)/max(len(letters), 8)))]
            out.append(f'<text transform="translate({x} {y + (j+1)*size*1.0}) scale({sx:.2f} 1)" text-anchor="middle" font-family="Inter" font-weight="700" font-size="{size}" fill="{col}">{html.escape(ch)}</text>')
    out.append('</svg>')
    return ''.join(out)
def tapes():
    W, H = 456, 400
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4EEE3"/><stop offset="1" stop-color="#E9DFCF"/></linearGradient></defs>']
    out.append(f'<rect x="0" y="40" width="{W}" height="10" fill="#5b5148"/>')
    rows = [['18:00  DINNER', '18:04  Tanya Andrianova', '18:52  Tanya Andrianova', '19:30  Igor Zotov', '20:15  Igor Zotov', '20:40  Andrey Lee'],
            ['18:00  COLORBLOCK × DNA', '18:30  Line-up', '19:00  Sasha Chernikov', '19:45  Sasha Chernikov', '20:20  Sophia Zhuravkova'],
            ['18:00  10 oct 2026', '18:10  Samokatnaya 4s53', '19:05  DNA Kitchen', '20:00  DINNER', '21:00  DINNER', '22:00  DINNER', '23:00  DINNER']]
    for k, (x, ln) in enumerate([(84, 312), (226, 268), (368, 350)]):
        out.append(f'<rect x="{x-36}" y="10" width="72" height="34" rx="5" fill="#1d1a17"/><rect x="{x-23}" y="40" width="46" height="3" fill="#000"/>')
        out.append(f'<path d="M {x-23} 43 L {x+23} 43 L {x+23} {43+ln} L {x+5} {43+ln-6} L {x-7} {43+ln+2} L {x-23} {43+ln-4} Z" fill="url(#fade)"/>')
        out.append(f'<g transform="translate({x+20} {43 + ln - 116}) rotate(90) scale(0.072)"><path d="{F["base"]}" fill="#2B140A"/></g>')
        t = ''; cw = 5.6
        for line, ylin in ((0, 0), (1, 15)):
            pos = ln - 126
            for i, r in enumerate(rows[k][line::2]):
                L = len(r)*cw
                if pos - L < 8: break
                if line == 0 and i == 1:
                    t += ''.join(f'<text x="{pos - d:.1f}" y="{ylin}" text-anchor="end" opacity="{0.5 - d*0.06:.2f}">{html.escape(r)}</text>' for d in (1.5, 3, 4.5, 6))
                t += f'<text x="{pos}" y="{ylin}" text-anchor="end">{html.escape(r)}</text>'
                pos -= L + 18
        out.append(f'<g transform="translate({x+2} 43) rotate(90)" font-family="Inter" font-weight="500" font-size="10" fill="#2B140A">{t}</g>')
    out.append('</svg>')
    return ''.join(out)
def grid_panel():
    W, H = 456, 400
    frames = ''.join(f'<image href="gen/scan_frame{k}.png" x="{8 + k*112}" y="300" width="104" height="53" preserveAspectRatio="xMidYMid meet"/>' for k in range(4))
    arrows = (f'<text x="8" y="378" font-family="Inter" font-size="12" fill="{MUTE}">гость идёт мимо → капли растут</text>')
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect x="8" y="10" width="440" height="270" fill="#5A2F1B"/>'
            f'<image href="gen/scan_view1.png" x="8" y="18" width="440" height="225" preserveAspectRatio="xMidYMid meet"/>'
            f'{frames}{arrows}</svg>')
body = header('COLORBLOCK × DNA · Dinner 10.10.2026 · антресоль', 'Листы на антресоли',
              'Полосы на клипсах (реф. 3) висят над столами и двигаются от воздуха и людей — это смаз с афиши, сделанный бумагой. На полосах — фото булки, DINNER и лайн-ап по диагонали.')
grid = '<div class="grid" style="grid-template-columns:1fr">'
grid += idea('А', 'Афиша, разрезанная на полосы', comp_strips(),
             'Полосы на клипсах, как в реф. 3, но на них напечатана афиша, разложенная на ширину антресоли: фото булки, три DINNER по диагонали и лайн-ап. Каждая полоса сдвинута по волне, и надпись ломается, как портрет у Койке. От воздуха полосы шевелятся — это живой смаз.',
             'Печать на бумаге 200 г, 24 полосы по 190 мм, длина 1,2–1,6 м, концы скруглены, как хвост у R. Снимаем: режем полосы ножом по линейке и вешаем по одной.',
             [(CLIENT[3], 'клиент · 3'), (ref_img('DZMZA_TzZWa')[0], '@kensukekoike'), (ref_img('DbVX4NtMCHh')[0], '@zabra.co')])
grid += '</div><div class="grid three" style="margin-top:46px">'
grid += idea('Б', 'Нити из букв лайн-апа', threads(),
             'Имена из лайн-апа вырезаны по буквам и висят нитями, как цифры у Моро. Буквы — гротеск афиши, цвет идёт от жёлтого к тонам булки. Буквы крутятся на леске, и имена мигают.',
             'Режем: картон 300 г, буквы 120 мм, леска. Снимаем: вырезаем буквы и нанизываем.',
             [(CLIENT[3], 'клиент · 3'), (ref_img('Emmanuelle')[0], 'Moureaux'), (ref_img('DT2-O7AEx0s')[0], '@topic_tomislav')])
grid += idea('В', 'Лента, которая растёт', tapes(),
             'На перилах три чековых принтера. Весь вечер они печатают лайн-ап и время, ленты свисают и растут к столам. К концу ужина это полосы из реф. 3, только напечатанные вживую.',
             'Термобумага 80 мм, 3 принтера, от 3 рулонов. Снимаем: таймлапс 18:00–23:00.',
             [(CLIENT[3], 'клиент · 3'), (ref_img('Dd_22UzoLQs')[0], '@ade3'), (ref_img('DJtSDChKvs2')[0], '@belencabello_')])
grid += idea('Г', 'Решётка: DINNER тает', grid_panel(),
             'Лист-скан: за решёткой из прорезей четыре кадра DINNER, который тает. Гость идёт мимо, и с букв стекают капли, как хвост у R на афише.',
             'Печать кадров и тёмный картон, прорези 15 мм через 60 мм, панель 1,4 × 1,6 м, режем по линейке.',
             [(ref_img('DULDDa1EqGq')[0], '@teekenng'), (ref_img('DaIZ-CwMMJw')[0], '@studio.ete'), (POSTER, 'афиша · R')])
grid += '</div>'
open('board_mezz.html', 'w').write(page(body + grid))
print('ok')
