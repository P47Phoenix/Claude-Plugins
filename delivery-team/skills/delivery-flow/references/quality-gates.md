# Quality Gates and Definition of Done

## Team Definition of Done Protocol

Every stage artifact must be validated by multiple team roles before the stage is considered complete. DoD validation is the final checkpoint before a stage advances -- it runs after all collaboration patterns (evaluator-optimizer, adversarial review, etc.) have completed.

### How DoD Validation Works

1. Stage produces its primary artifact.
2. Collaboration patterns run (evaluator-optimizer loop, adversarial review, etc.) and the artifact is revised as needed.
3. The revised artifact is submitted to DoD validators for the stage.
4. Each validator is a sub-agent spawned with the relevant skill and a role-specific review prompt.
5. Each validator independently produces one of:
   - **DONE** -- artifact meets this role's quality standards.
   - **NOT_DONE** -- with specific findings detailing what fails, why it matters, and how to fix it.
6. **ALL validators must return DONE** for the stage to complete.
7. Any NOT_DONE triggers self-correction (see protocol below).
8. Maximum 3 DoD validation cycles per stage (unless stage-specific override in gate criteria).
9. After exhausting max cycles with unresolved findings, dynamic escalation to human is triggered.

### DoD Validator Prompt Template

```
You are validating this artifact as the [ROLE] on the delivery team.

Review the artifact strictly from your perspective. Apply these criteria:

[ROLE-SPECIFIC CRITERIA]

Artifact:
---
[ARTIFACT CONTENT]
---

Respond with:
- **DONE** or **NOT_DONE**
- If NOT_DONE, list each failing criterion with:
  - What specifically fails (quote the relevant section)
  - Why it matters (impact if shipped as-is)
  - Actionable suggestion to fix it (specific enough to implement)
```

---

## Self-Correction Protocol

When DoD validation or quality gate evaluation returns failures:

**Step 1 -- Collect findings.**
Aggregate all NOT_DONE findings from all validators. Include DONE results for context (so the primary agent knows what is already acceptable).

**Step 2 -- Construct targeted feedback.**

```
The [ARTIFACT TYPE] needs revision. Findings from team validation:

[ROLE 1] -- NOT_DONE:
- [Finding 1]: [what specifically fails]. Fix: [actionable instruction]
- [Finding 2]: [what specifically fails]. Fix: [actionable instruction]

[ROLE 2] -- DONE (no issues)

[ROLE 3] -- NOT_DONE:
- [Finding 1]: [what specifically fails]. Fix: [actionable instruction]

Revise the artifact to address ALL findings above. Do not regress on
criteria that already passed.
```

**Step 3 -- Re-invoke the primary agent** with: original context + current artifact + aggregated feedback. The primary agent must address every finding explicitly.

**Step 4 -- Re-run DoD validation.** All validators re-evaluate (not just the ones that failed), because revisions can introduce regressions.

**Step 5 -- Track iteration count.** If max iterations reached and findings persist, trigger dynamic escalation.

---

## Dynamic Escalation Rules

Escalation can trigger at ANY point during pipeline execution, not only at stage boundaries. The orchestrator monitors for these conditions continuously.

| Trigger | Condition | Action |
|---------|-----------|--------|
| Repeated DoD failure | Same criterion fails across 3 consecutive validation cycles | Escalate with all 3 attempts shown side by side |
| Low adversarial confidence | Challenger agent rates artifact confidence at 2/5 or below | Escalate immediately, even mid-stage |
| Decision deadlock | Decision Owner cannot resolve a routed issue | Escalate with the decision context, options considered, and reasoning |
| Debate stalemate | Judge agent returns DEADLOCK (arguments equally compelling) | Escalate with both positions and judge's analysis |
| No correction progress | Self-correction iteration produces no meaningful change to failing criteria | Escalate with the stuck issue and all prior attempts |
| Cross-cutting conflict | Two roles produce contradictory guidance that cannot be reconciled | Escalate with both positions and the specific conflict |

### Escalation Format

Every escalation presented to the human follows this structure:

```
## Escalation: [Stage Name] -- [Brief Issue Description]

**Issue**: [What went wrong, stated clearly in 1-2 sentences]

**Attempts**: [What was tried and how many iterations occurred]

**Current state**: [Where the artifact stands now -- what passes, what still fails]

**Findings**:
[Aggregated validator/reviewer feedback from the most recent cycle]

**Options**:
1. **Provide guidance**: [Describe what kind of input would unblock progress]
2. **Override**: Proceed despite the issue (risk: [state the risk])
3. **Redirect**: Try a different approach (suggestion: [if applicable])
4. **Abort**: Halt pipeline execution, preserve all artifacts produced so far
```

---

## Stage Gate Criteria

Each gate lists its evaluation criteria, DoD validators, and maximum self-correction iterations. Criteria are tagged with severity (see Criteria Severity section).

### Gate 1: Idea Brief

- [ ] Problem statement present and specific (not vague or generic) [blocking]
- [ ] At least 1 target user persona identified with context (who they are, what they need) [blocking]
- [ ] At least 1 measurable goal stated (quantified success condition) [blocking]
- [ ] Constraints or known limitations listed (technical, timeline, budget, regulatory) [warning]
- [ ] Initial scope boundaries sketched (what is explicitly out of scope) [suggestion]
- **DoD validators**: Product Owner (completeness, business viability), Architect (feasibility signal -- can this be built?)
- **Max self-correction**: 2

### Gate 2: PRD Quality

- [ ] All functional requirements have acceptance criteria with testable conditions [blocking]
- [ ] Non-functional requirements are quantified with specific targets (not "fast" but "p99 < 200ms") [blocking]
- [ ] Out-of-scope section is present and non-empty [blocking]
- [ ] Success metrics are measurable with numeric targets and measurement method [blocking]
- [ ] No blocking open questions remain (all questions either answered or deferred with rationale) [blocking]
- [ ] User personas are specific with goals, pain points, and context (not generic "user") [warning]
- [ ] Dependencies identified with status (confirmed, pending, at-risk) [warning]
- [ ] Risks identified with likelihood, impact, and mitigation strategy [warning]
- [ ] Assumptions listed explicitly [suggestion]
- **DoD validators**: Product Owner (business value alignment), Architect (technical feasibility), QA Engineer (testability of acceptance criteria)
- **Max self-correction**: 3

### Gate 3: Design Completeness

- [ ] User flows cover happy path plus at least 1 error path per flow [blocking]
- [ ] Edge cases addressed: empty states, max content, first-time use, error recovery [blocking]
- [ ] Design aligns with PRD requirements (every user story has a corresponding design element) [blocking]
- [ ] Accessibility considerations documented (color contrast, keyboard navigation, screen reader support, or N/A with justification) [warning]
- [ ] Multi-device and responsive behavior specified (breakpoints, layout shifts, or N/A with justification) [warning]
- [ ] Interaction patterns defined (loading states, transitions, feedback for user actions) [warning]
- [ ] Content strategy addressed (placeholder vs real content, copy requirements) [suggestion]
- **DoD validators**: UX Designer (design quality and usability), Product Owner (requirement coverage), QA Engineer (testability), Architect (implementability)
- **Max self-correction**: 3

### Gate 4: Architecture Soundness

- [ ] Trade-offs documented for every major technical decision (what was chosen, what was rejected, why) [blocking]
- [ ] NFRs quantified with measurable targets and validation approach [blocking]
- [ ] Failure modes addressed for each component (what happens when it fails, how it recovers) [blocking]
- [ ] Data flows described with format, protocol, error handling, and validation [blocking]
- [ ] Security addressed: authentication, authorization, data protection, input validation [blocking]
- [ ] ADRs written for contested or consequential decisions [warning]
- [ ] Performance budgets set with specific numbers [warning]
- [ ] GAME_DEV: frame time budget, memory budget, network bandwidth budget [warning, if applicable]
- [ ] Dependency inventory with version constraints and update strategy [suggestion]
- [ ] Observability strategy: logging, metrics, tracing, alerting [suggestion]
- **DoD validators**: Architect (soundness, coherence), QA Engineer (testability), DevOps (deployability, operability), Security (security posture, threat model)
- **Max self-correction**: 2

### Gate 5: Plan Readiness

- [ ] Sprint goal is a single sentence expressing business value delivered [blocking]
- [ ] Every committed story has acceptance criteria [blocking]
- [ ] Dependencies between stories identified and sequenced [blocking]
- [ ] Commitment does not exceed 80% of available capacity [blocking]
- [ ] Capacity accounts for ceremonies, PTO, and known interruptions [warning]
- [ ] Test approach referenced (which stories need what kind of testing) [warning]
- [ ] Deployment approach referenced (how and when completed work ships) [warning]
- [ ] Risk items flagged with contingency (what if a story takes longer than estimated) [suggestion]
- **DoD validators**: Scrum Master (process compliance, realistic planning), Product Owner (scope and priority alignment), QA Engineer (test coverage plan), DevOps (deployment readiness)
- **Max self-correction**: 2

### Gate 6: Development Quality

- [ ] Code implements all acceptance criteria for the story [blocking]
- [ ] Tests written and passing (unit tests at minimum; integration tests for cross-boundary logic) [blocking]
- [ ] No critical issues from QA review [blocking]
- [ ] Code follows established language and framework best practices [warning]
- [ ] Inline documentation for non-obvious logic (why, not what) [warning]
- [ ] No hardcoded secrets, credentials, or environment-specific values [blocking]
- [ ] Error handling covers expected failure modes [warning]
- [ ] GAME_DEV: frame budget validated, no physics or rendering regressions [warning, if applicable]
- **DoD validators**: Developer (code quality, best practices), QA Engineer (tests pass, coverage adequate), Architect (design conformance, no architectural drift), Technical Writer (inline docs, API docs if applicable)
- **Max self-correction**: 3

### Gate 7: UAT Acceptance

- [ ] All test cases executed (no skipped tests without documented justification) [blocking]
- [ ] Pass rate meets threshold: 100% of critical tests, 90% overall [blocking]
- [ ] Documentation complete: release notes, user guides if applicable, API docs if applicable [blocking]
- [ ] Rollback plan documented with specific steps and validation criteria [blocking]
- [ ] Go/no-go criteria evaluated by review board [blocking]
- [ ] Known issues documented with severity and workaround if applicable [warning]
- [ ] Performance test results within budget (p99 latency, throughput, error rate) [warning]
- [ ] GAME_DEV: playtest feedback addressed, performance budgets met on target hardware [warning, if applicable]
- **DoD validators**: QA Engineer (all tests pass, coverage complete), DevOps (rollback ready, deployment verified), Product Owner (business acceptance), Technical Writer (documentation complete)
- **Max self-correction**: 2

---

## Criteria Severity

Every criterion in a quality gate carries one of three severity levels:

- **Blocking**: Must be resolved before the stage can complete. Any single blocking failure prevents advancement. There is no override except human escalation.
- **Warning**: Should be resolved. The stage can proceed, but findings are recorded in the pipeline state and carried forward as context for downstream stages. Accumulated warnings may trigger escalation if a pattern emerges.
- **Suggestion**: Nice to have. Recorded for future improvement and continuous learning. Does not affect the gate decision. Suggestions are surfaced in the final pipeline summary.
