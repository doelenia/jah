# Engines Layer

Protocol runtime for Jah. Engines read principal data and implement behavior defined in `system/agent/`.

## CLI

```bash
python3 system/engines/cli.py <command> [args...]
```

| Command | Purpose |
|---------|---------|
| `compile-context` | Build session `compiled_context.md` |
| `new-session` | Create a session folder |
| `list-instances` | List all `instance.yaml` paths |
| `validate-registry` | Check registry and type references |
| `validate-structure` | Check declared fields vs disk |
| `validate-knowledge` | Check knowledge-base index and entries |
| `resolve-knowledge` | Look up knowledge entries |
| `resolve-rules` | Resolve active rules for a session trigger |
| `check-write` | Advisory L4+ write check (optional `--strict`) |

## Layout

```
engines/
  env.py           # path and registry resolution
  cli.py           # unified entry point
  knowledge/       # pairs with agent/knowledge_base.md
  context/         # pairs with agent/context_compilation.md
  rules/           # pairs with agent/constitution.md, context_compilation.md
  registry/        # pairs with agent/type_system.md
  structure/       # pairs with agent/open_structure.md
  session/         # pairs with agent/session_lifecycle.md
  instances/       # instance discovery
```

## Adding an engine

1. Add spec in `system/agent/<topic>.md`
2. Create `engines/<topic>/` with `lib.py` (if shared) and command module
3. Register command in `cli.py`
4. Document in this README
5. Bump `system/release/VERSION`

Engines are **not copied** to principals. Updates flow from `git pull` on `system/`.
