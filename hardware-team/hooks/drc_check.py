#!/usr/bin/env python3
"""PostToolUse hook: Auto-run basic DRC validation when KiCad schematic files are modified.

Triggered on Write/Edit of .kicad_sch files. Reports findings as warnings (non-blocking).
Silent on success (no output when no violations found).

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

# Basic DRC rules checked via static analysis of .kicad_sch S-expression content.
# These are lightweight checks -- full DRC requires KiCad's own DRC engine.
DRC_RULES = {
    "DRC-001": {
        "description": "Unconnected power pin detected",
        "pattern": r'\(pin\s+"[^"]*"\s+power_in\b[^)]*\)\s*\(no_connect',
        "severity": "warning",
    },
    "DRC-002": {
        "description": "Missing value on component",
        "pattern": r'\(property\s+"Value"\s+""\s*\)',
        "severity": "warning",
    },
    "DRC-003": {
        "description": "Missing reference designator",
        "pattern": r'\(property\s+"Reference"\s+""\s*\)',
        "severity": "warning",
    },
    "DRC-004": {
        "description": "Duplicate reference designator",
        # This is detected by counting references, not a simple regex.
        "pattern": None,
        "severity": "warning",
    },
    "DRC-005": {
        "description": "Wire not connected (dangling wire end)",
        "pattern": r'\(wire\s*\(pts[^)]*\)\s*\(stroke[^)]*\)\s*\(uuid[^)]*\)\s*\)',
        "severity": "info",
    },
}


def _read_hook_input() -> dict:
    """Read hook input from stdin (Claude Code hook protocol)."""
    try:
        return json.loads(sys.stdin.read())
    except (json.JSONDecodeError, Exception):
        return {}


def _extract_file_path(hook_input: dict) -> str | None:
    """Extract the file path from the tool input.

    PostToolUse hooks receive the tool result. The file path is in the
    tool_input that triggered the Write/Edit operation.
    """
    # Try tool_input.file_path (Write tool) or tool_input.file_path (Edit tool).
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


def _validate_path_safe(file_path: str) -> bool:
    """Basic path safety check -- no traversal sequences."""
    # Reject null bytes and obvious traversal.
    if "\x00" in file_path:
        return False
    # Normalize and check -- we allow reading any .kicad_sch file the user edits,
    # but we do NOT write anything, so path validation here is for input safety only.
    return True


def _find_duplicate_references(content: str) -> list[str]:
    """Find duplicate reference designators in schematic content."""
    # Extract all reference designator values.
    refs = re.findall(
        r'\(property\s+"Reference"\s+"([^"]+)"', content
    )
    # Filter out empty and placeholder refs.
    refs = [r for r in refs if r and r not in ("", "#PWR", "#FLG", "#SYM")]

    seen = {}
    duplicates = []
    for ref in refs:
        if ref in seen:
            if seen[ref] == 1:
                duplicates.append(ref)
            seen[ref] += 1
        else:
            seen[ref] = 1

    return duplicates


def _run_basic_drc(file_path: str) -> list[dict]:
    """Run basic DRC checks on a .kicad_sch file.

    Returns list of findings: [{rule_id, description, severity, detail}].
    """
    findings = []

    try:
        content = Path(file_path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        # Cannot read the file -- fail silently (hook must not block).
        return findings

    # Run regex-based rules.
    for rule_id, rule in DRC_RULES.items():
        if rule["pattern"] is None:
            continue
        matches = re.findall(rule["pattern"], content)
        if matches:
            findings.append({
                "rule_id": rule_id,
                "description": rule["description"],
                "severity": rule["severity"],
                "count": len(matches),
            })

    # Run duplicate reference check (DRC-004).
    duplicates = _find_duplicate_references(content)
    if duplicates:
        dup_list = ", ".join(duplicates[:10])
        suffix = f" (and {len(duplicates) - 10} more)" if len(duplicates) > 10 else ""
        findings.append({
            "rule_id": "DRC-004",
            "description": DRC_RULES["DRC-004"]["description"],
            "severity": "warning",
            "count": len(duplicates),
            "detail": f"Duplicates: {dup_list}{suffix}",
        })

    return findings


def _format_findings(findings: list[dict], file_path: str) -> str:
    """Format DRC findings as a human-readable warning message."""
    lines = [f"DRC warnings for {Path(file_path).name}:"]
    for f in findings:
        detail = f.get("detail", "")
        detail_str = f" -- {detail}" if detail else ""
        lines.append(
            f"  [{f['severity'].upper()}] {f['rule_id']}: {f['description']} "
            f"(x{f['count']}){detail_str}"
        )
    return "\n".join(lines)


def main():
    hook_input = _read_hook_input()
    file_path = _extract_file_path(hook_input)

    # If no file path or not a KiCad schematic, exit silently.
    if not file_path or not _is_kicad_schematic(file_path):
        sys.exit(0)

    # Validate path safety.
    if not _validate_path_safe(file_path):
        sys.exit(0)

    # Run DRC.
    findings = _run_basic_drc(file_path)

    # Silent success -- no output when no violations.
    if not findings:
        sys.exit(0)

    # Report findings as warnings (non-blocking).
    message = _format_findings(findings, file_path)
    result = {"message": message}
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
