#!/usr/bin/env python3
"""Initialize a new Jah principal from system/bootstrap/."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a Jah principal.")
    parser.add_argument("principal_id", help="e.g. katakuchi")
    parser.add_argument("--force", action="store_true", help="Overwrite existing principal")
    args = parser.parse_args()

    root = repo_root()
    principal_id = args.principal_id.strip()
    principal_dir = root / "users" / principal_id
    registry_path = principal_dir / "registry.yaml"

    if registry_path.is_file() and not args.force:
        print(f"Error: principal already exists: {principal_dir}", file=sys.stderr)
        return 1

    bootstrap = root / "system" / "bootstrap"
    if not bootstrap.is_dir():
        print("Error: system/bootstrap/ not found", file=sys.stderr)
        return 1

    principal_dir.mkdir(parents=True, exist_ok=True)

    types_src = bootstrap / "types"
    types_dst = principal_dir / "types"
    if types_dst.exists():
        shutil.rmtree(types_dst)
    shutil.copytree(types_src, types_dst)

    seed_registry = bootstrap / "registry.seed.yaml"
    reg_data = yaml.safe_load(seed_registry.read_text(encoding="utf-8"))
    reg_data["id"] = f"registry.{principal_id}"
    registry_path.write_text(yaml.dump(reg_data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    seed_instance = bootstrap / "principal.seed" / "instance.yaml"
    instance_data = yaml.safe_load(seed_instance.read_text(encoding="utf-8"))
    instance_data["id"] = f"principal.{principal_id}"
    instance_data["name"] = principal_id
    (principal_dir / "instance.yaml").write_text(
        yaml.dump(instance_data, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )

    personal_dir = principal_dir / "personal"
    personal_dir.mkdir(exist_ok=True)
    personal_instance = personal_dir / "instance.yaml"
    if not personal_instance.is_file():
        personal_instance.write_text(
            f"id: personal.main\ntype: personal\nname: Personal\n",
            encoding="utf-8",
        )

    (principal_dir / "projects").mkdir(exist_ok=True)
    tools_dir = principal_dir / "tools"
    tools_dir.mkdir(exist_ok=True)
    scripts_dir = tools_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)

    jah_yaml = root / "jah.yaml"
    jah_yaml.write_text(f"active_principal: {principal_id}\n", encoding="utf-8")

    print(f"Initialized principal: users/{principal_id}/")
    print(f"Wrote jah.yaml with active_principal: {principal_id}")
    print("Next: copy tools/scripts into users/<id>/tools/scripts/ and create a project.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
