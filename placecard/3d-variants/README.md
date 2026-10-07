# 3D: how the place-card variants are assembled

`site/` is an interactive viewer for the 24 layout variants (system, fold, edge, optic) and
all five artists. Each flat final SVG is printed onto the card as a texture, cut into panels
along its creases and folded step by step onto the table, with plate and other props.
Views: from the guest's seat (eye 430 mm up, 450 mm away), around, side, top.

- `FOLDSPEC.md`: the fold spec format; specs live in `placecard/variants/<set>/fold3d/`.
- `fold.js` (fold engine), `scene.js` (table, light, views), `index.html` (viewer), `shot.html`.
- `tools/check_spec.py`: validate specs. `tools/shot.cjs`: screenshot one spec.
- `tools/textures.py`: SVG -> texture. `tools/build.py site ../variants/{system,fold,edge,optic}`: build the site.
- `tools/page_shot.cjs`: screenshot the built site.

Limits: no board thickness or springback, curved bends are narrow strips, the acrylic bar
does not refract, the scanimation grille is averaged rather than resolved.
