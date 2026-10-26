"""Unit tests for music-team/scripts/adapt_check.py (Wave 7)."""
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

SONG = FIXTURES / "songs" / "ADAPT_GENRE"
NEG = FIXTURES / "negative" / "adapt-report-missing-disposition"

GOOD = """---
song_type: ADAPT_GENRE
source_genre: folk
target_genre: bossa nova
---

## Kept
- hook line, first-person voice

## Changed

| Element | Source | Target | Why |
|---------|--------|--------|-----|
| bpm | 72 | 120 | bossa pulse |
| time_sig | 3/4 | 4/4 | straight pulse |

## Lyric re-fit
- Verse 1: 9 -> 7 syllables

## Risks
- singability of line 3
"""


class AdaptCheckTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_script("adapt_check")
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, text: str, name: str = "adaptation-report.md") -> str:
        p = self.root / name
        p.write_text(text, encoding="utf-8", newline="\n")
        return str(p)

    def _run(self, *argv: str) -> tuple[int, dict]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = self.mod.main(["--json", *argv])
        return code, json.loads(buf.getvalue())

    def test_help_exits_zero(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as cm:
            self.mod.main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("--max-changed", buf.getvalue())

    def test_pass_on_fixture(self):
        code, out = self._run(str(SONG / "adaptation-report.md"), str(SONG / "structure.md"), str(SONG / "lyrics.md"))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"]["changed"], 8)
        self.assertEqual(out["violations"], [])

    def test_pass_inline_report(self):
        code, out = self._run(self._write(GOOD))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["thresholds"], {"require_report": True, "max_changed_elements": 12})

    def test_fail_on_missing_disposition_fixture(self):
        code, out = self._run(str(NEG / "adaptation-report.md"))
        self.assertEqual((code, out["status"]), (1, "FAIL"), out)
        self.assertTrue(any("## Changed:row 2" in v["location"] and "why" in v["reason"] for v in out["violations"]))

    def test_fail_empty_cells_each_listed(self):
        text = GOOD.replace("| bossa pulse |", "|  |").replace("| 3/4 |", "|  |")
        code, out = self._run(self._write(text))
        self.assertEqual(code, 1)
        reasons = " ".join(v["reason"] for v in out["violations"])
        self.assertIn("'why'", reasons)
        self.assertIn("'source'", reasons)
        self.assertEqual(len(out["violations"]), 2)

    def test_fail_empty_kept(self):
        code, out = self._run(self._write(GOOD.replace("- hook line, first-person voice", "")))
        self.assertEqual(code, 1)
        self.assertTrue(any("## Kept" in v["location"] for v in out["violations"]))

    def test_fail_missing_sections(self):
        text = GOOD.split("## Lyric re-fit")[0]
        code, out = self._run(self._write(text))
        self.assertEqual(code, 1)
        locs = " ".join(v["location"] for v in out["violations"])
        self.assertIn("Lyric re-fit", locs)
        self.assertIn("Risks", locs)

    def test_fail_empty_risks(self):
        code, out = self._run(self._write(GOOD.replace("- singability of line 3", "")))
        self.assertEqual(code, 1)
        self.assertTrue(any("## Risks" in v["location"] for v in out["violations"]))

    def test_fail_over_max_flag(self):
        code, out = self._run("--max-changed", "1", self._write(GOOD))
        self.assertEqual(code, 1)
        v = out["violations"][0]
        self.assertEqual((v["observed"], v["limit"]), (2, 1))

    def test_fail_over_max_from_config(self):
        cfg = self.root / "config.yml"
        cfg.write_text("adaptation:\n  max_changed_elements: 1\n", encoding="utf-8")
        code, out = self._run("--config", str(cfg), self._write(GOOD))
        self.assertEqual(code, 1)
        self.assertEqual(out["thresholds"]["max_changed_elements"], 1)

    def test_flag_beats_config(self):
        cfg = self.root / "config.yml"
        cfg.write_text("adaptation:\n  max_changed_elements: 1\n", encoding="utf-8")
        code, out = self._run("--config", str(cfg), "--max-changed", "5", self._write(GOOD))
        self.assertEqual((code, out["status"]), (0, "PASS"))

    def test_unknown_target_genre_fails(self):
        code, out = self._run(self._write(GOOD.replace("target_genre: bossa nova", "target_genre: nowhere pop")))
        self.assertEqual(code, 1)
        self.assertTrue(any("target_genre" in v["reason"] for v in out["violations"]))

    def test_artist_target_does_not_resolve(self):
        code, out = self._run(self._write(GOOD.replace("target_genre: bossa nova", "target_genre: Some Named Band")))
        self.assertEqual(code, 1)

    def test_alias_and_slug_resolve(self):
        for label in ("bossa", "Bossa Nova", "bossa-nova"):
            with self.subTest(label=label):
                code, _ = self._run(self._write(GOOD.replace("bossa nova\n---", f"{label}\n---")))
                self.assertEqual(code, 0)

    def test_wrong_song_type_fails(self):
        code, out = self._run(self._write(GOOD.replace("ADAPT_GENRE", "FULL_SONG")))
        self.assertEqual(code, 1)
        self.assertTrue(any("song_type" in v["reason"] for v in out["violations"]))

    def test_error_on_malformed_table(self):
        for name, text in (
            ("header", GOOD.replace("| Why |", "| Reason |")),
            ("cells", GOOD.replace("| bpm | 72 | 120 | bossa pulse |", "| bpm | 72 | 120 |")),
            ("no table", GOOD.split("| Element")[0] + "\n- bpm changed\n\n## Lyric re-fit\n- x\n\n## Risks\n- y\n"),
        ):
            with self.subTest(case=name):
                code, out = self._run(self._write(text))
                self.assertEqual((code, out["status"]), (3, "ERROR"), out)
                self.assertIn("## Changed", out["violations"][0]["location"])

    def test_skipped_when_absent_and_not_required(self):
        cfg = self.root / "config.yml"
        cfg.write_text("adaptation:\n  require_report: false\n", encoding="utf-8")
        code, out = self._run("--config", str(cfg), str(self.root / "adaptation-report.md"))
        self.assertEqual((code, out["status"]), (2, "SKIPPED"), out)
        self.assertIn("skipped_reason", out["metrics"])
        self.assertEqual(out["violations"], [])

    def test_absent_and_required_fails(self):
        code, out = self._run(str(self.root / "adaptation-report.md"))
        self.assertEqual((code, out["status"]), (1, "FAIL"), out)
        self.assertIn("missing", out["violations"][0]["reason"])

    def test_no_arguments_required_fails(self):
        code, out = self._run()
        self.assertEqual((code, out["status"]), (1, "FAIL"))

    def test_bad_config_value_errors(self):
        cfg = self.root / "config.yml"
        cfg.write_text("adaptation:\n  max_changed_elements: lots\n", encoding="utf-8")
        code, out = self._run("--config", str(cfg), self._write(GOOD))
        self.assertEqual((code, out["status"]), (3, "ERROR"))

    def test_missing_config_errors(self):
        code, out = self._run("--config", str(self.root / "nope.yml"), self._write(GOOD))
        self.assertEqual((code, out["status"]), (3, "ERROR"))

    def test_warning_for_unmentioned_structure_section(self):
        s = self._write(
            "key: G\nmode: minor\nbpm: 120\ntime_sig: 4/4\nform_template: through-composed\n\n"
            "| section | label | bars | meter_spec | rhyme_scheme |\n|---|---|---|---|---|\n"
            "| 1 | Verse 1 | 8 | 7/SuSuSuS | A |\n| 2 | Coda | 4 | 7/SuSuSuS | A |\n", "structure.md")
        code, out = self._run(self._write(GOOD.replace("Verse 1", "Verse 1")), s)
        self.assertEqual(code, 0)
        self.assertEqual(out["warnings"][0]["observed"], "Coda")

    def test_json_shape(self):
        code, out = self._run(self._write(GOOD))
        self.assertEqual(set(out), {"script", "status", "thresholds", "metrics", "violations"})
        self.assertEqual(out["script"], "adapt_check")

    def test_subprocess_exit_codes_under_isolated_mode(self):
        script = str(SCRIPTS / "adapt_check.py")
        for args, want in (
            ([str(SONG / "adaptation-report.md")], 0),
            ([str(NEG / "adaptation-report.md")], 1),
            ([str(self._write(GOOD.replace("| Why |", "| Reason |")))], 3),
        ):
            proc = subprocess.run([sys.executable, "-I", script, "--json", *args], capture_output=True, text=True)
            self.assertEqual(proc.returncode, want, proc.stdout + proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["script"], "adapt_check")

    def test_selftest_flag(self):
        proc = subprocess.run([sys.executable, "-I", str(SCRIPTS / "adapt_check.py"), "--selftest"],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("OK", proc.stdout)


if __name__ == "__main__":
    unittest.main()
