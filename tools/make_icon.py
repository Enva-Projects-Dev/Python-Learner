"""Baut build/icon.ico: schwarzes quadrat, goldenes PL in Bebas Neue."""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "app", "ui", "vendor", "fonts",
                    "BebasNeue-Regular.ttf")
OUT = os.path.join(ROOT, "build", "icon.ico")
GOLD = (217, 165, 58)   # #d9a53a
BLACK = (10, 10, 10)    # #0a0a0a


def main():
    size = 256
    img = Image.new("RGB", (size, size), BLACK)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, int(size * 0.62))
    text = "PL"
    box = draw.textbbox((0, 0), text, font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    draw.text(((size - w) / 2 - box[0], (size - h) / 2 - box[1]),
              text, font=font, fill=GOLD)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, sizes=[(16, 16), (32, 32), (48, 48), (64, 64),
                         (128, 128), (256, 256)])
    print(OUT)


if __name__ == "__main__":
    main()
