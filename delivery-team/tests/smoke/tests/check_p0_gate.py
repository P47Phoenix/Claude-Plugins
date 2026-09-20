#!/usr/bin/env python3
"""P0 stub AST gate (PA-12, ADR-lmr-004 section 6 rules 1a to 1d).

    python3 tests/check_p0_gate.py --base <base_sha> --head <p0_commit>
    python3 tests/check_p0_gate.py --self-test

Prints `P0_GATE OK` rc 0, or `P0_GATE FAIL <reason>` rc 1 (rc 2 on usage or
git errors). Authored by the validator, never the producer.

Rules, over `delivery-team/tests/smoke/lib/*.py` and `run_smoke.py`:
  1a  every function present at base has an identical BODY (ast.dump; signature
      and decorators excluded) at head, except the named exemption
      EXEMPT = {(report.py, build_report)}.
  1b  build_report at head, after deleting the pinned new dict entries (each
      value REQUIRED to be a constant-only literal) and the nested
      tokens["cache_hit_ratio"] entry, equals the base body.
  1c  new top-level names are limited to ALLOWED_NEW_NAMES; every new function
      body is inert (pass, docstring, or return of a constant-only value; no
      raise/if/for/Call/Name/Attribute/Subscript); new exception classes have
      only a docstring body.
  1d  class Metrics == base members plus at most the three constant-default
      AnnAssign fields; a method, property, non-constant default or other
      member fails. Every other pre-existing class is unchanged.
Also: module-level statements other than def/class must be unchanged.
"""
from __future__ import annotations

import argparse
import ast
import copy
import subprocess
import sys

SMOKE = "delivery-team/tests/smoke"
EXEMPT = {("report.py", "build_report")}
PINNED_KEYS = {"model_requested", "model_resolved", "effort", "host_context",
               "session_id", "stream_file", "model_pin_env"}
METRICS_FIELDS = {"model_primary", "models_observed", "cache_hit_ratio"}
ALLOWED_NEW_NAMES = {"check_model_capture", "check_model_consistency", "load_baseline",
                     "ModelCaptureError", "ModelMovedError", "BaselineSchemaError"}


def _const_only(node: ast.AST) -> bool:
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return all(_const_only(e) for e in node.elts)
    if isinstance(node, ast.Dict):
        return all(k is not None and _const_only(k) for k in node.keys) and all(
            _const_only(v) for v in node.values)
    return False


def _dump(nodes) -> list[str]:
    return [ast.dump(n) for n in nodes]


def _inert_body(body: list[ast.stmt]) -> str | None:
    for st in body:
        if isinstance(st, ast.Pass):
            continue
        if isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant) and isinstance(st.value.value, str):
            continue
        if isinstance(st, ast.Return) and (st.value is None or _const_only(st.value)):
            continue
        return type(st).__name__
    return None


def _strip_build_report(fn: ast.FunctionDef) -> tuple[list[ast.stmt], str | None]:
    """Return (transformed body, error). Deletes pinned constant entries."""
    body = copy.deepcopy(fn.body)
    for st in body:
        if not (isinstance(st, ast.Return) and isinstance(st.value, ast.Dict)):
            continue
        d = st.value
        keep_k, keep_v = [], []
        for k, v in zip(d.keys, d.values):
            name = k.value if isinstance(k, ast.Constant) else None
            if name in PINNED_KEYS:
                if not _const_only(v):
                    return body, f"nonconst pinned value for {name!r}"
                continue
            if name == "tokens" and isinstance(v, ast.Dict):
                nk, nv = [], []
                for tk, tv in zip(v.keys, v.values):
                    if isinstance(tk, ast.Constant) and tk.value == "cache_hit_ratio":
                        if not _const_only(tv):
                            return body, "nonconst pinned value for tokens.cache_hit_ratio"
                        continue
                    nk.append(tk)
                    nv.append(tv)
                v = ast.Dict(keys=nk, values=nv)
            keep_k.append(k)
            keep_v.append(v)
        d.keys, d.values = keep_k, keep_v
    return body, None


def _index(src: str):
    tree = ast.parse(src)
    funcs: dict[str, ast.FunctionDef] = {}
    classes: dict[str, ast.ClassDef] = {}
    other: list[ast.stmt] = []

    def walk_cls(cls: ast.ClassDef, prefix: str) -> None:
        for m in cls.body:
            if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                funcs[f"{prefix}{cls.name}.{m.name}"] = m

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs[node.name] = node
        elif isinstance(node, ast.ClassDef):
            classes[node.name] = node
            walk_cls(node, "")
        else:
            other.append(node)
    return funcs, classes, other


def gate(base: dict[str, str], head: dict[str, str]) -> list[str]:
    """base/head map a basename (e.g. report.py) -> source. Returns failures."""
    fails: list[str] = []
    for fname in sorted(set(base) | set(head)):
        b_src, h_src = base.get(fname), head.get(fname)
        if b_src is None:
            b_src = ""
        if h_src is None:
            fails.append(f"{fname}: file missing at head")
            continue
        try:
            bf, bc, bo = _index(b_src)
            hf, hc, ho = _index(h_src)
        except SyntaxError as exc:
            fails.append(f"{fname}: SyntaxError {exc}")
            continue

        if _dump(bo) != _dump(ho):
            fails.append(f"{fname}: module-level statements changed")

        # 1a / 1b
        for qn, bfn in bf.items():
            hfn = hf.get(qn)
            if hfn is None:
                fails.append(f"{fname}::{qn}: function removed")
                continue
            if "." in qn and qn.split(".")[0] == "Metrics":
                fails.append(f"{fname}::{qn}: unexpected pre-existing method")
            if (fname, qn) in EXEMPT:
                tbody, err = _strip_build_report(hfn)
                if err:
                    fails.append(f"{fname}::{qn}: {err}")
                elif _dump(tbody) != _dump(bfn.body):
                    fails.append(f"{fname}::{qn}: body differs after strip")
            elif _dump(hfn.body) != _dump(bfn.body):
                fails.append(f"{fname}::{qn}: body changed (1a)")

        # 1c: new functions and classes
        for qn, hfn in hf.items():
            if qn in bf:
                continue
            top = "." not in qn
            if top and qn not in ALLOWED_NEW_NAMES:
                fails.append(f"{fname}::{qn}: new function name not allowed")
            if not top:
                if qn.split(".")[0] == "Metrics":
                    fails.append(f"{fname}::{qn}: disallowed class-body addition (method on Metrics)")
                else:
                    fails.append(f"{fname}::{qn}: new method not allowed at P0")
                continue
            bad = _inert_body(hfn.body)
            if bad:
                fails.append(f"{fname}::{qn}: new function not inert ({bad})")
        for cn, hcls in hc.items():
            if cn in bc:
                continue
            if cn not in ALLOWED_NEW_NAMES:
                fails.append(f"{fname}::{cn}: new class name not allowed")
                continue
            bad = _inert_body(hcls.body)
            if bad or any(isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)) for m in hcls.body):
                fails.append(f"{fname}::{cn}: new class body not inert")
        for cn, bcls in bc.items():
            hcls = hc.get(cn)
            if hcls is None:
                fails.append(f"{fname}::{cn}: class removed")
                continue
            if cn == "Metrics" and fname == "metrics.py":
                base_members = _dump(bcls.body)
                extra = []
                for m in hcls.body:
                    if ast.dump(m) in base_members:
                        continue
                    extra.append(m)
                names = []
                for m in extra:
                    ok = (isinstance(m, ast.AnnAssign) and isinstance(m.target, ast.Name)
                          and m.target.id in METRICS_FIELDS and m.value is not None)
                    if ok:
                        v = m.value
                        ok = _const_only(v) or (
                            isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == "field"
                            and not v.args and len(v.keywords) == 1 and v.keywords[0].arg == "default_factory"
                            and isinstance(v.keywords[0].value, ast.Name)
                            and v.keywords[0].value.id in ("list", "dict"))
                    if not ok:
                        fails.append(f"{fname}::Metrics: disallowed class-body addition ({ast.unparse(m)[:60]})")
                    else:
                        names.append(m.target.id)
                if len(names) != len(set(names)):
                    fails.append(f"{fname}::Metrics: duplicate field")
                if [d for d in base_members if d not in _dump(hcls.body)]:
                    fails.append(f"{fname}::Metrics: base member removed or changed")
            elif _dump(hcls.body) != _dump(bcls.body):
                fails.append(f"{fname}::{cn}: class body changed")
    return fails


def run_gate(base: dict[str, str], head: dict[str, str]) -> tuple[int, str]:
    fails = gate(base, head)
    if fails:
        return 1, "P0_GATE FAIL " + "; ".join(fails)
    return 0, "P0_GATE OK"


# ----------------------------------------------------------------- git input

def _git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def _sources(rev: str) -> dict[str, str]:
    top = _git("rev-parse", "--show-toplevel").strip()
    names = _git("ls-tree", "-r", "--name-only", rev, "--", f"{SMOKE}/lib", f"{SMOKE}/run_smoke.py").split()
    out = {}
    for n in names:
        if n.endswith(".py"):
            out[n.rsplit("/", 1)[-1]] = subprocess.run(
                ["git", "-C", top, "show", f"{rev}:{n}"], check=True, capture_output=True, text=True).stdout
    return out


# ----------------------------------------------------------------- self-test

BASE_METRICS = '''
from dataclasses import dataclass, field

@dataclass
class Metrics:
    cost_usd: float = 0.0
    model_usage: list = field(default_factory=list)

def parse_stream(events):
    m = Metrics()
    for e in events:
        m.cost_usd += 1
    return m
'''

P0_METRICS = '''
from dataclasses import dataclass, field

@dataclass
class Metrics:
    cost_usd: float = 0.0
    model_usage: list = field(default_factory=list)
    model_primary: str | None = None
    models_observed: list = field(default_factory=list)
    cache_hit_ratio: float = 0.0

class ModelCaptureError(Exception):
    """doc"""

def check_model_capture(metrics):
    """stub"""
    return []

def parse_stream(events):
    m = Metrics()
    for e in events:
        m.cost_usd += 1
    return m
'''

BASE_REPORT = '''
def build_report(*, metrics, run_id):
    """doc"""
    return {
        "run_id": run_id,
        "cost_usd": float(metrics.cost_usd),
        "tokens": {"input": int(metrics.tokens), "output": 1},
    }
'''

P0_REPORT = '''
def build_report(*, metrics, run_id, stream_path=None, session_id=None):
    """doc"""
    return {
        "run_id": run_id,
        "model_requested": None,
        "model_resolved": [],
        "host_context": {},
        "session_id": None,
        "model_pin_env": {},
        "cost_usd": float(metrics.cost_usd),
        "tokens": {"input": int(metrics.tokens), "output": 1, "cache_hit_ratio": 0.0},
    }
'''

BASE_BASELINE = '''
def check(reports):
    return 1
'''

P0_BASELINE = '''
class ModelMovedError(Exception):
    """doc"""

def check_model_consistency(reports):
    """stub"""
    return None

def load_baseline(path):
    return {}

def check(reports, strict_model=False):
    return 1
'''


def _mutations():
    """(name, {file: src}) wrong P0s. Each must be rejected."""
    good = {"metrics.py": P0_METRICS, "report.py": P0_REPORT, "baseline.py": P0_BASELINE}

    def mut(file, old, new):
        d = dict(good)
        assert old in d[file], old
        d[file] = d[file].replace(old, new)
        return d

    return [
        ("computed value in build_report key", mut("report.py", '"session_id": None', '"session_id": str(metrics.cost_usd)')),
        ("computed tokens.cache_hit_ratio", mut("report.py", '"cache_hit_ratio": 0.0', '"cache_hit_ratio": metrics.cost_usd')),
        ("method added to Metrics", mut("metrics.py", "    cache_hit_ratio: float = 0.0\n",
                                        "    cache_hit_ratio: float = 0.0\n    def ratio(self):\n        return 1\n")),
        ("property added to Metrics", mut("metrics.py", "    cache_hit_ratio: float = 0.0\n",
                                          "    cache_hit_ratio: float = 0.0\n    @property\n    def extra(self):\n        return 1\n")),
        ("real implementation in a stub", mut("baseline.py", "    return None\n\ndef load_baseline",
                                             "    for r in reports:\n        if r:\n            raise ValueError('x')\n    return None\n\ndef load_baseline")),
        ("raise in a stub", mut("metrics.py", "    return []\n", "    raise NotImplementedError\n")),
        ("stub returns a computed call", mut("baseline.py", "    return {}\n", "    return dict()\n")),
        ("non-constant default on Metrics field", mut("metrics.py", "cache_hit_ratio: float = 0.0", "cache_hit_ratio: float = len('a')")),
        ("fourth field on Metrics", mut("metrics.py", "    cache_hit_ratio: float = 0.0\n", "    cache_hit_ratio: float = 0.0\n    sneaky: int = 1\n")),
        ("other body changed (parse_stream)", mut("metrics.py", "m.cost_usd += 1", "m.cost_usd += 2")),
        ("other build_report edit", mut("report.py", "float(metrics.cost_usd)", "float(metrics.cost_usd) + 1")),
        ("metrics[...] assignment in build_report",
         mut("report.py", '    return {', '    metrics.tokens = 0.0\n    return {')),
        ("new function name not in section 2", mut("baseline.py", "def check(reports, strict_model=False):",
                                                   "def helper():\n    return 1\n\ndef check(reports, strict_model=False):")),
        ("existing function removed", {**good, "baseline.py": P0_BASELINE.replace("def check(reports, strict_model=False):\n    return 1\n", "")}),
        ("module-level statement changed", mut("baseline.py", "def check", "X = 1\n\ndef check")),
    ]


def self_test() -> int:
    base = {"metrics.py": BASE_METRICS, "report.py": BASE_REPORT, "baseline.py": BASE_BASELINE}
    results = []
    rc, line = run_gate(base, {"metrics.py": P0_METRICS, "report.py": P0_REPORT, "baseline.py": P0_BASELINE})
    results.append(("control: correct P0 accepted", rc == 0 and line == "P0_GATE OK", line))
    rc, line = run_gate(base, base)
    results.append(("identical head (no stub) accepted as inert", rc == 0, line))
    for name, head in _mutations():
        rc, line = run_gate(base, head)
        results.append((f"reject: {name}", rc == 1 and line.startswith("P0_GATE FAIL"), f"rc={rc} {line[:110]}"))
    passed = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(("  ok   " if ok else "  BAD  ") + name + ("" if ok else f" -> {detail}"))
        if ok and name.startswith("reject"):
            print("       " + detail)
    if passed == len(results):
        print(f"SELFTEST OK {passed}/{len(results)}")
        return 0
    print(f"SELFTEST FAIL {passed}/{len(results)}")
    return 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base")
    ap.add_argument("--head")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not (a.base and a.head):
        ap.error("--base and --head are required")
    try:
        base, head = _sources(a.base), _sources(a.head)
    except subprocess.CalledProcessError as exc:
        print(f"P0_GATE ERROR git failed: {exc.stderr.strip()}", file=sys.stderr)
        return 2
    rc, line = run_gate(base, head)
    print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
