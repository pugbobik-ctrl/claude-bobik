# SYSTEM theme: scale, crop and the system (6 variants + family sheet)

Root: /tmp/claude-0/-home-user-claude-bobik/6a3dcf92-132a-5018-88ad-a2068c46056a/scratchpad/variants/system/
- final/  30 layered SVGs (variant x artist) + final/index.json (file, variant, design, artist, width_mm, height_mm, notes)
- previews/  `<variant>_<artist>_seat.png` (perspective, eye 430 mm up / 450 mm away, 44 deg down, numpy+OpenCV), `<variant>_5up.png`, `family_sheet.png`, `flat_all_sophia.png`
- lib/, mods/, run.py, family.py  generators (re-run: `python3 run.py v1` ... `v6`)

SVG format: mm, viewBox 1 unit = 1 mm. Groups layer-art (lemon flood, melted names as filled Bezier paths, printed rules as filled rects, no strokes),
layer-text (LIVE <text>, Wix Madefor Text, numeric weight, size in mm, rotate() only), layer-cut, layer-crease, layer-guides. No clipPath/mask/filter/image/use.
Cropped names are cut geometrically (straight edges at trim + 3 mm bleed). Left artboard = recto, right = verso (turn like a page).
Type: details = SemiBold 9.5 pt (3.36 mm) tracking +10; lockup = Bold caps 13.6 pt / x SemiBold 9.5 pt / gap .55 em (as menu) unless stated; label 7.3 pt.
Melting: every scale/break is re-melted from plain text (melt.py, display700, stretch .9 or solved BEFORE melting to hit a width, sigma .1, thr .27, sigma scaled to each line's own cap). No melted shape is ever stretched.

## Ranking
1. V2 Wrap  2. V4 Receipt Mass  3. V5 Line-up Band  4. V1 Downstream  5. V3 Concertina  6. V6 Quiet Lockup
Family sheet uses V2 + V4 (previews/family_sheet.png).

## V2 Wrap (V-fold, ridge toward guest) - files final/v2_wrap_*.svg
Name 1 line, cap 23.2 mm (66 pt), same for all, starts x=9; the card is 2 x 95 mm so the name (183-355 mm long) always runs past the right edge and
continues on the verso (inner faces, read from the opposite seat; previews/v2_wrap_*_opposite_seat.png). Tanya: "TANYA AND | RIANOVA".
Sheet 190 x 64 mm, fold at x=95 (mountain). Grid: 190 = 2 panels of 95; margin 6; lockup baseline y=11.5; name top y=17; details baseline y=57.8 crossing the fold.

## V4 Receipt Mass (tent) - final/v4_receipt_mass_*.svg
Leaf 100 x 72 mm, sheet 100 x 144 one side (back leaf rotated 180). First name and surname each melted at their own cap so both fill 99 mm
(first name 19-27 mm cap, surname 10-11 mm; Lee 17/26-ish). Zone y 13.5-57; lockup 13.6 pt centred (baseline 9.2); dashed rule y=59.2; receipt line 7.3 pt SemiBold,
flush-left date/time, flush-right venue (baseline 64); double rule 0.25 mm at 66.6/67.8; margins 5.

## V5 Line-up Band (tent row) - final/v5_lineup_band_*.svg
Leaf 100 x 66; five cards butt together 01-05. First name cap 16 mm justified to the 92 mm measure (solved pre-melt, centred if >1.7x), surname cap 10 mm natural.
1.3 mm bar y=50.4 bleeds off both sides and runs along the whole table; details 9.5 pt two lines at 4 mm margin; label "01"/"Line-up" 7.3 pt; lockup 13.6 pt.
Seat renders show the whole row from each artist's seat.

## V1 Downstream (L-fold) - final/v1_downstream_*.svg
Upright 72 x 120 + foot 44 (sheet 72 x 164), upright raked 12 deg. Name rotated 90 cw like the poster DINNER; melted length always 171 mm so it runs over the fold and off the foot.
Caps: Tanya 18.5 (2 lines), Igor ~20 (1 line), Andrey ~21.6 (1 line), Sasha ~21 (2 lines), Sophia 17.6 (2 lines) - break chosen so thickness <= 48 mm.
Columns: name x 5-53, details (SemiBold 9.5 pt rotated) baseline x=58.4, lockup (13.6 pt rotated) x=63.7, all starting y=6. Verso: lockup, small 2-line name, details.

## V3 Concertina - final/v3_concertina_*.svg
Zig-zag of 14 mm panels (+-22 deg), one letter per panel, word space = blank panel; 14-17 panels (196-238 mm), height 58. Letters cap 20 mm re-melted singly
and condensed before melting to <=12 mm wide. Lockup (y=9.5) and details (y=53.4) run across the folds. Verso: lockup, 1-line name cap <=6.5, details.

## V6 Quiet Lockup (L-fold) - final/v6_quiet_lockup_*.svg
Upright 100 x 50 + foot 38. Lockup scaled x2.58 (35 pt Bold, COLORBLOCK = 88 mm wide, stacked "COLORBLOCK / x DNA"); melted name cap 4.6 mm (13 pt) on the foot; details 9.5 pt; dashed rule at y=46.

## Per-name refinements (all variants)
Plain-text letter-pair spacing before melting (cap fractions): RI +.09, NI +.13, IK +.12, ND +.06, RE +.06, EE +.07, ZH +.07, IA +.05, IG +.06, VK +.04, KO -.03 and others; global track +.025 cap.
Fixes: R-I and N-I-K were merging into blobs (ANDRIANOVA, CHERNIKOV), N-D / R-E in ANDREY, E-E in LEE, Z-H in ZHURAVKOVA, H-I-A in SOPHIA.
Multi-line blocks are melted per line at the line's own cap (a shared sigma turned small surnames into mush). Breaks: first name / surname everywhere (V3 one letter each; V1 1 line for Igor and Andrey, 2 lines for the long names).
Known trade-offs: V1/V2 crop letters by design (V1 last letter half cut; V2 splits one letter at the fold); V3 card length follows the name (196-238 mm); V5 preview uses 20 deg tent lean and 1 mm gaps.
