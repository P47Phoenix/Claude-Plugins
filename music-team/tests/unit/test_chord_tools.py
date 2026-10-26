"""Unit tests for music-team/scripts/chord_tools.py (Wave 5)."""
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

ct = load_script("chord_tools")

CHORDS = """key: C major

[Verse 1]
| I | vi | IV | V |
> | C | Am | F | G |
"""
STRUCTURE = "key: C\nmode: major\nbpm: 100\ntime_sig: 4/4\nform_template: VCVCBC\n"


def spell_scale(tonic: str, mode: str) -> list[str]:
    t, m = ct.parse_key(tonic, mode)
    return [ct.spell(n) for n in ct.scale_notes(t, m)]


def run_gate(chords: str, structure: str | None = STRUCTURE, extra: list[str] | None = None) -> tuple[int, dict]:
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "chords.md").write_text(chords, encoding="utf-8")
        args = ["--json", str(d / "chords.md")]
        if structure is not None:
            (d / "structure.md").write_text(structure, encoding="utf-8")
            args.append(str(d / "structure.md"))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ct.main(args + (extra or []))
        return code, json.loads(buf.getvalue())


class SpellingTests(unittest.TestCase):
    def test_scales(self):
        self.assertEqual(spell_scale("C", "major"), list("CDEFGAB"))
        self.assertIn("Bb", spell_scale("F", "major"))
        self.assertNotIn("A#", spell_scale("F", "major"))
        self.assertEqual(spell_scale("G", "major")[6], "F#")
        self.assertEqual(spell_scale("D", "minor")[5], "Bb")
        self.assertEqual(spell_scale("A", "melodic minor"), ["A", "B", "C", "D", "E", "F#", "G#"])
        self.assertEqual(spell_scale("D", "dorian"), list("DEFGABC"))
        self.assertEqual(spell_scale("B", "locrian")[1], "C")
        self.assertEqual(spell_scale("Gb", "major")[3], "Cb")

    def test_chords(self):
        self.assertEqual(ct.parse_chord("Am7").spelling(), ["A", "C", "E", "G"])
        self.assertEqual(ct.parse_chord("Fmaj7").spelling(), ["F", "A", "C", "E"])
        self.assertEqual(ct.parse_chord("G7").spelling(), ["G", "B", "D", "F"])
        self.assertEqual(ct.parse_chord("Bm7b5").spelling(), ["B", "D", "F", "A"])
        self.assertEqual(ct.parse_chord("Cdim7").spelling(), ["C", "Eb", "Gb", "Bbb"])
        self.assertEqual(ct.parse_chord("Dsus4").spelling(), ["D", "G", "A"])
        self.assertEqual(ct.parse_chord("Cadd9").spelling(), ["C", "E", "G", "D"])
        self.assertEqual(ct.parse_chord("C/E").spelling(), ["E", "C", "G"])
        self.assertEqual(ct.parse_chord("G9").spelling(), ["G", "B", "D", "F", "A"])
        self.assertEqual(ct.parse_chord("F#m").spelling(), ["F#", "A", "C#"])
        with self.assertRaises(ValueError):
            ct.parse_chord("H7")
        with self.assertRaises(ValueError):
            ct.parse_chord("Cxyz")

    def test_transpose(self):
        d, s, x = ct.parse_interval("P5")
        self.assertEqual([ct.transpose_chord(ct.parse_chord(c), d, s, x).symbol() for c in ("C", "F", "G")],
                         ["G", "C", "D"])
        d, s, x = ct.parse_interval("-M2")
        self.assertEqual(ct.transpose_chord(ct.parse_chord("C"), d, s, x).symbol(), "Bb")
        d, s, x = ct.parse_interval("m3")
        self.assertEqual(ct.transpose_chord(ct.parse_chord("Am7"), d, s, x).symbol(), "Cm7")
        with self.assertRaises(ValueError):
            ct.parse_interval("P3")

    def test_diatonic_and_roman(self):
        t, m = ct.parse_key("Eb")
        self.assertEqual([c.symbol() for c in ct.diatonic_chords(t, m, True)],
                         ["Ebmaj7", "Fm7", "Gm7", "Abmaj7", "Bb7", "Cm7", "Dm7b5"])
        t, m = ct.parse_key("C")
        self.assertEqual(" ".join(ct.chord_to_roman(ct.parse_chord(c), t) for c in ("Am", "F", "C", "G")), "vi IV I V")
        self.assertFalse(ct.is_diatonic(ct.parse_chord("Bb"), t, m))
        self.assertEqual(ct.roman_to_chord("V7/vi", t).symbol(), "E7")
        self.assertEqual(ct.roman_to_chord("bVII", ct.parse_key("D")[0]).symbol(), "C")
        self.assertEqual(ct.roman_to_chord("ii°", t).symbol(), "Ddim")
        self.assertEqual(ct.roman_to_chord("I/3", t).symbol(), "C/E")

    def test_reharmonize(self):
        t, m = ct.parse_key("C")
        out = ct.reharmonize(t, m, [ct.parse_chord(c) for c in ("C", "C", "F", "G")], "jazz")["progression"]
        self.assertIn("Dm7 G7 Cmaj7", " ".join(out))
        self.assertTrue(all(ct.parse_chord(c).has_seventh() for c in out))
        for style in ("blues", "gospel", "bossa-nova", "pop"):
            res = ct.reharmonize(t, m, [ct.parse_chord(c) for c in ("C", "Am", "F", "G")], style)
            self.assertTrue(res["rows"], style)
        blues = ct.reharmonize(t, m, [ct.parse_chord("C")], "blues")
        self.assertEqual(len(blues["sketch_12_bar"]), 12)
        with self.assertRaises(ValueError):
            ct.reharmonize(t, m, [ct.parse_chord("C")], "polka")


class ToolCliTests(unittest.TestCase):
    def run_tool(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-I", str(SCRIPTS / "chord_tools.py"), *args],
                              capture_output=True, text=True)

    def test_scale_and_json(self):
        p = self.run_tool("scale", "F", "major", "--json")
        self.assertEqual(p.returncode, 0)
        self.assertEqual(json.loads(p.stdout)["notes"], ["F", "G", "A", "Bb", "C", "D", "E"])

    def test_transpose_negative_interval(self):
        p = self.run_tool("transpose", "C", "F", "G", "--by", "-M2")
        self.assertEqual(p.stdout.split(), ["Bb", "Eb", "F"])
        p = self.run_tool("transpose", "C", "G", "--to", "D", "--from-key", "C")
        self.assertEqual(p.stdout.split(), ["D", "A"])

    def test_roman_command(self):
        p = self.run_tool("roman", "C:", "Am", "F", "C", "G")
        self.assertEqual(p.stdout.strip().splitlines()[-1], "vi IV I V")

    def test_selftest_exit_zero(self):
        p = self.run_tool("--selftest")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_tool_error_exit_three(self):
        self.assertEqual(self.run_tool("chord", "Zz9").returncode, 3)


class GateTests(unittest.TestCase):
    def test_pass_shape(self):
        code, data = run_gate(CHORDS)
        self.assertEqual(code, 0)
        self.assertEqual(data["status"], "PASS")
        self.assertEqual(data["script"], "chord_tools")
        for k in ("thresholds", "metrics", "violations"):
            self.assertIn(k, data)
        self.assertEqual(data["metrics"]["diatonic_ratio"], 1.0)
        self.assertIn("Verse 1:1 | C | Am | F | G", data["metrics"]["concert"])

    def test_non_diatonic_fails_ratio(self):
        chords = "key: C major\n\n[Verse 1]\n| bII | #iv | bVI | I |\n"
        code, data = run_gate(chords)
        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "FAIL")
        self.assertTrue(any("diatonic" in v["reason"] for v in data["violations"]))

    def test_ratio_override(self):
        chords = "key: C major\n\n[Verse 1]\n| I | bVII | IV | V |\n"
        self.assertEqual(run_gate(chords)[0], 0)
        self.assertEqual(run_gate(chords, extra=["--diatonic-min", "0.9"])[0], 1)

    def test_repeat_cell_counts(self):
        code, data = run_gate("key: C major\n\n[Verse 1]\n| I | % | IV | V |\n")
        self.assertEqual(data["metrics"]["chords"], 4)

    def test_concert_mismatch_fails(self):
        code, data = run_gate(CHORDS.replace("| C | Am | F | G |", "| C | Am | F | A |"))
        self.assertEqual(code, 1)
        self.assertTrue(any(v["location"] == "Verse 1:1:4" for v in data["violations"]))

    def test_unparseable_cell_is_error(self):
        code, data = run_gate("key: C major\n\n[Verse 1]\n| I | Q9 | IV | V |\n")
        self.assertEqual(code, 3)
        self.assertEqual(data["status"], "ERROR")

    def test_key_header_mismatch_fails(self):
        code, data = run_gate(CHORDS.replace("key: C major", "key: D major"))
        self.assertEqual(code, 1)
        self.assertTrue(any(v["location"] == "chords.md:key" for v in data["violations"]))

    def test_missing_file_is_error(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ct.main(["--json", "/nonexistent/chords.md"])
        self.assertEqual(code, 3)

    def test_cadence_warning_not_failure(self):
        code, data = run_gate("key: C major\n\n[Verse 1]\n| I | IV | vi | ii |\n")
        self.assertEqual(code, 0)
        self.assertGreaterEqual(data["metrics"]["warnings"], 1)

    def test_fixture_songs(self):
        song = FIXTURES / "songs" / "FULL_SONG"
        p = subprocess.run([sys.executable, "-I", str(SCRIPTS / "chord_tools.py"), "--json", "chords.md", "structure.md"],
                           cwd=str(song), capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout)
        neg = FIXTURES / "negative" / "wrong-key-chords"
        p = subprocess.run([sys.executable, "-I", str(SCRIPTS / "chord_tools.py"), "--json", "chords.md", "structure.md"],
                           cwd=str(neg), capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)


if __name__ == "__main__":
    unittest.main()
