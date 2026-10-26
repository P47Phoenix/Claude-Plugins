#!/usr/bin/env python3
"""rhyme_check.py - Stage 4 rhyme-scheme gate (stage-gates.md section 3).

usage: rhyme_check.py [--config P] [--json] [--genre G] [--language L]
                      [--slant-rhyme-allowed | --no-slant-rhyme] lyrics.md structure.md [brief.md]

Rhyme key of a line = its last word, lower-cased, punctuation stripped, from the
final vowel group to the end (``y`` counts as a vowel when final or after a
consonant; a trailing silent ``e`` after a consonant is part of the consonant
tail, so ``time``/``lime`` key as ``Ime``). ``data/rhyme-exceptions.txt``
(``word<TAB>key``) is consulted first for irregular spellings (through, you,
love, one ...). The final vowel group is then normalised to a vowel class:
ee/ea/ie/ei-after-c/final-e -> E; ay/ai/ei/ey/eigh -> A; oo/ue/ew/final-ou/
final-u -> U; igh/final-y-in-a-monosyllable/final-ie/final-i -> I; oa/ow/oe/
final-o -> O; a lone vowel before consonant+silent-e takes its long class
(name -> Ame); silent ``gh`` is dropped from the tail (bought -> out). Full
rhyme: identical keys. Slant rhyme: identical vowel class only, or an
identical non-empty final consonant cluster with a different vowel class (an
empty cluster is not a rhyme, so ``go``/``see`` do not slant-rhyme).

``rhyme_scheme`` letters are scoped per section; ``x`` is unconstrained. Every
pair of lines sharing a letter must full-rhyme, or slant-rhyme when
``slant_rhyme_allowed`` is true (counted in ``metrics.slant_pairs``). A section
whose lyric line count differs from its scheme length is an ERROR; an empty
scheme leaves the section unconstrained. The gate is
SKIPPED when the resolved language is not ``en``.
"""
from __future__ import annotations

import argparse
import re
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402

SCRIPT = "rhyme_check"
VOWELS = "aeiou"
_WORD_RE = re.compile(r"[a-z']+")


def last_word(line: str) -> str:
    words = _WORD_RE.findall(line.lower().replace("’", "'"))
    words = [w.strip("'") for w in words if w.strip("'")]
    return words[-1] if words else ""


def _vowel_mask(w: str) -> str:
    out = []
    for i, ch in enumerate(w):
        if ch in VOWELS:
            out.append("V")
        elif ch == "y" and (i == len(w) - 1 or (i > 0 and w[i - 1] not in VOWELS)):
            out.append("V")
        else:
            out.append("C")
    return "".join(out)


_exceptions: dict[str, str] | None = None
_LONG = {"a": "A", "e": "E", "i": "I", "o": "O", "u": "U"}


def _load_exceptions() -> dict[str, str]:
    global _exceptions
    if _exceptions is None:
        _exceptions = {}
        for line in gc.load_list_file(gc.DATA_DIR / "rhyme-exceptions.txt"):
            parts = [x.strip() for x in re.split(r"	+| {2,}", line) if x.strip()]
            if len(parts) >= 2:
                _exceptions[parts[0].lower()] = parts[1]
    return _exceptions


def _vowel_class(vg: str, tail: str, prev: str, silent_e: bool, only_group: bool) -> str:
    """Map a final vowel group (digraph) to one of A E I O U, else leave it as spelled."""
    final = tail == ""
    if vg == "igh":
        return "I"
    if vg == "eigh":
        return "A"
    vg = vg[:-2] if vg.endswith("gh") else vg  # ough/augh: silent gh, vowel letters kept
    if vg == "ei":
        return "E" if prev == "c" else "A"
    if vg in ("ee", "ea"):
        return "E"
    if vg == "ie":
        return "I" if tail in ("", "s", "d") else "E"
    if vg in ("ay", "ai", "ey"):
        return "A"
    if vg in ("oo", "ue", "ew") or (vg in ("ou", "u") and final):
        return "U"
    if vg in ("oa", "oe", "ow") or (vg == "o" and final):
        return "O"
    if vg == "y":
        return "I" if only_group else "E"
    if final and vg in ("e", "i"):
        return _LONG[vg]
    if silent_e and len(vg) == 1 and vg in _LONG:
        return _LONG[vg]  # magic e: name -> A, time -> I, home -> O
    return vg


def rhyme_key(word: str) -> str:
    """Normalised final vowel class plus the consonant tail; '' when the word has no vowel."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if w in _load_exceptions():
        return _load_exceptions()[w]
    mask = _vowel_mask(w)
    silent_e = len(w) > 2 and w.endswith("e") and mask[-2] == "C" and "V" in mask[:-1]
    if silent_e:
        mask = mask[:-1] + "C"  # trailing silent e (time, lime) belongs to the tail, not a vowel group
    groups = list(re.finditer("V+", mask))
    if not groups:
        return ""
    g = groups[-1]
    vg, tail = w[g.start():g.end()], w[g.end():]
    if tail.startswith("gh"):  # igh, eigh, ough, augh
        vg, tail = vg + "gh", tail[2:]
    elif tail == "w" and vg in ("e", "o"):  # new, snow
        vg, tail = vg + "w", ""
    prev = w[g.start() - 1] if g.start() else ""
    return _vowel_class(vg, tail, prev, silent_e, len(groups) == 1) + tail


def _split_key(key: str) -> tuple[str, str]:
    m = re.match(r"^([aeiouyAEIOU]+)(.*)$", key)
    return (m.group(1), m.group(2)) if m else (key, "")


def classify(word_a: str, word_b: str) -> str:
    """'full', 'slant', or 'none'."""
    ka, kb = rhyme_key(word_a), rhyme_key(word_b)
    if not ka or not kb:
        return "none"
    if ka == kb:
        return "full"
    va, ca = _split_key(ka)
    vb, cb = _split_key(kb)
    if va == vb:
        return "slant"
    if ca and ca == cb:
        return "slant"
    return "none"


def main_fn(args: argparse.Namespace, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    lang = gc.resolve_language(args.language, args.paths)
    if lang != "en":
        return res.skip(f"language {lang} not supported")
    lyrics_p = gc.file_named(args.paths, "lyrics.md")
    struct_p = gc.file_named(args.paths, "structure.md")
    if not lyrics_p or not struct_p:
        return res.error("lyrics.md and structure.md are both required")
    slant_ok = gc.resolve_threshold("slant_rhyme_allowed", config, gc.resolve_genre(args.genre, args.paths),
                                    args.slant_rhyme_allowed, kind=bool)
    res.thresholds["slant_rhyme_allowed"] = slant_ok
    _, body = gc.parse_frontmatter(gc.read_text(lyrics_p))
    sections = gc.parse_sections(body)
    if not sections or not any(lines for _, lines in sections):
        return res.error("lyrics.md is empty", lyrics_p)
    structure = gc.parse_structure(gc.read_text(struct_p))
    schemes = {s["label"]: s["rhyme_scheme"] for s in structure["sections"]}
    if not schemes:
        return res.error("structure.md has no sections", struct_p)
    pairs = slant = 0
    for label, lines in sections:
        if label not in schemes:
            return res.error(f"section [{label}] not found in structure.md", label)
        scheme = re.sub(r"\s+", "", schemes[label])
        if not scheme:
            continue  # no scheme declared: section is unconstrained
        if len(scheme) != len(lines):
            return res.error(f"line count {len(lines)} differs from rhyme_scheme length {len(scheme)}", label)
        groups: dict[str, list[int]] = {}
        for i, letter in enumerate(scheme):
            if letter.lower() != "x":
                groups.setdefault(letter, []).append(i)
        for letter, idx in groups.items():
            for a, b in combinations(idx, 2):
                pairs += 1
                kind = classify(last_word(lines[a]), last_word(lines[b]))
                if kind == "full":
                    continue
                if kind == "slant" and slant_ok:
                    slant += 1
                    continue
                res.violate(f"{label}:{b + 1}", f"line {a + 1} and line {b + 1} ({letter}) do not rhyme",
                            f"{last_word(lines[a])}/{last_word(lines[b])}", "full" if not slant_ok else "slant")
    res.metrics["pairs_checked"] = pairs
    res.metrics["slant_pairs"] = slant
    return res


def add_args(p: argparse.ArgumentParser) -> None:
    g = p.add_mutually_exclusive_group()
    g.add_argument("--slant-rhyme-allowed", dest="slant_rhyme_allowed", action="store_true", default=None,
                   help="tolerate slant rhymes")
    g.add_argument("--no-slant-rhyme", dest="slant_rhyme_allowed", action="store_false",
                   help="require full rhymes")


def main(argv: list[str] | None = None) -> int:
    return gc.run(SCRIPT, "Rhyme gate: lyric lines must honour structure.md rhyme_scheme.",
                  add_args, main_fn, argv)


if __name__ == "__main__":
    sys.exit(main())
