"""Unit tests for song-team/scripts/challenge_gate.py (W1-2)."""
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

HEAD = "## Findings\n\n| severity | location | finding | suggested fix |\n|---|---|---|---|\n"


class ChallengeGateTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_script("challenge_gate")
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, text: str, name: str = "challenge-report.md") -> str:
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
        self.assertIn("usage:", buf.getvalue())

    def test_pass_no_blockers(self):
        code, out = self._run(self._write(HEAD + "| MINOR | lyrics.md:Bridge:2 | rhyme predictable | slant it |\n"
                                                 "| major | chords.md:Chorus | static | add a IV |\n"))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"], {"blocker": 0, "major": 1, "minor": 1})
        self.assertEqual(out["violations"], [])

    def test_pass_header_only(self):
        code, out = self._run(self._write(HEAD))
        self.assertEqual((code, out["status"]), (0, "PASS"))
        self.assertEqual(out["metrics"]["blocker"], 0)

    def test_fail_blocker_rows(self):
        code, out = self._run(self._write(HEAD + "| BLOCKER | lyrics.md:Verse 2:3 | quotes a known lyric | rewrite |\n"
                                                 "| MINOR | lyrics.md:Bridge:2 | rhyme | slant |\n"
                                                 "| Blocker | melody.abc:Chorus | leap of 14 | narrow |\n"))
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        self.assertEqual(out["metrics"]["blocker"], 2)
        self.assertEqual([(v["location"], v["reason"]) for v in out["violations"]],
                         [("lyrics.md:Verse 2:3", "quotes a known lyric"), ("melody.abc:Chorus", "leap of 14")])

    def test_first_matching_table_only(self):
        text = ("| a | b |\n|---|---|\n| 1 | 2 |\n\n" + HEAD + "| MINOR | x | y | z |\n\n"
                "| severity | location | finding | suggested fix |\n|---|---|---|---|\n| BLOCKER | x | y | z |\n")
        code, out = self._run(self._write(text))
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["metrics"]["minor"], 1)

    def test_error_missing_table(self):
        code, out = self._run(self._write("## Findings\n\nNo table here, just prose.\n\n| a | b |\n|---|---|\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("no severity table", out["violations"][0]["reason"])

    def test_error_wrong_column_count(self):
        code, out = self._run(self._write("## Findings\n\n| severity | finding |\n|---|---|\n| MINOR | x |\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("header has 2 cells, expected 4", out["violations"][0]["reason"])
        code, out = self._run(self._write(HEAD.replace("| suggested fix |", "| suggested fix | owner |")
                                          + "| MINOR | x | y | z | me |\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("header has 5 cells, expected 4", out["violations"][0]["reason"])

    def test_error_bad_severity(self):
        code, out = self._run(self._write(HEAD + "| CRITICAL | x | y | z |\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("CRITICAL", out["violations"][0]["reason"])
        self.assertTrue(out["violations"][0]["location"].endswith(":5"))

    def test_error_short_row(self):
        code, out = self._run(self._write(HEAD + "| MINOR | x | y |\n"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("3 cells", out["violations"][0]["reason"])

    def test_windows_style_path(self):
        p = Path(self._write(HEAD + "| MINOR | x | y | z |\n"))
        arg = p.as_posix().replace("/", "\\", 1) if os.name == "nt" else str(p)
        code, out = self._run(arg)
        self.assertEqual(out["status"], "PASS", out)

    def test_config_and_genre_do_not_change_result(self):
        cfg = self._write("quality:\n  genre_overrides:\n    pop: { hook_max_syllables: 16 }\n", "config.yml")
        code, out = self._run("--config", cfg, "--genre", "pop", self._write(HEAD + "| BLOCKER | x | y | z |\n"))
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        self.assertEqual(out["thresholds"], {})


if __name__ == "__main__":
    unittest.main()
