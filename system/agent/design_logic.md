# Design Logic

## Philosophy

Jah should not be a black-box assistant. It is a local-first, inspectable, self-improving personal OS whose shape grows with the user.

## System vs principals

| Layer | Role | Git |
|-------|------|-----|
| `system/` | Universal protocol — declared layers in `system/instance.yaml` | Tracked on GitHub |
| `users/<id>/` | Principal local world — registry, types, instances, connectors | Local only |

Customization stays private. The protocol stays portable via GitHub.

## System layers

`system/` follows the same declared-structure model as principals. Read `system/instance.yaml` first.

| Layer | Path | Role |
|-------|------|------|
| **Agent** | `system/agent/` | Behavioral protocol — what agents should do (markdown only) |
| **Bootstrap** | `system/bootstrap/` | Copy-once starter kit — seeds principal data, not runtime code |
| **Engines** | `system/engines/` | Protocol runtime — Python that operates on principal data |
| **Release** | `system/release/` | Version, changelog, init and bump scripts |
| **Interface** | `system/interface/` | Human-facing surface (reserved, not implemented) |

**Spec ↔ engine pairing:** each agent doc pairs with an engine folder (e.g. `agent/knowledge_base.md` ↔ `engines/knowledge/`). Run engines via `python3 system/engines/cli.py <command>`.

**Principal connectors:** `users/<id>/connectors/` is optional — external services, devices, MCP configs, and personal automations only. Jah protocol code never copies there.

## Core concepts

- **Registry** — authoritative type index per principal (`registry.yaml`).
- **Types** — growable schemas and agent protocols; even starter types are user-editable after bootstrap.
- **Instances** — living data (personal, projects, workflows, sessions) under the principal.
- **Connectors** — optional principal-specific wiring under `users/<id>/connectors/` (external services, devices, MCP, custom glue).
- **Sessions** — isolated workspaces for one task.
- **Context compilation** — loads goal-matched dependencies before work so improvements propagate automatically.
- **Discovery protocol** — active search, discovery log, reference checklist (`discovery_protocol.md`).
- **Knowledge base** — curated IP index with OECD FORD field topics (`knowledge_base.md`).
- **Traces** — record what happened; **patch.md** for profile, new types, and system proposals.

## Types as the growth engine

Users do not only grow projects — they grow their **work/life model** by registering types, extending schemas, and attaching workflows. The registry makes that growth explicit and resolvable.

Bootstrap provides starter types; the principal owns them after init. Users may patch `base`, `project`, or any starter type.

## Open structure

Folder meaning is **declared**, not inferred. See `open_structure.md` (same rule applies to `system/instance.yaml` and principal `instance.yaml` files).

- **`open_fields`** defaults true on `type.base` — instances grow by adding fields.
- **Type `fields`** on containers = minimal baseline; instances must scaffold from it.
- **Instance `fields`** = baseline + grown fields — authoritative for that folder.
- **Types improve** when durable patterns generalize from instances; propagation uses `patch.md`.

## Agent tooling

Each AI tool (Cursor, Claude Code, etc.) may create root config (`.cursor/`, `.claude/`). Jah does not maintain an `agents/` folder. Portable guidance lives in `CLAUDE.md` and `system/agent/`.

## Improvement

- **System (`system/`)** → edit, bump system version (`../release/versioning.md`), commit, GitHub PR.
- **Principal** → edit directly or via session `patch.md`; never auto-applied.
- **Proactive capture** → agents gap-fill, auto-update existing principal instances/types, ask for profile/system (`proactive_capture.md`).

## Key differentiation

Stable workflow improvement through dependency-aware context compilation. Sessions invoke workflows by `workflow_id` or auto-resolution; only resolved workflow bodies load at compile time.

**Workflows as functions:** workflow instances live anywhere a container declares them (personal, project, or under `types/<artifact>/workflows/`). Resolution is by `workflow_id` and registry, not fixed paths.
