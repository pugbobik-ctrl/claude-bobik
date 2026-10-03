# Промпты для генерации подставок

Промпты на английском: генераторы понимают его лучше. Внутри каждого блока — что подставить и как варьировать.
Хвосты `--ar / --style raw / --s` — для Midjourney; для других генераторов просто уберите их.

---

## 1. Базовый стиль (вставляйте в начало любого промпта)

```
Product photography of die-cut coasters made of thick laminated colored paperboard, 4 layers glued together,
visible layered edge with a thin pale paper core line, matte velvety surface with fine paper tooth,
copper hot-foil stamped details, soft rounded playful silhouettes, minimal Scandinavian-Japanese graphic design,
studio shot, hard afternoon sunlight with crisp long shadows, clean seamless backdrop, high detail, 85mm lens
```

**Негативный промпт** (Stable Diffusion, Flux, Leonardo, OpenArt):

```
glossy plastic, 3d render look, cartoon illustration, clutter, text artifacts, logos, watermark, wood grain,
cork texture, ceramic, fabric, blurry, oversaturated, extra objects, hands
```

---

## 2. Сеты целиком (как на референсах)

**Плоско сверху на чёрном, как на референсе с зелёной, красной, розовой и белой подставками**

```
Top-down flat lay of four die-cut paperboard coasters on a pure black background: a sage-green shape with three
rounded bumps on top and a grid of tiny copper foil dots, a coral-red cloud-like scalloped shape with copper
hashtag-like foil marks, a cream double-oval biscuit shape with copper waffle grid lines and a copper "bitten"
edge, a pale pink soft bow shape with thin curved copper lines. Even soft light, slight paper thickness visible,
minimal, editorial --ar 4:3 --style raw --s 150
```

**Стопки в изометрии, жёсткие тени, как на референсе с варежками**

```
Isometric view of stacks of colorful die-cut paperboard coasters on a warm off-white seamless surface,
each stack 3 to 5 coasters high with visible layered edges, shapes: a mitten-like circle with a thumb tab,
a soft cloud, a coral puddle blob, a bone, a soft four-point star. Colors: silver grey, cobalt blue, coral,
orange, lilac. Thin black circular text "Cosy Dinner" printed around the edge of the grey coaster.
Strong low sun casting crisp diagonal shadows --ar 3:4 --style raw --s 200
```

**В упаковке, как на референсе с коробкой**

```
Kraft white cardboard box with a cobalt-blue sleeve, bold condensed lilac uppercase typography "COSY DINNER
TABLE STANDS", small spec text, simple flat icons of the coaster shapes on the sleeve; beside the box the
die-cut paperboard coasters themselves scattered on a white table: lilac bellflower with a star-shaped cut-out,
pink scalloped rosette, sage leaf with a slit, cotton twine. Soft daylight, product photography --ar 4:5 --style raw
```

**Сервировка — подставки в деле**

```
Overhead shot of a dinner table setting on a linen-free pale table: a white plate resting on a large coral
puddle-shaped paperboard coaster, cutlery laid across a sage-green coaster with three bumps, a wine glass on a
silver mitten-shaped coaster with circular printed text, a small cup on a sky-blue rounded pebble coaster.
Hard afternoon sun, long crisp shadows of the glass and cutlery, minimal styling, editorial food magazine --ar 4:5
```

---

## 3. По одной форме

Шаблон: **[базовый стиль] + строка ниже + `, single object centered on a [цвет] seamless backdrop, 3/4 view, stack of [N] --ar 1:1 --style raw`**

| № | Название | Под что | Строка для промпта | Фон |
|---|---|---|---|---|
| 01 | Лужа | тарелка | `a large coral-red organic puddle-shaped coaster, soft irregular blob outline wider than a dinner plate, two thin concentric copper foil arcs` | тёплый серо-бежевый |
| 02 | Варежка | бокал | `a silver-grey mitten-shaped coaster: a circle with a small round thumb tab, black thin circular text "Cosy Dinner · Cosy Dinner" around the rim, small black check mark on the tab` | пудрово-розовый |
| 03 | Волна | приборы | `a sage-green rectangular coaster with three soft rounded bumps along the top edge, a staggered grid of tiny copper foil dots` | чёрный |
| 04 | Розетка | пиала | `a blush-pink scalloped round coaster with ten soft lobes like a porcelain jam dish, four thin curved copper lines radiating from the centre` | кобальтово-синий |
| 05 | Галька | чашка | `a sky-blue soft rounded-rectangle pebble coaster, a minimal deadpan face printed in black: two dots and two short lines` | тёплый серо-бежевый |
| 06 | Облако | горячее | `a cobalt-blue cloud-shaped trivet, thick stack, three small copper foil hash marks` | молочный |
| 07 | Печенье | соль и перец | `a cream double-oval biscuit-shaped coaster with copper waffle grid lines in each oval and a bite taken out of one edge, bitten edge covered in copper foil like a baked crust` | чёрный |
| 08 | Косточка | нож, палочки | `a small orange bone-shaped knife rest made of stacked paperboard, one thin copper line along the middle` | светлый шалфей |
| 09 | Звезда | свеча, соусник | `a lilac soft four-pointed star coaster with rounded tips, a thin copper foil circle in the centre` | горчично-жёлтый |

Дополнительные формы, если хочется больше вариантов:

- `a lilac bellflower-shaped bowl coaster with five pointed petals and a six-point star cut out in the centre`
- `a sage-green leaf-shaped knife rest with a long slit cut along the midrib`
- `a mustard cup coaster shaped like a cup seen from above: a circle with a round handle loop with a hole`
- `a pale grey ghost-shaped spoon rest with a wavy bottom edge and sleepy printed eyes`

---

## 4. Как варьировать

- **Материал:** вместо `laminated colored paperboard` — `cork`, `matte glazed ceramic, 8 mm thick`, `colored felt`, `terrazzo` (форма остаётся, меняется ощущение).
- **Свет:** `hard afternoon sunlight with crisp long shadows` (как на референсе с варежками) ↔ `soft even studio light, no shadows` (как на чёрном фоне).
- **Ракурс:** `top-down flat lay` / `isometric view` / `low 30° angle, shallow depth of field`.
- **Палитра:** перечисляйте 4–5 цветов прямо в промпте: `coral, sage, blush pink, cream, cobalt`.
- **Фольга:** `copper foil` → `gold foil`, `blind deboss (no foil)`, `black screen print`.
- Если генератор рисует лишние надписи — уберите текст из промпта и добавьте `no text` в негатив; надпись по кругу лучше потом наложить вручную.
