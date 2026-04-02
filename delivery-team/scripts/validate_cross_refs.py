#!/usr/bin/env python3
"""Validate cross-skill references in delivery-team SKILL.md files.

Scans all SKILL.md files for declared cross-skill references and verifies
that each referenced file or directory exists on disk.

Usage:
    python validate_cross_refs.py [/path/to/delivery-team/]

Exit codes:
    0 — all cross-skill references are valid
    1 — one or more broken references found
"""

import re
import sys
from pathlib import Path


# Pattern to match the ## Cross-Skill References table rows.
# Expects: | `some/path` | owner | purpose |
TABLE_ROW_PATTERN = re.compile(
    r"^\|\s*`([^`]+)`\s*\|",
    re.MULTILINE,
)

# Pattern to detect cross-skill path references outside the formal table.
# Matches paths like: delivery-team/skills/<other-skill>/references/<file>
# or relative forms like: skills/<other-skill>/references/<file>
# or shorthand like: <other-skill>/references/<file>
CROSS_SKILL_PATH_PATTERN = re.compile(
    r"(?:delivery-team/)?skills/(\w[\w-]*)/references/([\w.*/-]+\.(?:md|yml|yaml))",
)


def find_skill_md_files(plugin_root: Path) -> list[Path]:
    """Find all SKILL.md files under the skills/ directory."""
    skills_dir = plugin_root / "skills"
    if not skills_dir.is_dir():
        print(f"ERROR: skills/ directory not found at {skills_dir}")
        sys.exit(1)
    return sorted(skills_dir.glob("*/SKILL.md"))


def extract_cross_ref_section(content: str) -> str | None:
    """Extract the ## Cross-Skill References section from SKILL.md content."""
    marker = "## Cross-Skill References"
    idx = content.find(marker)
    if idx == -1:
        return None
    # Find the next ## heading or end of file
    next_heading = content.find("\n## ", idx + len(marker))
    if next_heading == -1:
        return content[idx:]
    return content[idx:next_heading]


def extract_refs_from_section(
    section: str, skill_name: str, skill_md_path: Path, plugin_root: Path
) -> list[tuple[str, Path, int]]:
    """Extract file paths from a Cross-Skill References table.

    Returns list of (raw_path, resolved_path, line_number) tuples.
    """
    refs = []
    # Get the line offset of the section within the full file
    full_content = skill_md_path.read_text(encoding="utf-8")
    section_start = full_content.find(section)
    lines_before = full_content[:section_start].count("\n") if section_start >= 0 else 0

    for i, line in enumerate(section.splitlines()):
        match = TABLE_ROW_PATTERN.match(line.strip())
        if match:
            raw_path = match.group(1)
            # Skip table header separators
            if raw_path.startswith("-") or raw_path == "File":
                continue
            resolved = resolve_path(raw_path, skill_name, plugin_root)
            refs.append((raw_path, resolved, lines_before + i + 1))
    return refs


def extract_inline_cross_refs(
    content: str, skill_name: str, plugin_root: Path
) -> list[tuple[str, Path, int]]:
    """Find cross-skill path references anywhere in the SKILL.md content.

    Only returns references to OTHER skills (not self-references).
    """
    refs = []
    for i, line in enumerate(content.splitlines()):
        for match in CROSS_SKILL_PATH_PATTERN.finditer(line):
            target_skill = match.group(1)
            # Skip self-references
            if target_skill == skill_name:
                continue
            raw_path = match.group(0)
            resolved = resolve_path(raw_path, skill_name, plugin_root)
            refs.append((raw_path, resolved, i + 1))
    return refs


def resolve_path(raw_path: str, consumer_skill: str, plugin_root: Path) -> Path:
    """Resolve a cross-skill reference path to an absolute path.

    Handles these path forms:
    - delivery-team/skills/<skill>/references/<file>
    - skills/<skill>/references/<file>
    - <skill>/references/<file>  (legacy shorthand)
    """
    cleaned = raw_path.strip()
    # Strip leading delivery-team/ if present
    if cleaned.startswith("delivery-team/"):
        cleaned = cleaned[len("delivery-team/"):]
    # Strip leading skills/ if present
    if cleaned.startswith("skills/"):
        cleaned = cleaned[len("skills/"):]
    # Now we have: <skill>/references/<file>
    return plugin_root / "skills" / cleaned


def validate_path(resolved: Path) -> bool:
    """Check if a resolved path exists. Supports glob patterns (*.yml)."""
    path_str = str(resolved)
    if "*" in path_str:
        # Glob pattern — check if at least one file matches
        parent = resolved.parent
        pattern = resolved.name
        if parent.is_dir():
            matches = list(parent.glob(pattern))
            return len(matches) > 0
        return False
    return resolved.exists()


def main() -> int:
    if len(sys.argv) > 1:
        plugin_root = Path(sys.argv[1]).resolve()
    else:
        plugin_root = Path.cwd().resolve()

    if not (plugin_root / "skills").is_dir():
        print(f"ERROR: {plugin_root} does not look like a delivery-team plugin root")
        print(f"       Expected {plugin_root / 'skills'} to be a directory")
        return 1

    skill_md_files = find_skill_md_files(plugin_root)
    print(f"Scanning {len(skill_md_files)} SKILL.md files in {plugin_root}")
    print()

    all_refs: list[tuple[Path, str, Path, int, bool]] = []
    # (skill_md_path, raw_path, resolved_path, line_number, is_valid)

    for skill_md in skill_md_files:
        skill_name = skill_md.parent.name
        content = skill_md.read_text(encoding="utf-8")

        # Method 1: Formal ## Cross-Skill References section
        section = extract_cross_ref_section(content)
        if section:
            for raw_path, resolved, line_no in extract_refs_from_section(
                section, skill_name, skill_md, plugin_root
            ):
                valid = validate_path(resolved)
                all_refs.append((skill_md, raw_path, resolved, line_no, valid))

        # Method 2: Inline cross-skill path references
        for raw_path, resolved, line_no in extract_inline_cross_refs(
            content, skill_name, plugin_root
        ):
            # Deduplicate — skip if already found in formal section
            already_found = any(
                r[0] == skill_md and r[1] == raw_path for r in all_refs
            )
            if not already_found:
                valid = validate_path(resolved)
                all_refs.append((skill_md, raw_path, resolved, line_no, valid))

    if not all_refs:
        print("No cross-skill references found.")
        return 0

    # Report results
    ok_refs = [r for r in all_refs if r[4]]
    broken_refs = [r for r in all_refs if not r[4]]

    print(f"Found {len(all_refs)} cross-skill reference(s):")
    print()

    for skill_md, raw_path, resolved, line_no, valid in all_refs:
        skill_name = skill_md.parent.name
        status = "OK" if valid else "FAIL"
        print(f"  [{status}] {skill_name}/SKILL.md:{line_no}")
        print(f"         path: {raw_path}")
        if not valid:
            print(f"         resolved to: {resolved}")
            print(f"         FILE NOT FOUND")
        print()

    print(f"Result: {len(ok_refs)} valid, {len(broken_refs)} broken")

    if broken_refs:
        print("\nFAIL: Broken cross-skill references detected.")
        return 1
    else:
        print("\nOK: All cross-skill references are valid.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
