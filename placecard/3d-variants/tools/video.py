"""Caption rendered animation frames and encode one MP4 per set.

    python3 video.py RENDER_DIR OUT_DIR [--fps 12]

Each frame gets a bar with the set, the design and the current step's caption.
"""
import json
import math
import pathlib
import subprocess
import sys
import tempfile
import textwrap

from PIL import Image, ImageDraw, ImageFont

FONTS = pathlib.Path(__file__).resolve().parent.parent.parent / "fonts"
F = lambda w, s: ImageFont.truetype(str(FONTS / f"WixMadeforText-{w}.ttf"), s)
INK, MUTED, PANEL, LEMON = (20, 19, 16), (107, 103, 93), (248, 246, 240), (254, 237, 149)
SETS = [("system", "Система"), ("fold", "Сгиб"), ("edge", "Край"), ("optic", "Оптика")]


def caption(meta, fr):
    n = len(meta["steps"])
    if fr["view"] == "seat":
        return "С места гостя", ""
    if fr["t"] <= 0:
        return "Развёртка", "так карточка печатается"
    k = min(n, math.ceil(fr["t"] - 1e-6))
    return f"Шаг {k} из {n}", meta["steps"][k - 1] if k <= len(meta["steps"]) else ""


def main(rd, out, fps=12):
    rd, out = pathlib.Path(rd), pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for sid, stitle in SETS:
        rows = [(json.loads((p.parent / "stills.json").read_text()), p.parent) for p in (rd / sid).glob("*/frames.json")]
        rows.sort(key=lambda r: r[0]["rank"])
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            i = 0
            for meta, d in rows:
                for fr in json.loads((d / "frames.json").read_text()):
                    im = Image.open(d / fr["file"]).convert("RGB")
                    W, H = im.size
                    dr = ImageDraw.Draw(im)
                    dr.rectangle([0, 0, W, 64], fill=PANEL)
                    dr.rectangle([0, 0, 8, 64], fill=LEMON)
                    dr.text((24, 10), f"{stitle} · {meta['rank']}. {meta['design']}", font=F(700, 24), fill=INK)
                    dr.text((24, 40), f"{meta['blurb']}  ·  {meta['artist']}", font=F(500, 15), fill=MUTED)
                    head, body = caption(meta, fr)
                    lines = textwrap.wrap(body, 92)[:2]
                    bh = 44 + 22 * len(lines)
                    dr.rectangle([0, H - bh, W, H], fill=PANEL)
                    dr.text((24, H - bh + 10), head, font=F(700, 19), fill=INK)
                    for j, line in enumerate(lines):
                        dr.text((24, H - bh + 38 + 22 * j), line, font=F(400, 17), fill=MUTED)
                    im.save(tmp / f"f_{i:05d}.png")
                    i += 1
            mp4 = out / f"3d_{sid}.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "f_%05d.png"),
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "22", "-movflags", "+faststart", str(mp4)], check=True)
            print(mp4, i, "frames", f"{i / fps:.0f} s")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], int(a[a.index("--fps") + 1]) if "--fps" in a else 12)
