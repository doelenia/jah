# Context Compilation

## Why it exists

Sessions should not rely on vague memory. Before work starts, Jah collects relevant type definitions, preferences, rules, sources, and project context into one readable file: `compiled_context.md`.

This makes dependency logic explicit and recorded.

After compilation, agents should compare the session goal against compiled context and **gap-fill** any missing dependencies (`proactive_capture.md`) before executing work.

## How a session loads dependencies

Run:

```bash
python tools/scripts/compile_context.py memory/projects/<project>/sessions/<session-id>
```

The script deterministically loads:

1. `system/glossary.md`, `system/protocol.md`, `system/type_system.md`
2. Core type YAMLs and **type READMEs** (agent protocols for each built-in type)
3. Personal profile (`memory/personal/profile.md`)
4. Personal writing preferences
5. All active rules under `memory/personal/rules/` (including `general/`, `writing/`, etc.)
6. Project `context.md` and `instance.yaml`
7. Directory container boundaries (including `sources/index.md`, `workflows/index.md` when present)
8. **Resolved workflows** — selective, not all project workflows (see below)
9. Session `input.md`

Output sections: Session Goal, System Principles, Relevant Types, Personal Profile, Personal Preferences, Active Rules, Project Context, Project Instance, Directory Boundaries, Resolved Workflows, Available Workflows, Session Input, Required Output Files, Approval Boundaries.

Required session outputs must include **References** (internal paths and external links) when content draws on specific sources. See `memory_model.md` — References.

## Workflow resolution

Sessions are call sites. `compile_context.py` **resolves** which workflows to load full bodies for — it does not dump every workflow in the project.

### Session invocation fields

| Field | Purpose |
|-------|---------|
| `workflow_id` | Explicit call (strongest), e.g. `workflow.us_taxes.tax_filing` |
| `workflow` | Path relative to project, or `auto` for compile-time resolution |
| `target_type` | Hint for auto mode, e.g. `type.blog_post` |
Create sessions with an explicit workflow:

```bash
python tools/scripts/new_session.py memory/projects/us-taxes "Inventory 2025 tax documents" \
  --workflow-id workflow.us_taxes.tax_filing
```

### Resolution priority

1. **`workflow_id` set** → load that workflow + dependencies
2. **`workflow` path set** (not `auto`) → load that folder
3. **`target_type` set** → load active workflows where `operates_on` matches
4. **Goal/input keyword match** → match against `workflows/index.md`, workflow `name`, `description`
5. **Default** → list project-scoped active candidates in **Available Workflows** only; load full body if exactly one match

Personal workflows (`memory/personal/workflows/`) are included when `scope: personal` and `applies_to` matches the project or target type.

### Compiled workflow sections

- **Resolved Workflows** — invoked workflow instance, requirements, workflow body, evaluation, examples
- **Available Workflows** — catalog table of other active workflows not invoked

## How rules propagate

When you add a global writing rule under `memory/personal/rules/writing/`, every future session that compiles context will include it. Resolved workflows declare `dependencies` on preferences and rules; `evaluation.md` checks compliance.

## Example

1. You add `concrete_observation_first.yaml` as a global writing rule with `applies_to: workflow.jah.blog`.
2. A blog session sets `workflow_id: workflow.jah.blog` and runs `compile_context.py`.
3. Compiled context includes the rule under **Active Rules** and the blog workflow under **Resolved Workflows**.
4. `workflow.md` references global prefs and rules.
5. `evaluation.md` checks whether the output followed the rule.

Each workflow can adapt rules locally while still inheriting global rules through compilation.
