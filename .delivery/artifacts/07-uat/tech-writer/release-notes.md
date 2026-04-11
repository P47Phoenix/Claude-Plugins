# Release Notes — mtg-commander v2.18.0

**Author**: Bilbo (Tech Writer)
**Date**: 2026-04-11

## What's New

### Adversarial Challenger Agents
Every pipeline step now spawns dedicated Challenger agents that independently verify
the primary agent's output. Four challengers operate across the pipeline:

- **Deck Challenger** — validates synergy density and card selection rationale
- **Rules Challenger** — cross-checks format legality using deterministic validation
- **Optimization Challenger** — stress-tests mana curve, land count, and draw consistency
- **Price Challenger** — independently fetches Card Kingdom pricing for divergence checks

### Configurable Adversarial Loops
New optional `.mtg-commander.yml` in your project root controls loop iterations per step
(default: 2, max: 5). No config file needed — defaults apply automatically.

### Soft Per-Card Price Goal
New `max_card_price` config key sets a soft ceiling per individual card. Violations trigger
an escalation prompt to the user (blocking — no auto-accept). Hard 15%-of-budget cap unchanged.

### Sub-Agent Dispatch Guardrail
Structural enforcement that every pipeline step (primary + challenger) runs as a spawned
sub-agent. Inlining is explicitly flagged as a guardrail violation in SKILL.md language.

## Bug Fixes

### DEFECT-001: Color Identity Validation (Critical)
Rules Judge + Rules Challenger now mandate `validate-deck` programmatic command for color
identity checks. Zero reliance on LLM card knowledge for legality decisions.

### DEFECT-002: Card Kingdom Price Divergence (Major)
Price Challenger independently fetches CK prices. Divergence >30% per card or >20% total
triggers escalation to user. Multi-vendor awareness without requiring CK as primary source.

## Backwards Compatibility

- No config file required (absence = defaults)
- Existing pipeline behavior preserved for users who don't create `.mtg-commander.yml`
- No new external APIs (still Scryfall + Archidekt only)

## Known Limitations

- Challengers are prompt-enforced via SKILL.md language, not code-enforced runtime checks
- Effectiveness relies on the structural language strength of task blocks
- SKILL.md now 1179 lines — future decomposition may be warranted

## Credits

Built by the Fellowship: Gandalf (PO), Aragorn (Architect), Legolas (QA),
Sam (DevOps), Bilbo (Tech Writer), Gimli (Developer).
