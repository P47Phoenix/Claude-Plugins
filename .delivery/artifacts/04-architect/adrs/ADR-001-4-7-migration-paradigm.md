# ADR-001 — 4.7 Migration Paradigm: Keystone-First Rolling Sweep

**Status:** Accepted
**Date:** 2026-04-20
**Architect:** Celebrimbor
**Engagement:** Opus 4.6 → 4.7 Transformation Plan
**Related:** PRD REQ-01, REQ-02, REQ-03, REQ-03B; Open Question 1
**Supersedes:** none
**Superseded-by:** none

---

## Context

The PRD's Open Question 1 asks: is this a single big-bang PR or a per-plugin rolling sequence? Evidence from Sections 3.1 and 3.7 of the PRD:

- Model-ID sweep touches 2 files (`agentic-flow-builder/scripts/agent_registry.py`, `prd-quality-gate-flow/stage_definitions.py`) and exactly 10 lines.
- Keystone prose audit touches 6 SKILL.md files totaling 4,516 LOC.
- `delivery-flow/SKILL.md` carries the sub-agent dispatch contract (DISP-01/02/03) — a behavioural keystone, not a text keystone.
- `research-agent/SKILL.md` carries a grep-invisible tool-use regression risk (F-07).
- Past memory lesson (`feedback_dogfooding.md`): changes must be validated by using them, not merely read. Dogfood-before-ship is a binding user preference.

A big-bang PR containing all six keystone edits plus the two Python-script sweeps fails the dogfood rule on two counts: (a) the resulting PR is too large to meaningfully dogfood as a single unit before merge, and (b) a regression in any one keystone would require reverting the whole bundle.

Per-plugin rolling is the default shape in this repo (see memory `feedback_dogfooding.md` and `feedback_no_skip_stages.md`). But "per-plugin" is too fine a grain here: four of the six keystones live in `delivery-team/` and share the orchestrator contract. Pairing by similarity — a past dev-run memory lesson — applies.

## Decision

Adopt a **keystone-first, rolling, pair-wise sweep** sequenced into four waves:

1. **Wave 1 (Foundational):** REQ-09 AS-IS validator-dispatch count capture + REQ-10 4.7 baseline capture. No code edits. Unblocks all delta metrics.
2. **Wave 2 (Keystones — behavioural):** `delivery-flow/SKILL.md` annotation (REQ-03) paired with `research-agent/SKILL.md` dogfood probe (REQ-03B). Both implicate sub-agent/tool-use behaviour on 4.7.
3. **Wave 3 (Keystones — prose):** Four prose-read/annotate edits paired by blast radius: (a) `prompt-engineer/SKILL.md` + `product-delivery/SKILL.md` (author-facing teaching surfaces); (b) `architect/SKILL.md` + `mtg-commander/SKILL.md` (long instruction surfaces, tone-risk-relevant).
4. **Wave 4 (Drift hygiene & enhancements):** REQ-01 model-ID sweep + REQ-04 adversarial validation + REQ-05 alias-tone dogfood + REQ-06 (optional) over-pressure audit + REQ-07 new-backlog registration.

Each wave has an entry gate (prior wave DONE) and an exit gate (dogfood validation per PRD REQ-08). Waves 2 and 3 parallelise internally (the pairs are independent file edits); waves are sequential.

Big-bang was rejected. Strict per-plugin rolling was rejected (too granular; misses the pairing efficiency).

## Consequences

- **Positive:** Each wave is independently dogfoodable; a regression confines rollback to one wave. Pairing by similarity cuts review time. Wave 1 creates the baseline all subsequent metrics reference, closing the "regress against what?" gap.
- **Positive:** REQ-07 (NEW features) stay out of the critical path; they only register in Wave 4 as backlog entries, not absorbed into migration scope.
- **Negative:** Four waves means four dogfood checkpoints. That is the cost of the dogfood-before-ship rule; the user memory treats this cost as non-negotiable.
- **Negative:** Wave 2's pairing implies two keystones dogfooded in the same run. If both regress simultaneously, root-cause is harder. Mitigation: Wave 2 dogfood runs dispatch the two skills from separate invocations, not a fused run.

## Alternatives Considered

- **A. Big-bang single PR.** Rejected: violates dogfood-before-ship (one merge, one rollback boundary, one blast radius).
- **B. Strict per-plugin rolling (6 waves for 6 keystones + 2 for sweeps).** Rejected: ignores the pairing-by-similarity memory lesson; inflates review overhead without proportional safety gain.
- **C. Model-ID-first (REQ-01 before anything else).** Rejected by PRD AC-01.2 / Section 3.1.1 — MID-03 is drift hygiene, not retirement urgency. Sequencing it first on urgency grounds is a false premise.
- **D. Research-agent-first (fix F-07 regression risk before all else).** Rejected: research-agent regression is probabilistic (F-07 says "fewer tool calls by default," not "no tool calls"). REQ-03B's dogfood probe in Wave 2 catches it; a pre-emptive prose edit in Wave 1 would bypass the "don't edit until you observe" rule (PRD REQ-04 AC-04.3 precedent).

## Implementation Notes

- Wave boundaries map 1:1 to the Section 6 Roadmap of the transformation plan.
- Dogfood gates per wave use `delivery-team:user-feedback` (Wave 2, 3, 4) and `delivery-team:delivery-flow` full runs (Wave 1 baseline).
- Rollback per wave: `git revert` the wave's commit(s); the baseline capture in Wave 1 is the reference state for all regression comparisons.

---

*"Forge the keystones first. Set the mortar. Then raise the arch. A ring is not made all at once — it is made in stages, each tested before the next is begun."*

— Celebrimbor
