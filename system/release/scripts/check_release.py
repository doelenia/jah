#!/usr/bin/env python3
"""Verify system changes include a VERSION / CHANGELOG update."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


TRACKED_PREFIXES = ("system/", ".github/")
TRACKED_FILES = frozenset({"README.md", ".gitignore", "LICENSE", "CONTRIBUTING.md"})


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root(),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def changed_tracked_files() -> list[str]:
    """Files changed vs HEAD (staged or unstaged) under tracked paths."""
    diff_names = set()
    for arg in ("diff", "diff", "--cached"):
        out = git_output(arg, "--name-only", "HEAD")
        diff_names.update(line.strip() for line in out.splitlines() if line.strip())

    status = git_output("status", "--porcelain")
    for line in status.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        diff_names.add(path)

    return sorted(p for p in diff_names if is_public_path(p))


def is_public_path(path: str) -> bool:
    return path.startswith(TRACKED_PREFIXES) or path in TRACKED_FILES


def version_changelog_touched(files: list[str]) -> bool:
    return "system/release/VERSION" in files and "system/release/CHANGELOG.md" in files


def read_version(path: Path) -> str | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8").strip()
    if re.fullmatch(r"\d+\.\d+\.\d+", text):
        return text
    return None


def unreleased_has_content(changelog_path: Path) -> bool:
    text = changelog_path.read_text(encoding="utf-8")
    match = re.search(
        r"## \[Unreleased\]\s*\n(.*?)(?=\n## \[|\Z)",
        text,
        re.DOTALL,
    )
    if not match:
        return False
    body = match.group(1).strip()
    return bool(body)


def main() -> int:
    root = repo_root()
    changed = changed_tracked_files()

    if not changed:
        print("No tracked system changes detected.")
        return 0

    release_files = {"system/release/VERSION", "system/release/CHANGELOG.md"}
    only_release = set(changed).issubset(release_files)
    system_changed = any(is_public_path(f) and f not in release_files for f in changed)

    if system_changed and not version_changelog_touched(changed):
        print(
            "Error: system files changed but system/release/VERSION and system/release/CHANGELOG.md "
            "were not updated.\n"
            "Run: python3 system/release/scripts/bump_release.py --bump patch -m \"Your summary\"",
            file=sys.stderr,
        )
        print("Changed tracked files:", ", ".join(changed), file=sys.stderr)
        return 1

    if version_changelog_touched(changed) and not only_release and system_changed:
        version = read_version(root / "system" / "release" / "VERSION")
        if not version:
            print("Error: system/release/VERSION is missing or invalid.", file=sys.stderr)
            return 1
        changelog = root / "system" / "release" / "CHANGELOG.md"
        if f"## [{version}]" not in changelog.read_text(encoding="utf-8"):
            print(
                f"Error: CHANGELOG.md has no entry for version {version}.",
                file=sys.stderr,
            )
            return 1

    print("Release check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
