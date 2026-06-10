# Permission Model

Simple permission levels for Jah sessions and agents.

```txt
L0 think
L1 read approved files
L2 write inside session folder
L3 propose local change via session patch.md
L4 modify principal after explicit approval
L5 modify system/ via GitHub PR with explicit approval
L6 use external service after approval
L7 publish/send/delete/pay only with explicit approval
```

## Session defaults

New sessions set:

- **allowed_write:** session folder only
- **requires_approval:**
  - modify stable principal instances (including profile)
  - modify registry or type definitions
  - modify system/
  - use external tools
  - publish or send anything externally

## Git boundary

Changes to `system/` require L5 — explicit approval and a GitHub PR. Principal changes use L3–L4: propose in patch, apply manually after review.

## Proactive offers

Agents may **offer** L3–L5 changes during work (`proactive_capture.md`) but must not apply them until the user explicitly approves.
