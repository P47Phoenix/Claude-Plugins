"""Baseline init + regression detector. Mirrors check_skill_budgets.py exit convention."""
from __future__ import annotations

import json
import statistics
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


SCHEMA_VERSION = "2"


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
    "tokens.cache_hit_ratio",
)

MODEL_USAGE_PREFIX = "model_usage."


class ModelMovedError(Exception):
    """Raised when model_resolved[0] differs between samples (ADR-lmr-004 s2)."""


class BaselineSchemaError(Exception):
    """Raised by load_baseline on a schema_version other than "2" (ADR-lmr-004 s2)."""


def _primary(report: dict) -> str | None:
    resolved = report.get("model_resolved")
    if isinstance(resolved, list) and resolved and isinstance(resolved[0], str):
        return resolved[0]
    return None


def check_model_consistency(reports: list[dict]) -> None:
    """Raise ModelMovedError, naming both models, when model_resolved[0] differs."""
    first: str | None = None
    for rpt in reports:
        cur = _primary(rpt)
        if first is None:
            first = cur
            continue
        if cur != first:
            raise ModelMovedError(
                f"model moved between samples: {first} vs {cur}; "
                "the baseline must be re-captured with one model"
            )


def load_baseline(path: Path) -> dict:
    """Load a baseline JSON; reject any schema_version other than "2"."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    version = data.get("schema_version") if isinstance(data, dict) else None
    if version != SCHEMA_VERSION:
        raise BaselineSchemaError(
            f"baseline schema_version {version!r} != {SCHEMA_VERSION!r}; "
            "re-capture the baseline with run_smoke.py --init-baseline (never merged)"
        )
    return data


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
    if key.startswith(MODEL_USAGE_PREFIX):
        return "informational"
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

    model_keys: set[str] = set()
    for rpt in reports:
        for entry in rpt.get("model_usage") or []:
            m = entry.get("model") if isinstance(entry, dict) else None
            if isinstance(m, str) and m and m != "unknown":
                model_keys.add(m)
    for m in sorted(model_keys):
        values = []
        for rpt in reports:
            count = 0
            for entry in rpt.get("model_usage") or []:
                if isinstance(entry, dict) and entry.get("model") == m:
                    count = entry.get("dispatches", 0) or 0
                    break
            values.append(float(count))
        bucket[f"{MODEL_USAGE_PREFIX}{m}.dispatches"] = values

    return bucket


def _message_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(e, dict) and e.get("type") == "assistant" and isinstance(e.get("message"), dict):
            mid = e["message"].get("id")
            if isinstance(mid, str) and mid:
                ids.add(mid)
    return ids


def _check_distinct_samples(reports: list[dict]) -> list[dict]:
    """Reject copied streams (same hash, session_id or overlapping message.id); return samples[]."""
    import hashlib

    samples: list[dict] = []
    hashes: set[str] = set()
    sessions: set[str] = set()
    seen_ids: set[str] = set()
    for i, rpt in enumerate(reports, 1):
        sf = rpt.get("stream_file")
        if not sf or not Path(sf).is_file():
            raise ValueError(f"init_baseline: sample {i} has no readable stream_file ({sf!r})")
        path = Path(sf)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in hashes:
            raise ValueError(f"init_baseline: sample {i} stream has the same sha256 as an earlier sample (copied stream)")
        hashes.add(digest)
        sid = rpt.get("session_id")
        if sid:
            if sid in sessions:
                raise ValueError(f"init_baseline: sample {i} repeats session_id {sid!r} (copied stream)")
            sessions.add(sid)
        ids = _message_ids(path)
        if ids & seen_ids:
            raise ValueError(f"init_baseline: sample {i} shares message.id values with an earlier sample (copied stream)")
        seen_ids |= ids
        samples.append({"stream_file": str(sf), "stream_sha256": digest})
    return samples


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

    check_model_consistency(reports)
    samples = _check_distinct_samples(reports)

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

    first = reports[0]
    host = dict(first.get("host_context") or {})
    cli_version = host.get("claude_code_version") or _claude_cli_version()
    host["claude_code_version"] = cli_version

    baseline = {
        "schema_version": SCHEMA_VERSION,
        "scenario": "hello_world_spike",
        "sample_status": "active",
        "n_samples": n,
        "last_captured_utc": _now_utc_iso(),
        "last_captured_git_sha": _git_sha(),
        "last_captured_cli_version": cli_version,
        "model_requested": first.get("model_requested"),
        "model_resolved": list(first.get("model_resolved") or []),
        "model_pin_env": dict(first.get("model_pin_env") or {}),
        "effort": first.get("effort"),
        "host_context": host,
        "samples": samples,
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
    strict_model: bool = False,
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

    base_models = baseline.get("model_resolved")
    base_primary = base_models[0] if isinstance(base_models, list) and base_models else None
    run_primary = _primary(report)
    if base_primary and run_primary and base_primary != run_primary:
        text = f"model moved: baseline={base_primary} run={run_primary}"
        if strict_model:
            hard_failures.append(f"{text}; the baseline must be re-captured")
        else:
            advisory_warnings.append(f"{text} (baseline should be re-captured)")

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
