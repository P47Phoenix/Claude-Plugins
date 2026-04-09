# Retrospective — run-2026-04-08-b2c7

**Role:** Retro facilitator — *Aragorn* (king returning, looking back at the road)
**Scope:** Architecture Board capability build (BACKLOG-003 + -002)

## What Went Well

- **No-checkpoints mode** accelerated the pipeline dramatically — fewer context swaps, faster wave-to-wave cadence.
- **`constraints.yml` dogfood validated green on first use** — zero false positives, shape confirmed.
- **Architecture board dogfood caught 4 real gaps** the primary architect missed. The capability *proved itself inside its own build* — second instance of this meta-irony (first was a1f3). Self-validating capabilities are a pattern worth naming.
- Team DoD across Legolas/Sam/Bilbo/Gandalf converged cleanly on GO.

## What Didn't

- **US-1 hit API overload mid-wave** — retry succeeded, but wave pacing should account for provider turbulence.
- **US-7 shipped as simulation, not real dispatch** — dogfood artifacts hand-produced to the exact shape the design calls for; real orchestrator wiring deferred. Honest, but v1 doesn't yet exercise the code path end-to-end.

## Key Insight

The board's **CONDITIONAL verdict on its own architecture is a stronger success signal than PASS would have been.** A PASS from a brand-new reviewer looks like a rubber stamp. A CONDITIONAL with 4 specific, actionable catches proves the reviewers are doing real work. *Honesty is the feature.*

## Action Items

1. **Wire real orchestrator dispatch** for the board in a follow-up story (lift v1 simulation to v1.1 real).
2. **Measure token overhead** (NFR-1 baseline) across ≥3 real pipeline runs with and without the board.
3. **Address MAR rotation n ≤ 2 gap** in `architecture-board-personas.md` — add fallback guidance for small boards.

— *Aragorn*
