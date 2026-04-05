# Collaboration Patterns

The delivery pipeline uses 6 structured collaboration patterns to ensure quality. Patterns are configurable per project — enable or disable them in `.delivery/config.yml` under `pipeline.collaboration_patterns`.

## Pattern Summary

| Pattern | When Used | Purpose |
|---------|-----------|---------|
| Evaluator-Optimizer | After every stage artifact | Catch quality issues before DoD |
| Adversarial Review | Requirements, architecture, plans | Challenge assumptions and find blind spots |
| Review Board | Go/no-go and multi-domain decisions | Multiple expert perspectives |
| Decision Ownership | Mid-stage domain boundary questions | Route to the right expert |
| Debate | Technology or architecture trade-offs | Structured argumentation |
| Consensus | Cross-team alignment | Mutual agreement on shared commitments |

---

## 1. Evaluator-Optimizer Loop

The first quality pass after every stage produces an artifact.

**How it works**:

1. Primary agent produces the artifact
2. Evaluator agent reviews against quality gate criteria (PASS/FAIL per criterion)
3. If any criteria fail: route back to primary agent with findings
4. Primary agent revises, addressing each failure
5. Re-evaluate. Maximum 3 iterations.
6. If still failing after max iterations: escalate to user

The evaluator is intentionally a **separate agent** from the producer. The separation of roles — produce vs. evaluate — with distinct prompts produces meaningfully better results than self-review.

---

## 2. Adversarial Review (Red Team)

Challenges assumptions, finds blind spots, and stress-tests completeness.

**Used at**:

- Stage 2 (Refine): Challenge requirements completeness and hidden assumptions
- Stage 4 (Architect): Challenge design decisions, trade-offs, and security posture
- Stage 5 (Plan): Challenge estimates, risk assessments, and capacity assumptions

**How it works**:

1. Artifact has passed the evaluator-optimizer loop
2. Challenger agent receives ONLY the artifact (strict isolation — no production context)
3. Challenger produces: challenged assumptions, missing edge cases, alternative approaches, unaddressed risks, and a confidence rating (1-5)
4. If confidence is 2 or below: immediate escalation to user
5. If confidence is 3-5: primary agent addresses each challenge

**Confidence scale**:

| Rating | Meaning |
|--------|---------|
| 5 | Production-ready, minor suggestions only |
| 4 | Minor concerns, addressable without rework |
| 3 | Moderate concerns, direction is sound |
| 2 | Significant concerns, major revision needed — ESCALATE |
| 1 | Fundamental issues, reconsider entirely — ESCALATE |

---

## 3. Multi-Perspective Review Board

Multiple expert perspectives for high-stakes decisions.

**Used for**: Go/no-go decisions, cross-domain concerns where multiple specialists must weigh in.

**How it works**: Multiple role-specific validators review the same artifact independently and in parallel. All must approve for the decision to proceed.

---

## 4. Decision Ownership Routing

Routes mid-stage questions to the right expert.

**Used for**: Questions that cross domain boundaries during stage execution. Instead of the current agent guessing, the question is routed to the domain owner (e.g., security questions to the Security Architect, data questions to the Data Architect).

---

## 5. Debate

Structured argumentation for contested decisions.

**Used for**: Technology or architecture trade-offs where two valid options exist. Each side presents its case with evidence, and the debate produces a reasoned decision with documented trade-offs.

---

## 6. Consensus

Mutual agreement for shared commitments.

**Used for**: Sprint plans, release scope, and cross-team alignment where buy-in from all parties is required. The consensus pattern ensures all relevant roles agree before proceeding.

---

## Configuration

Control which patterns run via `.delivery/config.yml`:

```yaml
pipeline:
  collaboration_patterns:
    - evaluator-optimizer
    - adversarial
    - review-board
    - debate
    - consensus
    - decision-routing
```

The [Quick Start](../getting-started/quick-start.md) strictness levels set these automatically:

| Level | Patterns Enabled |
|-------|-----------------|
| Prototype | evaluator-optimizer only |
| Standard | evaluator-optimizer, adversarial, decision-routing |
| Strict | All 6 patterns |
