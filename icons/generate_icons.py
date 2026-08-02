"""Generates the Clay Terminal file/folder icon set as PNGs.

ponytail: raster icons via PIL instead of hand-authored SVGs — good enough at
the ~16-22px explorer display size, one script instead of dozens of art files.
Re-run this after editing PALETTE/ICONS to regenerate icons/*.png.
"""
from PIL import Image, ImageDraw, ImageFont
import os

SIZE = 128
OUT = os.path.dirname(os.path.abspath(__file__))

CLAY = (217, 119, 87)
CLAY_LIGHT = (240, 180, 140)
DARK_TEXT = (26, 26, 25)
WHITE = (255, 255, 255)

def font(size):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def document(fill, label=None, label_color=WHITE, fold=None):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    m = 18  # margin
    fold_size = 26
    d.rounded_rectangle([m, m, SIZE - m, SIZE - m], radius=10, fill=fill)
    fold_color = fold or tuple(max(0, c - 35) for c in fill)
    d.polygon(
        [(SIZE - m - fold_size, m), (SIZE - m, m + fold_size), (SIZE - m - fold_size, m + fold_size)],
        fill=fold_color,
    )

    if label:
        f = font(30 if len(label) <= 2 else 24)
        bbox = d.textbbox((0, 0), label, font=f)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text(((SIZE - w) / 2 - bbox[0], (SIZE - h) / 2 - bbox[1] + 10), label, font=f, fill=label_color)
    return img


def folder(open_=False):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fill = CLAY_LIGHT if open_ else CLAY
    tab_h = 16
    body_top = 40
    d.rounded_rectangle([14, body_top - tab_h, 54, body_top + 4], radius=6, fill=fill)
    if open_:
        d.polygon([(10, body_top), (118, body_top), (108, SIZE - 20), (20, SIZE - 20)], fill=fill)
    else:
        d.rounded_rectangle([10, body_top, 118, SIZE - 20], radius=10, fill=fill)
    return img


# category color, 2-4 char label -> file "kind"
ICONS = {
    "js": ((219, 147, 0), "JS"),
    "jsx": ((219, 147, 0), "JSX"),
    "ts": ((109, 167, 236), "TS"),
    "tsx": ((109, 167, 236), "TSX"),
    "json": ((235, 201, 183), "{ }"),
    "md": ((196, 195, 183), "MD"),
    "py": ((12, 163, 12), "PY"),
    "go": ((98, 153, 135), "GO"),
    "rs": ((217, 119, 87), "RS"),
    "java": ((236, 126, 126), "JV"),
    "html": ((217, 119, 87), "<>"),
    "css": ((130, 125, 189), "CSS"),
    "scss": ((130, 125, 189), "SC"),
    "yaml": ((98, 153, 135), "YML"),
    "toml": ((98, 153, 135), "TML"),
    "txt": ((92, 90, 82), "TXT"),
    "image": ((160, 150, 235), "IMG"),
    "pdf": ((208, 59, 59), "PDF"),
    "lock": ((92, 90, 82), "LK"),
    "env": ((217, 119, 87), "ENV"),
    "docker": ((109, 167, 236), "DKR"),
    "license": ((235, 201, 183), "LIC"),
    "readme": ((217, 119, 87), "RM"),
    "git": ((92, 90, 82), "GIT"),
    "shell": ((26, 26, 25), "SH"),
    "xml": ((235, 201, 183), "XML"),
    "sql": ((98, 153, 135), "SQL"),
    "vue": ((12, 163, 12), "VUE"),
}

os.makedirs(OUT, exist_ok=True)

document((60, 59, 55)).save(f"{OUT}/file-default.png")

for key, (color, label) in ICONS.items():
    document(color, label=label).save(f"{OUT}/file-{key}.png")

folder(open_=False).save(f"{OUT}/folder.png")
folder(open_=True).save(f"{OUT}/folder-open.png")

print("generated", len(ICONS) + 3, "icons in", OUT)
