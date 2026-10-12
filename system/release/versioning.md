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

**Default: patch (the last digit) for every release.** That covers docs, fixes, engine changes, new engines, and protocol additions alike.

- **Minor (second digit) or major (first digit) only when the principal explicitly says so.** Agents never choose them on their own, however large the change looks.
- `bump_release.py` enforces this: `--bump minor` or `--bump major` is refused unless `--principal-approved "<the principal's instruction, with date>"` is passed. The cited instruction appears in the agent's session trace.
- If unsure, use patch and mention in the PR that the principal can request a minor/major bump.
