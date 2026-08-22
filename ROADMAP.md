# Roadmap

Current state (v0.6.3): 4 color theme variants (dark, light, hc-black,
hc-light) with semantic highlighting, bracket-pair colors, test explorer,
notification/debug/problems colors, diagnostic scrollbar/gutter marks and
unnecessary-code fading, a 98-icon file icon theme, a scoped 8-glyph
product icon theme, and CI validation (`icons/validate_theme.py`) covering
both icon themes' references and font paths.

This file is read and updated by the automated release process (see
`.github/workflows` and the `clay-terminal-auto-release` cloud routine).
Conventions it follows, so keep them when hand-editing too:

- Items tagged **(needs go-ahead)** are intentionally not picked up
  automatically — they require new extension infrastructure (e.g. the
  extension's first activation script) or are speculative features to
  build only if a user actually asks. A human decides when those move
  forward, not the automated loop.
- Everything else is fair game for a small, additive, declarative change.
- Finished items move to **Shipped**, most recent first, instead of
  staying in the active sections — keeps this file focused on what's next.
- New ideas get added the same way they were originally: grounded in an
  actual check of the current repo state (grep/read the theme JSON,
  confirm a gap really exists), not generic theme-extension filler.

## Near-term

- **Icon theme screenshot in README** — only `images/dark.png` and
  `images/light.png` exist today, both color-theme-only. Needs an actual
  VS Code screenshot with the icon theme applied, which can't be captured
  headlessly — left for a human to grab and drop into `images/`.

## Mid-term

- **Light-tuned icon variant (needs go-ahead)** — a second icon set matched
  to the light color theme's contrast (currently one shared icon set
  across dark/light). Don't build speculatively — wait for a request.
- **Terminal ANSI color regression guard** — extend
  `icons/validate_theme.py` (or a sibling check) to assert all 16
  `terminal.ansi*` keys stay present in every color theme on every change.
  All 4 variants already have all 16 today; this locks that in rather than
  fixing an existing gap.

## Long-term / optional

- **Icon theme packs (needs go-ahead)** — an opt-in colorful vs.
  monochrome file icon toggle via a second `iconThemes` entry. Only build
  if users actually ask; avoid speculative branching.
- **Visual regression testing** for theme rendering (e.g. headless VS Code
  snapshots). High effort — only worth it if rendering bugs start
  recurring in practice.

## Features beyond color/icons

The extension is currently pure declarative JSON — no `main` entry point or
`activationEvents` in `package.json`, so nothing runs extension-host code
today. That caps what's possible without adding a build step:

- **Setup walkthrough** (`contributes.walkthroughs`) — a guided onboarding
  page ("Set File Icon Theme" → "Set Product Icon Theme" → "Pick a color
  variant") shown on first install. This is declarative, like themes and
  icon themes — no JS/activation code needed. Directly addresses the
  "installed but can't see the icons" confusion from earlier setup
  sessions, where users didn't know both the icon theme *and* product icon
  theme need to be selected separately.
- **Extension pack recommendation** (`extensionPack` or
  `extensionRecommendations` in a workspace `.vscode/extensions.json`
  template) — suggest a ligature-font-friendly setup alongside the theme,
  the way Material Theme and One Dark Pro do. Doc/config only.
- **Command + status bar theme switcher (needs go-ahead)**
  (`contributes.commands` + `StatusBarItem`) — a quick command to cycle
  dark/light/hc variants. This *does* require adding a real activation
  script (the extension's first bit of runtime code), which is a bigger
  structural change than anything else in this repo — worth doing only if
  users ask for it, not speculatively.

## CLI / terminal theme support

Extends the same coral/warm-gray palette to the actual terminal, not just
VS Code's built-in terminal panel. Lives as generated config files, not as
part of the `.vsix` — a VS Code extension can't install a shell config or a
terminal emulator's preferences.

- **Single palette source** — prerequisite for both items below: extract
  the raw hex values currently duplicated across the 4 `themes/*.json`
  files into one shared palette file (e.g. `icons/palette.py` or a JSON
  constants file) that both `generate_icons.py` and the new
  terminal/prompt generators read from. Do this first, before adding more
  consumers of the palette.
- **Terminal emulator color schemes** — a generator script (same pattern as
  `icons/generate_icons.py`) that derives `.itermcolors` (iTerm2),
  Windows Terminal `colorScheme` JSON, and Alacritty/Kitty TOML/conf output
  from the single palette source. Ships as downloadable assets linked from
  the README, not bundled in the extension package.
- **Shell prompt theme** — a Starship `starship.toml` preset (and
  optionally an Oh My Posh JSON / Powerlevel10k snippet) using the same
  coral accent (`#D97757`) and warm-gray neutrals for prompt segments.
  Same distribution model as the terminal emulator schemes.

## Language tooling integration (formatters, linters, diagnostics)

Not building formatters/linters from scratch — wiring in the established
per-language tools and making VS Code's error/warning rendering match this
theme's palette. Three pieces:

- **Recommended formatter/linter pack** — a curated
  `extensionRecommendations` list (Prettier for JS/TS/CSS/JSON, Black or
  Ruff for Python, gofmt/`golang.go` for Go, rustfmt for Rust, etc.) plus
  a documented `settings.json` snippet
  (`editor.defaultFormatter`, `editor.formatOnSave`, per-language
  `[python]`/`[go]` overrides) in the README. This is config/docs only —
  no new code, just pointing users at the right existing extension per
  language instead of reinventing formatting.
- **Recommend Error Lens for full-line highlighting** — theme colors alone
  can mark the gutter/scrollbar next to an error line, but a highlighted
  *whole-line background* with the error message inline is a decoration,
  not a static theme color; stock VS Code doesn't expose one. The
  established tool for this is the Error Lens extension, which reads the
  same `editorError`/`editorWarning` colors this theme already sets —
  errors and warnings already use distinct hues (red vs. amber), so Error
  Lens's line highlight, gutter mark, and scrollbar mark all inherit that
  same red/amber split automatically. Add it to the recommended pack above
  rather than building a custom decoration provider.

## Explicitly not planned

Generic "add more icons forever" churn, and new build tooling or
dependencies — everything above extends the existing Python generator +
JSON theme pattern already in the repo. The release workflow already
auto-generates GitHub Release notes from commits (`generate_release_notes:
true` in `.github/workflows/release.yml`), so no separate changelog
automation is needed.

## Shipped

### v0.6.3
- Indent guide / ruler consistency check: the dark theme's
  `editorRuler.foreground` (`#26261f`) didn't match
  `editorIndentGuide.background1` (`#2e2d27`), unlike the other 3 variants
  where ruler foreground and indent guide background are the same color.
  Fixed the dark theme to follow the same pattern.

### v0.6.2
- Added an Open VSX Registry badge and publish step, so the extension is
  also available outside the VS Code Marketplace.

### v0.6.1
- Diagnostic color polish: added `editorOverviewRuler.errorForeground`/
  `.warningForeground` (scrollbar marks) and `editorGutter.errorBackground`/
  `.warningBackground` (gutter strip) to all 4 color theme variants, so a
  squiggle, its scrollbar mark, and its gutter mark all point at the same
  line consistently. Also added `editorUnnecessaryCode.opacity` (fades
  unused imports/dead code) to the dark and light variants, and
  `editorUnnecessaryCode.border` to the two high-contrast variants per VS
  Code's accessibility guidance (fading isn't appropriate in HC themes).

### v0.6.0
- Extended the file icon theme with Elixir, Zig, Haskell, R, Solidity,
  Astro, and Prisma.
- Added test explorer colors to all 4 color theme variants.
- Added notification, debug, and problems-panel colors to all 4 color
  theme variants.
- Added a "Recommended settings" section to the README.
- Tuned Marketplace keywords for discoverability.

### v0.5.0
- Added the `Clay Terminal Icons` product icon theme (chevrons, folders,
  git glyphs).
- Extended the file icon theme with 12 more languages: C, C++, C#, Dart,
  GraphQL, Kotlin, Lua, PHP, Ruby, Svelte, Swift, Terraform.
- Added `icons/validate_theme.py` and a GitHub Actions CI workflow.
