# Storage Rules

Where things live and what not to move.

## Two layers

| Layer | Path | Purpose | Git |
|-------|------|---------|-----|
| System | `system/` | Protocol, bootstrap, design docs, release scripts | **Tracked** |
| Principal | `users/<id>/` | Registry, types, instances, optional connectors | Local |

## Active principal

Repo root `jah.yaml`:

```yaml
active_principal: <id>
```

Scripts and agents resolve `users/<active_principal>/` for all local work.

Declared instance `fields` must match on-disk layout — run `python3 system/engines/cli.py validate-structure` (`open_structure.md`).

## Principal layout

```
users/<id>/
  instance.yaml       # type: principal
  registry.yaml       # type registry
  types/              # registered type definitions
  personal/           # cross-project instances
  projects/           # project instances
  knowledge-base/     # curated knowledge index (see knowledge_base.md)
  connectors/         # optional — external services, devices, MCP configs
```

## Git policy

GitHub tracks the **system and landing page**: `system/`, root `README.md`, and `.gitignore`. Everything else is local and must not be committed.

```
.gitignore pattern:
  ignore *
  except .gitignore, README.md, and system/**
```

System version and history: `system/release/VERSION`, `system/release/CHANGELOG.md` (see `../release/versioning.md`).

Local-only paths include: `users/`, `jah.yaml`, `CLAUDE.md`, `requirements.txt`, sessions, outputs, and agent-service folders.

## Bootstrap

Uninitialized repos copy `system/bootstrap/` via `system/release/scripts/init_jah.py`. See `../bootstrap/SETUP.md`.

## What we do not create

- **`agents/`** — no Jah-managed agent instruction folder.
- **`patches/`** — no central patch queue. Session `patch.md` is a local working proposal.
- **Root `memory/`, `types/`, `tools/`** — legacy; use principal paths only.

## Agent-service folders

Tools like Cursor or Claude Code may create dot-folders at the repo root. These are:

- Not part of the Jah layer model
- Not tracked on GitHub
- Not stable instances unless manually promoted

Do not nest them under `users/`.

## Sessions

Sessions live under `users/<id>/projects/<project>/sessions/YYYY-MM-DD-NNN/`.

## Reusable resources (files)

PDFs, images, video, and other binary assets live under **`sources/`** within personal or project scope.

| Scope | Path |
|-------|------|
| Project | `users/<id>/projects/<project>/sources/files/` |
| Personal | `users/<id>/personal/sources/files/` |

Catalog every file in the matching `sources/index.md`. Protocol: `users/<id>/types/source/README.md` and `system/principal_model.md`.

## Instance rule

Every folder representing a living instance should contain `instance.yaml` with at least `id`, `type`, and `name`.

Resolve `type` through `registry.yaml` before reading `type.yaml`. See `system/type_system.md`.
