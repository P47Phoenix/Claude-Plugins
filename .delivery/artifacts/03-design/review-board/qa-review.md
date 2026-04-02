# QA Risk Review: Design Spec Testability Assessment

**Reviewer**: Legolas (QA Engineer) -- Risk Reviewer, Multi-Perspective Review Board
**Artifact**: `.delivery/artifacts/03-design/ux/design-spec.md` v1.0
**Date**: 2026-03-30

---

## Verdict: PASS

The design spec demonstrates strong testability across all four review dimensions. Two advisory findings are noted below -- neither rises to BLOCK severity, but both should be addressed during implementation.

---

## 1. Can Each Refactoring Step Be Verified Independently?

**Finding: PASS**

All 11 steps include explicit verification commands. Steps 1-5 (additive, new modules) each have a one-liner Python import/assertion test that can be run in isolation. Steps 6-9 (modifications to existing files) include structural verification (line counts, grep checks, node/rule count assertions). Steps 10-11 (deletion and docs) have grep-based negative checks.

The verification commands are concrete and automatable -- they are not vague statements like "verify it works." Each command produces a deterministic, inspectable output (e.g., `_count_nodes(fid) == 15`, `_count_rules(fid) == 20`).

**Strength**: Step 6 (the highest-risk transformation) has the most thorough verification: line count check, node count check, rule count check, and flow diagram structural diff. This is proportional to the risk.

---

## 2. Are There Clear Before/After States for Validation?

**Finding: PASS**

Section 1 (Current State Diagram) provides precise baselines: file inventory with exact line counts, hardcoded string counts (10 occurrences of `"prd_flows.db"` across 6 files), dependency graph with import/export lists, and a line-range breakdown of `PRDFlowBuilder` internals (9 segments mapped by line range).

Section 2 (Target State Diagram) provides exact target line counts per file with delta calculations. The net line delta (-499) is calculated and shown. Section 9 (Structural Equivalence Verification Plan) maps each CLI entry point to its pre-refactoring baseline and post-refactoring check with specific metrics.

The Behavioral Compatibility Matrix (Section 5.2) explicitly defines what "equivalent" means per entry point: output structure, exit codes, and DB side effects. This removes ambiguity from "it should work the same." The note that timestamp-based IDs are excluded from comparison (per NFR-04) is a mature testability decision -- it prevents false negatives from non-deterministic values.

---

## 3. Is Behavioral Compatibility Verifiable Without a Test Suite?

**Finding: PASS with advisory**

The design relies on manual CLI execution and count-based comparison rather than automated tests, which is appropriate given the PRD scope (no test runner configured, per CLAUDE.md). The verification plan in Section 9 is executable by hand. The 42 acceptance criteria in the FR Traceability Matrix (Section 6) each have a concrete verification method -- grep commands, Python one-liners, or code review checks.

However, there is one gap:

**Advisory F-01: No intermediate behavioral snapshot protocol for Step 6.** The design says to "capture pre-refactoring baseline" before Step 6 and compare afterward, but does not specify *where* that baseline is stored or *in what format* the comparison is performed. During implementation, the developer could skip this or do it inconsistently.

**Recommendation**: Add an explicit instruction to Step 6 mitigation: "Before modifying `prd_flow_builder.py`, run `python prd_flow_builder.py > /tmp/baseline_builder_output.txt` and capture node/rule counts to a file. After modification, diff the outputs." This makes the before/after comparison a concrete, repeatable action rather than a suggestion.

---

## 4. Are Rollback Points Defined for Each Step?

**Finding: PASS with advisory**

Section 8 (Risk Mitigations Summary) provides explicit rollback commands for all 11 steps. Additive steps roll back with `git rm`. Modification steps roll back with `git checkout <file>`. Deletion steps (Step 10) roll back with `git checkout` of the deleted files. The global rollback is a single atomic PR revert (PRD R7).

The rollback strategy is sound because each step leaves the codebase in a working state (stated in Section 4 intro), meaning any step's rollback returns to the previous working state.

**Advisory F-02: Step 3 rollback dependency chain unclear.** Step 3 wires `shared.get_connection()` to call `ensure_schema()`. The stated rollback is "revert `shared.py` edit." If Steps 4 or 5 have already been completed before a Step 3 regression is discovered, the rollback table implies Step 3 can be reverted independently. This is actually safe -- Steps 4 and 5 are purely additive data modules with zero internal imports (dependency rule 1), so they do not depend on Step 3's wiring. But this non-obvious safety should be stated explicitly.

**Recommendation**: Add a note to the Step 3 rollback cell: "Safe to revert independently -- Steps 4/5 are leaf modules with no dependency on `get_connection()` wiring."

---

## Summary of Findings

| ID | Severity | Category | Description |
|----|----------|----------|-------------|
| F-01 | Advisory | Behavioral verification | Step 6 pre-refactoring baseline capture needs explicit file-based snapshot instructions |
| F-02 | Advisory | Rollback clarity | Step 3 rollback independence from Steps 4-5 should be stated explicitly |

**Blocking findings**: 0
**Advisory findings**: 2

Neither finding represents a testability risk that would block the design. The spec is unusually thorough for a refactoring design -- the FR traceability matrix (42 acceptance criteria, each with a verification method), the structural equivalence verification plan, and the per-step verification commands provide a strong foundation for validation without a formal test suite. The PIPELINE_SEQUENCE design decision (Section 7) correctly identifies the non-trivial stage/gate ordering as orchestration logic rather than data, which is the right separation for testability.

---

**VERDICT**: PASS
