"""Tests for hooks/gate_check.py. Run: python bible-research/tests/test_gate_check.py"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "gate_check.py"


def run(mode: str, payload) -> dict | None:
    stdin = payload if isinstance(payload, str) else json.dumps(payload)
    proc = subprocess.run(
        [sys.executable, str(HOOK), mode], input=stdin, capture_output=True, text=True
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout) if proc.stdout.strip() else None


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
