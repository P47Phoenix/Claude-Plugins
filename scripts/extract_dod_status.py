#!/usr/bin/env python3
"""extract_dod_status.py — Wave 3 W3-15 STATUS-line parser.

Pragmatic STATUS extractor that handles BOTH historical formats observed
across Wave 0, Wave 2, and caveman-lite (tk3) DoD review files:

    STATUS: DONE                       (orchestrator-canonical, post-W3-13)
    **Status**: DONE                   (markdown-bold variant, Wave-2 era)
    **Status**: **DONE**               (double-bolded variant, Story 6 era)
    Status: DONE                       (Wave-0 plain variant)
    **Status**: PASS (all criteria…)   (alt verb, Wave-0 era)

Strict canonical going forward is the W3-13 template's `STATUS: <value>`
line. This helper exists to avoid breaking grep checks against the
existing artifact corpus while the canonical form propagates.

Wave 2 retro lesson #4 (DoD STATUS-line format diversity, gate-patterns.md):
"Standardize the format OR use a flexible regex everywhere." Architect at
Stage 4 picked standardize as cheaper; this helper is the bridge so legacy
artifacts still parse during the transition.

Returned values are **always upper-cased** verbatim STATUS tokens:
    DONE | NOT_DONE | CODE_COMPLETE | PASS_WITH_NOTES | PASS | PASSED | FAIL

Usage:
    python3 scripts/extract_dod_status.py <file>...
    python3 scripts/extract_dod_status.py --all .delivery/artifacts/06-dev/dod/

Exit codes:
    0 — STATUS extracted from every input file
    1 — at least one file had no STATUS line (orchestrator: re-dispatch)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Match canonical OR markdown-bold OR pipe-separated OR `Gate Status` variants.
# Anchored to a `(Gate )?Status:` token (case-insensitive, optional ** wrapping)
# so it picks up:
#   STATUS: DONE                      (canonical, post-W3-13)
#   **Status**: DONE                  (Wave-2 markdown-bold)
#   **Status**: **DONE**              (Story 6 double-bold)
#   Status: DONE                      (Wave-0 plain)
#   ... | **Status:** DONE            (inline pipe-separated)
#   **Gate Status**: DONE ✓           (Wave-0 alt)
STATUS_RE = re.compile(
    r"\**\s*(?:gate\s+)?status\s*\**\s*:\s*[\"'\*]*\s*"
    r"(DONE|NOT_DONE|CODE_COMPLETE|PASS_WITH_NOTES|PASSED|PASS|FAIL)"
    r"\b\s*[\"'\*]*",
    re.IGNORECASE,
)


def extract_status(text: str) -> str | None:
    """Return the FIRST STATUS token found in `text`, normalized to upper-case."""
    m = STATUS_RE.search(text)
    if not m:
        return None
    return m.group(1).upper()


def _iter_files(args: list[str]) -> list[Path]:
    files: list[Path] = []
    expand_dirs = False
    for arg in args:
        if arg == "--all":
            expand_dirs = True
            continue
        p = Path(arg)
        if p.is_dir() and expand_dirs:
            files.extend(sorted(p.rglob("*.md")))
        elif p.is_file():
            files.append(p)
        else:
            print(f"WARN: skip {arg} (not a file or --all not set for dir)", file=sys.stderr)
    return files


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    files = _iter_files(sys.argv[1:])
    if not files:
        print("FAIL: no input files", file=sys.stderr)
        return 1

    missing = 0
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"{path}\tERROR\t{exc}")
            missing += 1
            continue
        status = extract_status(text)
        if status is None:
            print(f"{path}\tMISSING\t-")
            missing += 1
        else:
            print(f"{path}\t{status}")
    return 0 if missing == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
