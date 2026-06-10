# Improvement Protocol

How Jah improves over time.

## Proactive capture

Agents should not wait passively for session end. During every task, follow `proactive_capture.md`:

1. **Gap-fill** — ask for missing information needed to do the work well.
2. **Capture** — when you notice reusable facts, workflows, schemas, or automations, offer to propose them for the right layer (memory, types, tools).
3. **Improve** — when Jah's protocol or tooling causes friction, offer a kernel or local fix.

All offers require explicit user approval before stable layers change. Deferrals and assumptions go in `trace.md`; formal proposals go in `patch.md`.

## Two improvement paths

### 1. Kernel changes (`system/`)

Edit files in `system/`, then **bump version and changelog** before commit (`versioning.md`):

```bash
python3 system/scripts/bump_release.py --bump patch -m "What changed"
```

Commit, push, open a GitHub PR. This is the only path for shared protocol changes. One kernel commit = one semver entry in `system/CHANGELOG.md`.

### 2. Local customization

Edit local files directly, or use session artifacts:

| Target | Location |
|--------|----------|
| Personal profile | `memory/personal/profile.md` |
| Personal preferences | `memory/personal/preferences/` |
| Personal rules | `memory/personal/rules/` |
| Project context | `memory/projects/<name>/context.md` |
| Workflows | `memory/projects/<name>/workflows/` or `memory/personal/workflows/` |
| Local types | `types/` |
| Local tools | `tools/` |

## Session patch.md

At the end of a session, write `patch.md` with proposed local changes. It is:

- A working proposal, not a queue item
- Never auto-applied by scripts
- Reviewed and applied manually by you

## Traces

`trace.md` records what happened — decisions, failures, surprises. Use traces to inform the next session or patch proposal.

## References on created content

When session or stable-memory content is created from a specific source:

- **Internal** — cite the repo-relative path (e.g. `memory/projects/us-taxes/context.md`)
- **External** — cite the full URL

Include references in `output.md`, `patch.md`, and `trace.md` as applicable. Patch proposals without citations for sourced changes should not be applied.

## Personal profile via patch

When a session learns or corrects a **stable personal fact** (nationality, address, age, tax residency, etc.), the agent must check it against the compiled profile and, if new or changed, include a `patch.md` proposal to update `memory/personal/profile.md`. Never write profile directly without explicit approval.

## What patches can propose

- Personal profile, preferences, and rules
- Project rules and workflows
- Local type definitions
- Local tools
- (Kernel changes should go directly to `system/` via GitHub, not session patch)

## Review gate

Local memory, types, and tools change only after you explicitly apply edits. Scripts never modify stable local memory automatically.
