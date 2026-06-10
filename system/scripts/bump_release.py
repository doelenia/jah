#!/usr/bin/env python3
"""Bump system version and sync CHANGELOG + README recent updates."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


RECENT_RELEASE_COUNT = 5
README_MARKER_START = "<!-- recent-updates:start -->"
README_MARKER_END = "<!-- recent-updates:end -->"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_version(version_path: Path) -> tuple[int, int, int]:
    text = version_path.read_text(encoding="utf-8").strip()
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", text)
    if not match:
        raise ValueError(f"Invalid VERSION format: {text!r} (expected MAJOR.MINOR.PATCH)")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def bump_version(parts: tuple[int, int, int], level: str) -> tuple[int, int, int]:
    major, minor, patch = parts
    if level == "major":
        return major + 1, 0, 0
    if level == "minor":
        return major, minor + 1, 0
    if level == "patch":
        return major, minor, patch + 1
    raise ValueError(f"Unknown bump level: {level}")


def format_version(parts: tuple[int, int, int]) -> str:
    return f"{parts[0]}.{parts[1]}.{parts[2]}"


def parse_changelog_entries(changelog_text: str) -> list[dict]:
    """Parse released sections from CHANGELOG (not [Unreleased])."""
    entries: list[dict] = []
    current: dict | None = None
    section: str | None = None

    for line in changelog_text.splitlines():
        header = re.match(r"^## \[([^\]]+)\] - (\d{4}-\d{2}-\d{2})$", line)
        if header:
            if current:
                entries.append(current)
            current = {
                "version": header.group(1),
                "date": header.group(2),
                "sections": {},
            }
            section = None
            continue

        if current is None:
            continue

        sec = re.match(r"^### (.+)$", line)
        if sec:
            section = sec.group(1)
            current["sections"].setdefault(section, [])
            continue

        item = re.match(r"^- (.+)$", line)
        if item and section:
            current["sections"][section].append(item.group(1))

    if current:
        entries.append(current)

    return entries


def prepend_changelog_entry(
    changelog_path: Path,
    version: str,
    release_date: str,
    messages: list[str],
) -> None:
    text = changelog_path.read_text(encoding="utf-8")
    if f"## [{version}]" in text:
        raise ValueError(f"CHANGELOG already contains [{version}]")

    bullets = "\n".join(f"- {msg}" for msg in messages)
    entry = f"""## [{version}] - {release_date}

### Added

{bullets}

"""

    marker = "## [Unreleased]"
    if marker not in text:
        raise ValueError(f"CHANGELOG missing {marker!r} section")

    updated = text.replace(marker, f"{marker}\n\n{entry.rstrip()}\n", 1)
    changelog_path.write_text(updated, encoding="utf-8")


def render_recent_updates(entries: list[dict], limit: int) -> str:
    lines: list[str] = []
    for entry in entries[:limit]:
        lines.append(f"### {entry['version']} ({entry['date']})")
        added = entry["sections"].get("Added", [])
        changed = entry["sections"].get("Changed", [])
        fixed = entry["sections"].get("Fixed", [])
        items = added or changed or fixed
        if not items:
            for section_items in entry["sections"].values():
                items.extend(section_items)
        for item in items[:4]:
            lines.append(f"- {item}")
        if len(items) > 4:
            lines.append(f"- …and {len(items) - 4} more (see changelog)")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def sync_readme_recent_updates(readme_path: Path, changelog_path: Path) -> None:
    readme = readme_path.read_text(encoding="utf-8")
    changelog = changelog_path.read_text(encoding="utf-8")
    entries = parse_changelog_entries(changelog)
    block = render_recent_updates(entries, RECENT_RELEASE_COUNT)

    pattern = re.compile(
        re.escape(README_MARKER_START) + r".*?" + re.escape(README_MARKER_END),
        re.DOTALL,
    )
    replacement = f"{README_MARKER_START}\n{block}{README_MARKER_END}"
    if not pattern.search(readme):
        raise ValueError(
            f"README.md missing recent-updates markers "
            f"({README_MARKER_START} / {README_MARKER_END})"
        )
    updated = pattern.sub(replacement, readme)

    version_line = re.search(
        r"^Current system version: \*\*[\d.]+\*\*",
        updated,
        re.MULTILINE,
    )
    if version_line:
        current = read_version(repo_root() / "system" / "VERSION")
        new_line = f"Current system version: **{format_version(current)}**"
        updated = updated[: version_line.start()] + new_line + updated[version_line.end() :]

    readme_path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bump Jah system version and update CHANGELOG + README."
    )
    parser.add_argument(
        "--bump",
        choices=("patch", "minor", "major"),
        default="patch",
        help="Semver bump level (default: patch)",
    )
    parser.add_argument(
        "-m",
        "--message",
        action="append",
        dest="messages",
        required=True,
        help="Changelog bullet (repeatable)",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Release date YYYY-MM-DD (default: today)",
    )
    args = parser.parse_args()

    root = repo_root()
    version_path = root / "system" / "VERSION"
    changelog_path = root / "system" / "CHANGELOG.md"
    readme_path = root / "README.md"

    for path in (version_path, changelog_path, readme_path):
        if not path.is_file():
            print(f"Error: required file missing: {path}", file=sys.stderr)
            return 1

    try:
        current = read_version(version_path)
        new_parts = bump_version(current, args.bump)
        new_version = format_version(new_parts)

        version_path.write_text(new_version + "\n", encoding="utf-8")
        prepend_changelog_entry(changelog_path, new_version, args.date, args.messages)
        sync_readme_recent_updates(readme_path, changelog_path)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Bumped system to {new_version}")
    print(f"  {version_path.relative_to(root)}")
    print(f"  {changelog_path.relative_to(root)}")
    print(f"  {readme_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
