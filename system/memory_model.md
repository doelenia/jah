# Memory Model

Where living instances live in Jah.

## Structure

```
memory/
  personal/           # You
    instance.yaml
    profile.md
    preferences/
    rules/
  projects/
    <project>/        # e.g. jah, ausna
      instance.yaml
      context.md
      rules/
      sources/
      work_patterns/
      sessions/
```

## Instance rule

Every folder representing a living instance contains `instance.yaml`:

```yaml
id: <unique-id>
type: <type-name>
name: <human name>
```

## Personal memory

- **Profile** — who you are (`profile.md`)
- **Preferences** — scoped defaults (writing, lifestyle, etc.)
- **Rules** — active constraints (YAML with scope, priority, applies_to)

## Project memory

- **Context** — what the project is
- **Rules / sources** — project-specific references
- **Work patterns** — repeatable workflows (requirements, workflow, evaluation, examples)
- **Sessions** — temporary workspaces

## Git

All of `memory/` is local. Never committed to GitHub.

## Stable vs session

- **Stable memory** — preferences, rules, project context, work patterns
- **Session memory** — input, output, evaluation, trace, patch, compiled_context

Modify stable memory only with explicit approval (see `permission_model.md`).
