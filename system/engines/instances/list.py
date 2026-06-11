#!/usr/bin/env python3
"""List all instance.yaml paths under the active principal."""

import sys
from pathlib import Path

from env import active_principal, principal_root, repo_root


def main() -> int:
    principal = active_principal()
    root = principal_root(principal)
    if not root.is_dir():
        print(f"Error: principal not found: {root}", file=sys.stderr)
        return 1

    repo = repo_root()
    paths = sorted(
        p.relative_to(repo).as_posix()
        for p in root.rglob("instance.yaml")
    )

    for path in paths:
        print(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
