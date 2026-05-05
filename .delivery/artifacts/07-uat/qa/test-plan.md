---
title: "Wave 0 UAT Test Plan"
stage: 07-uat
author: Legolas (quality skill)
created: 2026-05-03
version: 1.0
---

# Wave 0 UAT Test Plan

## Scope

Acceptance of W0-1 (telemetry hook) and W0-2 (SKILL.md line-budget CI gate) from the
perspective of a delivery-team contributor. UAT verifies that a contributor is unblocked
to start Wave 1+ work and that both features behave correctly end-to-end.

Stage 6 dogfood evidence already covers all unit and integration cases. UAT adds four
maintainer-perspective acceptance scenarios that answer: **"would a contributor be
unblocked from Wave 1+?"**

## Pre-conditions

- Clean git tree (`git status` reports nothing modified or staged).
- Both W0-1 and W0-2 branches are merged to main.
- `delivery-team/hooks/telemetry.py` and `scripts/check_skill_budgets.py` exist.
- Python 3.8+ available; no external packages required (stdlib only).
- GitHub Actions CI available on the repository (for Scenario 2 and 3 — CI scenarios).

## Acceptance Scenarios

### Scenario 1 — Telemetry runs invisibly
**Question**: Does the telemetry hook fire silently without blocking the contributor's
Skill invocation or emitting noise to the terminal?

- Trigger any Skill invocation via the hook directly.
- Verify: `.delivery/telemetry/skill-loads.jsonl` grows by exactly 1 row.
- Verify: exit code 0 (Skill not blocked).
- Verify: no output to stdout (invisible to the user).
- **Pass**: row appended; exit 0; stdout empty.

### Scenario 2 — CI gate fires correctly on over-budget PR
**Question**: Does a contributor adding lines to a Tier-A SKILL.md get a clear CI
failure before merge?

- Open a draft PR adding ≥50 prose lines to `delivery-team/skills/delivery-flow/SKILL.md`
  (Tier A, currently 1090/500 lines — no Budget-Exception in body).
- Verify: `skill-line-budget` CI check shows **failure** status.
- Verify: job summary names the file, the tier, and the overage delta.
- **Pass**: check failed; annotation present with file + delta.

### Scenario 3 — Budget-Exception token bypasses gate with warning
**Question**: Can a contributor intentionally carry known-debt through CI without blocking
the merge?

- Open a draft PR with the same over-budget SKILL.md from Scenario 2.
- Add `Budget-Exception: known-debt-tk0e` to the PR description body.
- Verify: `skill-line-budget` CI check shows **passing** status.
- Verify: job summary contains `EXCEPTION ACKNOWLEDGED` warning.
- **Pass**: check passed; warning present; no silent pass (warning required).

### Scenario 4 — Permissive-language scan warns but does not block
**Question**: Does adding `should` to a SKILL.md prose section produce a warning without
blocking the contributor's PR?

- Open a draft PR adding a prose sentence containing `should` to any Tier-C SKILL.md.
- Verify: CI job summary contains a `PERMISSIVE-LANGUAGE` warning line.
- Verify: CI check exits **passing** (warn-only, no failure).
- **Pass**: check passed; warning present in summary.

## Pass Criteria

All 4 scenarios must be green. A scenario is green when every bullet under "Verify"
is satisfied with no manual workarounds.

## Out-of-Scope

- Wave 1+ refactors (token backfill, log rotation, paradigm sub-skill resolution).
- Performance benchmarking beyond the 50 ms hook overhead (already confirmed at 18.7 ms
  in Stage 6 dogfood).
- End-to-end pipeline run timing or throughput testing.
- Non-delivery-team plugins.
