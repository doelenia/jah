# Bootstrap Setup

Initialize a fresh Jah repo after clone.

## Detect uninitialized repo

The repo is **uninitialized** when:

- No `jah.yaml` at repo root, or
- No `users/<id>/registry.yaml` for the active principal

## Init steps (agents or human)

```bash
python3 system/scripts/init_jah.py <principal-id>
```

Example:

```bash
python3 system/scripts/init_jah.py katakuchi
```

The script:

1. Copies `system/bootstrap/types/` → `users/<id>/types/`
2. Copies `system/bootstrap/registry.seed.yaml` → `users/<id>/registry.yaml` (rewrites id)
3. Creates `users/<id>/instance.yaml` (type: principal)
4. Scaffolds `users/<id>/personal/instance.yaml` and empty `projects/`, `tools/`
5. Writes `jah.yaml` with `active_principal: <id>`

## Post-init verification

```bash
python3 users/<id>/tools/scripts/list_instances.py
python3 users/<id>/tools/scripts/validate_registry.py
python3 users/<id>/tools/scripts/validate_structure.py
python3 users/<id>/tools/scripts/new_session.py users/<id>/projects/<project> "Smoke test goal"
python3 users/<id>/tools/scripts/compile_context.py users/<id>/projects/<project>/sessions/YYYY-MM-DD-NNN
```

New projects should scaffold **baseline fields** from `type.project` `fields` in `type.yaml`, then add grown fields in `instance.yaml` as needed (`system/open_structure.md`).

## Agent protocol on first load

1. Read `system/protocol.md` and this file.
2. If uninitialized, run `init_jah.py` or ask the user for a principal id.
3. Read `jah.yaml` → resolve `users/<active_principal>/`.
4. Read `registry.yaml` before working with any instance type.

## Growing types after bootstrap

All types under `users/<id>/types/` are user-owned. To add a type:

1. Register it in `registry.yaml`
2. Create `types/<name>/type.yaml` and `README.md`
3. Propose via session `patch.md`; apply after approval

Users may patch even starter types (`base`, `project`, etc.) — bootstrap is not runtime authority.
