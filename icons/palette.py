"""Single source of truth for hex/RGB values shared across Clay Terminal's
generators and the 4 themes/*.json color themes.

`CORAL` and `WARM_GRAY` are duplicated by hand today across
themes/claude-code-color-theme.json, -light-, -hc-black-, and
-hc-light-color-theme.json, plus icons/generate_icons.py's own CLAY
constant. This module exists so any future consumer (a terminal-emulator
color scheme generator, a Starship prompt preset — see ROADMAP.md's
"CLI / terminal theme support" section) reads the same values instead of
copy-pasting hex codes again. icons/validate_theme.py checks these values
actually appear in every theme JSON, to catch drift.
"""

CORAL = "#D97757"
CORAL_RGB = (0xD9, 0x77, 0x57)

WARM_GRAY = "#C3C2B7"
WARM_GRAY_RGB = (0xC3, 0xC2, 0xB7)
