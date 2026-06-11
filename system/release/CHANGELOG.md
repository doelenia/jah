# Changelog

All notable changes to the Jah system (`system/`) are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.2] - 2026-06-11

### Added

- Document connector access methods (MCP vs native CLI) and compile connectors index


## [0.4.1] - 2026-06-10

### Changed

- Rename principal `tools` field and folder to `connectors` — external services, devices, MCP, custom glue (`type.principal`, agent docs, engines)
- Add `system/release/scripts/migrate_tools_to_connectors.py` for local principal migration


## [0.4.0] - 2026-06-10

### Added

- `system/instance.yaml` — declared system layers (agent, bootstrap, engines, release, interface)
- `system/README.md` and per-layer READMEs
- `system/engines/` — protocol runtime grouped by domain (knowledge, context, registry, structure, session, instances)
- `system/engines/cli.py` — unified CLI for all protocol engines
- `system/interface/` — reserved layer stub for future human-facing surfaces
- Compatibility shims at `system/scripts/` forwarding to `system/release/scripts/`

### Changed

- Agent protocol docs moved to `system/agent/` (from flat `system/*.md`)
- Release artifacts moved to `system/release/` (`VERSION`, `CHANGELOG.md`, `versioning.md`, scripts)
- `init_jah.py` no longer copies Python scripts to principals — engines stay in `system/engines/`
- `type.principal` `tools` field is optional — integrations only (MCP, custom glue), not protocol code
- `design_logic.md` — system layer model and spec↔engine pairing
- All docs, `CLAUDE.md`, bootstrap SETUP, and type READMEs updated for new paths and CLI

### Removed

- `system/bootstrap/tools/` — runtime code consolidated under `system/engines/`

## [0.3.1] - 2026-06-10

### Added

- **Operation model** (Orient → Plan → Act → Capture) as top-priority default in `protocol.md`
- **Operation Checklist** preamble in `compile_context.py` — first section after Session Goal in every compiled context
- **Scope expansion** mandatory step in `discovery_protocol.md` — enumerate relevant paths before implementation; Session plan in `trace.md`

### Changed

- `session_lifecycle.md`, `context_compilation.md`, `CLAUDE.md`, `.cursor/rules/jah-system.mdc` — align with orient/plan before act

## [0.3.0] - 2026-06-10

### Added

- `system/knowledge_base.md` — curated IP engine: OECD FORD field topics, entry schema, facet separation, agent create/update/find/audit protocol
- `system/bootstrap/knowledge-base/` — topics.yaml (full FORD L1+L2 + `general.uncategorized`), index.yaml, instance.yaml scaffold
- Bootstrap tool scripts: `knowledge_lib.py`, `resolve_knowledge.py`, `validate_knowledge.py`
- `compile_context.py` — **Matched Knowledge** section; loads `knowledge_base.md` in agent protocol
- Principal `knowledge_base` field on `type.principal`; init copies `knowledge-base/` and tool scripts

### Changed

- Read order includes `knowledge_base.md` after `discovery_protocol.md`
- `proactive_capture.md`, `discovery_protocol.md`, `context_compilation.md`, `permission_model.md`, `principal_model.md`, `glossary.md`, `session_lifecycle.md`, `improvement_protocol.md`, `protocol.md`, `storage_rules.md`, `design_logic.md`, `CLAUDE.md`, bootstrap `SETUP.md` — knowledge-base integration
- `init_jah.py` — scaffolds knowledge-base and copies bootstrap scripts

## [0.2.1] - 2026-06-10

### Added

- `system/discovery_protocol.md` — active search, discovery log, reference checklist, auto-update vs ask table
- Goal-aware `compile_context.py`: scoped types, linked/related tasks and sessions, grown project fields, all preferences, project rules
- Session `task_id` field; evaluation and trace templates with reference checklist and discovery log
- Principal auto-update permission (L3): existing instances and types without approval; profile and new registry entries still require ask; system/ requires explicit request

### Changed

- `permission_model.md`, `proactive_capture.md`, `improvement_protocol.md`, `session_lifecycle.md`, `context_compilation.md`, `protocol.md` — aligned with discovery and auto-update model
- `patch.md` scope narrowed to profile, new registry types, and system proposals


## [0.2.0] - 2026-06-10

### Added

- Open structure strategy: `system/open_structure.md`; `open_fields` default on `type.base`; container baseline `fields`
- `type.type_package` starter type for improvable type folders
- `type.task` starter type with directory container scaffold
- Structural parity validation (`validate_structure.py`) documented in protocol
- Protocol read order and setup updated for open structure and venv


## [0.1.1] - 2026-06-10

### Added

- Principal architecture: users/<id>/ layout with registry.yaml and bootstrap
- Replace legacy memory/types/tools root paths; remove work_pattern
- Unify terminology: system (not kernel), principal (not top-level memory)


## [0.1.0] - 2026-06-09

### Added

- System versioning with `system/VERSION` and `system/CHANGELOG.md`
- Root `README.md` for open-source discovery (intro, quick start, recent updates)
- `system/scripts/bump_release.py` and `check_release.py` for release workflow and pre-commit guard
- `system/versioning.md` — release workflow and semver policy
- Protocol, storage, improvement, design, and glossary docs updated for versioning
