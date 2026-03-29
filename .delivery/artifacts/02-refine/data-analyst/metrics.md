# Success Metrics: Deterministic Rules Engine Integration

**Author**: Data Analyst
**Date**: 2026-03-28
**PRD Version**: 2.0
**Status**: Draft

---

## North Star Metric

**Flow Control Determinism Rate**

- **Definition**: The percentage of flow control decisions (routing, gating, escalation, depth selection, collaboration pattern selection) made by the rules engine rather than AI judgment, where identical structured inputs produce identical outputs. Per PRD v2.0 Section 5, determinism is measured from the point structured input enters the rules engine -- not end-to-end from user description to output.
- **Formula**: `(deterministic_rule_decisions / total_flow_control_decisions) * 100`
- **Baseline**: 0% (all flow control decisions are currently AI-interpreted)
- **Target**: 100%
- **Data source**: `.delivery/audit/audit-<pipeline_id>.jsonl` entries with `decision_source` field and `determinism_category` tag (a/b/c per Section 5)
- **Measurement cadence**: Per pipeline run (continuous)

---

## Goal Metrics

### G1: Deterministic Stage Routing

#### M1.1 -- Routing Reproducibility Rate

- **Definition**: The percentage of routing evaluations that produce byte-identical JSON output when run with identical structured inputs across N repeated trials.
- **Formula**: `(identical_output_runs / total_repeated_runs) * 100` where N >= 10 per input set
- **Baseline**: Not measurable (no structured routing output exists; persona interviews confirm non-deterministic behavior across all 5 personas)
- **Target**: 100% (zero variance across any number of identical runs)
- **Data source**: Automated reproducibility test harness comparing JSON output of `evaluate_rules.py` across repeated runs with identical input context
- **Measurement cadence**: Per release (regression test), and on-demand during development

#### M1.2 -- Routing Rule Coverage

- **Definition**: The number of project type + stage + risk tolerance combinations covered by explicit routing rules, out of the total possible combinations per FR-18 Routing Decision Specification.
- **Formula**: `(project_type_stage_risk_triples_with_rules / (6 project_types * 7 stages * 3 risk_tolerances)) * 100`
- **Baseline**: 0 explicit rules (all routing encoded in SKILL.md prose)
- **Target**: 100% (126/126 combinations have explicit rules in `references/rules/routing.json`)
- **Data source**: `references/rules/routing.json` rule inventory cross-referenced against Routing Decision Specification
- **Measurement cadence**: Per release

#### M1.3 -- AI-to-Rule Routing Equivalence

- **Definition**: The percentage of routing decisions where the rules engine produces the same stage depth map as the Routing Decision Specification (FR-18). Note: the specification is normative, not observed AI behavior. Divergences from AI behavior are intentional corrections, not regressions.
- **Formula**: `(matching_decisions / total_test_cases) * 100`
- **Baseline**: N/A (rules engine does not exist yet)
- **Target**: 100% match against the Routing Decision Specification. >= 95% match against common AI routing patterns (remaining differences documented as intentional corrections).
- **Data source**: Side-by-side comparison test log (Phase 1 exit criteria)
- **Measurement cadence**: Phase 1 exit gate only

---

### G2: Rule-Based DoD Gate Evaluation

#### M2.1 -- AI Gate Decision Rate

- **Definition**: The percentage of DoD gate pass/fail decisions made by AI judgment alone (without rules engine invocation).
- **Formula**: `(ai_only_gate_decisions / total_gate_decisions) * 100`
- **Baseline**: 100% (all gate decisions are AI-interpreted)
- **Target**: 0% (zero gate decisions made by AI judgment alone)
- **Data source**: Audit log entries in `.delivery/audit/`. Every gate decision must have a corresponding `GateEvaluationResult` log entry with `determinism_category` and `resolution_layer`. Gate decisions without audit entries are classified as AI-only.
- **Measurement cadence**: Per pipeline run (continuous)

#### M2.2 -- Gate Result Completeness

- **Definition**: The percentage of gate evaluations that return a complete `GateEvaluationResult` containing all required fields: pass/fail, score, rule-by-rule breakdown, reason, determinism_category, and resolution_layer.
- **Formula**: `(complete_gate_results / total_gate_evaluations) * 100`
- **Baseline**: 0% (no structured gate results exist)
- **Target**: 100%
- **Data source**: Audit log schema validation against `GateEvaluationResult` structure
- **Measurement cadence**: Per pipeline run (continuous)

#### M2.3 -- Per-Validator Rule Coverage

- **Definition**: The number of pipeline stage + validator combinations with explicit DoD rules in `references/rules/dod-gates.json`, out of total combinations.
- **Formula**: `(stage_validator_pairs_with_rules / total_stage_validator_pairs) * 100`
- **Baseline**: 0% (no per-validator rules exist)
- **Target**: 100% of validators defined in `references/rules/dod-gates.json` have explicit pass/fail criteria with weighted scoring
- **Data source**: `references/rules/dod-gates.json` DoD rule inventory
- **Measurement cadence**: Per release

---

### G3: User-Configurable Gate Rules

#### M3.1 -- Config Override Adoption Rate

- **Definition**: The percentage of active pipelines that use at least one Layer 3 (per-repo) custom rule override in their `rules` config section, beyond selecting a preset profile.
- **Formula**: `(pipelines_with_layer3_overrides / total_active_pipelines) * 100`
- **Baseline**: 0% (no rule customization exists)
- **Target**: >= 20% within 3 months of release (indicates the customization surface is useful and discoverable)
- **Data source**: `.delivery/config.yml` files across projects (self-reported or sampled via community survey)
- **Measurement cadence**: Quarterly

#### M3.2 -- Configurable Rule Surface Area

- **Definition**: The number of distinct rule parameters exposed for user override in the config schema v2.4 `rules.*` section.
- **Formula**: Count of unique overridable keys in `rules.*` section of config schema v2.4
- **Baseline**: 0 (no rule configuration surface exists)
- **Target**: Minimum 6 categories: `preset`, `strict_mode`, `escalation_sensitivity`, `pass_threshold` (per-stage), `routing_overrides` (per project type), `required_validators` (per-stage), and `custom` (user-defined rules). Quantified as >= 15 distinct overridable keys.
- **Data source**: `config-schema.md` v2.4 specification
- **Measurement cadence**: Per release

#### M3.3 -- Preset Profile Completeness

- **Definition**: The number of shipped preset profiles that fully configure all rule categories without requiring additional user overrides.
- **Formula**: Count of preset profiles where all rule categories (routing depths, pass thresholds, required validators, escalation thresholds, strict mode flag) have explicit values
- **Baseline**: 0 (no presets exist)
- **Target**: 3 complete profiles (solo, standard, strict) per DD2
- **Data source**: `references/rules/presets/` JSON preset definitions
- **Measurement cadence**: Per release

---

### G4: Full Audit Trail

#### M4.1 -- Audit Coverage Rate

- **Definition**: The percentage of rule evaluations (routing, gating, escalation, collaboration pattern) that have a corresponding audit log entry in `.delivery/audit/audit-<pipeline_id>.jsonl`.
- **Formula**: `(audit_log_entries / total_rule_evaluations_in_run) * 100`
- **Baseline**: 0% (no structured audit trail exists)
- **Target**: 100% (every rule evaluation produces an audit entry)
- **Data source**: Cross-reference audit log entry count against rules engine invocation count from pipeline execution trace
- **Measurement cadence**: Per pipeline run (continuous)

#### M4.2 -- Audit Entry Schema Compliance

- **Definition**: The percentage of audit log entries that contain all required fields: `timestamp` (ISO 8601), `pipeline_id`, `stage`, `gate_id`, `rule_id`, `input_context`, `passed`, `score`, `decision`, `reason`, `determinism_category` (a/b/c), and `resolution_layer` (1/2/3/4).
- **Formula**: `(schema_compliant_entries / total_audit_entries) * 100`
- **Baseline**: N/A (no audit log exists)
- **Target**: 100%
- **Data source**: JSON schema validation of `.delivery/audit/audit-<pipeline_id>.jsonl` files
- **Measurement cadence**: Per pipeline run (continuous)

#### M4.3 -- Audit Reproducibility Rate

- **Definition**: The percentage of audit log entries tagged with `determinism_category: "a"` where replaying the logged `input_context` through the rules engine produces the same `decision` and `passed` result as the original entry.
- **Formula**: `(reproducible_entries / total_category_a_entries_tested) * 100`
- **Baseline**: N/A (no audit log exists)
- **Target**: 100%
- **Data source**: Automated reproducibility test that reads audit log entries and replays them through `evaluate_rules.py`
- **Measurement cadence**: Per release (regression test)

---

### G5: AI Stays in Its Lane

#### M5.1 -- Flow Control Separation Rate

- **Definition**: The percentage of flow control decision points (routing, gating, escalation, depth selection, collaboration pattern selection) that are routed through the rules engine rather than resolved by AI judgment.
- **Formula**: `(rules_engine_decisions / total_flow_control_decision_points) * 100`
- **Baseline**: 0% (100% of flow control is AI-interpreted)
- **Target**: 100%
- **Data source**: Audit log entries. Every flow control decision point in the pipeline must have an audit entry. Decision points without entries indicate AI bypass.
- **Measurement cadence**: Per pipeline run (continuous)

#### M5.2 -- Decision Point Inventory Coverage

- **Definition**: The number of flow control decision points in the delivery-flow SKILL.md that have been identified and mapped to rules engine invocations, out of the total decision points.
- **Formula**: `(mapped_decision_points / total_decision_points_in_skill_md) * 100`
- **Baseline**: 0 mapped (all embedded in SKILL.md prose)
- **Target**: 100% of decision points catalogued and mapped to rules engine calls
- **Data source**: Decision point inventory document (created during Phase 0-1), cross-referenced against SKILL.md audit
- **Measurement cadence**: Per release

#### M5.3 -- AI Creative Domain Preservation

- **Definition**: Qualitative confirmation that artifact quality (code reviews, architecture reviews, UX reviews, brainstorming, feedback synthesis) is not degraded by rules engine integration. Measured by persona-based feedback.
- **Formula**: Average quality score (1-5 Likert scale) from simulated persona reviews of pipeline artifacts, comparing pre- and post-integration samples
- **Baseline**: Current artifact quality scores from user-feedback personas (establish baseline before integration)
- **Target**: No statistically significant regression (post-integration average >= pre-integration average - 0.3)
- **Data source**: `user-feedback` skill persona evaluations on matched artifact pairs
- **Measurement cadence**: Phase 3 exit gate and quarterly thereafter

---

## Layer Adoption Metrics

These metrics track which layers of the 4-layer rule resolution system (DD2) users actually use, enabling data-driven decisions about where to invest in documentation, UX, and defaults.

### LA-1 -- Layer Activation Distribution

- **Definition**: For each pipeline run, which resolution layers contributed at least one active rule to the final resolved rule set.
- **Formula**: Per pipeline run: count of layers (1-4) that contributed at least one override. Aggregated: `(runs_with_layer_N_active / total_runs) * 100` for each layer N.
- **Baseline**: N/A (no layer system exists)
- **Target**: Layer 1 = 100% (always active as foundation). Layer 2 >= 90% (presets expected for nearly all users). Layer 3 >= 20% within 3 months (per-repo customization). Layer 4 is informational only (transient overrides are ephemeral by design).
- **Data source**: Audit log `resolution_layer` field. Each rule evaluation entry records which layer provided the active rule. Aggregate across all entries per run to determine which layers were active.
- **Measurement cadence**: Per pipeline run (continuous), aggregated monthly

### LA-2 -- Layer 3 Override Depth

- **Definition**: The number of distinct rule keys overridden at Layer 3 (per-repo) in a given config, indicating how deeply users customize beyond presets.
- **Formula**: Count of unique `rules.*` keys in `.delivery/config.yml` that are not `rules.preset` or `rules.escalation_sensitivity` (those are Layer 2 selectors, not Layer 3 overrides)
- **Baseline**: 0 (no Layer 3 overrides exist)
- **Target**: Median <= 5 keys (indicates presets are sufficient for most needs), P90 <= 15 keys (power users customize heavily but do not need to configure everything)
- **Data source**: `.delivery/config.yml` analysis across projects
- **Measurement cadence**: Quarterly

### LA-3 -- Layer 4 Usage Frequency

- **Definition**: The percentage of pipeline runs that include at least one Layer 4 (per-run) transient override via natural language.
- **Formula**: `(runs_with_layer4_overrides / total_runs) * 100`
- **Baseline**: N/A (no layer system exists)
- **Target**: Informational only (no target). High usage (> 30%) may indicate Layer 2/3 defaults are insufficient. Low usage (< 5%) suggests the feature is undiscoverable or unnecessary.
- **Data source**: Audit log entries with `resolution_layer: 4`
- **Measurement cadence**: Monthly

### LA-4 -- Layer Conflict Rate

- **Definition**: The percentage of rule evaluations where a higher layer overrode a lower layer value (indicating active customization rather than passive defaults).
- **Formula**: `(evaluations_with_layer_override / total_evaluations) * 100`
- **Baseline**: N/A
- **Target**: Informational only. Tracked to understand the effectiveness of defaults -- a very low override rate (< 5%) means defaults are well-tuned; a very high rate (> 50%) means defaults are poorly matched to user needs.
- **Data source**: Audit log entries that record both the resolved value and the originating layer. A conflict is any evaluation where the active layer is > 1.
- **Measurement cadence**: Monthly

---

## Preset Distribution Metrics

These metrics track adoption patterns across the three preset profiles (solo, standard, strict) to inform future preset tuning, new preset creation, and documentation investment.

### PD-1 -- Preset Selection Distribution

- **Definition**: The percentage of active projects using each preset profile.
- **Formula**: `(projects_with_preset_X / total_projects_with_rules_config) * 100` for X in {solo, standard, strict, none/custom}
- **Baseline**: N/A (no presets exist)
- **Target**: No single preset > 70% (indicates the 3-preset model covers diverse needs). If one preset dominates at > 80%, investigate whether the others are undiscoverable or mispositioned. "None/custom" < 15% (indicates presets are sufficient as starting points).
- **Data source**: `.delivery/config.yml` `rules.preset` values across projects
- **Measurement cadence**: Quarterly

### PD-2 -- Preset-to-Override Ratio

- **Definition**: For each preset, the percentage of users who add Layer 3 overrides on top of the preset.
- **Formula**: `(preset_X_users_with_overrides / total_preset_X_users) * 100` for each preset
- **Baseline**: N/A
- **Target**: Solo < 10% override rate (solo users want zero config). Standard 20-40% override rate (expected customization). Strict < 20% override rate (strict users want maximum defaults enforced, not customized away).
- **Data source**: `.delivery/config.yml` analysis: projects with `rules.preset` set AND additional `rules.*` keys
- **Measurement cadence**: Quarterly

### PD-3 -- Preset Wizard Acceptance Rate

- **Definition**: The percentage of setup wizard runs where the user accepts the auto-detected preset recommendation (from Q3 mapping per DD3) without changing it.
- **Formula**: `(wizard_runs_accepting_recommendation / total_wizard_runs_showing_W11) * 100`
- **Baseline**: N/A (wizard extension does not exist)
- **Target**: >= 70% acceptance rate (indicates auto-detection is accurate and trusted). < 50% triggers investigation into Q3-to-preset mapping logic.
- **Data source**: Setup wizard telemetry (recommended preset vs. selected preset logged during wizard execution)
- **Measurement cadence**: Per release

### PD-4 -- Preset Migration Rate

- **Definition**: The percentage of projects that change their preset profile after initial setup, and the direction of change (e.g., solo -> standard, standard -> strict).
- **Formula**: `(projects_that_changed_preset / total_projects_with_preset) * 100`, with directional breakdown
- **Baseline**: N/A
- **Target**: < 20% migration within first month (indicates initial recommendation was appropriate). Track directional trends: consistent migration toward strict may indicate standard defaults are too lenient.
- **Data source**: Git history of `.delivery/config.yml` showing `rules.preset` value changes over time
- **Measurement cadence**: Quarterly

---

## Guardrail Metrics

These metrics must NOT regress as a result of the rules engine integration. Regression in any guardrail metric is a release blocker.

### GR-1 -- Pipeline Execution Time

- **Definition**: Wall-clock time from pipeline start to pipeline completion for a standard FEATURE project.
- **Formula**: `pipeline_end_timestamp - pipeline_start_timestamp`
- **Baseline**: Establish current average across 5 representative FEATURE runs before integration
- **Target**: No more than 10% increase. Rule evaluation overhead must be < 500ms per decision point (NFR-01). Total added latency across a full pipeline run must be < 5 seconds.
- **Data source**: Pipeline execution timestamps (start/end) from audit log or pipeline state files
- **Measurement cadence**: Per release (benchmark suite)

### GR-2 -- Agent Creative Quality

- **Definition**: Quality of AI-produced artifacts (code, architecture documents, test plans, UX designs) as evaluated by the team's existing DoD validators.
- **Formula**: Average DoD validator pass rate across all stages, measured on matched project types
- **Baseline**: Current DoD pass rates per stage (establish before integration)
- **Target**: No regression. Post-integration pass rates must be >= pre-integration pass rates.
- **Data source**: DoD gate evaluation results from audit log
- **Measurement cadence**: Per release

### GR-3 -- Pipeline Bypass Rate

- **Definition**: The frequency of pipeline bypass detection events (from the existing `pipeline-bypass-detection` hook), indicating developers are invoking skills outside the delivery-flow pipeline.
- **Formula**: `(bypass_events_per_week_post / bypass_events_per_week_pre)`
- **Baseline**: Current bypass event count per week (from hook logs)
- **Target**: No increase. Ideally decrease as determinism builds trust.
- **Data source**: Hook execution logs from `pipeline-bypass-detection` hook
- **Measurement cadence**: Weekly

### GR-4 -- Config Backward Compatibility

- **Definition**: The percentage of existing v2.3 config files that load and operate correctly with the v2.4 schema (automatic migration, default rules applied).
- **Formula**: `(successful_v23_loads / total_v23_configs_tested) * 100`
- **Baseline**: 100% (current configs work with current schema)
- **Target**: 100% (zero breakage for existing configs, per NFR-04)
- **Data source**: Automated migration test suite against sample v2.3 configs
- **Measurement cadence**: Per release (regression test)

### GR-5 -- Rule Evaluation Performance

- **Definition**: P95 latency of a single rules engine invocation (context serialization + rule evaluation + result deserialization).
- **Formula**: P95 of `evaluation_end_timestamp - evaluation_start_timestamp` across all invocations in a pipeline run
- **Baseline**: 0ms (no rules engine exists)
- **Target**: P95 < 500ms. P50 < 200ms (per NFR-01 and persona feedback from Jake).
- **Data source**: Timing data from `evaluate_rules.py` execution (included in audit log or stderr)
- **Measurement cadence**: Per pipeline run (continuous)

### GR-6 -- User Config Complexity

- **Definition**: The number of lines in the `rules.*` section of `.delivery/config.yml` for users who only select a preset (no Layer 3 overrides). Tracks Sarah's concern: "a 200-line YAML file would be a dealbreaker."
- **Formula**: Line count of `rules.*` section in `.delivery/config.yml` for preset-only users
- **Baseline**: 0 lines (no rules section exists)
- **Target**: Preset-only config <= 3 lines (`rules.preset`, `rules.escalation_sensitivity`, and optionally `rules.strict_mode`). Full customization config P90 <= 30 lines.
- **Data source**: `.delivery/config.yml` analysis across projects
- **Measurement cadence**: Quarterly

---

## Metrics Summary Table

| ID | Metric | Baseline | Target | Category |
|----|--------|----------|--------|----------|
| **North Star** | Flow Control Determinism Rate | 0% | 100% | All Goals |
| M1.1 | Routing Reproducibility Rate | Not measurable | 100% | G1 |
| M1.2 | Routing Rule Coverage | 0/126 | 126/126 (100%) | G1 |
| M1.3 | AI-to-Rule Routing Equivalence | N/A | 100% vs spec, >= 95% vs AI | G1 |
| M2.1 | AI Gate Decision Rate | 100% | 0% | G2 |
| M2.2 | Gate Result Completeness | 0% | 100% | G2 |
| M2.3 | Per-Validator Rule Coverage | 0% | 100% | G2 |
| M3.1 | Config Override Adoption Rate | 0% | >= 20% (3mo) | G3 |
| M3.2 | Configurable Rule Surface Area | 0 keys | >= 15 keys | G3 |
| M3.3 | Preset Profile Completeness | 0 profiles | 3 profiles | G3 |
| M4.1 | Audit Coverage Rate | 0% | 100% | G4 |
| M4.2 | Audit Entry Schema Compliance | N/A | 100% | G4 |
| M4.3 | Audit Reproducibility Rate | N/A | 100% | G4 |
| M5.1 | Flow Control Separation Rate | 0% | 100% | G5 |
| M5.2 | Decision Point Inventory Coverage | 0% | 100% | G5 |
| M5.3 | AI Creative Domain Preservation | Establish baseline | No regression | G5 |
| LA-1 | Layer Activation Distribution | N/A | L1=100%, L2>=90%, L3>=20% | Layer Adoption |
| LA-2 | Layer 3 Override Depth | 0 | Median<=5, P90<=15 | Layer Adoption |
| LA-3 | Layer 4 Usage Frequency | N/A | Informational | Layer Adoption |
| LA-4 | Layer Conflict Rate | N/A | Informational | Layer Adoption |
| PD-1 | Preset Selection Distribution | N/A | No single preset > 70% | Preset Distribution |
| PD-2 | Preset-to-Override Ratio | N/A | Solo<10%, Std 20-40%, Strict<20% | Preset Distribution |
| PD-3 | Preset Wizard Acceptance Rate | N/A | >= 70% | Preset Distribution |
| PD-4 | Preset Migration Rate | N/A | < 20% (1mo) | Preset Distribution |
| GR-1 | Pipeline Execution Time | Establish baseline | < 10% increase | Guardrail |
| GR-2 | Agent Creative Quality | Establish baseline | No regression | Guardrail |
| GR-3 | Pipeline Bypass Rate | Current weekly count | No increase | Guardrail |
| GR-4 | Config Backward Compatibility | 100% | 100% | Guardrail |
| GR-5 | Rule Evaluation Performance | N/A | P95 < 500ms | Guardrail |
| GR-6 | User Config Complexity | 0 lines | Preset-only <= 3 lines | Guardrail |

---

## Phase Exit Criteria (Metrics View)

### Phase 0 Exit
- M1.2 preliminary: Routing Decision Specification covers all 126 combinations (6 types x 7 stages x 3 risk tolerances)
- FR-01 validated: extracted `condition_evaluator.py` passes original BRE test cases

### Phase 1 Exit
- M1.1 = 100% (routing reproducibility across 10+ runs)
- M1.2 = 100% (all 126 project type + stage + risk tolerance triples covered)
- M1.3 = 100% match against Routing Decision Specification
- GR-5 P95 < 500ms (performance SLA met)
- LA-1 Layer 1 = 100% (defaults always active)

### Phase 2 Exit
- M2.1 = 0% (zero AI-only gate decisions)
- M2.2 = 100% (all gate results are complete, including determinism_category and resolution_layer)
- M2.3 = 100% (all validators have explicit rules)
- M3.2 >= 15 (config surface area)
- GR-4 = 100% (backward compatibility)
- GR-6 preset-only config <= 3 lines

### Phase 3 Exit
- M4.1 = 100% (audit coverage)
- M4.2 = 100% (audit schema compliance, including determinism_category and resolution_layer fields)
- M4.3 = 100% (audit reproducibility for category (a) entries)
- M3.3 = 3 (all preset profiles shipped: solo, standard, strict)
- M5.1 = 100% (full flow control separation)
- M5.3 no regression (creative quality preserved)
- GR-1 < 10% increase (execution time)
- GR-3 no increase (bypass rate)
- North Star = 100% (flow control determinism)
- PD-1 baseline established (initial preset distribution captured)
- LA-1 all 4 layers operational and tracked

### Dogfooding Exit (US-10)
- All Phase 0-3 exit criteria pass on the rules engine's own pipeline run
- Audit log shows zero category (c) decisions for flow control
- 10 routing evaluations replayed with byte-identical results
