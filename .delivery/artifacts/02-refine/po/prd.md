# PRD: MTG Commander Adversarial Review Loops + Price Rule Enhancements

**Pipeline:** run-2026-04-11-e6f3 | **Type:** FEATURE | **Plugin:** mtg-commander
**Author:** PO (Gandalf) | **Status:** Draft

---

## Problem Statement

The mtg-commander pipeline's four agents validate their own domains independently with no adversarial cross-check. When an agent passes, the pipeline advances -- no second opinion, no challenger, no skeptical review within a step. This architecture allowed DEFECT-001 (Rules Judge missed color identity via LLM inference) and DEFECT-002 (single-vendor pricing blind spot). Additionally, the per-card price cap is a hard wall with no user negotiation when budget-optimal cards exceed it.

## Functional Requirements

### FR-1: Per-Step Adversarial Challenger Agent

For each of the 4 pipeline steps (Deck Builder, Rules Judge, Optimizer, Price Evaluator), add an independent Challenger sub-agent. The Challenger reviews the primary agent's output from a skeptical perspective using the same reference guides but performing independent verification. The Challenger outputs one of:

- **PASS** -- output is sound, advance pipeline
- **CHALLENGE** -- specific findings with evidence, return to primary for correction

The Challenger is a separate Agent tool invocation from the primary. It must NOT share context with the primary agent's internal reasoning -- only the primary's output artifact.

### FR-2: Configurable Loop Per Step

Each pipeline step executes: primary agent produces output, Challenger reviews, if CHALLENGE then primary corrects and Challenger re-reviews. Maximum loop iterations are configurable per step. Default: 2 iterations per step. If maximum exceeded: behavior governed by `escalation.on_loop_exhaustion` config (warn, block, or best-effort).

Loop flow per step:
```
Primary Agent -> output -> Challenger -> PASS? advance : CHALLENGE -> Primary corrects -> Challenger re-reviews -> ... (up to max)
```

This is distinct from the existing pipeline-level correction cycle (which routes FAILs back to Deck Builder). Per-step loops are intra-step; the existing correction cycle is inter-step.

### FR-3: User-Repo Config File `.mtg-commander.yml`

A YAML config file loaded from the user's working directory (NOT the plugin directory). Schema:

```yaml
loops:
  deck_builder: 2
  rules_judge: 2
  optimizer: 2
  price_evaluator: 2

price_rules:
  max_card_price: null        # soft goal in USD, null = no goal
  max_card_escalation: true   # escalate to user if goal unachievable
  budget_source: "higher"     # "higher" | "tcg" | "ck" -- which vendor total for budget check

escalation:
  on_loop_exhaustion: "warn"  # "warn" | "block" | "best-effort"
```

- When file is absent: all defaults apply, pipeline works identically to current behavior
- When file is present: validate schema, apply overrides
- When file has invalid keys or structure: warn user, use defaults for invalid fields (do not fail pipeline)

### FR-4: Enhanced Price Rules -- Soft Per-Card Price Goal with Escalation

`max_card_price` is a GOAL, not a hard cap. Behavior:

1. Price Evaluator builds the deck optimally (synergy + legality first)
2. After pricing, check each card against `max_card_price`
3. If all cards are under the goal: proceed normally
4. If cards exceed the goal, the Price Evaluator follows this escalation sequence:
   - **Step 1 -- Substitution attempt**: For each over-goal card, search for a budget-valid substitution that maintains synergy and legality. If a valid substitution exists, swap silently and note in output (e.g., "Swapped Card A ($Y) -> Card B ($Z) to meet $X goal").
   - **Step 2 -- Escalation for unsubstitutable cards**: If ANY card exceeds the goal and NO substitution exists that maintains both synergy and legality, ESCALATE to user with a BLOCKING prompt:

```
These N cards exceed your $X per-card price goal (no budget-valid substitution found):
  - Card A: $Y (goal: $X) -- reason: unique combo enabler, no cheaper alternative maintains the synergy line
  - Card B: $Z (goal: $X) -- reason: only format-legal card with this effect

Options:
  (a) Accept exception for these specific cards (logged in deck output)
  (b) Raise per-card goal to $NEW_AMOUNT
  (c) Force budget-relaxed substitution (may reduce synergy)
```

   - **Step 3 -- Escalation is BLOCKING**: Pipeline pauses at this point. The user MUST respond before the pipeline advances. No timeout, no auto-accept.
   - **Step 4 -- Log exceptions**: User-approved exceptions are logged in the final deck output: "User approved $Y for Card A, exceeding $X goal (reason: [user's stated reason or 'accepted without comment'])"

5. If `max_card_escalation` is false: auto-substitute with cheaper alternatives (budget-wins tiebreaker applies). If no substitution exists, include the over-goal card silently with a note in output.

This is separate from the existing 15%-of-budget per-card CAP (which remains as a hard rule). The goal is a user-defined soft target on top of the hard cap.

### FR-5: DEFECT-001 Fix -- Deterministic Color Identity Validation

The Rules Judge Challenger MUST execute `validate-deck` programmatically for every card in the decklist. Zero tolerance for LLM-knowledge-based legality claims. The Challenger specifically:

1. Runs `card_lookup.py validate-deck --commander "<name>" --cards "<card1>" ... "<card99>"`
2. Parses the `violations` array
3. Any `color_identity`, `format_legality`, or `banned` violation triggers CHALLENGE

This ensures color identity is checked deterministically regardless of what the primary Rules Judge reports.

### FR-6: DEFECT-002 Fix -- CK Pricing Divergence Escalation

The Price Evaluator Challenger independently fetches Card Kingdom prices via `ck-batch-price` and compares against the primary agent's TCGPlayer prices. For each card where divergence exceeds 30%:

- Flag in Challenger output with both prices shown
- If total CK cost diverges > 20% from total TCG cost: escalate to user with both vendor totals
- User decides which vendor to optimize for (or accepts the higher total as the budget check)

### FR-7: Config File Loading Protocol

At pipeline start (before intake or after intake, before Agent 1):

1. Check working directory for `.mtg-commander.yml`
2. If absent: log "No user config found, using defaults" and continue
3. If present: parse YAML, validate against schema, apply overrides
4. If parse fails or invalid structure: warn "Config file has errors, using defaults for invalid fields" and continue (never fail the pipeline due to config)

### FR-8: Updated SKILL.md Documentation

Update `mtg-commander/SKILL.md` to document:
- The adversarial Challenger loop at each pipeline step
- The `.mtg-commander.yml` config file schema and defaults
- The enhanced price rules (soft goal + escalation)
- Updated pipeline flow diagram showing Challenger agents

### FR-9: Sub-Agent Dispatch is NON-OPTIONAL (Guardrail)

Every pipeline step -- Deck Builder, Rules Judge, Optimizer, Price Evaluator, AND all Challenger agents -- MUST be dispatched as a separate sub-agent via the Agent tool. This is a NON-NEGOTIABLE architectural invariant.

**Rationale:**

1. **Context isolation**: Each agent must be "context pure on intent." A Rules Judge that shares the Deck Builder's context inherits the builder's assumptions and blind spots. Separate sub-agents cannot see each other's internal reasoning.
2. **Adversarial independence**: Challengers cannot be adversarial if they share the primary agent's context. The entire adversarial review architecture (FR-1) is defeated by inlining.
3. **Correction loop integrity**: Each correction cycle requires a fresh agent invocation. A continued session accumulates prior reasoning that biases re-evaluation.

**SKILL.md must contain an explicit guardrail section with:**

- Clear statement that every pipeline step MUST be a separate sub-agent via the Agent tool
- Statement that inlining ANY pipeline step is a GUARDRAIL VIOLATION -- equivalent to skipping DoD in delivery-flow
- Use of the strongest directive language: "MUST", "NEVER", "NON-NEGOTIABLE", "GUARDRAIL VIOLATION"
- A "Common Anti-Pattern" callout quoting the real session failure:

> **Common Anti-Pattern (GUARDRAIL VIOLATION):** In session 0876a59e, Claude stated: *"I'll run the agent roles inline rather than spawning subagents (keeps context in one place and avoids re-deriving your intake)"*. Result: Rules Judge, Optimization Reviewer, and Price Evaluator were all inlined. No adversarial review occurred. No independent validation happened. This is the EXACT failure mode this guardrail prevents.

**Verification:** `grep SKILL.md` for `MUST.*sub-agent`, `NEVER.*inline`, and `GUARDRAIL VIOLATION` -- expect >= 3 matches. If Claude can read the SKILL.md and still choose to inline, the language is not strong enough.

**This requirement overrides the general Claude Code harness default of "don't spawn agents unless asked."** For mtg-commander pipeline workflows, sub-agent spawning is mandatory and pre-authorized.

## Non-Functional Requirements

- **NFR-1**: No new external dependencies. Challengers use existing `card_lookup.py` and reference files.
- **NFR-2**: Backwards compatible. Pipeline works identically without `.mtg-commander.yml`.
- **NFR-3**: Challenger agents use the same reference files as primary agents. No new reference files needed.
- **NFR-4**: Escalation messages must be clear enough for non-technical MTG players.
- **NFR-5**: Per-step loops do not reset the pipeline-level correction counter. They are independent.

## Acceptance Criteria

- **AC-1**: Each pipeline step (Deck Builder, Rules Judge, Optimizer, Price Evaluator) has an independent Challenger agent that reviews the primary output before advancing.
- **AC-2**: Challenger loops are configurable per step via `.mtg-commander.yml` with defaults of 2.
- **AC-3**: Pipeline works correctly when `.mtg-commander.yml` is absent (all defaults).
- **AC-4**: Pipeline works correctly when `.mtg-commander.yml` has partial overrides (missing keys use defaults).
- **AC-5**: `max_card_price` goal triggers user escalation when cards exceed it and `max_card_escalation` is true.
- **AC-6**: `max_card_price` goal auto-substitutes when `max_card_escalation` is false.
- **AC-7**: Rules Judge Challenger runs `validate-deck` deterministically (DEFECT-001 closure).
- **AC-8**: Price Evaluator Challenger flags CK divergence > 30% per card and > 20% total (DEFECT-002 closure).
- **AC-9**: Invalid config file warns but does not fail the pipeline.
- **AC-10**: `on_loop_exhaustion` controls behavior when max loops exceeded (warn / block / best-effort).
- **AC-11**: `grep SKILL.md` for `MUST.*sub-agent`, `NEVER.*inline`, and `GUARDRAIL VIOLATION` returns >= 3 matches. Sub-agent dispatch guardrail language is unambiguous and uses strongest directive terms.

## Out of Scope

- New card evaluation engines or APIs
- Partner commander support
- New archetypes or archetype detection changes
- Changes to intake flow or final output format structure (beyond escalation prompts)
- Delivery-flow pipeline integration for mtg-commander
- Rewriting core agent prompts (augment with Challengers, do not replace)

## Success Metrics

- DEFECT-001 regression: zero color identity misses across test cases TC-1 through TC-4
- DEFECT-002 mitigation: CK pricing divergence surfaced to user in 100% of cases where divergence > 30%
- Challenger catch rate: Challengers identify at least 1 finding per 3 pipeline runs (measured over 10 runs)
- Config adoption: pipeline correctly loads and applies all config overrides without error

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Challenger echo chamber -- Challenger uses same references and reaches same wrong conclusion as primary | Medium -- defeats adversarial purpose | Challenger prompt emphasizes skepticism and independent verification; DEFECT-001 fix mandates deterministic tools |
| Loop slowdown -- 4 steps x 2 loops = 8 additional agent invocations worst case | High -- user wait time doubles | Default loops to 2; config allows users to reduce to 1 or 0 (skip challenger); parallel challenger where possible |
| Config schema drift -- config schema evolves but old configs lack new keys | Medium -- silent misconfiguration | Schema validation with defaults for missing keys; never fail on unknown keys |
| Escalation fatigue -- frequent user prompts for price exceptions disrupt flow | Medium -- user abandons pipeline | Group all price exceptions into single escalation prompt; default `max_card_price` to null (off) |
