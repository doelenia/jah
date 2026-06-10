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

- **Types** define reusable forms (structure, typed fields, agent protocols in READMEs).
- **Memory** stores living instances; every instance folder has `instance.yaml`.
- **Tools** provide capabilities (MVP: local Python scripts).
- **Sessions** create isolated workspaces for one task.
- **Context compilation** loads dependencies before work so improvements propagate automatically.
- **Traces** record what happened; **patch.md** proposes local changes for manual review.

## Agent tooling

Each AI tool (Cursor, Claude Code, OpenCode, etc.) may create its own root config (`.cursor/`, `.claude/`, etc.). Jah does not maintain an `agents/` folder. Tool-specific rules live in those dot-folders; portable guidance lives in local `CLAUDE.md` and `system/`.

## Improvement

- **Kernel (`system/`)** → edit, bump version (`versioning.md`), commit, GitHub PR.
- **Local layers** → edit directly or via session `patch.md`; never auto-applied.
- **Proactive capture** → agents ask for missing info and offer to promote reusable artifacts during use (`proactive_capture.md`).
- No central patch queue. No `patches/` folder.

## Key differentiation

Stable workflow improvement through dependency-aware context compilation. Sessions invoke workflows by `workflow_id` or auto-resolution; only resolved workflow bodies load at compile time. When you add a global writing rule, blog and social-post sessions compile it automatically because workflows declare dependencies on preferences and active rules.

**Workflows as functions:** types define schema and scaffolds (`types/workflow/`, `types/<artifact_type>/workflows/`); memory holds callable instances (`scope: personal`, `type`, or `project`).
