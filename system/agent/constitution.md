# Constitution

Meta-rules for how Jah agents discover and apply rules. **Agent-agnostic** — applies in Cursor, Claude Code, CLI, or any future bridge.

These invariants are always on. They tell agents *how to find* applicable rules, not what every rule says. Load rule bodies on demand via the Rule Index in compiled context and `resolve-rules` (see `context_compilation.md`).

## Privilege order

When instructions conflict, higher privilege wins:

1. **Constitution** (this file)
2. **Permission model** (`permission_model.md`) — L2–L7 write boundaries
3. **Principal rules** — `personal/rules/`, project `rules/`
4. **User message** — current turn intent

Lower `priority` number on a rule = higher privilege among principal rules.

## Invariants

| # | Rule | When |
|---|------|------|
| C1 | **Resolve before write** — read `instance.yaml` → type → README for every write target in this turn | `pre_write` |
| C2 | **Re-orient on scope shift** — when write target, instance type, project, or approval class changes, resolve applicable rules before the next action | `topic_shift` |
| C3 | **Privilege wins** — on conflict, follow higher-privilege instruction; note suppressed rule in `trace.md` | always |
| C4 | **Search, don't infer** — if behavior is not declared in docs already read, search or `resolve-knowledge` before acting; do not infer from folder names | `uncertainty` |
| C5 | **Checkpoint external actions** — before profile, new registry entry, `system/` edit, or publish: re-read `permission_model.md` for that action class | `pre_approval` |
| C6 | **Attest at boundaries** — after resolving rules at a checkpoint, log active rule ids in `trace.md` under `## Rule checkpoint` | `checkpoint` |
| C7 | **Rules are pointers** — Rule Index lists what exists; load bodies with `resolve-rules` when a trigger fires | always |

## Activation triggers

| Trigger | Agent runs |
|---------|------------|
| `session_start` | After `compile-context` — session-start bundle in compiled context |
| `pre_write` | Before writing outside the current resolved scope |
| `topic_shift` | User or task changes project field, instance type, or principal subtree |
| `pre_approval` | Before L4+ actions (profile, registry, system, publish) |

```bash
python3 system/engines/cli.py resolve-rules <session-path> --trigger pre_write --target <path>
```

## Related

- `protocol.md` — full operation model
- `discovery_protocol.md` — scope expansion and rule checkpoints
- `context_compilation.md` — Rule Index and compile output
- `permission_model.md` — L2–L7 boundaries
