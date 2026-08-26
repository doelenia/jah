# Project Archive

How Jah moves finished or inactive projects out of active scope without deleting them.

**Engine:** `python3 system/engines/cli.py archive-project` / `unarchive-project`.

## Why a place, not only a flag

Active projects are the named children of `projects/` whose `instance.yaml` has `type: project`. A status flag left in place would still look like an active project on every listing. Archive is a **declared field of the projects directory** — a folder that is **not a project**.

## Layout

```
users/<id>/projects/
  instance.yaml       # type: directory, content_type: project
                      # fields.archive → archive/ (kind: project_archive)
  jah/                # type: project (active)
  archive/            # NOT a project — type: directory, kind: project_archive
    instance.yaml
    argentina-visa/   # type: project, status: archived
```

Read `instance.yaml` before treating any child of `projects/` as a project. The archive folder is `type: directory` with `kind: project_archive`. Do not invent `type.archive`.

## How Jah tells archive from a project

| Check | Archive container | Archived project | Active project |
|-------|-------------------|------------------|----------------|
| Path | `projects/archive/` | `projects/archive/<name>/` | `projects/<name>/` |
| `type` | `directory` | `project` | `project` |
| `kind` | `project_archive` | — | — |
| `status` | — | `archived` | `active` or omitted |

Parent declaration (required once archive exists) in `projects/instance.yaml`:

```yaml
fields:
  archive:
    type: directory
    content_type: project
    kind: project_archive
    storage: archive/
```

Engines resolve projects only when `type` is `project`. `new-session users/<id>/projects/archive` fails — that path is the container, not a project.

## Instance metadata (archived project)

Root keys on the **project** `instance.yaml`:

| Key | Values | Notes |
|-----|--------|-------|
| `status` | `active` (default if omitted) \| `archived` | Set by the engine on move |
| `archived_at` | ISO timestamp | Set on archive; removed on unarchive |
| `archived_from` | repo-relative path | Path before the move (e.g. `users/<id>/projects/<name>`) |

## Commands

```bash
python3 system/engines/cli.py archive-project users/<id>/projects/<name>
python3 system/engines/cli.py unarchive-project users/<id>/projects/archive/<name>
```

Archive:

1. Resolve a **project** instance (refuse if `type` is not `project`, including the archive container).
2. Scaffold `projects/archive/` with `kind: project_archive`; register `fields.archive` on `projects/instance.yaml`.
3. Move `projects/<name>/` → `projects/archive/<name>/`.
4. Set `status: archived`, `archived_at`, `archived_from`.
5. Rewrite session `main_instance` paths inside the moved project.

Unarchive reverses the move to `projects/<name>/`.

## Agent protocol

1. **List active projects** by reading each `projects/<name>/instance.yaml` and keeping `type: project` only. Skip `kind: project_archive`.
2. **New sessions** on an archived project fail unless `--force`. Prefer `unarchive-project` if work is resuming.
3. **Compile** still works on sessions that already exist under an archived project.
4. **Do not delete** on archive. The folder is the record.
5. After archive, cite `users/<id>/projects/archive/<name>/`.

## Permission

Archiving is **L3** (move an existing project). Creating `projects/archive/` is a grown field on the existing projects directory — also L3. No new registry type.

## Related

- `types/project/README.md` — project protocol
- `types/directory/README.md` — `kind: project_archive`
- `principal_model.md` — principal layout
- `storage_rules.md` — session paths after a move
