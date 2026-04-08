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

[ROLE-SPECIFIC CRITERIA from quality-gates.md]

--- INPUT ARTIFACTS (read these files) ---
- [ARTIFACT_FILE_PATH]: The artifact to validate

Respond with ONLY this signal block:
STATUS: DONE | NOT_DONE | CODE_COMPLETE
ARTIFACT: [path to your review file]
SUMMARY: [one sentence, max 200 characters]
FINDINGS: [if NOT_DONE: bullet list of specific failures]
```

**STATUS values**:
- **DONE** -- all criteria met from your perspective.
- **CODE_COMPLETE** -- (Stage 6 Development only) code passes all structural criteria, but acceptance criteria requiring runtime validation exist (see the Verification Status section). List the empirical criteria pending validation.
- **NOT_DONE** -- structural or logic issues that need fixing before proceeding. Each finding must include: what specifically fails (quote the relevant section), why it matters (impact if shipped as-is), and an actionable suggestion to fix it (specific enough to implement).

DoD validators run in PARALLEL when `pipeline.parallel_validators` is true. Each validator receives only the artifact file path and gate criteria -- no other validator's output.

**One validator = one Agent invocation.** Every validator role is dispatched as
a SEPARATE Agent tool call. Four validators = four Agent calls in a single
parallel message. Never fuse two validator roles into one compound prompt
(e.g., "validate as QA and also as Security"). The compound-role detector in
`audit_agent_prompt.py` warns on these patterns. This rule is what makes Team
DoD actually a team — independent perspectives cannot emerge from a single
sub-agent asked to wear multiple hats.

### Delegation Meta-Gate

Before any stage's DoD is allowed to pass, the orchestrator MUST answer:

> **"Was every domain artifact produced in this stage written by a delegated
> sub-agent via the Agent tool?"**

If the orchestrator used Write or Edit to author, amend, or materially revise
any non-routing file in `.delivery/artifacts/**` during this stage, the DoD
meta-gate FAILS regardless of how validators voted. Routing metadata
(`stage-summary.md`, `state.md`, `state.tmp.md`) is the only permitted
orchestrator write path.

This meta-gate exists because a violation of the Delegation Prime Directive
invalidates the entire stage — the artifact did not come from the team, it
came from the orchestrator, and no amount of after-the-fact validation can
restore the team-authored provenance. If this gate fails, the stage MUST be
re-run with proper delegation.

### Known Hook Limitations

The `enforce_pipeline_scope.py` hook implements layered origin detection
(ADR-001) but has known gaps that this meta-gate exists to compensate for:

- **Bash redirection bypass**: Orchestrator-origin writes via Bash
  (`>`, `>>`, `tee`, `cat <<EOF`, `dd of=`, `cp`/`mv` into artifact paths)
  are not matched by the hook's current tool matchers. Closing this gap
  requires registering the hook on the Bash tool AND pattern-matching
  the command string.
- **Layer 2 metadata drift**: The hook's secondary detection reads harness
  hook-input metadata (`parent_tool_use_id` and similar fields). The shape
  of that payload is harness-version-dependent; unknown keys fall through
  to the soft-deny fallback (warn-only, never hard-deny — NFR-05).
- **Missing env-var injection**: Layer 1 (env var) is load-bearing. A
  missed injection at any orchestrator dispatch site collapses Layer 1,
  leaving Layer 2 carrying the full weight. Centralizing sub-agent dispatch
  (one injection site) is the architectural mitigation.

Validators and the meta-gate should assume the hook is advisory and apply
the "Was every artifact produced by a delegated sub-agent?" check manually.

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
- [ ] File path references in Design artifacts verified: any file path cited in Design artifacts that does not exist on disk and is not annotated with `[PLANNED]` generates a WARNING finding. The WARNING is logged, surfaced to the author, and carried forward to downstream stages, but does NOT block stage completion. File paths annotated with `[PLANNED]` are exempt from phantom detection at this stage. [warning] <!-- retro k4m9 -->
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
- [ ] Sprint capacity threshold (two-tier model) <!-- retros c8f2, k4m9 -->:
  - **>80% and <=100% utilization**: WARNING -- emits a warning stating the utilization percentage. Plan can pass DoD only after the warning is acknowledged with brief justification recorded in the sprint plan.
  - **>100% utilization**: BLOCKING -- plan cannot pass DoD until allocation is reduced to <=100% OR the PO provides explicit sign-off with justification recorded in the sprint plan.
  - **Light Mode**: Applies to all project types -- even single-story plans can be overscoped.
- [ ] Capacity accounts for ceremonies, PTO, and known interruptions [warning]
- [ ] Test approach referenced (which stories need what kind of testing) [warning]
- [ ] Deployment approach referenced (how and when completed work ships) [warning]
- [ ] Risk items flagged with contingency (what if a story takes longer than estimated) [suggestion]
- **DoD validators**: Scrum Bag (process compliance, realistic planning), Product Owner (scope and priority alignment), QA Engineer (test coverage plan), DevOps (deployment readiness)
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
- [ ] Empirical validation requirements identified: if any acceptance criteria require runtime verification (visual output, user interaction, API responses, runtime behavior), they are flagged in the Verification Status and story status is CODE_COMPLETE rather than DONE [blocking]
- [ ] Derived artifacts regenerated: if any modified source files have derived artifacts (generated docs, compiled schemas, transformed configs), all derived artifacts have been regenerated from current sources and the regeneration is documented in the story's DoD review [blocking] <!-- retro c8f2 -->
- **DoD validators**: Developer (code quality, best practices), QA Engineer (tests pass, coverage adequate, empirical criteria flagged), Architect (design conformance, no architectural drift), Technical Writer (inline docs, API docs if applicable)
- **DoD status options**: DONE (all criteria verified), CODE_COMPLETE (code passes but empirical validation pending), NOT_DONE (structural issues remain)
- **CODE_COMPLETE behavior**: story advances to Stage 7 (UAT) with pending empirical validations carried forward as mandatory test cases
- **Max self-correction**: 3

### Gate 7: UAT Acceptance

- [ ] All test cases executed (no skipped tests without documented justification) [blocking]
- [ ] All pending empirical validations from Stage 6 included as mandatory UAT test cases [blocking]
- [ ] Empirical-items classification section present in UAT test plan: every PRD acceptance criterion classified as "structural" or "empirical" with justification, and empirical items have documented validation method [blocking] <!-- retro k4m9 -->
- [ ] Pass rate meets threshold: 100% of critical tests, 90% overall [blocking]
- [ ] Documentation complete: release notes, user guides if applicable, API docs if applicable [blocking]
- [ ] Rollback plan documented with specific steps and validation criteria [blocking]
- [ ] Go/no-go criteria evaluated by review board [blocking]
- [ ] Known issues documented with severity and workaround if applicable [warning]
- [ ] Performance test results within budget (p99 latency, throughput, error rate) [warning]
- [ ] GAME_DEV: playtest feedback addressed, performance budgets met on target hardware [warning, if applicable]
- [ ] Exploratory testing session completed with observations logged (cross-story interactions tested, GAME_DEV gets 2 sessions) [warning]
- [ ] All defects found during UAT logged to `.delivery/defects/` with severity, category, and root cause [blocking]
- [ ] Dogfooding: changes were validated by actually USING them as a real user would, not just code review [blocking]
  - For hook changes: trigger the hook by performing the action it monitors and verify it fires correctly
  - For config changes: re-run the setup wizard or reload config and verify new values are applied
  - For skill changes: invoke the skill with a representative task and verify references load and output matches
  - For pipeline changes: run a mini pipeline (BUG_FIX for a trivial issue) and verify all stages execute
- **DoD validators**: QA Engineer (all tests pass, coverage complete), DevOps (rollback ready, deployment verified), Product Owner (business acceptance), Technical Writer (documentation complete)
- **Max self-correction**: 2

---

## Criteria Severity

Every criterion in a quality gate carries one of three severity levels:

- **Blocking**: Must be resolved before the stage can complete. Any single blocking failure prevents advancement. There is no override except human escalation.
- **Warning**: Should be resolved. The stage can proceed, but findings are recorded in the pipeline state and carried forward as context for downstream stages. Accumulated warnings may trigger escalation if a pattern emerges.
- **Suggestion**: Nice to have. Recorded for future improvement and continuous learning. Does not affect the gate decision. Suggestions are surfaced in the final pipeline summary.
