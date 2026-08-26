# Protocol

Primary entry point for working in Jah.

## What Jah is

Jah is a local-first, AI-native personal OS. It turns repeated work into stable, preference-aware automation through typed instances, context compilation, sessions, traces, and local improvement proposals.

The shared design lives in `system/` (versioned on GitHub). Your principal — `users/<id>/` — stays local and private.

Discover system structure via `system/instance.yaml` — same declared-folder model as principals.

## Setup

1. Clone the repo (you get `system/` and `.gitignore`).
2. Bootstrap a principal: `python3 system/release/scripts/init_jah.py <id>` (see `../bootstrap/SETUP.md`).
3. Install Python deps in a virtualenv:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   ```
4. Read `design_logic.md`, `open_structure.md`, then `jah.yaml` and the active principal's `registry.yaml`.

## Operation model (default — top priority)

**Orient → Plan → Act → Capture.** No implementation writes until **Orient** and **Plan** are complete.

| Phase | When | Agent must |
|-------|------|------------|
| **Orient** | After compile, before any writes | Read behavior docs in compiled context; run scope expansion (`discovery_protocol.md`); resolve types for everything in scope |
| **Plan** | Before implementation | Write **Session plan** in `trace.md`: files to read, files likely to update, open questions — plan defines "relevant" for this session |
| **Act** | After plan | Execute against the plan; L2 session writes freely; L3 principal updates when capture is clear |
| **Capture** | Session end | Diff plan vs outcome; update stable targets the plan identified; complete discovery log and evaluation checklist |

The compiled context **Operation Checklist** (`engines/context/compile.py`) repeats this at the top of every session. Do not skip it.

Do **not** add per-feature sync checklists (e.g. "if system changed, update design/"). Relevant artifacts emerge from orient + plan + discovery — not from naming each target in a separate rule.

## Rule privilege

When instructions conflict, follow this order: **constitution** (`constitution.md`) → **permission model** (`permission_model.md`) → **principal rules** (`personal/rules/`, project `rules/`) → **user message**. Among principal rules, lower `priority` number wins. Resolve rule bodies on demand via Rule Index and `resolve-rules` — see `context_compilation.md`.

## How to work

1. **Create or use a session** for every task.
2. **Compile context** before execution.
3. **Orient** — read compiled context; scope expansion; resolve types (`discovery_protocol.md`, `type_system.md`). For any type-system work, run **Type coherence review** before writes.
4. **Plan** — write Session plan in `trace.md` before implementation writes.
5. **Act** — work inside the session folder; auto-update principal when the plan and capture say so; log in `trace.md`.
6. **Capture** — session end: evaluation, discovery log, plan vs outcome (`proactive_capture.md`).
7. **Discover structure** when touching new folders — `ls` → `instance.yaml` → type → `fields` → recurse (`open_structure.md`).
8. **External services** — read `users/<id>/connectors/README.md` and `connectors.md`; MCP config is per-agent, connector docs are canonical (`connectors.md`).
9. **Ask before profile, new registry entries, or system changes.**
10. **Cite sources** in session artifacts (`evaluation.md` reference checklist).
11. **Store reusable files** under `sources/files/` with catalog entries.
12. **Curate knowledge** — audited wisdom in `users/<id>/knowledge-base/` (`knowledge_base.md`).
13. **Change the system** only when explicitly asked — GitHub PR on `system/`. Bump `system/release/VERSION` before every system commit (`../release/versioning.md`).

## Type resolution (required)

1. Read `jah.yaml` → active principal.
2. Read `registry.yaml` → resolve instance `type`.
3. Read `types/<type>/type.yaml` and README (with extends chain).
4. For each field in scope, repeat.
5. Read child `instance.yaml` files for folder-based instances.

See `type_system.md`.

## Read order

1. `system/agent/constitution.md` — meta-rules for discovering and applying rules
2. `system/agent/protocol.md` (this file)
3. `system/agent/design_logic.md`
4. `system/agent/open_structure.md`
5. `system/agent/discovery_protocol.md`
6. `system/agent/knowledge_base.md`
7. `system/agent/storage_rules.md`
8. `system/agent/archive.md` (when archiving or working with archived projects)
9. `system/agent/connectors.md` (when task uses external services)
10. `system/agent/type_system.md`
11. `users/<id>/registry.yaml`
12. `users/<id>/connectors/README.md` (when task uses external services)
13. Relevant `instance.yaml` (principal, personal, project, or session)
14. `types/<type>/README.md` for instance and each field in scope
15. Session `compiled_context.md` after compilation

## CLI

All protocol engines run from `system/engines/cli.py`:

```bash
# Create a session
python3 system/engines/cli.py new-session users/<id>/projects/jah "Your goal here"

# Compile context
python3 system/engines/cli.py compile-context users/<id>/projects/jah/sessions/YYYY-MM-DD-001

# List instance.yaml paths
python3 system/engines/cli.py list-instances

# Validate registry
python3 system/engines/cli.py validate-registry

# Survey all registered types (type coherence review)
python3 system/engines/cli.py list-types

# Validate structure (baseline + disk parity)
python3 system/engines/cli.py validate-structure

# Knowledge base
python3 system/engines/cli.py validate-knowledge
python3 system/engines/cli.py resolve-knowledge <knowledge-id>
python3 system/engines/cli.py resolve-rules <session-path> --trigger <trigger> [--target <path>]
python3 system/engines/cli.py check-write <session-path> --target <path> [--strict]

# Archive / unarchive a project
python3 system/engines/cli.py archive-project users/<id>/projects/<name>
python3 system/engines/cli.py unarchive-project users/<id>/projects/archive/<name>
```

**System release** (`system/release/scripts/`):

```bash
python3 system/release/scripts/bump_release.py --bump patch -m "Summary of system change"
python3 system/release/scripts/check_release.py
```

## MVP philosophy

Boring, inspectable, durable. No black-box state. Dependencies are explicit and recorded in compiled context.
