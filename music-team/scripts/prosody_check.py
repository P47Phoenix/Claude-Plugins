#!/usr/bin/env python3
"""prosody_check.py - Stage 2 (``--hook``) and Stage 4 prosody gate (stage-gates.md section 3).

Lyrics mode:   prosody_check.py [--config P] [--json] [--genre G] [--language L]
                                [--prosody-tolerance F] lyrics.md structure.md [brief.md]
Hook mode:     prosody_check.py --hook [--hook-max-syllables N] concept.md [brief.md]

Syllables: the exception table ``data/syllable-exceptions.txt`` is consulted first;
otherwise vowel groups ``[aeiouy]+`` are counted (``y`` is a vowel only between a
consonant and a non-vowel), a trailing silent ``e`` after a consonant does not
count, ``-le`` after a consonant counts one (also before ``-s``/``-d``), ``-ed``
after a non-t/d consonant is silent, ``-es`` counts only after s/x/z/c/g/ch/sh,
hiatus pairs (ia/io/iu/eo/ua/uo) split, minimum one.

Stress: monosyllabic function words (``data/function-words.txt``) are ``u``;
polysyllabic words use, in order: the exception table's pattern, a stress-fixing
suffix (-tion, -ic, -ity, -ette ...), a neutral inflection (-ed, -ing, -ly ...)
stripped back to a table/prefix base, an unstressed Latin prefix (un-, re-, de-,
ex-, com- ...) before an open syllable, else first-syllable stress.

Mismatch ratio (per section): for lyric line i against meter line i, a position
counts as mismatched when the spec marks it ``S`` and the lyric does not; a
difference in syllable count adds ``abs(spec - observed)``; a lyric line with no
meter line counts all of its syllables; a meter line with no lyric line counts
its ``S`` positions; a section with an empty meter_spec is unconstrained
(ratio 0). The denominator is the number of ``S`` positions in the
section's meter spec (minimum 1): the stage-gates phrase "mismatched stressed
positions / positions in the meter spec" is read with stressed positions as the
denominator so that 1.0 means every beat is missed.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

SCRIPT = "prosody_check"
VOWELS = "aeiou"
_WORD_RE = re.compile(r"[A-Za-z0-9']+(?:-[A-Za-z0-9']+)*")
# (suffix, k): stress falls k syllables before the last one; None = suffix's own syllable count
_SUFFIXES: list[tuple[str, int | None]] = sorted([
    ("tion", 1), ("tions", 1), ("sion", 1), ("sions", 1), ("cian", 1), ("cians", 1), ("cial", 1),
    ("tial", 1), ("cious", 1), ("tious", 1), ("geous", 1), ("gious", 1), ("xious", 1), ("ic", 1),
    ("ics", 1), ("ient", 1), ("ience", 1), ("ental", 1), ("ential", 1), ("lian", 1), ("nian", 1),
    ("ual", None), ("ity", None), ("ities", None), ("ety", None), ("ify", None), ("ical", None),
    ("ious", None), ("eous", None), ("ial", None), ("ian", None), ("iar", None), ("logy", 2), ("graphy", 2),
    ("ette", 0), ("ettes", 0), ("eer", 0), ("eers", 0), ("oon", 0), ("oons", 0), ("ese", 0),
    ("ique", 0), ("esque", 0), ("self", 0), ("selves", 0),
], key=lambda s: -len(s[0]))
_LONG_SUFFIXES = ("ate", "ise", "ize", "ies", "ogy")  # k=2 when the base has >= 3 syllables
_NEUTRAL = ("ings", "ing", "ed", "es", "s", "ers", "er", "est", "ly", "ness", "ful", "less", "ments", "ment", "en", "'s")
_PREFIXES = ("trans", "dis", "com", "con", "per", "pre", "pro", "sur", "sub", "sus", "for", "ob", "ab",
             "ad", "un", "re", "de", "be", "ex", "in", "im", "en", "em", "um", "a", "e")
_DOUBLING = ("ap", "ac", "af", "al", "ar", "as", "at", "an", "ad", "oc", "of", "op", "sup", "suc", "ef",
             "dif", "il", "ir", "im", "com", "con", "col", "cor")
_FINAL_STRESSED = {"on", "in", "at", "by", "for", "with", "through", "off"}  # stranded line-final prepositions
_tables: tuple[dict[str, tuple[int, str]], set[str]] | None = None


def _load_tables() -> tuple[dict[str, tuple[int, str]], set[str]]:
    global _tables
    if _tables is None:
        table: dict[str, tuple[int, str]] = {}
        for line in gc.load_list_file(gc.DATA_DIR / "syllable-exceptions.txt"):
            parts = [p.strip() for p in re.split(r"\t+| {2,}", line) if p.strip()]
            if len(parts) >= 2 and parts[1].isdigit():
                table[parts[0].lower()] = (int(parts[1]), parts[2] if len(parts) > 2 else "")
        _tables = (table, {w.lower() for w in gc.load_list_file(gc.DATA_DIR / "function-words.txt")})
    return _tables


def _clean(word: str) -> str:
    w = word.lower().replace("’", "'")
    return re.sub(r"[^a-z0-9'\-]", "", w).strip("'-")


def _vc(w: str) -> str:
    """Mark each letter V or C; ``y`` is a vowel only between a consonant and a non-vowel."""
    out = []
    for i, ch in enumerate(w):
        y_vowel = (ch == "y" and i > 0 and w[i - 1].isalpha() and w[i - 1] not in VOWELS
                   and (i == len(w) - 1 or w[i + 1] not in VOWELS))
        out.append("V" if ch in VOWELS or y_vowel else "C")
    return "".join(out)


def _heuristic(w: str) -> int:
    if not w:
        return 0
    vc = _vc(w)
    n = len(re.findall("V+", vc))
    for m in re.finditer(r"(?<=[^aeiou])(?:i[aou]|eo|u[ao])", w):  # ra-di-o, vi-o-lin, u-su-al
        prev, pair = w[m.start() - 1], m.group()
        if pair == "ia" and prev in "cstxl":
            continue  # -cial, -tian, -sia, -lian
        if pair in ("io", "eo") and prev in "cstxghnl":
            continue  # -tion, -sion, -gion, -shion, -nion, -lion, pigeon
        if pair[0] == "u" and prev in "gq":
            continue  # guard, quality
        n += 1
    cons_le = len(w) > 3 and w[-3:-1] == "le" and vc[-4] == "C" and w[-4] != "l"  # bottles, tangled
    if w.endswith("e") and len(w) > 2 and vc[-2] == "C":
        if not (w.endswith("le") and vc[-3] == "C"):
            n -= 1
    elif w.endswith("ed") and len(w) > 3 and vc[-3] == "C" and w[-3] not in "td" and not cons_le:
        n -= 1
    elif w.endswith("es") and len(w) > 3 and vc[-3] == "C" and not cons_le:
        if not (w[-3] in "sxzcg" or w.endswith(("ches", "shes"))):
            n -= 1
    elif w.endswith("ing") and len(w) > 4 and w[-4] in VOWELS:
        n += 1  # be-ing, go-ing
    for suf in ("ely", "eless", "eness", "eful", "ement", "esome"):
        if w.endswith(suf) and len(w) > len(suf) + 1 and vc[-len(suf) - 1] == "C":
            n -= 1
            break
    return max(1, n)


def count_syllables(word: str) -> int:
    """Syllables in one word: exception table first, then the heuristic."""
    table, _ = _load_tables()
    raw = word.replace("’", "'")
    w = _clean(word)
    if not w:
        return 0
    if w in table:
        return table[w][0]
    if "-" in w:
        return sum(count_syllables(p) for p in w.split("-"))
    if raw.isupper() and raw.isalpha() and len(raw) <= 4:
        return len(raw) + raw.count("W") * 2  # initialisms: TV, OK
    base = w.replace("'", "")
    if base in table:
        return table[base][0]
    extra = 0
    if w.endswith("n't") and len(w) > 3 and w[-4] not in VOWELS:
        extra, base = 1, w[:-3]
    elif w.endswith(("'ll", "'ve")) and len(w) > 3 and w[-4] not in VOWELS:
        extra, base = 1, w[:-3]
    elif raw.lower().rstrip("'!?,.;:\"").endswith("in'"):
        base = w[:-2] + "ing"
    elif w.endswith("'s") and w[:-2] in table:
        return table[w[:-2]][0]
    return max(1, _heuristic(base.replace("'", "")) + extra)


def _fit(pattern: str, n: int) -> str:
    return (pattern + "u" * n)[:n]


def _table_pattern(w: str) -> str | None:
    table, _ = _load_tables()
    n, pat = table.get(w, (0, ""))
    return pat if pat and len(pat) == n and set(pat) <= {"S", "u"} else None


def _suffix_rule(w: str, n: int) -> str | None:
    for suf, k in _SUFFIXES:
        if w.endswith(suf) and len(w) > len(suf) + 1:
            kk = k if k is not None else n - _heuristic(w[:-len(suf)])
            idx = n - 1 - kk
            return "u" * idx + "S" + "u" * (n - 1 - idx) if idx >= 0 else None
    base = w
    for suf in ("ed", "ing", "es", "s"):
        if w.endswith(suf) and len(w) > len(suf) + 3:
            base = w[:-len(suf)] + ("e" if suf in ("ed", "ing", "s") and not w[:-len(suf)].endswith("e") else "")
            break
    if base.endswith(_LONG_SUFFIXES) and _heuristic(base) >= 3:
        nb = _heuristic(base)
        return _fit("u" * (nb - 3) + "Suu", n)
    return None


def _prefix_rule(w: str, n: int, depth: int = 0) -> str | None:
    if n < 2 or depth > 1:
        return None
    for p in _DOUBLING:
        rest = w[len(p):]
        if w.startswith(p) and rest[:1] == p[-1] and len(rest) >= 4 and rest[1:2] in VOWELS + "lr":
            return _fit("u" + _word_pattern(rest, depth + 1), n)
    for p in _PREFIXES:
        rest = w[len(p):]
        if not w.startswith(p) or len(rest) < 4:
            continue
        open_syl = (rest[0] not in VOWELS + "y" and rest[0] != p[-1] and rest[1] in VOWELS + "lr"
                    and rest[1] != rest[0])
        if open_syl or (p == "un" and rest[0] in VOWELS):
            return _fit("u" + _word_pattern(rest, depth + 1), n)
    return None


def _word_pattern(w: str, depth: int = 0) -> str:
    table, fwords = _load_tables()
    n = count_syllables(w)
    if n == 0:
        return ""
    pat = _table_pattern(w) or _table_pattern(w.replace("'", ""))
    if pat:
        return pat
    if "-" in w:
        return "".join(_fit(_word_pattern(part, depth), count_syllables(part)) for part in w.split("-"))
    if n == 1:
        return "u" if w in fwords or w.replace("'", "") in fwords else "S"
    pat = _suffix_rule(w, n)
    if pat:
        return pat
    for suf in _NEUTRAL:  # strip a neutral inflection back to a known base
        if not w.endswith(suf) or len(w) <= len(suf) + 2:
            continue
        stem = w[:-len(suf)]
        for base in (stem, stem + "e", stem[:-1] if len(stem) > 2 and stem[-1] == stem[-2] else stem):
            bp = _table_pattern(base) or _prefix_rule(base, count_syllables(base), depth)
            if bp and 0 <= n - len(bp) <= 2:
                return bp + "u" * (n - len(bp))
    return _prefix_rule(w, n, depth) or "S" + "u" * (n - 1)


def words_in_line(line: str) -> list[str]:
    return [w for w in _WORD_RE.findall(line.replace("’", "'")) if _clean(w)]


def syllables_in_line(line: str) -> int:
    return sum(count_syllables(w) for w in words_in_line(line))


def stress_pattern(line: str) -> str:
    """``S``/``u`` string for a lyric line, one char per syllable.

    A stranded preposition ending the line ("left the light on") is stressed."""
    words = words_in_line(line)
    out = [_fit(_word_pattern(_clean(w)), count_syllables(w)) for w in words]
    if words and _clean(words[-1]) in _FINAL_STRESSED:
        out[-1] = "S"
    return "".join(out)


def _line_mismatch(spec: str, observed: str) -> int:
    k = min(len(spec), len(observed))
    return sum(1 for j in range(k) if spec[j] == "S" and observed[j] != "S") + abs(len(spec) - len(observed))


def check_lyrics(args: argparse.Namespace, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    lyrics_p = gc.file_named(args.paths, "lyrics.md")
    struct_p = gc.file_named(args.paths, "structure.md")
    if not lyrics_p or not struct_p:
        return res.error("lyrics.md and structure.md are both required")
    tol = gc.resolve_threshold("prosody_tolerance", config, gc.resolve_genre(args.genre, args.paths),
                              args.prosody_tolerance, kind=float)
    res.thresholds["prosody_tolerance"] = tol
    _, body = gc.parse_frontmatter(gc.read_text(lyrics_p))
    sections = gc.parse_sections(body)
    if not sections or not any(lines for _, lines in sections):
        return res.error("lyrics.md is empty", lyrics_p)
    meters = {s["label"]: s["meter"] for s in gc.parse_structure(gc.read_text(struct_p))["sections"]}
    if not meters:
        return res.error("structure.md has no sections", struct_p)
    syll_mismatch = 0
    for label, lines in sections:
        if label not in meters:
            return res.error(f"section [{label}] not found in structure.md", label)
        spec_lines = meters[label]
        if not spec_lines:
            res.metrics[f"{label.lower().replace(' ', '_')}_mismatch_ratio"] = 0.0
            continue  # no meter declared: section is unconstrained
        denom = max(1, sum(st.count("S") for _, st in spec_lines))
        bad_total, worst = 0, (-1, 1)
        for i in range(max(len(lines), len(spec_lines))):
            if i >= len(lines):
                bad = spec_lines[i][1].count("S")
            elif i >= len(spec_lines):
                bad = max(1, syllables_in_line(lines[i]))
            else:
                observed = stress_pattern(lines[i])
                bad = _line_mismatch(spec_lines[i][1], observed)
                syll_mismatch += len(observed) != spec_lines[i][0]
            bad_total += bad
            if bad > worst[0]:
                worst = (bad, i + 1)
        ratio = round(bad_total / denom, 4)
        key = f"{label.lower().replace(' ', '_')}_mismatch_ratio"
        # A repeated section (three choruses) is one section: keep the worst ratio
        # and report at most one violation per distinct label.
        if ratio >= res.metrics.get(key, -1.0):
            res.metrics[key] = ratio
            if ratio > tol:
                res.violations = [v for v in res.violations if not v["location"].startswith(f"{label}:")]
                res.violate(f"{label}:{worst[1]}", "stress mismatch", ratio, tol)
    res.metrics["syllable_mismatch_lines"] = syll_mismatch
    return res


def check_hook(args: argparse.Namespace, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    concept_p = gc.file_named(args.paths, "concept.md")
    if not concept_p:
        return res.error("concept.md is required in --hook mode")
    limit = gc.resolve_threshold("hook_max_syllables", config, gc.resolve_genre(args.genre, args.paths),
                                 args.hook_max_syllables, kind=int)
    res.thresholds["hook_max_syllables"] = limit
    fm, _ = gc.parse_frontmatter(gc.read_text(concept_p))
    hook = fm.get("hook_line")
    if not hook and fm.get("motif"):
        return res.skip("instrumental motif")
    if not isinstance(hook, str) or not hook.strip():
        return res.error("concept.md has no hook_line or motif", "hook_line")
    n = syllables_in_line(hook)
    res.metrics["hook_syllables"] = n
    if n > limit:
        res.violate("hook_line", "hook exceeds max syllables", n, limit)
    return res


def main_fn(args: argparse.Namespace, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    lang = gc.resolve_language(args.language, args.paths)
    if lang != "en":
        return res.skip(f"language {lang} not supported")
    return check_hook(args, config, res) if args.hook else check_lyrics(args, config, res)


def add_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--hook", action="store_true", help="check concept.md hook_line syllables")
    p.add_argument("--prosody-tolerance", type=float, metavar="F", help="max section mismatch ratio")
    p.add_argument("--hook-max-syllables", type=int, metavar="N", help="max hook_line syllables")


def main(argv: list[str] | None = None) -> int:
    return gc.run(SCRIPT, "Prosody gate: stress/syllable match against structure.md meter_spec.",
                  add_args, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
