# Type System

How types work in Jah.

## Location

Type definitions live in `types/<name>/`:

| File | Purpose |
|------|---------|
| `type.yaml` | Schema — fields with typed references |
| `README.md` | **Agent protocol** — how to work with this type |

Both are local and gitignored.

## Type resolution protocol (required)

**Before working with any instance or field, agents must resolve its type:**

1. Read `instance.yaml` → get `type` (e.g. `project`, `directory`, `source`, `workflow`).
2. Read `types/<type>/type.yaml` → understand schema and field types.
3. Read `types/<type>/README.md` → follow agent protocol for that type.
4. For each field being touched, repeat steps 2–3 for the field's declared `type`.
5. Read child `instance.yaml` files for folder-based instances.

This applies at every level — project, session, workflow, preference, rule, source, profile, context, etc. Do not infer behavior from folder names alone.

### Read order with types

1. `system/protocol.md`
2. `system/design_logic.md`
3. `system/storage_rules.md`
4. `system/type_system.md` (this file)
5. Parent `instance.yaml` (project, session, or personal)
6. `types/<type>/README.md` and `types/<type>/type.yaml` for the instance and each field in scope
7. Session `compiled_context.md` after compilation

## Conventions

Every type has:

```yaml
id: type.<name>
description: "..."
extends: type.base   # except base itself
fields:
  <field_name>:
    type: type.<other> | scalar
    cardinality: one | many
    storage: <path>    # file, directory, instance_ref, or pattern
    optional: true     # when omitted, field is required
```

### Scalar fields

Primitive values stored directly in `instance.yaml` (e.g. `goal`, `scope`, `status`). Use `type: scalar` in the type definition with optional `allowed_values`.

### Typed fields

Every non-scalar field references another type by id (`type.context`, `type.preference`, etc.). Never use bare field name lists without type references.

### Storage patterns

| Pattern | Meaning | Example |
|---------|---------|---------|
| `context.md` | Single file at path | Project context |
| `preferences/` | Directory of child instances | Each subfolder has `instance.yaml` |
| `rules/` | Directory of YAML file instances | Each `.yaml` is a rule instance |
| `instance_ref` | Reference by path or id | `main_instance: memory/projects/jah` |
| `{content_path}` | Filename from instance field | Preference content file |
| `catalog: index.md` | Catalog file for source items | sources/index.md |
| `content_type: <name>` | Item type stored in a directory container | source, rule, preference, workflow, session, document |

### Directory type (`type.directory`)

**Directory containers** (`sources/`, `rules/`, `preferences/`, `workflows/`, `sessions/`, `documents/`) are **`type.directory` containers**. Each must have **`instance.yaml`** declaring `description`, `content_type`, layout fields (`catalog`, `binaries`, `instances`), and `protocol`. Agents read that file at the write boundary before storing content.

**Item types** (`source`, `rule`, `preference`, `workflow`, `session`, `document`) define individual entries — catalog rows, YAML files, leaf folders, or session workspaces. They extend `type.base`, not `type.directory`. See `types/directory/README.md`.

**Personal workflows** live under `memory/personal/workflows/` (optional cross-project callables).

### Instance `fields` block

Container instances declare their child field instances:

```yaml
id: project.jah
type: project
name: Jah
fields:
  context:
    id: context.jah
    type: context
    storage: context.md
  workflows:
    - id: workflow.jah.blog
      type: workflow
      storage: workflows/blog/
  rules:
    type: rule
    cardinality: many
    storage: rules/
```

- **One** (`cardinality: one`): single object under `fields.<name>`.
- **Many** (`cardinality: many`): list under `fields.<name>` or a directory pattern with `storage`.

When creating a new field instance, always:
1. Match the field type from the parent type definition.
2. Create the storage (file, folder, or YAML).
3. Add `instance.yaml` for folder-based instances.
4. Register the instance in the parent's `fields` block.

## Base type (`types/base/type.yaml`)

Required fields on all instances: `id`, `type`, `name`.

Optional fields: `extends`, `sensitivity`, `dependencies`, `capabilities`, `allowed_read`, `allowed_write`, `requires_approval`, `memory_paths`, `tool_access`, `fields`.

## Built-in types

| Type | Purpose |
|------|---------|
| `base` | Root schema |
| `directory` | Directory boundary base — layout, roles, agent protocol |
| `document` | Single markdown content file |
| `context` | Project background (`context.md`) |
| `profile` | Personal facts (`profile.md`) |
| `personal` | Personal memory container |
| `session` | Temporary working instance |
| `session_artifact` | Session working file |
| `project` | Project container |
| `preference` | Scoped preference |
| `rule` | Scoped rule |
| `source` | Reference material |
| `workflow` | Callable repeatable procedure (personal, type, or project scope) |

### Workflow type (`type.workflow`)

Workflow instances are **callables** — like functions with preconditions (`requirements.md`), body (`workflow.md`), and postconditions (`evaluation.md`).

| Field | Purpose |
|-------|---------|
| `scope` | `personal`, `type`, or `project` |
| `operates_on` | Artifact type id when `scope: type` (e.g. `type.blog_post`) |
| `project` | Project id when `scope: project` |
| `applies_to` | Narrowing for personal workflows |
| `status` | `active`, `draft`, or `deprecated` |

**Types vs memory:** `types/workflow/` defines schema and templates. `types/<artifact_type>/workflows/<name>/` holds scaffolds only. Living instances live in `memory/.../workflows/`.

## Inheritance

Types extend `type.base` (or another type) and add typed fields. Instances reference their type in `instance.yaml` via `type: <name>`.

When work reveals a reusable schema, agents should offer to create or extend a type (`proactive_capture.md`). Propose via session `patch.md`; apply to `types/` only after explicit approval.

## Validation

MVP has no schema engine. Types are human-readable YAML; consistency is maintained by convention, type README protocols, and review. `compile_context.py` loads type YAMLs and READMEs into sessions to make protocols visible at runtime.
