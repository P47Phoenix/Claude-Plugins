"""Shared pytest fixtures for smoke-test meta-tests.

Producer-validator separation per ADR-tk5-001: this conftest and the tests
that load it MUST exercise the producer modules (`lib/metrics.py`,
`lib/baseline.py`, `lib/aggregator.py`) as artifacts only. No imports happen
until inside a fixture/test body, and no Claude subprocesses may be spawned
(see the `_block_claude_subprocess` autouse guard).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


# --- Path discovery ----------------------------------------------------------

@pytest.fixture(scope="session")
def smoke_root() -> Path:
    """Absolute path to `delivery-team/tests/smoke/`."""
    # tests/conftest.py -> tests -> smoke
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def repo_root(smoke_root: Path) -> Path:
    """Absolute path to the repo root (containing .delivery/ and delivery-team/)."""
    # smoke -> tests -> delivery-team -> <repo>
    return smoke_root.parent.parent.parent


@pytest.fixture(scope="session", autouse=True)
def lib_path(smoke_root: Path) -> Path:
    """Insert `delivery-team/tests/smoke/` onto sys.path so `import lib.metrics` works.

    Autouse + session-scoped so every test in this package can import the
    producer modules without per-test boilerplate.
    """
    smoke_str = str(smoke_root)
    if smoke_str not in sys.path:
        sys.path.insert(0, smoke_str)
    return smoke_root


# --- No-Claude / no-subprocess guard ----------------------------------------

@pytest.fixture(autouse=True)
def _block_claude_subprocess(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail loudly if any test spawns a `claude` subprocess.

    Architecture binding: meta-tests must not invoke Claude Code. This guard
    monkeypatches `subprocess.Popen` and `subprocess.run` to raise
    `AssertionError` for any command whose first token is `claude` (or whose
    string form starts with `claude `).
    """
    import subprocess

    real_popen = subprocess.Popen
    real_run = subprocess.run

    def _is_claude_cmd(cmd) -> bool:
        if cmd is None:
            return False
        if isinstance(cmd, (list, tuple)) and cmd:
            head = str(cmd[0])
        else:
            head = str(cmd)
        # Strip path components so "/usr/local/bin/claude" still matches.
        leaf = head.rsplit("/", 1)[-1]
        return leaf == "claude" or leaf.startswith("claude ")

    def _guarded_popen(cmd, *args, **kwargs):
        if _is_claude_cmd(cmd):
            raise AssertionError(
                f"meta-tests must not spawn claude (attempted: {cmd!r})"
            )
        return real_popen(cmd, *args, **kwargs)

    def _guarded_run(cmd, *args, **kwargs):
        if _is_claude_cmd(cmd):
            raise AssertionError(
                f"meta-tests must not spawn claude (attempted: {cmd!r})"
            )
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr(subprocess, "Popen", _guarded_popen)
    monkeypatch.setattr(subprocess, "run", _guarded_run)


# --- Sample stream events ----------------------------------------------------

@pytest.fixture
def valid_stream_events() -> list[dict]:
    """Three well-formed stream-json events with usage blocks.

    Used to verify that `parse_stream` aggregates a happy-path stream and
    that fault-injection tests can mix valid + malformed events.
    """
    return [
        {
            "type": "assistant",
            "timestamp_seconds": 1000.0,
            "model": "claude-opus-4-7",
            "usage": {
                "input_tokens": 100,
                "output_tokens": 200,
                "cache_creation_input_tokens": 10,
                "cache_read_input_tokens": 20,
                "cost_usd": 0.10,
            },
        },
        {
            "type": "assistant",
            "timestamp_seconds": 1005.0,
            "model": "claude-opus-4-7",
            "usage": {
                "input_tokens": 150,
                "output_tokens": 250,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 30,
                "cost_usd": 0.15,
            },
        },
        {
            "type": "result",
            "timestamp_seconds": 1010.0,
            "model": "claude-opus-4-7",
            "usage": {
                "input_tokens": 50,
                "output_tokens": 75,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
                "cost_usd": 0.05,
            },
        },
    ]


@pytest.fixture
def malformed_stream_event() -> dict:
    """A single malformed event: `usage` key is a string, not a dict.

    Per `lib/metrics.py` contract, this must emit `warnings.warn(...)` and
    be skipped — never raise.
    """
    return {
        "type": "assistant",
        "timestamp_seconds": 1007.5,
        "model": "claude-opus-4-7",
        "usage": "not-a-dict-this-is-broken",
    }


# --- Sample baseline + reports for compare() --------------------------------

@pytest.fixture
def synthetic_baseline() -> dict:
    """A baseline JSON dict shaped per architecture §6.

    Includes `wall_clock_seconds`, `cost_usd` (hard with hard_max=3.00),
    `pipeline.dispatch_count` (hard), `pipeline.stories_completed` (hard),
    and `tokens.input` / `tokens.output` (advisory) — enough to drive the
    three comparison branches (PASS / HARD-FAIL / WARN).
    """
    return {
        "schema_version": "1",
        "scenario": "hello_world_spike",
        "n_samples": 5,
        "last_captured_utc": "2026-05-13T00:00:00Z",
        "last_captured_git_sha": "abc1234",
        "last_captured_cli_version": "claude 0.1.0",
        "metrics": {
            "wall_clock_seconds": {
                "mean": 600.0,
                "stddev": 50.0,
                "n": 5,
                "classification": "hard",
                "hard_max": 1800.0,
            },
            "cost_usd": {
                "mean": 1.50,
                "stddev": 0.25,
                "n": 5,
                "classification": "hard",
                "hard_max": 3.00,
            },
            "pipeline.dispatch_count": {
                "mean": 8.0,
                "stddev": 1.0,
                "n": 5,
                "classification": "hard",
                "hard_max": 16.0,
            },
            "pipeline.stories_completed": {
                "mean": 1.0,
                "stddev": 0.0,
                "n": 5,
                "classification": "hard",
                "hard_max": 1.0,
            },
            "tokens.input": {
                "mean": 10000.0,
                "stddev": 500.0,
                "n": 5,
                "classification": "advisory",
            },
            "tokens.output": {
                "mean": 5000.0,
                "stddev": 250.0,
                "n": 5,
                "classification": "advisory",
            },
        },
    }


@pytest.fixture
def passing_report() -> dict:
    """A report dict that should yield RegressionResult.status == "PASS"."""
    return {
        "schema_version": "1",
        "outcome": {"success": True, "exit_code": 0, "reason": None},
        "wall_clock_seconds": 605.0,
        "cost_usd": 1.55,
        "tokens": {"input": 10100, "output": 4950, "cache_creation": 0, "cache_read": 0},
        "pipeline": {
            "stages_completed": 7,
            "stories_completed": 1,
            "dispatch_count": 8,
            "defects_logged": 0,
        },
        "skill_loads": [],
    }


@pytest.fixture
def hard_fail_report() -> dict:
    """A report whose `cost_usd` exceeds hard_max ($3.00). Status must be FAIL."""
    return {
        "schema_version": "1",
        "outcome": {"success": True, "exit_code": 0, "reason": None},
        "wall_clock_seconds": 700.0,
        "cost_usd": 3.50,  # over hard_max=3.00
        "tokens": {"input": 10000, "output": 5000, "cache_creation": 0, "cache_read": 0},
        "pipeline": {
            "stages_completed": 7,
            "stories_completed": 1,
            "dispatch_count": 8,
            "defects_logged": 0,
        },
        "skill_loads": [],
    }


@pytest.fixture
def advisory_warn_report() -> dict:
    """A report whose `tokens.input` is outside mean ± 2σ. Status must be WARN."""
    return {
        "schema_version": "1",
        "outcome": {"success": True, "exit_code": 0, "reason": None},
        "wall_clock_seconds": 600.0,
        "cost_usd": 1.50,
        # mean=10000, stddev=500, ±2σ = [9000, 11000]. 13000 is outside.
        "tokens": {"input": 13000, "output": 5000, "cache_creation": 0, "cache_read": 0},
        "pipeline": {
            "stages_completed": 7,
            "stories_completed": 1,
            "dispatch_count": 8,
            "defects_logged": 0,
        },
        "skill_loads": [],
    }


# --- Fixture workspace factory ----------------------------------------------

@pytest.fixture
def sample_workspace_dir(smoke_root: Path) -> Path:
    """Absolute path to the on-disk fixture workspace under tests/fixtures/sample-workspace/."""
    path = smoke_root / "tests" / "fixtures" / "sample-workspace"
    assert path.is_dir(), f"sample-workspace fixture missing: {path}"
    return path


@pytest.fixture
def sample_workspace(sample_workspace_dir: Path):
    """Construct a `Workspace`-shaped stand-in pointing at the on-disk fixture.

    The real `Workspace` dataclass requires `setup()` to mktemp a HOME — we
    bypass that and hand-build the attributes `aggregator.aggregate()` reads
    (`home`). The fixture workspace lays files at `<root>/work/.delivery/...`
    to match the production layout the aggregator walks.
    """
    from lib.workspace import Workspace  # imported lazily to honor sys.path setup

    ws = Workspace(
        repo_root=sample_workspace_dir,
        plugin_path=sample_workspace_dir,
        config_fixture=sample_workspace_dir / "config_unused.yml",
    )
    ws.home = sample_workspace_dir
    ws.workdir = sample_workspace_dir / "work"
    ws._setup_done = True
    return ws
