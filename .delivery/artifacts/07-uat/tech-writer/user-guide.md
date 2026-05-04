---
title: "delivery-team Contributor Guide — Skill Token-Economy"
stage: 07-uat
author: Bilbo (operations skill, tech-writer role)
created: 2026-05-03
---

# Contributor Guide: Skill Token-Economy (Wave 0 Baseline)

## 1. What Does `tier: A|B|C` Mean?

The `tier:` field in every delivery-team SKILL.md frontmatter sets the **line budget**:

| Tier | Budget | Used for |
|------|--------|----------|
| A    | 500    | Orchestrators (`delivery-flow`) |
| B    | 300    | Multi-role / multi-domain skills |
| C    | 200    | Single-role or single-domain skills |

Full rationale: **ADR-tk0e-003** — `.delivery/artifacts/04-architect/adrs/ADR-tk0e-003-tier-default-mapping.md`

## 2. Declaring a Budget Exception

Add this line anywhere in the PR body to bypass the CI gate for legitimate over-budget work:

```
Budget-Exception: known-debt-tk0e
```

Pair each exception with a BACKLOG item tracking the planned extraction pass.

## 3. Reading the Telemetry JSONL

File: `.delivery/telemetry/skill-loads.jsonl` (one JSON object per line).
Full schema: `delivery-team/references/telemetry-schema.md` (ADR-tk0e-001: `.delivery/artifacts/04-architect/adrs/ADR-tk0e-001-telemetry-jsonl-schema.md`).

Key fields: `version` (`"1"`), `ts` (ISO-8601 UTC), `skill`, `session_id`,
`prefix_hash` (8-char sha256 hex of SKILL.md first 2 KB), `model` (null Wave 0),
`input_tokens` / `cache_read_tokens` / `cache_write_tokens` (0 in Wave 0; Wave 1 backfills).

```bash
python3 delivery-team/hooks/telemetry_report.py [--last N]   # tabular view
```

## 4. Adding a New SKILL.md — Checklist

1. Pick a tier (§1). Single-role → C; multi-role → B; orchestrator → A.
2. Add `tier: <A|B|C>` to the YAML frontmatter block.
3. Add an entry to `governance/skill-budgets.json` (`skill`, `tier`, `path`).
   If already over-budget at creation, add to `KNOWN_DEBT` with `wave` + `reason`.
4. Verify locally: `python3 scripts/check_skill_budgets.py`
5. If over-budget at PR time, use Budget-Exception token (§2) + open a BACKLOG item.

See `plugin-dev:skill-development` for full SKILL.md authoring conventions.
