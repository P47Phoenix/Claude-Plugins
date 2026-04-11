# Test Strategy: MTG Commander Adversarial Review Loops

**Stage:** 05-Plan | **Role:** QA (Legolas) | **Plugin:** mtg-commander
**Pipeline:** run-2026-04-11-e6f3

---

## Approach

All changes are SKILL.md and reference markdown edits -- no executable code changes. Testing is structural validation + behavioral verification via pipeline execution.

---

## Test Cases (1:1 to FRs)

### TC-1: Challenger Agent Presence (FR-1, AC-1)

- **Method:** Structural inspection of SKILL.md
- **Pass:** 4 distinct Challenger sections exist with adversarial prompts and PASS/CHALLENGE signal format
- **Verify:** Each Challenger receives only primary output artifact (not chain-of-thought)

### TC-2: Loop Protocol (FR-2, AC-10)

- **Method:** Trace SKILL.md flow for primary->challenger->correct->re-challenge path
- **Pass:** Loop cap sourced from config; exhaustion behavior documented for all 3 modes
- **Verify:** Per-step loops explicitly stated as independent of pipeline-level correction counter

### TC-3: Config Loading -- Present (FR-3/FR-7, AC-2/AC-4)

- **Method:** Pipeline run with `.mtg-commander.yml` present (partial overrides)
- **Pass:** Config values applied; missing keys use defaults; status line shown
- **Verify:** `loops.deck_builder: 1` results in max 1 challenger loop for deck step

### TC-4: Config Loading -- Absent (FR-7, AC-3)

- **Method:** Pipeline run without `.mtg-commander.yml`
- **Pass:** Pipeline works identically to pre-config behavior; "No config, using defaults" logged
- **Verify:** All challenger loops default to 2

### TC-5: Config Loading -- Invalid (FR-7, AC-9)

- **Method:** Pipeline run with malformed `.mtg-commander.yml` (bad YAML / unknown keys)
- **Pass:** Warning emitted; pipeline does NOT fail; defaults used for invalid fields
- **Verify:** Valid fields in same file still applied

### TC-6: Price Goal -- Substitution Path (FR-4, AC-6)

- **Method:** Set `max_card_price: 5` with `escalation: false`; include cards > $5
- **Pass:** Over-goal cards auto-substituted via budget-wins; no user prompt
- **Verify:** Unsubstitutable cards included silently with note

### TC-7: Price Goal -- Escalation Path (FR-4, AC-5)

- **Method:** Set `max_card_price: 5` with `escalation: true`; include unsubstitutable cards > $5
- **Pass:** BLOCKING prompt shown with card list, prices, options a/b/c
- **Verify:** Pipeline halts until user responds; no timeout

### TC-8: DEFECT-001 Regression (FR-5, AC-7)

- **Method:** Include card with off-color identity in decklist (e.g., Sejiri Refuge in mono-W)
- **Pass:** Rules Challenger runs `validate-deck`, parses violations, issues CHALLENGE
- **Verify:** Zero tolerance for LLM-based legality -- only programmatic validation accepted

### TC-9: DEFECT-002 Regression (FR-6, AC-8)

- **Method:** Pipeline run where CK price diverges > 30% from TCG for specific cards
- **Pass:** Price Challenger flags divergence with both prices shown
- **Verify:** Total divergence > 20% triggers user escalation with vendor totals

### TC-10: Sub-Agent Guardrail Language (FR-9, AC-11)

- **Method:** `grep -cE "MUST.*sub-agent|NEVER.*inline|GUARDRAIL VIOLATION|NON-NEGOTIABLE" mtg-commander/SKILL.md`
- **Pass:** Result >= 3
- **Verify:** Session 0876a59e anti-pattern callout present verbatim

### TC-11: Pipeline Flow Diagram (FR-8)

- **Method:** Structural inspection of SKILL.md pipeline diagram
- **Pass:** Diagram shows Challenger agents at each step; reference guides list updated sections
- **Verify:** price-evaluator-guide.md has sections 2.5 and 2.6; rules-judge-guide.md mandates validate-deck

---

## Regression Safety Net

| Invariant | Verification |
|-----------|-------------|
| Pipeline works without config | TC-4 (every sprint boundary) |
| 15% hard cap unchanged | Inspect SKILL.md -- soft goal is additive, not replacement |
| No new external APIs | Grep for new API endpoints in changed files |
| Correction cycle unchanged | Pipeline-level counter independent of per-step loops (TC-2) |
| Budget-wins tiebreaker preserved | price-evaluator-guide still lists budget > synergy priority |

---

## AC-11 Grep Test (Critical Gate)

```bash
grep -cE "MUST.*sub-agent|NEVER.*inline|GUARDRAIL VIOLATION|NON-NEGOTIABLE" mtg-commander/SKILL.md
# Expected: >= 3
```

If result < 3: US-7 fails DoD. Guardrail language must be strengthened until grep passes.

---

## Test Execution Plan

- **Sprint 1 exit:** TC-1, TC-4 (foundation + backwards compat)
- **Sprint 2 exit:** TC-2, TC-3, TC-5, TC-6, TC-7, TC-8 (loops + defects + price)
- **Sprint 3 exit:** TC-9, TC-10, TC-11 (guardrails + full regression)
- **Final gate:** All TC-1 through TC-11 pass; grep test >= 3; no regressions
