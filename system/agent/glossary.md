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
| **system version** | kernel version | Semver in `system/release/VERSION` |
| **engine** | tool (system) | Protocol runtime under `system/engines/` |
| **connector** | integration, principal tool, tools (principal) | Optional wiring under `users/<id>/connectors/` |

## Core terms

| Term | Meaning |
|------|---------|
| **Type** | Reusable form — `users/<id>/types/<name>/type.yaml` + README, registered in `registry.yaml` |
| **Instance** | A living thing under a principal (profile, project, workflow, session, etc.) |
| **Principal** | Namespace at `users/<id>/` — registry, types, personal, projects, optional connectors |
| **Registry** | `users/<id>/registry.yaml` — maps type names to paths and `extends` chains |
| **Bootstrap** | First-time copy from `system/bootstrap/` into a new principal |
| **Stable instances** | Long-lived instances (profile, context, workflows, sources) — vs session workspace |
| **Connector** | Optional principal-specific wiring under `users/<id>/connectors/` — documents access method (MCP or native CLI); see `connectors.md` |
| **Connector access (MCP)** | External service via Model Context Protocol — requires per-agent MCP config documented in connector README |
| **Connector access (native CLI)** | External service via principal script/shell — agent-agnostic; no MCP setup |
| **Engine** | System protocol runtime under `system/engines/` |
| **Session** | Temporary working instance under a project |
| **Trace** | Record of what happened during a session |
| **Reference** | Citation of a source; internal = repo-relative path, external = full URL |
| **Profile** | Canonical personal facts in `users/<id>/personal/profile.md`; updated via `patch.md` |
| **Operation model** | Default agent phases: Orient → Plan → Act → Capture (`protocol.md`) |
| **Session plan** | Pre-implementation scope in `trace.md` — files to read, likely updates, open questions |
| **Context compilation** | Collecting goal-matched types, preferences, rules, tasks, sessions, sources, and session input before work |
| **Discovery protocol** | Active search, discovery log, and reference checklist — see `discovery_protocol.md` |
| **Knowledge base** | Curated IP index at `knowledge-base/` — see `knowledge_base.md` |
| **Knowledge entry** | One audited wisdom item in `knowledge-base/entries/` registered in `index.yaml` |
| **Topic** | FORD field facet on an entry: `domain.field` from `topics.yaml` |
| **Context facet** | Where wisdom applies: `applies_to` refs (project, type, workflow, rule) |
| **Proactive capture** | Agent behavior: gap-fill, capture, improve — see `proactive_capture.md` |
| **Workflow** | Callable procedure (`type.workflow`); invoked by sessions via `workflow_id` |
| **System version** | Semver in `system/release/VERSION` for tracked system releases on GitHub |
| **Changelog** | Release history in `system/release/CHANGELOG.md` |
| **Archive** | `projects/archive/` — directory (`kind: project_archive`) of archived project instances; not itself a project (`archive.md`) |
| **Open structure** | Declared folder meaning via `instance.yaml` `fields`; default open growth (`open_structure.md`) |
| **System layer** | Declared field under `system/instance.yaml` (agent, bootstrap, engines, release, interface) |
| **Baseline fields** | Minimal `fields` on a container type — every instance must scaffold from this |
| **Grown fields** | Extra `fields` on an instance beyond the type baseline |
| **Type package** | `types/<name>/` as living container + leaf schema (`type.type_package`) |
| **Structural parity** | Declared `fields` match on-disk layout; checked by `validate_structure.py` |

## Layers

1. **`system/`** — Declared layers: agent, bootstrap, engines, release (tracked on GitHub)
2. **`users/<id>/`** — Principal local world: registry, types, instances, optional connectors (local)

Agent-service folders (`.cursor/`, `.claude/`) are outside this model.
