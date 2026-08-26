#!/usr/bin/env python3
"""Compile session context from Jah dependencies (goal-aware)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

from env import (
    active_principal,
    agent_dir,
    all_registry_type_names,
    principal_root,
    repo_root,
    type_readme_paths,
    type_yaml_paths,
)
from knowledge.lib import knowledge_base_dir, match_entries
from rules.lib import (
    format_rule_bundle,
    format_rule_index_table,
    load_rules,
    project_id_from_path,
    resolve_bundle,
)

WORKFLOW_DOCS = ("requirements.md", "workflow.md", "evaluation.md", "examples.md", "common_failures.md")
TASK_DOCS = ("description.md",)
CORE_TYPE_NAMES = {
    "base",
    "session",
    "session_artifact",
    "project",
    "directory",
    "task",
    "workflow",
    "context",
    "document",
    "rule",
    "preference",
    "source",
}
SKIP_FIELD_DIRS = {"sessions", "workflows", "tasks", "context"}
CONTENT_EXTENSIONS = {".md", ".yaml", ".yml"}


def read_text(path: Path) -> str:
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return f"*(missing: {path.relative_to(repo_root())})*"


def load_yaml_file(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_yaml_block(path: Path) -> str:
    content = read_text(path)
    rel = path.relative_to(repo_root()).as_posix()
    return f"### `{rel}`\n\n```yaml\n{content.strip()}\n```\n"


def load_md_block(path: Path, heading: str | None = None) -> str:
    content = read_text(path)
    rel = path.relative_to(repo_root()).as_posix()
    title = heading or rel
    return f"### {title}\n\n{content.strip()}\n\n"


def goal_tokens(goal: str, input_text: str) -> set[str]:
    text = f"{goal} {input_text}".lower()
    tokens = set(re.findall(r"[a-z0-9]{4,}", text))
    return tokens


def text_matches_goal(goal: str, input_text: str, meta: dict, path: Path | None = None) -> bool:
    haystack = f"{goal} {input_text}".lower()
    needles = [
        str(meta.get("id") or "").lower(),
        str(meta.get("name") or "").lower(),
        str(meta.get("goal") or "").lower(),
        str(meta.get("description") or "").lower(),
    ]
    if path is not None:
        needles.append(path.name.lower().replace("-", " ").replace("_", " "))
    if any(n and n in haystack for n in needles):
        return True
    tokens = goal_tokens(goal, input_text)
    blob = " ".join(needles)
    return any(t in blob for t in tokens if len(t) >= 5)


def discover_leaf_instances(container_dir: Path) -> list[dict]:
    items: list[dict] = []
    if not container_dir.is_dir():
        return items
    for child in sorted(container_dir.iterdir()):
        if not child.is_dir():
            continue
        instance_path = child / "instance.yaml"
        if not instance_path.is_file():
            continue
        meta = load_yaml_file(instance_path)
        meta["_path"] = child
        meta["_container"] = container_dir
        items.append(meta)
    return items


discover_workflows = discover_leaf_instances


def type_scoped_workflows(principal: Path) -> list[dict]:
    types_dir = principal / "types"
    if not types_dir.is_dir():
        return []
    result = []
    seen: set[str] = set()
    for type_dir in sorted(types_dir.iterdir()):
        if not type_dir.is_dir():
            continue
        wf_dir = type_dir / "workflows"
        for wf in discover_leaf_instances(wf_dir):
            wf_id = wf.get("id", "")
            if wf_id and wf_id in seen:
                continue
            if wf_id:
                seen.add(wf_id)
            result.append(wf)
    return result


def all_project_workflows(project_path: Path) -> list[dict]:
    wf_dir = project_path / "workflows"
    return discover_leaf_instances(wf_dir) if wf_dir.is_dir() else []


def personal_workflows(principal: Path) -> list[dict]:
    container = principal / "personal" / "workflows"
    return discover_leaf_instances(container)


def all_project_tasks(project_path: Path) -> list[dict]:
    tasks_dir = project_path / "tasks"
    return discover_leaf_instances(tasks_dir) if tasks_dir.is_dir() else []


def workflow_status(wf: dict) -> str:
    return str(wf.get("status") or "active")


def is_active(wf: dict) -> bool:
    return workflow_status(wf) == "active"


def workflow_summary(wf: dict) -> str:
    return str(wf.get("description") or wf.get("name") or wf.get("id") or wf["_path"].name)


def personal_applies(wf: dict, project_path: Path, target_type: str | None) -> bool:
    if wf.get("scope") != "personal":
        return False
    applies_to = wf.get("applies_to") or []
    if not applies_to:
        return True
    project_name = project_path.name.replace("-", "_")
    project_id = f"project.{project_name}"
    candidates = {project_id, project_path.as_posix(), target_type or ""}
    return any(item in candidates for item in applies_to)


def goal_matches(goal: str, input_text: str, wf: dict) -> bool:
    return text_matches_goal(goal, input_text, wf, wf["_path"])


def resolve_workflow_path(project_path: Path, rel_path: str) -> dict | None:
    rel_path = rel_path.strip().strip('"').strip("'")
    if not rel_path:
        return None
    rel_path = rel_path.removeprefix("workflows/")
    candidate = project_path / "workflows" / rel_path
    instance = candidate / "instance.yaml"
    if instance.is_file():
        meta = load_yaml_file(instance)
        meta["_path"] = candidate
        meta["_container"] = candidate.parent
        return meta
    return None


def resolve_workflows(
    principal: Path,
    session_path: Path,
    project_path: Path,
    goal: str,
    session: dict,
    input_text: str,
) -> tuple[list[dict], list[dict]]:
    project_wfs = all_project_workflows(project_path)
    personal_wfs = [
        wf for wf in personal_workflows(principal)
        if personal_applies(wf, project_path, session.get("target_type"))
    ]
    type_wfs = type_scoped_workflows(principal)
    all_wfs = project_wfs + personal_wfs + type_wfs
    active_wfs = [wf for wf in all_wfs if is_active(wf)]

    workflow_id = session.get("workflow_id")
    workflow = session.get("workflow")
    target_type = session.get("target_type")

    invoked: list[dict] = []

    if workflow_id:
        invoked = [wf for wf in all_wfs if wf.get("id") == workflow_id]
    elif workflow and str(workflow).strip().lower() != "auto":
        found = resolve_workflow_path(project_path, str(workflow))
        invoked = [found] if found else []
    elif target_type:
        invoked = [wf for wf in active_wfs if wf.get("operates_on") == target_type]
    else:
        matched = [wf for wf in active_wfs if goal_matches(goal, input_text, wf)]
        if len(matched) == 1:
            invoked = matched
        elif not workflow_id and not workflow:
            project_scoped = [
                wf for wf in active_wfs
                if wf.get("scope") == "project" or wf.get("scope") is None
            ]
            if len(project_scoped) == 1:
                invoked = project_scoped

    invoked_ids = {wf.get("id") for wf in invoked if wf.get("id")}
    available = [wf for wf in active_wfs if wf.get("id") not in invoked_ids]
    return invoked, available


def session_ref(session_path: Path) -> str:
    return f"session.{session_path.name}"


def resolve_linked_task(
    project_path: Path,
    session_path: Path,
    session: dict,
) -> dict | None:
    task_id = session.get("task_id")
    all_tasks = all_project_tasks(project_path)
    if task_id:
        matched = [t for t in all_tasks if t.get("id") == task_id]
        if matched:
            return matched[0]
    current_ref = session_ref(session_path)
    for task in all_tasks:
        if str(task.get("session") or "") == current_ref:
            return task
    return None


def resolve_related_tasks(
    project_path: Path,
    goal: str,
    input_text: str,
    linked: dict | None,
    limit: int = 5,
) -> list[dict]:
    linked_id = linked.get("id") if linked else None
    matched = [
        t for t in all_project_tasks(project_path)
        if t.get("id") != linked_id and text_matches_goal(goal, input_text, t, t["_path"])
    ]
    return matched[:limit]


def resolve_related_sessions(
    project_path: Path,
    session_path: Path,
    goal: str,
    input_text: str,
    linked_task: dict | None,
    limit: int = 5,
) -> list[dict]:
    sessions_dir = project_path / "sessions"
    if not sessions_dir.is_dir():
        return []
    current_name = session_path.name
    related: list[dict] = []
    seen: set[str] = {current_name}

    if linked_task:
        linked_session = str(linked_task.get("session") or "")
        if linked_session.startswith("session."):
            seen.add(linked_session.removeprefix("session."))

    for child in sorted(sessions_dir.iterdir(), reverse=True):
        if not child.is_dir() or child.name in seen:
            continue
        if not (child / "instance.yaml").is_file():
            continue
        meta = load_yaml_file(child / "instance.yaml")
        meta["_path"] = child
        if text_matches_goal(goal, input_text, meta, child):
            related.append(meta)
            if len(related) >= limit:
                break
    return related


def compile_task_body(task: dict) -> str:
    parts = [
        f"**id:** {task.get('id', '*(unknown)*')} | **status:** {task.get('status', '*(unset)*')}",
        "",
        load_yaml_block(task["_path"] / "instance.yaml"),
    ]
    for filename in TASK_DOCS:
        fpath = task["_path"] / filename
        if fpath.is_file():
            parts.append(load_md_block(fpath, f"{task.get('id', task['_path'].name)} — {filename}"))
    return "\n".join(parts)


def compile_task_section(title: str, tasks: list[dict], empty_msg: str) -> str:
    if not tasks:
        return empty_msg + "\n"
    parts = []
    for task in tasks:
        parts.append(f"### {task.get('id') or task['_path'].name}\n")
        parts.append(compile_task_body(task))
    return "\n".join(parts)


def compile_related_sessions(sessions: list[dict]) -> str:
    if not sessions:
        return "*No related sessions matched the goal.*\n"
    lines = ["| session | goal | status |", "|---------|------|--------|"]
    for s in sessions:
        lines.append(
            f"| {s['_path'].name} | {str(s.get('goal', '')).replace('|', '/')} | {s.get('status', '—')} |"
        )
    parts = ["\n".join(lines) + "\n"]
    for s in sessions[:3]:
        trace = s["_path"] / "trace.md"
        output = s["_path"] / "output.md"
        if trace.is_file():
            parts.append(load_md_block(trace, f"Prior session {s['_path'].name} — trace.md (excerpt)"))
        elif output.is_file():
            parts.append(load_md_block(output, f"Prior session {s['_path'].name} — output.md (excerpt)"))
    return "\n".join(parts)


def iter_project_fields(project_instance: dict) -> list[tuple[str, dict]]:
    fields = project_instance.get("fields") or {}
    items: list[tuple[str, dict]] = []
    if isinstance(fields, dict):
        for name, spec in fields.items():
            if isinstance(spec, dict):
                items.append((name, spec))
            elif isinstance(spec, list):
                for entry in spec:
                    if isinstance(entry, dict):
                        items.append((name, entry))
    return items


def normalize_type_name(ref: str) -> str | None:
    ref = str(ref).strip()
    if ref.startswith("type."):
        return ref.split(".", 1)[1]
    return ref or None


def collect_scoped_type_names(
    project_instance: dict,
    session: dict,
    invoked: list[dict],
    linked_task: dict | None,
) -> set[str]:
    names = set(CORE_TYPE_NAMES)
    for _, spec in iter_project_fields(project_instance):
        for key in ("type", "content_type"):
            if key in spec:
                normalized = normalize_type_name(str(spec[key]))
                if normalized:
                    names.add(normalized)
    names.add(normalize_type_name(str(session.get("type") or "session")) or "session")
    for wf in invoked:
        if wf.get("operates_on"):
            normalized = normalize_type_name(str(wf["operates_on"]))
            if normalized:
                names.add(normalized)
    if linked_task:
        names.add("task")
        names.add("document")
    return names


def compile_scoped_types(type_names: set[str]) -> str:
    registry_names = set(all_registry_type_names())
    parts = []
    for name in sorted(type_names):
        if name not in registry_names:
            continue
        for yaml_path in type_yaml_paths(name):
            parts.append(load_yaml_block(yaml_path))
        for readme_path in type_readme_paths(name):
            rel = readme_path.relative_to(repo_root()).as_posix()
            parts.append(load_md_block(readme_path, f"{rel} — Agent protocol"))
    if not parts:
        return "*No scoped types resolved.*\n"
    return "\n".join(parts)


def compile_personal_preferences(principal: Path) -> str:
    prefs_root = principal / "personal" / "preferences"
    if not prefs_root.is_dir():
        return "*No preferences found.*\n"
    parts = []
    instance = prefs_root / "instance.yaml"
    if instance.is_file():
        parts.append(load_yaml_block(instance))
    for pref_dir in sorted(prefs_root.iterdir()):
        if not pref_dir.is_dir():
            continue
        pref_instance = pref_dir / "instance.yaml"
        if pref_instance.is_file():
            parts.append(load_yaml_block(pref_instance))
        for md_file in sorted(pref_dir.glob("*.md")):
            parts.append(load_md_block(md_file, f"Preference: {pref_dir.name}/{md_file.name}"))
    return "\n".join(parts) if parts else "*No preferences found.*\n"


def compile_grown_project_fields(
    project_path: Path,
    project_instance: dict,
    goal: str,
    input_text: str,
) -> str:
    parts = []
    for field_name, spec in iter_project_fields(project_instance):
        storage = str(spec.get("storage") or "").strip()
        if not storage or field_name in SKIP_FIELD_DIRS:
            continue
        if storage.endswith(".md"):
            continue
        path = project_path / storage
        if not path.is_dir():
            continue
        parts.append(f"### Project field: `{field_name}` (`{storage}`)\n")
        instance = path / "instance.yaml"
        if instance.is_file():
            parts.append(load_yaml_block(instance))
        for catalog_name in ("index.md", "README.md"):
            catalog = path / catalog_name
            if catalog.is_file():
                parts.append(load_md_block(catalog, f"{field_name}/{catalog_name}"))
        content_files = sorted(
            f for f in path.rglob("*")
            if f.is_file() and f.suffix in CONTENT_EXTENSIONS
            and f.name not in ("index.md", "README.md", "instance.yaml")
        )
        matched = [f for f in content_files if text_matches_goal(goal, input_text, {"name": f.stem}, f)]
        if not matched and field_name == "design":
            matched = content_files[:5]
        elif not matched:
            matched = content_files[:3]
        for fpath in matched:
            if fpath.suffix == ".md":
                parts.append(load_md_block(fpath))
            elif fpath.suffix in (".yaml", ".yml"):
                parts.append(load_yaml_block(fpath))
    return "\n".join(parts) if parts else "*No additional grown project fields matched the goal.*\n"


def format_workflow_meta(wf: dict) -> str:
    parts = [
        f"**id:** {wf.get('id', '*(unknown)*')}",
        f"**scope:** {wf.get('scope', '*(unset)*')}",
    ]
    if wf.get("operates_on"):
        parts.append(f"**operates_on:** {wf['operates_on']}")
    if wf.get("project"):
        parts.append(f"**project:** {wf['project']}")
    if wf.get("status"):
        parts.append(f"**status:** {wf['status']}")
    return " | ".join(parts)


def compile_workflow_body(wf: dict) -> str:
    parts = [format_workflow_meta(wf), ""]
    parts.append(load_yaml_block(wf["_path"] / "instance.yaml"))
    for filename in WORKFLOW_DOCS:
        fpath = wf["_path"] / filename
        if fpath.is_file():
            parts.append(load_md_block(fpath, f"{wf.get('id', wf['_path'].name)} — {filename}"))
    return "\n".join(parts)


def compile_resolved_workflows(invoked: list[dict]) -> str:
    if not invoked:
        return "*No workflow invoked. Set `workflow_id`, `workflow`, or `target_type` in session instance.yaml.*\n"
    parts = []
    for wf in invoked:
        title = wf.get("id") or wf["_path"].name
        parts.append(f"### Invoked: {title}\n")
        parts.append(compile_workflow_body(wf))
    return "\n".join(parts)


def compile_available_workflows(available: list[dict]) -> str:
    if not available:
        return "*No additional active workflows.*\n"
    lines = ["| id | scope | operates_on | summary |", "|----|-------|-------------|---------|"]
    for wf in available:
        lines.append(
            f"| {wf.get('id', '')} | {wf.get('scope', '')} | {wf.get('operates_on', '—')} | {workflow_summary(wf)} |"
        )
    return "\n".join(lines) + "\n"


def parse_session(session_path: Path) -> tuple[Path, Path, str, dict]:
    root = repo_root()
    session_path = session_path.resolve()
    if not session_path.is_dir():
        raise FileNotFoundError(f"Session not found: {session_path}")

    session = load_yaml_file(session_path / "instance.yaml")
    goal = str(session.get("goal") or "")
    main_instance = str(session.get("main_instance") or "")
    project_path = root / main_instance if main_instance else session_path.parent.parent
    if not (project_path / "instance.yaml").is_file():
        fallback = session_path.parent.parent
        if (fallback / "instance.yaml").is_file():
            project_path = fallback
    return session_path, project_path, goal, session


def compile_session_start_bundle(
    principal: Path,
    project_path: Path,
    goal: str,
    session: dict,
) -> str:
    all_rules = load_rules(principal, project_path)
    matched = resolve_bundle(
        all_rules,
        trigger="session_start",
        goal=goal,
        project_id=project_id_from_path(project_path),
        workflow_id=str(session.get("workflow_id") or ""),
    )
    return format_rule_bundle(matched)


def compile_directory_boundaries(principal: Path, project_path: Path) -> str:
    parts = []
    containers = [
        (principal / "knowledge-base", "Knowledge base"),
        (principal / "personal" / "sources", "Personal — sources/"),
        (principal / "personal" / "rules", "Personal — rules/"),
        (principal / "personal" / "preferences", "Personal — preferences/"),
        (principal / "personal" / "documents", "Personal — documents/"),
        (principal / "personal" / "workflows", "Personal — workflows/"),
        (project_path / "sources", f"{project_path.name} — sources/"),
        (project_path / "rules", f"{project_path.name} — rules/"),
        (project_path / "workflows", f"{project_path.name} — workflows/"),
        (project_path / "sessions", f"{project_path.name} — sessions/"),
        (project_path / "tasks", f"{project_path.name} — tasks/"),
    ]
    for path, heading in containers:
        instance = path / "instance.yaml"
        if not instance.is_file():
            continue
        parts.append(f"### {heading}\n")
        parts.append(load_yaml_block(instance))
        if path.name == "knowledge-base":
            for name in ("topics.yaml", "index.yaml"):
                f = path / name
                if f.is_file():
                    parts.append(load_yaml_block(f))
        if path.name in ("sources", "workflows", "tasks"):
            index = path / "index.md"
            if index.is_file():
                parts.append(load_md_block(index, f"{heading} index.md"))
    return "\n".join(parts) if parts else "*No directory containers with instance.yaml found.*\n"


def compile_matched_knowledge(
    principal: Path, goal: str, input_md: str, project_name: str
) -> str:
    if match_entries is None or knowledge_base_dir is None:
        return "*Knowledge scripts not installed.*\n"
    kb = knowledge_base_dir()
    if not kb.is_dir():
        return "*No knowledge-base/ found for this principal.*\n"
    entries = match_entries(goal, input_md, project_name=project_name, limit=8)
    if not entries:
        return "*No knowledge entries matched the session goal.*\n"
    parts = []
    for entry in entries:
        eid = entry.get("id", "?")
        topic = entry.get("topic", "?")
        summary = entry.get("summary", "")
        audit = entry.get("audit", "unaudited")
        maturity = entry.get("maturity", "tentative")
        applies = entry.get("applies_to") or []
        parts.append(f"### `{eid}`")
        parts.append(f"- **topic:** `{topic}`")
        parts.append(f"- **audit:** {audit} | **maturity:** {maturity}")
        parts.append(f"- **summary:** {summary}")
        if applies:
            parts.append(f"- **applies_to:** {', '.join(str(a) for a in applies)}")
        parts.append("")
    parts.append(
        "Resolve full entry: "
        f"`python3 system/engines/cli.py resolve-knowledge <id>`"
    )
    return "\n".join(parts) + "\n"


def compile_connectors(principal: Path) -> str:
    connectors_dir = principal / "connectors"
    if not connectors_dir.is_dir():
        return "*No connectors configured for this principal.*\n"
    parts = [
        "Read connector docs before external service calls. MCP config is per-agent; these docs are canonical.",
        "",
        load_md_block(agent_dir() / "connectors.md", "Connector Protocol"),
    ]
    index = connectors_dir / "README.md"
    if index.is_file():
        parts.append(load_md_block(index, "Connectors Index"))
    else:
        parts.append("*Missing connectors index: `users/<id>/connectors/README.md`*\n")
    return "\n".join(parts)


def compile_operation_preamble(project_path: Path, goal: str) -> str:
    project_name = project_path.name
    goal_line = goal.strip() if goal.strip() else "(see Session Goal below)"
    return f"""## Operation Checklist (read first — do not skip)

**Default model:** Orient → Plan → Act → Capture. **No implementation writes until Orient and Plan are complete.**

### 1. Orient (mandatory before writes)

- Read **Constitution** and this compiled context — Agent Protocol, project instance, grown fields, matched knowledge.
- Run **scope expansion** for project `{project_name}` (`system/agent/discovery_protocol.md` § Scope expansion).
- Resolve types for every instance you will touch (`system/agent/type_system.md`).
- For type-system work (create, register, patch, design types or typed instances): survey full registry (`list-types`); log `## Type coherence review` in `trace.md` before writes.

### 2. Plan (mandatory before implementation)

Write **Session plan** in `trace.md` before any implementation write:

| Item | Path or note |
|------|----------------|
| Goal | {goal_line} |
| Files to read | (from scope expansion — design/, knowledge-base/, types/, …) |
| Files likely to update | (stable targets this session may touch) |
| Open questions | |

The plan defines what **relevant** means. Do not limit scope to the first path named in the user message or task list.

### 3. Act

Execute against the plan. Session folder = L2 (write freely). Principal updates = L3 when plan and capture agree — log in `trace.md`.

Before principal writes or scope shifts: `resolve-rules --trigger pre_write` or `topic_shift`; attest in `trace.md` (`discovery_protocol.md` § Rule checkpoints).

### 4. Capture (session end)

Diff plan vs outcome in `evaluation.md`. Update stable targets the plan identified. Complete discovery log and reference checklist.

---

"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile session context for Jah.")
    parser.add_argument("session_path", help="e.g. users/katakuchi/projects/jah/sessions/YYYY-MM-DD-001")
    args = parser.parse_args()

    root = repo_root()
    principal = principal_root()
    session_path = root / args.session_path

    try:
        session_path, project_path, goal, session = parse_session(session_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    input_md = read_text(session_path / "input.md")
    if input_md.startswith("*(missing"):
        input_md = ""

    project_instance = load_yaml_file(project_path / "instance.yaml")
    invoked, available = resolve_workflows(
        principal, session_path, project_path, goal, session, input_md
    )
    linked_task = resolve_linked_task(project_path, session_path, session)
    related_tasks = resolve_related_tasks(project_path, goal, input_md, linked_task)
    related_sessions = resolve_related_sessions(
        project_path, session_path, goal, input_md, linked_task
    )
    scoped_types = collect_scoped_type_names(project_instance, session, invoked, linked_task)

    pid = active_principal()

    sections = [
        "# Compiled Context",
        "",
        "## Session Goal",
        "",
        goal or "*(no goal in instance.yaml)*",
        "",
        compile_operation_preamble(project_path, goal),
        "## Constitution",
        "",
        load_md_block(agent_dir() / "constitution.md", "Constitution"),
        "## Agent Protocol",
        "",
        load_md_block(agent_dir() / "discovery_protocol.md", "Discovery Protocol"),
        load_md_block(agent_dir() / "knowledge_base.md", "Knowledge Base"),
        load_md_block(agent_dir() / "proactive_capture.md", "Proactive Capture"),
        load_md_block(agent_dir() / "open_structure.md", "Open Structure"),
        load_md_block(agent_dir() / "connectors.md", "Connectors"),
        "## System Principles",
        "",
        load_md_block(agent_dir() / "glossary.md", "Glossary"),
        load_md_block(agent_dir() / "protocol.md", "Protocol"),
        load_md_block(agent_dir() / "type_system.md", "Type System"),
        "## Scoped Types",
        "",
        "Types in scope for this session (not the full registry). Read each README before working with that type.",
        "",
        compile_scoped_types(scoped_types),
        "## Personal Profile",
        "",
        load_md_block(principal / "personal/profile.md", "Personal Profile"),
        "## Personal Preferences",
        "",
        compile_personal_preferences(principal),
        "## Rule Index",
        "",
        "Metadata for all active rules. Resolve bodies on demand — see Constitution C7.",
        "",
        format_rule_index_table(load_rules(principal, project_path)),
        "## Session-start Rules",
        "",
        "Rules matching `session_start` for this goal. Resolve others on demand — see Rule Index.",
        "",
        compile_session_start_bundle(principal, project_path, goal, session),
        "## Project Context",
        "",
        load_md_block(project_path / "context.md", project_path.name),
        "## Project Instance",
        "",
        load_yaml_block(project_path / "instance.yaml"),
        "## Grown Project Fields",
        "",
        compile_grown_project_fields(project_path, project_instance, goal, input_md),
        "## Linked Task",
        "",
        compile_task_section(
            "Linked Task",
            [linked_task] if linked_task else [],
            "*No task linked. Set `task_id` on the session or `session` on the task instance.*",
        ),
        "## Related Tasks",
        "",
        compile_task_section(
            "Related Tasks",
            related_tasks,
            "*No additional tasks matched the goal.*",
        ),
        "## Related Sessions",
        "",
        compile_related_sessions(related_sessions),
        "## Matched Knowledge",
        "",
        compile_matched_knowledge(principal, goal, input_md, project_path.name),
        "## Directory Boundaries",
        "",
        f"Active principal: `{pid}`. Read each container's `instance.yaml` before writing.",
        "",
        compile_directory_boundaries(principal, project_path),
        "## Principal Connectors",
        "",
        compile_connectors(principal),
        "## Resolved Workflows",
        "",
        compile_resolved_workflows(invoked),
        "## Available Workflows",
        "",
        compile_available_workflows(available),
        "## Session Input",
        "",
        input_md.strip(),
        "",
        "## Required Output Files",
        "",
        "- `output.md` — task deliverable; include **References** (internal paths + external URLs)",
        "- `evaluation.md` — requirements, rules, **References consulted**, **Stable updates applied/offered**, **Open questions**",
        "- `trace.md` — what happened; include **Discovery log** and **References**",
        "- `patch.md` — profile, new registry types, and system proposals only (see Approval Boundaries)",
        "",
        "## Approval Boundaries",
        "",
        "**Session folder (L2):** write freely inside this session.",
        "",
        "**Principal (L3):** agents may update existing principal instances and type definitions without asking.",
        "Record changes in `trace.md`. Profile and new registry entries require explicit approval.",
        "Includes `knowledge-base/` entries and index.",
        "",
        "**System (L5):** changes to `system/` require explicit user request and a GitHub PR.",
        "",
        "**External (L6–L7):** external services, publish, send — explicit approval only.",
    ]

    output = "\n".join(sections) + "\n"
    out_path = session_path / "compiled_context.md"
    out_path.write_text(output, encoding="utf-8")
    print(out_path.relative_to(root).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
