"""Tests for hooks/gate_check.py. Run: python bible-research/tests/test_gate_check.py"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "gate_check.py"


def run(mode: str, payload) -> dict | None:
    # Send real UTF-8 bytes, as Claude Code does. text=True would encode with the
    # console code page on Windows and hide decoding bugs in the hook.
    stdin = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    proc = subprocess.run(
        [sys.executable, str(HOOK), mode], input=stdin.encode("utf-8"), capture_output=True
    )
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    out = proc.stdout.decode("utf-8", "replace")
    return json.loads(out) if out.strip() else None


def msg(text: str, **extra) -> dict:
    return {"last_assistant_message": text, **extra}


NOTES = "\n\n**Verification notes:** All claims checked and verified against source - no corrections needed."


class StopHook(unittest.TestCase):
    def test_clean_shortlist_passes(self):
        self.assertIsNone(run("stop", msg("## 1. A\n**Why it fits:** x\nWhich one?" + NOTES)))

    def test_shortlist_without_notes_blocks(self):
        out = run("stop", msg("## 1. A\n**Why it fits:** x\nWhich one would you like?"))
        self.assertEqual(out["decision"], "block")

    def test_refusal_turn_is_not_blocked(self):
        self.assertIsNone(run("stop", msg("Task Type: breakdown | References: none | Scope: x\nWhich candidate would you like?")))

    def test_ordinary_reply_is_not_blocked(self):
        self.assertIsNone(run("stop", msg("Sure, here is the file.")))

    def test_breakdown_without_notes_blocks(self):
        out = run("stop", msg("## 1. Original Context\n..\n## 2. Original-Language Notes\n.."))
        self.assertEqual(out["decision"], "block")

    def test_clean_breakdown_passes(self):
        self.assertIsNone(run("stop", msg("## 1. Original Context\n..\n## 2. Original-Language Notes\n.." + NOTES)))

    def test_leaked_marker_blocks_even_with_notes(self):
        out = run("stop", msg("INTERNAL DRAFT\n**Why it fits:** x" + NOTES))
        self.assertEqual(out["decision"], "block")

    def test_repeat_block_guard(self):
        self.assertIsNone(run("stop", msg("**Why it fits:** x", stop_hook_active=True)))

    def test_bad_stdin_and_empty_message_pass(self):
        self.assertIsNone(run("stop", "not json"))
        self.assertIsNone(run("stop", {}))

    # research and idea-team contracts (0.2.0)
    TIMELINE = "# Timeline: The exile\n\n**Eras covered:** 7. **Translation:** ESV.\n\n| # | Event |\n|---|---|"
    SONGS = "# Song Ideas: Exodus and wilderness\n\n**Eras covered:** 3.\n\n1. **Event:** x"
    REVIEW = "# Idea Review: a sermon series on Ruth\n\n**Personas:** Skeptic, Lay Listener, Pastor.\n\n## Consensus\n- x"
    FINDINGS = "# Research Findings: hesed\n\n**Question shape:** descriptive. **Translation:** ESV.\n\n## Summary\nx"

    def test_timeline_without_notes_blocks(self):
        self.assertEqual(run("stop", msg(self.TIMELINE))["decision"], "block")

    def test_clean_timeline_passes(self):
        self.assertIsNone(run("stop", msg(self.TIMELINE + NOTES)))

    def test_song_ideas_without_notes_blocks(self):
        self.assertEqual(run("stop", msg(self.SONGS))["decision"], "block")

    def test_clean_song_ideas_passes(self):
        self.assertIsNone(run("stop", msg(self.SONGS + "\nWhich of these?" + NOTES)))

    def test_idea_review_without_notes_blocks(self):
        self.assertEqual(run("stop", msg(self.REVIEW))["decision"], "block")

    def test_clean_idea_review_passes(self):
        self.assertIsNone(run("stop", msg(self.REVIEW + NOTES)))

    def test_findings_without_notes_blocks(self):
        self.assertEqual(run("stop", msg(self.FINDINGS))["decision"], "block")

    def test_clean_findings_passes(self):
        self.assertIsNone(run("stop", msg(self.FINDINGS + NOTES)))

    def test_leaked_marker_in_research_blocks_even_with_notes(self):
        out = run("stop", msg("INTERNAL DRAFT - NOT FOR THE USER\n" + self.TIMELINE + NOTES))
        self.assertEqual(out["decision"], "block")

    def test_heading_variants_are_gated(self):
        for head in ("# Song ideas - Exodus", "# Biblical Timeline: Exile", "# TIMELINE – Judges"):
            text = head + "\n\n**Eras covered:** 3.\n\n| # |"
            self.assertEqual(run("stop", msg(text))["decision"], "block", head)

    def test_em_dash_heading_and_reformatted_marker_are_gated(self):
        text = "# Timeline \u2014 Judges\n\n**Eras covered**: 4.\n\n| # |"
        self.assertEqual(run("stop", msg(text))["decision"], "block")

    def test_fenced_example_is_not_gated(self):
        text = "The contract looks like this:\n```markdown\n# Timeline: [ERA]\n**Eras covered:** [N]\n```\nWhich era?"
        self.assertIsNone(run("stop", msg(text)))

    def test_marker_without_heading_or_heading_without_marker_pass(self):
        self.assertIsNone(run("stop", msg("**Eras covered:** 3. Nothing else here.")))
        self.assertIsNone(run("stop", msg("# Timeline: Exile\n\nno header line")))

    def test_notes_far_from_the_end_still_block(self):
        text = self.TIMELINE + NOTES + "\n" + ("filler line\n" * 400)
        self.assertEqual(run("stop", msg(text))["decision"], "block")

    def test_utf8_payload_with_hebrew_and_en_dash_is_gated(self):
        text = "# Timeline – Judah alone\n\n**Eras covered:** 7. חסד glossed.\n\n| # |"
        self.assertEqual(run("stop", msg(text))["decision"], "block")

    def test_idea_review_and_findings_without_marker_pass(self):
        self.assertIsNone(run("stop", msg("# Idea Review: Ruth\n\n## Consensus\n- x")))
        self.assertIsNone(run("stop", msg("# Research Findings: hesed\n\n## Summary\nx")))

    def test_long_output_with_notes_then_next_line_passes(self):
        text = self.SONGS + ("\n1. **Event:** x" * 300) + NOTES + "\n\n`next` for eras 4-6"
        self.assertIsNone(run("stop", msg(text)))

    def test_repeat_block_guard_on_new_contract(self):
        self.assertIsNone(run("stop", msg(self.REVIEW, stop_hook_active=True)))

    def test_heading_does_not_match_across_lines(self):
        self.assertIsNone(run("stop", msg("# Notes\n\nTimeline: next week\n**Eras covered:** none")))

    def test_project_plan_timeline_is_not_gated(self):
        # Another plugin's output with the same heading but no contract header line.
        self.assertIsNone(run("stop", msg("# Timeline: Q3 rollout\n\n- Week 1: kickoff\n- Week 2: build")))
        self.assertIsNone(run("stop", msg("# Song Ideas: for the album\n\n1. a ballad about rain")))

    def test_era_pick_list_is_not_blocked(self):
        text = "Task Type: song-ideas | References: none | Scope: era not chosen\nWhich era would you like?\n1. Primeval history\n2. The patriarchs"
        self.assertIsNone(run("stop", msg(text)))

    def test_talk_turn_is_not_blocked(self):
        self.assertIsNone(run("stop", msg("**Skeptic:** Where is the source for that? (my view)\n\n*Ask a follow-up or say `summary`.*")))

    def test_heading_must_be_top_level(self):
        # A mention of a timeline in prose, or a lower-level heading, is not gated output.
        self.assertIsNone(run("stop", msg("I can build a timeline: say which era.\n## Timeline: not a contract")))


class VerifierHook(unittest.TestCase):
    def test_clean_output_passes(self):
        self.assertIsNone(run("verifier", msg("corrected text" + NOTES)))

    def test_missing_notes_blocks(self):
        self.assertEqual(run("verifier", msg("corrected text only"))["decision"], "block")

    def test_draft_marker_blocks(self):
        self.assertEqual(run("verifier", msg("INTERNAL DRAFT - NOT FOR THE USER\nx" + NOTES))["decision"], "block")

    def test_report_leak_blocks(self):
        self.assertEqual(run("verifier", msg("# Citation Checklist\n.." + NOTES))["decision"], "block")

    def test_repeat_block_guard(self):
        self.assertIsNone(run("verifier", msg("no notes", stop_hook_active=True)))


if __name__ == "__main__":
    unittest.main()
