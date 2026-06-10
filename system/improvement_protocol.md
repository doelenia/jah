# Improvement Protocol

How Jah improves over time.

## Proactive capture

Follow `proactive_capture.md` during every task:

1. **Gap-fill** — ask for missing information.
2. **Capture** — offer reusable facts, workflows, schemas, automations for the principal.
3. **Improve** — offer system or principal fixes when friction appears.

## Two improvement paths

### 1. System changes (`system/`)

Edit `system/`, bump system version (`versioning.md`), commit, GitHub PR:

```bash
python3 system/scripts/bump_release.py --bump patch -m "What changed"
```

One system commit = one semver entry in `system/CHANGELOG.md`.

### 2. Principal customization

| Target | Location |
|--------|----------|
| Personal profile | `users/<id>/personal/profile.md` |
| Preferences | `users/<id>/personal/preferences/` |
| Rules | `users/<id>/personal/rules/` |
| Project context | `users/<id>/projects/<name>/context.md` |
| Workflows | project/personal `workflows/` or `types/<artifact>/workflows/` |
| Registry / types | `users/<id>/registry.yaml`, `users/<id>/types/` |
| Tools | `users/<id>/tools/` |

## Session patch.md

Working proposal — never auto-applied. Review and apply manually.

## References

Cite internal paths or external URLs in `output.md`, `patch.md`, and `trace.md`.

## Personal profile via patch

Profile updates must be proposed in `patch.md` — never auto-written.

## Review gate

Principal changes only after explicit approval. Scripts never modify stable instances automatically.
