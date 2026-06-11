# Versioning

Semver for the tracked `system/` layer.

## Files

| File | Purpose |
|------|---------|
| `system/release/VERSION` | Current system semver |
| `system/release/CHANGELOG.md` | Full release history |
| `README.md` | Recent updates block synced from changelog |

## Bump before every system commit

When you change tracked system files (`system/`, root `README.md`, `.gitignore`):

```bash
python3 system/release/scripts/bump_release.py --bump patch -m "Short summary"
python3 system/release/scripts/check_release.py   # optional
```

One system commit = one semver entry in `CHANGELOG.md`.

## Policy

- **Patch** — docs, fixes, small engine changes
- **Minor** — new engines, layer additions, backward-compatible protocol changes
- **Major** — breaking protocol or bootstrap contract changes
