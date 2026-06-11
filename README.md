# Jah

A local-first, AI-native personal OS. Jah turns repeated work into stable, preference-aware automation through typed instances, context compilation, sessions, traces, and local improvement proposals.

The **system** in `system/` is shared and versioned on GitHub. Your **principal** — `users/<id>/` — stays on your machine and private.

Current system version: **0.4.2** (see [system/release/VERSION](system/release/VERSION)).

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
### 0.4.2 (2026-06-11)
- Document connector access methods (MCP vs native CLI) and compile connectors index

### 0.4.1 (2026-06-10)
- Rename principal `tools` field and folder to `connectors` — external services, devices, MCP, custom glue (`type.principal`, agent docs, engines)
- Add `system/release/scripts/migrate_tools_to_connectors.py` for local principal migration

### 0.4.0 (2026-06-10)
- `system/instance.yaml` — declared system layers (agent, bootstrap, engines, release, interface)
- `system/README.md` and per-layer READMEs
- `system/engines/` — protocol runtime grouped by domain (knowledge, context, registry, structure, session, instances)
- `system/engines/cli.py` — unified CLI for all protocol engines
- …and 2 more (see changelog)

### 0.3.1 (2026-06-10)
- **Operation model** (Orient → Plan → Act → Capture) as top-priority default in `protocol.md`
- **Operation Checklist** preamble in `compile_context.py` — first section after Session Goal in every compiled context
- **Scope expansion** mandatory step in `discovery_protocol.md` — enumerate relevant paths before implementation; Session plan in `trace.md`

### 0.3.0 (2026-06-10)
- `system/knowledge_base.md` — curated IP engine: OECD FORD field topics, entry schema, facet separation, agent create/update/find/audit protocol
- `system/bootstrap/knowledge-base/` — topics.yaml (full FORD L1+L2 + `general.uncategorized`), index.yaml, instance.yaml scaffold
- Bootstrap tool scripts: `knowledge_lib.py`, `resolve_knowledge.py`, `validate_knowledge.py`
- `compile_context.py` — **Matched Knowledge** section; loads `knowledge_base.md` in agent protocol
- …and 1 more (see changelog)
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
