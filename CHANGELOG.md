# Changelog

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
