#!/usr/bin/env python3
"""Build round token images from the square portraits.

Every PNG in build/art/portraits/ becomes build/art/tokens/<same name>:
a 512x512 circular crop with a yellow-orange ring border and a transparent
background — what a token should look like when dragged onto a scene.

Idempotent and cheap; release.sh runs it before the pack build, so new
portraits get tokens automatically.

Run from the repo root:  python3 tools/make_tokens.py
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "build", "art", "portraits")
OUT = os.path.join(ROOT, "build", "art", "tokens")

SIZE = 512          # final token size
SS = 4              # supersample factor for smooth edges
RING = 22           # ring border thickness at final size
EDGE = 3            # darker edge line thickness at final size

RING_COLOR = (240, 160, 48, 255)    # yellow-orange
EDGE_COLOR = (179, 106, 20, 255)    # darker rim, inside and outside


def make_token(src_path, out_path):
    img = Image.open(src_path).convert("RGBA")

    # center-crop to square, then upscale to the supersampled working size
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2,
                    (w - side) // 2 + side, (h - side) // 2 + side))
    big = SIZE * SS
    img = img.resize((big, big), Image.LANCZOS)

    # circular mask for the artwork (inner circle, inside the ring)
    inner_r = (SIZE // 2 - RING) * SS
    center = big // 2
    mask = Image.new("L", (big, big), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([center - inner_r, center - inner_r,
               center + inner_r, center + inner_r], fill=255)

    token = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    token.paste(img, (0, 0), mask)

    # ring: filled annulus with darker edge lines inside and out
    d = ImageDraw.Draw(token)
    outer_r = (SIZE // 2) * SS
    def circle(r, color, width):
        d.ellipse([center - r, center - r, center + r, center + r],
                  outline=color, width=width)
    # main ring body
    ring_w = RING * SS
    circle(outer_r - ring_w // 2, RING_COLOR, ring_w)
    # edge lines
    edge_w = EDGE * SS
    circle(outer_r - edge_w // 2, EDGE_COLOR, edge_w)
    circle(outer_r - ring_w + edge_w // 2, EDGE_COLOR, edge_w)

    token = token.resize((SIZE, SIZE), Image.LANCZOS)
    token.save(out_path)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for f in sorted(os.listdir(SRC)):
        if f.lower().endswith(".png"):
            make_token(os.path.join(SRC, f), os.path.join(OUT, f))
            n += 1
    print(f"tokens: {n} written to build/art/tokens/")
