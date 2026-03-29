# Test Strategy: Deterministic Rules Engine Integration

**Version**: 1.0
**Author**: Legolas (QA Engineer, delivery-team)
**Date**: 2026-03-28
**Status**: Implementation-Ready
**Traces To**: PRD v2.1, Architecture v1.0, Stories v1.0

> *"Forty-two defects. Shall I describe them to you, or would you like me to file them in Jira?"*
>
> This test strategy ensures the rules engine delivers on its core promise: identical structured inputs produce identical outputs, every time. If it cannot prove that, it ships nothing.

---

## 1. Testing Philosophy

The rules engine exists to replace non-determinism with determinism. Therefore, the test strategy is built on three pillars:

1. **Determinism is the primary quality attribute.** Every component gets N-run replay tests. If any two runs diverge for the same structured input, the component fails regardless of whether the individual outputs are "correct."
2. **Boundary honesty over false confidence.** The PRD defines three determinism categories (a: fully deterministic, b: hybrid, c: AI-driven). Tests must validate determinism claims per category -- we do not claim end-to-end determinism where it does not exist.
3. **Dogfooding is not optional.** Phase 3 validation uses the rules engine in its own pipeline. This is the ultimate integration test. If the engine cannot govern its own delivery, it is not ready.

---

## 2. Component Test Approach

### 2.1 C1: `condition_evaluator.py` -- Extracted BRE Core

**Test level**: Unit tests (Python, `unittest` or plain `assert` scripts)

**What to test**:

| Area | Tests | Priority |
|------|-------|----------|
| Operator coverage | All 12 operators: ==, !=, >, <, >=, <=, IN, NOT IN, IS NULL, IS NOT NULL, MATCHES, .length | Must Have |
| Logical operators | AND, OR, NOT -- including 3+ levels of nesting | Must Have |
| Dot-notation field access | Nested paths, missing paths (return None), .length on lists | Must Have |
| BRE equivalence | Run original BRE test cases against extracted module; results must match | Must Have |
| Error handling | Malformed conditions (missing `field`, unknown operator, invalid AND/OR structure) raise ValueError | Must Have |
| Edge cases | Empty context, empty condition, null values, zero-length lists, deeply nested dicts (5+ levels) | Should Have |
| Utility builders | `field_equals`, `all_of`, `any_of`, `none_of`, `field_matches_pattern` produce valid condition structures | Must Have |

**Test cases**: US-01 T1-T17 from stories (17 cases). Add:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T18 | Empty AND | `{"AND": []}` | True (vacuous truth, matches BRE behavior) |
| T19 | Empty OR | `{"OR": []}` | False (vacuous falsehood) |
| T20 | Null context value with == | `eq("x", null)`, `context={"x": null}` | True |
| T21 | Numeric string comparison | `gt("score", 80)`, `context={"score": "90"}` | ValueError or defined coercion behavior -- must match BRE |
| T22 | Regex with special chars | `MATCHES` with `".*\\.py$"` | Correctly evaluates regex |

**Determinism test**: Run each of T1-T17 ten times. All 10 results must be identical. (These are pure functions operating on immutable data, so this is a sanity check confirming no hidden state.)

**Coverage target**: 100% line coverage on `condition_evaluator.py`. This module is the foundation; zero untested paths.

---

### 2.2 C2: `delivery_rules_adapter.py` -- Delivery-Flow Adapter

**Test level**: Unit tests (Python) + determinism replay tests

**What to test**:

| Area | Tests | Priority |
|------|-------|----------|
| 4-layer resolution | Layer 1 only, L1+L2, L1+L2+L3, L1+L2+L3+L4, L4 blocked in strict mode | Must Have |
| Merge semantics | Scalar last-writer-wins, list replace (default), list extend (`_merge: extend`), map shallow-merge | Must Have |
| `evaluate_routing()` | All 6 project types x 3 risk tolerances (18 combinations minimum) return correct RoutingDecision | Must Have |
| `evaluate_gate()` | GO, RECYCLE, HOLD, ESCALATE decisions based on score/threshold/critical rules | Must Have |
| `evaluate_escalation()` | Max iterations, repeated failure, deadlock, CONTINUE vs ESCALATE | Must Have |
| Critical rule override | Critical failure forces RECYCLE regardless of overall score | Must Have |
| HOLD threshold | Score between `threshold * 0.7` and `threshold` produces HOLD | Must Have |
| Immutability | Resolved rule set cannot be mutated after init | Should Have |
| Error handling | Missing rules_dir, malformed JSON files, missing preset file | Must Have |

**Test cases**: US-03 T1-T12, US-14 T1-T8 from stories.

**Determinism test (N-run replay)**:
- Call `evaluate_routing()` with the same context 10 times per combination.
- Serialize each result to JSON via `json.dumps(sort_keys=True)`.
- Assert all 10 outputs are byte-identical.
- Repeat for `evaluate_gate()` and `evaluate_escalation()`.
- **Script**: A dedicated `test_determinism.py` that loops N=10 (configurable) and compares outputs.

**Coverage target**: 95% line coverage. The remaining 5% may be defensive error paths that are difficult to trigger from unit tests.

---

### 2.3 C3: `yaml_to_rules.py` -- Translation Layer

**Test level**: Unit tests (Python)

**What to test**:

| Area | Tests | Priority |
|------|-------|----------|
| Key mapping | `pass_threshold.design` -> `gates.design_dod.pass_threshold`, `routing_overrides.BUG_FIX.architect` -> `routing.BUG_FIX.architect`, `escalation_sensitivity` -> `escalation.sensitivity` | Must Have |
| Custom rule translation | `rules.custom` list -> valid condition structures accepted by `condition_evaluator` | Must Have |
| Type validation | Numeric thresholds reject strings, enums reject unknown values, validator names reject unknowns | Must Have |
| YAML coercion detection (default mode) | `yes`/`no`/`on`/`off` as booleans, `3.10` as `3.1` -> warning logged, value preserved | Must Have |
| YAML coercion detection (strict mode) | Same coercion patterns -> hard error, no value reaches output | Must Have |
| Empty input | `{}` -> empty overrides, no warnings, no errors | Must Have |
| Preset validation | Only `solo`, `standard`, `strict` accepted | Must Have |

**Test cases**: US-06 T1-T12 from stories.

**YAML coercion-specific tests**:

| # | Scenario | Input | Default Mode Expected | Strict Mode Expected |
|---|----------|-------|-----------------------|----------------------|
| YC-1 | Boolean `yes` where string expected | `{"strict_mode": True}` (AI parsed `yes` as True) | Warning: "YAML type coercion detected for key strict_mode" | Error in `errors` list |
| YC-2 | Float truncation | `{"pass_threshold": {"design": 3.1}}` (was `3.10`) | Warning logged | Error in `errors` list |
| YC-3 | `on`/`off` as boolean | `{"some_flag": True}` (was `on`) | Warning logged | Error in `errors` list |
| YC-4 | `no` as boolean | `{"some_flag": False}` (was `no`) | Warning logged | Error in `errors` list |
| YC-5 | Valid string passes clean | `{"preset": "solo"}` | No warning | No error |
| YC-6 | Valid numeric passes clean | `{"pass_threshold": {"design": 90}}` | No warning | No error |

**Important constraint**: The translation layer receives Python values from the orchestrator (AI), not raw YAML. It cannot detect all coercion cases (e.g., it cannot distinguish `True` that was originally `yes` vs `True` that was originally `true`). Tests must validate the detection boundary honestly.

**Coverage target**: 95% line coverage.

---

### 2.4 C4: `evaluate_rules.py` -- CLI Entry Point

**Test level**: Integration tests (end-to-end Bash invocation)

**What to test**:

| Area | Tests | Priority |
|------|-------|----------|
| Routing invocation | Valid context file -> exit 0, valid JSON on stdout | Must Have |
| Gate invocation | Valid context with validator statuses -> exit 0, valid gate JSON | Must Have |
| Escalation invocation | Valid context with iteration data -> exit 0, escalation JSON | Must Have |
| Missing context file | Non-existent path -> exit 1, error on stderr | Must Have |
| Malformed context JSON | Invalid JSON -> exit 1, parse error on stderr | Must Have |
| Rule evaluation error | Missing required field -> exit 2, error JSON on stderr | Must Have |
| Dry-run no side effects | `--dry-run` -> exit 0, no audit file written, no state mutation | Must Have |
| Dry-run with compare | `--dry-run --compare` -> output includes `comparison` key | Must Have |
| Config integration | `--config` with Layer 3 overrides -> overrides visible in output | Must Have |
| No config (L1+L2 only) | Omit `--config` -> defaults + standard preset | Must Have |
| Stdout is valid JSON | `json.loads(stdout)` succeeds for all success paths | Must Have |
| Performance | Standard routing evaluation < 500ms | Must Have |

**Integration test pattern**:

```bash
# Write fixture context to temp file
echo '{"project": {"type": "FEATURE", "risk_tolerance": "standard"}}' > /tmp/test-ctx.json

# Invoke the CLI
OUTPUT=$(python delivery-team/scripts/evaluate_rules.py \
  --context /tmp/test-ctx.json \
  --rules-dir delivery-team/skills/delivery-flow/references/rules/ \
  --decision-type routing 2>/tmp/test-stderr.txt)
EXIT_CODE=$?

# Assert exit code
[ "$EXIT_CODE" -eq 0 ] || echo "FAIL: expected exit 0, got $EXIT_CODE"

# Assert valid JSON
echo "$OUTPUT" | python -c "import sys,json; json.load(sys.stdin)" || echo "FAIL: invalid JSON"

# Assert routing structure present
echo "$OUTPUT" | python -c "
import sys, json
d = json.load(sys.stdin)
assert d['decision_type'] == 'routing'
assert 'routing' in d
assert len(d['routing']) == 7
print('PASS')
"
```

**Determinism test (Bash-level N-run replay)**:

```bash
# Run the same invocation 10 times, capture outputs
for i in $(seq 1 10); do
  python evaluate_rules.py --context ctx.json --rules-dir rules/ \
    --decision-type routing > /tmp/run_$i.json
done

# Compare all outputs to run_1
for i in $(seq 2 10); do
  diff /tmp/run_1.json /tmp/run_$i.json || echo "FAIL: run $i differs"
done
```

**Test cases**: US-07 T1-T12 from stories.

**Coverage target**: All CLI argument combinations tested. 90% code coverage on `evaluate_rules.py`.

---

### 2.5 C5-C8: Rule JSON Files (routing, dod-gates, escalation, collaboration)

**Test level**: Structural validation (Python scripts that parse and validate JSON)

| File | Validation | Priority |
|------|-----------|----------|
| `routing.json` | 126 cells (6 types x 7 stages x 3 risks), all values "full" or "light", zero gaps | Must Have |
| `routing.json` | Every "light" cell has non-empty `scope_constraint` in metadata | Must Have |
| `routing.json` | BUG_FIX/standard matches PRD: Idea=light, Refine=light, Design=light, Architect=light, Plan=light, Development=full, UAT=full | Must Have |
| `dod-gates.json` | All 7 stages have gate definitions | Must Have |
| `dod-gates.json` | Every rule has `rule_id`, `name`, `condition`, `metadata.weight`, `metadata.determinism_category` | Must Have |
| `escalation.json` | All 3 sensitivity profiles present (relaxed, balanced, aggressive) with correct thresholds | Must Have |
| `collaboration.json` | All 6 project types x 7 stages have pattern assignments | Must Have |
| `presets/*.json` | Valid JSON, schema-valid, correct override values per PRD | Must Have |

**Test cases**: US-05 T1-T10, US-09 T1-T10, US-10 T1-T10, US-11 T1-T7 from stories.

**Coverage target**: 100% of JSON files structurally validated. Every cell, every rule, every preset.

---

### 2.6 C9-C11: Preset Profile Rule Sets

**Test level**: Unit tests via adapter (load preset, verify resolved values)

| Preset | Key Assertions |
|--------|---------------|
| Solo | 1 validator per gate, escalation threshold=2, UAT=light for FEATURE/standard, `strict_mode=false` |
| Standard | Default validator set, escalation threshold=3, balanced routing |
| Strict | All stages=full, security validator on every gate, `strict_mode=true`, warnings blocking |

**Test cases**: US-08 T1-T10 from stories.

---

## 3. 4-Layer Resolution Testing

The 4-layer resolution system (Plugin Defaults -> Presets -> Per-Repo Config -> Per-Run Override) is the most nuanced piece to test. Each test scenario below verifies a specific layer interaction.

### 3.1 Layer Precedence Scenarios

| # | Scenario | L1 | L2 (Preset) | L3 (Config) | L4 (Runtime) | Strict? | Expected Resolved Value |
|---|----------|-----|-------------|-------------|--------------|---------|------------------------|
| LP-1 | L1 only | threshold=80 | none | none | none | no | 80 |
| LP-2 | L2 overrides L1 | threshold=80 | threshold=70 (solo) | none | none | no | 70 |
| LP-3 | L3 overrides L2 | threshold=80 | threshold=70 (solo) | threshold=90 | none | no | 90 |
| LP-4 | L4 overrides L3 | threshold=80 | threshold=70 | threshold=90 | threshold=85 | no | 85 |
| LP-5 | L4 blocked in strict | threshold=80 | threshold=95 (strict) | none | threshold=70 | yes | 95 |
| LP-6 | L3 partial override | threshold=80 (all stages) | none | design=90 | none | no | design=90, others=80 |
| LP-7 | L4 cannot swap preset | preset=solo | N/A | none | preset=strict | no | solo (L4 cannot change preset) |
| LP-8 | L4 relaxes L3 with confirmation | threshold=80 | none | threshold=90 | threshold=70 | no | Confirmation prompt triggered |

### 3.2 Merge Semantics Scenarios

| # | Scenario | L1 Value | Higher Layer Value | `_merge` | Expected |
|---|----------|----------|-------------------|----------|----------|
| MS-1 | Scalar replace | 80 | 90 | N/A | 90 |
| MS-2 | List replace (default) | ["po", "arch"] | ["po", "qa"] | none | ["po", "qa"] |
| MS-3 | List extend | ["po", "arch"] | ["sec"] | extend | ["po", "arch", "sec"] |
| MS-4 | Map shallow merge | {x:1, y:2} | {y:3, z:4} | N/A | {x:1, y:3, z:4} |
| MS-5 | Map no deep merge | {a: {b:1, c:2}} | {a: {b:3}} | N/A | {a: {b:3}} (shallow -- c is lost) |

---

## 4. YAML Coercion Detection Testing

### 4.1 Default Mode (Warn)

| # | YAML Source | AI-Parsed Python Value | Expected Translation Layer Behavior |
|---|-----------|----------------------|-------------------------------------|
| CD-1 | `strict_mode: yes` | `True` (bool) | Warning: coercion detected for `strict_mode` |
| CD-2 | `strict_mode: true` | `True` (bool) | No warning (correct YAML boolean) |
| CD-3 | `version: 3.10` | `3.1` (float) | Warning: coercion detected (trailing zero lost) |
| CD-4 | `preset: on` | `True` (bool) | Warning: expected string "on", got bool True |
| CD-5 | `preset: solo` | `"solo"` (str) | No warning (correct type) |
| CD-6 | `threshold: "90"` | `"90"` (str) | Error: expected numeric, got string (type validation failure, not coercion) |

### 4.2 Strict Mode (Error)

Same inputs as CD-1 through CD-6 above, but:
- CD-1, CD-3, CD-4: Translation halts with error, no coerced value in output.
- CD-2, CD-5: No error (no coercion detected).
- CD-6: Error in both modes (type validation failure).

### 4.3 Detection Boundary (What CANNOT Be Detected)

The translation layer receives Python values after the orchestrator (AI) parses the YAML. This means:

- **Cannot detect**: Whether `True` was originally `yes`, `Yes`, `YES`, `true`, `True`, or `TRUE` in the YAML file. All become Python `True`.
- **Cannot detect**: Whether `3.1` was originally `3.1` or `3.10` in the YAML file. Both are Python `3.1`.
- **Can detect**: Type mismatches (bool where string expected, string where number expected).
- **Can detect**: Value mismatches against known enums (preset must be solo/standard/strict).

Tests must not claim to detect coercion that the layer structurally cannot detect. Test assertions must reflect this boundary.

---

## 5. Dogfooding Test Plan (Phase 3)

### 5.1 Objective

Run the delivery-flow pipeline for the rules engine feature itself with the rules engine active for all flow-control decisions. This is the ultimate integration test: the engine governs its own delivery.

### 5.2 Preconditions

- All Phase 0-2 code is complete and passes unit/integration tests.
- Phase 3 audit trail and SKILL.md integration are complete.
- `.delivery/config.yml` is configured with `rules.preset: standard` (eating our own cooking with default settings).

### 5.3 Execution Plan

| Step | Action | Verification |
|------|--------|-------------|
| D-1 | Start a delivery-flow pipeline run for the rules engine feature | Pipeline initializes and invokes `evaluate_rules.py` for initial routing |
| D-2 | Verify routing decision | Audit log shows routing entry with `determinism_category: "a"` |
| D-3 | Progress through each stage (Refine, Design, Architect, Plan, Development, UAT) | At each stage, DoD gate evaluation uses `evaluate_rules.py` |
| D-4 | Verify every gate decision is rule-based | Audit log: zero `category: "c"` entries for decision_type in (routing, gate, escalation) |
| D-5 | Trigger at least one self-correction loop | Escalation rules govern iteration limits |
| D-6 | Complete pipeline run | Full audit log produced |

### 5.4 Validation Checks (Post-Run)

| # | Check | Method | Pass Criteria |
|---|-------|--------|--------------|
| DF-1 | No AI flow control | Scan audit log for `determinism_category: "c"` with `decision_type` in (routing, gate, escalation) | Zero matches |
| DF-2 | All decision points logged | Count decision points in pipeline vs audit log entries | 1:1 correspondence, no gaps |
| DF-3 | Determinism proof | Extract 10 routing evaluations from audit log, replay each with same `input_context` through `evaluate_rules.py` | All 10 produce byte-identical output to original |
| DF-4 | Audit completeness | Read audit JSONL line by line | Every line is valid JSON with all required fields |
| DF-5 | Chronological ordering | Compare timestamps across entries | Monotonically increasing |
| DF-6 | Phase 1 exit criteria | Routing determinism | 10+ identical routing results for same input |
| DF-7 | Phase 2 exit criteria | Gate evaluation | All gates use rules engine, no AI fallback |
| DF-8 | Phase 3 exit criteria | Audit + SKILL.md | Complete audit trail, SKILL.md defers all flow control |
| DF-9 | Retrospective produced | Check for retrospective artifact | Document exists with lessons learned |

### 5.5 Dogfooding Failure Protocol

If the dogfooding run surfaces a defect:

1. Log the defect with: decision point, expected behavior, actual behavior, audit log excerpt.
2. Fix the defect in the rules engine code.
3. Re-run the affected pipeline stages (not the full pipeline -- resume from the stage where the defect occurred).
4. Verify the fix by replaying the same input through the corrected engine.
5. Add the scenario to the regression test suite.

---

## 6. Coverage Targets

| Component | Target | Rationale |
|-----------|--------|-----------|
| `condition_evaluator.py` (C1) | 100% line | Foundation module. Zero untested paths. |
| `delivery_rules_adapter.py` (C2) | 95% line | Core adapter. 5% allowance for hard-to-trigger defensive paths. |
| `yaml_to_rules.py` (C3) | 95% line | Translation layer with coercion detection. |
| `evaluate_rules.py` (C4) | 90% line | CLI integration. Some paths depend on file system state. |
| Rule JSON files (C5-C8) | 100% structural | Every cell, every rule, every preset validated. |
| Preset profiles (C9-C11) | 100% structural + behavioral | Every preset loaded and resolved values verified. |
| **Overall project target** | 95% weighted average | Weighted by component criticality (C1 weighs most). |

### 6.1 What Coverage Means Here

- **Line coverage** on Python modules: every line of code is executed by at least one test.
- **Structural coverage** on JSON files: every cell/rule/key is validated by a parsing script.
- **Behavioral coverage**: every documented behavior (from stories) has at least one test that exercises it.
- **Determinism coverage**: every component that claims determinism has an N-run replay test.

---

## 7. What CANNOT Be Tested Structurally (Empirical UAT Items)

The following items require runtime observation, user judgment, or AI behavior assessment. They cannot be validated by unit/integration tests and must be evaluated empirically during UAT.

### 7.1 AI-Derived Input Quality (Determinism Category C)

| Item | Why Structural Testing Fails | UAT Approach |
|------|------------------------------|--------------|
| Project type auto-detection accuracy | AI classifies natural language descriptions. No deterministic mapping exists. | Present 20 project descriptions. Have 3 humans classify independently. Compare AI classification against human consensus. Measure agreement rate. |
| Validator pass/fail quality | AI judges artifact quality against criteria. Subjective assessment. | Same artifact evaluated by 3 independent AI runs. Measure inter-run agreement. Flag items with < 80% agreement for criteria refinement. |
| Artifact quality review content | AI produces review text. Content quality is subjective. | PO reviews 10 representative artifact reviews for actionability, completeness, and accuracy. |

### 7.2 Orchestrator Compliance

| Item | Why Structural Testing Fails | UAT Approach |
|------|------------------------------|--------------|
| SKILL.md correctly defers all flow control | The orchestrator is AI reading SKILL.md instructions. Compliance depends on prompt adherence. | Run 5 pipeline instances. Audit each for any flow-control decision made without invoking `evaluate_rules.py`. The bypass detection hook can catch violations, but hook coverage depends on runtime context. |
| Error handling UX in default mode | Three-option prompt presentation depends on orchestrator behavior. | Inject errors during 3 pipeline runs. Verify the user sees exactly "Retry", "Skip this gate (AI evaluation)", or "Abort" each time. |
| Layer 4 confirmation prompt | When L4 relaxes L3, user should see a confirmation. This is orchestrator behavior. | Deliberately apply a L4 override that relaxes a L3 value. Verify prompt appears. |

### 7.3 End-to-End Pipeline Behavior

| Item | Why Structural Testing Fails | UAT Approach |
|------|------------------------------|--------------|
| Pipeline duration predictability | Depends on AI processing time for artifacts, which varies. | Record total pipeline time across 5 runs of the same project type. Calculate variance. Target: < 20% coefficient of variation on stage count and gate decisions (not on wall-clock time). |
| Setup wizard UX | W-11/W-12/W-13 question flow depends on AI presentation. | Walk 3 different personas through the wizard. Verify correct pre-selection, conditional display of W-12, and correct config output. |
| Dry-run trust | Users must trust that dry-run output matches actual behavior. | Run dry-run, then actual pipeline. Diff routing decisions. Document any discrepancies. |

### 7.4 Compliance and Audit Readiness

| Item | Why Structural Testing Fails | UAT Approach |
|------|------------------------------|--------------|
| Audit trail sufficiency for SOC2 | Whether the audit trail satisfies an actual auditor is a human judgment call. | Present sample audit logs to a compliance reviewer (or proxy). Get explicit sign-off on field completeness and format. |
| Determinism category accuracy | Whether a decision point is correctly tagged as "a", "b", or "c" requires understanding the full decision context. | Review 20 audit entries. For each, verify the determinism category matches the classification in PRD Section 5. |

---

## 8. Test Execution Order

Tests execute in dependency order, matching the phased delivery:

### Phase 0: Foundation

1. `condition_evaluator.py` unit tests (US-01 T1-T17 + T18-T22)
2. `condition_evaluator.py` N-run determinism tests
3. Routing Decision Specification structural validation (US-02 T1-T8)

**Phase 0 exit gate**: 100% condition evaluator tests pass. Specification is complete and PO-approved.

### Phase 1: Routing and Core Engine

4. `yaml_to_rules.py` unit tests (US-06 T1-T12)
5. YAML coercion detection tests (CD-1 through CD-6, both modes)
6. `delivery_rules_adapter.py` unit tests -- routing (US-03 T1-T12)
7. `delivery_rules_adapter.py` 4-layer resolution tests (LP-1 through LP-8)
8. `delivery_rules_adapter.py` merge semantics tests (MS-1 through MS-5)
9. `routing.json` structural validation (126-cell completeness)
10. Preset profile tests (US-08 T1-T10)
11. `evaluate_rules.py` integration tests -- routing (US-07 T1-T12)
12. `evaluate_rules.py` N-run determinism tests (Bash-level)
13. Pipeline context builder tests (US-04 T1-T8)

**Phase 1 exit gate**: Routing is deterministic. 10 identical results for same input. All integration tests pass.

### Phase 2: Gates, Escalation, Config

14. `dod-gates.json` structural validation (US-09 T1-T10)
15. `delivery_rules_adapter.py` unit tests -- gate evaluation (US-09 tests)
16. `escalation.json` structural validation (US-10 T1-T10)
17. `delivery_rules_adapter.py` unit tests -- escalation (US-10 tests)
18. `collaboration.json` structural validation (US-11 T1-T7)
19. Config schema v2.4 validation (US-12 T1-T10)
20. Error handling tests (US-13 T1-T10)
21. Rule override mechanism tests (US-14 T1-T8)

**Phase 2 exit gate**: All gate/escalation decisions are rule-based. Config schema validated. Error handling works in both strict and default modes.

### Phase 3: Integration, Audit, Dogfooding

22. Audit trail tests (US-15 T1-T11)
23. SKILL.md integration review (US-16 T1-T8)
24. Setup wizard tests (US-17 T1-T8)
25. Dry-run tests (US-18 T1-T7)
26. Dogfooding validation run (US-19 T1-T7, DF-1 through DF-9)
27. Empirical UAT items (Section 7)

**Phase 3 exit gate**: Dogfooding passes. Audit trail complete. Zero category (c) flow-control decisions.

---

## 9. Test Infrastructure

### 9.1 Test File Locations

```
delivery-team/scripts/tests/
  test_condition_evaluator.py      # C1 unit tests
  test_delivery_rules_adapter.py   # C2 unit tests
  test_yaml_to_rules.py            # C3 unit tests
  test_determinism.py              # N-run replay tests (all components)
  test_rule_json_structure.py      # C5-C8 structural validation
  test_preset_profiles.py          # C9-C11 behavioral tests
  test_evaluate_rules_integration.sh  # C4 end-to-end Bash tests
  fixtures/
    contexts/                      # Test context JSON files
    configs/                       # Test config YAML files
    expected/                      # Expected output JSON files
```

### 9.2 Running Tests

```bash
# All unit tests
python -m pytest delivery-team/scripts/tests/ -v

# Or without pytest (plain assert scripts)
python delivery-team/scripts/tests/test_condition_evaluator.py
python delivery-team/scripts/tests/test_delivery_rules_adapter.py
python delivery-team/scripts/tests/test_yaml_to_rules.py

# Determinism replay tests
python delivery-team/scripts/tests/test_determinism.py --runs 10

# Integration tests (Bash)
bash delivery-team/scripts/tests/test_evaluate_rules_integration.sh

# Structural validation
python delivery-team/scripts/tests/test_rule_json_structure.py
```

### 9.3 Test Data Management

- **Fixture contexts**: Pre-built context JSON files for each project type x risk tolerance combination. Stored in `fixtures/contexts/`.
- **Expected outputs**: Golden files for determinism comparison. Generated once, version-controlled.
- **Config fixtures**: Pre-built config files for each test scenario (no rules, solo preset, strict preset, custom overrides).

---

## 10. Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| BRE extraction introduces subtle behavioral differences | High -- foundation is wrong | Run every original BRE test case against extracted module. Diff results. |
| YAML coercion detection has false negatives | Medium -- silent corruption in strict mode | Document detection boundary explicitly (Section 4.3). Do not claim what cannot be detected. |
| N-run replay tests pass trivially (pure functions are always deterministic) | Low -- false confidence | Replay tests also verify correctness, not just consistency. Add state-dependent scenarios (e.g., time-based rules). |
| Dogfooding run masks defects by using simple project type | Medium -- edge cases untested | Configure dogfooding run as FEATURE/standard. Also run dry-run previews for BUG_FIX, GAME_DEV, and SPIKE to verify routing diversity. |
| 500ms performance target fails under load | Low -- single-evaluation invocation | Benchmark with the largest realistic context (all 7 stages, all validators, all artifacts). If close to 500ms, profile and optimize. |
| Layer 4 testing requires orchestrator cooperation | Medium -- cannot unit test L4 confirmation prompt | Unit test the resolution logic (L4 blocked in strict, L4 granular override). UAT tests the prompt behavior. |

---

## 11. Traceability Matrix

| PRD Goal | Stories | Test Strategy Section | Test Type |
|----------|---------|----------------------|-----------|
| G1: Deterministic Routing | US-01, US-02, US-03, US-05, US-08 | 2.1, 2.2, 2.4, 2.5, 2.6 | Unit + determinism replay + integration |
| G2: Rule-Based DoD Gates | US-09, US-03 (adapter) | 2.2, 2.5 | Unit + structural validation |
| G3: User-Configurable Rules | US-06, US-12, US-14, US-08 | 2.3, 3.1, 3.2 | Unit + layer resolution scenarios |
| G4: Full Audit Trail | US-15 | 5.4, 8 (Phase 3) | Integration + dogfooding |
| G5: AI Stays in Its Lane | US-16, US-19 | 5.3, 7.2 | Dogfooding + empirical UAT |
| DD1: Hybrid JSON/YAML | US-06 | 2.3, 4.1, 4.2, 4.3 | Unit + coercion detection |
| DD2: 4-Layer Resolution | US-03, US-14 | 3.1, 3.2 | Unit (all 8 precedence scenarios) |
| NFR-01: < 500ms | US-07 T9 | 2.4 | Integration (benchmark) |
| NFR-02: Determinism proof | All routing/gate stories | 2.1-2.4 determinism tests | N-run replay at every level |
