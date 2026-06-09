# Design Logic

## Philosophy

Jah should not be a black-box assistant. It is a local-first, inspectable, self-improving personal automation memory.

## Shared kernel vs local world

| Layer | Role | Git |
|-------|------|-----|
| `system/` | Universal protocol — how Jah works | Tracked on GitHub |
| `types/` | Reusable forms | Local only |
| `memory/` | Living instances | Local only |
| `tools/` | Executable capabilities | Local only |

Customization stays private. The protocol stays portable via GitHub.

## Core concepts

- **Types** define reusable forms (structure, defaults, permissions).
- **Memory** stores living instances; every instance folder has `instance.yaml`.
- **Tools** provide capabilities (MVP: local Python scripts).
- **Sessions** create isolated workspaces for one task.
- **Context compilation** loads dependencies before work so improvements propagate automatically.
- **Traces** record what happened; **patch.md** proposes local changes for manual review.

## Agent tooling

Each AI tool (Cursor, Claude Code, OpenCode, etc.) may create its own root config (`.cursor/`, `.claude/`, etc.). Jah does not maintain an `agents/` folder. Tool-specific rules live in those dot-folders; portable guidance lives in local `CLAUDE.md` and `system/`.

## Improvement

- **Kernel (`system/`)** → edit, commit, GitHub PR.
- **Local layers** → edit directly or via session `patch.md`; never auto-applied.
- No central patch queue. No `patches/` folder.

## Key differentiation

Stable workflow improvement through dependency-aware context compilation. When you add a global writing rule, blog and social-post sessions compile it automatically because work patterns depend on preferences and active rules.
