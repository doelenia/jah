# Principal Type

A principal is one user's (or organization's) local world at `users/<id>/`.

**Agents:** read this file before creating or modifying a principal namespace.

## Structure

```
users/<id>/
  instance.yaml       # type: principal
  registry.yaml       # type registry — authoritative type index
  types/              # registered type definitions
  personal/           # type: personal — cross-project instances
  projects/           # project instances (archive/ is kind: project_archive — not a project)
  knowledge-base/     # curated knowledge index — see system/agent/knowledge_base.md
  connectors/         # optional — how external services are accessed (MCP + CLI); see system/agent/connectors.md
```

## Agent protocol

1. Read `users/<id>/instance.yaml` and `registry.yaml`.
2. Resolve all types through the registry — see `system/type_system.md`.
3. Never assume types live outside `users/<id>/types/`.
4. Propose principal changes in session `patch.md`; apply only after user approval (L4).

## Active principal

The repo root `jah.yaml` declares `active_principal`. Scripts and agents use it to resolve paths.
