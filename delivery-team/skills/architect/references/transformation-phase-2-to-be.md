# Transformation Phase 2 — TO-BE Model (Architect-led)

*Part of `transformation-planning` task_type. Phase 2 of 4.*

## 1. Purpose

Architect-led construction of the **TO-BE structural model** — the target end-state the roadmap (Phase 3) will bridge toward. TO-BE uses the **same shared `constraints.yml` schema** as Phase 1B (BACKLOG-001), so AS-IS and TO-BE are directly comparable, directly diffable, and validated by the same `validate_constraints.py` toolchain. No bespoke target format — one schema, two artifacts.

## 2. Input

- **`as-is-constraints.yml`** — the Phase 1B structural reconstruction (authoritative starting state).
- **PRD-like migration goals** — desired business outcomes, drivers, non-negotiable outcomes (e.g., "reduce deploy time," "isolate the billing domain," "eliminate shared-mutable state across the scheduler"). These come from the invoking PO brief or the original transformation request.
- **Volatility golden rule reference** (when decomposition is volatility-based) — `delivery-team/skills/architect/references/volatility-strategy.md` and Löwy, *Righting Software*, Ch. 2.

## 3. Target model authoring

TO-BE is written to `to-be-constraints.yml` using the shared schema:

- `entities` — target subsystems / services / modules in the end state
- `state_variables` — target state ownership, volatility classification
- `actions` — the same reconstructed use cases from Phase 1A, re-homed onto the TO-BE entities
- `invariants` — the rules the target system must uphold (including any AS-IS invariants that must survive migration)
- `forbidden_vocabulary` — enumerated implementation details that MUST NOT appear (see §5)
- `metadata` — goals, drivers, references, citation block

Every TO-BE entity answers one question: **what axis of change justifies this boundary?** If the answer is "because the AS-IS has one too," that entity is not yet redesigned — it is copied.

## 4. Golden Rule citation requirement

When the TO-BE decomposition is **volatility-based**, the `citations` field in `to-be-constraints.yml` MUST reference Löwy's *Righting Software*, Chapter 2 (the Golden Rule: decompose along axes of volatility, never along functional lines).

- **Enforcement:** `check_dod_constraints.py`'s citation check scans `to-be-constraints.yml` for the Golden Rule reference when volatility language appears in `state_variables` or `metadata.strategy`.
- **Missing citation = DoD FAIL.** This is mechanical, not subjective.
- Non-volatility strategies (e.g., pure DDD bounded-context decomposition) cite their own authority (Evans, Vernon) in the same `citations` field.

## 5. Forbidden vocabulary enforcement

The TO-BE model is a **structural** artifact, not an implementation plan. It MUST NOT contain implementation details per ADR-003 of the prior transformation run. The enumerated forbidden list from `constraints-architect.yml` applies here verbatim:

- Cloud SKUs: Lambda, ECR, ECS, Fargate, DynamoDB, S3, RDS, Kinesis, SQS, SNS, Step Functions, API Gateway, CloudFront, Route53
- Runtimes / languages: Python, Node, Go, Rust, Java, .NET, TypeScript
- Frameworks: FastAPI, Express, Django, Spring, React, Vue
- Storage / infra primitives: Postgres, MySQL, Redis, Kafka, Docker, Kubernetes, Terraform

If an `entity` is called `billing-lambda`, the TO-BE is leaking. Rename to `billing-service` (or better, a volatility-named boundary like `pricing-policy-engine`). The `forbidden_vocabulary` field in the TO-BE file itself SHOULD re-list these so reviewers can run a one-shot grep.

Phase 3 roadmap is where platform choices appear. Not here.

## 6. Output

Canonical path: **`.delivery/artifacts/08-transform/to-be-constraints.yml`**

Validated by the same `validate_constraints.py` that validates AS-IS. Exit 0 required before Phase 3 begins.

## 7. Diffable

Because AS-IS and TO-BE share the schema, the orchestrator can mechanically diff:

- **`entities` diff** — which subsystems are new, removed, renamed, merged, split. This is the migration surface area.
- **`invariants` diff** — which AS-IS invariants survive unchanged, which are relaxed (danger: regression risk), which are tightened (danger: migration breakage), which are newly introduced.
- **`actions` diff** — which use cases re-home to different entities (the routing churn the roadmap must sequence).

The diff IS the migration scope. Phase 3 steps close named rows of this diff one at a time.

## 8. Anti-patterns

- **AS-IS with wishful labels.** Copying `as-is-constraints.yml`, renaming a few entities, declaring victory. The `entities` diff will show zero real structural change — caught at review.
- **Forbidden-vocabulary leakage.** TO-BE naming services after the platform you happen to like today. The model outlives the platform; it must not name it.
- **Scope drift into roadmap.** Writing *how* to get there (ordering, sequencing, step boundaries) inside the TO-BE file. That is Phase 3's job. TO-BE is a snapshot, not a journey.
- **Missing Golden Rule citation** under a volatility decomposition. Unsubstantiated authority = DoD fail.
- **Unjustified entity boundaries.** Any TO-BE entity that cannot answer "what axis of change justifies this boundary?" is a copy, not a design.
- **Invariant amnesia.** Dropping AS-IS invariants silently. Every drop must be an explicit, documented relaxation with a rationale — otherwise it reappears as a production incident.
