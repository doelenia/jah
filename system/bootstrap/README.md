# Bootstrap Layer

Copy-once starter kit for new principals. Contains **data scaffolds only** — no Python runtime.

## Contents

| Path | Purpose |
|------|---------|
| `SETUP.md` | Bootstrap procedure |
| `registry.seed.yaml` | Starter registry |
| `principal.seed/` | Principal instance template |
| `types/` | Starter type definitions |
| `knowledge-base/` | Knowledge index scaffold (topics, index) |

## Init

```bash
python3 system/release/scripts/init_jah.py <principal-id>
```

After init, the principal owns all copied types and data. Bootstrap is not runtime authority.

Protocol engines live in `system/engines/` — never copied to `users/<id>/`.
