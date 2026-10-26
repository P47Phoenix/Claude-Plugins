#!/usr/bin/env python3
"""structure_check.py - form-template gate for structure.md, plus ``--consistency``
across structure.md, lyrics.md, chords.md, melody.abc, arrangement.md
(stage-gates.md section 3). Stdlib only; ``python -I`` safe.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402
import abc_common as ac  # noqa: E402

TEMPLATES_PATH = gc.DATA_DIR / "form-templates.json"
HEADER_FIELDS = ("key", "mode", "bpm", "time_sig")


# ---------------------------------------------------------------------------
# Templates and form matching
# ---------------------------------------------------------------------------
def load_form_templates(path: Path = TEMPLATES_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data.get("templates", data)


def _match_form(groups: list[dict[str, Any]], labels: list[str]) -> list[int] | None:
    """Return group index per label (backtracking sequence match) or None."""
    compiled = [re.compile(g["label_pattern"]) for g in groups]

    def rec(gi: int, li: int) -> list[int] | None:
        if gi == len(groups):
            return [] if li == len(labels) else None
        g = groups[gi]
        lo, hi = int(g.get("min_repeat", 1)), int(g.get("max_repeat", 1))
        # greedy: take as many as possible, then back off
        n = 0
        while n < hi and li + n < len(labels) and compiled[gi].match(labels[li + n]):
            n += 1
        for take in range(n, lo - 1, -1):
            rest = rec(gi + 1, li + take)
            if rest is not None:
                return [gi] * take + rest
        return None

    return rec(0, 0)


def check_form(structure: dict[str, Any], templates: dict[str, Any], res: gc.GateResult,
               lyrics: list[tuple[str, list[str]]] | None) -> None:
    name = structure["header"].get("form_template")
    sections = structure["sections"]
    if not name:
        res.error("missing form_template", "structure.md:form_template")
        return
    tpl = templates.get(str(name))
    if tpl is None:
        res.error(f"unknown form_template {name!r}", "structure.md:form_template")
        return
    if not sections:
        res.error("no sections in structure.md", "structure.md")
        return
    res.thresholds["form_template"] = name
    labels = [s["label"] for s in sections]
    res.metrics["sections"] = len(labels)
    res.metrics["total_bars"] = sum(s["bars"] for s in sections)
    groups = tpl["sections"]
    assignment = _match_form(groups, labels)
    if assignment is None:
        expected = " ".join(g["label_pattern"] + ("?" if int(g.get("min_repeat", 1)) == 0 else "")
                            for g in groups)
        res.violate("structure.md:sections", f"section sequence does not match form template {name}",
                    " / ".join(labels), expected)
    else:
        for sec, gi in zip(sections, assignment):
            g = groups[gi]
            if not (int(g["min_bars"]) <= sec["bars"] <= int(g["max_bars"])):
                res.violate(sec["label"], "bars outside template range", sec["bars"],
                            [int(g["min_bars"]), int(g["max_bars"])])
    cap = tpl.get("max_total_bars")
    if cap is not None and res.metrics["total_bars"] > int(cap):
        res.violate("structure.md:total_bars", "total bars exceed template cap", res.metrics["total_bars"], int(cap))
    if lyrics is not None:
        by_label = {lbl: lines for lbl, lines in lyrics}
        for sec in sections:
            expected_n = len(sec["meter"])
            got = len(by_label.get(sec["label"], []))
            if got != expected_n:
                res.violate(sec["label"], "lyric line count differs from meter spec line count", got, expected_n)
        known = {sec["label"] for sec in sections}
        for lbl in by_label:
            if lbl not in known:
                res.violate(f"lyrics.md:{lbl}", "lyric section tag absent from structure.md", lbl, "one of " + ", ".join(sorted(known)))


# ---------------------------------------------------------------------------
# Consistency
# ---------------------------------------------------------------------------
def _norm_field(name: str, value: Any) -> str:
    s = str(value).strip()
    if name == "bpm":
        try:
            return str(int(float(s)))
        except ValueError:
            return s
    if name == "key":
        return s[:1].upper() + s[1:] if s else s
    return s.lower() if name == "mode" else s


def _compare(res: gc.GateResult, artifact: str, observed: dict[str, Any], expected: dict[str, Any],
             fields: tuple[str, ...] = HEADER_FIELDS) -> None:
    """Compare ``fields`` of ``observed`` against structure.md. A field the spec
    says must match but the artifact does not declare is a violation with
    observed None, never a silent skip."""
    for field in fields:
        if field not in expected:
            continue
        want = _norm_field(field, expected[field])
        if observed.get(field) is None:
            res.violate(f"{artifact}:{field}", f"{field} missing from {artifact}", None, want)
            continue
        got = _norm_field(field, observed[field])
        if got != want:
            res.violate(f"{artifact}:{field}", f"{field} differs from structure.md", got, want)


def _compare_sections(res: gc.GateResult, artifact: str, got: list[str], want: list[str]) -> None:
    if got != want:
        res.violate(f"{artifact}:sections", "section list differs from structure.md", got, want)


def check_consistency(args: Any, config: dict[str, Any], res: gc.GateResult, structure: dict[str, Any]) -> None:
    genre = gc.resolve_genre(args.genre, args.paths)
    vr = gc.resolve_threshold("vocal_range", config, genre, args.vocal_range)
    if isinstance(vr, str):
        vr = [x.strip() for x in vr.split(",")]
    if not isinstance(vr, (list, tuple)) or len(vr) != 2:
        raise ValueError(f"threshold vocal_range must be [lo, hi], got {vr!r}")
    vr = [gc.resolve_threshold("vocal_range", {}, None, vr[0], kind=int),
          gc.resolve_threshold("vocal_range", {}, None, vr[1], kind=int)]
    res.thresholds["vocal_range"] = vr
    header = structure["header"]
    want_sections = [s["label"] for s in structure["sections"]]
    compared = 0

    chords = gc.file_named(args.paths, "chords.md")
    if chords:
        text = gc.read_text(chords)
        kv = gc.parse_header_keys(text)
        parts = str(kv.get("key") or "").split()
        obs: dict[str, Any] = {}
        if parts:
            obs["key"] = parts[0]
        if len(parts) > 1:
            obs["mode"] = parts[1]
        # chords.md declares only ``key: <tonic> <mode>``; bpm/time_sig live elsewhere
        _compare(res, "chords.md", obs, header, ("key", "mode"))
        _compare_sections(res, "chords.md", [l for l, _ in gc.parse_sections(text)], want_sections)
        compared += 1

    lyrics = gc.file_named(args.paths, "lyrics.md")
    if lyrics:
        _compare_sections(res, "lyrics.md", [l for l, _ in gc.parse_sections(gc.read_text(lyrics))], want_sections)
        compared += 1

    melody = gc.file_named(args.paths, "melody.abc")
    if melody:
        compared += 1
        try:
            abc = ac.parse_abc(gc.read_text(melody))
        except ac.AbcParseError as exc:
            where = f"melody.abc:{exc.line}" if exc.line else "melody.abc"
            res.violate(where, f"ABC parse error: {exc}", None, "parseable ABC")
            abc = None
        if abc is not None:
            observed = {"key": abc["key"], "mode": abc["mode"], "bpm": abc["bpm"], "time_sig": abc["time_sig"]}
            _compare(res, "melody.abc", observed, header)
            _compare_sections(res, "melody.abc", [s["label"] for s in abc["sections"]], want_sections)
            pitches = ac.all_pitches(abc)
            if pitches:
                lo, hi = min(pitches), max(pitches)
                res.metrics["melody_min_pitch"], res.metrics["melody_max_pitch"] = lo, hi
                if lo < vr[0]:
                    res.violate("melody.abc:range", "lowest pitch below vocal_range", lo, vr[0])
                if hi > vr[1]:
                    res.violate("melody.abc:range", "highest pitch above vocal_range", hi, vr[1])

    arrangement = gc.file_named(args.paths, "arrangement.md")
    if arrangement:
        text = gc.read_text(arrangement)
        _compare(res, "arrangement.md", gc.parse_header_keys(text), header)
        _compare_sections(res, "arrangement.md", [r.get("section", "") for r in gc.parse_table(text)], want_sections)
        compared += 1
    res.metrics["artifacts_compared"] = compared


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------
def add_args(p: Any) -> None:
    p.add_argument("--consistency", action="store_true",
                   help="also compare key/mode/bpm/time_sig, section lists, and melody range across artifacts")
    p.add_argument("--vocal-range", metavar="LO,HI", help="override quality.vocal_range (MIDI numbers)")
    p.add_argument("--templates", metavar="PATH", help="form-templates.json override")


def main_fn(args: Any, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    spath = gc.file_named(args.paths, "structure.md")
    if not spath:
        return res.error("structure.md not given")
    structure = gc.parse_structure(gc.read_text(spath))
    templates = load_form_templates(Path(gc.norm(args.templates)) if args.templates else TEMPLATES_PATH)
    lyrics_path = gc.file_named(args.paths, "lyrics.md")
    lyrics = gc.parse_sections(gc.read_text(lyrics_path)) if lyrics_path else None
    check_form(structure, templates, res, lyrics)
    if res.status == gc.ERROR:
        return res
    if args.consistency:
        check_consistency(args, config, res, structure)
    return res


def main(argv: list[str] | None = None) -> int:
    return gc.run("structure_check.py", "Form-template and cross-artifact consistency gate.", add_args, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
