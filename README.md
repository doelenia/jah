# Jah

A local-first, AI-native personal OS. Jah turns repeated work into stable, preference-aware automation through typed instances, context compilation, sessions, traces, and local improvement proposals.

The **system** in `system/` is shared and versioned on GitHub. Your **principal** — `users/<id>/` — stays on your machine and private.

Current system version: **0.6.1** (see [system/release/VERSION](system/release/VERSION)).

## What you get from GitHub

- `system/` — declared layers: agent protocol, bootstrap, engines, release (`system/instance.yaml`)
- `.gitignore` — keeps principals local
- This `README.md`

## Quick start

1. **Clone** this repository.
2. **Bootstrap** a principal:
   ```bash
   python3 system/release/scripts/init_jah.py <your-id>
   ```
   Init scaffolds types, registry, personal scope, and `knowledge-base/` automatically.
3. **Install** Python deps: `pip install -r requirements.txt` in a virtualenv.
4. **Read** [system/agent/protocol.md](system/agent/protocol.md) and [system/bootstrap/SETUP.md](system/bootstrap/SETUP.md).

## How to use Jah

Every task runs in a **session** under a project.

```bash
# Create a session
python3 system/engines/cli.py new-session users/<id>/projects/<project> "Your goal"

# Compile context
python3 system/engines/cli.py compile-context users/<id>/projects/<project>/sessions/YYYY-MM-DD-NNN
```

Work inside the session folder. End with `output.md`, `evaluation.md`, `trace.md`, and `patch.md`.

Full workflow: [system/agent/protocol.md](system/agent/protocol.md) · Session lifecycle: [system/agent/session_lifecycle.md](system/agent/session_lifecycle.md)

## Recent updates

<!-- recent-updates:start -->
### 0.6.1 (2026-06-13)
- Slim compile to session-start rules; add advisory check-write CLI

### 0.6.0 (2026-06-13)
- Add resolve-rules CLI and rule checkpoint protocol

### 0.5.0 (2026-06-13)
- Add constitution, rules lib, and Rule Index in compile-context

### 0.4.3 (2026-06-11)
- `type.project` — extend projects as a **project directory** (typed subdirs, one folder per database row), not a flat `documents/` file repo
- `types/project/README.md` — project directory vs file repo table, migration mapping, agent protocol, and anti-patterns
- `open_structure.md`, `type_system.md` — cross-reference project-directory growth

### 0.4.2 (2026-06-11)
- Document connector access methods (MCP vs native CLI) and compile connectors index
<!-- recent-updates:end -->

Full history: [system/release/CHANGELOG.md](system/release/CHANGELOG.md).

## Contributing to the system

System changes live in `system/` and ship via GitHub PR.

**Before every commit** that changes tracked system files, bump the version and add a changelog entry:

```bash
python3 system/release/scripts/bump_release.py --bump patch -m "Short summary of the change"
python3 system/release/scripts/check_release.py   # optional guard
```

Details: [system/release/versioning.md](system/release/versioning.md) · Improvement path: [system/agent/improvement_protocol.md](system/agent/improvement_protocol.md)

## License

License not yet specified — add one when you open the repository publicly.
