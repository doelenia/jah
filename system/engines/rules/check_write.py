"""Classify write targets and advisory pre-approval checks."""

from __future__ import annotations

from pathlib import Path

from env import repo_root


def classify_write_level(target: str, session_path: Path) -> str:
    """Return L2, L3, L4, or L5 for a repo-relative target path."""
    target = target.strip().replace("\\", "/").lstrip("./")
    root = repo_root()
    session_rel = session_path.resolve().relative_to(root).as_posix()

    if target.startswith("system/"):
        return "L5"
    if target.endswith("personal/profile.md"):
        return "L4"
    if target.endswith("registry.yaml"):
        return "L4"
    if target.startswith(session_rel + "/") or target == session_rel:
        return "L2"
    if target.startswith("users/"):
        return "L3"
    return "L3"


def has_pre_approval_checkpoint(trace_text: str) -> bool:
    """True if trace contains a Rule checkpoint with pre_approval trigger."""
    if "## Rule checkpoint" not in trace_text:
        return False
    blocks = trace_text.split("## Rule checkpoint")
    for block in blocks[1:]:
        if "pre_approval" in block.lower():
            return True
    return False


def advisory_message(level: str, target: str, has_checkpoint: bool) -> str | None:
    if level not in ("L4", "L5"):
        return None
    if has_checkpoint:
        return None
    return (
        f"Advisory: write to `{target}` is {level} (requires approval). "
        "No `pre_approval` rule checkpoint found in trace.md. "
        "Run: resolve-rules --trigger pre_approval --target <path>; attest in trace."
    )
