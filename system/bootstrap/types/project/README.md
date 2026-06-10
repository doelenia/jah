# Project Type

A project in memory. Examples: `users/<principal>/projects/jah/`, `users/<principal>/projects/ausna/`.

**Agents:** read this file before creating, reading, or modifying any project.

## Structure

```
users/<principal>/projects/<project>/
  instance.yaml       # type: project — declares all field instances
  context.md          # type.context
  preferences/        # type.directory container (optional)
  rules/              # type.directory container (optional)
  sources/            # type.directory container (optional)
  workflows/          # type.directory container (optional)
  sessions/           # type.directory container (content_type: session)
```

## Agent protocol

1. Read `users/<principal>/types/project/type.yaml` and this README.
2. Read `users/<principal>/projects/<project>/instance.yaml` — resolve every field's `type`, `id`, and `storage`.
3. Before writing to a directory field, read that directory's **`instance.yaml`** (type.directory), then the **content type** README.
4. When creating a new project field instance:
   - Match the field's declared `type` from `type.yaml`.
   - Add the instance to the project `instance.yaml` `fields` block.
   - For directory containers, create `instance.yaml` from `users/<principal>/types/directory/scaffold/`.
   - For leaf instances (workflow, preference, session), create `instance.yaml` in the child folder.
5. Propose stable project changes in session `patch.md`; apply only after user approval.

## Creating a new project

1. Create `users/<principal>/projects/<name>/instance.yaml` with `type: project`.
2. Add `fields.context` pointing to `context.md`; write initial `context.md`.
3. Scaffold directory containers (`rules/`, `sources/`, `workflows/`, `sessions/`) from `users/<principal>/types/directory/scaffold/` as needed.
4. Register each child instance in the `fields` block as it is created.
