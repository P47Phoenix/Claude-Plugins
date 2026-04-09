# Risk Architect Review — architecture.md

STATUS: BLOCK
FINDINGS: .delivery/artifacts/04-architect/board/risk-architect-review.md
SUMMARY: MAR rotation underspecified for n=2; malformed judge persona has no rollback path; token-cost ceiling is documented but not enforced.

## Gate 1 — Explicit failure modes per boundary
- **Judge echo chamber** — acknowledged in §9 (architecture.md:85) but mitigation is "deferred". Not acceptable at enabled=true time. BLOCK.
- **Malformed judge persona file** — no failure mode listed. If `## chief-architect (judge)` section is missing or malformed, §5 step 4 (architecture.md:63) silently fails. No error path, no fallback.
- **Malformed reviewer persona** — personas file says "unknown ids fail the config validator" but architecture.md does not reference the validator. Gap between spec and implementation contract.
- **Iteration loop non-termination** — §5 step 5 (architecture.md:64) loops on convergence; if `convergence: all-done` and one reviewer is flaky, loop runs to `max_iterations` every time. Cost cliff, not a bug, but document it.

## Gate 2 — Blast radius per failure mode
- Not named. Implicit: persona failure scopes to a single Stage 4 run (good — bounded). Judge failure blocks Stage 4 entirely (bad — name it).

## Gate 3 — Single points of failure
- **The judge is a SPOF by design.** §4 (architecture.md:52-54) has one judge persona, one file section, one synthesis protocol. If the judge persona file section is corrupted, the entire board is down. No fallback judge. Argue it or mitigate it.
- **MAR rotation with n=2 reviewers** — §7 (architecture.md:72-74) says "round-robin, skipping the round-1 reviewer whose BLOCK triggered correction". With exactly 2 reviewers, skipping one leaves one. With exactly 1 reviewer (config allows it — ceiling is ≤6, no floor), rotation is undefined. **DEADLOCK at n≤2 is unhandled.** BLOCK.

## Gate 4 — Rollback paths
- Default-disabled (NFR-2, architecture.md:11) gives zero blast radius on existing pipelines. Good. This is the one true rollback: `enabled: false` reverts instantly. Call it out explicitly as the rollback strategy.

## Recommendation
BLOCK. Must-fix: (a) MAR rotation floor (reviewers >= 2 enforced, or explicit n=1/n=2 behavior), (b) malformed judge fallback, (c) echo-chamber mitigation cannot be "deferred" for an enabled feature.
