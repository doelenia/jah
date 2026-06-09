# Improvement Protocol

How Jah improves over time.

## Two improvement paths

### 1. Kernel changes (`system/`)

Edit files in `system/`, commit, open a GitHub PR. This is the only path for shared protocol changes.

### 2. Local customization

Edit local files directly, or use session artifacts:

| Target | Location |
|--------|----------|
| Personal preferences | `memory/personal/preferences/` |
| Personal rules | `memory/personal/rules/` |
| Project context | `memory/projects/<name>/context.md` |
| Work patterns | `memory/projects/<name>/work_patterns/` |
| Local types | `types/` |
| Local tools | `tools/` |

## Session patch.md

At the end of a session, write `patch.md` with proposed local changes. It is:

- A working proposal, not a queue item
- Never auto-applied by scripts
- Reviewed and applied manually by you

## Traces

`trace.md` records what happened — decisions, failures, surprises. Use traces to inform the next session or patch proposal.

## What patches can propose

- Personal preferences and rules
- Project rules and work patterns
- Local type definitions
- Local tools
- (Kernel changes should go directly to `system/` via GitHub, not session patch)

## Review gate

Local memory, types, and tools change only after you explicitly apply edits. Scripts never modify stable local memory automatically.
