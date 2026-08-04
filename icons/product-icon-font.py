"""Builds the Clay Terminal Product Icon Theme: a small custom font covering
only ~8 high-visibility codicon IDs (tree twisties, folder, git dots, tab
close). Any icon not defined here falls back to VS Code's default Codicon
glyph — this is a supported partial-theme approach, not a full ~500-icon
remap.

Glyphs are hand-authored as simple straight-line polygons (chevrons, a
folder silhouette, circles approximated as 16-gons, crossed bars for the
close 'X') via fontTools, the same "draw primitives" approach
generate_icons.py already uses with PIL, just emitted as font outlines
instead of raster pixels.

ponytail: no font-design tool (fontforge) dependency — pure fontTools,
polygon-only glyphs (no bezier curve fitting) to keep this a single
straightforward script.

Run: python3 icons/product-icon-font.py
"""
import json
import math
import os

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

UPM = 1000
ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(ROOT, "clay-product-icons.woff")
THEME_PATH = os.path.join(ROOT, "..", "themes", "clay-product-icon-theme.json")


def rotate(pt, cx, cy, deg):
    a = math.radians(deg)
    x, y = pt[0] - cx, pt[1] - cy
    return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))


def translate(points, dx, dy):
    return [(x + dx, y + dy) for x, y in points]


def circle(cx, cy, r, n=16):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def rect(w, h):
    return [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]


def build_glyph(contours):
    pen = TTGlyphPen(None)
    for c in contours:
        pts = [(round(x), round(y)) for x, y in c]
        pen.moveTo(pts[0])
        for p in pts[1:]:
            pen.lineTo(p)
        pen.closePath()
    return pen.glyph()


GLYPH_ORDER = [
    ".notdef", "chevron-right", "chevron-down", "folder", "folder-opened",
    "circle-filled", "close", "git-branch", "git-commit",
]

glyphs = {".notdef": build_glyph([[(100, 0), (700, 0), (700, 700), (100, 700)]])}

# chevron-right / chevron-down: thick ">" hexagon, rotated 90deg for down
chevron = [(330, 680), (650, 400), (330, 120), (410, 120), (570, 400), (410, 680)]
glyphs["chevron-right"] = build_glyph([chevron])
glyphs["chevron-down"] = build_glyph([[rotate(p, 500, 400, -90) for p in chevron]])

# folder / folder-opened: body + top-left tab silhouette
folder_pts = [(120, 180), (880, 180), (880, 600), (430, 600), (380, 680), (120, 680)]
glyphs["folder"] = build_glyph([folder_pts])
glyphs["folder-opened"] = build_glyph([folder_pts])

# circle-filled
glyphs["circle-filled"] = build_glyph([circle(500, 400, 280)])

# close: two crossed bars
bar = rect(700, 110)
bar1 = translate([rotate(p, 0, 0, 45) for p in bar], 500, 400)
bar2 = translate([rotate(p, 0, 0, -45) for p in bar], 500, 400)
glyphs["close"] = build_glyph([bar1, bar2])

# git-branch: vertical bar + diagonal bar + three circles
vbar = translate(rect(70, 470), 300, 415)
diag = translate([rotate(p, 0, 0, -5.3) for p in rect(382, 70)], 490, 397)
glyphs["git-branch"] = build_glyph([
    vbar, diag, circle(300, 180, 90), circle(300, 650, 90), circle(680, 380, 90),
])

# git-commit: circle with a bar through each side
left_bar = translate(rect(260, 70), 170, 400)
right_bar = translate(rect(260, 70), 830, 400)
glyphs["git-commit"] = build_glyph([left_bar, right_bar, circle(500, 400, 150)])

fb = FontBuilder(UPM, isTTF=True)
fb.setupGlyphOrder(GLYPH_ORDER)
fb.setupCharacterMap({0xEA01 + i: name for i, name in enumerate(GLYPH_ORDER[1:])})
fb.setupGlyf(glyphs)

glyf_table = fb.font["glyf"]
metrics = {}
for name in GLYPH_ORDER:
    g = glyf_table[name]
    lsb = g.xMin if g.numberOfContours > 0 else 0
    metrics[name] = (UPM, lsb)
fb.setupHorizontalMetrics(metrics)
fb.setupHorizontalHeader(ascent=UPM, descent=0)
fb.setupNameTable({"familyName": "Clay Terminal Icons", "styleName": "Regular"})
fb.setupOS2(sTypoAscender=UPM, sTypoDescender=0, usWinAscent=UPM, usWinDescent=0)
fb.setupPost()

fb.font.flavor = "woff"
fb.save(FONT_PATH)

icon_definitions = {
    name: {"fontCharacter": f"\\{hex(0xEA01 + i)[2:]}", "fontId": "clay-icons"}
    for i, name in enumerate(GLYPH_ORDER[1:])
}

theme = {
    "fonts": [
        {
            "id": "clay-icons",
            "src": [{"path": "../icons/clay-product-icons.woff", "format": "woff"}],
            "weight": "normal",
            "style": "normal",
        }
    ],
    "iconDefinitions": icon_definitions,
}

with open(THEME_PATH, "w") as f:
    json.dump(theme, f, indent=2)
    f.write("\n")

print(f"generated {FONT_PATH} and {THEME_PATH} ({len(icon_definitions)} glyphs)")
