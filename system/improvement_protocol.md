# Improvement Protocol

How Jah improves over time.

## Proactive capture

Follow `proactive_capture.md` during every task:

1. **Gap-fill** — ask for missing information; run active discovery (`discovery_protocol.md`).
2. **Capture** — promote reusable facts, workflows, schemas, automations to the principal.
3. **Improve** — fix principal friction directly; offer system fixes only after user asks.

## Two improvement paths

### 1. System changes (`system/`)

Edit `system/`, bump system version (`versioning.md`), commit, GitHub PR:

```bash
python3 system/scripts/bump_release.py --bump patch -m "What changed"
```

One system commit = one semver entry in `system/CHANGELOG.md`.

**Requires explicit user request** — never auto-edit `system/` during ordinary sessions.

### 2. Principal customization

| Target | Location | Approval |
|--------|----------|----------|
| Personal profile | `users/<id>/personal/profile.md` | Ask |
| Preferences | `users/<id>/personal/preferences/` | Auto (existing) |
| Rules | `users/<id>/personal/rules/` | Auto (existing) |
| Project context | `users/<id>/projects/<name>/context.md` | Auto (existing) |
| Workflows | project/personal `workflows/` or `types/<artifact>/workflows/` | Auto |
| Registry / types | `users/<id>/registry.yaml`, `users/<id>/types/` | New registry entry = ask; patch existing = auto |
| Tools | `users/<id>/tools/` | Auto |

Agents update existing principal targets directly and log changes in `trace.md`.

## Session patch.md

Use `patch.md` for:

- Profile update proposals
- New registry type proposals
- System change proposals (reference for PR)
- Deferred offers the user declined

Principal instance and type updates do not require `patch.md` when applied directly.

## References

Cite internal paths or external URLs in `output.md`, `evaluation.md`, `trace.md`, and `patch.md`.

## Personal profile via patch

Profile updates must be proposed in `patch.md` — never auto-written.

## Review gate

- **Profile and new registry types** — explicit approval only.
- **System** — explicit request + GitHub PR.
- **Existing principal instances and types** — agents may apply during work; user reviews via git diff and session `trace.md`.
