# Rule Type

Active constraints stored as self-contained YAML **file instances**.

The **`rules/` folder** is a **`type.directory` container** with `content_type: rule`. Read `rules/instance.yaml` before creating or editing rules.

**Agents:** read `rules/instance.yaml`, then this file. Container scaffold: `users/<principal>/types/directory/scaffold/rule-container.yaml`.

## Storage

```
users/<principal>/personal/rules/
  instance.yaml              # type: directory, content_type: rule
  <group>/<name>.yaml        # each YAML file is type: rule
users/<principal>/projects/<project>/rules/
  instance.yaml
  <group>/<name>.yaml
```

## Agent protocol

1. Read `rules/instance.yaml` (type.directory), `types/rule/type.yaml`, and this README.
2. Every rule file must include `id`, `type: rule`, `name`, `scope`, `status`, and `rule`.
3. Optional `activation_trigger` — when the rule applies (`session_start`, `pre_write`, `topic_shift`, `pre_approval`). Default: `[session_start]`.
4. When creating a new rule:
   - Choose group folder (e.g. `writing/`, `general/`).
   - Create `<name>.yaml` with a unique `id` (e.g. `rule.writing.<name>`).
4. Propose new rules in session `patch.md`; apply only after user approval.

## Instance example

```yaml
id: rule.writing.concrete_observation_first
type: rule
name: Concrete Observation First
scope: global
priority: 80
status: active
activation_trigger:
  - session_start
applies_to:
  - workflow.jah.blog
rule: "Begin from a concrete observation before the abstract thesis."
```
