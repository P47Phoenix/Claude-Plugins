#!/usr/bin/env python3
"""Smoke-test runner CLI. Exit codes: 0=pass, 1=outcome-fail, 2=cost-cap, 3=timeout, 4=plumbing."""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path


def _here() -> Path:
    return Path(__file__).resolve().parent


def _repo_root_from(here: Path) -> Path:
    # tests/smoke/run_smoke.py → tests/smoke → tests → delivery-team → <repo>
    return here.parent.parent.parent


def _utc_timestamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _build_parser() -> argparse.ArgumentParser:
    here = _here()
    repo_root = _repo_root_from(here)

    parser = argparse.ArgumentParser(
        prog="run_smoke.py",
        description="Delivery-team plugin smoke-test runner. Local-only.",
    )
    parser.add_argument(
        "--init-baseline",
        action="store_true",
        help="Run scenario 5× sequentially and write baseline JSON.",
    )
    parser.add_argument(
        "--cost-cap",
        type=float,
        default=3.00,
        help="Hard cumulative cost cap in USD (default: 3.00).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1800,
        help="Wall-clock timeout in seconds (default: 1800).",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=here / "baselines" / "hello_world_spike.json",
        help="Path to baseline JSON for regression comparison.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=here / "artifacts",
        help="Root artifacts directory (a <utc-timestamp>/ subdir is created per run).",
    )
    parser.add_argument(
        "--prompt",
        type=Path,
        default=here / "prompts" / "hello_world_spike.txt",
        help="Path to prompt text file fed to the spawned Claude subprocess.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=here / "fixtures" / "delivery_config_minimal.yml",
        help="Path to minimal .delivery/config.yml fixture installed into the mktemp HOME.",
    )
    parser.add_argument(
        "--stream-fixture",
        type=Path,
        default=None,
        help="Path to a fixture stream-json file (skips spawning Claude — cost-cap + meta-test path).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=repo_root,
        help="Repo root (default: derived from this script's location).",
    )
    return parser


def _read_prompt(prompt_path: Path) -> str:
    if not prompt_path.is_file():
        return ""
    return prompt_path.read_text(encoding="utf-8")


def _execute_single_run(args, run_out_dir: Path) -> tuple[int, dict]:
    """Run one scenario and write artifacts. Returns (exit_code, report_dict)."""
    from lib.runner import run_pipeline
    from lib.metrics import parse_stream
    from lib.aggregator import aggregate
    from lib.report import build_report, write_report
    from lib.workspace import Workspace
    from lib.baseline import compare as compare_to_baseline

    run_out_dir.mkdir(parents=True, exist_ok=True)
    stream_path = run_out_dir / "stream.jsonl"
    run_id = f"smoke-{run_out_dir.name}"

    prompt_text = _read_prompt(args.prompt)

    plugin_path = (args.repo_root / "delivery-team").resolve()
    workspace = Workspace(
        repo_root=args.repo_root.resolve(),
        plugin_path=plugin_path,
        config_fixture=args.config.resolve(),
    )

    advisory_warnings: list[str] = []
    hard_failures: list[str] = []
    exit_code = 0

    try:
        workspace.setup()
        run_result = run_pipeline(
            prompt=prompt_text,
            workspace=workspace,
            cost_cap=args.cost_cap,
            timeout=args.timeout,
            stream_path=stream_path,
            stream_fixture=args.stream_fixture,
            prompt_path=args.prompt,
        )

        events = run_result.get("events", [])
        outcome = run_result.get("outcome", {"success": False, "exit_code": 4, "reason": "no-outcome"})

        metrics = parse_stream(events)
        if not metrics.wall_clock_seconds:
            metrics.wall_clock_seconds = float(run_result.get("elapsed_seconds", 0.0))

        aggregator_dict = aggregate(workspace, metrics)

        outcome_reason = outcome.get("reason")
        if outcome_reason == "cost-cap-exceeded":
            hard_failures.append("cost-cap exceeded mid-stream")
            exit_code = 2
        elif outcome_reason == "timeout":
            hard_failures.append("subprocess wall-clock exceeded --timeout")
            exit_code = 3
        elif outcome.get("success") is False:
            exit_code = 1

        baseline_dict: dict | None = None
        if args.baseline.is_file():
            try:
                baseline_dict = json.loads(args.baseline.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                baseline_dict = None

        report = build_report(
            run_id=run_id,
            repo_root=args.repo_root.resolve(),
            plugin_load_strategy=workspace.plugin_load_strategy,
            outcome=outcome,
            metrics=metrics,
            aggregator_dict=aggregator_dict,
            advisory_warnings=advisory_warnings,
            hard_failures=hard_failures,
        )

        if baseline_dict is not None and exit_code == 0:
            rr = compare_to_baseline(report, baseline_dict)
            if rr.hard_failures:
                report["hard_failures"].extend(rr.hard_failures)
                exit_code = 1
            if rr.advisory_warnings:
                report["advisory_warnings"].extend(rr.advisory_warnings)

        write_report(run_out_dir, report, stream_path)
        return exit_code, report
    finally:
        workspace.cleanup()


def _init_baseline_flow(args) -> int:
    from lib.baseline import init_baseline

    reports: list[dict] = []
    for i in range(1, 6):
        ts = _utc_timestamp()
        run_dir = args.out_dir / f"{ts}-init-{i}"
        code, report = _execute_single_run(args, run_dir)
        reports.append(report)
        if code in (2, 3, 4):
            print(
                f"run_smoke: --init-baseline aborted on sample {i} (exit_code={code})",
                file=sys.stderr,
            )
            return code

    try:
        init_baseline(reports, args.baseline)
    except Exception as exc:
        print(f"run_smoke: baseline write failed: {exc}", file=sys.stderr)
        return 4

    print(f"run_smoke: baseline written to {args.baseline}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    args.out_dir = Path(args.out_dir).resolve()
    args.baseline = Path(args.baseline).resolve()
    args.prompt = Path(args.prompt).resolve()
    args.config = Path(args.config).resolve()
    args.repo_root = Path(args.repo_root).resolve()
    if args.stream_fixture is not None:
        args.stream_fixture = Path(args.stream_fixture).resolve()

    sys.path.insert(0, str(_here()))

    if args.init_baseline:
        return _init_baseline_flow(args)

    ts = _utc_timestamp()
    run_dir = args.out_dir / ts
    exit_code, _ = _execute_single_run(args, run_dir)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
