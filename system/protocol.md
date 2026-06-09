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
5. **Change the kernel** only via GitHub PR on `system/`.

## Read order

1. `system/protocol.md` (this file)
2. `system/design_logic.md`
3. `system/storage_rules.md`
4. Relevant `instance.yaml` for the project or session
5. Session `compiled_context.md` after compilation

## Scripts

```bash
# Create a session
python tools/scripts/new_session.py memory/projects/jah "Your goal here"

# Compile context for a session
python tools/scripts/compile_context.py memory/projects/jah/sessions/YYYY-MM-DD-001

# List all instance.yaml paths
python tools/scripts/list_instances.py
```

## MVP philosophy

Boring, inspectable, durable. No black-box memory. Dependencies are explicit and recorded in compiled context.
