# Context Compilation

## Why it exists

Sessions should not rely on vague memory. Before work starts, Jah collects relevant type definitions, preferences, rules, sources, and project context into one readable file: `compiled_context.md`.

This makes dependency logic explicit and recorded.

## How a session loads dependencies

Run:

```bash
python tools/scripts/compile_context.py memory/projects/<project>/sessions/<session-id>
```

The script deterministically loads:

1. `system/glossary.md`, `system/protocol.md`
2. Core type YAMLs (`base`, `session`, `project`, `preference`, `rule`, `work_pattern`)
3. Personal writing preferences
4. All active rules in `memory/personal/rules/writing/`
5. Project `context.md`
6. Work pattern files (`requirements.md`, `workflow.md`, `evaluation.md`, `examples.md`)
7. Session `input.md`

Output sections: Session Goal, System Principles, Relevant Types, Personal Preferences, Active Rules, Project Context, Work Patterns, Session Input, Required Output Files, Approval Boundaries.

## How rules propagate

When you add a global writing rule under `memory/personal/rules/writing/`, every future session that compiles context will include it — as long as the work pattern depends on writing preferences and rules.

## Example

1. You add `concrete_observation_first.yaml` as a global writing rule.
2. A blog session under `memory/projects/jah/` runs `compile_context.py`.
3. Compiled context includes the rule under **Active Rules**.
4. The blog work pattern's workflow references global prefs and rules.
5. `evaluation.md` checks whether the output followed the rule.

Each work pattern can adapt rules locally in its own workflow while still inheriting global rules through compilation.
