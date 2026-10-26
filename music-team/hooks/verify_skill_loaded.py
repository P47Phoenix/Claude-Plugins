#!/usr/bin/env python3
"""PostToolUse hook (matcher: Agent): verify a music-team sub-agent's hand-back.

Acts only on music-team dispatches. Warns (``systemMessage``, exit 0) when the reply lacks a
``SKILL_LOADED:`` line near the top, lacks the ``STATUS:`` / ``ARTIFACT:`` / ``SUMMARY:``
block, or has a ``SUMMARY:`` longer than 200 characters. Never blocks; never crashes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hook_common as hc  # noqa: E402

SUMMARY_MAX = 200


def check(text: str) -> list[str]:
    problems = []
    if "SKILL_LOADED:" not in "\n".join(text.splitlines()[:10]):
        problems.append("no SKILL_LOADED: line in the first lines (the agent may not have loaded its references)")
    missing = []
    status = re.search(r"^STATUS:[ \t]*(DONE|BLOCKED)\b", text, re.M)
    if not status:
        missing.append("STATUS: DONE|BLOCKED")
    if not re.search(r"^ARTIFACT:", text, re.M):
        missing.append("ARTIFACT:")
    summary = re.search(r"^SUMMARY:[ \t]*(.*)$", text, re.M)
    if not summary:
        missing.append("SUMMARY:")
    if missing:
        problems.append("hand-back block incomplete, missing " + ", ".join(missing))
    if summary and len(summary.group(1).strip()) > SUMMARY_MAX:
        problems.append(f"SUMMARY is {len(summary.group(1).strip())} characters (max {SUMMARY_MAX}); move detail into the artifact")
    return problems


def main() -> None:
    data = hc.read_input()
    if data.get("tool_name") not in ("Agent", "Task"):
        return
    skill = hc.music_skill(data)
    if skill is None:
        return
    text = hc.response_text(data)
    problems = check(text) if text.strip() else ["empty sub-agent reply"]
    if problems:
        hc.emit_message(f"WARNING (music-team, {skill}): " + "; ".join(problems) + ". Consider re-dispatching once.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"music-team verify_skill_loaded: internal error ({exc}); allowing", file=sys.stderr)
    sys.exit(0)
