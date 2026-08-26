#!/usr/bin/env python3
"""Jah system CLI — unified entry for all protocol engines."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ENGINES_DIR = Path(__file__).resolve().parent
if str(ENGINES_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINES_DIR))

COMMANDS: dict[str, tuple[str, str]] = {
    "compile-context": ("context.compile", "main"),
    "new-session": ("session.new", "main"),
    "list-instances": ("instances.list", "main"),
    "validate-registry": ("registry.validate", "main"),
    "list-types": ("registry.list_types", "main"),
    "validate-structure": ("structure.validate", "main"),
    "validate-knowledge": ("knowledge.validate", "main"),
    "resolve-knowledge": ("knowledge.resolve", "main"),
    "resolve-rules": ("rules.resolve", "main"),
    "check-write": ("rules.check_write_cli", "main"),
    "archive-project": ("archive.project", "archive_main"),
    "unarchive-project": ("archive.project", "unarchive_main"),
}


def usage() -> str:
    names = ", ".join(sorted(COMMANDS))
    return f"Usage: python3 system/engines/cli.py <command> [args...]\n\nCommands: {names}\n"


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if not args or args[0] in ("-h", "--help"):
        print(usage(), end="")
        return 0 if args and args[0] in ("-h", "--help") else 1

    command = args[0]
    spec = COMMANDS.get(command)
    if not spec:
        print(f"Error: unknown command: {command}\n", file=sys.stderr)
        print(usage(), end="")
        return 1

    module_name, attr = spec
    module = importlib.import_module(module_name)
    handler = getattr(module, attr)
    sys.argv = [f"cli.py {command}", *args[1:]]
    return int(handler())


if __name__ == "__main__":
    raise SystemExit(main())
