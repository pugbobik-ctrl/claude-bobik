---
name: photo-names
description: Put an artist's name in the melted DINNER lettering over their photo (4:5 post) for the Colorblock × DNA Dinner. Use for any photo + name overlay task in this repo.
---

# Artist name over a photo

Tools in `placecard/photo-names/`:
- `mask.py PHOTO` — person mask (rembg human segmentation) as `<stem>_mask.png` next to the photo. Run once per photo.
- `overlay.py LAYOUT.json` — renders the name and writes `out/<layout>.png` (1080×1350), `@src.png`
  (source resolution), `.svg` (editable: photo layer, name as vector paths, the person as a clipped
  photo copy on top so the name sits behind them), `.json` and `_check.png`. The layout format is in the
  file's docstring: crop in source px, lines with text / x / y (top of caps) / cap / align / rot, colour, behind.
  Lines can lie in perspective on a plane of the photo (`quad`: four corner points). `effects` makes the
  name live in the photo: `shadow` (dx, dy, blur, opacity: match the light direction in the photo),
  `texture` (0–1: the ink picks up folds and light falloff of the surface), `blur` (match depth of field),
  `grain` (match the photo's noise). The person's edge is tucked a pixel over the ink, so no fringe.

## Look (fixed, do not change)
- Lettering: Wix Madefor Display Bold, uppercase, x-stretch 0.9, melted (blur 0.10 × cap, threshold 0.27),
  tracking 0.03. First name / surname on two lines, one cap size, line gap about 0.08 × cap.
- Colours: black `#000000` on light areas, lemon `#feed95` on dark areas. Never both in one name,
  never a lemon name on a light background or black on black.

## Reading the photo
1. Find the calm, even areas (wall, sky, floor, dark sofa) and where the head and hands are
   (row/column brightness profiles plus the mask's `_check.png`).
2. The name goes in the largest calm area and stays fully on one tone: check the bottom of the letters
   against the edge where light turns dark (a sofa back, a horizon).
3. Let the person overlap the name a little (`behind: true`): one letter partly behind the head or
   shoulder reads as depth. Keep `name_hidden_by_person` under about 0.08 and never hide the first letter
   or the face.
4. Size: as large as the calm area allows. Keep the name inside 5 % margins (blue box) and inside the
   profile grid's 3:4 centre crop (green box).
5. Keep the eyes and face clear; follow the direction the person looks.

## Output
One layout JSON per idea next to the photo; review each `_check.png` and the plain `.png`. Report the
layout that works best and why, with sizes in px, and the hidden fraction.
