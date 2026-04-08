#!/usr/bin/env python3
"""PreToolUse hook: Audit Agent tool prompts for content leakage and compound roles."""
import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.hook_utils import read_hook_input, emit_response, exit_success, get_tool_name, get_tool_input


# Compound multi-role detection patterns (OD-10).
# Triggers a non-blocking warning when a single Agent prompt tries to
# collapse multiple reviewer/challenger/role identities into one dispatch.
_ROLE_LINE_RE = re.compile(r"^\s*ROLE:\s*\S+", re.MULTILINE)
_ALSO_ACT_AS_RE = re.compile(
    r"\b(also\s+act\s+as|then\s+act\s+as|additionally[,\s]+(play|act\s+as)|and\s+also\s+play)\b",
    re.IGNORECASE,
)
_YOU_ARE_MULTI_RE = re.compile(
    r"you\s+are\s+(?:a\s+|an\s+|the\s+)?[\w\- ]{3,40}\b.{0,200}?\byou\s+are\s+(?:also\s+)?(?:a\s+|an\s+|the\s+)?[\w\- ]{3,40}",
    re.IGNORECASE | re.DOTALL,
)
# Negation guard: "do not act as both", "never act as both", "don't also act as",
# "must not play multiple roles", etc. — these are anti-patterns warning the agent
# AGAINST compound roles, not requesting them. They should NOT trigger the warning.
_NEGATION_RE = re.compile(
    r"\b(do\s+not|don'?t|never|must\s+not|should\s+not|shouldn'?t|cannot|can'?t|no(?:t)?\s+allowed\s+to)\b",
    re.IGNORECASE,
)


def _is_negated(prompt: str, match_start: int, window: int = 60) -> bool:
    """Return True if a negation word appears within `window` chars before the match."""
    snippet = prompt[max(0, match_start - window):match_start]
    return bool(_NEGATION_RE.search(snippet))


def _detect_compound_roles(prompt: str) -> str | None:
    """Return a warning message if the prompt appears to fuse multiple roles."""
    # Multiple ROLE: declarations in one prompt.
    role_matches = _ROLE_LINE_RE.findall(prompt)
    if len(role_matches) > 1:
        return (
            f"{len(role_matches)} `ROLE:` declarations detected in a single Agent "
            "prompt. One role = one sub-agent invocation. Dispatch each reviewer/"
            "challenger/evaluator role as a SEPARATE Agent tool call."
        )
    # "Also act as" / "then act as" / "additionally play" phrasing.
    also_match = _ALSO_ACT_AS_RE.search(prompt)
    if also_match and not _is_negated(prompt, also_match.start()):
        return (
            "Compound-role phrasing detected (e.g., 'also act as', 'then act as'). "
            "Never collapse multiple roles into one compound prompt. Dispatch each "
            "role as a separate Agent tool call."
        )
    # Two "You are <role>" declarations close together.
    you_are_match = _YOU_ARE_MULTI_RE.search(prompt)
    if you_are_match and not _is_negated(prompt, you_are_match.start()):
        return (
            "Two 'You are ...' role declarations detected in a single Agent prompt. "
            "This is a compound multi-role invocation. Dispatch each role as a "
            "separate Agent tool call."
        )
    return None


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

    # Compound multi-role detection (OD-10). Non-blocking warning.
    compound_warning = _detect_compound_roles(prompt)
    if compound_warning:
        warnings.append(compound_warning)

    if warnings:
        emit_response(
            message="ISOLATION AUDIT WARNING: " + " ".join(warnings) +
            " The orchestrator should pass artifact FILE PATHS, not content, "
            "and dispatch each role as its own sub-agent. "
            "See two-channel communication and 'One Role = One Sub-Agent'."
        )

    exit_success()


if __name__ == "__main__":
    main()
