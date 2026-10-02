# DNA Dinner — вёрстка сета из афиши

Пять листов с вариантами по элементам: обложка (что берём из афиши), антресоль, карточки с именем, бокал и приборы, стол. Каждый элемент собран из контура DINNER, фото булки со смазом, диагонали 51°, цветов афиши и гротеска Inter. Рядом с каждым вариантом стоят референсы, из которых он сделан.

## Что лежит

- `dinner_alpha_flat.png`, `dinner_alpha_poster.png` — маска леттеринга DINNER, снятая с афиши: развёрнутая горизонтально и в положении афиши (угол 51,2°).
- `bun_print.jpg` — фон афиши без текста, со смазом по кругу. `bg_dark.jpg` — он же, затемнённый, для фона листов.
- `lib.py` — обрезка маски и трассировка в SVG через potrace, пути в абсолютных координатах.
- `make_assets.py` — контур, отступы, кадры таяния, буквы по перемычкам (D | I | N | N | E | R).
- `gear.py` — кольцо с вмятинами верхнего края букв. `cutlery.py` — вилка, нож и подложки. `tableware.py` — бумажная посуда. `scan.py` — кадры решётки.
- `ui.py` — общий вид листов. `b_cover.py`, `b_mezz.py`, `b_cards.py`, `b_ring.py`, `b_table.py` — сами листы.
- `shot.js` — рендер HTML в PNG через Playwright.

## Как собрать

Нужны Python с `opencv-python` и `numpy`, `potrace`, Node с Playwright.

```sh
export DNA_POSTER=/путь/к/афише.jpg      # афиша 1600×2000
export DNA_CLIENT_IMG=/путь/к/рефам       # референсы клиента 3–9 как 02.jpg…08.jpg
# refs/ — превью работ со страницы ресёрча и refs/index.json; без них вместо превью будут пустые места
python3 make_assets.py && python3 gear.py && python3 cutlery.py && python3 tableware.py && python3 scan.py
for b in cover mezz cards ring table; do python3 b_$b.py; node shot.js "$PWD/board_$b.html" "$PWD/board_$b.png" 1600 auto 1.5; done
```

Референсы клиента, превью чужих работ и сама афиша в git не лежат.
