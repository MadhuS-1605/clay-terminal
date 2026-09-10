"""Generates a Windows Terminal color scheme from the 16-color ANSI palette
already defined in the dark color theme (themes/claude-code-color-theme.json),
so this scheme can never drift from what the theme actually ships.

Distributed as a downloadable asset (terminal/windows-terminal.json), not
bundled in the .vsix -- a VS Code extension can't install a terminal
emulator's settings. First format shipped under ROADMAP.md's "Terminal
emulator color schemes" item (CLI / terminal theme support section);
iTerm2 and Alacritty/Kitty remain for a later cycle.

Run: python3 icons/generate_windows_terminal.py
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
THEME_PATH = os.path.join(ROOT, "..", "themes", "claude-code-color-theme.json")
OUT_PATH = os.path.join(ROOT, "..", "terminal", "windows-terminal.json")

# Windows Terminal color-scheme key -> theme's terminal.ansi* suffix.
ANSI_MAP = {
    "black": "Black", "red": "Red", "green": "Green", "yellow": "Yellow",
    "blue": "Blue", "purple": "Magenta", "cyan": "Cyan", "white": "White",
}

with open(THEME_PATH) as f:
    colors = json.load(f)["colors"]

scheme = {"name": "Clay Terminal"}
for wt_key, ansi_name in ANSI_MAP.items():
    scheme[wt_key] = colors[f"terminal.ansi{ansi_name}"]
    bright_key = "bright" + wt_key[0].upper() + wt_key[1:]
    scheme[bright_key] = colors[f"terminal.ansiBright{ansi_name}"]

scheme["background"] = colors["terminal.background"]
scheme["foreground"] = colors["terminal.foreground"]
scheme["cursorColor"] = colors["terminalCursor.foreground"]
scheme["selectionBackground"] = colors["list.activeSelectionBackground"]

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(scheme, f, indent=2)
        f.write("\n")
    print(f"Wrote {OUT_PATH}")
