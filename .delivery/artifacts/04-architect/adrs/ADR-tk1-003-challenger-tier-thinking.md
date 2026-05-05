# ADR-tk1-003: Challenger Model-Tier Inheritance + Extended Thinking Discipline

**Status**: Accepted
**Deciders**: Architect (solution_architect), Product Owner
**PRD refs**: FR-09, FR-10, FR-11
**Wave**: Wave 1 (W1-5)
**Date**: 2026-05-04
**Binds**: `delivery-team/skills/delivery-flow/SKILL.md` adversarial-review section;
           `delivery-team/hooks/audit_agent_prompt.py`

---

## Context

Anti-pattern session 0876a59e (mtg-commander) documented 14 undetected adversarial violations
caused by model capability asymmetry: a Haiku challenger reviewing a Sonnet primary's output
missed every meaningful architectural defect. The adversarial review pattern's sole architectural
property — independent critical evaluation — is nullified when the challenger lacks the capacity
to identify the defects the primary could produce.

Binding decision: skill-token-economy.md "Adversarial / challenger sub-agent rule" states
challengers MUST inherit the primary's model at dispatch time. This ADR operationalizes that
ruling and resolves the open team decision on hard-block vs warn-only enforcement.

Signal-blocks-emitted-EARLY lesson applies: the hook enforcement warning MUST appear at the
start of the hook's output block, not deferred to the end.

---

## Decision

### Challenger model-tier inheritance

1. When `delivery-flow` dispatches an adversarial challenger sub-agent, the agent frontmatter
   MUST carry `model: ${primary_model}` — the same model the primary agent used. The orchestrator
   resolves this at dispatch time from the stage's primary agent model value.

2. The adversarial-review section of `delivery-flow/SKILL.md` MUST state: "Adversarial challenger
   inherits model from primary at dispatch. Do not downgrade for cost savings."

3. **Sprint 1: warn-only**. `audit_agent_prompt.py` detects adversarial dispatches (role or prompt
   contains `adversarial`, `challenger`, `critic`, `reviewer`) and emits `## Warning` EARLY if
   `challenger.model != primary.model`. Does not block this sprint.

4. **Promotion to hard-block**: escalates (`exit 1`) when telemetry shows zero violations across
   5 consecutive runs AND a Wave 2 ADR supersedes this one. Pure Python — no LLM calls.

### Extended thinking default OFF

1. `delivery-flow/SKILL.md` frontmatter MUST declare `extended_thinking: false` as the default
   for all agent dispatches.

2. Opt-in sites (explicit per-stage annotation required):
   - Final synthesis (M4 debate cluster)
   - Opus-classified architect synthesis
   - Contested adversarial reruns (where loop 1 produced NO substantive finding)
   - Architecture Board chief-architect ruling
   - UAT go-no-go (where ≥1 validator voted NOT_DONE)

3. All other stages and all sub-agent dispatches in delivery-team: `extended_thinking: false`.
   Saves ~3× output tokens on average sub-agent calls (per skill-token-economy binding).

---

## Consequences

**Positive**:
- Preserves adversarial review's architectural value; eliminates silent quality loss.
- Warn-only sprint 1 gives telemetry data before committing to a blocking gate.
- Extended thinking OFF default delivers immediate token savings; opt-in is explicit and auditable.

**Negative / Trade-offs**:
- Warn-only does not prevent violations; a poorly-configured dispatch can still fire a downgraded
  challenger without blocking the run. Accepted for sprint 1 per team decision.
- 5-run promotion gate may delay hard-block if runs are infrequent; team MUST actively review
  telemetry rather than passively waiting.

---

## Alternatives Considered

| Option | Decision | Reason rejected |
|--------|----------|-----------------|
| Hard-block challenger mismatch sprint 1 | Rejected | No telemetry baseline yet; warn-only allows correction without pipeline stalls |
| Extended thinking ON by default (opt-out) | Rejected | Inverts safe default; silent 3× token cost on every unannotated dispatch |
| Regex-only adversarial detection | Rejected as sole mechanism | Prompt text varies; pair with role-field check for robustness |
