# Versioning

Semver for the tracked public tree: `system/`, plus the root license and contribution files.

## Files

| File | Purpose |
|------|---------|
| `system/release/VERSION` | Current system semver |
| `system/release/CHANGELOG.md` | Full release history |
| `README.md` | Recent updates block synced from changelog |
| `LICENSE` | MIT license and copyright |
| `CONTRIBUTING.md` | Issues and pull requests |
| `.github/` | Issue and pull request templates |

## Bump before every system commit

When you change tracked public files (`system/`, root `README.md`, `.gitignore`, `LICENSE`, `CONTRIBUTING.md`, `.github/`):

```bash
python3 system/release/scripts/bump_release.py --bump patch -m "Short summary"
python3 system/release/scripts/check_release.py   # optional
```

One system commit = one semver entry in `CHANGELOG.md`.

## Policy

- **Patch** — docs, fixes, small engine changes
- **Minor** — new engines, layer additions, backward-compatible protocol changes
- **Major** — breaking protocol or bootstrap contract changes
