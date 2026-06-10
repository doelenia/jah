# Principal Model

Where living instances live in Jah.

## Structure

```
users/<id>/
  instance.yaml
  registry.yaml
  types/
  personal/
    instance.yaml
    profile.md
    preferences/
    rules/
    workflows/        # optional cross-project workflows
    sources/
    documents/
  projects/
    <project>/
      instance.yaml
      context.md
      rules/
      sources/
      workflows/
      sessions/
      tasks/
  tools/
```

## Instance rule

Every folder representing a living instance contains `instance.yaml`:

```yaml
id: <unique-id>
type: <type-name>
name: <human name>
```

Container instances declare typed child fields in a `fields:` block — **baseline + grown fields** (`system/open_structure.md`). The type declares a minimal baseline; the instance is authoritative for shape. Resolve each field's type through `registry.yaml` — see `system/type_system.md`.

## Personal scope

- **Profile** — stable personal facts (`profile.md`)
- **Preferences** — scoped defaults
- **Rules** — active constraints
- **Workflows** — optional cross-project callables
- **Sources / documents** — reusable files

### Profile

`users/<id>/personal/profile.md` is the canonical store for **stable personal facts**.

**Update protocol:**

1. Context compilation includes the current profile.
2. Agents **must propose** profile updates in session `patch.md` — not write `profile.md` directly.
3. Apply profile changes manually after review (L4).

## Project scope

- **Context** — what the project is
- **Rules / sources** — project-specific references
- **Workflows** — callable procedures; cataloged in `workflows/index.md` when present
- **Tasks** — planned work backlog; cataloged in `tasks/index.md` when present
- **Sessions** — temporary workspaces

### Sources

| Path | Purpose |
|------|---------|
| `sources/index.md` | Catalog of every resource |
| `sources/files/` | Binary and file-based assets |

## Workflows

Workflow instances (`type.workflow`) may live:

- `users/<id>/personal/workflows/<name>/`
- `users/<id>/projects/<project>/workflows/<name>/`
- `users/<id>/types/<artifact>/workflows/<name>/` (type-scoped)

Resolution uses `workflow_id`, registry, and parent `fields` — not path assumptions alone.

## Tasks

Task instances (`type.task`) may live:

- `users/<id>/personal/tasks/<name>/`
- `users/<id>/projects/<project>/tasks/<name>/`

Tasks track backlog lifecycle (`pending` → `in_progress` → `done`). Link a session when work starts.

## Git

All of `users/` is local. Never committed to GitHub.

## References

| Source kind | Citation format | Example |
|-------------|-----------------|--------|
| Internal | Repo-relative path | `users/katakuchi/personal/profile.md` |
| External | Full URL | `https://www.irs.gov/...` |

## Stable vs session

- **Stable instances** — profile, preferences, rules, context, workflows, tasks, sources
- **Session workspace** — input, output, evaluation, trace, patch, compiled_context

Modify stable instances only with explicit approval (`permission_model.md`).
