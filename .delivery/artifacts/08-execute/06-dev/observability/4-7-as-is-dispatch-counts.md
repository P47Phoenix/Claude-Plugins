---
work_item: WI-01
task_type: observability-capture
role: developer (Gimli)
pipeline_id: run-2026-04-22-4x7e
captured_at: 2026-04-22
scope: AS-IS validator-dispatch counts for Opus 4.7 dogfood run
inputs:
  - .delivery/config.yml (dod_validators.*)
  - .delivery/artifacts/08-execute/01-idea/stage-summary.md
  - .delivery/artifacts/08-execute/02-refine/stage-summary.md
  - .delivery/artifacts/08-execute/04-architect/stage-summary.md
  - .delivery/artifacts/08-execute/05-plan/stage-summary.md
---

# 4.7 AS-IS Validator-Dispatch Count Capture

## Measurement rule

`expected_count` = length of `dod_validators.<stage>` list in `.delivery/config.yml` (v2.7).

`actual_count` = number of distinct DoD validator role-dispatches evidenced in the stage's `stage-summary.md` for this pipeline run (`run-2026-04-22-4x7e`). Re-invocations of the same role across self-correction rounds count once — the question is coverage, not invocation volume.

`delta` = `actual_count - expected_count`.

## Count table

| stage     | depth       | expected_count | actual_count | delta | note                                                                 |
|-----------|-------------|----------------|--------------|-------|----------------------------------------------------------------------|
| idea      | light       | 2              | 1            | -1    | light — sole-reviewer (architect); PO is primary author, not validator |
| refine    | light       | 4              | 1            | -3    | light — developer-only DoD across 2 rounds                           |
| design    | n/a         | 5              | 0            | -5    | skipped per DX-only routing deviation (documented, not silent)       |
| architect | light       | 5              | 1            | -4    | light — QA-only DoD for drift-check scope                            |
| plan      | full        | 5              | 3            | -2    | full — documented author-proxy reduction (SM/DevOps/PO); 3 cross-perspective validators (developer, qa, architect) |

## Row-by-row analysis

**idea (light, delta=-1):** Stage-summary shows one DoD validator — Celebrimbor (architect) — who passed all six blocking gates on Gandalf's idea-brief. The expected list `[po, architect]` treats PO as validator, but in this run PO is the primary author (Gandalf wrote the idea-brief), so PO cannot self-validate. Light-mode collapses to sole-reviewer and the reviewer is the non-author role. Expected for light depth.

**refine (light, delta=-3):** Stage-summary shows Gimli (developer) as the single DoD role, invoked across two rounds (round1 NOT_DONE with 6 gates, round2 DONE after self-correction). Same role re-invocation does not add distinct coverage — it is the evaluator-optimizer loop operating on one perspective. Light mode reduced `[po, architect, developer, qa]` to `[developer]`. Expected for light depth.

**design (delta=-5, skip):** Directory `.delivery/artifacts/08-execute/03-design/` does not exist. The DX-only routing deviation was a documented pipeline-level decision, surfaced at Phase-1 project-type detection for this engagement. Zero dispatches is the correct count for a documented skip; this is not silent fusion.

**architect (light, delta=-4):** Stage-summary shows Legolas (qa) as the single DoD validator who confirmed all five blocking gates PASS on Celebrimbor's drift-check. Primary agent and DoD validator are distinct roles (architect authored, qa validated), so coverage is honest. Light mode reduced `[architect, qa, developer, devops, security]` to `[qa]` because the primary artifact is a drift-check (no new architecture authored), narrowing the perspectives that add signal. Expected for light depth.

**plan (full, delta=-2):** Stage-summary shows three DoD validators — Gimli (developer), Legolas (qa), Celebrimbor (architect) — in parallel. The `dod_reduction_note` in the summary frontmatter explicitly documents the reduction: SM and DevOps are author-proxies of their own primary artifacts (sprint-plan and deploy-plan respectively), and PO is author-proxy of the upstream execution-PRD. Substituting Celebrimbor (architect) for the config-listed PO gives three cross-perspective validators who did not author the artifacts they reviewed. The reduction is documented in-band, not silent. Counts consistent across all four Plan artifacts per Legolas's DoD.

## R-09 verdict

**R-09: NOT_TRIGGERED.**

R-09 triggers only when a FULL-depth stage silently reduces validator count (F-08 silent fusion). In this run:

- Idea, Refine, Architect ran at LIGHT depth — `actual < expected` is the definition of light, not fusion. Each light reduction is annotated in the stage-summary frontmatter (`depth: light`) and justified against scope.
- Design is a documented DX-only skip, surfaced at project-type detection. Zero dispatches is the correct count for a skipped stage.
- Plan ran at FULL depth with `actual_count = 3 < expected_count = 5`, but the reduction is explicitly documented in the stage-summary `dod_reduction_note` frontmatter key, not silent. SM and DevOps are author-proxies (they wrote the very artifacts they would have been asked to review — self-validation is worthless); PO is author-proxy of the upstream PRD. Three cross-perspective validators (developer, qa, architect) provide the multi-perspective coverage F-08 demands.

Silent fusion requires loss of validator perspective without a paper trail. Every reduction in this run has a paper trail in the stage-summary frontmatter. No silent fusion detected. Wave 2 proceeds.

## Firming Assumption A-05 at count level: YES

A-05 (the validator-dispatch-count AS-IS is capturable from stage-summary frontmatter alone) holds. Every `expected`/`actual`/`delta` cell in the table above was derived from two sources: `.delivery/config.yml` (expected) and the `dod_validators` block in each stage's `stage-summary.md` frontmatter (actual). No grepping of transcripts, no log archaeology, no manual dispatch counting required. The frontmatter is the observability surface.
