# ADR-003 — Forbidden Vocabulary as an Enumerated List

**Status**: accepted
**Date**: 2026-04-08
**Stage**: 4 Architect (LIGHT) | **Author**: Celebrimbor (Solution Architect)
**Feature**: Paired Constraints Primitive

## Context

PRD Gap 2 and NFR-2 identify implementation-detail contamination as a blocking failure mode: decomposition artifacts name cloud services, runtimes, and languages at a stage where only volatility classes and bounded contexts belong. The DoD validator must detect such contamination deterministically — the Business Rules Engine philosophy forbids AI-inferred gate decisions. The question is *how* the validator recognizes a forbidden token.

## Decision

`forbidden_vocabulary` is an **enumerated list of exact tokens**, restated per `constraints.yml` file, matched by case-insensitive whole-word grep.

**Initial canonical list (copied into the Architect template, applied at decomposition stage only — these tokens are legitimate at Plan and Dev):**

- **Compute (cloud)**: Lambda, AWS Lambda, ECS, EKS, Fargate, EC2, Azure Functions, GCP, Google Cloud Functions
- **Container / orchestration**: Kubernetes, Docker, ECR
- **Messaging / streaming**: SQS, SNS, EventBridge, Kinesis, Kafka
- **Storage / data**: DynamoDB, S3, PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch
- **Languages**: Python, Node, Node.js, TypeScript, JavaScript, Go, Golang, Rust, Java, C#, Ruby
- **Frameworks (examples)**: Express, FastAPI, Django, Flask, Spring, Rails, Next.js

Maintainers may add tokens per the protocol below; removal requires a recorded justification in the PRD that supersedes NFR-2.

## Consequences

**Positive.**
- Fully deterministic: the check is a grep, auditable line by line, reproducible across runs.
- Rule-engine compatible: no language model in the gate path.
- Trivially implementable: a compiled regex alternation over the stage's artifact tree.
- Author-transparent: the list is physically present in the `constraints.yml` file the author is editing (IA §1 Flow B — "the mirror shows what must not be written").

**Negative.**
- **False positives are possible.** A legitimate prose mention of "the Java language as a historical example" fires the gate. *Mitigation*: whole-word matching, authorable per-artifact exception notes in the sequencing review, and the protocol below for PRD-recorded removals.
- **List maintenance burden.** New implementation fads (WebAssembly runtimes, novel databases) must be added over time. *Mitigation*: maintenance protocol below; quarterly review cadence.
- **Coverage is bounded by what the list names.** A token not on the list passes the gate even if it is an implementation leak. *Mitigation*: the list grows from observed violations; `.delivery/memory/topics/defect-patterns.md` is the evidence source.

## Alternatives Considered

1. **Regex heuristics.** Patterns like `/(?:AWS|Azure|GCP)\s+\w+/`. *Rejected*: false-positive rate climbs sharply on prose; maintainers cannot audit a regex as quickly as a list; edge cases explode.
2. **AI-judged contamination.** Ask a model "does this artifact contain implementation details?" *Rejected*: violates the Business Rules Engine philosophy (deterministic gate evaluation, no AI variance). Non-auditable; non-reproducible; the antithesis of this architecture's contract.
3. **Ontology-based matching.** A knowledge graph of "implementation concepts" with subsumption. *Rejected*: disproportionate infrastructure cost; ontology maintenance is itself a project; no reusable ontology exists for this domain at the granularity required.
4. **Per-stage heuristic thresholds.** "Fail only if more than N implementation terms appear." *Rejected*: the PRD target is zero (NFR-2); thresholds invite creeping tolerance.

## Rationale

The enumerated list wins on determinism, auditability, and rule-engine compatibility simultaneously. A grep is the smallest possible verifier; a list is the smallest possible specification. Both are within the reading and editing capacity of every role in the delivery team. False positives are a tolerable cost because they are *visible and fixable at authoring time*, not hidden in opaque model judgments.

## Maintenance Protocol

1. **Who adds tokens.** The Architect (Solution role) during Stage 4, when a new violation is observed in the wild. Additions land first in `constraints-model-guide.md` under "Canonical Forbidden Vocabulary," then propagate into `templates/constraints-architect.yml` in the same PR.
2. **How the list evolves.** Each addition cites the triggering artifact path and pipeline run ID in a commit message footer. Removals require a PRD amendment and an ADR supplement.
3. **Review cadence.** Quarterly — the Architect scans `.delivery/memory/topics/defect-patterns.md` for impl-leakage entries not yet covered and proposes additions.
4. **Scope discipline.** Tokens are forbidden *at decomposition stage only*. Stage 5 Plan and Stage 6 Dev legitimately name Lambda, Python, Postgres, and peers; the rule does not bleed into those stages.
