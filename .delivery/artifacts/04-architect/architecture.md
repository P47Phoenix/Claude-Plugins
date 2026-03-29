# Technical Architecture: Deterministic Rules Engine Integration

**Version**: 1.0
**Date**: 2026-03-28
**Author**: Celebrimbor, Solution Architect (delivery-team)
**Status**: Draft
**Inputs**: PRD v2.1, UX Design v1.0, `business_rules_engine.py`, delivery-flow SKILL.md, config-schema.md v2.3

> *"Let us forge something that will endure beyond the ages."*
>
> This architecture separates what endures (deterministic rule evaluation) from what must remain fluid (AI creative judgment). The boundary between the two is the most important line in this design.

---

## 1. Component Design

### 1.1 Component Map

| # | File | Location | Phase | Description |
|---|------|----------|-------|-------------|
| C1 | `condition_evaluator.py` | `delivery-team/scripts/condition_evaluator.py` | 0 | Extracted BRE condition evaluation core -- zero SQLite dependency |
| C2 | `delivery_rules_adapter.py` | `delivery-team/scripts/delivery_rules_adapter.py` | 1 | Adapter wrapping C1 for delivery-flow decision points |
| C3 | `yaml_to_rules.py` | `delivery-team/scripts/yaml_to_rules.py` | 1 | Translation layer: structured YAML data to JSON rule structures |
| C4 | `evaluate_rules.py` | `delivery-team/scripts/evaluate_rules.py` | 1 | CLI entry point invoked by orchestrator via Bash tool |
| C5 | `routing.json` | `delivery-team/skills/delivery-flow/references/rules/routing.json` | 1 | Default stage routing rules (6 types x 7 stages x 3 risk levels) |
| C6 | `dod-gates.json` | `delivery-team/skills/delivery-flow/references/rules/dod-gates.json` | 2 | Per-validator DoD gate rules for all 7 stages |
| C7 | `escalation.json` | `delivery-team/skills/delivery-flow/references/rules/escalation.json` | 2 | Escalation trigger rules with 3 sensitivity profiles |
| C8 | `collaboration.json` | `delivery-team/skills/delivery-flow/references/rules/collaboration.json` | 2 | Collaboration pattern selection rules |
| C9 | `presets/solo.json` | `delivery-team/skills/delivery-flow/references/rules/presets/solo.json` | 1 | Solo preset profile overlay |
| C10 | `presets/standard.json` | `delivery-team/skills/delivery-flow/references/rules/presets/standard.json` | 1 | Standard preset profile overlay |
| C11 | `presets/strict.json` | `delivery-team/skills/delivery-flow/references/rules/presets/strict.json` | 1 | Strict preset profile overlay |

### 1.2 Modified Files

| File | Change | Phase |
|------|--------|-------|
| `delivery-team/skills/delivery-flow/SKILL.md` | Add rules engine invocation protocol at all decision points | 3 |
| `delivery-team/skills/delivery-flow/references/config-schema.md` | Add `rules.*` section, bump v2.3 to v2.4 | 2 |
| `delivery-team/skills/delivery-flow/references/setup-wizard.md` | Add 3 new questions (W-15, W-16, W-17) | 3 |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | Replace prose criteria with rule-based evaluation instructions | 2 |
| `delivery-team/hooks/check_config.py` | Add `rules.*` key validation | 2 |
| `delivery-team/scripts/generate-schema.py` | Regenerate JSON schema after v2.4 update | 2 |

---

## 2. Component Interfaces

### 2.1 C1: `condition_evaluator.py` -- Extracted BRE Core

**What is extracted from `business_rules_engine.py`**:

| Method | Lines | Extracted? | Rationale |
|--------|-------|-----------|-----------|
| `_evaluate_condition()` | 258-301 | Yes | Pure logic: AND/OR/NOT, MATCHES, field comparisons. No SQLite. |
| `_get_field_value()` | 303-331 | Yes | Dot-notation field access on dictionaries. No SQLite. |
| `_compare_values()` | 333-372 | Yes | Operator dispatch (==, !=, >, <, >=, <=, IN, NOT IN, IS NULL/NOT NULL). No SQLite. |
| `_extract_field_paths()` | 386-407 | Yes | Recursive field path extraction from condition trees. No SQLite. |
| `_extract_relevant_context()` | 374-384 | Yes | Subset extraction of context fields referenced in condition. No SQLite. |
| Utility functions | 469-519 | Yes | `field_equals`, `all_of`, `any_of`, `none_of`, `field_matches_pattern`, etc. |

**What stays behind** (coupled to SQLite, not extracted):

| Method | Lines | Rationale |
|--------|-------|-----------|
| `evaluate_gate()` | 55-208 | Reads gate config from `nodes` table, loads rules from `business_rules` table, logs to `gate_evaluations` and `audit_log` tables. Fully coupled to SQLite schema. |
| `evaluate_rule()` | 210-256 | Reads rule condition from SQLite row format (`json.loads(rule['condition'])`). Thin wrapper over `_evaluate_condition` but tied to SQLite row dict format. |
| `_log_gate_evaluation()` | 409-466 | Writes to `gate_evaluations` and `audit_log` tables. Pure SQLite. |
| `__init__()` | 52-53 | Accepts `sqlite3.Connection`. |

**Public API**:

```python
# condition_evaluator.py

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class ConditionResult:
    """Result of evaluating a single condition tree."""
    passed: bool
    fields_evaluated: Dict[str, Any]  # field_path -> actual_value

def evaluate_condition(condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
    """
    Evaluate a condition tree against a context dictionary.

    Supports: field comparisons (==, !=, >, <, >=, <=, IN, NOT IN,
    IS NULL, IS NOT NULL), logical operators (AND, OR, NOT),
    pattern matching (MATCHES), collection operations (.length).

    Args:
        condition: JSON condition tree (same format as existing BRE)
        context: Dictionary with dot-notation accessible fields

    Returns:
        True if condition is satisfied, False otherwise

    Raises:
        ValueError: Invalid condition format or unknown operator
    """

def evaluate_condition_with_details(
    condition: Dict[str, Any],
    context: Dict[str, Any]
) -> ConditionResult:
    """
    Like evaluate_condition but returns field values that were evaluated.
    Used for audit trail population.
    """

def get_field_value(field_path: str, context: Dict[str, Any]) -> Any:
    """
    Resolve a dot-notation field path against a context dict.
    Supports .length accessor for collections.
    Returns None if path does not resolve.
    """

def extract_field_paths(condition: Dict[str, Any]) -> List[str]:
    """Extract all field paths referenced in a condition tree."""

# Condition builder utilities (unchanged from BRE)
def field_equals(field: str, value: Any) -> Dict: ...
def field_not_equals(field: str, value: Any) -> Dict: ...
def field_greater_than(field: str, value: Any) -> Dict: ...
def field_less_than(field: str, value: Any) -> Dict: ...
def field_is_null(field: str) -> Dict: ...
def field_is_not_null(field: str) -> Dict: ...
def all_of(*conditions) -> Dict: ...
def any_of(*conditions) -> Dict: ...
def none_of(condition: Dict) -> Dict: ...
def field_matches_pattern(field: str, pattern: str) -> Dict: ...
```

**Backward compatibility**: The original `business_rules_engine.py` retains its own copy of these methods (no import from `condition_evaluator.py`). The extraction creates a parallel, decoupled module. Future work may refactor the original BRE to import from `condition_evaluator.py`, but that is out of scope for this feature.

### 2.2 C2: `delivery_rules_adapter.py` -- Delivery-Flow Adapter

This component is the most significant new build. It rebuilds gate orchestration, rule loading, weighted scoring, and decision logic on top of `condition_evaluator.py` without any SQLite dependency.

**Public API**:

```python
# delivery_rules_adapter.py

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class RuleResult:
    """Result of evaluating a single rule."""
    rule_id: str
    rule_name: str
    passed: bool
    score: float           # 0.0 - 100.0
    reason: str
    fields_evaluated: Dict[str, Any]
    determinism_category: str  # "a", "b", or "c"
    resolution_layer: int      # 1, 2, 3, or 4

@dataclass
class GateDecision:
    """Result of evaluating all rules for a gate."""
    gate_id: str
    decision: str          # GO, RECYCLE, HOLD, ESCALATE, HALTED
    overall_score: float
    passed: bool
    pass_threshold: float
    rule_results: List[RuleResult]
    reason: str
    recommendations: List[str]
    determinism_category: str  # Highest non-determinism level across all rules

@dataclass
class RoutingDecision:
    """Result of evaluating stage routing."""
    stages: Dict[str, str]         # stage_name -> "full" | "light"
    collaboration_patterns: Dict[str, List[str]]  # stage_name -> [patterns]
    preset: str
    resolution_layers: Dict[str, int]  # stage_name -> layer that determined depth
    determinism_category: str

class DeliveryRulesAdapter:
    """
    Adapter between condition_evaluator.py and delivery-flow decision points.
    Accepts JSON rule definitions (from files) and context dictionaries.
    No SQLite dependency.
    """

    def __init__(
        self,
        rules_dir: str,          # Path to references/rules/
        preset: str = "standard", # solo | standard | strict
        config_overrides: Optional[Dict[str, Any]] = None,  # Layer 3 from config
        runtime_overrides: Optional[Dict[str, Any]] = None   # Layer 4 ephemeral
    ):
        """
        Initialize with rule sources for all 4 layers.

        Layer resolution order:
          1. Load plugin defaults from rules_dir/*.json
          2. Apply preset overlay from rules_dir/presets/{preset}.json
          3. Apply config_overrides (per-repo, from .delivery/config.yml)
          4. Apply runtime_overrides (per-run, ephemeral)

        All layers are resolved at init time. The resolved rule set is immutable
        for the lifetime of this adapter instance.
        """

    def evaluate_routing(
        self,
        context: Dict[str, Any]
    ) -> RoutingDecision:
        """
        Evaluate stage routing rules.

        Context must include: project.type, project.risk_tolerance, config.*
        Returns: stage depth map, collaboration patterns, resolution metadata
        """

    def evaluate_gate(
        self,
        gate_id: str,
        context: Dict[str, Any]
    ) -> GateDecision:
        """
        Evaluate all rules for a DoD gate.

        Context must include: stage.*, artifacts.*, config.*,
        stage.validators.* (per-validator status)
        Returns: aggregate pass/fail decision with rule breakdown
        """

    def evaluate_escalation(
        self,
        context: Dict[str, Any]
    ) -> GateDecision:
        """
        Evaluate escalation trigger rules.

        Context must include: run.iteration_count, run.failure_history,
        run.repeated_failures, config.rules.escalation_sensitivity
        Returns: ESCALATE or CONTINUE decision
        """

    def get_resolved_rules(self) -> Dict[str, Any]:
        """
        Return the fully resolved rule set (all 4 layers merged).
        Used by --dry-run to show what rules are active.
        """
```

**4-Layer Resolution Logic** (implemented in `__init__`):

```
FUNCTION resolve_layers(rules_dir, preset, config_overrides, runtime_overrides):
    # Layer 1: Plugin defaults
    resolved = load_json(rules_dir / "routing.json")
    merge_into(resolved, load_json(rules_dir / "dod-gates.json"))
    merge_into(resolved, load_json(rules_dir / "escalation.json"))
    merge_into(resolved, load_json(rules_dir / "collaboration.json"))

    # Layer 2: Preset overlay
    preset_file = rules_dir / "presets" / f"{preset}.json"
    IF preset_file exists:
        apply_overlay(resolved, load_json(preset_file))
        # Overlay semantics: scalars replace, lists replace, maps shallow-merge

    # Layer 3: Per-repo config overrides
    IF config_overrides is not None:
        apply_overlay(resolved, config_overrides)
        # Same merge semantics as Layer 2

    # Layer 4: Per-run runtime overrides (strict mode disables this)
    IF runtime_overrides is not None AND NOT resolved.strict_mode:
        apply_overlay(resolved, runtime_overrides)
        # Granular key-level only. Cannot swap preset.

    RETURN resolved
```

**Merge semantics** (per PRD DD2):
- Scalars: last-writer-wins (higher layer replaces lower)
- Lists: last-writer-wins by default; opt-in `_merge: extend` appends
- Maps: shallow-merge (higher layer keys override, unmentioned keys preserved)

**Gate evaluation algorithm** (rebuilt, not extracted from BRE):

```
FUNCTION evaluate_gate(gate_id, context):
    rules = resolved_rules.gates[gate_id].rules
    pass_threshold = resolved_rules.gates[gate_id].pass_threshold

    total_weight = 0
    weighted_score = 0
    critical_failures = []
    results = []

    FOR rule IN rules:
        IF NOT rule.enabled: CONTINUE

        passed = evaluate_condition(rule.condition, context)
        score = 100.0 IF passed ELSE 0.0
        weight = rule.metadata.weight (default 10)
        total_weight += weight

        IF passed:
            weighted_score += weight * score
        ELSE:
            IF rule.metadata.critical:
                critical_failures.append(rule)

        results.append(RuleResult(...))

    overall_score = weighted_score / total_weight IF total_weight > 0 ELSE 0

    IF critical_failures:
        decision = "RECYCLE"
        reason = f"Critical failures: {names}"
    ELIF overall_score >= pass_threshold:
        decision = "GO"
    ELIF overall_score >= pass_threshold * 0.7:
        decision = "HOLD"  # Marginal -- may need review
    ELSE:
        decision = "RECYCLE"

    RETURN GateDecision(...)
```

### 2.3 C3: `yaml_to_rules.py` -- Translation Layer

**Input**: Structured data parsed from `.delivery/config.yml` by the orchestrator. The orchestrator (AI) reads the YAML file and passes structured Python data (dicts/lists/scalars) to this module. This module does NOT parse YAML itself (no `pyyaml` dependency).

**Output**: JSON rule override structures consumable by `DeliveryRulesAdapter` as `config_overrides` (Layer 3).

**Public API**:

```python
# yaml_to_rules.py

from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TranslationResult:
    """Result of translating config overrides to rule structures."""
    overrides: Dict[str, Any]      # Ready for DeliveryRulesAdapter config_overrides
    warnings: List[str]            # YAML coercion warnings (default mode)
    errors: List[str]              # Validation errors (always blocking)

def translate_config_to_rules(
    config_rules_section: Dict[str, Any],
    strict_mode: bool = False
) -> TranslationResult:
    """
    Translate the rules.* section from config into JSON rule overrides.

    Args:
        config_rules_section: The "rules" dict from parsed config YAML.
            Expected keys: preset, strict_mode, escalation_sensitivity,
            pass_threshold, routing_overrides, required_validators, custom.
        strict_mode: If True, YAML type coercion warnings become errors.

    Returns:
        TranslationResult with overrides, warnings, and errors.

    The function:
    1. Validates all values against expected types (numeric thresholds,
       string enums, known validator names).
    2. Detects YAML type coercion (yes/no/on/off, trailing zeros).
    3. Converts config keys to JSON rule override structures.
    4. In strict mode: any coercion detection produces an error, not a warning.
    """

def validate_rule_value(
    key: str,
    value: Any,
    expected_type: type,
    valid_values: Optional[List[Any]] = None
) -> Tuple[Any, Optional[str]]:
    """
    Validate and optionally coerce a single rule value.

    Returns:
        (validated_value, warning_or_None)

    Raises:
        ValueError: Value fails validation (wrong type, not in valid set)
    """
```

**Type coercion detection**:

The translation layer checks for known YAML coercion patterns:
- `yes`/`no`/`on`/`off` interpreted as booleans
- Trailing zeros dropped from floats (e.g., `3.10` becomes `3.1`)
- Bare strings that match YAML reserved words

Since the orchestrator (AI) parses the YAML and passes Python values, the translation layer checks the Python types against expected schema types. If the Python type does not match the expected type (e.g., a boolean where a string is expected), it flags a coercion warning.

**Config-to-JSON mapping examples**:

| Config Key | JSON Override Structure |
|-----------|----------------------|
| `rules.pass_threshold.design: 90` | `{"gates": {"design_dod": {"pass_threshold": 90}}}` |
| `rules.routing_overrides.BUG_FIX.architect: light` | `{"routing": {"BUG_FIX": {"architect": "light"}}}` |
| `rules.required_validators.development: [dev, qa, arch, sec]` | `{"gates": {"development_dod": {"required_validators": ["dev", "qa", "arch", "sec"]}}}` |
| `rules.escalation_sensitivity: aggressive` | `{"escalation": {"sensitivity": "aggressive"}}` |
| `rules.custom` (list of rule objects) | `{"custom_rules": [{condition dict}, ...]}` |

### 2.4 C4: `evaluate_rules.py` -- CLI Entry Point

**Invocation**:

```bash
python delivery-team/scripts/evaluate_rules.py \
  --context .delivery/tmp/context-<decision_id>.json \
  --rules-dir delivery-team/skills/delivery-flow/references/rules/ \
  --config .delivery/config.yml \
  [--decision-type routing|gate|escalation] \
  [--gate-id <gate_id>] \
  [--dry-run] \
  [--compare]
```

**Arguments**:

| Arg | Required | Description |
|-----|----------|-------------|
| `--context` | Yes | Path to JSON file containing the pipeline context dictionary |
| `--rules-dir` | Yes | Path to directory containing default rule JSON files |
| `--config` | No | Path to `.delivery/config.yml` (for Layer 3 overrides). If omitted, only Layers 1+2 apply. |
| `--decision-type` | No | One of: `routing`, `gate`, `escalation`. Default: `routing`. |
| `--gate-id` | Conditional | Required when `--decision-type gate`. The gate to evaluate. |
| `--dry-run` | No | Output full decision JSON without audit writes or state mutations. |
| `--compare` | No | With `--dry-run`, also output side-by-side comparison of overridden vs default routing. |

**Exit codes**:

| Code | Meaning |
|------|---------|
| 0 | Success. Decision JSON on stdout. |
| 1 | Script error (missing files, invalid arguments, malformed JSON). Error message on stderr. |
| 2 | Rule evaluation error (condition evaluation failure, type validation failure in strict mode). Error JSON on stderr. |

**Stdout contract (success, decision-type=routing)**:

```json
{
  "decision_type": "routing",
  "routing": {
    "idea": "light",
    "refine": "light",
    "design": "full",
    "architect": "full",
    "plan": "light",
    "development": "full",
    "uat": "full"
  },
  "collaboration_patterns": {
    "refine": ["evaluator-optimizer"],
    "design": ["review-board"],
    "architect": ["adversarial-review", "debate"],
    "development": ["evaluator-optimizer"],
    "uat": ["consensus"]
  },
  "preset": "standard",
  "resolution_layers": {
    "idea": 2,
    "refine": 2,
    "design": 3,
    "architect": 2,
    "plan": 2,
    "development": 2,
    "uat": 2
  },
  "determinism_category": "a"
}
```

**Stdout contract (success, decision-type=gate)**:

```json
{
  "decision_type": "gate",
  "gate_id": "design_dod",
  "decision": "GO",
  "overall_score": 87.5,
  "passed": true,
  "pass_threshold": 80,
  "rule_results": [
    {
      "rule_id": "design-artifacts-present",
      "rule_name": "Design artifacts exist",
      "passed": true,
      "score": 100.0,
      "reason": "Condition satisfied",
      "determinism_category": "a",
      "resolution_layer": 1
    }
  ],
  "reason": "All checks passed (score: 87.5)",
  "recommendations": [],
  "determinism_category": "b"
}
```

**Stderr contract (error, exit code 2)**:

```json
{
  "gate_id": "design_dod",
  "error_type": "rule_evaluation_error",
  "message": "Field 'stage.validators.architect.status' is null but rule 'arch-review-required' requires a non-null value",
  "timestamp": "2026-03-28T14:32:01Z"
}
```

**Internal flow**:

```
1. Parse CLI arguments (argparse)
2. Read context JSON from --context file
3. Read config YAML overrides:
   a. Orchestrator passes structured data via the context file
      OR config path is read and the rules.* section extracted
   b. Pass rules section to yaml_to_rules.translate_config_to_rules()
   c. If TranslationResult has errors: exit 2 with error JSON
   d. If TranslationResult has warnings: print to stderr
4. Initialize DeliveryRulesAdapter(rules_dir, preset, config_overrides)
5. Based on --decision-type:
   - routing: call adapter.evaluate_routing(context)
   - gate: call adapter.evaluate_gate(gate_id, context)
   - escalation: call adapter.evaluate_escalation(context)
6. Serialize result to JSON, print to stdout
7. If NOT --dry-run: write audit log entry to .delivery/audit/
8. Exit 0
```

### 2.5 Audit Trail (Phase 2)

**JSONL schema** (one JSON object per line in `.delivery/audit/audit-<pipeline_id>.jsonl`):

```json
{
  "timestamp": "2026-03-28T14:32:01.123456Z",
  "pipeline_id": "pipe_20260328_143200",
  "stage": "design",
  "decision_type": "gate",
  "gate_id": "design_dod",
  "rule_id": "design-artifacts-present",
  "input_context": {
    "project.type": "FEATURE",
    "stage.name": "design",
    "stage.depth": "full",
    "artifacts.ux_design.exists": true
  },
  "passed": true,
  "score": 100.0,
  "decision": "GO",
  "reason": "Condition satisfied",
  "determinism_category": "a",
  "resolution_layer": 1
}
```

**Write path**: Synchronous append after each evaluation in `evaluate_rules.py`. The file is opened in append mode, one JSON line is written, and the file is closed. No buffering across evaluations. This is simple and correct; performance is not a concern (file append is sub-1ms).

**Post-run summary**: After a pipeline completes, the orchestrator invokes:

```bash
python delivery-team/scripts/evaluate_rules.py \
  --audit-summary .delivery/audit/audit-<pipeline_id>.jsonl
```

This reads the JSONL file and outputs a human-readable summary:

```
Pipeline: pipe_20260328_143200
Total evaluations: 23
  Routing: 1 (category a)
  Gate: 14 (12 category a, 2 category b)
  Escalation: 8 (category a)
Decisions: 19 GO, 3 RECYCLE, 1 ESCALATE
Pass rate: 82.6%
Layer usage: L1=15, L2=6, L3=2, L4=0
```

### 2.6 Default Rules (Phase 1 -- JSON file structures)

**Directory structure**:

```
delivery-team/skills/delivery-flow/references/rules/
  routing.json           # Stage routing + depth selection rules
  dod-gates.json         # Per-validator DoD gate rules (Phase 2)
  escalation.json        # Escalation trigger rules (Phase 2)
  collaboration.json     # Collaboration pattern selection (Phase 2)
  presets/
    solo.json            # Solo profile overlay
    standard.json        # Standard profile overlay
    strict.json          # Strict profile overlay
```

**`routing.json` structure**:

```json
{
  "version": "1.0",
  "description": "Stage routing rules per Routing Decision Specification",
  "routing_table": {
    "GREENFIELD": {
      "low": {
        "idea": "full", "refine": "full", "design": "full",
        "architect": "full", "plan": "full", "development": "full", "uat": "full"
      },
      "standard": {
        "idea": "full", "refine": "full", "design": "full",
        "architect": "full", "plan": "light", "development": "full", "uat": "full"
      },
      "high": {
        "idea": "light", "refine": "full", "design": "full",
        "architect": "full", "plan": "light", "development": "full", "uat": "light"
      }
    },
    "FEATURE": { "...": "..." },
    "BUG_FIX": { "...": "..." },
    "GAME_DEV": { "...": "..." },
    "SPIKE": { "...": "..." },
    "DOCS_ONLY": { "...": "..." }
  },
  "depth_constraints": {
    "light": {
      "description": "Reduced depth with specific scope. Light means less deep, NEVER skipped.",
      "per_stage": {
        "idea": "Quick signal validation, no deep exploration",
        "refine": "Focused requirements, no exhaustive stakeholder analysis",
        "design": "Visual/gameplay impact only, no full UX research",
        "architect": "Performance/integration validation only, no new ADRs",
        "plan": "Task list only, no detailed estimates or risk analysis",
        "development": "Implementation with minimal patterns, no advanced optimization",
        "uat": "Happy-path validation, no edge-case or persona testing"
      }
    }
  }
}
```

**`presets/solo.json` structure**:

```json
{
  "preset_name": "solo",
  "description": "Minimal ceremony for solo developers and prototypes",
  "overrides": {
    "routing": {
      "FEATURE": {
        "standard": {
          "idea": "light", "refine": "light", "design": "light",
          "architect": "light", "plan": "light", "development": "full", "uat": "light"
        }
      }
    },
    "gates": {
      "default_pass_threshold": 70,
      "max_validators_per_gate": 1
    },
    "escalation": {
      "sensitivity": "relaxed",
      "max_iterations": 2,
      "repeated_failure_threshold": 2,
      "deadlock_timeout_minutes": 10
    },
    "strict_mode": false,
    "warnings_blocking": false
  }
}
```

**`dod-gates.json` structure** (Phase 2):

```json
{
  "version": "1.0",
  "gates": {
    "refine_dod": {
      "pass_threshold": 80,
      "rules": [
        {
          "rule_id": "refine-prd-exists",
          "name": "PRD artifact exists",
          "condition": {
            "field": "artifacts.prd.exists",
            "operator": "==",
            "value": true
          },
          "metadata": {
            "weight": 30,
            "critical": true,
            "determinism_category": "a"
          }
        },
        {
          "rule_id": "refine-prd-sections",
          "name": "PRD has minimum sections",
          "condition": {
            "field": "artifacts.prd.sections.length",
            "operator": ">=",
            "value": 5
          },
          "metadata": {
            "weight": 20,
            "critical": false,
            "determinism_category": "a"
          }
        },
        {
          "rule_id": "refine-po-approved",
          "name": "PO validator passed",
          "condition": {
            "field": "stage.validators.po.status",
            "operator": "==",
            "value": "DONE"
          },
          "metadata": {
            "weight": 50,
            "critical": true,
            "determinism_category": "b"
          }
        }
      ]
    },
    "design_dod": { "...": "..." },
    "architect_dod": { "...": "..." },
    "plan_dod": { "...": "..." },
    "development_dod": { "...": "..." },
    "uat_dod": { "...": "..." }
  }
}
```

---

## 3. Data Flow Diagram

### 3.1 End-to-End Flow for a Single Decision Point

```
                                DECISION POINT
                                (e.g., Stage 3 routing)
                                      |
                                      v
+-------------------+    +--------------------------+
| SKILL.md          |    | Pipeline State           |
| (Orchestrator)    |--->| project.type = FEATURE   |
|                   |    | project.risk = standard  |
|                   |    | stage.name = design      |
|                   |    | stage.validators = {...}  |
|                   |    | config.rules.* = {...}   |
+-------------------+    +--------------------------+
                                      |
                         1. Serialize to JSON
                                      |
                                      v
                         +------------------------+
                         | .delivery/tmp/          |
                         | context-<id>.json       |
                         +------------------------+
                                      |
                         2. Bash tool invocation
                                      |
                                      v
+----------------------------------------------------------------------+
| evaluate_rules.py (Python process)                                   |
|                                                                      |
|  a. Read context JSON                                                |
|  b. Read config -> yaml_to_rules.translate_config_to_rules()         |
|  c. Init DeliveryRulesAdapter(rules_dir, preset, config_overrides)   |
|     - Layer 1: Load routing.json, dod-gates.json, etc.               |
|     - Layer 2: Apply presets/{preset}.json overlay                   |
|     - Layer 3: Apply config overrides                                |
|     - Layer 4: Apply runtime overrides (if not strict mode)          |
|  d. adapter.evaluate_routing(context) or evaluate_gate(gate_id, ctx) |
|     - condition_evaluator.evaluate_condition(rule.condition, context) |
|     - Aggregate weighted scores                                      |
|     - Determine decision (GO/RECYCLE/HOLD/ESCALATE)                  |
|  e. Serialize decision to JSON -> stdout                             |
|  f. Write audit log entry (unless --dry-run)                         |
|                                                                      |
|  Exit code 0 (stdout: decision JSON)                                 |
|  Exit code 2 (stderr: error JSON)                                    |
+----------------------------------------------------------------------+
                                      |
                         3. Read stdout JSON
                                      |
                                      v
+-------------------+
| SKILL.md          |
| (Orchestrator)    |
|                   |
| Parse decision -> |
| Route/Gate/       |
| Escalate based    |
| on result         |
+-------------------+
```

### 3.2 Layer Resolution Visualization

```
Layer 4 (runtime)     { "pass_threshold.design": 95 }         Ephemeral
        |                                                       |
        v  (last-writer-wins)                                   | Strict mode
Layer 3 (config)      rules.pass_threshold.design: 90          | disables L4
        |                                                       |
        v  (shallow-merge)                                      v
Layer 2 (preset)      solo.json: { default_pass_threshold: 70 }
        |
        v  (shallow-merge)
Layer 1 (defaults)    routing.json, dod-gates.json, ...

RESOLVED = L1 <- L2 <- L3 <- L4
```

---

## 4. Architecture Decision Records

### ADR-001: Bash+Python Invocation Model

See [ADR-001](adrs/ADR-001.md).

**Summary**: Rule evaluation is performed by invoking a Python script via Bash tool call rather than the orchestrator evaluating rules inline in the SKILL.md prompt. This ensures rules are code-executed (deterministic) rather than prompt-interpreted (non-deterministic).

### ADR-002: 4-Layer Rule Resolution with Last-Writer-Wins

See [ADR-002](adrs/ADR-002.md).

**Summary**: Rules resolve bottom-up across 4 layers using last-writer-wins semantics rather than merge-all or most-specific-wins. This provides a predictable mental model where each layer can fully override any lower layer's decisions.

---

## 5. File Layout

All new files within the delivery-team plugin directory:

```
delivery-team/
  scripts/
    condition_evaluator.py          # C1: Extracted BRE core (Phase 0)
    delivery_rules_adapter.py       # C2: Delivery-flow adapter (Phase 1)
    yaml_to_rules.py                # C3: Config translation layer (Phase 1)
    evaluate_rules.py               # C4: CLI entry point (Phase 1)
    generate-schema.py              # (existing, modified Phase 2)
    validate-config.py              # (existing, unmodified)
    session_keepalive.py            # (existing, unmodified)
  skills/
    delivery-flow/
      SKILL.md                      # (modified Phase 3)
      references/
        rules/                      # NEW directory
          routing.json              # C5: Stage routing rules (Phase 1)
          dod-gates.json            # C6: DoD gate rules (Phase 2)
          escalation.json           # C7: Escalation rules (Phase 2)
          collaboration.json        # C8: Collaboration pattern rules (Phase 2)
          presets/                   # NEW directory
            solo.json               # C9: Solo preset (Phase 1)
            standard.json           # C10: Standard preset (Phase 1)
            strict.json             # C11: Strict preset (Phase 1)
        config-schema.md            # (modified Phase 2 -- v2.4)
        setup-wizard.md             # (modified Phase 3)
        quality-gates.md            # (modified Phase 2)
        routing-decision-spec.md    # NEW (Phase 0, FR-18)
  hooks/
    check_config.py                 # (modified Phase 2)
```

**Runtime files** (per-project, not checked into plugin):

```
.delivery/
  config.yml                        # User config (rules.* section added)
  tmp/
    context-<decision_id>.json      # Ephemeral context files (written per eval)
  audit/
    audit-<pipeline_id>.jsonl       # Audit trail (one per pipeline run)
  state.md                          # (existing, may add HALTED status)
```

---

## 6. Integration Points

### 6.1 delivery-flow SKILL.md (Orchestrator Prompt Changes)

**What changes**: At every decision point (routing, DoD gate, escalation, collaboration pattern), the SKILL.md instructs the orchestrator to invoke the rules engine instead of making the decision inline.

**New orchestrator protocol** (added to SKILL.md):

```
## Rules Engine Invocation Protocol

At every flow-control decision point, the orchestrator MUST:

1. ASSEMBLE context: Serialize current pipeline state into a JSON dictionary.
   Required fields depend on decision type:
   - Routing: project.type, project.risk_tolerance, config.rules.*
   - Gate: stage.*, artifacts.*, stage.validators.*, config.rules.*
   - Escalation: run.iteration_count, run.failure_history, config.rules.*

2. WRITE context to .delivery/tmp/context-<decision_id>.json

3. INVOKE via Bash:
   python <plugin_root>/scripts/evaluate_rules.py \
     --context .delivery/tmp/context-<decision_id>.json \
     --rules-dir <plugin_root>/skills/delivery-flow/references/rules/ \
     --config .delivery/config.yml \
     --decision-type <routing|gate|escalation> \
     [--gate-id <gate_id>]

4. PARSE the JSON response from stdout.

5. ACT on the decision:
   - Routing: use the stage depth map from the response
   - Gate GO: proceed to next stage
   - Gate RECYCLE: route feedback to the responsible agent
   - Gate HOLD: present to user for review
   - ESCALATE: escalate to user immediately

6. On exit code 2: handle error per strict_mode setting.

The orchestrator NEVER makes routing, gating, or escalation decisions
by interpreting SKILL.md prose. All flow-control decisions are delegated
to the rules engine. AI produces artifacts; rules decide flow.
```

**Decision points in SKILL.md that become rules engine invocations**:

| Current Location | Decision | New Invocation |
|-----------------|----------|----------------|
| Phase 1: Project type routing | Stage depth map selection | `--decision-type routing` |
| Phase 3-9: Stage DoD validation | Pass/fail per stage | `--decision-type gate --gate-id <stage>_dod` |
| Self-correction loops | Escalation check | `--decision-type escalation` |
| Stage entry: collaboration selection | Pattern selection | Embedded in routing decision response |

### 6.2 config-schema.md (v2.4 Extension)

**New keys added to the Complete Schema table**:

| Key | Type | Required | Default | Valid Values | Wizard Q# | Consumed By |
|-----|------|----------|---------|-------------|-----------|-------------|
| `rules.preset` | string | no | "standard" | solo, standard, strict | W-15 | evaluate_rules.py (Layer 2 selection) |
| `rules.strict_mode` | boolean | no | false | true, false | W-15 (implied by strict preset) | evaluate_rules.py (Layer 4 disable, coercion errors) |
| `rules.escalation_sensitivity` | string | no | "balanced" | relaxed, balanced, aggressive | W-17 | evaluate_rules.py (escalation thresholds) |
| `rules.pass_threshold` | map | no | {} | stage_name: integer 0-100 | W-16 | evaluate_rules.py (gate threshold overrides) |
| `rules.routing_overrides` | map | no | {} | project_type.stage: full/light | W-16 | evaluate_rules.py (routing overrides) |
| `rules.required_validators` | map | no | {} | stage_name: [validator_names] | W-16 | evaluate_rules.py (validator overrides) |
| `rules.custom` | list | no | [] | list of {field, operator, value, gate, description} | W-16 | evaluate_rules.py (custom rule conditions) |

**Extension protocol checklist**:

| Step | Action | Status |
|------|--------|--------|
| 1. Add to Schema | 7 new rows in Complete Schema table | Defined above |
| 2. Bump Version | 2.3 -> 2.4 | Required |
| 3. Add Wizard Questions | W-15, W-16 (conditional), W-17 | Defined |
| 4. Add to Pipeline Config Table | `rules.*` consumed by evaluate_rules.py | Defined |
| 5. Add Migration Note | v2.4 version history | Required |
| 6. Update Consuming Skill | SKILL.md rules engine protocol | Defined in 6.1 |
| 6.5. Regenerate JSON Schema | Run generate-schema.py | Post-implementation |

### 6.3 setup-wizard.md (3 New Questions)

Three new questions appended after the current last wizard question:

| # | Question | Auto-detect | Options | Maps To |
|---|----------|------------|---------|---------|
| W-15 | Rule Profile | Q5 (Timeline & Risk) -> preset recommendation | solo / standard / strict / Custom / Let's discuss / Skip | `rules.preset` |
| W-16 | Rule Customizations | Conditional: shown only if W-15 = "Custom" or auto-detect confidence < 80% | Routing overrides / Validator overrides / Gate threshold overrides | `rules.pass_threshold`, `rules.routing_overrides`, `rules.required_validators` |
| W-17 | Escalation Sensitivity | None (always shown) | relaxed / balanced / eager (mapped to config value `aggressive`) / Let's discuss / Skip | `rules.escalation_sensitivity` |

**Integration note**: The wizard writes `rules.*` keys to `.delivery/config.yml` using the same YAML generation approach as existing wizard questions. The rules section is appended after the existing config sections with a comment header: `# --- Rules Engine Configuration ---`.

### 6.4 quality-gates.md (Rule-Based Criteria)

**Current state**: Quality gates are described as prose criteria that the AI evaluates subjectively.

**New state**: Quality gates reference the `dod-gates.json` rule definitions. The prose descriptions remain as documentation, but the actual pass/fail evaluation is deferred to the rules engine via `evaluate_rules.py --decision-type gate`.

**Change**: Add a preamble to quality-gates.md stating that all gate evaluations are performed by the rules engine. Prose criteria are documentation of intent; the JSON rules in `references/rules/dod-gates.json` are the executable definitions.

---

## 7. Risk Mitigations

| Risk | Mitigation | Owner |
|------|------------|-------|
| Context assembly incomplete (missing fields cause rule failures) | Define a context schema in `evaluate_rules.py` that validates required fields before evaluation. Fail with exit code 2 and specific missing-field error. | Developer |
| Performance overhead exceeds 500ms budget | Benchmark in Phase 1. The evaluation is pure in-memory JSON traversal -- no I/O during evaluation. JSON file reads are cached at adapter init. Target sub-200ms for routing, sub-500ms for gate. | Developer |
| YAML coercion introduces silent bugs | Translation layer validates all values against expected types. Strict mode promotes coercion to hard errors. All coercion warnings are logged. | Developer |
| Default rules diverge from user expectations | Routing Decision Specification (FR-18) is the normative source, authored by PO. `--dry-run --compare` lets users preview before committing. Migration notes document intentional changes. | PO + Architect |
| Scope creep into DSL territory | Strict boundary: conditions are true/false, gates aggregate with AND/OR, rules evaluate in order. No loops, no variables, no side effects. Reject Turing-complete features. | Architect |
| Config complexity drives away solo developers | Presets are the primary mitigation. `rules.preset: solo` is 2 lines of config. Presets must be genuinely complete. | PO + UX |

---

## 8. Implementation Sequence

| Order | Phase | Component | Dependencies | Exit Criteria |
|-------|-------|-----------|-------------|---------------|
| 1 | 0 | `condition_evaluator.py` (C1) | `business_rules_engine.py` | All BRE condition tests pass against extracted module |
| 2 | 0 | `routing-decision-spec.md` (FR-18) | PO approval | Complete 6x7x3 routing table, PO signed off |
| 3 | 1 | `delivery_rules_adapter.py` (C2) | C1 | Routing + gate evaluation produce correct results from JSON rules |
| 4 | 1 | `yaml_to_rules.py` (C3) | None | Config overrides translate correctly, coercion detected |
| 5 | 1 | `evaluate_rules.py` (C4) | C1, C2, C3 | CLI invocation produces correct JSON output, exit codes correct |
| 6 | 1 | `routing.json` + presets (C5, C9-C11) | routing-decision-spec.md | 10 identical runs produce byte-identical routing |
| 7 | 2 | `dod-gates.json` (C6) | C2 | Gate evaluations return correct decisions |
| 8 | 2 | `escalation.json` + `collaboration.json` (C7, C8) | C2 | Escalation and pattern selection deterministic |
| 9 | 2 | Config schema v2.4 + check_config.py | C4 | Schema validates, config check hook passes |
| 10 | 3 | SKILL.md orchestrator updates | C4, all rules | All decision points invoke rules engine |
| 11 | 3 | Setup wizard extension (W-15, W-16, W-17) | Config schema v2.4 | Wizard writes correct rules.* config |
| 12 | 3 | Dogfooding validation (US-10) | All components | Pipeline run uses rules engine for all flow control |
