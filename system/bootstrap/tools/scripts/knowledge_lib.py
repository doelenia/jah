#!/usr/bin/env python3
"""Shared knowledge-base loading and matching for Jah principal scripts."""

from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from jah_env import principal_root, repo_root


def knowledge_base_dir(principal: str | None = None) -> Path:
    return principal_root(principal) / "knowledge-base"


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_topics(principal: str | None = None) -> dict[str, Any]:
    return _load_yaml(knowledge_base_dir(principal) / "topics.yaml")


def load_index(principal: str | None = None) -> dict[str, Any]:
    return _load_yaml(knowledge_base_dir(principal) / "index.yaml")


def topic_ids_from_tree(topics_data: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    topics = topics_data.get("topics") or {}
    for domain, domain_meta in topics.items():
        if not isinstance(domain_meta, dict):
            continue
        children = domain_meta.get("children") or {}
        for field in children:
            result.add(f"{domain}.{field}")
    aliases = topics_data.get("aliases") or {}
    for alias, canonical in aliases.items():
        if isinstance(canonical, str):
            result.add(canonical)
            result.add(alias)
    return result


def resolve_topic_id(topic: str, topics_data: dict[str, Any] | None = None) -> str:
    data = topics_data or load_topics()
    aliases = data.get("aliases") or {}
    if topic in aliases:
        return str(aliases[topic])
    return topic


def entry_path_from_index(index_data: dict[str, Any], entry_id: str) -> Path | None:
    entries = index_data.get("entries") or {}
    row = entries.get(entry_id)
    if not isinstance(row, dict):
        return None
    rel = row.get("path")
    if not rel:
        return None
    return knowledge_base_dir() / str(rel)


def load_entry_by_id(entry_id: str, principal: str | None = None) -> dict[str, Any] | None:
    kb = knowledge_base_dir(principal)
    index_data = load_index(principal)
    path = entry_path_from_index(index_data, entry_id)
    if path is None:
        return None
    if not path.is_file():
        return None
    data = _load_yaml(path)
    data["_path"] = path
    return data


def iter_entries(principal: str | None = None) -> list[dict[str, Any]]:
    index_data = load_index(principal)
    entries_map = index_data.get("entries") or {}
    result: list[dict[str, Any]] = []
    for entry_id, row in entries_map.items():
        if not isinstance(row, dict):
            continue
        rel = row.get("path")
        if not rel:
            continue
        path = knowledge_base_dir(principal) / str(rel)
        if not path.is_file():
            result.append({"id": entry_id, "_path": path, "_missing": True})
            continue
        data = _load_yaml(path)
        data.setdefault("id", entry_id)
        data["_path"] = path
        result.append(data)
    return result


def goal_tokens(goal: str, input_text: str) -> set[str]:
    text = f"{goal} {input_text}".lower()
    return set(re.findall(r"[a-z0-9]{4,}", text))


def entry_matches_goal(
    entry: dict[str, Any],
    goal: str,
    input_text: str,
    project_name: str | None = None,
) -> bool:
    haystack = f"{goal} {input_text}".lower()
    needles = [
        str(entry.get("id") or "").lower(),
        str(entry.get("summary") or "").lower(),
        str(entry.get("topic") or "").lower().replace("_", " ").replace(".", " "),
    ]
    applies = entry.get("applies_to") or []
    if isinstance(applies, list):
        needles.extend(str(a).lower() for a in applies)
    if project_name:
        needles.append(project_name.lower())
    if any(n and n in haystack for n in needles if len(n) >= 4):
        return True
    tokens = goal_tokens(goal, input_text)
    blob = " ".join(needles)
    return any(t in blob for t in tokens if len(t) >= 5)


def match_entries(
    goal: str,
    input_text: str,
    project_name: str | None = None,
    principal: str | None = None,
    *,
    authoritative_only: bool = False,
    limit: int = 10,
) -> list[dict[str, Any]]:
    matched: list[dict[str, Any]] = []
    for entry in iter_entries(principal):
        if entry.get("_missing"):
            continue
        audit = str(entry.get("audit") or "unaudited")
        if authoritative_only and audit not in ("reviewed", "endorsed"):
            continue
        applies = entry.get("applies_to") or []
        project_hit = project_name and any(
            project_name.lower() in str(a).lower() for a in applies
        )
        if entry_matches_goal(entry, goal, input_text, project_name) or project_hit:
            matched.append(entry)
    matched.sort(
        key=lambda e: (
            0 if str(e.get("audit")) in ("reviewed", "endorsed") else 1,
            0 if str(e.get("maturity")) == "stable" else 1,
            str(e.get("id") or ""),
        )
    )
    return matched[:limit]


def find_by_topic(topic: str, principal: str | None = None) -> list[dict[str, Any]]:
    canonical = resolve_topic_id(topic, load_topics(principal))
    prefix = f"{canonical}."
    return [
        e
        for e in iter_entries(principal)
        if not e.get("_missing")
        and (
            str(e.get("topic") or "") == canonical
            or str(e.get("topic") or "").startswith(prefix)
        )
    ]


def find_by_applies_to(ref: str, principal: str | None = None) -> list[dict[str, Any]]:
    ref_lower = ref.lower()
    result = []
    for entry in iter_entries(principal):
        if entry.get("_missing"):
            continue
        applies = entry.get("applies_to") or []
        if not isinstance(applies, list):
            continue
        if any(ref_lower in str(a).lower() for a in applies):
            result.append(entry)
    return result


def find_by_source_id(source_id: str, principal: str | None = None) -> list[dict[str, Any]]:
    sid = source_id.lower()
    result = []
    for entry in iter_entries(principal):
        if entry.get("_missing"):
            continue
        grounded = entry.get("grounded_in") or []
        if not isinstance(grounded, list):
            continue
        for g in grounded:
            if isinstance(g, dict) and str(g.get("source_id") or "").lower() == sid:
                result.append(entry)
                break
    return result


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def source_catalog_path(scope: str, principal: str | None = None) -> Path | None:
    root = principal_root(principal)
    scope = scope.strip()
    if scope.startswith("project."):
        project = scope.split(".", 1)[1]
        return root / "projects" / project / "sources" / "index.md"
    if scope in ("personal", "personal.main"):
        return root / "personal" / "sources" / "index.md"
    if scope.startswith("users/"):
        p = repo_root() / scope / "sources" / "index.md"
        if p.is_file():
            return p
    project_path = root / "projects" / scope / "sources" / "index.md"
    if project_path.is_file():
        return project_path
    return None


def source_id_in_catalog(catalog_path: Path, source_id: str) -> bool:
    if not catalog_path.is_file():
        return False
    text = catalog_path.read_text(encoding="utf-8")
    return f"id: {source_id}" in text or f"id:{source_id}" in text
