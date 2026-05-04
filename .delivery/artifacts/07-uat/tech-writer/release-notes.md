---
title: "Wave 0 Release Notes — Skill Token-Economy (tk0e)"
stage: 07-uat
author: Bilbo (operations skill, tech-writer role)
created: 2026-05-03
initiative: SKILL-TOKEN-ECONOMY
wave: 0
---

# Release Notes — Wave 0: Skill Token-Economy Foundation

## What's New

### Telemetry Hook (`W0-1`)
A new `PreToolUse (Skill)` hook in `delivery-team/hooks/telemetry.py` silently records
every skill load to `.delivery/telemetry/skill-loads.jsonl`. Each JSONL row captures:
`version`, `ts`, `skill`, `session_id`, `prefix_hash`, `model` (null in Wave 0),
and three token fields (zero-valued in Wave 0; Wave 1 backfills via PostToolUse).

Overhead measured at **18.7 ms mean** (target < 50 ms). Hook always exits 0.
Schema documented in `delivery-team/references/telemetry-schema.md` (ADR-tk0e-001: `.delivery/artifacts/04-architect/adrs/ADR-tk0e-001-telemetry-jsonl-schema.md`).

### CI Line-Budget Gate (`W0-2`)
`skill-line-budget.yml` is a new GitHub Actions workflow (PR trigger, paths-filtered
to `*/SKILL.md`) that runs `scripts/check_skill_budgets.py` against `governance/skill-budgets.json`.
Fails PRs whose SKILL.md exceeds its tier budget unless a `Budget-Exception: <token>` line
appears in the PR body. Known-debt baseline: **11 entries** (ADR-tk0e-003: `.delivery/artifacts/04-architect/adrs/ADR-tk0e-003-tier-default-mapping.md`).

### Tier Frontmatter on 13 SKILL.md Files
All 13 delivery-team SKILL.md files now carry a `tier:` field in their YAML frontmatter:
- **Tier A** (1): `delivery-flow` (orchestrator; budget 500 lines — exempt/known-debt)
- **Tier B** (8): `product-delivery`, `architect`, `developer`, `presentation`, `ui`,
  `operations`, `quality`, `user-feedback`
- **Tier C** (4): `godot`, `alias-creator`, `paradigms/ddd`, `paradigms/volatility`

No SKILL.md *content* was modified; only the frontmatter `tier:` line was added (+1 each).

## Why

Wave 0 establishes the measurement and regression-prevention baseline for the
Skill Token-Economy initiative. Without telemetry we cannot measure; without the CI gate
we cannot prevent regressions. Waves 1+ will use both to safely reduce context load.

## Breaking Changes

None. The telemetry hook is invisible to users and exits 0 on any error.
The CI gate respects the known-debt list; existing over-budget files do not break PRs.

## Known Issues / Debt

- **alias-creator at 201 lines** (Tier C budget = 200): Wave 1 will trim 1 line to restore
  compliance (see `governance/skill-budgets.json` known-debt entry).
- **Token counts always 0 in Wave 0**: Wave 1 adds a PostToolUse enrichment hook.
- **`model` field always null**: `CLAUDE_MODEL` env not set at hook time; Wave 1 to explore.
- **No log rotation**: deferred to Wave 3 (ADR-tk0e-001: `.delivery/artifacts/04-architect/adrs/ADR-tk0e-001-telemetry-jsonl-schema.md`).
- **CLAUDE.md over 150-line cap**: Currently at 169 lines (cap = 150 per binding ruling 3).
  The Wave 0 CLAUDE.md hook/CI additions are **deferred** to Wave 3 when CLAUDE.md gets its
  refactor pass. See BACKLOG item: `tk0e-claude-md-refactor`.
- **TODO (Wave 1)**: Prune `marketplace.json` descriptions to ≤500 chars per binding ruling 2
  (BACKLOG-100). Not actioned this wave.

## What's Next (Wave 1)

Wave 1 begins the actual SKILL.md extractions to reduce context load:
- Extract `delivery-flow` stage prose → `references/stage-*.yml` YAML
- Extract `architect` output contracts → `references/` markdown files
- Backfill token counts via PostToolUse hook
- Reduce `alias-creator` by 1 line (restore Tier C compliance)
- Reduce `godot` by ~35 lines
- Update KNOWN_DEBT counts after reductions

## Operator Instructions

```bash
# View telemetry log (last N rows)
python3 delivery-team/hooks/telemetry_report.py [--last N]

# Run budget check locally (all SKILL.md files)
python3 scripts/check_skill_budgets.py

# Budget check — known-debt report only
python3 scripts/check_skill_budgets.py --known-debt-report

# Bypass CI gate for legitimate over-budget PRs:
# Add this line to the PR body:
#   Budget-Exception: known-debt-tk0e
```

## Credits

Wave 0 delivered by the Fellowship:
- **Gandalf** (PO) — backlog, ADRs, sprint planning
- **Celebrimbor** (Architect) — telemetry schema, tier ADR, CI design
- **Aragorn** (SM) — sprint coordination
- **Legolas** (QA) — acceptance criteria, dogfood evidence
- **Gimli** (Dev) — `telemetry.py`, `check_skill_budgets.py`, frontmatter rollout
- **Sam** (DevOps) — CI workflow, `skill-line-budget.yml`
- **Bilbo** (TW) — release notes, user guide, CLAUDE.md updates
