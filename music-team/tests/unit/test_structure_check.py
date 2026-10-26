"""Unit tests for music-team/scripts/structure_check.py (W1-2)."""
from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # noqa: E402
from _helpers import load_script


STRUCTURE = """key: D
mode: major
bpm: 118
time_sig: 4/4
form_template: VCVCBC

| section | label | bars | meter_spec | rhyme_scheme |
|---------|-------|------|------------|--------------|
| 1 | Verse 1 | 8 | 8/uSuSuSuS; 8/uSuSuSuS | AB |
| 2 | Chorus | 8 | 7/SuSuSuS; 7/SuSuSuS | AA |
| 3 | Verse 2 | 8 | 8/uSuSuSuS; 8/uSuSuSuS | AB |
| 4 | Chorus | 8 | 7/SuSuSuS; 7/SuSuSuS | AA |
| 5 | Bridge | 4 | 8/uSuSuSuS | A |
| 6 | Chorus | 8 | 7/SuSuSuS; 7/SuSuSuS | AA |
"""

LYRICS = """[Verse 1]
I packed the car with everything I own
# comment line is ignored
the road was long and quiet as a stone

[Chorus]
Nobody knows my name here yet
Nobody knows my name here yet

[Verse 2]
A key that does not fit a single door
I hang it on a nail and ask for more

[Chorus]
Nobody knows my name here yet
Nobody knows my name here yet

[Bridge]
a stranger says it and the street goes still

[Chorus]
Nobody knows my name here yet
Nobody knows my name here yet
"""

CHORDS = """key: D major

[Verse 1]
| I | V | vi | IV |
> | D | A | Bm | G |

[Chorus]
| I | V | vi | IV |

[Verse 2]
| I | V | vi | IV |

[Chorus]
| I | V | vi | IV |

[Bridge]
| vi | IV |

[Chorus]
| I | V | vi | IV |
"""

MELODY = """X:1
T:Nobody Knows My Name Here
M:4/4
L:1/8
Q:1/4=118
K:D
%%section Verse 1
D2 F2 A2 F2 | G2 F2 E4 |
w: I packed the car with ev-ery-thing_ |
%%section Chorus
"D"d2 f2 g2 f2 | g2 f2 e4 |
%%section Verse 2
D2 F2 A2 F2 | G2 F2 E4 |
%%section Chorus
d2 f2 g2 f2 | g2 f2 e4 |
%%section Bridge
B2 A2 G2 F2 | E8 |
%%section Chorus
d2 f2 g2 f2 | g2 f2 e4 |
"""

ARRANGEMENT = """key: D
mode: major
bpm: 118
time_sig: 4/4

| section | energy | instruments_in | instruments_out | texture_note |
|---------|--------|----------------|-----------------|--------------|
| Verse 1 | 3 | acoustic guitar | - | sparse |
| Chorus | 6 | drums | - | wide |
| Verse 2 | 4 | bass | - | fuller |
| Chorus | 7 | synth pad | - | wide |
| Bridge | 8 | strings | drums | lift |
| Chorus | 9 | - | - | all in |
"""


class StructureCheckTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_script("structure_check")
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

    def _structure(self, rows: list[tuple[str, int, str]], template: str = "VCVCBC", header: str = "") -> str:
        head = header or "key: D\nmode: major\nbpm: 118\ntime_sig: 4/4\n"
        lines = [head + f"form_template: {template}\n", "| section | label | bars | meter_spec | rhyme_scheme |",
                 "|---|---|---|---|---|"]
        for i, (label, bars, meter) in enumerate(rows, 1):
            lines.append(f"| {i} | {label} | {bars} | {meter} | A |")
        return self._write("structure.md", "\n".join(lines) + "\n")

    # ---- form -----------------------------------------------------------
    def test_pass_basic_vcvcbc(self):
        code, out = self._run(self._write("structure.md", STRUCTURE))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["violations"], [])
        self.assertEqual(out["metrics"]["sections"], 6)

    def test_pass_appendix_a_expansion(self):
        rows = [("Verse 1", 8, "8/uS"), ("Pre-Chorus 1", 4, "6/uS"), ("Chorus", 8, "7/S"),
                ("Verse 2", 8, "8/uS"), ("Pre-Chorus 2", 4, "6/uS"), ("Chorus", 8, "7/S"),
                ("Bridge", 8, "8/uS"), ("Chorus", 8, "7/S"), ("Outro", 4, "")]
        code, out = self._run(self._structure(rows))
        self.assertEqual(out["status"], "PASS", out)
        rows[-1] = ("Chorus", 8, "7/S")
        code, out = self._run(self._structure(rows))
        self.assertEqual(out["status"], "PASS", out)

    def test_fail_wrong_order(self):
        rows = [("Chorus", 8, "7/S"), ("Verse 1", 8, "8/uS"), ("Verse 2", 8, "8/uS"),
                ("Chorus", 8, "7/S"), ("Bridge", 8, "8/uS"), ("Chorus", 8, "7/S")]
        code, out = self._run(self._structure(rows))
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        self.assertEqual(out["violations"][0]["location"], "structure.md:sections")

    def test_fail_bars_out_of_range(self):
        rows = [("Verse 1", 40, "8/uS"), ("Chorus", 8, "7/S"), ("Verse 2", 8, "8/uS"),
                ("Chorus", 8, "7/S"), ("Bridge", 8, "8/uS"), ("Chorus", 8, "7/S")]
        code, out = self._run(self._structure(rows))
        self.assertEqual(out["status"], "FAIL")
        v = out["violations"][0]
        self.assertEqual((v["location"], v["observed"], v["limit"]), ("Verse 1", 40, [4, 16]))

    def test_fail_lyric_line_count(self):
        lyrics = LYRICS.replace("the road was long and quiet as a stone\n", "")
        code, out = self._run(self._write("structure.md", STRUCTURE), self._write("lyrics.md", lyrics))
        self.assertEqual(out["status"], "FAIL")
        v = out["violations"][0]
        self.assertEqual((v["location"], v["observed"], v["limit"]), ("Verse 1", 1, 2))

    def test_pass_with_matching_lyrics(self):
        code, out = self._run(self._write("structure.md", STRUCTURE), self._write("lyrics.md", LYRICS))
        self.assertEqual(out["status"], "PASS", out)

    def test_error_unknown_template(self):
        code, out = self._run(self._structure([("Verse 1", 8, "8/uS")], template="sonata"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("unknown form_template", out["violations"][0]["reason"])

    def test_error_missing_template(self):
        code, out = self._run(self._structure([("Verse 1", 8, "8/uS")], template=""))
        self.assertEqual((code, out["status"]), (3, "ERROR"))

    def test_jingle_total_bar_cap(self):
        rows = [("Chorus", 8, "6/S"), ("Verse 1", 8, "7/S"), ("Chorus", 8, "6/S")]
        code, out = self._run(self._structure(rows, template="jingle"))
        self.assertEqual(out["status"], "FAIL")
        self.assertEqual(out["violations"][0]["location"], "structure.md:total_bars")

    def test_other_templates_pass(self):
        cases = {
            "AABA": [("A1", 8, ""), ("A2", 8, ""), ("B", 8, ""), ("A3", 8, "")],
            "edm-build-drop": [("Intro", 8, ""), ("Build", 8, ""), ("Drop", 16, ""), ("Breakdown", 8, ""),
                               ("Build", 8, ""), ("Drop", 16, ""), ("Outro", 8, "")],
            "verse-refrain": [("Verse 1", 12, ""), ("Verse 2", 12, ""), ("Verse 3", 12, "")],
            "through-composed": [("Intro", 4, ""), ("Verse 1", 12, ""), ("Bridge", 6, "")],
        }
        for tpl, rows in cases.items():
            code, out = self._run(self._structure(rows, template=tpl))
            self.assertEqual(out["status"], "PASS", (tpl, out))

    def test_windows_style_path(self):
        p = Path(self._write("structure.md", STRUCTURE))
        arg = p.as_posix().replace("/", "\\", 1) if os.name == "nt" else str(p)
        code, out = self._run(arg)
        self.assertEqual(out["status"], "PASS", out)

    def test_help_exits_zero(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as cm:
            self.mod.main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("--consistency", buf.getvalue())

    # ---- consistency ----------------------------------------------------
    def _all(self, melody: str = MELODY, chords: str = CHORDS, arrangement: str = ARRANGEMENT) -> list[str]:
        return [self._write("structure.md", STRUCTURE), self._write("lyrics.md", LYRICS),
                self._write("chords.md", chords), self._write("melody.abc", melody),
                self._write("arrangement.md", arrangement)]

    def test_consistency_pass(self):
        code, out = self._run("--consistency", *self._all())
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"]["artifacts_compared"], 4)
        self.assertEqual(out["thresholds"]["vocal_range"], [55, 79])
        self.assertEqual((out["metrics"]["melody_min_pitch"], out["metrics"]["melody_max_pitch"]), (62, 79))

    def test_consistency_fail_abc_key(self):
        code, out = self._run("--consistency", *self._all(melody=MELODY.replace("K:D\n", "K:Em\n")))
        self.assertEqual(out["status"], "FAIL")
        locs = {v["location"]: v for v in out["violations"]}
        self.assertEqual(locs["melody.abc:key"]["observed"], "E")
        self.assertEqual(locs["melody.abc:key"]["limit"], "D")
        self.assertEqual(locs["melody.abc:mode"]["observed"], "minor")

    def test_consistency_fail_pitch_out_of_range(self):
        code, out = self._run("--consistency", *self._all(melody=MELODY.replace("E8 |", "E8 | a'4 z4 |")))
        self.assertEqual(out["status"], "FAIL")
        v = [v for v in out["violations"] if v["location"] == "melody.abc:range"][0]
        self.assertEqual((v["observed"], v["limit"]), (93, 79))

    def test_consistency_fail_chords_and_arrangement(self):
        code, out = self._run("--consistency", *self._all(
            chords=CHORDS.replace("key: D major", "key: G major"),
            arrangement=ARRANGEMENT.replace("bpm: 118", "bpm: 120").replace("| Bridge |", "| Breakdown |")))
        locs = {v["location"] for v in out["violations"]}
        self.assertEqual(locs, {"chords.md:key", "arrangement.md:bpm", "arrangement.md:sections"})

    def test_consistency_missing_fields_are_violations(self):
        melody = MELODY.replace("M:4/4\n", "").replace("Q:1/4=118\n", "")
        chords = CHORDS.replace("key: D major\n", "")
        arrangement = ARRANGEMENT.replace("key: D\nmode: major\nbpm: 118\ntime_sig: 4/4\n", "")
        code, out = self._run("--consistency", *self._all(melody=melody, chords=chords, arrangement=arrangement))
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        missing = {v["location"]: v for v in out["violations"] if v["observed"] is None}
        self.assertEqual(set(missing), {"melody.abc:bpm", "melody.abc:time_sig", "chords.md:key", "chords.md:mode",
                                        "arrangement.md:key", "arrangement.md:mode", "arrangement.md:bpm",
                                        "arrangement.md:time_sig"})
        self.assertEqual(missing["melody.abc:bpm"]["limit"], "118")
        self.assertIn("missing from", missing["chords.md:key"]["reason"])
        # ABC without K: declares no key either
        code, out = self._run("--consistency", *self._all(melody=MELODY.replace("K:D\n", "")))
        locs = {v["location"] for v in out["violations"] if v["observed"] is None}
        self.assertEqual(locs, {"melody.abc:key", "melody.abc:mode"})

    def test_error_bad_vocal_range(self):
        cfg = self._write("config.yml", "quality:\n  vocal_range: [low, high]\n")
        code, out = self._run("--consistency", "--config", cfg, *self._all())
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("vocal_range", out["violations"][0]["reason"])

    def test_threshold_precedence_genre_override(self):
        cfg = self._write("config.yml", "quality:\n  vocal_range: [55, 79]\n  genre_overrides:\n"
                                        "    pop:\n      vocal_range: [60, 70]\n")
        code, out = self._run("--consistency", "--config", cfg, "--genre", "pop", *self._all())
        self.assertEqual(out["thresholds"]["vocal_range"], [60, 70])
        self.assertEqual(out["status"], "FAIL")
        code, out = self._run("--consistency", "--config", cfg, "--genre", "pop", "--vocal-range", "50,90", *self._all())
        self.assertEqual(out["thresholds"]["vocal_range"], [50, 90])
        self.assertEqual(out["status"], "PASS")

    # ---- helpers --------------------------------------------------------
    def test_abc_note_to_midi(self):
        f = self.mod.abc_note_to_midi
        self.assertEqual(f("C", {}), 60)
        self.assertEqual(f("c", {}), 72)
        self.assertEqual(f("C,", {}), 48)
        self.assertEqual(f("c'", {}), 84)
        self.assertEqual(f("^F", {}), 66)
        self.assertEqual(f("_B", {}), 70)
        self.assertEqual(f("F", {"F": 1}), 66)
        self.assertEqual(f("=F", {"F": 1}), 65)
        self.assertEqual(self.mod.key_accidentals("D", "major"), {"F": 1, "C": 1})
        self.assertEqual(self.mod.key_accidentals("D", "minor"), {"B": -1})
        self.assertEqual(self.mod.parse_abc_key("D dorian"), ("D", "dorian"))
        self.assertEqual(self.mod.parse_abc_key("Dmin"), ("D", "minor"))

    def test_parse_abc_sections_and_templates(self):
        self.assertEqual(self.mod.parse_abc_sections(MELODY)[:2], ["Verse 1", "Chorus"])
        tpls = self.mod.load_form_templates()
        self.assertEqual(set(tpls), {"VCVCBC", "AABA", "verse-refrain", "jingle", "edm-build-drop", "through-composed"})
        for t in tpls.values():
            self.assertIn("tempo_band", t)
            self.assertIn("default_meter", t)


if __name__ == "__main__":
    unittest.main()
