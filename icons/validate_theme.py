"""Validates theme JSON: parses cleanly, and every icon/font reference resolves.

Run: python3 icons/validate_theme.py
Exits non-zero on any failure (used in CI).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
THEMES_DIR = os.path.join(ROOT, "..", "themes")

REF_KEYS = (
    "fileExtensions", "fileNames", "folderNames", "folderNamesExpanded",
)
REF_SCALARS = ("file", "folder", "folderExpanded", "rootFolder", "rootFolderExpanded")

ANSI_COLORS = (
    "Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White",
)
TERMINAL_ANSI_KEYS = tuple(
    f"terminal.ansi{variant}{color}"
    for variant in ("", "Bright")
    for color in ANSI_COLORS
)

errors = []

for name in sorted(os.listdir(THEMES_DIR)):
    if not name.endswith(".json"):
        continue
    path = os.path.join(THEMES_DIR, name)
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"{name}: invalid JSON ({e})")
        continue

    if "colors" in data:
        colors = data["colors"]
        for key in TERMINAL_ANSI_KEYS:
            if key not in colors:
                errors.append(f"{name}: missing color theme key '{key}'")

    if "iconDefinitions" not in data:
        continue  # color theme, not an icon theme

    defs = data["iconDefinitions"]
    font_ids = set()

    for font in data.get("fonts", []):
        font_ids.add(font.get("id"))
        for src in font.get("src", []):
            src_path = src.get("path")
            resolved = os.path.normpath(os.path.join(THEMES_DIR, src_path))
            if not os.path.isfile(resolved):
                errors.append(f"{name}: fonts[{font.get('id')}].src -> {src_path} does not exist")

    for key, entry in defs.items():
        icon_path = entry.get("iconPath")
        if icon_path:
            resolved = os.path.normpath(os.path.join(THEMES_DIR, icon_path))
            if not os.path.isfile(resolved):
                errors.append(f"{name}: iconDefinitions.{key}.iconPath -> {icon_path} does not exist")
        font_id = entry.get("fontId")
        if font_id and font_id not in font_ids:
            errors.append(f"{name}: iconDefinitions.{key}.fontId -> '{font_id}' not in fonts")

    for scalar_key in REF_SCALARS:
        ref = data.get(scalar_key)
        if ref and ref not in defs:
            errors.append(f"{name}: {scalar_key} -> '{ref}' not in iconDefinitions")

    for map_key in REF_KEYS:
        for name_key, ref in data.get(map_key, {}).items():
            if ref not in defs:
                errors.append(f"{name}: {map_key}.{name_key} -> '{ref}' not in iconDefinitions")

if errors:
    print(f"FAIL: {len(errors)} issue(s)\n")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print("OK: all theme references resolve")
