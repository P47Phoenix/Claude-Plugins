"""Unit tests for song-team/scripts/gate_common.py (W1-1)."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"


def _load():
    spec = importlib.util.spec_from_file_location("gate_common", SCRIPTS / "gate_common.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


CONFIG = """schema_version: 1

routing:
  force_type: null   # comment
  default_language: en

quick: false

loops:
  concept: 3

quality:
  cliche_max_per_100_words: 2
  prosody_tolerance: 0.15
  vocal_range: [55, 79]
  genre_overrides: { hip-hop: { hook_max_syllables: 16, vocal_range: [50, 70] } }

originality:
  resemblance_corpus:
    - lyrics/a.txt
    - "lyrics/b.txt"
  ngram_max_overlap: 0.05
"""

STRUCTURE = """key: D
mode: major
bpm: 118
time_sig: 4/4
form_template: VCVCBC

| section | label | bars | meter_spec | rhyme_scheme |
|---------|-------|------|------------|--------------|
| 1 | Verse 1 | 8 | 8/uSuSuSuS; 8/uSuSuSuS | AxAx |
| 2 | Chorus | 8 | 7/SuSuSuS | A |
"""

LYRICS = """[Verse 1]
I packed the car with everything I own
# comment line
and drove until the road was mine alone

[Chorus]
Nobody knows my name here yet
"""


class GateCommonTests(unittest.TestCase):
    def setUp(self):
        self.gc = _load()

    def test_yaml_subset(self):
        cfg = self.gc.load_yaml(CONFIG)
        self.assertEqual(cfg["schema_version"], 1)
        self.assertIsNone(cfg["routing"]["force_type"])
        self.assertEqual(cfg["routing"]["default_language"], "en")
        self.assertIs(cfg["quick"], False)
        self.assertEqual(cfg["loops"]["concept"], 3)
        self.assertEqual(cfg["quality"]["prosody_tolerance"], 0.15)
        self.assertEqual(cfg["quality"]["vocal_range"], [55, 79])
        ov = cfg["quality"]["genre_overrides"]["hip-hop"]
        self.assertEqual(ov["hook_max_syllables"], 16)
        self.assertEqual(ov["vocal_range"], [50, 70])
        self.assertEqual(cfg["originality"]["resemblance_corpus"], ["lyrics/a.txt", "lyrics/b.txt"])

    def test_threshold_precedence(self):
        cfg = self.gc.load_yaml(CONFIG)
        r = self.gc.resolve_threshold
        self.assertEqual(r("hook_max_syllables", {}, None), 12)                 # default
        self.assertEqual(r("cliche_max_per_100_words", cfg, None), 2)           # quality
        self.assertEqual(r("hook_max_syllables", cfg, "hip-hop"), 16)           # genre override
        self.assertEqual(r("hook_max_syllables", cfg, "hip-hop", flag_value=9), 9)  # flag
        self.assertEqual(r("ngram_max_overlap", cfg, None, section="originality"), 0.05)

    def test_parse_structure_and_sections(self):
        st = self.gc.parse_structure(STRUCTURE)
        self.assertEqual(st["header"]["key"], "D")
        self.assertEqual(st["header"]["bpm"], 118)
        self.assertEqual(st["header"]["time_sig"], "4/4")
        self.assertEqual([s["label"] for s in st["sections"]], ["Verse 1", "Chorus"])
        self.assertEqual(st["sections"][0]["meter"], [(8, "uSuSuSuS"), (8, "uSuSuSuS")])
        self.assertEqual(st["sections"][0]["rhyme_scheme"], "AxAx")
        secs = self.gc.parse_sections(LYRICS)
        self.assertEqual(secs[0][0], "Verse 1")
        self.assertEqual(len(secs[0][1]), 2)  # comment skipped
        self.assertEqual(secs[1][1], ["Nobody knows my name here yet"])

    def test_frontmatter(self):
        fm, body = self.gc.parse_frontmatter("---\ntheme: a\nlanguage: es\nmust_avoid: [x, y]\n---\n## Brief\ntext\n")
        self.assertEqual(fm["language"], "es")
        self.assertEqual(fm["must_avoid"], ["x", "y"])
        self.assertIn("## Brief", body)

    def test_norm_and_file_named(self):
        self.assertEqual(self.gc.norm("a\\b\\lyrics.md"), "a/b/lyrics.md")
        self.assertEqual(self.gc.file_named(["x\\structure.md", "x\\Lyrics.md"], "lyrics.md"), "x\\Lyrics.md")

    def test_run_contract_and_exit_codes(self):
        gc = self.gc
        with tempfile.TemporaryDirectory() as d:
            brief = Path(d) / "brief.md"
            brief.write_text("---\nlanguage: es\ngenre: pop\n---\n", encoding="utf-8")

            def main(args, config, result):
                lang = gc.resolve_language(args.language, args.paths)
                if lang != "en":
                    return result.skip("language " + lang)
                return result

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = gc.run("demo.py", "demo", None, main, ["--json", str(brief)])
            data = json.loads(out.getvalue())
            self.assertEqual(code, 2)
            self.assertEqual(data["status"], "SKIPPED")
            self.assertEqual(data["script"], "demo")
            self.assertEqual(data["violations"], [])

            def failing(args, config, result):
                result.violate("Verse 1:2", "x", 0.2, 0.15)
                return result

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = gc.run("demo.py", "demo", None, failing, ["--json"])
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(out.getvalue())["violations"][0]["location"], "Verse 1:2")

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = gc.run("demo.py", "demo", None, lambda a, c, r: r.error("bad"), ["--json"])
            self.assertEqual(code, 3)

            # explicit --config that does not exist -> ERROR, never silent defaults
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = gc.run("demo.py", "demo", None, lambda a, c, r: r, ["--json", "--config", str(Path(d) / "nope.yml")])
            self.assertEqual(code, 3)
            self.assertIn("nope.yml", json.loads(out.getvalue())["violations"][0]["reason"])

            # any unexpected exception class in main_fn -> ERROR with JSON, not a traceback
            for exc in (TypeError("t"), AttributeError("a"), PermissionError("p")):
                def boom(a, c, r, exc=exc):
                    raise exc
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = gc.run("demo.py", "demo", None, boom, ["--json"])
                self.assertEqual(code, 3)
                self.assertEqual(json.loads(out.getvalue())["status"], "ERROR")

    def test_yaml_edge_cases(self):
        gc = self.gc
        self.assertEqual(gc.load_yaml("a:\nb: 1\n"), {"a": None, "b": 1})            # empty scalar is null
        self.assertEqual(gc.load_yaml("x:\n  k:\n    - 1\ny:\n  k:\n    - 2\n"),
                         {"x": {"k": [1]}, "y": {"k": [2]}})                           # repeated container lines
        with self.assertRaises(ValueError):
            gc.load_yaml("a:\n\tb: 1\n")                                                # tabs
        self.assertEqual(gc.load_yaml("n: nan\ni: 1_000\nf: 1.5\n"), {"n": "nan", "i": "1_000", "f": 1.5})

    def test_threshold_kind_validation(self):
        gc = self.gc
        with self.assertRaises(ValueError):
            gc.resolve_threshold("prosody_tolerance", {"quality": {"prosody_tolerance": "fast"}}, None, kind=float)
        self.assertEqual(gc.resolve_threshold("hook_max_syllables", {"quality": {"hook_max_syllables": "9"}}, None, kind=int), 9)
        self.assertIs(gc.resolve_threshold("slant_rhyme_allowed", {}, None, kind=bool), True)
        self.assertEqual(gc.resolve_threshold("zz", {}, None, default=0), 0)           # default=0 is honoured


if __name__ == "__main__":
    unittest.main()
