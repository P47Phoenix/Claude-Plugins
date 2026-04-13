#!/usr/bin/env python3
"""PostToolUse hook: Detect BOM drift when schematic files are modified.

Triggered on Write/Edit of .kicad_sch files. Compares the schematic's component
list against the most recent BOM artifact. Warns about added/removed components.
Silent when no BOM exists or no drift detected.

Security: All input parsed via json.loads(). No shell=True. Paths validated.
Per SEC-06, all environment variables treated as untrusted input.
"""
import json
import os
import re
import sys
from pathlib import Path


# KiCad schematic file extension to watch.
KICAD_SCH_EXT = ".kicad_sch"

# Known BOM artifact locations within .hardware/artifacts/.
BOM_ARTIFACT_PATHS = [
    ".hardware/artifacts/05-dfm-dfa/bom-validation.md",
    ".hardware/artifacts/08-production-release/final-bom.md",
]


def _read_hook_input() -> dict:
    """Read hook input from stdin (Claude Code hook protocol)."""
    try:
        return json.loads(sys.stdin.read())
    except (json.JSONDecodeError, Exception):
        return {}


def _extract_file_path(hook_input: dict) -> str | None:
    """Extract the file path from the tool input."""
    tool_input = hook_input.get("tool_input", {})
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except (json.JSONDecodeError, TypeError):
            return None

    file_path = tool_input.get("file_path", "")
    if not file_path:
        file_path = tool_input.get("path", "")
    return file_path if file_path else None


def _is_kicad_schematic(file_path: str) -> bool:
    """Check if the file is a KiCad schematic."""
    return file_path.lower().endswith(KICAD_SCH_EXT)


def _get_cwd(hook_input: dict) -> Path:
    """Extract working directory from hook input."""
    return Path(hook_input.get("cwd", os.getcwd()))


def _extract_schematic_components(file_path: str) -> set[str]:
    """Extract component reference designators from a .kicad_sch file.

    Parses S-expression format to find (symbol ... (property "Reference" "Rxx"))
    patterns. Returns a set of reference designators.
    """
    components = set()

    try:
        content = Path(file_path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return components

    # Find all reference designators in symbol instances.
    # Pattern: (property "Reference" "C1" ...) within (symbol blocks.
    refs = re.findall(
        r'\(property\s+"Reference"\s+"([^"]+)"', content
    )

    # Filter out power symbols and flags (they are not BOM components).
    for ref in refs:
        if ref and not ref.startswith(("#PWR", "#FLG", "#SYM")):
            components.add(ref)

    return components


def _extract_bom_components(bom_path: Path) -> set[str]:
    """Extract component reference designators from a BOM artifact file.

    BOM artifacts are markdown files. Components appear in table rows or
    as reference designator lists. We look for standard ref-des patterns.
    """
    components = set()

    try:
        content = bom_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return components

    # Match standard reference designators: C1, R23, U4, D1, L2, Q1, etc.
    # Also handles comma-separated lists like "R1, R2, R3".
    refs = re.findall(r'\b([A-Z]{1,3}\d+)\b', content)

    # Filter out common false positives (section headers, etc.).
    valid_prefixes = (
        "R", "C", "L", "D", "U", "Q", "J", "P", "SW", "F", "FB",
        "Y", "T", "K", "TP", "LED", "BT", "M", "X",
    )
    for ref in refs:
        prefix = re.match(r'^([A-Z]+)', ref)
        if prefix and prefix.group(1) in valid_prefixes:
            components.add(ref)

    return components


def _find_latest_bom(cwd: Path) -> Path | None:
    """Find the most recent BOM artifact file."""
    for rel_path in BOM_ARTIFACT_PATHS:
        bom_path = cwd / rel_path
        if bom_path.exists():
            return bom_path

    # Also check for any BOM-related files in the artifacts tree.
    artifacts_dir = cwd / ".hardware" / "artifacts"
    if artifacts_dir.exists():
        for bom_file in sorted(artifacts_dir.rglob("*bom*"), reverse=True):
            if bom_file.is_file() and bom_file.suffix in (".md", ".csv", ".txt"):
                return bom_file

    return None


def _format_drift_message(
    added: set[str],
    removed: set[str],
    bom_path: Path,
    sch_name: str,
) -> str:
    """Format BOM drift findings as a warning message."""
    lines = [f"BOM DRIFT DETECTED -- {sch_name} vs {bom_path.name}:"]

    if added:
        sorted_added = sorted(added)[:20]
        suffix = f" (and {len(added) - 20} more)" if len(added) > 20 else ""
        lines.append(
            f"  NEW in schematic (not in BOM): {', '.join(sorted_added)}{suffix}"
        )

    if removed:
        sorted_removed = sorted(removed)[:20]
        suffix = f" (and {len(removed) - 20} more)" if len(removed) > 20 else ""
        lines.append(
            f"  REMOVED from schematic (still in BOM): {', '.join(sorted_removed)}{suffix}"
        )

    lines.append("  Run BOM update to reconcile: invoke kicad-happy:bom")
    return "\n".join(lines)


def main():
    hook_input = _read_hook_input()
    file_path = _extract_file_path(hook_input)

    # If no file path or not a KiCad schematic, exit silently.
    if not file_path or not _is_kicad_schematic(file_path):
        sys.exit(0)

    cwd = _get_cwd(hook_input)

    # Find the latest BOM artifact.
    bom_path = _find_latest_bom(cwd)
    if bom_path is None:
        # No BOM exists yet -- nothing to drift against. Silent exit.
        sys.exit(0)

    # Extract components from both sources.
    sch_components = _extract_schematic_components(file_path)
    bom_components = _extract_bom_components(bom_path)

    # If either set is empty, skip comparison (likely parse failure).
    if not sch_components or not bom_components:
        sys.exit(0)

    # Compute drift.
    added = sch_components - bom_components  # In schematic but not in BOM.
    removed = bom_components - sch_components  # In BOM but not in schematic.

    # Silent success -- no output when no drift.
    if not added and not removed:
        sys.exit(0)

    # Report drift as warning (non-blocking).
    message = _format_drift_message(
        added, removed, bom_path, Path(file_path).name
    )
    result = {"message": message}
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
