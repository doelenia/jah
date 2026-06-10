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
4. Read `compiled_context.md` and the session `instance.yaml`.
5. Resolve `main_instance` → read parent project `instance.yaml` and relevant field type READMEs.
6. If `workflow_id` or `workflow` is set, compiled context includes resolved workflow bodies.
7. Write only inside the session folder (L2) unless user approves stable-memory changes.
8. End with complete `output.md`, `evaluation.md`, `trace.md`, `patch.md`.

## Field types

| Field | Type | Notes |
|-------|------|-------|
| `goal` | scalar | Set at creation |
| `main_instance` | type.project | Parent project path |
| `workflow_id` | scalar | Explicit workflow invocation |
| `workflow` | scalar | Path relative to project, or `auto` |
| `target_type` | scalar | Hint for auto resolution |
| `input`, `output`, … | type.session_artifact | See `types/session_artifact/README.md` |
