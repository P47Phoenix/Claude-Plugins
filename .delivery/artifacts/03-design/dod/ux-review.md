# UX Designer DoD Review — Gate 3: Design Completeness

**Reviewer**: Galadriel (UX Designer)
**Date**: 2026-04-01
**Artifact**: `.delivery/artifacts/03-design/ux/design-spec.md` v1.0
**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.1

---

## Gate 3 Criteria

### 1. Flows complete, edge cases addressed [blocking]

**PASS**

Every user-facing flow is designed end-to-end with edge case and error handling:

| Flow | Edge Cases Addressed |
|------|---------------------|
| Intake (Section 1) | 3 input modes (full inline, partial, guided). One-at-a-time questioning in partial mode. Smart defaults and contextual adaptation per prior answers. Commander recommendation sub-flow when user is unsure. |
| Validation at intake (Section 1.4) | Name typo with fuzzy suggestion (1.4A), banned commander with ban reason (1.4B), color identity conflict with explicit user choice (1.4C). System never silently overrides. |
| Partner rejection (Section 1.5) | Clear message explaining why partners are unsupported in v1, prompts for single commander. |
| Pipeline visibility (Section 2) | Banner with 4-agent sequence, per-agent sub-step progress, estimated time. User cannot intervene mid-pipeline — input queued. Two intervention points defined (intake and post-output). |
| Correction cycles (Section 4) | Violations listed with suggested replacements, cycle counter (n/3), re-validation shown. Budget-wins tiebreaker with explicit synergy tradeoff disclosure (4.2). Max cycles exhausted outputs best-effort with grouped warnings (4.3). |
| Final output (Section 5) | Summary card, categorized deck with pricing, pipeline verdicts, export-ready list, purchase summary. Post-output actions: approve, swap, rerun, adjust. |
| Error handling (Section 6) | Scryfall timeout/5xx with retry (6.1), rate limiting informational (6.1), impossible budget warning at intake (6.2), no valid commander (6.3), invalid must-include card (6.4). |
| Post-output swap (Section 5.6) | Single-card swap with full validation (Scryfall, color identity, banned, price) and synergy re-check. |

First-time use is handled by the guided mode (Mode C) — the system walks the user through all 7 questions with plain-language descriptions. No prior knowledge required.

### 2. All PRD requirements have corresponding design elements [blocking]

**PASS**

Spot-check of FR-02 (intake) and FR-07 (orchestration):

**FR-02 (Deck Builder / Intake):**

| AC | Design Coverage |
|----|----------------|
| FR-02.1: 7 intake questions in sequence | Section 1.2 — all 7 questions listed in order with smart defaults |
| FR-02.2: Inline or interactive input | Section 1.1 — 3 modes: Full Inline (A), Partial Inline (B), Guided (C) |
| FR-02.3: Commander Scryfall validation | Section 1.4A — validation with typo suggestion flow |
| FR-02.3a: Banned commander check | Section 1.4B — banned message with ban reason, prompts alternative |
| FR-02.4: Color identity derived from commander | Section 1.4C — cross-check with conflict resolution, user decides |
| FR-02.5: Exactly 100 cards | Section 3.1 — "Total: 100 cards" shown in output |
| FR-02.6: Cards assigned to categories | Section 3.1 — 8 categories shown with card counts |
| FR-02.7: Grouped output with synergy rationale | Section 3.1 — card name, mana cost, one-sentence rationale per non-land card |
| FR-02.8: Game plan before card list | Section 3.1 — "Game Plan" block at top of deck output |
| FR-02.9: Pre-validation during construction | Section 2.2 — Deck Builder progress shows "Validating card names against Scryfall (batch lookup)" |
| FR-02.10: Partner commander rejection | Section 1.5 — explicit rejection message with v1 explanation |

**FR-07 (Orchestration):**

| AC | Design Coverage |
|----|----------------|
| FR-07.1: Sequential pipeline | Section 2.1 — 4-agent banner in order: Deck Builder > Rules Judge > Optimization Reviewer > Price Evaluator |
| FR-07.2: FAIL cycles back to Deck Builder | Section 4.1 — correction cycle with violations, corrections, re-validation narrative |
| FR-07.3: Uses existing config mechanism | Internal config — not a UX surface, no design element needed |
| FR-07.4: Max cycles + budget priority | Section 4.3 — max cycles exhausted with best-effort output. Section 4.2 — budget-wins tiebreaker with synergy threshold relaxation disclosure |
| FR-07.5: Final formatted output | Section 5.1 (summary card), 5.2 (categorized list with pricing), 5.3 (verdicts) |
| FR-07.6: Export-ready card list | Section 5.4 — one card per line, basic land quantity notation |
| FR-07.7: Agent verdicts preserved | Section 5.3 — all 4 agent verdicts shown in pipeline results block |

All acceptance criteria for FR-02 (11 ACs) and FR-07 (7 ACs) have corresponding design elements. No gaps found.

---

## Verdict

**STATUS: DONE**
