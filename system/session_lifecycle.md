# Session Lifecycle

Stages of a Jah session.

## 1. Created

```bash
python3 users/<id>/tools/scripts/new_session.py users/<id>/projects/jah "Goal here"
# optional: --workflow-id workflow.jah.blog
```

Creates `users/<id>/projects/jah/sessions/YYYY-MM-DD-NNN/` with:

- `instance.yaml` — goal, main_instance, optional `workflow_id` / `workflow` / `target_type` / `task_id`, permissions
- `input.md` — goal text
- Placeholders: `compiled_context.md`, `output.md`, `evaluation.md`, `trace.md`, `patch.md`

Status: `created`

## 2. Compiled

```bash
python3 users/<id>/tools/scripts/compile_context.py users/<id>/projects/jah/sessions/YYYY-MM-DD-NNN
```

Populates `compiled_context.md` with goal-matched dependencies. Work should not start until context is compiled.

After compilation:

1. Resolve types for the session, project, and resolved workflows (`system/type_system.md`).
2. Run a **gap-fill scan** (`proactive_capture.md`).
3. Start the **discovery log** in `trace.md` (`discovery_protocol.md`).

## 3. Worked

Agent or human executes the task using compiled context. Writes stay inside the session folder (L2) for session artifacts.

During work:

- **Watch for capture signals** — stable facts, workflows, type shapes, tool opportunities, or system friction.
- **Auto-update existing principal instances and types** when capture targets are clear; log in `trace.md`.
- **Ask** before profile updates, new registry entries, or `system/` changes.

## 4. Evaluated

Fill `evaluation.md`:

- Success criteria
- **References consulted** (checklist)
- **Stable updates** applied or offered
- **Open questions** for the user

## 5. Traced

Fill `trace.md`:

- **Discovery log** — paths searched/read and whether used
- Steps taken
- **References** behind key decisions

## 6. Patched (optional)

Fill `patch.md` for:

- Profile update proposals
- New registry type proposals
- System change proposals (for PR)
- Deferred offers

Principal instance and type updates applied during work do not need to be duplicated in `patch.md`.

## End state

Session folder is a complete record. Profile and new registry changes apply only after approval. System changes ship via GitHub PR.

## System changes

To change how Jah works globally, edit `system/` and open a GitHub PR — only when the user explicitly requests it.
