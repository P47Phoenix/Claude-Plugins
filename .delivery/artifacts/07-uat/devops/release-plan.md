---
title: "Release Plan — Wave 2"
stage: 07-uat
author: Sam (operations skill)
created: 2026-05-03
wave: W2
branch: feature/skill-token-economy-wave-2-tk2
---

# Release Plan: Wave 2

## 1. Release Scope — 65 files

| Story | Key Files |
|-------|-----------|
| S1 doctrine extract | `delivery-flow/SKILL.md`, `references/orchestrator-doctrine.md` (new), `cache-prefix-hash.txt` |
| S2 architect contracts | `architect/SKILL.md` (500 locked), `architect/references/output-contracts/` (new), ADR-tk2-002 |
| S3 developer | `developer/SKILL.md` (296), `references/agent-prompts/` (new), `coding-standards-template.md` |
| S4 product-delivery | `product-delivery/SKILL.md` (299), `references/patterns/` (new) |
| S5 admin | `skill-budgets.json`, `check_skill_budgets.py`, BACKLOG-101, ADR-tk2-001, ADR-tk2-003 |

No service deploy. CI gate already in place.

---

## 2. Pre-Merge Checklist

```bash
# 1 — All 20 Stage 6 DoD files exist (expect: 20)
ls .delivery/artifacts/06-dev/dod/story-{1,2,3,4,5}-{architect,dev,qa,techwriter}-review.md | wc -l

# 2 — All 20 have STATUS: line (expect: empty output)
grep -rL "STATUS:" .delivery/artifacts/06-dev/dod/story-{1,2,3,4,5}-{architect,dev,qa,techwriter}-review.md

# 3 — delivery-flow ≤500 (current 497 ✓)
wc -l delivery-team/skills/delivery-flow/SKILL.md

# 4 — architect ==500 (current 500 ✓)
wc -l delivery-team/skills/architect/SKILL.md

# 5 — developer ≤300 (current 296 ✓)
wc -l delivery-team/skills/developer/SKILL.md

# 6 — product-delivery ≤300 (current 299 ✓)
wc -l delivery-team/skills/product-delivery/SKILL.md

# 7 — cache-prefix sha256 matches stored (expect: OK)
python3 -c "import hashlib; h=hashlib.sha256(open('delivery-team/skills/delivery-flow/SKILL.md','rb').read()).hexdigest(); s=open('governance/cache-prefix-hash.txt').read().split()[0]; print('OK' if h==s else f'MISMATCH {h}')"

# 8 — skill-budgets.json valid + 7 debt entries (expect: debt=7)
python3 -c "import json; d=json.load(open('governance/skill-budgets.json')); kd=d['known_debt']; print(f'debt={len(kd)}'); assert len(kd)==7"

# 9 — CI gate exits 0
python3 scripts/check_skill_budgets.py 2>&1; echo $?
```

> **BLOCKER:** 13/20 DoD files missing `STATUS:` (check 2). Resolve before merge.

---

## 3. Merge Sequencing

Single PR — `feature/skill-token-economy-wave-2-tk2` → `main`. File-disjoint stories; no ordering dependency. Merge commit: `feat(token-economy): Wave 2 doctrine extract, architect contracts, dev/PD trims`

---

## 4. Rollback per Story

| Story | Rollback |
|-------|---------|
| S1 doctrine extract | `git revert <merge-commit>`; restore hash: `git show HEAD~1:governance/cache-prefix-hash.txt > governance/cache-prefix-hash.txt` |
| S2 architect contracts | `git revert -- delivery-team/skills/architect/` |
| S3 developer | `git revert -- delivery-team/skills/developer/` |
| S4 product-delivery | `git revert -- delivery-team/skills/product-delivery/` |
| S5 admin | `git revert -- governance/ scripts/check_skill_budgets.py .delivery/backlog/BACKLOG-101* .delivery/artifacts/04-architect/adrs/ADR-tk2-00*` |

---

## 5. Post-Merge Monitoring

| Window | Check | Pass |
|--------|-------|------|
| First 5 pipeline invocations | `orchestrator-doctrine.md` loaded only in orchestrator role (telemetry) | No stray doctrine loads |
| First 5 architect dispatches | `task_type` → contract file routing resolves correctly | Correct contract selected |
| Cache hit ratio | Second run: `cache_read_input_tokens / input_tokens ≥ 0.85` (ADR-tk2-001) | Ratio ≥ 0.85 |

---

## 6. Stop Rule

Defects/story rate > 0.4 across any rolling 3-PR window → **pause Wave 3**.