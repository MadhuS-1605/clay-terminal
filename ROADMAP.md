# Roadmap

Current state (v0.8.0): 4 color theme variants (dark, light, hc-black,
hc-light) with semantic highlighting, bracket-pair colors, test explorer,
notification/debug/problems colors, diagnostic scrollbar/gutter marks,
quick-fix lightbulb colors, inlay hint colors, symbol icon colors (Outline/
breadcrumbs/suggest widget), and unnecessary-code fading, a 98-icon file icon theme, a scoped 8-glyph
product icon theme, a first-run "Get Started" walkthrough covering both
icon theme pickers and the color theme picker, a single palette source
(`icons/palette.py`) for the coral/warm-gray hex values shared by the
icon generator, all 4 color themes, a Starship prompt preset
(`terminal/starship.toml`), an Oh My Posh prompt theme
(`terminal/ohmyposh.json`), a Powerlevel10k color override
(`terminal/p10k-clay-terminal.zsh`), a Windows Terminal color scheme
(`terminal/windows-terminal.json`), an iTerm2 color preset
(`terminal/clay-terminal.itermcolors`), an Alacritty color scheme
(`terminal/alacritty.toml`), and a Kitty color scheme
(`terminal/kitty.conf`), all downloadable and not bundled in
the extension, and CI validation (`icons/validate_theme.py`) covering both icon themes'
references and font paths, a regression guard asserting all 16 terminal
ANSI colors stay defined in every color theme, and a palette-drift guard
asserting the coral/warm-gray colors stay present in every color theme.

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
terminal emulator's preferences. All items shipped — see Shipped below.

## Language tooling integration (formatters, linters, diagnostics)

Not building formatters/linters from scratch — wiring in the established
per-language tools and making VS Code's error/warning rendering match this
theme's palette. Quick-fix lightbulb colors shipped in v0.7.13; inlay hint
colors shipped in v0.7.14. All grounded gaps in this section are now
shipped.

## Explicitly not planned

Generic "add more icons forever" churn, and new build tooling or
dependencies — everything above extends the existing Python generator +
JSON theme pattern already in the repo. The release workflow already
auto-generates GitHub Release notes from commits (`generate_release_notes:
true` in `.github/workflows/release.yml`), so no separate changelog
automation is needed.

## Shipped

### v0.8.0
- Added `symbolIcon.*` colors (20 keys: class/interface/struct/enumerator/
  enumeratorMember/function/method/constructor/namespace/module/package/
  typeParameter/variable/constant/property/field/keyword/operator/string/
  number) to all 4 color theme variants — these color the symbol-kind icons
  in the Outline view, breadcrumbs, and the suggest/autocomplete widget.
  Each key reuses that theme's existing semantic-token color for the
  matching construct, grouping related kinds onto their nearest semantic
  cousin (struct/enumerator → the theme's type color, module/package → its
  namespace color) — no new hex values introduced. Grounded find for this
  cycle: the active roadmap sections were all either tagged (needs
  go-ahead) or required a human (the icon-theme screenshot), so the theme
  JSON was checked against VS Code's full color-theme key set again, same
  as the v0.7.12-v0.7.14 cycles — `grep -ic symbolIcon` across all 4 theme
  JSON files found zero matches. Kinds without a clean existing semantic
  match (array, boolean, color, event, file, folder, key, null, object,
  reference, snippet, text, unit) were left unset rather than inventing new
  design decisions for them — a future cycle can revisit if a clear mapping
  emerges.

### v0.7.14
- Added `editorInlayHint.foreground`, `editorInlayHint.background`,
  `editorInlayHint.typeForeground`, and `editorInlayHint.parameterForeground`
  (the inlay hints TS/Python/Rust-analyzer show inline for inferred types and
  parameter names) to all 4 color theme variants. Reused each theme's
  existing muted foreground (`descriptionForeground`'s hex) for the general
  hint text, its existing type/class semantic color for `typeForeground`,
  and its existing parameter semantic color for `parameterForeground`, with
  a translucent badge background built from the theme's own
  `editorLineNumber.foreground` hex plus alpha — no new hex values
  introduced. Grounded find for this cycle: the "Language tooling
  integration" section explicitly flagged `editorInlayHint.*` as a real,
  checked-for gap (confirmed via `grep -i inlayHint` across all 4 theme
  JSON files, which found none) left over from the v0.7.13 cycle, and it
  wasn't tagged (needs go-ahead).

### v0.7.13
- Added `editorLightBulb.foreground` and `editorLightBulbAutoFix.foreground`
  (the quick-fix lightbulb icon shown when a linter/formatter/language
  server offers a code action) to all 4 color theme variants, reusing each
  theme's existing `editorWarning.foreground`/`editorInfo.foreground`
  values respectively, matching VS Code's own default semantic split
  (plain suggestion vs. auto-fixable) without introducing new hex values.
  Grounded find for this cycle: the near-term and mid/long-term roadmap
  items were all either tagged (needs go-ahead) or required a human (the
  icon-theme screenshot), so the theme JSON was checked against VS Code's
  full color-theme key set again — these two keys were a real gap directly
  under the previously-empty "Language tooling integration" section.

### v0.7.12
- Added `editorOverviewRuler.infoForeground` (scrollbar mark for info-level
  diagnostics) to all 4 color theme variants, matching each theme's existing
  `editorInfo.foreground`. Grounded find for this cycle: the near-term and
  mid/long-term roadmap items were all either tagged (needs go-ahead) or
  required a human (the icon-theme screenshot), so the repo's own color
  theme JSON was checked against VS Code's actual theme-color set instead.
  The v0.6.1 "diagnostic color polish" pass added `editorOverviewRuler.
  errorForeground`/`.warningForeground` (mirroring `editorError.foreground`/
  `editorWarning.foreground`) but missed the info-level counterpart, even
  though `editorInfo.foreground` itself was already set — confirmed via
  VS Code's source that `editorOverviewRuler.infoForeground` is a real,
  documented color id and that no gutter equivalent exists for info
  (`editorGutter.infoBackground` isn't a real VS Code color, unlike the
  error/warning gutter colors), so gutter marks are correctly left as-is.

### v0.7.11
- Shipped the ligature-font-friendly half of the "Extension pack
  recommendation" item: added `editor.fontLigatures: true` to the README's
  "Recommended settings" snippet, with a note that JetBrains Mono/Berkeley
  Mono (already recommended there) ship ligature glyphs for `=>`, `!=`,
  `>=` and similar. The `.vscode/extensions.json` half of that item was
  already covered by the "Recommended extensions" section added in v0.7.2,
  so the roadmap item is now fully shipped. Doc/config only, no code.

### v0.7.10
- Added a Powerlevel10k color override (`terminal/p10k-clay-terminal.zsh`),
  generated by `icons/generate_p10k.py` from the shared `icons/palette.py`
  coral/warm-gray values. Unlike the other prompt/terminal generators, this
  doesn't produce a full replacement config — Powerlevel10k's own
  `~/.p10k.zsh` is a large file from its `p10k configure` wizard — so it's a
  small snippet meant to be sourced *after* it, overriding just the
  directory/git/prompt-character colors (`POWERLEVEL9K_DIR_FOREGROUND`,
  `POWERLEVEL9K_VCS_*_FOREGROUND`, `POWERLEVEL9K_PROMPT_CHAR_*_FOREGROUND`).
  Downloadable from the README, excluded from the `.vsix` via
  `.vscodeignore`. Last format under the "CLI / terminal theme support"
  roadmap item, after Starship in v0.7.3 and Oh My Posh in v0.7.5 — that
  roadmap item is now fully shipped.

### v0.7.9
- Added a Kitty color scheme (`terminal/kitty.conf`), generated by
  `icons/generate_kitty.py` directly from the dark theme's own
  `terminal.ansi*` colors (no duplicated hex values). Fourth and final
  format under the "Terminal emulator color schemes" roadmap item, after
  Windows Terminal in v0.7.6, iTerm2 in v0.7.7, and Alacritty in v0.7.8 —
  downloadable from the README, excluded from the `.vsix` via
  `.vscodeignore`. That roadmap item is now fully shipped.

### v0.7.8
- Added an Alacritty color scheme (`terminal/alacritty.toml`), generated by
  `icons/generate_alacritty.py` directly from the dark theme's own
  `terminal.ansi*` colors (no duplicated hex values). Third format under
  the "Terminal emulator color schemes" roadmap item, after Windows
  Terminal in v0.7.6 and iTerm2 in v0.7.7 — downloadable from the README,
  excluded from the `.vsix` via `.vscodeignore`. Kitty format remains for
  a later cycle.

### v0.7.7
- Added an iTerm2 color preset (`terminal/clay-terminal.itermcolors`),
  generated by `icons/generate_itermcolors.py` directly from the dark
  theme's own `terminal.ansi*` colors (no duplicated hex values), using
  Python's `plistlib` to write a valid iTerm2 property list. Second format
  under the "Terminal emulator color schemes" roadmap item, after Windows
  Terminal in v0.7.6 — downloadable from the README, excluded from the
  `.vsix` via `.vscodeignore`. Alacritty and Kitty formats remain for a
  later cycle.

### v0.7.6
- Added a Windows Terminal color scheme (`terminal/windows-terminal.json`),
  generated by `icons/generate_windows_terminal.py` directly from the dark
  theme's own `terminal.ansi*` colors (no duplicated hex values). First
  format under the "Terminal emulator color schemes" roadmap item —
  downloadable from the README, excluded from the `.vsix` via
  `.vscodeignore`. iTerm2 and Alacritty/Kitty formats remain for a later
  cycle.

### v0.7.5
- Added an Oh My Posh (https://ohmyposh.dev) prompt theme
  (`terminal/ohmyposh.json`), generated by `icons/generate_ohmyposh.py` from
  the shared `icons/palette.py` coral/warm-gray values: coral git-branch
  segment and prompt character, warm-gray path segment. Second entry under
  the "CLI / terminal theme support" roadmap section, following the same
  distribution model as the Starship preset — downloadable from the README,
  excluded from the `.vsix` via `.vscodeignore`.

### v0.7.3
- Added a Starship (https://starship.rs) prompt preset
  (`terminal/starship.toml`), generated by `icons/generate_starship.py`
  from the shared `icons/palette.py` coral/warm-gray values: coral prompt
  character/git-branch/git-status, warm-gray directory/duration segments.
  First entry under the "CLI / terminal theme support" roadmap section —
  downloadable from the README, excluded from the `.vsix` via
  `.vscodeignore` since a VS Code extension can't install a shell config.

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
