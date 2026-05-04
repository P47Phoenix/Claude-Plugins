---
title: "W0-2 Budget Gate Dogfood Evidence"
story: W0-2
stage: 06-dev
author: Developer (Gimli)
created: 2026-05-03
---

# W0-2 Dogfood Evidence: SKILL.md Line-Budget CI Gate

## Evidence 1 — All 13 SKILL.md files have tier: frontmatter

```
find delivery-team -name 'SKILL.md' | wc -l  → 13
find delivery-team -name 'SKILL.md' -exec grep -L "^tier:" {} \;  → (empty — all pass)
grep "^tier:" delivery-team/skills/architect/paradigms/ddd/SKILL.md  → tier: C
grep "^tier:" delivery-team/skills/architect/paradigms/volatility/SKILL.md  → tier: C
```

RESULT: PASS

## Evidence 2 — Full check on current state (exit 0, all over-budget = known-debt)

```
python3 scripts/check_skill_budgets.py
# Output:
KNOWN-DEBT: delivery-team/skills/alias-creator/SKILL.md 201/200 lines — target wave: W1
KNOWN-DEBT: delivery-team/skills/architect/SKILL.md 671/300 lines — target wave: W1
KNOWN-DEBT: delivery-team/skills/delivery-flow/SKILL.md 1090/500 lines — target wave: W1
KNOWN-DEBT: delivery-team/skills/developer/SKILL.md 494/300 lines — target wave: W1
KNOWN-DEBT: delivery-team/skills/godot/SKILL.md 235/200 lines — target wave: W1
KNOWN-DEBT: delivery-team/skills/operations/SKILL.md 418/300 lines — target wave: W2
KNOWN-DEBT: delivery-team/skills/presentation/SKILL.md 544/300 lines — target wave: W2
KNOWN-DEBT: delivery-team/skills/product-delivery/SKILL.md 689/300 lines — target wave: W1
KNOWN-DEBT: delivery-team/skills/quality/SKILL.md 416/300 lines — target wave: W2
KNOWN-DEBT: delivery-team/skills/ui/SKILL.md 494/300 lines — target wave: W2
KNOWN-DEBT: delivery-team/skills/user-feedback/SKILL.md 398/300 lines — target wave: W2

BUDGET CHECK PASSED: 13 file(s) checked, 11 known-debt, 0 exception(s).
Exit: 0
```

RESULT: PASS (all 13 files check; 11 known-debt pass; 2 fully-compliant files pass)

## Evidence 3 — Known-debt report (11 entries, exit 0)

```
python3 scripts/check_skill_budgets.py --known-debt-report
# Output: 11 KNOWN-DEBT lines (delivery-flow 1089/500 ... alias-creator 201/200)
Exit: 0
```

RESULT: PASS (satisfies AC-10 floor of ≥6; full audit = 11 entries in KNOWN_DEBT)

## Evidence 4 — Permissive-language scan exits 0 (warn-only)

```
python3 scripts/check_skill_budgets.py --warn-permissive delivery-team/skills/delivery-flow/SKILL.md
# Output: 14 PERMISSIVE-LANGUAGE warnings to stderr
Exit: 0
```

RESULT: PASS (warn-only confirmed; exit never 1)

## Evidence 5 — Exempt zones: code block, blockquote, table NOT flagged

```
# File with: ```python ... should ... ```, > ... may ..., | can | skip |
python3 scripts/check_skill_budgets.py --warn-permissive /tmp/code_block.md
# No warnings emitted
Exit: 0
```

RESULT: PASS (all three exempt zones correctly excluded)

## Evidence 6 — Prose permissive language IS flagged (exit 0)

```
# File with: "You should check this." in prose
python3 scripts/check_skill_budgets.py --warn-permissive /tmp/prose_perm.md
# stderr: PERMISSIVE-LANGUAGE: /tmp/prose_perm.md:4: 'should' — You should check this.
Exit: 0
```

RESULT: PASS

## Evidence 7 — Synthetic over-budget file exits 1

```
python3 -c "open('/tmp/ob_c.md','w').write('---\ntier: C\n---\n'+'# x\n'*201)"
python3 scripts/check_skill_budgets.py --check /tmp/ob_c.md --tier C
# Output: BUDGET VIOLATION: /tmp/ob_c.md 204/200 lines (Tier-C)
Exit: 1
```

RESULT: PASS (exit 1, file named, overage shown)

## Evidence 7b — PR body exception token exits 0

```
PR_BODY="Budget-Exception: known-debt-tk0e" python3 scripts/check_skill_budgets.py --check /tmp/ob_b.md
# Output: EXCEPTION ACKNOWLEDGED: /tmp/ob_b.md — budget override active (304/300 lines Tier-B)
Exit: 0
```

RESULT: PASS

## Evidence 7c — Missing tier: field exits 1 with hint

```
python3 scripts/check_skill_budgets.py --check /tmp/no_tier.md
# Output: MISSING TIER: /tmp/no_tier.md — add `tier: A|B|C` to frontmatter
Exit: 1
```

RESULT: PASS

## Evidence 8 — Line delta exactly +1 for all 13 SKILL.md files

All 13 files confirmed OK +1 line vs ADR-tk0e-003 baseline.
No SKILL.md line counts were reduced. Additive-only, Wave 0 constraint satisfied.

## Workflow YAML structure check

```
grep -E 'name:|on:|pull_request:|paths:|jobs:|runs-on:|uses:|run:' .github/workflows/skill-line-budget.yml
# All required YAML keys present; paths filter on delivery-team/**/SKILL.md + governance/skill-budgets.json
```

RESULT: PASS

## Notable Finding

alias-creator was exactly at 200 lines (Tier-C limit) in the ADR-tk0e-003 audit baseline.
The Wave 0 tier-frontmatter rollout adds +1 line, pushing it to 201.
This is expected and unavoidable: tier classification REQUIRES the tier: field.
alias-creator is added to KNOWN_DEBT with target_wave=1. Wave 1 reduces it back to compliance.
