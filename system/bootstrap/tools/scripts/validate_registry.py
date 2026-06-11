#!/usr/bin/env python3
"""Validate principal registry and instance type references. Warn-only."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from jah_env import (
    active_principal,
    extends_chain,
    load_registry,
    principal_root,
    resolve_type_key,
)


def load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def main() -> int:
    principal = active_principal()
    root = principal_root(principal)
    registry = load_registry(principal)
    types = registry.get("types") or {}
    issues = 0

    for key, entry in types.items():
        if not isinstance(entry, dict):
            print(f"WARN: invalid registry entry for {key}")
            issues += 1
            continue
        path = entry.get("path")
        if not path:
            print(f"WARN: {key} missing path")
            issues += 1
            continue
        type_yaml = root / str(path) / "type.yaml"
        if not type_yaml.is_file():
            print(f"WARN: missing type.yaml for {key}: {type_yaml}")
            issues += 1
        parent = entry.get("extends")
        if parent and parent not in types:
            print(f"WARN: {key} extends unknown type: {parent}")
            issues += 1

    for key in types:
        try:
            chain = extends_chain(key, principal)
            if len(chain) != len(set(chain)):
                print(f"WARN: circular extends chain for {key}")
                issues += 1
        except Exception as exc:
            print(f"WARN: extends chain error for {key}: {exc}")
            issues += 1

    for instance_path in sorted(root.rglob("instance.yaml")):
        meta = load_yaml(instance_path)
        type_name = meta.get("type")
        if not type_name:
            continue
        resolved = resolve_type_key(str(type_name), registry)
        if resolved not in types:
            print(f"WARN: unknown type '{type_name}' in {instance_path.relative_to(root)}")
            issues += 1

    if issues:
        print(f"\n{issues} issue(s) found.")
        return 1
    print("Registry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
