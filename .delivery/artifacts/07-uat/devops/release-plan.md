---
title: "Release Plan — Wave 0"
stage: 07-uat
author: Sam (operations skill)
created: 2026-05-04
wave: W0
---

# Release Plan: Wave 0

## 1. Release Scope — 20 files

| WI | Files |
|----|-------|
| W0-1 | telemetry.py, telemetry_report.py, telemetry-schema.md, hooks.json (edited) — 4 files |
| W0-2 | check_skill_budgets.py, skill-line-budget.yml, skill-budgets.json + 13 existing SKILL.md files (tier: frontmatter added; +1 line each) — 16 files |

## 2. Pre-Merge Checklist

- [ ] All 8 Stage 6 DoD review files exist with STATUS: DONE — verify with: `ls .delivery/artifacts/06-dev/dod/w0-{1,2}-{dev,qa,architect,techwriter}-review.md && grep -c "STATUS: DONE" .delivery/artifacts/06-dev/dod/w0-*-*-review.md` — expect 8 files listed and 8 DONE counts
- [ ] Dogfood evidence files present:
      `06-dev/dogfood-evidence/w0-1-telemetry-evidence.md` + `w0-2-budget-gate-evidence.md`
- [ ] `find delivery-team -name SKILL.md -exec grep -L "^tier:" {} \;` returns empty
- [ ] `python3 scripts/check_skill_budgets.py --known-debt-report` exits 0 (≥11 lines)
- [ ] `python3 -c "import json; json.load(open('delivery-team/hooks/hooks.json'))"` no exception
- [ ] `git status` clean — no untracked Wave 0 leftovers
- [ ] PR body contains token `Budget-Exception: known-debt-tk0e`

## 3. Merge Sequencing

Single PR to `main`. Conventional-commit message:
`feat(token-economy): Wave 0 telemetry + CI gate`

PR body MUST include `Budget-Exception: known-debt-tk0e` — the new gate would
otherwise block its own introducing commit (chicken-and-egg).

## 4. Rollback Plan

**W0-1 misbehaves** (overhead breach, JSONL corruption, phantom path):
```
git revert <merge-commit> -- delivery-team/hooks/hooks.json \
  delivery-team/hooks/telemetry.py delivery-team/hooks/telemetry_report.py \
  delivery-team/references/telemetry-schema.md
```

**W0-2 misbehaves** (false positives blocking clean PRs):
```
git revert <merge-commit> -- .github/workflows/skill-line-budget.yml \
  scripts/check_skill_budgets.py governance/skill-budgets.json
```
Then revert the 13 SKILL.md `tier:` additions. Note: `tier:` frontmatter is
reader-benign — only revert SKILL.md edits if the gate actively breaks downstream PRs.

## 5. Post-Merge Monitoring

| Window | Check | Pass |
|--------|-------|------|
| First 5 invocations | JSONL row written, all 8 fields present | ≥1 row / invocation |
| First 5 invocations | Hook overhead (`time`) | Mean < 50 ms (baseline 18.7 ms) |
| First 5 SKILL.md PRs | CI gate fires or bypasses correctly | No false block/pass |

## 6. Stop Rule (BACKLOG-100)

Defects/story rate > 0.4 across any rolling 3-PR window → pause Wave 2.
