# ADR-002 — Judge Persona Synthesis Protocol

**Status:** Accepted
**Date:** 2026-04-08
**Stage:** 4 Architect (light)
**Forged by:** Celebrimbor

## Context

PRD FR-4 requires a judge persona that synthesizes N reviewer outputs into a single verdict (`PASS | CONDITIONAL | BLOCK`). The risk (PRD R2) is a judge that merely averages rather than synthesizes — an echo chamber dressed in robes. We must define how the judge loads inputs, handles conflict, and fails safely when reviewers deadlock.

## Decision

The judge (default `chief-architect`) follows a **cite-synthesize-verdict** protocol:

1. **Load.** Orchestrator passes N file paths to the judge sub-agent. Judge reads `.delivery/artifacts/04-architect/board/<persona-id>-review.md` for each. No reviewer content is inlined into the prompt (NFR-3 isolation).
2. **Cite per finding.** Judge enumerates every finding from every reviewer, citing the source persona-id and the finding's `gate-criteria` line.
3. **Declare alignment.** For each finding the judge explicitly marks `AGREE`, `DISAGREE`, or `DEFER` with a one-line reason.
4. **Synthesize.** Judge produces `synthesized_findings[]` (merged, deduplicated, priority-ordered) and `dissent[]` (findings where personas conflict irreconcilably).
5. **Emit verdict.** Schema:
   ```
   VERDICT: PASS | CONDITIONAL | BLOCK
   SYNTHESIZED_FINDINGS: - <bullet>
   DISSENT: - <bullet or none>
   CITATIONS: - <persona-id> -> <finding>
   ```
6. **Persist.** Write to `.delivery/artifacts/04-architect/board/judge-verdict.md`.

### Deadlock Fallback

If `dissent[]` is non-empty **and** the orchestrator has already exhausted `max_iterations`, the judge emits `VERDICT: BLOCK` with reason `DEADLOCK` and the orchestrator escalates via the existing debate pattern's DEADLOCK handler in `delivery-team/skills/delivery-flow/references/team-patterns.md` (Pattern 4 Debate). No new deadlock mechanism is invented.

## Alternatives Considered

### A1 — Majority vote

Simple count of PASS/BLOCK verdicts, no synthesis. **Rejected:** a majority of reviewers missing a single critical risk still ships a broken design; ignores the richness of per-persona findings; invites R2 echo chamber directly.

### A2 — Weighted synthesis (per-persona weights)

Each reviewer carries a configured weight; judge multiplies. **Rejected:** weights are politics disguised as math; who decides weights? Adds a config field with no principled calibration. Violates the dogfooding ethos — we would be making up numbers.

## Consequences

**Positive**
- Forces the judge to *cite* each finding individually, directly mitigating R2 (judge echo chamber).
- Deadlock path reuses an existing, tested mechanism rather than inventing a new one (minimizes surface area).
- Verdict schema is machine-parseable for future DoD integration.

**Negative**
- Judge prompt is longer than a pure-vote prompt → small token cost (within NFR-1 25% ceiling given `max_reviewers ≤ 6`).
- Requires the debate pattern's DEADLOCK rule to remain stable; if that rule changes, ADR-002 must be revisited.

## Rationale

Synthesis-with-citation is the smallest protocol that prevents the echo chamber failure mode named in PRD R2, while deadlock-reuse keeps the blast radius LIGHT. Majority vote is cheaper but wrong; weighted vote is more complex and also wrong. Cite-synthesize-verdict is the only option that treats the reviewers as *voices* rather than *ballots*.

## References

- PRD: `.delivery/artifacts/02-refine/po/prd.md` FR-4, R2, NFR-1, NFR-3
- Existing deadlock handler: `delivery-team/skills/delivery-flow/references/team-patterns.md` Pattern 4 Debate
- Sibling: ADR-001 (config schema that names the judge)
