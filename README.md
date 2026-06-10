# Jah

A local-first, AI-native personal OS. Jah turns repeated work into stable, preference-aware automation through typed instances, context compilation, sessions, traces, and local improvement proposals.

The **system** in `system/` is shared and versioned on GitHub. Your **principal** — `users/<id>/` — stays on your machine and private.

Current system version: **0.1.1** (see [system/VERSION](system/VERSION)).

## What you get from GitHub

- `system/` — protocol, bootstrap starter kit, design docs, release scripts
- `.gitignore` — keeps principals local
- This `README.md`

## Quick start

1. **Clone** this repository.
2. **Bootstrap** a principal:
   ```bash
   python3 system/scripts/init_jah.py <your-id>
   ```
   Copy `users/<id>/tools/scripts/` from an existing setup or add scripts after bootstrap (see `system/bootstrap/SETUP.md`).
3. **Install** Python deps: `pip install -r requirements.txt` in a virtualenv.
4. **Read** [system/protocol.md](system/protocol.md) and [system/bootstrap/SETUP.md](system/bootstrap/SETUP.md).

## How to use Jah

Every task runs in a **session** under a project.

```bash
# Create a session
python3 users/<id>/tools/scripts/new_session.py users/<id>/projects/<project> "Your goal"

# Compile context
python3 users/<id>/tools/scripts/compile_context.py users/<id>/projects/<project>/sessions/YYYY-MM-DD-NNN
```

Work inside the session folder. End with `output.md`, `evaluation.md`, `trace.md`, and `patch.md`.

Full workflow: [system/protocol.md](system/protocol.md) · Session lifecycle: [system/session_lifecycle.md](system/session_lifecycle.md)

## Recent updates

<!-- recent-updates:start -->
### 0.1.1 (2026-06-10)
- Principal architecture: users/<id>/ layout with registry.yaml and bootstrap
- Replace legacy memory/types/tools root paths; remove work_pattern
- Unify terminology: system (not kernel), principal (not top-level memory)

### 0.1.0 (2026-06-09)
- System versioning with `system/VERSION` and `system/CHANGELOG.md`
- Root `README.md` for open-source discovery (intro, quick start, recent updates)
- `system/scripts/bump_release.py` and `check_release.py` for release workflow and pre-commit guard
- `system/versioning.md` — release workflow and semver policy
- …and 1 more (see changelog)
<!-- recent-updates:end -->

Full history: [system/CHANGELOG.md](system/CHANGELOG.md).

## Contributing to the system

System changes live in `system/` and ship via GitHub PR.

**Before every commit** that changes tracked system files, bump the version and add a changelog entry:

```bash
python3 system/scripts/bump_release.py --bump patch -m "Short summary of the change"
python3 system/scripts/check_release.py   # optional guard
```

Details: [system/versioning.md](system/versioning.md) · Improvement path: [system/improvement_protocol.md](system/improvement_protocol.md)

## License

License not yet specified — add one when you open the repository publicly.
