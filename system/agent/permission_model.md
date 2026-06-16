# Permission Model

Simple permission levels for Jah sessions and agents.

```txt
L0 think
L1 read approved files
L2 write inside session folder
L3 modify existing principal instances and types (auto allowed)
L4 register new types or modify profile (explicit approval)
L5 modify system/ via GitHub PR with explicit approval
L6 use external service after approval
L7 publish/send/delete/pay only with explicit approval
```

## Session defaults

New sessions set:

- **allowed_write:** session folder; existing principal instances and types
- **requires_approval:**
  - modify personal profile
  - register new types in registry
  - modify system/
  - use external services
  - publish or send anything externally

## Principal auto-update (L3)

Agents may **update existing principal instances and type definitions without asking**, including:

- tasks, context, design docs, rules, preferences, sources, workflows, knowledge-base
- patches to `users/<id>/types/<name>/type.yaml` and README
- principal connectors under `users/<id>/connectors/` (optional)

Record what changed in session `trace.md` with source paths.

**Still requires approval (L4):**

- `users/<id>/personal/profile.md`
- new entries in `registry.yaml` (registering a type that did not exist)

Type-system writes (L3 patches and L4 registry registration) must follow the review protocol in `type_system.md` and matching principal rules — resolve with `resolve-rules` before acting.

## System boundary (L5)

Changes to `system/` require explicit user request and a GitHub PR. Never auto-edit `system/` during ordinary work.

## Proactive capture

Agents gap-fill, capture, and improve during work (`proactive_capture.md`). Apply principal updates directly when the target is an existing instance or type; ask when unsure or when the target is profile, a new registry entry, or `system/`.

## Related docs

- `discovery_protocol.md` — active search and discovery log
- `proactive_capture.md` — gap-fill, capture, improve
