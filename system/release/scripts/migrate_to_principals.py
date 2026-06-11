#!/usr/bin/env python3
"""One-time migration from legacy memory/types/tools to users/<principal>/."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml

DEFAULT_PRINCIPAL_ID = "katakuchi"


def path_replacements(principal_id: str) -> list[tuple[str, str]]:
    return [
        ("memory/personal/", f"users/{principal_id}/personal/"),
        ("memory/projects/", f"users/{principal_id}/projects/"),
        ("memory/", f"users/{principal_id}/"),
        ("types/", f"users/{principal_id}/types/"),
        ("tools/scripts/", f"users/{principal_id}/connectors/scripts/"),
        ("tools/", f"users/{principal_id}/connectors/"),
    ]

EXTENDS_MAP = {
    "base": None,
    "directory": "base",
    "document": "base",
    "context": "document",
    "profile": "document",
    "personal": "base",
    "principal": "base",
    "session": "base",
    "session_artifact": "document",
    "project": "base",
    "preference": "base",
    "rule": "base",
    "source": "base",
    "workflow": "base",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def rewrite_text(content: str, principal_id: str) -> str:
    if f"users/{principal_id}/" in content and "memory/" not in content:
        return content
    for old, new in path_replacements(principal_id):
        if old not in content:
            continue
        content = content.replace(old, new)
    content = content.replace("work_pattern", "workflow")
    content = content.replace("kernel", "system")
    content = content.replace("Kernel", "System")
    content = content.replace("modify stable memory", "modify stable principal instances")
    content = content.replace("Types vs memory", "Types vs instances")
    return content


def rewrite_tree(directory: Path, principal_id: str) -> None:
    if not directory.is_dir():
        return
    for path in directory.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix in (".md", ".yaml", ".yml", ".py", ".mdc") or path.name in ("CLAUDE.md",):
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            new_text = rewrite_text(text, principal_id)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")


def generate_registry(types_dir: Path, principal_id: str) -> dict:
    types: dict = {}
    for type_dir in sorted(types_dir.iterdir()):
        if not type_dir.is_dir() or type_dir.name == "work_pattern":
            continue
        name = type_dir.name
        type_yaml = type_dir / "type.yaml"
        extends = EXTENDS_MAP.get(name)
        if type_yaml.is_file():
            data = yaml.safe_load(type_yaml.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("extends"):
                ext = str(data["extends"]).replace("type.", "")
                extends = ext
        types[name] = {
            "id": f"type.{name}",
            "path": f"types/{name}",
            "extends": extends,
        }
    return {
        "id": f"registry.{principal_id}",
        "version": 1,
        "types": types,
        "aliases": {},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate legacy layout to principals.")
    parser.add_argument("--principal", default=DEFAULT_PRINCIPAL_ID)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    principal_id = args.principal

    root = repo_root()
    legacy_memory = root / "memory"
    legacy_types = root / "types"
    legacy_tools = root / "tools"

    if not legacy_memory.is_dir() and not legacy_types.is_dir():
        print("Nothing to migrate — legacy paths not found.")
        return 0

    principal_dir = root / "users" / principal_id
    if args.dry_run:
        print(f"Would migrate to {principal_dir}")
        return 0

    principal_dir.mkdir(parents=True, exist_ok=True)

    if legacy_types.is_dir():
        types_dst = principal_dir / "types"
        if types_dst.exists():
            shutil.rmtree(types_dst)
        shutil.copytree(
            legacy_types,
            types_dst,
            ignore=shutil.ignore_patterns("work_pattern"),
        )
        # Add principal type from bootstrap if missing
        bootstrap_principal = root / "system" / "bootstrap" / "types" / "principal"
        if bootstrap_principal.is_dir() and not (types_dst / "principal").exists():
            shutil.copytree(bootstrap_principal, types_dst / "principal")

    if legacy_memory.is_dir():
        personal_src = legacy_memory / "personal"
        projects_src = legacy_memory / "projects"
        if personal_src.is_dir():
            personal_dst = principal_dir / "personal"
            if personal_dst.exists():
                shutil.rmtree(personal_dst)
            shutil.copytree(personal_src, personal_dst)
        if projects_src.is_dir():
            projects_dst = principal_dir / "projects"
            if projects_dst.exists():
                shutil.rmtree(projects_dst)
            shutil.copytree(projects_src, projects_dst)

    connectors_dst = principal_dir / "connectors"
    scripts_dst = connectors_dst / "scripts"
    scripts_dst.mkdir(parents=True, exist_ok=True)

    prebuilt_scripts = root / "users" / principal_id / "connectors" / "scripts"
    if prebuilt_scripts.is_dir() and prebuilt_scripts.resolve() != scripts_dst.resolve():
        for script in prebuilt_scripts.glob("*.py"):
            if script.name != "migrate_to_principals.py":
                shutil.copy2(script, scripts_dst / script.name)

    instance_data = {
        "id": f"principal.{principal_id}",
        "type": "principal",
        "name": principal_id,
        "fields": {
            "registry": {"storage": "registry.yaml"},
            "types": {"storage": "types/"},
            "personal": {"id": "personal.main", "type": "personal", "storage": "personal/"},
            "projects": {
                "id": "directory.projects",
                "type": "directory",
                "content_type": "project",
                "storage": "projects/",
            },
            "connectors": {"storage": "connectors/"},
        },
    }
    (principal_dir / "instance.yaml").write_text(
        yaml.dump(instance_data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    (root / "jah.yaml").write_text(f"active_principal: {principal_id}\n", encoding="utf-8")

    rewrite_tree(principal_dir, principal_id)
    if (root / "CLAUDE.md").is_file():
        text = (root / "CLAUDE.md").read_text(encoding="utf-8")
        (root / "CLAUDE.md").write_text(rewrite_text(text, principal_id), encoding="utf-8")
    if (root / ".cursor").is_dir():
        rewrite_tree(root / ".cursor", principal_id)

    registry = generate_registry(principal_dir / "types", principal_id)
    (principal_dir / "registry.yaml").write_text(
        yaml.dump(registry, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    if legacy_memory.is_dir():
        shutil.rmtree(legacy_memory)
    if legacy_types.is_dir():
        shutil.rmtree(legacy_types)
    if legacy_tools.is_dir():
        shutil.rmtree(legacy_tools)

    print(f"Migration complete: users/{principal_id}/")
    print("Legacy memory/, types/, tools/ removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
