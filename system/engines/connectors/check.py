#!/usr/bin/env python3
"""Validate a principal's connector route map and detect drift against agent MCP configs.

The route map (`users/<id>/connectors/routes.yaml`) records, per external service, every route an
agent can use (repo MCP, user MCP, host-provided connector, native CLI, direct API, browser), which
hosts each route serves, and how to discover its tools. See `system/agent/connectors.md`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

from env import active_principal, principal_root, repo_root

KINDS = {"mcp-repo", "mcp-user", "host-connector", "native-cli", "direct-api", "browser"}
HOSTS = {"claude-desktop", "claude-code-cli", "claude-web", "cursor", "codex", "any-shell"}
STATUSES = {"active", "dead", "planned"}

# Config files a route's `config: "<file>#<server>"` may point at. `~` = $HOME.
CONFIG_FILES = [".mcp.json", ".cursor/mcp.json", "~/.cursor/mcp.json"]


def routes_file(principal: str) -> Path:
    return principal_root(principal) / "connectors" / "routes.yaml"


def resolve_config(path_str: str) -> Path:
    return Path(path_str).expanduser() if path_str.startswith("~") else repo_root() / path_str


def load_mcp_servers(path_str: str) -> set[str] | None:
    path = resolve_config(path_str)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return set((data.get("mcpServers") or {}).keys())


def check(principal: str) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    path = routes_file(principal)
    if not path.is_file():
        return [f"missing route map: {path.relative_to(repo_root())}"], [], {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    services = data.get("services") or {}
    if not isinstance(services, dict) or not services:
        errors.append("route map has no `services` mapping")
        return errors, warnings, data

    configs = {name: load_mcp_servers(name) for name in CONFIG_FILES}
    referenced: set[tuple[str, str]] = set()

    for svc, entry in services.items():
        entry = entry or {}
        readme = entry.get("readme")
        if readme and not (repo_root() / readme).is_file():
            warnings.append(f"{svc}: readme not found: {readme}")
        routes = entry.get("routes") or []
        if not routes:
            errors.append(f"{svc}: no routes")
        ids: set[str] = set()
        for route in routes:
            rid = route.get("id", "?")
            where = f"{svc}/{rid}"
            if rid in ids:
                errors.append(f"{where}: duplicate route id")
            ids.add(rid)
            kind = route.get("kind")
            if kind not in KINDS:
                errors.append(f"{where}: unknown kind {kind!r} (allowed: {', '.join(sorted(KINDS))})")
            status = route.get("status", "active")
            if status not in STATUSES:
                errors.append(f"{where}: unknown status {status!r}")
            hosts = set(route.get("hosts") or [])
            if not hosts:
                errors.append(f"{where}: no hosts")
            bad = hosts - HOSTS
            if bad:
                errors.append(f"{where}: unknown hosts {sorted(bad)} (allowed: {', '.join(sorted(HOSTS))})")
            pref = set(route.get("preferred_on") or [])
            if pref - hosts:
                errors.append(f"{where}: preferred_on {sorted(pref - hosts)} not in hosts")
            if status == "dead" and pref:
                errors.append(f"{where}: dead route cannot be preferred")
            if kind in {"mcp-repo", "mcp-user"}:
                cfg = route.get("config") or ""
                if "#" not in cfg:
                    errors.append(f"{where}: MCP route needs config '<file>#<server>'")
                    continue
                file_part, server = cfg.split("#", 1)
                referenced.add((file_part, server))
                servers = configs.get(file_part)
                if servers is None and file_part not in configs:
                    servers = load_mcp_servers(file_part)
                present = servers is not None and server in servers
                if status == "active" and not present:
                    errors.append(f"{where}: active route but '{server}' not in {file_part}")
                if status == "dead" and present:
                    warnings.append(f"{where}: dead route still configured in {file_part} (remove it)")
            if kind == "host-connector" and not route.get("discover"):
                warnings.append(f"{where}: host connector without `discover` hint (agents can't find deferred tools)")
            if kind == "native-cli":
                cmd = route.get("command") or ""
                if cmd and not (repo_root() / cmd.split()[0]).exists():
                    errors.append(f"{where}: command not found: {cmd.split()[0]}")
        # every host that has an active route should know which one to use
        active = [r for r in routes if r.get("status", "active") == "active"]
        for host in sorted({h for r in active for h in (r.get("hosts") or [])}):
            candidates = [r for r in active if host in (r.get("hosts") or [])]
            if len(candidates) > 1 and not any(host in (r.get("preferred_on") or []) for r in candidates):
                warnings.append(f"{svc}: {len(candidates)} active routes on {host} but none preferred_on it")

    for file_part, servers in configs.items():
        for server in sorted(servers or []):
            if (file_part, server) not in referenced:
                warnings.append(f"unregistered MCP server '{server}' in {file_part}")

    conn_dir = principal_root(principal) / "connectors"
    folders = {p.name for p in conn_dir.iterdir() if p.is_dir() and not p.name.startswith(".")}
    covered = set(services)
    for entry in services.values():
        readme = (entry or {}).get("readme") or ""
        parts = Path(readme).parts
        if "connectors" in parts and parts.index("connectors") + 1 < len(parts):
            covered.add(parts[parts.index("connectors") + 1])
    for folder in sorted(folders - covered):
        warnings.append(f"connector folder without a route-map entry: connectors/{folder}/")
    return errors, warnings, data


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate connector route map and MCP config drift.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()
    principal = active_principal()
    errors, warnings, data = check(principal)
    services = (data or {}).get("services") or {}
    print(f"# Connector routes — {principal}\n")
    for svc, entry in services.items():
        for r in (entry or {}).get("routes") or []:
            pref = ",".join(r.get("preferred_on") or []) or "-"
            print(f"- {svc}/{r.get('id')}: {r.get('kind')} [{r.get('status', 'active')}] hosts={','.join(r.get('hosts') or [])} preferred_on={pref}")
    print()
    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN: {w}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
