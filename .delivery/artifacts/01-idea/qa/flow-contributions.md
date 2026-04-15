# QA Flow Contributions — Stage 1 Brainstorm

> *Legolas of the Woodland Realm, bow strung: "A thousand arrows nocked cannot
> hide a single crack in the wall. Show me every seam — I will find what the
> mapmaker misses." The architect forges the city; I walk its walls at night.*

**Contributor:** Legolas (QA lens)
**Parallel lead:** Celebrimbor (Architect) — assumed to cover component map,
pipeline sequence, routing matrix, state machine, hook perimeter already.
**Scope:** gaps only a QA eye catches — validation lifecycle, gate routing,
traceability, test-type selection, validator locality.

---

## Proposal 1 — Empirical vs Analytical Validation Lifecycle

- **Title:** `empirical-validation-lifecycle.md`
- **Audience:** QA + Developer + Godot skill contributors; UAT owners.
- **Why it matters:** `CODE_COMPLETE` exists in `delivery-flow/SKILL.md` and
  `quality/SKILL.md` L270-311, but there is no single diagram showing how an AC
  is *classified* (analytical vs runtime-only), *tagged* at Dev, *carried* to
  UAT, and *closed* with user evidence. Today the knowledge is scattered across
  `empirical-validation.md`, the developer skill, and the UAT stage.
- **Diagram:** state machine (AC lifecycle: proposed → classified → code-complete-pending → empirically-validated → accepted) + swimlane (Developer / QA validator / UAT owner / User).
- **Complexity:** M.
- **Celebrimbor overlap:** Low. He will show the pipeline state machine; the AC-level lifecycle is a QA-owned refinement.

## Proposal 2 — Gate Failure and Self-Correction Routing

- **Title:** `dod-self-correction-routing.md`
- **Audience:** Orchestrator maintainers; anyone debugging a stuck stage.
- **Why it matters:** `SKILL.md` L516-534 states "ALL validators must return
  DONE" and aggregate NOT_DONE findings — but the *shape* of the round-trip is
  implicit: what fields each NOT_DONE finding must carry, how DONE findings are
  retained for context, whether the revision re-runs ALL validators (yes) or
  only the failed ones (no — regression risk), and the 3-round bound before
  dynamic escalation. Implicit contracts rot fastest.
- **Diagram:** sequence diagram (orchestrator ↔ N validators ↔ primary) with
  a decision node for round count, plus a small contract table for finding schema.
- **Complexity:** M.
- **Celebrimbor overlap:** Partial. He will mention the evaluator-optimizer
  pattern at the component level; the per-round wiring is QA's lens.

## Proposal 3 — Test Case Traceability Through the Pipeline

- **Title:** `test-traceability-matrix.md`
- **Audience:** PO, QA, UAT reviewers, auditors.
- **Why it matters:** FR → Story → AC → Test Case → Evidence is the spine of
  defensible delivery, yet nothing in `ARCHITECTURE.md` shows the matrix
  stitching Plan → Development → UAT. Coverage today is asserted, not proven.
- **Diagram:** flowchart (PRD FR nodes → AC nodes → Test Case nodes → Evidence
  nodes, with stage bands) plus a sample matrix table.
- **Complexity:** L. This one earns its keep — it is the artifact an auditor
  or an angry stakeholder will ask for first.
- **Celebrimbor overlap:** None expected. Architect rarely owns traceability.

## Proposal 4 — Test-Type Decision Tree for an AC

- **Title:** `test-type-decision-tree.md`
- **Audience:** Developer + QA validators choosing the right check.
- **Why it matters:** Given an AC, which verification applies — static grep,
  schema validation, unit test, runtime smoke, dogfood, longitudinal metric?
  Today this judgement lives in reviewers' heads; new contributors guess.
  Pairs naturally with `empirical-validation.md` but orthogonal to it.
- **Diagram:** decision tree (one page) + worked examples table.
- **Complexity:** S.
- **Celebrimbor overlap:** None. Test-type selection is QA craft.

## Proposal 5 — Per-Stage Validator Criteria Loading and Locality

- **Title:** `validator-criteria-locality.md`
- **Audience:** Orchestrator maintainers; hook authors; anyone adding a validator.
- **Why it matters:** `SKILL.md` L518-522 asserts each validator sees *only*
  the artifact path + its own criteria, never another validator's output. This
  locality boundary is load-bearing for parallel validation correctness, but is
  not diagrammed anywhere. Where exactly do criteria come from (quality-gates.md),
  how are they injected, and how do we prove a validator cannot leak context?
- **Diagram:** component diagram (criteria source → prompt builder → validator
  sandbox) + boundary annotation showing what each validator *cannot* see.
- **Complexity:** S-M.
- **Celebrimbor overlap:** Low. He will show the hook perimeter; criteria
  injection is an interior contract he is unlikely to draw.

---

## Honest Deferrals to Celebrimbor

- Component overview, 7-stage sequence, project-type routing, collaboration
  pattern catalogue, hook layer table — already strong in `ARCHITECTURE.md`.
  I will not re-forge what the smith has hammered true.

## Priority Ranking (QA judgement)

1. **#3 Traceability** — highest defensibility return.
2. **#1 Empirical Lifecycle** — closes the most dangerous documentation gap.
3. **#2 Self-Correction Routing** — unblocks debuggers fastest.
4. **#5 Validator Locality** — protects a load-bearing invariant.
5. **#4 Decision Tree** — smallest, highest leverage for new contributors.

*"That bug still only counts as one — but mark every one of them."*
