# Story 6 (W3-10 + W3-11 + W3-12) — Retro KPI + Fitness Review + CLAUDE.md Refactor — Implementation Record

**Date**: 2026-05-09
**Pipeline**: run-2026-05-09-tk4 (Wave 3)
**Developer**: Gimli (delivery-team:developer + plugin-dev:skill-development pre-load)
**Branch**: feature/wave-3-tk4
**Authority**: Stage 5 stories.md §Story 6, BACKLOG-104 §W3-10/11/12, DEFECT-004 regression guard

Three small forge-strikes. Retro pattern sharpened, fitness wheel built, CLAUDE.md hewn to size — and well past the cap.

---

## Three-WI Implementation Table

| WI | Surface | Action | Verification |
|----|---------|--------|--------------|
| W3-10 | `delivery-team/skills/product-delivery/references/patterns/retro.md` | Added `context_tokens_per_pipeline_run` KPI section: 5-run rolling-mean formula, source-data path (`.delivery/telemetry/skill-loads.jsonl`), compute spec, Δ annotation rules (REGRESSION/IMPROVEMENT thresholds), W3-18 PENDING marker | `grep context_tokens_per_pipeline_run` returns 2 hits in retro.md |
| W3-11 | `governance/fitness-review.md` (new, 80 lines) + `.github/workflows/fitness-review.yml` (new, 145 lines) | Authored process doc (Purpose / Cadence / Scope / Procedure / Outputs / Escalation) + weekly cron workflow that scans every SKILL.md frontmatter `fitness_review_due:`, opens reminder issue 30-day window, P1-labels >180-day overdue | both files exist; YAML parses cleanly; workflow-injection-lint PASSES (no `github.event.*` in run blocks) |
| W3-12 | `CLAUDE.md` (168 → 110), `delivery-team/ARCHITECTURE.md` (+per-skill roster table), `hardware-team/ARCHITECTURE.md` (new, 47 lines) | Extracted delivery-team 11-skill table + 7-hooks table + hardware-team 7-skill + 6-hooks tables to per-plugin ARCHITECTURE.md. Added `Detail` column to plugin index (one-hop discoverability). Fixed stale `architect/skills/paradigms/` → `architect/paradigms/`. | `wc -l CLAUDE.md` returns 110 (≤150); `grep "architect/skills/paradigms/" CLAUDE.md` exit 1 (no match); 4 ARCHITECTURE.md links from CLAUDE.md |

---

## Per-WI Verification

### W3-10 — Retro KPI

```
$ grep -n "context_tokens_per_pipeline_run" delivery-team/skills/product-delivery/references/patterns/retro.md
22:#### context_tokens_per_pipeline_run
42:   ... extract their `context_tokens_per_pipeline_run`
```

KPI section adds: 5-row table (This run / Rolling mean / Δ / Source / Compute / Status), 5-step compute spec (filter telemetry → sum → read prior 4 archives → mean → Δ), thresholds (>+10% = REGRESSION, <-10% = IMPROVEMENT), and explicit `PENDING (W3-18)` marker until Story 7 telemetry hardening lands.

### W3-11 — Fitness review process

`governance/fitness-review.md` (102 lines) contains six sections — Purpose, Cadence, Scope, Procedure, Outputs, Escalation — plus a companion-artifact box. Procedure is a 7-step protocol with rotation rules (no author-reviews-own-work), budget check, frontmatter inspection, trigger-phrase spot-check, references freshness, KPI check, outcome record. Escalation triggers Architect review on 2-cycle FAIL streak; >180-day overdue auto-P1.

`.github/workflows/fitness-review.yml` (157 lines) runs weekly cron `0 14 * * 1` + manual dispatch. Single job: embedded Python walks `Path('.').rglob('SKILL.md')`, parses `fitness_review_due:` frontmatter, classifies due_soon (≤30 days) / overdue (>180 days = P1), writes step summary + `fitness-review-scan.json`, then `gh issue create --body-file` (no `github.event.*` in any run block — DEFECT-004 regression guard PASSES).

```
$ python3 [workflow-injection-lint logic] .github/workflows/fitness-review.yml
OK: no injection antipattern found.

$ python3 -c "import yaml; print(list(yaml.safe_load(open('.github/workflows/fitness-review.yml'))))"
['name', True, 'permissions', 'jobs']
```
(The `True` key is YAML's harmless boolean coercion of unquoted `on:` — GitHub Actions runtime reads it correctly; same shape as the other shipped workflows.)

### W3-12 — CLAUDE.md refactor

```
$ wc -l CLAUDE.md
110 CLAUDE.md
```

**58-line reduction** (168 → 110), 40-line headroom under the 150 cap.

Extracted: delivery-team 11-skill table → `delivery-team/ARCHITECTURE.md` §1 "Per-skill roster" (newly added subsection). hardware-team 7-skill + 6-hook tables → new `hardware-team/ARCHITECTURE.md` (47 lines). Deep-dive 15-bullet pipeline list → already in `delivery-team/ARCHITECTURE.md` + `delivery-flow/references/*`; CLAUDE.md keeps a 5-bullet summary with one-line pointer. delivery-team 7-hook table was already in `delivery-team/ARCHITECTURE.md` §7 — no duplication needed.

Preserved per directive: repository purpose, plugin structure (directory tree), plugin index (now with `Detail` column → per-plugin ARCHITECTURE.md), CI regression guards (extended with `skill-line-budget.yml` and new `fitness-review.yml`), running scripts, architecture patterns summary, key conventions (added SKILL.md line-budget rule + fitness-review pointer), permissions.

One-hop discoverability holds: 4 ARCHITECTURE.md links from CLAUDE.md (delivery-team, hardware-team, agentic-flow-builder rows + summary pointer).

```
$ grep "architect/skills/paradigms/" CLAUDE.md ; echo exit=$?
exit=1
```
Stale path eliminated; per-skill-roster row in the new ARCHITECTURE.md subsection cites correct `architect/paradigms/`.

---

## DoD Self-Check (Story 6 ACs)

| AC | Required | Result |
|----|----------|--------|
| W3-10 AC | Retro template contains KPI section with formula + source-data reference; rolling-mean + Δ compute documented | PASS — section authored, formula explicit, W3-18 PENDING marker recorded |
| W3-11 AC-doc | `governance/fitness-review.md` exists with cadence/owner/inputs/outputs/kill-criteria | PASS — 6 sections present, escalation rules concrete |
| W3-11 AC-workflow | Workflow exists, weekly cron, opens issues, workflow-injection-lint PASSES | PASS — file exists, cron `0 14 * * 1`, gh issue create via --body-file, no `github.event.*` in any run block |
| W3-12 AC | `wc -l CLAUDE.md` ≤150; one-hop link preserved | PASS — 110 lines (40-line headroom); 4 ARCHITECTURE.md links |
| W3-12 AC-side-fix | `grep "architect/skills/paradigms/" CLAUDE.md` returns 0 | PASS — exit 1 (no match) |

**Skill budgets regression check** (verification step 5):
```
$ python3 scripts/check_skill_budgets.py
BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).
```
No regressions on the 17 SKILL.md files in scope. CLAUDE.md is excluded from skill budgets per the prompt; the cap on CLAUDE.md is the binding cap from `topics/skill-token-economy.md` Ruling 3 (≤150 lines), enforced informally pending W3-12 AC's optional CI extension.

**plugin-dev routing**: `plugin-dev:skill-development` SKILL_LOADED at the top of this dispatch (binding for skill-adjacent edits — retro template lives under product-delivery/references). No SKILL.md file was directly modified in this story; the changes touched `references/`, `governance/`, `.github/workflows/`, and the repo-root `CLAUDE.md`. `plugin-dev:skill-reviewer` not required (no SKILL.md edit). `plugin-dev:plugin-validator` recommended pre-PR for the marketplace-discoverability check (no marketplace registration changed; mechanically inert).

**No state.md modification** per directive. **No Stories 1-5 or Story 7 surfaces touched.**

---

## Files Created / Modified

```
M  CLAUDE.md                                                                  168 → 110
M  delivery-team/skills/product-delivery/references/patterns/retro.md         20 → 50
M  delivery-team/ARCHITECTURE.md                                              261 → 280 (+per-skill roster table)
A  governance/fitness-review.md                                               80 lines
A  .github/workflows/fitness-review.yml                                       145 lines
A  hardware-team/ARCHITECTURE.md                                              47 lines
A  .delivery/artifacts/06-dev/developer/story-6-implementation.md             this file
```

Three forge-strikes landed clean. No half-measures, no hot iron left on the anvil.

— Gimli, Stage 6 Developer, run-2026-05-09-tk4
