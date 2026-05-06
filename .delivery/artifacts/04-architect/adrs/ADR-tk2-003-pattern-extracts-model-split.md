---
id: ADR-tk2-003
title: "product-delivery 12-pattern split + developer coding-standards extract (W2-3, W2-5)"
status: Accepted
work_items: [W2-3, W2-5]
wave: 2
author: Architect (delivery-team:architect, Celebrimbor persona)
created: 2026-05-05
---

# ADR-tk2-003: Pattern Extracts — product-delivery (W2-5) + developer (W2-3)

## Context

Two role-multiplexer skills exceed Tier-B (≤300) with large per-task-type blocks:
- `product-delivery/SKILL.md`: **691 lines** — 12 Pattern blocks (~380 lines, lines ~140–511)
- `developer/SKILL.md`: **495 lines** — coding-standards block (~155 lines, lines ~162–318)

Both follow the canonical "output contracts behind task-type detection" binding pattern
(`topics/skill-token-economy.md`). W2-6 (architect model split) is in ADR-tk2-002.

## Decision

### W2-5: product-delivery 12 Patterns Split

Move each `### Pattern N:` block to `product-delivery/references/patterns/<slug>.md`
(12 files; stable slug names, no numeric-only prefix). SKILL.md retains a Phase 1
routing table (task_type → pattern file, ~14 lines). Phase 2 loads ONLY matched file.

**Batching Math:**
```
product-delivery/SKILL.md: 691 − 380 (W2-5) = 311 (+11 over Tier-B 300)
```
Stage 6 Dev MUST trim 11 lines (candidates: whitespace, duplicate headers, routing
commentary). If not achievable: known-debt in `governance/skill-budgets.json` → Wave 3.

### W2-3: developer coding-standards Extract

Move to two reference files:
- `developer/references/agent-prompts/coding-standards.md` (~100 lines, agent-prompt block)
- `developer/references/coding-standards-template.md` (~55 lines, per-language matrix)

SKILL.md retains a one-line dispatch pointer: `coding-standards → load both files`.

**Batching Math:**
```
developer/SKILL.md: 495 − 155 (W2-3) = 340 (+40 over Tier-B 300)
```
Stage 6 Dev MUST trim 40 lines (candidates: consolidate 14-language matrix to routing
table only; remove duplicate paradigm commentary). If ≥20 trimmed but ≤40: remainder
is known-debt → Wave 3.

### Dogfood Gates

- W2-5: 12/12 task-type routing log in PR body
- W2-3: `write` task (template NOT loaded) + `coding-standards` task (template IS loaded)

`plugin-dev:skill-development` MUST be pre-loaded for all SKILL.md and reference
file changes (FR-12).

## Consequences

**Positive:**
- product-delivery: 691 → **≤300** (Tier-B ✓ if +11 trimmed)
- developer: 495 → **≤300** (Tier-B ✓ if +40 trimmed)
- Per-invocation cold-load savings: ~32 lines (product-delivery), ~155 lines (developer)
- 14 new reference files with stable slugs support Wave 3 versioning

**Negative:**
- +11 / +40 surplus risk if Stage 6 trimming insufficient → known-debt
- Pattern slug renames break cached routing table pointers

## Alternatives Considered

**1. Single all-patterns.md per skill (rejected):** Phase 2 would still load all
12 patterns per invocation — eliminates the routing benefit entirely.

**2. Python build_agent_prompt.py (rejected):** Ruling 4 prefers markdown references
for v1; escaping risk + dependency overhead outweigh marginal savings. Revisit only
if telemetry confirms agent prompts dominate context post-extraction.
