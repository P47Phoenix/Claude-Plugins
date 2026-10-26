"""Dry-run tests for the music-team hooks (Wave 9): hooks.json shape and each hook script."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
HOOKS = PLUGIN / "hooks"
SHARED = PLUGIN / "references" / "shared"
FIXTURES = PLUGIN / "tests" / "fixtures"


def clause() -> str:
    text = (SHARED / "originality-policy.md").read_text(encoding="utf-8")
    return re.search(r"```text\n(ORIGINALITY POLICY.*?)```", text, re.S).group(1).strip()


def build_prompt(role="verse-writer", skill="lyricist", loaded=None, extra="", policy=True, summary_block=True):
    loaded = loaded or ("skills/lyricist/references/roles/verse-writer.md, "
                        "skills/lyricist/references/contracts/lyrics-output.md, "
                        "references/shared/genres/folk.md, "
                        "skills/lyricist/references/techniques/rhyme-schemes.md")
    parts = [f"SKILL: {skill}", "TASK_TYPE: section-lyrics", f"ROLE: {role}", "",
             f'Begin your response with "SKILL_LOADED: {loaded}".', "",
             'You are the verse-writer for music-team, working on "Test Song" (folk, FULL_SONG).', ""]
    if policy:
        parts += ["<!-- originality-policy -->", clause(), ""]
    parts += [extra, "<!-- memory-lessons -->", "No lessons recorded."]
    return "\n".join(parts)


def run_hook(script: str, payload, args=None, cwd=None, raw=None):
    stdin = raw if raw is not None else json.dumps(payload)
    return subprocess.run([sys.executable, "-I", str(HOOKS / script), *(args or [])], input=stdin,
                          capture_output=True, text=True, cwd=cwd, timeout=60)


def agent_event(prompt, event="PreToolUse", response=None, subagent="lyricist"):
    ev = {"hook_event_name": event, "tool_name": "Agent",
          "tool_input": {"description": "d", "subagent_type": subagent, "prompt": prompt}}
    if response is not None:
        ev["tool_response"] = response
    return ev


class HooksJsonTests(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads((HOOKS / "hooks.json").read_text(encoding="utf-8"))

    def test_wrapper_format(self):
        self.assertIsInstance(self.cfg.get("description"), str)
        self.assertIsInstance(self.cfg.get("hooks"), dict)
        self.assertEqual(set(self.cfg["hooks"]), {"PreToolUse", "PostToolUse", "SubagentStop"})

    def test_every_script_exists_with_timeout(self):
        count = 0
        for groups in self.cfg["hooks"].values():
            for group in groups:
                self.assertIn("matcher", group)
                for hook in group["hooks"]:
                    self.assertEqual(hook["type"], "command")
                    self.assertIsInstance(hook["timeout"], int)
                    m = re.match(r"python3 \$\{CLAUDE_PLUGIN_ROOT\}/hooks/([A-Za-z0-9_]+\.py)", hook["command"])
                    self.assertIsNotNone(m, hook["command"])
                    self.assertTrue((HOOKS / m.group(1)).is_file(), m.group(1))
                    count += 1
        self.assertEqual(count, 7)

    def test_matchers(self):
        h = self.cfg["hooks"]
        self.assertEqual(h["PreToolUse"][0]["matcher"], "Agent")
        self.assertIn("audit_agent_prompt.py", h["PreToolUse"][0]["hooks"][0]["command"])
        self.assertEqual(h["PostToolUse"][0]["matcher"], "Agent")
        self.assertIn("verify_skill_loaded.py", h["PostToolUse"][0]["hooks"][0]["command"])
        stops = {g["matcher"]: g["hooks"][0]["command"] for g in h["SubagentStop"]}
        self.assertEqual(set(stops), {"lyricist", "composer", "arranger", "song-critic", "adapter"})
        for agent, cmd in stops.items():
            self.assertTrue(cmd.endswith(f"subagent_gate.py --agent {agent}"), cmd)


class AuditAgentPromptTests(unittest.TestCase):
    def audit(self, prompt, subagent="lyricist"):
        return run_hook("audit_agent_prompt.py", agent_event(prompt, subagent=subagent))

    def test_non_music_prompt_silent(self):
        r = run_hook("audit_agent_prompt.py", {"tool_name": "Agent", "tool_input": {
            "subagent_type": "general-purpose", "prompt": "SKILL: developer\nROLE: python\nwrite a script for Taylor Swift fans"}})
        self.assertEqual((r.returncode, r.stdout, r.stderr), (0, "", ""))

    def test_good_prompt_allowed(self):
        r = self.audit(build_prompt())
        self.assertEqual((r.returncode, r.stdout), (0, ""), r.stderr)

    def test_missing_originality_block_denied(self):
        r = self.audit(build_prompt(policy=False))
        self.assertEqual(r.returncode, 2)
        out = json.loads(r.stdout)["hookSpecificOutput"]
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertEqual(out["hookEventName"], "PreToolUse")
        self.assertIn("originality-policy", out["permissionDecisionReason"])
        self.assertIn("originality-policy", r.stderr)

    def test_blocked_targets(self):
        r = self.audit(build_prompt(extra="Make the hook feel like taylor swift."))
        self.assertEqual(r.returncode, 2)
        self.assertIn("blocked", json.loads(r.stdout)["hookSpecificOutput"]["permissionDecisionReason"])

    def test_single_word_entries_are_case_sensitive(self):
        self.assertEqual(self.audit(build_prompt(extra="Keep the queen of hearts image.")).returncode, 0)
        self.assertEqual(self.audit(build_prompt(extra="A bit like Queen here.")).returncode, 2)

    def test_memory_marker_is_not_a_blocked_hit(self):
        prompt = build_prompt()
        self.assertIn("<!-- memory-lessons -->", prompt)
        self.assertEqual(self.audit(prompt).returncode, 0)
        self.assertEqual(self.audit(build_prompt(extra="Write it as a Memory.")).returncode, 2)

    def test_over_allowance_denied(self):
        loaded = ("skills/lyricist/references/roles/verse-writer.md, references/shared/genres/folk.md, "
                  "skills/lyricist/references/techniques/rhyme-schemes.md, "
                  "skills/lyricist/references/techniques/hook-craft.md, "
                  "skills/lyricist/references/techniques/section-roles.md")
        r = self.audit(build_prompt(loaded=loaded))
        self.assertEqual(r.returncode, 2)
        self.assertIn("techniques", json.loads(r.stdout)["hookSpecificOutput"]["permissionDecisionReason"])

    def test_per_role_allowances(self):
        two_genres = ("skills/adapter/references/roles/lyric-adapter.md, references/shared/genres/folk.md, "
                      "references/shared/genres/pop.md")
        self.assertEqual(self.audit(build_prompt(role="lyric-adapter", skill="adapter", loaded=two_genres),
                                    subagent="adapter").returncode, 0)
        self.assertEqual(self.audit(build_prompt(role="verse-writer", loaded=two_genres)).returncode, 2)
        three_tech = ", ".join(f"skills/composer/references/techniques/t{i}.md" for i in range(3))
        self.assertEqual(self.audit(build_prompt(role="theorist", skill="composer", loaded=three_tech),
                                    subagent="composer").returncode, 0)

    def test_challenger_may_paste_the_blocked_list(self):
        listing = (SHARED / "blocked-targets.txt").read_text(encoding="utf-8")
        prompt = build_prompt(role="challenger", skill="song-critic", extra=listing,
                              loaded="skills/song-critic/references/roles/challenger.md, "
                                     "references/shared/blocked-targets.txt")
        r = self.audit(prompt, subagent="song-critic")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_malformed_stdin_exits_zero(self):
        for raw in ["{not json", "", "[1,2]"]:
            r = run_hook("audit_agent_prompt.py", None, raw=raw)
            self.assertEqual(r.returncode, 0, raw)
            self.assertEqual(r.stdout, "")


class VerifySkillLoadedTests(unittest.TestCase):
    GOOD = ("SKILL_LOADED: skills/lyricist/references/roles/verse-writer.md\nSTATUS: DONE\n"
            "ARTIFACT: .song/x/lyrics.md\nSUMMARY: Wrote two verses and a chorus.")

    def verify(self, text, prompt=None):
        return run_hook("verify_skill_loaded.py", agent_event(prompt or build_prompt(), "PostToolUse", response=text))

    def test_non_music_silent(self):
        ev = {"tool_name": "Agent", "tool_input": {"subagent_type": "general-purpose", "prompt": "hello"},
              "tool_response": "no markers at all"}
        r = run_hook("verify_skill_loaded.py", ev)
        self.assertEqual((r.returncode, r.stdout), (0, ""))

    def test_good_reply_silent(self):
        r = self.verify(self.GOOD)
        self.assertEqual((r.returncode, r.stdout), (0, ""))

    def test_content_list_response_is_read(self):
        r = self.verify({"content": [{"type": "text", "text": self.GOOD}]})
        self.assertEqual(r.stdout, "")

    def test_missing_skill_loaded_warns(self):
        r = self.verify(self.GOOD.replace("SKILL_LOADED:", "NOTE:"))
        self.assertEqual(r.returncode, 0)
        self.assertIn("SKILL_LOADED", json.loads(r.stdout)["systemMessage"])

    def test_missing_block_warns(self):
        r = self.verify("SKILL_LOADED: a.md\nI wrote the thing.")
        msg = json.loads(r.stdout)["systemMessage"]
        self.assertIn("STATUS", msg)
        self.assertIn("SUMMARY", msg)

    def test_long_summary_warns(self):
        r = self.verify(self.GOOD.replace("Wrote two verses and a chorus.", "x" * 201))
        self.assertIn("201 characters", json.loads(r.stdout)["systemMessage"])

    def test_theory_answer_block_is_fine(self):
        text = "SKILL_LOADED: a.md\nSTATUS: DONE\nARTIFACT: none\nSUMMARY: D mixolydian.\nANSWER:\n" + "x" * 500
        self.assertEqual(self.verify(text).stdout, "")

    def test_malformed_stdin_exits_zero(self):
        r = run_hook("verify_skill_loaded.py", None, raw="{oops")
        self.assertEqual((r.returncode, r.stdout), (0, ""))


class SubagentGateTests(unittest.TestCase):
    def test_no_active_run_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run_hook("subagent_gate.py", {"hook_event_name": "SubagentStop", "cwd": tmp},
                         args=["--agent", "lyricist"], cwd=tmp)
        self.assertEqual(r.returncode, 0)
        msg = json.loads(r.stdout)["systemMessage"]
        self.assertIn("SKIPPED", msg)
        self.assertIn("lyricist", msg)

    def test_active_run_reports_gate_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / ".song" / "demo"
            run.mkdir(parents=True)
            (Path(tmp) / ".song" / "active").write_text("demo\n", encoding="utf-8")
            shutil.copy(FIXTURES / "negative" / "challenge-blocker" / "challenge-report.md", run)
            r = run_hook("subagent_gate.py", {"cwd": tmp}, args=["--agent", "song-critic"], cwd=tmp)
        self.assertEqual(r.returncode, 0)
        msg = json.loads(r.stdout)["systemMessage"]
        self.assertIn("challenge_gate FAIL", msg)

    def test_no_artifact_yet_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".song" / "demo").mkdir(parents=True)
            (Path(tmp) / ".song" / "active").write_text("demo\n", encoding="utf-8")
            r = run_hook("subagent_gate.py", {"cwd": tmp}, args=["--agent", "adapter"], cwd=tmp)
        self.assertIn("SKIPPED", json.loads(r.stdout)["systemMessage"])

    def test_malformed_stdin_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run_hook("subagent_gate.py", None, args=["--agent", "composer"], cwd=tmp, raw="{{")
        self.assertEqual(r.returncode, 0)

    def test_unknown_agent_is_silent(self):
        r = run_hook("subagent_gate.py", {}, args=["--agent", "something-else"])
        self.assertEqual((r.returncode, r.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
