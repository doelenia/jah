#!/usr/bin/env python3
"""Shared path and registry resolution for Jah system engines."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def agent_dir() -> Path:
    return repo_root() / "system" / "agent"


def jah_config_path() -> Path:
    return repo_root() / "jah.yaml"


def load_jah_config() -> dict[str, Any]:
    path = jah_config_path()
    if not path.is_file():
        _fail_uninitialized()
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def active_principal() -> str:
    config = load_jah_config()
    principal = config.get("active_principal")
    if not principal:
        print(
            "Error: jah.yaml missing active_principal. Run: python3 system/release/scripts/init_jah.py <id>",
            file=sys.stderr,
        )
        sys.exit(1)
    return str(principal)


def principal_root(principal: str | None = None) -> Path:
    pid = principal or active_principal()
    return repo_root() / "users" / pid


def registry_path(principal: str | None = None) -> Path:
    return principal_root(principal) / "registry.yaml"


def load_registry(principal: str | None = None) -> dict[str, Any]:
    path = registry_path(principal)
    if not path.is_file():
        print(f"Error: registry not found: {path}", file=sys.stderr)
        sys.exit(1)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def resolve_type_key(type_name: str, registry: dict[str, Any] | None = None) -> str:
    reg = registry or load_registry()
    aliases = reg.get("aliases") or {}
    if type_name in aliases:
        return str(aliases[type_name])
    types = reg.get("types") or {}
    if type_name in types:
        return type_name
    for key, entry in types.items():
        if isinstance(entry, dict) and entry.get("id") == f"type.{type_name}":
            return key
    return type_name


def type_dir(type_name: str, principal: str | None = None) -> Path | None:
    reg = load_registry(principal)
    key = resolve_type_key(type_name, reg)
    types = reg.get("types") or {}
    entry = types.get(key)
    if not isinstance(entry, dict):
        return None
    rel = entry.get("path")
    if not rel:
        return None
    return principal_root(principal) / str(rel)


def extends_chain(type_name: str, principal: str | None = None) -> list[str]:
    reg = load_registry(principal)
    types = reg.get("types") or {}
    chain: list[str] = []
    key = resolve_type_key(type_name, reg)
    seen: set[str] = set()
    while key and key not in seen:
        seen.add(key)
        chain.append(key)
        entry = types.get(key)
        if not isinstance(entry, dict):
            break
        parent = entry.get("extends")
        if not parent:
            break
        key = str(parent)
    return list(reversed(chain))


def type_yaml_paths(type_name: str, principal: str | None = None) -> list[Path]:
    paths = []
    for key in extends_chain(type_name, principal):
        tdir = type_dir(key, principal)
        if tdir and (tdir / "type.yaml").is_file():
            paths.append(tdir / "type.yaml")
    return paths


def type_readme_paths(type_name: str, principal: str | None = None) -> list[Path]:
    paths = []
    for key in extends_chain(type_name, principal):
        tdir = type_dir(key, principal)
        if tdir and (tdir / "README.md").is_file():
            paths.append(tdir / "README.md")
    return paths


def all_registry_type_names(principal: str | None = None) -> list[str]:
    reg = load_registry(principal)
    return sorted((reg.get("types") or {}).keys())


def _fail_uninitialized() -> None:
    print(
        "Error: jah.yaml not found. See system/bootstrap/SETUP.md or run:\n"
        "  python3 system/release/scripts/init_jah.py <principal-id>",
        file=sys.stderr,
    )
    sys.exit(1)
