# Consolidated Dev Notes

**Sprint**: UAT Hardening + Pipeline Guardrails
**Developer**: Gimli
**Date**: 2026-03-29

> "Five stories. Four files touched. No line left unverified."

---

## 1. File Change Summary

| File | Stories | Changes |
|------|---------|---------|
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | US-01, US-02/03, US-04, US-05 | Stage 7: new step 5 "Shared-module review", renumbered steps 6-11, QA Engineer validator updated (US-01). Stage 6: new entry condition "Filename reconciliation gate" with 5-step process (US-02/03). Stage 5: new step 4 "Matrix validation", Scrum Bag validator extended, renumbered steps 5-9 (US-04). Stage 6: new step 5 "Regenerate derived artifacts" with 4 substeps, Developer validator updated, renumbered steps 6-7 (US-05). |
| `delivery-team/skills/quality/SKILL.md` | US-01 | New "Shared-Module Review Protocol" section with definition, 5 identification steps, 4-item review checklist, output format. |
| `delivery-team/skills/delivery-flow/references/artifact-contracts.md` | US-01 | New "Empirical Items Classification" row in Stage 6->7 contract table. New "Empirical-Items Tracking Template" section at end of file. |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | US-01, US-02/03, US-04, US-05 | Gate 7: new blocking criterion for empirical-items classification (US-01). Gate 3: new WARNING criterion for phantom file references with `[PLANNED]` exemption (US-02/03). Gate 5: replaced old 80% blocking threshold with two-tier model -- >80% WARNING, >100% BLOCKING (US-04). Gate 6: new blocking criterion for derived artifact regeneration (US-05). |
| `delivery-team/skills/delivery-flow/references/project-templates.md` | US-04 | New "Sprint Plan Mandatory Sections" with Capacity Matrix template (5 columns + Total row) and Coverage Matrix template (5 columns + Unmapped FRs area). Light Mode waiver for BUG_FIX and DOCS_ONLY. |

---

## 2. Per-Story Status

| Story | FRs | Status | Notes |
|-------|-----|--------|-------|
| US-01 | FR-01, FR-02, FR-03, FR-04 | DONE | All 9 ACs verified structurally. No deviations. |
| US-02 | FR-05, FR-06 | CODE_COMPLETE | FR-05 phantom detection WARNING and FR-06 filename reconciliation gate both implemented. All 6 ACs verified structurally. |
| US-03 | FR-05 (Gate 3 portion) | CODE_COMPLETE | Gate 3 phantom reference WARNING with `[PLANNED]` exemption. All 3 ACs verified. |
| US-04 | FR-07, FR-08, FR-09, FR-10 | CODE_COMPLETE | Capacity/coverage templates, matrix validation step, two-tier threshold. All 10 ACs verified structurally. All ACs are structural -- no runtime validation needed. |
| US-05 | FR-11, FR-12 | CODE_COMPLETE | Derived artifact regeneration step + Gate 6 blocking criterion. All 4 ACs verified structurally. |

---

## 3. Deviations from Design Spec

None across all five stories. Every insertion point, content block, severity tag, and retro annotation matches the design spec exactly.

---

## 4. Pending Empirical Validations for UAT

| Item | Story | What Needs Validating | Classification |
|------|-------|-----------------------|----------------|
| Shared-module review step triggers correctly in a real Stage 7 run | US-01 | Step 5 fires, produces output, does not break step sequencing | Empirical (runtime pipeline behavior) |
| QA Engineer DoD validator catches missing shared-module review | US-01 | Validator rejects DoD when shared modules modified but review absent | Empirical (validator logic) |
| Phantom reference WARNING surfaces in Gate 3 without blocking | US-02/03 | Non-existent, non-PLANNED paths produce WARNING that is logged and carried forward | Empirical (gate execution) |
| `[PLANNED]` exemption works at Gate 3, fails at Dev entry | US-02/03 | Gate 3 exempts PLANNED paths; Stage 6 entry blocks on PLANNED without sprint plan entry | Empirical (two-stage gating) |
| Filename reconciliation blocks Stage 6 entry on missing files | US-02/03 | 5-step process runs, FAIL items block entry, resolution guidance shown | Empirical (entry condition) |
| Capacity matrix >80% triggers WARNING with acknowledgment | US-04 | Pipeline prompts for acknowledgment, does not block | Empirical (threshold behavior) |
| Capacity matrix >100% blocks with PO sign-off option | US-04 | Pipeline blocks, offers reduction or PO sign-off path | Empirical (threshold behavior) |
| Coverage matrix unmapped FR = BLOCKING | US-04 | Step 4 validation catches unmapped FRs and blocks | Empirical (validation step) |
| Derived artifact regeneration step runs in Stage 6 sub-flow | US-05 | Step 5 identifies, regenerates, verifies, documents derived artifacts | Empirical (sub-flow execution) |
| Gate 6 blocks when derived artifacts not regenerated | US-05 | Blocking criterion enforced at gate evaluation | Empirical (gate execution) |

---

## 5. Verification Status Summary

| Category | Count |
|----------|-------|
| Total ACs across all stories | 32 |
| Structurally verified (PASS) | 32 |
| Empirical validations pending (UAT) | 10 |
| Deviations from spec | 0 |
| Files modified | 5 |
| Retro annotations applied | All changes tagged with `<!-- retro c8f2 -->` and/or `<!-- retro k4m9 -->` per NFR-05 |

All structural verification is complete. The 10 empirical items above require runtime pipeline execution during UAT to confirm behavioral correctness.
