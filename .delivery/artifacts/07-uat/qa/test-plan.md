<!-- run: run-2026-05-05-tk3 | stage: 07-uat | depth: light | author: QA Engineer (Legolas Greenleaf) | role: qa-engineer | task: test-plan -->

# UAT Test Plan — Caveman-Lite Prose Discipline (run-2026-05-05-tk3)

> "Five leagues hence — a host of structural ACs. Twelve verified. One waits beyond the next ridge."
> — Legolas, marking the field.

Stage 7 UAT for one Story (BACKLOG-102 W2-1 + W2-2 + W2-3 consolidated). Light depth — single story, mostly verification of Stage-6 Dev DoD output, plus the empirical core (synthetic structural dogfood + post-merge measurement protocol carry-forward).

## Objective

Validate that the caveman-lite prose discipline implementation lands cleanly: structural ACs (TC-1..8) all pass, the orchestrator's PROSE STYLE injection logic is correct under all four conditional paths (default caveman-lite, three auto-clarity exemptions, opt-out standard), and the post-merge empirical measurement protocol (BACKLOG-102 AC-1 token reduction; AC-2 DoD review byte reduction; AC-3 DoD pass-rate; AC-4 downstream artifact quality) is documented and ready to fire on the next pipeline run.

## Scope

**In**: 8 TCs from `.delivery/artifacts/05-plan/qa/test-strategy.md`, all 13 Story-1 ACs, structural verification of all 6 ADR-tk3-001 contract elements, 5-dispatch synthetic structural dogfood, post-merge measurement protocol carry-forward. **Out**: Real post-merge token measurements (by design — requires next pipeline run); per-role overrides; Tier 2 retrospective/sprint-plan A/B (BACKLOG-103+).

## Strategy Summary

Two halves:

1. **Structural verification** (TC-1 through TC-8) — re-run every Stage-6 Dev DoD verification command. Every command from `06-dev/developer/story-1-implementation.md` §"Verification Commands and Outputs" gets re-executed by Legolas independently. PASS only on byte-exact match to expected output.
2. **Empirical structural dogfood** (5 synthetic dispatches) — verify the orchestrator's Phase 4 Step 4/5/7 prompt-construction logic produces the right PROSE STYLE block under each conditional branch (default; security; destructive-op; multi-step; opt-out). No real Agent dispatch needed — the PROSE STYLE block is in-prompt directive, so the agent is the detector for exemptions per ADR-tk3-001 Element 3. Verifying the directive is structurally present and unambiguous closes AC-5 and AC-6 short of a full pipeline run.

The empirical AC-13 sub-clause (BACKLOG-102 AC-1: ≥20% prose-token reduction over 5 dispatches; AC-2: ≥25% DoD review byte reduction) cannot close pre-merge — by definition it requires post-merge dispatches against this implementation. Documented as carry-forward in `dogfood-report.md` §3.

## Test Schedule

| Phase | Activities | Duration | Dependencies |
|---|---|---|---|
| Phase 1 — Structural verification | TC-1..8 re-runs | 5 min | Stage 6 implementation report |
| Phase 2 — Synthetic structural dogfood | 5 dispatch-prompt constructions | 10 min | Phase 1 PASS |
| Phase 3 — Carry-forward documentation | Post-merge measurement protocol | 5 min | Phase 2 PASS |

## Test Cases

Embedded in `test-cases.md` (one entry per TC + pass/fail with evidence).

## Shared-Module Review

Five files modified by Stage 6 are referenced across multiple stages (Idea/Refine/Architect/Plan/Dev artifacts):

| Module Path | Stages Referencing | Modified in Dev | Test Coverage | Status |
|---|---|---|---|---|
| `delivery-team/skills/delivery-flow/SKILL.md` | 04-architect, 05-plan, 06-dev | Yes | TC-7 (sha), TC-8 (budget), Dispatch 1+5 (Phase 0 directive) | PASS |
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | 04-architect, 05-plan, 06-dev | Yes | TC-2 (3 templates), Dispatch 1-5 (delimiter ordering) | PASS |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | 04-architect, 05-plan, 06-dev | Yes | TC-3 (verdict-prose, STATUS, FINDINGS) | PASS |
| `delivery-team/skills/delivery-flow/references/config-schema.md` | 04-architect, 05-plan, 06-dev | Yes | TC-1, TC-6 (v2.9 + prose_style row) | PASS |
| `delivery-team/skills/delivery-flow/references/config-schema.json` | 06-dev (regenerated) | Yes | TC-6 (Python json.load assertion) | PASS |
| `governance/cache-prefix-hash.txt` | 04-architect (ADR Element 5), 06-dev | Yes | TC-7 (sha-match) | PASS |
| `delivery-team/skills/delivery-flow/references/prose-style.md` | 06-dev (NEW) | Yes (created) | Dispatch 2-4 (verbatim exemption clauses) | PASS |

**Findings**: No gaps. Every modified shared module has a TC or dispatch covering its consuming context. The new `prose-style.md` reference is the canonical fixture for the verbatim PROSE STYLE block; it is not registered in `marketplace.json` because it is a reference (not a sub-skill) — same pattern as `pipeline-stages.md` and `quality-gates.md`.

## Entry / Exit Criteria

**Entry**: Stage 6 implementation report exists with STATUS: CODE_COMPLETE; all source files referenced in the report exist on disk.

**Exit**: TC-1..8 all PASS; 5 synthetic dispatches verify conditional logic structurally; post-merge measurement protocol documented in `dogfood-report.md`; PO go/no-go input emitted.

**CODE_COMPLETE rationale**: AC-13 sub-clause (BACKLOG-102 initiative AC-1/AC-2 telemetry deltas) cannot empirically close without a post-merge pipeline run. Per UAT memory lesson 3, structural-only validation caps confidence below 5/5 and carries a P1 follow-up. This is GO_WITH_NOTES territory, not NO_GO.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| First post-merge run shows <15% prose-token reduction | BACKLOG-102 stop-rule armed; pause Tier-2 A/B; root-cause retro before further waves |
| Auto-clarity false-positive in production (security warning compressed) | In-prompt directive verbatim per ADR Element 3; agent is the detector; spot-check the first 3 post-merge dispatches that touch security/destructive/multi-step contexts |
| Telemetry hook (BACKLOG-100 W0-1) emits zero-value rows on next run | Existing rows in `.delivery/telemetry/skill-loads.jsonl` are zero-token placeholders from a single 21ms burst on 2026-05-04; Wave 2 archive prose-byte data is the de-facto baseline |

## Sign-Off

QA recommends GO_WITH_NOTES at PO checkpoint. Evidence: `test-cases.md` (8/8 PASS), `dogfood-report.md` (5/5 dispatches PASS structural, AC-13 carry-forward documented), `go-no-go-input.md`.

---

STATUS: CODE_COMPLETE
ARTIFACT: .delivery/artifacts/07-uat/qa/test-plan.md
SUMMARY: Light UAT plan; 8 TCs structurally verified; 5-dispatch synthetic dogfood; AC-13 telemetry carry-forward to next pipeline run.
