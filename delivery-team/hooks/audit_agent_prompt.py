#!/usr/bin/env python3
"""PreToolUse hook: Audit Agent tool prompts for content leakage."""
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.hook_utils import read_hook_input, emit_response, exit_success, get_tool_name, get_tool_input


def main():
    hook_input = read_hook_input()

    if get_tool_name(hook_input) != "Agent":
        exit_success()

    tool_input = get_tool_input(hook_input)
    prompt = tool_input.get("prompt", "")

    if not prompt:
        exit_success()

    warnings = []

    # Check for code fences (likely pasting artifact content)
    code_fence_count = prompt.count("```")
    if code_fence_count > 2:
        warnings.append(
            f"Code fences detected in agent prompt ({code_fence_count} found) — "
            f"may indicate artifact content being pasted instead of file paths."
        )

    # Check prompt length
    if len(prompt) > 5000:
        warnings.append(
            f"Agent prompt is very long ({len(prompt)} chars) — "
            f"may indicate content leakage. Prefer passing file paths."
        )

    if warnings:
        emit_response(
            message="ISOLATION AUDIT WARNING: " + " ".join(warnings) +
            " The orchestrator should pass artifact FILE PATHS, not content. "
            "See two-channel communication model."
        )

    exit_success()


if __name__ == "__main__":
    main()
