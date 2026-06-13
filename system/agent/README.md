# Agent Layer

Behavioral protocol for Jah agents. **No executable code** — specs and operating procedures only.

## Entry

Start at `constitution.md`, then `protocol.md`.

## Read order

1. `constitution.md`
2. `protocol.md`
3. `design_logic.md`
4. `open_structure.md`
5. `discovery_protocol.md`
6. `knowledge_base.md`
7. `storage_rules.md`
8. `type_system.md`

## Spec ↔ engine pairing

Each agent spec has a matching engine under `system/engines/`:

| Agent spec | Engine |
|------------|--------|
| `knowledge_base.md` | `engines/knowledge/` |
| `context_compilation.md` | `engines/context/`, `engines/rules/` |
| `open_structure.md` | `engines/structure/` |
| `type_system.md` | `engines/registry/` |
| `session_lifecycle.md` | `engines/session/` |

Run engines via `python3 system/engines/cli.py <command>`.
