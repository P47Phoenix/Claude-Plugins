---
title: "W0-2 QA Gate Review — SKILL.md Line Budget"
reviewer: Legolas (quality skill)
gate: Budget DoD validation
created: 2026-05-03
status: PASS
---

# W0-2 QA Gate Review

## Gate Criteria Validation

**✓ AC-1 thru AC-8: Story W0-2 acceptance criteria fully covered by TC-W0-2-1 through TC-W0-2-10**
- TC-W0-2-1: Over-budget failure (AC-9 happy path)
- TC-W0-2-2: Clean pass (AC-9 inverse)
- TC-W0-2-3: Budget-Exception token bypass (FR-10)
- TC-W0-2-4: Missing tier hint (FR-06)
- TC-W0-2-5 thru TC-W0-2-8: Exempt zones (code block, blockquote, table, prose)
- TC-W0-2-9: Known-debt report ≥6 entries (AC-10 floor; audit = 11)
- TC-W0-2-10: All 13 SKILL.md files carry tier frontmatter (AC-8)

**✓ Dogfood evidence complete**
- Evidence 1: 13 files confirmed; both paradigm sub-skills (ddd, volatility) carry `tier: C`
- Evidence 2: Full budget check: 13/13 processed; 11 known-debt + 2 compliant = exit 0
- Evidence 3: Known-debt report: 11 entries listed (exceeds AC-10 floor of ≥6)
- Evidence 4: Permissive scan warn-only confirmed (exit 0)
- Evidence 5: Exempt zones validated — code fence + blockquote + table NOT flagged
- Evidence 6: Prose permissive word IS flagged (exit 0)
- Evidence 7-7c: Over-budget (exit 1), exception token (exit 0), missing tier (exit 1) all verified
- Evidence 8: Line delta +1 per file (additive-only Wave 0 constraint met)

**✓ Exempt zones honored**
Created fixture with permissive language in fenced blocks, blockquotes, tables AND in plain prose.
Ran `--warn-permissive`; only prose hit flagged. Exit 0 (warn-only). All three exempt zones functional.

**✓ No untestable AC**
Every Story W0-2 AC has a verifiable command in test-strategy.md (Scenarios 1–8) with expected outputs.

**✓ Workflow trigger precision**
`paths:` filter: `delivery-team/**/SKILL.md` + `governance/skill-budgets.json`
Scope tight; no spurious triggers on unrelated files. Correct.

---

## Notable Findings

1. **Pre-existing gap in tier frontmatter**
   Eight of 13 SKILL.md files (developer, godot, architect, quality, operations, ui, product-delivery, delivery-flow) initially lacked the `tier:` field.
   All 13 now carry the frontmatter; no content modified. Wave 0 pure structural change, per ADR-tk0e-002.

2. **alias-creator knowns-debt entry**
   alias-creator was exactly 200 lines (Tier-C limit) in audit baseline.
   The `tier:` field addition pushed it to 201. Registered as known-debt with target_wave=1.
   This is unavoidable and expected; Wave 1 will restore compliance.

3. **Permissive language exempt zones fully functional**
   The three exempt zones (fenced code, blockquotes, tables) are correctly implemented in `scan_permissive_language()`.
   Fence-delimited content is skipped; regex-matched blockquotes (^\s*>) and table rows (^\s*\|) are exempted.
   Plain prose matches are flagged to stderr as advisory (never blocks merge).

---

## Gate Verdict

**PASS — W0-2 budget gate DoD satisfied.**

All 8 Story ACs covered by test cases, dogfood evidence complete, exempt zones verified, workflow trigger scoped correctly. The script and CI gate are production-ready.

