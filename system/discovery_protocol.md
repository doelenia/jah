# Discovery Protocol

How Jah agents actively link relevant files before and during work.

## Purpose

Compiled context pre-loads goal-matched dependencies. Agents still **discover** anything missing — search, read, document, and ask when unsure.

Discovery is not optional search after the fact. It starts with **scope expansion** so agents do not optimize for a single deliverable while missing related principal instances.

## When to run

| Checkpoint | Action |
|------------|--------|
| After compilation | Read Operation Checklist; run scope expansion; write Session plan in `trace.md` |
| Before implementation writes | Confirm plan lists files to read/update; types resolved |
| During work | Follow references; search when a claim needs a source |
| Before session end | Diff plan vs outcome; complete discovery log and reference checklist |

## Scope expansion (mandatory before implementation)

After reading compiled context, **enumerate candidate relevant paths** before choosing what to read or write.

1. **Project instance** — read `projects/<name>/instance.yaml` → `fields`; list every declared path (baseline + grown fields: `design/`, `tasks/`, `sources/`, …).
2. **Principal cross-links** — from compiled context and goal keywords:
   - knowledge entries whose `applies_to` matches this project, type, or workflow
   - linked and related tasks and sessions
   - personal rules/preferences when the goal touches them
3. **Work-type siblings** — for the kind of work (system feature, project doc, workflow, type patch): which sibling artifacts are usually also in scope?
   - project `design/`, `context.md`
   - `knowledge-base/` entries and index
   - related `types/<name>/` README and type.yaml
   - prior sessions on the same topic
4. **Record candidates** — add paths to **Session plan** in `trace.md` (read list and likely-update list) before any implementation write.

Scope expansion answers: *"What else might be relevant?"* — not *"What did the user message mention?"*

## Active discovery steps

1. **Start from compiled context** — Operation Checklist, linked task, related tasks/sessions, grown project fields, scoped types, matched knowledge.
2. **Scope expansion** — complete the four steps above; update Session plan in `trace.md`.
3. **Search when gaps remain** — use repo search (`grep`, semantic search, `list_instances.py`) for:
   - project `tasks/`, `design/`, `sources/`, `context.md`
   - prior `sessions/` on the same topic
   - personal `profile.md`, `preferences/`, `rules/`
   - `knowledge-base/` — `index.yaml`, `entries/`, `topics.yaml`; or `resolve_knowledge.py`
   - principal `types/<name>/` when schema is in scope
   - `system/` docs when changing protocol (L5 — ask first)
4. **Read before acting** — resolve `instance.yaml` → type → README for every instance you touch.
5. **Document in `trace.md`**:

```markdown
## Session plan

| Item | Path or note |
|------|----------------|
| Goal | (from session) |
| Files to read | users/.../design/, system/knowledge_base.md, … |
| Files likely to update | users/.../projects/jah/design/, knowledge-base/entries/, … |
| Open questions | … |

## Discovery log

| Path | Why read | Used? |
|------|----------|-------|
| users/.../tasks/foo/instance.yaml | Linked task | yes |
| users/.../knowledge-base/entries/foo.yaml | Matched knowledge | yes |
```

6. **Ask the user** when:
   - Missing info would cause wrong output
   - Unsure whether a fact belongs in stable memory or the session
   - A **system/** change seems needed (always ask before editing `system/`)
   - A **profile** update is warranted (always ask before editing `profile.md`)

## Auto-update vs ask

| Target | Agent may update without asking | Must ask first |
|--------|----------------------------------|----------------|
| Existing principal instances (tasks, context, design, rules, prefs, sources, workflows, knowledge-base) | Yes | — |
| Existing principal type definitions (`users/<id>/types/`) | Yes | — |
| Principal tools (`users/<id>/tools/`) | Yes | — |
| New registry type registration | — | Yes |
| Personal profile | — | Yes |
| `system/` | — | Yes (explicit request + PR) |

When auto-updating, cite the source path in the session `trace.md` and record what changed.

## Related docs

- `protocol.md` — operation model (Orient → Plan → Act → Capture)
- `knowledge_base.md` — knowledge entry protocol
- `context_compilation.md` — what compile loads automatically
- `proactive_capture.md` — gap-fill, capture, improve
- `permission_model.md` — L2–L7 boundaries
- `session_lifecycle.md` — session checkpoints
