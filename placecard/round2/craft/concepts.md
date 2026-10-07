# Dinner place card, Colorblock x DNA Kitchen, Moscow, 10 Oct 2026: six crafted concepts

Sample name on every drawing: Sophia Zhuravkova. All type is Wix Madefor Text, printed black on lemon (#feed95, to be matched by drawdown). SVG units are mm. Every concept has `cN_dieline.svg`, `cN_assembled.svg`, PNGs in `png/`, and `cN_verify.txt` with the computed geometry. The generator is `cN*.py`. Folder: `/tmp/claude-0/-home-user-claude-bobik/6a3dcf92-132a-5018-88ad-a2068c46056a/scratchpad/round2/craft/`.

Scores: risk 1 (safe) to 5 (needs a prototype to know it works). Delight 1 to 5. Cost level is per card for about 40 guests, materials plus hand labour.

| # | Name | The trick | Risk | Delight | Cost | Rank |
|---|------|-----------|------|---------|------|------|
| 01 | Kosode | origata-style wrap round the napkin; untie the cord, lift the V-flap, the name is on its lining | 2 | 4 | low | 1 |
| 05 | Flag Up | pulling the napkin toward the lap pulls a tab; the name flag stands up out of a black pit, a latch clicks, the tab tears free | 4 | 5 | medium-high (labour) | 2 |
| 06 | Walk-By | a pleated agamograph strip: you read "Dinner" walking up the table, your name when you arrive | 3 | 4 | medium | 3 |
| 04 | Raking Light | name is tone-on-tone relief (vertical ridges on a horizontal-ridge ground), readable only in low side light | 3 | 4 | high | 4 |
| 02 | Lantern Lattice | knife-cut brick lattice cylinder; press it and 32 pre-creased ribbons kink out into a double barrel; name on the belt | 3 | 4 | medium | 5 |
| 03 | One Thread | 4-page book sewn with one thread; the thread's tails are the napkin ring and the bow | 1 | 3 | low materials, labour 3 min | 6 |

Recommendation: make 01 the baseline (cheap, napkin-integrated, hard to get wrong) and prototype 05 in parallel for a week as the showpiece. If 05 passes, use 05 for the head table and 01 for the rest, or the reverse for budget. 06 is the best "only at this dinner" idea after 05 but needs scoring precision. 04 is the most refined but depends on lighting and on one plate per name.

Not selected, kept in reserve: hexaflexagon (nice but the guest is busy flipping a card at a dinner table, and printing the name on 3 faces needs a template per guest); a bread-obi with a tear strip (food contact and glassine liner needed).

---

## 01 Kosode: origata-style wrap, name under the V-flap

Files: `c1_dieline.svg`, `c1_assembled.svg`, `c1_verify.txt`, `c1_sim.py`, `c1_draw.py`.

Guest experience. A lemon packet with a cord bow lies on the setting; the front reads only "Dinner | 10.10.2026" either side of the cord. Pull the bow, lift the V-shaped flap (hinged away from you) and the name is printed upright on its lining, with the event line under it. The napkin is inside, so unwrapping is also taking the napkin. The cord goes back round as a napkin band.

Construction. One 200 x 200 mm square, folded corner-up, valley folds only, no cuts, no glue:
1. Bottom corner up along y = -41 (pack lower edge, counting half the 12 mm thickness).
2. Right corner in along the line from the shoulder (63.0, 78.4) to (66, -41).
3. Left corner in along the mirror line, over the right (left-over-right, migi-mae). Lapel tips land 11.4 mm past the centre line, so they overlap 22.7 mm.
4. Apex down along y = 79.9; its tip lands at y = 18.4 and covers the upper pack.
5. 2 mm black waxed cotton cord round the short way, bow on the flap (cut 400 mm).
The napkin is folded to a flat 120 x 70 x 12 pack. Print is on the lining only (name, event line); optional duplex adds "Dinner / date" on the flap outside.

Checked by computation (`c1_verify.txt`): folded-layer simulation with convex polygon clipping and reflection; 99.7 % of the pack footprint (inset 1.5 mm) is under a layer. The 0.3 % is two small slivers at the top V-corners, about 4 mm, where the linen can peek. The lapel layers top out 1.5 mm below the apex crease so the apex folds over nothing. "Zhuravkova" (67.5 mm at 12 mm SemiBold) clears the sheet edge by 6.3 mm per side; "Sophia" by 6 mm.

Materials. 135 g lemon text paper (Colorplan Citrine or equivalent), hard enough to hold a crisp valley, thin enough to wrap 12 mm. This is paper, not card: the brief's "lemon card" is met by a 135 g sheet, and a 170 g sheet still folds if you score. Black waxed cotton cord 2 mm.
Size: 200 x 200 flat; closed 132 x 123 x ~14 mm.
Production. Digital or offset 1 colour (plus optional back print), guillotine to square, hand score or crease-wheel the four lines, hand fold 40 s. 4 sheets per SRA3.
Cost level: low (about 1.5 to 2.5 per card plus 40 s labour). Risk 2 (cord holds the flap, napkin size varies: the sheet scales, see the crease offsets). Delight 4.

## 05 Flag Up: napkin-triggered pull-tab pop-up

Files: `c5_dieline.svg`, `c5_assembled.svg`, `c5_verify.txt`, `c5.py`.

Guest experience. A flat lemon card lies by the plate with a lemon tail running out of its front edge under the folded napkin, the napkin's rolled corner threaded through a slot in the tail. Lift the napkin toward your lap: the card's name flag, which was lying flat in the card, stands up out of a black pit to 78 deg, a latch clicks, and the tail tears off with the napkin. The person opposite sees "Dinner" on the flag's back.

Construction (4 parts, 1.7 mm card total).
- A top card 124 x 88, 350 g: the flag (100 x 50) is cut out of it as a U-cut, hinged at y = 20 (valley score). A 3 x 3 latch window in the front lip at y = 8..11.
- C spacer 124 x 88, 0.9 mm board: window = flag outline, plus a 12.6 mm channel from the window to the guest edge. The window's front edge (y = 20) is the stroke stop.
- B base 124 x 88, 350 g: solid black pit under the window (bleed 1 mm under C).
- D one strip, 12 wide, 183 long: tab 8 glued to the flag back at y = 27..35; P hinge at y = 35; leg 30; F fold 180 deg; slider 65 to the guest edge; 20 mm out then a perforation; 60 mm tail with a 10 x 3 napkin slot. Shoulder 16 x 6 on the slider at 29.3 mm from the foot; latch tongue 5 x 3 at 41.3 mm.
Geometry and results are in `c5_verify.txt`: with hinge-to-pivot a = 15 and leg l = 30 the foot moves from y = 65 to y = 49.3 as the flag goes 0 to 78 deg, a stroke of 15.7 mm. The shoulder meets the channel mouth exactly there (49.29 - 29.29 = 20), so the stop is built into the cut. Without the stop the flag would carry on to 90 deg and fall toward the guest; the stop is mandatory. The leg crosses the card plane inside the window, so nothing collides with the lip.
Estimates, not tested: pull to erect 0.1 to 0.3 N; perforation tear 1.0 to 1.5 N; latch holds more than 2 N. The order erect, latch, tear is then enforced by those margins. This is the risk: friction in the channel, crease spring-back and the napkin's grip on the tail are all guesses until a hand prototype exists.
Materials: 350 g lemon board (2 sheets), 0.9 mm board for C, 350 g for D, PVA or double-sided tape. SRA3: 10 per sheet per layer, 4 sheets per layer for 40.
Production. Digital print (flag front, flag back, black pit), flatbed knife cutter with crease wheel, hand assembly 10 to 12 min.
Cost level: medium-high (labour). Risk 4. Delight 5.

## 06 Walk-By: pleated agamograph, name for the seat, "Dinner" for the walker

Files: `c6_dieline.svg`, `c6_assembled.svg`, `c6_verify.txt`, `c6.py`.

Guest experience. The place card is a pleated strip on a small tent card. Walking up the table you see "Dinner" on every card; two or three seats away the cards shimmer, and at your own seat your name resolves. Flipping from one image to the other is the whole effect.

Construction. A strip of 13 teeth. Facet A, 9.0 mm, rises +18 deg from the plane and faces the seat; facet B, 2.96 mm, falls -70 deg and faces the walker. Planarity needs a sin(alpha) = b sin(beta), which gives b = 2.960 and a closure of 0.00 mm (verified). Pitch 9.57 mm, panel 124.4 mm, tooth depth 2.78 mm. The print file interleaves 13 slices of the name image (pre-stretched 1/cos 18 deg) with 13 slices of the "Dinner" image. B ink is confined to the top 12 mm and bottom 6 mm of the 34 mm strip, so at the seat angle B only adds slivers above and below the name, never through it (see the 0 deg row of `c6_assembled.png`). 26 vertical creases: valley B|A, mountain A|B. Two 8 mm tabs go through slits in the tent card's front panel and fold flat behind. Tent card 136 x 100, 300 g, 50 mm panels, 40 deg apex.

Checked by computation (`c6_verify.txt`, simulated for five angles in `c6_assembled.png`): B share of the visible area is 1 % at -18 deg, 11 % at 0, 31 % at 35, 90 % at 70 deg. "Dinner" is clean from about 70 deg, which for a walker at 0.9 m lateral distance means 2.5 m along the table, so it reads two or three places away. The honest limit: the name is clean only at theta of 3 deg or less (readable to 26 deg), so the tent should be turned about 15 deg toward the walker, and the shimmer zone is gibberish by design. The B strip is 2.96 mm, so a 0.3 mm score error moves 10 % of it: score with registration ticks, not by hand.
Materials: 200 g lemon for the strip, 300 g lemon for the tent. Production: digital print of interleaved art, crease wheel, hand pleating on a jig (4 min). Cost level medium. Risk 3. Delight 4.

## 04 Raking Light: tone-on-tone relief name

Files: `c4_dieline.svg`, `c4_assembled.svg`, `c4_verify.txt`, `c4.py`, `png/c4_sim_*.png`.

Guest experience. A thick lemon slab that says only "Dinner" and the date in black. Hold it low against a candle and "Sophia Zhuravkova" lights up in corduroy against velvet; turn it 90 deg and the name goes dark. Under room light or a flash it disappears.

Construction. 118 x 64 x 1.4 mm board, corner radius 3. Front relief: a ground of horizontal ridges (pitch 0.5, depth 0.2, triangle profile, flank 38.7 deg), the name in vertical ridges of the same pitch (Wix Madefor Bold 16 mm; "Zhuravkova" 91.3 mm, stem 2.6 mm, about 5 periods). Black plate: "Dinner", date, event line, and an "S.Zh." find-aid so the seat is findable in daylight. Back plain, or the name in plain ink as a fallback.

Checked by computation: Lambert simulation of the actual height field (16 px/mm, gradient normals). Mean brightness letters vs ground: diffuse +0 %, lamp 15 deg from the left +43 %, from the far edge -30 %. Contrast falls to +18 % at 25 deg lamp elevation, +4 % at 35 deg, 0 above that: it only works with a low lamp (candle height), which fits a dinner table but not a bright overhead. The cross-section in `c4_assembled.png` is true scale.
Production. Photopolymer relief plate per guest, blind impression 0.2 mm on 1.4 mm cotton-rich board, 8 names ganged per A4 plate (5 plates), black letterpress or digital first, die-cut after. Cost level: high (plates, 1.4 mm board, make-ready). Risk 3 (lighting, plate fidelity at 0.5 pitch). Delight 4.

## 02 Lantern Lattice: kirigami cylinder

Files: `c2_dieline.svg`, `c2_assembled.svg`, `c2_verify.txt`, `c2.py`.

Guest experience. A lemon ring on the table with the name on a belt, facing you and the person across. Press the belt down 7 mm and a double barrel of paper ribbons buckles outward, with a tealight (LED) glowing through the lattice.

Construction. One strip 194 x 78, 350 g. Ring circumference 170 mm (54 mm diameter) closed with two belt tongues and one foot tongue through slots. Rows (top down): belt 22 | 4 | slit row A 18 | 4 | slit row B 18 | 4 | foot 8. Each row has 16 ribbons, 10.625 mm wide, from zero-width knife slits; row B is offset half a pitch (brick lattice). Each ribbon has one mountain crease at its middle, 32 in all.
Checked by computation: kinked ribbon, 9 mm segments, 5 mm outward sagitta, chord 14.97 so each row loses 3.03 mm; lantern 78 mm becomes 71.9 mm; belt radius 27.06 and bulge radius 32.06, so the circumference at the bulge (201.4) exceeds the ribbons' sum (170.0) and 1.96 mm gaps open between neighbours. Name set at 8 mm over a 95 deg arc of the belt (foreshortened to cos 47 = 0.67 at the ends).
Uncertain: ribbons splaying while their ends are held in the continuous bridge bands is a twist the paper must do; and whether the pressed state is stable or springs back to nearly straight depends on the crease and board. Prototype before committing.
Materials: 350 g lemon board. Production: flatbed digital cutter with oscillating knife and crease wheel (no tooling), 8 per SRA3, assembly 30 s. Cost level: medium. Risk 3. Delight 4.

## 03 One Thread: sewn book that becomes the napkin ring

Files: `c3_dieline.svg`, `c3_assembled.svg`, `c3_verify.txt`, `c3.py`.

Guest experience. A tiny 52 x 80 mm book is tied to the rolled napkin with a bow; the only thread is the one that binds the pages. Untie, open: Moscow / date on the left, name on the right. The two tails stay as the napkin ring.

Construction. One 104 x 80 sheet, 300 g, scored once; three pierced holes on the fold at 12, 40, 68 (0.9, 1.3, 0.9 mm). 3-hole pamphlet stitch worked from the outside: tail A in at H2, inside run to H1, out; long stitch H1 to H3 on the spine outside; in at H3, inside run back to H2, out as tail B; both tails leave H2 on the outside either side of the long stitch. Thread 0.6 mm waxed linen, black.
Checked by computation: thread in the book 112 mm + passes; belt round a 42 mm roll with the 2.2 mm book 146 mm; bow 134; total about 398, cut 500 mm for knot and a spare turn. "Zhuravkova" 42.8 mm at 7.6 mm on a 52 mm page (4.6 mm each side).
Materials: 300 g lemon, waxed linen thread. Production: digital print, score, pierce on the fold, sew by hand 2 to 3 min; 15 sheets per SRA3. Cost level: low materials, labour 3 min. Risk 1. Delight 3 (lovely and safe, but no surprise beyond the book itself).
