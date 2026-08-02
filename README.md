# Clay Terminal

[![Version](https://img.shields.io/visual-studio-marketplace/v/astechlabs.cc-theme?label=marketplace)](https://marketplace.visualstudio.com/items?itemName=astechlabs.cc-theme)
[![Installs](https://img.shields.io/visual-studio-marketplace/i/astechlabs.cc-theme)](https://marketplace.visualstudio.com/items?itemName=astechlabs.cc-theme)
[![Rating](https://img.shields.io/visual-studio-marketplace/r/astechlabs.cc-theme)](https://marketplace.visualstudio.com/items?itemName=astechlabs.cc-theme)

VS Code color themes inspired by a coral terminal aesthetic — dark and light variants, built from real warm-gray/coral design tokens. Coral accent (`#D97757`), semantic highlighting, bracket-pair colors, diff/merge colors.

- **Clay Terminal** — dark, near-black warm background
- **Clay Terminal Light** — light, warm off-white background
- **Clay Terminal High Contrast** / **Clay Terminal Light High Contrast** — accessibility-focused variants with stronger borders and higher-contrast text
- **Clay Terminal Icons** — a matching file icon theme, included in this same extension (no separate install)

Pairs well with a clean monospace font like JetBrains Mono or Berkeley Mono, though that's a personal editor setting, not something this extension can install for you.

## Screenshots

| Dark | Light |
| --- | --- |
| ![Clay Terminal dark](https://raw.githubusercontent.com/MadhuS-1605/clay-terminal/main/images/dark.png) | ![Clay Terminal light](https://raw.githubusercontent.com/MadhuS-1605/clay-terminal/main/images/light.png) |

## Install (local dev)

Package and install the `.vsix` rather than symlinking — VS Code doesn't reliably resolve an icon theme's image assets through a symlinked dev extension.

```sh
npx @vscode/vsce package
```

Command Palette → **Extensions: Install from VSIX...** → select the generated file, reload VS Code, then Command Palette → **Preferences: Color Theme** to pick a color theme, and **Preferences: File Icon Theme** → **Clay Terminal Icons** for the file icons. (Neither picker has a default keybinding.)
