# Place card, round 2: twelve concepts with an изюминка

Dinner, Colorblock x DNA Kitchen, Moscow, 10 Oct 2026. Black on lemon (#feed95), Wix Madefor Text. Guest used in every sketch: Sophia Zhuravkova.
Each sketch is `svg/NN_name.svg` with its render in `png/NN_name.png`. Computations are in `src/` (Python) and their outputs in `calc/`. Render script: `render.js` (playwright + Chromium).

Ratings: **F** = feasibility 1 to 5 (5 = easy, safe), **D** = delight 1 to 5.

## Ranking

| # | Concept | F | D | One line |
|---|---|---|---|---|
| 1 | 07 SKIRT | 4 | 5 | Flat spiral disc becomes a spiral lampshade on the glass stem, name running down it |
| 2 | 03 DECODER RING | 3 | 5 | Mirror napkin ring decodes a swoosh of calligraphy into the name |
| 3 | 02 SIT DOWN | 5 | 4 | V-fold card whose name only assembles from your own seat |
| 4 | 11 JACK | 4 | 4 | Lift the napkin, a rubber-band card pops up |
| 5 | 01 LIT | 2 | 5 | The lamp throws the name onto your plate through a stencil card |
| wild card | 09 BLACK TO COLOUR | 2 | 5 | A black bar separates into colour blocks over the evening: Colorblock as a chemical clock |

Most unexpected (as asked, more than 3): 01 Lit, 03 Decoder Ring, 02 Sit Down, 09 Black to Colour, 12 Pour.

## Assumptions used in the computations
Table lamp: bulb centre 300 mm above the cloth. Guest eye: 430 mm above the cloth, 450 mm horizontal from the object. Plate: 270 mm, surface at 12 mm. Letters are always Wix Madefor Text 700.

---

## 01 LIT (`svg/01_lit.svg`)
**Guest:** A lemon card stands between the lamp and the plate. Its face shows a squashed, upside-down stencil, nothing readable. The lamp is on, and a patch of shadow on the plate has the name lit inside it.
**Mechanism:** A card (96 x 124 mm) stands 195 mm from the lamp axis. The name is cut as stencil holes in a band at 85 to 114 mm height. Each hole is the central projection from the bulb onto the plate plane, so the card shows a vertically flipped, 0.7x narrow version, and the plate gets the correct one. Every counter is held by a 1.5 mm bridge (checked by connected-component test: no islands).
**Proof:** `src/c01_calc.py`, `src/c01_build.py`. Ray-traced top views in `calc/c01_shadow_*.png`: point source reads, 5 mm LED filament bulb reads, 25 mm opal bulb does not (blur about 6 mm). Sensitivity: bulb 30 mm lower moves the text 15 mm toward the guest; lamp 25 mm sideways moves it 11 mm; so every lamp must be placed on a mark.
**Materials:** 300 gsm lemon card, slotted foot piece, and supplied LED filament bulbs (clear, 4 to 5 mm source). **Size:** 96 x 124 + foot 96 x 50. **Production:** laser cut (stencil bridges too fine for a steel rule die), digital print.
**F 2:** the lamp bulb is outside the designer's control, and placement tolerance is 10 mm. **D 5:** the one idea where the room itself does the trick.

## 02 SIT DOWN (`svg/02_sit_down.svg`)
**Guest:** A winged lemon V stands by the plate. Walking up you see fragments; sitting down, the two leaves snap into one flat banner with the full name.
**Mechanism:** Two 82 mm leaves open 90 degrees toward the guest. Print is computed by casting rays from the seat eye through the flat name onto each leaf (stretch 1.4x). Top edge rises from 38 to 88 mm so the apparent top is level. From 330 mm to the side one leaf turns edge-on and the other shears.
**Proof:** `src/c02_calc.py`: four ray-cast renders (seat, next seat, walking past, across the table) in the sketch. The first stair-step version I tried read from everywhere, so I dropped it.
**Materials:** one sheet 300 gsm lemon. **Size:** 164 x 88 mm flat, 113 mm wide standing. **Production:** digital print + die cut + one score, no glue. Back (seen from across) carries the seat number.
**F 5, D 4:** a graphic trick that needs no object, only a pre-warped print file; the client needs a seat-to-eye diagram per table. Risk: guests who lean change the reading; mild.

## 03 DECODER RING (`svg/03_decoder_ring.svg`)
**Guest:** A lemon card with an abstract fan of calligraphic swoops. A mirror-board napkin ring comes rolled in the napkin. Put it on the card and the name appears in the metal.
**Mechanism:** Cylindrical anamorphosis. The ring (r 26, h 50) reflects the eye ray from 430 up and 450 away onto the card; the print is the preimage of the name (1500 x 500 rays). Letters land 34 mm (bottom) to 72 mm (top) in front of the ring.
**Proof:** `src/c03_calc.py`: print generated, then a separate ray-trace of the finished print in the mirror reads "Sophia Zhuravkova" (see sketch). From the next seat it is displaced, so the card also works as a seat check.
**Materials:** mirror PET board (metallised) on card, or mirror-chrome laminate; lemon card 160 x 130. **Production:** die cut, print, ring is a strip with tab and slot.
**F 3:** cap height is only 5.7 mm in the mirror and mirror board scratches; sample first. **D 5:** transformation by an object the guest already holds. **Flag:** the stretched swooping letters are typographic distortion, not the melted blobs of the poster, but a nervous client may read them as an echo. The 02 and 03 cards can share one file.

## 04 CHEERS (`svg/04_cheers.svg`)
**Guest:** A black sleeve on a lemon card. A tab sticks out. Pull it in small strokes and two glasses on the card approach and clink with sparks, in a loop.
**Mechanism:** Scanimation: three frames interlaced in 0.7 mm slices under a black card with 0.7 mm slits (pitch 2.1). Sliding 0.7 mm shows the next frame.
**Proof:** `src/c04_calc.py`: frames composed column by column and blurred as the eye does: frame 1, 2, 3 in the sketch. The picture reads but the ground goes dark olive (a lemon barrier would invert the contrast and read as stripes, which I tested and dropped).
**Materials:** lemon card, black card sleeve. **Size:** 100 x 80. **Production:** laser cut slits, print registered to 0.1 mm.
**F 3:** registration at 0.7 mm. **D 4:** a toy that plays itself on the table, but small and dim in candle light.

## 05 SPIN (`svg/05_spin.svg`)
**Guest:** A lemon disc on two thread loops hangs from the glass stem. One side is an empty plate with knife and fork, the other your name. Roll the threads and the name settles on the plate.
**Mechanism:** Thaumatrope: side B printed upside-down (flip about the thread axis), 12 turns per second for persistence of vision.
**Materials:** 400 gsm card, black thread. **Size:** 70 mm disc. **Production:** digital print both sides, punch.
**F 5, D 3:** every guest knows it from childhood, pleasant but not new; works as a quiet add-on to another idea.

## 06 THREE FACES (`svg/06_three_faces.svg`)
**Guest:** A lemon hexagon the size of a coaster. Pinch and flex: name and seat, the menu, then the evening and the date.
**Mechanism:** Trihexaflexagon: strip of 10 equilateral triangles (45 mm side), both sides printed.
**Materials:** 350 gsm card. **Production:** print, score, die cut, one glue tab.
**F 4:** the face layout on the strip follows the standard template, which I have not re-derived here, so mock up in white paper first. **D 4:** the programme is the object, and guests share it. A flexagon is a known genre, so less surprising than 01 to 03.

## 07 SKIRT (`svg/07_skirt.svg`)
**Guest:** A flat lemon disc under the napkin with a name winding in a spiral. Lift it by its centre, clip it on the wine glass stem: the turns fall apart into a conical spiral lampshade 92 mm tall, name running round it 17 times.
**Mechanism:** Laser-cut Archimedean spiral (r 9 to 81, pitch 12, 6 turns, 1.6 m ribbon). The helix is drawn to scale in the sketch with letters placed in 3D on the front-facing ribbon.
**Materials:** 300 gsm lemon card, keyhole for the stem. **Size:** 160 mm disc. **Production:** laser or steel-rule die; print text along the spiral.
**F 4:** must test that the turns hang evenly (heavier card = stiffer, more even). **D 5:** flat to dimensional; echoes the table lamps' cones without being a lamp; looks like sculpture. No blobby type: straight text on a clean spiral.

## 08 NOD (`svg/08_nod.svg`)
**Guest:** A tiny cone that cannot fall over. A flick makes it nod to you and rock for 3 to 4 seconds.
**Mechanism:** Cone (85 mm, base 60) on a half-ball. Centre of mass is 13.3 mm below the ball centre (shell 3 g, cone 4 g, 15 g steel weight); small-oscillation period 0.57 s (hand calculation in the script).
**Materials:** lemon card, steel washers. **Production:** die-cut cone sector, 6 gores, hand assembly (about 3 min each).
**F 3:** hand assembly and weights per card. **D 4:** the lamps' small cousins; a table full of nodding cones is memorable but toy-like.

## 09 BLACK TO COLOUR (`svg/09_black_to_colour.svg`)
**Guest:** The card has a narrow window with a paper strip, its tail in a shot of water. At 20:00 it shows a black bar. By dessert the bar has separated into yellow, pink and blue blocks.
**Mechanism:** Paper chromatography: dye-based black splits as the water front climbs. Four-state storyboard in the sketch.
**Materials:** chromatography paper, dye-based inkjet black (or water-soluble marker), shot glass, lemon card. **Production:** laser cut, hand-fitted strip.
**F 2:** climb speed and colours depend on the ink, needs tests; shot glass adds a second table object. **D 5:** the only idea that changes over the whole evening; it is literally black turning into colour blocks. The colours are the one non-lemon, non-black element; the client should approve that.

## 10 COLLAR (`svg/10_collar.svg`)
**Guest:** Neighbours' cards slot into each other and build a collar around the shared lamp, each guest's name facing outward.
**Mechanism:** Egg-crate slots: north/south cards slotted from the top, east/west from the bottom (26 mm deep, 1.2 mm wide). Cards 160 x 52 mm.
**Materials:** 350 gsm lemon. **Production:** die cut, print both sides.
**F 4, D 3:** structurally trivial, but the lamp-and-plate zone gets cluttered and a missing guest leaves a gap (I count that as a feature). Weakest of the twelve visually.

## 11 JACK (`svg/11_jack.svg`)
**Guest:** A folded napkin sits flat. Lift it and a lemon card springs up from below.
**Mechanism:** Hinged flap on a base card, an elastic band from the flap (anchor tab 5 mm proud) to a point behind the hinge (stretched 93 mm flat, 75 mm upright), and a 47 mm paper strap that stops the flap at 70 degrees. The napkin (about 40 g) is the weight.
**Proof:** the numbers come from `src/c11_svg.py`; the analysis found the band alone would pull the flap past vertical to 150 degrees, so the strap is required.
**Materials:** 300 gsm card, 2 mm elastic band. **Production:** die cut, hand-fitted band.
**F 4:** the napkin has to be left alone by staff. **D 4:** a real surprise with a physical start; the napkin becomes the trigger.

## 12 POUR (`svg/12_pour.svg`)
**Guest:** A card with a smudged, mirrored name. Water is poured into the tumbler in front of it and the name reads cleanly through the glass.
**Mechanism:** A water-filled cylinder (r 36, n 1.33) is a lens: from 450 mm it mirrors the card (centre slope -0.43 against +1.27 for the bare view, so 3x magnified and inverted). Print is the 2D ray-traced preimage.
**Proof:** `src/c12_calc.py`: three images in the sketch (empty glass, full glass, print).
**Materials:** lemon card on slotted foot, plain straight tumbler (the table's water glass, not a tulip wine glass). **Production:** digital print.
**F 3:** the glass shape and distance (120 mm) must be fixed; the vertical optics are ignored. **D 4:** the glass the guest was going to use does the trick. **Flag:** mirrored, non-linear type; see the echo note in 03.

---

## Notes and honest limits
- The computed ones (01, 02, 03, 12) are geometry in plan or ideal optics; real glass, real bulbs and real card will move them. All four need a one-day mock-up.
- 05, 06, 08, 10 are conventional paper engineering with a twist; the sketch is a statement of mechanism, not a measured prototype (the flexagon strip's face order is not re-derived).
- Two ideas I tried and dropped: a stair-stepped anamorph (reads from every seat, so no surprise) and a lemon scanimation barrier (stripe contrast inverts).
