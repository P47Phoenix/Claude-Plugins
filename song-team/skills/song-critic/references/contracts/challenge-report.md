---
loaded_by: challenger
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: challenge-report (placeholder, lands in W3-4)

Written to `.song/<slug>/challenge-report.md` by the `challenger` role. The normative grammar is in `song-team/references/shared/artifact-formats.md` (section `challenge-report.md`): `## Findings` followed by the table `| severity | location | finding | suggested fix |`, severity in {BLOCKER, MAJOR, MINOR}; `challenge_gate.py` reads it and fails on any BLOCKER row.

The full contract (what counts as BLOCKER versus MAJOR, resemblance reporting, cliche density rows) lands with the `challenger` role in W3-4.
