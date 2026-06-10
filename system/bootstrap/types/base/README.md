# Base Type

Root schema for all Jah types. Every other type extends this.

**Agents:** read this file when creating a new type or any `instance.yaml`. See `system/open_structure.md` for the open structure strategy.

## Required on every instance

```yaml
id: <unique-id>
type: <type-name>   # matches users/<principal>/types/<name>/ — e.g. project, session, preference
name: <human name>
```

## Open fields (default)

`type.base` sets `open_fields: true`. Container instances may declare registry-resolvable fields beyond the type's minimal baseline. Opt-out (`open_fields: false`) is rare.

## Container vs leaf `fields`

| Type role | `fields` in `type.yaml` |
|-----------|-------------------------|
| **Container** (`role: container`) | Minimal baseline — every instance must scaffold from this and may grow beyond it |
| **Leaf** (task, workflow, session, …) | Item schema — not instance field growth |

## Field instances

Container instances (project, personal, principal, type_package) declare child field instances in a `fields:` block:

```yaml
fields:
  context:
    id: context.jah
    type: context
    storage: context.md
  design:
    id: directory.design.jah
    type: directory
    content_type: document
    storage: design/
```

The type baseline lists required scaffolding (e.g. `context`, `sessions`). Grown fields (e.g. `design/`) are declared only on the instance.

Each field's `type` must resolve in `registry.yaml`. Before working with a field, read that type's README.
