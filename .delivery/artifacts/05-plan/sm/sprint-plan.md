---
title: "Sprint Plan — Wave 0 (Skill Token-Economy Foundations)"
sprint: Wave-0
stage: 05-plan
author: Scrum Master (product-delivery skill)
sources: [prd.md v1.0, ADR-tk0e-001, ADR-tk0e-002, ADR-tk0e-003, architecture-tk0e-wave0.md]
created: 2026-05-03
version: 1.0
---

# Sprint Plan: Wave-0

## 1. Sprint Goal

Install the measurement layer (telemetry hook) and regression guard (CI budget gate) that give the delivery-team plugin an auditable token-economy baseline, unblocking all Wave 1–3 reduction work.

---

## 2. Sprint Dates

| | |
|---|---|
| **Sprint name** | Sprint Wave-0 |
| **Start** | 2026-05-03 |
| **End** | 2026-05-04 (single iteration, ≤ 1 day each WI) |
| **Duration** | 1 iteration (no extensions, no replan) |

---

## 3. Capacity Declaration

| Attribute | Value |
|-----------|-------|
| Team size | 1 (solo — `team.size: 1` per config) |
| Velocity baseline | None (fresh initiative; no historical data) |
| Capacity ceiling | 80% — full attention on W0-1 and W0-2 only |
| WI ceiling | 2 items, hard cap (PRD §8 Sprint Ceiling; gate-patterns memory binding) |

No new items may enter mid-sprint. No replan permitted.

---

## 4. Committed Stories

| WI ID | Story Title | Estimate | Assignee | Dependencies |
|-------|-------------|----------|----------|--------------|
| W0-1 | Telemetry hook: JSONL row per skill invocation | S (≤ 1 day) | Gimli | None |
| W0-2 | Line-budget CI gate + tier frontmatter rollout | S (≤ 1 day) | Gimli | None |

**Parallel execution**: W0-1 and W0-2 are mechanically independent within Stage 6 (Dev). They may proceed in parallel.

### Mandatory Artifacts per WI

**W0-1 — Telemetry Hook**
- `delivery-team/hooks/telemetry.py`
- `delivery-team/hooks/telemetry_report.py`
- `delivery-team/references/telemetry-schema.md` (schema version 1)
- `delivery-team/hooks/hooks.json` (edited: add `PreToolUse` Skill matcher entry)

**W0-2 — CI Budget Gate**
- `scripts/check_skill_budgets.py` (11 known-debt entries; `Budget-Exception` bypass; permissive-language warn-only)
- `.github/workflows/skill-line-budget.yml` (paths-filter: `delivery-team/**/SKILL.md`, `governance/skill-budgets.json`)
- `governance/skill-budgets.json` (fallback tier registry)
- `tier:` frontmatter added to all 13 delivery-team SKILL.md files (per ADR-tk0e-003 canonical mapping)

---

## 5. Commitment Rationale

**Why only these 2:** W0-1 and W0-2 are the complete Wave 0 scope as defined in BACKLOG-100 and PRD §8. Without the telemetry baseline (W0-1), Wave 1 optimization work has no feedback loop. Without the CI gate (W0-2), any gains from Wave 1 will regress. No other work is rational until both land.

**What is NOT included (Wave 1+):**
- SKILL.md line-count reductions (W1-1 through W1-6, W2-1 through W2-6, W3-1 through W3-3)
- PostToolUse token enrichment (deferred to Wave 1 per ADR-tk0e-001)
- Telemetry dashboards or visualization tooling (PRD §6 out-of-scope)
- Non-delivery-team plugin CI gates (out-of-scope)

---

## 6. Risks to Sprint Goal

| # | Risk | Likelihood | Impact |
|---|------|-----------|--------|
| R1 | Hook overhead exceeds 50 ms (NFR-01) — disk read of SKILL.md first 2048B adds latency | Low | High (AC-5 hard fail) |
| R2 | Python frontmatter parser edge cases — SKILL.md files with non-standard YAML blocks, nested fences, or missing closing `---` confuse the regex-based parser | Medium | Medium (CI false positives or misses) |
| R3 | `tier:` frontmatter rollout misses one or more SKILL.md files — 13 files across nested directories including two paradigm sub-skills | Low | Medium (AC-8 fails; CI gate has no tier to check) |
| R4 | `hooks.json` phantom path reference — W0-1 registers a script path that does not exist at merge time (recurring defect pattern) | Low | High (hard AC-7 violation; breaks all PreToolUse hooks) |
| R5 | AC-10 "6 lines" vs actual 11 known-debt files inconsistency causes reviewer confusion | Low | Low (documented in ADR-tk0e-003 footnote) |

---

## 7. Risk Mitigations

| Risk | Mitigation |
|------|-----------|
| R1 (overhead > 50 ms) | Run `--dry-run` timing loop (10 iterations) before committing; synchronous write is < 3 ms on local disk; budget is 50 ms; margin is large. ADR-tk0e-001 explicitly accepted synchronous write as sufficient. |
| R2 (frontmatter parser edge cases) | Use stdlib regex only; parse lines between leading `---` delimiters; treat missing closing `---` as no frontmatter; fall back to `governance/skill-budgets.json` registry. Test against all 13 real files before PR. |
| R3 (tier rollout misses a file) | Run `find delivery-team -name 'SKILL.md' | wc -l` (MUST: 13) and `find delivery-team -name 'SKILL.md' -exec grep -qL "^tier:" {} \; -print` (MUST: no output) as AC-8 verification before marking W0-2 Done. |
| R4 (phantom hook path) | Run FR-12 path-check one-liner before every push: `python3 -c "import json,os; h=json.load(open('delivery-team/hooks/hooks.json')); bad=[e['script'] for e in h.get('hooks',[]) if not os.path.exists(e['script'])]; assert not bad, bad; print('PASS')"` |
| R5 (AC-10 6 vs 11) | Script reports all 11; AC-10 assertion treats 6 as a minimum floor. Document in PR body. |

---

## 8. Dogfood Plan

Per user directive: every WI touching a delivery-team skill MUST be validated by actually running the relevant pipeline path before marking Done. Code review alone is insufficient.

**Wave 0 specific dogfood sequence (after merging W0-1 + W0-2):**

1. **Telemetry verification (W0-1):** Invoke any delivery-team skill through the normal delivery-flow pipeline with the telemetry hook active. Verify `.delivery/telemetry/skill-loads.jsonl` contains ≥ 1 row with all 8 required fields. Attach the JSONL output to the PR body (or linked gist).

2. **Overhead measurement (W0-1 NFR-01):** Run the `--dry-run` 10-call timing script; record mean delta. MUST be < 50 ms. Attach stdout to PR.

3. **CI gate synthetic failure (W0-2 AC-9):** Create a synthetic over-budget SKILL.md (`tier: C`, 201 lines) and run `check_skill_budgets.py` against it locally. Verify exit 1 with budget violation message. Also create a test PR in GitHub Actions (or capture the log) showing the CI step failing on this file. Attach the Actions run log or screenshot to PR.

4. **Tier count verification (W0-2 AC-8):** Paste output of `find delivery-team -name 'SKILL.md' | wc -l` showing `13`; paste `grep "^tier:"` output for both paradigm sub-skills confirming `tier: C`.

5. **Known-debt report (W0-2 AC-10):** Paste full output of `python3 scripts/check_skill_budgets.py --known-debt-report` showing all 11 known-debt entries (minimum 6 lines per PRD AC-10 floor).

All 5 evidence items MUST appear in the PR body or linked gist before reviewer approval.

---

## 9. Definition of Done (Sprint-Level)

- [ ] `delivery-team/hooks/telemetry.py` exists; JSONL row written and verified (AC-1, AC-2)
- [ ] `delivery-team/hooks/hooks.json` updated; every `script:` path verified to exist on disk (AC-7 / FR-12 phantom-path guard)
- [ ] CI gate (`skill-line-budget.yml` + `check_skill_budgets.py`) fails synthetic over-budget test PR and passes a clean PR (AC-9, NFR-03)
- [ ] `tier:` frontmatter present on all 13 delivery-team SKILL.md files; paradigm sub-skills confirmed `tier: C` (AC-8)
- [ ] `check_skill_budgets.py --known-debt-report` outputs ≥ 6 known-debt lines matching format `KNOWN-DEBT: <skill>/SKILL.md <current>/<budget> lines — target wave: W<N>` (AC-10)
- [ ] Dogfood evidence (all 5 items) attached to PR before merge
- [ ] Retrospective completed; defects logged; changelog/release notes drafted
- [ ] No new items entered sprint (sprint ceiling maintained)
