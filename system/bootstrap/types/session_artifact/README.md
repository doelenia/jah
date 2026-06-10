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
5. Include **Discovery log** in `trace.md` and the **reference checklist** in `evaluation.md` (`system/discovery_protocol.md`).

## Required artifacts

| File | Role |
|------|------|
| `input.md` | Session input and clarifications |
| `compiled_context.md` | Goal-matched dependencies (via `compile_context.py`) |
| `output.md` | Task deliverable; **References** |
| `evaluation.md` | Requirements, rules, **References consulted**, **Stable updates**, **Open questions** |
| `trace.md` | **Discovery log**, steps, **References** |
| `patch.md` | Profile, new registry type, and system proposals only |

## patch.md scope

Use `patch.md` only for changes that require approval:

- personal profile updates
- new registry type registration
- system change proposals (reference for PR)

Existing principal instances and types may be updated directly during work; record in `trace.md`.
