# ADR-003: Isolated Adversarial Loop Convergence Criteria

**Status**: Accepted (LIGHT Architect stage)
**Date**: 2026-04-05
**Architect**: Celebrimbor
**Related**: PRD FR-13, FR-14, FR-15, R3, C4

---

## Context

Issue #69 introduces the Isolated Adversarial Loop pattern for the Architect stage: each reviewer loop is a fresh sub-agent with no context from prior loops, so that deeper structural issues are surfaced instead of anchored away by the first critique.

C4 raised a sharp objection: fresh-context reviewers produce **non-monotonic** critique sets. A single clean loop is no proof of convergence — the next fresh reviewer, having no memory of what was fixed, may surface an entirely disjoint set of issues. "Zero findings in the current loop" is therefore insufficient as a termination criterion. Without a stronger rule, `max_self_correction` becomes the *normal* exit path and "adversarially clean" becomes vanishingly rare.

Four termination strategies were considered:

- **A. One-clean**: exit on first zero-finding loop. (Original naive FR-13.) Rejected by C4.
- **B. Two-clean**: exit only after two *consecutive* zero-finding loops. Guards against lucky single passes.
- **C. Severity threshold**: exit when all findings are below a configured severity. Requires reviewer severity tagging and a threshold policy.
- **D. No-new-issue-classes**: exit when consecutive loops produce findings, but no new issue *class* has appeared for N loops. Requires a taxonomy.
- **E. Hard cap**: exit at `max_self_correction`. Cannot be the only rule — then "cap_reached" is the normal state.

## Decision

Terminate the loop when ANY of the following holds:

1. **Two-clean rule** (B): Two *consecutive* loops return zero findings. Exit `converged (two_clean)`.
2. **No-new-classes rule** (D): Two *consecutive* loops produce findings, but every finding in each belongs to an issue class raised in an earlier loop. Exit `converged (class_saturated)`. Residuals documented.
3. **Hard cap** (E): `N >= max_self_correction` (default 3). Exit `cap_reached`. Residuals documented and surfaced to human checkpoint.

**Issue class taxonomy** (declared in `team-patterns.md`, enforced on reviewer output):

```
coupling | security | data-integrity | naming | testability | performance | docs
```

Untagged or invalid-tag findings are bucketed as `misc` and counted as a new class (conservative — prevents taxonomy evasion).

**Loop protocol invariants**:

- Every reviewer dispatch is a fresh sub-agent whose prompt contains **only** the current artifact and the reviewer brief + taxonomy. No prior findings, no "this is loop N", no fix summaries.
- The Architect revision sub-agent sees the **current loop's** findings only — not prior loops — to prevent compound patching against contradictory priorities.
- A clean pass at N=1 with no prior clean loop does NOT exit. It re-runs the reviewer on the same artifact to seek the second consecutive clean.
- `cap_reached` is a **documented exit**, not a failure. The human checkpoint decides whether residuals are acceptable or require manual remediation.

Pseudocode lives in the architecture document §4.3.

## Alternatives considered

- **A (one-clean)**: Rejected per C4. A single fresh reviewer's clean pass proves nothing about a non-monotonic critique stream.
- **C (severity threshold)**: Rejected for this stage. Requires reviewers to assign severities on a shared scale, which is harder to enforce consistently than a class taxonomy. The taxonomy already captures "have we seen this kind of concern before?" which is what class saturation measures. Severity can be added in a future iteration if the taxonomy proves insufficient.
- **E alone**: Rejected. Makes cap the normal exit and defeats the purpose of adversarial review.
- **B alone**: Rejected. Without the class-saturation rule, a reviewer stream that never fully cleans (but only raises already-known classes) would run to the cap even though it has converged in substance.
- **Three-clean (stricter B)**: Rejected as excessive given default cap of 3 — three-clean would require a cap of at least 4 to be reachable, changing the default config behavior.

## Consequences

**Positive**
- Convergence is now provable by repetition OR by class saturation, not merely hoped for.
- Cap-reached remains bounded (default 3) so latency is predictable.
- Reviewer context isolation is preserved — the whole point of the pattern.
- Residuals are always documented, making cap-reached a navigable state for the human checkpoint.
- Taxonomy gives reviewers a shared vocabulary and makes "already raised" a decidable question.

**Negative**
- A reviewer who invents new class-ish labels can defeat class saturation. Mitigated by the fixed taxonomy and `misc` bucket.
- With the default `max_self_correction: 3`, the two-clean rule requires loops 2 and 3 to both be clean — leaving only one loop of actual fixing before the cap. For complex architectures this may frequently hit cap_reached. This is acceptable because cap_reached is a documented exit, not a failure, and the default can be tuned per-repo.
- Adds protocol complexity to `team-patterns.md` — reviewers must understand the taxonomy and tag their findings.

**Mitigation**
- Taxonomy is short, fixed, and documented with one-line examples per class.
- `max_self_correction` default stays at 3 (no default change this bundle), but Design stage may recommend raising it to 4 or 5 for repos that show frequent cap_reached exits.
- Dogfood run's Architect stage MUST demonstrate at least one full loop iteration to validate the protocol end-to-end (resolves OQ-5 in the direction of "at least one loop, cap is informational").

## Compliance

- FR-13: satisfied (protocol, three convergence rules, taxonomy, no-context-leak guarantee all specified).
- FR-14: satisfied (Stage 4 references this pattern).
- FR-15: satisfied (`max_self_correction` reused, default 3).
- R3 (non-convergence): mitigated by two-clean + class saturation.
- C4 (single clean is insufficient): resolved.

---

*"A blade is not proven by a single strike. Strike it twice in the same place, or strike it against every stone on the mountain until no new voice answers back. Only then is the work done."*

— Celebrimbor
