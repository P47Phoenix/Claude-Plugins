# US-6 — marketplace.json verification

**Tech Writer:** Bilbo
**Date:** 2026-04-14

## Registered plugins (6)
- agentic-flow-builder
- prompt-engineer
- prd-quality-gate-flow
- research-agent
- delivery-team
- mtg-commander

## Top-level directories (8)
agentic-flow-builder, delivery-team, docs, mtg-commander, prd-quality-gate-flow, prompt-engineer, research-agent, site

## Mismatches
- None. All registered plugins have matching directories.
- `docs/` and `site/` are documentation site scaffolding (non-plugin), correctly omitted from registry.

## Changes made
- **mtg-commander description:** updated to mention adversarial challenger agents (Deck Builder, Rules Judge, Optimizer, Price Evaluator), independent correction loop, `.mtg-commander.yml` config, and price goal escalation — reflects the b63ebc5 push.
- **delivery-team description:** added mention of shared `constraints.yml`, configurable Architecture Board, Transformation Planning sub-workflow (AS-IS/TO-BE/Roadmap) for brownfield migrations, and paradigm-as-skill router under architect.
- Version field left untouched per protocol (version bot owns bumps).
- Formatting preserved (2-space indent, trailing newline).

## JSON validation
`python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"` — **PASS** (6 plugins registered).
