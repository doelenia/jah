#!/usr/bin/env python3
"""List registered types with extends chain and description — for type coherence review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from env import active_principal, load_registry, principal_root, type_dir


def load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def type_description(type_key: str, principal: str) -> str:
    tdir = type_dir(type_key, principal)
    if not tdir:
        return ""
    data = load_yaml(tdir / "type.yaml")
    desc = data.get("description") or data.get("id") or ""
    return str(desc).replace("\n", " ").strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List principal registry types (extends, path, description)."
    )
    parser.parse_args()

    principal = active_principal()
    root = principal_root(principal)
    registry = load_registry(principal)
    types = registry.get("types") or {}
    aliases = registry.get("aliases") or {}

    if not types:
        print("No types in registry.")
        return 0

    print(f"# Registry types — {principal}\n")
    print("| type | extends | path | description |")
    print("|------|---------|------|-------------|")
    for key in sorted(types):
        entry = types[key] if isinstance(types[key], dict) else {}
        extends = entry.get("extends")
        extends_str = str(extends) if extends else "—"
        path = entry.get("path") or ""
        rel = (root / path).relative_to(root).as_posix() if path else ""
        desc = type_description(key, principal) or entry.get("id", "")
        if len(desc) > 80:
            desc = desc[:77] + "..."
        print(f"| {key} | {extends_str} | {rel} | {desc} |")

    if aliases:
        print("\n## Aliases\n")
        print("| alias | resolves_to |")
        print("|-------|-------------|")
        for alias, target in sorted(aliases.items()):
            print(f"| {alias} | {target} |")

    print(f"\n{len(types)} type(s). Run validate-registry for structural checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
