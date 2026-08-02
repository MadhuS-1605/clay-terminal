# Clay Terminal — publish workflow

When asked to "push the code" or "publish" in this repo, follow these steps in order (pre-authorized, no need to re-confirm each one):

1. `ghswitch personal` — switch to the `MadhuS-1605` GitHub profile.
2. Update `README.md` to reflect whatever changed.
3. Bump `version` in `package.json` (patch for fixes/tweaks, minor for new features — use judgment based on the diff).
4. Commit and `git push` to `origin/main`.
5. Create and push a release tag matching the new version, e.g. `git tag v0.2.2 && git push origin v0.2.2`. This triggers `.github/workflows/release.yml`, which auto-creates the GitHub Release.
6. `npx @vscode/vsce publish` — publish the new version to the VS Code Marketplace under the `astechlabs` publisher.
7. `ghswitch tachi` — switch back to the `gopher-phoenix` profile.

Marketplace listing: https://marketplace.visualstudio.com/items?itemName=astechlabs.cc-theme
GitHub repo: https://github.com/MadhuS-1605/clay-terminal
