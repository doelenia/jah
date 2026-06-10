# Storage Rules

Where things live and what not to move.

## Four layers

| Layer | Path | Purpose | Git |
|-------|------|---------|-----|
| System | `system/` | Kernel, protocol, design docs | **Tracked** |
| Types | `types/` | Reusable type definitions | Local |
| Memory | `memory/` | Living instances | Local |
| Tools | `tools/` | Scripts, future MCP | Local |

## Git policy

GitHub tracks the **kernel and landing page**: `system/`, root `README.md`, and `.gitignore`. Everything else is local customization and must not be committed.

```
.gitignore pattern:
  ignore *
  except .gitignore, README.md, and system/**
```

Kernel version and history: `system/VERSION`, `system/CHANGELOG.md` (see `versioning.md`).

Local-only paths include: `types/`, `memory/`, `tools/`, `CLAUDE.md`, `requirements.txt`, sessions, outputs, and agent-service folders.

## What we do not create

- **`agents/`** — no LifeOS-managed agent instruction folder. Each AI tool owns its config.
- **`patches/`** — no central patch queue. Session `patch.md` is a local working proposal.

## Agent-service folders

Tools like Cursor or Claude Code may create dot-folders at the repo root (`.cursor/`, `.claude/`, etc.). These are:

- Not part of the Jah layer model
- Not scaffolded in MVP
- Not tracked on GitHub
- Not stable memory unless you manually promote content via local edits

Do not nest them under `types/`, `memory/`, or `tools/`.

## Sessions

Sessions live under `memory/projects/<project>/sessions/YYYY-MM-DD-NNN/`. All session artifacts (input, output, trace, patch, compiled context) are local.

## Reusable resources (files)

PDFs, images, video, audio, and other binary assets that should persist across sessions live under **`sources/`**, not in session folders.

| Scope | Path |
|-------|------|
| Project | `memory/projects/<project>/sources/files/` |
| Personal (cross-project) | `memory/personal/sources/files/` |

Every stored file must have a catalog entry in the matching `sources/index.md`. Full protocol: `types/source/README.md` and `system/memory_model.md` — Sources.

## Instance rule

Every folder representing a living instance should contain `instance.yaml` with at least `id`, `type`, and `name`.

Container instances (project, personal, session) should also declare child field instances in a `fields:` block. Each field must reference a type defined in `types/<name>/type.yaml`. Before creating or editing a field, read that type's `README.md` — see `system/type_system.md`.
