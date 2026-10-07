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
| Lemon flood | light fills from the SVGs: the back of the Decoder Ring strip, bleed floods; hide it when printing on lemon board | Dinner Lemon |
| Board (preview) | the lemon card under the die (non-printing) | Dinner Lemon |

Nothing is a raster image: names are editable curves, text is live, die lines are paths.
Install Wix Madefor Text (all weights) before running; the script reports any missing weight.

Input SVG format (one file per card and artist): mm units (`viewBox` 1 unit = 1 mm) and
top-level groups `layer-cut`, `layer-crease`, `layer-perf`, `layer-art`, `layer-text`,
`layer-guides`; text as `<text>`; no images.

## Scripts

| Script | What | Sources |
|---|---|---|
| `place-cards.jsx` | approved forms: Sit Down, Walk-By, Decoder Ring (+ ring) × 5 artists | `placecard/round3/` |
| `variants-system.jsx` | V1 Downstream, V2 Wrap, V3 Concertina, V4 Receipt Mass, V5 Line-up Band, V6 Quiet Lockup | `placecard/variants/system/` |
| `variants-fold.jsx` | Ridge, Napkin flag, Crenel, Elbow, Slope, Bridge | `placecard/variants/fold/` |
| `variants-edge.jsx` | Overhang, Halo, Bend, Slot, Pop-up, Drip (name breaks the card edge) | `placecard/variants/edge/` |
| `variants-optic.jsx` | Standup, Relay, Scanimation, Vault, Bar lens, Runway | `placecard/variants/optic/` |

Each `variants/<set>/variants.md` has the idea, construction, ranking and risks of its six variants.
