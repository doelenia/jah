# Changelog

All notable changes to the Jah system (`system/`) are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
