#!/usr/bin/env python3
"""PreToolUse hook (matcher: Agent): audit music-team sub-agent prompts.

Acts only on music-team dispatches (a ``SKILL: <music-team skill>`` header or a music-team
``subagent_type``). Denies (exit 2 plus a PreToolUse deny decision) when:

1. the ``<!-- originality-policy -->`` block or the policy clause is missing;
2. a ``blocked-targets.txt`` entry appears in the prompt (single-word entries are
   case-sensitive, multi-word entries case-insensitive; the literal
   ``<!-- memory-lessons -->`` marker is ignored; lines that are bare list entries,
   as pasted by the challenger, are ignored);
3. the references declared on the ``SKILL_LOADED:`` line (or, without one, found in the
   prompt) exceed ``prompt-allowances.json`` for the dispatched ROLE.

Any other prompt, a malformed payload, or any internal error allows (exit 0).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hook_common as hc  # noqa: E402

POLICY_MARKER = "<!-- originality-policy -->"
POLICY_HEADER = "ORIGINALITY POLICY (non-negotiable)"
MARKERS = (POLICY_MARKER, "<!-- memory-lessons -->")
KINDS = {
    "genres": re.compile(r"genres/[A-Za-z0-9_&.+-]+?\.md"),
    "techniques": re.compile(r"techniques/[A-Za-z0-9_&.+-]+?\.md"),
    "rubrics": re.compile(r"rubrics/[A-Za-z0-9_&.+-]+?\.md"),
    "personas": re.compile(r"personas/[A-Za-z0-9_&.+-]+?\.md"),
}


def load_blocked() -> list[str]:
    path = hc.SHARED / "blocked-targets.txt"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    return [l.strip() for l in lines if l.strip() and not l.lstrip().startswith("#")]


def blocking_enabled() -> bool:
    cfg = Path(".song") / "config.yml"
    try:
        return not re.search(r"^\s*block_artist_references:\s*false\b", cfg.read_text(encoding="utf-8"), re.M)
    except OSError:
        return True


def blocked_hits(prompt: str, entries: list[str]) -> list[str]:
    for m in MARKERS:
        prompt = prompt.replace(m, "")
    entry_set = set(entries)
    # Bare list entries and "#" comment lines are a pasted blocked-targets.txt (challenger), not style targets.
    kept = [l for l in prompt.splitlines() if l.strip() not in entry_set and not l.lstrip().startswith("#")]
    text = "\n".join(kept)
    hits = []
    for entry in entries:
        flags = 0 if " " not in entry else re.I
        pat = r"(?<![A-Za-z0-9])" + re.escape(entry) + r"(?![A-Za-z0-9])"
        if re.search(pat, text, flags):
            hits.append(entry)
    return hits


def allowance_for(role: str | None) -> dict:
    try:
        manifest = json.loads((hc.SHARED / "prompt-allowances.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    allow = dict(manifest.get("defaults", {}))
    if role:
        allow.update(manifest.get("roles", {}).get(role, {}))
    return allow


def declared_text(prompt: str) -> str:
    for line in prompt.splitlines():
        if "SKILL_LOADED:" in line and "references/" in line:
            return line
    return prompt


def over_allowance(prompt: str, role: str | None) -> list[str]:
    allow = allowance_for(role)
    scope = declared_text(prompt)
    problems = []
    for kind, pat in KINDS.items():
        found = set(pat.findall(scope))
        limit = allow.get(kind)
        if isinstance(limit, int) and len(found) > limit:
            problems.append(f"{len(found)} {kind} references pasted for role {role or 'default'} (allowance {limit})")
    return problems


def deny(reasons: list[str]) -> None:
    reason = "music-team prompt audit: " + "; ".join(reasons)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))
    print(reason, file=sys.stderr)
    sys.exit(2)


def main() -> None:
    data = hc.read_input()
    if data.get("tool_name") not in ("Agent", "Task"):
        return
    if hc.music_skill(data) is None:
        return
    prompt = hc.prompt_of(data)
    reasons: list[str] = []
    if POLICY_MARKER not in prompt or POLICY_HEADER not in prompt:
        reasons.append("originality-policy block missing (marker and clause are required in every music-team dispatch)")
    if blocking_enabled():
        hits = blocked_hits(prompt, load_blocked())
        if hits:
            reasons.append("blocked style target(s) in prompt: " + ", ".join(hits[:5]))
    reasons.extend(over_allowance(prompt, hc.header_field(prompt, "ROLE")))
    if reasons:
        deny(reasons)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - a hook must never crash the tool call
        print(f"music-team audit_agent_prompt: internal error ({exc}); allowing", file=sys.stderr)
    sys.exit(0)
