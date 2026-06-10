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

## How to work

1. **Discover structure** — `ls` → read `instance.yaml` → resolve type → read `fields` → recurse (`open_structure.md`).
2. **Create or use a session** for every task.
3. **Compile context** before execution.
4. **Work inside the session folder** — outputs, evaluation, trace, patch.
5. **Propose improvements** in session `patch.md`; apply to principal manually after review.
6. **Be proactive** — gap-fill, capture, improve (`proactive_capture.md`).
7. **Capture stable personal facts** via `patch.md` — never auto-write profile.
8. **Cite sources** in session artifacts and stable-instance proposals.
9. **Store reusable files** under `sources/files/` with catalog entries.
10. **Change the system** only via GitHub PR on `system/`. Bump `system/VERSION` before every system commit (`versioning.md`).

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
4. `system/storage_rules.md`
5. `system/type_system.md`
6. `users/<id>/registry.yaml`
7. Relevant `instance.yaml` (principal, personal, project, or session)
8. `types/<type>/README.md` for instance and each field in scope
9. Session `compiled_context.md` after compilation

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
```

**System release** (tracked in `system/scripts/`):

```bash
python3 system/scripts/bump_release.py --bump patch -m "Summary of system change"
python3 system/scripts/check_release.py
```

## MVP philosophy

Boring, inspectable, durable. No black-box state. Dependencies are explicit and recorded in compiled context.
