#!/usr/bin/env python3
"""PostToolUse hook: Detect when KiCad project files are modified and notify
the user.

Triggered on Write/Edit operations. Checks if the modified file is a KiCad
project file (.kicad_sch, .kicad_pcb, .kicad_pro) and emits a notification
so downstream hooks (drc_check.py, bom_drift.py) and the user are aware of
the change.

This hook runs before drc_check.py and bom_drift.py in the PostToolUse chain
(see hooks.json ordering). It provides the notification layer; DRC and BOM
drift hooks provide the validation layer.

Security: All input parsed via json.loads(). No shell=True. Paths validated.
Per SEC-06, all environment variables treated as untrusted input.
"""
import json
import os
import sys
from pathlib import Path


# KiCad file extensions to watch.
KICAD_EXTENSIONS = {
    ".kicad_sch": "schematic",
    ".kicad_pcb": "PCB layout",
    ".kicad_pro": "project",
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


def _get_kicad_file_type(file_path: str) -> str | None:
    """Return the KiCad file type description if the file is a KiCad file,
    or None if it is not."""
    lower_path = file_path.lower()
    for ext, file_type in KICAD_EXTENSIONS.items():
        if lower_path.endswith(ext):
            return file_type
    return None


def _validate_path_safe(file_path: str) -> bool:
    """Basic path safety check -- no null bytes."""
    if "\x00" in file_path:
        return False
    return True


def main():
    hook_input = _read_hook_input()
    file_path = _extract_file_path(hook_input)

    # If no file path, exit silently.
    if not file_path:
        sys.exit(0)

    # Validate path safety.
    if not _validate_path_safe(file_path):
        sys.exit(0)

    # Check if the file is a KiCad project file.
    file_type = _get_kicad_file_type(file_path)
    if file_type is None:
        # Not a KiCad file -- exit silently.
        sys.exit(0)

    # KiCad file modified -- emit notification.
    file_name = Path(file_path).name
    message = (
        f"KiCad {file_type} modified: {file_name}\n"
        f"  Downstream hooks (DRC check, BOM drift) will validate this change."
    )

    result = {"message": message}
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
