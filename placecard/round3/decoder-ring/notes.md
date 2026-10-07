# DECODER RING - production notes (five artists)

Dinner, Colorblock x DNA Kitchen, 10 oct 2026. Black on pre-coloured lemon #feed95. All units mm.
Scope after the client's re-scope: Under the Lamp, Flag Up, Kosode and the Absent-Guest tab were dropped (their early files are parked in `_dropped_by_rescope/`, not maintained).

## What it is
A lemon card carries the artist's name as a cylindrical-mirror anamorph (melted DINNER-logo letters, UPPERCASE, two lines first / last). A mirror ring stands inside a printed circle on the card; from the seat the name resolves in the ring, upright and complete. Straight (readable) type on the card: lockup COLORBLOCK x DNA and the event lines. The ring is a mirror-board strip, mirror outside, lemon inside with the lockup on the inside lip.

## Final files (Illustrator)
`../final/decoder-ring_<artist-slug>.svg` x5 and `../final/decoder-ring_ring.svg`, plus `../final/index.json`. Groups: layer-art (filled paths, as printed), layer-cut (stroke only), layer-text (live text, Wix Madefor Text 700 / 600), layer-guides (non-printing). No raster, clip, mask, filter, use or transforms. layer-crease / layer-perf are omitted (empty). On the ring file layer-art is the lemon flood #feed95 (printed on the board back). PNG previews in `../final/preview/`.
Working files here: `dr_card_<slug>.svg` (dieline with spec block, outlined type), `dr_ring_flat.svg`, `dr_sheet_cards_SRA3_1/2.svg`, `dr_sheet_rings_SRA3.svg`, `dr_assembly.svg`, `dr_section.svg`, `dr_views_*.png` (renders), `dr_verify.txt`, `dr.json` (ring, eye, mapping, strip polygon), `dr_<slug>.json` (name outlines in the picture plane, anamorph print outlines in ring-centred world mm and in card mm, sample mapping table, ray-trace scores).

## Dimensions
- Ring: mirror (outer) R 40 (outside diameter 80, inside 79), height 48, board 0.40. Flat strip 266.1 body + 12 tab = 278.1 x 48; lap 16; slit 10.8 x 0.5 at 22 from the slit end; tab 12 x 10. Formula L = 2 pi (R - t/2) + 16, recompute for another caliper.
- Card: 150 x 156, corner r 4, ring axis at (75, 47.5) from the top-left; printed foot ring r 40.45 (0.4 line) hugs the ring; a black dot 3.6 mm outside the circle at the guest-left marks the seam position.
- Eye: 430 up, 450 toward the guest from the ring axis (elevation 44.7 deg to the front of the ring). Next seat for the displacement test: +650 mm to the side.
- Why bigger than the first sketch (r 26, h 50, card 160 x 130): apparent cap height 7.0 mm (target >= 7) in two lines needs a mirror 62 mm wide and 40 mm of mirror height once the straight lines are curved by the cylinder; R 40 / H 48 keeps the widest names (SOPHIA ZHURAVKOVA, TANYA ANDRIANOVA) within +-55 deg of the mirror front and 4 mm clear of the rim and base. The print then needs 150 x 156 (name lands 40 to 95 mm in front of the ring axis).
- Cap height: 7.0 mm apparent (picture plane at the ring, perpendicular to the sight line). On the mirror surface it is 9.6-9.7 mm tall at the centre (foreshortened by the 45 deg view).

## Anamorph derivation (own ray-trace, no reuse of the round-2 print)
Plain uppercase Wix Madefor Display Bold (x-stretch 0.9) is set on a virtual picture plane through the front-centre mirror point, perpendicular to the sight line. The melt (Gaussian blur 0.10 x cap, threshold 0.27, the client's fit of the logo) is applied IN that plane, i.e. in the reflection domain, so the softness is even in the mirror (a melt applied on the card after the mapping would be stretched unevenly by the mirror). Each outline point of the melted shape is then mapped: eye ray through the point -> first hit on the cylinder -> specular reflection about n = (Qx,Qy,0)/R -> card plane. Outlines are densified to 0.2 mm; the card artwork is vector. Check: the finished print (rasterised at 0.1 mm) is ray-traced from the seat on the picture plane and compared with the intended name.

## Results (dr_verify.txt, all PASS)
| artist | name height on mirror z (of 48) | arc | print on card (x, y mm) | seat IoU / best-shape corr | next seat best-shape corr |
|---|---|---|---|---|---|
| Tanya Andrianova | 4.6-43.4 | -54..54 | 26.7-123.3, 69-133 | 0.89 / 1.00 | 0.49 |
| Igor Zotov | 10.6-37.4 | -24..24 | 43.4-106.9, 91-126 | 0.86 / 1.00 | 0.57 |
| Andrey Lee | 11.9-36.1 | -28..28 | 32.7-120.9, 94-125 | 0.86 / 1.00 | below 0.7 (displaced) |
| Sasha Chernikov | 7.6-40.4 | -44..44 | 30.9-119.4, 76-130 | 0.89 / 1.00 | 0.52 |
| Sophia Zhuravkova | 4.1-43.9 | -55..55 | 25.2-123.5, 66-134 | 0.89 / 1.00 | 0.44 |
Renders: `dr_views_<slug>.png` (seat close, seat with card, next seat) and `dr_views_all.png`. From the next seat the name is displaced, tilted and mirror-tangled (it reads as a seat check); short names (Igor, Andrey) stay half-readable there because they sit near the mirror centre.
Straight text is clear of the printed arcs by 12 mm or more and lies outside the ring footprint and outside the strip of card hidden behind the ring from the seat (50 mm behind the ring).

## Per-name refinement (seat view checked for each)
Generated by `src/dr_melt.py` (per glyph melt, then spacing) and listed in `src/dr_names.py`.
- All names: letters are melted one by one and then spaced so that no two letters fuse (the logo setting fuses N-D-R, E-E, N-I-K, which merged counters and made the names read as a blob in the mirror). Minimum outline gap 0.35 mm (0.05 cap); loose diagonal pairs are pulled to 0.8 mm for optical evenness.
- All names: the counter of A closes at the logo setting; A is melted slightly less (sigma 0.075, thr 0.28) so its counter stays open (a 0.4 mm slot: it shows as a dot in the mirror at 7 mm cap, which is the honest limit of the letterform).
- TANYA / ANDRIANOVA: pairs TA -1.44, YA -1.60, VA -1.46 mm tightened (loose diagonals); D-R opened 0.06; line break kept (first / last).
- IGOR / ZOTOV: G-O, O-R opened 0.06; O-T, T-O tightened 0.33; I and R terminals checked (no thin ends).
- ANDREY / LEE: D-R opened 0.06; the E-E pair in LEE no longer closes the counters (fused in the logo setting); break kept.
- SASHA / CHERNIKOV: K-O tightened 0.58; N-I-K separated (the logo setting fused them).
- SOPHIA / ZHURAVKOVA: A-V -1.41, V-A -1.46, K-O -0.58 tightened; O-P, P-H opened 0.06; Z-H separated.

## Tolerances (Sophia Zhuravkova, the widest name; best-shape correlation, reads >= 0.75; scan in dr_verify.txt)
- Ring sideways off its mark: +-2 mm ok (0.85), +-4 mm fails (0.62). Along the guest axis: +-4 mm ok (0.84). Therefore the printed foot ring and the seam dot.
- Ring radius error +-1.5 mm ok (0.86): the ring must be round; an out-of-round or kinked ring breaks the name.
- Seated eye: +-80 mm sideways ok (0.88), +-60 mm height ok (0.97), +-100 mm distance ok (0.85). Lean in or out a hand's width and it still reads, but it slides; "seat check" (neighbour sees it displaced) is therefore soft, not a lock.
- Mirror quality: image displacement = 2 x normal error x path (50-95 mm). To keep it under 1 mm the normal must stay within +-0.4 deg: smooth cylinder, no flats, no creases, no orange-peel lamination.

## Materials
Card: lemon pre-coloured board 300-350 gsm (0.4 mm), 1 colour black, no flood, no bleed.
Ring (choose one, test first):
1. Mirror-metallised PET laminated on 0.35-0.45 mm paperboard ("mirror board"; protective peel film on the mirror face). Reflectance >= 85 %, smooth specular finish (no brushed, pearl, holographic or embossed), no lamination bubbles. Grain parallel to the 48 mm ring axis. Cheapest and fastest; seam with lap + tape + tab.
2. 0.2-0.3 mm mirror PET film (polyester) laminated with transfer tape on 135 g lemon paper (Colorplan Citrine or equivalent; lockup printed on it first). Best optics, no board texture; needs a laminating step.
3. 0.5 mm mirror PETG/acrylic sheet cold-bent (not scored): perfect specular; lemon inside lost; butt joint with tape, no overlap (cut L = 2 pi (R - t/2)). Use if 1 shows waviness.
Printing on mirror board: the board back is paper, but digital presses often refuse metallised stock; use offset/UV or laminate lemon-printed paper to the back (option 2 route). Glue: 8 mm double-sided tape on the marked lap.
Type on the card is set at the menu's scale: lockup COLORBLOCK / DNA Bold 13.61 pt (4.80 mm font size), x SemiBold 9.52 pt, event lines SemiBold 9.52 pt (3.36 mm font size, cap height 2.4 mm - below our earlier 3.5 mm minimum; it follows the client's menu, so check legibility on the prototype).

## Production
Cards: 4 per SRA3 (rotated 90 deg, long grain along the 450 side), 2 sheets for five artists (3 spares/test blanks). Print black, die cut or laser/flatbed knife. Rings: 8 per SRA3 mirror sheet (strips along the 320 side), one sheet covers five + 3 spares; print the lemon flood and lockup on the back before cutting; cut with the mirror face masked (laser scorches the film: prefer knife/die with a 0.5 mm slit rule). Assembly: ring 90 s (tape, roll, tab through the slit), placing on the card 10 s. About 8 minutes of hand work for the set of five.

## First prototype test
1. Print one card (Sophia Zhuravkova, the widest) on white paper and make one ring from whichever mirror board is on offer (all three options if possible).
2. Mark the ring axis and a seat 450 mm back / 430 mm up with a tape and a chair; measure the real eye height of three people (a small, an average and a tall person).
3. Pass: name upright and complete in the mirror from the seat; the lap seam invisible from the seat; with the ring shifted 2 mm it still reads; from the neighbouring seat (650 mm) it does not read; the 9.5 pt event lines are readable without the ring at arm's length.
4. Fail modes: waviness (reject the mirror stock), name too small to read through the melt (increase cap_vis to 7.5 and R to 42; the generator takes both), seam visible (rotate the seam dot to the guest-left silhouette).
5. Check the mirror surface after 30 s of handling for fingerprints and film scratches; keep the peel film on until the card is on the table.

## Open points
- The inside lockup is only visible at the far wall, upright; if the client prefers it on the outside leave it off the ring and put it only on the card.
- Names with Cyrillic spelling: the generator takes Latin names set in Wix Madefor Display Bold; Cyrillic would need the same melt with the same font (glyphs exist).
