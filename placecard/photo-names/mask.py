"""Person mask for a photo (white = person), saved as <stem>_mask.png next to it.

    python3 mask.py PHOTO [PHOTO ...]

Uses rembg's human segmentation model (pip install rembg onnxruntime; the model downloads on
first use). Check the mask with overlay.py's _check.png before trusting it.
"""
import pathlib
import sys

from PIL import Image
from rembg import new_session, remove

if __name__ == "__main__":
    s = new_session("u2net_human_seg")
    for p in map(pathlib.Path, sys.argv[1:]):
        m = remove(Image.open(p).convert("RGB"), session=s, only_mask=True, post_process_mask=True)
        out = p.with_name(p.stem + "_mask.png")
        m.save(out)
        print(out, m.size)
