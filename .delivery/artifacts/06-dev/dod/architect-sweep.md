# Architect DoD Sweep — Stage 6 Stories

**Stage**: 6 Development | **Role**: Solution Architect (Celebrimbor) | **Date**: 2026-04-08
**Feature**: Paired Constraints Primitive

> *"I have walked the forge. Every ring set against the mark I struck at Stage 4."*

## ADR Conformance Table

| # | Gate Criterion | Source | Evidence | Verdict |
|---|---|---|---|---|
| 1 | 8-field schema, `entities`+`invariants` required, forward-compat permitted | ADR-001 | `constraints-schema.json`: 8 properties, `required: ["entities","invariants"]`, `additionalProperties: true` | PASS |
| 2 | Refine template — 8-field shape, scope discipline | ADR-001 | `templates/constraints-refine.yml` — all 8 fields present in canonical order; PRB-scoped commentary | PASS |
| 3 | Architect template — 8-field shape, forbidden_vocabulary pre-populated | ADR-003 | `templates/constraints-architect.yml` — 30 tokens pre-populated (lambda, ecr/ecs/eks, sqs/sns/eventbridge, dynamodb/s3/kinesis, ec2/fargate, kubernetes/docker, python/node/typescript/javascript/go/rust/java, express/fastapi/django, postgresql/mysql/mongodb, gcp, azure functions); Löwy citation stub present | PASS |
| 4 | Stage 5 Plan insertion — Architect as `implementation-sequencing` participant | ADR-002 | `pipeline-stages.md:432-436` — new step 2 inserted after PO step 1; task_type `implementation-sequencing`, ROLE `solution`, correct input artifact set, output `sequencing.md`; ADR-002 explicitly cited in comment | PASS |
| 5 | Stage 5 waiver for BUG_FIX/DOCS_ONLY/DESIGN | ADR-002 | `pipeline-stages.md:432` inline waiver + `pipeline-stages.md:491` Light Mode section restates WAIVED | PASS |
| 6 | Golden Rule stated AS A RULE in §0, Löwy cited | Architecture §5 | `volatility-decomposition.md:5-11` — §0 header, rule verbatim, "This is not a guideline. It is not a preference. It is **THE RULE**"; citation to *Righting Software* Ch. 2; functional-decomposition-trap anti-pattern with before/after table at lines 21-44 | PASS |
| 7 | DDD Decomposition Hygiene sidebar spans Phases 1–4 | Architecture §5 | `strategic-ddd.md` lines 24, 64, 106, 141 — sidebar repeated at head of all four phases | PASS |
| 8 | Dogfood `constraints.yml` uses structured `{work, chapter, page}` citations | Arch Q2 ruling | `.delivery/artifacts/02-refine/po/constraints.yml:75-84` — three citation entries, all structured; Löwy Ch. 2 cited (page TBD flagged) | PASS* |
| 9 | Forward-compat fixture exists (US-1) | US-1 AC | `delivery-team/skills/delivery-flow/references/fixtures/constraints-forward-compat.yml` present | PASS |

\* **Note on Row 8**: Löwy citation `page: "TBD"` — structurally valid per schema (`page` accepts string), but page number should be resolved (Ch. 2, p. 31 per architecture §5) before release. Non-blocking for DoD; filed as trim-polish nit.

## Observations

- Schema's `additionalProperties: true` at root and within each `citations` object provides explicit forward-compat headroom for AC-1.4 without schema-version churn.
- Architect template's forbidden_vocabulary is a **superset** of ADR-003's enumerated canon (adds `eks`, `gcp`, `azure functions`) — additive evolution is within the ADR-003 maintenance protocol; compliant.
- Stage 5 step 2 comment block explicitly invokes ADR-002 by name, preserving decision traceability at the point of use.
- Both templates preserve the canonical field order stipulated in Architecture §3, honoring the Q4 ruling (order enforced by template, not validator).

## Verdict

All nine gate criteria met. The implementation conforms to Architecture, ADR-001, ADR-002, and ADR-003 without deviation. The single nit (Löwy page TBD in the dogfood file) is cosmetic and does not breach any deterministic rule.

> *"The work is true to the mark. Let it stand."*

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/06-dev/dod/architect-sweep.md
SUMMARY: All nine criteria conform to architecture and the three ADRs. Schema, templates, Stage 5 insertion, golden rule, DDD sidebars, dogfood, and fixture all true to the mark.
