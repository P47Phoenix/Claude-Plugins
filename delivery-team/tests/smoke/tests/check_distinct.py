#!/usr/bin/env python3
"""AC-5.5c distinctness checker (PA-15, ADR-lmr-004 section 5).

    python3 tests/check_distinct.py <baseline.json | streams-dir | s1.jsonl s2.jsonl ...> [--expect N]
    python3 tests/check_distinct.py --self-test

Independent of lib/metrics.py. Requirements across the sample streams:
  * distinct stream sha256
  * distinct, non-empty session_id
  * pairwise NON-overlapping message.id sets (assistant events). If any
    assistant event lacks message.id, the event `uuid` field is used instead
    for every stream; if that is missing too, the result is WEAKENED.
Prints `AC-5.5c OK n=<k> id_source=<message.id|uuid>` rc 0, or
`AC-5.5c WEAKENED <reason>` rc 1 (a WEAKENED result is a FAIL of AC-5.5c at UAT
unless a dated PO waiver file exists; never silent). rc 2 on unreadable input.
Baseline JSON input: also requires `samples[]` `stream_sha256` to match the file
bytes, and the file count to equal --expect (default 5; 0 disables).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path


def _events(path: Path) -> list[dict]:
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            out.append(obj)
    return out


def _facts(path: Path) -> dict:
    evs = _events(path)
    session = None
    mids: set[str] = set()
    uuids: set[str] = set()
    missing_mid = 0
    assistants = 0
    for e in evs:
        if session is None and isinstance(e.get("session_id"), str) and e["session_id"]:
            session = e["session_id"]
        if e.get("type") == "assistant":
            assistants += 1
            msg = e.get("message") if isinstance(e.get("message"), dict) else {}
            mid = msg.get("id")
            if isinstance(mid, str) and mid:
                mids.add(mid)
            else:
                missing_mid += 1
            u = e.get("uuid")
            if isinstance(u, str) and u:
                uuids.add(u)
    return {
        "sha": hashlib.sha256(path.read_bytes()).hexdigest(),
        "session": session,
        "mids": mids,
        "uuids": uuids,
        "assistants": assistants,
        "missing_mid": missing_mid,
    }


def evaluate(paths: list[Path], expect: int = 5, recorded_sha: list[str | None] | None = None) -> tuple[int, str]:
    if expect and len(paths) != expect:
        return 1, f"AC-5.5c WEAKENED expected {expect} streams, found {len(paths)}"
    if len(paths) < 2:
        return 1, "AC-5.5c WEAKENED fewer than 2 streams"
    facts = [_facts(p) for p in paths]
    if recorded_sha:
        for p, f, rec in zip(paths, facts, recorded_sha):
            if rec is not None and rec != f["sha"]:
                return 1, f"AC-5.5c WEAKENED stream_sha256 mismatch for {p.name}"
    if len({f["sha"] for f in facts}) != len(facts):
        return 1, "AC-5.5c WEAKENED identical stream hashes"
    sessions = [f["session"] for f in facts]
    if any(not s for s in sessions):
        return 1, "AC-5.5c WEAKENED a stream has no session_id"
    if len(set(sessions)) != len(sessions):
        return 1, "AC-5.5c WEAKENED duplicate session_id"
    if all(f["assistants"] > 0 and f["missing_mid"] == 0 for f in facts):
        key, source = "mids", "message.id"
    elif all(f["uuids"] for f in facts):
        key, source = "uuids", "uuid"
    else:
        return 1, "AC-5.5c WEAKENED no message.id and no uuid on the streams (hash and session_id only)"
    for i in range(len(facts)):
        for j in range(i + 1, len(facts)):
            shared = facts[i][key] & facts[j][key]
            if shared:
                return 1, (f"AC-5.5c WEAKENED {source} overlap between {paths[i].name} and "
                           f"{paths[j].name} ({len(shared)} shared)")
    return 0, f"AC-5.5c OK n={len(paths)} id_source={source}"


def resolve(target: list[str]) -> tuple[list[Path], list[str | None] | None]:
    if len(target) == 1 and target[0].endswith(".json"):
        bp = Path(target[0])
        data = json.loads(bp.read_text(encoding="utf-8"))
        samples = data.get("samples")
        if not isinstance(samples, list) or not samples:
            raise ValueError("baseline has no samples[] list")
        paths, shas = [], []
        for s in samples:
            sf = Path(s.get("stream_file", ""))
            cands = [sf, bp.parent / sf, bp.parent / sf.name]
            found = next((c for c in cands if c.is_file()), None)
            if found is None:
                raise ValueError(f"stream file not found: {sf}")
            paths.append(found)
            shas.append(s.get("stream_sha256"))
        return paths, shas
    if len(target) == 1 and Path(target[0]).is_dir():
        return sorted(Path(target[0]).glob("*.jsonl")), None
    return [Path(t) for t in target], None


def _stream(session, mids, *, with_uuid=False, with_mid=True, tag="") -> str:
    lines = [json.dumps({"type": "system", "subtype": "init", "session_id": session, "model": "claude-opus-fixture"})]
    for i, m in enumerate(mids):
        msg = {"model": "claude-opus-fixture", "usage": {"input_tokens": 1}}
        if with_mid:
            msg["id"] = m
        ev = {"type": "assistant", "message": msg}
        if with_uuid:
            ev["uuid"] = f"u-{m}"
        lines.append(json.dumps(ev))
    lines.append(json.dumps({"type": "result", "total_cost_usd": 0.01, "tag": tag}))
    return "\n".join(lines) + "\n"


def self_test() -> int:
    results = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        def mk(name, texts):
            d = root / name
            d.mkdir()
            ps = []
            for i, t in enumerate(texts):
                p = d / f"sample-{i + 1}.jsonl"
                p.write_text(t)
                ps.append(p)
            return d, ps

        def case(name, texts, want_rc, want_sub, expect=5):
            d, ps = mk(name.replace(" ", "_"), texts)
            rc, line = evaluate(ps, expect)
            results.append((name, rc == want_rc and want_sub in line, f"rc={rc} {line}"))
            return d

        good = [_stream(f"s{i}", [f"m{i}a", f"m{i}b"], tag=str(i)) for i in range(5)]
        gd = case("distinct streams OK", good, 0, "AC-5.5c OK")
        case("5 identical copies WEAKENED", [good[0]] * 5, 1, "WEAKENED")
        case("no message.id and no uuid WEAKENED",
             [_stream(f"s{i}", [f"m{i}"], with_mid=False, tag=str(i)) for i in range(5)], 1, "no message.id and no uuid")
        case("uuid fallback OK",
             [_stream(f"s{i}", [f"m{i}"], with_mid=False, with_uuid=True, tag=str(i)) for i in range(5)], 0, "id_source=uuid")
        case("overlapping message.id WEAKENED",
             [_stream(f"s{i}", ["shared", f"m{i}"], tag=str(i)) for i in range(5)], 1, "overlap")
        case("duplicate session_id WEAKENED",
             [_stream("same", [f"m{i}"], tag=str(i)) for i in range(5)], 1, "duplicate session_id")
        case("missing session_id WEAKENED",
             ["\n".join(json.dumps(json.loads(l)) for l in _stream("s", [f"m{i}"], tag=str(i)).splitlines()[1:]) + "\n"
              for i in range(5)], 1, "no session_id")
        case("wrong stream count WEAKENED", good[:4], 1, "expected 5")
        # baseline JSON form: sha must match the file
        bj = root / "baseline.json"
        bj.write_text(json.dumps({"samples": [
            {"stream_file": str(p), "stream_sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(gd.glob("*.jsonl"))]}))
        paths, shas = resolve([str(bj)])
        rc, line = evaluate(paths, 5, shas)
        results.append(("baseline json form OK", rc == 0, f"rc={rc} {line}"))
        data = json.loads(bj.read_text())
        data["samples"][0]["stream_sha256"] = "0" * 64
        bj.write_text(json.dumps(data))
        paths, shas = resolve([str(bj)])
        rc, line = evaluate(paths, 5, shas)
        results.append(("baseline json wrong sha WEAKENED", rc == 1 and "sha256 mismatch" in line, f"rc={rc} {line}"))
    passed = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        print(("  ok   " if ok else "  BAD  ") + name + "  " + detail)
    if passed == len(results):
        print(f"SELFTEST OK {passed}/{len(results)}")
        return 0
    print(f"SELFTEST FAIL {passed}/{len(results)}")
    return 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="*")
    ap.add_argument("--expect", type=int, default=5)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.target:
        ap.error("a baseline json, a streams directory, or stream files are required")
    try:
        paths, shas = resolve(a.target)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"AC-5.5c ERROR {exc}", file=sys.stderr)
        return 2
    rc, line = evaluate(paths, a.expect, shas)
    print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
