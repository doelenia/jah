# Context Compilation

## Why it exists

Sessions should not rely on vague recall. Before work starts, Jah collects **goal-matched** type definitions, preferences, rules, tasks, sessions, sources, and project context into `compiled_context.md`.

After compilation, agents **gap-fill** and run **active discovery** (`discovery_protocol.md`, `proactive_capture.md`) before executing work.

## How to compile

```bash
python3 users/<id>/tools/scripts/compile_context.py users/<id>/projects/<project>/sessions/<session-id>
```

The script loads (via active principal from `jah.yaml`):

1. **Agent protocol** — `discovery_protocol.md`, `proactive_capture.md`, `open_structure.md`
2. **System principles** — glossary, protocol, type_system
3. **Scoped types** — types referenced by the project, session, workflows, and linked task (not the full registry)
4. Personal profile and **all** personal preferences
5. Personal rules and project rules (when present)
6. Project `context.md`, `instance.yaml`, and **grown fields** matched to the goal (e.g. `design/`)
7. **Linked task** — from session `task_id` or task `session` field
8. **Related tasks** and **related sessions** — goal keyword match
9. Directory container boundaries (`sources/index.md`, `workflows/index.md`, `tasks/index.md` when present)
10. **Resolved workflows** — selective (see below)
11. Session `input.md`

Output sections: Session Goal, Agent Protocol, System Principles, Scoped Types, Personal Profile, Personal Preferences, Active Rules, Project Context, Project Instance, Grown Project Fields, Linked Task, Related Tasks, Related Sessions, Directory Boundaries, Resolved Workflows, Available Workflows, Session Input, Required Output Files, Approval Boundaries.

## Task linking

| Link | How |
|------|-----|
| Session → task | Optional `task_id` on session `instance.yaml` |
| Task → session | `session: session.YYYY-MM-DD-NNN` on task `instance.yaml` |

Compile resolves either direction and loads the task `instance.yaml` and `description.md`.

## Workflow resolution

Sessions are call sites. `compile_context.py` resolves which workflows to load — not every workflow in the project.

### Session invocation fields

| Field | Purpose |
|-------|---------|
| `workflow_id` | Explicit call, e.g. `workflow.us_taxes.tax_filing` |
| `workflow` | Path relative to project, or `auto` |
| `target_type` | Hint for auto mode, e.g. `type.blog_post` |
| `task_id` | Explicit task to link, e.g. `task.jah.my_task` |

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

Global rules under `users/<id>/personal/rules/` compile into every session. Project rules compile when the project has a `rules/` container. Workflows declare `dependencies` on preferences and rules; `evaluation.md` checks compliance.

## Related docs

- `discovery_protocol.md` — active search after compile
- `session_lifecycle.md` — session checkpoints
