# Session Lifecycle

Stages of a Jah session.

## 1. Created

```bash
python3 system/engines/cli.py new-session users/<id>/projects/jah "Goal here"
# optional: --workflow-id workflow.jah.blog
```

Creates `users/<id>/projects/jah/sessions/YYYY-MM-DD-NNN/` with:

- `instance.yaml` — goal, main_instance, optional `workflow_id` / `workflow` / `target_type` / `task_id`, permissions
- `input.md` — goal text
- Placeholders: `compiled_context.md`, `output.md`, `evaluation.md`, `trace.md`, `patch.md`

Status: `created`

## 2. Compiled

```bash
python3 system/engines/cli.py compile-context users/<id>/projects/jah/sessions/YYYY-MM-DD-NNN
```

Populates `compiled_context.md` with goal-matched dependencies. Work should not start until context is compiled.

After compilation:

1. **Orient** — read Operation Checklist and compiled context; run scope expansion (`discovery_protocol.md`).
2. **Plan** — write Session plan in `trace.md` (files to read, likely updates, open questions) **before implementation writes**.
3. Resolve types for the session, project, and resolved workflows (`type_system.md`).
4. Start the **discovery log** in `trace.md` as you read.

## 3. Worked

Agent or human executes the task using compiled context. Writes stay inside the session folder (L2) for session artifacts.

During work:

- **Re-orient on scope shift** — when write target or instance type changes, run `resolve-rules` and log a rule checkpoint in `trace.md` (`discovery_protocol.md` § Rule checkpoints).
- **Watch for capture signals** — stable facts, audited wisdom, workflows, type shapes, tool opportunities, or system friction.
- **Auto-update existing principal instances and types** when capture targets are clear (including `knowledge-base/`); log in `trace.md`.
- **Ask** before profile updates, new registry entries, or `system/` changes.

## 4. Evaluated

Fill `evaluation.md`:

- Success criteria
- **References consulted** (checklist — include `knowledge.<id>` when cited)
- **Stable updates** applied or offered
- **Open questions** for the user
- Unpromoted session IP that should become knowledge entries

## 5. Traced

Fill `trace.md`:

- **Session plan** — files to read, likely updates, open questions (written before implementation)
- **Rule checkpoints** — trigger, target, active rule ids (on scope shift or principal writes)
- **Discovery log** — paths searched/read and whether used
- Steps taken
- **References** behind key decisions
- Plan vs outcome at session end

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
