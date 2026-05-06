---
story: Story 1 (W2-1 + W2-4)
wave: 2
executed: 2026-05-03
executor: Gimli (delivery-team:developer)
---

# Story 1 Doctrine Evidence — Dogfood Log

## Pre-Flight Measurements

| Check | Result |
|-------|--------|
| `wc -l delivery-flow/SKILL.md` | 999 lines (baseline confirmed) |
| `grep -c "^## Phase" SKILL.md` | 5 (all 5 phases present) |
| `grep -n "Common Orchestrator Anti-Patterns" SKILL.md` | line 628 |
| Old cache-prefix hash (Wave 1) | `aea33d5732e31ab6455dda3675f7ad536d5d0e440a52dd0c1802ec2dabf03db9` |

## Old Cache-Prefix Hash (Audit Record)

`aea33d5732e31ab6455dda3675f7ad536d5d0e440a52dd0c1802ec2dabf03db9`

This hash is now RETIRED per ADR-tk2-001 §D. Recorded here for audit trail.

## Per-Task Outcomes

### Task A — W2-1: Doctrine Extraction

**Target file**: `delivery-team/references/shared/orchestrator-doctrine.md` (new)

Content moved from SKILL.md to orchestrator-doctrine.md:
- Design Principle prose elaboration (paragraphs + write-path enumeration)
- Core Principles 1–7 full text (~47 lines)
- Model awareness F-08 intro note (~7 lines)
- Common Orchestrator Anti-Patterns 8 enumerated items (~53 lines)
- Team DoD Protocol full prose (~37 lines)
- Dynamic Escalation Protocol triggers table + format template (~46 lines)
- Cross-Stage Artifact Flow narrative prose (~8 lines)
- Memory and Self-Learning detail blocks (~63 lines)
- Guardrails enumerated detail (~43 lines)
- Theme-Gated Reporting Protocol 4-paragraph detail (~30 lines)

**Lines extracted (doctrine)**: ~393 lines → orchestrator-doctrine.md (406 lines total with headers)
**Line delta W2-1 portion**: −393 from SKILL.md body

### Task B — W2-4: Config/Commands/Manifest Tables

| New File | Lines | Content |
|----------|-------|---------|
| `references/config-keys.md` | 43 | 35-row config settings table |
| `references/commands.md` | 29 | 18-row user commands table |
| `references/manifest.yml` | 107 | 22-entry references manifest (YAML) |

Replaced in SKILL.md with 1-line pointer each. Table removal from SKILL.md: ~109 lines.

### Task C — Cache-Prefix Re-Freeze

- Old hash: `aea33d5732e31ab6455dda3675f7ad536d5d0e440a52dd0c1802ec2dabf03db9`
- New hash: `9d4011d11e5b83321526c41ff79dd25c9186f4c659a745feb0c13f686205926f`
- Written to: `governance/cache-prefix-hash.txt`
- Format: `<sha256-hex>  delivery-team/skills/delivery-flow/SKILL.md`

## Post-Flight Verification

| Check | Command | Result | Pass? |
|-------|---------|--------|-------|
| SKILL.md ≤500 lines | `wc -l SKILL.md` | 497 | PASS |
| orchestrator-doctrine.md >0 lines | `wc -l orchestrator-doctrine.md` | 406 | PASS |
| config-keys.md >0 lines | `wc -l config-keys.md` | 43 | PASS |
| Phase 0 heading present | `grep -c "^## Phase 0" SKILL.md` | 1 | PASS |
| Phase 1 heading present | `grep -c "^## Phase 1" SKILL.md` | 1 | PASS |
| Phase 2 heading present | `grep -c "^## Phase 2" SKILL.md` | 1 | PASS |
| Phase 3 heading present | `grep -c "^## Phase 3" SKILL.md` | 1 | PASS |
| Phase 4 heading present | `grep -c "^## Phase 4" SKILL.md` | 1 | PASS |
| One Role invariant present | `grep "One Role = One Sub-Agent"` | 2 matches | PASS |
| Two-Channel invariant present | `grep "Two-Channel"` | 1 match | PASS |
| Stage Routing Matrix present | `grep -c "## Stage Routing Matrix"` | 1 | PASS |
| Cache hash NOT Wave 1 | `cat governance/cache-prefix-hash.txt` | `9d4011d1...` ≠ `aea33d57...` | PASS |
| commands.md >0 lines | `wc -l commands.md` | 29 | PASS |
| manifest.yml >0 lines | `wc -l manifest.yml` | 107 | PASS |

## Recursive Dogfood Result

- `head -50 SKILL.md` — valid YAML frontmatter, then valid markdown heading hierarchy
- All 5 Phase headings confirmed at exactly 1 occurrence each
- `One Role = One Sub-Agent` invariant appears in heading AND model awareness callout
- `Two-Channel Communication` heading preserved in Phase 4
- Stage Routing Matrix table intact and complete (7 stages × 7 project types)
- Volatile section preserved at EOF

## New Cache-Prefix Hash (Governance)

`9d4011d11e5b83321526c41ff79dd25c9186f4c659a745feb0c13f686205926f`

Written to `governance/cache-prefix-hash.txt`. CI re-baseline required.

## Final Line Count

| File | Lines | Target | Status |
|------|-------|--------|--------|
| delivery-flow/SKILL.md | 497 | ≤500 | PASS (Tier-A ✓) |
| orchestrator-doctrine.md | 406 | >0 | PASS |
| config-keys.md | 43 | >0 | PASS |
| commands.md | 29 | >0 | PASS |
| manifest.yml | 107 | >0 | PASS |

**Net SKILL.md delta**: 999 → 497 = −502 lines
