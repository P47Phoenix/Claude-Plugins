---
title: "Sprint Plan — Skill Token-Economy Wave 2"
sprint: Wave-2
stage: 05-plan
role: scrum_master
author: Scrum Master (product-delivery skill)
sources: [prd.md v1.0, ADR-tk2-001, ADR-tk2-002, ADR-tk2-003, architecture-tk2-wave2.md]
created: 2026-05-03
version: 1.0
---

# Sprint Plan: Skill Token-Economy Wave 2

## 1. Sprint Goal

Wave 2 brings delivery-flow under Tier-A 500 and ships partial Tier-B compliance for architect, product-delivery, and developer.

---

## 2. Sprint Dates

**Sprint Wave-2** — single iteration; no mid-sprint replan; 5-story ceiling (absolute).

---

## 3. Capacity Declaration

| Parameter | Value |
|-----------|-------|
| Team size | 1 (solo) |
| Effective capacity ceiling | 80% |
| Buffer | 20% — dogfood re-runs and surplus-trim attempts only |
| Replan trigger | None — 5-story ceiling is absolute per BACKLOG-103 |

---

## 4. Committed Stories

| Story | Title | Estimate | Commit Group | Dependencies |
|-------|-------|----------|--------------|--------------|
| S1 | delivery-flow: doctrine extract (W2-1) + config/tables (W2-4) | L | A | Story 5 pre-flight complete |
| S2 | architect: output contracts (W2-2) + model split (W2-6) | M | B | Story 1 merged; cache-prefix stable |
| S3 | developer: coding-standards extract (W2-3) | M | B | Story 1 merged; cache-prefix stable |
| S4 | product-delivery: 12-pattern split (W2-5) | M | B | Story 1 merged; cache-prefix stable |
| S5 | Admin: registry re-baseline (W2-0) + Wave 1 retro backports (W2-7) | S | B | None (anytime) |

**WI consolidation:** 8 WIs → 5 stories by file scope (Wave 1 retro lesson applied).
**Estimates:** S ≈ 1 hr; M ≈ 2–3 hrs including verification; L ≈ 4–6 hrs.

---

## 5. Sequencing Groups

### Group A — Story 1 (serial; critical path)

Story 1 owns the cache-prefix invalidation. Nothing in Group B may merge until
Story 1's dogfood gate passes and `governance/cache-prefix-hash.txt` is updated.

**Story 1 — delivery-flow doctrine extract + config/commands/manifest tables**

Pre-merge gate (Architect dogfood — ADR-tk2-001 §E): synthetic Phase 0–3 pipeline run
(config detect, FEATURE type detect, memory load, Stage 2 Refine dispatch) — zero
routing failures; `wc -l` ≤ 500 (if >520: restore anchors first); cache-prefix hash
updated; W2-4 tables in same PR; bytes 0..2048 unchanged after W2-4.
`plugin-dev:skill-development` pre-loaded (FR-12).

Artifacts (Story 1):
- NEW `delivery-team/references/shared/orchestrator-doctrine.md`
- UPDATED `delivery-team/skills/delivery-flow/SKILL.md` (target ≤ 489 lines)
- UPDATED `governance/cache-prefix-hash.txt` (Wave 1 hash aea33d57... retired)
- NEW `delivery-team/skills/delivery-flow/references/config-keys.md`
- NEW `delivery-team/skills/delivery-flow/references/commands.md`
- NEW `delivery-team/skills/delivery-flow/references/manifest.yml`
- NEW ADR commit (ADR-tk2-001 ratified in-tree)

### Group B — Stories 2, 3, 4, 5 (parallel; non-overlapping file scope)

File-scope isolation enforced: each story touches exactly one SKILL.md and its
own references subtree. No cross-story file overlap permitted.

**Story 2 — architect output contracts + model split** (`plugin-dev:skill-development` FR-12)
- NEW 5 files: `architect/references/output-contracts/{design,adr,game,review,evaluation}.md`
- UPDATED `architect/SKILL.md` ≤498 lines; task_type → contract routing table retained; `{role, task_type, recommended_model}` router + phase-to-model map (~8 lines inline); skill router frontmatter; 198-line Tier-B debt in `skill-budgets.json` (`target_wave: 3`)

**Story 3 — developer coding-standards extract** (`plugin-dev:skill-development` FR-12)
- NEW `developer/references/agent-prompts/coding-standards.md` + `coding-standards-template.md`
- UPDATED `developer/SKILL.md` target ≤300; if ≤340 after Stage 6 trim, register +40 as W3 known-debt

**Story 4 — product-delivery 12-pattern split** (`plugin-dev:skill-development` FR-12)
- NEW 12 files: `product-delivery/references/patterns/<slug>.md` (stable slugs)
- UPDATED `product-delivery/SKILL.md` target ≤300; Phase 1 routing table (~14 lines) retained; if ≤311 after Stage 6 trim, register +11 as W3 known-debt

**Story 5 — Admin: registry re-baseline + Wave 1 retro backports** (no plugin-dev required FR-12)
- UPDATED `governance/skill-budgets.json`: post-W1 counts accurate (delivery-flow 999); W3 known-debt entries (architect ~198, product-delivery +11 risk, developer +40 risk)
- UPDATED `BACKLOG-101` + `ADR-tk1-002`: W1-7 math −1→−2; filename `agent_audit.py`→`audit_agent_prompt.py`; edit-history footer appended

---

## 6. Commitment Rationale

All 5 stories are mechanically scoped with pre-confirmed artifact lists and explicit
line-count math from the three ADRs. No open architectural decisions remain.

Story 1 is the sole serial dependency: it owns the cache-prefix freeze, unblocking all
Group B stories from conflicting on a moving hash target. Group B parallelism is safe
because W2-2, W2-3, and W2-5 each touch a distinct SKILL.md and non-overlapping
references subdirectories. Story 5 admin carries zero file overlap and may land in
any order without coordination cost.

Surplus risk (+11 product-delivery, +40 developer) is bounded and has a defined
fallback: Stage 6 trim then known-debt registration. Architect Tier-B (198-line debt)
is explicitly deferred to BACKLOG-104 Wave 3 per ADR-tk2-002.

---

## 7. Risks to Sprint Goal

| # | Risk | Severity |
|---|------|----------|
| a | **F-08 dispatch fusion regression**: doctrine extraction inadvertently removes a Phase 0–4 routing anchor; project-type or stage dispatch misfires post-merge | High |
| b | **Cache-prefix invalidation**: re-freeze procedure error (wrong byte range, stale hash, W2-4 not co-shipped) breaks CI hash-check | High |
| c | **Surplus lines exceed trim capacity**: architect (+198), product-delivery (+11), developer (+40) not registered in `skill-budgets.json` promptly; Wave-3 scope creep | Medium |
| d | **Doctrine extraction misjudgment**: prose marked safe-to-move contains a Phase 4 behavioral gate; pipeline misfires require partial revert + re-merge | High |

---

## 8. Risk Mitigations

**(a) F-08 regression**
ADR-tk2-001 §A enumerates every load-bearing anchor with line-range estimates. Stage 6
Dev verifies each named anchor present after extraction. Architect dogfood gate (§E) is
a hard pre-merge gate — Phase 0–3 synthetic run MUST pass; any phase misfire restores
the affected anchor before merge. Correctness > line count (ADR-tk2-001 §C).

**(b) Cache-prefix invalidation**
Follow ADR-tk2-001 §D procedure exactly: W2-4 tables co-shipped in same PR as W2-1;
new hash computed via `head -c 2048 delivery-team/skills/delivery-flow/SKILL.md | sha256sum`
post-merge; CI re-baseline committed atomically. W2-4 content verified to touch only
the post-prefix region before closing the hash cycle.

**(c) Surplus lines**
Stage 6 Dev attempts identified surplus-trim candidates first: developer (condense
14-language matrix to routing-table-only; remove duplicate paradigm commentary);
product-delivery (whitespace, duplicate headers, routing commentary). If trim yields
≥ 20 lines but not full target: register remainder as `target_wave: 3` in
`governance/skill-budgets.json` — do NOT block merge on surplus. Story 5 (W2-0)
MUST include these partial known-debt entries; omission is a merge blocker.

**(d) Doctrine misjudgment**
ADR-tk2-001 §B extraction list is conservative — prose elaborations only; behavioral
gate sentences explicitly stay inline. If post-merge pipeline misfires: `git revert`
the extraction commit; restore the affected anchor inline; doctrine file absorbs
compensating growth to maintain Tier-A target.

---

## 9. Dogfood Plan

Per BACKLOG-100 W0-1 directive: end-to-end pipeline iteration before any WI is Done.

| Story | Dogfood Method | Pass Criterion |
|-------|---------------|----------------|
| S1 (W2-1 + W2-4) | **Recursive**: THIS pipeline run (Wave 2) continues into Stage 6 without routing failure after Story 1 merges. Phase 0–3 all fire on the reduced SKILL.md. | No phase misfire; `cache-prefix-hash.txt` non-empty and ≠ aea33d57...; CI green |
| S2 (W2-2 + W2-6) | Synthetic dispatch: 10 representative inputs (Prior Art, ADR draft, TO-BE, Tech Eval, Game Arch, Compliance, Paradigm pick, IR, Review, Decomp). Verify routing table loads only the matched contract; `recommended_model` correct for each. | 10/10 correct contract load + model tier; log attached to PR body |
| S3 (W2-3) | Two synthetic invocations: (1) `write` task → coding-standards template NOT in context; (2) `coding-standards` task → both reference files ARE loaded. | File-presence log confirms conditional load in both cases |
| S4 (W2-5) | 12-task-type dispatch log: each of the 12 task types loads only its matched pattern file; routing table covers all 12. | 12/12 dispatch entries in PR body; no "file not found" errors |
| S5 (W2-0 + W2-7) | `python3 scripts/check_skill_budgets.py --known-debt-report` shows Wave-3 entries for architect (198), and any unresolved product-delivery/developer surplus. Diff of BACKLOG-101 + ADR-tk1-002 shows corrected filenames and math. | Script exits 0; Wave-3 entries visible; corrected docs verified by diff |

---

## 10. Definition of Done (Sprint-Level)

- [ ] All 5 stories merged; all 22 new reference files present in-tree
- [ ] `delivery-team/skills/delivery-flow/SKILL.md` ≤ 500 lines (`wc -l` output in PR body)
- [ ] `delivery-team/skills/architect/SKILL.md` ≤ 500 lines (Tier-A met; Tier-B ≤300 deferred Wave 3 — entry in `skill-budgets.json`)
- [ ] `delivery-team/skills/product-delivery/SKILL.md` ≤ 300 lines OR Wave-3 known-debt entry registered in `governance/skill-budgets.json`
- [ ] `delivery-team/skills/developer/SKILL.md` ≤ 300 lines OR Wave-3 known-debt entry registered in `governance/skill-budgets.json`
- [ ] `governance/cache-prefix-hash.txt` updated (≠ aea33d57...); CI hash-check green
- [ ] All 13 delivery-team SKILL.md tier frontmatter entries intact (no tier field removed or degraded)
- [ ] `delivery-team/hooks/audit_agent_prompt.py` unchanged (filename corrections are docs-only; no script modifications)
- [ ] Telemetry post-merge captures Wave 2 line counts and per-pipeline token delta (delivery-flow ≥ 30% reduction vs Wave 1 baseline)
- [ ] Retrospective completed; defects logged; Wave 2 changelog drafted
