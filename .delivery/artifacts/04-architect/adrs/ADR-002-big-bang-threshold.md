# ADR-002: 30% subsystem change per roadmap step is the no-big-bang threshold

**Status:** Accepted
**Date:** 2026-04-08
**Deciders:** Celebrimbor (Architect)
**Related:** ADR-001, PRD FR-5, constraints.yml `max_subsystem_change_per_step_pct: 30`

## Context

A transformation roadmap that permits any single step to rewrite the whole system is not a roadmap — it is a big bang wearing a costume. The PRD (FR-5) and refine-stage constraints (`max_subsystem_change_per_step_pct: 30`) require a mechanical, auditable ceiling so that "iterative" is not a word the Architect may hand-wave. We must fix the threshold, define the measurement axis, and handle the edge case of very small AS-IS models where any single subsystem already exceeds a percentage-based rule.

## Decision

- **Threshold:** each roadmap step may touch at most **30%** of the subsystems enumerated in the AS-IS structural model (`as-is-constraints.yml` entities count).
- **Measurement:** `subsystems_touched / total_subsystems_in_as_is_model`. Mechanical, computed per step at authoring time and verified at review.
- **Edge case (total subsystems < 4):** the 30% rule would forbid touching even one subsystem (e.g. 1/3 = 33%). In that regime the threshold collapses to **"at most 1 subsystem per step."**
- **Escape valve:** if the AS-IS→TO-BE diff genuinely cannot be closed in ≤ 3 steps at 30%, up to 7 steps are permitted; >7 requires written justification in the roadmap header.

## Consequences

**Easier:**
- Reviewers apply a one-line test: count touched subsystems, divide, compare.
- Forces Architects to decompose ambitious transformations into shippable increments.
- Each step is small enough to be reversible and independently valuable.

**Harder:**
- Small systems (2–3 subsystems) have almost no room to maneuver — any cross-cutting change forces many steps.
- Percentage axis ignores step *depth* (a 10% touch may be more invasive than a 30% touch) — mitigated by the `scope` and `risk` fields in the step schema, not by the threshold itself.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|---|---|---|---|
| **20% threshold** | More conservative; tinier increments | Too punishing for small systems (any touch is ≥ 25% at 4 subsystems); forces absurd step counts | Wrong tradeoff for typical plugin-sized AS-IS models |
| **50% threshold** | Flexible; fewer steps | A single step can rewrite half the system — that is a big bang with extra syllables | Defeats the "no big-bang" invariant |
| **Line-count threshold (e.g. max N lines changed per step)** | Directly measures implementation cost | Wrong axis — roadmap operates on subsystems/modules, not lines; impossible to estimate before the step is implemented | Measurement axis mismatch with the roadmap abstraction |
| **No threshold; rely on reviewer judgment** | Maximum flexibility | Non-auditable; "iterative" becomes vibes; defeats the whole PRD FR-5 invariant | PRD explicitly requires a mechanical ceiling |
| **Tiered threshold by system size** | Scales with context | Complexity cost exceeds benefit; the <4 subsystem edge case is the only genuinely different regime | Edge case handled more simply by the "1 subsystem per step" collapse |

## Rationale

30% is the smallest ceiling that still permits a real roadmap on typical plugin-sized AS-IS models (4–10 subsystems), and large enough to be achievable without absurd decomposition. The edge-case collapse to "1 subsystem per step" under 4 total subsystems preserves the no-big-bang invariant without producing division-by-small-numbers nonsense. The escape valve to 7 steps (beyond which written justification is required) honors the PRD's ≥ 3 step minimum while acknowledging that genuinely large transformations may need more breathing room than the default suggests.
