#!/usr/bin/env python3
"""Resolve active rules for a session trigger and context."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from env import principal_root, repo_root

from context.compile import parse_session
from rules.lib import (
    format_rule_bundle,
    load_rules,
    project_id_from_path,
    resolve_bundle,
    rule_index_entry,
)


def bundle_payload(rules: list[dict]) -> list[dict]:
    return [
        {
            **rule_index_entry(rule),
            "rule": str(rule.get("rule", "")).strip(),
        }
        for rule in rules
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve Jah rules for a session trigger.")
    parser.add_argument("session_path", help="e.g. users/katakuchi/projects/jah/sessions/YYYY-MM-DD-001")
    parser.add_argument(
        "--trigger",
        required=True,
        choices=["session_start", "pre_write", "topic_shift", "pre_approval"],
        help="Activation trigger",
    )
    parser.add_argument("--target", default="", help="Write target path for applies_to matching")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    root = repo_root()
    session_path = root / args.session_path

    try:
        session_path, project_path, goal, session = parse_session(session_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    principal = principal_root()
    all_rules = load_rules(principal, project_path)
    workflow_id = str(session.get("workflow_id") or "")
    project_id = project_id_from_path(project_path)

    matched = resolve_bundle(
        all_rules,
        trigger=args.trigger,
        goal=goal,
        project_id=project_id,
        workflow_id=workflow_id,
        target=args.target,
    )

    if args.json:
        print(
            json.dumps(
                {
                    "trigger": args.trigger,
                    "target": args.target,
                    "project_id": project_id,
                    "goal": goal,
                    "rules": bundle_payload(matched),
                },
                indent=2,
            )
        )
        return 0

    header = [
        f"# Resolved rules — `{args.trigger}`",
        "",
        f"**Session:** `{args.session_path}`",
        f"**Goal:** {goal or '*(none)*'}",
    ]
    if args.target:
        header.append(f"**Target:** `{args.target}`")
    header.append(f"**Matched:** {len(matched)} rule(s)")
    header.append("")

    ids = ", ".join(f"`{r.get('id', '?')}`" for r in matched) or "*(none)*"
    header.append(f"**Rule ids:** {ids}")
    header.append("")

    print("\n".join(header))
    print(format_rule_bundle(matched))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
