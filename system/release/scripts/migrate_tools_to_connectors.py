#!/usr/bin/env python3
"""Rename principal tools/ field and folder to connectors/."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def patch_yaml_field(path: Path, dry_run: bool) -> bool:
    if not path.is_file():
        return False
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return False
    fields = data.get("fields")
    if not isinstance(fields, dict) or "tools" not in fields:
        return False
    connectors_field = fields.pop("tools")
    if isinstance(connectors_field, dict):
        connectors_field["storage"] = "connectors/"
    fields["connectors"] = connectors_field
    data["fields"] = fields
    if isinstance(data.get("description"), str):
        data["description"] = (
            data["description"]
            .replace("and tools.", "and connectors.")
            .replace("optional integrations", "optional connectors")
        )
    if dry_run:
        return True
    path.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return True


def patch_principal_type_yaml(path: Path, dry_run: bool) -> bool:
    if not path.is_file():
        return False
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return False
    fields = data.get("fields")
    if not isinstance(fields, dict) or "tools" not in fields:
        return False
    connectors_field = fields.pop("tools")
    if isinstance(connectors_field, dict):
        connectors_field["storage"] = "connectors/"
        desc = connectors_field.get("description")
        if isinstance(desc, str):
            connectors_field["description"] = (
                "Optional connectors — external services, devices, MCP configs, "
                "and personal automations (not Jah protocol code)."
            )
    fields["connectors"] = connectors_field
    data["fields"] = fields
    if isinstance(data.get("description"), str):
        data["description"] = (
            data["description"]
            .replace("optional integrations", "optional connectors")
            .replace("and tools.", "and connectors.")
        )
    if dry_run:
        return True
    path.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return True


def patch_readme(path: Path, dry_run: bool) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    replacements = [
        ("  tools/              # optional — MCP configs and personal integrations", "  connectors/         # optional — external services, devices, MCP configs"),
        ("  tools/              # optional — integrations only (MCP, custom glue)", "  connectors/         # optional — external services, devices, MCP, custom glue"),
        ("principal `tools/`", "principal `connectors/`"),
        ("not from principal `tools/`", "not from principal `connectors/`"),
        ("not from principal tools/", "not from principal connectors/"),
    ]
    new_text = text
    for old, new in replacements:
        new_text = new_text.replace(old, new)
    if new_text == text:
        return False
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def migrate_principal(principal_dir: Path, dry_run: bool) -> list[str]:
    changes: list[str] = []
    tools_dir = principal_dir / "tools"
    connectors_dir = principal_dir / "connectors"

    if tools_dir.is_dir():
        if connectors_dir.exists():
            changes.append(f"ERROR: both tools/ and connectors/ exist under {principal_dir.name}")
            return changes
        changes.append(f"Rename {tools_dir.relative_to(principal_dir.parent.parent)} -> connectors/")
        if not dry_run:
            tools_dir.rename(connectors_dir)

    instance_yaml = principal_dir / "instance.yaml"
    if patch_yaml_field(instance_yaml, dry_run):
        changes.append(f"Update {instance_yaml.relative_to(principal_dir.parent.parent)}")

    type_yaml = principal_dir / "types" / "principal" / "type.yaml"
    if patch_principal_type_yaml(type_yaml, dry_run):
        changes.append(f"Update {type_yaml.relative_to(principal_dir.parent.parent)}")

    readme = principal_dir / "types" / "principal" / "README.md"
    if patch_readme(readme, dry_run):
        changes.append(f"Update {readme.relative_to(principal_dir.parent.parent)}")

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate principal tools/ to connectors/.")
    parser.add_argument("--principal", help="Migrate one principal id (default: all under users/)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = repo_root()
    users_dir = root / "users"
    if not users_dir.is_dir():
        print("No users/ directory found.", file=sys.stderr)
        return 1

    if args.principal:
        principal_dirs = [users_dir / args.principal.strip()]
    else:
        principal_dirs = sorted(p for p in users_dir.iterdir() if p.is_dir())

    any_changes = False
    for principal_dir in principal_dirs:
        if not principal_dir.is_dir():
            print(f"Principal not found: {principal_dir}", file=sys.stderr)
            return 1
        changes = migrate_principal(principal_dir, args.dry_run)
        if changes:
            any_changes = True
            prefix = "[dry-run] " if args.dry_run else ""
            print(f"{prefix}{principal_dir.name}:")
            for line in changes:
                print(f"  - {line}")

    if not any_changes:
        print("Nothing to migrate — no principal tools/ field or folder found.")
    elif args.dry_run:
        print("Dry run complete.")
    else:
        print("Migration complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
