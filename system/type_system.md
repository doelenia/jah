# Type System

How types work in Jah. Types are the **growth engine** — users extend their work/life model through the registry.

## Location

Type definitions live in `users/<id>/types/<name>/`:

| File | Purpose |
|------|---------|
| `type.yaml` | Schema — fields with typed references |
| `README.md` | **Agent protocol** — how to work with this type |

Registered in `users/<id>/registry.yaml`. Starter types come from bootstrap; the principal owns them after init.

## Registry

`users/<id>/registry.yaml` is the authoritative type index:

```yaml
id: registry.<id>
version: 1
types:
  project:
    id: type.project
    path: types/project
    extends: base
  blog_post:
    id: type.blog_post
    path: types/blog_post
    extends: document
aliases: {}
```

- **path** — relative to principal root
- **extends** — registry key of parent type (`null` for root)
- **aliases** — optional backward-compatible names

## Type resolution protocol (required)

**Before working with any instance or field:**

1. Read `jah.yaml` → `active_principal`
2. Read `users/<id>/registry.yaml`
3. Read `instance.yaml` → get `type` (resolve aliases)
4. Registry lookup → `path` → read `type.yaml`
5. Walk `extends` chain via registry; **merge fields** (child overrides parent on conflict)
6. Read README chain: base → … → child (child supplements parent)
7. For each field in scope, repeat for the field's declared type
8. Read child `instance.yaml` files for folder-based instances

Do not infer behavior from folder names alone.

### Extends merge rules

- Child `fields` override parent fields with the same name
- Child `optional`, `storage`, `description` replace parent for that field
- README: child sections append; use an **Overrides** section to replace a parent protocol step

## Type growth operators

| Operator | Effect |
|----------|--------|
| **Register** | Add entry to `registry.yaml` + create `types/<name>/` |
| **Extend** | New type with `extends: <parent>` in registry |
| **Patch** | Edit owned `type.yaml` or README |
| **Attach workflow** | Add `type.workflow` instance under a container or `types/<artifact>/workflows/` |
| **Add container field** | Add `type.directory` field to personal/project type |
| **Deprecate** | Mark registry entry `status: deprecated` |

Propose via session `patch.md`; apply after user approval (L4).

## Conventions

Every type has:

```yaml
id: type.<name>
description: "..."
extends: type.base
fields:
  <field_name>:
    type: type.<other> | scalar
    cardinality: one | many
    storage: <path>
    optional: true
```

### Directory type (`type.directory`)

Directory containers declare `content_type` as a **registry type id**. Resolve via registry before write — not a closed enum.

Each container must have `instance.yaml`. See `users/<id>/types/directory/README.md`.

### Workflow type (`type.workflow`)

Callable procedure with `requirements.md`, `workflow.md`, `evaluation.md`, `examples.md`.

| Field | Purpose |
|-------|---------|
| `scope` | `personal`, `type`, or `project` |
| `operates_on` | Artifact type id when `scope: type` |
| `project` | Project id when `scope: project` |
| `applies_to` | Narrowing for personal workflows |
| `status` | `active`, `draft`, or `deprecated` |

## Starter types (bootstrap)

Bootstrap copies these into new principals — all editable after init:

| Type | Purpose |
|------|---------|
| `base` | Root schema |
| `principal` | Principal container |
| `directory` | Directory boundary |
| `document` | Single content file |
| `context` | Project background |
| `profile` | Personal facts |
| `personal` | Personal scope container |
| `session` | Temporary workspace |
| `session_artifact` | Session file |
| `project` | Project container |
| `preference` | Scoped preference |
| `rule` | Scoped rule |
| `source` | Reference material |
| `workflow` | Callable procedure |

See `system/bootstrap/registry.seed.yaml` for the full seed.

## Validation

MVP has no schema engine. Optional: `users/<id>/tools/scripts/validate_registry.py` warns on broken extends chains or unknown instance types.

`compile_context.py` loads registry types into sessions at runtime.
