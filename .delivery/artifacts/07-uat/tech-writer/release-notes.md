---
title: "Wave 1 Release Notes — Skill Token-Economy (tk1)"
stage: 07-uat
author: Bilbo (operations skill, tech-writer role)
created: 2026-05-03
initiative: SKILL-TOKEN-ECONOMY
wave: 1
supersedes: Wave 0 release notes (2026-05-03)
---

# Release Notes — Wave 1: Per-Skill Model Discipline + Cache-Prefix Freeze

## What's New

### delivery-flow/SKILL.md restructured (`W1-1`, `W1-2`)
1090 → 999 lines (−91). Three concrete changes:
- **Cache-prefix frozen** at end of Phase 3 (~first 2 KB). SHA-256 of bytes 0–2048 written
  to `governance/cache-prefix-hash.txt` (`aea33d57…`). Any PR touching the frozen region
  must update the hash and cite an ADR (`Cache-Prefix-Change:` PR token).
- **stages.yml extracted**: inline Stage 1–7 prose replaced with a single pointer block.
  Authoritative manifest: `delivery-team/skills/delivery-flow/references/stages.yml`
  (7,394 bytes, all 7 stages). JSON Schema: `references/stages-schema.json`.
- **Model defaults declared**: `model: sonnet` + `extended_thinking: false` added to
  delivery-flow frontmatter. Opus is opt-in per annotated site only.

### Per-skill `allowed-tools` + `phase_1_detector_model` (`W1-3`, `W1-4`)
- 12 SKILL.md files now carry `allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]`.
- 5 router skills (`product-delivery`, `architect`, `quality`, `operations`, `ui`) declare
  `phase_1_detector_model: haiku` — classification dispatch now runs on Haiku.

### Adversarial-challenger warn-only hook (`W1-5`)
`audit_agent_prompt.py` extended (+95 lines, additive only). New
`check_challenger_tier_inheritance()` emits `[CHALLENGER-TIER-WARN]` to stderr and
`$GITHUB_STEP_SUMMARY` when a challenger model differs from the primary. Called EARLY in
`main()`. Exit 0 always this wave. Promotion to hard-block in Wave 2 after 5-run clean run.

### alias-creator graduates from known-debt (`W1-7`)
Trimmed 201 → 200 lines; Tier-C compliant. Removed from `governance/skill-budgets.json`
known_debt list and from hardcoded `KNOWN_DEBT` in `check_skill_budgets.py`.
Known-debt baseline: 11 → 10 entries.

### marketplace.json description pruned (`W1-4`)
delivery-team entry: 913 → 464 chars (≤500 binding). Session-start payload reduced.

## Why

Realizes three binding decisions: prefix freeze (Ruling 1), stage YAML manifest (Ruling Corollary),
and per-skill model rollout (ADR-tk1-002/003). No breaking changes — all additive.

## Known Issues / Debt

- **CLAUDE.md at 168 lines** (cap = 150, binding ruling 3): Wave 1 additions deferred
  to Wave 3 refactor (which trims CLAUDE.md to ≤150 first). See `tk0e-claude-md-refactor`.
- **10 SKILL.md over Tier-A/B budgets**: Wave 2 structural extractions will address
  (architect, product-delivery, developer, presentation, ui, operations, quality, user-feedback,
  godot, delivery-flow are all still above their nominal long-term targets).
- **stages.yml not yet parsed at runtime**: orchestrator reads the pointer block as
  documentation only. Wave 2 wires programmatic loading.
- **YAML validation gap**: `stages.yml` content verified visually; `yamllint`/PyYAML
  CI validation deferred to Wave 2.
- **Challenger hard-block deferred**: warn-only this wave; escalates in Wave 2 after
  zero-violation telemetry across 5 runs.

## What's Next (Wave 2)

- BACKLOG-102: caveman-lite prose discipline (sequenced post-W1).
- Wave 2 structural extractions: output-contract tables out of architect, developer,
  quality, operations SKILL.md → `references/` markdown files.
- Pre-commit hook: enforce cache-prefix hash refresh on SKILL.md edits.
- Wire orchestrator to load stages.yml as structured data (Phase 4, Step 3).
- Challenger hard-block promotion (pending 5-run clean telemetry).

## Operator Instructions

```bash
# View tier compliance + known-debt report
python3 scripts/check_skill_budgets.py --known-debt-report

# Verify cache-prefix integrity (local)
python3 -c "
import hashlib
h = hashlib.sha256(open('delivery-team/skills/delivery-flow/SKILL.md','rb').read()[:2048]).hexdigest()
stored = open('governance/cache-prefix-hash.txt').read().split()[0]
print('OK' if h == stored else f'MISMATCH: got {h}, want {stored}')
"

# Run budget check
python3 scripts/check_skill_budgets.py
```

## Credits

Gandalf (PO) · Celebrimbor (Architect) · Aragorn (SM) · Legolas (QA) · Gimli (Dev) · Sam (DevOps) · Bilbo (TW)
