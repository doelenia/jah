# Proactive Capture

How Jah agents gather missing information and surface reusable improvements during use.

## Purpose

Jah should improve through everyday use — not only at session end. Agents are active curators: they ask for what they need, notice what could become stable memory or reusable types, and flag kernel improvements. Nothing is auto-promoted; the user always decides.

## Three behaviors

| Behavior | When | Goal |
|----------|------|------|
| **Gap-fill** | Before or during work | Get missing info needed to complete the task well |
| **Capture** | During work | Detect reusable facts, patterns, or structures |
| **Improve** | During or after work | Detect friction or gaps in Jah itself |

All three require **explicit user approval** before writing to stable layers (`memory/`, `types/`, `tools/`, `system/`).

## 1. Gap-fill — ask for missing information

After reading compiled context, scan for gaps that would block or weaken the task.

**Ask when:**

- Compiled context lacks a fact the task clearly needs (profile field, project constraint, preference, rule)
- The user's request is ambiguous and a small clarification would prevent rework
- A decision depends on user preference not present in context

**Do not ask when:**

- Reasonable defaults exist and the user can revise later
- The detail is clearly one-off for this session
- You can proceed safely and note the assumption in `trace.md`

**How to ask:**

- One focused question (or a short numbered list, max 3 items)
- Say why you need it and where it would live if stable
- Example: *"Your profile doesn't include tax residency. For this filing task, which country should I treat as your tax residence? If stable, I can propose adding it to `profile.md`."*

## 2. Capture — detect reusable artifacts

While working, watch for signals that something belongs in stable memory, a type, or a tool — not only in session output.

### Classification

| Signal | Likely target | Examples |
|--------|---------------|----------|
| Stable personal fact | `memory/personal/profile.md` | nationality, address, legal name, tax residency |
| Scoped default or style | `memory/personal/preferences/` | writing tone, formatting habits |
| Constraint or policy | `memory/personal/rules/` or project `rules/` | "always cite sources", project-specific constraints |
| Project background | `memory/projects/<name>/context.md` | goals, stakeholders, constraints |
| Repeatable workflow | `memory/projects/<name>/workflows/` or `memory/personal/workflows/` | requirements + workflow + evaluation + examples; catalog in `index.md` |
| Reference material | `memory/projects/<name>/sources/` | PDFs, images, video, links, templates — catalog in `index.md`, files in `files/` |
| Personal reusable files | `memory/personal/sources/` | cross-project identity docs, certificates, scans |
| Reusable schema or form | `types/<name>/type.yaml` + `README.md` | new instance kind, typed field, pipeline stage |
| Automation or script | `tools/` | script, integration, repeated command sequence |
| Kernel or protocol gap | `system/` (via PR) | missing protocol step, unclear permission, workflow friction |

### Stable vs session-only

**Prefer stable capture when** the item is:

- Likely to recur across sessions or projects
- A fact, rule, or pattern the user treats as "always true"
- A workflow the user has done or will do again
- A structure reused for multiple instances

**Keep session-only when** the item is:

- Specific to this deliverable or date
- Experimental or draft
- Sensitive unless the user explicitly wants it in stable memory
- Duplicative of something already in compiled context

When unsure, ask: *"Should this be stable memory or stay in this session?"*

### How to offer capture

At a natural pause (after a milestone, before session end, or when the signal is strong):

1. **Name** what you noticed
2. **Classify** the target layer and path
3. **Offer** a concrete action (propose in `patch.md`, or apply if user approves now)
4. **Do not block** the main task — note in `trace.md` and `patch.md` if the user defers

Example:

> I noticed you want blog posts to open with a concrete observation — that's not in your active rules. Should I propose a new rule under `memory/personal/rules/writing/` in this session's `patch.md`?

Example (type):

> This invoice pipeline (intake → validate → export) looks reusable. Should I propose a `workflow` for project `ausna`, a type scaffold under `types/<artifact_type>/workflows/`, or a new artifact type under `types/`?

## 3. Improve — detect system-level opportunities

When Jah's own protocol causes friction, confusion, or repeated manual work, flag it.

**Examples:**

- A step in the workflow is always skipped or unclear
- Permission boundaries blocked useful behavior
- Context compilation misses a dependency type
- Agent rules contradict `system/` docs

**How to offer:**

- Describe the friction and a minimal fix
- Ask whether to propose a kernel change (`system/` → PR) or a local workaround (memory/types/tools via `patch.md`)
- Kernel changes require explicit user approval (L5); never edit `system/` without it

## Checkpoints

Agents should run proactive capture at these points:

| Checkpoint | Actions |
|------------|---------|
| **After compilation** | Gap-fill scan against session goal and compiled context |
| **During work** | Capture signals as they appear; ask at natural pauses |
| **Before ending session** | Summarize all capture offers not yet decided; ensure `patch.md` lists proposals |
| **In conversation** | Prefer asking inline when the signal is fresh; don't wait only for session end |

## Session artifacts

| File | Proactive role |
|------|----------------|
| `trace.md` | Log gaps found, assumptions made, capture offers made or deferred |
| `patch.md` | Formal proposals for memory, types, tools (with references) |
| `evaluation.md` | Note whether gap-fill or capture would have improved the outcome |
| `output.md` | Deliverable only; capture offers belong in chat, trace, or patch |

## User responses

| User says | Agent does |
|-----------|------------|
| Yes / approve | Propose in `patch.md` or apply directly if L4/L5 approval covers that target |
| Not now / defer | Record in `trace.md`; include in `patch.md` as optional proposal |
| No / session only | Do not propose for stable layers; keep in session artifacts |
| Apply it | Only with explicit approval per `permission_model.md` |

## Do not

- Auto-write to `memory/`, `types/`, `tools/`, or `system/` without approval
- Ask about every trivial detail — use judgment and the stable vs session-only heuristics
- Invent stable facts — only capture what the user provided or confirmed
- Skip gap-fill when missing info would likely cause wrong output
- Batch more than 3 unrelated capture offers in one message — prioritize by impact

## Related docs

- `improvement_protocol.md` — how proposals become changes
- `permission_model.md` — L3–L5 approval boundaries
- `memory_model.md` — profile, preferences, rules, work patterns
- `type_system.md` — when to create or extend types
- `session_lifecycle.md` — when capture runs in the session lifecycle
