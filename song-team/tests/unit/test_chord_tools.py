"""Unit tests for song-team/scripts/chord_tools.py (W3-1)."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # noqa: E402
from _helpers import FIXTURES, load_script, mixed_path

FULL = FIXTURES / "songs" / "FULL_SONG"
WRONG_KEY = FIXTURES / "negative" / "wrong-key-chords"

STRUCTURE_D = """key: D
mode: major
bpm: 118
time_sig: 4/4
form_template: VCVCBC

| section | label | bars | meter_spec | rhyme_scheme |
|---------|-------|------|------------|--------------|
| 1 | Verse 1 | 8 | 8/uSuSuSuS | A |
"""


class ChordToolsTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_script("chord_tools")
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, name: str, text: str) -> str:
        p = self.root / name
        p.write_text(text, encoding="utf-8", newline="\n")
        return str(p)

    def _run(self, *argv: str) -> tuple[int, dict]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = self.mod.main(["--json", *argv])
        return code, json.loads(buf.getvalue())

    def _chords(self, body: str, key: str = "D major") -> str:
        return self._write("chords.md", f"key: {key}\n\n{body}")

    # -- fixtures -----------------------------------------------------------
    def test_help_exits_zero(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as cm:
            self.mod.main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("--diatonic-min-ratio", buf.getvalue())

    def test_full_song_fixture_passes(self):
        code, out = self._run(str(FULL / "chords.md"), str(FULL / "structure.md"))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        m = out["metrics"]
        self.assertEqual((m["chords_total"], m["diatonic"], m["diatonic_ratio"], m["sections"]), (56, 56, 1.0, 8))
        self.assertEqual(out["thresholds"]["diatonic_min_ratio"], 0.6)
        self.assertEqual(out["thresholds"]["key"], "D major")
        self.assertEqual(out["violations"], [])
        self.assertEqual(out["concert"]["Verse 1"][0], ["D", "A", "Bm", "G"])
        self.assertEqual(out["concert"]["Bridge"][1], ["Bm", "G", "A", "D"])

    def test_wrong_key_fixture_fails_with_ratio_one_sixteenth(self):
        code, out = self._run(str(WRONG_KEY / "chords.md"), str(WRONG_KEY / "structure.md"))
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        self.assertEqual(out["metrics"]["chords_total"], 16)
        self.assertEqual(out["metrics"]["diatonic"], 1)
        self.assertEqual(out["metrics"]["diatonic_ratio"], 0.0625)
        locs = [v["location"] for v in out["violations"]]
        self.assertEqual(len(locs), 15 + 1)  # one per non-diatonic cell plus the summary
        self.assertIn("Verse 1:1:1", locs)
        self.assertNotIn("Chorus:1:3", locs)  # iii is diatonic
        self.assertEqual(locs[-1], "chords.md")
        # concert spellings follow the accidental direction (fixture's own > lines)
        self.assertEqual(out["concert"]["Verse 1"][0], ["Db", "F#m", "Ab", "Bb"])

    # -- parsing ------------------------------------------------------------
    def test_parse_roman_grammar(self):
        pr = self.mod.parse_roman
        self.assertEqual(pr("I"), (0, 1, False, "maj", None))
        self.assertEqual(pr("vi"), (0, 6, True, "min", None))
        self.assertEqual(pr("bVII"), (-1, 7, False, "maj", None))
        self.assertEqual(pr("#iv"), (1, 4, True, "min", None))
        self.assertEqual(pr("vii°"), (0, 7, True, "dim", None))
        self.assertEqual(pr("viidim"), (0, 7, True, "dim", None))
        self.assertEqual(pr("III+"), (0, 3, False, "aug", None))
        self.assertEqual(pr("V7"), (0, 5, False, "maj7", None))
        self.assertEqual(pr("IVmaj7"), (0, 4, False, "majmaj7", None))
        self.assertEqual(pr("iim7"), (0, 2, True, "min7", None))
        self.assertEqual(pr("IIm7"), (0, 2, False, "min7", None))  # m7 forces a minor triad
        self.assertEqual(pr("Isus4"), (0, 1, False, "majsus4", None))
        self.assertEqual(pr("I/III"), (0, 1, False, "maj", (0, 3)))
        self.assertEqual(pr("V7/bVII"), (0, 5, False, "maj7", (-1, 7)))
        self.assertEqual(pr("I/3"), (0, 1, False, "maj", (0, 3)))
        for bad in ("H", "VIII", "", "I-V", "Db", "%%"):
            with self.assertRaises(ValueError, msg=bad):
                pr(bad)

    def test_concert_name(self):
        cn, pr = self.mod.concert_name, self.mod.parse_roman
        self.assertEqual(cn("D", "major", pr("vi")), "Bm")
        self.assertEqual(cn("D", "major", pr("I/III")), "D/F#")
        self.assertEqual(cn("D", "major", pr("bVII")), "C")
        self.assertEqual(cn("F", "major", pr("V7")), "C7")
        self.assertEqual(cn("Bb", "major", pr("iii")), "Dm")
        self.assertEqual(cn("A", "minor", pr("VI")), "F")
        self.assertEqual(cn("A", "minor", pr("bVII")), "G")
        self.assertEqual(cn("A", "minor", pr("ii°")), "Bdim")
        self.assertEqual(cn("C", "major", pr("#iv")), "F#m")
        self.assertEqual(cn("E", "major", pr("V")), "B")

    def test_slash_bass_and_bvii_counted(self):
        # D major: I/III and V/VII diatonic; bVII is not -> 3/4 passes the 0.6 default
        code, out = self._run(self._chords("[Verse 1]\n| I/III | V/VII | bVII | I |\n"))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"]["diatonic_ratio"], 0.75)
        self.assertEqual(out["concert"]["Verse 1"][0], ["D/F#", "A/C#", "C", "D"])

    def test_percent_repeats_previous_cell_and_counts(self):
        code, out = self._run(self._chords("[Verse 1]\n| I | % | bVII | % |\n"))
        self.assertEqual(out["metrics"]["chords_total"], 4)
        self.assertEqual(out["metrics"]["diatonic"], 2)
        self.assertEqual(out["metrics"]["diatonic_ratio"], 0.5)
        self.assertEqual(out["status"], "FAIL")
        self.assertEqual(out["concert"]["Verse 1"][0], ["D", "D", "C", "C"])

    def test_percent_first_cell_is_error(self):
        code, out = self._run(self._chords("[Verse 1]\n| % | I |\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertEqual(out["violations"][0]["location"], "Verse 1:1:1")

    def test_unparseable_cell_is_error_with_location(self):
        code, out = self._run(self._chords("[Verse 1]\n| I | V |\n| vi | H7 |\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertEqual(out["violations"][0]["location"], "Verse 1:2:2")
        self.assertIn("H7", out["violations"][0]["reason"])

    def test_concert_and_comment_lines_ignored(self):
        body = "[Verse 1]\n# a comment\n| I | V |\n> | D | A |\n| IV | I |\n"
        code, out = self._run(self._chords(body))
        self.assertEqual(out["metrics"]["chords_total"], 4)
        self.assertEqual(out["concert"]["Verse 1"], [["D", "A"], ["G", "D"]])

    # -- key resolution -----------------------------------------------------
    def test_key_from_structure_overrides_chords_header(self):
        chords = self._chords("[Verse 1]\n| I | IV | V | I |\n", key="G major")
        structure = self._write("structure.md", STRUCTURE_D)
        code, out = self._run(chords, structure)
        self.assertEqual(out["thresholds"]["key"], "D major")
        self.assertEqual(out["concert"]["Verse 1"][0], ["D", "G", "A", "D"])

    def test_key_falls_back_to_chords_header(self):
        code, out = self._run(self._chords("[Verse 1]\n| i | iv | V | i |\n", key="A minor"))
        self.assertEqual(out["thresholds"]["key"], "A minor")
        self.assertEqual(out["concert"]["Verse 1"][0], ["Am", "Dm", "E", "Am"])
        self.assertEqual(out["metrics"]["diatonic"], 3)  # V major is borrowed in natural minor

    def test_error_when_no_key_anywhere(self):
        code, out = self._run(self._write("chords.md", "[Verse 1]\n| I | V |\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("key", out["violations"][0]["reason"])

    def test_minor_and_modal_tables(self):
        code, out = self._run(self._chords("[Verse 1]\n| i | ii° | III | iv | v | VI | VII | bVII |\n", key="A minor"))
        self.assertEqual(out["metrics"]["diatonic"], 8)
        code, out = self._run(self._chords("[Verse 1]\n| I | ii | iii | IV | v | vi | bVII |\n", key="G mixolydian"))
        self.assertEqual(out["metrics"]["diatonic"], 6)  # iii is dim in mixolydian
        code, out = self._run(self._chords("[Verse 1]\n| i | ii | bIII | IV | v | vi° | bVII |\n", key="D dorian"))
        self.assertEqual(out["metrics"]["diatonic"], 7)
        code, out = self._run(self._chords("[Verse 1]\n| I | II | iii | #iv° | V | vi | vii |\n", key="F lydian"))
        self.assertEqual(out["metrics"]["diatonic"], 7)

    def test_sus_and_sevenths_tolerated(self):
        code, out = self._run(self._chords("[Verse 1]\n| Isus4 | V7 | iim7 | IVmaj7 | Iadd9 | vii° |\n"))
        self.assertEqual(out["metrics"]["diatonic"], 6)
        self.assertEqual(out["concert"]["Verse 1"][0], ["Dsus4", "A7", "Em7", "Gmaj7", "Dadd9", "C#dim"])

    # -- thresholds ---------------------------------------------------------
    def test_boundary_ratio_exactly_at_threshold_passes(self):
        # 3 of 5 diatonic = 0.6 == default threshold -> PASS
        code, out = self._run(self._chords("[Verse 1]\n| I | IV | V | bVII | bVI |\n"))
        self.assertEqual(out["metrics"]["diatonic_ratio"], 0.6)
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        code, out = self._run("--diatonic-min-ratio", "0.61", self._chords("[Verse 1]\n| I | IV | V | bVII | bVI |\n"))
        self.assertEqual((code, out["status"]), (1, "FAIL"))

    def test_threshold_precedence(self):
        cfg = self._write("config.yml", "quality:\n  diatonic_min_ratio: 0.5\n  genre_overrides:\n"
                                        "    jazz: { diatonic_min_ratio: 0.1 }\n")
        chords = self._chords("[Verse 1]\n| I | bII | bIII | bVI |\n")  # ratio 0.25
        code, out = self._run("--config", cfg, chords)
        self.assertEqual((out["thresholds"]["diatonic_min_ratio"], out["status"]), (0.5, "FAIL"))
        code, out = self._run("--config", cfg, "--genre", "jazz", chords)
        self.assertEqual((out["thresholds"]["diatonic_min_ratio"], out["status"]), (0.1, "PASS"))
        code, out = self._run("--config", cfg, "--genre", "jazz", "--diatonic-min-ratio", "0.9", chords)
        self.assertEqual((out["thresholds"]["diatonic_min_ratio"], out["status"]), (0.9, "FAIL"))

    def test_error_bad_threshold_type(self):
        cfg = self._write("config.yml", "quality:\n  diatonic_min_ratio: mostly\n")
        code, out = self._run("--config", cfg, self._chords("[Verse 1]\n| I |\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("diatonic_min_ratio", out["violations"][0]["reason"])

    # -- warnings -----------------------------------------------------------
    def test_warnings_parallel_fifths_and_cadence(self):
        code, out = self._run(self._chords("[Verse 1]\n| I | IV | V | I |\n[Chorus]\n| I | IV | ii | iii |\n"))
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["metrics"]["warnings"], 3)
        reasons = {(w["location"], w["reason"].split(":")[0]) for w in out["warnings"]}
        self.assertIn(("Verse 1:1:3", "possible parallel fifths"), reasons)   # IV -> V
        self.assertIn(("Chorus:1:4", "possible parallel fifths"), reasons)    # ii -> iii
        self.assertIn(("Chorus:1:4", "section does not end on a cadence"), reasons)
        self.assertNotIn(("Verse 1:1:4", "section does not end on a cadence"), reasons)  # V-I

    def test_cadences_accepted(self):
        for ending in ("V | I", "IV | I", "V | vi", "bVII | I"):
            code, out = self._run(self._chords(f"[Verse 1]\n| ii | {ending} |\n"))
            self.assertFalse(any("cadence" in w["reason"] for w in out.get("warnings", [])), ending)

    def test_no_warnings_key_absent_when_clean(self):
        code, out = self._run(self._chords("[Verse 1]\n| I | iii | V | I |\n"))
        self.assertEqual(out["status"], "PASS")
        self.assertNotIn("warnings", out)
        self.assertEqual(out["metrics"]["warnings"], 0)

    # -- misc ---------------------------------------------------------------
    def test_error_no_chord_cells(self):
        code, out = self._run(self._chords("[Verse 1]\n> | D | A |\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))

    def test_windows_style_path(self):
        code, out = self._run(mixed_path(str(FULL / "chords.md")), mixed_path(str(FULL / "structure.md")))
        self.assertEqual(out["status"], "PASS", out)

    def test_text_mode_prints_concert_lines(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = self.mod.main([self._chords("[Verse 1]\n| I | V | vi | IV |\n")])
        self.assertEqual(code, 0)
        self.assertIn("> | D | A | Bm | G |", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
