#!/usr/bin/env python3
"""resemblance_check.py - word 5-gram overlap between the lyric and an opt-in
resemblance corpus (stage-gates.md section 3). Stdlib only; ``python -I`` safe.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

N = 5
_WORD = re.compile(r"[a-z0-9']+")


def tokenize(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def lyric_lines(path: str) -> list[tuple[str, str]]:
    """(location, text) pairs: ``<Label>:<n>`` for lyrics.md, ``text:<n>`` otherwise."""
    text = gc.read_text(path)
    if Path(gc.norm(path)).name.lower() == "lyrics.md" or gc.parse_sections(text):
        return [(f"{label}:{i}", line) for label, lines in gc.parse_sections(text)
                for i, line in enumerate(lines, 1)]
    return [(f"text:{i}", line) for i, line in enumerate(text.splitlines(), 1)
            if line.strip() and not line.lstrip().startswith("#")]


def ngrams(tokens: list[str], n: int = N) -> list[tuple[str, ...]]:
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def lyric_ngrams(lines: list[tuple[str, str]]) -> list[tuple[tuple[str, ...], str]]:
    """Every 5-gram of the lyric token stream with the location of its first word."""
    tokens: list[str] = []
    locs: list[str] = []
    for loc, text in lines:
        toks = tokenize(text)
        tokens.extend(toks)
        locs.extend([loc] * len(toks))
    return [(g, locs[i]) for i, g in enumerate(ngrams(tokens))]


def resolve_corpus(args: Any, config: dict[str, Any]) -> list[str]:
    if args.corpus:
        return [gc.norm(c) for c in args.corpus]
    orig = config.get("originality", {}) if isinstance(config, dict) else {}
    listed = orig.get("resemblance_corpus", []) if isinstance(orig, dict) else []
    if isinstance(listed, str):
        listed = [listed]
    base = Path(gc.norm(args.config)).resolve().parent if args.config else Path.cwd()
    out: list[str] = []
    for item in listed or []:
        p = Path(gc.norm(str(item)))
        if not p.is_absolute() and not p.exists() and (base / p).exists():
            p = base / p
        out.append(gc.norm(p))
    return out


def add_args(p: Any) -> None:
    p.add_argument("--corpus", action="append", metavar="PATH",
                   help="corpus lyric file (repeatable; overrides originality.resemblance_corpus)")
    p.add_argument("--ngram-max-overlap", type=float, metavar="RATIO", help="override originality.ngram_max_overlap")


def main_fn(args: Any, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    limit = gc.resolve_threshold("ngram_max_overlap", config, None, args.ngram_max_overlap, section="originality")
    res.thresholds["ngram_max_overlap"] = limit
    corpus = resolve_corpus(args, config)
    present = [c for c in corpus if Path(c).is_file()]
    missing = [c for c in corpus if c not in present]
    res.metrics["missing_files"] = len(missing)
    if not corpus:
        return res.skip("resemblance_corpus is empty")
    if not present:
        return res.skip("every corpus file is missing: " + ", ".join(missing))
    targets = [p for p in args.paths if Path(p).name.lower() != "brief.md"]
    if not targets:
        return res.error("no lyric file given")
    lines: list[tuple[str, str]] = []
    for t in targets:
        lines.extend(lyric_lines(t))
    total_words = sum(len(tokenize(t)) for _, t in lines)
    if total_words < N:
        return res.error(f"lyric text has fewer than {N} words", gc.norm(targets[0]))
    grams = lyric_ngrams(lines)
    corpus_set: set[tuple[str, ...]] = set()
    for c in present:
        corpus_set.update(ngrams(tokenize(gc.read_text(c))))
    matching = [(g, loc) for g, loc in grams if g in corpus_set]
    ratio = round(len(matching) / len(grams), 4) if grams else 0.0
    res.metrics.update({"overlap_ratio": ratio, "total_ngrams": len(grams),
                        "matching_ngrams": len(matching), "corpus_files": len(present)})
    if ratio > float(limit):
        g, loc = matching[0]
        res.violate(loc, f"5-gram overlap with corpus: {' '.join(g)!r}", ratio, limit)
    return res


def main(argv: list[str] | None = None) -> int:
    return gc.run("resemblance_check.py", "Word 5-gram overlap against the resemblance corpus.", add_args, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
