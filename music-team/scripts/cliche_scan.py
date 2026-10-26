#!/usr/bin/env python3
"""cliche_scan.py - cliche density gate for concept.md / lyrics.md / plain text
(stage-gates.md section 3). Stdlib only; ``python -I`` safe.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

DEFAULT_LIST = gc.SHARED_DIR / "cliche-list.txt"
CONCEPT_FIELDS = ("title", "hook_line", "central_image")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def normalise(text: str) -> str:
    """Lower-case, collapse every non-alphanumeric run to one space, trim."""
    return _NON_ALNUM.sub(" ", text.lower()).strip()


def load_phrases(path: Path) -> list[str]:
    seen: list[str] = []
    for raw in gc.load_list_file(path):
        p = normalise(raw)
        if p and p not in seen:
            seen.append(p)
    return seen


def collect_lines(path: str) -> list[tuple[str, str]]:
    """Return (location, text) pairs to scan, per the artifact kind."""
    text = gc.read_text(path)
    name = Path(gc.norm(path)).name.lower()
    out: list[tuple[str, str]] = []
    if name == "concept.md":
        fm, _ = gc.parse_frontmatter(text)
        for field in CONCEPT_FIELDS:
            val = fm.get(field)
            if isinstance(val, str) and val.strip():
                out.append((field, val))
        return out
    if name == "lyrics.md":
        for label, lines in gc.parse_sections(text):
            for i, line in enumerate(lines, 1):
                out.append((f"{label}:{i}", line))
        return out
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip() and not line.lstrip().startswith("#"):
            out.append((f"text:{i}", line))
    return out


def scan(lines: list[tuple[str, str]], phrases: list[str]) -> tuple[int, int, list[tuple[str, str]]]:
    """Return (hits, words, [(location, phrase)]).

    Phrases are matched longest-first and every matched word span is masked, so
    a nested list entry ("take my breath away" inside "you take my breath away")
    yields exactly one hit per span. Two distinct phrases on one line still
    count as two hits."""
    ordered = sorted(phrases, key=lambda p: (-len(p.split()), -len(p), p))
    patterns = [(p, re.compile(r"(?<![a-z0-9])" + re.escape(p) + r"(?![a-z0-9])")) for p in ordered]
    hits: list[tuple[str, str]] = []
    words = 0
    for loc, text in lines:
        norm = normalise(text)
        words += len(norm.split())
        consumed = [False] * len(norm)
        for phrase, pat in patterns:
            for m in pat.finditer(norm):
                if any(consumed[m.start():m.end()]):
                    continue
                for i in range(m.start(), m.end()):
                    consumed[i] = True
                hits.append((loc, phrase))
    return len(hits), words, hits


def add_args(p: Any) -> None:
    p.add_argument("--cliche-max-per-100-words", type=float, metavar="N",
                   help="override quality.cliche_max_per_100_words")
    p.add_argument("--cliche-list", metavar="PATH", help="phrase list (default references/shared/cliche-list.txt)")


def main_fn(args: Any, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    genre = gc.resolve_genre(args.genre, args.paths)
    limit = gc.resolve_threshold("cliche_max_per_100_words", config, genre, args.cliche_max_per_100_words,
                                 kind=float)
    res.thresholds["cliche_max_per_100_words"] = limit
    list_path = Path(gc.norm(args.cliche_list)) if args.cliche_list else DEFAULT_LIST
    phrases = load_phrases(list_path)
    if not phrases:
        return res.error(f"cliche list empty or unreadable: {gc.norm(list_path)}")
    targets = [p for p in args.paths if Path(p).name.lower() != "brief.md"]
    if not targets:
        return res.error("no artifact given")
    lines: list[tuple[str, str]] = []
    for p in targets:
        lines.extend(collect_lines(p))
    hits, words, found = scan(lines, phrases)
    if words == 0:
        return res.error("empty text: nothing to scan", gc.norm(targets[0]))
    per_100 = round(hits * 100.0 / words, 3)
    res.metrics.update({"hits": hits, "words": words, "per_100_words": per_100})
    if per_100 > float(limit):
        for loc, phrase in found:
            res.violate(loc, f"cliche: {phrase!r}", per_100, limit)
    return res


def main(argv: list[str] | None = None) -> int:
    return gc.run("cliche_scan.py", "Cliche density gate (hits per 100 words).", add_args, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
