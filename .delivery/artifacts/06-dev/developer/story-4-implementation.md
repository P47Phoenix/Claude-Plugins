---
story: 4
title: product-delivery 12 patterns split (W2-5)
status: DONE
date: 2026-05-03
author: Gimli
lines_before: 691
lines_after: 299
tier_b_target: 300
surplus_trimmed: yes
wave_3_debt: none
---

# Story 4 Implementation: product-delivery 12 Patterns Split

## What Was Done

Extracted all 12 `### Pattern N:` blocks from product-delivery/SKILL.md into individual
files under `references/patterns/`. Replaced the inline blocks with a 12-row routing table
mapping task_type to pattern file. Trimmed surplus to reach 299 lines (Tier-B ≤300).

## Files Modified

- `delivery-team/skills/product-delivery/SKILL.md` — 691 → 299 lines

## Files Created (12 pattern files)

```
delivery-team/skills/product-delivery/references/patterns/
├── ab-test.md        (Pattern 12: A/B Test Plan)
├── backlog.md        (Pattern 3: Backlog Prioritization)
├── dod-dor.md        (Pattern 8: Definition of Done / Ready)
├── epic.md           (Pattern 2: Epic Decomposition)
├── metrics.md        (Pattern 11: Metrics Definition)
├── prd.md            (Pattern 4: PRD)
├── retro.md          (Pattern 9: Retrospective)
├── roadmap.md        (Pattern 6: Roadmap Item)
├── sprint.md         (Pattern 5: Sprint Planning)
├── stakeholder.md    (Pattern 7: Stakeholder Communication)
├── story.md          (Pattern 1: User Story)
└── velocity.md       (Pattern 10: Velocity/Metrics Analysis)
```

## Routing Table (in SKILL.md ## Output Patterns)

Phase 2 now loads ONLY the matched file per task_type. Cold-load savings: ~372 lines/invocation.

## Trimming Applied to Hit ≤300

1. Sub-agent prompt template condensed (context list → single line, output requirements → 2 lines)
2. Cross-role tasks intro sentence removed (1 line)
3. References section: 21 bullet lines → 4-row table
4. Sub-agent interface intro sentence removed (1 line)
5. downstream_ready description tightened (1 line)

## Dogfood Evidence

`.delivery/artifacts/06-dev/dogfood-evidence/story-4-product-delivery-evidence.md`
