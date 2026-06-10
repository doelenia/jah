# Profile Type

Canonical store for stable, reusable personal facts.

**Agents:** read this file before proposing or discussing profile updates.

## Storage

```
users/<principal>/personal/profile.md
```

Declared in `users/<principal>/personal/instance.yaml`:

```yaml
fields:
  profile:
    id: profile.main
    type: profile
    storage: profile.md
```

## Agent protocol

1. Read `users/<principal>/types/personal/README.md` and `types/profile/type.yaml`.
2. Use compiled profile from `compiled_context.md` during work.
3. When a session surfaces a new or corrected stable fact, **propose** an update in session `patch.md` — never write `profile.md` directly without explicit approval.
4. Ask the user whether to capture profile updates at session end.

## Do not

- Store one-off or session-only details in profile.
- Auto-write profile during a session.
