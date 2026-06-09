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

GitHub tracks **`system/` only** (plus `.gitignore`). Everything else is local customization and must not be committed.

```
.gitignore pattern:
  ignore *
  except .gitignore and system/**
```

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

## Instance rule

Every folder representing a living instance should contain `instance.yaml` with at least `id`, `type`, and `name`.
