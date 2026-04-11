# ADR-001: One Adversarial Challenger Per Pipeline Step

**Status:** Accepted
**Date:** 2026-04-08
**Author:** Celebrimbor (Architect)
**Pipeline:** run-2026-04-11-e6f3

---

## Context

The mtg-commander pipeline has 4 sequential agents. Each agent validates its own domain independently. When an agent passes, the pipeline advances with no second opinion. This architecture allowed DEFECT-001 (Rules Judge missed color identity via LLM inference) and DEFECT-002 (single-vendor pricing blind spot). The pipeline needs adversarial review to catch errors before they propagate.

## Decision

Add one independent Challenger sub-agent per pipeline step (4 challengers total, 8 agent invocations per run). Each Challenger is a **separate Agent tool invocation** with clean context -- it receives only the primary's structured output artifact, the original intake parameters, and the same reference guides the primary used. It never sees the primary's internal reasoning.

## Alternatives Considered

### (a) Single Combined Reviewer at End

A single "meta-reviewer" agent runs after all 4 primary agents complete, reviewing the full pipeline output.

**Rejected because:**
- Late detection: errors propagate through all 4 steps before being caught. A color identity violation (Step 2) would pass through optimization (Step 3) and pricing (Step 4) before discovery, wasting 2 agent invocations.
- Context overload: a single reviewer checking deck construction, rules legality, synergy optimization, AND pricing compliance in one pass is too broad. Each domain requires specialized knowledge.
- Correction routing is ambiguous: when the meta-reviewer finds issues spanning multiple domains, which agent corrects? The existing correction cycle routes to Deck Builder, but optimization issues should not.
- Does not fix DEFECT-001: the meta-reviewer would still be an LLM making legality judgments. Per-step challengers can be designed to mandate deterministic tools (validate-deck).

### (b) Challenger Shares Context with Primary

The challenger is invoked within the same agent session as the primary, receiving the primary's full context including internal reasoning.

**Rejected because:**
- Defeats adversarial independence. A challenger that sees the primary's reasoning inherits its assumptions and blind spots. If the primary reasoned "Sejiri Refuge is W/B because it gains life like Orzhov lands," a context-sharing challenger would see that reasoning and be biased toward agreement.
- The entire adversarial architecture (FR-1) is designed around context isolation. Sharing context is architecturally equivalent to not having a challenger.
- Correction loops require fresh invocations. A continued session accumulates prior reasoning that biases re-evaluation -- the agent is reluctant to contradict its own earlier output.

### (c) Two Challengers Per Step

Each step gets two independent challengers. Both must PASS for the step to advance.

**Rejected because:**
- Overkill for v1. The pipeline already has 4 agent invocations; adding 8 challengers (12 total) would triple worst-case invocations. User wait time becomes prohibitive.
- Diminishing returns: two challengers using the same reference guides and tools are unlikely to catch errors that one missed. The value of adversarial review comes from independence from the primary, not from redundancy among challengers.
- Can be added later if challenger catch rates prove insufficient. The per-step architecture supports N challengers without structural changes.

## Consequences

### Positive
- Each domain gets a specialist adversarial review using the same tools and references.
- DEFECT-001 is structurally fixed: the Rules Challenger mandates `validate-deck` deterministically.
- DEFECT-002 is structurally fixed: the Price Challenger independently fetches CK prices.
- Errors are caught at the step where they originate, before propagating downstream.
- Loop caps are configurable per step, allowing users to trade thoroughness for speed.

### Negative
- Worst case: 4 primary + 4 challenger + (4 steps x 2 loops x 2 invocations) = up to 24 agent invocations per run. Realistic case (most steps pass first try): 8 invocations.
- Each challenger adds latency. Mitigated by default loop cap of 2 and user-configurable reduction to 0 (skip challenger).
- Challenger echo chamber risk: challenger uses same references and may reach the same wrong conclusion. Mitigated by adversarial prompting and mandatory deterministic tools for critical checks.

### Neutral
- No new external dependencies. Challengers use existing `card_lookup.py` and reference files.
- Pipeline-level correction cycles remain unchanged. Per-step loops are independent.
- Config allows setting any step's loop count to 0, effectively disabling its challenger.

## Validation

- AC-1: Each pipeline step has an independent Challenger agent.
- AC-7: Rules Challenger runs `validate-deck` deterministically.
- AC-8: Price Challenger flags CK divergence > 30% per card.
- AC-11: Sub-agent dispatch guardrail language present in SKILL.md.
