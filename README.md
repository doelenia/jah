# Jah

A local-first, AI-native personal OS. Jah turns repeated work into stable, preference-aware automation through typed memory, context compilation, sessions, traces, and local improvement proposals.

The **kernel** in `system/` is shared and versioned on GitHub. Your living world — types, memory, tools — stays on your machine and private.

Current kernel version: **0.1.0** (see [system/VERSION](system/VERSION)).

## What you get from GitHub

- `system/` — protocol, design docs, release scripts
- `.gitignore` — keeps local layers out of git
- This `README.md`

Everything else (`types/`, `memory/`, `tools/`, agent config) you scaffold locally.

## Quick start

1. **Clone** this repository.
2. **Scaffold** local layers at the repo root:
   - `types/`
   - `memory/` (e.g. `memory/personal/`, `memory/projects/`)
   - `tools/` (e.g. `tools/scripts/`)
3. **Install** Python dependencies: `pip install -r requirements.txt` (create this file locally as needed).
4. **Read** [system/protocol.md](system/protocol.md), then [system/design_logic.md](system/design_logic.md).

## How to use Jah

Every task runs in a **session** — an isolated folder under a project.

```bash
# Create a session
python3 tools/scripts/new_session.py memory/projects/<project> "Your goal"

# Compile context (loads types, preferences, rules, workflows)
python3 tools/scripts/compile_context.py memory/projects/<project>/sessions/YYYY-MM-DD-NNN
```

Work inside the session folder. End with `output.md`, `evaluation.md`, `trace.md`, and `patch.md`. Propose stable-memory changes in `patch.md`; apply them manually after review.

Full workflow: [system/protocol.md](system/protocol.md) · Session lifecycle: [system/session_lifecycle.md](system/session_lifecycle.md)

## Recent updates

<!-- recent-updates:start -->
### 0.1.0 (2026-06-09)
- Kernel versioning with `system/VERSION` and `system/CHANGELOG.md`
- Root `README.md` for open-source discovery (intro, quick start, recent updates)
- `system/scripts/bump_release.py` and `check_release.py` for release workflow and pre-commit guard
- `system/versioning.md` — release workflow and semver policy
- …and 1 more (see changelog)
<!-- recent-updates:end -->

Full history: [system/CHANGELOG.md](system/CHANGELOG.md).

## Contributing to the kernel

Kernel changes live in `system/` and ship via GitHub PR.

**Before every commit** that changes tracked kernel files, bump the version and add a changelog entry:

```bash
python3 system/scripts/bump_release.py --bump patch -m "Short summary of the change"
python3 system/scripts/check_release.py   # optional guard
```

Details: [system/versioning.md](system/versioning.md) · Improvement path: [system/improvement_protocol.md](system/improvement_protocol.md)

## License

License not yet specified — add one when you open the repository publicly.
