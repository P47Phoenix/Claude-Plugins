# US-4 — Architect constraints template

**Developer**: Gimli | **Date**: 2026-04-08 | **Stage**: 6 Dev

## Scope
Template only. No pipeline-stages.md changes (that is US-7).

## Artifacts written
- `delivery-team/skills/delivery-flow/references/templates/constraints-architect.yml` (NEW)
- `delivery-team/skills/delivery-flow/references/templates/README.md` (NEW)

## Acceptance criteria
- **AC-4.1** — All 8 ADR-001 fields instantiated with Architect-scoped
  comments: `entities`, `invariants`, `forbidden_vocabulary`,
  `numeric_ceilings`, `state_variables`, `actions`, `mandatory_artifacts`,
  `citations`. Field order preserved per architecture.md §3. ✓
- **AC-4.2** — `forbidden_vocabulary` pre-populated with the full
  enumerated token list from US-4 spec (30 tokens: lambda, aws lambda,
  ecr, ecs, eks, sqs, sns, eventbridge, dynamodb, s3, kinesis, fargate,
  ec2, gcp, azure functions, kubernetes, docker, python, node, typescript,
  javascript, go, rust, java, express, fastapi, django, postgresql, mysql,
  mongodb). ✓
- **AC-4.3** — `citations` field carries a commented requirement note
  binding Löwy's *Righting Software* Ch. 2 to volatility-strategy runs,
  aligned with ADR-001 and DoD rule R-CITATIONS. ✓

## Notes
- Template embeds the forbidden list verbatim (Galadriel's Q1 ruling:
  glance-ability wins; DRY honored at author time via this template).
- README introduces both templates; refine template lives in US-3 scope.
- Pure YAML per `feedback_config_format.md`.

STATUS: DONE
