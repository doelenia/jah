# Agent Layer

Behavioral protocol for Jah agents. **No executable code** — specs and operating procedures only.

## Entry

Start at `protocol.md`.

## Read order

1. `protocol.md`
2. `design_logic.md`
3. `open_structure.md`
4. `discovery_protocol.md`
5. `knowledge_base.md`
6. `storage_rules.md`
7. `type_system.md`

## Spec ↔ engine pairing

Each agent spec has a matching engine under `system/engines/`:

| Agent spec | Engine |
|------------|--------|
| `knowledge_base.md` | `engines/knowledge/` |
| `context_compilation.md` | `engines/context/` |
| `open_structure.md` | `engines/structure/` |
| `type_system.md` | `engines/registry/` |
| `session_lifecycle.md` | `engines/session/` |

Run engines via `python3 system/engines/cli.py <command>`.
