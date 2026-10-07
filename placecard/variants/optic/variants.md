# OPTIC variants (black on lemon #feed95, one place card per artist)

Seat: eye 430 mm up, 450 mm from the card; neighbour 650 mm to the side; across 1200 mm.
Finals: `final/<variant>_<artist>.svg` (30 files, mm, 1 unit = 1 mm) + `final/index.json`.
Layers: layer-cut / layer-crease / layer-perf / layer-art / layer-text / layer-guides; names are filled Bezier paths,
event details and COLORBLOCK x DNA are live `<text>` (Wix Madefor Text 600, 9.5 pt details). No image/clipPath/mask/filter/use (checked by `validate.py`).
Name pipeline: plain uppercase Display Bold x0.9 -> projective/ray-traced warp from the eye -> melt in warped space (blur 0.10 x local cap, thr 0.27) -> carve counters open -> vector.
Per-name refinement: letter-spacing raised per name/variant until every letter is a separate blob after the melt (`tracks.json`, 0.06-0.20 cap), counters kept open, widths refitted by cap.
Source: `lib/` (common, art, rt = ray tracer), `v*_*.py`, `driver.py`. Preview renders in `prev/` are from earlier test runs (indicative).

| rank | variant | idea | how it is made | tolerance / risk |
|---|---|---|---|---|
| 1 | v4_vault | curved card: sheet bent into a semicircular arch, name pre-distorted so it looks flat and straight from the seat; wraps and skews from the sides | print + one crease + hand bend, flat apron carries the details | most forgiving (head +-40 mm); arch needs 300 gsm and may spring open, tape the feet |
| 2 | v1_standup | flat card whose anamorph makes the name stand up above the table, with a hatched extrusion behind | print only | cheapest; illusion is mild at 43 deg and binocular vision flattens it; best with one eye or a photo |
| 3 | v6_runway | long strip lying along the gaze axis, rotated name stretched like a road marking, reads upright and large from the seat | print only, 90x420 mm (A3 long edge) | very strong from the seat, but the strip is big and reaches into the neighbour's zone; +-30 mm head |
| 4 | v2_relay | name split between the table card and a clear pane standing in slots; aligns only from the seat, melts off the glass onto the card | print + PET pane + two slots | wow effect, but pane must stand within ~2 deg and head within ~10 mm; acetate is fragile |
| 5 | v3_scanimation | grille over interlaced frames, the name melts crisp-to-approved as you sway (46 mm per frame) | print + spacer frame + printed PET grille | high: 0.27 mm registration/scale (same printer for both), dark image (25% light), slide acetate to set phase |
| 6 | v5_barlens | name printed squashed to a ribbon, an acrylic bar restores it | print + bought bar (200x32x32 mm) | needs an extra object and +-2 mm placement; squashed name is still legible, so no surprise; bar not in the guide budget |

Ranking is by robustness x effect x ease. All 30 finals pass the structural QA; v2 and v3 are complete (all five artists).
Not done in this pass: refreshed seat/neighbour renders for the final tracking values and 5-up seat render sheets (the preview images in `prev/` come from earlier tracking).
