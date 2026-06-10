# Session Lifecycle

Stages of a Jah session.

## 1. Created

```bash
python tools/scripts/new_session.py memory/projects/jah "Goal here"
# optional: --workflow-id workflow.jah.blog
```

Creates `memory/projects/jah/sessions/YYYY-MM-DD-NNN/` with:

- `instance.yaml` — goal, main_instance, optional `workflow_id` / `workflow` / `target_type`, permissions
- `input.md` — goal text
- Empty placeholders: `compiled_context.md`, `output.md`, `evaluation.md`, `trace.md`, `patch.md`

Status: `created`

## 2. Compiled

```bash
python tools/scripts/compile_context.py memory/projects/jah/sessions/YYYY-MM-DD-NNN
```

Populates `compiled_context.md` with dependencies, including type YAMLs and type READMEs (agent protocols). Work should not start until context is compiled.

After compilation, resolve types for the session, project, and any **resolved workflows** in scope (`system/type_system.md`). Run a **gap-fill scan** (`proactive_capture.md`): identify missing profile fields, preferences, rules, or project context needed for the session goal. Ask the user before proceeding if gaps would likely cause wrong output.

## 3. Worked

Agent or human executes the task using compiled context. Writes stay inside the session folder (L2).

During work, **watch for capture signals** — stable facts, repeatable workflows, reusable type shapes, tool opportunities, or kernel friction. Offer to capture at natural pauses; do not auto-promote to stable layers.

## 4. Evaluated

Fill `evaluation.md` — did the output meet requirements, rules, and resolved workflow criteria? Confirm that `output.md`, `patch.md`, and `trace.md` include references when they drew on specific internal paths or external links. Note whether proactive gap-fill or capture would have improved the outcome.

## 5. Traced

Fill `trace.md` — what happened, what was learned, what failed.

## 6. Patched (optional)

Fill `patch.md` — proposed changes to local memory, types, or tools. Review and apply manually.

Before closing the session, **summarize capture offers** not yet decided and ensure `patch.md` includes all proposals the user approved or deferred.

If the session surfaced new or corrected stable personal facts, `patch.md` must propose updates to `memory/personal/profile.md`. Do not write profile directly.

Every `patch.md` proposal must cite the internal path or external link that informed each change.

## End state

Session folder is a complete record. Stable memory changes only if you explicitly apply patch proposals.

## Kernel changes

To change how Jah works globally, edit `system/` and open a GitHub PR — not via session patch alone.
