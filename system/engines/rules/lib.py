"""Load and resolve Jah principal rules."""

from __future__ import annotations

from pathlib import Path

import yaml

DEFAULT_PRIORITY = 100
DEFAULT_TRIGGERS = ["session_start"]
VALID_TRIGGERS = frozenset({"session_start", "pre_write", "topic_shift", "pre_approval"})


def load_yaml_file(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _iter_rule_files(rules_root: Path) -> list[Path]:
    if not rules_root.is_dir():
        return []
    return sorted(
        path
        for path in rules_root.rglob("*")
        if path.is_file()
        and path.suffix in (".yaml", ".yml")
        and path.name != "instance.yaml"
    )


def load_rules(principal: Path, project_path: Path) -> list[dict]:
    """Scan personal and project rules/ trees; return rule dicts with _path."""
    rules: list[dict] = []
    for rules_root in (principal / "personal" / "rules", project_path / "rules"):
        for rule_file in _iter_rule_files(rules_root):
            data = load_yaml_file(rule_file)
            if data.get("type") != "rule":
                continue
            data["_path"] = rule_file
            rules.append(data)
    return rules


def activation_triggers(rule: dict) -> list[str]:
    raw = rule.get("activation_trigger")
    if not raw:
        return list(DEFAULT_TRIGGERS)
    if isinstance(raw, str):
        raw = [raw]
    return [str(t) for t in raw if str(t) in VALID_TRIGGERS] or list(DEFAULT_TRIGGERS)


def rule_priority(rule: dict) -> int:
    value = rule.get("priority")
    if value is None:
        return DEFAULT_PRIORITY
    try:
        return int(value)
    except (TypeError, ValueError):
        return DEFAULT_PRIORITY


def project_id_from_path(project_path: Path) -> str:
    return f"project.{project_path.name.replace('-', '_')}"


def match_applies_to(
    rule: dict,
    *,
    goal: str = "",
    project_id: str = "",
    workflow_id: str = "",
    target: str = "",
) -> bool:
    """Return True if rule applies to current context. Empty applies_to matches all."""
    applies_to = rule.get("applies_to") or []
    if not applies_to:
        return True

    haystack = " ".join(
        [
            goal.lower(),
            project_id.lower(),
            workflow_id.lower(),
            target.lower().replace("/", " ").replace("-", " "),
        ]
    )
    candidates = {project_id, workflow_id, "session", target}
    for item in applies_to:
        item_str = str(item)
        if item_str in candidates:
            return True
        if item_str.lower() in haystack:
            return True
        # path fragment match (e.g. connectors ref in target path)
        if target and item_str.replace(".", "/") in target.replace("-", "_"):
            return True
    return False


def rule_index_entry(rule: dict) -> dict:
    """Metadata only — no rule body."""
    return {
        "id": rule.get("id", ""),
        "name": rule.get("name", ""),
        "priority": rule_priority(rule),
        "applies_to": rule.get("applies_to") or [],
        "activation_trigger": activation_triggers(rule),
        "status": rule.get("status", "active"),
        "scope": rule.get("scope", ""),
    }


def active_rules(rules: list[dict]) -> list[dict]:
    return [r for r in rules if str(r.get("status", "active")) == "active"]


def filter_by_trigger(rules: list[dict], trigger: str) -> list[dict]:
    return [r for r in rules if trigger in activation_triggers(r)]


def resolve_bundle(
    rules: list[dict],
    *,
    trigger: str,
    goal: str = "",
    project_id: str = "",
    workflow_id: str = "",
    target: str = "",
) -> list[dict]:
    """Return ordered active rules matching trigger and applies_to."""
    matched = []
    for rule in active_rules(rules):
        if trigger not in activation_triggers(rule):
            continue
        if not match_applies_to(
            rule,
            goal=goal,
            project_id=project_id,
            workflow_id=workflow_id,
            target=target,
        ):
            continue
        matched.append(rule)
    matched.sort(key=rule_priority)
    return matched


def format_rule_index_table(rules: list[dict]) -> str:
    entries = [rule_index_entry(r) for r in active_rules(rules)]
    entries.sort(key=lambda e: (e["priority"], e["id"]))
    if not entries:
        return "*No active rules found.*\n"

    lines = [
        "| id | priority | applies_to | activation_trigger |",
        "|----|----------|------------|-------------------|",
    ]
    for entry in entries:
        applies = ", ".join(str(a) for a in entry["applies_to"]) or "—"
        triggers = ", ".join(entry["activation_trigger"])
        lines.append(
            f"| {entry['id']} | {entry['priority']} | {applies} | {triggers} |"
        )
    lines.append("")
    lines.append(
        "Resolve rule bodies: "
        "`python3 system/engines/cli.py resolve-rules <session-path> --trigger <trigger>`"
    )
    return "\n".join(lines) + "\n"


def format_rule_bundle(rules: list[dict]) -> str:
    if not rules:
        return "*No rules matched this trigger and context.*\n"
    parts = []
    for rule in rules:
        rid = rule.get("id", "?")
        parts.append(f"### `{rid}` (priority {rule_priority(rule)})\n")
        parts.append(f"**{rule.get('name', rid)}**\n")
        parts.append(str(rule.get("rule", "")).strip())
        parts.append("")
    return "\n".join(parts) + "\n"
