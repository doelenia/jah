# Jah System

Declared system instance for the Jah protocol. Inspect `instance.yaml` first — same discovery model as principal instances (`system/agent/open_structure.md`).

## Layers

| Layer | Path | Role |
|-------|------|------|
| **Agent** | `agent/` | Behavioral protocol — what agents should do |
| **Bootstrap** | `bootstrap/` | First-run kit — seeds a new principal (data only) |
| **Engines** | `engines/` | Runtime — implements protocol against principal data |
| **Release** | `release/` | Version, changelog, init and bump scripts |
| **Interface** | `interface/` | Human-facing surface (reserved, not implemented) |

## Read order

1. `agent/protocol.md` — primary entry
2. `agent/design_logic.md` — philosophy and system layers
3. `agent/open_structure.md` — declared folder growth
4. `bootstrap/SETUP.md` — if bootstrapping a principal

## CLI

All protocol engines run from a single entry:

```bash
python3 system/engines/cli.py <command> [args...]
```

Commands: `compile-context`, `new-session`, `list-instances`, `validate-registry`, `validate-structure`, `validate-knowledge`, `resolve-knowledge`

See `engines/README.md` for details.

## Bootstrap a principal

```bash
python3 system/release/scripts/init_jah.py <principal-id>
```

## System changes

Bump version before every system commit:

```bash
python3 system/release/scripts/bump_release.py --bump patch -m "Summary"
```

See `release/versioning.md`.
