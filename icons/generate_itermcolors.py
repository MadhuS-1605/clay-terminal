"""Generates an iTerm2 .itermcolors color preset from the 16-color ANSI
palette already defined in the dark color theme
(themes/claude-code-color-theme.json), so this preset can never drift from
what the theme actually ships.

Distributed as a downloadable asset (terminal/clay-terminal.itermcolors),
not bundled in the .vsix -- a VS Code extension can't install a terminal
emulator's preferences. Second format shipped under ROADMAP.md's "Terminal
emulator color schemes" item (CLI / terminal theme support section), after
Windows Terminal in v0.7.6; Alacritty/Kitty remain for a later cycle.

Run: python3 icons/generate_itermcolors.py
"""
import json
import os
import plistlib

ROOT = os.path.dirname(os.path.abspath(__file__))
THEME_PATH = os.path.join(ROOT, "..", "themes", "claude-code-color-theme.json")
OUT_PATH = os.path.join(ROOT, "..", "terminal", "clay-terminal.itermcolors")

# ANSI slot index -> theme's terminal.ansi* suffix. 0-7 normal, 8-15 bright,
# in the standard black/red/green/yellow/blue/magenta/cyan/white order.
ANSI_NAMES = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]


def hex_to_component(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return {
        "Color Space": "sRGB",
        "Red Component": r,
        "Green Component": g,
        "Blue Component": b,
        "Alpha Component": 1.0,
    }


with open(THEME_PATH) as f:
    colors = json.load(f)["colors"]

preset = {}
for i, name in enumerate(ANSI_NAMES):
    preset[f"Ansi {i} Color"] = hex_to_component(colors[f"terminal.ansi{name}"])
    preset[f"Ansi {i + 8} Color"] = hex_to_component(colors[f"terminal.ansiBright{name}"])

preset["Background Color"] = hex_to_component(colors["terminal.background"])
preset["Foreground Color"] = hex_to_component(colors["terminal.foreground"])
preset["Bold Color"] = hex_to_component(colors["terminal.foreground"])
preset["Cursor Color"] = hex_to_component(colors["terminalCursor.foreground"])
preset["Cursor Text Color"] = hex_to_component(colors["terminal.background"])
preset["Selection Color"] = hex_to_component(colors["list.activeSelectionBackground"])
preset["Selected Text Color"] = hex_to_component(colors["terminal.foreground"])

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "wb") as f:
        plistlib.dump(preset, f, fmt=plistlib.FMT_XML)
    print(f"Wrote {OUT_PATH}")
