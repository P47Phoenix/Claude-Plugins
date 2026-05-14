"""Workspace artifact reader: telemetry jsonl + run-summary + state.md merger."""
from __future__ import annotations

import json
import re
import warnings
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .metrics import Metrics
    from .workspace import Workspace


SKILL_LOADS_REL = ".delivery/telemetry/skill-loads.jsonl"
RUN_SUMMARY_GLOB = ".delivery/telemetry/run-summary-*.json"
STATE_MD_REL = ".delivery/state.md"


def _read_skill_loads(path: Path) -> list[dict]:
    """Read .delivery/telemetry/skill-loads.jsonl. Missing-file returns []."""
    if not path.is_file():
        return []

    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for idx, raw in enumerate(fh):
            text = raw.strip()
            if not text:
                continue
            try:
                obj = json.loads(text)
            except json.JSONDecodeError as exc:
                warnings.warn(
                    f"aggregator: skill-loads line {idx} malformed ({exc}); skipping",
                    stacklevel=2,
                )
                continue
            if isinstance(obj, dict):
                rows.append(obj)
    return rows


def _aggregate_skill_loads(rows: list[dict]) -> list[dict]:
    """Collapse jsonl rows to per-skill (skill, count, prose_tokens_mean).

    Placeholder rows are excluded per W3-18 semantics in telemetry.py.
    """
    counts: dict[str, int] = defaultdict(int)
    prose_sum: dict[str, float] = defaultdict(float)
    prose_n: dict[str, int] = defaultdict(int)

    for row in rows:
        if row.get("placeholder") is True:
            continue
        skill = row.get("skill")
        if not skill:
            continue
        counts[skill] += 1
        prose = row.get("prose_tokens")
        if isinstance(prose, (int, float)) and prose > 0:
            prose_sum[skill] += float(prose)
            prose_n[skill] += 1

    out: list[dict] = []
    for skill in sorted(counts.keys()):
        mean = (prose_sum[skill] / prose_n[skill]) if prose_n[skill] > 0 else None
        out.append({
            "skill": skill,
            "count": counts[skill],
            "prose_tokens_mean": mean,
        })
    return out


def _newest_run_summary(workspace_home: Path) -> Path | None:
    telemetry_dir = workspace_home / ".delivery" / "telemetry"
    if not telemetry_dir.is_dir():
        return None
    candidates = sorted(telemetry_dir.glob("run-summary-*.json"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _read_run_summary(path: Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        warnings.warn(f"aggregator: run-summary {path} unreadable ({exc})", stacklevel=2)
        return {}


def _parse_state_md(path: Path) -> dict:
    """Extract stages_completed, human_checkpoints_passed, stories_completed, defects_logged from state.md.

    Tolerant of missing file / missing keys — returns zeros where data is absent.
    """
    result = {
        "stages_completed": 0,
        "human_checkpoints_passed": 0,
        "stories_completed": 0,
        "defects_logged": 0,
    }
    if not path.is_file():
        return result

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        warnings.warn(f"aggregator: state.md unreadable ({exc})", stacklevel=2)
        return result

    m_stages = re.search(r"stages_completed\s*:\s*(\d+)", text)
    if m_stages:
        result["stages_completed"] = int(m_stages.group(1))

    m_chk = re.search(r"human_checkpoints_passed\s*:\s*(\d+)", text)
    if m_chk:
        result["human_checkpoints_passed"] = int(m_chk.group(1))

    m_defects = re.search(r"defects_logged\s*:\s*(\d+)", text)
    if m_defects:
        result["defects_logged"] = int(m_defects.group(1))

    story_section = re.search(
        r"##\s*Stories?\b(.*?)(?:\n##\s|\Z)",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if story_section:
        body = story_section.group(1)
        done_count = len(re.findall(r"^\s*-\s*\[x\]\s+", body, flags=re.MULTILINE | re.IGNORECASE))
        if done_count:
            result["stories_completed"] = done_count
        else:
            m_stories = re.search(r"stories_completed\s*:\s*(\d+)", text)
            if m_stories:
                result["stories_completed"] = int(m_stories.group(1))
    else:
        m_stories = re.search(r"stories_completed\s*:\s*(\d+)", text)
        if m_stories:
            result["stories_completed"] = int(m_stories.group(1))

    return result


def aggregate(workspace: "Workspace", metrics: "Metrics") -> dict:
    """Merge telemetry + state.md + metrics into one report-ready dict."""
    if workspace.home is None:
        raise RuntimeError("aggregate() requires Workspace.setup() to have run")

    skill_load_rows = _read_skill_loads(workspace.home / "work" / SKILL_LOADS_REL)
    if not skill_load_rows:
        skill_load_rows = _read_skill_loads(workspace.home / SKILL_LOADS_REL)
    skill_loads = _aggregate_skill_loads(skill_load_rows)

    summary_path = _newest_run_summary(workspace.home / "work")
    if summary_path is None:
        summary_path = _newest_run_summary(workspace.home)
    run_summary = _read_run_summary(summary_path)

    state_data = _parse_state_md(workspace.home / "work" / STATE_MD_REL)
    if state_data["stages_completed"] == 0 and state_data["stories_completed"] == 0:
        fallback = _parse_state_md(workspace.home / STATE_MD_REL)
        if fallback["stages_completed"] or fallback["stories_completed"]:
            state_data = fallback

    pipeline = {
        "stages_completed": state_data["stages_completed"],
        "stories_completed": state_data["stories_completed"],
        "dispatch_count": metrics.dispatch_count,
        "defects_logged": state_data["defects_logged"],
    }

    overall = run_summary.get("overall") if isinstance(run_summary, dict) else None
    if isinstance(overall, dict) and overall.get("rows_real") is not None:
        # Run-summary signal is informational; primary dispatch_count source is stream metrics.
        pipeline["telemetry_rows_real"] = overall.get("rows_real")

    return {
        "skill_loads": skill_loads,
        "pipeline": pipeline,
        "run_summary_present": summary_path is not None,
        "state_md_present": (workspace.home / "work" / STATE_MD_REL).is_file()
        or (workspace.home / STATE_MD_REL).is_file(),
    }
