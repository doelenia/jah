# Versioning

How the Jah **kernel** (`system/`) is versioned and released on GitHub.

Local layers (`types/`, `memory/`, `tools/`) are not versioned in this file. They evolve privately on your machine.

## Files

| File | Purpose |
|------|---------|
| `system/VERSION` | Current kernel semver (single line, e.g. `0.2.1`) |
| `system/CHANGELOG.md` | Full release history ([Keep a Changelog](https://keepachangelog.com/)) |
| `README.md` | Open-source landing page with a short **Recent updates** section synced from the changelog |

## When to bump

Bump the kernel version **before every GitHub commit** that changes tracked kernel files (`system/`, root `README.md`, or `.gitignore`).

One commit = one version entry. If you batch several kernel edits, describe them in a single changelog entry.

## Release workflow

1. Finish your kernel edits under `system/` (and `README.md` / `.gitignore` if needed).
2. Run the release script from the repo root:

```bash
python3 system/scripts/bump_release.py --bump patch -m "Short summary of the change"
```

Use `--bump minor` or `--bump major` when the change warrants it (see Semver below).

3. Review the diff: `system/VERSION`, `system/CHANGELOG.md`, and the **Recent updates** block in `README.md`.
4. Commit and push to GitHub.

### Multiple bullet points

```bash
python3 system/scripts/bump_release.py --bump patch \
  -m "Add versioning protocol" \
  -m "Document release workflow in improvement_protocol.md"
```

### Check before push (optional)

Verify that a kernel change includes a version bump:

```bash
python3 system/scripts/check_release.py
```

Exits non-zero if `system/` (or tracked root files) changed since the last release commit without updating `VERSION` / `CHANGELOG.md`.

## Semver policy

| Bump | When |
|------|------|
| **patch** | Docs, clarifications, small fixes — default for most kernel edits |
| **minor** | New protocol features or scripts that do not break existing local setups |
| **major** | Breaking changes to kernel contracts (storage layout, required session fields, compilation rules) |

When in doubt, use **patch**.

## README recent updates

`README.md` contains HTML comment markers:

```markdown
<!-- recent-updates:start -->
...
<!-- recent-updates:end -->
```

`bump_release.py` maintains this block automatically (last five releases). Do not edit it by hand except when fixing mistakes after a failed script run.

## What is tracked on GitHub

See `storage_rules.md`. Tracked paths include `system/**`, `.gitignore`, and `README.md`.

## References

- `system/improvement_protocol.md` — kernel improvement path
- `system/protocol.md` — setup and daily workflow
