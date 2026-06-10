# Discovery Protocol

How Jah agents actively link relevant files before and during work.

## Purpose

Compiled context pre-loads goal-matched dependencies. Agents still **discover** anything missing — search, read, document, and ask when unsure.

## When to run

| Checkpoint | Action |
|------------|--------|
| After compilation | Review compiled sections; run active discovery for gaps |
| Before writing | Confirm types and instances in scope are read |
| During work | Follow references; search when a claim needs a source |
| Before session end | Complete discovery log and reference checklist in `trace.md` / `evaluation.md` |

## Active discovery steps

1. **Start from compiled context** — linked task, related tasks/sessions, grown project fields, scoped types.
2. **Search when gaps remain** — use repo search (`grep`, semantic search, `list_instances.py`) for:
   - project `tasks/`, `design/`, `sources/`, `context.md`
   - prior `sessions/` on the same topic
   - personal `profile.md`, `preferences/`, `rules/`
   - principal `types/<name>/` when schema is in scope
   - `system/` docs when changing protocol (L5 — ask first)
3. **Read before acting** — resolve `instance.yaml` → type → README for every instance you touch.
4. **Document in `trace.md`** under **Discovery log**:

```markdown
## Discovery log

| Path | Why read | Used? |
|------|----------|-------|
| users/.../tasks/foo/instance.yaml | Linked task | yes |
| system/open_structure.md | Goal keyword match | yes |
```

5. **Ask the user** when:
   - Missing info would cause wrong output
   - Unsure whether a fact belongs in stable memory or the session
   - A **system/** change seems needed (always ask before editing `system/`)
   - A **profile** update is warranted (always ask before editing `profile.md`)

## Auto-update vs ask

| Target | Agent may update without asking | Must ask first |
|--------|----------------------------------|----------------|
| Existing principal instances (tasks, context, design, rules, prefs, sources, workflows) | Yes | — |
| Existing principal type definitions (`users/<id>/types/`) | Yes | — |
| Principal tools (`users/<id>/tools/`) | Yes | — |
| New registry type registration | — | Yes |
| Personal profile | — | Yes |
| `system/` | — | Yes (explicit request + PR) |

When auto-updating, cite the source path in the session `trace.md` and record what changed.

## Related docs

- `context_compilation.md` — what compile loads automatically
- `proactive_capture.md` — gap-fill, capture, improve
- `permission_model.md` — L2–L7 boundaries
- `session_lifecycle.md` — session checkpoints
