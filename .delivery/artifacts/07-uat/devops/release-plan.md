---
title: "Release Plan — Wave 1"
stage: 07-uat
author: Sam (operations skill)
created: 2026-05-03
wave: W1
branch: feature/skill-token-economy-wave-1-tk1
---

# Release Plan: Wave 1

## 1. Release Scope — 55 files

| Story | WIs | Files |
|-------|-----|-------|
| Story 1 — delivery-flow restructure | W1-1, W1-2, W1-6 | `delivery-flow/SKILL.md` (−91 lines), `references/stages.yml` (new), `references/stages-schema.json` (new), `governance/cache-prefix-hash.txt` (new), `.delivery/artifacts/` (plan/arch/ADR docs) |
| Story 2 — frontmatter rollout | W1-3, W1-4, W1-7 | 12 SKILL.md (`allowed-tools`), 5 SKILL.md (`phase_1_detector_model: haiku`), `alias-creator/SKILL.md` (200 lines final), `governance/skill-budgets.json`, `scripts/check_skill_budgets.py`, `.claude-plugin/marketplace.json` |
| Story 3 — challenger hook | W1-5 | `delivery-team/hooks/audit_agent_prompt.py` (+95 lines, additive) |

**Total changed files (git status --short):** 55

---

## 2. Pre-Merge Checklist

- [ ] **DoD files (12):** `ls .delivery/artifacts/06-dev/dod/story-{1,2,3}-{dev,qa,architect,techwriter}-review.md` — expect 12 paths, all present
- [ ] **alias-creator budget:** `wc -l delivery-team/skills/alias-creator/SKILL.md` — expect `200`
- [ ] **allowed-tools coverage:** `find delivery-team -name SKILL.md ! -path '*delivery-flow*' -exec grep -L "^allowed-tools:" {} \;` — expect empty output
- [ ] **delivery-flow frontmatter:** `grep -E "^model: sonnet|^## Volatile" delivery-team/skills/delivery-flow/SKILL.md` — expect 2 matches
- [ ] **Cache-prefix hash:** `python3 -c "import hashlib; print(hashlib.sha256(open('delivery-team/skills/delivery-flow/SKILL.md','rb').read()[:2048]).hexdigest())" | diff - <(awk '{print $1}' governance/cache-prefix-hash.txt)` — expect no diff
- [ ] **Hook syntax:** `python3 -m py_compile delivery-team/hooks/audit_agent_prompt.py` — expect exit 0
- [ ] **CI budget gate:** `python3 scripts/check_skill_budgets.py 2>&1` — expect exit 0, 0 violations
- [ ] **Marketplace description ≤500 chars:** `python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); print(len([p for p in d['plugins'] if p['id']=='delivery-team'][0]['description']))"` — expect ≤500
- [ ] **No LLM calls in hook:** `grep -rE 'anthropic|openai|litellm' delivery-team/hooks/` — expect empty

---

## 3. Merge Sequencing

Single PR — branch `feature/skill-token-economy-wave-1-tk1` → `main`. All 7 WIs are already committed as 3 story groups on the feature branch.

Conventional-commit message for merge:
```
feat(token-economy): Wave 1 cache-freeze, haiku routing, challenger hook
```

No service deploy. CI gate (`.github/workflows/skill-line-budget.yml`) already in place from Wave 0.

---

## 4. Rollback Plan

| Scenario | Action |
|----------|--------|
| Cache-prefix freeze breaks future pipeline runs | `git revert <merge-commit>` — reverts all Wave 1 changes; `cache-prefix-hash.txt` deletion is benign (CI will warn, not block) |
| Frontmatter additions (`allowed-tools`, `phase_1_detector_model`) cause dispatch errors | Revert specific SKILL.md files; `allowed-tools` and `phase_1_detector_model` are additive — reverting selectively leaves others intact |
| Challenger hook fires false positives | Warn-only by design (exit 0). Temporarily disable: add `# DISABLED` comment before the `_emit_challenger_warning()` call in `audit_agent_prompt.py`, then raise PR for proper fix before full revert |

---

## 5. Post-Merge Monitoring

| Window | Check | Pass signal |
|--------|-------|-------------|
| First 5 pipeline invocations | Telemetry JSONL contains `"model": "haiku"` rows for Phase 1 routing | ≥1 haiku row per invocation |
| First 5 PRs | CI budget gate exits 0 on clean PRs; fires on over-budget additions | No false block or false pass |
| First adversarial dispatch | `[CHALLENGER-TIER-WARN]` present in stderr if model mismatch; absent when models match | Correct presence/absence in both cases |

---

## 6. Stop Rule (carryover)

Defects/story rate > 0.4 across any rolling 3-PR window → **pause Wave 2**.
