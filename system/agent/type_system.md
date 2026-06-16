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

Do not infer behavior from folder names alone. See `open_structure.md` for the open structure strategy.

### Open structure

- **`open_fields: true`** on `type.base` — container instances may add registry-resolvable fields beyond the type baseline (default; growth is normal).
- **Container type `fields`** — minimal baseline every instance must scaffold from; not an exhaustive allow-list.
- **Instance `fields`** — baseline + grown fields; authoritative shape for that living folder.
- **Leaf type `fields`** — item schema (task, workflow, …); not instance field growth.
- **Project directory** — when extending `type.project`, prefer typed subdirectories over a flat `documents/` repo (`types/project/README.md`).

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
| **Add container field** | Add field to instance `fields` (grown field) or extend type baseline via patch |
| **Add type package** | Register type with `type: type_package` instance under `types/<name>/` |
| **Deprecate** | Mark registry entry `status: deprecated` |

Propose via session `patch.md`; apply after user approval (L4).

## Type coherence review (required)

**Whenever** you create, register, extend, patch, or design a type **or** create or reshape a typed instance (container fields, `instance.yaml`, `content_type`), run this review **before** writing. Enforced by principal rule `rule.general.type_coherence` (seeded at bootstrap; editable or replaceable under `personal/rules/`).

This is not optional discovery — it prevents duplicate types, overlapping abstractions, and designs that do not scale.

### When to run

| Situation | Review before |
|-----------|---------------|
| New registry entry (`registry.yaml`) | Any write to `registry.yaml` or new `types/<name>/` |
| Extend or patch a type | Edits to `type.yaml`, type README, or type package |
| Add or change container fields | Instance `fields` blocks, directory `content_type` |
| Design session (no write yet) | Proposing a type in `design/`, `patch.md`, or plan |
| Instance type change | Changing `type:` on any `instance.yaml` |

### How to run

1. **Survey the registry** — read `users/<id>/registry.yaml` and run:
   ```bash
   python3 system/engines/cli.py list-types
   python3 system/engines/cli.py validate-registry   # optional sanity check
   ```
2. **Resolve rules** for the write target:
   ```bash
   python3 system/engines/cli.py resolve-rules <session-path> \
     --trigger pre_write --target <path>
   ```
   Use `pre_approval` when registering a new type; use `topic_shift` when scope moves to a different type subtree.
3. **Compare** the planned change against every related type:
   - same or similar `extends` parent?
   - overlapping purpose or fields with an existing type?
   - could this be a field, alias, workflow, or patch instead of a new type?
   - naming clear and distinct from siblings and `aliases`?
   - right level of abstraction (not skipping parent types, not over-specializing)?
   - fields reuse registry types instead of ad-hoc scalars?
4. **Decide** — proceed, revise, merge with an existing type, or deprecate the weaker duplicate.
5. **Proactively surface issues** — if you find duplication, confusion, or unsustainable design, tell the user and propose a fix **before** applying L4 registry changes or large L3 type patches.
6. **Log** in `trace.md`:

```markdown
## Type coherence review

| Field | Value |
|-------|-------|
| trigger | pre_write |
| target | users/<id>/types/foo/type.yaml |
| action | extend | register | patch | design | instance_field |
| related_types | document, context |
| rationale | One sentence — why this type/field exists and why this shape |
| issues_found | none — or: overlaps with X; suggest merge / rename / extend Y |
| resolution | proceed | revise | defer — and what changed |
```

### Review checklist

- [ ] Full registry surveyed (`list-types` or `registry.yaml`)
- [ ] Closest existing types read (`type.yaml` + README + extends chain)
- [ ] Clear rationale — not "we might need this later"
- [ ] No duplicate purpose with an existing type unless deprecated
- [ ] `extends` points at the narrowest correct parent
- [ ] Field types resolve in registry; no parallel informal schemas
- [ ] Names and storage paths are predictable and documented
- [ ] Change is sustainable — instances can grow without breaking the model
- [ ] User informed of any issues found; L4 proposals in `patch.md`

## Conventions

Every type has:

```yaml
id: type.<name>
description: "..."
extends: type.base
role: container          # container types only
fields:                  # minimal baseline (containers) or item schema (leaves)
  <field_name>:
    type: type.<other> | scalar
    cardinality: one | many
    storage: <path>
    optional: true
```

Container instances declare baseline + optional grown fields in their own `instance.yaml`.
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
| `task` | Planned work item with lifecycle |
| `type_package` | Living type folder — schema + templates + workflows |

See `system/bootstrap/registry.seed.yaml` for the full seed.

## Validation

Optional principal scripts:

- `validate_registry.py` — broken extends chains or unknown instance types
- `validate_structure.py` — baseline fields, grown fields, storage parity (`open_structure.md`)

`compile_context.py` loads registry types into sessions at runtime.
