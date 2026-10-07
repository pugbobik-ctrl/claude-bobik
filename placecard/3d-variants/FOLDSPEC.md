# Fold spec: how a flat card becomes 3D

One JSON per final SVG (one card, one artist). The viewer textures the flat SVG
(art + live text, lemon board inside the closed cut outline), cuts it into panels,
folds the panels along hinges step by step and places each sheet on the table.

File: `<set>/fold3d/<svg-stem>.json`; `svg` is a file name in `<set>/final/`.

## Units and frames

- **Sheet frame**: the SVG's own mm coordinates, x right, y down (viewBox 1 unit = 1 mm).
  One SVG may hold several physical sheets (front/back stacks, card + acetate, recto/verso).
- **World frame**: mm, three.js style. **Y is up**, the table top is the plane **y = 0**.
  The guest sits on **+Z**, looking toward -Z. The card stands around the origin.
  Default eye: `[0, 430, 450]`, looking at `[0, 40, 0]` (seated eye 430 up, 450 away).
  A plate, if any, is a prop you add yourself.

## Schema

```json
{
  "svg": "e1-overhang_andrey-lee.svg",
  "title": "E1 Overhang",
  "eye": [0, 430, 450], "target": [0, 40, 0],
  "steps": ["Согнуть верхний лист назад", "Поставить домиком"],
  "sheets": [
    {
      "id": "card",
      "stock": "board",
      "back": {"front": [0, 0, 130, 68], "region": [0, 70, 130, 68]},
      "pose": {"origin": [0, 68], "at": [-65, 0, 20], "u": [1, 0, 0], "v": [0, -0.94, -0.34]},
      "step": 1,
      "panels": [
        {"id": "front", "poly": [[0,0],[130,0],[130,68],[0,68]]},
        {"id": "back", "poly": [[0,68],[130,68],[130,136],[0,136]], "holes": [],
         "parent": "front", "hinge": [[0,68],[130,68]], "angle": -120, "step": 2}
      ]
    }
  ],
  "props": [
    {"type": "plate", "r": 135, "at": [0, 0, -150]},
    {"type": "box", "size": [200, 32, 32], "at": [0, 16, 60], "material": "acrylic", "rotY": 0},
    {"type": "cylinder", "r": 22, "h": 300, "at": [0, 22, 80], "axis": "x", "material": "napkin"},
    {"type": "mirror", "size": [180, 120], "at": [0, 0.5, 40]}
  ]
}
```

### sheets[]
- `stock`: `board` (lemon board: the texture is lemon inside the closed cut outline, art on top)
  or `acetate` (clear film: only the printed art is drawn, the rest is transparent).
- `back` (optional): the part of the SVG printed on side 2. `front` is this sheet's region
  `[x, y, w, h]`, and `region` is the side-2 artwork. Side 2 is drawn *as seen from the back*
  (the sheet is turned over about its vertical axis): point (x, y) of `front` shows, from
  behind, the side-2 point (`region.x + front.w - (x - front.x)`, `region.y + y - front.y`).
  Without `back`, side 2 is plain lemon (or clear for acetate).
- `pose`: final placement of the **root panel** (the one with no parent):
  `world = at + (x - origin.x) * u + (y - origin.y) * v`, with `u`, `v` unit vectors for
  sheet +x and sheet +y. The printed face points along **v × u**.
  - Flat on the table, printed side up, top edge away from the guest: `u = [1,0,0]`, `v = [0,0,1]`.
  - Upright, facing the guest: `u = [1,0,0]`, `v = [0,-1,0]`.
  - Leaning back (top away from the guest) by angle a from upright: `v = [0, -cos a, +sin a]`.
- `step`: the step during which the sheet moves from lying flat to its pose (default 1).
- `flat` (optional): `{"at": [X, Y, Z]}`, where sheet (0,0) lies before assembly
  (default: sheets laid out in a row behind the scene).

### panels[]
- `poly`: outline in sheet mm, any winding, can be concave and long (a melted letter outline
  is fine). `holes`: optional list of polygons cut out of it (windows, the hole a pop-up leaves).
  Panels of one sheet tile it along the crease lines; they must not overlap.
  The closed cut outline in the texture clips the panels too, so for a plain rectangle sheet
  with an odd silhouette a band polygon is enough; for pieces separated by open cuts
  (pop-up letters, notches) give the exact outline.
- `parent`, `hinge`: the child turns about the segment `hinge` (two sheet points, on the
  shared edge). Exactly one panel per sheet has no parent (the root).
- `angle`: fold angle in degrees at the end of assembly, relative to the parent.
  **Positive = valley seen from the printed side** (the printed faces close toward each
  other), negative = mountain. 180 = folded flat onto the printed face.
- `step`: the step during which this fold goes from 0 to `angle` (default 1).
- A curved bend (arch, roll) is a run of narrow strips (3–6 mm) chained parent to child,
  each with a small angle, so the strips add up to the curve.

### props[]
`plate` (disc on the table, `r`, `at` centre), `box` (`size` [x, y, z], `at` centre, `rotY`
degrees), `cylinder` (`r`, `h`, `at` centre, `axis` x|y|z), `mirror` (a mirror tile flat on
the table, `size` [x, z], `at` centre; reflects the scene). Materials: `acrylic`, `glass`,
`pet`, `napkin`, `plate`, `wood`, `mirror`.

### steps[]
One short Russian caption per step (step 1 = `steps[0]`). Step 0 is the flat sheet.

## Tools

- `python3 tools/check_spec.py SPEC.json`: schema, tree, hinges on panel edges, overlaps.
- `node tools/shot.cjs SPEC.json OUT.png [--t=STEP] [--view=seat|front|side|top|orbit]`:
  a screenshot from the viewer. `--t` may be fractional (1.5 = halfway through step 2);
  the default is fully assembled.
