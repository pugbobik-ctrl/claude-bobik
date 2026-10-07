# Light, shadow, motion, balance, perception: six place cards for "Dinner"

Colorblock x DNA Kitchen, Moscow, 10 Oct 2026. Lemon card #feed95, black print, Wix Madefor Text. Sample guest: **Sophia Zhuravkova**.
Nothing here echoes the poster's melted lettering: type is set plain; the surprise comes from physics.

All geometry is code (numpy/shapely/OpenCV; code in this folder). Sketch = `out/cNN_sketch.svg` (+ `.png`). Assumed scene: bare bulb 300 mm above the table; eye 430 mm up, 450 mm from the card; plate 270 mm; lamp on the table centreline about 450 mm beyond the card (a table about 1.3 m wide, or lamps staggered; see the risk on concept 1).

## Ranking

| # | Concept | Effect | Risk | Delight | Proven by |
|---|---|---|---|---|---|
| 1 | **Under the Lamp** | your name appears as light on your plate | 4 | 5 | shadow ray-trace of the real cut file, 12 stress cases |
| 2 | **Slip** | a screen slid by half a millimetre flips the name light/dark | 3 | 4 | composited line pattern, contrast curves |
| 3 | **Rim Walker** | name panel perched on a glass rim, held by a coin hanging inside | 3 | 4 | CoM, potential well, ring-down ODE |
| 4 | **Seat-Lock** | the name assembles only from your seat | 2 | 4 | ray-cast render from 9 viewpoints |
| 5 | **Spin Plate** | roll a skewer: empty place setting + name fuse | 3 | 4 | 3D persistence simulation |
| 6 | **Lemon Cradle** | name rocks like a see-saw, self-righting | 1 | 3 | nonlinear rolling ODE |

If the client wants zero surprise on the night: **Slip** (self-contained, no dependence on room lamps or glassware).
If they want the one people talk about: **Under the Lamp**, with a pre-event bulb/marker check.

---

## 1. Under the Lamp (risk 4, delight 5)

**Guest sees / does.** A 223 x 84 mm lemon screen stands behind the plate. Its cut-outs read as an upside-down, stretched, abstract lace. The table lamp throws a dark shadow trapezoid across the plate, and inside it, in light, **Sophia / Zhuravkova** upright. Small black band at the foot gives name + table/seat so the card still works in the dark.

**Physics.** Holes at card height z project through the bulb to depth Y = D z/(H-z), widths scaled x*H/(H-z) (D = 450 lamp distance, H = 300). The cut is the exact projective inverse: text on a picture plane perpendicular to the sight line -> table via the eye ray -> card via the lamp ray (forward-mapped vector outlines, so it is exact, not resampled). Because the shadow falls toward the guest, the card pattern is flipped top-to-bottom. Stencil bridges added for the o, p, a counters (min web 0.9-1.0 mm; slivers < 0.8 mm removed).

**Proof (`out/c1_view_hero.png`, `c1_matrix.png`, `c1_scores.json`).** Ray-traced with an extended bulb (160 samples), cosine/inverse-square lighting, 10 % ambient, card drawn as an occluder. Correlation of the seat-rectified shadow with the ideal text (as placed / after allowing a viewer's stretch-shear):
- 8 mm LED capsule 0.96/0.96; **clear filament 25 mm 0.93/0.93 (hero)**; opal globe 45 mm 0.87/0.88; opal globe 80 mm 0.73/0.75 (blurry, fails).
- Card re-cut for a lamp 300 mm / 600 mm sideways: 0.85 / 0.73 (readable, but blur grows with the grazing angle).
- Lamp 60 mm off its mark sideways: reads, italic (0.34 placed, 0.90 tolerant). 120 mm: 0.81 tolerant. 100 mm nearer: squashed (0.71). **200 mm farther: fails (0.32)**. Bulb 30 mm lower: 0.77. Neighbour lamp 900 mm away adds a faint ghost, still 0.89.
- Rotating the card to face an off-axis lamp does NOT help (text rotates with it): the file must be cut per seat.

**Materials / production.** 350 gsm lemon board, laser or plotter cut, 2 slot-in cross feet (90 x 26). Per-seat file from the floor plan (lamp x, y) by script, ~1 min compute per guest. Print: black band only (offset or digital), name small. Need: tape marks for each lamp base, clear filament or LED bulbs <= 25 mm (we supply, ~10 bulbs). Cost low; assembly 20 s.

**Risk (4).** Everything depends on lamp position (+-60 mm), bulb size, and the plate sitting where drawn. Mitigations: our own bulbs and floor marks, test with the real lamps on the recce, fallback = the card is still legible by its black band.

---

## 2. Slip (risk 3, delight 4)

**Guest sees / does.** A lemon sleeve with a window full of fine vertical lines. Pull the tab a hair: the name flashes in **lemon on black**; keep sliding 0.6 mm and it flips to **black on lemon**; halfway it vanishes. Slide continuously and the whole window shimmers (Riley / Cruz-Diez).

**Physics.** Base print: background lines on a 1.2 mm pitch; letter areas use the same lines shifted half a pitch. Screen (clear PET with 0.6 mm opaque bars, same pitch) passes one phase at a time; shifting by p/2 swaps them.

**Proof (`out/c6_*.png`, `c6_results.json`).** Composited at 20 px/mm with dot gain and eye blur. Name contrast +0.83 at slide 0, -0.83 at 0.6 mm (printed black on lemon alone is 0.89), 0.00 in between. Dot gain 0.12 mm still gives 0.76. Skew between screen and print: 0.4 deg keeps 0.73, 0.8 deg ~0.25, 1 deg fails; the sleeve rails (0.3 mm clearance over 150 mm) give 0.1 deg.

**Materials / size.** Sleeve 124 x 100 mm lemon 300 gsm with window + rails; base print 170 x 76; screen 158 x 68 clear matt PET (the only non-paper part; a laser-cut lemon comb would need 0.6 mm bars: too fragile). Offset press at 2400 dpi / 1.2 mm pitch; registration only needs parallelism, not position. Assembly ~2 min.

**Risk (3).** Screen skew/bowing and a printer who rounds 0.6 mm lines; cheap fix = test sheet.

---

## 3. Rim Walker (risk 3, delight 4)

**Guest sees / does.** A 90 x 45 mm name panel stands on a strip laid over the rim of the wine glass; a 1-rouble coin hangs in a card pocket inside the glass. The panel nods and wobbles for ~4 s when touched, never falls, and the coin is visible in the glass (the "raisin").

**Physics.** Knife-edge pivot at the rim; stable iff the centre of mass is below the pivot. Computed from the real masses (300 gsm): total 4.9 g, **CoM 15 mm below the rim, 0.0 mm off-axis**, pitch period 0.58 s. Potential well and 22-deg ring-down in `out/c3_physics.png`. Without the coin the CoM is 12 mm above the pivot and the panel tips off.

**Sensitivity (honest).** Equilibrium tilt = atan(x_cm/d): a 2 / 5 / 10 RUB coin in the same pocket leans the panel 11 / 13 / 12 deg (still stable); card 250 / 350 gsm shifts the lean +5 / -6 deg; sliding the coin 1 mm in its pocket trims ~2.5 deg. Design makes the trim a guest game.

**Materials / production.** One piece lemon 300 gsm (panel, 10 mm strip with ridge fold, tail, glue-up coin pocket) + coin we supply (3.2 g). Hand fold 40 s.

**Risk (3).** Glass shape varies (rim diameter, lips); coin must be removed before pouring (it hangs 15-45 mm below the rim, above a normal pour but the bottle needs a free rim); clinking noise.

---

## 4. Seat-Lock (risk 2, delight 4)

**Guest sees / does.** Three lemon flats in a slotted base, 47 and 29 mm apart. From any other angle they show shredded half-letters. Sit down: the slices align into **Sophia / Zhuravkova**. Lean 60 mm and the name tears again.

**Physics.** Anamorphic slicing. Each card's visible band ends where the sight line over the card in front reaches it, so bands tile; ink = (text AND band k) projected from the eye onto card plane k (exact vector projection). Spacings solved from the eye ray through the card tops.

**Proof (`out/c2_view_*.png`, `c2_sketch.png`).** Ray-cast from the seat (clean), +-30 mm head shift (ripple), 60 mm (broken), neighbour 650 mm (scrambled), across the table (blank backs), standing, table end. Head tolerance ~+-30 mm.

**Materials.** Three cards 170 x 62 + 8 mm tabs, base 186 x 120 with 6 slits, lemon 300 gsm. Pure print + die cut, flat-packed; staff assemble in 30 s. Small readable ID at the foot of the front card.

**Risk (2).** Guests who pull their chair in or sit sideways see slightly torn names (part of the joke); seat geometry assumed fixed.

---

## 5. Spin Plate (risk 3, delight 4)

**Guest sees / does.** Ø110 mm disc on a skewer in two V-cradles. At rest: an empty place setting (plate, fork, knife). Roll the skewer between your palms: your name and "No 7" appear on the plate.

**Physics.** Thaumatrope: skewer 3 mm, palms sliding 10 cm/s gives omega = 67 rad/s ~ 10 turns/s, 20 swaps/s > flicker fusion. Side B is printed upside-down so it flips upright; perceived image = temporal average (ink on one side reads 50 %).

**Proof (`out/c5_spin_seat.png`, `c5_fused_ideal.png`).** 3D simulation from the seat, 180 phases per turn including edge-on. Result reads but is weak: **name stroke contrast ~17 %** (static print is 89 %); ring and cutlery smear vertically because the axis runs along the text. Bold type (cap 7.2 mm, +0.3 mm embolden) helps.

**Materials.** Two discs 300 gsm printed one side, bamboo skewer, 2 V-cradles; ~2 min assembly.

**Risk (3).** Low contrast, guests who spin too slowly or too fast; only works when you actively do it.

---

## 6. Lemon Cradle (risk 1, delight 3)

**Guest sees / does.** A lemon-wedge half-cylinder 150 x 90 x 45 mm with the name on its flat deck. Flick it: it rocks toward and away, nodding the name at you for ~6 s, never tipping.

**Physics.** Rolling rocker, radius R = 45. CoM depth a below the centre of curvature: stable for any a > 0; restoring torque M g a sin(theta); T = 2 pi sqrt((I_cm + M (R-a)^2)/(M g a)). Paper only: 14.2 g, a = 17.9 mm, T = 0.63 s. With 2 two-rouble coins under the deck: 24.4 g, a = 10.4 mm, T = 0.86 s (floatier). Full nonlinear rolling Lagrangian in `out/c4_physics.png`.

**Materials.** One strip (deck + shell + tab, 241 x 150) + 2 laminated end caps (600 gsm) printed with black wedge segments; hand assembly 3 min, rounded shell needs scoring every 14 mm.

**Risk (1).** Cannot fail physically; only risk is that it is "a nice paper toy", plus assembly time and table footprint.

---

## Files

Sketches: `out/c1_sketch.svg` ... `out/c6_sketch.svg` (and .png). Simulations: `c1_view_hero.png`, `c1_matrix.png`, `c2_view_*.png`, `c3_physics.png`, `c4_physics.png`, `c5_spin_seat.png`, `c6_s*.png`, `c6_physics.png`. Code: `common.py`, `c1_*.py` ... `c6*.py`, `render.js` (SVG to PNG via Chromium).
