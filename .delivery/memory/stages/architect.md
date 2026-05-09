# Architect Stage — Memory

## Lessons Learned

- Architect-revision pattern converges cleanly in one round when reviewers ACCEPT with tactical findings. Stage 4 flow: QA ACCEPT + DevOps ACCEPT + Challenger confidence-4 with 3 priority findings → Architect rev 1 absorbing priorities + adding WI-14 → all 5 DoD validators DONE first round. Works reliably when findings are tactical, not structural. (validated: 1, last: run-2026-04-20-o4v7)

- ADR status must be binary (Proposed | Accepted | Deprecated). An ADR stamped "Accepted (contingent on an un-executed spike)" is a process smell — the status line is louder than the contingency clause, and readers greping for `Status: Accepted` will stop reading. Mark it Proposed until the contingency resolves. (validated: 1, last: run-2026-04-20-o4v7)

- Transformation-planning single-artifact is right for modest scope. The sub-workflow officially has 4 phase artifacts (AS-IS behavioral / AS-IS structural / TO-BE / Roadmap), but for a ≤ 10-plugin, ≤ 10k-LOC migration a single 500-700 line transformation-plan.md + 4-6 ADRs is more usable than 4 separate docs. The 4-doc split earns its cost on multi-team brownfield. (validated: 1, last: run-2026-04-20-o4v7)

- Adversarial review catches structural/framing defects that iterative authors miss. On Stage 4: ADR-006 contingent-acceptance, WI-06 measurement gap, ADR-005 missing worked example, WI-13 wave-placement inefficiency — all surfaced by a fresh-context Challenger reading end-to-end. Evaluator-Optimizer caught AC precision; Adversarial caught framing. Both are needed. (validated: 1, last: run-2026-04-20-o4v7)

- **Architect batching constraints MUST simulate end-state numerically.** When an ADR claims that batching multiple WIs together resolves a budget/limit violation, the ADR MUST include explicit math: `before → +Δ_w1 → -Δ_w2 → after, with after ≤ budget`. ADR-tk1-002 in run-2026-05-04-tk1 declared W1-7 (-1 line) + W1-4 (+1 line) batching would resolve alias-creator's Tier-C overage, but the math actually closes at 201 (still over 200) — Stage 5 Dev DoD caught it via runs-the-command discipline. The corrected math required W1-7 to trim 2 lines, not 1. Add as Architect DoD gate: any batching-resolves-budget claim MUST show explicit additive math in the ADR's Decision section. (validated: 1, last: run-2026-05-04-tk1)

- **Cache-prefix-impacting ADRs MUST have Dev runs-the-command at DoD.** ADR Element 5 (re-freeze procedure) is byte-arithmetic-dense; even seasoned architect roles can invert boundary measurements. At run-2026-05-05-tk3, the architect cited Phase 0 starting at byte 3603 (actual: 1803, Δ=1794, INVERTING the cache-warmup-prefix conclusion). Dev DoD's runs-the-command discipline caught it. Action: cache-prefix-impacting ADRs MUST list the Dev runs-the-command validator in their DoD configuration. (validated: 1, last: run-2026-05-05-tk3)

- **Architect ADR projection MUST pre-emptively check AT-CAP files for downstream rollouts.** Wave 3 Architect projected godot 236→198 (target ≤200) but missed Story-5 mandatory frontmatter rollout would push 198+3=201. QA caught at Stage 4 R1; Architect R2 deepened godot trim to 197. Pattern: any ADR adding lines to ALL files MUST verify each at-cap file has ≥(rollout-Δ) headroom. (validated: 1, last: run-2026-05-09-tk4)
