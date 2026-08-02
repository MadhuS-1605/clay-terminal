# Clay Terminal

[![Version](https://img.shields.io/visual-studio-marketplace/v/astechlabs.cc-theme?label=marketplace)](https://marketplace.visualstudio.com/items?itemName=astechlabs.cc-theme)
[![Installs](https://img.shields.io/visual-studio-marketplace/i/astechlabs.cc-theme)](https://marketplace.visualstudio.com/items?itemName=astechlabs.cc-theme)
[![Rating](https://img.shields.io/visual-studio-marketplace/r/astechlabs.cc-theme)](https://marketplace.visualstudio.com/items?itemName=astechlabs.cc-theme)

VS Code color themes inspired by a coral terminal aesthetic — dark and light variants, built from real warm-gray/coral design tokens. Coral accent (`#D97757`), semantic highlighting, bracket-pair colors, diff/merge colors.

- **Clay Terminal** — dark, near-black warm background
- **Clay Terminal Light** — light, warm off-white background
- **Clay Terminal High Contrast** / **Clay Terminal Light High Contrast** — accessibility-focused variants with stronger borders and higher-contrast text

## Screenshots

| Dark | Light |
| --- | --- |
| ![Clay Terminal dark](https://raw.githubusercontent.com/MadhuS-1605/clay-terminal/main/images/dark.png) | ![Clay Terminal light](https://raw.githubusercontent.com/MadhuS-1605/clay-terminal/main/images/light.png) |

## Install (local dev)

```sh
ln -s "$(pwd)" ~/.vscode/extensions/clay-terminal
```

Reload VS Code, then `Cmd+K Cmd+T` → pick a variant.

## Package for sharing

```sh
npx @vscode/vsce package
```
