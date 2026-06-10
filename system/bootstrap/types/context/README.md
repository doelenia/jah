# Context Type

Stable project or scope background. One per project at `context.md`.

**Agents:** read this file before reading or editing project context.

## Storage

```
users/<principal>/projects/<project>/context.md
```

Declared in the project `instance.yaml`:

```yaml
fields:
  context:
    id: context.<project>
    type: context
    storage: context.md
```

## Agent protocol

1. Read `users/<principal>/types/project/README.md` and `types/context/type.yaml`.
2. Read the project `instance.yaml` to confirm the context field id and path.
3. Edit `context.md` only with user approval (L3–L4); propose changes in session `patch.md`.
4. Cite `context.md` in session artifacts when it informed output.

## Do not

- Store session-only notes in `context.md` — use session `input.md` or `output.md`.
- Create multiple context files per project without updating the type and instance.
