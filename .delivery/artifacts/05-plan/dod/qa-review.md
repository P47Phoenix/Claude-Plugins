# QA DoD Review: Plan stage (BUG_FIX, LIGHT), round 2

Status: DONE (all criteria PASS; 2 non-blocking notes)

## AC enumeration (16 total)
Story 1: AC-1.1 to AC-1.8 (8). Story 2: AC-2.1 to AC-2.5 (5). Story 3: AC-3.1 to AC-3.3 (3). Test cases: TC-1.1..1.7, TC-2.1..2.4, TC-3.1..3.2 (13). Each AC has a command and expected result.

## Baseline runs (read-only)
- `python3 scripts/check_skill_budgets.py`: prints `BUDGET VIOLATION ... delivery-flow/SKILL.md 514/500 (Tier-A)`, exit rc=1. Reproduces. AC-1.1 baseline correct.
- SKILL.md is 514 lines; main is 499. Worktree file equals HEAD. Target <=497 needs net -17 lines. The moved block (Step 4 para 1, orchestrator para, Step 5 sentence) is about 20 lines, so pointers must total <=3 net-added lines. Feasible, tight; margin of 3 is right.
- Stale-id guard, full pipeline, GNU grep 3.12 (`/usr/bin/grep`; the shell `grep` is a ugrep wrapper): HITS is exactly `smoke-test-architecture.md:116: {"model": "claude-sonnet-4-5", ...}`. Matches AC-2.1 and TC-2.1. Line 116 text matches AC-2.2 pre-edit apart from the model string. Post-edit expectation (no hits, "No stale 4.x model IDs found.") is sound: `claude-sonnet-4-6` is allowlisted.
- `python3 scripts/lint_known_debt.py`: exit 0 (lint baseline OK). header-warn checks only `model_awareness:` in `*SKILL.md`; the new reference is not a SKILL.md, so no regression risk beyond keeping the SKILL.md header untouched (TC-1.3 covers lines 1-332).
- `git diff origin/main...HEAD --stat -- '*/SKILL.md'`: 8 files (7 roles + delivery-flow), 99+/266-. Consistent with AC-3.3 and the PR text (about -170 net).

## Per-criterion
- AC-1.1 PASS. AC-1.2 PASS. AC-1.3 PASS. AC-1.4 PASS. AC-1.6 PASS (see note 2). AC-1.7 PASS. AC-1.8 PASS (covered via lint script and header-warn command, both runnable).
- AC-1.5 PASS with note 1.
- AC-2.1 PASS. AC-2.2 PASS. AC-2.3 PASS (overlaps AC-2.1; harmless). AC-2.4 PASS. AC-2.5 PASS.
- AC-3.1 PASS. AC-3.2 PASS. AC-3.3 PASS.
- Budget margin: PASS (497 target, 3 lines).
- Lint/header-warn regression coverage: PASS (AC-1.8, TC-1.3).

## Notes (non-blocking, dev should apply)
1. AC-1.5: "lines 333-346" is imprecise. In the current file the Step 4 paragraph starts at about line 335 and the orchestrator paragraph is at 350-352, so 333-346 misses the orchestrator text. Dev should use the actual line range (about 335-352, plus Step 5 line 385) or `git diff` removed lines (TC-1.4), which is the robust check.
2. AC-1.6: "prefer" currently appears only in Step 5 (line 385), not Step 4. The Step 4 pointer must add the word "prefer" or the grep will not hit within Step 4. TC-1.5 similarly requires `delivery-orchestrator` to remain in SKILL.md.
3. Shell `grep` here is a ugrep wrapper; use `/usr/bin/grep` for the guard, as stories already state.
