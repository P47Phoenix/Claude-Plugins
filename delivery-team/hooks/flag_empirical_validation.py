#!/usr/bin/env python3
"""SubagentStop hook: Flag acceptance criteria requiring empirical validation."""
import json
import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.hook_utils import read_hook_input, emit_response, exit_success, get_transcript_path


# Empirical validation keyword patterns
PATTERNS = [
    # Visual / Rendering
    r'renders?|displays?|visible|appears?(?:\s+on\s+screen)?|shows?|hides?|layout|responsive|animated|animation\s+plays',
    # User Interaction
    r'clicks?|taps?|swipes?|drags?|scrolls?|hovers?|selects?|triggers\s+action|input\s+handling|gesture|touch',
    # Runtime Behavior
    r'returns\s+\d{3}|responds\s+with|fires|executes|processes|plays|navigates\s+to|redirects|loads\s+correctly|streams',
    # Physics / Simulation
    r'collision|physics|gravity|velocity|raycast|pathfinding|navigation|AI\s+behaves|spawns\s+at|moves\s+to',
    # Audio / Media
    r'sound\s+plays|audio|music|video\s+plays',
]

COMBINED_PATTERN = re.compile('|'.join(f'({p})' for p in PATTERNS), re.IGNORECASE)

AC_PATTERN = re.compile(
    r'acceptance|criteria|given|when|then|should|must|shall|verify|validate|test\s+that',
    re.IGNORECASE
)


def main():
    hook_input = read_hook_input()
    transcript_path = get_transcript_path(hook_input)

    if not transcript_path:
        exit_success()

    # Extract text content from transcript
    try:
        transcript = json.loads(transcript_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        exit_success()

    content_lines = []
    for entry in transcript:
        if entry.get("role") in ("user", "assistant"):
            content = entry.get("content", "")
            if isinstance(content, str):
                content_lines.append(content)
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        content_lines.append(item.get("text", ""))

    if not content_lines:
        exit_success()

    # Filter to acceptance criteria sections
    full_text = "\n".join(content_lines)
    ac_lines = [line for line in full_text.splitlines() if AC_PATTERN.search(line)]

    if not ac_lines:
        exit_success()

    ac_text = "\n".join(ac_lines[:50])

    # Find empirical matches
    matches = set()
    for match in COMBINED_PATTERN.finditer(ac_text):
        matches.add(match.group(0).strip())

    if not matches:
        exit_success()

    match_list = "\n".join(f'  - "{m}"' for m in sorted(matches))
    count = len(matches)

    emit_response(
        message=(
            f"EMPIRICAL VALIDATION REQUIRED: This sub-agent task includes {count} "
            f"acceptance criteria keyword(s) requiring runtime verification:\n"
            f"{match_list}\n\n"
            f"ACTION: Mark these as 'Requires runtime validation' in Verification Status. "
            f"Story status should be CODE_COMPLETE (not DONE). Carry forward to UAT. "
            f"See the quality skill's references/empirical-validation.md for recommended validation approaches."
        )
    )
    exit_success()


if __name__ == "__main__":
    main()
