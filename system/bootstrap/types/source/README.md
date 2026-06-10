# Source Type

A **single** reusable reference — one catalog entry in `index.md`, or one binary under `files/`.

The **`sources/` folder** is a **`type.directory` container** with `content_type: source`. Read `sources/instance.yaml` before storing anything.

**Agents:** read `sources/instance.yaml`, then this file. Schema: `users/<principal>/types/source/type.yaml`. Examples: `users/<principal>/types/source/examples.md`. Container scaffold: `users/<principal>/types/directory/scaffold/source-container.yaml`. Starter catalog: `users/<principal>/types/source/index.template.md`.

## Where files live

**Project resources:**

```
users/<principal>/projects/<project>/sources/
  instance.yaml     # type: directory, content_type: source — read before writing
  index.md          # catalog — one entry per source item
  files/            # binary assets only
    <group>/        # e.g. 2025/, identity/
      <name>.<ext>  # kebab-case descriptive filename
```

**Personal resources:**

```
users/<principal>/personal/sources/
  instance.yaml     # type: directory, content_type: source
  index.md
  files/
    <group>/
      <name>.<ext>
```

External-only references (no local file) are cataloged in `index.md` with a URL instead of a `files/` path.

## When to use

| Situation | Location |
|-----------|----------|
| Reusable PDF, image, video, or audio for a project | `sources/files/<group>/` + entry in `index.md` |
| Reusable personal file used across projects | `users/<principal>/personal/sources/files/` + entry in `index.md` |
| External link (no local copy) | Entry in `index.md` with `path_or_url` as full URL |
| Session-only draft | Session folder; promote to `sources/` after user approval |

## Agent directory steps

1. **Read** `sources/instance.yaml` (type.directory) and this README.
2. **Classify** — reusable across sessions? project-scoped or personal?
3. **Ask** if approval is needed (default session is L2; writing to `sources/` is L3–L4).
4. **Save the file** under `sources/files/<group>/<descriptive-name>.<ext>`.
5. **Catalog** — add a **source** entry to `sources/index.md` (never store a reusable binary without one).
6. **Cite** the path in session `output.md`, `trace.md`, or `patch.md` when the file informed work.

## Catalog entry format

Each entry in `index.md` is one **source** item:

```markdown
### <Human-readable name>

- **id:** source.<slug>
- **media_type:** pdf | image | video | audio | markdown | other
- **source_type:** internal_file | external_url
- **path_or_url:** `files/2025/w2-minerva.pdf` or `https://...`
- **summary:** One-line description
- **sensitivity:** low | medium | high
- **tags:** optional, comma-separated
- **added:** YYYY-MM-DD
```

For `internal_file`, `path_or_url` is relative to the `sources/` folder.

## Media types

| media_type | Typical extensions |
|------------|-------------------|
| pdf | `.pdf` |
| image | `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.heic` |
| video | `.mp4`, `.mov`, `.webm` |
| audio | `.mp3`, `.m4a`, `.wav` |
| markdown | `.md` |
| other | anything else — note format in summary |

## Scaffolding a new sources folder

1. Create `sources/` under the project or `users/<principal>/personal/`
2. Copy `users/<principal>/types/directory/scaffold/source-container.yaml` → `sources/instance.yaml` and set `id`, `name`
3. Copy `users/<principal>/types/source/index.template.md` → `sources/index.md` and remove example entries
4. Create `sources/files/` (add `<group>/` subfolders as files arrive)
5. Register in parent `instance.yaml` with `type: directory`, `content_type: source`

## Do not

- Set `type: source` on `sources/instance.yaml` — the folder is `type: directory`
- Store binaries at `sources/` root — use `sources/files/<group>/`
- Add catalog entries without a real file or URL
- Auto-write to `sources/` without user approval in a default session
