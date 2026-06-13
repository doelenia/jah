# Project Type

A project in memory. Examples: `users/<principal>/projects/jah/`, `users/<principal>/projects/ausna/`.

**Agents:** read this file before creating, reading, or modifying any project. Open structure: `system/agent/open_structure.md`.

## Baseline and growth

`type.project` declares a **minimal baseline** in `type.yaml` `fields` (context, sessions, rules, …). Every project instance must include non-optional baseline fields. Instances may **add** grown fields without a new project subtype — `open_fields` defaults true on `type.base`.

When extending a project, use a **project directory** — a tree of typed subdirectories — not a flat file repo.

## Project directory vs file repo

| Pattern | Use when | Shape |
|---------|----------|--------|
| **Project directory** (preferred) | Grown project parts, migrated pages, database rows, domain sections | Each logical unit is its own subdirectory with `instance.yaml` |
| **File repo** (`documents/` dump) | Avoid for project growth | Flat markdown files — belongs on `type.personal`, not default project extension |

**Default for grown fields:** treat each new part as a **subdirectory**, not a file in a shared `documents/` folder.

| Notion / source concept | Local shape |
|-------------------------|-------------|
| Top-level page or section | Grown field → subdir (`program-design/`, `partners/`) with `type.base` + `context.md` |
| Nested page | Subdir under its parent (`program-design/initial-proposal/proposal-v01-en/`) |
| Database / table | `type.directory` container; **one folder per row** (`fellowship/<person>/`, `opportunities/sf-matrix/<entry>/`) |
| Support docs for a database | Markdown files **inside that container** (`fellowship/validating-questions.md`), not at project root |
| External references | `sources/` (`content_type: source`) |
| Repeatable procedures | `workflows/` (`content_type: workflow`) |

Do not create a project-level `documents/` folder to hold migrated pages or database exports. That pattern is for `type.personal` reference files, not for living project structure.

## Structure

```
users/<principal>/projects/<project>/
  instance.yaml       # type: project — declares baseline + grown fields
  context.md          # type.context
  preferences/        # type.directory (optional)
  rules/              # type.directory
  sources/            # type.directory — external references
  workflows/          # type.directory — callable procedures
  sessions/           # type.directory (content_type: session)
  tasks/              # type.directory (optional)
  program/            # example grown part — type.base or nested tree
    instance.yaml
    context.md
    program-design/
    fellowship/       # type.directory — people pipeline
      index.md
      validating-questions.md
      <person-slug>/  # one folder per database row
  platform/           # example grown part — sibling section
```

## Grown field types

| Grown field role | Typical `type` | Notes |
|------------------|----------------|-------|
| Section / page | `base` | `context.md` + optional nested subdirs |
| Database / catalog | `directory` | `content_type: base` (or item type); entry folders + `catalog: index.md` |
| Callable procedure | `workflow` | Under `workflows/` or scoped under a part |

Register every grown field in the project `instance.yaml` `fields` block with `storage:` pointing at the subdirectory.

## Agent protocol

1. Read `users/<principal>/types/project/type.yaml` and this README.
2. Read `users/<principal>/projects/<project>/instance.yaml` — resolve every field's `type`, `id`, and `storage`.
3. Before writing to a directory field, read that directory's **`instance.yaml`** (`type.directory`), then the **content type** README.
4. When adding a grown field:
   - Create a **subdirectory** with its own `instance.yaml` (not a loose file in `documents/`).
   - For databases and pipelines: use `type.directory`; one subfolder per entry.
   - For section pages: use `type.base` with `context.md`; nest children as subdirs.
   - Register the field in the parent `instance.yaml` `fields` block.
5. Keep Notion or external URLs as archive links in `context.md` footers — local folders are authoritative.
6. Propose durable type baseline changes in session `patch.md`; apply after user approval.

## Creating a new project

1. Create `users/<principal>/projects/<name>/instance.yaml` with `type: project`.
2. Add `fields.context` pointing to `context.md`; write initial `context.md`.
3. Scaffold baseline directory containers (`rules/`, `sources/`, `workflows/`, `sessions/`, `tasks/`) from `users/<principal>/types/directory/scaffold/` as needed.
4. Add grown parts as subdirectories (`design/`, `program/`, …) — project-directory shape from the start.
5. Register each child instance in the `fields` block as it is created.

## Do not

- Default to a top-level `documents/` folder for project pages or migrations
- Store database rows only in a single catalog markdown file when each row should be its own instance folder
- Infer field meaning from folder names without reading `instance.yaml`
