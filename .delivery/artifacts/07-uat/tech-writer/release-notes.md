---
title: "Wave 2 Release Notes — Doctrine Extraction + Per-Skill Contracts"
stage: 07-uat
author: Bilbo (operations skill, tech-writer role)
created: 2026-05-03
initiative: SKILL-TOKEN-ECONOMY
wave: 2
supersedes: Wave 1 release notes (2026-05-03)
---

# Release Notes — Wave 2: Doctrine Extraction + Per-Skill Model Map + Pattern Split

## What's New

### delivery-flow/SKILL.md — 999 → 497 lines (Tier-A ✓)
- **Doctrine externalized** to `delivery-team/references/shared/orchestrator-doctrine.md`
  (Prime Directive elaboration, Anti-Patterns, collaboration pattern prose — 502 lines removed).
- **Cache prefix re-frozen**: `governance/cache-prefix-hash.txt` updated to sha256 `9d4011d1…`
  following doctrine extraction. Any PR touching delivery-flow/SKILL.md first ~2 KB must
  re-freeze and cite an ADR.

### architect/SKILL.md — 673 → 500 lines (Tier-A ✓; partial Tier-B progress)
- **5 output contracts extracted** to `references/output-contracts/<task_type>.md`:
  greenfield-design, brownfield-migration, spike, design-sprint, transformation-planning.
- **Model split applied**:
  - Classification phases → `recommended_model: sonnet`
  - Design synthesis phases → `recommended_model: opus`
- ~200-line Tier-B residual remains; closure deferred to Wave 3 (BACKLOG-104).

### developer/SKILL.md — 495 → 296 lines (Tier-B ✓)
- Coding standards extracted to `references/agent-prompts/coding-standards.md`.
- Language-agnostic template at `references/coding-standards-template.md`.
- Paradigm-aware loading paths preserved in skill body.

### product-delivery/SKILL.md — 691 → 299 lines (Tier-B ✓)
- 12 task-type-specific patterns split to `references/patterns/<slug>.md`.
- Skill body retains routing index; pattern files load on demand per task type.

### Wave 1 Retro Backports (BACKLOG-101 W1-7)
- Severity corrected: `-1 → -2` per retro finding.
- Hook file renamed to `audit_agent_prompt.py` (previously undiscoverable under old name).
- Edit-history footers appended to all affected files (history-preserving; no content lost).

## Why

Realizes the doctrine extraction + per-skill model map + per-task pattern split from
the audit. Closes 3 of 10 known-debt files (delivery-flow, developer, product-delivery
reach Tier-A/B). Wave 1 retro obligations cleared.

## Breaking Changes

None. All changes are extractive; routing tables and DoD validators preserved.
Cache-prefix hash invalidated once — operators must re-verify (see below).

## Known Issues / Debt

| File | Remaining Issue | Wave |
|------|----------------|------|
| `architect/SKILL.md` | Tier-B ~200-line residual | Wave 3 |
| `CLAUDE.md` | 169 lines, binding-deferred | Wave 3 |
| `presentation/SKILL.md` | Tier-B/C | Wave 3 |
| `ui/SKILL.md` | Tier-B/C | Wave 3 |
| `operations/SKILL.md` | Tier-B/C | Wave 3 |
| `quality/SKILL.md` | Tier-B/C | Wave 3 |
| `user-feedback/SKILL.md` | Tier-B/C | Wave 3 |
| `godot/SKILL.md` | Tier-B/C | Wave 3 |

Known-debt baseline: 10 → 7 entries after Wave 2.

## What's Next

- **BACKLOG-104 Wave 3**: presentation / ui / operations / quality / user-feedback / godot
  trims; architect Tier-B closure; governance frontmatter; paradigm sub-skill pattern;
  CLAUDE.md refactor (169 → ≤150).
- **BACKLOG-102**: caveman-lite prose discipline — still queued, no change this wave.

## Operator Instructions

```bash
# Tier compliance report (now shows 7 known-debt entries)
python3 scripts/check_skill_budgets.py --known-debt-report

# Verify cache-prefix integrity
python3 -c "
import hashlib
h = hashlib.sha256(open('delivery-team/skills/delivery-flow/SKILL.md','rb').read()[:2048]).hexdigest()
stored = open('governance/cache-prefix-hash.txt').read().split()[0]
print('OK' if h == stored else f'MISMATCH: got {h}, want {stored}')
"

# Telemetry summary
python3 delivery-team/hooks/telemetry_report.py
```

## Credits

Gandalf (PO) · Celebrimbor (Architect) · Aragorn (SM) · Legolas (QA) · Gimli (Dev) · Sam (DevOps) · Bilbo (TW)
