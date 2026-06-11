#!/usr/bin/env python3
"""Validate structural parity — baseline fields, grown fields, disk layout."""

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
    type_dir,
)

CONTAINER_TYPES = frozenset({"project", "personal", "principal", "type_package"})


def load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def merged_baseline_fields(type_name: str, principal: str, registry: dict) -> dict:
    """Merge container baseline fields from type extends chain."""
    key = resolve_type_key(type_name, registry)
    merged: dict = {}
    for chain_key in extends_chain(key, principal):
        tdir = type_dir(chain_key, principal)
        if not tdir:
            continue
        data = load_yaml(tdir / "type.yaml")
        baseline = data.get("fields")
        if isinstance(baseline, dict):
            merged.update(baseline)
    return merged


def is_container_type(type_name: str, principal: str, registry: dict) -> bool:
    if type_name in CONTAINER_TYPES:
        return True
    key = resolve_type_key(type_name, registry)
    tdir = type_dir(key, principal)
    if not tdir:
        return False
    data = load_yaml(tdir / "type.yaml")
    return data.get("role") == "container"


def instance_field_keys(fields: object) -> set[str]:
    if not isinstance(fields, dict):
        return set()
    return set(fields.keys())


def field_storage(field: object) -> str | None:
    if isinstance(field, dict):
        storage = field.get("storage")
        return str(storage) if storage else None
    if isinstance(field, list) and field:
        first = field[0]
        if isinstance(first, dict):
            storage = first.get("storage")
            return str(storage) if storage else None
    return None


def field_type_name(field: object) -> str | None:
    if isinstance(field, dict):
        t = field.get("type")
        return str(t) if t else None
    if isinstance(field, list) and field:
        first = field[0]
        if isinstance(first, dict):
            t = first.get("type")
            return str(t) if t else None
    return None


def field_content_type(field: object) -> str | None:
    if isinstance(field, dict):
        ct = field.get("content_type")
        return str(ct) if ct else None
    return None


def top_level_name(storage: str) -> str:
    return storage.rstrip("/").split("/")[0]


def declared_roots(instance_fields: dict) -> set[str]:
    roots: set[str] = set()
    for _name, spec in instance_fields.items():
        storage = field_storage(spec)
        if storage:
            roots.add(top_level_name(storage))
    return roots


def resolve_field_type(type_name: str, registry: dict) -> bool:
    if type_name in ("scalar", "document"):
        return True
    key = resolve_type_key(type_name.replace("type.", ""), registry)
    types = registry.get("types") or {}
    return key in types


def validate_container_instance(
    instance_path: Path,
    root: Path,
    principal: str,
    registry: dict,
    issues: list[str],
) -> None:
    meta = load_yaml(instance_path)
    type_name = meta.get("type")
    if not type_name or not is_container_type(str(type_name), principal, registry):
        return

    rel = instance_path.relative_to(root)
    instance_fields = meta.get("fields") or {}
    if not isinstance(instance_fields, dict):
        issues.append(f"WARN: {rel} fields block is not a mapping")
        return

    baseline = merged_baseline_fields(str(type_name), principal, registry)
    present = instance_field_keys(instance_fields)

    for bname, bspec in baseline.items():
        if not isinstance(bspec, dict):
            continue
        if bspec.get("optional"):
            continue
        if bname not in present:
            issues.append(f"WARN: {rel} missing required baseline field '{bname}'")

    for fname, fspec in instance_fields.items():
        if fname in baseline:
            continue
        tname = field_type_name(fspec)
        if tname and not resolve_field_type(tname, registry):
            issues.append(f"WARN: {rel} grown field '{fname}' has unknown type '{tname}'")

    container_dir = instance_path.parent
    for fname, fspec in instance_fields.items():
        storage = field_storage(fspec)
        if not storage:
            continue
        target = container_dir / storage
        if not target.exists():
            issues.append(f"WARN: {rel} field '{fname}' storage missing: {storage}")

        ftype = field_type_name(fspec)
        ct = field_content_type(fspec)
        if ftype in ("directory", "type.directory") or ct:
            if storage.endswith("/"):
                dir_instance = container_dir / storage / "instance.yaml"
                if not dir_instance.is_file():
                    issues.append(
                        f"WARN: {rel} directory field '{fname}' missing instance.yaml at {storage}"
                    )
                else:
                    dir_meta = load_yaml(dir_instance)
                    declared_ct = ct or field_content_type(
                        baseline.get(fname) if isinstance(baseline.get(fname), dict) else {}
                    )
                    actual_ct = dir_meta.get("content_type")
                    if declared_ct and actual_ct and str(declared_ct) != str(actual_ct):
                        issues.append(
                            f"WARN: {rel} field '{fname}' content_type mismatch: "
                            f"parent={declared_ct} dir={actual_ct}"
                        )

    declared = declared_roots(instance_fields)
    if container_dir.is_dir():
        for entry in container_dir.iterdir():
            if entry.name.startswith("."):
                continue
            if entry.name == "instance.yaml":
                continue
            if entry.name not in declared:
                if type_name == "project" and entry.name in declared:
                    continue
                issues.append(
                    f"WARN: {rel} orphan at root: '{entry.name}' not declared in fields"
                )


def main() -> int:
    principal = active_principal()
    root = principal_root(principal)
    registry = load_registry(principal)
    issues: list[str] = []

    for instance_path in sorted(root.rglob("instance.yaml")):
        validate_container_instance(instance_path, root, principal, registry, issues)

    for msg in issues:
        print(msg)

    if issues:
        print(f"\n{len(issues)} issue(s) found.")
        return 1
    print("Structural validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
