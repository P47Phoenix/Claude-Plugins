"""Unit tests for music-team/scripts/abc_validate.py (Wave 5)."""
from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # noqa: E402
from _helpers import FIXTURES, SCRIPTS, load_script

av = load_script("abc_validate")

GOOD = """X:1
T:Test Tune
M:4/4
L:1/8
Q:1/4=118
K:D
%%section Verse 1
D2 E2 F2 GA | B2 A2 F4 |
w: I count the num-bers | on the street |
%%section Chorus
d2 c2 B2 A2 | B2 A2 F2 ED |
w: No-bo-dy knows | my name here yet_ |
"""
STRUCTURE = """key: D
mode: major
bpm: 118
time_sig: 4/4
form_template: VCVCBC

| section | label | bars | meter_spec | rhyme_scheme |
|---------|-------|------|------------|--------------|
| 1 | Verse 1 | 2 | 8/uSuSuuuS | A |
| 2 | Chorus | 2 | 8/SuuSuSSS | A |
"""
LYRICS = "[Verse 1]\nI count the numbers on the street\n\n[Chorus]\nNobody knows my name here yet\n"


def run_gate(abc: str, structure: str | None = STRUCTURE, lyrics: str | None = None,
             extra: list[str] | None = None) -> tuple[int, dict]:
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "melody.abc").write_text(abc, encoding="utf-8")
        args = ["--json", str(d / "melody.abc")]
        for name, body in (("structure.md", structure), ("lyrics.md", lyrics)):
            if body is not None:
                (d / name).write_text(body, encoding="utf-8")
                args.append(str(d / name))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = av.main(args + (extra or []))
        return code, json.loads(buf.getvalue())


class ParseTests(unittest.TestCase):
    def test_pitches_follow_key_signature(self):
        tune = av.parse_abc(GOOD)
        first = [e.pitches[0] for s in tune.lines[0].segments for e in s.events]
        self.assertEqual(first[:4], [62, 64, 66, 67])  # D E F# G in D major
        self.assertEqual(tune.lines[1].segments[0].events[0].pitches, [74])  # d = D5

    def test_accidental_persists_within_bar(self):
        tune = av.parse_abc(GOOD.replace("D2 E2 F2 GA |", "D2 =F2 F2 GA |"))
        pitches = [e.pitches[0] for e in tune.lines[0].segments[0].events]
        self.assertEqual(pitches[1:3], [65, 65])

    def test_durations_tuplet_and_broken_rhythm(self):
        abc = GOOD.replace("D2 E2 F2 GA |", "(3DEF G2 A2 B2 |").replace("B2 A2 F4 |", "B>A F2 F4 |")
        tune = av.parse_abc(abc)
        self.assertEqual(tune.bars[0][3], av.Fraction(1))
        self.assertEqual(tune.bars[1][3], av.Fraction(1))

    def test_ties_take_no_syllable(self):
        tune = av.parse_abc(GOOD.replace("B2 A2 F4 |", "B2 A2 F2-F2 |"))
        self.assertEqual(tune.lines[0].segments[1].slots(), 3)

    def test_rests_chords_and_annotations(self):
        abc = GOOD.replace("D2 E2 F2 GA |", '"D"[DF]2 z2 F2 GA |')
        tune = av.parse_abc(abc)
        self.assertEqual(tune.lines[0].segments[0].slots(), 4)

    def test_lyric_tokens(self):
        self.assertEqual(av.tokenize_lyric("a-b c | d_ e * |"), [3, 4])
        self.assertEqual(av.tokenize_lyric("one~two three |"), [2])
        self.assertEqual(av.tokenize_lyric("he- llo | x"), [2, 1])

    def test_malformed_raises(self):
        for bad in (GOOD.replace("X:1", "X:one"), GOOD.replace("D2 E2", "D2 ]] E2"), GOOD.replace("D2 E2", "(D2 E2"),
                    GOOD.replace("K:D", "Zq: nope\nK:D"), GOOD.replace("D2 E2", "D2 ? E2")):
            with self.assertRaises(ValueError):
                av.parse_abc(bad)


class GateTests(unittest.TestCase):
    def test_pass(self):
        code, data = run_gate(GOOD, lyrics=LYRICS)
        self.assertEqual(code, 0, data)
        self.assertEqual(data["status"], "PASS")
        self.assertEqual(data["script"], "abc_validate")
        self.assertEqual(data["metrics"]["lyric_lines_checked"], 2)

    def test_headers_required(self):
        code, data = run_gate(GOOD.replace("Q:1/4=118\n", ""), structure=None)
        self.assertEqual(code, 1)
        self.assertTrue(any("missing required header Q" in v["reason"] for v in data["violations"]))

    def test_structure_consistency(self):
        cases = ((GOOD.replace("M:4/4", "M:3/4"), "melody.abc:M"), (GOOD.replace("K:D", "K:Dm"), "melody.abc:K"),
                 (GOOD.replace("1/4=118", "1/4=90"), "melody.abc:Q"),
                 (GOOD.replace("%%section Chorus", "%%section Bridge"), "melody.abc:sections"))
        for abc, loc in cases:
            code, data = run_gate(abc)
            self.assertEqual(code, 1, loc)
            self.assertTrue(any(v["location"] == loc for v in data["violations"]), (loc, data["violations"]))

    def test_bar_length(self):
        code, data = run_gate(GOOD.replace("D2 E2 F2 GA |", "D2 E2 F2 G |"), structure=None)
        self.assertEqual(code, 0)  # short first bar is a tolerated pickup
        code, data = run_gate(GOOD.replace("B2 A2 F4 |", "B2 A2 F2 |"), structure=None)
        self.assertEqual(code, 1)  # a short bar mid-tune is not a pickup
        self.assertTrue(any(v["location"] == "Verse 1:2" for v in data["violations"]))
        code, _ = run_gate(GOOD.replace("D2 E2 F2 GA |", "D2 E2 F2 GA D |"), structure=None)
        self.assertEqual(code, 1)  # overfull
        code, _ = run_gate(GOOD.replace("B2 A2 F2 ED |", "B2 A2 F2 |"), structure=None)
        self.assertEqual(code, 0)  # short final bar tolerated
        code, _ = run_gate(GOOD.replace("B2 A2 F2 ED |", "B2 A2 F2 |"), structure=None, extra=["--strict-bars"])
        self.assertEqual(code, 1)

    def test_range_and_leap(self):
        code, data = run_gate(GOOD, structure=None, extra=["--vocal-range", "C5-E5"])
        self.assertEqual(code, 1)
        self.assertTrue(any("vocal range" in v["reason"] for v in data["violations"]))
        self.assertEqual(run_gate(GOOD, structure=None, extra=["--vocal-range", "A3-E5"])[0], 0)
        self.assertEqual(run_gate(GOOD, structure=None, extra=["--vocal-range", "50-80"])[0], 0)
        code, data = run_gate(GOOD, structure=None, extra=["--max-leap", "2"])
        self.assertEqual(code, 1)
        self.assertTrue(any("leap" in v["reason"] for v in data["violations"]))

    def test_lyric_mismatch_location(self):
        abc = GOOD.replace("w: I count the num-bers | on the street |", "w: I count the | num-bers on the street |")
        code, data = run_gate(abc, lyrics=LYRICS)
        self.assertEqual(code, 1)
        self.assertTrue(any("Verse 1:1" in v["location"] for v in data["violations"]))

    def test_lyric_text_mismatch(self):
        code, data = run_gate(GOOD.replace("on the street", "on the roads"), lyrics=LYRICS)
        self.assertEqual(code, 1)
        self.assertTrue(any(v["location"] == "Verse 1:text" for v in data["violations"]))

    def test_instrumental_skips_alignment(self):
        abc = GOOD.replace("w: I count the num-bers | on the street |\n", "")
        self.assertEqual(run_gate(abc, lyrics=LYRICS)[0], 1)
        self.assertEqual(run_gate(abc, lyrics=None)[0], 0)

    def test_v_lines_limit(self):
        code, data = run_gate(GOOD.replace("K:D", "K:D\nV:1\nV:2"), structure=None)
        self.assertEqual(code, 1)

    def test_malformed_is_error(self):
        code, data = run_gate(GOOD.replace("X:1", "X:one"))
        self.assertEqual(code, 3)
        self.assertEqual(data["status"], "ERROR")

    def test_missing_file_is_error(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(av.main(["--json", "/nonexistent/melody.abc"]), 3)

    def test_selftest(self):
        p = subprocess.run([sys.executable, "-I", str(SCRIPTS / "abc_validate.py"), "--selftest"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)


class FixtureTests(unittest.TestCase):
    def run_in(self, case: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-I", str(SCRIPTS / "abc_validate.py"), "--json", *args],
                              cwd=str(case), capture_output=True, text=True)

    def test_full_song_passes(self):
        p = self.run_in(FIXTURES / "songs" / "FULL_SONG", "melody.abc", "structure.md", "lyrics.md", "brief.md")
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_negative_fixtures(self):
        p = self.run_in(FIXTURES / "negative" / "malformed-abc", "melody.abc", "structure.md")
        self.assertEqual(p.returncode, 3)
        p = self.run_in(FIXTURES / "negative" / "w-mismatch", "melody.abc", "lyrics.md", "structure.md")
        self.assertEqual(p.returncode, 1)
        self.assertIn("Verse 1:1", p.stdout)


if __name__ == "__main__":
    unittest.main()
