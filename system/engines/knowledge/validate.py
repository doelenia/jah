#!/usr/bin/env python3
"""Validate knowledge-base index, entries, and topic assignments."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from env import repo_root

from knowledge.lib import (
    knowledge_base_dir,
    load_index,
    load_topics,
    parse_date,
    source_catalog_path,
    source_id_in_catalog,
    topic_ids_from_tree,
)


def main() -> int:
    kb = knowledge_base_dir()
    if not kb.is_dir():
        print(f"Error: knowledge-base not found: {kb}", file=sys.stderr)
        return 1

    topics_data = load_topics()
    valid_topics = topic_ids_from_tree(topics_data)
    aliases = topics_data.get("aliases") or {}
    for alias, canonical in aliases.items():
        if isinstance(canonical, str) and canonical in valid_topics:
            valid_topics.add(alias)

    index_data = load_index()
    entries_map = index_data.get("entries") or {}
    errors: list[str] = []
    warnings: list[str] = []
    seen_files: set[str] = set()
    today = date.today()

    for entry_id, row in entries_map.items():
        if not isinstance(row, dict):
            errors.append(f"index entry {entry_id}: invalid row")
            continue
        rel = row.get("path")
        if not rel:
            errors.append(f"index entry {entry_id}: missing path")
            continue
        path = kb / str(rel)
        if str(rel) in seen_files:
            errors.append(f"duplicate index path: {rel}")
        seen_files.add(str(rel))
        if not path.is_file():
            errors.append(f"index entry {entry_id}: missing file {rel}")
            continue
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            errors.append(f"{rel}: not a YAML mapping")
            continue
        file_id = data.get("id")
        if file_id and file_id != entry_id:
            errors.append(f"{rel}: id {file_id} != index key {entry_id}")
        topic = str(data.get("topic") or "")
        if not topic:
            errors.append(f"{entry_id}: missing topic")
        elif topic not in valid_topics:
            errors.append(f"{entry_id}: invalid topic {topic}")
        parts = topic.split(".")
        if topic and len(parts) > 2:
            errors.append(f"{entry_id}: topic depth > 2: {topic}")
        canonical = data.get("canonical_path")
        if canonical:
            full = repo_root() / str(canonical)
            if not full.is_file():
                errors.append(f"{entry_id}: canonical_path missing: {canonical}")
        grounded = data.get("grounded_in") or []
        if isinstance(grounded, list):
            for g in grounded:
                if not isinstance(g, dict):
                    continue
                sid = g.get("source_id")
                scope = g.get("scope")
                if sid and scope:
                    catalog = source_catalog_path(str(scope))
                    if catalog is None:
                        warnings.append(f"{entry_id}: no sources catalog for scope {scope}")
                    elif not source_id_in_catalog(catalog, str(sid)):
                        warnings.append(f"{entry_id}: source_id {sid} not in {catalog.relative_to(repo_root())}")
        audit = str(data.get("audit") or "unaudited")
        maturity = str(data.get("maturity") or "tentative")
        updated = parse_date(str(data.get("updated") or data.get("created") or ""))
        if audit == "unaudited" and maturity == "tentative" and updated:
            age = (today - updated).days
            if age > 90:
                warnings.append(f"{entry_id}: tentative/unaudited for {age} days — review or archive")

    entries_dir = kb / "entries"
    if entries_dir.is_dir():
        for path in sorted(entries_dir.rglob("*.yaml")):
            rel = path.relative_to(kb).as_posix()
            if rel not in seen_files:
                warnings.append(f"orphan entry file not in index: {rel}")

    if errors:
        print("Knowledge validation FAILED:")
        for e in errors:
            print(f"  ERROR: {e}")
    else:
        print("Knowledge validation OK")

    for w in warnings:
        print(f"  WARN: {w}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
