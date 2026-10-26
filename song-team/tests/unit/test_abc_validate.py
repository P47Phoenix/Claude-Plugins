"""Unit tests for song-team/scripts/abc_validate.py and abc_common.py (W3-1)."""
from __future__ import annotations

import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # noqa: E402
from _helpers import FIXTURES, load_script, mixed_path

FULL = FIXTURES / "songs" / "FULL_SONG"
NEG = FIXTURES / "negative"


class AbcValidateTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_script("abc_validate")
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, *argv: str) -> tuple[int, dict]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = self.mod.main(["--json", *argv])
        return code, json.loads(buf.getvalue())

    def _copy_full(self, **edits: str) -> dict[str, str]:
        """Copy the FULL_SONG set into tmp; ``edits`` maps file name to replacement text."""
        out = {}
        for name in ("melody.abc", "structure.md", "lyrics.md", "brief.md"):
            dst = self.root / name
            text = edits[name] if name in edits else (FULL / name).read_text(encoding="utf-8")
            dst.write_text(text, encoding="utf-8", newline="\n")
            out[name] = str(dst)
        return out

    def _melody(self, **repl: str) -> str:
        text = (FULL / "melody.abc").read_text(encoding="utf-8")
        for old, new in repl.items():
            self.assertIn(old, text)
            text = text.replace(old, new)
        return text

    # ---- fixtures -------------------------------------------------------
    def test_full_song_passes_with_melisma_and_skip(self):
        code, out = self._run(str(FULL / "melody.abc"), str(FULL / "structure.md"), str(FULL / "lyrics.md"),
                              str(FULL / "brief.md"))
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["violations"], [])
        m = out["metrics"]
        self.assertEqual((m["bars"], m["aligned_bars"], m["alignment_skipped"]), (56, 56, 0))
        self.assertEqual((m["min_pitch"], m["max_pitch"]), (62, 74))
        self.assertLessEqual(m["max_leap"], 12)
        self.assertEqual(out["thresholds"], {"max_melodic_leap": 12, "vocal_range": [55, 79]})

    def test_w_mismatch_fails_at_verse_1_bar_1(self):
        d = NEG / "w-mismatch"
        code, out = self._run(str(d / "melody.abc"), str(d / "lyrics.md"), str(d / "structure.md"))
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        v = out["violations"][0]
        self.assertEqual((v["location"], v["observed"], v["limit"]), ("Verse 1:1", 3, 4))

    def test_malformed_abc_errors(self):
        d = NEG / "malformed-abc"
        code, out = self._run(str(d / "melody.abc"), str(d / "structure.md"))
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertIn("parse error", out["violations"][0]["reason"])
        self.assertEqual(out["violations"][0]["location"], "melody.abc:1")

    # ---- alignment skipping ---------------------------------------------
    def test_alignment_skipped_for_instrumental(self):
        brief = (FULL / "brief.md").read_text(encoding="utf-8").replace("song_type: FULL_SONG", "song_type: INSTRUMENTAL")
        melody = "\n".join(l for l in self._melody().splitlines() if not l.startswith("w:")) + "\n"
        f = self._copy_full(**{"brief.md": brief, "melody.abc": melody})
        code, out = self._run(f["melody.abc"], f["structure.md"], f["lyrics.md"], f["brief.md"])
        self.assertEqual(out["status"], "PASS", out)
        self.assertEqual(out["metrics"]["alignment_skipped"], 1)

    def test_alignment_skipped_without_lyrics(self):
        f = self._copy_full(**{"melody.abc": self._melody(**{"w: I count the num-bers | on the street |": "w: wrong |"})})
        code, out = self._run(f["melody.abc"], f["structure.md"])
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"]["alignment_skipped"], 1)
        code, out = self._run(f["melody.abc"], f["structure.md"], f["lyrics.md"])
        self.assertEqual(out["status"], "FAIL")

    def test_text_mismatch_fails_even_when_counts_match(self):
        f = self._copy_full(**{"melody.abc": self._melody(**{"w: I count the num-bers | on the street |":
                                                             "w: I count the num-bers | on the beach |"})})
        code, out = self._run(f["melody.abc"], f["structure.md"], f["lyrics.md"])
        self.assertEqual(out["status"], "FAIL")
        v = out["violations"][0]
        self.assertEqual(v["location"], "Verse 1:1")
        self.assertIn("differs from lyrics.md", v["reason"])

    # ---- pitch rules ------------------------------------------------------
    def test_fail_leap_over_threshold(self):
        f = self._copy_full(**{"melody.abc": self._melody(**{"D2 E2 F2 GA | B2 A2 F4 |\nw: I count": "D2 E2 F2 Ga | B2 A2 F4 |\nw: I count"})})
        code, out = self._run(f["melody.abc"], f["structure.md"])
        self.assertEqual(out["status"], "FAIL")
        v = [v for v in out["violations"] if "leap" in v["reason"]][0]
        self.assertEqual((v["location"], v["observed"], v["limit"]), ("Verse 1:1", 14, 12))
        self.assertEqual(out["metrics"]["max_leap"], 14)

    def test_fail_pitch_outside_range(self):
        f = self._copy_full(**{"melody.abc": self._melody(**{"B2 A2 F4 |\nw: I count": "B2 A2 F,4 |\nw: I count"})})
        code, out = self._run(f["melody.abc"], f["structure.md"])
        self.assertEqual(out["status"], "FAIL")
        v = [v for v in out["violations"] if "vocal_range" in v["reason"]][0]
        self.assertEqual((v["location"], v["observed"], v["limit"]), ("Verse 1:2", 54, [55, 79]))  # F, in D major = F#3
        self.assertEqual(out["metrics"]["min_pitch"], 54)

    def test_leap_boundary_twelve_passes_thirteen_fails(self):
        # G (67) -> g (79) is exactly 12 semitones: PASS at the default 12
        f = self._copy_full(**{"melody.abc": self._melody(**{"D2 E2 F2 GA | B2 A2 F4 |\nw: I count": "D2 E2 F2 Gg | B2 A2 F4 |\nw: I count"})})
        code, out = self._run(f["melody.abc"], f["structure.md"], f["lyrics.md"])
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"]["max_leap"], 12)
        # F# (66) -> g (79) is 13: FAIL
        f = self._copy_full(**{"melody.abc": self._melody(**{"D2 E2 F2 GA | B2 A2 F4 |\nw: I count": "D2 E2 F2 Fg | B2 A2 F4 |\nw: I count"})})
        code, out = self._run(f["melody.abc"], f["structure.md"], f["lyrics.md"])
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        v = [v for v in out["violations"] if "leap" in v["reason"]]
        self.assertEqual([(x["location"], x["observed"], x["limit"]) for x in v], [("Verse 1:1", 13, 12)])

    def test_vocal_range_boundaries_inclusive(self):
        # G, = 55 and g = 79 sit exactly on the default [55, 79]: PASS; ^F, = 54 and ^g = 80: FAIL
        for old, new, want_status, pitch in (("B2 A2 F4 |\nw: I count", "B2 A2 G,4 |\nw: I count", "PASS", 55),
                                            ("B2 A2 F4 |\nw: I count", "B2 A2 g4 |\nw: I count", "PASS", 79),
                                            ("B2 A2 F4 |\nw: I count", "B2 A2 ^F,4 |\nw: I count", "FAIL", 54),
                                            ("B2 A2 F4 |\nw: I count", "B2 A2 ^g4 |\nw: I count", "FAIL", 80)):
            f = self._copy_full(**{"melody.abc": self._melody(**{old: new})})
            code, out = self._run("--max-melodic-leap", "30", f["melody.abc"], f["structure.md"], f["lyrics.md"])
            self.assertEqual(out["status"], want_status, (pitch, out))
            v = [v for v in out["violations"] if "vocal_range" in v["reason"]]
            if want_status == "FAIL":
                self.assertEqual([(x["location"], x["observed"], x["limit"]) for x in v], [("Verse 1:2", pitch, [55, 79])])
            else:
                self.assertEqual(v, [])
                self.assertIn(pitch, (out["metrics"]["min_pitch"], out["metrics"]["max_pitch"]))

    def test_tilde_joins_words_end_to_end(self):
        # two heads, two tokens; 'on~the' compares as 'on the' against lyrics.md
        f = self._copy_full(**{"melody.abc": self._melody(**{"B2 A2 F4 |\nw: I count the num-bers | on the street |":
                                                             "B4 F4 |\nw: I count the num-bers | on~the street |"})})
        code, out = self._run(f["melody.abc"], f["structure.md"], f["lyrics.md"])
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"]["aligned_bars"], 56)

    def test_empty_section_with_lyrics_fails_text_differs(self):
        text = self._melody()
        start = text.index("%%section Bridge\n") + len("%%section Bridge\n")
        end = text.index("%%section Chorus", start)
        f = self._copy_full(**{"melody.abc": text[:start] + text[end:]})
        code, out = self._run(f["melody.abc"], f["structure.md"], f["lyrics.md"])
        self.assertEqual((code, out["status"]), (1, "FAIL"))
        v = [v for v in out["violations"] if v["location"].startswith("Bridge")]
        self.assertEqual(len(v), 1)
        self.assertEqual(v[0]["location"], "Bridge:1")
        self.assertIn("w: text differs from lyrics.md section text", v[0]["reason"])
        self.assertEqual(v[0]["observed"], "")

    def test_tie_across_line_end_is_one_head(self):
        # F4 at the end of bar 2 tied into the next line: the tied-into note takes no token
        f = self._copy_full(**{"melody.abc": self._melody(**{
            "D2 E2 F2 GA | B2 A2 F4 |\nw: I count the num-bers | on the street |\nD2 F2 D2 F2 | E2 G2 F2 E2 |\nw: A key, a map, | a bor-rowed town |":
            "D2 E2 F2 GA | B2 A2 F4- |\nw: I count the num-bers | on the street |\nF2 F2 D2 F2 | E2 G2 F2 E2 |\nw: A~key, a map, | a bor-rowed town |"})})
        code, out = self._run(f["melody.abc"], f["structure.md"], f["lyrics.md"])
        self.assertEqual((code, out["status"]), (0, "PASS"), out)
        self.assertEqual(out["metrics"]["aligned_bars"], 56)

    def test_slur_between_different_pitches_is_a_new_head(self):
        # B2- d2: the d is a new head (and takes a token) and is checked for the leap
        f = self._copy_full(**{"melody.abc": self._melody(**{"D2 E2 F2 GA | B2 A2 F4 |\nw: I count":
                                                             "D2 E2 F2 GA | B2- d2 F4 |\nw: I count"})})
        code, out = self._run("--max-melodic-leap", "2", f["melody.abc"], f["structure.md"], f["lyrics.md"])
        self.assertEqual(out["status"], "FAIL")
        leaps = [(v["location"], v["observed"]) for v in out["violations"] if "leap" in v["reason"]]
        self.assertIn(("Verse 1:2", 3), leaps)                       # B -> d is checked
        self.assertNotIn(("Verse 1:2", "w: tokens + extensions + skips differ from note heads"),
                         [(v["location"], v["reason"]) for v in out["violations"]])

    def test_missing_melody_error_wording(self):
        f = self._copy_full()
        code, out = self._run(f["structure.md"])
        self.assertEqual((code, out["status"]), (3, "ERROR"))
        self.assertEqual(out["violations"][0]["reason"], "no argument whose basename is melody.abc")

    # ---- header and section rules ----------------------------------------
    def test_fail_key_mismatch(self):
        f = self._copy_full(**{"melody.abc": self._melody(**{"K:D\n": "K:Em\n"})})
        code, out = self._run(f["melody.abc"], f["structure.md"])
        self.assertEqual(out["status"], "FAIL")
        v = [v for v in out["violations"] if v["location"] == "melody.abc:K"][0]
        self.assertEqual((v["observed"], v["limit"]), ("E minor", "D major"))

    def test_fail_time_sig_mismatch_and_missing_headers(self):
        f = self._copy_full(**{"melody.abc": self._melody(**{"M:4/4\n": "M:3/4\n", "Q:1/4=118\n": ""})})
        code, out = self._run(f["melody.abc"], f["structure.md"])
        self.assertEqual(out["status"], "FAIL")
        locs = {v["location"] for v in out["violations"]}
        self.assertEqual(locs, {"melody.abc:M", "melody.abc:Q"})

    def test_fail_two_voices(self):
        f = self._copy_full(**{"melody.abc": self._melody(**{"K:D\n": "K:D\nV:1\nV:2\n"})})
        code, out = self._run(f["melody.abc"], f["structure.md"])
        self.assertEqual(out["status"], "FAIL")
        self.assertIn("melody.abc:V", {v["location"] for v in out["violations"]})

    def test_fail_section_list_mismatch(self):
        f = self._copy_full(**{"melody.abc": self._melody(**{"%%section Bridge": "%%section Breakdown"})})
        code, out = self._run(f["melody.abc"], f["structure.md"])
        self.assertEqual(out["status"], "FAIL")
        v = [v for v in out["violations"] if v["location"] == "melody.abc:sections"][0]
        self.assertIn("Breakdown", v["observed"])
        self.assertIn("Bridge", v["limit"])

    # ---- thresholds, paths, help -----------------------------------------
    def test_threshold_precedence(self):
        cfg = self.root / "config.yml"
        cfg.write_text("quality:\n  max_melodic_leap: 5\n  vocal_range: [55, 79]\n  genre_overrides:\n"
                       "    pop:\n      max_melodic_leap: 7\n      vocal_range: [64, 70]\n", encoding="utf-8")
        f = self._copy_full()
        code, out = self._run("--config", str(cfg), f["melody.abc"], f["structure.md"])
        self.assertEqual(out["thresholds"]["max_melodic_leap"], 5)      # quality.<key>
        self.assertEqual(out["status"], "FAIL")
        code, out = self._run("--config", str(cfg), "--genre", "pop", f["melody.abc"], f["structure.md"])
        self.assertEqual(out["thresholds"], {"max_melodic_leap": 7, "vocal_range": [64, 70]})
        code, out = self._run("--config", str(cfg), f["melody.abc"], f["structure.md"], f["brief.md"])
        self.assertEqual(out["thresholds"]["max_melodic_leap"], 7)      # genre from brief.md
        code, out = self._run("--config", str(cfg), "--genre", "pop", "--max-melodic-leap", "12",
                              "--vocal-range", "55,79", f["melody.abc"], f["structure.md"])
        self.assertEqual(out["thresholds"], {"max_melodic_leap": 12, "vocal_range": [55, 79]})
        self.assertEqual(out["status"], "PASS", out)

    def test_error_bad_vocal_range(self):
        cfg = self.root / "config.yml"
        cfg.write_text("quality:\n  vocal_range: [79, 55]\n", encoding="utf-8")
        f = self._copy_full()
        code, out = self._run("--config", str(cfg), f["melody.abc"], f["structure.md"])
        self.assertEqual((code, out["status"]), (3, "ERROR"))

    def test_mixed_separator_windows_path(self):
        f = self._copy_full()
        code, out = self._run(mixed_path(f["melody.abc"]), mixed_path(f["structure.md"]), f["lyrics.md"])
        self.assertEqual(out["status"], "PASS", out)

    def test_missing_inputs_error(self):
        f = self._copy_full()
        code, out = self._run(f["structure.md"])
        self.assertEqual((code, out["status"]), (3, "ERROR"))

    def test_help_exits_zero(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as cm:
            self.mod.main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("--vocal-range", buf.getvalue())
        self.assertIn("--max-melodic-leap", buf.getvalue())


class AbcCommonTests(unittest.TestCase):
    def setUp(self):
        self.ac = load_script("abc_common")

    def test_w_tokens(self):
        groups = self.ac.parse_w_line("No-bo-dy knows | my name here yet_ | on the floor * | hel~lo")
        kinds = [[t["kind"] for t in g] for g in groups]
        self.assertEqual(kinds, [["syl"] * 4, ["syl"] * 4 + ["ext"], ["syl"] * 3 + ["skip"], ["syl"]])
        self.assertEqual(groups[3][0]["text"], "hel lo")

    def test_tie_is_one_head_and_accidentals_persist(self):
        p = self.ac.parse_abc("X:1\nT:t\nM:4/4\nL:1/8\nQ:1/4=100\nK:D\n%%section Verse 1\n^F2 F2 =F2 A2-A2 | F2 z2 |\n")
        bars = p["sections"][0]["bars"]
        self.assertEqual([n["midi"] for n in bars[0]["notes"]], [66, 66, 65, 69, 69])
        self.assertEqual(self.ac.note_heads(bars[0]), 4)
        self.assertEqual(bars[1]["notes"][0]["midi"], 66)          # key signature again after the bar
        self.assertTrue(bars[1]["notes"][1]["is_rest"])
        self.assertEqual(p["unit_length"], Fraction(1, 8))

    def test_durations_chords_and_ignored_syntax(self):
        p = self.ac.parse_abc('X:1\nT:t\nM:4/4\nL:1/8\nQ:1/4=100\nK:C\n"C"C2 !trill!{d}D/ E3/2 [K:C] F>G (3ABc z/ |]\n')
        bar = p["sections"][0]["bars"][0]
        durs = [n["dur_units"] for n in bar["notes"]]
        self.assertEqual(durs, [2, Fraction(1, 2), Fraction(3, 2), Fraction(3, 2), Fraction(1, 2),
                                Fraction(2, 3), Fraction(2, 3), Fraction(2, 3), Fraction(1, 2)])
        self.assertEqual(bar["chords"], ["C"])

    def test_parse_errors(self):
        for bad in ("X:1\nK:C\nC2 ]] D2 |\n", "X:1\nK:C\nw: no music yet\n", "X:1\nK:C\nC2 D2 |\nw: a b\nw: c d\n",
                    "X:1\nK:C\nC2 (3(3DEF G2 |\n",                       # nested tuplet
                    "X:1\nK:C\nC2 D2 |\nw: a b \\\nC2 D2 |\n"):          # w: continuation with no w: after
            with self.assertRaises(self.ac.AbcParseError, msg=bad):
                self.ac.parse_abc(bad)

    def test_tie_carries_across_line_end_and_merges(self):
        p = self.ac.parse_abc("X:1\nK:C\n%%section A\nC4 E4- |\nE4 G4 |\n")
        bars = p["sections"][0]["bars"]
        self.assertEqual([n["tied_from_prev"] for n in bars[1]["notes"]], [True, False])
        self.assertEqual(self.ac.note_heads(bars[1]), 1)

    def test_hyphen_between_different_pitches_is_a_slur(self):
        p = self.ac.parse_abc("X:1\nK:C\nB2- d2 | A2- z2 A2 |\n")
        b0, b1 = p["sections"][0]["bars"]
        self.assertEqual([n["tied_from_prev"] for n in b0["notes"]], [False, False])
        self.assertEqual(self.ac.note_heads(b0), 2)
        self.assertEqual([n["tied_from_prev"] for n in b1["notes"] if not n["is_rest"]], [False, False])
        self.assertEqual(self.ac.note_heads(b1), 2)                 # a rest breaks the tie

    def test_dangling_tie_is_error_with_line(self):
        with self.assertRaises(self.ac.AbcParseError) as cm:
            self.ac.parse_abc("X:1\nK:C\n%%section A\nC4 E4- |\n%%section B\nE4 G4 |\n")
        self.assertEqual(cm.exception.line, 4)
        with self.assertRaises(self.ac.AbcParseError) as cm:
            self.ac.parse_abc("X:1\nK:C\nC4 E4 |\nG4- |\n")
        self.assertEqual(cm.exception.line, 4)

    def test_w_continuation_tuplet_reset_and_bom(self):
        p = self.ac.parse_abc("﻿X:1\nK:C\n%%section A\nC2 D2 E2 F2 | (3GAB c2 (3cde |\nw: a b c \\\nw: d | e f g h i j k |\n")
        bars = p["sections"][0]["bars"]
        self.assertEqual(p["headers"]["X"], "1")
        self.assertEqual([t["text"] for t in bars[0]["w_tokens"]], ["a", "b", "c", "d"])
        self.assertEqual(len(bars[1]["w_tokens"]), 7)
        self.assertEqual([n["dur_units"] for n in bars[1]["notes"]],
                         [Fraction(2, 3)] * 3 + [2] + [Fraction(2, 3)] * 3)
        p = self.ac.parse_abc("X:1\nK:C\n(3CDE | F2 G2 A2 B2 |\n")  # tuplet state does not leak past the bar
        self.assertEqual([n["dur_units"] for n in p["sections"][0]["bars"][1]["notes"]], [2, 2, 2, 2])

    def test_key_helpers(self):
        self.assertEqual(self.ac.parse_abc_key("D dorian"), ("D", "dorian"))
        self.assertEqual(self.ac.key_accidentals("D", "minor"), {"B": -1})
        self.assertEqual(self.ac.abc_note_to_midi("c'", {}), 84)
        self.assertEqual(self.ac.parse_time_sig("C|"), (2, 2))
        self.assertEqual(self.ac.parse_tempo_bpm("1/4=118"), 118)
        self.assertEqual(self.ac.parse_tempo_beat("3/8=50"), Fraction(3, 8))
        self.assertEqual(self.ac.PC["G"], 7)
        self.assertEqual((self.ac.SHARP_NAMES[6], self.ac.FLAT_NAMES[6]), ("F#", "Gb"))


if __name__ == "__main__":
    unittest.main()
