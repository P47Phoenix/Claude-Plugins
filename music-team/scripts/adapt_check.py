#!/usr/bin/env python3
"""adapt_check.py - disposition gate for adaptation-report.md (ADAPT_GENRE, Stage 7p;
stage-gates.md section 3). Stdlib only; ``python -I`` safe.

    adapt_check.py [--config C] [--json] [--genre G] [--max-changed N] report.md [artifact paths...]

PASS when the report has: front-matter ``song_type: ADAPT_GENRE`` plus ``source_genre`` and
``target_genre`` that both resolve to a ``references/shared/genres/<slug>.md`` profile (by its
``genre:`` or ``aliases:``); a non-empty ``## Kept`` list; a ``## Changed`` table with the four
columns ``Element | Source | Target | Why``, every cell filled, at most ``--max-changed`` rows
(else ``adaptation.max_changed_elements``, else 12); non-empty ``## Lyric re-fit`` and ``## Risks``.
FAIL lists each missing or empty disposition. ERROR (3) on a malformed table. SKIPPED (2) when the
report is absent and ``adaptation.require_report`` is false. Extra artifact paths (structure.md,
lyrics.md, ...) are used only for advisory warnings: a structure.md section the report never mentions.
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

GENRES_DIR = gc.SHARED_DIR / "genres"
COLUMNS = ["element", "source", "target", "why"]
REQUIRED_SECTIONS = ("kept", "changed", "lyric re-fit", "risks")
DEFAULT_MAX_CHANGED = 12


def _norm_label(label: str) -> str:
    return re.sub(r"[\s_\-]+", " ", str(label).strip().lower())


def genre_labels(genres_dir: Path = GENRES_DIR) -> dict[str, str]:
    """Map every normalised genre label and alias to its profile slug."""
    out: dict[str, str] = {}
    for path in sorted(genres_dir.glob("*.md")):
        try:
            fm, _ = gc.parse_frontmatter(gc.read_text(path))
        except (OSError, ValueError):
            continue
        names = [path.stem, fm.get("genre")]
        aliases = fm.get("aliases")
        names += aliases if isinstance(aliases, list) else [aliases]
        for n in names:
            if isinstance(n, str) and n.strip():
                out[_norm_label(n)] = path.stem
    return out


def split_sections(body: str) -> dict[str, list[str]]:
    """Level-2 headings -> body lines (heading text lower-cased)."""
    sections: dict[str, list[str]] = {}
    current: list[str] | None = None
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = sections.setdefault(m.group(1).strip().lower(), [])
            continue
        if current is not None:
            current.append(line)
    return sections


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_changed(lines: list[str]) -> tuple[list[tuple[int, list[str]]], str | None]:
    """Return ([(index, cells)], error). Error text means the table is malformed."""
    pipe = [(i, l) for i, l in enumerate(lines) if l.strip().startswith("|")]
    if not pipe:
        return [], "no table under ## Changed (expected | Element | Source | Target | Why |)"
    header = [c.lower() for c in _cells(pipe[0][1])]
    if header != COLUMNS:
        return [], f"header is {header}, expected {COLUMNS}"
    rows: list[tuple[int, list[str]]] = []
    for _, line in pipe[1:]:
        cells = _cells(line)
        if gc.is_separator_row(cells):
            continue
        n = len(rows) + 1
        if len(cells) != len(COLUMNS):
            return [], f"row {n} has {len(cells)} cells, expected {len(COLUMNS)}"
        rows.append((n, cells))
    return rows, None


def _bullets(lines: list[str]) -> list[str]:
    return [l.strip() for l in lines if re.match(r"^\s*[-*]\s+\S", l)]


def _has_text(lines: list[str]) -> bool:
    return any(l.strip() for l in lines)


def check_report(text: str, rpath: str, max_changed: int, genres: dict[str, str],
                 res: gc.GateResult) -> None:
    """Run every report check, recording violations on ``res``."""
    fm, body = gc.parse_frontmatter(text)
    if str(fm.get("song_type") or "") != "ADAPT_GENRE":
        res.violate(f"{rpath}:front-matter", "song_type must be ADAPT_GENRE", fm.get("song_type"), "ADAPT_GENRE")
    for key in ("source_genre", "target_genre"):
        val = fm.get(key)
        if not isinstance(val, str) or not val.strip():
            res.violate(f"{rpath}:front-matter", f"{key} missing or empty", val, "a genre label")
        elif _norm_label(val) not in genres:
            res.violate(f"{rpath}:front-matter", f"{key} does not resolve to a genre profile", val,
                        "genre or alias in references/shared/genres/")
    res.metrics["source_genre"] = fm.get("source_genre")
    res.metrics["target_genre"] = fm.get("target_genre")

    secs = split_sections(body)
    for name in REQUIRED_SECTIONS:
        if name not in secs:
            res.violate(f"{rpath}:## {name.title() if name != 'lyric re-fit' else 'Lyric re-fit'}",
                        "required section missing", None, "present")

    if "kept" in secs:
        kept = _bullets(secs["kept"])
        res.metrics["kept"] = len(kept)
        if not kept:
            res.violate(f"{rpath}:## Kept", "no preserved elements listed (empty disposition)", 0, ">= 1")

    if "changed" in secs:
        rows, err = parse_changed(secs["changed"])
        if err:
            res.error(err, f"{rpath}:## Changed")
            return
        res.metrics["changed"] = len(rows)
        if not rows:
            res.violate(f"{rpath}:## Changed", "table has no rows (empty disposition)", 0, ">= 1")
        if len(rows) > max_changed:
            res.violate(f"{rpath}:## Changed", "more changed elements than allowed", len(rows), max_changed)
        for n, cells in rows:
            for col, cell in zip(COLUMNS, cells):
                if not cell or set(cell) <= set("-–—."):
                    res.violate(f"{rpath}:## Changed:row {n}",
                                f"empty '{col}' cell (element '{cells[0] or '?'}')", cell, "non-empty")

    for name, label in (("lyric re-fit", "Lyric re-fit"), ("risks", "Risks")):
        if name in secs and not _has_text(secs[name]):
            res.violate(f"{rpath}:## {label}", "section is empty", 0, ">= 1 line")


def warn_unmentioned_sections(structure_path: str, report_text: str, rpath: str, res: gc.GateResult) -> None:
    structure = gc.parse_structure(gc.read_text(structure_path))
    missing = [s["label"] for s in structure["sections"] if s["label"].lower() not in report_text]
    res.metrics["structure_sections"] = len(structure["sections"])
    for label in missing:
        res.warn(f"{rpath}", f"structure.md section '{label}' is not mentioned in the report", label, "mentioned")


def main_fn(args: Any, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    require = gc.resolve_threshold("require_report", config, None, section="adaptation", default=True, kind=bool)
    max_changed = gc.resolve_threshold("max_changed_elements", config, None,
                                       getattr(args, "max_changed", None), section="adaptation",
                                       default=DEFAULT_MAX_CHANGED, kind=int)
    if max_changed < 1:
        raise ValueError("max_changed_elements must be >= 1")
    res.thresholds.update({"require_report": require, "max_changed_elements": max_changed})

    rpath = gc.file_named(args.paths, "adaptation-report.md") or (args.paths[0] if args.paths else None)
    if rpath is None or not Path(gc.norm(rpath)).is_file():
        if not require:
            return res.skip("adaptation-report.md absent and adaptation.require_report is false")
        shown = gc.norm(rpath) if rpath else "adaptation-report.md"
        res.violate(shown, "adaptation-report.md is missing and adaptation.require_report is true", None, "present")
        return res

    rpath = gc.norm(rpath)
    check_report(gc.read_text(rpath), rpath, max_changed, genres=genre_labels(), res=res)
    if res.status == gc.ERROR:
        return res
    structure = gc.file_named([p for p in args.paths if gc.norm(p) != rpath], "structure.md")
    if structure and Path(structure).is_file():
        warn_unmentioned_sections(structure, gc.read_text(rpath).lower(), rpath, res)
    return res


def add_args(p: Any) -> None:
    p.add_argument("--max-changed", type=int, metavar="N",
                   help="max rows in ## Changed (else adaptation.max_changed_elements, else 12)")
    p.add_argument("--selftest", action="store_true", help="run the built-in self-test and exit")


GOOD = """---
song_type: ADAPT_GENRE
source_genre: folk
target_genre: bossa nova
---

## Kept
- hook line, title idea, first-person voice

## Changed

| Element | Source | Target | Why |
|---------|--------|--------|-----|
| bpm | 72 | 120 | bossa pulse |
| time_sig | 3/4 | 4/4 | straight-eighth feel |

## Lyric re-fit
- Verse 1: 11 syllables per line -> 7-8; rhyme AABB kept

## Risks
- shortened lines lose a small image
"""


def selftest() -> int:
    """Exercise PASS, FAIL, ERROR, and SKIPPED paths in a temp dir. Exit 0 on success."""
    failures: list[str] = []

    def run(report: str | None, *extra: str) -> int:
        with tempfile.TemporaryDirectory() as tmp:
            args = list(extra)
            if report is not None:
                p = Path(tmp) / "adaptation-report.md"
                p.write_text(report, encoding="utf-8", newline="\n")
                args.append(str(p))
            return _quiet_main(args)

    def expect(name: str, got: int, want: int) -> None:
        if got != want:
            failures.append(f"{name}: expected exit {want}, got {got}")

    expect("pass", run(GOOD), 0)
    expect("empty why", run(GOOD.replace("| bossa pulse |", "|  |")), 1)
    expect("missing kept", run(GOOD.replace("- hook line, title idea, first-person voice", "")), 1)
    expect("unknown genre", run(GOOD.replace("bossa nova", "nowhere pop")), 1)
    expect("over max", run(GOOD, "--max-changed", "1"), 1)
    expect("bad header", run(GOOD.replace("| Why |", "| Reason |")), 3)
    expect("absent required", run(None, "--max-changed", "3"), 1)
    for msg in failures:
        sys.stderr.write(f"selftest FAIL {msg}\n")
    sys.stdout.write("adapt_check selftest: " + ("FAIL\n" if failures else "OK\n"))
    return 1 if failures else 0


def _quiet_main(argv: list[str]) -> int:
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        return main(argv)


def main(argv: list[str] | None = None) -> int:
    raw = sys.argv[1:] if argv is None else argv
    if "--selftest" in raw:
        return selftest()
    return gc.run("adapt_check.py", "Fail when adaptation-report.md leaves any kept/changed disposition empty.",
                  add_args, main_fn, raw)


if __name__ == "__main__":
    sys.exit(main())
