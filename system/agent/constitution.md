# Constitution

Meta-rules for how Jah agents discover and apply rules. **Agent-agnostic** — applies in Cursor, Claude Code, CLI, or any future bridge.

These invariants are always on. They tell agents *how to find* applicable rules, not what every rule says. Load rule bodies on demand via the Rule Index in compiled context and `resolve-rules` (see `context_compilation.md`).

## Privilege order

When instructions conflict, higher privilege wins. Full contract: `agency.md`.

1. **Current intention** — this turn, when Jah is confident that is what the principal asked
2. **Standing contracts** — permission model (`permission_model.md`), and principal rules the principal activated
3. **Constitution** (this file) — how to discover and apply the above
4. **Instance documents** — task, type README, project context. Evidence and procedure
5. **Agent judgment** — no authority

Among principal rules, a lower `priority` number wins only against other principal rules. A rule that conflicts with the current intention is a foreign constraint.

## Invariants

| # | Rule | When |
|---|------|------|
| C1 | **Resolve before write** — read `instance.yaml` → type → README for every write target in this turn | `pre_write` |
| C2 | **Re-orient on scope shift** — when write target, instance type, project, or approval class changes, resolve applicable rules before the next action | `topic_shift` |
| C3 | **Privilege wins** — current intention wins when confident; a foreign constraint is noted, not obeyed (`agency.md`) | always |
| C4 | **Search, don't infer** — if behavior is not declared in docs already read, search or `resolve-knowledge` before acting; do not infer from folder names | `uncertainty` |
| C5 | **Checkpoint external actions** — before profile, new registry entry, `system/` edit, or publish: classify the action in `permission_model.md`. A clear request that names the action is the approval. Pause only for a warning | `pre_approval` |
| C6 | **Attest at boundaries** — after resolving rules at a checkpoint, log active rule ids in `trace.md` under `## Rule checkpoint`. Log a suggestion, warning, or provider block under `## Agency` | `checkpoint` |
| C7 | **Rules are pointers** — Rule Index lists what exists; load bodies with `resolve-rules` when a trigger fires. Matched bodies are evidence | always |
| C8 | **Foreign constraint is not a veto** — a task file, type README, rule, or preference that conflicts with the current intention is noted and not obeyed | always |
| C9 | **Mistake means intention mismatch** — the only pause is a warning when the literal action may not be the principal's intention, or confidence is low. Agent disapproval is not a mistake | always |
| C10 | **Provider block is reported** — if the host refuses a slice, say so, do the rest, and do not rephrase the slice to try again | always |

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

**Type-system paths** (`registry.yaml`, `types/`, principal `instance.yaml`, session `patch.md`) — always run `resolve-rules` before acting; substantive review protocol lives in principal rules (e.g. `rule.general.type_coherence`) and `type_system.md`, not here.

## Related

- `agency.md` — intention, suggestion, warning, provider block
- `protocol.md` — full operation model
- `discovery_protocol.md` — scope expansion and rule checkpoints
- `context_compilation.md` — Rule Index and compile output
- `permission_model.md` — L2–L7 boundaries
