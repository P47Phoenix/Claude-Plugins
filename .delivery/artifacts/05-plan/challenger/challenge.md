# Adversarial Challenge: Sprint Plan for prd-quality-gate-flow Refactoring

**Challenger**: Adversarial Reviewer
**Date**: 2026-03-30
**Artifacts Reviewed**: Sprint Plan v1.0, User Stories v1.0, Test Strategy v1.0, Design Spec v1.0
**Codebase Inspected**: `prd-quality-gate-flow/` (8 Python files, 3,042 total lines)

---

## Challenge 1: The 20 SP Velocity Baseline Is Ungrounded

**Confidence**: 2/5 (serious doubts)

The sprint plan declares a "standard Python code refactoring velocity for a solo developer" of 20 SP per sprint. There is no historical velocity data to support this. This is a greenfield estimate on a codebase that has never been refactored before, by a team that has never measured its velocity.

**Evidence**:
- No prior sprints exist in this project to calibrate from.
- The plan itself acknowledges this implicitly by needing to redistribute from 2 sprints to 3 sprints -- if the baseline were reliable, the PO's original 2-sprint allocation would have been closer to correct.
- The 80% ceiling (16 SP) is only meaningful if the 20 SP base is trustworthy. If actual velocity is 15 SP, the ceiling should be 12 SP, and Sprint 1 at 16 SP is already 133% of ceiling.

**What should change**: Acknowledge the velocity is an assumption, not a measurement. Add a Sprint 1 retrospective checkpoint that recalibrates Sprint 2/3 commitments based on actual Sprint 1 throughput. The plan currently treats the 3-sprint allocation as fixed rather than adaptive.

---

## Challenge 2: Sprint 1 at 100% Ceiling Is Not "Low Risk"

**Confidence**: 2/5 (serious doubts)

The plan justifies Sprint 1 at 100% of the 80% ceiling (16 SP) by claiming "all stories are additive (new files) with zero modification of existing code." This reasoning is flawed.

**Evidence**:
- US-04 (5 SP) and US-05 (5 SP) require extracting data from `prd_flow_builder.py` lines 362-1068. This is not "creating new files from scratch" -- it is transcription of 700+ lines of deeply nested Python dicts with multi-line strings, embedded JSON-like condition objects, and heterogeneous metadata fields. The QA test strategy itself flags "whitespace corruption during extraction" (US-04) and "transcription errors in complex conditions" (US-05) as regression concerns.
- The 20 business rules across 7 gates have inconsistent structure: some rules have `metadata` dicts, some do not. Some conditions use `AND` with nested arrays, some use flat field/operator/value. Gate 4 has a `validation` rule_type instead of `gate`. This heterogeneity increases transcription error probability.
- US-03 (1 SP) modifies `shared.py` which was created in US-01. It is not purely additive -- it is the first modification of a file created in the same sprint.

**What should change**: Drop Sprint 1 to 14 SP (88% of ceiling) by moving US-05 to Sprint 2. This gives Sprint 2 a heavier load (16 SP) but Sprint 2 already has the 31% buffer, and US-05 (gate definitions) is needed by US-06 anyway -- they can be done consecutively in the same sprint without adding dependency risk.

---

## Challenge 3: US-06 at 8 SP Underestimates the Decomposition Complexity

**Confidence**: 2/5 (serious doubts)

US-06 (Decompose PRDFlowBuilder) is estimated at 8 SP. This story rewrites 1,157 lines into <=200 lines while preserving exact behavioral output (15 nodes, 20 rules, identical parent-child chaining). I believe this is underestimated.

**Evidence**:
- The `build_prd_flow()` method (lines 280-360) does not just call factory methods -- it chains return values. Each `_create_stageN` returns a `node_id` that becomes the `parent_id` for the next `_create_gateN`. The decomposed version must replicate this chaining through a `PIPELINE_SEQUENCE` loop. Getting the parent-child threading right requires understanding the exact interleaving of stages and gates.
- The interleaving is not uniform: Gates 3 and 4 are consecutive (no stage between them), and Stages 5 and 6 are consecutive (no gate between them). A naive loop over alternating stage/gate pairs will produce the wrong tree structure. The plan mentions `PIPELINE_SEQUENCE` but does not acknowledge this irregularity.
- The `create_node()` and `create_rule()` methods (lines 205-278) contain internal logic (timestamp ID generation, JSON serialization, config storage) that must be preserved exactly. The decomposition must also preserve the `self.conn.commit()` call at line 354, which commits the entire flow atomically.
- Stage 3 uses `NodeType.CONTROL_FLOW` instead of `NodeType.AGENT` -- another irregularity a data-driven loop must handle.
- The plan says "atomic commit, compare counts, revert if wrong." But count comparison (15 nodes, 20 rules) is necessary but not sufficient. Two completely different tree structures can produce the same counts. The `export_flow_diagram()` output comparison is mentioned but not formalized as a hard gate.

**What should change**: Increase US-06 to 10-12 SP. Make `export_flow_diagram()` output comparison a hard P0 acceptance criterion (not just a verification step). Document the irregularities (consecutive gates 3-4, consecutive stages 5-6, CONTROL_FLOW node type for stage 3) explicitly in the story's implementation notes so the developer does not discover them mid-implementation.

---

## Challenge 4: The Test Strategy Is Fragile Without a Test Framework

**Confidence**: 3/5 (moderate doubts)

The test strategy relies entirely on ad-hoc `python -c` one-liners and `grep` commands. There is no test runner, no assertion framework, no way to run "all tests" as a suite.

**Evidence**:
- The test strategy documents 42 acceptance criteria across 11 stories, verified by approximately 35+ individual CLI commands. These commands are scattered across the test strategy document and the sprint plan. There is no script that runs all of them.
- If any test fails, the developer must manually identify which command failed and re-run it. There is no red/green feedback loop.
- The "baselines are captured to stdout and recorded in the development session" (Test Strategy section 2). This means baselines are ephemeral -- if the session ends or the developer forgets to record them, the behavioral compatibility check cannot be performed.
- The empirical tests (running `python prd_flow_builder.py` and comparing output) depend on a clean database state. If a previous run left a `prd_flows.db` file, the builder creates a new flow alongside old ones, and `check_db.py` will report different counts than expected. The test strategy does not address database cleanup between test runs.

**What should change**: Create a single `verify.py` script (or shell script) that runs all structural and empirical checks in sequence and reports pass/fail. This is not a test framework -- it is a verification script, which is consistent with NFR-01 (zero new dependencies). Persist baselines to a file (e.g., `baseline.json`) rather than relying on session memory. Add explicit database cleanup (delete `prd_flows.db`) before empirical test runs.

---

## Challenge 5: Behavioral Compatibility Verification Is Insufficient

**Confidence**: 2/5 (serious doubts)

The plan defines behavioral compatibility as "structural equivalence: 15 nodes, 20 rules, 7 gates, matching flow structure, exit code 0." This is too coarse.

**Evidence**:
- Node and rule counts are aggregate numbers. They do not verify that each gate has the correct number of rules. Gate 1 has 4 rules, Gate 2 has 4 rules, Gate 3 has 3 rules, Gate 4 has 1 rule, Gate 5 has 4 rules, Gate 6 has 3 rules, Gate 7 has 1 rule. If the decomposition accidentally assigns Gate 4's single rule to Gate 3 (giving Gate 3 four rules and Gate 4 zero), the total is still 20.
- Rule content is not verified at all. The conditions, priorities, metadata, and rule_types could all be wrong while counts match. For example, if `"operator": ">="` becomes `"operator": ">"` during transcription, the count is unchanged but the business rule behavior is different.
- The `export_flow_diagram()` function (lines 1086-1110) only outputs node names, descriptions, and per-gate rule counts. It does not output rule names, conditions, or priorities. It is a structural summary, not a behavioral fingerprint.
- Parent-child relationships are verified only by visual inspection of the diagram output, which shows indentation based on tree depth. Two different tree structures could produce the same indentation pattern if they have the same depths.

**What should change**: Add per-gate rule count verification (not just total). Add a verification step that queries `SELECT gate_node_id, COUNT(*) FROM business_rules WHERE flow_id = ? GROUP BY gate_node_id` and compares the distribution to the known baseline [4, 4, 3, 1, 4, 3, 1]. Consider adding a rule content hash (SHA-256 of JSON-serialized condition dicts) for the highest-risk rules (Gate 1's complex AND condition, Gate 4's validation rule, Gate 5's nested AND condition).

---

## Challenge 6: The PO and SM Disagree on Sprint Count, and the SM Won Without Re-Verification Step

**Confidence**: 4/5 (fairly confident this is fine, minor concern)

The PO's user stories allocate 27 SP to Sprint 1 and 7 SP to Sprint 2 (2 sprints). The SM overrides this to 3 sprints (16/11/7). The SM's reasoning is sound (27 SP exceeds 16 SP ceiling), but the override creates a process concern.

**Evidence**:
- The SM's redistribution is documented and justified (Section 2.1 of the sprint plan).
- However, the PO's original 2-sprint plan has a valid internal logic: Sprint 1 does all the building, Sprint 2 does all the cleanup. The SM's 3-sprint plan splits the "building" phase across two sprints, which means Sprint 2 begins with the highest-risk story (US-06) without the safety net of having just completed the foundation work in the same sprint context.
- Session continuity is a real concern for an AI-assisted solo developer. Each sprint boundary is a potential context loss point. The SM's plan introduces one additional context boundary in the middle of the critical path.

**What should change**: This is acceptable as-is, but the plan should explicitly note that Sprint 2 must begin by re-verifying Sprint 1's exit criteria before starting US-06. A 5-minute re-verification step at Sprint 2 start eliminates the context loss risk.

---

## Challenge 7: The "Single Atomic PR" Strategy Conflicts with 3-Sprint Duration

**Confidence**: 3/5 (moderate doubts)

The deployment approach calls for "single atomic PR with all 11 commits." But the work is spread across 3 sprints. This means the PR stays open for the entire duration of all 3 sprints.

**Evidence**:
- A long-lived feature branch (`refactor/prd-quality-gate-decomposition`) will diverge from `main` if other work lands on `main` during the 3 sprints.
- The `CLAUDE.md` file (modified in US-11) is a high-traffic file that other contributors may also modify. Merge conflicts are likely.
- If Sprint 2's US-06 introduces a regression that is not caught until Sprint 3's dogfooding, the remediation happens 2 sprints after the defect was introduced. The feedback loop is too long.

**What should change**: Consider shipping Sprint 1 as its own PR since it is purely additive (new files, zero modification of existing code). This reduces the long-lived branch window and gives an earlier integration signal. Sprint 2+3 can remain a single PR since they modify existing files and must be atomic.

---

## Summary Scorecard

| # | Challenge | Confidence | Recommendation |
|---|-----------|:----------:|----------------|
| 1 | Velocity baseline is ungrounded | 2/5 | Add retrospective recalibration after Sprint 1 |
| 2 | Sprint 1 at 100% ceiling is riskier than claimed | 2/5 | Move US-05 to Sprint 2, or reduce to 88% |
| 3 | US-06 at 8 SP is underestimated | 2/5 | Increase to 10-12 SP, document irregularities |
| 4 | Test strategy is fragile without a verification script | 3/5 | Create `verify.py`, persist baselines |
| 5 | Behavioral compatibility checks are too coarse | 2/5 | Add per-gate rule counts and content hashing |
| 6 | SM overrode PO sprint count without re-verification step | 4/5 | Add Sprint 2 entry verification (minor) |
| 7 | Single atomic PR over 3 sprints risks divergence | 3/5 | Ship Sprint 1 as separate additive-only PR |

**Overall assessment**: The sprint plan is well-structured and thoughtfully written. The SM correctly identified and addressed the overcommitment problem. However, the plan is overconfident in three areas: the velocity baseline, the US-06 estimate, and the behavioral compatibility verification. The highest-impact improvement would be formalizing per-gate rule count verification (Challenge 5) -- this is cheap to implement and catches the most likely class of decomposition bugs.
