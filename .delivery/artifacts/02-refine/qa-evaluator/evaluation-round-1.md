# Gate 2 Evaluation: PRD Quality Gate Flow Refactoring

**Evaluator**: Legolas, QA Engineer
**Date**: 2026-03-30
**PRD Version**: 1.0
**Metrics Version**: 1.0
**Round**: 1

---

## BLOCKING Criteria

### B1: Every FR has testable acceptance criteria

**Verdict: PASS**

All 8 FRs (FR-01 through FR-08) have explicit acceptance criteria written as checkboxes. Each criterion is verifiable by a concrete command or inspection method. Examples of strong testability:

- FR-01 AC-01a: "A new file `stage_definitions.py` exists" -- file existence check
- FR-03 AC-03a: "`PRDFlowBuilder` class is <=200 lines (measured by `wc -l`)" -- deterministic measurement
- FR-05 AC-05c: "`grep -r '\"prd_flows.db\"'` across the plugin directory returns only `shared.py`" -- exact verification command provided

I can write a test for every single AC in this PRD. No criterion is left to subjective judgment.

---

### B2: No ambiguous language in acceptance criteria

**Verdict: FAIL**

The acceptance criteria themselves are free of "should", "might", and "could". Present tense and "must" are used correctly throughout. However, three ACs contain branching "either...or" constructs that create ambiguous end-states:

**Finding 1 -- FR-04 AC-04a**:
> `"run_execute.py is either deleted or converted to a thin wrapper (<=10 lines) that imports from prd_execute.py and prints a deprecation warning"`

**Finding 2 -- FR-04 AC-04b**:
> `"run_builder.py is either deleted or converted to a thin wrapper (<=10 lines) that imports from prd_flow_builder.py and prints a deprecation warning"`

A QA engineer cannot write a single definitive test when the expected state branches. Is the file deleted or is it a wrapper? Both are valid outcomes, but the assertion must know which one to verify. The PRD already contains a recommendation in OQ-1: "Thin wrappers with deprecation print(), remove in next release." Commit to it.

**Finding 3 -- FR-03 AC-03b**:
> `"Schema creation (_create_schema) is extracted to a separate module (e.g., schema.py) or to a standalone function"`

Same pattern. This maps to OQ-5 (open question deferred to Design). The AC is untestable until the extraction target is decided. The "New Files" table already proposes `schema.py` as a separate module with an estimated 150-180 lines. Commit to it.

**Fix**: Replace all "either...or" ACs with definitive statements. Resolve OQ-1 and OQ-5 before exiting Refine. The PRD already has recommendations for both -- promote them to decisions.

---

### B3: Success metrics are measurable with defined baselines and targets

**Verdict: PASS**

The metrics artifact (by Elrond) is thorough. All 10 metrics (M1-M10) have:
- Precise definitions with explicit formulas (`wc -l`, `grep -rl`, `git diff --stat`)
- Numeric baselines captured from the actual codebase at commit `834b532`
- Numeric targets with direction indicators
- A complete verification script that can be run in a single pass

The PRD Goals table (Section 2) aligns 1:1 with the metrics artifact. Every goal has a baseline, target, and measurement method. The dogfooding validation requirement (P0 UAT gate for before/after output comparison) is explicit with a capture protocol.

---

### B4: User roles are specific (not just "user")

**Verdict: PASS**

Section 3 defines two personas with who/goal/pain/success structure:
- **P1: Plugin Maintainer** -- "A developer extending or modifying the PRD quality gate flow"
- **P2: Pipeline User** -- "A user running PRD workflows via the documented CLI commands in CLAUDE.md"

User stories reference these roles consistently: "As a maintainer..." (US-01 through US-04, US-07 through US-09), "As a user..." (US-05, US-06). The "user" in US-05/US-06 maps unambiguously to the defined P2 persona.

---

### B5: Out of scope section is present and non-empty

**Verdict: PASS**

Section 7 lists 8 explicit exclusions: core module changes, new features, schema migrations, test framework setup, YAML data files, SKILL.md changes, performance optimization, and documentation file changes. Well-bounded. The exclusions align with NFR-06 (core modules untouched) and NFR-01 (zero new dependencies).

---

## BLOCKING Summary

| # | Criterion | Verdict |
|---|-----------|---------|
| B1 | Every FR has testable acceptance criteria | PASS |
| B2 | No ambiguous language in acceptance criteria | **FAIL** |
| B3 | Measurable success metrics with baselines and targets | PASS |
| B4 | Specific user roles | PASS |
| B5 | Out of scope present and non-empty | PASS |

**Gate 2 Result: FAIL** -- B2 must be resolved before proceeding.

---

## WARNING Criteria

### W1: NFRs have quantified targets

**Verdict: PASS (with note)**

All 6 NFRs have quantified or binary-verifiable targets:
- NFR-01: "No non-stdlib imports added" -- grep verification
- NFR-02: "Existing `prd_flows.db` files work without migration" -- load test
- NFR-03: "No syntax or stdlib features requiring >3.9" -- code review
- NFR-04: "Before/after output identical for all 4 CLI entry points" -- diff
- NFR-05: "Every modified/new `.py` file <=300 lines" -- `wc -l`
- NFR-06: "zero diff" on core modules -- `git diff`

**Note**: NFR-03 lacks a concrete verification command. The metrics artifact does not include a metric for Python version compatibility. Recommend adding a specific check (e.g., `python3.9 -c "import ast; ast.parse(open(f).read())"` for each file, or listing prohibited syntax: `match`/`case`, `X | Y` type unions, `tomllib`).

---

### W2: Edge cases are identified

**Verdict: WARNING -- Partial coverage**

The Risks section identifies 6 risks that function as edge cases (ordering bugs, missed hardcoded paths, backward compat breaks, schema breaks, multi-line string formatting). FR-01 AC-01e adds load-time validation via `KeyError` for stage definitions.

**Missing edge cases I would test**:
1. Gate definitions have no equivalent load-time validation. FR-02 lacks an AC parallel to AC-01e. If `gate_definitions.py` has a malformed dict, the failure mode is undefined.
2. What if `shared.py` is imported via relative path from outside the plugin directory?
3. What if `prd_flows.db` is read-only or locked by another process?
4. What if deprecation wrapper scripts are run with Python 2 accidentally? (minor, but the wrappers would be the most user-facing entry points)

**Recommendation**: Add AC-02f: "Gate definitions are validated at load time -- `KeyError` raised if required fields are missing" (mirrors AC-01e).

---

### W3: Dependencies documented

**Verdict: PASS**

Section 8 documents 5 dependencies with Type, Impact, and Status columns. The pre-refactoring output baselines dependency is critical and is explicitly called out with a capture protocol in the metrics artifact. All statuses are tracked (Confirmed, Active).

---

## WARNING Summary

| # | Criterion | Verdict |
|---|-----------|---------|
| W1 | NFRs have quantified targets | PASS (note on NFR-03 verification) |
| W2 | Edge cases identified | WARNING -- gate definition validation gap |
| W3 | Dependencies documented | PASS |

---

## Actionable Fixes Required (Blocking)

| # | Location | Issue | Fix |
|---|----------|-------|-----|
| F1 | FR-04 AC-04a | "either deleted or converted" is ambiguous | Commit to thin-wrapper approach per OQ-1 recommendation. Rewrite: "run_execute.py is a thin wrapper (<=10 lines) that imports from prd_execute.py and prints a deprecation warning to stderr" |
| F2 | FR-04 AC-04b | Same branching ambiguity | Same fix pattern as F1 for run_builder.py |
| F3 | FR-03 AC-03b | "extracted to a separate module ... or to a standalone function" is ambiguous | Resolve OQ-5. Commit to schema.py (already proposed in New Files table). Rewrite: "Schema creation (_create_schema) is extracted to a new file schema.py as a standalone function" |

## Actionable Fixes Recommended (Non-blocking)

| # | Location | Issue | Fix |
|---|----------|-------|-----|
| R1 | FR-02 | No load-time validation AC for gate definitions | Add AC-02f: "Gate definitions are validated at load time -- KeyError raised if required fields are missing" (mirrors AC-01e) |
| R2 | NFR-03 | No concrete verification method for Python 3.9+ compat | Add measurement method: list prohibited syntax features or add AST parse check |

---

## Verdict

**STATUS: FAIL**

The PRD passes 4 of 5 blocking criteria. It fails B2 due to three acceptance criteria containing branching "either...or" language that prevents writing deterministic tests. The fixes are straightforward -- the PRD already contains recommendations for both open questions. Promote the recommendations to decisions and rewrite the three ACs.

Two non-blocking recommendations are noted: add gate definition load-time validation (mirrors existing stage validation), and strengthen NFR-03 verification.

The edge case you thought was unreachable -- branching acceptance criteria that a QA engineer cannot write a single test for -- I have already tested it. It fails.
