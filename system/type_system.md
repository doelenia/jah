# Type System

How types work in Jah.

## Location

Type definitions live in `types/<name>/type.yaml` (local, gitignored).

## Conventions

Every type has:

```yaml
id: type.<name>
type: <name>   # or implied
description: "..."
extends: type.base   # except base itself
```

### Base type (`types/base/type.yaml`)

Required fields on all instances: `id`, `type`, `name`.

Optional fields: `extends`, `sensitivity`, `dependencies`, `capabilities`, `allowed_read`, `allowed_write`, `requires_approval`, `memory_paths`, `tool_access`.

## Built-in types

| Type | Purpose |
|------|---------|
| `base` | Root schema |
| `session` | Temporary working instance |
| `project` | Container for context, rules, work patterns, sessions |
| `preference` | Scoped preference with content path |
| `rule` | Scoped rule with priority and applies_to |
| `source` | Reference material |
| `work_pattern` | Repeatable workflow template |

## Inheritance

Types extend `type.base` and add domain fields. Instances reference their type in `instance.yaml`.

## Validation

MVP has no schema engine. Types are human-readable YAML; consistency is maintained by convention and review.
