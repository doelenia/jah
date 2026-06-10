# Open Structure

How Jah declares folder meaning — inspectable, growable, and validated.

## Core rule

A living folder's shape is what it declares in **`instance.yaml` → `fields`**, resolved through `registry.yaml`. Do not infer behavior from folder names alone.

## Three layers

| Layer | Role |
|-------|------|
| **`type.base`** | `open_fields: true` by default — instance field growth is normal |
| **Container type `fields`** | Minimal baseline every instance must scaffold from |
| **Instance `fields`** | Baseline + **grown fields** (e.g. jah adds `design/` on top of context/sessions) |

## Default open growth

`open_fields: true` on `type.base` means container instances may declare any registry-resolvable field beyond the type baseline. Opt-out (`open_fields: false`) is rare and must be documented on that type.

## Minimal baseline

Container types (`project`, `personal`, `principal`, `type_package`) declare **`fields`** as the **minimum structure** — not an exhaustive allow-list.

- Instance **must include** every non-optional baseline field.
- Instance **may omit** baseline fields marked `optional: true`.
- Instance **may add** grown fields without a type migration.
- Instance **must not silently drop** required baseline fields.

## Container vs leaf `fields`

| Type role | `fields` in `type.yaml` means |
|-----------|-------------------------------|
| **Container** (`role: container`) | Minimal baseline for instance structure |
| **Leaf** (task, workflow, session, …) | Item schema — not instance field growth |

## Type packages

`types/<name>/` can be a **type package** (`type: type_package`): container + leaf schema + optional templates/workflows. Types and projects use the same machinery. See `system/bootstrap/types/type_package/README.md`.

## Instance → type → instances loop

1. **Instances explore** — add fields, try workflows, refine shape in `instance.yaml`.
2. **Types improve** — durable patterns patch type baseline, README, templates.
3. **Propagation** — other instances adopt via session `patch.md` (review gate).

## Discovery protocol

For any living folder:

1. `ls` — see declared directories
2. Read `instance.yaml` → `type`
3. Resolve type chain via registry
4. For each field in `fields:` → leaf path or `type: directory`
5. Read directory `instance.yaml` → `content_type` → item type README
6. Recurse into nested containers

## Structural parity

Declared structure must match disk. Run:

```bash
python3 users/<id>/tools/scripts/validate_structure.py
```

Checks: baseline present, grown fields valid, storage paths exist, no orphan directories, directory containers have matching `instance.yaml`.

## References

- `system/type_system.md` — registry, resolution, growth operators
- `system/design_logic.md` — philosophy
- `system/principal_model.md` — where instances live
