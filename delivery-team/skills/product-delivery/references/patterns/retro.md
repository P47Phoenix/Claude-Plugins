# Pattern: Retrospective

```
## Retrospective: [Sprint N]
**Format:** [format name]
**Date:** [date]
**Facilitator:** [name]
**Duration:** [time-boxed]

### Activity Results
[Format-specific content]

### Action Items
| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|

### Follow-Up from Previous Retro
[Status of prior action items]

### KPIs

#### context_tokens_per_pipeline_run

5-run rolling-mean of total Claude context tokens consumed across all Agent
dispatches in a single delivery-flow pipeline run. Surfaces token-economy
regressions before they accumulate over multiple waves.

| Field | Value |
|-------|-------|
| This run | [N tokens] |
| Rolling mean (last 5 runs) | [M tokens] |
| Δ vs prior 5-run window | [+/-X% — annotate >+10% as REGRESSION] |
| Source data | `.delivery/telemetry/skill-loads.jsonl` (per-dispatch rows) |
| Compute | `python3 scripts/compute_context_tokens.py --window 5 --run <run-id>` |
| Status | [PENDING — populated when W3-18 telemetry hardening lands] |

**Compute spec (for orchestrator at end-of-run)**:
1. Read `.delivery/telemetry/skill-loads.jsonl`; filter to rows where `run_id`
   matches the current pipeline run AND `placeholder != true` (W3-18 marker).
2. Sum the `context_tokens` field across all rows for the current run.
3. Read the prior 4 retro records under `.delivery/memory/archive/
   retrospective-run-*.md`; extract their `context_tokens_per_pipeline_run`
   "This run" values. Combined with the current run = 5-sample window.
4. Rolling mean = sum(5) / 5. Δ = (current - mean(prior_4)) / mean(prior_4).
5. Annotate Δ > +10% as REGRESSION (action item required); Δ < -10% as
   IMPROVEMENT (note the cause for replication).

**PENDING marker**: until W3-18 (telemetry hook output capture quality
hardening, Story 7) lands, the `context_tokens` field on per-dispatch rows
in `.delivery/telemetry/skill-loads.jsonl` is unreliable. Until then, leave
"This run" + "Rolling mean" cells as `PENDING (W3-18)` and skip Δ compute.
Once W3-18 ships, retroactively backfill the prior runs from
`.delivery/memory/archive/run-*.md` Agent-call counts × baseline estimate
to seed the 5-sample window.
```
