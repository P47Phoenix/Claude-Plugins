# Migration Roadmap — <system-name>

**Phase:** 3 Roadmap (Architect-led)
**Run:** <run-id>
**Date:** <YYYY-MM-DD>

## Header

- **AS-IS path:** `.delivery/artifacts/08-transform/as-is-constraints.yml`
- **TO-BE path:** `.delivery/artifacts/08-transform/to-be-constraints.yml`
- **total_subsystems_in_as_is:** <N>
- **total steps:** <M>
- **Escape-valve justification (only if M > 7 or M == 1):** <n/a or written justification>

---

## STEP-<NN>: <short name>

- **scope:** <which AS-IS→TO-BE diff rows this step closes>
- **ordering_rationale:** <driver from §6 (dependency | risk-reduction | value-first | reversibility-first) + why>
- **reversibility:** <full | partial | none> — <explanation>
- **risk:** <low | medium | high> — <named hazard + blast radius>
- **incremental_value:** <value the moment this step ships, independent of later steps>
- **preserved_invariants:**
  - <invariant copied verbatim from as-is-constraints.yml>
  - <invariant copied verbatim from as-is-constraints.yml>
- **estimated_subsystem_change_pct:** <N>  (subsystems_touched=<k> / total_subsystems_in_as_is=<N>) * 100

---

<!-- Repeat H2 block per step. Minimum 3 steps per FR-5. -->

---

## No big-bang check (summary)

| step_id | subsystems_touched | total_subsystems_in_as_is | estimated_subsystem_change_pct | passes ≤ 30% |
|---|---|---|---|---|
| STEP-01 | <k> | <N> | <pct> | yes/no |
| STEP-02 | <k> | <N> | <pct> | yes/no |
| STEP-03 | <k> | <N> | <pct> | yes/no |

**Edge case note:** if `total_subsystems_in_as_is < 4`, the 30% rule collapses to "at most 1 subsystem per step" per ADR-002. Record that explicitly in the table header.

---

## Example (fully populated step)

## STEP-01: Extract pricing policy from monolithic order service

- **scope:** Closes diff rows: `entities.pricing-policy-engine` (added), `actions.calculate_order_total` (re-homed from `order-service` to `pricing-policy-engine`). Touches AS-IS subsystems: `order-service`.
- **ordering_rationale:** risk-reduction — pricing logic is the highest-volatility component per the AS-IS `state_variables` classification; isolating it first prevents churn from propagating into the stable order-persistence layer during later steps.
- **reversibility:** full — new engine runs alongside legacy path behind a feature flag; flip reverts instantly with zero data migration.
- **risk:** medium — incorrect pricing directly affects revenue; hazard mitigated by parallel-run shadow comparison for 7 days before cutover.
- **incremental_value:** Pricing rule changes ship in minutes instead of full order-service redeploys; shadow comparison exposes 3 latent rounding bugs already observed in production incidents INC-0412 and INC-0418.
- **preserved_invariants:**
  - "Order total always equals sum of line items plus tax minus discounts, to the cent."
  - "No order may be persisted with a negative total."
- **estimated_subsystem_change_pct:** 14  (subsystems_touched=1 / total_subsystems_in_as_is=7) * 100
