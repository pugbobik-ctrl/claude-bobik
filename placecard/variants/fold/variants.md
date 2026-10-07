# FOLD variants: type across folds and surfaces

Six place-card forms for the art dinner, one sheet each, black on lemon #feed95. Seat model: eye 430 mm up / 450 mm away from the card, card on the table, plate in front. All six were built as a projection model, not drawn by hand: each artist name is set as plain Wix Madefor Display Bold caps, projected from the seated eye onto the folded panels, and only then melted (blur + threshold) in the flat sheet and fitted to Bezier curves.

Everything below lives in `scratchpad/variants/fold/`.

* `final/<design>_<artist-slug>.svg` : 30 production dielines (6 designs x 5 artists), 1 unit = 1 mm, origin top-left of the flat sheet. Groups: `layer-guides` (non-printing: lemon stock swatch, safe area, panel labels), `layer-cut`, `layer-crease` (dash = valley, dash-dot = mountain, seen from the printed side), `layer-art` (melted name, filled Bezier paths, no strokes), `layer-text` (live `<text>`, font-family "Wix Madefor Text", weight 600 details / 700 lockup, size in mm, text-anchor, letter-spacing). No `perf` layer is needed. No images, clipPath, masks, filters or use. Details are 9.5 pt = 3.351 mm; lockup COLORBLOCK x DNA is 2.9 mm Bold caps, x at 85 % size.
* `final/index.json` : file, variant, artist, width_mm, height_mm, notes.
* `previews/<design>_<slug>_seat.png` and `_other.png` : perspective renders from the seat and from a second viewpoint, 1600x1000; `previews/<design>_tanya_andrianova_extra.png` and `elbow_angles_tanya.png` : extra viewpoints (picked up, from above, other side, fold angles).
* `previews/5up_<design>.png` : 5-up sheet per design (seat | second view | flat print for all five artists). `flat/*.png` : Chromium renders of the final SVGs (live text, so it proves the font mapping).
* Source: `core.py` (fonts, melt, Bezier, SVG writer), `engine.py` (fold model, projection, renderer), `v1..v6_*.py` (one per design), `export.py`, `previews.py`, `compose.py`.

## Ranking (my recommendation)

1. Ridge  2. Napkin flag  3. Crenel  4. Elbow  5. Slope  6. Bridge

Ridge ranks first because it is a three-fold prism from one sheet and the reveal is the strongest honest one: from the seat the name assembles seamlessly across the ridge, from the guest opposite the rear leaf shows the letter tops pulled into tall drips. Napkin flag is the most charming object and the name visibly continues from card to napkin. Crenel is the most spectacular from the side but is fragile and busy. Elbow is the safest. Slope is the clearest idea (picked up, the name straightens) but the weakest device. Bridge needs an extra object (mirror) and a glossy surface.

## Index

### 1. Elbow (`elbow`)
* Idea: the name wraps over a fold. The leaf stands leaning back 10 deg and the foot lies flat toward the guest; line 2 of the name crosses the hinge, so letters are cut on the fold and continue on the foot.
* Made: one sheet 132 x 116 mm, one valley fold, no glue. Name projected from the seat onto leaf and foot. Lockup on the leaf, details along the foot front edge (live text, straight).
* Risk: honest finding: it is tolerant. The name still reads at the design angle and with the leaf laid back to about 35 deg above the table (only these two poses were rendered, see `elbow_angles_tanya.png`); it only collapses when the leaf is pushed forward, and flat on the table it reads stretched. So "reads only at one angle" is a half-truth; sell it as "opens into the name". Needs stiff board (leaf has no stay).

### 2. Bridge (`bridge`)
* Idea: the name is split between the front and the back of the card; the back half is read in a mirror. Line 1 is on the shelf top, line 2 is printed on an underside flap and reads (upright, not reversed) in a mirror tile under the bridge.
* Made: one T-shaped sheet 178 x 104 mm: shelf 126 x 52 on two 26 mm legs (mountain folds), the flap folds 180 deg under the shelf. Needs a mirror tile ~180 x 120 mm (or a mirror charger) under the card; the layout assumes the card centred on it.
* Risk: highest. Depends on a supplied mirror and on the card being square to the guest; the printed reflection is projected for the 430/450 mm seat and drifts if the guest sits much higher or lower; a glossy plate gives too weak a reflection. Lemon-on-grey mirror reads dim in photos.

### 3. Slope (`slope`)
* Idea: a card that stands at an angle so the name is foreshortened into a squat melted shape, and straightens when you pick it up. The wedge descends 15 deg away from the guest; the seated eye sees the top at about half height, lifted and held up it reads true (`slope_tanya_andrianova_extra.png`). Lockup and details sit on the vertical wall facing the guest.
* Made: one sheet 140 x 270 mm, three mountain folds and a glue tab (triangular prism, 30 mm high wall, 112 mm deep).
* Risk: lowest "device" content: nothing is pre-distorted, the distortion is only the viewing angle. Prism is stable and cheap. Name is set with a looser line pitch (1.62) so the squashed lines never touch.

### 4. Crenel (`crenel`)
* Idea: an accordion in which each panel shows a slice; the whole name reads only from the seat. Six 26 mm slices step front and back by 10 mm (square-wave zigzag). From the seat the slices line up; from the side they separate and the name breaks (`previews/*_other.png`, `crenel_tanya_andrianova_extra.png`).
* Made: one strip 206 x 76 mm, ten mountain/valley folds, no glue. The name is projected slice by slice; connector strips are left blank. Details and lockup are split into live-text fragments, one per slice, so each word stays inside one panel.
* Risk: wobbly stand (needs 350 g board; add a glue dot under the end slices), and the 1 mm slivers of blank connector cut thin notches through letters. The block is shifted up to 6 mm per name to put letter gaps on the folds.

### 5. Napkin flag (`napkin-flag`)
* Idea: the name continues from the card onto the napkin band. A paper band wraps a rolled napkin (diameter 44 mm, 122 mm long); the same strip bends up into a flag. Line 1 is on the flag, line 2 runs on down over the napkin; both are projected from the seat so they read as one two-line name. Details run along the roll axis, which keeps them straight.
* Made: one strip 122 x 214 mm: flag 64 mm, one 90 deg mountain fold, band 138 mm round the roll, 12 mm overlap tab glued behind the flag.
* Risk: napkin diameter must be 44 mm +- 3 or line 2 slides off the visible arc; a soft napkin deforms. Hand-rolling is a service burden.

### 6. Ridge (`ridge`)
* Idea: a tent whose two leaves carry the top and bottom halves of the letters, which assemble at the ridge. A low gable: front leaf 76 mm at 12 deg, rear leaf 50 mm at about 18 deg. From the seat both leaves are visible; the rear leaf is seen at about 0.4, so the tops of line 1 are printed about 2.5 times too tall on it. From the opposite side the rear leaf shows the stretched tops (`ridge_tanya_andrianova_other.png`).
* Made: one sheet 132 x 258 mm, three mountain folds and a glue tab: triangular prism, 16 mm high. Lockup and details are live text on the front leaf.
* Risk: low profile (16 mm), so the card is flat and the name sits low; if the guest leans in, the join at the ridge opens slightly. The rear-leaf pitch is set by the crease, so scoring accuracy matters (not measured).

## Name refinement (all designs)

The approved melt (sigma 0.10 cap, threshold 0.27, no tracking) fuses letters once the plain text has been warped, because the warp brings letters closer: D-R-I, A-N, N-I-K, P-H-I-A, Z-H, E-E. Settings used for all 30 files: sigma 0.085 cap, threshold 0.30, plain text tracked per line:

| name | line 1 tracking | line 2 tracking | what it fixed |
|---|---|---|---|
| Tanya Andrianova | 0.025 | 0.030 | D-R-I and A-N fused; the NY pair stayed too tight at 0 |
| Igor Zotov | 0.030 | 0.025 | I-G and T-O touching |
| Andrey Lee | 0.025 | 0.040 | E-E merged into one blob, N-D |
| Sasha Chernikov | 0.025 | 0.035 | R-N-I-K one mass, A-S |
| Sophia Zhuravkova | 0.030 | 0.045 | Z-H, V-K, O-P |

Counters: D, O, R, P keep an open counter (an eroded copy of the plain counter is cut back out of the melt, so it cannot plug when the letter is stretched); the counter of A plugs completely at this weight, exactly as in the approved logo, and the pinholes that remained at small size were removed. Name block heights are capped per design (cap table below) so that two-line names with a short surname (Igor, Andrey) do not overflow the panel. Line breaks: first name / surname in all designs; in Bridge each line sits on its own surface; in Ridge the ridge cuts line 1 at 50 % of cap height; in Napkin flag the hinge sits between the lines; in Elbow the hinge crosses the middle of line 2.

Cap height of the name (mm) per design and artist:

| design | sheet (mm) | Tanya | Igor | Andrey | Sasha | Sophia |
|---|---|---|---|---|---|---|
| ridge | 132 x 258 | 11.2 | 15.5 | 15.5 | 12.9 | 10.6 |
| napkin-flag | 122 x 214 | 11.2 | 13.8 | 13.8 | 12.8 | 10.6 |
| crenel | 206 x 76 | 10.7 | 10.7 | 10.7 | 10.7 | 10.7 |
| elbow | 132 x 116 | 13.0 | 14.6 | 14.6 | 14.6 | 12.3 |
| slope | 140 x 270 | 13.3 | 25.5 | 22.2 | 15.3 | 12.6 |
| bridge | 178 x 104 | 11.6 | 12.5 | 12.5 | 12.5 | 11.0 |

## Notes and limits

* The perspective renders come from my own projection renderer (numpy/cv2): paper has no thickness, light is a single soft key, the mirror tile reflects at 92 %. Treat them as layout checks, not photographs.
* Names that are not warped (Slope) are the approved melt with only the tracking/sigma refinement above.
* The lemon colour is not in `layer-art`; it is a non-printing swatch in `layer-guides` so the stock (or a flood layer added in Illustrator) is the lemon.
* Fold directions in `layer-crease` are given as seen from the printed side; every design is printed on one side only.
