# Plan DoD: QA coverage review (Round 2, LIGHT)

SKILL_LOADED: delivery-team:quality
Role: QA | Task: dod-validation | Base tip 337edb5 | Inputs: stories.md, prd.md, ADR-models-001

**Status: DONE** (all criteria PASS; 0 must-fix; 3 non-blocking notes)

## 1. PRD AC enumeration (own count from prd.md)

FR-1 4 | FR-2 2 | FR-3 2 | FR-4 2 | FR-5 1 | FR-6 5 (positive, negative-inject, positive-IDs, delimiters, no github.event) | FR-7 2 | FR-8 3 | FR-9 1 | FR-10 3 | FR-11 3 = **28**. Matches stories.md.

Mapping: AC-01..04 FR-1; 05-06 FR-2; 07-08 FR-3; 09-10 FR-4; 11 FR-5; 12-16 FR-6; 17-18 FR-7; 19-21 FR-8; 22 FR-9; 23-25 FR-10; 26-28 FR-11. AC-01..AC-28 contiguous, no gaps, no dupes, each FR-order matches PRD order. **PASS**

## 2. Runnable / non-vacuous checks (RUN for real)

| Criterion | Result | Evidence |
|---|---|---|
| (a) `'*.ext'` globs cover root files | PASS | Scratch repo, root README.md with stale ID: `git ls-files '*.md'` -> 1 match; `'**/*.md'` -> 0 (false pass reproduced). Guard built with `'*.ext'` flagged injected README.md line exit 1. `'**/*.ext'` only in `on.paths` (AC-19 = 7 stays valid; current file has 2 such lines, becomes 7 after rewrite). |
| (b) diff/commit-count post-commit forms | PASS | Scratch clone sim: `rev-list --count 337edb5..HEAD -- ':!.delivery'` = 0 pre-ship, 0 after .delivery-only commit (all=1, so bare count would break), 1 after ship. Post-ship: `numstat` prompt-engineer `1 1`; delivery-flow name-only count `0`; CHANGELOG `-vc` `0`; AC-10 `git diff -U0 337edb5..HEAD` and `git show -U0 HEAD` both `0`. Pre-ship forms yield 0/empty (vacuous only pre-ship; each has a non-vacuous post-ship expected value, so the final pass is real). |
| (c) CHANGELOG rule vs guard | PASS | Baseline count of `claude-opus-5\|claude-sonnet-5\|stale-model-id-guard` in CHANGELOG = 0 (so AC-28a not vacuous). Guard on current tree flags exactly the 10 live sites, none in CHANGELOG. Stale ID appended to root CHANGELOG.md -> exit 1, so the no-retired-ID wording rule (T-C3) is needed and present. Placeholder `_No unreleased changes at this time._` exists at line 10. |
| (d) US-4 | PASS | Explicit paths `.delivery/backlog/BACKLOG-109..112-*.md`; runnable US4-a/b/c; pre-impl run: 109-112 unused, US4-a prints MISSING, US4-b/c error rc=2 (not false pass). Wording "25 SKILL.md files" present; verified 25 SKILL.md files / 26 stamp lines. |
| Guard matrix (guard per story contract, post-migration sim) | PASS | Clean tree -> message + 0. T-N1..N8 all 1; T-N9 1; T-P1..P4 all 0; T-D1/D2 0; T-D3 1; T-E1/E2 0; T-E3/E4 1; T-W1 scratch.json 1; T-R1 README/CHANGELOG 1. `\2` sed correct. |
| Pre-impl gates | PASS | AC-02 baseline 4 old IDs in conftest (lines 105,117,129,151); AC-03 line 36; AC-04 line 174; AC-09 `3 passed`; AC-23 budget check exit 0; AC-24 `0`; AC-21 YAML loads; AC-22 currently exit 1 (gate blocks, T-V1). |

## 3. Ordering and atomicity

US-2 -> US-3 -> US-1 (guard + literals + fixtures + CHANGELOG in one commit) -> US-4 sane. US-1 holds guard (S15), literals (S1,S2,S5,S6,S11-S14) and fixtures (S7-S10); T-X1 proves halves fail alone; AC-26 `':!.delivery'` count tolerates interleaved artifact commits. **PASS**

## Non-blocking notes (no fix required for DoD)

1. AC-04 (line 174) and AC-06 (lines 148, 189) are line-pinned; S1/S5 provenance rewrite must stay line-neutral or Dev updates the numbers. Baseline lines 148/189 are already `#` lines.
2. AC-01 has no guard-file exclusion: the rewritten guard must not keep old IDs outside `#` lines (current echo text at line 39 and grep at line 30 do). Rewrite removes them; keep in mind for Dev.
3. AC-23/AC-10 pre-commit `git diff` is empty if changes are staged; use the stated post-commit forms for the final pass.

## Verdict: DONE
