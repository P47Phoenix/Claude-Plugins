# Dev Log: US-7 + US-1 + US-2

**File:** `mtg-commander/SKILL.md`
**Developer:** Gimli (delivery-team:developer)
**Date:** 2026-04-08

## US-7 — Sub-Agent Dispatch Guardrail

- Inserted `## Sub-Agent Dispatch Guardrail` after intro, before Required Setup
- MUST/NEVER/NON-NEGOTIABLE count: 10 (AC-11 gate requires >= 3)
- Anti-pattern callout quotes session 0876a59e verbatim
- Rationale covers: context isolation, adversarial independence, correction loop integrity
- All 8 dispatches (4 primary + 4 challenger) enumerated

## US-1 — Challenger Agent Definitions

- Inserted `## Challenger Agents` after Agent 4 (Price Evaluator), before Correction Cycles
- 4 challengers defined: Deck, Rules, Optimization, Price
- Each challenger specifies: inputs, verification method, what it flags
- DEFECT-001 (Rules): mandate validate-deck as sole legality mechanism
- DEFECT-002 (Price): independent CK fetch, 30% per-card / 20% total divergence thresholds
- Signal format: CHALLENGER_VERDICT: PASS|CHALLENGE + FINDINGS + SUMMARY

## US-2 — Adversarial Loop Protocol

- Inserted `## Adversarial Loop Protocol` immediately after Challengers
- Flow: Primary -> Challenger -> (CHALLENGE: new primary + new challenger) -> loop
- Loop cap from `.mtg-commander.yml` (default 2 per step)
- Loop exhaustion: warn (default) / block / best-effort per config
- Visibility format with [NC] challenger indicators
- Fresh agent spawns each iteration (references guardrail section)

## Verification

- `grep -c 'MUST\|NEVER\|NON-NEGOTIABLE'` = 10 (pass)
- 4 challenger headings confirmed
- All existing content preserved (no deletions)
