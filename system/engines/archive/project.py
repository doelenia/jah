#!/usr/bin/env python3
"""Archive and unarchive project instances under projects/archive/."""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from env import (
    active_principal,
    find_project_path,
    is_archived_project,
    is_project_archive_container,
    is_project_instance,
    principal_root,
    project_archive_path,
    repo_root,
)


def load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def dump_yaml(path: Path, data: dict) -> None:
    path.write_text(
        yaml.dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def rel_posix(path: Path) -> str:
    return path.resolve().relative_to(repo_root()).as_posix()


def project_meta(project_path: Path) -> dict:
    meta = load_yaml(project_path / "instance.yaml")
    if not meta:
        raise ValueError(f"No instance.yaml at {rel_posix(project_path)}")
    if not is_project_instance(project_path):
        kind = meta.get("kind")
        extra = f" (kind: {kind})" if kind else ""
        raise ValueError(
            f"{rel_posix(project_path)} is type {meta.get('type')!r}{extra}, not a project"
        )
    return meta


def rewrite_session_main_instance(project_path: Path, old: str, new: str) -> int:
    sessions_dir = project_path / "sessions"
    if not sessions_dir.is_dir():
        return 0
    updated = 0
    for child in sessions_dir.iterdir():
        instance = child / "instance.yaml"
        if not instance.is_file():
            continue
        text = instance.read_text(encoding="utf-8")
        if old not in text:
            continue
        instance.write_text(text.replace(old, new), encoding="utf-8")
        updated += 1
    return updated


def ensure_archive_container(proot: Path, principal_id: str) -> Path:
    projects = proot / "projects"
    projects.mkdir(exist_ok=True)

    projects_instance = projects / "instance.yaml"
    data = load_yaml(projects_instance)
    if not data:
        data = {
            "id": f"directory.projects.{principal_id}",
            "type": "directory",
            "name": "Projects",
            "description": (
                "Active project instances. Archived projects live in the archive "
                "field — that folder is not a project."
            ),
            "role": "container",
            "content_type": "project",
            "instances": "<name>/instance.yaml",
            "protocol": f"users/{principal_id}/types/project/README.md",
            "requires_approval": True,
            "fields": {},
        }
    fields = data.setdefault("fields", {})
    if not isinstance(fields, dict):
        fields = {}
        data["fields"] = fields
    if "archive" not in fields:
        fields["archive"] = {
            "id": f"directory.archive.{principal_id}",
            "type": "directory",
            "content_type": "project",
            "kind": "project_archive",
            "storage": "archive/",
        }
    dump_yaml(projects_instance, data)

    archive_dir = project_archive_path(principal_id)
    archive_dir.mkdir(parents=True, exist_ok=True)
    instance_path = archive_dir / "instance.yaml"
    if not instance_path.is_file():
        dump_yaml(
            instance_path,
            {
                "id": f"directory.archive.{principal_id}",
                "type": "directory",
                "kind": "project_archive",
                "name": "Project Archive",
                "description": (
                    "Archived project instances. This folder is not a project. "
                    "Each child is type: project with status: archived. "
                    "Unarchive to restore as a sibling of this folder."
                ),
                "role": "container",
                "content_type": "project",
                "instances": "<name>/instance.yaml",
                "protocol": f"users/{principal_id}/types/project/README.md",
                "requires_approval": True,
            },
        )
    return archive_dir


def _is_active_project_child(src: Path, proot: Path) -> bool:
    projects = (proot / "projects").resolve()
    try:
        rel = src.resolve().relative_to(projects)
    except ValueError:
        return False
    if len(rel.parts) != 1:
        return False
    if is_project_archive_container(src):
        return False
    return True


def archive_project(src: Path) -> Path:
    principal_id = active_principal()
    proot = principal_root(principal_id)
    project_meta(src)
    if is_archived_project(src):
        raise ValueError(f"Already archived: {rel_posix(src)}")
    if not _is_active_project_child(src, proot):
        raise ValueError(
            f"Can only archive a top-level project under projects/: {rel_posix(src)}"
        )

    archive_dir = ensure_archive_container(proot, principal_id)
    dest = archive_dir / src.name
    if dest.exists():
        raise ValueError(f"Destination exists: {rel_posix(dest)}")

    old_rel = rel_posix(src)
    shutil.move(str(src), str(dest))
    new_rel = rel_posix(dest)

    meta = load_yaml(dest / "instance.yaml")
    meta["status"] = "archived"
    meta["archived_at"] = datetime.now(timezone.utc).isoformat()
    meta["archived_from"] = old_rel
    dump_yaml(dest / "instance.yaml", meta)

    n = rewrite_session_main_instance(dest, old_rel, new_rel)
    print(new_rel)
    if n:
        print(f"Updated main_instance on {n} session(s).", file=sys.stderr)
    return dest


def unarchive_project(src: Path) -> Path:
    principal_id = active_principal()
    proot = principal_root(principal_id)
    project_meta(src)

    archive_dir = project_archive_path(principal_id)
    try:
        src.resolve().relative_to(archive_dir)
    except ValueError as exc:
        raise ValueError(
            f"Can only unarchive from the project archive: {rel_posix(src)}"
        ) from exc

    dest = proot / "projects" / src.name
    if dest.exists():
        raise ValueError(f"Destination exists: {rel_posix(dest)}")
    if is_project_archive_container(dest):
        raise ValueError("Cannot unarchive onto the archive container path")

    old_rel = rel_posix(src)
    dest.parent.mkdir(exist_ok=True)
    shutil.move(str(src), str(dest))
    new_rel = rel_posix(dest)

    meta = load_yaml(dest / "instance.yaml")
    meta["status"] = "active"
    meta.pop("archived_at", None)
    meta.pop("archived_from", None)
    dump_yaml(dest / "instance.yaml", meta)

    n = rewrite_session_main_instance(dest, old_rel, new_rel)
    print(new_rel)
    if n:
        print(f"Updated main_instance on {n} session(s).", file=sys.stderr)
    return dest


def _resolve_arg(raw: str) -> Path:
    found = find_project_path(raw, include_archived=True)
    if found is None:
        raise FileNotFoundError(f"Project not found: {raw}")
    return found


def archive_main() -> int:
    parser = argparse.ArgumentParser(
        description="Move a project from projects/<name>/ to projects/archive/<name>/."
    )
    parser.add_argument(
        "project_path",
        help="e.g. users/katakuchi/projects/argentina-visa",
    )
    args = parser.parse_args()
    try:
        src = _resolve_arg(args.project_path)
        archive_project(src)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


def unarchive_main() -> int:
    parser = argparse.ArgumentParser(
        description="Move a project from projects/archive/<name>/ back to projects/<name>/."
    )
    parser.add_argument(
        "project_path",
        help="e.g. users/katakuchi/projects/archive/argentina-visa",
    )
    args = parser.parse_args()
    try:
        src = _resolve_arg(args.project_path)
        unarchive_project(src)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
