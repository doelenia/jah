# Release Layer

System versioning and repo lifecycle.

| File | Purpose |
|------|---------|
| `VERSION` | Current system semver |
| `CHANGELOG.md` | Release history |
| `versioning.md` | Versioning rules |
| `scripts/init_jah.py` | Bootstrap a principal |
| `scripts/bump_release.py` | Bump version and sync changelog |
| `scripts/check_release.py` | Pre-commit guard for version bumps |

Bump before every system commit:

```bash
python3 system/release/scripts/bump_release.py --bump patch -m "Summary"
```
