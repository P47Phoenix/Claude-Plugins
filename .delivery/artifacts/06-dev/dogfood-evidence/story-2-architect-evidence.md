---
story: Story 2 (W2-2 + W2-6)
implementer: Gimli (developer)
date: 2026-05-03
---

# Dogfood Evidence: Story 2 — Architect Output Contracts Split + Model Split

## Pre-Flight

- `wc -l delivery-team/skills/architect/SKILL.md` → **673** (baseline recorded)
- `grep -n "^### Output\|## Output Contract"` → Contracts at lines 388–540 (5 blocks, ~153 lines)

## Task A: W2-2 Output Contracts Split

### Contract Files Created

```
delivery-team/skills/architect/references/output-contracts/
├── design.md      (design, decompose, model, analyze-quality, data-design, security-design, strategic, integration, transformation-planning)
├── adr.md         (document, game-design-doc)
├── game.md        (game-systems, level-design, netcode, render-pipeline)
├── review.md      (review, game-review)
└── evaluation.md  (evaluate)
```

### Verification

```
find .../output-contracts -name '*.md' | wc -l → 5  ✓
```

### SKILL.md Routing Table

5-row table at line ~400 maps every task_type to its contract file. Sub-agent prompt loads only the matched contract.

## Task B: W2-6 Model Split

### Changes Made

1. Phase 1 declaration line updated: `Role | Task | Model | References`
2. Model Split table added (Classification → sonnet, Synthesis → opus, Checklist/Policy → sonnet)
3. Sub-Agent Output Contract JSON: added `"recommended_model": "sonnet | opus"` field
4. `paradigms/ddd/SKILL.md` frontmatter: added `model: sonnet`
5. `paradigms/volatility/SKILL.md` frontmatter: added `model: sonnet`

### Verification

```
grep "^model:" paradigms/ddd/SKILL.md paradigms/volatility/SKILL.md
→ model: sonnet  ✓ (both files)

grep "recommended_model" SKILL.md
→ 4 hits (declaration, Model Split table header, table content, Output Contract JSON)  ✓
```

## Post-Flight

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Contract file count | 5 | 5 | PASS |
| SKILL.md line count | ≤500 | 500 | PASS (Tier-A met) |
| Routing table present | yes | yes | PASS |
| DDD paradigm model frontmatter | sonnet | sonnet | PASS |
| Volatility paradigm model frontmatter | sonnet | sonnet | PASS |
| recommended_model in output contract JSON | yes | yes | PASS |

## Line Reduction Summary

| Stage | Lines |
|-------|-------|
| Baseline | 673 |
| After contracts removal | ~520 |
| After model split addition (+18) | ~538 |
| After targeted trimming (Prior Art, Paradigm tree, Domain Discovery, Principle) | 500 |
| Net reduction | **173 lines (−26%)** |

## Tier Compliance

- Tier-A ≤500: **MET** (exactly 500)
- Tier-B ≤300: deferred to Wave 3 (BACKLOG-104) per ADR-tk2-002
