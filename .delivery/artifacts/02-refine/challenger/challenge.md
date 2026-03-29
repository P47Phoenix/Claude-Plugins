# Adversarial Review: Rules Engine Integration PRD v2.0

**Reviewer**: Challenger
**Date**: 2026-03-28
**PRD Version**: 2.0
**Previous Review**: v1.0 (3 critical, 8 high/medium -- all resolved or addressed in v2.0)
**Status**: Complete

---

## Prior Challenge Resolution Assessment

Before stress-testing new content, confirming the v1.0 critical findings are genuinely resolved:

| v1.0 Challenge | Status | How Resolved |
|----------------|--------|-------------|
| Challenge 1: BRE coupling deeper than admitted | **Resolved.** | FR-01 now calls for line-by-line audit. FR-02 explicitly states "partial rewrite, not a thin wrapper." Phase 0 added for extraction. Dependencies table is honest about what is reusable vs. must rebuild. |
| Challenge 2: Untestable "match current behavior" | **Resolved.** | FR-18 introduces the Routing Decision Specification as the normative reference. NFR-04 says defaults match the specification, not observed AI behavior. PO sign-off required before implementation. |
| Challenge 3: Undefined determinism boundary | **Resolved.** | Section 5 (Determinism Boundary) classifies every decision point into categories (a)/(b)/(c). Honest about hybrid decisions. Strict mode eliminates category (c) for routing. Audit trail tags every decision with its category. |
| Challenge 5: Skip vs. light contradiction | **Resolved.** | US-06 AC-4 now says "no stages are executed at depth less than light." FR-15 says "Light means reduced depth, never skipped." No more skip language. |

All three critical and the high-severity contradiction are resolved. The PRD v2.0 is substantively stronger. The remaining v1.0 medium/low challenges (tamper-evidence, rule versioning, unmeasurable metrics, dry-run mode, AI fallback in default mode) are partially addressed or acknowledged as open questions.

---

## Challenge 1: 4-Layer Resolution -- The Layer 4 Parsing Trap

**Target**: DD2 (4-layer resolution), OQ-3 (Layer 4 parsing)

**Challenge**: Layer 4 (per-run natural language override) is the weakest link in an otherwise sound resolution system. The PRD acknowledges this in OQ-3 ("inherently an AI task") and wisely disables it in strict mode. But in default and solo modes, Layer 4 is active, and the parsing is best-effort AI interpretation.

The edge case: a user says "run this lighter" and the AI maps it to `rules.preset: solo` -- overriding their carefully configured Layer 3 per-repo rules. Layer 4 is last-writer-wins, meaning a vague natural language command can silently replace specific, deliberate Layer 3 configuration. The user set `rules.pass_threshold.development: 95` in their config (Layer 3), then casually says "keep it light" and the AI wipes their development threshold by applying the solo preset at Layer 4. The audit trail logs the override, but the damage is done.

Worse: Layer 4 overrides are transient and not persisted, so there is no config diff to review. The user may not even realize their Layer 3 rules were overridden until they inspect the audit log after a gate passed that should not have.

**Risk**: Solo and default mode users -- the majority segment -- get surprising layer interactions that undermine trust in the very configurability the system promises.

**Severity**: High

**Recommendation**: Layer 4 should apply granular overrides only, never preset-level overrides. If the AI parses "run this lighter," it should adjust specific thresholds, not swap the entire preset. Alternatively, Layer 4 should only be additive (can tighten rules, not relax them) unless the user uses explicit syntax. Add a confirmation prompt when Layer 4 would override Layer 3 values: "This override will replace your configured development pass threshold (95) with the solo default (80). Proceed?"

---

## Challenge 2: Translation Layer -- The Silent Corruption Vector

**Target**: DD1 (hybrid format), FR-10, US-13

**Challenge**: The YAML-to-JSON translation layer (`yaml_to_rules.py`) is a new, critical-path component with a dangerous failure mode: silent data corruption. The PRD correctly identifies YAML type coercion as a risk (US-13 AC-4 logs warnings), but the mitigation is insufficient for three reasons:

1. **The translation layer cannot parse YAML itself.** NFR-07 prohibits `pyyaml`. The PRD says the orchestrator parses YAML and passes structured data to the translation layer. But how does the orchestrator parse YAML? It is an AI agent reading a YAML file. The AI's YAML parsing is itself non-deterministic -- it might or might not notice that `3.10` becomes `3.1` or that `no` becomes `false`. The type coercion detection in US-13 AC-4 assumes the translation layer receives both the raw string and the coerced value, but if the AI already coerced it during parsing, the translation layer has no raw value to compare against.

2. **Warning is not sufficient for gate rules.** If YAML coercion silently changes a pass threshold from `3.10` to `3.1` (or a validator name from `no` to `false`), a warning logged after the fact does not prevent a wrong gate decision. Priya specifically flagged this: "coerced value in a gate rule is a compliance incident." The persona validation report recommends promoting warnings to errors in strict mode -- the PRD does not yet incorporate this.

3. **No round-trip verification.** The PRD does not require that the translation layer verify its output against the original intent. A simple round-trip test (translate YAML to JSON, then back, check equivalence) would catch coercion errors before they reach the engine. This is absent.

**Risk**: The translation layer becomes the single point of failure for configuration correctness. A subtle type coercion bug in the translation layer produces wrong gate decisions with full confidence and a clean audit trail -- the worst kind of failure because it looks correct.

**Severity**: Critical

**Recommendation**: Three actions. (1) Add FR or AC requiring strict mode to promote YAML coercion warnings to hard errors (per Priya's feedback in persona validation). (2) Define explicitly how the orchestrator reads YAML without `pyyaml` -- if it is AI-parsed, acknowledge that the YAML-to-structured-data step is category (c) non-deterministic and add it to the Determinism Boundary table. (3) Add a validation step to the translation layer that checks all rule values against expected types defined in the rule schema (e.g., pass thresholds must be numeric, validator names must be strings matching a known set).

---

## Challenge 3: Preset Coverage Gap -- The "Standard" Trap

**Target**: DD2 (preset profiles), FR-07, persona validation

**Challenge**: Three presets (solo/standard/strict) map to three archetypes (Sarah/Marcus/Priya+Chen). But the persona interviews reveal that Marcus actually lives between standard and strict. He wants `standard` defaults but with `rules.pass_threshold.development: 95` for his API repo and security validator on the payments module. Priya wants strict but with custom compliance validators added. Jake does not map to any preset -- he wants solo + GAME_DEV routing, which the PRD handles through project type, not preset.

The real gap is Marcus's team. Standard is too loose for their core API. Strict is too heavy for their internal tools. Marcus will use standard + heavy Layer 3 customization, which means the "standard" preset provides almost no value to him -- it is just a starting point he immediately overrides. The preset system promises "one setting, predictable behavior" (Sarah's magic wand) but delivers "one setting + 15 lines of YAML overrides" for the team lead segment.

This is not a blocking issue, but it reveals that "standard" is trying to be the default for too many segments. The gap between standard and strict is wider than the gap between solo and standard.

**Risk**: The team lead segment -- the highest-pain, highest-enthusiasm adopter (Marcus, 5/5 priority) -- gets the least value from presets and the most configuration burden. If Marcus's experience is "I set standard and then override everything," the preset promise rings hollow.

**Severity**: Medium

**Recommendation**: Consider whether a 4th preset (e.g., "team" positioned between standard and strict -- adds security validator to critical stages, raises thresholds for core services, but does not require full ceremony on all stages) would reduce Layer 3 burden for the team lead segment. Alternatively, acknowledge in the PRD that standard is a starting point for team leads, not a complete configuration, and provide documented example configs for common team patterns (e.g., "standard + elevated API quality" example in config-schema.md v2.4).

---

## Challenge 4: Wizard Integration -- The 13-Question Threshold

**Target**: DD3, FR-17, persona validation

**Challenge**: The existing wizard has 10 questions. Adding 3 makes 13. Sarah said "three questions is fine." Jake said "three questions is fine." But both are reacting to the 3 new questions in isolation, not the cumulative 13-question experience. No persona was asked: "How do you feel about a 13-question setup wizard?"

The conditional display on W-12 (hidden unless the user selects "customize" or confidence is low) mitigates this somewhat -- in the best case, solo users answer 12 questions (W-12 hidden). But Priya said her team would never use the wizard for production setup. Marcus did not raise concerns about wizard length because his team lead workflow is config-template-based.

The risk is not that 13 questions is objectively too many -- it is that the wizard's value proposition degrades with length. The first 10 questions configure the pipeline. The next 3 configure the rules engine. A new user does not know what a "rule profile" or "escalation sensitivity" is at setup time. They have not used the pipeline yet. They are making configuration decisions without context.

**Risk**: New users pick defaults on W-11/W-12/W-13 without understanding the implications, then later discover their rule configuration is wrong and have to manually edit config.yml anyway -- defeating the wizard's purpose.

**Severity**: Low

**Recommendation**: This is acceptable as-is with one enhancement: W-11 auto-detection from Q3 (already specified) combined with a "skip rules setup (use recommended defaults)" meta-option at W-11 that bypasses W-11/W-12/W-13 entirely. Users who want to get started fast can defer rules configuration to when they understand the system better. The wizard writes `rules.preset: {auto-detected}` silently. This reduces the worst-case to 10 questions for first-time users.

---

## Challenge 5: Dry-Run Mode -- The Highest-Severity User Gap

**Target**: Persona validation synthesis, FR-11

**Challenge**: The persona validation report identifies dry-run mode as the highest-severity gap, raised independently by Sarah (preview before committing) and Chen (CI/CD validation). The PRD mentions `--compare` in the risks section for migration purposes but does not include a general-purpose `--dry-run` flag in FR-11 or any user story.

This is not a nice-to-have. Chen needs `--dry-run` for CI/CD pre-merge validation -- a use case that is explicitly enabled by this PRD (Section 9 item 6 acknowledges CI/CD integration as a fast-follow). If `--dry-run` ships as a fast-follow rather than with the initial release, Chen's CI/CD integration is blocked until the follow-up, which defeats the purpose of making the rules engine the foundation for CI/CD.

Sarah needs dry-run to build trust. She switched from 3/5 to 4/5 priority precisely because deterministic routing lets her predict behavior. But prediction requires a preview mechanism. Without `--dry-run`, Sarah's only option is to run the full pipeline and hope -- which is her current frustration.

**Risk**: The two personas who increased priority (Sarah 3->4, Jake 3->4) did so based on predictability. Dry-run is the predictability interface. Without it, the rules engine delivers determinism that users cannot easily observe before committing to a run.

**Severity**: High

**Recommendation**: Add `--dry-run` to FR-11 as a Must Have. The evaluation script already outputs JSON to stdout -- `--dry-run` simply skips pipeline execution after outputting the routing/gate decision. Minimal additional implementation effort (it is a flag that prevents side effects after evaluation). Add a user story: "As a developer, I want to preview what the rules engine would decide for my project before running the pipeline, so that I can validate my configuration and predict pipeline duration." This is low-effort, high-impact, and directly addresses the top user gap from persona validation.

---

## Challenge 6: Scope Realism -- 18 FRs, 15 Stories, 4 Phases

**Target**: Section 11 (Timeline), Sections 6-7

**Challenge**: The PRD specifies 18 functional requirements, 15 user stories, 8 non-functional requirements, and 4 open questions, organized across 4 phases (0 through 3). This is a substantial scope. Let me stress-test the phase boundaries:

**Phase 0** (FR-01, FR-18) is well-scoped -- extraction and specification. Low risk.

**Phase 1** (FR-02, FR-03, FR-05, FR-10, FR-11, FR-15) is the heaviest phase: adapter layer, routing rules for all 126 combinations (6 types x 7 stages x 3 risk tolerances), context serialization, translation layer, evaluation script, and depth selection. FR-03 alone (encoding 126 routing combinations as JSON rules) is a significant authoring effort. FR-10 (translation layer) is a new, critical-path component with the coercion risks identified in Challenge 2. Phase 1 has 6 FRs and is the foundation for everything else.

**Phase 2** (FR-04, FR-08, FR-09, FR-12, FR-14, FR-16) is also 6 FRs, including DoD gate rules for all 7 pipeline stages with per-validator granularity (FR-04) and config schema extension (FR-12).

**Phase 3** (FR-06, FR-07, FR-13, FR-17) looks lighter but includes SKILL.md integration (FR-13) -- which is arguably the highest-risk FR because it changes how the orchestrator itself operates -- and the dogfooding run (US-10), which is a full pipeline execution that may surface integration issues.

The concern is not that any single FR is unreasonable, but that:
- Phase 1 and Phase 2 each carry 6 FRs with no explicit prioritization within the phase.
- FR-13 (SKILL.md integration) in Phase 3 is the actual "make it work end-to-end" FR. If Phases 1-2 slip, Phase 3 (where the system actually becomes usable) gets compressed.
- The 4 open questions (OQ-1 through OQ-4) all need resolution by Phase 1 or Phase 2 start. If decisions stall, phases stall.

**Risk**: Phase 1 takes longer than expected (FR-03's 126-combination matrix, FR-10's coercion edge cases), Phase 2 gets compressed, Phase 3 (where users actually see value) is rushed, and the dogfooding run (US-10) becomes a checkbox rather than genuine validation.

**Severity**: Medium

**Recommendation**: The scope is achievable but has no slack. Three mitigations: (1) Resolve OQ-1 through OQ-4 before Phase 0 ends, not at Phase 1/2 start. (2) Within Phase 1, identify FR-03 (126 routing combinations) as the long pole and consider whether the Routing Decision Specification (FR-18 in Phase 0) can pre-generate the JSON rule structure to reduce Phase 1 authoring effort. (3) Add an explicit "integration checkpoint" between Phase 2 and Phase 3 where FR-11 (evaluation script) is tested end-to-end with FR-02 (adapter), FR-03 (routing), and FR-04 (DoD gates) before SKILL.md integration begins -- catching integration issues early rather than during the dogfooding run.

---

## Challenges Not Raised (Considered but Not Escalated)

| Topic | Why Not Escalated |
|-------|-------------------|
| Audit log tamper-evidence (v1.0 Challenge 6) | Still absent from the PRD, but Priya's persona validation does not re-raise it as blocking. Acceptable as a fast-follow for enterprise hardening. |
| Rule definition versioning (v1.0 Challenge 7) | Still absent. Rules are version-controlled via git, which provides implicit versioning. Formal rule versioning is a real concern but acceptable for v1. |
| AI fallback option in default mode (v1.0 Challenge 10) | US-11 AC-3 still offers "Skip this gate (AI evaluation)" in non-strict mode. Chen warned against it. However, it is user-initiated and logged, which is an acceptable compromise for non-strict mode. |
| Sub-200ms routing performance target | Jake requested sub-200ms. NFR-01 says sub-500ms. The risks section mentions sub-200ms as a target for routing specifically. Not escalated because the risks section already acknowledges it and the benchmark requirement in Phase 1 will surface issues early. |
| Audit log JSON Schema definition | Priya requested it. Not in the PRD. Low effort to add but not blocking -- the field list in FR-06 is sufficient for implementation. Schema can be derived from implementation. |

---

## Overall Assessment

### What PRD v2.0 Gets Right That v1.0 Did Not

1. **Determinism Boundary (Section 5)** is the standout improvement. Honest, detailed, and auditor-friendly. The category (a)/(b)/(c) classification is exactly what was missing.
2. **Phase 0 extraction** (FR-01 + FR-18) front-loads the two highest-risk activities. Smart phasing.
3. **Routing Decision Specification** (FR-18) replaces the untestable "match current behavior" with a normative reference. This was the most important fix.
4. **BRE reuse honesty** -- FR-02 now says "partial rewrite, not a thin wrapper." The dependencies table quantifies what is reusable vs. what must rebuild. No more hidden effort.
5. **Persona validation** is thorough. 5 personas, 2 rounds, concern resolution tracking. The PRD is grounded in real user needs.

### What Needs Work Before Design

1. **Translation layer YAML parsing chain** (Challenge 2) -- the orchestrator's AI-based YAML parsing is a category (c) non-deterministic step not acknowledged in the Determinism Boundary. Strict mode needs coercion-as-error.
2. **Dry-run mode** (Challenge 5) -- highest-severity gap from persona validation, low implementation cost, should be promoted to Must Have in FR-11.
3. **Layer 4 override scope** (Challenge 1) -- transient natural language overrides that silently replace deliberate Layer 3 config are a trust risk.

### What Is Acceptable As-Is

- Preset coverage gap (Challenge 3) -- solvable with documented example configs, does not need a 4th preset.
- Wizard length (Challenge 4) -- 13 questions is fine with the auto-detection and conditional display already specified.
- Scope realism (Challenge 6) -- achievable with the mitigations recommended. No single FR is unreasonable.

---

## Confidence Rating: 4 / 5

**PRD is strong with targeted gaps to close before design.**

PRD v2.0 is a significant improvement over v1.0. The three critical findings from v1.0 are all resolved. The Determinism Boundary, Routing Decision Specification, and honest BRE sizing give the team a solid foundation for implementation.

One new critical finding (Challenge 2: translation layer parsing chain) and two high findings (Challenge 1: Layer 4 override scope, Challenge 5: dry-run mode) need resolution. All three are addressable within a PRD revision without architectural changes:

- Challenge 2 requires adding the YAML parsing step to the Determinism Boundary and promoting coercion warnings to errors in strict mode (2-3 AC additions).
- Challenge 5 requires adding `--dry-run` to FR-11 and one new user story (minimal spec work).
- Challenge 1 requires scoping Layer 4 override behavior to prevent preset-level overrides (one AC addition to US-11 or DD2).

**No escalation to human required.** The PRD can proceed to design after these targeted revisions.
