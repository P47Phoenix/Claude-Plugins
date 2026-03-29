# Idea Brief: Deterministic Rules Engine for Delivery-Flow Pipeline

**Project Type**: FEATURE
**Date**: 2026-03-28
**Author**: Product Owner

---

## Problem Statement

The delivery-flow pipeline orchestrator currently makes all routing, gating, and escalation decisions through AI interpretation of SKILL.md prompts. This means:

1. **Non-deterministic routing.** The same project signals (e.g., project type FEATURE, risk tolerance standard, tech stack Python) can produce different stage routing, depth decisions, and skip logic across runs. There is no guarantee that identical inputs yield identical pipeline behavior.

2. **AI-judged gates.** Stage gates and DoD validation are evaluated by AI judgment against prose criteria. Whether a stage "passes" depends on how the model interprets the criteria at that moment, not on a fixed set of pass/fail rules. Two runs with identical artifacts can produce different gate outcomes.

3. **No audit trail for decisions.** When the pipeline routes a project type to light-depth on Stage 3 or decides a DoD validator's output constitutes DONE, there is no structured record of *why* that decision was made, what rules were evaluated, or what data was considered. This makes pipeline behavior unauditable.

4. **Compliance gap.** Teams operating under SOC2, ISO 27001, HIPAA, or similar frameworks need deterministic, auditable gate decisions. AI-interpreted gates cannot satisfy audit requirements because the decision logic is opaque and non-reproducible.

5. **Configuration has no enforcement teeth.** `.delivery/config.yml` contains rich configuration (checkpoints, collaboration patterns, DoD validators, iteration limits, risk tolerance) but enforcement is entirely dependent on the AI reading and correctly applying those values every time. There is no mechanism that *prevents* a misconfigured run.

---

## Target Users and Pain Points

### Primary: Teams using delivery-flow for software delivery

- **Pain**: Run the same pipeline twice, get different routing decisions. Have to manually verify the pipeline respected their config.
- **Need**: Predictable, repeatable pipeline behavior where config drives routing deterministically.

### Secondary: Enterprises with compliance requirements (SOC2, ISO 27001, HIPAA, PCI-DSS)

- **Pain**: Cannot demonstrate to auditors that gate decisions are rule-based and reproducible. AI judgment is not an acceptable decision authority for regulated gates.
- **Need**: Structured audit trail showing which rules were evaluated, what data was input, and what decision was rendered -- for every gate in every run.

### Tertiary: Individual developers wanting predictable pipelines

- **Pain**: Surprising pipeline behavior (unexpected stage depths, inconsistent skip logic) erodes trust.
- **Need**: Pipeline that behaves the way the config says it should, every time.

---

## Goals and Success Criteria

### G1: Deterministic stage routing

**Success**: Given identical project signals and config, the pipeline produces identical routing decisions (stage depths, skip/light/full, collaboration patterns selected) 100% of the time. This is verified by running the same inputs through the rules engine N times and comparing outputs.

### G2: Rule-based DoD gate evaluation

**Success**: DoD pass/fail decisions are evaluated by the rules engine against structured criteria, not by AI interpretation of prose. The rules engine returns a `GateEvaluationResult` with pass/fail, score, rule-by-rule breakdown, and reason -- for every gate at every stage.

### G3: User-configurable gate rules in config

**Success**: Users can define custom gate rules in `.delivery/config.yml` (or a referenced rules file) that override or extend default rules. The config schema is extended with a `rules` section, documented in `config-schema.md`.

### G4: Full audit trail

**Success**: Every rule evaluation is logged with: timestamp, gate ID, rule ID, input context, pass/fail result, score, and reason. Logs are stored in `.delivery/audit/` (or SQLite) and can be reviewed after any run.

### G5: AI stays in its lane

**Success**: AI continues to handle all creative work -- artifact production, reviews, brainstorming, feedback synthesis -- while the rules engine handles all flow control decisions. The boundary is clean: rules engine decides *what happens next*; AI decides *how to do the work*.

---

## Design Decisions

### DD1: Hybrid Rules Format (JSON engine internals, YAML user config)

**Decision**: Users customize rules in `.delivery/config.yml` (pure YAML, consistent with existing convention). The engine evaluates rules using JSON internally via the stdlib `json` module (zero external dependencies). Default rules ship as JSON files in the plugin under `references/rules/`. A translation layer converts YAML config overrides into JSON rule structures at evaluation time.

**Rationale**:
- **No external dependencies**: The `pyyaml` library is not allowed; the stdlib `json` module is the only structured data parser available.
- **YAML's implicit typing is dangerous for gate conditions**: YAML silently converts values like `on`, `off`, `yes`, `no`, `3.10` in ways that produce incorrect rule evaluations. JSON has no implicit typing -- what you write is what you get.
- **Consistency**: The existing BRE in `prd-quality-gate-flow/business_rules_engine.py` already uses JSON conditions. Keeping the same format avoids a second rule parser.
- **User experience preserved**: Users never touch JSON. They work in `.delivery/config.yml` (pure YAML) which is the established convention for this project. The translation layer is invisible to them.

### DD2: 4-Layer Rule Resolution System

Rules resolve bottom-up using a last-writer-wins model across four layers:

| Layer | Source | Mutability | Description |
|-------|--------|------------|-------------|
| **Layer 1: Plugin Defaults** | `references/rules/*.json` | Read-only, versioned | Complete rule set shipped with the plugin. Encodes current SKILL.md routing logic as deterministic rules. |
| **Layer 2: Preset Profiles** | Built-in profiles | Read-only | Named presets that override Layer 1 defaults for common team configurations. |
| **Layer 3: Per-Repo Custom** | `rules.*` keys in `.delivery/config.yml` | User-editable | Per-project overrides that tailor rules to a specific repo's needs. |
| **Layer 4: Per-Run Override** | Ephemeral natural language | Transient, not persisted | Session-scoped overrides via natural language (e.g., "run strict"). Not written to config. |

**Preset profiles** (Layer 2):
- **Solo**: Minimal ceremony. 1 validator per stage. Warnings demoted to suggestions.
- **Standard**: Balanced defaults. Default validator set. 3 collaboration patterns enabled.
- **Strict**: Full ceremony. Security validator added to all stages. Warnings promoted to blocking.

**Merge semantics**:
- Scalars: last-writer-wins (higher layer replaces lower)
- Lists: last-writer-wins by default; opt-in `_merge: extend` appends instead of replacing
- Maps: shallow-merge (higher layer keys override, unmentioned keys preserved)

### DD3: Setup Wizard Integration

The setup wizard receives 3 new questions to configure rule behavior during project onboarding:

1. **Rule Profile**: Which preset profile? (solo / standard / strict) -- auto-detected from team size and risk tolerance answers
2. **Rule Customizations**: Any per-repo overrides? (conditional -- only shown if user selects "customize" or profile detection confidence is low)
3. **Escalation Sensitivity**: How aggressively should rules escalate? (relaxed / balanced / aggressive) -- maps to escalation trigger thresholds

These questions integrate into the existing 10-question wizard flow, bringing the total to 13 questions.

### DD4: User Requirements Confirmation

User interview confirmed: "Plugin has defaults, users can modify rules per repo as needed. Setup wizard should walk them through this." This validates the 4-layer approach -- plugin ships sensible defaults (Layers 1-2), users customize per repo (Layer 3), and the wizard guides initial configuration.

---

## Existing Assets to Leverage

### 1. `prd-quality-gate-flow/business_rules_engine.py`

A deterministic rules engine already in this codebase. The core rule evaluation logic (condition parsing, field comparisons, logical operators, weighted scoring) is reusable as-is. However, the gate evaluation and audit logging layers are tightly coupled to prd-quality-gate-flow's SQLite schema (queries `nodes`, `business_rules` tables with specific columns) and will need an adapter or refactor for delivery-flow integration. Supports:

- Field comparisons (`==`, `!=`, `>`, `<`, `>=`, `<=`)
- Null checks (`IS NULL`, `IS NOT NULL`)
- Logical operators (`AND`, `OR`, `NOT`)
- Pattern matching (`MATCHES` with regex)
- Collection operations (`IN`, `NOT IN`, `.length`)
- Weighted scoring with configurable thresholds
- Critical rule failures with auto-kill
- Human review escalation triggers
- Full audit logging to SQLite

This engine evaluates rules against a context dictionary using dot-notation field paths. It produces `GateEvaluationResult` objects with decision (`GO`, `HOLD`, `RECYCLE`, `KILL`), score, rule-by-rule breakdown, and recommendations.

### 2. prd-quality-gate-flow SQLite/DAL logic (distributed)

The prd-quality-gate-flow plugin does not have a standalone `database.py`. Its SQLite schema, DAL, execution tracking, and audit logging logic is distributed across `prd_flow_builder.py`, `flow_orchestrator.py`, `check_db.py`, and `fix_and_run.py`. A new DAL module will need to be extracted or written for delivery-flow integration. (Note: `agentic-flow-builder/scripts/database.py` is a separate plugin's DAL and not directly reusable here.)

### 3. `agentic-flow-builder/`

Shares the same business rules pattern with agent registry and flow orchestrator components. Validates that the rules engine pattern works for multi-agent orchestration.

### 4. `.delivery/config.yml` + `config-schema.md` (v2.3)

Existing config infrastructure with versioned schema, migration support, and setup wizard integration. The rules engine config extension will follow the established extension protocol.

### 5. Delivery-flow hooks infrastructure

Seven existing hooks across five event types. The rules engine can integrate with hooks for enforcement (e.g., PreToolUse hook evaluates rules before allowing stage transitions).

---

## High-Level Scope

### In Scope

1. **Rules engine integration layer**: Adapt `business_rules_engine.py` for delivery-flow's decision points (stage routing, DoD gates, depth selection, escalation triggers, collaboration pattern selection).

2. **Default rule definitions as JSON files**: Ship a complete set of default rules as versioned JSON files under `references/rules/` that encode the current SKILL.md routing logic as deterministic rules. Cover:
   - Project type to stage routing map (which stages are full/light/skip)
   - DoD gate pass/fail criteria per stage
   - Depth selection rules (risk tolerance + project type + stage = depth)
   - Escalation trigger rules (repeated failures, low confidence, deadlocks)
   - Collaboration pattern selection rules (which patterns apply at which stages)

3. **Preset profiles (solo/standard/strict)**: Three built-in rule profiles that adjust rule behavior for common team configurations. Profiles override plugin defaults at Layer 2 and are selectable via the setup wizard or config.

4. **YAML-to-JSON translation layer**: A translation module that reads user rule overrides from `.delivery/config.yml` (pure YAML) and converts them into JSON rule structures for engine evaluation. Handles merge semantics (scalar replace, list replace with optional `_merge: extend`, map shallow-merge).

5. **Config schema extension**: Add a `rules` section to `config-schema.md` (v2.4) that allows users to define custom rules, override defaults, and set gate thresholds. Follow the existing extension protocol. Include `rules.profile`, `rules.escalation_sensitivity`, and per-gate override keys.

6. **Setup wizard extension (3 new questions)**: Add Rule Profile, Rule Customizations (conditional), and Escalation Sensitivity questions to the setup wizard. Auto-detect profile from existing answers where possible.

7. **Audit trail storage**: Implement structured logging of all rule evaluations to `.delivery/audit/` (format TBD: SQLite vs structured markdown vs JSON lines).

8. **SKILL.md integration**: Update delivery-flow SKILL.md to defer flow-control decisions to the rules engine rather than making them inline. The orchestrator invokes the rules engine (via Python script) at each decision point and acts on the result.

9. **Dogfooding**: Validate the rules engine by running delivery-flow through its own pipeline with the rules engine active. This is a P0 UAT gate.

### Out of Scope

1. **UI/dashboard for rule management**: Rules are configured in YAML config files, not through a GUI. A dashboard is a separate future feature.

2. **ML-based rule optimization**: Rules are authored by humans and evaluated deterministically. No AI-generated or AI-tuned rules in this iteration.

3. **Cross-pipeline rule sharing**: Rules are scoped to a single project's `.delivery/config.yml`. Sharing rules across projects is a future concern.

4. **Replacing AI for artifact quality assessment**: The rules engine handles flow control (routing, gating, escalation). Artifact quality reviews (code review, architecture review, UX review) remain AI-driven because they require creative judgment.

5. **External rules engine integration**: No integration with third-party rules engines (Drools, OPA, etc.). We use the in-repo engine.

---

## Open Questions

1. **Audit storage format**: SQLite (like `prd-quality-gate-flow`) vs JSON lines vs structured markdown? SQLite is more queryable; structured files are more git-friendly and inspectable. Need to decide based on primary use case (compliance audits favor SQLite; developer inspection favors files).

2. **Rules engine invocation mechanism**: The orchestrator is prompt-driven. How does it invoke a Python-based rules engine? Options:
   - Bash tool call to a Python script that reads context from a JSON file and writes the decision
   - Inline rule evaluation encoded in SKILL.md prompts (deterministic but not truly code-executed)
   - Hook-based: PreToolUse hook evaluates rules before stage transitions

   The first option (Bash + Python) is most consistent with the existing BRE pattern.

3. **Migration path**: How do existing pipelines transition? Options:
   - Rules engine is opt-in via config flag (`pipeline.rules_engine: true`)
   - Rules engine is always-on with defaults that match current AI behavior
   - Phased rollout: routing rules first, then DoD gates, then escalation

   Phased rollout with opt-in seems lowest risk.

4. **Context assembly for rule evaluation**: The BRE evaluates rules against a context dictionary. Who assembles that context? The orchestrator must serialize current pipeline state (project type, stage, config values, artifact statuses, validator results) into a structured dict before calling the engine. This serialization logic needs design.

5. **Fallback behavior**: If the rules engine errors or returns an unexpected result, does the pipeline fall back to AI-driven decisions or halt? Halting is safer for compliance; fallback is better for developer experience.

6. **How granular should DoD rules be?** Options:
   - Per-stage pass/fail (stage 2 DoD requires all validators DONE)
   - Per-validator rules (architect validator requires ADR present, QA validator requires test plan present)
   - Per-artifact rules (PRD must have problem statement > 100 chars, must have >= 3 success metrics)

   Per-validator seems like the right granularity -- it maps to the existing DoD validator structure.
