# Protocol

Primary entry point for working in Jah.

## What Jah is

Jah is a local-first, AI-native personal OS. It turns repeated work into stable, preference-aware automation through typed instances, context compilation, sessions, traces, and local improvement proposals.

The shared design lives in `system/` (versioned on GitHub). Your principal — `users/<id>/` — stays local and private.

## Setup

1. Clone the repo (you get `system/` and `.gitignore`).
2. Bootstrap a principal: `python3 system/scripts/init_jah.py <id>` (see `system/bootstrap/SETUP.md`).
3. Install Python deps: `pip install -r requirements.txt` (local file).
4. Read `design_logic.md`, then `jah.yaml` and the active principal's `registry.yaml`.

## How to work

1. **Create or use a session** for every task.
2. **Compile context** before execution.
3. **Work inside the session folder** — outputs, evaluation, trace, patch.
4. **Propose improvements** in session `patch.md`; apply to principal manually after review.
5. **Be proactive** — gap-fill, capture, improve (`proactive_capture.md`).
6. **Capture stable personal facts** via `patch.md` — never auto-write profile.
7. **Cite sources** in session artifacts and stable-instance proposals.
8. **Store reusable files** under `sources/files/` with catalog entries.
9. **Change the system** only via GitHub PR on `system/`. Bump `system/VERSION` before every system commit (`versioning.md`).

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
3. `system/storage_rules.md`
4. `system/type_system.md`
5. `users/<id>/registry.yaml`
6. Relevant `instance.yaml` (principal, personal, project, or session)
7. `types/<type>/README.md` for instance and each field in scope
8. Session `compiled_context.md` after compilation

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
```

**System release** (tracked in `system/scripts/`):

```bash
python3 system/scripts/bump_release.py --bump patch -m "Summary of system change"
python3 system/scripts/check_release.py
```

## MVP philosophy

Boring, inspectable, durable. No black-box state. Dependencies are explicit and recorded in compiled context.
