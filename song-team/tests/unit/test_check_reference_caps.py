"""Unit tests for song-team/scripts/check_reference_caps.py (W0-3)."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN_ROOT = HERE.parent.parent
SCRIPT = PLUGIN_ROOT / "scripts" / "check_reference_caps.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_reference_caps", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


FM = "---\nloaded_by: test\nlevel: L3\nlast_reviewed: 2026-10-26\n---\n"


class ReferenceCapsTests(unittest.TestCase):
    def setUp(self):
        self.mod = _load()
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.plugin = self.root / "song-team"
        (self.plugin / "skills" / "x" / "references" / "genres").mkdir(parents=True)
        (self.plugin / "references" / "shared").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, rel: str, lines: int, frontmatter: bool = True) -> Path:
        p = self.plugin / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        body = "\n".join(f"line {i}" for i in range(lines)) + "\n"
        p.write_text((FM if frontmatter else "") + body, encoding="utf-8")
        return p

    def test_passes_within_caps(self):
        self._write("references/shared/a.md", 100)
        self._write("skills/x/references/genres/pop.md", 50)
        self.assertEqual(self.mod.main(["--root", str(self.root), "--quiet"]), 0)

    def test_fails_on_oversized_then_passes_after_removal(self):
        big = self._write("references/shared/big.md", 200)
        self.assertEqual(self.mod.main(["--root", str(self.root), "--quiet"]), 1)
        big.unlink()
        self.assertEqual(self.mod.main(["--root", str(self.root), "--quiet"]), 0)

    def test_genre_cap_is_100(self):
        self._write("skills/x/references/genres/rock.md", 120)
        self.assertEqual(self.mod.main(["--root", str(self.root), "--quiet"]), 1)

    def test_missing_frontmatter_fails(self):
        self._write("references/shared/nofm.md", 10, frontmatter=False)
        self.assertEqual(self.mod.main(["--root", str(self.root), "--quiet"]), 1)

    def test_unclosed_frontmatter_fails(self):
        p = self.plugin / "references/shared/open.md"
        p.write_text("---\nloaded_by: x\nlevel: L3\nlast_reviewed: 2026-10-26\nbody\n", encoding="utf-8")
        self.assertEqual(self.mod.main(["--root", str(self.root), "--quiet"]), 1)

    def test_txt_pseudo_frontmatter(self):
        p = self.plugin / "references/shared/list.txt"
        header = "# loaded_by: challenger\n# level: L3\n# last_reviewed: 2026-10-26\n"
        p.write_text(header + "x\n" * 400, encoding="utf-8")
        self.assertEqual(self.mod.main(["--root", str(self.root), "--quiet"]), 0)
        p.write_text("x\n" * 5, encoding="utf-8")
        self.assertEqual(self.mod.main(["--root", str(self.root), "--quiet"]), 1)

    def test_cross_ref_with_no_pairs_fails(self):
        (self.plugin / "CROSS-SKILL-REFERENCES.md").write_text(
            "# x\n\n## Duplicated files\n\nnone\n", encoding="utf-8"
        )
        self.assertEqual(self.mod.main(["--root", str(self.root), "--quiet"]), 1)

    def test_duplicate_drift(self):
        self._write("skills/x/references/t.md", 10)
        self._write("skills/y/references/t.md", 10)
        xref = self.plugin / "CROSS-SKILL-REFERENCES.md"
        xref.write_text(
            "# Cross-skill references\n\n## Duplicated files\n\n"
            "| Source | Copy | Reason |\n|---|---|---|\n"
            "| `skills/x/references/t.md` | `skills/y/references/t.md` | isolation |\n",
            encoding="utf-8",
        )
        self.assertEqual(self.mod.main(["--root", str(self.root), "--quiet"]), 0)
        (self.plugin / "skills/y/references/t.md").write_text(FM + "drifted\n", encoding="utf-8")
        self.assertEqual(self.mod.main(["--root", str(self.root), "--quiet"]), 1)

    def test_windows_style_root_path(self):
        self._write("references/shared/a.md", 5)
        win = str(self.root).replace("/", "\\")
        self.assertEqual(self.mod.main(["--root", win, "--quiet"]), 0)

    def test_missing_plugin_root_is_error(self):
        self.assertEqual(self.mod.main(["--root", str(self.root / "nope"), "--quiet"]), 3)


if __name__ == "__main__":
    unittest.main()
