# Session Type

One temporary workspace under a project. Example: `users/<principal>/projects/jah/sessions/YYYY-MM-DD-001/`.

**Agents:** read this file before creating or working in a session.

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
2. Create sessions with `python3 users/<id>/tools/scripts/new_session.py <project> "Goal"` (optional `--workflow-id`).
3. Compile context before work: `python3 users/<id>/tools/scripts/compile_context.py <session-path>`.
4. Read `compiled_context.md` and run **active discovery** (`system/discovery_protocol.md`).
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
