# Personal Type

Cross-project personal memory at `users/<principal>/personal/`.

**Agents:** read this file before reading or modifying personal memory. Open structure: `system/agent/open_structure.md`.

## Baseline and growth

`type.personal` declares a minimal baseline in `type.yaml` `fields`. Instances must include non-optional baseline fields and may add grown fields beyond the baseline.

## Structure

```
users/<principal>/personal/
  instance.yaml       # type: personal
  profile.md          # type.profile
  preferences/        # type.directory container (content_type: preference)
  rules/              # type.directory container (content_type: rule)
  sources/            # type.directory container (content_type: source)
  documents/          # type.directory container (content_type: document)
```

## Agent protocol

1. Read `users/<principal>/types/personal/type.yaml` and this README.
2. Read `users/<principal>/personal/instance.yaml` to resolve field ids and child instance paths.
3. Before writing to a directory field, read that directory's **`instance.yaml`** (type.directory), then the **content type** README (`users/<principal>/types/source/`, `types/rule/`, or `types/preference/`).
4. Propose changes to stable personal memory in session `patch.md`; apply only after user approval.

## Creating child instances

| Field | Container | Item type | How to create |
|-------|-----------|-----------|---------------|
| `profile` | — | profile | Single file; declare in `instance.yaml` `fields.profile` |
| `preferences/` | type.directory | preference | Folder with `instance.yaml` + content file |
| `rules/` | type.directory | rule | `<group>/<name>.yaml` with `type: rule` |
| `sources/` | type.directory | source | `files/<group>/` + entry in `index.md` |
| `documents/` | type.directory | document | `<name>.<ext>` at directory root |

Scaffold containers from `users/<principal>/types/directory/scaffold/`.
