# Permission Model

Simple permission levels for Jah sessions and agents.

```txt
L0 think
L1 read approved files
L2 write inside session folder
L3 propose local change via session patch.md
L4 modify local memory/types/tools after explicit approval
L5 modify system/ via GitHub PR with explicit approval
L6 use external service after approval
L7 publish/send/delete/pay only with explicit approval
```

## Session defaults

New sessions (`new_session.py`) set:

- **allowed_write:** session folder only
- **requires_approval:**
  - modify stable local memory
  - modify type definitions
  - modify system/
  - use external tools
  - publish or send anything externally

## Git boundary

Changes to `system/` require L5 — explicit approval and a GitHub PR. Local layers use L3–L4: propose in patch, apply manually after review.
