# BACKLOG-004: Decomposition guidance depth — volatility golden rule, implementation-detail guardrails, Architect in Plan stage

**Status**: Open
**Priority**: P1 (addresses an active, observable failure mode in current Architect output — implementation-detail contamination)
**Size**: S–M (reference doc additions + guardrail checks + Architect stage wiring into Plan)
**Created**: 2026-04-08
**Owner**: PO → Architect (content authorship) → delivery-flow (Plan-stage wiring)

## Source
- **PO ask (verbatim, 2026-04-08)**: "We need more to add more guidance for volatility based decomposition. Things like the golden rule are missing. Also the architect being involved in the project planning. The architect trying to functional decompose with volatility. tries to tie architect to the implementation details like lambda or ecr, language, sqs, etc. I suspect the same issue occurs in domain driven decomposition as well."
- **Architect examination (in progress)**: `.delivery/artifacts/research/architect-examine-decomposition-gaps.md` *(placeholder — link when written)*

## Problem Statement (three linked defects)
> "guidance for volatility based decomposition. Things like the golden rule are missing" — PO

> "the architect trying to functional decompose with volatility. tries to tie architect to the implementation details like lambda or ecr, language, sqs, etc." — PO

> "the architect being involved in the project planning" — PO

Today:
1. **Volatility golden rule absent.** The volatility decomposition reference does not teach Juval Löwy's golden rule ("decompose by volatility, not by functionality"). Architects revert to functional decomposition under the volatility label.
2. **Implementation-detail contamination.** Architect output names cloud services (Lambda, ECR, SQS), languages, and runtimes inside decomposition artifacts — these are Plan/Dev concerns, not Architect concerns. PO suspects parallel contamination in DDD output.
3. **Architect missing from Plan stage.** Project planning happens without Architect involvement, so the decomposition→plan handoff loses fidelity.

## Proposed Direction (high level — Architect is examining concrete content)
- Add golden rule + volatility vs functional contrast to volatility reference doc(s) under `delivery-team/skills/architect/references/`
- Add an **implementation-detail guardrail** — a rule-checkable lint (list of forbidden tokens: `lambda`, `ecr`, `sqs`, `python`, `node`, specific service names) applied to Architect-stage artifacts; violation triggers self-correction
- Wire Architect into Plan stage as a named participant (not owner) with a narrow brief: validate decomposition→work-breakdown fidelity
- Apply the same guardrail review to DDD reference doc (PO-flagged parallel suspicion) — Architect examination will confirm scope
- Defer concrete content and lint token list to Architect examination output

## Research lineage
- **Model-First Reasoning (arXiv:2512.14474)**: decomposition IS model construction. Volatility-based decomposition produces entities (subsystems), state (volatility classification), actions (interactions), and constraints (golden rule, anti-corruption, no functional decomposition). The implementation-noun guardrail and golden-rule invariant are **constraints in the Model-First sense** and should be expressed as rule-checkable invariants consumable by downstream stages — not as prose guidance.
- **Shared mechanism with BACKLOG-001**: the `constraints.yml` primitive built by BACKLOG-001 in Refine is the right shape for decomposition constraints here. The banned-token lint (`lambda|ecr|sqs|...`) and golden-rule invariant become entries in an Architect-stage constraints artifact (or a `decomposition-constraints.yml` sibling) that reuses BACKLOG-001's schema, DoD hook pattern, and Business-Rules-Engine-style deterministic checks. **Run in parallel with BACKLOG-001 so the schema is pressure-tested against two domains before any v2.8 bump.**
- **Feeds BACKLOG-003**: the `volatility_reviewer` seat in the architecture board (see architect examination Option C) enforces exactly these invariants. Board review becomes the runtime enforcement layer for the guardrails authored here.

## Success Criteria (concrete)
1. **Zero cloud-service-name contamination**: a new pipeline run (GREENFIELD or FEATURE) produces an Architect decomposition artifact containing **zero** occurrences of `lambda|ecr|sqs|ec2|s3|dynamodb|<language-name>` (configurable token list), verified by a rule check
2. **Golden rule cited**: the same artifact explicitly cites the volatility golden rule (or equivalent named principle) when volatility decomposition is selected
3. **Architect in Plan**: Plan-stage artifacts from a real run show Architect as a named contributor with at least one validation note
4. **DDD parity**: if Architect examination confirms DDD contamination, DDD reference gets the same guardrail treatment in the same PR
5. Guardrail is rule-based (deterministic), not AI-inferred (aligns with Business Rules Engine convention)
6. **Model-First alignment**: guardrails and golden-rule invariant are expressed as structured constraint entries (candidate reuse of BACKLOG-001's `constraints.yml` schema), not prose — enabling deterministic downstream consumption by Plan and by the BACKLOG-003 board's `volatility_reviewer` seat

## Size & Complexity
- **S–M**. Content additions + token-list lint + Plan-stage participation wiring. No new pattern, no new skill.

## Dependencies
- **Runs in parallel with BACKLOG-001** — shared `constraints.yml` mechanism; co-develop so schema covers Refine constraints + decomposition constraints
- **Blocks BACKLOG-003** — board seats (especially `volatility_reviewer`) consume these guardrails as their rule set
- **Blocks BACKLOG-005** — the paradigm-as-skill pilot (volatility) should absorb these corrections rather than restructure first and fix later

## Links
- Architect examination: `.delivery/artifacts/research/architect-examine-decomposition-gaps.md` *(placeholder)*
- Current decomposition refs: `delivery-team/skills/architect/` (4 decomposition strategies per CLAUDE.md)
