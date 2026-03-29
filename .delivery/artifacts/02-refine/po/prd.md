# PRD: Deterministic Rules Engine Integration for Delivery-Flow Pipeline

**Version**: 2.1
**Author**: Product Owner
**Date**: 2026-03-28
**Status**: Draft
**Project Type**: FEATURE

---

## 1. Problem Statement

The delivery-flow pipeline orchestrator currently makes all routing, gating, and escalation decisions through AI interpretation of SKILL.md prompts. This produces three categories of failure:

**Non-deterministic behavior.** Identical project signals (project type, risk tolerance, tech stack) produce different stage routing, depth decisions, and collaboration pattern selections across runs. Teams cannot predict pipeline duration or behavior, which erodes trust and drives pipeline bypass. User interviews confirm this: 5 of 5 personas identified inconsistent gate results as a significant problem.

**Unauditable gate decisions.** Stage gates and DoD validation are evaluated by AI judgment against prose criteria. There is no structured record of why a decision was made, what rules were evaluated, or what data was considered. This makes pipeline behavior opaque and non-reproducible. For regulated environments (SOC2, ISO 27001, HIPAA, PCI-DSS), AI-interpreted gates cannot satisfy audit requirements because the decision logic is non-deterministic.

**Configuration without enforcement.** `.delivery/config.yml` contains rich configuration (checkpoints, collaboration patterns, DoD validators, iteration limits, risk tolerance) but enforcement depends entirely on the AI reading and correctly applying those values every time. There is no mechanism that prevents a misconfigured run or guarantees config is respected.

**Why now.** Enterprise adoption is blocked (Priya: "non-determinism in flow control is a non-starter for regulated environments"). Team leads cannot mandate pipeline usage because they cannot defend inconsistent results to leadership (Marcus: "lack of reproducibility undermines trust in the tool"). DevOps engineers cannot integrate delivery-flow into CI/CD because non-deterministic pipelines violate the fundamental CI/CD contract (Chen: "same commit, same environment, same result"). Solo developers bypass the pipeline entirely for small work because they cannot predict time cost (Sarah: "unpredictability killed my ability to plan"). An existing, proven business rules engine (`prd-quality-gate-flow/business_rules_engine.py`) is already in this codebase, making the integration technically feasible now.

---

## 2. Goals and Success Metrics

### G1: Deterministic Stage Routing

**Goal**: Given identical **structured** project signals and config, the rules engine produces identical routing decisions 100% of the time. Where inputs are AI-derived (e.g., project type classification), determinism applies from the point the structured input enters the rules engine -- not end-to-end from user description to routing output. See Section 5 (Determinism Boundary) for the full classification.

**Metric**: Run the same structured inputs through the rules engine N times (N >= 10) and compare outputs. 100% match rate required. For hybrid decision points, the metric applies to the deterministic segment (rule evaluation given structured input), not to the AI-derived input assembly.

**Baseline**: Current state is non-deterministic -- identical inputs can produce different routing across runs (confirmed by all 5 interview personas).

### G2: Rule-Based DoD Gate Evaluation

**Goal**: DoD pass/fail decisions are evaluated by the rules engine against structured criteria, not by AI interpretation of prose.

**Metric**: Every gate evaluation returns a `GateEvaluationResult` with pass/fail, score, rule-by-rule breakdown, and reason. Zero gate decisions made by AI judgment alone.

**Baseline**: Currently 100% of gate decisions are AI-interpreted.

### G3: User-Configurable Gate Rules

**Goal**: Users can define custom gate rules in `.delivery/config.yml` that override or extend default rules through the 4-layer resolution system.

**Metric**: Config schema extended with a `rules` section (documented in `config-schema.md` v2.4). Users can override at least: pass thresholds per stage, required validators per stage, routing depth per project type, escalation sensitivity, and preset profile. Layer 3 (per-repo) overrides take precedence over Layer 2 (presets) which take precedence over Layer 1 (plugin defaults).

**Baseline**: No rule customization exists. Config values are advisory, not enforced.

### G4: Full Audit Trail

**Goal**: Every rule evaluation is logged with structured data sufficient for compliance audits.

**Metric**: Every rule evaluation logged with: timestamp, gate ID, rule ID, input context, pass/fail result, score, reason, determinism category, and resolution layer. Logs stored in `.delivery/audit/` and reviewable after any run.

**Baseline**: No structured audit trail exists. Decision rationale is embedded in conversation context and lost between sessions.

### G5: AI Stays in Its Lane

**Goal**: Clean separation -- rules engine handles all flow control decisions; AI handles all creative work (artifact production, reviews, brainstorming, feedback synthesis).

**Metric**: Zero flow control decisions (routing, gating, escalation, depth selection) made by AI judgment. All flow control routed through rules engine invocation.

**Baseline**: Currently 100% of flow control decisions are AI-interpreted.

---

## 3. User Personas

### Sarah -- Solo Developer

**Profile**: Freelance full-stack developer. Uses Claude Code daily for personal projects. Values speed and simplicity.

**Core need**: Predictable pipeline behavior so she can estimate time cost before starting. Wants a "solo" profile that reduces ceremony for small changes.

**Pain**: Bypasses the pipeline for small work because she cannot predict whether it will take 20 minutes or 2 hours. Inconsistency killed her trust.

**Priority**: 4/5. Would use the pipeline for everything if routing were predictable and configurable.

### Marcus -- Engineering Team Lead

**Profile**: Leads a 6-person team at a mid-size SaaS company. Needs to justify tooling decisions to VP of Engineering.

**Core need**: Reproducible gate results so he can mandate pipeline usage and retire his parallel manual checklist. Needs audit logs for leadership reporting.

**Pain**: Two developers with similar-scoped changes get different gate results. Senior devs treat gate results as suggestions. Running two quality systems in parallel.

**Priority**: 5/5. Single biggest blocker to recommending the pipeline for all team work.

### Priya -- Enterprise Architect

**Profile**: Works at a regulated financial services firm. SOC2 and ISO 27001 compliance are non-negotiable.

**Core need**: Deterministic, auditable gate decisions that can be cited as automated controls in SOC2 Type II reports. 100% rule-based pass/fail with no AI fallback.

**Pain**: Shelved evaluation after PoC produced three different routing decisions for identical inputs. Compliance team flagged non-deterministic gates as definitionally not a control.

**Priority**: 5/5. Binary -- without this, the tool is not viable for regulated environments.

### Jake -- Game Developer

**Profile**: Indie game dev using Godot. Cares about game feel and iteration speed. Skeptical of process overhead.

**Core need**: Fast iteration paths for game-feel tuning without being routed through heavyweight stages. Wants game-dev presets that create fast paths out of the box.

**Pain**: Pipeline classified physics value tweaks as FEATURE and routed through full architecture. Game dev is 70% iteration work that does not fit standard software development buckets.

**Priority**: 3/5. Values the outcome (fast paths) more than the mechanism (rules engine).

### Chen -- DevOps Engineer

**Profile**: Platform engineer at a startup. Wants to integrate delivery-flow into CI/CD pipelines.

**Core need**: Deterministic pipeline behavior that mirrors CI/CD philosophy (same input = same result). Wants to gate PR merges on rule evaluation results. Needs structured JSON audit logs.

**Pain**: Non-determinism is a cardinal sin in CI/CD. Built his own lightweight pre-push hooks instead of adopting delivery-flow.

**Priority**: 5/5. Prerequisite for all desired CI/CD integrations.

---

## 4. Design Decisions

### DD1: Hybrid JSON/YAML Format

**Decision**: Users customize rules in `.delivery/config.yml` (pure YAML, consistent with existing convention). The engine evaluates rules using JSON internally via the stdlib `json` module (zero external dependencies). Default rules ship as JSON files in the plugin under `references/rules/`. A translation layer converts YAML config overrides into JSON rule structures at evaluation time.

**Rationale**:
- **No external dependencies**: The `pyyaml` library is not allowed; the stdlib `json` module is the only structured data parser available.
- **YAML's implicit typing is dangerous for gate conditions**: YAML silently converts values like `on`, `off`, `yes`, `no`, `3.10` in ways that produce incorrect rule evaluations. JSON has no implicit typing -- what you write is what you get.
- **Consistency**: The existing BRE in `prd-quality-gate-flow/business_rules_engine.py` already uses JSON conditions. Keeping the same format avoids a second rule parser.
- **User experience preserved**: Users never touch JSON. They work in `.delivery/config.yml` (pure YAML) which is the established convention for this project. The translation layer is invisible to them.

**Implications**:
- Default rule definitions are stored as JSON files (`references/rules/*.json`), not YAML
- The translation layer (`yaml_to_rules.py`) is a required component in Phase 1
- Config schema v2.4 documents the YAML surface syntax; the JSON internal format is an implementation detail

### DD2: 4-Layer Rule Resolution System

**Decision**: Rules resolve bottom-up using a last-writer-wins model across four layers.

| Layer | Source | Mutability | Description |
|-------|--------|------------|-------------|
| **Layer 1: Plugin Defaults** | `references/rules/*.json` | Read-only, versioned | Complete rule set shipped with the plugin. Encodes the Routing Decision Specification (FR-16) as deterministic rules. |
| **Layer 2: Preset Profiles** | Built-in profiles (solo, standard, strict) | Read-only | Named presets that override Layer 1 defaults for common team configurations. |
| **Layer 3: Per-Repo Custom** | `rules.*` keys in `.delivery/config.yml` | User-editable | Per-project overrides that tailor rules to a specific repo's needs. |
| **Layer 4: Per-Run Override** | Ephemeral natural language | Transient, not persisted | Session-scoped **granular** overrides via natural language (e.g., "set development threshold to 80 this time"). Not written to config. Layer 4 cannot apply preset-level changes (cannot swap `rules.preset`). Layer 4 can only adjust individual thresholds, toggle individual validators, or modify escalation sensitivity. When a Layer 4 override would relax a Layer 3 value (e.g., lower a threshold the user explicitly configured), the orchestrator displays a confirmation prompt: "This override will replace your configured {key} ({Layer 3 value}) with {Layer 4 value}. Proceed?" The user must confirm before the override takes effect. In strict mode, Layer 4 is disabled entirely (only Layers 1-3 apply). |

**Preset profiles** (Layer 2):
- **Solo**: Minimal ceremony. 1 validator per stage. Warnings demoted to suggestions. Escalation threshold: 2 iterations.
- **Standard**: Balanced defaults. Default validator set. 3 collaboration patterns enabled. Escalation threshold: 3 iterations.
- **Strict**: Full ceremony. Security validator added to all stages. Warnings promoted to blocking. No AI fallback on gate decisions. Full audit trail required.

**Merge semantics**:
- Scalars: last-writer-wins (higher layer replaces lower)
- Lists: last-writer-wins by default; opt-in `_merge: extend` appends instead of replacing
- Maps: shallow-merge (higher layer keys override, unmentioned keys preserved)

**Rationale**: This layered approach satisfies all personas -- Sarah gets presets, Marcus gets per-repo config, Priya gets strict mode, Jake gets game-dev fast paths, Chen gets version-controlled rules. The 4-layer model is validated by DD4 (user requirements confirmation).

### DD3: Setup Wizard Extension

**Decision**: The setup wizard receives 3 new questions to configure rule behavior during project onboarding.

| # | Question | Options | Maps To |
|---|----------|---------|---------|
| W-11 | Rule Profile | solo / standard / strict | `rules.preset` |
| W-12 | Rule Customizations | (conditional, shown only if user selects "customize" or profile detection confidence is low) | `rules.*` overrides |
| W-13 | Escalation Sensitivity | relaxed / balanced / aggressive | `rules.escalation_sensitivity` |

**Auto-detection**: Existing wizard Q3 ("How strict?") maps to `rules.preset`. If Q3 answer is "minimal" the wizard recommends `solo`; if "balanced" it recommends `standard`; if "thorough" it recommends `strict`. The user can override the recommendation.

**Rationale**: Integrating into the existing wizard flow ensures rule configuration happens at project setup, not as an afterthought. Conditional display of W-12 prevents overwhelming solo developers with customization options they do not need (Sarah's concern about configuration complexity).

### DD4: User Requirements Confirmation

**Decision**: User interview confirmed: "Plugin has defaults, users can modify rules per repo as needed. Setup wizard should walk them through this."

**Validation**: This confirms the 4-layer approach -- plugin ships sensible defaults (Layers 1-2), users customize per repo (Layer 3), and the wizard guides initial configuration. The interview consensus (4.4/5 priority, 5 of 5 personas requesting presets) validates that preset profiles are a Must Have, not a convenience feature.

---

## 5. Determinism Boundary

Not all pipeline decision points are equally deterministic. The PRD's determinism guarantee (G1, NFR-02) applies to **rule evaluation given structured inputs** -- but some of those inputs are AI-derived. This section explicitly classifies every pipeline decision point to prevent false claims of end-to-end determinism.

### Classification

| Decision Point | Category | Input Source | Rule Evaluation | Net Determinism |
|---------------|----------|-------------|-----------------|-----------------|
| **Stage routing** (which stages, what depth) | **(a) Fully deterministic** when project type is user-declared; **(b) Hybrid** when project type is auto-detected | Config values, project type (user-declared or AI-classified) | Deterministic lookup in routing table | Fully deterministic if user declares project type; hybrid if auto-detected |
| **Stage depth selection** (full/light per stage) | **(a) Fully deterministic** | Config values, risk tolerance (from config), project type | Deterministic rule evaluation | Fully deterministic -- all inputs from config |
| **DoD gate pass/fail aggregation** | **(b) Hybrid** | Per-validator pass/fail booleans (AI-derived), weighted scores | Deterministic weighted aggregation with threshold comparison | Deterministic aggregation of non-deterministic inputs. Same validator outputs always produce same gate result, but validator outputs may vary between runs |
| **DoD structural checks** (artifact exists, field non-null, word count) | **(a) Fully deterministic** | File system state, artifact metadata | Deterministic fact-checking | Fully deterministic -- no AI involvement |
| **Escalation triggers** (max iterations, repeated failure) | **(a) Fully deterministic** | Iteration counter, failure history (structured data) | Deterministic threshold comparison | Fully deterministic -- all inputs are counters/booleans |
| **Collaboration pattern selection** | **(a) Fully deterministic** | Project type, stage number, config overrides | Deterministic lookup | Fully deterministic -- all inputs from config/context |
| **Rule layer resolution** | **(a) Fully deterministic** for Layers 1-3; **(b) Hybrid** when Layer 4 is active | Layer 1-3 rule definitions (files + config), Layer 4 parsed granular override (AI-interpreted, scoped to individual keys only -- cannot apply preset-level changes) | Deterministic merge with last-writer-wins. Layer 4 requires user confirmation when relaxing Layer 3 values. | Fully deterministic for Layers 1-3. When Layer 4 is active (default/solo mode only), the AI-parsed override introduces a hybrid step, but the override is scoped to granular keys and user-confirmed before application. In strict mode, Layer 4 is disabled -- fully deterministic. |
| **YAML config parsing** | **(b) Hybrid** | `.delivery/config.yml` file content (text) | Deterministic translation layer (`yaml_to_rules.py`) validates and converts structured data to JSON rules | The orchestrator (AI) reads the YAML file and passes structured data to the translation layer. The YAML-to-structured-data step is non-deterministic (AI-parsed, no `pyyaml`). The structured-data-to-JSON step is deterministic. In strict mode, the translation layer performs schema-based type validation and promotes YAML type coercion warnings to hard errors, eliminating silent corruption. In default mode, coercion is warned but not blocking. |
| **Project type auto-detection** | **(c) AI-driven** | User's natural language description | N/A -- classification is AI work | Non-deterministic. AI classifies; result enters rules engine as structured input |
| **Artifact quality assessment** (code review, architecture review) | **(c) AI-driven** | Artifact content | N/A -- creative judgment | Non-deterministic. Explicitly out of scope for rules engine (NFR-06) |
| **Validator pass/fail determination** | **(c) AI-driven** | Artifact content, review criteria | N/A -- subjective assessment | Non-deterministic. AI judges quality; boolean result enters rules engine |

### Implications

1. **G1 success criteria** measure determinism of rule evaluation (category a and the rule-evaluation segment of category b), not end-to-end pipeline determinism. This is honest and verifiable.

2. **For enterprise/strict mode** (Priya's use case): require user-declared project type (eliminating the hybrid path for routing) and weight structural DoD checks at >= 80% (reducing exposure to AI-derived validator variance). In strict mode, category (b) hybrid decisions must log both the AI-derived input and the deterministic aggregation separately in the audit trail so auditors can distinguish them.

3. **For all modes**: the audit trail (FR-06) must tag each decision with its determinism category (a/b/c) so users and auditors can assess the actual determinism level of any given pipeline run.

4. **Project type declaration**: In strict mode, auto-detection is disabled and the user must explicitly declare project type. In default mode, auto-detection is available but the detected type is logged and the user is shown the classification before routing proceeds (allowing correction).

---

## 6. User Stories

### US-01: Deterministic Stage Routing

**As a** team lead running the delivery pipeline,
**I want** identical project signals and config to always produce identical stage routing decisions,
**So that** my team can trust the pipeline and I can mandate its usage without defending inconsistent results.

**Acceptance Criteria**:
- **Given** a project with type FEATURE, risk tolerance "standard", and tech stack "Python", **When** the rules engine evaluates routing, **Then** it produces the same stage depth map (full/light per stage) every time -- no variation across runs.
- **Given** the same structured project signals run 10 times, **When** comparing all 10 routing results, **Then** all 10 are byte-identical JSON objects.
- **Given** a project type BUG_FIX with risk tolerance "standard", **When** routing rules are evaluated, **Then** stages are routed according to the BUG_FIX routing table: Idea=light, Refine=light, Design=light, Architect=light, Plan=light, Development=full, UAT=full.

### US-02: BRE Extraction and Adapter Layer

**As a** delivery-flow orchestrator,
**I want** an adapter layer between the existing BRE core logic and delivery-flow's decision points,
**So that** the proven rule evaluation logic (condition parsing, field comparisons, logical operators, weighted scoring) can be reused without coupling delivery-flow to the prd-quality-gate-flow SQLite schema.

**Acceptance Criteria**:
- **Given** the existing `BusinessRulesEngine._evaluate_condition` method, **When** extracted into a standalone `condition_evaluator.py` module, **Then** the module evaluates all condition types (field comparisons, AND/OR/NOT, MATCHES, IN/NOT IN, IS NULL/IS NOT NULL, .length) identically to the original -- verified by running the BRE's own test cases against the extracted module.
- **Given** the `DeliveryRulesAdapter` class, **When** initialized without a SQLite connection, **Then** it accepts a context dictionary and rule definitions (from JSON files) and returns `GateEvaluationResult` objects with decision, score, rule-by-rule breakdown, and recommendations.
- **Given** the adapter layer, **When** the BRE core logic (`condition_evaluator.py`) is updated, **Then** the adapter continues to function without delivery-flow code changes (loose coupling verified by separate import paths).

### US-03: DoD Gate Rule Evaluation

**As a** pipeline orchestrator validating stage completion,
**I want** DoD pass/fail decisions evaluated by the rules engine against structured criteria,
**So that** gate outcomes are reproducible and not dependent on how the AI interprets prose criteria at that moment.

**Acceptance Criteria**:
- **Given** a stage with 3 DoD validators (PO, Architect, QA), **When** each validator's output is evaluated, **Then** the rules engine checks each validator against per-validator rules (e.g., "architect validator requires ADR present with at least 3 sections") and returns pass/fail per validator with score and reason.
- **Given** all validators pass their individual rules, **When** the gate is evaluated, **Then** the overall gate decision is GO with a weighted score >= the configured pass threshold and a rule-by-rule breakdown showing each validator's contribution.
- **Given** a critical validator fails (e.g., security review on a project with `rules.preset: strict`), **When** the gate is evaluated, **Then** the decision is RECYCLE with specific failure reasons identifying the failed validator and the specific rule that was not satisfied.

### US-04: Config Schema Extension for Rules

**As a** team configuring their delivery pipeline,
**I want** a `rules` section in `.delivery/config.yml` where I can customize gate thresholds, routing overrides, and validator requirements,
**So that** I can tailor pipeline behavior to my team's needs without editing JSON rule definition files directly.

**Acceptance Criteria**:
- **Given** the config schema, **When** version 2.4 is released, **Then** it includes a `rules` section with keys for: `preset` (profile name), `escalation_sensitivity` (relaxed/balanced/aggressive), `strict_mode` (boolean), `pass_threshold` (per-stage map), `routing_overrides` (project type to stage depth map), `required_validators` (per-stage list), and `custom` (list of user-defined rule objects).
- **Given** a config with `rules.pass_threshold.design: 90`, **When** the Design stage DoD is evaluated, **Then** the pass threshold is 90 (overriding the default 80) because Layer 3 (per-repo) takes precedence over Layer 1 (plugin defaults) per DD2 merge semantics.
- **Given** a config with no `rules` section, **When** the pipeline runs, **Then** Layer 1 (plugin defaults) and Layer 2 (standard preset) apply and the pipeline behaves identically to the shipped defaults.
- **Given** a config with schema version < 2.4, **When** the config is loaded, **Then** the pipeline writes a migration warning to stderr in the format `[MIGRATION] config v{detected} -> v2.4: rules section added with default values`, applies safe defaults for missing `rules.*` keys, and continues execution. If the config contains keys that conflict with v2.4 semantics, the pipeline halts with exit code 1 and a stderr message listing the conflicting keys.

### US-05: Structured Audit Trail

**As an** enterprise architect preparing for a SOC2 audit,
**I want** every rule evaluation logged with timestamp, gate ID, rule ID, input context, result, score, reason, determinism category, and resolution layer in a structured format,
**So that** I can demonstrate to auditors that gate decisions are rule-based, reproducible, and traceable.

**Acceptance Criteria**:
- **Given** any rule evaluation occurs, **When** the evaluation completes, **Then** a JSON log entry is written to `.delivery/audit/audit-<pipeline_id>.jsonl` containing: `timestamp` (ISO 8601), `pipeline_id`, `stage`, `gate_id`, `rule_id`, `input_context` (serialized), `passed` (boolean), `score` (float), `decision`, `reason`, `determinism_category` (a/b/c), and `resolution_layer` (1/2/3/4).
- **Given** a completed pipeline run, **When** the audit log is read, **Then** every routing decision and gate evaluation from that run is present and ordered chronologically with no gaps.
- **Given** an audit log entry tagged with determinism category (a), **When** the same input context is replayed through the rules engine, **Then** the identical decision is produced (reproducibility proof).

### US-06: Preset Profiles

**As a** solo developer who does not want to write complex YAML configuration,
**I want** preset profiles (solo, standard, strict) that configure all rule thresholds and routing behavior with a single setting,
**So that** I get predictable, sensible pipeline behavior without learning the rules engine internals.

**Acceptance Criteria**:
- **Given** a config with `rules.preset: solo`, **When** the pipeline runs a FEATURE project, **Then** all routing rules use the "solo" preset: Idea=light, Refine=light, Design=light, Architect=light, Plan=light, Development=full, UAT=light; 1 validator per gate; escalation threshold: 2 iterations.
- **Given** a config with `rules.preset: strict`, **When** the pipeline runs, **Then** all routing rules use the "strict" preset: all stages=full, security validator added to every gate, warnings promoted to blocking, `strict_mode: true` applied, full audit trail required with determinism category tagging.
- **Given** a config with both `rules.preset: solo` and `rules.pass_threshold.development: 95`, **When** the pipeline runs, **Then** the Development stage uses pass threshold 95 (Layer 3 override) while all other stages use solo preset defaults (Layer 2) -- per DD2 merge semantics.
- **Given** a config with `rules.preset: solo` and a GAME_DEV project, **When** physics/animation parameter changes are detected, **Then** Design=light (scope: visual/gameplay impact only) and Architect=light (scope: performance validation only); no stages are executed at depth less than light.

### US-07: Context Assembly for Rule Evaluation

**As a** rules engine receiving evaluation requests,
**I want** the orchestrator to serialize current pipeline state into a structured context dictionary before calling me,
**So that** I can evaluate rules against well-defined fields using dot-notation paths (e.g., `project.type`, `stage.validators.architect.status`).

**Acceptance Criteria**:
- **Given** the pipeline is at Stage 4 (Architect), **When** the orchestrator assembles context for a DoD gate evaluation, **Then** the context dictionary includes: `project.type`, `project.risk_tolerance`, `project.tech_stack`, `stage.number`, `stage.name`, `stage.depth`, `stage.validators` (with per-validator status and output), `config.*` (relevant config values including `rules.*`), `artifacts.*` (artifact presence/metadata), and `run.iteration_count`.
- **Given** a context dictionary, **When** the rules engine accesses `project.type` via dot-notation, **Then** it resolves to the correct value (verified by round-trip: serialize then evaluate).
- **Given** incomplete pipeline state (e.g., missing validator output), **When** the context is assembled, **Then** missing fields are set to `null` (not omitted) so null-check rules can evaluate correctly.

### US-08: Escalation Trigger Rules

**As a** pipeline orchestrator managing self-correction loops,
**I want** escalation decisions (human escalation, loop termination, deadlock detection) made by rules, not AI judgment,
**So that** escalation behavior is predictable and configurable per escalation sensitivity level.

**Acceptance Criteria**:
- **Given** a self-correction loop has iterated 3 times (configurable via `pipeline.max_self_correction`), **When** the escalation rule is evaluated, **Then** the decision is ESCALATE with reason "max iterations reached: 3 of 3."
- **Given** a DoD gate has failed the same validator twice consecutively, **When** the escalation rule is evaluated, **Then** the decision is ESCALATE with reason "repeated validator failure: {validator_name} failed 2 consecutive evaluations."
- **Given** `rules.escalation_sensitivity: relaxed`, **When** escalation rules are evaluated, **Then** thresholds are: max iterations = 5, repeated failure threshold = 3, deadlock timeout = 10 minutes. **Given** `rules.escalation_sensitivity: aggressive`, **Then** thresholds are: max iterations = 2, repeated failure threshold = 1, deadlock timeout = 3 minutes.

### US-09: Collaboration Pattern Selection Rules

**As a** pipeline orchestrator selecting collaboration patterns per stage,
**I want** collaboration pattern selection (evaluator-optimizer, adversarial review, review board, debate, consensus) driven by rules based on project type, stage, and config,
**So that** pattern selection is deterministic and does not vary between runs.

**Acceptance Criteria**:
- **Given** a FEATURE project at Stage 2 (Refine) with `pipeline.collaboration_patterns.refine: [evaluator-optimizer]` in config, **When** the collaboration pattern rule is evaluated, **Then** the result is `["evaluator-optimizer"]` every time with no variation.
- **Given** the same project type, stage, and config, **When** run 10 times, **Then** the same collaboration patterns are selected all 10 times -- byte-identical JSON arrays.
- **Given** a GREENFIELD project at Stage 4 (Architect), **When** the default routing rules are evaluated with no config overrides, **Then** the pattern includes `["adversarial-review", "debate"]` per default rules for GREENFIELD architecture.

### US-10: Dogfooding Validation

**As a** team building the rules engine,
**I want** the rules engine validated by running delivery-flow through its own pipeline with the rules engine active,
**So that** we prove the engine works in a real pipeline context before shipping it to users.

**Acceptance Criteria**:
- **Given** the rules engine is implemented (Phases 1-3 complete), **When** a delivery-flow pipeline run for the rules engine feature itself uses the rules engine for routing and gating, **Then** all routing and gate decisions are made by the rules engine (verified by audit log showing zero category (c) decisions for flow control).
- **Given** the dogfooding run, **When** the audit log is reviewed, **Then** every decision point in the pipeline has a corresponding audit entry with determinism category (a) or (b).
- **Given** the dogfooding run completes, **When** 10 routing evaluations from the run are replayed with identical inputs, **Then** all 10 produce byte-identical results (determinism proof).
- **Given** the dogfooding run completes, **When** the run is validated against Phase 1-3 exit criteria, **Then** all exit criteria pass.

### US-11: Fallback Behavior on Engine Error

**As a** developer whose pipeline must not silently fail,
**I want** the pipeline to halt with a clear error message when the rules engine encounters an unexpected error,
**So that** I never get a gate decision based on AI fallback when I configured rule-based evaluation.

**Acceptance Criteria**:
- **Given** the rules engine raises an exception during evaluation, **When** the orchestrator handles the error, **Then** the pipeline halts with an error message that includes: the failed rule/gate ID, the exception type and message, and instructions to resume or retry.
- **Given** `rules.strict_mode: true` in config, **When** the rules engine encounters any error, **Then** the evaluation script exits with code 2, writes a JSON error object to stderr containing `{"gate_id": "...", "error_type": "...", "message": "...", "timestamp": "..."}`, updates `.delivery/state.json` with `status: "HALTED"` and `halt_reason: "rules_engine_error"`, and no AI fallback evaluation is attempted.
- **Given** `rules.strict_mode: false` (default), **When** the rules engine encounters an error, **Then** the pipeline halts and prompts the user with exactly three options: "Retry", "Skip this gate (AI evaluation)", or "Abort". The user's choice is logged in the audit trail with `decision_source: "user_override"`.

### US-12: Rules Engine Invocation Mechanism

**As a** delivery-flow orchestrator that operates via SKILL.md prompts,
**I want** to invoke the rules engine via a Bash tool call to a Python script that reads context from JSON and writes the decision to JSON,
**So that** rule evaluation is truly code-executed (not prompt-interpreted) and consistent with the existing BRE invocation pattern.

**Acceptance Criteria**:
- **Given** the orchestrator reaches a decision point, **When** it prepares a rules engine invocation, **Then** it writes the context dictionary to `.delivery/tmp/context-<decision_id>.json`, calls `python evaluate_rules.py --context .delivery/tmp/context-<decision_id>.json --rules-dir references/rules/ --config .delivery/config.yml` via Bash tool, and reads the decision from stdout JSON.
- **Given** the Python script is invoked, **When** it evaluates rules, **Then** it exits with code 0 on success (decision JSON on stdout) and code 2 on rule evaluation error (error JSON on stderr). Exit code 1 is reserved for script-level errors (missing files, invalid arguments).
- **Given** the invocation mechanism, **When** benchmarked, **Then** rule evaluation completes in less than 500ms per decision point (measured from script invocation to stdout output).
- **Given** the `--dry-run` flag is passed, **When** the script evaluates rules, **Then** it outputs the full decision JSON to stdout and exits with code 0 without triggering pipeline actions, state mutations, or audit log writes.

### US-13: YAML-to-JSON Translation Layer

**As a** rules engine that evaluates JSON conditions internally,
**I want** a translation layer that converts user YAML config overrides into JSON rule structures,
**So that** users write rules in familiar YAML while the engine evaluates them in type-safe JSON (per DD1).

**Acceptance Criteria**:
- **Given** a user config with `rules.pass_threshold.design: 90`, **When** the translation layer processes this, **Then** it produces a JSON rule override: `{"gate_id": "design_dod", "config": {"pass_threshold": 90}}` that merges with plugin defaults per DD2 merge semantics.
- **Given** a user config with `rules.routing_overrides.BUG_FIX.architect: light`, **When** the translation layer processes this, **Then** it produces a JSON routing rule that sets BUG_FIX architect stage depth to "light" -- overriding the default.
- **Given** a user config with `rules.custom` containing a list of rule objects with `field`, `operator`, and `value` keys, **When** the translation layer processes these, **Then** it produces valid JSON condition structures that the BRE condition evaluator accepts without error.
- **Given** YAML values that would be silently type-coerced (e.g., `yes`, `no`, `on`, `off`, `3.10`), **When** the translation layer encounters these as rule values in default mode, **Then** it preserves the string representation and logs a warning: `[WARN] YAML type coercion detected for key {key}: value {raw} interpreted as {coerced}. Use quotes for literal strings.`
- **Given** `rules.strict_mode: true`, **When** the translation layer encounters any YAML type coercion, **Then** the translation layer halts with exit code 2 and a JSON error to stderr: `{"error_type": "yaml_coercion", "key": "{key}", "raw": "{raw}", "coerced": "{coerced}", "message": "YAML type coercion is a hard error in strict mode. Use quotes for literal strings."}`. No coerced value reaches the rules engine.
- **Given** any rule values passed to the translation layer, **When** the translation layer processes them, **Then** it validates all values against expected types defined in the rule schema (e.g., pass thresholds must be numeric, validator names must be strings matching a known set, preset must be one of solo/standard/strict). Values that fail type validation are rejected with a descriptive error, regardless of mode.

### US-14: SKILL.md Integration

**As a** delivery-flow SKILL.md orchestrator,
**I want** clear instructions for deferring all flow-control decisions to the rules engine,
**So that** the orchestrator invokes the evaluation script at every decision point instead of making routing/gating decisions inline.

**Acceptance Criteria**:
- **Given** the updated SKILL.md, **When** the orchestrator reaches a stage routing decision, **Then** SKILL.md instructs it to: (1) assemble context via `PipelineContextBuilder`, (2) write context to `.delivery/tmp/`, (3) invoke `evaluate_rules.py` via Bash, (4) parse the JSON response, (5) act on the decision.
- **Given** the updated SKILL.md, **When** the orchestrator reaches a DoD gate, **Then** SKILL.md instructs it to invoke the rules engine for pass/fail determination rather than judging the gate against prose criteria.
- **Given** the updated SKILL.md, **When** any flow-control decision is made without invoking the rules engine, **Then** this is a SKILL.md compliance violation detectable by the pipeline bypass detection hook.

### US-15: Setup Wizard Extension

**As a** new user setting up delivery-flow for the first time,
**I want** the setup wizard to ask me about rule profile and escalation preferences,
**So that** my rules are configured correctly from the start without manual YAML editing.

**Acceptance Criteria**:
- **Given** the setup wizard is running, **When** the user reaches question W-11 (Rule Profile), **Then** the wizard presents three options: solo, standard, strict. If the user's answer to Q3 ("How strict?") was "minimal" the wizard pre-selects solo; if "balanced" pre-selects standard; if "thorough" pre-selects strict.
- **Given** the user selects a profile, **When** they are asked W-12 (Rule Customizations), **Then** this question is displayed only if the user explicitly says "customize" or if the auto-detection confidence from Q3 mapping is below 80%. Otherwise W-12 is not shown.
- **Given** the user completes W-13 (Escalation Sensitivity), **When** the wizard writes config, **Then** `.delivery/config.yml` contains `rules.preset: {selected}` and `rules.escalation_sensitivity: {selected}`, and any W-12 customizations are written under `rules.custom`.

### US-16: Dry-Run Preview

**As a** developer configuring delivery-flow rules,
**I want** to preview what the rules engine would decide for my project without running the pipeline,
**So that** I can validate my configuration, predict pipeline duration, and build trust in deterministic routing before committing to a full run.

**Acceptance Criteria**:
- **Given** the user runs `python evaluate_rules.py --context <context_file> --rules-dir references/rules/ --config .delivery/config.yml --dry-run`, **When** the script completes, **Then** it outputs the full decision JSON to stdout including: resolved routing map (stage depths for all 7 stages), gate pass thresholds per stage, active preset, resolution layer per rule, determinism category per decision point, and estimated stage count. No pipeline actions are executed, no state files are mutated, and no audit log entries are written.
- **Given** a dry-run invocation, **When** the output is compared to an actual pipeline run with the same context and config, **Then** the routing decisions and gate thresholds are identical (the dry-run is a faithful preview of what the engine would decide).
- **Given** a dry-run invocation with `--compare` flag, **When** the script evaluates, **Then** it additionally outputs a side-by-side comparison of the current rule-based routing versus the default routing, highlighting any overrides from Layer 3 or Layer 4.

---

## 7. Functional Requirements

| ID | Requirement | Priority | Traces To |
|----|-------------|----------|-----------|
| FR-01 | **BRE condition evaluator extraction**: Extract `_evaluate_condition` and its supporting methods (`_get_field_value`, `_compare_values`, `_extract_field_paths`, `_extract_relevant_context`) into a standalone `condition_evaluator.py` module, decoupled from SQLite. This module is the shared foundation for both prd-quality-gate-flow and delivery-flow. Phase 0 deliverable. | Must Have | US-02 |
| FR-02 | **Integration adapter layer**: Create a `DeliveryRulesAdapter` class that rebuilds gate orchestration, rule iteration, weighted scoring aggregation, and decision threshold logic on top of `condition_evaluator.py`. Accepts a context dictionary (not SQLite) and JSON rule definitions (from files). Returns `GateEvaluationResult` objects. Estimated effort: partial rewrite, not a thin wrapper -- only `_evaluate_condition` is directly reusable from the existing BRE. | Must Have | US-02 |
| FR-03 | **Stage routing rules**: Implement a complete set of default routing rules as JSON files (`references/rules/routing.json`) that encode the Routing Decision Specification (FR-18). Covers: project type to stage depth map for all 6 project types (GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, DOCS_ONLY) x 7 stages x 3 risk tolerances. Every combination is explicitly defined -- no fallback to AI interpretation. | Must Have | US-01 |
| FR-04 | **DoD gate rules**: Implement per-validator DoD rules as JSON files (`references/rules/dod-gates.json`) for each pipeline stage. Each validator has structured pass/fail criteria evaluated by the rules engine. Supports weighted scoring with configurable pass thresholds per stage. Granularity is per-validator (maps to existing DoD validator structure). | Must Have | US-03 |
| FR-05 | **Context serialization**: Implement a `PipelineContextBuilder` class that serializes current pipeline state into a structured dictionary with dot-notation accessible fields. Schema includes: `project.*`, `stage.*`, `config.*`, `artifacts.*`, `run.*`. Missing fields are set to `null`. | Must Have | US-07 |
| FR-06 | **Audit trail logging**: Write a JSON Lines log entry to `.delivery/audit/audit-<pipeline_id>.jsonl` for every rule evaluation. Each entry includes: `timestamp` (ISO 8601), `pipeline_id`, `stage`, `gate_id`, `rule_id`, `input_context`, `passed`, `score`, `decision`, `reason`, `determinism_category` (a/b/c), `resolution_layer` (1/2/3/4). One file per pipeline run. | Must Have | US-05 |
| FR-07 | **Preset profiles**: Ship 3 preset profiles (solo, standard, strict) as bundled JSON rule sets under `references/rules/presets/`. Each profile configures: routing depths, pass thresholds, required validators, escalation thresholds, and strict mode flag. Profiles are selected via `rules.preset` in config and resolve at Layer 2 per DD2. | Must Have | US-06 |
| FR-08 | **Escalation rules**: Implement rules for escalation triggers as JSON (`references/rules/escalation.json`): max iteration reached, repeated validator failure, low confidence threshold, deadlock detection. Thresholds configurable via `rules.escalation_sensitivity` (relaxed/balanced/aggressive) in config. Each sensitivity level defines explicit numeric thresholds. | Must Have | US-08 |
| FR-09 | **Collaboration pattern rules**: Implement rules that deterministically select collaboration patterns per stage as JSON (`references/rules/collaboration.json`) based on project type, stage, and config. | Must Have | US-09 |
| FR-10 | **YAML-to-JSON translation layer**: Create `yaml_to_rules.py` that reads user rule overrides from `.delivery/config.yml` (parsed by the orchestrator, passed as structured data) and converts them into JSON rule structures. Implements DD2 merge semantics (scalars replace, lists replace with opt-in `_merge: extend`, maps shallow-merge). Detects YAML type coercion: warns in default mode, promotes to hard error in strict mode. Validates all rule values against expected types defined in the rule schema (numeric thresholds, string enums, known validator names) regardless of mode. | Must Have | US-13 |
| FR-11 | **Python evaluation script**: Create `evaluate_rules.py` that reads context from a JSON file (via `--context` arg), loads rules from `--rules-dir`, applies config overrides from `--config`, resolves layers per DD2, evaluates rules, and outputs the decision as JSON to stdout. Exit code 0 = success, 2 = rule error, 1 = script error. Invoked via Bash tool call from the orchestrator. Supports `--dry-run` flag: when set, the script evaluates rules and outputs the full routing/gate decision JSON to stdout but does not trigger any pipeline actions, state mutations, or audit log writes. Dry-run output includes: resolved routing map, gate decisions, active preset, resolution layer per rule, and determinism category per decision point. | Must Have | US-12, US-16 |
| FR-12 | **Config schema extension (v2.4)**: Extend `config-schema.md` with a `rules` section supporting: `preset` (solo/standard/strict), `strict_mode` (boolean), `escalation_sensitivity` (relaxed/balanced/aggressive), `pass_threshold` (per-stage map), `routing_overrides` (project type to stage depth map), `required_validators` (per-stage list), `custom` (list of user-defined rule objects). Follow the existing extension protocol. | Must Have | US-04 |
| FR-13 | **SKILL.md orchestrator updates**: Update delivery-flow SKILL.md to defer all flow-control decisions to the rules engine. At each decision point (routing, DoD gate, escalation, collaboration pattern selection), the orchestrator invokes `evaluate_rules.py` via Bash and acts on the result. AI produces artifacts; rules engine decides flow. | Must Have | US-14, US-01, US-03 |
| FR-14 | **Error handling and fallback**: Implement halt-on-error behavior. In strict mode (`rules.strict_mode: true`), halt immediately with JSON error to stderr. In default mode, halt and prompt user with 3 options (retry / skip with AI / abort). Never silently fall back to AI evaluation. User override choices are logged in audit trail. | Must Have | US-11 |
| FR-15 | **Depth selection rules**: Implement rules within `references/rules/routing.json` that determine stage depth (full/light) based on risk tolerance, project type, and stage. Light means reduced depth with specific scope constraints documented per stage -- never executed at zero depth. | Must Have | US-01 |
| FR-16 | **Rule override mechanism**: When a user defines rules in config (Layer 3) that overlap with defaults (Layer 1) or presets (Layer 2), Layer 3 takes precedence per DD2 merge semantics. Override is per-key (not all-or-nothing). Unmentioned keys are preserved from lower layers. | Must Have | US-04, US-06 |
| FR-17 | **Setup wizard extension**: Add 3 new questions (W-11: Rule Profile, W-12: Rule Customizations (conditional), W-13: Escalation Sensitivity) to the existing setup wizard. W-11 auto-detects from Q3; W-12 displays conditionally. Wizard writes `rules.*` keys to config. | Must Have | US-15 |
| FR-18 | **Routing Decision Specification**: Before writing any routing rules, produce a normative "Routing Decision Specification" document that explicitly defines the intended routing for every combination of project type (6 types) x stage (7 stages) x risk tolerance (low/standard/high). This specification defines what routing **is correct** -- not what the current AI inconsistently does. The PO signs off on the specification before implementation begins. Stored at `delivery-team/delivery-flow/references/routing-decision-spec.md`. | Must Have | US-01, US-02 |

---

## 8. Non-Functional Requirements

### NFR-01: Performance

Rule evaluation must add less than 500ms per decision point. The rules engine performs no network calls and no file system mutations during evaluation (read-only). Audit log writes occur after evaluation returns and must not block the evaluation response. Context serialization + rule evaluation + JSON output must complete within the 500ms budget.

### NFR-02: Determinism

Given identical inputs (context dictionary + resolved rule set from all 4 layers), the rules engine must produce byte-identical JSON outputs every time. No randomness, no timestamp-dependent logic, no external state dependencies in the evaluation path. Timestamps are recorded in audit logs but are not inputs to rule evaluation.

### NFR-03: Auditability

Every rule evaluation must produce a structured log entry sufficient for a SOC2 Type II audit. Log entries must include enough context to reconstruct the decision independently. The audit log format is JSON Lines (`.jsonl`) -- one JSON object per line, one file per pipeline run. Each entry includes the determinism category (a/b/c) and the resolution layer (1-4) that provided the active rule.

### NFR-04: Backward Compatibility

Existing pipelines with no `rules` section in config must continue to function using Layer 1 defaults + Layer 2 standard preset. The rules engine is always-on with defaults that encode the **Routing Decision Specification** (FR-18). Where the specification diverges from observed AI behavior (which it will, because the AI was inconsistent), the specification is authoritative. Migration notes document any intentional behavioral changes from common AI routing patterns. No opt-in flag required for basic functionality.

### NFR-05: Config Schema Versioning

The config schema extension follows the established extension protocol in `config-schema.md`. Schema version bumps from v2.3 to v2.4. Existing v2.3 configs receive automatic migration (defaults applied for new keys) with a warning. Conflicting keys cause a halt with exit code 1.

### NFR-06: Separation of Concerns

The rules engine handles only flow control: routing, gating, escalation, depth selection, collaboration pattern selection. Artifact quality assessment (code review, architecture review, UX review, design quality) remains AI-driven. The two domains never cross -- rules decide what happens next; AI decides how to do the work.

### NFR-07: Zero External Dependencies

The rules engine uses only Python standard library modules (`json`, `re`, `datetime`, `pathlib`, `sys`, `argparse`). No `pyyaml`, no `sqlite3` (for delivery-flow integration -- the existing BRE's SQLite usage is not carried forward). All structured data is JSON.

### NFR-08: Maintainability

Rule definitions are stored as human-readable JSON files, version-controlled alongside the plugin code. The rule format uses the same condition structure as the existing BRE (field comparisons, AND/OR/NOT, pattern matching). Translation from YAML config to JSON conditions is handled by `yaml_to_rules.py`.

---

## 9. Out of Scope

1. **UI/dashboard for rule management.** Rules are configured in YAML config files, not through a GUI. A dashboard for visualization or editing is a separate future feature.

2. **ML-based rule optimization.** Rules are authored by humans and evaluated deterministically. No AI-generated or AI-tuned rules in this iteration.

3. **Cross-pipeline rule sharing.** Rules are scoped to a single project's `.delivery/config.yml`. Sharing rules across projects (rule libraries, rule packages) is a future concern.

4. **Replacing AI for artifact quality assessment.** The rules engine handles flow control (routing, gating, escalation). Artifact quality reviews (code review, architecture review, UX review) remain AI-driven because they require creative judgment.

5. **External rules engine integration.** No integration with third-party rules engines (Drools, OPA, etc.). We use the in-repo engine.

6. **CI/CD pipeline generation.** Chen wants to integrate delivery-flow gates into GitHub Actions. The rules engine makes this possible, but the actual CI/CD integration (GitHub Action, exportable rule manifest) is a separate feature built on top of this foundation.

7. **Rule change review workflow.** Marcus wants rule changes treated as seriously as code changes. While rules are version-controlled (enabling PR review), a dedicated rule change approval workflow is out of scope.

8. **Game-dev as a separate preset.** Game-dev fast paths are handled by project type GAME_DEV in the routing rules (FR-03) and per-repo config overrides (FR-16), not as a separate Layer 2 preset. Jake's use case is addressed by the routing table + solo preset combination.

---

## 10. Dependencies and Risks

### Dependencies

| Dependency | Description | Impact if Unavailable |
|-----------|-------------|----------------------|
| `business_rules_engine.py` | Existing BRE. **Reusable**: `_evaluate_condition`, `_get_field_value`, `_compare_values`, `_extract_field_paths` (condition parsing, field comparisons, logical operators, pattern matching). **Must rebuild**: gate orchestration, rule iteration, weighted scoring aggregation, decision threshold logic (all coupled to SQLite schema). Phase 0 extracts the reusable core; Phase 1 rebuilds the rest. | Must rewrite all evaluation logic from scratch including condition evaluation. Very high effort increase. |
| `config-schema.md` (v2.3) | Existing config schema with extension protocol. | Cannot extend config without schema. Moderate effort to work around. |
| Delivery-flow SKILL.md | Current orchestrator instructions. Must be updated to defer flow control to rules engine. | Cannot integrate without SKILL.md changes. Blocking. |
| `.delivery/config.yml` infrastructure | Config loading, version checking, migration, setup wizard. | Rules config has no delivery mechanism. Blocking. |
| Hooks infrastructure | 7 existing hooks across 5 event types. Pipeline bypass detection hook may need updates to detect rules engine bypass. | Rules engine works but enforcement is weaker. Non-blocking. |
| Setup wizard (existing 10 questions) | Wizard infrastructure for adding 3 new questions. | W-11/W-12/W-13 cannot be added. Non-blocking for core rules engine; blocking for FR-17 only. |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Default rules diverge from user expectations.** Default rules based on the Routing Decision Specification (FR-18) may produce different routing than what individual users experienced with AI-driven routing (which varied per run). Users may perceive intentional improvements as regressions. | High | Medium | The Routing Decision Specification (FR-18) is the normative baseline, not observed AI behavior. Publish migration notes documenting any intentional divergences from common AI routing patterns. The `--dry-run` mode (FR-11, US-16) with optional `--compare` flag shows old-AI-typical vs new-rule routing for a given project type so users can preview changes before adoption. |
| **Context assembly is incomplete.** The rules engine evaluates against a context dictionary. If the context is missing fields the rules need, evaluations fail or produce wrong results. | Medium | High | Define a `pipeline-context-schema.md` reference document that enumerates every field, its type, and when it becomes available (which stage). Validate context completeness before evaluation. Fail loudly on missing required fields. |
| **Rule expressiveness is insufficient.** Interview personas (Marcus, Chen) need conditional logic (e.g., "if file path matches X, require Y"). The existing BRE supports regex matching and collection operations, but real-world conditions may exceed current capabilities. | Medium | Medium | Start with the existing BRE condition set. Track rule requests that cannot be expressed. Extend condition operators only when concrete use cases demand it. |
| **Performance overhead in iteration-heavy workflows.** Jake (game dev) flagged that even 5 seconds added per step is too many for tight iteration loops. Rule evaluation plus JSON serialization/deserialization could introduce latency. | Low | Medium | Benchmark early in Phase 1. Target sub-200ms for routing evaluations, sub-500ms for full DoD gate evaluations. Optimize context serialization if needed. |
| **Configuration complexity drives away solo developers.** Sarah flagged that a 200-line YAML file would be a dealbreaker. If the rules config is complex, solo devs will bypass the pipeline (the exact problem we are solving). | Medium | High | Preset profiles (FR-07) are the primary mitigation. Solo devs set `rules.preset: solo` and never touch individual rules. Presets must be genuinely complete -- not a starting point that requires customization. |
| **Scope creep into a DSL.** Chen warned that rules engines tend to grow into their own DSL. Each new operator or condition type adds complexity. | Medium | Medium | Strict scope boundary: conditions evaluate to true/false, gates aggregate with AND/OR, rules evaluate in defined order. No loops, no variables, no side effects. Reject feature requests that push toward Turing-completeness. |
| **YAML-to-JSON translation introduces bugs.** The translation layer (FR-10) is a new component that could introduce subtle type coercion or mapping errors between user intent (YAML) and engine evaluation (JSON). | Medium | High | Comprehensive test cases for the translation layer covering: type coercion edge cases (yes/no/on/off/3.10), nested overrides, merge semantics, and round-trip verification. The translation layer logs warnings on detected coercion (US-13 AC-4). |

---

## 11. Timeline and Milestones

### Phase 0: BRE Extraction and Routing Decision Specification

**Scope**: FR-01 (condition evaluator extraction), FR-18 (Routing Decision Specification).

**Deliverables**:
- **BRE reuse inventory**: Line-by-line audit of `business_rules_engine.py` documenting what is reusable (condition evaluation, comparison operators, logical operators, pattern matching) vs. what must be rebuilt (gate orchestration, rule loading, scoring aggregation, decision mapping)
- **`condition_evaluator.py`**: Extracted standalone module containing `_evaluate_condition` and its supporting methods, decoupled from SQLite
- **Routing Decision Specification** (`delivery-team/delivery-flow/references/routing-decision-spec.md`): Normative routing table for all 6 project types x 7 stages x 3 risk tolerances, PO-approved

**Exit criteria**: Extracted `condition_evaluator.py` passes the same condition evaluation tests as the original BRE. Routing Decision Specification is complete and PO-signed-off.

### Phase 1: Stage Routing Rules and Foundation

**Scope**: FR-02 (adapter layer), FR-03 (routing rules), FR-05 (context serialization), FR-10 (translation layer), FR-11 (evaluation script), FR-15 (depth selection).

**Deliverables**:
- `DeliveryRulesAdapter` class with delivery-flow interface
- `PipelineContextBuilder` for context serialization
- `yaml_to_rules.py` translation layer (DD1 implementation)
- `evaluate_rules.py` standalone evaluation script with 4-layer resolution (DD2 implementation)
- `references/rules/routing.json` with routing rules encoding the Routing Decision Specification for all 6 project types
- Depth selection rules (risk tolerance + project type + stage = depth)

**Exit criteria**: Routing rules produce byte-identical results for identical inputs across 10+ runs. Default rules match the Routing Decision Specification. Translation layer correctly converts YAML overrides to JSON rules. 4-layer resolution merges correctly per DD2 semantics.

### Phase 2: DoD Gates, Config Extension, and Escalation

**Scope**: FR-04 (DoD gate rules), FR-08 (escalation rules), FR-09 (collaboration pattern rules), FR-12 (config schema v2.4), FR-14 (error handling), FR-16 (rule overrides).

**Deliverables**:
- Per-validator DoD rules for all 7 pipeline stages (`references/rules/dod-gates.json`)
- Escalation trigger rules (`references/rules/escalation.json`)
- Collaboration pattern selection rules (`references/rules/collaboration.json`)
- Config schema v2.4 with `rules` section
- Error handling (halt-on-error, strict mode, user prompt)
- Rule override mechanism (Layer 3 over Layer 2 over Layer 1)

**Exit criteria**: All gate decisions are rule-based with no AI fallback. Config overrides work correctly per DD2 merge semantics. Error handling halts (never silently falls back). Schema v2.4 passes validation. Escalation rules respect sensitivity levels.

### Phase 3: Audit Trail, Presets, Wizard, and SKILL.md Integration

**Scope**: FR-06 (audit trail), FR-07 (preset profiles), FR-13 (SKILL.md updates), FR-17 (setup wizard extension).

**Deliverables**:
- JSON Lines audit logging to `.delivery/audit/` with determinism category and resolution layer tagging
- 3 preset profiles (solo, standard, strict) as bundled JSON rule sets
- Updated delivery-flow SKILL.md with rules engine integration at all decision points
- Setup wizard with 3 new questions (W-11, W-12, W-13)
- Dogfooding run (US-10): deliver the rules engine feature through its own pipeline with the rules engine active

**Exit criteria**: Audit log entries are complete, structured, and tagged with determinism category. Preset profiles produce expected behavior per US-06 ACs. SKILL.md defers all flow control to rules engine. Wizard correctly writes `rules.*` keys. Dogfooding run completes successfully with full audit trail.

---

## 12. Open Questions

### OQ-1: Context Schema Completeness

**Question**: What fields must be available in the context dictionary for rule evaluation? The existing BRE uses dot-notation paths. We need a complete schema of available fields before writing rules.

**Current leaning**: Define a `pipeline-context-schema.md` reference document that enumerates every field, its type, and when it becomes available (which stage).

**Decision needed by**: Phase 1 start (affects FR-05).

### OQ-2: Migration Path Communication

**Question**: How do we communicate routing behavior changes to existing users when the Routing Decision Specification (FR-18) intentionally diverges from previously observed AI routing patterns?

**Current leaning**: Ship migration notes with v2.4 documenting specific changes. The `--dry-run --compare` mode (FR-11, US-16) shows old-AI-typical vs new-rule routing for a given project type. Rules engine is always-on (no opt-in flag) per NFR-04.

**Decision needed by**: Phase 2 start (affects FR-12).

### OQ-3: Layer 4 (Per-Run Override) Parsing

**Question**: How does the orchestrator parse natural language per-run overrides (Layer 4) into structured rule overrides? This is inherently an AI task, which means Layer 4 resolution has a non-deterministic input step.

**Decision (v2.1)**: Layer 4 is scoped to granular overrides only. The orchestrator interprets the user's natural language command and maps it to individual override keys (e.g., "lower the development threshold to 80" maps to `rules.pass_threshold.development: 80`). Layer 4 **cannot** apply preset-level changes (cannot swap `rules.preset`). When Layer 4 would relax a Layer 3 value, the orchestrator displays a confirmation prompt before applying the override. The interpreted override is logged in the audit trail. For strict mode, Layer 4 is disabled (only Layers 1-3 apply). Layer 4 is documented as hybrid in the Determinism Boundary (Section 5).

**Decision needed by**: Phase 1 start (affects FR-11 evaluation script).

### OQ-4: DoD Rule Granularity for Custom Rules

**Question**: How granular can user-defined custom rules (Layer 3, `rules.custom`) be? Per-stage pass/fail? Per-validator rules? Per-artifact field rules?

**Current leaning**: Per-validator rules as the primary granularity (maps to existing DoD validator structure). Per-artifact rules are available as condition predicates within validator rules (e.g., "PRD validator passes if `artifacts.prd.sections.length >= 5`"). Full per-artifact rules are deferred to a future iteration.

**Decision needed by**: Phase 2 start (affects FR-04, FR-12).

---

## 13. Traceability Matrix

### FR to US to Goal

| FR | Requirement | US | Goal |
|----|-------------|-----|------|
| FR-01 | BRE condition evaluator extraction | US-02 | G5 |
| FR-02 | Integration adapter layer | US-02 | G1, G5 |
| FR-03 | Stage routing rules | US-01 | G1 |
| FR-04 | DoD gate rules | US-03 | G2 |
| FR-05 | Context serialization | US-07 | G1, G2 |
| FR-06 | Audit trail logging | US-05 | G4 |
| FR-07 | Preset profiles | US-06 | G3 |
| FR-08 | Escalation rules | US-08 | G1, G5 |
| FR-09 | Collaboration pattern rules | US-09 | G1, G5 |
| FR-10 | YAML-to-JSON translation layer | US-13 | G3, G5 |
| FR-11 | Python evaluation script (with dry-run) | US-12, US-16 | G1, G2, G5 |
| FR-12 | Config schema extension (v2.4) | US-04 | G3 |
| FR-13 | SKILL.md orchestrator updates | US-14, US-01, US-03 | G1, G2, G4, G5 |
| FR-14 | Error handling and fallback | US-11 | G2, G5 |
| FR-15 | Depth selection rules | US-01 | G1 |
| FR-16 | Rule override mechanism | US-04, US-06 | G3 |
| FR-17 | Setup wizard extension | US-15 | G3 |
| FR-18 | Routing Decision Specification | US-01, US-02 | G1 |

### US to Goal Coverage

| US | User Story | Goals Served |
|----|-----------|-------------|
| US-01 | Deterministic Stage Routing | G1 |
| US-02 | BRE Extraction and Adapter Layer | G1, G5 |
| US-03 | DoD Gate Rule Evaluation | G2 |
| US-04 | Config Schema Extension | G3 |
| US-05 | Structured Audit Trail | G4 |
| US-06 | Preset Profiles | G3 |
| US-07 | Context Assembly | G1, G2 |
| US-08 | Escalation Trigger Rules | G1, G5 |
| US-09 | Collaboration Pattern Rules | G1, G5 |
| US-10 | Dogfooding Validation | G1, G2, G4, G5 |
| US-11 | Fallback Behavior on Engine Error | G2, G5 |
| US-12 | Rules Engine Invocation Mechanism | G1, G2, G5 |
| US-13 | YAML-to-JSON Translation Layer | G3, G5 |
| US-14 | SKILL.md Integration | G1, G2, G4, G5 |
| US-15 | Setup Wizard Extension | G3 |
| US-16 | Dry-Run Preview | G1, G3 |

### Goal Coverage Verification

| Goal | FRs | USs | Covered? |
|------|-----|-----|----------|
| G1: Deterministic Routing | FR-02, FR-03, FR-05, FR-08, FR-09, FR-11, FR-13, FR-15, FR-18 | US-01, US-02, US-07, US-08, US-09, US-10, US-12, US-14 | Yes |
| G2: Rule-Based DoD | FR-04, FR-11, FR-13, FR-14 | US-03, US-10, US-11, US-12, US-14 | Yes |
| G3: User-Configurable Rules | FR-07, FR-10, FR-12, FR-16, FR-17 | US-04, US-06, US-13, US-15 | Yes |
| G4: Full Audit Trail | FR-06, FR-13 | US-05, US-10, US-14 | Yes |
| G5: AI Stays in Its Lane | FR-01, FR-02, FR-08, FR-09, FR-10, FR-11, FR-13, FR-14 | US-02, US-08, US-09, US-10, US-11, US-12, US-13, US-14 | Yes |

### Interview-Derived Requirements Mapping

| Interview Requirement | PRD Coverage |
|-----------------------|-------------|
| Deterministic gate evaluation (same input = same result) | G1, FR-03, FR-04, NFR-02 |
| YAML-based rule configuration in version control | DD1, FR-10, FR-12, NFR-08 |
| Structured audit log (JSON) for every rule evaluation | FR-06, NFR-03 |
| Preset profiles (solo, standard, strict) | DD2, FR-07, US-06 |
| Separation of AI advisory from gate pass/fail | G5, NFR-06, FR-13 |
| Conditional routing rules (file paths, modules, change scope) | FR-03, FR-15 (extensible via BRE pattern matching) |
| Strict mode (no AI influence on gate decisions) | FR-14, US-11 |
| Dry-run preview mode (preview before committing, CI/CD pre-merge validation) | FR-11 (`--dry-run`), US-16 |
| CI/CD integration hooks (exportable rule manifest) | Out of scope (Section 9, item 6) -- enabled by this work |
| Custom fast-path definitions (e.g., "iteration mode") | FR-07 (solo preset + GAME_DEV routing), FR-16 (overrides) |
| Rule evaluation performance SLA (sub-200ms routing, sub-500ms gates) | NFR-01 |
| Rule change review workflow (treat as code) | Out of scope (Section 9, item 7) -- enabled by version control |
| Dashboard/reporting from audit logs | Out of scope (Section 9, item 1) -- enabled by structured audit logs |
