---
story: 2
wi: W1-3, W1-4, W1-7
date: 2026-05-03
---

# Story 2 Frontmatter Rollout — Dogfood Evidence

## Pre-Flight Line Counts (Baseline)

| File | Pre-Edit Lines |
|------|---------------|
| alias-creator/SKILL.md | 201 |
| architect/paradigms/ddd/SKILL.md | 84 |
| architect/paradigms/volatility/SKILL.md | 70 |
| architect/SKILL.md | 671 |
| developer/SKILL.md | 494 |
| godot/SKILL.md | 235 |
| operations/SKILL.md | 418 |
| presentation/SKILL.md | 544 |
| product-delivery/SKILL.md | 689 |
| quality/SKILL.md | 416 |
| ui/SKILL.md | 494 |
| user-feedback/SKILL.md | 398 |

## Post-Flight Line Counts (After All Edits)

| File | Post-Edit Lines | Delta | Expected Delta |
|------|----------------|-------|----------------|
| alias-creator/SKILL.md | 200 | -1 | +1 (allowed-tools) -2 (W1-7 trim) = -1 ✓ |
| architect/paradigms/ddd/SKILL.md | 85 | +1 | +1 (allowed-tools) ✓ |
| architect/paradigms/volatility/SKILL.md | 71 | +1 | +1 (allowed-tools) ✓ |
| architect/SKILL.md | 673 | +2 | +2 (phase_1_detector_model + allowed-tools) ✓ |
| developer/SKILL.md | 495 | +1 | +1 (allowed-tools) ✓ |
| godot/SKILL.md | 236 | +1 | +1 (allowed-tools) ✓ |
| operations/SKILL.md | 420 | +2 | +2 (phase_1_detector_model + allowed-tools) ✓ |
| presentation/SKILL.md | 545 | +1 | +1 (allowed-tools) ✓ |
| product-delivery/SKILL.md | 691 | +2 | +2 (phase_1_detector_model + allowed-tools) ✓ |
| quality/SKILL.md | 418 | +2 | +2 (phase_1_detector_model + allowed-tools) ✓ |
| ui/SKILL.md | 496 | +2 | +2 (phase_1_detector_model + allowed-tools) ✓ |
| user-feedback/SKILL.md | 399 | +1 | +1 (allowed-tools) ✓ |

## alias-creator Math Verification

- Start: 201 lines
- +1 (W1-4 allowed-tools): 202 lines
- -2 (W1-7 trim — removed redundant Note + blank line): 200 lines
- Result: 200 ✓ (Tier-C ≤200 compliant)

```
$ wc -l delivery-team/skills/alias-creator/SKILL.md
200
```

## Trim Details (W1-7)

Removed from alias-creator: 1 redundant blank line + the Note that restated table content.
The table row already read "Feedback facilitator (personas keep their own identities)".
The Note below it repeated identical information — zero substantive loss.

## marketplace.json Description Verification

```
$ python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); \
  pkg=[p for p in d['plugins'] if p['name']=='delivery-team'][0]; print(len(pkg['description']))"
464
```

Result: 464 chars ≤ 500 ✓

## Frontmatter Key Coverage

```
$ grep -l "^allowed-tools:" <all 12 SKILL.md> | wc -l
12
```
12/12 SKILL.md files contain `allowed-tools:` ✓

```
$ grep -l "^phase_1_detector_model: haiku" <5 router files> | wc -l
5
```
5/5 Phase 1 router SKILL.md files contain `phase_1_detector_model: haiku` ✓
Files: product-delivery, architect, quality, operations, ui

## CI Gate Dry-Run

```
$ python3 scripts/check_skill_budgets.py
BUDGET CHECK PASSED: 13 file(s) checked, 10 known-debt, 0 exception(s).
```

alias-creator no longer appears in known-debt list ✓
CI passes with no violations ✓

## Governance Registry Updates

- `governance/skill-budgets.json`: Removed alias-creator known-debt entry; updated godot current to 236
- `scripts/check_skill_budgets.py`: Removed alias-creator from hardcoded KNOWN_DEBT list
