---
title: "Wave 2 UAT Test Plan"
stage: 07-uat
author: Legolas (quality skill)
created: 2026-05-03
version: 2.0
stories: [story-1-delivery-flow-w2, story-2-architect-output-contracts, story-3-developer-coding-standards, story-4-product-delivery-patterns, story-5-admin-rebaseline]
---

# Wave 2 UAT Test Plan

## Scope

Contributor-perspective acceptance of 5 Wave 2 stories:
- Story 1 — delivery-flow/SKILL.md trim to 497 lines (Tier-A)
- Story 2 — architect output-contracts split + model split
- Story 3 — developer coding-standards extraction to agent-prompts
- Story 4 — product-delivery 12-pattern split
- Story 5 — governance re-baseline (skill-budgets.json, Wave 1 retro backports)

Stage 6 dogfood covers unit/integration. UAT answers: **"would a contributor pick this up cleanly?"**

## Pre-conditions

- All 5 story branches merged to main; clean git tree.
- Files exist:
  - `delivery-team/skills/delivery-flow/SKILL.md` (497 lines)
  - `delivery-team/skills/architect/references/output-contracts/` (5 files)
  - `delivery-team/skills/developer/references/agent-prompts/coding-standards.md`
  - `delivery-team/skills/product-delivery/references/patterns/` (12 files)
  - `governance/skill-budgets.json` (7 known_debt entries)
  - `governance/cache-prefix-hash.txt`
- Python 3.8+ stdlib-only environment available.
- `scripts/check_skill_budgets.py` present and runnable.

## Acceptance Scenarios

### Scenario 1 — delivery-flow Tier-A compliance + doctrine reference
**Question**: Is delivery-flow/SKILL.md at 497 lines and doctrine pointer intact?

- Verify `wc -l` == 497 (Tier-A ≤ 500).
- Verify at least one reference to `orchestrator-doctrine.md` in the file.
- Verify `## Volatile` marker present exactly once.
- **Pass**: all 3 checks pass.

### Scenario 2 — architect routes to output-contracts per task type
**Question**: Does architect/SKILL.md carry a complete routing table pointing to all 5 contract files?

- Verify `references/output-contracts/` contains exactly 5 `.md` files: `design.md`, `adr.md`, `game.md`, `review.md`, `evaluation.md`.
- Verify SKILL.md routing table maps each of the 5 contracts (grep for each filename in SKILL.md).
- Verify architect/SKILL.md line count ≤ 500 (partial-compliance Tier-A ceiling).
- **Pass**: 5 files present; all 5 referenced in routing table; line count ≤ 500.

### Scenario 3 — developer routes coding-standards to agent-prompts; 6 other tasks unaffected
**Question**: Is coding-standards dispatch isolated without disturbing other task routing?

- Verify `references/agent-prompts/coding-standards.md` exists.
- Verify developer/SKILL.md references `references/agent-prompts/coding-standards.md`.
- Verify developer/SKILL.md line count ≤ 300 (Tier-B target after extraction).
- Verify SKILL.md still routes `write`, `fix`, `refactor`, `review`, `test`, `explain` tasks (6 non-coding-standards types present).
- **Pass**: file present; routing pointer in SKILL.md; line count ≤ 300; 6 other task types intact.

### Scenario 4 — product-delivery routes to patterns/<slug>.md per task_type
**Question**: Does product-delivery carry a full 12-row routing table pointing to individual pattern files?

- Verify `references/patterns/` contains exactly 12 `.md` files.
- Verify SKILL.md line count == 299 (Tier-B ≤ 300 compliant).
- Verify routing table present in SKILL.md (grep for "references/patterns/").
- **Pass**: 12 files present; line count 299; routing table confirmed.

### Scenario 5 — governance/skill-budgets.json shows 7 known_debt entries; CI gate passes
**Question**: Is the registry exactly 7 entries (architect + 6 Wave-3 targets) and gate clean?

- `python3 -c "import json; d=json.load(open('governance/skill-budgets.json')); print(len(d['known_debt']))"` → 7.
- Verify architect entry has `target_wave == 3`.
- Run `python3 scripts/check_skill_budgets.py` → exit 0.
- **Pass**: count == 7; architect wave 3; gate exits 0.

### Scenario 6 — cache-prefix-hash.txt matches sha256(bytes 0..2048) of current SKILL.md; old hash retired
**Question**: Does the frozen hash still match after the 497-line trim?

- Recompute `sha256(bytes 0..2048)` of `delivery-team/skills/delivery-flow/SKILL.md`.
- Compare to value stored in `governance/cache-prefix-hash.txt`.
- Verify hash file contains exactly one line (old pre-trim hash absent).
- **Pass**: live hash matches stored hash; file has one line.

## Pass Criteria

All 6 scenarios green. A scenario is green when every Verify bullet is satisfied
without manual workarounds.

## Out of Scope

- BACKLOG-102 (caveman refactor), Wave 3 trims.
- Other plugins (hardware-team, mtg-commander, etc.).
- End-to-end pipeline timing or throughput benchmarks.
- Paradigm sub-skill deep-routing (Wave 3 scope).
