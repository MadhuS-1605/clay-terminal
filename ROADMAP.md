# Roadmap

Current state (v0.7.2): 4 color theme variants (dark, light, hc-black,
hc-light) with semantic highlighting, bracket-pair colors, test explorer,
notification/debug/problems colors, diagnostic scrollbar/gutter marks and
unnecessary-code fading, a 98-icon file icon theme, a scoped 8-glyph
product icon theme, a first-run "Get Started" walkthrough covering both
icon theme pickers and the color theme picker, a single palette source
(`icons/palette.py`) for the coral/warm-gray hex values shared by the
icon generator and all 4 color themes, and CI validation
(`icons/validate_theme.py`) covering both icon themes' references and font
paths, a regression guard asserting all 16 terminal ANSI colors stay
defined in every color theme, and a palette-drift guard asserting the
coral/warm-gray colors stay present in every color theme.

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

- **Terminal emulator color schemes** — a generator script (same pattern as
  `icons/generate_icons.py`) that derives `.itermcolors` (iTerm2),
  Windows Terminal `colorScheme` JSON, and Alacritty/Kitty TOML/conf output
  from `icons/palette.py`. Ships as downloadable assets linked from the
  README, not bundled in the extension package.
- **Shell prompt theme** — a Starship `starship.toml` preset (and
  optionally an Oh My Posh JSON / Powerlevel10k snippet) using the same
  coral accent (`#D97757`) and warm-gray neutrals for prompt segments.
  Same distribution model as the terminal emulator schemes.

## Language tooling integration (formatters, linters, diagnostics)

Not building formatters/linters from scratch — wiring in the established
per-language tools and making VS Code's error/warning rendering match this
theme's palette.

## Explicitly not planned

Generic "add more icons forever" churn, and new build tooling or
dependencies — everything above extends the existing Python generator +
JSON theme pattern already in the repo. The release workflow already
auto-generates GitHub Release notes from commits (`generate_release_notes:
true` in `.github/workflows/release.yml`), so no separate changelog
automation is needed.

## Shipped

### v0.7.2
- Added a "Recommended extensions" section to the README: a curated
  `.vscode/extensions.json` snippet (Prettier, Ruff, `golang.go`,
  rust-analyzer, Error Lens) plus a matching `settings.json` snippet
  (`editor.formatOnSave`, per-language `editor.defaultFormatter`
  overrides). Config/docs only, no extension code. Also notes that Error
  Lens's line/gutter/scrollbar marks inherit this theme's existing
  `editorError`/`editorWarning` red/amber split automatically.

### v0.7.1
- Added `icons/palette.py` as the single source of truth for the coral
  accent (`#D97757`) and warm-gray neutral (`#C3C2B7`) hex values, which
  were previously duplicated by hand across all 4 `themes/*.json` color
  themes and hardcoded again in `icons/generate_icons.py`'s `CLAY`
  constant. `generate_icons.py` now imports `CORAL_RGB` from it instead of
  hardcoding the RGB tuple, and `icons/validate_theme.py` gained a check
  that both palette colors actually appear in every color theme's
  `colors` block, to catch drift. Prerequisite for the terminal-emulator
  and shell-prompt generators later in this file.

### v0.7.0
- Added a "Get Started with Clay Terminal" walkthrough
  (`contributes.walkthroughs`): three steps — "Set File Icon Theme" →
  "Set Product Icon Theme" → "Pick a Color Variant" — each with a command
  button and a completion event tied to the matching setting. Purely
  declarative, no `main`/`activationEvents` added. Directly addresses the
  "installed but can't see the icons" confusion, since only the color
  theme applies automatically on install.

### v0.6.5
- Backfilled `CHANGELOG.md` entries for 0.6.1-0.6.4, which had fallen
  behind actual releases.

### v0.6.4
- Terminal ANSI color regression guard: `icons/validate_theme.py` now
  asserts all 16 `terminal.ansi*` keys (8 colors × normal/Bright) are
  present in every theme JSON's `colors` block, so a future edit can't
  silently drop one. All 4 variants already had all 16; this locks that
  in.

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
