# Glossary

Use this vocabulary consistently across Jah. **One term per concept** — do not use synonyms in docs or scripts.

## Terminology canon

| Use | Never use | Meaning |
|-----|-----------|---------|
| **system** | kernel | Tracked protocol layer at `system/` |
| **principal** | (top-level) memory | A user's local world: `users/<id>/` |
| **registry** | built-in types | `registry.yaml` — authoritative type index for a principal |
| **bootstrap** | — | `system/bootstrap/` — copy-once starter kit |
| **starter types** | built-in types | Types copied from bootstrap into `users/<id>/types/` |
| **instance** | — | Living thing with `instance.yaml` |
| **type** | — | Schema registered in the principal's registry |
| **workflow** | work_pattern | Callable `type.workflow` instance |
| **system version** | kernel version | Semver in `system/VERSION` |

## Core terms

| Term | Meaning |
|------|---------|
| **Type** | Reusable form — `users/<id>/types/<name>/type.yaml` + README, registered in `registry.yaml` |
| **Instance** | A living thing under a principal (profile, project, workflow, session, etc.) |
| **Principal** | Namespace at `users/<id>/` — registry, types, personal, projects, tools |
| **Registry** | `users/<id>/registry.yaml` — maps type names to paths and `extends` chains |
| **Bootstrap** | First-time copy from `system/bootstrap/` into a new principal |
| **Stable instances** | Long-lived instances (profile, context, workflows, sources) — vs session workspace |
| **Tool** | Executable capability under `users/<id>/tools/` |
| **Session** | Temporary working instance under a project |
| **Trace** | Record of what happened during a session |
| **Reference** | Citation of a source; internal = repo-relative path, external = full URL |
| **Profile** | Canonical personal facts in `users/<id>/personal/profile.md`; updated via `patch.md` |
| **Patch** | Local proposal for improvement (session `patch.md`; not auto-applied) |
| **Context compilation** | Collecting goal-matched types, preferences, rules, tasks, sessions, sources, and session input before work |
| **Discovery protocol** | Active search, discovery log, and reference checklist — see `discovery_protocol.md` |
| **Proactive capture** | Agent behavior: gap-fill, capture, improve — see `proactive_capture.md` |
| **Workflow** | Callable procedure (`type.workflow`); invoked by sessions via `workflow_id` |
| **System version** | Semver in `system/VERSION` for tracked system releases on GitHub |
| **Changelog** | Release history in `system/CHANGELOG.md` |
| **Open structure** | Declared folder meaning via `instance.yaml` `fields`; default open growth (`system/open_structure.md`) |
| **Baseline fields** | Minimal `fields` on a container type — every instance must scaffold from this |
| **Grown fields** | Extra `fields` on an instance beyond the type baseline |
| **Type package** | `types/<name>/` as living container + leaf schema (`type.type_package`) |
| **Structural parity** | Declared `fields` match on-disk layout; checked by `validate_structure.py` |

## Layers

1. **`system/`** — Shared protocol, bootstrap, release scripts (tracked on GitHub)
2. **`users/<id>/`** — Principal local world: registry, types, instances, tools (local)

Agent-service folders (`.cursor/`, `.claude/`) are outside this model.
