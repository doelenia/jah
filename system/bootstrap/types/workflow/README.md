# Workflow Type

Callable repeatable procedure — like a function with preconditions, body, and postconditions.

Each **leaf folder** is one `type: workflow` instance. The **`workflows/` folder** is a **`type.directory` container** with `content_type: workflow`. Read `workflows/instance.yaml` before creating or invoking a workflow.

**Agents:** read `workflows/instance.yaml`, then this file. Container scaffold: `users/<principal>/types/directory/scaffold/workflow-container.yaml`.

## Types vs memory

| Layer | Location | Role |
|-------|----------|------|
| **Type** | `users/<principal>/types/workflow/` | Schema, agent protocol, templates |
| **Type scaffold** | `users/<principal>/types/<artifact_type>/workflows/<name>/` | Default signature + markdown templates (not invoked directly) |
| **Memory** | `users/<principal>/projects/<p>/workflows/<name>/` or `users/<principal>/personal/workflows/<name>/` | Living callable instances |

Types hold contracts and scaffolds. Memory holds what you actually invoke.

## Structure

```
users/<principal>/projects/<project>/workflows/
  instance.yaml              # type: directory, content_type: workflow
  index.md                   # catalog — required
  <name>/
    instance.yaml            # type: workflow (leaf)
    requirements.md          # preconditions
    workflow.md              # procedure body
    evaluation.md            # postconditions
    examples.md
    common_failures.md       # optional

users/<principal>/personal/workflows/   # cross-project workflows (optional)
  instance.yaml
  index.md
  <name>/
    ...
```

## Scope

| scope | Meaning | Example |
|-------|---------|---------|
| `personal` | Cross-project utility | `users/<principal>/personal/workflows/literature-review/` |
| `type` | Operates on instances of an artifact type | Draft a `type.blog_post` |
| `project` | Project-specific procedure | `workflow.us_taxes.tax_filing` |

## Invocation (sessions)

Sessions are call sites. Set in session `instance.yaml`:

- `workflow_id` — explicit call (strongest), e.g. `workflow.us_taxes.tax_filing`
- `workflow` — path relative to project, or `auto` for compile-time resolution
- `target_type` — hint for auto mode, e.g. `type.blog_post`

`compile_context.py` resolves workflows at compile time — only invoked workflows load full bodies.

## Agent protocol

1. Read `workflows/instance.yaml` (type.directory), `users/<principal>/types/workflow/type.yaml`, and this README.
2. Read the workflow folder's `instance.yaml` for `id`, `scope`, `dependencies`.
3. Each document field (`requirements`, `workflow`, …) is `type.document` — see `types/document/README.md`.
4. When creating a new workflow:
   - Create folder under `workflows/<name>/`.
   - Add `instance.yaml` with `type: workflow`, `scope`, `status: active`.
   - Create the four core markdown files.
   - Add entry to `workflows/index.md`.
   - Register in parent `instance.yaml` `fields.workflows` list.
5. To scaffold from a type default: copy from `users/<principal>/types/<artifact_type>/workflows/<name>/` into project memory, then customize.

## Type scaffolds

When an artifact type needs default procedures, add scaffolds only under types:

```
types/blog_post/workflows/draft/
  signature.template.yaml
  workflow.template.md
  requirements.template.md
  evaluation.template.md
```

Instantiate into `users/<principal>/projects/<p>/workflows/draft/` on first use. Project instances override type scaffolds.

## Instance examples

```yaml
# Project-scoped
id: workflow.us_taxes.tax_filing
type: workflow
name: Tax Filing
scope: project
project: project.us_taxes
status: active
dependencies:
  - users/<principal>/personal/profile.md

---
# Type-scoped (when artifact type exists)
id: workflow.blog.draft
type: workflow
name: Draft Blog Post
scope: type
operates_on: type.blog_post
status: active
dependencies:
  - users/<principal>/personal/preferences/writing/general.md
  - users/<principal>/personal/rules/writing/
```
