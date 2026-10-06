"""
Prepare a photo for clean ASCII conversion:
  1. remove the background (rembg) so only the subject prints
  2. boost local contrast (CLAHE) so a flatly lit face gets highlights/shadows
  3. composite onto pure white (white maps to blank in the ASCII ramp)
  4. crop square around the subject

Output: source-prepped.png (grayscale), consumed by make_ascii_svg.py.
Runs locally only when you change your photo (needs pillow numpy opencv-python rembg).

    python scripts/prep_photo.py <input.jpg> [output.png]
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import new_session, remove

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

CLIP = float(os.environ.get("CLIP", 2.5))        # CLAHE strength
HEAD_ONLY = os.environ.get("HEAD_ONLY", "1") == "1"  # crop to head + shoulders

# 1. cut out the subject
session = new_session(os.environ.get("REMBG_MODEL", "u2net"))  # light model; the default one needs >1GB RAM
cut = remove(Image.open(INP).convert("RGBA"), session=session)
rgb = np.array(cut.convert("RGB"))
alpha = np.array(cut.split()[-1])
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

# 2. local contrast on the subject
clahe = cv2.createCLAHE(clipLimit=CLIP, tileGridSize=(8, 8))
gray = clahe.apply(gray)

# 3. composite on white (feathered a hair to avoid a halo)
mask = cv2.GaussianBlur(alpha.astype(np.float32) / 255.0, (0, 0), 1.0)
out = gray.astype(np.float32) * mask + 255.0 * (1.0 - mask)

# 4. square crop on head + shoulders (face-centred, sized from the subject height)
ys, xs = np.where(alpha > 20)
y0s, y1s = ys.min(), ys.max()
h = y1s - y0s
band = (ys < y0s + 0.45 * h)
cx = int(xs[band].mean())                       # centre on the head, not the shoulders
side = int(float(os.environ.get("CROP", 0.80)) * h)
cy = y0s - int(0.05 * side) + side // 2
canvas = np.full((side, side), 255, np.uint8)
x0, y0 = cx - side // 2, cy - side // 2
sx0, sy0 = max(x0, 0), max(y0, 0)
sx1, sy1 = min(x0 + side, out.shape[1]), min(y0 + side, out.shape[0])
canvas[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = out[sy0:sy1, sx0:sx1].astype(np.uint8)

Image.fromarray(canvas, mode="L").save(OUT)
print("wrote", OUT, canvas.shape)
