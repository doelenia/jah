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
3. When a session surfaces a new or corrected stable fact and the current request did not name the profile, **propose** an update in session `patch.md`. Do not write `profile.md` from the agent's own capture.
4. When the current request names the profile change, apply it. That request is the approval (`system/agent/agency.md`). Do not ask a second time.

## Do not

- Store one-off or session-only details in profile.
- Auto-write profile when the current request did not name it.
