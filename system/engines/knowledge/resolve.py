#!/usr/bin/env python3
"""Resolve knowledge entries by id, topic, applies_to, or source_id."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from env import repo_root

from knowledge.lib import (
    find_by_applies_to,
    find_by_source_id,
    find_by_topic,
    load_entry_by_id,
    resolve_topic_id,
)


def format_entry(entry: dict, show_path: bool = False) -> str:
    payload = {k: v for k, v in entry.items() if not str(k).startswith("_")}
    lines = [yaml.dump(payload, sort_keys=False, allow_unicode=True).strip()]
    if show_path:
        path = entry.get("_path")
        if path:
            rel = Path(path).relative_to(repo_root()).as_posix()
            canonical = entry.get("canonical_path")
            lines.append(f"canonical_path: {canonical}" if canonical else "")
            lines.append(f"entry_file: {rel}")
            if canonical:
                full = repo_root() / str(canonical)
                if full.is_file():
                    preview = full.read_text(encoding="utf-8")[:2000]
                    lines.append("\n--- canonical content (preview) ---\n")
                    lines.append(preview)
    return "\n".join(line for line in lines if line)


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve Jah knowledge entries.")
    parser.add_argument("entry_id", nargs="?", help="e.g. knowledge.concrete-observation-first")
    parser.add_argument("--topic", help="FORD topic domain.field")
    parser.add_argument("--applies-to", dest="applies_to", help="Context ref e.g. project.jah")
    parser.add_argument("--source-id", dest="source_id", help="Reverse lookup by source id")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--content", action="store_true", help="Include canonical file preview")
    args = parser.parse_args()

    if args.entry_id:
        entry = load_entry_by_id(args.entry_id)
        if not entry:
            print(f"Error: knowledge entry not found: {args.entry_id}", file=sys.stderr)
            return 1
        if args.json:
            payload = {k: v for k, v in entry.items() if not str(k).startswith("_")}
            print(json.dumps(payload, indent=2))
        else:
            print(format_entry(entry, show_path=args.content))
        return 0

    entries: list[dict] = []
    if args.topic:
        canonical = resolve_topic_id(args.topic)
        entries = find_by_topic(canonical)
    elif args.applies_to:
        entries = find_by_applies_to(args.applies_to)
    elif args.source_id:
        entries = find_by_source_id(args.source_id)
    else:
        parser.print_help()
        return 1

    if not entries:
        print("No matching knowledge entries.")
        return 0

    if args.json:
        payload = [{k: v for k, v in e.items() if not str(k).startswith("_")} for e in entries]
        print(json.dumps(payload, indent=2))
        return 0

    for entry in entries:
        print(format_entry(entry, show_path=args.content))
        print("---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
