#!/usr/bin/env python3
"""Create a new Jah session folder."""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from jah_env import repo_root


def next_session_id(sessions_dir: Path, date_prefix: str) -> str:
    existing = sorted(
        p.name for p in sessions_dir.iterdir()
        if p.is_dir() and p.name.startswith(date_prefix)
    )
    if not existing:
        return f"{date_prefix}-001"
    last = existing[-1].split("-")[-1]
    return f"{date_prefix}-{int(last) + 1:03d}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new Jah session.")
    parser.add_argument("project_path", help="e.g. users/katakuchi/projects/jah")
    parser.add_argument("goal", help="Session goal")
    parser.add_argument(
        "--workflow-id",
        help="Explicit workflow id to invoke, e.g. workflow.us_taxes.tax_filing",
    )
    args = parser.parse_args()

    root = repo_root()
    project_path = root / args.project_path
    if not project_path.is_dir():
        print(f"Error: project path not found: {project_path}", file=sys.stderr)
        return 1

    sessions_dir = project_path / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    session_id = next_session_id(sessions_dir, today)
    session_dir = sessions_dir / session_id
    session_dir.mkdir()

    created_at = datetime.now(timezone.utc).isoformat()
    rel_project = args.project_path.replace("\\", "/")

    workflow_id_line = ""
    if args.workflow_id:
        workflow_id_line = f'workflow_id: "{args.workflow_id}"\n'

    instance_yaml = f"""id: session.{session_id}
type: session
name: Session {session_id}
status: created
main_instance: {rel_project}
goal: "{args.goal.replace('"', '\\"')}"
{workflow_id_line}created_at: "{created_at}"
fields:
  input:
    type: session_artifact
    storage: input.md
  compiled_context:
    type: session_artifact
    storage: compiled_context.md
  output:
    type: session_artifact
    storage: output.md
  evaluation:
    type: session_artifact
    storage: evaluation.md
  trace:
    type: session_artifact
    storage: trace.md
  patch:
    type: session_artifact
    storage: patch.md
allowed_write:
  - this session folder
  - existing principal instances and types
requires_approval:
  - modify personal profile
  - register new types in registry
  - modify system/
  - use external tools
  - publish or send anything externally
"""

    files = {
        "instance.yaml": instance_yaml,
        "input.md": f"# Session Input\n\n{args.goal}\n",
        "compiled_context.md": "",
        "output.md": "# Output\n\n## References\n\n### Internal\n\n### External\n\n",
        "evaluation.md": (
            "# Evaluation\n\n"
            "## Success criteria\n\n"
            "| Criterion | Met? | Notes |\n"
            "|-----------|------|-------|\n\n"
            "## References consulted\n\n"
            "| Path | Role |\n"
            "|------|------|\n\n"
            "## Stable updates\n\n"
            "| Target | Action | Applied? |\n"
            "|--------|--------|----------|\n\n"
            "## Open questions\n\n"
        ),
        "trace.md": (
            "# Trace\n\n"
            "## Discovery log\n\n"
            "| Path | Why read | Used? |\n"
            "|------|----------|-------|\n\n"
            "## Steps\n\n"
            "## References\n\n"
            "### Internal\n\n"
            "### External\n\n"
        ),
        "patch.md": (
            "# Patch Proposal\n\n"
            "For profile updates, new registry types, and system change proposals only. "
            "Existing principal instances and types may be updated directly (see `system/permission_model.md`).\n\n"
            "## References\n\n"
            "### Internal\n\n"
            "### External\n\n"
        ),
    }

    for name, content in files.items():
        (session_dir / name).write_text(content, encoding="utf-8")

    rel_session = session_dir.relative_to(root).as_posix()
    print(rel_session)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
