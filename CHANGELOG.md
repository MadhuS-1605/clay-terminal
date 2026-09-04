# Changelog

## 0.7.3

- Added a Starship prompt preset (`terminal/starship.toml`), generated from the shared coral/warm-gray palette via a new `icons/generate_starship.py` generator. Downloadable, not bundled in the `.vsix` — first item shipped under ROADMAP.md's "CLI / terminal theme support" section.

## 0.7.2

- Added a "Recommended extensions" section to the README (Prettier, Ruff, `golang.go`, `rust-analyzer`, Error Lens), with a matching per-language default-formatter `settings.json` snippet.

## 0.7.1

- Added `icons/palette.py` as the single source of truth for the coral accent (`#D97757`) and warm-gray neutral (`#C3C2B7`) hex values shared across all 4 `themes/*.json` color themes and `icons/generate_icons.py`. `icons/validate_theme.py` now checks both colors stay present in every color theme, to catch drift.

## 0.7.0

- Added a "Get Started with Clay Terminal" walkthrough (`contributes.walkthroughs`), walking through setting the file icon theme, product icon theme, and color variant — addresses the "installed but can't see the icons" confusion, since only the color theme applies automatically on install.

## 0.6.5

- Backfilled changelog entries for 0.6.1-0.6.4.

## 0.6.4

- Added a terminal ANSI color regression guard to `validate_theme.py`.

## 0.6.3

- Fixed dark theme `editorRuler.foreground` to match the indent guide background.

## 0.6.2

- Added Open VSX publishing to the release workflow, so releases now go to both the VS Code Marketplace and Open VSX.
- Added an Open VSX badge to the README.

## 0.6.1

- Added diagnostic scrollbar/gutter marks and unnecessary-code fading to all 4 color theme variants.

## 0.6.0

- Extended `Clay Terminal Icons` file icon theme with Elixir, Zig, Haskell, R, Solidity, Astro, and Prisma.
- Added test explorer colors (`testing.icon*`, `testing.runAction`) to all 4 color theme variants.
- Added notification, debug, and problems-panel colors (`notificationCenter.*`, `debugIcon.*`, `problemsErrorIcon.*`/`problemsWarningIcon.*`) to all 4 color theme variants, so those UI surfaces use the theme's palette instead of VS Code defaults.
- Added a "Recommended settings" section to the README.
- Tuned Marketplace keywords for discoverability.

## 0.5.0

- Added `Clay Terminal Icons` product icon theme — themed chevrons, folder glyphs, and git icons for the editor UI.
- Extended `Clay Terminal Icons` file icon theme with 12 more languages: C, C++, C#, Dart, GraphQL, Kotlin, Lua, PHP, Ruby, Svelte, Swift, Terraform.
- Added `icons/validate_theme.py` and a GitHub Actions workflow to catch broken icon references in CI.

## 0.4.2

- Fixed Marketplace README badges showing "retired badge" — shields.io retired its `visual-studio-marketplace` badge family; switched to `vsmarketplacebadges.dev`.

## 0.4.1

- Expanded `Clay Terminal Icons` to 79 icons: real brand logos (JS/TS/Python/Go/Rust/Docker/Git/ESLint/Prettier/Webpack/Vite/Jest/Babel/...) plus more folder types (api, database, kubernetes, i18n, vendor, coverage, ...).
- Refined icon proportions — bigger centered logos, tighter card margins, closer to a Material Icon Theme look.
- Fixed icon theme not rendering when the extension is dev-installed via symlink (VS Code fails to resolve icon image paths through symlinks); README now recommends installing the packaged `.vsix` instead.

## 0.4.0

- Added `Clay Terminal Icons`, a matching file icon theme (folders + ~30 file types), bundled in this same extension.

## 0.3.0

- Added `Clay Terminal High Contrast` (hc-black) and `Clay Terminal Light High Contrast` (hc-light) theme variants.
- Added README badges (version, installs, rating).

## 0.2.2

- Added dark/light screenshots to the Marketplace README.
- Trimmed `.github/` and `CLAUDE.md` from the packaged `.vsix`.

## 0.2.1

- Added `repository` field to `package.json`.

## 0.2.0

- Added semantic highlighting, expanded token scopes (JSX/tags, decorators, regex, template literals, markdown).
- Added diff/merge editor colors and bracket-pair colorization.
- Added minimap and peek-view colors.
- Added `Clay Terminal Light` variant.
- Added extension icon, `LICENSE`, and packaging metadata.

## 0.1.0

- Initial release: `Clay Terminal` dark theme.
