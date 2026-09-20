#!/usr/bin/env python3
"""Paid-run spend and run-cap checker (PA-16, PA-22; ADR-lmr-004 section 8).

Single implementation shared by the S5b pre-run snippet (PA-22), the harness
spend snippet (PA-16) and the PA-24 dry-run `CEILING_OK` case. All money math
is `decimal.Decimal`, never float.

Usage (from delivery-team/tests/smoke/):
    python3 tests/spend_check.py --dir "$SMOKE_OUT" --attempts <attempts-file>
    python3 tests/spend_check.py --self-test

Rules:
  * Every subdirectory of --dir is a run dir. `report.json` absent => counts
    the per-sample cap ($3.00). Present but `cost_usd` missing, non-numeric or
    a bool => `BAD_COST <dir>` and rc 2 (never treated as 0).
  * If a run dir has `stream.jsonl`, its last `result` event must carry a
    numeric `total_cost_usd`, else `BAD_COST` rc 2.
  * Attempt log (`run=<n> <utc-time>` lines, written BEFORE each launch): run
    count = max(run-dir count, attempt-log lines). Counted runs without a run
    dir cost $3.00 each (a run killed before its dir existed).
  * Output `spent=<x> next_cap=3.00 runs=<n> ok` rc 0.
  * rc 3 `STOP ceiling` if spent + 3.00 > 15.00; rc 3 `STOP runs` if runs >= 7.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

CAP = Decimal("3.00")
CEILING = Decimal("15.00")
MAX_RUNS = 7


class BadCost(Exception):
    def __init__(self, where: str):
        super().__init__(where)
        self.where = where


def _is_num(v) -> bool:
    return isinstance(v, (int, float, Decimal)) and not isinstance(v, bool)


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"), parse_float=Decimal)


def _last_result_cost_ok(stream: Path) -> bool:
    last = None
    for line in stream.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            evt = json.loads(line, parse_float=Decimal)
        except json.JSONDecodeError:
            continue
        if isinstance(evt, dict) and evt.get("type") == "result":
            last = evt
    if last is None:
        return False
    return _is_num(last.get("total_cost_usd"))


def run_dir_cost(d: Path) -> Decimal:
    rpt = d / "report.json"
    if not rpt.is_file():
        return CAP
    try:
        cost = _load(rpt).get("cost_usd")
    except (json.JSONDecodeError, AttributeError, OSError):
        raise BadCost(d.name)
    if not _is_num(cost):
        raise BadCost(d.name)
    stream = d / "stream.jsonl"
    if stream.is_file() and stream.stat().st_size > 0 and not _last_result_cost_ok(stream):
        raise BadCost(d.name)
    return Decimal(cost)


def compute(run_root: Path, attempts: Path | None) -> tuple[Decimal, int]:
    """Return (spent, runs). Raises BadCost."""
    dirs = sorted(p for p in run_root.iterdir() if p.is_dir()) if run_root.is_dir() else []
    spent = sum((run_dir_cost(d) for d in dirs), Decimal("0"))
    lines = 0
    if attempts is not None and attempts.is_file():
        lines = sum(1 for ln in attempts.read_text(encoding="utf-8").splitlines() if ln.strip())
    runs = max(len(dirs), lines)
    spent += CAP * (runs - len(dirs))
    return spent, runs


def evaluate(spent: Decimal, runs: int) -> tuple[int, str]:
    head = f"spent={spent:.2f} next_cap=3.00 runs={runs}"
    stops = []
    if spent + CAP > CEILING:
        stops.append("STOP ceiling")
    if runs >= MAX_RUNS:
        stops.append("STOP runs")
    if stops:
        return 3, head + " " + " ".join(stops)
    return 0, head + " ok"


def check(run_root: Path, attempts: Path | None) -> tuple[int, str]:
    try:
        spent, runs = compute(run_root, attempts)
    except BadCost as exc:
        return 2, f"BAD_COST {exc.where}"
    return evaluate(spent, runs)


def _mk_run(root: Path, name: str, cost, *, stream: bool = False, result_cost=True) -> None:
    d = root / name
    d.mkdir(parents=True)
    if cost is not ...:
        rpt = {} if cost is None else {"cost_usd": cost}
        (d / "report.json").write_text(json.dumps(rpt), encoding="utf-8")
    if stream:
        res = {"type": "result"}
        if result_cost:
            res["total_cost_usd"] = 1.0
        (d / "stream.jsonl").write_text(json.dumps(res) + "\n", encoding="utf-8")


def self_test() -> int:
    results: list[tuple[str, bool, str]] = []

    def case(name, build, want_rc, want_sub, attempts_lines=0):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "runs"
            root.mkdir()
            build(root)
            att = None
            if attempts_lines:
                att = Path(td) / "attempts.txt"
                att.write_text("".join(f"run={i + 1} t\n" for i in range(attempts_lines)))
            rc, line = check(root, att)
        ok = rc == want_rc and want_sub in line
        results.append((name, ok, f"rc={rc} {line}"))

    case("empty ok", lambda r: None, 0, "spent=0.00 next_cap=3.00 runs=0 ok")
    case("four runs 12.00 ok", lambda r: [_mk_run(r, f"r{i}", 3.0) for i in range(4)], 0, "spent=12.00")
    case("ceiling: 4 x 3.01 => 12.04+3 > 15", lambda r: [_mk_run(r, f"r{i}", 3.01) for i in range(4)],
         3, "STOP ceiling")
    case("no report counts 3.00", lambda r: [_mk_run(r, "a", ...), _mk_run(r, "b", 3.0), _mk_run(r, "c", 3.0),
                                            _mk_run(r, "d", 3.0), _mk_run(r, "e", 3.0)],
         3, "spent=15.00")
    case("float drift: 0.1 x 3 exact", lambda r: [_mk_run(r, f"r{i}", 0.1) for i in range(3)], 0, "spent=0.30")
    case("BAD_COST missing", lambda r: _mk_run(r, "x", None), 2, "BAD_COST x")
    case("BAD_COST string", lambda r: _mk_run(r, "x", "1.0"), 2, "BAD_COST x")
    case("BAD_COST bool", lambda r: _mk_run(r, "x", True), 2, "BAD_COST x")
    case("BAD_COST stream result lacks total_cost_usd",
         lambda r: _mk_run(r, "x", 1.0, stream=True, result_cost=False), 2, "BAD_COST x")
    case("stream ok", lambda r: _mk_run(r, "x", 1.0, stream=True), 0, "spent=1.00")
    case("STOP runs at 7 (dirs)", lambda r: [_mk_run(r, f"r{i}", 0.0) for i in range(7)], 3, "STOP runs")
    case("attempt log outranks dirs", lambda r: _mk_run(r, "a", 1.0), 3, "runs=7", attempts_lines=7)
    case("killed run before dir costs 3.00", lambda r: _mk_run(r, "a", 1.0), 0, "spent=7.00 next_cap=3.00 runs=3 ok",
         attempts_lines=3)
    case("exact 15.00 pre-run boundary allowed (12+3)", lambda r: [_mk_run(r, f"r{i}", 3.0) for i in range(4)],
         0, "ok")
    case("both stops", lambda r: [_mk_run(r, f"r{i}", 3.0) for i in range(7)], 3, "STOP ceiling STOP runs")
    passed = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        if not ok:
            print(f"SELFTEST FAIL {name}: {detail}")
    if passed == len(results):
        print(f"SELFTEST OK {passed}/{len(results)}")
        return 0
    print(f"SELFTEST FAIL {passed}/{len(results)}")
    return 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", help="directory holding one subdirectory per run ($SMOKE_OUT)")
    ap.add_argument("--attempts", help="attempt log, one `run=<n> <utc>` line per launch")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.dir:
        ap.error("--dir is required")
    rc, line = check(Path(a.dir), Path(a.attempts) if a.attempts else None)
    print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
