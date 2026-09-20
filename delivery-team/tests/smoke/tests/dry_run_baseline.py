#!/usr/bin/env python3
"""Baseline writer dry-run, no spend (PA-24, NFR-9).

    python3 tests/dry_run_baseline.py --out "$SMOKE_OUT/dry-baseline.json" [--case ok|abort|ceiling]

Runs `run_smoke.py --init-baseline` end to end against a STUB `claude` placed
first on PATH (a generated script; the real CLI is never spawned: the shim
answers `--version`, `--help` and the stream-json call itself, and this script
asserts `claude` resolves to the shim before every run).

Sub-cases in ONE invocation (rc 0 only if all print their expected token):
  happy    5 samples, distinct message.id / session_id / uuid rewritten per
           sample by the shim. Expect `DRYRUN OK` after the AC-5.1, AC-5.4 and
           AC-5.5c snippets pass on the written baseline.
  abort    sample 3 exits non-zero. Expect the flow to stop at once, exit
           non-zero, and write NO baseline: `DRYRUN ABORT_OK`.
  ceiling  injected run dirs whose costs sum past the ceiling: spend_check.py
           MUST return rc 3 (asserted here, not returned): `DRYRUN CEILING_OK`.
Any mismatch prints `DRYRUN FAIL <case> <reason>` and the invocation returns 1.

Stream template: the real-shape fixture (tests/fixtures/stream_real_shape.jsonl)
when it exists, otherwise a SYNTHETIC placeholder stream built here. The
output says which (`DRYRUN NOTE fixture=...`). Until the H1 capture lands the
happy case therefore exercises the writer on a synthetic stream only.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent
sys.path.insert(0, str(HERE))
import spend_check  # noqa: E402  (same module as PA-16 / PA-22)

FIXTURE = HERE / "fixtures" / "stream_real_shape.jsonl"

SHIM = r'''#!{python}
"""STUB claude for PA-24. Never contacts any service."""
import json, os, sys
args = sys.argv[1:]
if "--version" in args:
    print("claude 0.0.0-dryrun-stub"); sys.exit(0)
if "--help" in args:
    print("Usage: claude [options]\n  --plugin-dir <path>\n  --max-budget-usd <amount>"); sys.exit(0)
prompt = sys.stdin.read()
counter = os.environ["DRYRUN_COUNTER"]
n = int(open(counter).read() or 0) + 1 if os.path.exists(counter) else 1
open(counter, "w").write(str(n))
open(os.environ["DRYRUN_ARGV_LOG"], "a").write(json.dumps(args) + "\n")
for line in open(os.environ["DRYRUN_TEMPLATE"], encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    e = json.loads(line)
    if isinstance(e.get("session_id"), str):
        e["session_id"] = f"{{e['session_id']}}-{{n}}"
    if isinstance(e.get("uuid"), str):
        e["uuid"] = f"{{e['uuid']}}-{{n}}"
    if isinstance(e.get("message"), dict) and isinstance(e["message"].get("id"), str):
        e["message"]["id"] = f"{{e['message']['id']}}-{{n}}"
    if e.get("type") == "result" and isinstance(e.get("total_cost_usd"), (int, float)):
        e["total_cost_usd"] = round(e["total_cost_usd"] + n * 0.001, 6)
    print(json.dumps(e), flush=True)
fail_at = os.environ.get("DRYRUN_FAIL_AT")
sys.exit(1 if fail_at and int(fail_at) == n else 0)
'''

SYNTH = [
    {"type": "system", "subtype": "init", "session_id": "sess-synth", "model": "claude-opus-fixture"},
    {"type": "assistant", "uuid": "uu-1", "parent_tool_use_id": None,
     "message": {"id": "msg-a", "model": "claude-opus-fixture",
                 "usage": {"input_tokens": 100, "output_tokens": 50,
                           "cache_creation_input_tokens": 20, "cache_read_input_tokens": 300}}},
    {"type": "assistant", "uuid": "uu-2", "parent_tool_use_id": None,
     "message": {"id": "msg-b", "model": "claude-opus-fixture",
                 "usage": {"input_tokens": 80, "output_tokens": 60,
                           "cache_creation_input_tokens": 0, "cache_read_input_tokens": 320}}},
    {"type": "result", "subtype": "success", "is_error": False, "total_cost_usd": 0.05,
     "usage": {"input_tokens": 180, "output_tokens": 110,
               "cache_creation_input_tokens": 20, "cache_read_input_tokens": 620},
     "modelUsage": {"claude-opus-fixture": {"inputTokens": 180}}},
]


def _template(work: Path) -> tuple[Path, str]:
    if FIXTURE.is_file():
        return FIXTURE, "real-shape"
    p = work / "synthetic-template.jsonl"
    p.write_text("".join(json.dumps(e) + "\n" for e in SYNTH), encoding="utf-8")
    return p, "synthetic-placeholder (H1 fixture not captured)"


def _shim_env(work: Path, template: Path, fail_at: int | None) -> tuple[dict, Path]:
    bindir = work / "bin"
    bindir.mkdir(parents=True, exist_ok=True)
    shim = bindir / "claude"
    shim.write_text(SHIM.format(python=sys.executable), encoding="utf-8")
    shim.chmod(shim.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    env = dict(os.environ)
    env["PATH"] = f"{bindir}{os.pathsep}/usr/bin{os.pathsep}/bin"
    env["DRYRUN_COUNTER"] = str(work / "counter.txt")
    env["DRYRUN_ARGV_LOG"] = str(work / "argv.log")
    env["DRYRUN_TEMPLATE"] = str(template)
    env.pop("DRYRUN_FAIL_AT", None)
    if fail_at:
        env["DRYRUN_FAIL_AT"] = str(fail_at)
    got = shutil.which("claude", path=env["PATH"])
    if got != str(shim):
        raise RuntimeError(f"claude resolves to {got}, not the stub shim; refusing to run")
    return env, shim


def _init_baseline_run(work: Path, baseline: Path, env: dict) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(SMOKE / "run_smoke.py"), "--init-baseline", "--baseline", str(baseline),
           "--out-dir", str(work / "runs"), "--cost-cap", "3.00", "--timeout", "60"]
    return subprocess.run(cmd, cwd=str(SMOKE), env=env, capture_output=True, text=True, timeout=300)


def case_happy(work: Path, out: Path) -> tuple[bool, str]:
    template, kind = _template(work)
    print(f"DRYRUN NOTE fixture={kind}")
    env, _ = _shim_env(work, template, None)
    baseline = out
    if baseline.exists():
        baseline.unlink()
    r = _init_baseline_run(work, baseline, env)
    if r.returncode != 0:
        return False, f"run_smoke rc={r.returncode}: {(r.stderr or r.stdout).strip()[-200:]}"
    if not baseline.is_file():
        return False, "no baseline file written"
    b = json.loads(baseline.read_text(encoding="utf-8"))
    m = b.get("metrics", {})
    probs = []
    if b.get("schema_version") != "2":
        probs.append(f"schema_version {b.get('schema_version')!r}")
    if "tokens.cache_hit_ratio" not in m:
        probs.append("AC-5.1: tokens.cache_hit_ratio missing")
    md = [k for k in m if k.startswith("model_usage.")]
    if not md:
        probs.append("AC-5.1: no model_usage.* keys")
    if any("unknown" in k for k in md):
        probs.append("AC-5.1: model_usage key contains unknown")
    for key in ("model_requested", "model_resolved", "model_pin_env", "host_context", "effort"):
        if key not in b:
            probs.append(f"AC-5.5: baseline lacks {key}")
    res = b.get("model_resolved")
    if not (isinstance(res, list) and res and isinstance(res[0], str) and res[0]):
        probs.append(f"AC-5.5: model_resolved {res!r}")
    samples = b.get("samples")
    if not (isinstance(samples, list) and len(samples) == 5 and all(s.get("stream_sha256") for s in samples)):
        probs.append("AC-5.5c: samples[] must hold 5 entries with stream_sha256")
    cost = m.get("cost_usd", {})
    if cost.get("hard_max") != 3.0 or not (isinstance(cost.get("mean"), (int, float)) and cost["mean"] > 0):
        probs.append(f"AC-5.4: cost_usd hard_max/mean {cost}")
    if not probs:
        d = subprocess.run([sys.executable, str(HERE / "check_distinct.py"), str(baseline)],
                           capture_output=True, text=True)
        if d.returncode != 0 or "AC-5.5c OK" not in d.stdout:
            probs.append(f"AC-5.5c: {d.stdout.strip() or d.stderr.strip()}")
    return (not probs), "; ".join(probs)


def case_abort(work: Path, out: Path) -> tuple[bool, str]:
    template, _ = _template(work)
    env, _ = _shim_env(work, template, fail_at=3)
    baseline = out.with_name(out.stem + "-abort.json")
    if baseline.exists():
        baseline.unlink()
    r = _init_baseline_run(work, baseline, env)
    calls = int((work / "counter.txt").read_text() or 0) if (work / "counter.txt").exists() else 0
    probs = []
    if r.returncode == 0:
        probs.append("run_smoke returned 0 after an injected non-zero outcome")
    if baseline.exists():
        probs.append("a baseline file was written after an aborted sample")
    if calls != 3:
        probs.append(f"flow ran {calls} samples; must stop at the failed sample 3")
    return (not probs), "; ".join(probs)


def case_ceiling(work: Path, out: Path) -> tuple[bool, str]:
    root = work / "spend-runs"
    shutil.rmtree(root, ignore_errors=True)
    for i in range(5):
        d = root / f"run{i}"
        d.mkdir(parents=True)
        (d / "report.json").write_text(json.dumps({"cost_usd": 2.99}))
    rc, line = spend_check.check(root, None)
    probs = []
    if rc != 3 or "STOP ceiling" not in line:
        probs.append(f"spend_check rc={rc} {line!r}, expected rc 3 STOP ceiling")
    shutil.rmtree(root)
    for i in range(4):
        d = root / f"run{i}"
        d.mkdir(parents=True)
        (d / "report.json").write_text(json.dumps({"cost_usd": 2.99}))
    rc, line = spend_check.check(root, None)
    if rc != 0:
        probs.append(f"spend_check rc={rc} {line!r} below the ceiling, expected 0")
    return (not probs), "; ".join(probs)


CASES = {"ok": ("DRYRUN OK", "happy", case_happy),
         "abort": ("DRYRUN ABORT_OK", "abort", case_abort),
         "ceiling": ("DRYRUN CEILING_OK", "ceiling", case_ceiling)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="temp baseline path, e.g. $SMOKE_OUT/dry-baseline.json")
    ap.add_argument("--case", choices=sorted(CASES))
    a = ap.parse_args(argv)
    out = Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    rc = 0
    for key in ([a.case] if a.case else ["ok", "abort", "ceiling"]):
        token, name, fn = CASES[key]
        work = Path(tempfile.mkdtemp(prefix="dryrun-", dir=str(out.parent)))
        try:
            ok, why = fn(work, out)
        except Exception as exc:  # noqa: BLE001 - a crash is a FAIL, reported
            ok, why = False, f"{type(exc).__name__}: {exc}"
        finally:
            shutil.rmtree(work, ignore_errors=True)
        if ok:
            print(token)
        else:
            print(f"DRYRUN FAIL {name} {why}")
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
