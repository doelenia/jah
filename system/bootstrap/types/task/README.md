# Task Type

Planned work item — backlog and lifecycle tracking distinct from ephemeral **sessions** (execution) and repeatable **workflows** (procedures).

Each **leaf folder** is one `type: task` instance. The **`tasks/` folder** is a **`type.directory` container** with `content_type: task`. Read `tasks/instance.yaml` before creating or updating tasks.

**Agents:** read `tasks/instance.yaml`, then this file. Container scaffold: `users/<principal>/types/directory/scaffold/task-container.yaml`.

## Tasks vs sessions vs workflows

| Concept | Role | Lifetime |
|---------|------|----------|
| **Task** | Planned work with status (backlog → done) | Persistent until closed |
| **Session** | Isolated workspace executing one unit of work | Temporary |
| **Workflow** | Callable repeatable procedure | Persistent template |

A task may spawn a session when work starts (`status: in_progress`, `session` field set).

## Structure

```
users/<principal>/projects/<project>/tasks/
  instance.yaml              # type: directory, content_type: task
  index.md                   # catalog — required
  <name>/
    instance.yaml            # type: task (leaf)
    description.md           # goal, acceptance criteria, notes

users/<principal>/personal/tasks/   # optional cross-project backlog
  instance.yaml
  index.md
  <name>/
    ...
```

## Agent protocol

1. Read `tasks/instance.yaml` (type.directory), `users/<principal>/types/task/type.yaml`, and this README.
2. Read the task folder's `instance.yaml` for `id`, `status`, `scope`, `project`.
3. When creating a new task:
   - Create folder under `tasks/<kebab-name>/`.
   - Add `instance.yaml` with `type: task`, `status: pending`, and scope fields.
   - Write `description.md` with goal and acceptance criteria.
   - Add entry to `tasks/index.md`.
4. When starting work on a task:
   - Create or reuse a session.
   - Set task `status: in_progress` and `session: <session-id>`.
5. When work completes, set `status: done` and keep the linked session for traceability.

## Instance example

```yaml
id: task.example.my_task
type: task
name: My Task
status: pending
scope: project
project: project.example
priority: medium
description:
  type: document
  storage: description.md
```
