# Memory Model

Where living instances live in Jah.

## Structure

```
memory/
  personal/           # You
    instance.yaml
    profile.md
    preferences/
    rules/
    workflows/        # cross-project callable procedures (optional)
      index.md
    sources/          # cross-project reusable files (optional)
      index.md
      files/
  projects/
    <project>/        # e.g. jah, ausna
      instance.yaml
      context.md
      rules/
      sources/        # project reusable files and links
        index.md      # catalog — required when storing files
        files/        # PDFs, images, video, audio, etc.
      workflows/
        index.md      # catalog — required
      sessions/
```

## Instance rule

Every folder representing a living instance contains `instance.yaml`:

```yaml
id: <unique-id>
type: <type-name>
name: <human name>
```

Container instances declare typed child fields in a `fields:` block. Each field references a type from `types/<name>/type.yaml`. Agents must read the type README before working with a field — see `system/type_system.md`.

Personal memory uses `type: personal` (not `base`). Projects use `type: project`.

## Personal memory

- **Profile** — who you are (`profile.md`)
- **Preferences** — scoped defaults (writing, lifestyle, etc.)
- **Rules** — active constraints (YAML with scope, priority, applies_to)

### Profile

`memory/personal/profile.md` is the canonical store for **stable, reusable personal facts**: identity, nationality, age, addresses, tax residency, legal names, contact info, and similar attributes that should persist across sessions.

**Update protocol:**

1. Context compilation includes the current profile so agents can reuse and diff against it.
2. When a session surfaces a new or corrected stable personal fact, the agent **must propose** an update in session `patch.md` — not write `profile.md` directly.
3. During work, agents **should ask** whether to capture profile updates when the user provides stable facts (`proactive_capture.md`).
4. Apply profile changes manually after review (L4). Scripts never auto-update profile.
5. Do not store one-off or session-only details in profile; keep those in session `input.md`, `output.md`, or `trace.md`.

## Project memory

- **Context** — what the project is
- **Rules / sources** — project-specific references
- **Workflows** — callable procedures (`scope: personal`, `type`, or `project`) with requirements, workflow body, evaluation, examples; cataloged in `workflows/index.md`
- **Sessions** — temporary workspaces

### Sources (reusable resources)

`sources/` holds **stable, reusable reference material** — PDFs, images, video, audio, markdown notes, and external links used across sessions.

| Path | Purpose |
|------|---------|
| `sources/index.md` | Catalog of every resource (file path or URL, summary, sensitivity) |
| `sources/files/` | Binary and file-based assets, grouped by year or topic when helpful |

**Personal sources** (`memory/personal/sources/`) follow the same layout for cross-project files (e.g. passport scan, certificates).

**Agent protocol** — see `types/source/README.md`:

1. Save reusable files under `sources/files/<group>/<descriptive-name>.<ext>` (kebab-case).
2. Add a catalog entry to `sources/index.md` (never store a reusable file without cataloging it).
3. Session-only working copies may stay in the session folder; promote to `sources/` after user approval.
4. Cite `path_or_url` in session artifacts when the resource informed output.

External-only references (no local copy) are cataloged in `index.md` with a full URL.

## Git

All of `memory/` is local. Never committed to GitHub.

## References

When content is created from an internal or external source, it must cite that source.

| Source kind | Citation format | Example |
|-------------|-----------------|--------|
| Internal | Repo-relative path | `memory/personal/profile.md` |
| External | Full URL | `https://www.irs.gov/...` |

**Where references belong:**

- **Session `output.md`** — cite sources that informed the deliverable
- **Session `patch.md`** — cite sources behind every proposed stable-memory change
- **Session `trace.md`** — cite sources behind key decisions when applicable
- **Stable memory** (profile, preferences, project context, workflows) — cite sources inline or in a References section when content draws on specific files or URLs

If nothing beyond compiled context and undifferentiated session input was used, say so explicitly (e.g. "None — original work from session input and compiled context").

Do not create unattributed content from specific internal files or external links.

## Stable vs session

- **Stable memory** — preferences, rules, project context, workflows, sources (catalog + `files/`)
- **Session memory** — input, output, evaluation, trace, patch, compiled_context, session-only drafts

Modify stable memory only with explicit approval (see `permission_model.md`).
