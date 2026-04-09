# Migration Roadmap — Claude-Plugins Marketplace

**Phase:** 3 Roadmap (Architect-led)
**Run:** US-8-dogfood-phase1b-2-3
**Date:** 2026-04-08
**Scribe:** Celebrimbor of Eregion

## Header

- **AS-IS path:** `.delivery/artifacts/08-transform/as-is-constraints.yml`
- **TO-BE path:** `.delivery/artifacts/08-transform/to-be-constraints.yml`
- **total_subsystems_in_as_is:** 19
- **total steps:** 5
- **Escape-valve justification:** n/a (3 ≤ M ≤ 7)

*Five anvils, struck in order. None strikes harder than the thirty-percent rule permits; none waits upon the next to justify its ringing. Each ring is its own music, and together they temper the Marketplace without melting it.*

---

## STEP-01: Transformation-planning capability lands

- **scope:** Closes diff rows: `entities.transformation_planning_task_type` (added); `actions.invoke_transformation_planning` (added). Touches AS-IS subsystems: `architect_skill`.
- **ordering_rationale:** dependency — every later step in this roadmap (and every future brownfield engagement across the Marketplace) consumes the transformation-planning task_type. It must exist before paradigm extraction or empirical measurement have an anvil to rest upon. This step already rang in run c4d1.
- **reversibility:** full — reference files and task_type are additive; removal is a `git revert` with zero persisted state.
- **risk:** low — additive refs in a single skill; no existing flows disturbed.
- **incremental_value:** Brownfield migrations become describable inside the Marketplace's own vocabulary. Gandalf's Phase 1A and Celebrimbor's Phase 1B/2/3 can be invoked by any future engagement without re-inventing the ritual.
- **preserved_invariants:**
  - "Two-channel communication: orchestrator signals and domain artifacts are separate"
  - "Context isolation: sub-agents receive only role-scoped references"
  - "Orchestrator does not produce domain artifacts itself"
- **estimated_subsystem_change_pct:** 5  (subsystems_touched=1 / total_subsystems_in_as_is=19) * 100

---

## STEP-02: Paradigm-as-skill MVP — volatility slice

- **scope:** Closes diff rows: `entities.paradigm_skill_registry` (added, minimal form); `entities.volatility_decomposition_skill` (added); `actions.select_decomposition_paradigm` (added in single-paradigm form). Touches AS-IS subsystems: `architect_skill`, `delivery_flow_orchestrator` (references only).
- **ordering_rationale:** risk-reduction — the volatility strategy is the highest-churn body of architect knowledge (HIGH volatility per AS-IS header). Isolating it into its own skill first de-risks the later DDD/functional extraction by proving the registration contract on the noisiest paradigm before quieter ones are touched.
- **reversibility:** partial — new skill directory is reversible; updated references in delivery-flow require a follow-up revert. Rollback cost: one commit.
- **risk:** medium — architect skill is load-bearing for every pipeline. Hazard: broken paradigm selection blocks Architect stage. Mitigation: registry defaults to embedded volatility logic until new skill proves itself over ≥3 pipeline runs.
- **incremental_value:** Volatility decomposition becomes independently testable and independently loadable — a Marketplace user picking the volatility paradigm no longer pays the context cost of the entire architect reference tree. Ships even if STEP-03 never happens.
- **preserved_invariants:**
  - "Context isolation: sub-agents receive only role-scoped references"
  - "DoD validation is multi-validator — ALL validators must say DONE"
  - "Orchestrator does not produce domain artifacts itself"
  - "constraints.yml primitive is used at every stage transition"
- **estimated_subsystem_change_pct:** 11  (subsystems_touched=2 / total_subsystems_in_as_is=19) * 100

---

## STEP-03: Paradigm-as-skill expansion — DDD + functional slices

- **scope:** Closes diff rows: `entities.ddd_decomposition_skill` (added); `entities.functional_decomposition_skill` (added); `actions.select_decomposition_paradigm` (completed for multi-paradigm selection). Touches AS-IS subsystems: `architect_skill`, `paradigm_skill_registry` (new, from STEP-02).
- **ordering_rationale:** dependency — requires the paradigm_skill_registry contract proven in STEP-02. Running these paradigms before STEP-02 would mean inventing a registry under two paradigms simultaneously, doubling the surface area of the first mistake.
- **reversibility:** full — each new skill is independently revertible; the registry from STEP-02 remains functional with only the volatility paradigm.
- **risk:** medium — two new paradigms simultaneously widen the testing surface. Hazard: cross-paradigm contamination (volatility language bleeding into DDD skill refs). Mitigation: forbidden-vocabulary check per skill at DoD.
- **incremental_value:** Architects can select the decomposition paradigm that matches the engagement — honest pluralism replaces implicit volatility-monopoly. Each new skill is independently shippable; if only DDD lands and functional does not, the Marketplace is still strictly better off.
- **preserved_invariants:**
  - "Context isolation: sub-agents receive only role-scoped references"
  - "DoD validation is multi-validator — ALL validators must say DONE"
  - "Self-correction loops are capped at 3 rounds before escalation"
  - "constraints.yml primitive is used at every stage transition"
- **estimated_subsystem_change_pct:** 16  (subsystems_touched=3 / total_subsystems_in_as_is=19) * 100

---

## STEP-04: Empirical measurement harness for architecture-board overhead

- **scope:** Closes diff rows: `entities.empirical_measurement_harness` (added); `actions.measure_plan_first_try_rate_empirically` (added); `numeric_ceilings.plan_first_try_pct: 80` (target bound introduced with measurement path). Touches AS-IS subsystems: `memory_system`, `architecture_board_pattern`.
- **ordering_rationale:** value-first — this step is value-positive without any preceding paradigm work. It can be sequenced earlier if STEP-02/03 slip; it is placed here only because architecture-board use will be exercised most heavily during paradigm work, giving richer measurement data.
- **reversibility:** full — config keys and memory-namespaced measurement logs are additive and removable.
- **risk:** low — measurement-only; no production behavior changes.
- **incremental_value:** The Marketplace stops guessing whether architecture-board is worth its token overhead. Real numbers from ≥3 pipelines replace folklore. Ships independently — the measurements are useful even if no later tuning happens.
- **preserved_invariants:**
  - "Two-channel communication: orchestrator signals and domain artifacts are separate"
  - "Retrospective is mandatory at Stop — enforced by hook"
- **estimated_subsystem_change_pct:** 11  (subsystems_touched=2 / total_subsystems_in_as_is=19) * 100

---

## STEP-05: Transformation-planning orchestrator wiring

- **scope:** Closes diff rows: `invariants."Every brownfield engagement runs transformation-planning before architecture"` (introduced — promoted from aspirational to enforced); `mandatory_artifacts.".delivery/artifacts/NN-transform/"` (enforced at orchestrator level). Touches AS-IS subsystems: `delivery_flow_orchestrator`, `architect_skill`.
- **ordering_rationale:** dependency — wiring the orchestrator dispatch is only safe after STEP-01 (task_type exists) AND after at least STEP-02 (at least one paradigm skill proves the registry). Wiring earlier would bind the orchestrator to a task_type whose paradigm tree still lives inside a single monolithic reference.
- **reversibility:** partial — orchestrator SKILL.md and pipeline-stages.md edits are revertible, but any engagement that has already produced `.delivery/artifacts/08-transform/` artifacts under the new convention will keep those artifacts; no data loss, but a directory drift.
- **risk:** medium — orchestrator is the single busiest subsystem; a misrouted dispatch blocks every pipeline. Mitigation: feature-flag gate the new routing, dogfood on Claude-Plugins itself for ≥2 runs before promotion.
- **incremental_value:** Brownfield engagements automatically enter transformation-planning instead of relying on human memory. The invariant moves from documentation to enforcement.
- **preserved_invariants:**
  - "Two-channel communication: orchestrator signals and domain artifacts are separate"
  - "Orchestrator does not produce domain artifacts itself"
  - "Light stages reduce depth but never skip execution"
  - "Retrospective is mandatory at Stop — enforced by hook"
- **estimated_subsystem_change_pct:** 11  (subsystems_touched=2 / total_subsystems_in_as_is=19) * 100

---

## No big-bang check (summary)

| step_id | subsystems_touched | total_subsystems_in_as_is | estimated_subsystem_change_pct | passes ≤ 30% |
|---|---|---|---|---|
| STEP-01 | 1 | 19 | 5  | yes |
| STEP-02 | 2 | 19 | 11 | yes |
| STEP-03 | 3 | 19 | 16 | yes |
| STEP-04 | 2 | 19 | 11 | yes |
| STEP-05 | 2 | 19 | 11 | yes |

**Max change:** 16% (STEP-03) — well under the 30% ceiling.

---

## Honest assessment

STEP-04 is the weakest link in sequencing rigor: its `ordering_rationale` is the soft "value-first" driver, and its placement between STEP-03 and STEP-05 is convenience, not necessity. It could legitimately run at any point in the sequence. I have not merged it with its neighbors because its value is genuinely independent — but reviewers should know the ordering here is loose, not load-bearing. If the team wants it earlier, move it. The 30% check still passes either way.

STEP-05's `reversibility: partial` is honest: once `.delivery/artifacts/08-transform/` becomes an enforced convention, engagements that have already written there carry the convention even after a revert. This is acceptable drift, not a blocker — but it is drift, and I will not pretend otherwise.

*Thus the roadmap. Five rings, each independently shippable, none exceeding the thirty-percent bound. The craft is honest, the ordering named, the invariants preserved. Strike when ready.* — Celebrimbor
