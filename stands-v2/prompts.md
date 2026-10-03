# Промпты для генерации подставок

Из референсов взят только принцип, а не конкретные формы:
силуэт подсказывает, что ставить; толщина и срез материала — часть дизайна; на поверхности одна маленькая деталь, не больше;
форма мягкая и немного смешная, но не мультяшная.

Промпты на английском — генераторы понимают его лучше. Хвосты `--ar / --style raw / --s` — для Midjourney, в других генераторах их можно убрать.

---

## 1. Стиль (ставится в начало любого промпта)

```
Design object photography, tabletop accessory, thick die-cut slab with a clean vertical cut edge,
the edge shows the material layers, matte surface, one tiny graphic detail only,
soft simple silhouette, quiet contemporary design, natural light, seamless backdrop, high detail, 85mm lens
```

**Негативный промпт** (Stable Diffusion, Flux, Leonardo, OpenArt):

```
cartoon face, mascot, cute character, clip art, glossy plastic, 3d render look, clutter, random text, logo,
watermark, blurry, oversaturated, busy pattern
```

---

## 2. Повторяют посуду

**Тень тарелки — под тарелку.** Подставка в форме тени, которую тарелка отбрасывает на закате: тарелка стоит на собственной тени.

```
A dinner plate standing on a coaster cut in the exact shape of its own long evening shadow: a stretched
elongated ellipse that trails off to one side, made of deep ink-blue felt 6 mm thick, real sunlight casting
the true shadow in the same direction so the two overlap, overhead shot on a warm sand-colored table --ar 4:5 --style raw
```

**След бокала — под бокал.** Подставка повторяет кольцо, которое бокал оставляет на скатерти: незамкнутое двойное кольцо с каплей.

```
A coaster shaped like the ring stain a wine glass leaves on a tablecloth: an imperfect open double ring with
a small drip, cut from 5 mm burgundy cork with a darker sealed edge, a wine glass standing on it slightly off
centre, top-down, soft window light, linen-white backdrop --ar 1:1 --style raw
```

**Уголок салфетки — под приборы.** Треугольная подставка с мягким «загибом», как угол сложенной салфетки. Вилка и нож лежат вдоль сгиба.

```
A cutlery rest shaped like the folded corner of a napkin: a soft rounded triangle with one corner gently
lifted and a crisp fold crease, made of thick matte powder-yellow ceramic, a fork and knife resting in the
crease, low angle 20 degrees, warm afternoon light, terracotta backdrop --ar 4:5 --style raw
```

**Круги на воде — под миску.** Стопка из 3–4 колец разного размера, каждый слой меньше и другого оттенка — как рябь вокруг миски.

```
A bowl trivet made of three stacked concentric wavy rings like ripples on water, each layer smaller and a
slightly different shade of sea-green, visible stepped edges, a ceramic bowl sitting in the centre,
three-quarter view, soft daylight, pale grey backdrop --ar 1:1 --style raw
```

**Пар — под чайник.** Плоский силуэт поднимающегося пара, положенный на стол: длинная волнистая форма из трёх «струек», которые сливаются внизу.

```
A trivet shaped like rising steam laid flat: three soft wavy ribbons merging into one base, cut from thick
off-white wool felt with a stitched edge, a cast iron teapot standing on the base, overhead shot, morning light,
charcoal backdrop --ar 3:4 --style raw
```

**Пустое место ложки — под ложку.** Прямоугольная плитка, в которой насквозь вырезан силуэт ложки, — ложка ложится в свой «негатив».

```
A spoon rest: a thick rounded rectangle tile with a spoon-shaped cut-out going through it, the real spoon
lying beside it, made of speckled terrazzo in cream and rust, crisp side light showing the depth of the
cut-out, minimal, sage backdrop --ar 4:3 --style raw
```

---

## 3. Сами по себе

**Топография.** Стопка слоёв, как контурная карта холма; каждый слой своего цвета. Вблизи кажется пейзажем, сверху — подставкой.

```
A coaster built as a stacked contour map of a small hill: five thin irregular layers, each one smaller than
the last, colors stepping from deep olive to pale lime, visible stepped edges, three-quarter macro view,
low raking light, warm grey backdrop --ar 1:1 --style raw
```

**Затмение.** Два диска разного цвета, сдвинутые друг относительно друга; там, где они пересекаются, вырезан полумесяц.

```
A pair of overlapping thick discs, one tomato red and one dusty violet, slightly offset like an eclipse,
a thin crescent of the table showing through where they overlap, cork core visible on the edge,
top-down, hard sun with crisp shadow, cream backdrop --ar 1:1 --style raw
```

**Петля.** Одна толстая лента, завязанная мягкой восьмёркой; приборы лежат в петлях.

```
A cutlery rest shaped like a thick soft ribbon tied in a loose figure-eight, one continuous rounded form,
matte cobalt glazed ceramic, a pair of chopsticks resting across both loops, low angle, studio light,
butter-yellow backdrop --ar 4:3 --style raw
```

**Крошки.** Россыпь маленьких неровных подставок, как крошки от хлеба, только крупные; ставятся под соль, специи, свечи.

```
A scattered set of seven small irregular crumb-shaped coasters in different sizes, cut from thick toasted
brown and cream card stock with rough deckled edges, a salt cellar and a tealight on two of them, top-down,
soft light, deep chocolate backdrop --ar 4:5 --style raw
```

**Инициалы — карточка с местом.** Подставка под бокал в форме первой буквы имени гостя: одновременно и рассадка.

```
Place card coasters cut as single bold rounded letters, chunky soft geometric letterforms, each letter a
different muted color — clay, moss, ink blue — a wine glass standing on each letter at a set dinner table,
overhead shot, candle-lit evening mood --ar 3:2 --style raw
```

---

## 4. Сцены целиком

**Стол на закате**

```
Overhead view of a dinner table at golden hour with a set of sculptural tabletop coasters in muted earthy
colors — a plate on its own shadow-shaped coaster, a wine glass on a ring-stain coaster, cutlery on a folded
napkin-corner rest, a teapot on a steam-shaped trivet, long warm shadows across the table, editorial
interior magazine style --ar 4:5 --style raw --s 200
```

**Срез крупно**

```
Extreme macro of the cut edge of stacked coasters, layers of colored card stock, cork and felt visible like
geological strata, shallow depth of field, soft side light --ar 16:9 --style raw
```

---

## 5. Как варьировать

- **Материал:** картон, пробка, войлок, керамика, терраццо, литой силикон, крашеный шпон — форма та же, ощущение другое.
- **Свет:** жёсткое низкое солнце, если идея в тени («Тень тарелки», «Затмение»); мягкий дневной свет для фактуры.
- **Ракурс:** сверху, если важен силуэт; под углом 20–30°, если важна толщина и срез.
- **Палитра:** называйте 2–3 цвета прямо в промпте. Приглушённые природные цвета дают более «дизайнерский» результат, чем чистые яркие.
- Если генератор рисует лишние надписи — добавьте `no text` в негатив.
