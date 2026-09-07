"""Generates an Oh My Posh (https://ohmyposh.dev) prompt theme using the same
coral/warm-gray palette as the color themes and icon set.

Distributed as a downloadable asset (terminal/ohmyposh.json), not bundled in
the .vsix -- a VS Code extension can't install a shell prompt config. See
ROADMAP.md's "CLI / terminal theme support" section (next entry after the
Starship preset shipped in v0.7.3).

Run: python3 icons/generate_ohmyposh.py
"""
import json
import os

from palette import CORAL, WARM_GRAY

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(ROOT, "..", "terminal", "ohmyposh.json")

THEME = {
    "$schema": "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/schema.json",
    "version": 2,
    "blocks": [
        {
            "type": "prompt",
            "alignment": "left",
            "segments": [
                {
                    "type": "path",
                    "style": "plain",
                    "foreground": WARM_GRAY,
                    "properties": {
                        "style": "folder"
                    },
                    "template": "{{ .Path }}",
                },
                {
                    "type": "git",
                    "style": "plain",
                    "foreground": CORAL,
                    "properties": {
                        "branch_icon": " "
                    },
                    "template": " {{ .HEAD }}{{ if .Working.Changed }} *{{ end }}",
                },
                {
                    "type": "text",
                    "style": "plain",
                    "foreground": CORAL,
                    "template": " ❯",
                },
            ],
        }
    ],
    "final_space": True,
}

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(THEME, f, indent=2)
        f.write("\n")
    print(f"Wrote {OUT_PATH}")
