#!/usr/bin/env python3
"""Backstop for the bible-research verification gate.

Reads a Stop or SubagentStop hook payload on stdin and blocks only when the
final message delivers gated output (sermon-builder shortlist or breakdown,
research timeline, song-ideas list or findings, idea-team review report)
without a closing "Verification notes" section, or leaks the pre-correction
draft. A hook can only block or continue; it cannot rewrite output (see
DESIGN_NOTES.md), so the gate itself lives in the skills.

Usage: gate_check.py stop | verifier
Exit 0 always; a block is expressed as JSON on stdout.
"""
import json
import re
import sys

NOTES = re.compile(r"verification notes", re.IGNORECASE)
DRAFT_MARKER = re.compile(r"INTERNAL DRAFT", re.IGNORECASE)
# Markers of sermon-builder output delivered to the user.
SHORTLIST = re.compile(r"\*\*Why it fits:?\*\*|Why it fits:", re.IGNORECASE)
BREAKDOWN = re.compile(r"Original Context", re.IGNORECASE)
BREAKDOWN2 = re.compile(r"Original-Language Notes", re.IGNORECASE)
# Per-check reports the verifier must not return.
REPORT_MARKERS = [
    re.compile(r"^#\s*Citation Checklist", re.MULTILINE),
    re.compile(r"^#\s*Claims Checked", re.MULTILINE),
    re.compile(r"^#\s*Flagged Claims", re.MULTILINE),
    re.compile(r"^#\s*Doctrinal Concerns", re.MULTILINE),
]
# Markers of research and idea-team output delivered to the user: the
# contract's top-level heading (case-insensitive, up to two leading words on
# the same line, then a colon or dash) AND the contract's header line, so a
# project plan titled "# Timeline: Q3" in another session is never gated.
# Keep in step with references/contracts/.
SEP = r"[ \t]*[:\-–—]"  # colon, hyphen, en dash, em dash
FENCE = re.compile(r"```.*?```", re.DOTALL)


def _heading(name: str) -> "re.Pattern[str]":
    return re.compile(r"^#[ \t]*(?:\w+[ \t]+){0,2}" + name + SEP, re.MULTILINE | re.IGNORECASE)


def _marker(label: str) -> "re.Pattern[str]":
    # Accept **Label:**, **Label**: and plain Label: alike.
    return re.compile(r"\*{0,2}" + label + r"\*{0,2}[ \t]*:", re.IGNORECASE)


GATED_CONTRACTS = [
    (_heading("Timeline"), _marker("Eras covered")),
    (_heading("Song Ideas"), _marker("Eras covered")),
    (_heading("Idea Review"), _marker("Personas")),
    (_heading("Research Findings"), _marker("Question shape")),
]


def block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}))


def has_closing_notes(text: str) -> bool:
    """True if a 'Verification notes' heading appears in the last part of the message."""
    tail = text[-3000:]
    return bool(NOTES.search(tail))


def read_payload():
    """Read the JSON payload as UTF-8 regardless of the console code page.

    On Windows, sys.stdin decodes as cp1252 by default, which garbles dashes,
    Hebrew and Greek in the message and makes the heading patterns miss.
    """
    try:
        raw = sys.stdin.buffer.read()
    except (AttributeError, OSError):
        raw = sys.stdin.read().encode("utf-8", errors="replace")
    return json.loads(raw.decode("utf-8", errors="replace"))


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "stop"
    try:
        payload = read_payload()
    except (ValueError, OSError):
        return 0
    if not isinstance(payload, dict):
        return 0
    # Never block twice in a row: a repeated block can loop.
    if payload.get("stop_hook_active"):
        return 0
    text = payload.get("last_assistant_message") or ""
    if not text:
        return 0

    if mode == "verifier":
        if DRAFT_MARKER.search(text):
            block("Remove the 'INTERNAL DRAFT' marker. Return only the corrected draft in the corrected-draft contract, ending in Verification notes.")
        elif any(p.search(text) for p in REPORT_MARKERS):
            block("Do not return per-check reports. Return only the corrected draft in the corrected-draft contract, ending in Verification notes (minimum one line).")
        elif not has_closing_notes(text):
            block("The corrected draft must end with a Verification notes section (minimum one line). Add it.")
        return 0

    # mode == "stop": main-thread reply
    delivers_builder_output = bool(SHORTLIST.search(text)) or (
        bool(BREAKDOWN.search(text)) and bool(BREAKDOWN2.search(text))
    )
    unfenced = FENCE.sub("", text)  # a contract shown as an example in a code block is not delivery
    delivers_gated_output = delivers_builder_output or any(
        heading.search(unfenced) and marker.search(unfenced)
        for heading, marker in GATED_CONTRACTS
    )
    if not delivers_gated_output:
        return 0
    if DRAFT_MARKER.search(text):
        block("The pre-correction draft must never reach the user. Run the sermon-verification gate and return only the corrected version.")
    elif not has_closing_notes(text):
        block("The verification gate did not complete: sermon-builder, research and idea-team output must pass the sermon-verification gate and end with Verification notes. Run the gate, then return only the corrected version.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
