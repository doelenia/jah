# Type Package

A registered type folder (`types/<name>/`) as a **living container** — same growth model as projects — that also carries a leaf schema.

**Agents:** read `types/<name>/instance.yaml` (when present), `type.yaml`, and this README.

## Structure

```
users/<principal>/types/<name>/
  instance.yaml       # type: type_package (optional until package is formalized)
  type.yaml           # leaf schema — required baseline
  README.md           # agent protocol — required baseline
  templates/          # optional — copy into projects
  workflows/          # optional scaffolds
```

## Baseline vs growth

`type.type_package` declares a **minimal baseline** in `type.yaml` `fields`:

- **Required:** `type_schema` (`type.yaml`), `readme` (`README.md`)
- **Optional baseline:** `templates/`, `workflows/`

Instances may **add** fields beyond baseline (`open_fields` defaults true on `type.base`). They must not drop required baseline fields.

## Agent protocol

1. Read `users/<principal>/types/type_package/type.yaml` and this README.
2. When formalizing a type as a package, add `instance.yaml` with `type: type_package` and register baseline fields.
3. **Adopt** — register in `registry.yaml`; projects reference `content_type: <name>` in directory fields.
4. **Use templates** — copy from `types/<name>/templates/` into a project (same pattern as workflow scaffolds).
5. **Improve** — patch the type package; propagate to instances via session `patch.md`.

## Example (future)

```
types/event/
  instance.yaml
  type.yaml
  README.md
  templates/
    instance.template.yaml
  workflows/
    announce/
```

Projects declare `events/` with `content_type: event`. No separate project subtype required.
