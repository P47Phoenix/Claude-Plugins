# Transformation Phase 3 — Migration Roadmap (Architect-led)

*Part of `transformation-planning` task_type. Phase 3 of 4. Final phase.*

## 1. Purpose

Architect-led derivation of an **iterative migration roadmap** bridging the AS-IS structural model to the TO-BE structural model. The roadmap is an ordered sequence of independently-shippable steps; each step closes a named row of the AS-IS→TO-BE diff, preserves stated invariants, and can be reasoned about in isolation. No roadmap = no migration; only a wish.

## 2. Input

- **`.delivery/artifacts/08-transform/as-is-constraints.yml`** — Phase 1B authoritative starting state.
- **`.delivery/artifacts/08-transform/to-be-constraints.yml`** — Phase 2 authoritative target state.
- The mechanical diff of the two (§7 in `architecture.md`) — the migration surface area.

Both files MUST exist and MUST pass `validate_constraints.py` before Phase 3 begins.

## 3. Roadmap step schema (verbatim)

Every roadmap step carries **exactly** these eight fields (from `architecture.md` §6):

- `step_id` — stable identifier (e.g., `STEP-01`)
- `scope` — which AS-IS→TO-BE diff rows this step closes (entities added/removed/split/merged, invariants introduced/relaxed, actions re-homed)
- `ordering_rationale` — WHY this step comes where it does in the sequence (see §6)
- `reversibility` — can this step be rolled back without data loss? (`full` | `partial` | `none` + explanation)
- `risk` — blast radius if the step fails in production (`low` | `medium` | `high` + named hazard)
- `incremental_value` — the value delivered at the moment this step ships, independent of every later step
- `preserved_invariants` — which AS-IS invariants MUST continue to hold during and after this step (see §7)
- `estimated_subsystem_change_pct` — mechanical number per §4

Deviation from this schema is a DoD fail.

## 4. The "no big-bang" check

Per **ADR-002** (30% rule), no single roadmap step may change more than 30% of the AS-IS subsystems. This is mechanical and auditable.

**Formula (exact):**

```
estimated_subsystem_change_pct = (subsystems_touched_by_step / total_subsystems_in_as_is) * 100
```

Where `total_subsystems_in_as_is` = count of top-level entries in `as-is-constraints.yml` `entities`.

**Threshold:** `estimated_subsystem_change_pct ≤ 30`. Any step exceeding 30% MUST be split.

**Edge case — AS-IS has fewer than 4 subsystems:** the 30% rule degenerates (1/3 = 33%, already failing). In that regime the threshold collapses to **"at most 1 subsystem per step."** Reviewers count, not divide.

**Escape valve:** if the full AS-IS→TO-BE diff cannot be closed in ≤ 3 steps at 30%, up to 7 steps are permitted without justification; > 7 steps requires a written justification block in the roadmap header.

The check is applied at authoring time AND re-applied at Team DoD review. Both must pass.

## 5. Independently-shippable rule

Every step MUST be **value-positive on its own the moment it ships**. No step may rely on a future step to justify its existence.

- If `STEP-03`'s only `incremental_value` is "prepares the ground for STEP-04," then STEP-03 and STEP-04 must be **merged**, or STEP-03 must be **re-scoped** to deliver standalone value (e.g., ship STEP-03 behind a feature flag that delivers observability even before STEP-04 flips it on).
- Reviewers apply a blunt test: **"if we stopped the migration at this step and never did the next one, would the world be better than before?"** If the answer is no, the step is not independently shippable.
- Scaffolding-only steps (new empty module, new empty table, new empty queue) fail this test. Scaffolding rides inside the first step that uses it.

## 6. Ordering rationale

Each step's `ordering_rationale` field states **WHY it comes before the next step** in terms of one of these four drivers (pick the dominant one, name it):

- **Dependency** — step N produces an entity/invariant step N+1 consumes.
- **Risk-reduction** — step N de-risks a later step by isolating a volatile component early.
- **Value-first** — step N delivers the highest-leverage business outcome earliest (value is scheduled, not discovered).
- **Reversibility-first** — reversible steps run before irreversible ones so rollback remains cheap as long as possible.

Volatility-driven sequencing is the default: **least-volatile foundations first**, most-volatile components last so churn does not propagate downward. Deviation from volatility-first ordering must be explicitly named in `ordering_rationale`.

## 7. Preserved invariants

Each step names **which AS-IS invariants MUST continue to hold during AND after the step**. This is the production-safety contract.

- Invariants are copied (not paraphrased) from `as-is-constraints.yml`.
- Every AS-IS invariant not listed in a step's `preserved_invariants` is implicitly suspended for that step — this MUST be deliberate and noted.
- The union of all `preserved_invariants` across all steps must cover every invariant that appears in BOTH AS-IS and TO-BE. An invariant that survives the migration cannot go un-preserved in any single step.
- Invariants being **introduced** by the migration (TO-BE-only) are not listed in `preserved_invariants`; they appear in `scope` of the step that introduces them.

## 8. Minimum bar

- **≥ 3 steps**, unless the migration is genuinely single-step (extremely rare — requires written justification in roadmap header).
- Each step conforms to §3 schema, §4 check, §5 rule, §6 rationale, §7 invariants.
- Roadmap header records: AS-IS path, TO-BE path, `total_subsystems_in_as_is`, total step count, and any §4 escape-valve justification.

## 9. Output

Canonical path: **`.delivery/artifacts/08-transform/roadmap.md`**

Uses `delivery-team/skills/delivery-flow/references/templates/transformation-roadmap-template.md` as its shape. Closing "No big-bang check" table reproduces each step's `estimated_subsystem_change_pct` for one-pass reviewer audit.

## 10. Anti-patterns

- **Big-bang disguised as phases.** Three "phases" where phase 1 is "rewrite everything" and phases 2 and 3 are "polish." The 30% check catches this mechanically.
- **Dependency-only steps.** Steps whose only purpose is to enable the next step. Fails §5; merge or re-scope.
- **Wish-list roadmaps without invariants.** Steps that describe the destination but never name what must stay true en route. Production safety disappears.
- **Single-step "roadmaps."** A roadmap of one step is a big bang, even if it is called iterative.
- **Unnamed ordering rationale.** "Because it makes sense" is not an ordering rationale. Name the driver from §6.
- **Invariant laundering.** Quietly dropping an AS-IS invariant from `preserved_invariants` in every step without declaring it relaxed. Every omission must be deliberate.
- **Platform choices smuggled into `scope`.** Roadmap steps may name platforms (that is Phase 3's job), but `scope` must still be expressed in terms of AS-IS→TO-BE diff closure, not in terms of "adopt Foo."
