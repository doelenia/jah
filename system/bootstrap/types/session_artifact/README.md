# Session Artifact Type

A required session working file (`input.md`, `output.md`, `evaluation.md`, `trace.md`, `patch.md`, `compiled_context.md`).

**Agents:** read this file when creating or closing session artifacts.

## Storage

Each artifact path is declared in `types/session/type.yaml` and created by `new_session.py`.

## Agent protocol

1. Read `users/<principal>/types/session/README.md` and `types/session/type.yaml`.
2. Write freely inside the session folder (L2) for all session artifacts.
3. End every session with complete `output.md`, `evaluation.md`, `trace.md`, and `patch.md`.
4. Include **References** in `output.md`, `trace.md`, and `patch.md` when content drew on specific sources.

## Required artifacts

| File | Role |
|------|------|
| `input.md` | Session input and clarifications |
| `compiled_context.md` | Compiled dependencies (via `compile_context.py`) |
| `output.md` | Task deliverable |
| `evaluation.md` | Did output meet requirements and rules? |
| `trace.md` | What happened; capture offers deferred |
| `patch.md` | Proposed stable-memory and type changes |
