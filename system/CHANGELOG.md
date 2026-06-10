# Changelog

All notable changes to the Jah system (`system/`) are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
