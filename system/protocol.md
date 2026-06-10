# Protocol

Primary entry point for working in Jah.

## What Jah is

Jah is a local-first, AI-native personal OS. It turns repeated work into stable, preference-aware automation through typed memory, context compilation, sessions, traces, and local improvement proposals.

The shared design lives in `system/` (versioned on GitHub). Your living world — types, memory, tools — stays local and private.

## Setup

1. Clone the repo (you get `system/` and `.gitignore`).
2. Scaffold local layers: `types/`, `memory/`, `tools/` (see `storage_rules.md`).
3. Install Python deps: `pip install -r requirements.txt` (local file).
4. Read `design_logic.md`, then relevant `instance.yaml` files before work.

## How to work

1. **Create or use a session** for every task.
2. **Compile context** before execution: `python tools/scripts/compile_context.py <session-path>`.
3. **Work inside the session folder** — outputs, evaluation, trace, patch.
4. **Propose improvements** in session `patch.md`; apply to local memory/types/tools manually after review.
5. **Be proactive** — ask for missing info, and offer to capture reusable facts, types, tools, or kernel improvements when you detect them (`proactive_capture.md`).
6. **Capture stable personal facts** in `memory/personal/profile.md` via `patch.md` proposals — never auto-write profile during a session.
7. **Cite sources** when creating content from internal files (repo-relative path) or external links (full URL). Record references in session artifacts and stable-memory proposals.
8. **Store reusable files** (PDF, image, video, etc.) under `sources/files/` with a catalog entry in `sources/index.md` — see `types/source/README.md`.
8. **Change the kernel** only via GitHub PR on `system/`. Bump `system/VERSION` and add a `system/CHANGELOG.md` entry before every kernel commit (`versioning.md`).

## Type resolution (required)

Before working with any instance or field, resolve its type:

1. Read the `instance.yaml` → get `type`.
2. Read `types/<type>/type.yaml` and `types/<type>/README.md`.
3. For each field in scope, repeat for that field's declared type.
4. Read child `instance.yaml` files for folder-based instances.

See `system/type_system.md` for field typing and instance creation rules.

## Read order

1. `system/protocol.md` (this file)
2. `system/design_logic.md`
3. `system/storage_rules.md`
4. `system/type_system.md`
5. Relevant `instance.yaml` for the project, personal scope, or session
6. `types/<type>/README.md` for the instance and each field being touched
7. Session `compiled_context.md` after compilation

Deeper reference: `system/session_lifecycle.md`, `system/context_compilation.md`, `system/permission_model.md`, `system/improvement_protocol.md`, `system/proactive_capture.md`, `system/versioning.md`.

## Scripts

**Local** (in your `tools/scripts/`):

```bash
# Create a session
python3 tools/scripts/new_session.py memory/projects/jah "Your goal here"

# Compile context for a session
python3 tools/scripts/compile_context.py memory/projects/jah/sessions/YYYY-MM-DD-001

# List all instance.yaml paths
python3 tools/scripts/list_instances.py
```

**Kernel release** (tracked in `system/scripts/`, run before GitHub commit):

```bash
python3 system/scripts/bump_release.py --bump patch -m "Summary of kernel change"
python3 system/scripts/check_release.py   # optional: verify version bump present
```

## MVP philosophy

Boring, inspectable, durable. No black-box memory. Dependencies are explicit and recorded in compiled context.
