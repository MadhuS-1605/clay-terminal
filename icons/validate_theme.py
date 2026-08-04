"""Validates theme JSON: parses cleanly, and every icon reference resolves.

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

    if "iconDefinitions" not in data:
        continue  # color theme, not an icon theme

    defs = data["iconDefinitions"]

    for key, entry in defs.items():
        icon_path = entry.get("iconPath")
        if not icon_path:
            continue
        resolved = os.path.normpath(os.path.join(THEMES_DIR, icon_path))
        if not os.path.isfile(resolved):
            errors.append(f"{name}: iconDefinitions.{key}.iconPath -> {icon_path} does not exist")

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
