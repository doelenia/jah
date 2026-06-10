# Preference Type

Scoped defaults. Each **leaf folder** is one `type: preference` instance.

The **`preferences/` folder** is a **`type.directory` container** with `content_type: preference`. Read `preferences/instance.yaml` before creating or editing preferences.

**Agents:** read `preferences/instance.yaml`, then this file. Container scaffold: `users/<principal>/types/directory/scaffold/preference-container.yaml`.

## Structure

```
users/<principal>/personal/preferences/
  instance.yaml              # type: directory, content_type: preference
  <name>/
    instance.yaml            # type: preference (leaf)
    general.md               # content file (path in content_path)
```

## Agent protocol

1. Read `preferences/instance.yaml` (type.directory), `types/preference/type.yaml`, and this README.
2. Read the preference folder's `instance.yaml` for `id`, `scope`, and `content_path`.
3. Edit the content file at `content_path` only with user approval; propose in `patch.md`.
4. When creating a new preference:
   - Create folder under `preferences/<name>/`.
   - Add `instance.yaml` with `type: preference`, `scope`, `content_path`.
   - Register in parent `instance.yaml` `fields.preferences` list.
   - Create the content markdown file.

## Instance example

```yaml
id: preference.writing
type: preference
name: Writing Preferences
scope: global
content_path: general.md
```
