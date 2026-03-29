# Stage 6: Development Notes -- Deterministic Rules Engine

**Feature**: Deterministic Rules Engine for Delivery Pipeline
**Date**: 2026-03-28
**Author**: Bilbo (Technical Writer), summarizing work by Gimli (Developer)
**Sprint Plan**: `05-plan/sprint-plan.md`
**Phases**: 4 (Phase 0-3)

---

## 1. Implementation Summary

### Phase 0: Core Extraction (Foundation)

Extracted the pure condition evaluation logic from the existing Business Rules Engine into a standalone module with zero external dependencies.

- **condition_evaluator.py** (227 lines): 5 public functions (`evaluate_condition`, `get_field_value`, `compare_values`, `extract_field_paths`, `extract_relevant_context`). Supports nested AND/OR/NOT logic, field comparisons, null checks, regex matching, and collection operations. Python stdlib only -- no SQLite, no database references.
- **stage-routing.json** (1034 lines): Complete routing decision specification encoding 126 cells (6 project types x 7 stages x 3 risk tolerances). Each cell defines stage depth, DoD validators, collaboration patterns, and max iterations. Includes formal definitions for depth levels (full, light, skip, full+game) and risk tolerances (standard, solo, strict). Traces to PRD FR-03, FR-15, FR-18, US-02, US-05.

### Phase 1: Adapter, Translation, CLI, Presets

Built the delivery-specific rule resolution and evaluation stack.

- **delivery_rules_adapter.py** (504 lines): 4-layer rule resolution (defaults -> preset -> config -> runtime). Three exported data classes (`StageRouting`, `GateResult`, `ValidatorResult`). Three evaluation functions (`resolve_rules`, `evaluate_stage_routing`, `evaluate_dod_gate`). Weighted scoring for gate evaluation. Imports only from `condition_evaluator`.
- **yaml_to_rules.py** (709 lines): Translation layer converting pre-parsed YAML dicts into JSON rule override structures. Detects YAML coercion artifacts (yes/no -> bool, 3.10 -> 3.1, on/off -> bool). In strict mode, coercion detections become hard errors. Does NOT parse YAML itself -- receives Python dicts from the orchestrator.
- **evaluate_rules.py** (520 lines): CLI entry point with 3 actions (`route`, `gate`, `resolve`). Supports `--dry-run` mode and produces JSON audit trail on stdout. Exit codes: 0 (success), 1 (argument/config error), 2 (rule evaluation error). Invoked by SKILL.md orchestrator via Bash tool.
- **Preset profiles** (3 files in `presets/`):
  - `solo.json` (71 lines): Prototype/solo developer -- fewer validators, faster iteration, warnings non-blocking.
  - `standard.json` (40 lines): Default balanced profile matching SKILL.md Stage Routing Matrix baseline.
  - `strict.json` (86 lines): Enterprise/compliance -- more validators, warnings become blocking, no Layer 4 runtime overrides.
- **dod-gates.json** (574 lines): 55 gate criteria across 7 stages. Each criterion has a unique ID, description, severity level (blocking/warning/informational), assigned validator role, and determinism category (a=fully deterministic, b=hybrid, c=AI-driven). Default pass threshold: 80. Traces to PRD FR-04, US-09.

### Phase 2: Escalation, Collaboration, Config, Wizard

Extended the rules engine with escalation triggers, collaboration pattern rules, config schema additions, and wizard questions.

- **escalation-rules.json** (241 lines): 6 escalation triggers with 3 sensitivity profiles (relaxed, balanced, aggressive). Each trigger maps to an action: escalate_to_human, retry_with_feedback, or abort. Traces to PRD FR-08, US-10.
- **collaboration-patterns.json** (153 lines): Per-stage pattern selection rules. Deterministic mapping of which collaboration patterns run at which stage, for which project type and depth. Fixed execution order. Skip conditions prevent unnecessary patterns at light depth. Traces to PRD FR-09, US-11.
- **config-schema-v2.4-additions.md**: Specifies 12 new config keys under the `rules.*` section (enabled, preset, strict_mode, routing_overrides, gate_overrides, escalation.sensitivity, escalation.max_iterations_override, escalation.repeated_failure_override, dod_overrides, limits_overrides, custom). Ready to merge into config-schema.md, bumping version from 2.3 to 2.4. Traces to PRD FR-12, US-12.
- **wizard-extension.md**: 3 new wizard questions (W-15: Rule Profile, W-16: Rule Overrides, W-17: Escalation Sensitivity). Auto-detect logic maps from existing Q5 (Timeline & Risk Tolerance) answers. Follows established wizard protocol: auto-detect, present, options, record. Traces to US-15, FR-17.

### Phase 3: SKILL.md Integration (Spec Complete, Integration Pending)

- **skill-integration-spec.md**: Comprehensive change specification for wiring the rules engine into `delivery-team/skills/delivery-flow/SKILL.md`. Covers 5 change areas: Phase 0 rules validation on config load, Phase 3 routing evaluation, Phase 4 DoD gate evaluation, post-pipeline audit trail, and error handling/fallback behavior. Includes exact Bash invocation templates. Status: implementation-ready, not yet applied. Traces to US-16, US-17, US-18.

---

## 2. Files Created

### Scripts (delivery-team/scripts/)

| File | Lines | Purpose |
|------|-------|---------|
| `condition_evaluator.py` | 227 | Standalone condition evaluation -- AND/OR/NOT logic, comparisons, regex |
| `delivery_rules_adapter.py` | 504 | 4-layer rule resolution, routing + gate evaluation |
| `yaml_to_rules.py` | 709 | YAML-to-JSON translation with coercion detection |
| `evaluate_rules.py` | 520 | CLI entry point: route, gate, resolve actions |
| **Total** | **1,960** | |

### Rule Specifications (delivery-team/skills/delivery-flow/references/rules/)

| File | Lines | Purpose |
|------|-------|---------|
| `stage-routing.json` | 1,034 | 126-cell routing decision matrix |
| `dod-gates.json` | 574 | 55 gate criteria across 7 stages |
| `escalation-rules.json` | 241 | 6 triggers, 3 sensitivity profiles |
| `collaboration-patterns.json` | 153 | Per-stage pattern selection rules |
| `presets/solo.json` | 71 | Solo/prototype preset |
| `presets/standard.json` | 40 | Default balanced preset |
| `presets/strict.json` | 86 | Enterprise/compliance preset |
| **Total** | **2,199** | |

### Design Artifacts (.delivery/artifacts/06-dev/)

| File | Purpose |
|------|---------|
| `config-schema-v2.4-additions.md` | 12 new config keys for rules.* section |
| `wizard-extension.md` | 3 new wizard questions (W-15, W-16, W-17) |
| `skill-integration-spec.md` | SKILL.md wiring specification (5 change areas) |

---

## 3. Files Modified

None. All work in this feature is net-new files. The SKILL.md integration (Phase 3) is specified but not yet applied -- that is tracked as a CODE_COMPLETE item for UAT.

---

## 4. Verification Status

### Verified (Smoke Tests Passed)

| Component | Test | Result |
|-----------|------|--------|
| `condition_evaluator.py` | Smoke test: nested AND/OR/NOT evaluation against sample context | PASS |
| `delivery_rules_adapter.py` | `resolve` action: 4-layer resolution with standard preset | PASS |
| `delivery_rules_adapter.py` | `route` action: FEATURE/architect -> depth=light confirmed | PASS |

### Not Yet Verified (CODE_COMPLETE for UAT)

| Item | What Needs Validation | Why It Cannot Be Verified Now |
|------|----------------------|-------------------------------|
| SKILL.md integration | Apply skill-integration-spec.md changes, run a full pipeline | Spec written but edits not yet applied to SKILL.md |
| Full pipeline dogfooding | End-to-end pipeline run with rules engine active | Requires SKILL.md integration first |
| Wizard extension UX | Run setup wizard with W-15/W-16/W-17 questions | Requires wizard-extension.md merge into setup-wizard.md |
| Config schema v2.4 merge | Merge 12 new keys into config-schema.md | Requires review and version bump |
| Preset profile coverage | Run pipeline with solo, standard, and strict presets | Requires full integration |
| Escalation trigger firing | Trigger each of the 6 escalation conditions | Requires pipeline iteration loops |
| Coercion detection | Feed YAML with known coercion traps (yes/no, 3.10) | Requires yaml_to_rules integration path |
| Error handling / fallback | Simulate rule engine failure, verify AI fallback | Requires SKILL.md error handling wiring |

---

## 5. Deviations from Plan

None. All four phases implemented as specified in the sprint plan.

---

## 6. Architecture Notes

### Design Principle: Deterministic by Default

The Business Rules Engine is intentionally deterministic -- gate decisions are rule-based, not AI-inferred, to ensure consistent and auditable workflow outcomes. The `rules.enabled: false` config key provides a backward-compatible escape hatch that falls back to prose-based AI routing.

### 4-Layer Resolution Order

```
Layer 1 (Defaults)  ->  Layer 2 (Preset)  ->  Layer 3 (Config)  ->  Layer 4 (Runtime)
   stage-routing.json     solo/standard/strict     .delivery/config.yml     CLI --override flags
```

Each layer can override values set by the previous layer. In strict mode, Layer 4 (runtime) overrides are disabled entirely.

### Zero External Dependencies

All four scripts use Python stdlib only. No pip install, no requirements.txt, no virtual environment. This is deliberate -- the rules engine must work in any environment where Python 3.8+ is available, with no setup step.

---

## 7. Known Issues

None specific to this feature. Pre-existing issue [#50](https://github.com/P47Phoenix/Claude-Plugins/issues/50) (alias injection bug) remains open but is out of scope.
