# Developer DoD review: Stage 4 architecture (LIGHT)

SKILL_LOADED: delivery-team:developer
Verdict: PASS (5/5), 2 non-blocking notes.

## 1. Design conforms to PRD/constraints: PASS
- FR-1/5 -> section 6 + sites; FR-2 -> section 3 step 3; FR-3/BC-07 -> ALLOW keeps fable, not adopted; FR-4/BC-11 -> section 6 separate hunks; FR-6 -> section 3 + ALLOW/TOK; FR-7/BC-04 -> step 3 + failure table; FR-8 -> file set/excludes; FR-9/BC-13 -> merge gate; FR-10/BC-10/12 -> section 7, pre-push checks; FR-11/BC-03 -> section 8.
- No contradictions found. ADR matches architecture.
- Note A (non-blocking): PRD section 12 prose says sed replacement `\3`; architecture script uses `\2`. With D containing a nested group, `\2` is the correct (whole delimiter) choice. Dev should use `\2` (as /tmp/arch-g.sh) and not copy `\3`.

## 2. Guard pipeline run (scratch clone /tmp/dodv, HEAD 337edb5): PASS
- Current tree: exit 1, exactly 10 lines: agent_registry.py:149,190; smoke-test-architecture.md:115,116; telemetry-schema.md:36; conftest.py:105,117,129,151; prompt-engineer/SKILL.md:368. `#` provenance lines 148/189 exempt.
- Simulated migration (sed 4-6->sonnet-5, 4-7->opus-5 on the 5 files): prints OK, exit 0.
- Matrix, exit codes as expected:
  - 0: "Use claude-haiku-4-5-20251001." ; comma list of 3 ; `claude-opus-5.` ; `claude-fable-5-1` ; `# prior: claude-opus-4-8` ; `> prior: ...`
  - 1: `claude-opus-5.1` ; `claude-opus-5-` ; `claude-opus-5-20260101` ; `claude-fable-5` ; `claude-haiku-4-5` ; `claude-opus-4-8` ; `claude-opus-5.x` ; `claude-mythos-5-1` ; bare-line `prior: claude-opus-4-8` ; trailing `M = "claude-sonnet-5"  # prior: claude-opus-4-7` ; tracked .json with retired ID.
- CHANGELOG.md currently has zero `claude-` hits.

## 3. Single atomic commit: PASS
- Post-migration tree passes guard, and `python3 -m pytest delivery-team/tests/smoke -q` = 3 passed with conftest literals migrated (no test asserts the literal).
- Guard + literals in one commit means no CI-evaluated commit has them disagreeing. Verified the two halves each fail alone (guard-only run on old literals = exit 1; old guard cannot see -5).
- Note B (non-blocking, factual): architecture section 8 says `origin/..HEAD` count = 1 before push. Actual now = 0 (HEAD already on origin). Consequence: the shipping commit will be the sole commit ahead; conclusion unchanged. Fix wording only.

## 4. ADR: PASS
- Alternatives table A-E, Decision, Consequences, Rollback present. Status "Accepted" (binary; parenthetical restates rule, fine).

## 5. cache-prefix-hash honesty: PASS
- Section 7 and ADR say pre-existing stale, not touched, no CI reads it, deferred to BACKLOG-B. Confirmed: recorded 43067c9e..., current SKILL.md sha256 starts 0a7aa92f...; no workflow or script references the file.
