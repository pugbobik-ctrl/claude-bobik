# Place cards → Illustrator

`svg2ai.py` turns the layered card SVGs into one Illustrator script:

    python3 placecard/illustrator/svg2ai.py placecard/illustrator/place-cards.jsx <dir-with-final-svgs> ...

Every card for every artist gets its own artboard at 1:1, one row per design. Layers:

| Layer | Content | Colour |
|---|---|---|
| Guides | safe area, labels (non-printing) | grey |
| Cut | die cut | spot **Cut** |
| Crease | folds and scores | spot **Crease** |
| Perforation | perforations | spot **Perforation** |
| Text | event details and COLORBLOCK × DNA as live Wix Madefor Text | Dinner Black |
| Artwork | the melted artist names, as vector compound paths | Dinner Black |
| Board (preview) | the lemon card under the die (non-printing) | Dinner Lemon |

Nothing is a raster image: names are editable curves, text is live, die lines are paths.
Install Wix Madefor Text (all weights) before running; the script reports any missing weight.

Input SVG format (one file per card and artist): mm units (`viewBox` 1 unit = 1 mm) and
top-level groups `layer-cut`, `layer-crease`, `layer-perf`, `layer-art`, `layer-text`,
`layer-guides`; text as `<text>`; no images.
