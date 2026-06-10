# Versioning

How the Jah **system** (`system/`) is versioned and released on GitHub.

Principals (`users/`) are not versioned in this file. They evolve privately.

## Files

| File | Purpose |
|------|---------|
| `system/VERSION` | Current system semver |
| `system/CHANGELOG.md` | Full release history |
| `README.md` | Landing page with **Recent updates** synced from changelog |

## When to bump

Bump before every GitHub commit that changes tracked system files (`system/`, `README.md`, `.gitignore`).

## Release workflow

```bash
python3 system/scripts/bump_release.py --bump patch -m "Short summary"
python3 system/scripts/check_release.py   # optional
```

## Semver policy

| Bump | When |
|------|------|
| **patch** | Docs, clarifications, small fixes |
| **minor** | New protocol features without breaking principals |
| **major** | Breaking changes (storage layout, session fields, compilation rules) |

## References

- `improvement_protocol.md` — system improvement path
- `protocol.md` — setup and daily workflow
