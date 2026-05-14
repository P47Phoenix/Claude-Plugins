"""Baseline init + regression detector. Mirrors check_skill_budgets.py exit convention."""
from __future__ import annotations

import json
import statistics
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


SCHEMA_VERSION = "1"


HARD_METRIC_KEYS = (
    "wall_clock_seconds",
    "cost_usd",
    "pipeline.dispatch_count",
    "pipeline.stories_completed",
)

ADVISORY_METRIC_KEYS = (
    "tokens.input",
    "tokens.output",
    "tokens.cache_creation",
    "tokens.cache_read",
)


@dataclass
class RegressionResult:
    """Outcome of a single report-vs-baseline comparison."""
    status: Literal["PASS", "FAIL", "WARN"]
    hard_failures: list[str] = field(default_factory=list)
    advisory_warnings: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)


def _extract_metric(report: dict, dotted_key: str):
    cursor = report
    for part in dotted_key.split("."):
        if not isinstance(cursor, dict):
            return None
        cursor = cursor.get(part)
    return cursor


def _classify(key: str) -> str:
    if key in HARD_METRIC_KEYS:
        return "hard"
    return "advisory"


def _git_sha() -> str | None:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None
    if r.returncode != 0:
        return None
    return (r.stdout or "").strip() or None


def _claude_cli_version() -> str | None:
    try:
        r = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None
    if r.returncode != 0:
        return None
    return (r.stdout or r.stderr or "").strip() or None


def _now_utc_iso() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def _collect_metric_values(reports: list[dict]) -> dict[str, list[float]]:
    """Walk reports; pull each known metric + each skill_loads.<skill> count."""
    bucket: dict[str, list[float]] = {}

    fixed_keys = list(HARD_METRIC_KEYS) + list(ADVISORY_METRIC_KEYS)
    for key in fixed_keys:
        values: list[float] = []
        for rpt in reports:
            v = _extract_metric(rpt, key)
            if isinstance(v, (int, float)):
                values.append(float(v))
        if values:
            bucket[key] = values

    skill_keys: set[str] = set()
    for rpt in reports:
        for entry in rpt.get("skill_loads") or []:
            sk = entry.get("skill")
            if isinstance(sk, str):
                skill_keys.add(sk)
    for sk in sorted(skill_keys):
        values = []
        for rpt in reports:
            count = 0
            for entry in rpt.get("skill_loads") or []:
                if entry.get("skill") == sk:
                    count = entry.get("count", 0)
                    break
            values.append(float(count))
        bucket[f"skill_loads.{sk}"] = values

    return bucket


def _hard_max_for(key: str, mean: float) -> float | None:
    """Architecture §6 hard_max table."""
    if key == "wall_clock_seconds":
        return 1800.0
    if key == "cost_usd":
        return 3.00
    if key == "pipeline.dispatch_count":
        return 16.0
    if key == "pipeline.stories_completed":
        return max(1.0, mean)
    return None


def init_baseline(reports: list[dict], out_path: Path) -> None:
    """Compute mean+stddev per metric across N reports; write baseline JSON.

    n ≥ 1 enforced. stddev with n==1 emits 0.0.
    """
    if not reports:
        raise ValueError("init_baseline: at least one report required")

    n = len(reports)
    bucketed = _collect_metric_values(reports)

    metrics_block: dict[str, dict] = {}
    for key, values in bucketed.items():
        mean = statistics.fmean(values) if values else 0.0
        stddev = statistics.pstdev(values) if len(values) > 1 else 0.0
        classification = _classify(key)
        entry: dict = {
            "mean": mean,
            "stddev": stddev,
            "n": len(values),
            "classification": classification,
        }
        if classification == "hard":
            hm = _hard_max_for(key, mean)
            if hm is not None:
                entry["hard_max"] = hm
        metrics_block[key] = entry

    baseline = {
        "schema_version": SCHEMA_VERSION,
        "scenario": "hello_world_spike",
        "n_samples": n,
        "last_captured_utc": _now_utc_iso(),
        "last_captured_git_sha": _git_sha(),
        "last_captured_cli_version": _claude_cli_version(),
        "metrics": metrics_block,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")


def _check_hard_rules(report: dict, baseline: dict) -> list[str]:
    """Architecture §7 hard-fail rules. Returns list of rule strings violated."""
    failures: list[str] = []

    outcome = report.get("outcome") or {}
    if outcome.get("success") is False:
        reason = outcome.get("reason")
        failures.append(f"outcome.success=false (reason={reason!r})")

    metrics_block = baseline.get("metrics") or {}

    for key in HARD_METRIC_KEYS:
        meta = metrics_block.get(key) or {}
        observed = _extract_metric(report, key)
        if observed is None:
            if meta.get("classification") == "hard":
                failures.append(f"{key}: missing from report (hard-classed)")
            continue

        hard_max = meta.get("hard_max")
        if key == "pipeline.stories_completed":
            expected = meta.get("mean")
            if isinstance(expected, (int, float)) and float(observed) != float(expected):
                failures.append(
                    f"pipeline.stories_completed mismatch: report={observed} baseline_mean={expected}"
                )
            continue

        if isinstance(hard_max, (int, float)) and float(observed) > float(hard_max):
            failures.append(
                f"{key} exceeds hard_max: report={observed} hard_max={hard_max}"
            )

    return failures


def _check_advisory_rules(
    report: dict,
    baseline: dict,
    advisory_metrics: set[str] | None = None,
) -> list[str]:
    """Architecture §7 ±2σ advisory rules. Returns list of warning strings."""
    warnings_list: list[str] = []
    metrics_block = baseline.get("metrics") or {}

    candidate_keys = list(ADVISORY_METRIC_KEYS)
    for k in metrics_block.keys():
        if k.startswith("skill_loads."):
            candidate_keys.append(k)

    if advisory_metrics is not None:
        candidate_keys = [k for k in candidate_keys if k in advisory_metrics]

    for key in candidate_keys:
        meta = metrics_block.get(key)
        if not meta:
            continue
        mean = meta.get("mean")
        stddev = meta.get("stddev")
        if not isinstance(mean, (int, float)) or not isinstance(stddev, (int, float)):
            continue

        if key.startswith("skill_loads."):
            skill_name = key.split(".", 1)[1]
            observed = None
            for entry in report.get("skill_loads") or []:
                if entry.get("skill") == skill_name:
                    observed = entry.get("count")
                    break
            if observed is None:
                continue
        else:
            observed = _extract_metric(report, key)
            if not isinstance(observed, (int, float)):
                continue

        # Zero-stddev guard: only emit if value differs from mean exactly.
        if stddev == 0:
            if float(observed) != float(mean):
                warnings_list.append(
                    f"{key} differs from zero-variance baseline: report={observed} mean={mean}"
                )
            continue

        lower = mean - 2.0 * stddev
        upper = mean + 2.0 * stddev
        if float(observed) < lower or float(observed) > upper:
            warnings_list.append(
                f"{key} outside mean±2σ: report={observed} mean={mean} stddev={stddev}"
            )

    return warnings_list


def compare(
    report: dict,
    baseline: dict,
    *,
    hard_metrics: set[str] | None = None,
    advisory_metrics: set[str] | None = None,
) -> RegressionResult:
    """Diff a report against a baseline. Returns RegressionResult.

    Exit-code intent (consumed by run_smoke.py):
        PASS → exit 0
        FAIL → exit 1 (hard-fail)
        WARN → exit 0 (advisory only)
    """
    _ = hard_metrics

    hard_failures = _check_hard_rules(report, baseline)
    advisory_warnings = _check_advisory_rules(report, baseline, advisory_metrics)

    if hard_failures:
        status: Literal["PASS", "FAIL", "WARN"] = "FAIL"
    elif advisory_warnings:
        status = "WARN"
    else:
        status = "PASS"

    return RegressionResult(
        status=status,
        hard_failures=hard_failures,
        advisory_warnings=advisory_warnings,
        details={
            "baseline_n_samples": baseline.get("n_samples"),
            "baseline_captured_utc": baseline.get("last_captured_utc"),
        },
    )
