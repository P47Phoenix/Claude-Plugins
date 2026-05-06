---
title: "delivery-team Contributor Guide — Wave 2 additions"
stage: 07-uat
author: Bilbo (operations skill, tech-writer role)
created: 2026-05-03
supersedes: Wave 1 user-guide (2026-05-03)
---

# Contributor Guide: Skill Token-Economy (Wave 0–2)

## 1. Tier Budgets (unchanged)
| Tier | Budget | Used for |
|------|--------|----------|
| A | 500 | Orchestrators (`delivery-flow`) |
| B | 300 | Multi-role / multi-domain skills |
| C | 200 | Single-role or single-domain skills |

## 2. Wave 2 — Shared Doctrine File
`delivery-team/references/shared/orchestrator-doctrine.md` is the canonical home for Prime
Directive elaboration, Anti-Patterns, and collaboration pattern prose. Edit doctrine there,
not inside individual SKILL.md files.

## 3. Architect Output Contracts
Per-task contracts: `references/output-contracts/<task_type>.md`
(greenfield-design · brownfield-migration · spike · design-sprint · transformation-planning).
The task router loads the matched contract at dispatch time.

## 4. Product-Delivery Patterns
12 task-type patterns at `references/patterns/<slug>.md`.
Skill body holds only the routing index — add new patterns as separate files.

## 5. Developer Coding Standards
- `references/agent-prompts/coding-standards.md` — shared standards
- `references/coding-standards-template.md` — template for new languages

Never inline language-specific standards back into `developer/SKILL.md`.

## 6. Cache-Prefix Freeze (hash updated)
First ~2 KB of `delivery-flow/SKILL.md` frozen at sha256 `9d4011d1…`.
PRs touching that region must regenerate `governance/cache-prefix-hash.txt`, cite an ADR,
and add `Cache-Prefix-Change: <ADR-link>` to the PR body.
```bash
python3 -c "import hashlib; h=hashlib.sha256(open('delivery-team/skills/delivery-flow/SKILL.md','rb').read()[:2048]).hexdigest(); open('governance/cache-prefix-hash.txt','w').write(h+'\n'); print(h)"
```

## 7. Architect Model Split
| Phase type | Model |
|------------|-------|
| Classification / task routing | `sonnet` |
| Design synthesis / architecture output | `opus` |

## 8. Budget Exception + New SKILL.md Checklist (unchanged from Wave 1)
`Budget-Exception: known-debt-tk0e` in PR body bypasses CI gate.
New SKILL.md: tier → `model:` → `allowed-tools:` → `extended_thinking:` →
`governance/skill-budgets.json` → `python3 scripts/check_skill_budgets.py`.
See `plugin-dev:skill-development` for full authoring conventions.

## 9. Rollback
If a Wave 2 change misbehaves post-merge, see `.delivery/artifacts/07-uat/devops/release-plan.md` §4 for per-story rollback procedures. Quick reference:
- delivery-flow restructure (Story 1): `git revert <merge-commit>` + restore prior `governance/cache-prefix-hash.txt`
- architect / developer / product-delivery extraction: `git revert -- delivery-team/skills/<skill>/`
- Story 5 admin (registry + retro backports): `git revert -- governance/ scripts/check_skill_budgets.py .delivery/backlog/BACKLOG-101*`
