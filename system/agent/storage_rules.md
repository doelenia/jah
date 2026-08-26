# Storage Rules

Where things live and what not to move.

## Two layers

| Layer | Path | Purpose | Git |
|-------|------|---------|-----|
| System | `system/` | Protocol, bootstrap, design docs, release scripts | **Tracked** |
| Principal | `users/<id>/` | Registry, types, instances, optional connectors | Local |

## Default creation target — local jah repo

**New sessions, documents, and any regular files are created inside this repo under `users/<active_principal>/…` by default.** This is the home for created content unless the user explicitly names an external surface *for that item*.

- Do **not** create or write content in an external surface (Notion, Google Docs, Drive, etc.) unless the user names it for the thing being created ("put this in Notion", "make a Google Doc"). "Create a session in `<project>`" means the **local** project, even when a same-named page exists externally.
- A local instance **may reference** an external page without the content living there — e.g. a `notion_url:` field on the instance (see `users/<id>/projects/*/instance.yaml`). Referencing ≠ authoring there.
- External surfaces reached through `connectors/` are **read-first**. Writing/publishing to them is an external action that requires explicit user direction (`permission_model.md`).

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
  projects/           # project instances (archive/ field is not a project — see archive.md)
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

Sessions live under the parent project's `sessions/` folder:

| Project state | Path |
|---------------|------|
| Active | `users/<id>/projects/<project>/sessions/YYYY-MM-DD-NNN/` |
| Archived | `users/<id>/projects/archive/<project>/sessions/YYYY-MM-DD-NNN/` |

See `archive.md`.

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
