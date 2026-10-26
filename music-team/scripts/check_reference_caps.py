#!/usr/bin/env python3
"""check_reference_caps.py - plugin-local reference lint for music-team (W0-3).

Rules (music-team-plan.md section 12):
  * every prose (.md) file under music-team/**/references/** is <= 150 lines
    (.json manifests and .txt data lists are exempt from the cap)
  * files under a genres/ directory are <= 100 lines
  * every pair listed in music-team/CROSS-SKILL-REFERENCES.md as a duplicate
    must be byte-identical (drift check)
  * every Markdown reference file begins with the 3-line frontmatter
    (loaded_by / level / last_reviewed)

This lint never touches the shared scripts/check_skill_budgets.py walker.

Usage:
  python -I music-team/scripts/check_reference_caps.py [--root <repo-root>] [--quiet]
Exit codes: 0 pass, 1 violations, 3 plugin root not found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

GENERAL_CAP = 150
GENRE_CAP = 100
FRONTMATTER_KEYS = ("loaded_by", "level", "last_reviewed")
# Markdown table rows in CROSS-SKILL-REFERENCES.md: | <path-a> | <path-b> | ...
_PAIR_ROW = re.compile(r"^\|\s*`?([^`|]+?)`?\s*\|\s*`?([^`|]+?)`?\s*\|")


def _count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        return sum(1 for _ in fh)


def _has_frontmatter(path: Path) -> bool:
    """Markdown: a ``---`` fence, the three keys, and a closing ``---`` within
    the first eight lines. Text data lists: ``# <key>:`` comment lines at top."""
    try:
        head = path.read_text(encoding="utf-8", errors="replace").splitlines()[:8]
    except OSError:
        return False
    if path.suffix == ".txt":
        keys = {line.lstrip("# ").split(":", 1)[0].strip() for line in head if line.startswith("#") and ":" in line}
        return all(k in keys for k in FRONTMATTER_KEYS)
    if not head or head[0].strip() != "---":
        return False
    if not any(line.strip() == "---" for line in head[1:]):
        return False
    close = next(i for i, line in enumerate(head[1:], 1) if line.strip() == "---")
    keys = {line.split(":", 1)[0].strip() for line in head[1:close] if ":" in line}
    return all(k in keys for k in FRONTMATTER_KEYS)


def find_reference_files(plugin_root: Path) -> list[Path]:
    files = [p for p in plugin_root.rglob("references/**/*") if p.is_file()]
    return sorted(files)


def check_caps(plugin_root: Path) -> list[str]:
    violations: list[str] = []
    for path in find_reference_files(plugin_root):
        rel = path.relative_to(plugin_root).as_posix()
        if path.suffix in (".md", ".txt") and not _has_frontmatter(path):
            violations.append(
                f"FRONTMATTER: {rel} missing loaded_by/level/last_reviewed block"
            )
        if path.suffix in (".json", ".txt"):
            continue  # manifests and data lists (blocked targets, cliches) are not prose; no line cap
        cap = GENRE_CAP if "/genres/" in f"/{rel}" else GENERAL_CAP
        n = _count_lines(path)
        if n > cap:
            violations.append(f"CAP: {rel} {n}/{cap} lines")
    return violations


def parse_duplicate_pairs(cross_ref: Path) -> list[tuple[str, str]]:
    """Read duplicate pairs from the 'Duplicated files' table of
    CROSS-SKILL-REFERENCES.md. Rows whose first cell is a header or a
    separator are skipped; paths are plugin-relative."""
    if not cross_ref.exists():
        return []
    pairs: list[tuple[str, str]] = []
    in_section = False
    in_fence = False
    for line in cross_ref.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("#"):
            in_section = "duplicat" in line.lower()
            continue
        if not in_section:
            continue
        m = _PAIR_ROW.match(line)
        if not m:
            continue
        a, b = m.group(1).strip(), m.group(2).strip()
        if a.lower() in ("source", "file a", "path") or set(a) <= {"-", ":", " "}:
            continue
        pairs.append((a, b))
    return pairs


def check_duplicates(plugin_root: Path) -> list[str]:
    violations: list[str] = []
    cross_ref = plugin_root / "CROSS-SKILL-REFERENCES.md"
    if not cross_ref.exists():
        print("WARN: CROSS-SKILL-REFERENCES.md absent; duplicate drift check skipped (lands in W5-3)")
        return violations
    pairs = parse_duplicate_pairs(cross_ref)
    if not pairs:
        return [f"DUPLICATE-TABLE: {cross_ref.name} exists but lists no duplicate pairs"]
    for a, b in pairs:
        pa, pb = plugin_root / a, plugin_root / b
        if not pa.exists() or not pb.exists():
            violations.append(f"DUPLICATE-MISSING: {a} <-> {b} (one side absent)")
            continue
        if pa.read_bytes() != pb.read_bytes():
            violations.append(f"DUPLICATE-DRIFT: {a} differs from {b}")
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".", help="repository root (default: cwd)")
    parser.add_argument("--quiet", action="store_true", help="print violations only")
    args = parser.parse_args(argv)

    plugin_root = Path(args.root) / "music-team"
    if not plugin_root.is_dir():
        print(f"ERROR: plugin root not found: {plugin_root}")
        return 3

    violations = check_caps(plugin_root) + check_duplicates(plugin_root)
    for v in violations:
        print(v)
    total = len(find_reference_files(plugin_root))
    if violations:
        print(f"\nREFERENCE CAPS FAILED: {len(violations)} violation(s) in {total} file(s).")
        return 1
    if not args.quiet:
        print(f"REFERENCE CAPS PASSED: {total} reference file(s) checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
