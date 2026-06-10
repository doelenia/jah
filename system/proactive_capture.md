# Proactive Capture

How Jah agents gather missing information and surface reusable improvements during use.

## Purpose

Jah improves through everyday use. Agents are active curators: gap-fill, capture, improve. Nothing is auto-promoted; the user always decides.

## Three behaviors

| Behavior | When | Goal |
|----------|------|------|
| **Gap-fill** | Before or during work | Get missing info needed to complete the task |
| **Capture** | During work | Detect reusable facts, patterns, structures |
| **Improve** | During or after work | Detect friction in Jah itself |

All require **explicit user approval** before writing to stable principal instances, registry, types, tools, or system.

## 1. Gap-fill

After compilation, scan for gaps that would block or weaken the task.

**Ask when:** missing profile, preference, rule, or project context needed for the goal.

**Do not ask when:** reasonable defaults exist; detail is session-only; proceed safely and note assumption in `trace.md`.

## 2. Capture — classification

| Signal | Target |
|--------|--------|
| Stable personal fact | `users/<id>/personal/profile.md` |
| Scoped default | `users/<id>/personal/preferences/` |
| Constraint | `users/<id>/personal/rules/` or project `rules/` |
| Project background | `users/<id>/projects/<name>/context.md` |
| Repeatable workflow | personal or project `workflows/`, or `types/<artifact>/workflows/` |
| Reference material | `sources/` (catalog + `files/`) |
| Reusable schema | `registry.yaml` + `types/<name>/` |
| Automation | `users/<id>/tools/` |
| System gap | `system/` (via PR) |

When unsure: *"Should this be a stable instance or stay in this session?"*

## 3. Improve

Flag protocol friction. Offer system change (`system/` → PR) or principal workaround via `patch.md`.

## Checkpoints

| Checkpoint | Actions |
|------------|---------|
| After compilation | Gap-fill scan |
| During work | Capture signals at natural pauses |
| Before session end | Summarize offers; ensure `patch.md` lists proposals |

## Do not

- Auto-write to principal, registry, types, tools, or system without approval
- Invent stable facts
- Skip gap-fill when missing info would cause wrong output

## Related docs

- `improvement_protocol.md`
- `permission_model.md`
- `principal_model.md`
- `type_system.md`
- `session_lifecycle.md`
