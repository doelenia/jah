# Design Logic

## Philosophy

Jah should not be a black-box assistant. It is a local-first, inspectable, self-improving personal OS whose shape grows with the user.

## System vs principals

| Layer | Role | Git |
|-------|------|-----|
| `system/` | Universal protocol — how Jah works; bootstrap starter kit | Tracked on GitHub |
| `users/<id>/` | Principal local world — registry, types, instances, tools | Local only |

Customization stays private. The protocol stays portable via GitHub.

## Core concepts

- **Registry** — authoritative type index per principal (`registry.yaml`).
- **Types** — growable schemas and agent protocols; even starter types are user-editable after bootstrap.
- **Instances** — living data (personal, projects, workflows, sessions) under the principal.
- **Tools** — executable capabilities under `users/<id>/tools/`.
- **Sessions** — isolated workspaces for one task.
- **Context compilation** — loads dependencies before work so improvements propagate automatically.
- **Traces** — record what happened; **patch.md** proposes local changes for manual review.

## Types as the growth engine

Users do not only grow projects — they grow their **work/life model** by registering types, extending schemas, and attaching workflows. The registry makes that growth explicit and resolvable.

Bootstrap provides starter types; the principal owns them after init. Users may patch `base`, `project`, or any starter type.

## Agent tooling

Each AI tool (Cursor, Claude Code, etc.) may create root config (`.cursor/`, `.claude/`). Jah does not maintain an `agents/` folder. Portable guidance lives in `CLAUDE.md` and `system/`.

## Improvement

- **System (`system/`)** → edit, bump system version (`versioning.md`), commit, GitHub PR.
- **Principal** → edit directly or via session `patch.md`; never auto-applied.
- **Proactive capture** → agents ask for missing info and offer to promote reusable artifacts (`proactive_capture.md`).

## Key differentiation

Stable workflow improvement through dependency-aware context compilation. Sessions invoke workflows by `workflow_id` or auto-resolution; only resolved workflow bodies load at compile time.

**Workflows as functions:** workflow instances live anywhere a container declares them (personal, project, or under `types/<artifact>/workflows/`). Resolution is by `workflow_id` and registry, not fixed paths.
