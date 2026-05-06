---
id: ADR-tk2-002
title: "Architect output contracts split + model split (W2-2, W2-6)"
status: Accepted
work_items: [W2-2, W2-6]
wave: 2
author: Architect (delivery-team:architect, Celebrimbor persona)
created: 2026-05-05
---

# ADR-tk2-002: Architect Output Contracts Split + Model Split

## Context

`architect/SKILL.md` stands at **673 lines** post-Wave-1; Tier-B ≤300 is the eventual
target. Wave 2 can only reach ~498 (Tier-A ≤500 met; Tier-B deferred to BACKLOG-104 Wave 3).

- **W2-2:** 5 output contract blocks (~155 lines) are task-type-specific; only one needed
  per invocation. Canonical "output contracts behind task-type detection" pattern applies.
- **W2-6:** Classification phases (Prior Art, paradigm/decomp pick, Compliance/Privacy/IR)
  suit Sonnet. Design synthesis (ADR drafting, transformation TO-BE) requires Opus.
  Current skill router returns no model hint.

## Decision

### W2-2: Output Contracts Move

| Contract | Lines | Target |
|----------|-------|--------|
| Design Output | ~25 | `references/output-contracts/design.md` |
| ADR Output | ~28 | `references/output-contracts/adr.md` |
| Game Architecture Output | ~22 | `references/output-contracts/game.md` |
| Review Output | ~40 | `references/output-contracts/review.md` |
| Technology Evaluation Output | ~40 | `references/output-contracts/evaluation.md` |

SKILL.md retains a task_type → contract routing table (~8 lines). Phase 1 detects
task_type; Phase 2 loads only the matched contract.

### W2-6: Architect Model Split

Skill router MUST return `{role, task_type, recommended_model}`:

| Phase | recommended_model | task_types |
|-------|------------------|------------|
| Classification | `sonnet` | Prior Art Analysis, paradigm pick, decomposition pick, Compliance/Privacy/IR checklist |
| Synthesis | `opus` | ADR drafting, transformation TO-BE, Technology Evaluation |
| Review | `sonnet` | Architecture Review, Game Architecture Review |

Phase-to-model map documented inline in SKILL.md (~8 lines). `plugin-dev:skill-development`
MUST be pre-loaded for all changes (FR-12).

### Batching Math

```
architect/SKILL.md: 673 − 155 (W2-2) − 20 (W2-6) = 498  (Tier-A ≤500 ✓)
```
198-line Tier-B debt tracked in `skill-budgets.json` `target_wave: 3`.

## Consequences

**Positive:** architect/SKILL.md 673 → **~498** (Tier-A ✓); ~155-line cold-load
reduction per invocation; model split yields ≥3× cost reduction on classification turns;
`recommended_model` plumbing reusable by orchestrator.

**Negative:** 198-line Tier-B debt to Wave 3; 5 new files in `references/`;
Review vs Synthesis boundary is a judgment call — mitigated by 10-input regression set.

## Alternatives Considered

**1. Full Tier-B compliance Wave 2 (rejected):** Exceeds 5-story ceiling; paradigm
sub-skill restructuring (BACKLOG-005) carries independent risk. BACKLOG-104 owns it.

**2. Model split as config option (rejected):** Adds config surface area; removes
principled classification. Skill router returning `recommended_model` is cleaner;
orchestrator can still override via config if needed.
