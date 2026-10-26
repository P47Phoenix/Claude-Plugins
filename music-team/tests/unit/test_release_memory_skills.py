"""Structure tests for the music-release and music-memory skills (Wave 9)."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
SHARED = PLUGIN / "references" / "shared"
SKILLS = {
    "music-release": {"contract": "package-output", "budget": 200,
                      "needles": ["midi_export.py", "--out package/song.mid", "--structure", "lyric-sheet.md",
                                  "release-notes.md", "lead-sheet.abc", "one-pager.md", "new-sections.md",
                                  "NOT RELEASABLE", "SKILL_LOADED:"]},
    "music-memory": {"contract": "retrospective-output", "budget": 200,
                     "needles": ["retrospective.md", "run_id", "index.md", "stage-or-role | genre | lesson",
                                 "<!-- memory-lessons -->", "never lyric text", "Dedupe", "SKILL_LOADED:"]},
}
EXPECTED = {
    "license": "Apache License 2.0 - See repository LICENSE file",
    "model_awareness": "opus-4-7",
    "last_audited": "2026-10-26",
    "pattern_library_version": "4-7-1",
    "model": "sonnet",
    "tier": "C",
    "maintainer": "music-team-leads",
    "fitness_review_due": "2027-01-24",
    "context_budget": "200",
    "allowed-tools": "[Read, Write, Edit, Bash, Agent, Skill]",
}


def frontmatter(path: Path) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def blocked_hits(text: str) -> list[str]:
    lines = (SHARED / "blocked-targets.txt").read_text(encoding="utf-8").splitlines()
    text = text.replace("<!-- memory-lessons -->", "")
    hits = []
    for t in (l.strip() for l in lines if l.strip() and not l.lstrip().startswith("#")):
        pat = r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])"
        if re.search(pat, text, 0 if " " not in t else re.I):
            hits.append(t)
    return hits


class ReleaseMemorySkillTests(unittest.TestCase):
    def test_frontmatter_and_budget(self):
        for name, spec in SKILLS.items():
            path = PLUGIN / "skills" / name / "SKILL.md"
            fm = frontmatter(path)
            self.assertEqual(fm.get("name"), name)
            for key, want in EXPECTED.items():
                self.assertEqual(fm.get(key), want, f"{name}: {key}")
            self.assertNotIn("phase_1_detector_model", fm, name)
            self.assertGreater(len(fm.get("description", "")), 80)
            n = len(path.read_text(encoding="utf-8").splitlines())
            self.assertLessEqual(n, spec["budget"], f"{name}: {n} lines")
            self.assertNotIn("scaffold", path.read_text(encoding="utf-8"), f"{name}: stub text remains")

    def test_required_content(self):
        for name, spec in SKILLS.items():
            text = (PLUGIN / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            for needle in spec["needles"]:
                self.assertIn(needle, text, f"{name}: {needle}")
            self.assertIn("## User Commands", text)

    def test_triggers(self):
        rel = frontmatter(PLUGIN / "skills/music-release/SKILL.md")["description"]
        for phrase in ["export the song", "song package", "lead sheet"]:
            self.assertIn(phrase, rel)
        mem = frontmatter(PLUGIN / "skills/music-memory/SKILL.md")["description"]
        for phrase in ["song retrospective", "what did we learn"]:
            self.assertIn(phrase, mem)

    def test_contracts(self):
        for name, spec in SKILLS.items():
            path = PLUGIN / "skills" / name / "references" / "contracts" / f"{spec['contract']}.md"
            fm = frontmatter(path)
            self.assertEqual(fm.get("loaded_by"), name)
            self.assertEqual(fm.get("level"), "L2")
            self.assertIn("last_reviewed", fm)
            self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 150)

    def test_release_contract_matches_midi_cli(self):
        text = (PLUGIN / "skills/music-release/SKILL.md").read_text(encoding="utf-8")
        stage = (PLUGIN / "skills/music-flow/references/stages/07-release.md").read_text(encoding="utf-8")
        for flag in ["--out", "--chords", "--melody", "--structure", "--check"]:
            self.assertIn(flag, text)
        self.assertIn("midi_export.py --out {dir}/package/song.mid", stage)
        contract = (PLUGIN / "skills/music-release/references/contracts/package-output.md").read_text(encoding="utf-8")
        for needle in ["gates passed".split()[0], "Overrides", "Panel", "Loops used", "lyric-sheet.md", "Hook:"]:
            self.assertIn(needle, contract)

    def test_memory_contract_front_matter_and_lines(self):
        text = (PLUGIN / "skills/music-memory/references/contracts/retrospective-output.md").read_text(encoding="utf-8")
        for needle in ["run_id", "slug", "genre", "song_type", "date", "Never contains lyric text",
                       "stage-or-role | genre | lesson", "Dedupe", "200 lines"]:
            self.assertIn(needle, text)
        flow = (PLUGIN / "skills/music-flow/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("<stage-or-role> | <genre or *> | <lesson>", flow)

    def test_no_blocked_targets_or_model_ids(self):
        for name in SKILLS:
            for path in (PLUGIN / "skills" / name).rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("claude-", text, path.name)
                self.assertEqual(blocked_hits(text), [], str(path.relative_to(PLUGIN)))


class FlowTheoryAnswerTests(unittest.TestCase):
    def test_theory_answer_relay_documented(self):
        flow = PLUGIN / "skills/music-flow"
        dispatch = (flow / "references/dispatch-templates.md").read_text(encoding="utf-8")
        self.assertIn("ANSWER:", dispatch)
        self.assertLessEqual(len(dispatch.splitlines()), 150)
        skill = (flow / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("ANSWER:", skill)
        self.assertLessEqual(len(skill.splitlines()), 500)
        self.assertIn("ANSWER:", (flow / "references/stages/01-brief.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
