# SIT DOWN: V-fold seat-locked anamorph (production notes, round 3 A)

Client content (final): ONE artist per card, melted uppercase name (logo style), two lines first / last. Back of the V: COLORBLOCK x DNA lockup and event details, set straight. No seat or table numbers. Five artists: Tanya Andrianova, Igor Zotov, Andrey Lee, Sasha Chernikov, Sophia Zhuravkova.

## Files
- `final/sitdown_<artist>.svg` (5): layered hand-off for Illustrator. Front card at y 0-88, back card at y 100-188 (drawn as seen from the back). Layers `layer-cut`, `layer-crease`, `layer-art` (melted name as filled Bezier paths), `layer-text` (live Wix Madefor Text), `layer-guides`. No images, clips, masks.
- `sit_down/sitdown_<artist>_dieline.svg` + PNG: annotated 1:1 dielines (older preview art style; geometry identical). `sitdown_back.svg`, `sitdown_SRA3_front.svg`, `sitdown_SRA3_back.svg`.
- `sit_down/png/sitdown_views_<artist>.png`: ray-cast of the folded card from the seat, 330 mm left, 330 mm right, walking past, across the table, plan.
- `json/sitdown_geometry.json`: eye, leaf corners, outline polyline, crease, banner plane, homographies banner -> leaf -> flat sheet, per-artist printed outlines and melt parameters.
- `sit_down/sitdown_verify.txt` (RESULT ALL PASS), generators in `src/` (`sitdown_build.py`, `sitdown_art.py`, `sitdown_geom.py`, `sitdown_views.py`, `sitdown_verify.py`, `final_export.py`; the name is an input, `python3 final_export.py` loops over the five).

## Dimensions and board
- One sheet 164 x 88 mm, one valley score at x = 82, two leaves of 82 mm that open 90 deg toward the guest (each 45 deg from the sight line). Winged-V outline: straight bottom (table edge), top edge 88 mm at the free ends falling in a straight line to 50.6 mm at the crease (leaf height 37.4 mm there). Concave apex rounded R1.
- Top edge rule: plane through the eye and the crease top containing the x direction, so the apparent top is a level line from the seat. The free end comes out at exactly 88.0 when the crease-end leaf is 37.42 (round 2 used 38 / 88.5).
- Board: pre-coloured lemon #feed95, 300 g/m2 (caliper about 0.40), grain parallel to the crease. Black on lemon, duplex. No bleed. Single score from the printed face (valley).

## Geometry and the warp (recomputed)
Eye E = (0, -450, 430) mm, crease at the origin (card at the far edge of the plate). The banner plane is perpendicular to the sight line to the crease midpoint (610 mm from the eye); banner X right, Yb down from the level top edge. Every banner point maps to each leaf by a ray from E (a projective map; matrices in the JSON). Seen from the seat the two leaves tile the banner silhouette: crease column 27.6 mm high, ends 69.8 mm.

Artwork pipeline (changed in this pass, as requested):
1. Plain uppercase text (Wix Madefor Display Bold, x-stretch 0.9) is set in the banner plane, two lines, gap 0.40 cap.
2. It is projected onto the flat sheet through the map above (sheet space, 16 px/mm).
3. The melt is applied in sheet space: Gaussian blur sigma x LOCAL cap height (local cap = banner cap / local vertical scale, 11.3 to 12.8 mm on the sheet), threshold, so blobs have the same weight on the card on both sides of the crease and at the free ends (no stretched blobs on the far side).
4. Contour traced (sub-pixel, 0.03 mm tolerance) and smoothed to cubic Bezier curves.
Guest sees cap height 9.2 mm in the banner plane (same for all five names; about 12 mm printed on the leaf, x1.41 wide, x1.30 high in sheet space). Seen block 24 mm high, 51 to 103 mm wide.

## Refinement per name (viewed from the seat, metrics in sitdown_verify.txt; logs in src/sitdown_tune*_log.json)
Reference = the logo-style asset (letters merge into blobs, A counters mostly closed). Targets: separate the letters, keep counters open, keep stroke weight even and close to the asset, name block inside the silhouette with >= 1.5 mm margin. Search over track (+0.06 / +0.09 cap), threshold (0.27-0.37) and blur (0.075-0.10 cap).
- Tanya Andrianova: first pass track +0.09 / thr 0.27 left 3 of 8 counters open (RIA and the A's closed); final track +0.06, thr 0.32, blur 0.075: 8 of 8 counters, 15 blobs, stroke 2.2-3.6 mm. Split TANYA / ANDRIANOVA kept.
- Igor Zotov: IGOR merged I with G; track +0.09 separates; thr 0.27, blur 0.10 kept (stroke 2.8 mm, even); 5 counters (expected 4). Split IGOR / ZOTOV.
- Andrey Lee: AND and the two E's of LEE merged; track +0.09, blur 0.075, thr 0.27: 3 of 3 counters, 9 blobs, stroke 2.5-3.5 mm. Split ANDREY / LEE.
- Sasha Chernikov: SASHA and NIK merged; track +0.06, thr 0.27, blur 0.10: 4 of 5 counters (one A counter still closes; blur 0.075 opens it but thins CHERNIKOV below 2.4 mm so it was rejected), 14 blobs. Block top touched the 1.5 mm margin (1.44 mm), so the name is lowered by 0.35 mm (dy). Split SASHA / CHERNIKOV.
- Sophia Zhuravkova: HIA and VK merged; track +0.09, thr 0.32, blur 0.075: 7 of 7 counters, 16 blobs, stroke 2.3 mm even across the five bins. Split SOPHIA / ZHURAVKOVA.
- All: cap lowered from 10.2 to 9.2 mm and the block top moved to 2.5 mm below the apparent top edge, because the melt grows the ink by about 0.8 mm per side and the crease column is only 27.6 mm high. Verification: all five names sit inside the apparent silhouette with >= 1.5 mm margin as SEEN from the seat, >= 0.7 mm from the cut edges on the sheet; 97 % or more of each plain letter area is inked and under 1 % of ink lies beyond 0.35 cap from a letter.

## Type
Name: melted Display Bold uppercase (paths). Back, live text in Wix Madefor Text: COLORBLOCK and DNA Bold 13.6 pt (4.80 mm), x SemiBold 9.5 pt (3.35 mm), gap 0.55 em of 13.6 pt (2.64 mm), no tracking; details SemiBold 9.5 pt = 3.35 mm font size (cap 2.40 mm, below the earlier 3.5 mm secondary-cap rule: set by the client to match the menu), tracking +10/1000 (0.034 mm), mixed case: "Dinner · 10 oct 2026 · 18:00" / "DNA Kitchen, Samokatnaya 4s53". Lockup on the viewer-left leaf (the world right leaf), details on the other, 14 mm from the crease. Seen from across the table the leaves are at 45 deg, widths foreshorten to 0.71, so the details are arm's-length text; only the lockup is readable from across.

## Assembly and production
- Open the V toward the guest to 90 deg (+-9 deg keeps the reading clean), crease vertical, bottom edges on the cloth; the card stands on its two lower edges. No glue.
- Print duplex on the pre-coloured sheet (back page = front mirrored about the vertical axis, supplied as sitdown_SRA3_back.svg), then cut and score. Steel-rule die or flatbed knife; one crease rule from the printed face; crease runs to the apex fillet.
- SRA3 (450 x 320, gripper 10): 6 cards nested at 180 deg alternation with the crease parallel to the 450 mm long grain, gap 3 mm (4 per sheet without nesting). Slots: five artists + one spare. Waste is the V-notch triangles.

## Tolerances (from sitdown_verify.txt; RMS shift of the ink in the banner plane <= 0.25 cap = 2.3 mm)
Eye height +-52 mm, eye distance +-50 mm, sideways +-36 mm, V opening 90 +-9 deg. 330 mm to either side the name shears by 21 mm RMS (2.3 caps) and half of it hides in the fold, so only the seated guest reads it. Chair height and leaning change the reading inside these limits.

## First prototype test
Print the front on plain paper at 100 %, score, fold to a square (90 deg gauge cut from card), put it at a real table at the plate's far edge. Seat five people of different heights, ask them to read it on sitting, leaning in and back, and from the next seat. Pass: four of five read the whole name on sitting. Also check: the 0.4 mm score does not crack the melted ink, the V holds 90 deg without a gauge (if it relaxes toward flat, add a 5 mm tape dot inside the crease), and the back type is acceptable at 3.35 mm.

## Open points
The melted name asset parameters follow `logo/melt_params.json`; counters of A are small at this size and one remains closed on SASHA. The final SVG name paths are curves (Catmull-Rom to cubic), not potrace output; they edit normally in Illustrator.
