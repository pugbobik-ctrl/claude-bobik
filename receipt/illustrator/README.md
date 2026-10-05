# Dinner receipts → Illustrator

## Quickest: open the SVGs

`svg/*.svg` (also zipped as `dinner-receipts-svg.zip`) are the seven strips at print size.
Open one with File → Open: each opens on its own artboard with **live text** in
Wix Madefor Text (one text object per line, the runner's paragraphs as one object each),
named groups for paper, type, wordmark, barcode and QR, dashed rules as dashed strokes,
No images, no masks, no patterns.
They are written by `../build/build_svg.js` from the same layout engine as the script below.

## Fullest: run the script

`dinner-receipts.jsx` builds all seven strips in a new Illustrator document, one artboard
each, at print size (80 mm rolls, 72 mm for the ticket roll, 57 mm for the till receipt).

**Run it:** File → Scripts → Other Script… → `dinner-receipts.jsx`.
Install Wix Madefor Text first (all weights, Regular to ExtraBold, from Google Fonts);
if a weight is missing the script says which and falls back to the default font.

If any part fails, the script still builds everything else and ends with a list of what went
wrong and on which line. Send that list back to get it fixed.

Everything stays editable:

- **Spacing follows the poster**: measured off it, capitals run at +170 (1/1000 em) and
  mixed case at +10, kerning is the font's own (Auto), lists at about 1.1 leading.
- **Type is live text.** Each step of the type scale is a paragraph style named
  `Dinner <step> <size>pt` with its size, leading, tracking, metric kerning and caps
  (caps are a style setting, so the text itself stays in normal case). Retype freely.
- **Colours are global swatches**: Dinner Black (type and graphics) and Dinner Lemon (paper).
  Change one and every strip follows.
- **The DINNER wordmark** is a compound path traced from the poster.
- **Rules** are dashed strokes, the **barcode** (EAN-13 2026101018001) and **QR** are
  rectangles, paper edges are plain paths.

The script is generated: edit `../build/spec.py` and run `python3 ../build/build_jsx.py`
(and `build_html.py` for the web versions) rather than editing the `.jsx` by hand.
