"""Unit tests for music-team/scripts/arrangement_check.py (W8)."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # noqa: E402
from _helpers import FIXTURES, load_script

HEADER = "key: D\nmode: major\nbpm: 118\ntime_sig: 4/4\n\n"
TABLE_HEAD = ("| section | energy | instruments_in | instruments_out | texture_note |\n"
              "|---------|--------|----------------|-----------------|--------------|\n")
GOOD_ROWS = [
    ("Verse 1", 3, "guitar, bass", "-", "sparse"),
    ("Chorus", 7, "drums, pad", "-", "wide"),
    ("Verse 2", 4, "shaker", "pad", "thin"),
    ("Chorus", 8, "keys", "-", "full"),
    ("Bridge", 5, "piano", "drums", "stripped"),
    ("Chorus", 9, "backing vocals", "-", "peak"),
]
STRUCTURE = ("key: D\nmode: major\nbpm: 118\ntime_sig: 4/4\nform_template: VCVCBC\n\n"
             "| section | label | bars | meter_spec | rhyme_scheme |\n|---|---|---|---|---|\n"
             "| 1 | Verse 1 | 8 | 8/uSuSuSuS | A |\n| 2 | Chorus | 8 | 8/uSuSuSuS | A |\n"
             "| 3 | Verse 2 | 8 | 8/uSuSuSuS | A |\n| 4 | Chorus | 8 | 8/uSuSuSuS | A |\n"
             "| 5 | Bridge | 4 | 8/uSuSuSuS | A |\n| 6 | Chorus | 8 | 8/uSuSuSuS | A |\n")


def table(rows) -> str:
    return HEADER + TABLE_HEAD + "".join(f"| {a} | {b} | {c} | {d} | {e} |\n" for a, b, c, d, e in rows)


class ArrangementCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_script("arrangement_check")

    def run_gate(self, text: str, *extra: str, structure: str | None = None, config: str | None = None):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "arrangement.md").write_text(text, encoding="utf-8")
            argv = ["--json", *extra]
            if structure is not None:
                (d / "structure.md").write_text(structure, encoding="utf-8")
                argv += ["--structure", str(d / "structure.md")]
            if config is not None:
                (d / "config.yml").write_text(config, encoding="utf-8")
                argv += ["--config", str(d / "config.yml")]
            argv.append(str(d / "arrangement.md"))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = self.mod.main(argv)
            return code, json.loads(buf.getvalue())

    def test_pass_with_structure(self):
        code, data = self.run_gate(table(GOOD_ROWS), structure=STRUCTURE)
        self.assertEqual((code, data["status"]), (0, "PASS"))
        self.assertEqual(data["metrics"]["energy_range"], 6)

    def test_json_shape(self):
        _, data = self.run_gate(table(GOOD_ROWS))
        self.assertEqual(set(data), {"script", "status", "thresholds", "metrics", "violations"})
        self.assertEqual(data["script"], "arrangement_check")
        self.assertEqual(data["thresholds"]["min_energy_range"], 3)

    def test_flat_energy_fails(self):
        rows = [(n, 5, c, o, t) for n, _, c, o, t in GOOD_ROWS]
        code, data = self.run_gate(table(rows))
        self.assertEqual((code, data["status"]), (1, "FAIL"))
        self.assertTrue(any("flat" in v["reason"] for v in data["violations"]))

    def test_min_energy_range_flag_and_config(self):
        rows = [("Verse 1", 4, "a", "-", "x"), ("Chorus", 6, "b", "-", "y")]
        self.assertEqual(self.run_gate(table(rows))[0], 1)
        self.assertEqual(self.run_gate(table(rows), "--min-energy-range", "2")[0], 0)
        self.assertEqual(self.run_gate(table(rows), config="quality:\n  min_energy_range: 2\n")[0], 0)

    def test_missing_section_fails(self):
        rows = [r for r in GOOD_ROWS if r[0] != "Bridge"]
        code, data = self.run_gate(table(rows), structure=STRUCTURE)
        self.assertEqual(code, 1)
        self.assertTrue(any(v["location"] == "Bridge" for v in data["violations"]))

    def test_extra_section_fails(self):
        rows = GOOD_ROWS + [("Outro", 4, "pad", "-", "thin")]
        code, data = self.run_gate(table(rows), structure=STRUCTURE)
        self.assertEqual(code, 1)
        self.assertTrue(any(v["location"] == "Outro" for v in data["violations"]))

    def test_chorus_lower_than_verse_fails(self):
        rows = list(GOOD_ROWS)
        rows[1] = ("Chorus", 2, "drums, pad", "-", "wide")
        code, data = self.run_gate(table(rows))
        self.assertEqual(code, 1)
        self.assertTrue(any("Verse 1" in v["location"] for v in data["violations"]))

    def test_free_curve_passes_any_shape(self):
        rows = list(GOOD_ROWS)
        rows[1] = ("Chorus", 2, "drums, pad", "-", "wide")
        code, _ = self.run_gate(table(rows), "--energy-curve", "free")
        self.assertEqual(code, 0)

    def test_empty_instrument_cell_fails(self):
        rows = list(GOOD_ROWS)
        rows[2] = ("Verse 2", 4, "", "pad", "thin")
        code, data = self.run_gate(table(rows))
        self.assertEqual(code, 1)
        self.assertTrue(any("instruments_in" in v["reason"] for v in data["violations"]))

    def test_sounds_like_fails(self):
        rows = list(GOOD_ROWS)
        rows[0] = ("Verse 1", 3, "guitar, bass", "-", "sounds like a late-night demo")
        code, data = self.run_gate(table(rows))
        self.assertEqual(code, 1)
        self.assertTrue(any("banned phrase" in v["reason"] for v in data["violations"]))

    def test_blocked_target_fails(self):
        rows = list(GOOD_ROWS)
        rows[0] = ("Verse 1", 3, "guitar, bass", "-", "tone from Taylor Swift")
        code, data = self.run_gate(table(rows))
        self.assertEqual(code, 1)
        self.assertTrue(any("blocked target" in v["reason"] for v in data["violations"]))

    def test_malformed_tables_are_errors(self):
        bad_cases = {
            "missing column": HEADER + "| section | energy |\n|---|---|\n| Verse 1 | 3 |\n",
            "non-integer energy": table([("Verse 1", "loud", "a", "-", "x")]),
            "energy out of range": table([("Verse 1", 11, "a", "-", "x")]),
            "wrong cell count": HEADER + TABLE_HEAD + "| Verse 1 | 3 | a |\n",
            "no rows": HEADER + TABLE_HEAD,
            "no table": HEADER,
        }
        for name, text in bad_cases.items():
            with self.subTest(name):
                code, data = self.run_gate(text)
                self.assertEqual((code, data["status"]), (3, "ERROR"))

    def test_bad_energy_curve_is_error(self):
        code, _ = self.run_gate(table(GOOD_ROWS), "--energy-curve", "zigzag")
        self.assertEqual(code, 3)

    def test_no_chorus_reports_metric(self):
        rows = [("Verse 1", 2, "a", "-", "x"), ("Bridge", 6, "b", "-", "y"), ("Outro", 4, "c", "-", "z")]
        code, data = self.run_gate(table(rows))
        self.assertEqual(code, 0)
        self.assertEqual(data["metrics"]["no_chorus"], 1)

    def test_selftest_passes(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.mod.main(["--selftest"]), 0)

    def test_fixtures(self):
        full = FIXTURES / "songs" / "FULL_SONG"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = self.mod.main(["--json", "--structure", str(full / "structure.md"), str(full / "arrangement.md")])
        self.assertEqual(code, 0)
        for case in ("flat-energy", "arrangement-missing-section", "arrangement-chorus-low"):
            d = FIXTURES / "negative" / case
            if not d.exists():
                continue
            with self.subTest(case):
                argv = ["--json"] + (["--structure", str(d / "structure.md")] if (d / "structure.md").exists() else [])
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(self.mod.main(argv + [str(d / "arrangement.md")]), 1)


if __name__ == "__main__":
    unittest.main()
