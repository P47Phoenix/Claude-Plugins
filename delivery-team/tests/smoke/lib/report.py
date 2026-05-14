"""Report writer: report.json + summary.md + stream.jsonl copy/symlink."""
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import asdict, is_dataclass
from pathlib import Path

from .metrics import Metrics, ModelUsage


SCHEMA_VERSION = "1"


def _git_sha(repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=5,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None
    if result.returncode != 0:
        return None
    out = (result.stdout or "").strip()
    return out or None


def _claude_cli_version() -> str | None:
    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None
    if result.returncode != 0:
        return None
    out = (result.stdout or result.stderr or "").strip()
    return out or None


def _model_usage_dicts(usage: list[ModelUsage]) -> list[dict]:
    out: list[dict] = []
    for u in usage:
        if is_dataclass(u):
            out.append(asdict(u))
        elif isinstance(u, dict):
            out.append(u)
    return out


def build_report(
    *,
    run_id: str,
    repo_root: Path,
    plugin_load_strategy: str | None,
    outcome: dict,
    metrics: Metrics,
    aggregator_dict: dict,
    advisory_warnings: list[str] | None = None,
    hard_failures: list[str] | None = None,
) -> dict:
    """Assemble the schema-v1 report dict per architecture §5."""
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "git_sha": _git_sha(repo_root),
        "claude_cli_version": _claude_cli_version(),
        "plugin_load_strategy": plugin_load_strategy,
        "outcome": {
            "success": bool(outcome.get("success", False)),
            "exit_code": int(outcome.get("exit_code", 0)),
            "reason": outcome.get("reason"),
        },
        "wall_clock_seconds": float(metrics.wall_clock_seconds),
        "cost_usd": float(metrics.cost_usd),
        "tokens": {
            "input": int(metrics.tokens.get("input", 0)),
            "output": int(metrics.tokens.get("output", 0)),
            "cache_creation": int(metrics.tokens.get("cache_creation", 0)),
            "cache_read": int(metrics.tokens.get("cache_read", 0)),
        },
        "model_usage": _model_usage_dicts(metrics.model_usage),
        "pipeline": {
            "stages_completed": int(aggregator_dict.get("pipeline", {}).get("stages_completed", 0)),
            "stories_completed": int(aggregator_dict.get("pipeline", {}).get("stories_completed", 0)),
            "dispatch_count": int(aggregator_dict.get("pipeline", {}).get("dispatch_count", metrics.dispatch_count)),
            "defects_logged": int(aggregator_dict.get("pipeline", {}).get("defects_logged", 0)),
        },
        "skill_loads": list(aggregator_dict.get("skill_loads", [])),
        "advisory_warnings": list(advisory_warnings or []),
        "hard_failures": list(hard_failures or []),
    }


def _render_summary_md(report: dict) -> str:
    outcome = report.get("outcome", {})
    success = outcome.get("success")
    banner = "PASS" if success else "FAIL"
    tokens = report.get("tokens", {})
    pipeline = report.get("pipeline", {})

    lines: list[str] = []
    lines.append(f"# Smoke-test run — {report.get('run_id', '?')}")
    lines.append("")
    lines.append(f"**Outcome**: {banner}  (exit_code={outcome.get('exit_code')}, reason={outcome.get('reason')})")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| wall_clock_seconds | {report.get('wall_clock_seconds')} |")
    lines.append(f"| cost_usd | {report.get('cost_usd')} |")
    lines.append(f"| tokens.input | {tokens.get('input')} |")
    lines.append(f"| tokens.output | {tokens.get('output')} |")
    lines.append(f"| tokens.cache_creation | {tokens.get('cache_creation')} |")
    lines.append(f"| tokens.cache_read | {tokens.get('cache_read')} |")
    lines.append(f"| pipeline.stages_completed | {pipeline.get('stages_completed')} |")
    lines.append(f"| pipeline.stories_completed | {pipeline.get('stories_completed')} |")
    lines.append(f"| pipeline.dispatch_count | {pipeline.get('dispatch_count')} |")
    lines.append(f"| pipeline.defects_logged | {pipeline.get('defects_logged')} |")
    lines.append(f"| git_sha | {report.get('git_sha')} |")
    lines.append(f"| claude_cli_version | {report.get('claude_cli_version')} |")
    lines.append(f"| plugin_load_strategy | {report.get('plugin_load_strategy')} |")
    lines.append("")

    skills = report.get("skill_loads") or []
    if skills:
        lines.append("## Skill loads")
        lines.append("")
        lines.append("| Skill | Count | Prose tokens (mean) |")
        lines.append("|---|---|---|")
        for s in skills:
            lines.append(f"| {s.get('skill')} | {s.get('count')} | {s.get('prose_tokens_mean')} |")
        lines.append("")

    hard = report.get("hard_failures") or []
    advisory = report.get("advisory_warnings") or []
    if hard:
        lines.append("## Hard failures")
        for h in hard:
            lines.append(f"- {h}")
        lines.append("")
    if advisory:
        lines.append("## Advisory warnings")
        for a in advisory:
            lines.append(f"- {a}")
        lines.append("")

    return "\n".join(lines) + "\n"


def write_report(out_dir: Path, report: dict, stream_path: Path) -> None:
    """Write report.json + summary.md + place stream.jsonl into out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)

    report_path = out_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    summary_path = out_dir / "summary.md"
    summary_path.write_text(_render_summary_md(report), encoding="utf-8")

    dest_stream = out_dir / "stream.jsonl"
    if stream_path.is_file() and stream_path.resolve() != dest_stream.resolve():
        shutil.copy2(str(stream_path), str(dest_stream))
    elif not dest_stream.exists():
        dest_stream.write_text("", encoding="utf-8")
