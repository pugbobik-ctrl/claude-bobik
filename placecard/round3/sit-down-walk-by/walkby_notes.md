# WALK-BY: pleated agamograph tent (production notes, round 3 A)

Seated guest sees the artist name (melted uppercase) on the A facets; people walking along the table see DINNER and 10.10.2026 on the B facets; the tent's back panel carries COLORBLOCK x DNA and the event details. Five artists: Tanya Andrianova, Igor Zotov, Andrey Lee, Sasha Chernikov, Sophia Zhuravkova. Source: round2/craft c6; tooth geometry unchanged.

## Files
- `final/walkby_<artist>.svg` (5): layered hand-off. Strip at y 6-40 and tent card at y 58-158 on one proof sheet (they are separate boards in production). Layers: `layer-cut` (strip outline with necked tabs, tent outline, slits), `layer-crease` (27 strip creases, tent apex; `data-fold` valley / mountain), `layer-art` (interleaved name slices + DINNER / date slices as filled paths, crease ticks as thin filled rects), `layer-text` (live text: tent back panel, rotate(180)), `layer-guides`. No images.
- `walk_by/walkby_<artist>_strip.svg`, `walkby_tent.svg`, `walkby_profile.svg` (tooth profile x11, viewing table, jig, tolerances), `walkby_SRA3_strips.svg`, `walkby_SRA3_tents.svg` and PNGs.
- `walk_by/png/walkby_views_<artist>.png`: simulated views from five angles (theta -18, 0, 35, 55, 70) for each artist.
- `json/walkby_geometry.json`: profile polyline, facets, 27 crease positions, strip and tent outlines, slits, interleave mapping, per-artist name shapes. `walk_by/walkby_verify.txt` (RESULT ALL PASS). Generators: `walkby_geom.py`, `walkby_art.py`, `walkby_build.py`, `walkby_extra.py`, `walkby_views.py`, `walkby_tune.py`, `final_export.py`.

## Pleat and tooth profile
13 teeth. A facet 9.000 mm at +18 deg (faces the seat), B facet 2.9596 mm at -70 deg (faces the walker); closure a sin18 = b sin70 gives zero residual and the profile returns to z = 0. Pitch 9.5718 mm, panel 124.43 mm, depth 2.78 mm, developed length per tooth 11.96, body 155.5 mm, strip 171.475 x 34 mm with 8 mm tabs (necked to 16 mm tall to pass the 18 mm tent slits). 27 creases: 13 valleys (A starts), 13 mountains (A ends), right tab hinge; minimum crease pitch 2.96 mm.

## Scoring and registration
Valleys and the tab hinges are scored from the printed face, mountains from the back (two passes registered on the corner crosses); single-pass alternative: everything from the printed face and the mountains fold against the score (rougher, B facets wander first). Crease positions are tabulated on the strip dieline (tolerance +-0.15 on the die, +-0.3 in use, which moves 10 % of a B facet). 3 mm crease ticks sit 0.8 mm outside the cut at all 27 creases, top and bottom, shared in the 8 mm gap between nested strips; four registration crosses per sheet.

## Interleaved artwork per name (script input = name)
- Name image: plain uppercase (Wix Madefor Display Bold, x-stretch 0.9) set at cap 7.32 mm in the apparent frame (111.27 mm wide, 34 mm high, centred at y 20), melted there (blur sigma x cap, threshold), traced to vector. The melt stays in apparent (seat) space because the A slices are separated by B strips on the sheet; the only stretch applied afterwards is 1/cos 18 deg = 1.0515 in x (5 %, negligible for the blob shape).
- A slices: apparent u in [k x 8.5596, (k+1) x 8.5596] maps to sheet x = 8 + k x 11.9596 + (u - k x 8.5596)/cos 18 deg.
- B image (38.48 mm wide): melted DINNER (logo style, 36 mm wide, cap 7.5, y 1.6-9.9; a stand-in for the logo file) plus 10.10.2026 in Wix Madefor Text SemiBold 5.0 mm, baseline y 31.2, outlined because it is sliced. B slices 2.9596 mm, 1:1 at x = 8 + k x 11.9596 + 9.
- No B ink between y 12 and 27.5 (the name zone 15.8-24.2), so at theta = 0 the B facets add slivers above and below the name only. Slice boundaries lie on creases. verify: vector slices reproduce the ideal images (IoU 0.99), and the pleat simulator shows the right ink on the facets facing the viewer.

## Simulated views (all five artists in the PNGs)
B share of visible area: -18 deg 1 %, 0 deg 11 %, 26 deg 25 %, 35 deg 31 %, 50 deg 45 %, 65 deg 73 %, 70 deg 90 %. Name clean up to theta = 3 deg (readable striped to 26 deg), so turn the tent about 15-18 deg toward the walker's side if possible; DINNER clean from 70 deg, which for a walker 0.9 m off the table is 2.5 m along it. The shimmer zone between is intended.

## Tent
136 x 100 mm, 300 g, one mountain crease at y 50 (score from the back), panels 50 mm, apex 40 deg, footprint 34.2, height 47.0. Front panel carries the strip (8 mm above the table edge, 124.4 wide), two slits 18 mm at x 5.78 and 130.22. Tab goes through the slit and folds flat behind, 6 mm double-sided tape. Back panel printed upside down so it reads for the person opposite; live text: COLORBLOCK and DNA Bold 13.6 pt, x SemiBold 9.5 pt, gap 0.55 em; details SemiBold 9.5 pt (3.35 mm; cap 2.4 mm, below the old 3.5 mm rule, client-set), tracking +10/1000, mixed case. The same tent artwork serves all five artists.

## Production
Strip 200 g lemon, grain parallel to the creases: SRA3 holds 10 strips with their length across the 320 mm side (14 if the creases may run across the grain). Tents on 300 g: 9 per SRA3 (3 x 3, gap 3). Digital print of the interleaved file, creasing wheel on a flatbed cutter, hand pleating on a jig (profile in walkby_profile.svg), tabs through slits, about 4 minutes per card. First test: print a strip in white 200 g, pleat 3 samples with creases at +-0.3 mm, check the three views at 0.9 m with five people.

## Refinement per name (logs in src/walkby_tune_log.json)
Reference = the logo asset (merged letters, closed counters). Search over track, threshold and blur, scored for open counters, separated letters and stroke weight.
- Tanya Andrianova: track +0.03, thr 0.32, blur 0.075 -> 8 of 8 counters, 15 blobs.
- Igor Zotov: track +0.09, thr 0.27, blur 0.10 -> 4 of 4, 9 blobs.
- Andrey Lee: track +0.03, thr 0.27, blur 0.075 -> 3 of 3, 9 blobs.
- Sasha Chernikov: track +0.03, thr 0.27, blur 0.075 -> 4 of 4, 14 blobs.
- Sophia Zhuravkova: track +0.06, thr 0.27, blur 0.075 -> 7 of 7, 16 blobs; the widened name was scaled by 0.942 to keep 2 mm margins in the 111.3 mm image (cap 6.9 mm).
Strokes come out at 1.8-2.4 mm (the logo asset 2.2-3.6): thinner so that counters stay open at this small cap; the thin strokes are the first thing to check in the prototype.

## Notes
The SKIRT concept was dropped by the client; its files are in `archive_skirt/`. DINNER here is a melted stand-in (the logo itself is a vertical blob); swap the B-image shapes when the logo file arrives (`walkby_geom.b_image`).
