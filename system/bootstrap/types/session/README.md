# Session Type

One temporary workspace under a project. Example: `users/<principal>/projects/jah/sessions/YYYY-MM-DD-001/` (archived: `users/<principal>/projects/archive/<project>/sessions/…`).

**Agents:** read this file before creating or working in a session.

> **Default location — local repo.** Sessions (and their artifacts, and any regular files a session produces) are created **here in the local jah repo**, never on an external surface. "Create a session in `<project>`" always means the local `users/<principal>/projects/<project>/`, even when a same-named page exists in Notion or elsewhere. Only write to an external surface when the user names it for that specific item. See `system/agent/storage_rules.md` § *Default creation target*.

## Structure

```
users/<principal>/projects/<project>/sessions/
  instance.yaml              # type: directory, content_type: session — read before creating sessions
  YYYY-MM-DD-NNN/
    instance.yaml
    input.md
    compiled_context.md
    output.md
    evaluation.md
    trace.md
    patch.md
```

## Agent protocol

1. Read `users/<principal>/types/session/type.yaml` and this README.
2. Create sessions with `python3 system/engines/cli.py new-session <project> "Goal"` (optional `--workflow-id`).
3. Compile context before work: `python3 system/engines/cli.py compile-context <session-path>`.
4. Read `compiled_context.md` and run **active discovery** (`system/agent/discovery_protocol.md`).
5. Resolve `main_instance` → read parent project `instance.yaml` and relevant field type READMEs.
6. Link tasks: set `task_id` on the session or `session` on the task when work starts.
7. Write session artifacts freely (L2). Update existing principal instances/types directly when capture is clear (L3).
8. Ask before profile updates, new registry entries, or `system/` changes.
9. End with complete `output.md`, `evaluation.md` (reference checklist), `trace.md` (discovery log), and `patch.md` (profile/system/new-type proposals only).

## Field types

| Field | Type | Notes |
|-------|------|-------|
| `goal` | scalar | Set at creation |
| `main_instance` | type.project | Parent project path |
| `workflow_id` | scalar | Explicit workflow invocation |
| `workflow` | scalar | Path relative to project, or `auto` |
| `target_type` | scalar | Hint for auto resolution |
| `task_id` | scalar | Optional linked task |
| `input`, `output`, … | type.session_artifact | See `types/session_artifact/README.md` |
