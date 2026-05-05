---
title: "delivery-team Contributor Guide — Skill Token-Economy (Wave 1 additions)"
stage: 07-uat
author: Bilbo (operations skill, tech-writer role)
created: 2026-05-03
supersedes: Wave 0 user-guide (2026-05-03)
---

# Contributor Guide: Skill Token-Economy (Wave 0 + Wave 1)

## 1. Tier Budgets (unchanged)

| Tier | Budget | Used for |
|------|--------|----------|
| A    | 500    | Orchestrators (`delivery-flow`) |
| B    | 300    | Multi-role / multi-domain skills |
| C    | 200    | Single-role or single-domain skills |

## 2. Wave 1 Frontmatter Keys

```yaml
model: sonnet                  # or haiku for router agents
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
extended_thinking: false       # delivery-flow default; opt-in per annotated site
phase_1_detector_model: haiku  # router/dispatch skills only
```

Extensions to `allowed-tools` require an inline `# justification:` comment.

## 3. stages.yml — Authoritative Stage Manifest

`delivery-team/skills/delivery-flow/references/stages.yml` is the single source of truth.
SKILL.md carries only a pointer block. Edit `stages.yml`, not SKILL.md, for stage changes.
JSON Schema: `references/stages-schema.json` (CI-validated on every PR).

## 4. Cache-Prefix Freeze Contract

First ~2 KB of `delivery-flow/SKILL.md` (through end of Phase 3) is frozen.
Any PR touching that region must:
1. Regenerate `governance/cache-prefix-hash.txt` (SHA-256 of bytes 0–2048).
2. Reference an ADR in the commit message.
3. Add `Cache-Prefix-Change: <ADR-link>` to the PR body.

```bash
python3 -c "
import hashlib
h = hashlib.sha256(open('delivery-team/skills/delivery-flow/SKILL.md','rb').read()[:2048]).hexdigest()
open('governance/cache-prefix-hash.txt','w').write(h + '\n'); print(h)"
```

## 5. Adversarial Challenger Discipline

Challengers inherit the primary's model at dispatch. Never downgrade for cost savings.
Wave 1: `audit_agent_prompt.py` emits `[CHALLENGER-TIER-WARN]` on mismatch (warn-only, exit 0).
Wave 2: promotes to hard-block after 5-run zero-violation telemetry.

## 6. Budget Exception + New SKILL.md Checklist

Add `Budget-Exception: known-debt-tk0e` to the PR body to bypass the CI gate.
New SKILL.md checklist: pick tier → add `tier:` + `model:` + `allowed-tools:` +
`extended_thinking:` → add to `governance/skill-budgets.json` → run
`python3 scripts/check_skill_budgets.py` → exception token + BACKLOG item if over-budget.

See `plugin-dev:skill-development` for full authoring conventions.
