# PRD — Paired Constraints Primitive (`constraints.yml`)

**Feature**: Shared Model-First `constraints.yml` primitive across Refine & Architect stages
**Pipeline ID**: run-2026-04-08-a1f3
**Stage**: 2 (Refine) | **Role**: Product Owner (Gandalf)
**Date**: 2026-04-08
**Source backlog**: BACKLOG-001 (Refine spike) ∥ BACKLOG-004 (decomposition depth)
**Inputs**: `.delivery/artifacts/01-idea/po/idea-brief.md`, `.delivery/artifacts/research/architect-examine-decomposition-gaps.md`, `.delivery/artifacts/research/po-synthesis-model-first-mar.md`

> *"A product owner is never late, nor early. They prioritize precisely when they mean to."*

---

## 1. Problem

Four failure modes, one root. The burden is not vague; the stones of memory name it plainly.

- **Plan stage drifts at 57% first-try pass** — `.delivery/memory/stages/plan.md` records 3 of 7 runs reworked on constraints *already known at Refine time*. The knowledge existed; the structure to carry it did not.
- **The Golden Rule of volatility decomposition is unnamed.** `delivery-team/skills/architect/references/volatility-decomposition.md:7` speaks of "WHAT CHANGES" but never states Löwy's rule — *"decompose by volatility, not by functionality"* — as a rule. The anti-pattern at `volatility-decomposition.md:181` warns only of the layer-disguise variant, not the broader functional trap (evidence: `architect-examine-decomposition-gaps.md` Gap 1).
- **Implementation-detail contamination bleeds upward.** `volatility-decomposition.md:49-96` (Phases 1–4) and `strategic-ddd.md` Phases 1–4 contain no prohibition against naming cloud services, runtimes, or languages during decomposition (Gap 2). Architects name Lambda, ECR, SQS where only volatility classes and bounded contexts belong.
- **The Architect is absent from Stage 5 Plan.** `delivery-team/skills/delivery-flow/references/pipeline-stages.md:428-449` invokes PO, QA, Scrum Bag, DevOps — not the one who drew the map. `config-schema.md:57-63` keeps the Architect as a passive DoD validator only (Gap 3).

Four faces, one burden: **constraints known but not structured, and therefore not consumed.**

## 2. Users / Actors

Five who will be served — and held to — the primitive:

- **Orchestrator (delivery-flow)** — consumes `constraints.yml` at every gate to pre-load downstream stages with the burden they must carry.
- **Architect sub-agents** — produce decomposition constraints: volatility classifications, boundary invariants, forbidden vocabulary, Golden Rule citation.
- **PO sub-agents** — produce problem constraints at Refine: entities, state variables, actions, numeric ceilings, mandatory artifacts, invariants.
- **DoD validators** — perform deterministic rule checks against `constraints.yml` alongside prose review. Rule-based, not AI-inferred — the Business Rules Engine philosophy wins the day.
- **Human checkpoint reviewer** — reads `constraints.yml` as a terse, deterministic summary of what the stage has committed to, without spelunking the prose.

> *"Even the smallest validator can change the course of the pipeline."*

## 3. Functional Requirements

- **FR-1** `constraints.yml` schema — a single YAML document, ≤8 top-level fields: `entities`, `state_variables`, `actions`, `numeric_ceilings`, `mandatory_artifacts`, `invariants`, `forbidden_vocabulary`, `citations`. Each field typed; `entities` and `invariants` required, remainder optional. Schema documented in a new `delivery-team/skills/delivery-flow/references/constraints-model-guide.md`.
- **FR-2** Refine-stage domain template — PO template instantiating FR-1 with problem-scoped content: entities (domain nouns), state_variables (observable pipeline state), actions (PO-authored state transitions), numeric_ceilings (e.g., sprint ceiling, token budget), mandatory_artifacts (required downstream files), invariants (ADR-level truths).
- **FR-3** Architect-stage decomposition template — instantiates FR-1 with volatility/DDD-scoped content: entities (subsystems/bounded contexts), state_variables (volatility classifications), invariants (Golden Rule, anti-corruption), `forbidden_vocabulary` enumerated (`lambda`, `ecr`, `sqs`, `ec2`, `s3`, `dynamodb`, `kafka`, `python`, `node`, `typescript`, `golang`), and `citations` requiring Löwy golden-rule reference when volatility strategy is selected.
- **FR-4** Volatility reference update — add a named "Golden Rule" section to `volatility-decomposition.md` with explicit Löwy citation (*Righting Software*, Ch. 2) and a functional-decomposition-trap anti-pattern with worked example (closes Gap 1).
- **FR-5** DDD reference update — add "No Implementation Nouns at Decomposition" guardrail threaded through Phases 1–4 of `strategic-ddd.md`, plus bounded-context integrity rules (closes Gap 2 for DDD parity).
- **FR-6** Architect integration into Stage 5 Plan — new invocation step in `pipeline-stages.md` between Plan steps 1 and 3, task_type `implementation-sequencing`, producing `.delivery/artifacts/05-plan/architect/sequencing.md`. Architect named as participant (not owner) in Stage 5 (closes Gap 3).
- **FR-7** DoD validator augmentation — Plan and Architect DoD gates perform at least one deterministic rule check against `constraints.yml` (forbidden-vocabulary grep, mandatory-artifact presence, numeric-ceiling compliance) in addition to existing prose review.
- **FR-8** Dogfood validation — this PRD's own companion `constraints.yml` must ship as Exhibit A at `.delivery/artifacts/02-refine/po/constraints.yml`, authored in Stage 3 Design, and must pass FR-7 checks during UAT.

## 4. Non-Functional Requirements

- **NFR-1** Plan stage first-try pass rate ≥80% measured over 5 subsequent pipeline runs (baseline 57% from `.delivery/memory/stages/plan.md`).
- **NFR-2** Zero implementation-detail vocabulary (`lambda`, `ecr`, `sqs`, `ec2`, `s3`, `dynamodb`, `kafka`, language names, specific cloud services) in any new decomposition artifact produced after this feature lands, verified by deterministic grep.
- **NFR-3** Schema changes backwards-compatible for ≥1 minor version; optional fields may be added without breaking existing consumers.
- **NFR-4** No new required `.delivery/config.yml` keys without a migration default; behind `experimental.constraints_model: true` during the 5-run A/B window.
- **NFR-5** Token cost increase per Refine stage ≤15% (the MAR-style overhead ceiling).
- **NFR-6** Installed↔source file sync: source-of-truth in `delivery-team/`, validators check the installed copy; sync asserted at SessionStart.

## 5. Acceptance Criteria

- **AC-1** (rule-based) `constraints-model-guide.md` exists and documents exactly the 8 fields in FR-1 with type and required/optional markers.
- **AC-2** (rule-based) Both domain templates (Refine, Architect) exist as reference files and are loadable by their respective sub-agents.
- **AC-3** (rule-based) `grep -Eiw 'lambda|ecr|sqs|ec2|s3|dynamodb|kafka|python|node|typescript|golang' .delivery/artifacts/04-architect/**/*.md` returns zero matches on any post-feature pipeline run.
- **AC-4** (rule-based) Every volatility-strategy Architect artifact cites Löwy's golden rule; absence fails DoD.
- **AC-5** (rule-based) Stage 5 Plan artifacts include `.delivery/artifacts/05-plan/architect/sequencing.md` with at least one Architect validation note.
- **AC-6** (empirical) Run the pipeline 5 times after landing; Plan first-try pass rate ≥80%. Measured via memory-index stage health table.
- **AC-7** (empirical, dogfood P0) This feature's own `constraints.yml` exists and passes FR-7 checks in UAT. No DoD submission before the dogfood — per memory lesson.
- **AC-8** (rule-based) Refine-stage token cost delta ≤15% versus prior 5-run rolling average.

## 6. Out of Scope

- BACKLOG-003 configurable architecture board pattern (consumes our output in the *next* run)
- BACKLOG-005 paradigm-as-skill restructure
- BACKLOG-006 transformation planning
- MAR cross-persona pilot (absorbed into BACKLOG-003 per `po-revision-research-integration.md`)
- Rewriting architect references beyond the three gaps confirmed in `architect-examine-decomposition-gaps.md`
- `.delivery/config.yml` schema bump v2.7 → v2.8 (earned only after the primitive survives both domains)

## 7. Success Metrics

| Metric | Baseline | Target | Source | Method |
|---|---|---|---|---|
| Plan first-try pass rate | 57% (`.delivery/memory/stages/plan.md`) | ≥80% | Memory index stage health table | 5-run rolling window post-land |
| Impl-detail vocab occurrences per Architect artifact | >0 (Gap 2 evidence) | 0 | Deterministic grep (NFR-2 token list) | DoD validator on every run |
| Golden Rule citation rate (volatility runs) | ~0% (Gap 1) | 100% | Artifact scan | DoD validator |
| Architect-in-Plan participation | 0 runs (Gap 3) | 100% of runs | `.delivery/artifacts/05-plan/architect/` presence | DoD validator |
| Refine token cost delta | 0% | ≤+15% | Orchestrator token accounting | Per-run measurement |

## 8. Risks + Mitigations

> *"Even the wise cannot foretell all roads, but the wise plan for the dark ones."*

- **R-1 Schema bloat.** The primitive grows arms and legs until it models everything and enforces nothing. *Mitigation*: MVP fields only (≤8), extension protocol deferred to v2.8, rejection criterion if any field lacks a rule-check consumer.
- **R-2 Architect Stage 4 Light mode producing shallow decomposition.** Light means reduced depth, not skipped (memory lesson). *Mitigation*: FR-6 explicitly calls out Architect-in-Plan as the recovery point; Stage 4 Light still must emit `forbidden_vocabulary` and `citations`.
- **R-3 Impl-detail guardrails too aggressive — false positives block legitimate artifacts.** *Mitigation*: forbidden vocabulary is **enumerated, not heuristic** (explicit token list in FR-3 and NFR-2); additions require PRD revision.
- **R-4 Plan stage metric regression from increased Refine ceremony.** *Mitigation*: NFR-5 caps token delta at 15%; 5-run measurement window with pre-feature baseline; rollback protocol — if Plan first-try drops below 57% over any 3-run window, revert behind `experimental.constraints_model: false` and reopen BACKLOG-001 as REJECT.
- **R-5 Produce-and-ignore (Architect's modeling-theater risk).** *Mitigation*: FR-7 makes downstream consumption mandatory; DoD fails if no deterministic check fires.

## 9. Dependencies

- Config schema bump deferred (v2.7 holds; `experimental.constraints_model` flag lives in the existing `experimental` block — no required-key addition).
- New reference file: `delivery-team/skills/delivery-flow/references/constraints-model-guide.md`.
- Updated references: `volatility-decomposition.md`, `strategic-ddd.md`, `pipeline-stages.md`, `config-schema.md` (`dod_validators` augmentation).
- Installed↔source sync mandatory for the distributed theme cache and reference files; verified at SessionStart hook.
- Memory write hooks to record the 5-run A/B window into `.delivery/memory/stages/plan.md` and `topics/defect-patterns.md`.

## 10. Assumptions

- The existing delivery-flow Business Rules Engine pattern (from `prd-quality-gate-flow`) is reusable for deterministic `constraints.yml` checks without new infrastructure.
- The three gaps named in `architect-examine-decomposition-gaps.md` are the complete set; no further gaps will be introduced by this PRD's scope.
- A single shared schema can serve both domains; if pressure-testing in Stage 3 Design reveals structural divergence, the PRD returns here for revision before Architect stage.
- Pipeline runs producing measurable data exist within the 5-run window (i.e., real features, not synthetic).
- Gandalf is never early, nor late.
