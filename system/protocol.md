# Protocol

Primary entry point for working in Jah.

## What Jah is

Jah is a local-first, AI-native personal OS. It turns repeated work into stable, preference-aware automation through typed instances, context compilation, sessions, traces, and local improvement proposals.

The shared design lives in `system/` (versioned on GitHub). Your principal — `users/<id>/` — stays local and private.

## Setup

1. Clone the repo (you get `system/` and `.gitignore`).
2. Bootstrap a principal: `python3 system/scripts/init_jah.py <id>` (see `system/bootstrap/SETUP.md`).
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

The compiled context **Operation Checklist** (`compile_context.py`) repeats this at the top of every session. Do not skip it.

Do **not** add per-feature sync checklists (e.g. "if system changed, update design/"). Relevant artifacts emerge from orient + plan + discovery — not from naming each target in a separate rule.

## How to work

1. **Create or use a session** for every task.
2. **Compile context** before execution.
3. **Orient** — read compiled context; scope expansion; resolve types (`discovery_protocol.md`, `type_system.md`).
4. **Plan** — write Session plan in `trace.md` before implementation writes.
5. **Act** — work inside the session folder; auto-update principal when the plan and capture say so; log in `trace.md`.
6. **Capture** — session end: evaluation, discovery log, plan vs outcome (`proactive_capture.md`).
7. **Discover structure** when touching new folders — `ls` → `instance.yaml` → type → `fields` → recurse (`open_structure.md`).
8. **Ask before profile, new registry entries, or system changes.**
9. **Cite sources** in session artifacts (`evaluation.md` reference checklist).
10. **Store reusable files** under `sources/files/` with catalog entries.
11. **Curate knowledge** — audited wisdom in `users/<id>/knowledge-base/` (`knowledge_base.md`).
12. **Change the system** only when explicitly asked — GitHub PR on `system/`. Bump `system/VERSION` before every system commit (`versioning.md`).

## Type resolution (required)

1. Read `jah.yaml` → active principal.
2. Read `registry.yaml` → resolve instance `type`.
3. Read `types/<type>/type.yaml` and README (with extends chain).
4. For each field in scope, repeat.
5. Read child `instance.yaml` files for folder-based instances.

See `system/type_system.md`.

## Read order

1. `system/protocol.md` (this file)
2. `system/design_logic.md`
3. `system/open_structure.md`
4. `system/discovery_protocol.md`
5. `system/knowledge_base.md`
6. `system/storage_rules.md`
7. `system/type_system.md`
8. `users/<id>/registry.yaml`
9. Relevant `instance.yaml` (principal, personal, project, or session)
10. `types/<type>/README.md` for instance and each field in scope
11. Session `compiled_context.md` after compilation

## Scripts

**Principal** (under `users/<id>/tools/scripts/`):

```bash
# Create a session
python3 users/<id>/tools/scripts/new_session.py users/<id>/projects/jah "Your goal here"

# Compile context
python3 users/<id>/tools/scripts/compile_context.py users/<id>/projects/jah/sessions/YYYY-MM-DD-001

# List instance.yaml paths
python3 users/<id>/tools/scripts/list_instances.py

# Validate registry
python3 users/<id>/tools/scripts/validate_registry.py

# Validate structure (baseline + disk parity)
python3 users/<id>/tools/scripts/validate_structure.py

# Knowledge base
python3 users/<id>/tools/scripts/validate_knowledge.py
python3 users/<id>/tools/scripts/resolve_knowledge.py <knowledge-id>
```

**System release** (tracked in `system/scripts/`):

```bash
python3 system/scripts/bump_release.py --bump patch -m "Summary of system change"
python3 system/scripts/check_release.py
```

## MVP philosophy

Boring, inspectable, durable. No black-box state. Dependencies are explicit and recorded in compiled context.
