#!/usr/bin/env python3
"""PostToolUse hook: Validate GDScript files after Write/Edit."""
import subprocess
import shutil
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.hook_utils import read_hook_input, exit_success, exit_block, get_tool_input


def main():
    hook_input = read_hook_input()
    tool_input = get_tool_input(hook_input)

    file_path = tool_input.get("file_path", "")
    if not file_path or not file_path.endswith(".gd"):
        exit_success()

    if not Path(file_path).exists():
        exit_success()

    # Check if godot is available
    godot_path = shutil.which("godot")
    if not godot_path:
        exit_success()  # Godot not on PATH, skip silently

    # Run parse validation (requires Godot 4.2+)
    try:
        result = subprocess.run(
            [godot_path, "--headless", "--check-only", "--script", file_path],
            capture_output=True, text=True, timeout=15
        )
        output = result.stdout + result.stderr
    except (subprocess.TimeoutExpired, OSError):
        exit_success()  # Timeout or error running godot, skip

    # Check for errors
    if any(kw in output.lower() for kw in ("error", "script error", "parse error")):
        # Truncate output for the error message
        error_lines = output.strip().splitlines()[:20]
        error_text = "\\n".join(error_lines)
        exit_block(f"GDScript parse error in {file_path}:\\n{error_text}")

    exit_success()


if __name__ == "__main__":
    main()
