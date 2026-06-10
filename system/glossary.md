# Glossary

Use this vocabulary consistently across Jah.

| Term | Meaning |
|------|---------|
| **Type** | Reusable form or definition (`types/`) |
| **Instance** | An actual living thing in memory |
| **Memory** | Where instances live (`memory/`) |
| **Tool** | Executable capability (`tools/`) |
| **Session** | One temporary working instance under a project |
| **Trace** | Record of what happened during a session |
| **Reference** | Citation of a source behind created content; internal = repo-relative path, external = full URL |
| **Profile** | Canonical personal facts in `memory/personal/profile.md`; updated via `patch.md`, not auto-written |
| **Patch** | Local proposal for improvement (session `patch.md`; not auto-applied) |
| **Context compilation** | Collecting relevant types, preferences, rules, sources, and session input before work begins |
| **Proactive capture** | Agent behavior: gap-fill (ask for missing info), capture (offer stable memory/types/tools), improve (flag kernel friction) — see `proactive_capture.md` |
| **Gap-fill** | Asking the user for information missing from compiled context that the task needs |
| **Capture signal** | Something encountered during work that may belong in stable memory, a type, a tool, or the kernel |
| **Workflow** | Callable repeatable procedure (`type.workflow`); scoped to personal, type, or project; invoked by sessions via `workflow_id` |
| **Kernel version** | Semver in `system/VERSION` for tracked protocol releases on GitHub |
| **Changelog** | Release history in `system/CHANGELOG.md`; README shows a short recent-updates excerpt |

## Layers

1. **`system/`** — Shared kernel/protocol (tracked on GitHub)
2. **`types/`** — Reusable type definitions (local)
3. **`memory/`** — Living instances (local)
4. **`tools/`** — Scripts and future integrations (local)
