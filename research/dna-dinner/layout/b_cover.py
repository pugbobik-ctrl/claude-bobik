import sys, math; sys.path.insert(0, '.')
from ui import *
F = load('flat'); P = load('poster')
ANG = 51.2
def row(visual, title, text):
    return (f'<div class="dna"><div class="dv">{visual}</div><div><h3>{title}</h3><p>{text}</p></div></div>')
def v_contour():
    return f'<svg width="250" height="96" viewBox="80 80 1330 360"><path d="{F["base"]}" fill="{Y}"/></svg>'
def v_axis():
    sc = 0.0612; fx, fy = 70, 2
    cx, cy = fx + 650.5*sc, fy + 691.4*sc
    ca, sa = math.cos(math.radians(ANG)), math.sin(math.radians(ANG))
    x0, y0 = cx - 62*ca, cy - 62*sa; x1, y1 = cx + 66*ca, cy + 66*sa
    r = 30
    return (f'<svg width="250" height="122" viewBox="0 0 250 122">'
            f'<rect x="{fx}" y="{fy}" width="98" height="118" fill="none" stroke="rgba(246,231,200,.35)"/>'
            f'<g transform="translate({fx} {fy}) scale({sc})"><path d="{P["d"]}" fill="{Y}"/></g>'
            f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{CAR}" stroke-width="1.6" stroke-dasharray="4 3"/>'
            f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0+56:.1f}" y2="{y0:.1f}" stroke="{CAR}" stroke-width="1.6"/>'
            f'<path d="M {x0+r:.1f} {y0:.1f} A {r} {r} 0 0 1 {x0+r*ca:.1f} {y0+r*sa:.1f}" fill="none" stroke="{CAR}" stroke-width="1.6"/>'
            f'<text x="{x0+62:.1f}" y="{y0+30:.1f}" font-family="Inter" font-weight="600" font-size="20" fill="{Y}">51°</text></svg>')
def v_spin():
    return ('<div style="width:250px;height:110px;overflow:hidden;border-radius:2px;position:relative">'
            '<img src="bun_print.jpg" style="position:absolute;width:520px;left:-150px;top:-470px"></div>')
def v_color():
    sw = [(Y, 'FEED95'), ('#E9C27A', 'E9C27A'), (CAR, 'C68B4E'), (CRUST, '7A462A'), (DARK, '452213')]
    return ('<div style="display:flex;gap:8px">' + ''.join(
        f'<div style="width:44px"><div style="width:44px;height:58px;background:{c};border-radius:2px"></div>'
        f'<div style="font-size:10.5px;color:{MUTE};margin-top:5px">{t}</div></div>' for c, t in sw) + '</div>')
def v_type():
    return (f'<svg width="250" height="110" viewBox="0 0 250 110"><defs><filter id="mb" x="-20%" y="-50%" width="140%" height="200%">'
            f'<feGaussianBlur stdDeviation="1.7 0.3"/></filter></defs>'
            f'<g transform="translate(8 6) rotate({ANG*0.0})" font-family="Inter" font-size="20" fill="{Y}">'
            f'<text y="20" font-weight="500" letter-spacing=".02em">COLORBLOCK</text>'
            f'<text y="48" font-weight="500">Tanya Andrianova</text>'
            f'<text y="74" font-weight="500" filter="url(#mb)">Igor Zotov</text>'
            f'<text y="100" font-weight="500" filter="url(#mb)" opacity=".9">10 oct 2026</text></g></svg>')
CLIENT_MAP = [(3, 'полосы на клипсах', 'антресоль'), (4, 'домик с фигурой', 'карточки'), (5, 'карточка с вырезом', 'карточки'),
              (6, 'силуэты посуды', 'стол'), (7, 'фигуры среди еды', 'стол'), (8, 'кольцо на бокал', 'бокал'), (9, 'подложка под прибор', 'приборы')]
extra = f'''
.cov{{display:grid;grid-template-columns:470px 1fr;gap:64px;margin-top:40px;align-items:start}}
.poster img{{width:470px;display:block}}
.poster figcaption{{margin-top:10px;font-size:13px;color:{MUTE}}}
.dnas{{display:flex;flex-direction:column}}
.dna{{display:grid;grid-template-columns:270px 1fr;gap:28px;align-items:center;padding:16px 0;border-top:1px solid rgba(254,237,149,.3)}}
.dna h3{{margin:0 0 6px;font-size:21px;font-weight:600;color:{Y}}}
.dna p{{margin:0;font-size:15.5px;line-height:1.45;color:{CREAM}}}
.cl{{margin-top:44px;border-top:1px solid rgba(254,237,149,.35);padding-top:16px}}
.cl h2{{margin:0 0 16px;font-size:21px;font-weight:600;color:{Y}}}
.clrow{{display:grid;grid-template-columns:repeat(7,1fr);gap:16px}}
.clrow img{{width:100%;aspect-ratio:1;object-fit:cover;display:block;border-radius:2px}}
.clrow div{{margin-top:8px;font-size:13.5px;line-height:1.35;color:{CREAM}}}
.clrow span{{color:{Y};font-weight:600}}
'''
body = header('COLORBLOCK × DNA · Dinner 10.10.2026 · бумажный сет', 'Из афиши в бумагу',
              'Носители берём из референсов клиента, характер — из афиши. На следующих листах каждый элемент сделан в 2–4 вариантах, и рядом с каждым стоят референсы, из которых он собран.')
dn = (row(v_contour(), 'Контур DINNER', 'Одна мягкая лента, буквы выдавлены V-вмятинами, у R хвост-капля. Не шрифт, а сам контур с афиши: по нему режем кольца, домики, слои.')
      + row(v_axis(), 'Диагональ 51°', 'Надпись и все строки идут под одним углом. На столе по нему ложатся приборы, буквы и сдвиг слоёв.')
      + row(v_spin(), 'Вращение и смаз', 'Фон — булка со смазом по кругу. Печатаем его на полосах и скатерти, а в бумаге повторяем веером, шлейфом и полосами на ветру.')
      + row(v_color(), 'Цвет', 'Жёлтый надписи и тона булки, от мякиша к корке. Больше цветов не добавляем.')
      + row(v_type(), 'Шрифт', 'Гротеск, как на афише. Имена и даты стоят по диагонали, часть строк смазана, как будто бумага двигалась.'))
cov = (f'<div class="cov"><figure class="poster" style="margin:0"><img src="{POSTER}"><figcaption>Афиша Dinner, 10.10.2026</figcaption></figure>'
       f'<div class="dnas">{dn}</div></div>')
cl = ('<div class="cl"><h2>Что просит клиент</h2><div class="clrow">' + ''.join(
      f'<figure style="margin:0"><img src="{CLIENT[n]}"><div><span>{n}</span> · {a} → {b}</div></figure>' for n, a, b in CLIENT_MAP) + '</div></div>')
open('board_cover.html', 'w').write(page(body + cov + cl, extra_css=extra))
print('ok')
