"""Shared helpers for music-team hook scripts. Stdlib only; never raises on bad input.

Hook protocol: one JSON object on stdin; exit 0 allows; exit 2 blocks with the reason on
stderr; optional JSON on stdout carries ``systemMessage`` or ``hookSpecificOutput``.
Every music-team hook acts only on music-team dispatches and fails open on any error.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SHARED = PLUGIN_ROOT / "references" / "shared"

MUSIC_SKILLS = {
    "music-flow", "music-brief", "lyricist", "composer", "arranger", "adapter",
    "song-critic", "music-release", "music-memory",
}
MUSIC_AGENTS = {"lyricist", "composer", "arranger", "song-critic", "adapter"}

_HEADER_SCAN = 1500  # the SKILL:/ROLE: header sits at the very top of a dispatch prompt


def read_input() -> dict[str, Any]:
    """Parse stdin JSON. On failure note it on stderr and return {} (caller exits 0)."""
    try:
        raw = sys.stdin.read() if sys.stdin is not None else ""
        data = json.loads(raw) if raw and raw.strip() else {}
    except Exception as exc:  # noqa: BLE001 - fail open on any malformed payload
        print(f"music-team hook: could not parse stdin ({exc}); allowing", file=sys.stderr)
        return {}
    if not isinstance(data, dict):
        print("music-team hook: stdin is not a JSON object; allowing", file=sys.stderr)
        return {}
    return data


def tool_input(data: dict[str, Any]) -> dict[str, Any]:
    ti = data.get("tool_input")
    return ti if isinstance(ti, dict) else {}


def prompt_of(data: dict[str, Any]) -> str:
    p = tool_input(data).get("prompt")
    return p if isinstance(p, str) else ""


def header_field(prompt: str, key: str) -> str | None:
    m = re.search(rf"^[ \t]*{key}:[ \t]*([A-Za-z0-9_-]+)", prompt[:_HEADER_SCAN], re.M)
    return m.group(1) if m else None


def music_skill(data: dict[str, Any]) -> str | None:
    """Return the music-team skill or agent name the dispatch targets, else None."""
    skill = header_field(prompt_of(data), "SKILL")
    if skill in MUSIC_SKILLS:
        return skill
    sub = tool_input(data).get("subagent_type")
    if isinstance(sub, str) and sub in MUSIC_AGENTS:
        return sub
    return None


def response_text(data: dict[str, Any]) -> str:
    """Flatten a PostToolUse tool_response (string, dict, or content list) into text."""
    def walk(node: Any) -> list[str]:
        if isinstance(node, str):
            return [node]
        if isinstance(node, list):
            return [t for item in node for t in walk(item)]
        if isinstance(node, dict):
            if isinstance(node.get("text"), str):
                return [node["text"]]
            out: list[str] = []
            for key in ("content", "result", "output", "response"):
                if key in node:
                    out.extend(walk(node[key]))
            return out
        return []
    resp = data.get("tool_response", data.get("tool_result", ""))
    return "\n".join(walk(resp))


def emit_message(message: str) -> None:
    print(json.dumps({"systemMessage": message}))
