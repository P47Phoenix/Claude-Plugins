# QA DoD Review — Refine Stage (Paired Constraints Primitive)

**Validator**: Legolas (QA Engineer) | **Date**: 2026-04-08 | **Stage**: 2 Refine
**Under review**: `.delivery/artifacts/02-refine/po/prd.md`
**Supporting**: `.delivery/artifacts/02-refine/data/metrics-baseline.md`

> *"That bug still only counts as one."*

## Gate Criteria — QA Lens

1. **Every AC testable.** PASS. AC-1..AC-5, AC-8 are rule-based with explicit file/grep predicates; AC-6 and AC-7 are empirical with named denominator (5 runs) and artifact path. Each has an imaginable failing and passing case. My bow-hand is still.
2. **Metrics measurable with existing instrumentation.** PASS. Elrond's §5 maps each PRD metric to an extant memory file or grep over `.delivery/artifacts/04-architect/**/*.md`. No new tooling required — `memory/index.md`, `stages/plan.md`, `topics/gate-patterns.md`, `defects/index.md` all exist.
3. **Forbidden vocabulary enumerated, not heuristic.** PASS. FR-3, NFR-2, AC-3 list the tokens: `lambda|ecr|sqs|ec2|s3|dynamodb|kafka|python|node|typescript|golang`. R-3 codifies "enumerated, not heuristic". Greppable. I count them like orc kills.
4. **80% Plan target has defined measurement window.** PASS. NFR-1 and AC-6 say **"5 subsequent pipeline runs"**; Success Metrics row 1 echoes "5-run rolling window post-land". Window stated plainly.
5. **Dogfood AC has concrete Exhibit A.** PASS. FR-8 and AC-7 name the exact path `.delivery/artifacts/02-refine/po/constraints.yml`, author stage (Design), gate stage (UAT via FR-7), and P0 priority. No DoD before dogfood — the memory lesson holds.
6. **Rollback/regression protocol for Plan metric.** PASS. R-4 mitigation: threshold (<57%), window (any 3-run), switch (`experimental.constraints_model: false`), disposition (reopen BACKLOG-001 as REJECT). All four moving parts named.
7. **No "should"/"approximately" hiding in ACs.** PASS. Scanned §5 Acceptance Criteria — zero "should", zero "approximately", zero "~". The ACs stand on verbs like "exists", "returns", "cites", "include", "passes".
8. **A/B confounds acknowledged.** PASS. Metrics baseline §6 names the gate-patterns-injection confound explicitly and counsels BACKLOG-001 spike flag as the only clean read. NFR-4 provides the `experimental.constraints_model: true` flag that makes the A/B mechanically possible. Small-n caveat also logged.

## Non-Blocking Observations (route to Design)

- AC-8 token-delta baseline (prior 5-run Refine average) is not snapshotted in metrics-baseline.md §1. Capture before the flag flips.
- Banned-token pre-feature grep over the last 5 Architect artifacts (baseline §6 caveat) must run before Stage 4 so AC-3's "zero" has a truthful pre-state.
- Token enumeration diverges slightly across FR-3/NFR-2 (includes `kafka`) vs baseline §5.2 (adds `javascript`, `rust`, `nodejs`). Canonicalize in `constraints-model-guide.md` — FR-1 correctly defers the single source there.

## Defect Ledger

Zero defects logged this gate. Eight arrows, eight marks struck.

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/02-refine/dod/qa-review.md
SUMMARY: Eight arrows, eight orcs. Every AC testable, window stated, rollback armed, confounds named. That bug still only counts as one — and today there are none.
```
