#!/usr/bin/env python3
"""PreToolUse hook: Skill-load telemetry — writes one JSONL row per Skill invocation.

Schema v1 per ADR-tk0e-001. Never raises; always exits 0.
Supports --dry-run flag (no file write; used for overhead benchmarking).
"""
import datetime
import hashlib
import json
import os
import sys
import uuid
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TELEMETRY_FILE = ".delivery/telemetry/skill-loads.jsonl"
SKILL_ROOT = "delivery-team/skills"
SKILL_FILENAME = "SKILL.md"
PREFIX_READ_BYTES = 2048

# Map from marketplace skill name segment to directory under SKILL_ROOT.
# e.g. "delivery-team:developer" → "developer"
# Paradigm sub-skills: "delivery-team:architect/ddd" → "architect/paradigms/ddd"
_PARADIGM_MAP = {
    "ddd": "architect/paradigms/ddd",
    "volatility": "architect/paradigms/volatility",
}


def _resolve_skill_md(skill_name: str, cwd: Path) -> Path | None:
    """Return the Path to SKILL.md for the given marketplace skill name, or None."""
    # Strip plugin prefix if present (e.g. "delivery-team:developer" → "developer")
    segment = skill_name.split(":")[-1] if ":" in skill_name else skill_name

    # Check paradigm shortcut
    if segment in _PARADIGM_MAP:
        candidate = cwd / SKILL_ROOT / _PARADIGM_MAP[segment] / SKILL_FILENAME
    else:
        candidate = cwd / SKILL_ROOT / segment / SKILL_FILENAME

    return candidate if candidate.is_file() else None


def _compute_prefix_hash(skill_md: Path) -> str | None:
    """Return sha256[:8] of first PREFIX_READ_BYTES of SKILL.md, or None on error."""
    try:
        data = skill_md.read_bytes()[:PREFIX_READ_BYTES]
        return hashlib.sha256(data).hexdigest()[:8]
    except Exception:
        return None


def _iso_utc() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def _build_row(skill_name: str, prefix_hash: str | None, hook_input: dict) -> dict:
    """Construct the telemetry JSONL row.

    W3-18 hardening: PreToolUse hooks fire BEFORE token usage is observable
    (the model has not yet dispatched). So token fields are emitted as
    placeholders (`placeholder=true`) per PRD §FR-7.6 — downstream KPI
    compute (W3-10) MUST exclude rows where `placeholder == true`.

    `prose_tokens` is recorded ONLY when the hook input includes a
    `prose_tokens` field (e.g. PostToolUse enrichment from a wrapper).
    Pipeline-id (when present in cwd's `.delivery/state.md` frontmatter or
    in the hook environment) is captured for run-scoped summary aggregation.
    """
    session_id = os.environ.get("CLAUDE_SESSION_ID", "unknown")
    model = os.environ.get("CLAUDE_MODEL", None)
    pipeline_id = os.environ.get("DELIVERY_PIPELINE_ID", None) or hook_input.get("pipeline_id")

    # If hook_input carries actual measurements (PostToolUse-style enrichment),
    # capture them and clear the placeholder flag.
    prose_tokens = hook_input.get("prose_tokens")
    input_tokens = hook_input.get("input_tokens")
    cache_read = hook_input.get("cache_read_tokens")
    cache_write = hook_input.get("cache_write_tokens")
    has_measurement = any(
        v is not None and v != 0 for v in (prose_tokens, input_tokens, cache_read, cache_write)
    )

    return {
        "version": "1",
        "timestamp": _iso_utc(),
        "session_id": session_id,
        "skill": skill_name,
        "model": model,
        "prefix_hash": prefix_hash,
        "pipeline_id": pipeline_id,
        "prose_tokens": prose_tokens if prose_tokens is not None else 0,
        "input_tokens": input_tokens if input_tokens is not None else 0,
        "cache_read_tokens": cache_read if cache_read is not None else 0,
        "cache_write_tokens": cache_write if cache_write is not None else 0,
        "placeholder": not has_measurement,
    }


def _write_row(row: dict, cwd: Path) -> None:
    """Append one JSONL row to the telemetry file. Flushes immediately."""
    telemetry_path = cwd / TELEMETRY_FILE
    os.makedirs(str(telemetry_path.parent), exist_ok=True)
    with open(str(telemetry_path), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")
        fh.flush()


def main() -> None:
    """Main entry point; never raises."""
    dry_run = "--dry-run" in sys.argv

    try:
        raw = sys.stdin.read()
        hook_input = json.loads(raw) if raw.strip() else {}

        tool_name = hook_input.get("tool_name", "")
        if tool_name != "Skill":
            sys.exit(0)

        tool_input = hook_input.get("tool_input", {})
        # Claude Code sends the skill identifier in field "skill" or "skill_name"
        skill_name = (
            tool_input.get("skill")
            or tool_input.get("skill_name")
            or ""
        )
        if not skill_name:
            sys.exit(0)

        cwd = Path(hook_input.get("cwd", ".")).resolve()

        # Resolve prefix_hash from disk — ADR-tk0e-001 option (a)
        skill_md = _resolve_skill_md(skill_name, cwd)
        prefix_hash = _compute_prefix_hash(skill_md) if skill_md else None

        row = _build_row(skill_name, prefix_hash, hook_input)

        # EARLY write (before any optional enrichment) — memory lesson 3
        if not dry_run:
            _write_row(row, cwd)

    except Exception as exc:
        print(f"telemetry.py: non-fatal error: {exc}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
