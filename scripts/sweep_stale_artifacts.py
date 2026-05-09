#!/usr/bin/env python3
"""sweep_stale_artifacts.py — Wave 3 W3-17 Stage-7 stale-sweep helper.

DEFECT-006 systemic fix. Architect picked Option A (banner each stale file)
at architecture-tk4-wave-3.md §Open questions #3.

Scans `.delivery/artifacts/<NN>-<stage>/` (default 07-uat/) for files with a
`<!-- run: run-... -->` HTML-comment marker that does NOT match the current
pipeline_id. Emits one of two actions per stale file:

  * `--mode banner` (DEFAULT)  — prepend a one-line banner warning to each
    stale file in place (idempotent: skips if banner already present).
  * `--mode archive`           — move the stale file into
    `.delivery/artifacts/_archive/<orig-stage>/<filename>` preserving paths.

Run at orchestrator's Stage-7 entry. Always exits 0 (helper, not a gate).

Usage:
    python3 scripts/sweep_stale_artifacts.py --pipeline-id run-2026-05-09-tk4
    python3 scripts/sweep_stale_artifacts.py --pipeline-id <id> --mode archive
    python3 scripts/sweep_stale_artifacts.py --pipeline-id <id> --stage 07-uat
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STAGE_DIR = ".delivery/artifacts/07-uat"
ARCHIVE_DIR = ".delivery/artifacts/_archive"
RUN_MARKER_RE = re.compile(r"<!--\s*run:\s*(run-[\w\-]+)", re.IGNORECASE)
BANNER_PREFIX = "<!-- STALE-WAVE-N-1 (W3-17 banner): "


def _find_marker(path: Path) -> str | None:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for _ in range(20):  # only scan first 20 lines
                line = fh.readline()
                if not line:
                    break
                m = RUN_MARKER_RE.search(line)
                if m:
                    return m.group(1)
    except OSError:
        return None
    return None


def _has_banner(path: Path) -> bool:
    try:
        first = path.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
    except (OSError, IndexError):
        return False
    return bool(first) and first[0].startswith(BANNER_PREFIX)


def _apply_banner(path: Path, stale_run: str, current_run: str) -> None:
    if _has_banner(path):
        return
    banner = (
        f"{BANNER_PREFIX}this artifact carries marker `{stale_run}` "
        f"but the current pipeline is `{current_run}`. "
        f"Producer/validator: confirm relevance before re-using. -->\n"
    )
    original = path.read_text(encoding="utf-8", errors="replace")
    path.write_text(banner + original, encoding="utf-8")


def _archive_file(path: Path, stale_run: str) -> Path:
    rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
    parts = rel.parts
    # rel like .delivery/artifacts/07-uat/dod/foo.md → archive under _archive/07-uat/dod/foo.md
    try:
        idx = parts.index("artifacts")
        sub = Path(*parts[idx + 1 :])
    except ValueError:
        sub = Path(rel.name)
    target = REPO_ROOT / ARCHIVE_DIR / sub
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(target))
    return target


def sweep(stage_dir: Path, current_run: str, mode: str) -> tuple[int, int]:
    """Return (stale_count, action_count). Always non-raising."""
    if not stage_dir.is_dir():
        print(f"sweep: {stage_dir} does not exist (nothing to do).", file=sys.stderr)
        return 0, 0

    stale = 0
    actioned = 0
    for path in sorted(stage_dir.rglob("*.md")):
        marker = _find_marker(path)
        if marker is None or marker == current_run:
            continue
        stale += 1
        if mode == "archive":
            target = _archive_file(path, marker)
            print(f"ARCHIVED: {path}  →  {target}  (stale marker: {marker})")
            actioned += 1
        else:  # banner mode (default)
            if _has_banner(path):
                print(f"SKIP (already-bannered): {path}  (stale marker: {marker})")
            else:
                _apply_banner(path, marker, current_run)
                print(f"BANNERED: {path}  (stale marker: {marker})")
                actioned += 1
    return stale, actioned


def main() -> int:
    ap = argparse.ArgumentParser(description="Sweep stale Wave-N-1 artifacts.")
    ap.add_argument("--pipeline-id", required=True, help="current pipeline id (e.g. run-2026-05-09-tk4)")
    ap.add_argument("--stage", default=DEFAULT_STAGE_DIR, help="stage subdir (default: 07-uat)")
    ap.add_argument(
        "--mode",
        choices=("banner", "archive"),
        default="banner",
        help="banner = prepend warning (default, Option A); archive = move to _archive/",
    )
    args = ap.parse_args()

    stage_dir = REPO_ROOT / args.stage
    stale, actioned = sweep(stage_dir, args.pipeline_id, args.mode)

    print(
        f"\nSWEEP DONE: scanned {stage_dir.relative_to(REPO_ROOT)} | "
        f"stale={stale} | actioned={actioned} (mode={args.mode})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
