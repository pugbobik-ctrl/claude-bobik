# Dinner receipts → Illustrator

`dinner-receipts.jsx` builds all seven strips in a new Illustrator document, one artboard
each, at print size (80 mm rolls, 72 mm for the ticket roll, 57 mm for the till receipt).

**Run it:** File → Scripts → Other Script… → `dinner-receipts.jsx`.
Install Wix Madefor Display first (all weights, Regular to ExtraBold, from Google Fonts);
if a weight is missing the script says which and falls back to the default font.

Everything stays editable:

- **Type is live text.** Each step of the type scale is a paragraph style named
  `Dinner <step> <size>pt` with its size, leading, tracking, metric kerning and caps
  (caps are a style setting, so the text itself stays in normal case). Retype freely.
- **Colours are global swatches**: Dinner Ink, Dinner Paper, Dinner Brown, Dinner Cream.
  Change one and every strip follows.
- **The DINNER wordmark** is a compound path traced from the poster.
- **Rules** are dashed strokes, the **barcode** (EAN-13 2026101018001) and **QR** are
  rectangles, paper edges are plain paths.
- **The caramel swirl** is a group of rings with a live Gaussian Blur, clipped to the paper:
  double-click in to recolour or move the rings.

The script is generated: edit `../build/spec.py` and run `python3 ../build/build_jsx.py`
(and `build_html.py` for the web versions) rather than editing the `.jsx` by hand.
