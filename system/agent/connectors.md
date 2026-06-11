# Connectors

Principal connectors document **how** external services are accessed — not only that they exist.

MCP config often lives in agent-specific files (Cursor, Claude Code, Codex). The canonical description lives under `users/<id>/connectors/`. When using a **new agent** for the first time, read the connectors index and replicate the documented setup for that agent.

## Where connectors live

```
users/<id>/connectors/
  README.md              # index — access method per connector (read first)
  <name>/README.md       # setup and usage for one service
```

Optional: scripts, CLI, credential paths, calendar IDs, etc. under each `<name>/` folder.

## Access methods

| Method | Meaning | Agent setup |
|--------|---------|-------------|
| **MCP** | Model Context Protocol — tools exposed by an MCP server | **Per agent.** Document config file paths in the connector README. A new agent must add the same server entry before tools work. |
| **Native CLI** | Principal script invoked via shell (`python3 …/calendar.py`) | **Agent-agnostic.** Any agent with shell access runs the documented command. No MCP config. |
| **Direct API** | Hand-rolled HTTP/SDK calls using documented tokens and paths | **Agent-agnostic.** Prefer wrapping in a CLI under `connectors/` when non-trivial. |

## Agent protocol

1. **Orient** — if the task touches an external service, read `users/<id>/connectors/README.md` before acting.
2. **Resolve access** — open the connector's `README.md` for method (MCP vs CLI), credential paths, and account routing.
3. **New agent** — if MCP tools are missing, do **not** guess. Follow the connector README to add MCP config for **that** agent (Cursor: `.cursor/mcp.json` or `~/.cursor/mcp.json`; Claude Code: `.mcp.json`; others: that product's MCP config path).
4. **Prefer documented path** — use the connector's CLI or MCP as documented; avoid one-off API hacks unless the README allows it.
5. **Semantic routing** — business rules (which account, which calendar, which workspace) stay in `personal/preferences/`, `personal/rules/`, or project context — not in MCP config alone.

## MCP config is not the source of truth

| Layer | Role |
|-------|------|
| `users/<id>/connectors/` | **Canonical** — what is connected, how, and how to set up each agent |
| `~/.cursor/mcp.json`, `.cursor/mcp.json`, `.mcp.json` | **Agent-local** — copies of MCP entries; must match connector docs |
| MCP server runtime | Executes tools once the agent has loaded the server |

Compiled context includes the connector protocol and principal connectors index (`context_compilation.md`).

## Capture

When adding or changing a connector:

- Update `users/<id>/connectors/README.md` index
- Add or update `users/<id>/connectors/<name>/README.md`
- Note which agents have MCP configured (Cursor, Claude Code, etc.)
- Log in session `trace.md` when wiring changes

## Related docs

- `discovery_protocol.md` — scope expansion may include `connectors/`
- `principal_model.md` — principal layout
- `permission_model.md` — L3 auto-update for connectors
