# User Stories: MTG Commander Adversarial Review Loops + Price Enhancements

**Stage:** 05-Plan | **Role:** PO (Gandalf) | **Plugin:** mtg-commander
**Pipeline:** run-2026-04-11-e6f3 | **Type:** FEATURE
**Sprint ceiling:** 4 pts | **Hard cap:** 5 pts

---

## Capacity Declaration

- **Velocity baseline:** 8 pts/sprint (code), 6 pts/sprint (markdown-tier calibrated)
- **80% ceiling:** 6 pts/sprint (markdown-tier work)
- **Hard cap:** 5 pts single story
- **Sprint commitment:** 3 sprints planned, 18 pts total capacity
- **Total estimate:** 11 pts across 9 stories

---

## Stories

### US-1: Per-Step Challenger Agents (FR-1)

**As** a deck builder user, **I want** independent Challenger agents for each pipeline step **so that** errors are caught adversarially before propagating downstream.

**Size:** M (3 pts) | **Sprint:** 1
**Dependencies:** None (foundational)

**Acceptance Criteria:**
- AC-1.1: Deck Challenger template added to SKILL.md with adversarial prompt (re-count 100 cards, spot-check 5 synergy claims, structural minimums)
- AC-1.2: Rules Challenger template added with deterministic validation mandate
- AC-1.3: Optimization Challenger template added (independent synergy recalc, isolation detection, mana curve)
- AC-1.4: Price Challenger template added (independent CK fetch, divergence flags)
- AC-1.5: Each Challenger outputs PASS or CHALLENGE with evidence format

**Traces:** FR-1, AC-1

---

### US-2: Configurable Loop Protocol (FR-2)

**As** a deck builder user, **I want** configurable per-step correction loops **so that** I control the tradeoff between thoroughness and speed.

**Size:** M (3 pts) | **Sprint:** 2
**Dependencies:** US-1

**Acceptance Criteria:**
- AC-2.1: Loop protocol documented in SKILL.md: primary -> challenger -> PASS/CHALLENGE -> correct -> re-challenge
- AC-2.2: Loop cap sourced from config (default 2 per step)
- AC-2.3: `escalation.on_loop_exhaustion` behavior documented for all 3 modes (warn/block/best-effort)
- AC-2.4: Per-step loops explicitly independent of pipeline-level correction counter (NFR-5)
- AC-2.5: Each correction spawns a NEW primary agent (no context accumulation)

**Traces:** FR-2, AC-10

---

### US-3: `.mtg-commander.yml` Config Loading (FR-3, FR-7)

**As** a deck builder user, **I want** a per-repo YAML config file **so that** my preferences persist across pipeline runs without re-specifying.

**Size:** M (3 pts) | **Sprint:** 1
**Dependencies:** None

**Acceptance Criteria:**
- AC-3.1: Config loaded from user's working directory after intake, before pipeline banner
- AC-3.2: Missing file = all defaults, pipeline works identically to pre-config (AC-3)
- AC-3.3: Partial overrides apply; missing keys use defaults (AC-4)
- AC-3.4: Invalid keys/structure warns but does not fail pipeline (AC-9)
- AC-3.5: Schema documented in new `references/config-reference.md` with version field, all keys, defaults, valid values
- AC-3.6: Config status line shown after intake ("Config loaded" or "No config, using defaults")

**Traces:** FR-3, FR-7, AC-2, AC-3, AC-4, AC-9

---

### US-4: Enhanced Price Rules -- Soft Goal + Escalation (FR-4)

**As** a deck builder user, **I want** a soft per-card price goal with substitution-first logic **so that** I stay within budget without losing critical cards unnecessarily.

**Size:** S (2 pts) | **Sprint:** 2
**Dependencies:** US-3 (config provides `max_card_price` value)

**Acceptance Criteria:**
- AC-4.1: Over-goal cards trigger substitution attempt first (synergy + legality preserved)
- AC-4.2: Unsubstitutable cards grouped into BLOCKING escalation prompt with options a/b/c
- AC-4.3: Pipeline halts on escalation (no timeout, no auto-accept)
- AC-4.4: User-approved exceptions logged in PRICE_EXCEPTIONS section of deck output
- AC-4.5: When `escalation: false`, auto-substitute via budget-wins; no sub = include silently with note
- AC-4.6: Soft goal is separate from existing 15%-of-budget hard cap (hard cap unchanged)

**Traces:** FR-4, AC-5, AC-6

---

### US-5: DEFECT-001 Fix -- Deterministic Color Identity (FR-5)

**As** a deck builder user, **I want** the Rules Challenger to run `validate-deck` deterministically **so that** color identity violations are never missed due to LLM inference.

**Size:** S (1 pt) | **Sprint:** 2
**Dependencies:** US-1 (Rules Challenger exists)

**Acceptance Criteria:**
- AC-5.1: Rules Challenger runs `card_lookup.py validate-deck --commander "<name>" --cards "<card1>" ... "<card99>"`
- AC-5.2: Violations array parsed for `color_identity`, `format_legality`, `banned`
- AC-5.3: Any violation triggers CHALLENGE verdict
- AC-5.4: Rules Judge primary ALSO mandated to use `validate-deck` (belt and suspenders)

**Traces:** FR-5, AC-7

---

### US-6: DEFECT-002 Fix -- CK Pricing Divergence (FR-6)

**As** a deck builder user, **I want** the Price Challenger to independently verify CK prices **so that** single-vendor blind spots are surfaced.

**Size:** S (1 pt) | **Sprint:** 3
**Dependencies:** US-1 (Price Challenger exists)

**Acceptance Criteria:**
- AC-6.1: Price Challenger fetches CK prices independently via `ck-batch-price`
- AC-6.2: Per-card divergence > 30% flagged in Challenger output with both prices
- AC-6.3: Total CK vs TCG divergence > 20% escalates to user with both vendor totals
- AC-6.4: User decides which vendor to optimize for

**Traces:** FR-6, AC-8

---

### US-7: Sub-Agent Dispatch Guardrail Section (FR-9)

**As** a pipeline maintainer, **I want** explicit guardrail language in SKILL.md **so that** Claude never inlines pipeline steps regardless of context pressure.

**Size:** S (1 pt) | **Sprint:** 3
**Dependencies:** US-1

**Acceptance Criteria:**
- AC-7.1: Guardrail section uses MUST, NEVER, NON-NEGOTIABLE, GUARDRAIL VIOLATION
- AC-7.2: Lists all 8 mandatory Agent dispatches (4 primary + 4 challenger)
- AC-7.3: Includes session 0876a59e anti-pattern callout (verbatim from PRD)
- AC-7.4: `grep -cE "MUST.*sub-agent|NEVER.*inline|GUARDRAIL VIOLATION|NON-NEGOTIABLE" SKILL.md` >= 3 (AC-11)

**Traces:** FR-9, AC-11

---

### US-8: Update Reference Guides (FR-8)

**As** a pipeline maintainer, **I want** reference guides updated to reflect adversarial flow **so that** agents have accurate instructions.

**Size:** S (1 pt) | **Sprint:** 3
**Dependencies:** US-1, US-4, US-5, US-6

**Acceptance Criteria:**
- AC-8.1: `price-evaluator-guide.md` updated: per-card goal section (2.5), CK divergence section (2.6), escalation format
- AC-8.2: `rules-judge-guide.md` updated: mandate `validate-deck` as SOLE legality mechanism
- AC-8.3: New `references/config-reference.md` with full schema docs (if not created in US-3)
- AC-8.4: Pipeline flow diagram in SKILL.md updated to show Challengers

**Traces:** FR-8

---

### US-9: Dogfood -- Sub-Agent Enforcement Verification (FR-9 verification)

**As** a pipeline maintainer, **I want** a structural grep test **so that** guardrail language is verified before shipping.

**Size:** XS (0 pts -- verification only) | **Sprint:** 3
**Dependencies:** US-7

**Acceptance Criteria:**
- AC-9.1: `grep -cE "MUST.*sub-agent|NEVER.*inline|GUARDRAIL VIOLATION|NON-NEGOTIABLE" mtg-commander/SKILL.md` returns >= 3
- AC-9.2: SKILL.md reviewed for spawned-agent language that would be nonsensical if inlined
- AC-9.3: If grep fails, US-7 is reopened and language strengthened

**Traces:** FR-9, AC-11

---

## Summary & Sprint Allocation

| Story | Size | Sprint | Deps | FR |
|-------|------|--------|------|----|
| US-1  | M (3) | 1 | -- | FR-1 |
| US-3  | M (3) | 1 | -- | FR-3,7 |
| US-2  | M (3) | 2 | US-1 | FR-2 |
| US-5  | S (1) | 2 | US-1 | FR-5 |
| US-4  | S (2) | 2 | US-3 | FR-4 |
| US-6  | S (1) | 3 | US-1 | FR-6 |
| US-7  | S (1) | 3 | US-1 | FR-9 |
| US-8  | S (1) | 3 | US-1,4,5,6 | FR-8 |
| US-9  | XS (0) | 3 | US-7 | FR-9 |

**Sprint 1:** 6 pts (US-1+US-3) | **Sprint 2:** 6 pts (US-2+US-5+US-4) | **Sprint 3:** 3 pts (US-6+US-7+US-8+US-9)
**Totals:** 9 stories, 11 pts, 3 sprints -- no sprint exceeds 6-pt ceiling. All 9 FRs traced.
