# Directory Type

Directory **containers** at stable memory boundaries — `sources/`, `rules/`, `preferences/`, `workflows/`, `sessions/`, `documents/`.

**Agents:** read `instance.yaml` in the directory before writing anything there. Schema: `users/<principal>/types/directory/type.yaml`. Scaffolds: `users/<principal>/types/directory/scaffold/`.

## Container vs content type

| Layer | Type | Example |
|-------|------|---------|
| Container | `directory` | `users/<principal>/projects/us-taxes/sources/instance.yaml` |
| Item | `source`, `rule`, `preference`, `workflow`, `session`, `document` | Catalog entry in `index.md`, `rules/writing/foo.yaml`, `workflows/blog/`, `sessions/2026-06-09-001/` |

The container declares **what** is stored (`content_type`) and **how** (`catalog`, `binaries`, `instances`). The content type defines the **item schema**.

## Container instance format

```yaml
id: directory.sources.us-taxes
type: directory
name: US Taxes Sources
description: "Reusable reference files and catalog for US tax filing work."
role: container
content_type: source
catalog: index.md
binaries: files/
protocol: users/<principal>/types/source/README.md
requires_approval: true
```

| content_type | Required fields | Item location |
|--------------|-----------------|---------------|
| `source` | `catalog`, `binaries`, `protocol` | `files/<group>/<name>.<ext>` + entry in `index.md` |
| `rule` | `instances`, `protocol` | `<group>/<name>.yaml` |
| `preference` | `instances`, `protocol` | `<name>/instance.yaml` + content file |
| `workflow` | `catalog`, `instances`, `protocol` | `index.md` + `<name>/instance.yaml` + workflow markdown files |
| `session` | `instances`, `protocol` | `YYYY-MM-DD-NNN/instance.yaml` + session artifacts |
| `document` | `instances`, `protocol` | `<name>.<ext>` at directory root |

Layout defaults for each `content_type` are in `users/<principal>/types/directory/type.yaml` under `content_type_layouts`.

## Agent protocol

1. **Read** the directory's `instance.yaml`.
2. **Resolve** `content_type` → read `users/<principal>/types/<content_type>/README.md` (path in `protocol`).
3. **Follow** layout rules — never store item files at the container root unless permitted.
4. **Ask** for approval in a default session (L3–L4) before writing.
5. **Register** new leaf instances in the parent `instance.yaml` `fields` block when required.

## Scaffolding a new container

1. Create the directory under project or personal memory.
2. Copy the matching template from `users/<principal>/types/directory/scaffold/<content_type>-container.yaml`.
3. Set `id`, `name`, `description`, and paths.
4. Create initial layout (`index.md`, `files/`, etc.) per content type.
5. Register in parent `instance.yaml` with `type: directory` and matching `content_type`.

## Do not

- Store item content at the directory root when `forbidden_at_root` applies
- Use `type: source` (or other item types) on the container `instance.yaml`
- Skip reading `instance.yaml` before writing to a directory path
- Auto-write without user approval in a default session
