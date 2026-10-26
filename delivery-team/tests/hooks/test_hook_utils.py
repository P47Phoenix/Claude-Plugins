"""Tests for delivery-team/hooks/lib/hook_utils.py and hook importability.

Run:  python -I -m unittest discover delivery-team/tests/hooks
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

HOOKS_DIR = Path(__file__).resolve().parents[2] / "hooks"
sys.path.insert(0, str(HOOKS_DIR))

from lib import hook_utils as hu  # noqa: E402

HOOKS_USING_LIB = [
    "audit_agent_prompt.py",
    "check_config.py",
    "enforce_pipeline_scope.py",
    "flag_empirical_validation.py",
    "validate_gdscript.py",
    "verify_skill_load.py",
]


def _run_hook(name: str, payload: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-I", str(HOOKS_DIR / name)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(HOOKS_DIR.parent.parent),
    )


class ReadInputTests(unittest.TestCase):
    def _read(self, text: str) -> dict:
        sys.stdin = io.StringIO(text)
        try:
            return hu.read_hook_input()
        finally:
            sys.stdin = sys.__stdin__

    def test_parses_json(self):
        data = self._read('{"hook_event_name": "PreToolUse", "tool_name": "Agent"}')
        self.assertEqual(hu.get_tool_name(data), "Agent")

    def test_malformed_returns_empty(self):
        self.assertEqual(self._read("not json"), {})
        self.assertEqual(self._read(""), {})

    def test_accessors_tolerate_missing(self):
        self.assertEqual(hu.get_tool_name({}), "")
        self.assertEqual(hu.get_tool_input({}), {})
        self.assertEqual(hu.get_tool_result({}), "")
        self.assertIsNone(hu.get_transcript_path({}))
        self.assertEqual(hu.get_cwd({}), Path(os.getcwd()))

    def test_tool_result_flattens_dict_and_list(self):
        self.assertEqual(hu.get_tool_result({"tool_response": "plain"}), "plain")
        self.assertEqual(
            hu.get_tool_result({"tool_response": {"content": [{"type": "text", "text": "a"}, {"type": "text", "text": "b"}]}}),
            "a\nb",
        )
        self.assertEqual(hu.get_tool_result({"tool_result": "legacy"}), "legacy")


class EmitTests(unittest.TestCase):
    def test_emit_response_shape(self):
        sys.stdin = io.StringIO('{"hook_event_name": "PostToolUse"}')
        try:
            hu.read_hook_input()
        finally:
            sys.stdin = sys.__stdin__
        out = io.StringIO()
        with redirect_stdout(out):
            hu.emit_response(message="hello", continue_=True)
        payload = json.loads(out.getvalue())
        self.assertTrue(payload["continue"])
        self.assertEqual(payload["systemMessage"], "hello")
        self.assertEqual(payload["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        self.assertEqual(payload["hookSpecificOutput"]["additionalContext"], "hello")

    def test_exit_codes(self):
        with self.assertRaises(SystemExit) as cm:
            hu.exit_success()
        self.assertEqual(cm.exception.code, 0)
        err = io.StringIO()
        with redirect_stderr(err), self.assertRaises(SystemExit) as cm:
            hu.exit_block("nope")
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(err.getvalue(), "nope")

    def test_exit_block_non_ascii_does_not_raise(self):
        proc = subprocess.run(
            [sys.executable, "-I", "-X", "utf8=0", "-c",
             "import sys; sys.path.insert(0, sys.argv[1]); from lib.hook_utils import exit_block; exit_block('path \\u2192 caf\\u00e9 \\u4e2d')",
             str(HOOKS_DIR)],
            input=b"", capture_output=True, timeout=30,
            env={**os.environ, "PYTHONIOENCODING": "cp1252"},
        )
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertNotIn(b"Traceback", proc.stderr)

    def test_stop_event_has_no_hook_specific_output(self):
        sys.stdin = io.StringIO('{"hook_event_name": "SubagentStop"}')
        try:
            hu.read_hook_input()
        finally:
            sys.stdin = sys.__stdin__
        out = io.StringIO()
        with redirect_stdout(out):
            hu.emit_response(message="m")
        payload = json.loads(out.getvalue())
        self.assertNotIn("hookSpecificOutput", payload)
        self.assertEqual(payload["systemMessage"], "m")


class HookImportSmokeTests(unittest.TestCase):
    """Every hook that imports lib.hook_utils must start and exit 0 on a benign payload."""

    def test_hooks_import_and_allow(self):
        benign = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "README.md"},
            "cwd": str(HOOKS_DIR.parent.parent),
        }
        for name in HOOKS_USING_LIB:
            with self.subTest(hook=name):
                proc = _run_hook(name, benign)
                self.assertEqual(
                    proc.returncode, 0,
                    f"{name} exited {proc.returncode}\nstderr:\n{proc.stderr}",
                )
                self.assertNotIn("ModuleNotFoundError", proc.stderr)

    def test_hooks_survive_empty_stdin(self):
        for name in HOOKS_USING_LIB:
            with self.subTest(hook=name):
                proc = subprocess.run(
                    [sys.executable, "-I", str(HOOKS_DIR / name)],
                    input="", capture_output=True, text=True, timeout=30,
                    cwd=str(HOOKS_DIR.parent.parent),
                )
                self.assertEqual(proc.returncode, 0, f"{name}\n{proc.stderr}")


if __name__ == "__main__":
    unittest.main()
