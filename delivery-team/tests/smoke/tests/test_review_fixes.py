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
