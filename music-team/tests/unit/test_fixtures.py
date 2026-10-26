"""Fixture-driven gate tests (W1-0 / W1-2 / W3-1).

Walks music-team/tests/fixtures/{negative,songs,resemblance}/**/expected.json and
runs the real gate scripts as subprocesses under ``python -I`` so the CLI,
exit codes and --json contract are exercised end to end.

expected.json shapes:
  negative / resemblance: {"expectations": [{"script", "args", "status", "location_contains"?}]}
  songs/<TYPE>:           {"<script_name>": "PASS|SKIPPED", ...}  (plus "song_type")
Scripts that do not exist yet (later waves) are skipped, not failed.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
SCRIPTS = PLUGIN / "scripts"
FIXTURES = PLUGIN / "tests" / "fixtures"

# Default artifact arguments per script for the songs/<TYPE>/ sets.
SONG_ARGS = {
    "prosody_check": ["lyrics.md", "structure.md", "brief.md"],
    "rhyme_check": ["lyrics.md", "structure.md", "brief.md"],
    "structure_check": ["structure.md", "lyrics.md"],
    "cliche_scan": ["lyrics.md"],
    "chord_tools": ["chords.md", "structure.md"],
    "abc_validate": ["melody.abc", "structure.md", "lyrics.md", "brief.md"],
    "arrangement_check": ["arrangement.md"],
    "challenge_gate": ["challenge-report.md"],
    "resemblance_check": ["lyrics.md"],
}
EXIT = {"PASS": 0, "FAIL": 1, "SKIPPED": 2, "ERROR": 3}


def run_script(script: str, args: list[str], cwd: Path) -> tuple[int, dict]:
    path = SCRIPTS / f"{script}.py"
    if not path.exists():
        return -1, {}
    proc = subprocess.run(
        [sys.executable, "-I", str(path), "--json", *args],
        cwd=str(cwd), capture_output=True, text=True, encoding="utf-8",
    )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        data = {"_stdout": proc.stdout, "_stderr": proc.stderr}
    return proc.returncode, data


class FixtureGateTests(unittest.TestCase):
    def _check(self, case_dir: Path, exp: dict) -> None:
        script = exp["script"]
        code, data = run_script(script, exp.get("args", []), case_dir)
        if code == -1:
            self.skipTest(f"{script}.py not implemented yet")
        want = exp["status"]
        self.assertEqual(
            code, EXIT[want],
            f"{case_dir.name}: {script} {exp.get('args')} expected {want}, got exit {code}: {json.dumps(data)[:400]}",
        )
        self.assertEqual(data.get("status"), want)
        self.assertEqual(data.get("script"), script)
        sub = exp.get("location_contains")
        if sub:
            locs = " | ".join(v.get("location", "") for v in data.get("violations", []))
            self.assertIn(sub, locs, f"{case_dir.name}: no violation location contains {sub!r}: {locs}")

    def test_negative_and_resemblance_cases(self):
        ran = 0
        for group in ("negative", "resemblance"):
            for exp_file in sorted((FIXTURES / group).glob("**/expected.json")):
                spec = json.loads(exp_file.read_text(encoding="utf-8"))
                for exp in spec.get("expectations", []):
                    with self.subTest(case=f"{group}/{exp_file.parent.name}", script=exp["script"]):
                        self._check(exp_file.parent, exp)
                        ran += 1
        self.assertGreater(ran, 0)

    def test_song_sets_pass_every_gate(self):
        ran = 0
        for exp_file in sorted((FIXTURES / "songs").glob("*/expected.json")):
            spec = json.loads(exp_file.read_text(encoding="utf-8"))
            for script, want in spec.items():
                if script == "song_type" or script not in SONG_ARGS:
                    continue
                args = [a for a in SONG_ARGS[script] if (exp_file.parent / a).exists()]
                with self.subTest(song=exp_file.parent.name, script=script):
                    self._check(exp_file.parent, {"script": script, "args": args, "status": want})
                    ran += 1
        self.assertGreater(ran, 0)

    def test_song_sets_pass_structure_consistency(self):
        artifacts = ["structure.md", "lyrics.md", "chords.md", "melody.abc", "arrangement.md"]
        ran = 0
        for exp_file in sorted((FIXTURES / "songs").glob("*/expected.json")):
            present = [a for a in artifacts if (exp_file.parent / a).exists()]
            if "structure.md" not in present:
                continue
            with self.subTest(song=exp_file.parent.name):
                self._check(exp_file.parent, {"script": "structure_check", "args": ["--consistency", *present],
                                              "status": "PASS"})
                ran += 1
        self.assertGreater(ran, 0)

    def test_every_fixture_dir_has_expected_json(self):
        for group in ("negative", "songs"):
            for d in sorted((FIXTURES / group).iterdir()):
                if d.is_dir():
                    self.assertTrue((d / "expected.json").exists(), f"{group}/{d.name} lacks expected.json")

    def test_windows_style_fixture_paths(self):
        path = FIXTURES / "negative" / "challenge-blocker" / "challenge-report.md"
        # Windows: a genuinely mixed separator path; POSIX: the plain path (backslash is a filename char there)
        arg = path.as_posix().replace("/", "\\", 1) if os.name == "nt" else str(path)
        code, data = run_script("challenge_gate", [arg], PLUGIN)
        if code == -1:
            self.skipTest("challenge_gate.py missing")
        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
