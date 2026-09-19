# PO DoD Review: Idea Brief (model migration)

Reviewer: PO | Input: .delivery/artifacts/01-idea/po/idea-brief.md | Verdict: PASS (1 minor wording fix)

## Discovery grep re-run
Command: `grep -rnoE 'claude-(opus|sonnet|haiku)-[0-9][0-9a-z.-]*' . --exclude-dir=.git --exclude-dir=.delivery`
Result: 22 hits. Per file: agent_registry.py 6, conftest.py 4, stale-model-id-guard.yml 8, smoke-test-architecture.md 2, telemetry-schema.md 1, prompt-engineer/SKILL.md 1. Zero `claude-fable` hits (matches brief).
Count CONFIRMED: 22 hits, 6 files. But the 6 files INCLUDE the guard; brief says "22 literal hits across 6 files plus the guard" and "The 6 files above with live literals, plus ... guard". Real split: 14 hits in 5 files + 8 hits in guard.

## Criteria
| Criterion | Result | Note |
|---|---|---|
| Problem | PASS | Stale IDs, guard allows old IDs, Fable absent. |
| Users | PASS (weak) | Implicit (plugin maintainers/consumers, downstream API callers). Acceptable for LIGHT stage. |
| Measurable goals | PASS | 4 goals + Success signal testable via git grep, guard inject test, smoke/budget/hash checks. |
| Constraints | PASS | CI static-only, guard mechanics, budgets, hash re-freeze, Fable/Opus5 API diffs. |
| Scope / out-of-scope | PASS | Both explicit; out-of-scope marked "proposed", Refine confirms. |
| Open questions actionable | PASS | 9 items, each with option set or recommended default; Refine told to take Q1-4 first. |
| BACKLOG-108 coherent | PASS | Supersede+retarget; carry-forward, retarget, split-out lists consistent with scope; memory topic handling stated. |
| Discovery count | FAIL (minor) | Section: Discovery totals + In scope. Why: "6 files plus the guard" is off by one; guard is the 6th file. Fix: reword to "22 hits: 14 in 5 files plus 8 in the guard (6 files total)"; In scope: "the 5 files above plus the guard rewrite".
