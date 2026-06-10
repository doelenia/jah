# Base Type

Root schema for all Jah types. Every other type extends this.

**Agents:** read this file when creating a new type or any `instance.yaml`.

## Required on every instance

```yaml
id: <unique-id>
type: <type-name>   # matches users/<principal>/types/<name>/ — e.g. project, session, preference
name: <human name>
```

## Optional instance fields

From `type.base`: `extends`, `sensitivity`, `dependencies`, `capabilities`, `allowed_read`, `allowed_write`, `requires_approval`, `memory_paths`, `tool_access`.

## Field instances

Container instances (project, personal, session) should declare child field instances in a `fields:` block:

```yaml
fields:
  context:
    id: context.jah
    type: context
    storage: context.md
  workflows:
    - id: workflow.jah.blog
      type: workflow
      storage: workflows/blog/
```

Each field's `type` must match the type definition in `users/<principal>/types/<name>/type.yaml`. Before working with a field, read that type's README.
