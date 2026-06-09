# Session Lifecycle

Stages of a Jah session.

## 1. Created

```bash
python tools/scripts/new_session.py memory/projects/jah "Goal here"
```

Creates `memory/projects/jah/sessions/YYYY-MM-DD-NNN/` with:

- `instance.yaml` — goal, main_instance, permissions
- `input.md` — goal text
- Empty placeholders: `compiled_context.md`, `output.md`, `evaluation.md`, `trace.md`, `patch.md`

Status: `created`

## 2. Compiled

```bash
python tools/scripts/compile_context.py memory/projects/jah/sessions/YYYY-MM-DD-NNN
```

Populates `compiled_context.md` with dependencies. Work should not start until context is compiled.

## 3. Worked

Agent or human executes the task using compiled context. Writes stay inside the session folder (L2).

## 4. Evaluated

Fill `evaluation.md` — did the output meet requirements, rules, and work pattern criteria?

## 5. Traced

Fill `trace.md` — what happened, what was learned, what failed.

## 6. Patched (optional)

Fill `patch.md` — proposed changes to local memory, types, or tools. Review and apply manually.

## End state

Session folder is a complete record. Stable memory changes only if you explicitly apply patch proposals.

## Kernel changes

To change how Jah works globally, edit `system/` and open a GitHub PR — not via session patch alone.
