#!/usr/bin/env python3
"""Red-first and ordering checker (PA-13, FR-4.4, ADR-lmr-004 section 6 items 2 to 4).

    python3 tests/check_red_first.py --base <base_sha> [--manifest FILE] [--worktree]
    python3 tests/check_red_first.py --self-test

Prints `RED_FIRST OK failed=<n> void=0` rc 0, or `RED_FIRST FAIL <reasons>` rc 1
(rc 2 on git or environment errors). Authored by the validator.

History checks (derived, not self-recorded):
  * validator commits = commits in base..HEAD touching test_model_capture.py or
    tests/fixtures/stream_real_shape*; validator_start = parent of the first,
    validator_end = the last.
  * `lib/` and run_smoke.py are identical between validator_start and validator_end.
  * fix commits = commits in base..HEAD touching lib/ that are not ancestors of
    validator_start; the first validator commit must be an ancestor of the first
    fix commit (`merge-base --is-ancestor`). No fix commits yet is fine.
  * `Dispatch-Id` trailers: producer (lib/ commits) and validator sets are
    non-empty and disjoint; with --manifest every validator id appears in it.
    The placeholder `pending-orchestrator` is reported as UNRESOLVED and never
    counted as an id.
Red run (at validator_start): the validator test file and fixtures are overlaid
on the tree as of validator_start and run with --junitxml. Every test must be
COLLECTED and FAILED with message starting `AssertionError` or
`Failed: DID NOT RAISE`; ImportError, ModuleNotFoundError, SyntaxError,
TypeError, AttributeError, NameError, NotImplementedError, any <error>, any
skip and any pass void the evidence. At least one real_shape test and one
capture-failure test must be present.
"""
from __future__ import annotations

import argparse
import io
import re
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

SMOKE = "delivery-team/tests/smoke"
LIB = [f"{SMOKE}/lib", f"{SMOKE}/run_smoke.py"]
VALIDATOR = [f"{SMOKE}/tests/test_model_capture.py", f"{SMOKE}/tests/fixtures/stream_real_shape.jsonl",
             f"{SMOKE}/tests/fixtures/stream_real_shape.provenance.txt"]
PERMITTED = ("AssertionError", "Failed: DID NOT RAISE")
VOID = ("ImportError", "ModuleNotFoundError", "SyntaxError", "TypeError", "AttributeError", "NameError",
        "NotImplementedError")
PLACEHOLDER = "pending-orchestrator"


def git(repo: str, *args: str, check=True) -> str:
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def _commits(repo, rng, paths):
    out = git(repo, "log", "--reverse", "--format=%H", rng, "--", *paths).split()
    return out


def _trailer_ids(repo, shas):
    ids, unresolved = set(), 0
    missing = []
    for s in shas:
        body = git(repo, "show", "-s", "--format=%B", s)
        m = re.findall(r"^Dispatch-Id:\s*(\S+)\s*$", body, re.M)
        if not m:
            missing.append(s[:8])
        for i in m:
            if i == PLACEHOLDER:
                unresolved += 1
            else:
                ids.add(i)
    return ids, unresolved, missing


def check_history(repo: str, base: str, manifest: Path | None = None) -> tuple[list[str], dict]:
    probs: list[str] = []
    info: dict = {}
    v_commits = _commits(repo, f"{base}..HEAD", VALIDATOR)
    if not v_commits:
        return ["no validator commits touching test_model_capture.py or the fixtures in base..HEAD"], info
    start = git(repo, "rev-parse", f"{v_commits[0]}^").strip()
    end = v_commits[-1]
    info.update(validator_start=start, validator_end=end, validator_commits=len(v_commits))

    if git(repo, "diff", "--name-only", start, end, "--", *LIB).strip():
        probs.append("lib/ changed between validator_start and validator_end")
    lib_commits = _commits(repo, f"{base}..HEAD", LIB)
    fixes = [c for c in lib_commits
             if subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor", c, start]).returncode != 0]
    info["fix_commits"] = len(fixes)
    if fixes:
        if subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor", v_commits[0], fixes[0]]).returncode != 0:
            probs.append("first validator commit is not an ancestor of the first fix commit")
    prod_ids, prod_unres, prod_missing = _trailer_ids(repo, lib_commits)
    val_ids, val_unres, val_missing = _trailer_ids(repo, v_commits)
    if prod_missing:
        probs.append(f"lib commits without Dispatch-Id: {prod_missing}")
    if val_missing:
        probs.append(f"validator commits without Dispatch-Id: {val_missing}")
    if not prod_ids and not prod_unres:
        probs.append("no producer Dispatch-Id found")
    both = prod_ids & val_ids
    if both:
        probs.append(f"producer and validator Dispatch-Id overlap: {sorted(both)}")
    info["unresolved_ids"] = prod_unres + val_unres
    if manifest is not None:
        listed = set()
        for line in manifest.read_text(encoding="utf-8").splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) >= 2:
                listed.add(parts[1].strip())
        gone = val_ids - listed
        if gone:
            probs.append(f"validator Dispatch-Id not in manifest: {sorted(gone)}")
    return probs, info


def evaluate_junit(xml_text: str, pytest_rc: int) -> tuple[list[str], int, int]:
    """Returns (problems, failed_count, void_count)."""
    probs: list[str] = []
    failed = void = 0
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        return [f"junit xml unreadable: {exc}"], 0, 0
    cases = list(root.iter("testcase"))
    if pytest_rc != 1:
        probs.append(f"pytest exit {pytest_rc} (need 1; 2 is a collection error)")
    if not cases:
        probs.append("no tests collected")
    real = capture = 0
    blocked = 0
    for tc in cases:
        name = tc.get("name", "?")
        if "real_shape" in name:
            real += 1
        if "capture_fails" in name:
            capture += 1
        fail, err, skip = tc.find("failure"), tc.find("error"), tc.find("skipped")
        if err is not None:
            void += 1
            probs.append(f"{name}: <error> voids the evidence ({(err.get('message') or '')[:60]})")
        elif skip is not None:
            msg = skip.get("message") or ""
            if msg.startswith("blocked_on H1"):
                blocked += 1
            probs.append(f"{name}: skipped, not FAILED ({msg[:60]})")
        elif fail is None:
            probs.append(f"{name}: PASSED against the stub (a passing test is not red)")
        else:
            msg = (fail.get("message") or "").lstrip()
            if msg.startswith(VOID):
                void += 1
                probs.append(f"{name}: void failure type ({msg[:60]})")
            elif msg.startswith(PERMITTED):
                failed += 1
            else:
                void += 1
                probs.append(f"{name}: failure does not start with AssertionError or Failed: DID NOT RAISE ({msg[:60]})")
    if cases and not real:
        probs.append("no real_shape test collected")
    if cases and not capture:
        probs.append("no capture-failure test collected")
    if blocked:
        probs.append(f"BLOCKED: {blocked} test(s) skipped with blocked_on H1 (real fixture not captured)")
    return probs, failed, void


def red_run(repo: str, start: str, worktree: bool) -> tuple[list[str], int, int]:
    with tempfile.TemporaryDirectory() as td:
        def extract(rev_or_tree, paths):
            data = subprocess.run(["git", "-C", repo, "archive", rev_or_tree, "--", *paths],
                                  capture_output=True, check=True).stdout
            with tarfile.open(fileobj=io.BytesIO(data)) as tf:
                tf.extractall(td)
        extract(start, [SMOKE])
        top = git(repo, "rev-parse", "--show-toplevel").strip()
        if worktree:
            import shutil
            for rel in VALIDATOR:
                src = Path(top) / rel
                if src.is_file():
                    dst = Path(td) / rel
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
        else:
            present = [p for p in VALIDATOR if git(repo, "ls-tree", "HEAD", "--", p).strip()]
            if present:
                extract("HEAD", present)
        xml = Path(td) / "red.xml"
        test = Path(td) / SMOKE / "tests" / "test_model_capture.py"
        if not test.is_file():
            return ["test_model_capture.py absent"], 0, 0
        r = subprocess.run([sys.executable, "-m", "pytest", str(test), "-q", "-p", "no:cacheprovider",
                            f"--junitxml={xml}"], cwd=td, capture_output=True, text=True)
        if not xml.is_file():
            return [f"pytest produced no junit xml (rc {r.returncode}): {r.stdout[-200:]}"], 0, 0
        return evaluate_junit(xml.read_text(encoding="utf-8"), r.returncode)


def run(repo: str, base: str, manifest: Path | None, worktree: bool) -> tuple[int, str]:
    hp, info = check_history(repo, base, manifest)
    if "validator_start" not in info:
        return 1, "RED_FIRST FAIL " + "; ".join(hp)
    rp, failed, void = red_run(repo, info["validator_start"], worktree)
    probs = hp + rp
    note = (f"validator_start={info['validator_start'][:10]} validator_end={info['validator_end'][:10]} "
            f"fix_commits={info['fix_commits']} unresolved_ids={info['unresolved_ids']}")
    if probs:
        return 1, f"RED_FIRST FAIL failed={failed} void={void} :: " + "; ".join(probs) + f" :: {note}"
    return 0, f"RED_FIRST OK failed={failed} void={void}"


# ----------------------------------------------------------------- self-test

def _junit(cases) -> str:
    out = ['<testsuites><testsuite>']
    for name, kind, msg in cases:
        out.append(f'<testcase name="{name}">')
        if kind:
            out.append(f'<{kind} message="{msg}"/>')
        out.append("</testcase>")
    out.append("</testsuite></testsuites>")
    return "".join(out)


BASE_OK = [("test_real_shape_a", "failure", "AssertionError: x"),
           ("test_capture_fails_b", "failure", "Failed: DID NOT RAISE &lt;class X&gt;")]


def _junit_cases():
    ok = _junit(BASE_OK)
    yield "good red run", ok, 1, True
    for v in VOID:
        bad = _junit([BASE_OK[0], ("test_capture_fails_b", "failure", f"{v}: boom")])
        yield f"void {v}", bad, 1, False
    yield "an <error> (collection or setup)", _junit([BASE_OK[0], ("test_capture_fails_b", "error", "collection")]), 1, False
    yield "a passing test", _junit(BASE_OK + [("test_other", None, "")]), 1, False
    yield "a skipped test", _junit(BASE_OK + [("test_real_shape_c", "skipped", "blocked_on H1: no fixture")]), 1, False
    yield "unpermitted failure type ValueError", _junit([BASE_OK[0], ("test_capture_fails_b", "failure", "ValueError: x")]), 1, False
    yield "pytest exit 2 (collection error)", ok, 2, False
    yield "pytest exit 0", ok, 0, False
    yield "nothing collected", "<testsuites><testsuite/></testsuites>", 5, False
    yield "no real_shape test", _junit([BASE_OK[1]]), 1, False
    yield "no capture-failure test", _junit([BASE_OK[0]]), 1, False


def _mk_repo(td: Path, steps) -> str:
    repo = str(td)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.invalid")
    git(repo, "config", "user.name", "t")
    (td / SMOKE / "lib").mkdir(parents=True)
    (td / SMOKE / "tests").mkdir(parents=True)
    (td / SMOKE / "lib" / "x.py").write_text("v = 0\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base")
    base = git(repo, "rev-parse", "HEAD").strip()
    n = 0
    for kind, ident in steps:
        n += 1
        f = td / SMOKE / "lib" / "x.py" if kind == "lib" else td / SMOKE / "tests" / "test_model_capture.py"
        f.write_text(f"v = {n}\n")
        git(repo, "add", "-A")
        msg = f"c{n} {kind}" + (f"\n\nDispatch-Id: {ident}\n" if ident else "\n")
        git(repo, "commit", "-q", "-m", msg)
    return base


def self_test() -> int:
    results = []
    for name, xml, rc, want_ok in _junit_cases():
        probs, failed, void = evaluate_junit(xml, rc)
        ok = (not probs) == want_ok
        results.append((f"junit: {name}", ok, "; ".join(probs)[:100]))
    hist = [
        ("P0, V, fix in order", [("lib", "A"), ("test", "B"), ("lib", "A")], True),
        ("P0, V (no fix yet)", [("lib", "A"), ("test", "B")], True),
        ("two lib commits (P0 in two steps) before validator", [("lib", "A"), ("lib", "A"), ("test", "B")], True),  # P0 has 2 lib commits: both precede V
        ("lib edited between validator commits", [("lib", "A"), ("test", "B"), ("lib", "A"), ("test", "B")], False),
        ("same id for producer and validator", [("lib", "A"), ("test", "A"), ("lib", "A")], False),
        ("validator commit lacks Dispatch-Id", [("lib", "A"), ("test", None)], False),
        ("lib commit lacks Dispatch-Id", [("lib", None), ("test", "B")], False),
        ("no validator commit at all", [("lib", "A")], False),
    ]
    for name, steps, want_ok in hist:
        with tempfile.TemporaryDirectory() as td:
            base = _mk_repo(Path(td), steps)
            probs, _ = check_history(td, base)
        results.append((f"history: {name}", (not probs) == want_ok, "; ".join(probs)[:100]))
    with tempfile.TemporaryDirectory() as td:
        base = _mk_repo(Path(td), [("lib", "A"), ("test", "B")])
        mf = Path(td) / "m.txt"
        mf.write_text("expected_validators: 1\nqa\tB\n")
        probs, _ = check_history(td, base, mf)
        results.append(("history: manifest lists validator id", not probs, "; ".join(probs)))
        mf.write_text("expected_validators: 1\nqa\tZZZ\n")
        probs, _ = check_history(td, base, mf)
        results.append(("history: validator id missing from manifest", bool(probs), "; ".join(probs)))
    passed = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(("  ok   " if ok else "  BAD  ") + name + ("" if ok else f" -> {detail}"))
    if passed == len(results):
        print(f"SELFTEST OK {passed}/{len(results)}")
        return 0
    print(f"SELFTEST FAIL {passed}/{len(results)}")
    return 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base")
    ap.add_argument("--manifest")
    ap.add_argument("--worktree", action="store_true", help="overlay validator files from the working tree instead of HEAD")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.base:
        ap.error("--base is required")
    try:
        rc, line = run(".", a.base, Path(a.manifest) if a.manifest else None, a.worktree)
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"RED_FIRST ERROR {exc}", file=sys.stderr)
        return 2
    print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
