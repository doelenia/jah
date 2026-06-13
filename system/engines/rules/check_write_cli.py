#!/usr/bin/env python3
"""Advisory check before writing to a path — warns on L4+ without pre_approval checkpoint."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from env import repo_root

from context.compile import parse_session
from rules.check_write import advisory_message, classify_write_level, has_pre_approval_checkpoint


def main() -> int:
    parser = argparse.ArgumentParser(description="Advisory write-level check for Jah sessions.")
    parser.add_argument("session_path", help="e.g. users/katakuchi/projects/jah/sessions/YYYY-MM-DD-001")
    parser.add_argument("--target", required=True, help="Repo-relative write target path")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when L4+ write lacks pre_approval checkpoint (for CI opt-in)",
    )
    args = parser.parse_args()

    root = repo_root()
    session_path = root / args.session_path

    try:
        session_path, _, _, _ = parse_session(session_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    level = classify_write_level(args.target, session_path)
    trace_path = session_path / "trace.md"
    trace_text = trace_path.read_text(encoding="utf-8") if trace_path.is_file() else ""
    has_checkpoint = has_pre_approval_checkpoint(trace_text)

    print(f"target: {args.target}")
    print(f"level: {level}")
    print(f"pre_approval_checkpoint: {'yes' if has_checkpoint else 'no'}")

    warning = advisory_message(level, args.target, has_checkpoint)
    if warning:
        print(f"warning: {warning}", file=sys.stderr)
        return 1 if args.strict else 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
