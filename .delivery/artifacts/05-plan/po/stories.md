# User Stories: Deterministic Rules Engine Integration

**Version**: 1.0
**Author**: Gandalf (Product Owner)
**Date**: 2026-03-28
**Status**: Implementation-Ready
**Traces To**: PRD v2.1, Architecture v1.0

> *"I will not say: do not weep; for not all stories are implementation-ready. But these ones are."*

---

## Story Point Scale

Fibonacci: 1, 2, 3, 5, 8, 13. One point equals roughly one focused session of work for a single developer. Stories above 8 points should be decomposed further before sprint commitment.

---

## Phase 0: BRE Extraction and Routing Decision Specification

Phase 0 establishes the reusable foundation. Nothing else can begin until the condition evaluator is proven equivalent to the original BRE and the routing specification is PO-approved.

---

### US-01: BRE Condition Evaluator Extraction

**As a** delivery-flow developer building a rules engine adapter,
**I want** the BRE's condition evaluation logic extracted into a standalone `condition_evaluator.py` module with zero SQLite dependency,
**So that** I can reuse the proven evaluation logic (AND/OR/NOT, field comparisons, pattern matching) without coupling delivery-flow to the prd-quality-gate-flow database schema.

**Story Points**: 5
**Priority**: Must Have
**Traces To**: PRD FR-01, US-02
**Component**: C1 (`delivery-team/scripts/condition_evaluator.py`)

**Acceptance Criteria**:

1. **Given** the existing `BusinessRulesEngine` class in `prd-quality-gate-flow/business_rules_engine.py`, **When** the methods `_evaluate_condition`, `_get_field_value`, `_compare_values`, `_extract_field_paths`, and `_extract_relevant_context` are extracted into `delivery-team/scripts/condition_evaluator.py`, **Then** the extracted module has zero imports from `prd-quality-gate-flow`, zero references to `sqlite3`, and zero references to database tables or connections.

2. **Given** the extracted `condition_evaluator.py` module, **When** the public API exposes `evaluate_condition(condition, context)`, `evaluate_condition_with_details(condition, context)`, `get_field_value(field_path, context)`, and `extract_field_paths(condition)`, **Then** each function signature matches the architecture specification (Section 2.1) and accepts only `Dict`/`str`/`Any` types -- no SQLite row objects.

3. **Given** the BRE's existing condition evaluation test cases, **When** run against `condition_evaluator.py` using equivalent context dictionaries instead of SQLite rows, **Then** every test produces identical pass/fail results as the original BRE.

4. **Given** a condition tree with nested AND/OR/NOT operators (3+ levels deep), **When** evaluated by `condition_evaluator.py`, **Then** the result matches the original BRE's evaluation for the same condition tree and context.

5. **Given** an invalid condition format (missing `field` key, unknown operator, malformed AND/OR), **When** passed to `evaluate_condition()`, **Then** a `ValueError` is raised with a descriptive message identifying the malformed element.

6. **Given** the extraction is complete, **When** the original `business_rules_engine.py` is inspected, **Then** it retains its own copy of the extracted methods unchanged -- no import from `condition_evaluator.py` is introduced (parallel module, not refactor).

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Field equality | `condition={"field": "project.type", "operator": "==", "value": "FEATURE"}`, `context={"project": {"type": "FEATURE"}}` | `True` |
| T2 | Field inequality | Same condition with `context.project.type = "BUG_FIX"` | `False` |
| T3 | Nested AND | `{"AND": [field_equals("a", 1), field_equals("b", 2)]}`, `context={"a": 1, "b": 2}` | `True` |
| T4 | Nested AND partial fail | Same condition, `context={"a": 1, "b": 3}` | `False` |
| T5 | Nested OR | `{"OR": [field_equals("a", 1), field_equals("a", 2)]}`, `context={"a": 2}` | `True` |
| T6 | NOT operator | `{"NOT": field_equals("a", 1)}`, `context={"a": 2}` | `True` |
| T7 | Deep nesting (3 levels) | `{"AND": [{"OR": [eq("a",1), eq("a",2)]}, {"NOT": eq("b",3)}]}`, `context={"a":2, "b":4}` | `True` |
| T8 | MATCHES pattern | `{"field": "name", "operator": "MATCHES", "value": "^feat/.*"}`, `context={"name": "feat/login"}` | `True` |
| T9 | IN operator | `{"field": "type", "operator": "IN", "value": ["FEATURE","BUG_FIX"]}`, `context={"type": "FEATURE"}` | `True` |
| T10 | IS NULL | `{"field": "missing", "operator": "IS NULL"}`, `context={"missing": null}` | `True` |
| T11 | IS NOT NULL | `{"field": "present", "operator": "IS NOT NULL"}`, `context={"present": 42}` | `True` |
| T12 | .length accessor | `{"field": "items.length", "operator": ">=", "value": 3}`, `context={"items": [1,2,3]}` | `True` |
| T13 | Dot-notation nested | `get_field_value("project.tech.stack", {"project": {"tech": {"stack": "Python"}}})` | `"Python"` |
| T14 | Missing path returns None | `get_field_value("x.y.z", {"x": {"y": {}}})` | `None` |
| T15 | Invalid condition format | `evaluate_condition({"bad": "format"}, {})` | `ValueError` raised |
| T16 | extract_field_paths | `extract_field_paths({"AND": [eq("a.b", 1), eq("c.d", 2)]})` | `["a.b", "c.d"]` |
| T17 | evaluate_condition_with_details | `evaluate_condition_with_details(eq("x", 5), {"x": 5})` | `ConditionResult(passed=True, fields_evaluated={"x": 5})` |

**Dependencies**: Access to `prd-quality-gate-flow/business_rules_engine.py` source code.

---

### US-02: Routing Decision Specification

**As a** Product Owner defining what correct routing looks like,
**I want** a normative specification that explicitly defines the intended routing for every combination of project type (6) x stage (7) x risk tolerance (3),
**So that** the rules engine has an authoritative, PO-approved source of truth -- not a reverse-engineering of inconsistent AI behavior.

**Story Points**: 8
**Priority**: Must Have
**Traces To**: PRD FR-18, US-01
**Artifact**: `delivery-team/delivery-flow/references/routing-decision-spec.md`

**Acceptance Criteria**:

1. **Given** the 6 project types (GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, DOCS_ONLY), 7 stages (Idea, Refine, Design, Architect, Plan, Development, UAT), and 3 risk tolerances (low, standard, high), **When** the specification is complete, **Then** every combination (6 x 7 x 3 = 126 cells) has an explicit depth value of "full" or "light" with no gaps or "TBD" entries.

2. **Given** any cell in the routing table, **When** the depth is "light", **Then** the specification includes a scope constraint describing what "light" means for that specific project type + stage combination (e.g., "BUG_FIX + Design + light: scope limited to impact analysis on affected components only").

3. **Given** the specification, **When** reviewed against the PRD's out-of-scope section (OOS-8), **Then** GAME_DEV is handled as a project type in the routing table combined with the solo preset, not as a separate preset.

4. **Given** the completed specification, **When** the PO signs off, **Then** the sign-off is recorded as a dated entry at the top of the document (e.g., "Approved by PO on 2026-03-28").

5. **Given** the specification, **When** compared to the PRD's US-01 AC-3 (BUG_FIX default routing), **Then** the specification's BUG_FIX + standard risk row matches: Idea=light, Refine=light, Design=light, Architect=light, Plan=light, Development=full, UAT=full.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Completeness check | Count all cells in routing table | 126 cells (6 x 7 x 3), zero blank |
| T2 | All values valid | Scan every cell value | Each is exactly "full" or "light" |
| T3 | Light scope constraints | Filter all "light" cells | Each has an accompanying scope constraint string (non-empty) |
| T4 | BUG_FIX/standard matches PRD | Read BUG_FIX row, standard risk | Idea=light, Refine=light, Design=light, Architect=light, Plan=light, Development=full, UAT=full |
| T5 | GREENFIELD/high is heavyweight | Read GREENFIELD row, high risk | All 7 stages = full |
| T6 | DOCS_ONLY is lightweight | Read DOCS_ONLY row, standard risk | Development=full, all others=light |
| T7 | SPIKE is time-boxed | Read SPIKE row, standard risk | Idea=light, Refine=light, Design=light, Architect=light, Plan=light, Development=full, UAT=light |
| T8 | PO sign-off present | Check document header | Contains dated approval line |

**Dependencies**: None (this is a specification artifact, not code).

---

## Phase 1: Stage Routing Rules and Foundation

Phase 1 builds the core engine: adapter, context builder, translation layer, evaluation script, and routing rules. By the end of Phase 1, routing decisions are deterministic.

---

### US-03: Delivery Rules Adapter

**As a** delivery-flow orchestrator,
**I want** a `DeliveryRulesAdapter` class that wraps the condition evaluator and provides delivery-flow-specific decision methods (routing, gate, escalation),
**So that** I can call a single adapter interface for all flow-control decisions without understanding the underlying condition evaluation mechanics.

**Story Points**: 8
**Priority**: Must Have
**Traces To**: PRD FR-02, US-02 (PRD)
**Component**: C2 (`delivery-team/scripts/delivery_rules_adapter.py`)

**Acceptance Criteria**:

1. **Given** the `DeliveryRulesAdapter` class, **When** initialized with `rules_dir`, `preset`, `config_overrides`, and `runtime_overrides`, **Then** it loads rule JSON files from `rules_dir`, applies the 4-layer resolution per architecture Section 2.2 (load defaults, apply preset, apply config overrides, apply runtime overrides if not strict mode), and stores the resolved rule set as an immutable snapshot.

2. **Given** the adapter is initialized without a SQLite connection or any database dependency, **When** `evaluate_routing(context)` is called, **Then** it returns a `RoutingDecision` dataclass with `stages` (Dict[str, str]), `collaboration_patterns` (Dict[str, List[str]]), `preset` (str), `resolution_layers` (Dict[str, int]), and `determinism_category` (str).

3. **Given** the adapter is initialized, **When** `evaluate_gate(gate_id, context)` is called, **Then** it returns a `GateDecision` dataclass with `gate_id`, `decision` (GO/RECYCLE/HOLD/ESCALATE/HALTED), `overall_score`, `passed`, `pass_threshold`, `rule_results` (List[RuleResult]), `reason`, `recommendations`, and `determinism_category`.

4. **Given** a gate with a critical rule that fails, **When** `evaluate_gate()` is called, **Then** the decision is RECYCLE regardless of the overall weighted score, and the reason identifies the critical failure.

5. **Given** a gate where overall_score >= pass_threshold but < pass_threshold and >= pass_threshold * 0.7, **When** `evaluate_gate()` is called, **Then** the decision is HOLD (marginal -- may need review).

6. **Given** identical `rules_dir`, `preset`, `config_overrides`, and `context`, **When** `evaluate_routing()` is called 10 times, **Then** all 10 results are byte-identical when serialized to JSON.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Init with defaults only | `rules_dir` with routing.json, preset="standard", no overrides | Adapter initializes, `get_resolved_rules()` returns Layer 1+2 merged rules |
| T2 | Layer 3 override | config_overrides=`{"gates":{"design_dod":{"pass_threshold":90}}}` | Design gate threshold is 90, others unchanged |
| T3 | Layer 4 blocked in strict | preset="strict", runtime_overrides=`{"gates":{"design_dod":{"pass_threshold":70}}}` | Runtime override ignored, threshold stays at strict default |
| T4 | Routing determinism | Call evaluate_routing 10x with same context | All 10 JSON outputs identical |
| T5 | Gate GO decision | All rules pass, score=95, threshold=80 | `GateDecision(decision="GO", passed=True, overall_score=95)` |
| T6 | Gate RECYCLE on critical fail | Critical rule fails, other rules pass | `decision="RECYCLE"`, reason mentions critical failure |
| T7 | Gate HOLD on marginal | Score=72, threshold=80 (72 >= 80*0.7=56) | `decision="HOLD"` |
| T8 | Gate RECYCLE on low score | Score=40, threshold=80 | `decision="RECYCLE"` |
| T9 | Missing rules_dir | Non-existent path | Raises FileNotFoundError |
| T10 | Merge semantics: scalar | L1 threshold=80, L3 threshold=90 | Resolved threshold=90 |
| T11 | Merge semantics: list replace | L1 validators=["po","arch"], L3 validators=["po","qa"] | Resolved=["po","qa"] |
| T12 | Merge semantics: list extend | L3 validators with `_merge: extend` | Resolved=["po","arch","po","qa"] (appended) |

**Dependencies**: US-01 (condition_evaluator.py), routing.json files.

---

### US-04: Pipeline Context Builder

**As a** rules engine evaluating pipeline decisions,
**I want** the orchestrator to serialize the current pipeline state into a structured context dictionary with dot-notation accessible fields,
**So that** I can evaluate rules against well-defined fields without parsing unstructured data.

**Story Points**: 5
**Priority**: Must Have
**Traces To**: PRD FR-05, US-07 (PRD)
**Component**: Part of C4 or standalone utility

**Acceptance Criteria**:

1. **Given** the pipeline is at any stage, **When** the `PipelineContextBuilder` assembles a context, **Then** the resulting dictionary includes all required field groups: `project.*` (type, risk_tolerance, tech_stack), `stage.*` (number, name, depth, validators), `config.*` (relevant config including rules.*), `artifacts.*` (presence/metadata per artifact), and `run.*` (iteration_count, failure_history).

2. **Given** a context dictionary with `project.type` set to "FEATURE", **When** `get_field_value("project.type", context)` is called, **Then** it returns "FEATURE".

3. **Given** incomplete pipeline state where a validator has not yet run, **When** the context is assembled, **Then** missing validator fields are set to `null` (not omitted from the dictionary) so that IS NULL conditions can evaluate correctly.

4. **Given** the context dictionary, **When** serialized to JSON via `json.dumps()`, **Then** the output is valid JSON and round-trips correctly (`json.loads(json.dumps(context)) == context`).

5. **Given** a pipeline at Stage 4 (Architect) with 3 validators (PO, Architect, QA), **When** the context is assembled, **Then** `stage.validators.po.status`, `stage.validators.architect.status`, and `stage.validators.qa.status` are all present with values of either "passed", "failed", or `null`.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Full context assembly | Pipeline at Stage 4, FEATURE, standard risk, Python | Context dict has all required field groups with correct values |
| T2 | Dot-notation access | Context with nested project.tech.stack | `get_field_value("project.tech.stack", ctx)` returns correct value |
| T3 | Missing validator is null | Stage 2 with no QA validator output yet | `ctx["stage"]["validators"]["qa"]["status"]` is `None` |
| T4 | JSON round-trip | Assembled context | `json.loads(json.dumps(ctx)) == ctx` |
| T5 | All 7 stages representable | Build context for each stage 1-7 | `stage.number` and `stage.name` are correct for each |
| T6 | Artifact presence | Pipeline with PRD artifact existing | `artifacts.prd.exists` is `True` |
| T7 | Artifact absence | Pipeline without architecture doc | `artifacts.architecture.exists` is `False` |
| T8 | Run metadata | After 2 self-correction iterations | `run.iteration_count` is 2 |

**Dependencies**: None (utility module).

---

### US-05: Stage Routing Rules (JSON)

**As a** rules engine evaluating routing decisions,
**I want** a complete set of default routing rules encoded as JSON in `references/rules/routing.json`,
**So that** every routing decision is a deterministic lookup from the Routing Decision Specification -- not an AI interpretation of prose instructions.

**Story Points**: 5
**Priority**: Must Have
**Traces To**: PRD FR-03, FR-15, US-01 (PRD)
**Component**: C5 (`delivery-team/skills/delivery-flow/references/rules/routing.json`)

**Acceptance Criteria**:

1. **Given** `routing.json`, **When** it is loaded and parsed, **Then** it contains routing rules for all 6 project types (GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, DOCS_ONLY) x 7 stages x 3 risk tolerances, matching the Routing Decision Specification (US-02) cell for cell.

2. **Given** a context with `project.type = "BUG_FIX"` and `project.risk_tolerance = "standard"`, **When** the routing rules are evaluated, **Then** the result is: Idea=light, Refine=light, Design=light, Architect=light, Plan=light, Development=full, UAT=full.

3. **Given** the same context and routing rules evaluated 10 times, **When** comparing all 10 outputs, **Then** all 10 are byte-identical JSON.

4. **Given** a context with `project.type = "GREENFIELD"` and `project.risk_tolerance = "high"`, **When** routing rules are evaluated, **Then** all 7 stages are "full".

5. **Given** each "light" entry in the routing rules, **When** inspected, **Then** the rule metadata includes a `scope_constraint` string that describes what "light" means for that combination (carried from the Routing Decision Specification).

6. **Given** a project type not in the known set (e.g., "UNKNOWN"), **When** routing rules are evaluated, **Then** the evaluation fails with exit code 2 and an error message identifying the unknown project type.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | BUG_FIX/standard routing | type=BUG_FIX, risk=standard | Idea=light, Refine=light, Design=light, Architect=light, Plan=light, Development=full, UAT=full |
| T2 | GREENFIELD/high routing | type=GREENFIELD, risk=high | All 7 stages=full |
| T3 | DOCS_ONLY/standard routing | type=DOCS_ONLY, risk=standard | Development=full, all others=light |
| T4 | SPIKE/standard routing | type=SPIKE, risk=standard | Development=full, UAT=light, all others=light |
| T5 | GAME_DEV/low routing | type=GAME_DEV, risk=low | Fast paths for iteration stages |
| T6 | FEATURE/standard routing | type=FEATURE, risk=standard | Balanced depth across stages |
| T7 | Determinism (10 runs) | Same input 10x | Byte-identical output |
| T8 | Unknown project type | type="UNKNOWN" | Error exit code 2 |
| T9 | All 126 cells covered | Iterate all combinations | No combination returns error or default fallback |
| T10 | Light scope constraints | Filter all "light" results | Each has non-empty scope_constraint in metadata |

**Dependencies**: US-02 (Routing Decision Specification), US-01 (condition_evaluator.py).

---

### US-06: YAML-to-JSON Translation Layer

**As a** user who configures rules in `.delivery/config.yml`,
**I want** a translation layer that converts my YAML rule overrides into JSON rule structures the engine understands,
**So that** I never touch JSON directly while the engine evaluates type-safe JSON internally (per DD1).

**Story Points**: 5
**Priority**: Must Have
**Traces To**: PRD FR-10, US-13 (PRD), DD1
**Component**: C3 (`delivery-team/scripts/yaml_to_rules.py`)

**Acceptance Criteria**:

1. **Given** a config with `rules.pass_threshold.design: 90`, **When** `translate_config_to_rules()` processes this, **Then** the output `overrides` dict contains `{"gates": {"design_dod": {"pass_threshold": 90}}}`.

2. **Given** a config with `rules.routing_overrides.BUG_FIX.architect: light`, **When** the translation layer processes this, **Then** the output contains `{"routing": {"BUG_FIX": {"architect": "light"}}}`.

3. **Given** a config with `rules.custom` containing a list of rule objects with `field`, `operator`, and `value` keys, **When** processed, **Then** the output contains valid JSON condition structures that `condition_evaluator.evaluate_condition()` accepts.

4. **Given** YAML-coerced values (`yes` as boolean True, `3.10` as float 3.1) in default mode, **When** the translation layer encounters these, **Then** it preserves the value and logs a warning in `TranslationResult.warnings` with format: `[WARN] YAML type coercion detected for key {key}: value {raw} interpreted as {coerced}. Use quotes for literal strings.`

5. **Given** `strict_mode=True`, **When** any YAML type coercion is detected, **Then** the translation layer returns `TranslationResult` with the coercion listed in `errors` (not warnings), and no coerced value reaches the output overrides.

6. **Given** a rule value that fails type validation (e.g., `pass_threshold: "high"` where a number is expected), **When** processed, **Then** the `errors` list contains a descriptive error and the invalid value is excluded from the output, regardless of mode.

7. **Given** `rules.preset: "solo"`, **When** processed, **Then** the output includes `preset: "solo"` and the adapter uses this to load the solo preset overlay.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Pass threshold mapping | `{"pass_threshold": {"design": 90}}` | `{"gates": {"design_dod": {"pass_threshold": 90}}}` |
| T2 | Routing override mapping | `{"routing_overrides": {"BUG_FIX": {"architect": "light"}}}` | `{"routing": {"BUG_FIX": {"architect": "light"}}}` |
| T3 | Required validators | `{"required_validators": {"development": ["dev","qa","sec"]}}` | `{"gates": {"development_dod": {"required_validators": ["dev","qa","sec"]}}}` |
| T4 | Escalation sensitivity | `{"escalation_sensitivity": "aggressive"}` | `{"escalation": {"sensitivity": "aggressive"}}` |
| T5 | Custom rule translation | `{"custom": [{"field": "a", "operator": "==", "value": 1}]}` | Valid condition structure accepted by evaluator |
| T6 | Boolean coercion warning | `{"strict_mode": True}` (was `yes` in YAML) | Warning logged, value preserved as True |
| T7 | Float coercion warning | `{"pass_threshold": {"design": 3.1}}` (was `3.10`) | Warning logged |
| T8 | Coercion error in strict | `strict_mode=True`, any coercion detected | Error in errors list, no output |
| T9 | Invalid type rejected | `{"pass_threshold": {"design": "high"}}` | Error: "pass_threshold.design must be numeric" |
| T10 | Unknown preset rejected | `{"preset": "turbo"}` | Error: "preset must be one of: solo, standard, strict" |
| T11 | Empty rules section | `{}` | Empty overrides, no warnings, no errors |
| T12 | Nested custom rules | Complex condition with AND/OR | Valid nested JSON condition |

**Dependencies**: US-01 (condition_evaluator.py for validation).

---

### US-07: Evaluation Script (CLI Entry Point)

**As a** delivery-flow orchestrator invoking the rules engine,
**I want** a standalone Python script (`evaluate_rules.py`) that reads context from JSON, evaluates rules, and writes the decision to stdout as JSON,
**So that** rule evaluation is truly code-executed (via Bash tool call) and not prompt-interpreted.

**Story Points**: 8
**Priority**: Must Have
**Traces To**: PRD FR-11, US-12 (PRD), US-16 (PRD)
**Component**: C4 (`delivery-team/scripts/evaluate_rules.py`)

**Acceptance Criteria**:

1. **Given** the orchestrator writes context to `.delivery/tmp/context-<decision_id>.json`, **When** `python evaluate_rules.py --context <path> --rules-dir <path> --decision-type routing` is invoked, **Then** valid routing decision JSON is written to stdout and the script exits with code 0.

2. **Given** `--decision-type gate --gate-id design_dod`, **When** invoked with a valid context containing validator statuses, **Then** the gate decision JSON is written to stdout per the architecture stdout contract (Section 2.4).

3. **Given** `--decision-type escalation`, **When** invoked with context containing iteration count and failure history, **Then** the escalation decision JSON is written to stdout.

4. **Given** a missing context file, **When** the script is invoked, **Then** it exits with code 1 and writes an error message to stderr.

5. **Given** a rule evaluation error (e.g., null field referenced by a non-null rule), **When** the error occurs, **Then** the script exits with code 2 and writes error JSON to stderr per the architecture stderr contract.

6. **Given** the `--dry-run` flag, **When** the script evaluates rules, **Then** it outputs the full decision JSON to stdout but does not write audit log entries and does not mutate any state files.

7. **Given** the `--dry-run --compare` flags, **When** invoked, **Then** the output additionally includes a `comparison` key showing default routing vs current (overridden) routing side by side.

8. **Given** any successful invocation, **When** benchmarked, **Then** the script completes in under 500ms from invocation to stdout output (NFR-01).

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Routing invocation | Valid context, decision-type=routing | Exit 0, valid routing JSON on stdout |
| T2 | Gate invocation | Valid context with validators, decision-type=gate, gate-id=design_dod | Exit 0, valid gate JSON on stdout |
| T3 | Escalation invocation | Context with iteration_count=3, max=3 | Exit 0, escalation decision ESCALATE |
| T4 | Missing context file | Non-existent path | Exit 1, error on stderr |
| T5 | Malformed context JSON | Invalid JSON in context file | Exit 1, parse error on stderr |
| T6 | Rule evaluation error | Context missing required non-null field | Exit 2, error JSON on stderr |
| T7 | Dry-run no side effects | --dry-run flag | Exit 0, JSON on stdout, no audit file created |
| T8 | Dry-run with compare | --dry-run --compare | Output includes `comparison` key |
| T9 | Performance benchmark | Standard routing evaluation | < 500ms end-to-end |
| T10 | Config integration | --config with Layer 3 overrides | Overrides applied in output |
| T11 | No config (L1+L2 only) | No --config arg | Defaults + standard preset used |
| T12 | Stdout is valid JSON | Capture stdout, parse | `json.loads(stdout)` succeeds |

**Dependencies**: US-01 (condition_evaluator.py), US-03 (adapter), US-04 (context builder), US-06 (translation layer), US-05 (routing.json).

---

### US-08: Preset Profile Rule Sets

**As a** user who does not want to write complex YAML configuration,
**I want** preset profiles (solo, standard, strict) shipped as bundled JSON rule sets,
**So that** I get predictable, sensible pipeline behavior with a single `rules.preset` setting.

**Story Points**: 5
**Priority**: Must Have
**Traces To**: PRD FR-07, US-06 (PRD)
**Components**: C9, C10, C11 (`delivery-team/skills/delivery-flow/references/rules/presets/`)

**Acceptance Criteria**:

1. **Given** the `solo.json` preset, **When** applied as Layer 2 overlay on a FEATURE project, **Then** routing is: Idea=light, Refine=light, Design=light, Architect=light, Plan=light, Development=full, UAT=light; 1 validator per gate; escalation threshold=2.

2. **Given** the `strict.json` preset, **When** applied, **Then** all stages=full, security validator added to every gate, warnings promoted to blocking, `strict_mode=true`, full audit trail required with determinism category tagging.

3. **Given** the `standard.json` preset, **When** applied, **Then** it represents the balanced default: default validator set, 3 collaboration patterns enabled, escalation threshold=3.

4. **Given** `rules.preset: solo` and `rules.pass_threshold.development: 95`, **When** resolved, **Then** Development threshold=95 (Layer 3) while all other thresholds use solo defaults (Layer 2). Merge semantics: Layer 3 overrides Layer 2 per key.

5. **Given** each preset file, **When** parsed as JSON, **Then** it is valid JSON with the same schema as the default rule structure (routing depths, pass thresholds, required validators, escalation thresholds, strict_mode flag).

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Solo FEATURE routing | preset=solo, type=FEATURE, risk=standard | All stages light except Development=full |
| T2 | Solo validator count | preset=solo, any gate | 1 validator per gate |
| T3 | Solo escalation threshold | preset=solo | Escalation at 2 iterations |
| T4 | Strict all-full routing | preset=strict, type=FEATURE, risk=standard | All 7 stages=full |
| T5 | Strict security validator | preset=strict, any gate | Security validator present in required list |
| T6 | Strict mode enabled | preset=strict | strict_mode=true in resolved rules |
| T7 | Standard defaults | preset=standard | Matches shipped defaults (Layer 1 + Layer 2 standard = baseline) |
| T8 | L3 override on solo | preset=solo, L3 development threshold=95 | Development=95, others=solo defaults |
| T9 | Valid JSON | Parse each preset file | json.loads succeeds, schema-valid |
| T10 | GAME_DEV + solo | preset=solo, type=GAME_DEV | Fast paths: Design=light, Architect=light |

**Dependencies**: US-05 (routing.json base rules).

---

## Phase 2: DoD Gates, Config Extension, and Escalation

Phase 2 adds structured gate evaluation, escalation rules, collaboration pattern rules, config schema extension, and error handling. By the end of Phase 2, all flow-control decisions are rule-based.

---

### US-09: DoD Gate Rules

**As a** pipeline orchestrator validating stage completion,
**I want** per-validator DoD rules encoded as JSON for each pipeline stage,
**So that** gate pass/fail decisions are evaluated by the rules engine against structured criteria instead of AI interpretation of prose.

**Story Points**: 8
**Priority**: Must Have
**Traces To**: PRD FR-04, US-03 (PRD)
**Component**: C6 (`delivery-team/skills/delivery-flow/references/rules/dod-gates.json`)

**Acceptance Criteria**:

1. **Given** `dod-gates.json`, **When** parsed, **Then** it contains gate definitions for all 7 pipeline stages, each with per-validator rules, weighted scoring configuration, and a default pass threshold.

2. **Given** a stage with 3 DoD validators (PO, Architect, QA), **When** each validator's output is evaluated against per-validator rules, **Then** the rules engine returns pass/fail per validator with score, reason, and the specific condition that was evaluated.

3. **Given** all validators pass and the weighted score is >= the configured pass threshold, **When** the gate is evaluated, **Then** the decision is GO with a rule-by-rule breakdown.

4. **Given** a critical validator fails (e.g., security review on a strict-mode project), **When** the gate is evaluated, **Then** the decision is RECYCLE regardless of overall score, with failure reasons identifying the failed validator and the specific rule.

5. **Given** a validator rule that checks artifact presence (e.g., "ADR exists with at least 3 sections"), **When** the artifact exists with 4 sections, **Then** the rule passes with determinism category "a" (fully deterministic structural check).

6. **Given** a validator rule that checks AI-derived pass/fail status (e.g., "architect validator passed"), **When** evaluated, **Then** the rule is tagged with determinism category "b" (hybrid -- deterministic aggregation of non-deterministic input).

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | All validators pass | 3 validators all passed, threshold=80 | GO, score >= 80 |
| T2 | One non-critical fails | 1 of 3 fails (non-critical), score=67 | RECYCLE (below threshold) or HOLD (if >= threshold * 0.7) |
| T3 | Critical validator fails | Security validator fails | RECYCLE regardless of score |
| T4 | Structural check (artifact) | ADR exists, 4 sections | Rule passes, category="a" |
| T5 | AI-derived check | Validator status="passed" | Rule passes, category="b" |
| T6 | All 7 stages covered | Parse dod-gates.json | 7 gate definitions present |
| T7 | Weighted scoring | Validator weights 10, 20, 10 | Score weighted correctly |
| T8 | Custom threshold | L3 override threshold=90 | Gate uses 90, not default 80 |
| T9 | Zero validators pass | All fail | RECYCLE, score=0 |
| T10 | Marginal score | Score=60, threshold=80 (60 >= 56=80*0.7) | HOLD |

**Dependencies**: US-03 (adapter), US-01 (condition_evaluator.py).

---

### US-10: Escalation Trigger Rules

**As a** pipeline orchestrator managing self-correction loops,
**I want** escalation decisions (max iterations, repeated failure, deadlock) made by rules with configurable sensitivity levels,
**So that** escalation behavior is predictable and not dependent on AI judgment about when to give up.

**Story Points**: 5
**Priority**: Must Have
**Traces To**: PRD FR-08, US-08 (PRD)
**Component**: C7 (`delivery-team/skills/delivery-flow/references/rules/escalation.json`)

**Acceptance Criteria**:

1. **Given** a self-correction loop has iterated 3 times with `pipeline.max_self_correction: 3`, **When** the escalation rule is evaluated, **Then** the decision is ESCALATE with reason "max iterations reached: 3 of 3."

2. **Given** a DoD gate has failed the same validator twice consecutively, **When** the escalation rule is evaluated, **Then** the decision is ESCALATE with reason "repeated validator failure: {validator_name} failed 2 consecutive evaluations."

3. **Given** `rules.escalation_sensitivity: relaxed`, **When** escalation rules are evaluated, **Then** thresholds are: max iterations=5, repeated failure threshold=3, deadlock timeout=10 minutes.

4. **Given** `rules.escalation_sensitivity: aggressive`, **When** escalation rules are evaluated, **Then** thresholds are: max iterations=2, repeated failure threshold=1, deadlock timeout=3 minutes.

5. **Given** `rules.escalation_sensitivity: balanced` (default), **When** escalation rules are evaluated, **Then** thresholds are: max iterations=3, repeated failure threshold=2, deadlock timeout=5 minutes.

6. **Given** escalation rules, **When** evaluated with context where iteration count < max, **Then** the decision is CONTINUE (not escalate).

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Max iterations reached | iteration_count=3, max=3 | ESCALATE, reason="max iterations reached: 3 of 3" |
| T2 | Below max iterations | iteration_count=2, max=3 | CONTINUE |
| T3 | Repeated validator failure | qa failed 2x consecutively | ESCALATE, reason includes "qa" |
| T4 | First-time failure | qa failed 1x | CONTINUE |
| T5 | Relaxed thresholds | sensitivity=relaxed | max=5, repeated=3, deadlock=10min |
| T6 | Aggressive thresholds | sensitivity=aggressive | max=2, repeated=1, deadlock=3min |
| T7 | Balanced thresholds | sensitivity=balanced | max=3, repeated=2, deadlock=5min |
| T8 | Deadlock detected | No progress for > timeout | ESCALATE, reason="deadlock" |
| T9 | Determinism | Same context 10x | Identical ESCALATE/CONTINUE decision |
| T10 | L3 override on sensitivity | Config overrides to relaxed | Relaxed thresholds apply |

**Dependencies**: US-03 (adapter), US-01 (condition_evaluator.py).

---

### US-11: Collaboration Pattern Selection Rules

**As a** pipeline orchestrator selecting collaboration patterns per stage,
**I want** pattern selection driven by deterministic rules based on project type, stage, and config,
**So that** the same project always uses the same collaboration patterns at each stage.

**Story Points**: 3
**Priority**: Must Have
**Traces To**: PRD FR-09, US-09 (PRD)
**Component**: C8 (`delivery-team/skills/delivery-flow/references/rules/collaboration.json`)

**Acceptance Criteria**:

1. **Given** a FEATURE project at Stage 2 (Refine) with `pipeline.collaboration_patterns.refine: [evaluator-optimizer]`, **When** the collaboration pattern rule is evaluated, **Then** the result is `["evaluator-optimizer"]` every time.

2. **Given** the same project type, stage, and config evaluated 10 times, **When** comparing outputs, **Then** all 10 are byte-identical JSON arrays.

3. **Given** a GREENFIELD project at Stage 4 (Architect) with no config overrides, **When** default rules are evaluated, **Then** the pattern includes `["adversarial-review", "debate"]`.

4. **Given** a config override for collaboration patterns at a specific stage, **When** the pattern rule is evaluated, **Then** the Layer 3 override takes precedence over the Layer 1 default.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | FEATURE/Refine default | type=FEATURE, stage=refine, no overrides | Evaluator-optimizer |
| T2 | GREENFIELD/Architect default | type=GREENFIELD, stage=architect, no overrides | adversarial-review + debate |
| T3 | Config override | L3 override refine=["review-board"] | ["review-board"] |
| T4 | Determinism (10 runs) | Same inputs 10x | Identical arrays |
| T5 | All stages have patterns | Evaluate all 7 stages for FEATURE | Each returns a non-empty array |
| T6 | BUG_FIX lightweight patterns | type=BUG_FIX, stage=design | Lighter pattern set than GREENFIELD |
| T7 | DOCS_ONLY patterns | type=DOCS_ONLY | Minimal patterns reflecting low ceremony |

**Dependencies**: US-05 (routing.json for project type context), US-03 (adapter).

---

### US-12: Config Schema Extension (v2.4)

**As a** team configuring their delivery pipeline,
**I want** a `rules` section in the config schema (v2.4) with documented keys for preset, thresholds, routing overrides, and validators,
**So that** I can customize pipeline behavior in YAML and know exactly what keys are available and valid.

**Story Points**: 5
**Priority**: Must Have
**Traces To**: PRD FR-12, US-04 (PRD)
**Modified File**: `delivery-team/skills/delivery-flow/references/config-schema.md`

**Acceptance Criteria**:

1. **Given** config-schema.md, **When** updated to v2.4, **Then** it includes a `rules` section with keys: `preset` (enum: solo/standard/strict), `strict_mode` (boolean), `escalation_sensitivity` (enum: relaxed/balanced/aggressive), `pass_threshold` (map: stage name to number), `routing_overrides` (map: project type to stage depth map), `required_validators` (map: stage name to list of validator names), and `custom` (list of rule objects).

2. **Given** a config with `rules.pass_threshold.design: 90`, **When** validated against the schema, **Then** it passes validation (number type, valid stage name key).

3. **Given** a config with no `rules` section, **When** the pipeline runs, **Then** defaults (Layer 1 + Layer 2 standard preset) apply with no error or warning.

4. **Given** a config with schema version < 2.4, **When** loaded, **Then** the pipeline writes `[MIGRATION] config v{detected} -> v2.4: rules section added with default values` to stderr and applies safe defaults. If conflicting keys exist, it halts with exit code 1.

5. **Given** the schema extension, **When** it follows the established extension protocol in config-schema.md, **Then** the new `rules` section is documented with the same structure and detail level as existing sections.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Valid rules section | All keys present with valid types | Schema validation passes |
| T2 | Missing rules section | No rules key in config | No error, defaults apply |
| T3 | Invalid preset value | `preset: "turbo"` | Validation error: unknown preset |
| T4 | Invalid threshold type | `pass_threshold.design: "high"` | Validation error: must be numeric |
| T5 | Migration from v2.3 | Config with version: "2.3" | Migration warning on stderr, defaults applied |
| T6 | Conflicting keys | v2.3 config with keys that conflict with v2.4 | Exit code 1, stderr lists conflicts |
| T7 | Schema version bump | Check version field | "2.4" |
| T8 | Extension protocol followed | Compare format to existing sections | Same documentation pattern |
| T9 | Per-stage threshold map | `pass_threshold: {design: 90, development: 95}` | Valid, unmentioned stages use defaults |
| T10 | Routing override structure | `routing_overrides: {BUG_FIX: {architect: light}}` | Valid, correct nesting |

**Dependencies**: Existing `config-schema.md` v2.3.

---

### US-13: Error Handling and Fallback Behavior

**As a** developer whose pipeline must not silently fail,
**I want** the pipeline to halt with a clear error message when the rules engine encounters an error, with explicit user choice in non-strict mode,
**So that** I never get a gate decision based on silent AI fallback.

**Story Points**: 5
**Priority**: Must Have
**Traces To**: PRD FR-14, US-11 (PRD)
**Component**: Part of C4 (`evaluate_rules.py`) and C2 (adapter)

**Acceptance Criteria**:

1. **Given** the rules engine raises an exception during evaluation, **When** the orchestrator handles the error, **Then** the pipeline halts with an error message including: the failed rule/gate ID, the exception type and message, and instructions to resume or retry.

2. **Given** `rules.strict_mode: true`, **When** the rules engine encounters any error, **Then** `evaluate_rules.py` exits with code 2, writes error JSON to stderr (`{"gate_id": "...", "error_type": "...", "message": "...", "timestamp": "..."}`), and no AI fallback evaluation is attempted.

3. **Given** `rules.strict_mode: false` (default), **When** the rules engine encounters an error, **Then** the pipeline halts and presents exactly three options: "Retry", "Skip this gate (AI evaluation)", or "Abort". The user's choice is logged in the audit trail with `decision_source: "user_override"`.

4. **Given** the user selects "Skip this gate (AI evaluation)", **When** the override is applied, **Then** the audit trail entry includes `decision_source: "user_override"`, `override_reason: "rules_engine_error"`, and the original error details.

5. **Given** strict mode and any error, **When** the state file is updated, **Then** `.delivery/state.json` contains `status: "HALTED"` and `halt_reason: "rules_engine_error"`.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Strict mode error | strict_mode=true, rule evaluation throws | Exit 2, error JSON on stderr |
| T2 | Strict mode no fallback | strict_mode=true, error occurs | No AI evaluation attempted |
| T3 | Strict mode state update | strict_mode=true, error occurs | state.json: status=HALTED |
| T4 | Default mode error | strict_mode=false, error occurs | Three-option prompt presented |
| T5 | Default mode retry | User selects "Retry" | Evaluation retried |
| T6 | Default mode skip | User selects "Skip" | AI evaluation used, audit logged with decision_source |
| T7 | Default mode abort | User selects "Abort" | Pipeline halted, no evaluation |
| T8 | Error JSON format | Any error | JSON has gate_id, error_type, message, timestamp |
| T9 | Error includes gate ID | Gate evaluation fails | Error message identifies specific gate |
| T10 | Error includes rule ID | Rule evaluation fails | Error message identifies specific rule |

**Dependencies**: US-07 (evaluate_rules.py), US-03 (adapter).

---

### US-14: Rule Override Mechanism (Layer 3 over Layer 2 over Layer 1)

**As a** team with per-repo customizations,
**I want** my config overrides (Layer 3) to take precedence over presets (Layer 2) which take precedence over plugin defaults (Layer 1), with per-key granularity,
**So that** I only override what I need and everything else uses sensible defaults.

**Story Points**: 3
**Priority**: Must Have
**Traces To**: PRD FR-16, DD2
**Component**: Part of C2 (adapter __init__ merge logic)

**Acceptance Criteria**:

1. **Given** Layer 1 default `pass_threshold.design = 80` and Layer 3 override `pass_threshold.design = 90`, **When** resolved, **Then** the effective threshold is 90 (Layer 3 wins).

2. **Given** Layer 2 preset sets `routing.FEATURE.architect = full` and Layer 3 overrides `routing.FEATURE.architect = light`, **When** resolved, **Then** architect depth is "light" (Layer 3 wins).

3. **Given** Layer 3 overrides only `pass_threshold.design`, **When** resolved, **Then** all other thresholds remain at their Layer 1/2 values (per-key override, not all-or-nothing).

4. **Given** a list override without `_merge: extend`, **When** resolved, **Then** the higher layer's list replaces the lower layer's list entirely.

5. **Given** a list override with `_merge: extend`, **When** resolved, **Then** the higher layer's list is appended to the lower layer's list.

6. **Given** a map override, **When** resolved, **Then** shallow-merge applies: higher layer keys override, unmentioned keys from the lower layer are preserved.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Scalar override | L1=80, L3=90 | Resolved=90 |
| T2 | Unmentioned key preserved | L1 has key A=1 and B=2, L3 overrides A=3 | A=3, B=2 |
| T3 | List replace (default) | L1=["a","b"], L3=["c"] | Resolved=["c"] |
| T4 | List extend | L1=["a","b"], L3=["c"] with _merge:extend | Resolved=["a","b","c"] |
| T5 | Map shallow merge | L1={x:1, y:2}, L3={y:3, z:4} | Resolved={x:1, y:3, z:4} |
| T6 | Three-layer cascade | L1=80, L2(solo)=70, L3=90 | Resolved=90 |
| T7 | L2 over L1 only | L1=80, L2(strict)=95, no L3 | Resolved=95 |
| T8 | L4 blocked in strict | L3=90, L4=70, strict_mode=true | Resolved=90 (L4 ignored) |

**Dependencies**: US-03 (adapter), US-08 (presets).

---

## Phase 3: Audit Trail, SKILL.md Integration, Wizard, and Dogfooding

Phase 3 completes the integration: audit logging, SKILL.md updates, setup wizard extension, and the dogfooding validation run. By the end of Phase 3, the rules engine is fully operational and self-validated.

---

### US-15: Structured Audit Trail

**As an** enterprise architect preparing for a SOC2 audit,
**I want** every rule evaluation logged as structured JSON Lines with timestamp, gate ID, rule ID, input context, result, determinism category, and resolution layer,
**So that** I can demonstrate to auditors that gate decisions are rule-based, reproducible, and traceable.

**Story Points**: 5
**Priority**: Must Have
**Traces To**: PRD FR-06, US-05 (PRD)
**Component**: Audit module within C4 (`evaluate_rules.py`)

**Acceptance Criteria**:

1. **Given** any rule evaluation completes, **When** not in dry-run mode, **Then** a JSON log entry is appended to `.delivery/audit/audit-<pipeline_id>.jsonl` containing: `timestamp` (ISO 8601), `pipeline_id`, `stage`, `decision_type`, `gate_id`, `rule_id`, `input_context` (serialized subset), `passed` (boolean), `score` (float), `decision`, `reason`, `determinism_category` (a/b/c), and `resolution_layer` (1/2/3/4).

2. **Given** a completed pipeline run, **When** the audit log is read line by line, **Then** every routing decision and gate evaluation from that run is present and ordered chronologically with no gaps.

3. **Given** an audit log entry tagged with determinism category "a", **When** the same `input_context` is replayed through `evaluate_rules.py`, **Then** the identical decision is produced (reproducibility proof).

4. **Given** `--audit-summary <path>` is invoked, **When** the script processes the JSONL file, **Then** it outputs a human-readable summary including: total evaluations, breakdown by decision type, determinism category distribution, decision distribution, pass rate, and layer usage.

5. **Given** dry-run mode, **When** a rule evaluation completes, **Then** no audit log entry is written.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Audit entry written | Rule evaluation completes | JSONL entry appended to audit file |
| T2 | Entry schema valid | Parse audit entry as JSON | All required fields present with correct types |
| T3 | Chronological order | Multiple evaluations | Timestamps are monotonically increasing |
| T4 | No gaps | Complete pipeline run | Every decision point has a corresponding entry |
| T5 | Reproducibility proof | Replay category "a" entry input_context | Identical decision output |
| T6 | Dry-run no write | --dry-run flag | Audit file not created/modified |
| T7 | Audit summary output | --audit-summary on completed log | Summary includes total, breakdown, pass rate |
| T8 | One file per pipeline | Two pipeline runs | Two separate audit files |
| T9 | Resolution layer recorded | L3 override applied | Entry shows resolution_layer=3 |
| T10 | Determinism category tagged | Structural check vs AI-derived | category="a" vs category="b" |
| T11 | JSONL format | Each line of audit file | Valid JSON (one object per line) |

**Dependencies**: US-07 (evaluate_rules.py), US-03 (adapter).

---

### US-16: SKILL.md Orchestrator Integration

**As a** delivery-flow orchestrator reading SKILL.md instructions,
**I want** clear, unambiguous instructions for deferring all flow-control decisions to the rules engine via Bash tool calls,
**So that** I invoke `evaluate_rules.py` at every decision point instead of making routing/gating decisions inline.

**Story Points**: 5
**Priority**: Must Have
**Traces To**: PRD FR-13, US-14 (PRD)
**Modified File**: `delivery-team/skills/delivery-flow/SKILL.md`

**Acceptance Criteria**:

1. **Given** the updated SKILL.md, **When** the orchestrator reaches a stage routing decision, **Then** SKILL.md instructs it to: (1) assemble context via `PipelineContextBuilder`, (2) write context to `.delivery/tmp/context-<id>.json`, (3) invoke `python evaluate_rules.py --context <path> --rules-dir <path> --decision-type routing` via Bash, (4) parse the JSON response, (5) act on the routing decision.

2. **Given** the updated SKILL.md, **When** the orchestrator reaches a DoD gate, **Then** SKILL.md instructs it to invoke `evaluate_rules.py --decision-type gate --gate-id <id>` for pass/fail determination rather than judging the gate against prose criteria.

3. **Given** the updated SKILL.md, **When** the orchestrator reaches an escalation decision point, **Then** SKILL.md instructs it to invoke `evaluate_rules.py --decision-type escalation`.

4. **Given** any flow-control decision made without invoking the rules engine, **When** detected, **Then** this is a SKILL.md compliance violation detectable by the pipeline bypass detection hook.

5. **Given** the updated SKILL.md, **When** the orchestrator encounters a rules engine error, **Then** SKILL.md instructs it to follow the error handling protocol (US-13): halt in strict mode, present 3 options in default mode.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Routing invocation present | Read SKILL.md routing section | Contains evaluate_rules.py invocation for routing |
| T2 | Gate invocation present | Read SKILL.md gate section | Contains evaluate_rules.py invocation for gate |
| T3 | Escalation invocation present | Read SKILL.md escalation section | Contains evaluate_rules.py invocation for escalation |
| T4 | No inline routing decisions | Search SKILL.md for routing logic | No AI-interpreted routing instructions remain |
| T5 | No inline gate decisions | Search SKILL.md for gate logic | No "judge against criteria" instructions remain |
| T6 | Error handling protocol | Read SKILL.md error section | Strict mode and default mode paths documented |
| T7 | Context assembly instructions | Read SKILL.md context section | PipelineContextBuilder usage documented |
| T8 | Bash tool invocation format | Read SKILL.md invocation section | Exact CLI command with all required args |

**Dependencies**: All Phase 1 and Phase 2 stories (the SKILL.md must reference components that exist).

---

### US-17: Setup Wizard Extension

**As a** new user setting up delivery-flow for the first time,
**I want** the setup wizard to ask me about rule profile and escalation preferences,
**So that** my rules are configured correctly from the start without manual YAML editing.

**Story Points**: 3
**Priority**: Must Have
**Traces To**: PRD FR-17, US-15 (PRD)
**Modified File**: `delivery-team/skills/delivery-flow/references/setup-wizard.md`

**Acceptance Criteria**:

1. **Given** the setup wizard is running, **When** the user reaches question W-11 (Rule Profile), **Then** the wizard presents three options: solo, standard, strict. If the user's Q3 answer was "minimal", solo is pre-selected; "balanced" pre-selects standard; "thorough" pre-selects strict.

2. **Given** the user selects a profile, **When** asked W-12 (Rule Customizations), **Then** this question is shown only if the user explicitly says "customize" or if Q3 auto-detection confidence is below 80%. Otherwise W-12 is skipped.

3. **Given** the user completes W-13 (Escalation Sensitivity), **When** the wizard writes config, **Then** `.delivery/config.yml` contains `rules.preset: {selected}` and `rules.escalation_sensitivity: {selected}`, and any W-12 customizations are written under `rules.custom`.

4. **Given** a user who selects solo and does not customize, **When** the wizard completes, **Then** the config contains exactly two new keys: `rules.preset: solo` and `rules.escalation_sensitivity: {selected}`. No other `rules.*` keys are written.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Q3=minimal auto-maps | Q3 answer="minimal" | W-11 pre-selects solo |
| T2 | Q3=balanced auto-maps | Q3 answer="balanced" | W-11 pre-selects standard |
| T3 | Q3=thorough auto-maps | Q3 answer="thorough" | W-11 pre-selects strict |
| T4 | W-12 shown conditionally | User says "customize" | W-12 displayed |
| T5 | W-12 skipped by default | User accepts profile, no "customize" | W-12 not displayed |
| T6 | Config output | Solo profile, balanced escalation | Config has `rules.preset: solo`, `rules.escalation_sensitivity: balanced` |
| T7 | Custom rules written | User provides W-12 customizations | `rules.custom` key present in config |
| T8 | Minimal config for solo | Solo, no customization | Only 2 rules.* keys in config |

**Dependencies**: Existing setup wizard infrastructure, US-12 (config schema v2.4).

---

### US-18: Dry-Run Preview

**As a** developer configuring delivery-flow rules,
**I want** to preview what the rules engine would decide for my project without running the pipeline,
**So that** I can validate my configuration and predict pipeline behavior before committing to a full run.

**Story Points**: 2
**Priority**: Must Have
**Traces To**: PRD US-16, FR-11
**Component**: Part of C4 (`evaluate_rules.py` `--dry-run` flag)

**Acceptance Criteria**:

1. **Given** `python evaluate_rules.py --context <file> --rules-dir <dir> --config <config> --dry-run`, **When** the script completes, **Then** stdout includes: resolved routing map (7 stage depths), gate pass thresholds per stage, active preset, resolution layer per rule, determinism category per decision point, and estimated stage count. No state files are mutated and no audit entries are written.

2. **Given** a dry-run output, **When** compared to an actual pipeline run with the same context and config, **Then** the routing decisions and gate thresholds are identical (dry-run is a faithful preview).

3. **Given** `--dry-run --compare`, **When** invoked, **Then** the output includes a `comparison` object showing default (Layer 1+2) routing vs current (with overrides) routing side by side, highlighting differences.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Dry-run output complete | --dry-run | All routing, thresholds, preset, layers in output |
| T2 | No side effects | --dry-run | No audit file, no state mutation |
| T3 | Faithful preview | Compare dry-run to actual run | Identical routing decisions |
| T4 | Compare mode | --dry-run --compare | Side-by-side default vs overridden |
| T5 | Compare highlights diffs | L3 overrides present | Differences marked in comparison output |
| T6 | Compare no diffs | No overrides | Comparison shows all values identical |
| T7 | Exit code 0 | --dry-run succeeds | Exit code is 0 |

**Dependencies**: US-07 (evaluate_rules.py).

---

### US-19: Dogfooding Validation

**As a** team building the rules engine,
**I want** the rules engine validated by running delivery-flow through its own pipeline with the engine active,
**So that** we prove the engine works in a real pipeline context before shipping it to users.

**Story Points**: 5
**Priority**: Must Have
**Traces To**: PRD US-10
**Artifact**: Dogfooding run results + audit log

**Acceptance Criteria**:

1. **Given** the rules engine is implemented (Phases 0-2 complete plus Phase 3 audit/SKILL.md), **When** a delivery-flow pipeline run for the rules engine feature itself uses the rules engine for routing and gating, **Then** all routing and gate decisions are made by the rules engine -- verified by the audit log showing zero category (c) decisions for flow control.

2. **Given** the dogfooding run, **When** the audit log is reviewed, **Then** every decision point has a corresponding audit entry with determinism category (a) or (b).

3. **Given** the dogfooding run completes, **When** 10 routing evaluations from the run are replayed with identical inputs, **Then** all 10 produce byte-identical results (determinism proof).

4. **Given** the dogfooding run completes, **When** validated against Phase 1-3 exit criteria, **Then** all exit criteria pass: routing determinism (Phase 1), gate evaluation (Phase 2), audit completeness (Phase 3).

5. **Given** the dogfooding run encounters any issues, **When** documented, **Then** a retrospective is produced that captures lessons learned and any rules engine improvements identified during the run.

**Test Cases**:

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | No category (c) flow control | Audit log from dogfooding run | Zero entries with category="c" and decision_type in (routing, gate, escalation) |
| T2 | All decision points logged | Audit log completeness | Every routing + gate + escalation decision has an entry |
| T3 | Determinism proof | Replay 10 routing evaluations | All 10 byte-identical |
| T4 | Phase 1 exit criteria | Routing determinism check | 10+ identical routing results |
| T5 | Phase 2 exit criteria | Gate evaluation check | All gates use rules engine, no AI fallback |
| T6 | Phase 3 exit criteria | Audit + SKILL.md check | Complete audit trail, SKILL.md defers all flow control |
| T7 | Retrospective produced | Dogfooding run completes | Retrospective document exists with lessons learned |

**Dependencies**: All other stories (US-01 through US-18).

---

## Story Dependency Graph

```
Phase 0:
  US-01 (Condition Evaluator) ──────┐
  US-02 (Routing Spec)        ──────┤
                                    │
Phase 1:                            ▼
  US-03 (Adapter)         ◄── US-01
  US-04 (Context Builder)
  US-05 (Routing Rules)   ◄── US-01, US-02
  US-06 (Translation Layer) ◄── US-01
  US-07 (Eval Script)     ◄── US-01, US-03, US-04, US-05, US-06
  US-08 (Presets)          ◄── US-05
                                    │
Phase 2:                            ▼
  US-09 (DoD Gate Rules)   ◄── US-01, US-03
  US-10 (Escalation Rules) ◄── US-01, US-03
  US-11 (Collab Patterns)  ◄── US-03, US-05
  US-12 (Config Schema)
  US-13 (Error Handling)   ◄── US-03, US-07
  US-14 (Rule Overrides)   ◄── US-03, US-08
                                    │
Phase 3:                            ▼
  US-15 (Audit Trail)     ◄── US-03, US-07
  US-16 (SKILL.md)        ◄── All Phase 1+2
  US-17 (Setup Wizard)    ◄── US-12
  US-18 (Dry-Run)         ◄── US-07
  US-19 (Dogfooding)      ◄── All US-01 through US-18
```

## Summary

| Phase | Stories | Total Points |
|-------|---------|-------------|
| Phase 0 | US-01, US-02 | 13 |
| Phase 1 | US-03, US-04, US-05, US-06, US-07, US-08 | 36 |
| Phase 2 | US-09, US-10, US-11, US-12, US-13, US-14 | 29 |
| Phase 3 | US-15, US-16, US-17, US-18, US-19 | 20 |
| **Total** | **19 stories** | **98 points** |

## FR Traceability Matrix

| FR | Story |
|----|-------|
| FR-01 | US-01 |
| FR-02 | US-03 |
| FR-03 | US-05 |
| FR-04 | US-09 |
| FR-05 | US-04 |
| FR-06 | US-15 |
| FR-07 | US-08 |
| FR-08 | US-10 |
| FR-09 | US-11 |
| FR-10 | US-06 |
| FR-11 | US-07, US-18 |
| FR-12 | US-12 |
| FR-13 | US-16 |
| FR-14 | US-13 |
| FR-15 | US-05 |
| FR-16 | US-14 |
| FR-17 | US-17 |
| FR-18 | US-02 |
