# Context Compilation

## Why it exists

Sessions should not rely on vague recall. Before work starts, Jah collects relevant type definitions, preferences, rules, sources, and project context into `compiled_context.md`.

After compilation, agents **gap-fill** missing dependencies (`proactive_capture.md`) before executing work.

## How to compile

```bash
python3 users/<id>/tools/scripts/compile_context.py users/<id>/projects/<project>/sessions/<session-id>
```

The script loads (via active principal from `jah.yaml`):

1. `system/glossary.md`, `system/protocol.md`, `system/type_system.md`
2. **Registry types** — all types in `registry.yaml` (YAML + README)
3. Personal profile and writing preferences
4. Active rules under `users/<id>/personal/rules/`
5. Project `context.md` and `instance.yaml`
6. Directory container boundaries (`sources/index.md`, `workflows/index.md` when present)
7. **Resolved workflows** — selective (see below)
8. Session `input.md`

Output sections: Session Goal, System Principles, Relevant Types, Personal Profile, Personal Preferences, Active Rules, Project Context, Project Instance, Directory Boundaries, Resolved Workflows, Available Workflows, Session Input, Required Output Files, Approval Boundaries.

## Workflow resolution

Sessions are call sites. `compile_context.py` resolves which workflows to load — not every workflow in the project.

### Session invocation fields

| Field | Purpose |
|-------|---------|
| `workflow_id` | Explicit call, e.g. `workflow.us_taxes.tax_filing` |
| `workflow` | Path relative to project, or `auto` |
| `target_type` | Hint for auto mode, e.g. `type.blog_post` |

```bash
python3 users/<id>/tools/scripts/new_session.py users/<id>/projects/us-taxes "Goal" \
  --workflow-id workflow.us_taxes.tax_filing
```

### Resolution priority

1. **`workflow_id` set** → load that workflow + dependencies
2. **`workflow` path set** (not `auto`) → load that folder
3. **`target_type` set** → load active workflows where `operates_on` matches
4. **Goal/input keyword match** → match against catalog, name, description
5. **Default** → list candidates in **Available Workflows**; load body if exactly one match

Workflow discovery searches:

- `users/<id>/projects/<project>/workflows/`
- `users/<id>/personal/workflows/` (when `scope: personal` and `applies_to` matches)
- `users/<id>/types/*/workflows/` (type-scoped workflows)

### Compiled workflow sections

- **Resolved Workflows** — invoked instance, requirements, body, evaluation, examples
- **Available Workflows** — catalog of other active workflows not invoked

## How rules propagate

Global rules under `users/<id>/personal/rules/` compile into every session. Workflows declare `dependencies` on preferences and rules; `evaluation.md` checks compliance.
