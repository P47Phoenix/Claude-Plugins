# Architect Stage — Memory

## Lessons Learned

- Architect-revision pattern converges cleanly in one round when reviewers ACCEPT with tactical findings. Stage 4 flow: QA ACCEPT + DevOps ACCEPT + Challenger confidence-4 with 3 priority findings → Architect rev 1 absorbing priorities + adding WI-14 → all 5 DoD validators DONE first round. Works reliably when findings are tactical, not structural. (validated: 1, last: run-2026-04-20-o4v7)

- ADR status must be binary (Proposed | Accepted | Deprecated). An ADR stamped "Accepted (contingent on an un-executed spike)" is a process smell — the status line is louder than the contingency clause, and readers greping for `Status: Accepted` will stop reading. Mark it Proposed until the contingency resolves. (validated: 1, last: run-2026-04-20-o4v7)

- Transformation-planning single-artifact is right for modest scope. The sub-workflow officially has 4 phase artifacts (AS-IS behavioral / AS-IS structural / TO-BE / Roadmap), but for a ≤ 10-plugin, ≤ 10k-LOC migration a single 500-700 line transformation-plan.md + 4-6 ADRs is more usable than 4 separate docs. The 4-doc split earns its cost on multi-team brownfield. (validated: 1, last: run-2026-04-20-o4v7)

- Adversarial review catches structural/framing defects that iterative authors miss. On Stage 4: ADR-006 contingent-acceptance, WI-06 measurement gap, ADR-005 missing worked example, WI-13 wave-placement inefficiency — all surfaced by a fresh-context Challenger reading end-to-end. Evaluator-Optimizer caught AC precision; Adversarial caught framing. Both are needed. (validated: 1, last: run-2026-04-20-o4v7)
