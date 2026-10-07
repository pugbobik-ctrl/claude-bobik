"""Compose rendered stills into one assembly sheet per set.

    python3 sheets.py RENDER_DIR OUT_DIR

Each row: rank, name and idea on the left, then the flat sheet, every step half way,
the finished card and the view from the guest's seat, each with its caption.
"""
import json
import pathlib
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

FONTS = pathlib.Path(__file__).resolve().parent.parent.parent / "fonts"
F = lambda w, s: ImageFont.truetype(str(FONTS / f"WixMadeforText-{w}.ttf"), s)
INK, MUTED, BG, LEMON = (20, 19, 16), (107, 103, 93), (244, 242, 236), (254, 237, 149)
SETS = [("system", "Система"), ("fold", "Сгиб"), ("edge", "Край"), ("optic", "Оптика")]


def main(rd, out):
    rd, out = pathlib.Path(rd), pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    TW, TH = 420, 280          # tile
    LW = 330                    # label column
    CAP = 92                    # caption band under tiles
    for sid, stitle in SETS:
        rows = [(json.loads(p.read_text()), p.parent) for p in (rd / sid).glob("*/stills.json")]
        rows = sorted(rows, key=lambda r: r[0]["rank"])
        if not rows:
            continue
        cols = max(len(r[0]["stills"]) for r in rows)
        W = LW + cols * (TW + 12) + 24
        H = 110 + len(rows) * (TH + CAP + 24)
        im = Image.new("RGB", (W, H), BG)
        dr = ImageDraw.Draw(im)
        dr.rectangle([0, 0, 10, H], fill=LEMON)
        dr.text((36, 30), f"{stitle} · сборка в 3D", font=F(700, 40), fill=INK)
        dr.text((36, 78), f"Dinner · 10.10.2026 · посадочные карточки · {rows[0][0]['artist']}", font=F(500, 20), fill=MUTED)
        y = 110
        for meta, d in rows:
            dr.text((36, y + 4), str(meta["rank"]), font=F(700, 34), fill=INK)
            dr.text((80, y + 8), meta["design"], font=F(700, 28), fill=INK)
            yy = y + 50
            for line in textwrap.wrap(meta["blurb"], 26):
                dr.text((80, yy), line, font=F(500, 19), fill=MUTED); yy += 26
            x = LW
            for st in meta["stills"]:
                tile = Image.open(d / st["file"]).convert("RGB")
                tile.thumbnail((TW, TH))
                im.paste(tile, (x, y))
                dr.text((x, y + TH + 8), st["label"], font=F(700, 18), fill=INK)
                cy = y + TH + 32
                for line in textwrap.wrap(st.get("caption", ""), 46)[:3]:
                    dr.text((x, cy), line, font=F(400, 15), fill=MUTED); cy += 19
                x += TW + 12
            y += TH + CAP + 24
        im.save(out / f"3d_{sid}.png", optimize=True)
        print(out / f"3d_{sid}.png", im.size)


if __name__ == "__main__":
    main(*sys.argv[1:3])
