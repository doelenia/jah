# Proactive Capture

How Jah agents gather missing information and surface reusable improvements during use.

## Purpose

Jah improves through everyday use. Agents are active curators: gap-fill, capture, improve. Principal instances and types update proactively; profile, new registry entries, and system changes stay behind explicit approval.

## Three behaviors

| Behavior | When | Goal |
|----------|------|------|
| **Gap-fill** | Before or during work | Get missing info needed to complete the task |
| **Capture** | During work | Detect reusable facts, patterns, structures |
| **Improve** | During or after work | Detect friction in Jah itself |

## Approval boundaries

| Target | Action |
|--------|--------|
| Existing principal instances (tasks, context, design, rules, prefs, sources, workflows, knowledge-base) | Update directly; log in `trace.md` |
| Existing principal types (`users/<id>/types/`) | Patch directly; log in `trace.md` |
| Principal connectors (`connectors/`) | Update directly when improving MCP or custom glue |
| Personal profile | Propose in `patch.md`; ask user |
| New registry type | Propose in `patch.md`; ask user |
| System (`system/`) | Ask user; GitHub PR only |

When unsure: *"Should this be a stable instance or stay in this session?"*

## 1. Gap-fill

After compilation, scan for gaps that would block or weaken the task. Run **active discovery** (`discovery_protocol.md`).

**Ask when:** missing profile, preference, rule, or project context needed for the goal; a system change seems needed.

**Do not ask when:** reasonable defaults exist; detail is session-only; proceed safely and note assumption in `trace.md`.

## 2. Capture — classification

| Signal | Target |
|--------|--------|
| Stable personal fact | `users/<id>/personal/profile.md` (ask first) |
| Scoped default | `users/<id>/personal/preferences/` |
| Constraint | `users/<id>/personal/rules/` or project `rules/` |
| Project background | `users/<id>/projects/<name>/context.md` |
| Repeatable workflow | personal or project `workflows/`, or `types/<artifact>/workflows/` |
| Reference material | `sources/` (catalog + `files/`) |
| Curated wisdom (audited IP) | `users/<id>/knowledge-base/` (entry + `index.yaml`; see `knowledge_base.md`) |
| Reusable schema | `registry.yaml` + `users/<id>/types/` (new = ask; patch existing = auto) |
| Connectors | `users/<id>/connectors/` (optional — external services, devices, MCP, custom automations) |
| System gap | `system/` (via PR; ask first) |

## 3. Improve

Flag protocol friction. Apply principal workarounds directly when safe. Offer system change (`system/` → PR) only after user asks.

## Checkpoints

| Checkpoint | Actions |
|------------|---------|
| After compilation | Gap-fill scan; start discovery log in `trace.md` |
| During work | Capture signals; auto-update principal when target is existing instance/type |
| Before session end | Complete evaluation reference checklist; check unpromoted audited IP for knowledge-base; summarize profile/system offers in `patch.md` |

## Do not

- Auto-write profile or register new types without approval
- Edit `system/` without explicit user request
- Invent stable facts
- Skip gap-fill when missing info would cause wrong output
- Skip discovery log and reference checklist at session end

## Related docs

- `knowledge_base.md`
- `discovery_protocol.md`
- `improvement_protocol.md`
- `permission_model.md`
- `principal_model.md`
- `type_system.md`
- `session_lifecycle.md`
