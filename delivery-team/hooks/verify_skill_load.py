#!/usr/bin/env python3
"""PostToolUse hook: Verify sub-agents loaded the expected skill."""
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.hook_utils import read_hook_input, emit_response, exit_success, get_tool_name, get_tool_result


def main():
    hook_input = read_hook_input()

    if get_tool_name(hook_input) != "Agent":
        exit_success()

    result = get_tool_result(hook_input)
    if not result:
        exit_success()

    # Check first 5 lines for SKILL_LOADED marker
    first_lines = "\n".join(result.splitlines()[:5])
    if "SKILL_LOADED:" in first_lines:
        exit_success()

    emit_response(
        message=(
            "WARNING: Sub-agent did not confirm skill loading (no SKILL_LOADED marker in output). "
            "The agent may not have loaded its designated skill references. "
            "Consider retrying the delegation."
        )
    )
    exit_success()


if __name__ == "__main__":
    main()
