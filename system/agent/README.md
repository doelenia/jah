# Agent Layer

Behavioral protocol for Jah agents. **No executable code** — specs and operating procedures only.

## Entry

Start at `constitution.md`, then `agency.md`, then `protocol.md`.

## Read order

1. `constitution.md`
2. `agency.md`
3. `protocol.md`
4. `design_logic.md`
5. `open_structure.md`
6. `discovery_protocol.md`
7. `knowledge_base.md`
8. `storage_rules.md`
9. `type_system.md`

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
