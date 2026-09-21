"""Review-fix regression tests (BACKLOG-108): no paid calls, no real claude."""
import sys
from decimal import Decimal
from pathlib import Path

import pytest

SMOKE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SMOKE))

from lib import baseline as bl  # noqa: E402
from lib import runner  # noqa: E402


def test_consistency_seeds_none_first():
    reports = [{}, {"model_resolved": ["m-a"]}, {"model_resolved": ["m-a"]}]
    with pytest.raises(bl.ModelMovedError):
        bl.check_model_consistency(reports)


def test_budget_rounds_down_and_never_zero():
    ws = type("W", (), {"plugin_load_strategy": "none", "plugin_path": "."})()
    cmd = runner._build_claude_command(ws, Path("p"), max_budget_usd=2.999)
    assert cmd[cmd.index("--max-budget-usd") + 1] == "2.99"
    cmd = runner._build_claude_command(ws, Path("p"), max_budget_usd=0.001)
    assert Decimal(cmd[cmd.index("--max-budget-usd") + 1]) > 0


def test_cost_cap_must_be_positive():
    import run_smoke
    with pytest.raises(SystemExit) as ei:
        run_smoke.main(["--cost-cap", "0"])
    assert ei.value.code == 2


def test_cost_cap_floor_rejects_below_cent():
    import run_smoke
    with pytest.raises(SystemExit) as ei:
        run_smoke.main(["--cost-cap", "0.005"])
    assert ei.value.code == 2


def _sample_report(i, stream):
    return {
        "schema_version": "2",
        "outcome": {"success": True, "exit_code": 0, "reason": None},
        "wall_clock_seconds": 600.0, "cost_usd": 1.5,
        "tokens": {"input": 1, "output": 1, "cache_creation": 0, "cache_read": 0, "cache_hit_ratio": 0.5},
        "pipeline": {"stages_completed": 7, "stories_completed": 1, "dispatch_count": 8, "defects_logged": 0},
        "skill_loads": [], "model_requested": "opus", "model_resolved": ["claude-opus-fixture"],
        "model_usage": [{"model": "claude-opus-fixture", "dispatches": 3}],
        "effort": "xhigh", "host_context": {"bare": False, "claude_code_version": "claude 0.0.0-test"},
        "model_pin_env": {}, "session_id": f"s{i}", "stream_file": str(stream),
    }


def test_baseline_streams_resolve_with_check_distinct(tmp_path):
    import json
    import subprocess
    smoke = tmp_path / "smoke"
    (smoke / "baselines").mkdir(parents=True)
    reports = []
    for i in range(5):
        d = smoke / "artifacts" / f"20260101T00000{i}Z-init-{i + 1}"
        d.mkdir(parents=True)
        p = d / "stream.jsonl"
        p.write_text(
            json.dumps({"type": "system", "subtype": "init", "session_id": f"s{i}", "model": "claude-opus-fixture"}) + "\n"
            + json.dumps({"type": "assistant", "message": {"id": f"m{i}", "model": "claude-opus-fixture"}}) + "\n"
            + json.dumps({"type": "result", "total_cost_usd": 1.0 + i / 10}) + "\n")
        reports.append(_sample_report(i, p))
    out = smoke / "baselines" / "b.json"
    bl.init_baseline(reports, out)
    text = out.read_text()
    for s in json.loads(text)["samples"]:
        assert not Path(s["stream_file"]).is_absolute() and s["stream_file"].startswith("../artifacts/")
    assert str(tmp_path) not in text
    checker = SMOKE / "tests" / "check_distinct.py"
    r = subprocess.run([sys.executable, str(checker), str(out)], capture_output=True, text=True)
    assert r.returncode == 0 and "AC-5.5c OK" in r.stdout, (r.stdout, r.stderr)


class _FakeProc:
    def __init__(self, running):
        self.running = running
        self.terminated = False

    def poll(self):
        return None if self.running else 0

    def terminate(self):
        self.terminated = True
        self.running = False

    def wait(self, timeout=None):
        return 0

    def kill(self):
        pass


def test_watchdog_ignores_already_exited_process():
    proc = _FakeProc(running=False)
    timer, flag = runner._start_watchdog(proc, 0.01)
    timer.join(1)
    assert not flag.is_set() and not proc.terminated


def test_watchdog_terminates_running_process():
    proc = _FakeProc(running=True)
    timer, flag = runner._start_watchdog(proc, 0.01)
    timer.join(1)
    assert flag.is_set() and proc.terminated
