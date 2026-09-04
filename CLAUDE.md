# Clay Terminal — publish workflow

When asked to "push the code" or "publish" in this repo, follow these steps in order (pre-authorized, no need to re-confirm each one):

1. Update `README.md` to reflect whatever changed.
2. Bump `version` in `package.json` (patch for fixes/tweaks, minor for new features — use judgment based on the diff).
3. Add a matching `## X.Y.Z` entry at the top of `CHANGELOG.md`, above the previous top entry, summarizing what this release actually shipped. Do this in the same commit as the version bump — every past drift where a release shipped with no changelog entry (see the "Backfilled changelog entries" entries) happened because this step was skipped.
4. Commit and push the change to `origin/main`.
5. Release, using whichever of these two paths the current session supports:
   - **Have real git push + local shell access** (e.g. a session on the maintainer's machine): `ghswitch personal`, then `git tag vX.Y.Z && git push origin vX.Y.Z` (triggers `.github/workflows/release.yml`'s tag-push path, which creates the GitHub Release), then `npx @vscode/vsce publish`, then `ghswitch tachi` to switch back.
   - **GitHub-MCP-only session** (e.g. the automated `clay-terminal-auto-release` routine — no git push credentials, and `marketplace.visualstudio.com` is blocked by egress policy from this kind of session): trigger `release.yml` via `workflow_dispatch` with input `tag: vX.Y.Z` (the GitHub MCP `actions_run_trigger` tool, method `run_workflow`). The workflow itself creates and pushes the tag, creates the GitHub Release, and publishes to the Marketplace using the `VSCE_PAT` repo secret — all from the Actions runner, which isn't subject to this session's network/credential restrictions.

Either path ends with the same result: a matching git tag, GitHub Release, and Marketplace publish. Don't attempt `git push` or `npx vsce publish` directly from a GitHub-MCP-only session — both are blocked there (no push credentials for the former, egress policy for the latter); use the `workflow_dispatch` path instead.

Marketplace listing: https://marketplace.visualstudio.com/items?itemName=astechlabs.cc-theme
GitHub repo: https://github.com/MadhuS-1605/clay-terminal
