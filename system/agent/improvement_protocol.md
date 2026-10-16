# Improvement Protocol

How Jah improves over time.

## Proactive capture

Follow `proactive_capture.md` during every task:

1. **Gap-fill** — ask for missing information; run active discovery (`discovery_protocol.md`).
2. **Capture** — promote reusable facts, workflows, schemas, automations to the principal.
3. **Improve** — fix principal friction directly; offer system fixes only after user asks.

## Two improvement paths

### 1. System changes (`system/`)

Edit `system/`, bump system version (`versioning.md`: patch by default; minor/major only on the principal's explicit instruction), commit, GitHub PR:

```bash
python3 system/release/scripts/bump_release.py --bump patch -m "What changed"
```

One system commit = one semver entry in `system/release/CHANGELOG.md`.

**Requires explicit user request** — never auto-edit `system/` during ordinary sessions.

### 2. Principal customization

| Target | Location | Approval |
|--------|----------|----------|
| Personal profile | `users/<id>/personal/profile.md` | Clear request (`agency.md`) |
| Preferences | `users/<id>/personal/preferences/` | Auto (existing) |
| Rules | `users/<id>/personal/rules/` | Auto (existing) |
| Project context | `users/<id>/projects/<name>/context.md` | Auto (existing) |
| Workflows | project/personal `workflows/` or `types/<artifact>/workflows/` | Auto |
| Knowledge entries | `users/<id>/knowledge-base/` | Auto (existing) |
| Registry / types | `users/<id>/registry.yaml`, `users/<id>/types/` | New registry entry = clear request; patch existing = auto |
| Connectors | `users/<id>/connectors/` (optional) | Auto |

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

Do not auto-write profile. A clear request that names the profile change is the approval; apply it and record the change in `trace.md`. Use `patch.md` when proposing a profile change the principal has not asked for.

## Review gate

- **Profile and new registry types** — a clear request that names the action is the approval (`agency.md`). Do not ask a second time.
- **System** — a clear request that names `system/`, plus a GitHub PR.
- **Existing principal instances and types** — agents may apply during work; user reviews via git diff and session `trace.md`.
