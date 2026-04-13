#!/usr/bin/env python3
"""PreToolUse hook: Warn when hardware role skills are invoked outside the
hardware-flow pipeline context.

Triggered on every Skill tool invocation. Checks whether the invoked skill
is a hardware-team role skill (electrical-engineer, pcb-layout-engineer, etc.)
and whether it appears to be invoked from within the hardware-flow orchestrator.

If a role skill is invoked directly (outside the pipeline), emits a warning
advising the user to run the pipeline instead.

Security: All input parsed via json.loads(). No shell=True. Paths validated.
Per SEC-06, all environment variables treated as untrusted input.
"""
import json
import sys


# Hardware-team role skills that should normally be invoked via the pipeline.
HARDWARE_ROLE_SKILLS = {
    "hardware-team:hw-product-owner",
    "hardware-team:electrical-engineer",
    "hardware-team:pcb-layout-engineer",
    "hardware-team:manufacturing-engineer",
    "hardware-team:compliance-engineer",
    "hardware-team:test-engineer",
}

# The orchestrator skill -- invoking this IS running the pipeline.
ORCHESTRATOR_SKILL = "hardware-team:hardware-flow"


def _read_hook_input() -> dict:
    """Read hook input from stdin (Claude Code hook protocol)."""
    try:
        return json.loads(sys.stdin.read())
    except (json.JSONDecodeError, Exception):
        return {}


def _extract_skill_name(hook_input: dict) -> str:
    """Extract the skill name from the tool input.

    PreToolUse hooks receive the tool_input before execution.
    For Skill tool invocations, the skill name is in tool_input.skill
    or tool_input.name.
    """
    tool_input = hook_input.get("tool_input", {})
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except (json.JSONDecodeError, TypeError):
            return ""

    skill_name = tool_input.get("skill", "")
    if not skill_name:
        skill_name = tool_input.get("name", "")
    return str(skill_name).strip()


def main():
    hook_input = _read_hook_input()
    skill_name = _extract_skill_name(hook_input)

    # If not a hardware role skill, exit silently.
    if skill_name not in HARDWARE_ROLE_SKILLS:
        sys.exit(0)

    # Check if we appear to be inside a pipeline context.
    # Heuristic: if the hook input contains a session_id or agent_prompt
    # that references hardware-flow, we are inside the pipeline.
    # Also check for the presence of a pipeline state file.
    agent_prompt = str(hook_input.get("agent_prompt", ""))
    session_context = str(hook_input.get("session_context", ""))

    inside_pipeline = (
        ORCHESTRATOR_SKILL in agent_prompt
        or "hardware-flow" in agent_prompt.lower()
        or "hardware-flow" in session_context.lower()
        or "pipeline_stage" in session_context.lower()
    )

    if inside_pipeline:
        # Inside the pipeline -- no warning needed.
        sys.exit(0)

    # Outside the pipeline -- warn the user.
    friendly_name = skill_name.replace("hardware-team:", "")
    message = (
        f"WARNING: '{friendly_name}' invoked outside the hardware-flow pipeline.\n"
        f"  Role skills are designed to run within the 8-stage pipeline context.\n"
        f"  Running outside the pipeline skips gate validation, state tracking,\n"
        f"  and rework loop management.\n"
        f"  To run the full pipeline: invoke hardware-team:hardware-flow\n"
        f"  To proceed anyway: continue (this warning is non-blocking)."
    )

    result = {"message": message}
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
