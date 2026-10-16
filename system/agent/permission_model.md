# Permission Model

Simple permission levels for Jah sessions and agents.

```txt
L0 think
L1 read approved files
L2 write inside session folder
L3 modify existing principal instances and types (auto allowed)
L4 register new types or modify profile (clear request that names the action)
L5 modify system/ via GitHub PR (clear request that names system/)
L6 use external service (clear request that names the service)
L7 publish/send/delete/pay (clear request that names the action)
```

## Session defaults

New sessions set:

- **allowed_write:** session folder; existing principal instances and types
- **standing contracts** (a clear current request that names the action is the approval; pause only for a warning — `agency.md`):
  - modify personal profile
  - register new types in registry
  - modify system/
  - use external services
  - publish, send, delete, or pay

Jah has no ethical permission class. Agent disapproval is not a reason to refuse or to pause.

## Principal auto-update (L3)

Agents may **update existing principal instances and type definitions without asking**, including:

- tasks, context, design docs, rules, preferences, sources, workflows, knowledge-base
- patches to `users/<id>/types/<name>/type.yaml` and README
- principal connectors under `users/<id>/connectors/` (optional)

Record what changed in session `trace.md` with source paths.

**Standing contracts (L4).** A clear current request that names the action is the approval. Do not ask a second time. Pause only for a warning when the intention is unclear:

- `users/<id>/personal/profile.md`
- new entries in `registry.yaml` (registering a type that did not exist)

Type-system writes (L3 patches and L4 registry registration) must follow the review protocol in `type_system.md` and matching principal rules — resolve with `resolve-rules` before acting.

## System boundary (L5)

Changes to `system/` require a current request that names `system/`, and a GitHub PR. A clear request is the approval. Never auto-edit `system/` during ordinary work.

## Proactive capture

Agents gap-fill, capture, and improve during work (`proactive_capture.md`). Apply principal updates directly when the target is an existing instance or type. Profile, a new registry entry, or `system/` proceeds when the current request names that action. When the intention is unclear, warn and wait (`agency.md`).

## Related docs

- `agency.md` — suggestion, warning, and provider block
- `discovery_protocol.md` — active search and discovery log
- `proactive_capture.md` — gap-fill, capture, improve
