# Session Lifecycle

Stages of a Jah session.

## 1. Created

```bash
python3 users/<id>/tools/scripts/new_session.py users/<id>/projects/jah "Goal here"
# optional: --workflow-id workflow.jah.blog
```

Creates `users/<id>/projects/jah/sessions/YYYY-MM-DD-NNN/` with:

- `instance.yaml` — goal, main_instance, optional `workflow_id` / `workflow` / `target_type`, permissions
- `input.md` — goal text
- Empty placeholders: `compiled_context.md`, `output.md`, `evaluation.md`, `trace.md`, `patch.md`

Status: `created`

## 2. Compiled

```bash
python3 users/<id>/tools/scripts/compile_context.py users/<id>/projects/jah/sessions/YYYY-MM-DD-NNN
```

Populates `compiled_context.md` with dependencies, including registry types. Work should not start until context is compiled.

After compilation, resolve types for the session, project, and resolved workflows (`system/type_system.md`). Run a **gap-fill scan** (`proactive_capture.md`).

## 3. Worked

Agent or human executes the task using compiled context. Writes stay inside the session folder (L2).

During work, **watch for capture signals** — stable facts, workflows, type shapes, tool opportunities, or system friction.

## 4. Evaluated

Fill `evaluation.md` — requirements, rules, workflow criteria, references.

## 5. Traced

Fill `trace.md` — what happened, what was learned, what failed.

## 6. Patched (optional)

Fill `patch.md` — proposed changes to the principal (registry, types, instances, tools).

Summarize capture offers not yet decided. Profile updates must go through `patch.md`.

## End state

Session folder is a complete record. Stable instances change only if you apply patch proposals.

## System changes

To change how Jah works globally, edit `system/` and open a GitHub PR — not via session patch alone.
