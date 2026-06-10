# Document Type

A single content file that belongs to a parent instance. Used for workflow steps, preference content, identity document files, and other stable artifacts.

**Agents:** read this file before creating or editing a `type.document` field or writing to a `documents/` directory container.

## Storage

- Filename is declared in the parent type's `storage` pattern or in the parent `instance.yaml` `fields` block.
- Content lives at that path relative to the parent instance folder.
- Document fields do **not** get their own folder or separate `instance.yaml` unless promoted to a first-class instance (e.g. `type.context`, `type.profile`).
- The **`documents/` folder** is a **`type.directory` container** with `content_type: document`. Read `documents/instance.yaml` before storing files there.

## Agent protocol

1. Resolve the parent instance's `instance.yaml` and its type definition (`users/<principal>/types/<name>/type.yaml`).
2. Read the field's declared `type` — if it is `type.document` or extends it, follow this README.
3. Create or edit only the declared `storage` path; do not invent alternate filenames.
4. When adding a new document field to a parent instance, declare it in the parent's `fields` block with `id`, `type`, and `storage`.

## Examples

- `users/<principal>/personal/preferences/writing/general.md` — content for `preference.writing`
- `users/<principal>/projects/jah/workflows/blog/requirements.md` — requirements for `workflow.jah.blog`
