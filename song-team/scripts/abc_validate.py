#!/usr/bin/env python3
"""abc_validate.py - Stage 5 melody gate for melody.abc (stage-gates.md section 3).

usage: abc_validate.py [--config P] [--json] [--genre G] [--max-melodic-leap N]
                       [--vocal-range LO,HI] melody.abc structure.md [lyrics.md] [brief.md]

Checks, in order: the file parses as the ABC subset in artifact-formats.md
(ERROR otherwise); headers X: T: M: L: Q: K: are present and there is at most
one V:; K: equals structure.md key/mode and M: equals time_sig; the ordered
``%%section`` labels equal the structure.md section list; no interval between
consecutive note heads exceeds ``max_melodic_leap`` semitones; every pitch lies
within ``vocal_range`` inclusive; and, when lyrics.md is given and brief.md
``song_type`` is not INSTRUMENTAL, lyric alignment: per bar the ``w:``
syllable tokens + ``_`` extensions + ``*`` skips must equal the non-rest note
heads (a tied-into note is not a new head), and the de-hyphenated ``w:`` text
of each section must equal the lyrics.md section text ignoring case and
punctuation. One violation per failing item, ``location`` ``<Label>:<bar>``.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402
import abc_common as ac  # noqa: E402

SCRIPT = "abc_validate"
_WORD_RE = re.compile(r"[a-z0-9]+")


def norm_text(text: str) -> str:
    """Lower-case, punctuation-insensitive word string for the section text comparison."""
    return " ".join(_WORD_RE.findall(text.lower().replace("'", "").replace("’", "")))


def resolve_vocal_range(config: dict[str, Any], genre: str | None, flag: str | None) -> list[int]:
    vr = gc.resolve_threshold("vocal_range", config, genre, flag)
    if isinstance(vr, str):
        vr = [x.strip() for x in vr.split(",")]
    if not isinstance(vr, (list, tuple)) or len(vr) != 2:
        raise ValueError(f"threshold vocal_range must be [lo, hi], got {vr!r}")
    lo = gc.resolve_threshold("vocal_range", {}, None, vr[0], kind=int)
    hi = gc.resolve_threshold("vocal_range", {}, None, vr[1], kind=int)
    if lo > hi:
        raise ValueError(f"threshold vocal_range low must be <= high, got {[lo, hi]}")
    return [lo, hi]


def song_type_of(paths: list[str]) -> str | None:
    brief = gc.file_named(paths, "brief.md")
    if not brief:
        return None
    fm, _ = gc.parse_frontmatter(gc.read_text(brief))
    st = fm.get("song_type")
    return str(st).upper() if st else None


def check_headers(abc: dict[str, Any], structure: dict[str, Any], res: gc.GateResult) -> None:
    headers, counts = abc["headers"], abc["header_counts"]
    for field in ac.REQUIRED_HEADERS:
        if field not in headers:
            res.violate(f"melody.abc:{field}", f"required header {field}: missing", None, f"{field}:")
    if counts.get("V", 0) > 1:
        res.violate("melody.abc:V", "more than one V: line", counts["V"], 1)
    want = structure["header"]
    if "K" in headers:
        want_key = str(want.get("key", "")).strip()
        want_key = want_key[:1].upper() + want_key[1:]
        want_mode = str(want.get("mode") or "major").strip().lower()
        if want_key and (abc["key"], abc["mode"]) != (want_key, want_mode):
            res.violate("melody.abc:K", "K: differs from structure.md key/mode",
                        f"{abc['key']} {abc['mode']}", f"{want_key} {want_mode}")
    if "M" in headers and want.get("time_sig") is not None:
        got, exp = ac.parse_time_sig(headers["M"]), ac.parse_time_sig(str(want["time_sig"]))
        if got != exp or got is None:
            res.violate("melody.abc:M", "M: differs from structure.md time_sig", headers["M"], str(want["time_sig"]))


def check_sections(abc: dict[str, Any], structure: dict[str, Any], res: gc.GateResult) -> None:
    got = [s["label"] for s in abc["sections"]]
    want = [s["label"] for s in structure["sections"]]
    if got != want:
        res.violate("melody.abc:sections", "section list differs from structure.md", got, want)


def check_pitches(abc: dict[str, Any], res: gc.GateResult, max_leap: int, vr: list[int]) -> None:
    prev: int | None = None
    max_seen = 0
    pitches: list[int] = []
    for sec in abc["sections"]:
        label = sec["label"] or "(none)"
        for bi, bar in enumerate(sec["bars"], 1):
            for note in bar["notes"]:
                if note["is_rest"]:
                    continue
                p = note["midi"]
                pitches.append(p)
                if prev is not None and not note["tied_from_prev"]:
                    leap = abs(p - prev)
                    max_seen = max(max_seen, leap)
                    if leap > max_leap:
                        res.violate(f"{label}:{bi}", "melodic leap exceeds max_melodic_leap", leap, max_leap)
                if p < vr[0] or p > vr[1]:
                    res.violate(f"{label}:{bi}", "pitch outside vocal_range", p, vr)
                prev = p
    res.metrics["notes"] = len(pitches)
    res.metrics["min_pitch"] = min(pitches) if pitches else None
    res.metrics["max_pitch"] = max(pitches) if pitches else None
    res.metrics["max_leap"] = max_seen


def check_alignment(abc: dict[str, Any], lyrics: list[tuple[str, list[str]]], res: gc.GateResult) -> None:
    aligned = 0
    for si, sec in enumerate(abc["sections"]):
        label = sec["label"] or "(none)"
        words: list[str] = []
        for bi, bar in enumerate(sec["bars"], 1):
            heads = ac.note_heads(bar)
            units = len(bar["w_tokens"])
            if units != heads:
                res.violate(f"{label}:{bi}", "w: tokens + extensions + skips differ from note heads", units, heads)
            else:
                aligned += 1
            # rebuild words: syllables glued together, a new word per whitespace-separated chunk is
            # not recoverable, so compare on the punctuation-insensitive letter string instead
            words.extend(t["text"] for t in bar["w_tokens"] if t["kind"] == "syl")
        lyr_sec = lyrics[si] if si < len(lyrics) and lyrics[si][0] == sec["label"] else None
        if lyr_sec is None:
            res.violate(f"{label}:1", "no matching lyrics.md section", sec["label"],
                        [l for l, _ in lyrics])
            continue
        got = norm_text("".join(words)).replace(" ", "")
        want = norm_text(" ".join(lyr_sec[1])).replace(" ", "")
        if got != want:
            res.violate(f"{label}:1", "w: text differs from lyrics.md section text",
                        " ".join(words), " ".join(lyr_sec[1]))
    res.metrics["aligned_bars"] = aligned


def add_args(p: Any) -> None:
    p.add_argument("--max-melodic-leap", metavar="N", type=int, help="override quality.max_melodic_leap")
    p.add_argument("--vocal-range", metavar="LO,HI", help="override quality.vocal_range (MIDI numbers)")


def main_fn(args: Any, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    mpath = gc.file_named(args.paths, "melody.abc")
    spath = gc.file_named(args.paths, "structure.md")
    if not mpath:
        return res.error("melody.abc not given")
    if not spath:
        return res.error("structure.md not given")
    genre = gc.resolve_genre(args.genre, args.paths)
    max_leap = gc.resolve_threshold("max_melodic_leap", config, genre, args.max_melodic_leap, kind=int)
    vr = resolve_vocal_range(config, genre, args.vocal_range)
    res.thresholds["max_melodic_leap"] = max_leap
    res.thresholds["vocal_range"] = vr

    try:
        abc = ac.parse_abc(gc.read_text(mpath))
    except ac.AbcParseError as exc:
        return res.error(f"ABC parse error: {exc}", f"melody.abc:{exc.line}" if exc.line else "melody.abc")
    structure = gc.parse_structure(gc.read_text(spath))
    res.metrics["bars"] = sum(len(s["bars"]) for s in abc["sections"])

    check_headers(abc, structure, res)
    check_sections(abc, structure, res)
    check_pitches(abc, res, max_leap, vr)

    lpath = gc.file_named(args.paths, "lyrics.md")
    song_type = song_type_of(args.paths)
    if lpath and song_type != "INSTRUMENTAL":
        res.metrics["alignment_skipped"] = 0
        check_alignment(abc, gc.parse_sections(gc.read_text(lpath)), res)
    else:
        res.metrics["alignment_skipped"] = 1
        res.metrics["aligned_bars"] = 0
    return res


def main(argv: list[str] | None = None) -> int:
    return gc.run(f"{SCRIPT}.py", "ABC melody gate: headers, key, sections, leaps, range, lyric alignment.",
                  add_args, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
