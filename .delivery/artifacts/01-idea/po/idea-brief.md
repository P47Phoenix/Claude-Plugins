# Idea Brief: MTG Commander Adversarial Review + Price Rule Enhancements

**Pipeline:** run-2026-04-11-e6f3 | **Type:** FEATURE | **Plugin:** mtg-commander

---

## The Burden

The MTG Commander pipeline runs four agents sequentially -- Deck Builder, Rules Judge, Optimizer, Price Evaluator -- but each agent is a lone voice in the wilderness. The Rules Judge checks legality and nobody second-guesses the Rules Judge. The Optimizer evaluates synergy and nobody challenges its card choices. The Price Evaluator enforces budget with a hard per-card cap and no negotiation when budget-optimal cards exceed it.

This architecture produced DEFECT-001: the Rules Judge missed a color identity violation (Sejiri Refuge in an Orzhov deck) because it trusted LLM knowledge instead of deterministic validation. And DEFECT-002: TCGPlayer-only pricing diverged 50%+ from Card Kingdom, blindsiding users who buy from CK.

The pipeline produces good decks. But it has no self-skepticism. No challenger. No second opinion at any step.

## The Vision

Each pipeline step gets an independent **Challenger agent** that reviews the primary agent's output from a skeptical, adversarial perspective before the pipeline advances. Challenger-primary loops are configurable per step via a user-repo config file (`.mtg-commander.yml`), not baked into the plugin. Enhanced price rules add a "no card over $X" soft goal with user escalation when the goal cannot be met. DEFECT-001 and DEFECT-002 fixes fold into the Challenger architecture naturally.

## Scope IN

- Per-step adversarial Challenger agent (4 challengers, one per pipeline step)
- User-repo config file `.mtg-commander.yml` with loop counts, escalation rules, price rules
- Enhanced price rules: soft per-card price goal + user escalation
- DEFECT-001 fix: Rules Judge Challenger mandates `validate-deck` for color identity
- DEFECT-002 fix: Price Evaluator Challenger fetches CK prices independently, escalates on divergence > 30%

## Scope OUT

- New card evaluation engines or APIs beyond Scryfall + Archidekt
- Partner commander support
- New archetypes or archetype detection changes
- UI/UX changes to output format (beyond escalation prompts)
- Delivery-flow pipeline integration (mtg-commander remains standalone)

## The Stakes

- DEFECT-001 closed: zero color identity misses (deterministic validation by Challenger)
- DEFECT-002 addressed: CK pricing divergence triggers escalation with both vendor prices
- Per-step adversarial catches errors the primary agent misses before they cascade
- Users control loop depth and escalation behavior via their own config file

## Anti-Scope

- Do NOT rewrite the 4 core agents -- augment with Challengers, do not replace
- Do NOT add new external APIs beyond Scryfall and Archidekt
- Do NOT change the intake flow or output format structure
