"""Shared helpers for delivery-team hook scripts.

Implements the Claude Code hook I/O protocol so every hook in this plugin
reads and writes the same way:

- Input: one JSON object on stdin (``hook_event_name``, ``tool_name``,
  ``tool_input``, ``tool_response``, ``cwd``, ``transcript_path`` ...).
- Allow: exit 0. Optional JSON on stdout carries ``systemMessage`` (shown to
  the user) and ``hookSpecificOutput.additionalContext`` (fed to the model).
- Block: exit 2 with the reason on stderr.

Stdlib only. Never raises on malformed input: a hook that cannot parse its
payload must fail open (allow), not crash the tool call.

History: this module was referenced by six hooks from the start but was
never committed because the repository ``.gitignore`` ignores every ``lib/``
directory. It was reconstructed from the call sites; see CHANGELOG.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

_EVENT_NAME: str | None = None

# Events whose protocol defines a hookSpecificOutput object. Stop/SubagentStop
# carry only continue/stopReason/systemMessage.
_EVENTS_WITH_SPECIFIC_OUTPUT = {"PreToolUse", "PostToolUse", "UserPromptSubmit", "SessionStart"}


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
def read_hook_input() -> dict[str, Any]:
    """Parse the hook payload from stdin. Returns {} on any failure."""
    global _EVENT_NAME
    try:
        raw = sys.stdin.read() if sys.stdin is not None else ""
        data = json.loads(raw) if raw and raw.strip() else {}
    except Exception:  # never raise on a malformed payload; fail open
        data = {}
    if not isinstance(data, dict):
        data = {}
    event = data.get("hook_event_name")
    _EVENT_NAME = event if isinstance(event, str) else None
    return data


def get_tool_name(hook_input: dict[str, Any]) -> str:
    name = hook_input.get("tool_name", "")
    return name if isinstance(name, str) else ""


def get_tool_input(hook_input: dict[str, Any]) -> dict[str, Any]:
    tool_input = hook_input.get("tool_input", {})
    return tool_input if isinstance(tool_input, dict) else {}


def get_tool_result(hook_input: dict[str, Any]) -> str:
    """Return the PostToolUse tool response as text.

    Claude Code sends ``tool_response``; older payloads used ``tool_result``.
    Dict responses are flattened to their text content so callers can run
    string checks (e.g. the ``SKILL_LOADED:`` marker scan).
    """
    result = hook_input.get("tool_response", hook_input.get("tool_result"))
    return _to_text(result)


def get_cwd(hook_input: dict[str, Any]) -> Path:
    cwd = hook_input.get("cwd")
    if isinstance(cwd, str) and cwd:
        return Path(cwd)
    return Path(os.getcwd())


def get_transcript_path(hook_input: dict[str, Any]) -> Path | None:
    path = hook_input.get("transcript_path")
    if isinstance(path, str) and path:
        return Path(path)
    return None


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        content = value.get("content", value.get("output", value.get("text")))
        if content is not None:
            return _to_text(content)
        try:
            return json.dumps(value)
        except (TypeError, ValueError):
            return str(value)
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict) and "text" in item:
                parts.append(str(item["text"]))
            else:
                parts.append(_to_text(item))
        return "\n".join(p for p in parts if p)
    return str(value)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def emit_response(
    message: str | None = None,
    continue_: bool = True,
    hook_specific: dict[str, Any] | None = None,
) -> None:
    """Write a hook JSON response to stdout without exiting.

    ``message`` is surfaced both as ``systemMessage`` (user-visible) and as
    ``hookSpecificOutput.additionalContext`` (model-visible) when the event
    name is known. ``continue_=False`` asks Claude Code to stop after the
    tool call. Extra ``hook_specific`` keys are merged into
    ``hookSpecificOutput`` (e.g. ``permissionDecision`` for PreToolUse).
    """
    payload: dict[str, Any] = {"continue": bool(continue_)}
    if message:
        payload["systemMessage"] = message
        if not continue_:
            payload["stopReason"] = message
    specific: dict[str, Any] = {}
    if _EVENT_NAME in _EVENTS_WITH_SPECIFIC_OUTPUT:
        specific["hookEventName"] = _EVENT_NAME
        if message:
            specific["additionalContext"] = message
    if hook_specific:
        specific.update(hook_specific)
    if specific:
        payload["hookSpecificOutput"] = specific
    try:
        sys.stdout.write(json.dumps(payload))
        sys.stdout.flush()
    except OSError:
        pass


def exit_success() -> None:
    """Allow the tool call and stop the hook."""
    sys.exit(0)


def exit_block(reason: str) -> None:
    """Exit 2 with the reason on stderr.

    Exit 2 blocks the action for PreToolUse, UserPromptSubmit, Stop and
    SubagentStop; for PostToolUse the tool has already run and the reason is
    fed back to the model instead. Encodes with replacement so a non-ASCII
    path or tool output cannot turn the block into a traceback on a cp1252
    Windows console.
    """
    try:
        encoding = getattr(sys.stderr, "encoding", None) or "utf-8"
        buffer = getattr(sys.stderr, "buffer", None)
        if buffer is not None:
            buffer.write(reason.encode(encoding, "replace"))
        else:
            sys.stderr.write(reason.encode(encoding, "replace").decode(encoding, "replace"))
        sys.stderr.flush()
    except Exception:
        pass
    sys.exit(2)


__all__ = [
    "read_hook_input",
    "get_tool_name",
    "get_tool_input",
    "get_tool_result",
    "get_cwd",
    "get_transcript_path",
    "emit_response",
    "exit_success",
    "exit_block",
]
