# Knowledge Base

Curated intellectual property index for a principal. Source files stay in `sources/files/` (personal, project, or type scope); the knowledge base tracks **what you learned**, **where it applies**, and **how to find it again**.

## What knowledge is

Knowledge entries are **reusable wisdom with user audit** — not all information.

| In knowledge-base | Not in knowledge-base |
|-------------------|------------------------|
| User-authored insight you'd reuse | Raw session scratch |
| AI output you annotated or reviewed | Unreviewed model output |
| External work you annotated or reviewed | Source catalog entry with no curation |
| Synthesis used for decisions or generation | Profile facts, rule text, project context |

**Evidence vs wisdom:** `sources/` holds artifacts (PDF, markdown, URL). Knowledge entries hold curated claims linked to those artifacts via `grounded_in`.

## Architecture

```
users/<id>/
  knowledge-base/
    topics.yaml       # OECD FORD field taxonomy (domain.field)
    index.yaml        # knowledge.<id> → entry file path
    entries/          # one YAML file per entry
  personal/sources/files/
  projects/<p>/sources/files/
```

- **No `type.knowledge`** — tracked markdown remains `type.source` in scope catalogs.
- **Identity** — stable `knowledge.<slug>` in `index.yaml`; file paths are mutable metadata.
- **System engine** — runtime in `system/engines/knowledge/`; schema defined here, not in the type registry.

## Facet separation

| Facet | Question | Stored in |
|-------|----------|-----------|
| **Field** | What domain of knowledge is this about? | `topic: domain.field` |
| **Context** | Where is it applied? | `applies_to` (project, type, workflow, rule) |
| **Evidence** | What artifact grounds it? | `grounded_in`, `canonical_path` |
| **Lifecycle** | How mature / audited? | `maturity`, `audit`, `status` |

**Topic assignment rule:** pick the FORD **field** the wisdom is *about*. Put project, type, workflow, and rule refs in `applies_to` — never in `topic`.

Example:

```yaml
topic: humanities_arts.languages_literature
applies_to:
  - rule.writing.concrete_observation_first
  - workflow.jah.blog
  - project.jah
```

## Topics — OECD FORD 2015

**Framework:** [Frascati Manual 2015](https://www.oecd.org/en/publications/frascati-manual-2015_g1g57dcb.html) Table 2.2 — [UNSD FORD](https://unstats.un.org/unsd/classifications/Family/Detail/1039).

- **L1** = broad field (domain slug)
- **L2** = field (facet slug)
- Topic ID = `domain.field` (max depth 2)
- Each L2 node has `ford_code` for external mapping
- **`general.uncategorized`** — Jah extension for staging only

Design influence: [FAST](https://www.oclc.org/en/fast.html) facet separation — topics carry the Field facet; `applies_to` carries Context. Do not import FAST headings.

Topic tree lives in `knowledge-base/topics.yaml`. Validate with `validate_knowledge.py`.

## Entry schema

Each entry is a YAML file under `knowledge-base/entries/<domain>/<slug>.yaml`:

```yaml
id: knowledge.concrete-observation-first
topic: humanities_arts.languages_literature
status: active              # active | superseded | archived
maturity: developing        # tentative | developing | stable
audit: reviewed             # unaudited | reviewed | endorsed
provenance: user            # user | ai_assisted | external_cited
summary: "One-line reusable claim."
grounded_in:
  - source_id: source.writing.notes-2026-06
    scope: project.jah
    annotation: "User audit note."
applies_to:
  - rule.writing.concrete_observation_first
  - workflow.jah.blog
  - project.jah
canonical_path: users/<id>/projects/jah/sources/files/writing/concrete-obs.md
related_topics: []
related_entries: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

Register every entry in `knowledge-base/index.yaml`:

```yaml
entries:
  knowledge.concrete-observation-first:
    path: entries/humanities_arts/concrete-observation-first.yaml
```

### Agent use gate

- **Authoritative for generation:** `audit: reviewed` or `audit: endorsed`
- **List only (do not cite as authority):** `audit: unaudited` or `maturity: tentative`

## Agent protocol

### 1. Find

After context compilation, review **Matched Knowledge** in `compiled_context.md`.

During discovery (`discovery_protocol.md`):

```bash
python3 system/engines/cli.py resolve-knowledge <knowledge-id>
python3 system/engines/cli.py resolve-knowledge --topic domain.field
python3 system/engines/cli.py resolve-knowledge --applies-to project.jah
python3 system/engines/cli.py resolve-knowledge --source-id source.foo
```

Search paths: `knowledge-base/index.yaml`, `knowledge-base/entries/`, `topics.yaml`.

### 2. Create

Create an entry when:

- User asks to save insight
- Reusable wisdom with user audit or annotation
- Same idea appears in 2+ sessions
- A rule or workflow needs grounding

Steps:

1. Assign FORD `topic` (or `general.uncategorized` if unsure)
2. Write entry YAML under `entries/<domain>/<slug>.yaml`
3. Add row to `index.yaml`
4. Link `grounded_in` to `source.<id>` when a source file exists
5. Set `applies_to` for project/type/workflow/rule context
6. Log in session `trace.md`

Default on capture: `maturity: tentative`, `audit: unaudited` unless user explicitly reviewed.

Do **not** create entries for: session-only scratch, unreviewed AI output, catalog-only sources.

### 3. Update

| Event | Action |
|-------|--------|
| Referenced in later session | Bump `maturity` toward `stable`; set `updated` |
| User confirms insight | Set `audit: reviewed` or `endorsed` |
| File moved | Update `canonical_path` only |
| Superseded | Set `status: superseded`; link `related_entries` |
| Topic clarified | Change `topic`; keep entry `id` stable |

Record changes in session `trace.md` (L3 — no approval needed for existing entries).

### 4. Audit

Run periodically and at session end when knowledge was touched:

```bash
python3 system/engines/cli.py validate-knowledge
```

Checks:

- Index ↔ entry file parity
- Entry `id` matches index key
- `topic` exists in `topics.yaml` (or alias)
- `canonical_path` exists when set
- `grounded_in.source_id` resolvable in scope catalog
- `tentative` + `unaudited` entries older than 90 days (warning)

## Permissions

| Action | Level |
|--------|-------|
| Create/update existing knowledge entries | L3 — auto; log in `trace.md` |
| Add Jah extension topic nodes | Note in `trace.md`; offer in `patch.md` |
| Modify `system/agent/knowledge_base.md` | L5 — explicit request + PR |

## Related docs

- `discovery_protocol.md` — active search
- `proactive_capture.md` — capture classification
- `context_compilation.md` — Matched Knowledge section
- `principal_model.md` — principal layout
- `storage_rules.md` — where files live
