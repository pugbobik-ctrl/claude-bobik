# Dinner place card

A freestanding place card for the Colorblock × DNA dinner: a flat die-cut form that
stands on its own. Its form is its own idea and does not reuse the poster's lettering
or the receipt runners. Black on pre-coloured lemon board (#feed95), Wix Madefor Text.

## Directions (v2, after review)

| | Idea | Reference | Size | Per SRA3 |
|---|---|---|---|---|
| D1 | two plates slotted into a cross, plus a "sail" variant with a big table numeral | Eames House of Cards, Noguchi | 100 × 34 + 64 wide | 15 |
| D2 | a segment and a strut lifted from the card, their voids left in the base | Peter Callesen, origamic architecture | 105 × 118 | 8 |
| D3 | twelve skewed tents cut from one sheet, one heavy line runs across all of them | Enzo Mari, 16 Animali | ~106 × 101 | 12 |

`dielines/` holds the 1:1 mm SVGs (cut, crease, slot, safe and bleed layers),
assembled views, notes with specs and assembly, and `*_verify.txt` geometry checks.
`dielines/src/` regenerates everything: `python3 d1.py` (needs fontTools, shapely).
`png/` has previews.

D2 is the lead direction. Test first: slot widths on the D1 test strip (0.6–0.9 mm),
the D2 strut flanges, and the D3 tab lock.

## Research

- `research/references.md`: 18 artist and designer references, grouped by how the flat form stands.
- `research/factcheck.md`: an independent check of each one (confirmed, corrected or dropped).
- `research/dieline-review-v1.md`: the production and concept review that v2 answers.
