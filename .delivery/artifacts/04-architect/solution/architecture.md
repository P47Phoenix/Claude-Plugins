# Solution Architecture: Adversarial Review Loops + Price Enhancements

**Stage:** 04-Architect (Light) | **Role:** Celebrimbor | **Plugin:** mtg-commander
**Pipeline:** run-2026-04-11-e6f3 | **Type:** FEATURE

---

## 1. Context

Augmenting the existing 4-agent MTG pipeline with: per-step adversarial challengers (separate Agent spawns), `.mtg-commander.yml` user-repo config, and enhanced pricing (soft per-card goals + CK divergence). Existing flow, correction cycles, budget-wins tiebreaker, and output format are preserved.

## 2. Resolved Open Questions from Galadriel

**Q1 -- Context scope**: Challengers receive primary's output artifact + intake params (objective inputs for drift detection). Never the primary's chain-of-thought.

**Q2 -- Cross-domain pipelining**: Strictly sequential. Step 2 waits for Step 1C PASS. Challengers may trigger corrections that change deck state.

**Q3 -- Escalation stacking**: Loop exhaustion resolves first. Challenger must reach verdict before price goal flow evaluates.

**Q4 -- Config versioning**: Add `version: 1`. Unknown keys warned/ignored, missing keys default.

## 3. Adversarial Loop Architecture

```
Primary (Agent spawn) -> output -> Challenger (separate Agent spawn, clean context)
  -> PASS: advance | CHALLENGE: NEW primary spawn with findings -> NEW challenger -> loop until PASS or cap
```

Per-step loops are independent of pipeline-level correction counter. Default cap: 2. Exhaustion: `escalation.on_loop_exhaustion` (warn/block/best-effort).

## 4. `.mtg-commander.yml` Config Schema

```yaml
version: 1
loops:
  deck_builder: 2
  rules_judge: 2
  optimizer: 2
  price_evaluator: 2
price_rules:
  max_card_price: null      # soft goal USD, null = off (15% cap remains)
  escalation: true          # user prompt if goal unmet
  budget_source: higher     # higher | tcgplayer | cardkingdom
escalation:
  on_loop_exhaustion: warn  # warn | block | best-effort
```

Missing file = all defaults. Invalid keys = warned, ignored. Parse failure = warned, all defaults. Pipeline NEVER fails from config. Loaded after intake, before banner.

## 5. Challenger Agent Design

**Deck Challenger**: re-counts cards (must be 100), spot-checks 5 random synergy claims against oracle text, checks structural minimums, flags obvious omissions.

**Rules Challenger**: runs `validate-deck` independently (DEFECT-001 fix), parses violations array for color_identity/format_legality/banned, cross-checks 3 random color identities via individual Scryfall lookups.

**Optimization Challenger**: recalculates synergy score independently, identifies isolated cards (< 3 interactions, < 2 for BUDGET_RELAXED), validates mana curve against actual CMC distribution.

**Price Challenger**: fetches CK prices independently via `ck-batch-price`, flags per-card divergence > 30% and total divergence > 20% (DEFECT-002 fix), checks per-card goal violations, attempts substitution before escalation.

## 6. Sub-Agent Dispatch Guardrail (FR-9)

New SKILL.md section: `## Sub-Agent Dispatch Guardrail`. Lists all 8 Agent dispatches (4 primary + 4 challenger). Inlining ANY step = GUARDRAIL VIOLATION. Includes session 0876a59e anti-pattern callout. Task blocks use spawned-agent language ("your output", "write to disk", "{deck_state}" as input param) that produces nonsensical instructions if inlined.

## 7. Price Goal Escalation Flow (FR-4)

1. Price Evaluator prices all cards (TCG + CK)
2. Over-goal cards identified if `max_card_price` is non-null
3. Substitution attempted per card (synergy-preserving, legal, under goal)
4. Unsubstitutable cards grouped into BLOCKING escalation prompt (Galadriel's table format, options a/b/c)
5. Pipeline halts -- no timeout, no auto-accept
6. User response logged in PRICE_EXCEPTIONS section
7. If `escalation: false`: auto-substitute via budget-wins; no sub = include silently with note

Separate from existing 15%-of-budget hard cap (unchanged).

## 8. File Changes

| File | Action | Summary |
|------|--------|---------|
| `mtg-commander/SKILL.md` | UPDATE | Adversarial loop protocol, Sub-Agent Guardrail (FR-9), config loading, 4 challenger templates, price escalation, 8-step banner |
| `references/price-evaluator-guide.md` | UPDATE | Per-card goal (2.5), CK divergence (2.6), escalation format |
| `references/rules-judge-guide.md` | UPDATE | Mandate validate-deck as SOLE mechanism (DEFECT-001) |
| `references/config-reference.md` | NEW | Full schema docs, defaults, valid values, version field |

## 9. Non-Goals

No new agents beyond 4 challengers. No new APIs. No partner commanders. No delivery-flow integration. No core prompt rewrites.
