#!/usr/bin/env python3
"""abc_validate.py - Stage 5 gate for melody.abc (stage-gates.md section 3). Stdlib only; ``python -I`` safe.

Parses an ABC 2.1 subset: headers X T M L Q K (V optional, at most one), notes with accidentals and
octave marks, rests, lengths, broken rhythm, tuplets, ties, chords in [], bar lines and repeats,
``%%section <Label>`` markers and ``w:`` lyric lines.

Checks
  * headers X T M L Q K present; M, K and Q equal structure.md time_sig / key+mode / bpm
  * ``%%section`` labels equal the structure.md labels in order
  * every bar sums to the meter (a short pickup bar and a short final bar are tolerated unless --strict-bars)
  * leaps <= max_melodic_leap and every pitch inside the vocal range (--vocal-range A3-E5)
  * lyric alignment (lyrics.md given, song_type != INSTRUMENTAL, or --lyrics-aligned): per bar,
    syllables + ``_`` extensions + ``*`` skips == pitched note heads (rests and tied continuations
    take no syllable); w: text per section equals the lyrics.md section ignoring case and punctuation

Exit codes: 0 PASS | 1 FAIL | 2 SKIPPED | 3 ERROR (unparseable ABC).
"""
from __future__ import annotations

import argparse
import re
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_common as gc  # noqa: E402
import chord_tools as ct  # noqa: E402

NOTE_RE = re.compile(r"(\^\^|\^|__|_|=)?([A-Ga-g])([',]*)")
BASE_MIDI = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71}
PC_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
DECORATIONS = set("~.HLMOPSTuv")
REQUIRED = ["X", "T", "M", "L", "Q", "K"]


def midi_name(m: int) -> str:
    return f"{PC_NAMES[m % 12]}{m // 12 - 1}"


def parse_pitch_name(text: str) -> int:
    t = text.strip()
    if re.fullmatch(r"\d+", t):
        return int(t)
    m = re.fullmatch(r"([A-Ga-g])([#b]?)(-?\d+)", t)
    if not m:
        raise ValueError(f"cannot parse pitch {text!r} (use A3 or a MIDI number)")
    pc = ct.BASE_PC[m.group(1).upper()] + {"#": 1, "b": -1, "": 0}[m.group(2)]
    return pc + 12 * (int(m.group(3)) + 1)


def parse_range(value: Any) -> tuple[int, int]:
    if isinstance(value, (list, tuple)) and len(value) == 2:
        lo, hi = parse_pitch_name(str(value[0])), parse_pitch_name(str(value[1]))
    else:
        m = re.fullmatch(r"\s*(\S+?)\s*-\s*(\S+)\s*", str(value))
        if not m:
            raise ValueError(f"cannot parse vocal range {value!r} (use A3-E5 or 55-79)")
        lo, hi = parse_pitch_name(m.group(1)), parse_pitch_name(m.group(2))
    if lo > hi:
        raise ValueError(f"vocal range {value!r} is inverted")
    return lo, hi


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
class Ev:
    __slots__ = ("pitches", "dur", "tied_from_prev", "tied_next", "lyric")

    def __init__(self, pitches: list[int], dur: Fraction):
        self.pitches, self.dur = pitches, dur  # empty pitches = rest
        self.tied_from_prev = False
        self.tied_next = False
        self.lyric = bool(pitches)


class Segment:
    def __init__(self, bar_no: int):
        self.bar_no, self.events = bar_no, []  # type: int, list[Ev]

    def slots(self) -> int:
        return sum(1 for e in self.events if e.lyric)


class MusicLine:
    def __init__(self, section: str | None, sec_idx: int, line_no: int):
        self.section, self.sec_idx, self.line_no = section, sec_idx, line_no
        self.segments: list[Segment] = []
        self.lyrics: list[tuple[int, list[int]]] = []  # (line_no, slot counts per segment)
        self.lyric_text: list[str] = []


class Tune:
    def __init__(self) -> None:
        self.headers: dict[str, str] = {}
        self.v_lines = 0
        self.lines: list[MusicLine] = []
        self.sections: list[str] = []
        self.bars: list[tuple[int, str | None, int, Fraction]] = []  # (section index, label, bar no in section, duration)
        self.meter = Fraction(4, 4)
        self.unit = Fraction(1, 8)
        self.key_acc: dict[str, int] = {}


def parse_meter(value: str) -> Fraction:
    v = value.strip()
    if v == "C":
        return Fraction(4, 4)
    if v == "C|":
        return Fraction(2, 2)
    m = re.fullmatch(r"(\d+)\s*/\s*(\d+)", v)
    if not m or int(m.group(2)) == 0:
        raise ValueError(f"cannot parse M: field {value!r}")
    return Fraction(int(m.group(1)), int(m.group(2)))


def parse_unit(value: str) -> Fraction:
    m = re.fullmatch(r"\s*(\d+)\s*/\s*(\d+)\s*", value)
    if not m or int(m.group(2)) == 0 or int(m.group(1)) == 0:
        raise ValueError(f"cannot parse L: field {value!r}")
    return Fraction(int(m.group(1)), int(m.group(2)))


def parse_tempo(value: str) -> int:
    m = re.search(r"(\d+)\s*/\s*(\d+)\s*=\s*(\d+)", value)
    if m:
        return round(int(m.group(3)) * Fraction(int(m.group(1)), int(m.group(2))) * 4)
    m = re.fullmatch(r'\s*(?:"[^"]*"\s*)?(\d+)\s*', value)
    if m:
        return int(m.group(1))
    raise ValueError(f"cannot parse Q: field {value!r}")


def parse_abc_key(value: str) -> tuple[ct.Note, str]:
    tokens = value.replace("K:", "").split()
    if not tokens:
        raise ValueError("empty K: field")
    text = tokens[0]
    if len(tokens) > 1 and re.sub(r"[-_\s]", "", tokens[1].lower()) in ct.MODE_ALIASES:
        text += " " + tokens[1]
    try:
        return ct.parse_key(text)
    except ValueError:
        raise ValueError(f"cannot parse K: field {value!r}") from None


def key_accidentals(tonic: ct.Note, mode: str) -> dict[str, int]:
    out = {}
    for idx, pc in ct.scale_notes(tonic, mode):
        letter = ct.LETTERS[idx]
        d = (pc - ct.BASE_PC[letter]) % 12
        out[letter] = d - 12 if d > 6 else d
    return out


class Scanner:
    """Turns music-line text into events, tracking bar accidentals, ties, slurs and tuplets."""

    def __init__(self, tune: Tune) -> None:
        self.t = tune
        self.slur = 0
        self.tup_left = 0
        self.tup_factor = Fraction(1)
        self.pending_second: Fraction | None = None
        self.carry_tie = False
        self.bar_acc: dict[tuple[str, int], int] = {}

    def dur(self, s: str, i: int) -> tuple[Fraction, int]:
        m = re.compile(r"(\d+)?(/+)?(\d+)?").match(s, i)
        num = int(m.group(1)) if m.group(1) else 1
        if m.group(2):
            den = int(m.group(3)) if (m.group(3) and len(m.group(2)) == 1) else 2 ** len(m.group(2))
            val = Fraction(num, den)
            end = m.end() if (m.group(3) and len(m.group(2)) == 1) else m.end(2)
        else:
            val, end = Fraction(num), m.end(1) if m.group(1) else i
        return val, end

    def pitch(self, acc: str | None, letter: str, marks: str) -> int:
        up = letter.islower()
        name = letter.upper()
        octave = marks.count("'") - marks.count(",")
        key = (name, octave + (1 if up else 0))
        if acc:
            a = {"^^": 2, "^": 1, "=": 0, "_": -1, "__": -2}[acc]
            self.bar_acc[key] = a
        else:
            a = self.bar_acc.get(key, self.t.key_acc.get(name, 0))
        return BASE_MIDI[name] + 12 * (1 if up else 0) + 12 * octave + a

    def scale_dur(self, d: Fraction) -> Fraction:
        d = d * self.t.unit
        if self.tup_left > 0:
            d *= self.tup_factor
            self.tup_left -= 1
        if self.pending_second is not None:
            d *= self.pending_second
            self.pending_second = None
        return d

    def scan(self, s: str, line_no: int, on_event, on_bar) -> None:
        i, n = 0, len(s)
        while i < n:
            c = s[i]
            if c in " \t":
                i += 1
            elif c == '"':
                j = s.find('"', i + 1)
                if j < 0:
                    raise ValueError(f"line {line_no}: unterminated chord annotation")
                i = j + 1
            elif c in "!+":
                j = s.find(c, i + 1)
                if j < 0:
                    raise ValueError(f"line {line_no}: unterminated decoration {c}...{c}")
                i = j + 1
            elif c == "{":
                j = s.find("}", i + 1)
                if j < 0:
                    raise ValueError(f"line {line_no}: unterminated grace group")
                i = j + 1
            elif c == "(":
                m = re.compile(r"\((\d+)(?::(\d*))?(?::(\d*))?").match(s, i)
                if m:
                    p = int(m.group(1))
                    q = int(m.group(2)) if m.group(2) else {2: 3, 3: 2, 4: 3, 6: 2, 8: 3}.get(p, 2)
                    r = int(m.group(3)) if m.group(3) else p
                    self.tup_left, self.tup_factor = r, Fraction(q, p)
                    i = m.end()
                else:
                    self.slur += 1
                    i += 1
            elif c == ")":
                self.slur -= 1
                if self.slur < 0:
                    raise ValueError(f"line {line_no}: ')' without matching '('")
                i += 1
            elif c == "[":
                nxt = s[i + 1] if i + 1 < n else ""
                if nxt == "|":
                    j = i + 1
                    while j < n and s[j] in "|:]":
                        j += 1
                    on_bar(s[i:j])
                    self.bar_acc = {}
                    i = j
                elif nxt.isdigit():
                    j = i + 1
                    while j < n and (s[j].isdigit() or s[j] in ",-"):
                        j += 1
                    i = j
                elif nxt.isalpha() and i + 2 < n and s[i + 2] == ":":
                    j = s.find("]", i)
                    if j < 0:
                        raise ValueError(f"line {line_no}: unterminated inline field")
                    i = j + 1
                else:
                    j = s.find("]", i)
                    if j < 0:
                        raise ValueError(f"line {line_no}: unterminated chord '['")
                    inner = s[i + 1:j]
                    pitches, first, k = [], None, 0
                    while k < len(inner):
                        if inner[k] in " \t-":
                            k += 1
                            continue
                        m = NOTE_RE.match(inner, k)
                        if not m:
                            raise ValueError(f"line {line_no}: bad chord content {inner!r}")
                        pitches.append(self.pitch(m.group(1), m.group(2), m.group(3)))
                        d, k = self.dur(inner, m.end())
                        first = d if first is None else first
                    if not pitches:
                        raise ValueError(f"line {line_no}: empty chord []")
                    outer, i = self.dur(s, j + 1)
                    self.emit(on_event, pitches, (first or Fraction(1)) * outer)
            elif c in "|:":
                j = i
                while j < n and s[j] in "|:]":
                    j += 1
                while j < n and s[j].isdigit():
                    j += 1
                on_bar(s[i:j])
                self.bar_acc = {}
                i = j
            elif c == "]":
                raise ValueError(f"line {line_no}: stray ']'")
            elif c == "-":
                on_event(None)  # tie marker handled by caller
                i += 1
            elif c in "zZxX":
                d, i = self.dur(s, i + 1)
                self.emit(on_event, [], d * self.t.meter / self.t.unit if c in "ZX" else d)
            elif c == "y":
                _, i = self.dur(s, i + 1)
            elif c in DECORATIONS or c in "&*`":
                i += 1
            elif c == "\\":
                i = n
            elif c in "<>":
                j = i
                while j < n and s[j] == c:
                    j += 1
                k = min(j - i, 3)
                big, small = 2 - Fraction(1, 2 ** k), Fraction(1, 2 ** k)
                first, second = (big, small) if c == ">" else (small, big)
                on_event(("broken", first))
                self.pending_second = second
                i = j
            elif c in "^_=" or c.upper() in "ABCDEFG":
                m = NOTE_RE.match(s, i)
                if not m:
                    raise ValueError(f"line {line_no}: bad note at {s[i:i + 6]!r}")
                p = self.pitch(m.group(1), m.group(2), m.group(3))
                d, i = self.dur(s, m.end())
                self.emit(on_event, [p], d)
            else:
                raise ValueError(f"line {line_no}: unexpected character {c!r}")

    def emit(self, on_event, pitches: list[int], d: Fraction) -> None:
        ev = Ev(pitches, self.scale_dur(d))
        on_event(ev)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def tokenize_lyric(text: str) -> list[int]:
    """Slots per bar segment for one ``w:`` line (``|`` splits bars)."""
    segs, cur = [], 0
    for tok in re.findall(r"\||[^\s|]+", text):
        if tok == "|":
            segs.append(cur)
            cur = 0
        elif tok == "*":
            cur += 1
        elif tok in ("_", "-"):
            cur += 1 if tok == "_" else 0
        else:
            word = tok.replace("\\-", "\u0001")
            word = word.replace("~", "\u0002")
            cur += len([p for p in word.split("-") if p.strip("_*")]) + word.count("_") + word.count("*")
    segs.append(cur)
    if segs and segs[-1] == 0 and len(segs) > 1:
        segs.pop()
    return segs


def lyric_words(text: str) -> str:
    out = []
    for tok in re.findall(r"\||[^\s|]+", text):
        if tok in ("|", "*", "_", "-"):
            continue
        out.append(tok.replace("~", " ").replace("-", "").replace("_", "").replace("*", ""))
    return " ".join(out)


class Parser:
    """Line-by-line ABC reader: headers, %%section markers, music lines and w: lines."""

    def __init__(self) -> None:
        self.t = Tune()
        self.scanner = Scanner(self.t)
        self.in_body = False
        self.section: str | None = None
        self.sec_idx = -1
        self.section_bars = 0
        self.cur_bar: list[Ev] = []
        self.cur_dur = Fraction(0)
        self.line: MusicLine | None = None
        self.seg = Segment(1)
        self.last_ev: Ev | None = None

    # -- bars and segments ------------------------------------------------
    def flush_bar(self) -> None:
        if self.cur_bar:
            self.section_bars += 1
            self.t.bars.append((self.sec_idx, self.section, self.section_bars, self.cur_dur))
        self.cur_bar, self.cur_dur = [], Fraction(0)

    def close_segment(self) -> None:
        if self.line is not None and self.seg.events:
            self.line.segments.append(self.seg)
        self.seg = Segment(self.section_bars + 1)

    def on_bar(self, _: str) -> None:
        self.close_segment()
        self.flush_bar()
        self.seg = Segment(self.section_bars + 1)

    def on_event(self, ev: Any) -> None:
        sc = self.scanner
        if ev is None:  # tie marker
            if self.last_ev is not None and self.last_ev.pitches:
                self.last_ev.tied_next = True
                sc.carry_tie = True
            return
        if isinstance(ev, tuple):  # broken rhythm rescales the previous event
            if self.last_ev is not None:
                delta = self.last_ev.dur * ev[1] - self.last_ev.dur
                self.last_ev.dur += delta
                self.cur_dur += delta
            return
        if sc.carry_tie and ev.pitches:
            ev.tied_from_prev, ev.lyric = True, False
            sc.carry_tie = False
        self.cur_bar.append(ev)
        self.cur_dur += ev.dur
        self.seg.events.append(ev)
        self.last_ev = ev

    # -- fields -------------------------------------------------------------
    def field(self, no: int, name: str, value: str) -> None:
        t = self.t
        if name == "w":
            if self.line is None:
                raise ValueError(f"line {no}: w: line with no music line before it")
            self.line.lyrics.append((no, tokenize_lyric(value)))
            self.line.lyric_text.append(lyric_words(value))
            return
        if name == "V":
            t.v_lines += 1
            return
        if name == "X" and not re.fullmatch(r"\d+", value):
            raise ValueError(f"line {no}: X: reference number must be an integer, got {value!r}")
        if name == "M":
            t.meter = parse_meter(value)
        elif name == "L":
            t.unit = parse_unit(value)
        elif name == "Q":
            parse_tempo(value)
        elif name == "K":
            tonic, mode = parse_abc_key(value)
            t.key_acc = key_accidentals(tonic, mode)
            self.in_body = True
        if not (self.in_body and name != "K") and name not in t.headers:
            t.headers[name] = value

    def feed(self, no: int, raw: str) -> None:
        s = raw.strip()
        if not s:
            return
        if s.startswith("%%section"):
            label = s[len("%%section"):].strip()
            if not label:
                raise ValueError(f"line {no}: %%section with no label")
            self.flush_bar()
            self.section, self.section_bars = label, 0
            self.t.sections.append(label)
            self.sec_idx = len(self.t.sections) - 1
            return
        s = s.split("%", 1)[0].strip()
        if not s:
            return
        if re.match(r"^[A-Za-z]{2,}\s*:", s):
            raise ValueError(f"line {no}: unknown field {s.split(':', 1)[0]!r}")
        m = re.match(r"^([A-Za-z]):\s*(.*)$", s)
        if m:
            self.field(no, m.group(1), m.group(2).strip())
            return
        if not self.in_body:
            raise ValueError(f"line {no}: music before the K: header")
        self.line = MusicLine(self.section, self.sec_idx, no)
        self.t.lines.append(self.line)
        self.seg = Segment(self.section_bars + 1)
        self.scanner.scan(s, no, self.on_event, self.on_bar)
        self.close_segment()

    def finish(self) -> Tune:
        if self.scanner.slur != 0:
            raise ValueError("unclosed slur '(' at end of tune")
        self.flush_bar()
        return self.t


def parse_abc(text: str) -> Tune:
    p = Parser()
    for no, raw in enumerate(text.splitlines(), 1):
        p.feed(no, raw)
    return p.finish()


# ---------------------------------------------------------------------------
# Gate
# ---------------------------------------------------------------------------
def _letters(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _norm_key(tonic: ct.Note, mode: str) -> tuple[int, str]:
    return tonic[1], mode


def gate_main(args: argparse.Namespace, config: dict[str, Any], res: gc.GateResult) -> gc.GateResult:
    paths = args.paths
    abc_path = gc.file_named(paths, "melody.abc") or next((p for p in paths if p.lower().endswith(".abc")), None)
    if not abc_path:
        return res.error("no melody.abc path given")
    structure_path = args.structure or gc.file_named(paths, "structure.md")
    lyrics_path = gc.file_named(paths, "lyrics.md")
    genre = gc.resolve_genre(args.genre, paths)
    max_leap = gc.resolve_threshold("max_melodic_leap", config, genre, args.max_leap, kind=int)
    vr_flag = args.vocal_range
    vr = parse_range(vr_flag if vr_flag else gc.resolve_threshold("vocal_range", config, genre))
    res.thresholds.update({"max_melodic_leap": max_leap, "vocal_range": [midi_name(vr[0]), midi_name(vr[1])]})

    tune = parse_abc(gc.read_text(abc_path))
    h = tune.headers
    for f in REQUIRED:
        if f not in h:
            res.violate("melody.abc:headers", f"missing required header {f}:", None, "X T M L Q K")
    if h.get("T", "x") == "":
        res.violate("melody.abc:headers", "T: title is empty", "", "non-empty")
    if tune.v_lines > 1:
        res.violate("melody.abc:headers", "more than one V: line (single voice only)", tune.v_lines, 1)
    if "K" in h and "M" in h:
        tonic, mode = parse_abc_key(h["K"])
        res.metrics["key"] = f"{ct.spell(tonic)} {mode}"
    res.metrics["meter"] = h.get("M")

    sections = None
    if structure_path:
        st = gc.parse_structure(gc.read_text(structure_path))
        hd = st["header"]
        if "M" in h and hd.get("time_sig") and parse_meter(h["M"]) != parse_meter(str(hd["time_sig"])):
            res.violate("melody.abc:M", "meter differs from structure.md time_sig", h["M"], hd["time_sig"])
        if "K" in h and hd.get("key"):
            want = ct.parse_key(str(hd["key"]), str(hd.get("mode") or "major"))
            if _norm_key(*parse_abc_key(h["K"])) != _norm_key(*want):
                res.violate("melody.abc:K", "key differs from structure.md key/mode", h["K"],
                            f"{hd['key']} {hd.get('mode', 'major')}")
        if "Q" in h and hd.get("bpm") is not None:
            got = parse_tempo(h["Q"])
            if got != int(hd["bpm"]):
                res.violate("melody.abc:Q", "tempo differs from structure.md bpm", got, int(hd["bpm"]))
        sections = st["sections"]
        want_labels = [s["label"] for s in sections]
        if tune.sections != want_labels:
            res.violate("melody.abc:sections", "%%section labels differ from structure.md",
                        " / ".join(tune.sections), " / ".join(want_labels))
        else:
            _warn_bar_counts(tune, sections, res)

    # bar lengths
    nb = len(tune.bars)
    for i, (_, sec, bar_no, dur) in enumerate(tune.bars):
        loc = f"{sec or 'melody.abc'}:{bar_no}"
        if dur > tune.meter:
            res.violate(loc, "bar longer than the meter", str(dur), str(tune.meter))
        elif dur < tune.meter:
            tolerated = not args.strict_bars and (i == 0 or i == nb - 1)
            if not tolerated:
                res.violate(loc, "bar shorter than the meter", str(dur), str(tune.meter))
            else:
                res.warn(loc, "short pickup/final bar tolerated", str(dur), str(tune.meter))

    # pitches: range and leaps
    prev: tuple[int, str] | None = None
    lo = hi = None
    max_seen = 0
    notes = 0
    bar_of_line: dict[int, str] = {}
    for ml in tune.lines:
        for seg in ml.segments:
            loc = f"{ml.section or 'melody.abc'}:{seg.bar_no}"
            bad = None
            for ev in seg.events:
                if not ev.pitches:
                    continue
                notes += 1
                top = max(ev.pitches)
                for p in ev.pitches:
                    lo = p if lo is None else min(lo, p)
                    hi = p if hi is None else max(hi, p)
                    if (p < vr[0] or p > vr[1]) and bad is None:
                        bad = p
                if prev is not None:
                    leap = abs(top - prev[0])
                    max_seen = max(max_seen, leap)
                    if leap > max_leap:
                        res.violate(loc, "melodic leap exceeds max_melodic_leap", leap, max_leap)
                prev = (top, loc)
            if bad is not None:
                res.violate(loc, "note outside the vocal range", midi_name(bad),
                            f"{midi_name(vr[0])}-{midi_name(vr[1])}")
    res.metrics.update({"notes": notes, "bars": nb, "sections": len(tune.sections), "max_leap": max_seen})
    if lo is not None:
        res.metrics["pitch_range"] = f"{midi_name(lo)}-{midi_name(hi)}"

    # lyric alignment
    instrumental = False
    brief = gc.file_named(paths, "brief.md")
    if brief:
        fm, _ = gc.parse_frontmatter(gc.read_text(brief))
        instrumental = str(fm.get("song_type", "")).upper() == "INSTRUMENTAL"
    aligned = args.lyrics_aligned or (lyrics_path is not None and not instrumental)
    if aligned:
        checked = 0
        for ml in tune.lines:
            if not any(s.slots() for s in ml.segments):
                continue
            loc0 = f"{ml.section or 'melody.abc'}:{ml.segments[0].bar_no}"
            if not ml.lyrics:
                res.violate(loc0, "music line has no w: lyric line", 0, "w: line")
                continue
            for _, counts in ml.lyrics:
                checked += 1
                for k in range(max(len(counts), len(ml.segments))):
                    got = counts[k] if k < len(counts) else 0
                    seg = ml.segments[k] if k < len(ml.segments) else None
                    want = seg.slots() if seg else 0
                    if got != want:
                        bar = seg.bar_no if seg else ml.segments[-1].bar_no + (k - len(ml.segments) + 1)
                        res.violate(f"{ml.section or 'melody.abc'}:{bar}",
                                    "w: syllables + extensions + skips differ from note heads in this bar", got, want)
        res.metrics["lyric_lines_checked"] = checked
        if lyrics_path:
            lyr = gc.parse_sections(gc.read_text(lyrics_path))
            by_label: dict[str, list[str]] = {}
            for lbl, lines in lyr:
                by_label.setdefault(lbl, []).append(" ".join(lines))
            grouped: dict[int, list[str]] = {}
            for ml in tune.lines:
                if ml.sec_idx >= 0:
                    grouped.setdefault(ml.sec_idx, []).extend(ml.lyric_text)
            seen: dict[str, int] = {}
            for idx in sorted(grouped):
                label, texts = tune.sections[idx], grouped[idx]
                if not any(texts):
                    continue
                i = seen.get(label, 0)
                seen[label] = i + 1
                variants = by_label.get(label)
                if not variants:
                    res.violate(f"{label}:text", "melody section has no matching lyrics.md section", label, "lyrics.md tag")
                    continue
                want_text = variants[min(i, len(variants) - 1)]
                if _letters(" ".join(texts)) != _letters(want_text):
                    res.violate(f"{label}:text", "w: text differs from lyrics.md section text",
                                " ".join(texts)[:60], want_text[:60])
    else:
        res.metrics["lyric_alignment"] = "skipped"
    return res


def _warn_bar_counts(tune: Tune, sections: list[dict[str, Any]], res: gc.GateResult) -> None:
    per: dict[int, int] = {}
    for idx, _, bar_no, _ in tune.bars:
        per[idx] = max(per.get(idx, 0), bar_no)
    for idx, sec in enumerate(sections):
        got = per.get(idx, 0)
        if sec["bars"] and got != sec["bars"]:
            res.warn(sec["label"], "bar count differs from structure.md bars", got, sec["bars"])


def gate_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--structure", metavar="PATH", help="structure.md (else found among the paths)")
    p.add_argument("--vocal-range", metavar="LO-HI", help="e.g. A3-E5 or 55-79 (else quality.vocal_range)")
    p.add_argument("--max-leap", type=int, metavar="SEMITONES", help="override quality.max_melodic_leap")
    p.add_argument("--lyrics-aligned", action="store_true", help="force lyric alignment even without lyrics.md")
    p.add_argument("--strict-bars", action="store_true", help="do not tolerate short pickup or final bars")
    p.add_argument("--selftest", action="store_true", help="run the built-in self-test and exit")


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
_GOOD = """X:1
T:Test Tune
M:4/4
L:1/8
Q:1/4=100
K:D
%%section Verse 1
D2 E2 F2 GA | B2 A2 F4 |
w: I count the num-bers | on the street |
%%section Chorus
d2 c2 B2 A2 | B2 A2 F2 ED |
w: No-bo-dy knows | my name here yet_ |
"""


def _run_text(text: str, extra: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    import io
    import json
    import tempfile
    from contextlib import redirect_stdout
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "melody.abc"
        f.write_text(text, encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = gc.run("abc_validate.py", "selftest", gate_args, gate_main,
                          ["--json", str(f), "--lyrics-aligned", *(extra or [])])
        return code, json.loads(buf.getvalue())


def selftest() -> int:
    failures: list[str] = []

    def eq(name: str, got: Any, want: Any) -> None:
        if got != want:
            failures.append(f"{name}: got {got!r}, want {want!r}")

    code, data = _run_text(_GOOD)
    eq("good tune exit", code, 0)
    code, data = _run_text(_GOOD.replace("w: I count the num-bers |", "w: I count the | num-bers"))
    eq("w mismatch exit", code, 1)
    eq("w mismatch location", any("Verse 1:1" in v["location"] for v in data["violations"]), True)
    code, data = _run_text(_GOOD.replace("B2 A2 F4 |", "B2 A2 F3 |"))
    eq("short bar (middle) exit", code, 1)
    code, _ = _run_text(_GOOD.replace("D2 E2 F2 GA", "D2 E2 F2 GA D").replace("w: I count", "w: I I count"))
    eq("long bar exit", code, 1)
    code, data = _run_text(_GOOD.replace("d2 c2 B2 A2", "d2 c2 B2 a'2"))
    eq("leap/range exit", code, 1)
    code, _ = _run_text(_GOOD, ["--vocal-range", "A3-E5"])
    eq("in range exit", code, 0)
    code, _ = _run_text(_GOOD, ["--vocal-range", "C5-E5"])
    eq("out of range exit", code, 1)
    code, _ = _run_text(_GOOD.replace("X:1", "X:one"))
    eq("malformed exit", code, 3)
    code, _ = _run_text(_GOOD.replace("Q:1/4=100\n", ""))
    eq("missing Q exit", code, 1)
    if failures:
        sys.stdout.write("abc_validate selftest: FAIL\n" + "\n".join("  " + f for f in failures) + "\n")
        return 1
    sys.stdout.write("abc_validate selftest: PASS\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--selftest" in argv:
        return selftest()
    return gc.run("abc_validate.py", "Validate melody.abc: headers, bars, range, leaps, lyric alignment.",
                  gate_args, gate_main, argv)


if __name__ == "__main__":
    sys.exit(main())
