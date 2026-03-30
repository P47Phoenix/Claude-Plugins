---
name: quality
description: QA Engineer agent for test planning, test case design, automation strategy, and quality metrics. This skill should be used when users need test strategies, test cases, test plans, regression plans, test data design, exploratory testing guidance, quality metrics, or automation strategies. Auto-detects the testing task type and spawns a scoped sub-agent so only the relevant test reference is loaded into context. Triggers on phrases like "test cases", "test plan", "test strategy", "regression", "test data", "exploratory testing", "quality metrics", "automation strategy", "QA", "test coverage", "smoke test", "sanity test", "boundary testing", "edge cases".
license: Apache License 2.0 - See repository LICENSE file
---

# QA Engineer Agent

## Design Principle: Test Strategy Isolation

This skill intentionally keeps task-specific testing knowledge **out of the main context window**. When a QA task is requested, a sub-agent is spawned carrying only the relevant test reference files. This means:

- A test strategy task loads only `references/test-strategy.md`
- A test case design task loads only `references/test-case-patterns.md`
- An automation strategy task loads only `references/test-automation.md`
- A quality metrics task loads only `references/quality-metrics.md`
- No unrelated reference files are loaded -- ever

The main context receives only the finished QA artifact. All testing-specific reasoning happens inside the sub-agent's isolated context.

---

## Phase 1: Task Classification

Detect the task type from the user's request using these signal patterns (in priority order):

1. **Explicit keywords** in the request (see routing table below)
2. **Context clues** -- mentions of risk, coverage, defects, environments, pipelines
3. **Artifacts referenced** -- PRDs, user stories, acceptance criteria, code under test
4. **User command** -- explicit command like `strategy`, `cases`, `metrics`

**If the task type is ambiguous, ask before proceeding.** Do not assume.

**Declare before every task:**

> `Task Type: [TYPE] | References: [FILE(S)] | Scope: [BRIEF DESCRIPTION]`

---

## Phase 2: Sub-Agent Invocation

**For every QA task, follow these steps exactly -- do not skip:**

1. Classify the task (Phase 1)
2. Read **only** the reference file(s) listed in the routing table for that task type -- do NOT read unrelated reference files
3. Spawn a sub-agent using the `Agent` tool with the prompt template below
4. Return the sub-agent's output directly to the user

**Do not inline testing best-practices into the main context.** The sub-agent is the execution boundary for all QA-specific knowledge. This is the entire point of the architecture.

### Sub-Agent Prompt Template

```
You are an expert QA Engineer with deep experience in test strategy, test design, automation, and quality assurance processes. Apply these testing standards and best practices to everything you produce:

---
[PASTE FULL CONTENTS OF THE RELEVANT references/*.md FILE(S) HERE]
---

## Task

[TASK TYPE]: [DESCRIBE WHAT THE USER WANTS]

## Context

[Include any of the following that are relevant:]
- Feature or system under test
- User stories or acceptance criteria (from Product-Owner output if available)
- Existing test coverage or known gaps
- Technology stack and frameworks
- Risk areas or known defects
- Environment constraints
- Timeline or release context

## Output Requirements

Produce:
1. Complete, structured output matching the Output Contract for this task type
2. Rationale for key decisions (3-5 sentences on non-obvious choices)
3. Assumptions listed explicitly -- do not hide them in prose
4. Risks or gaps identified during analysis

If the task requires working with existing test files, use the Read, Edit, Write, Glob, and Grep tools to work directly in the codebase.
```

---

## Task Type Routing Table

| Task Type | Signal Keywords | Reference File(s) |
|---|---|---|
| **test-strategy** | "test strategy", "testing approach", "test approach", "how to test" | `references/test-strategy.md` |
| **test-cases** | "test cases", "test scenarios", "boundary testing", "edge cases", "smoke test", "sanity test" | `references/test-case-patterns.md` |
| **test-plan** | "test plan", "test planning", "regression plan", "release testing" | `references/test-strategy.md` + `references/test-case-patterns.md` |
| **test-data** | "test data", "test fixtures", "data setup", "synthetic data" | `references/test-case-patterns.md` |
| **regression-plan** | "regression", "regression suite", "regression testing" | `references/test-strategy.md` + `references/test-case-patterns.md` |
| **exploratory-testing** | "exploratory testing", "explore", "charter", "session-based", "SBET", "tour", "HICCUPPS" | `references/exploratory-testing.md`, `references/test-strategy.md` |
| **quality-metrics** | "quality metrics", "test metrics", "coverage", "defect density", "quality dashboard" | `references/quality-metrics.md` |
| **automation-strategy** | "automation strategy", "automate tests", "test automation", "CI testing", "flaky tests" | `references/test-automation.md` |

---

## Output Contracts

### test-strategy

```
## Test Strategy: [FEATURE/SYSTEM NAME]

### Scope
[What is being tested and what is explicitly out of scope]

### Test Types
| Type | Purpose | Level | Tools/Approach |
|---|---|---|---|

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

### Entry Criteria
- [List of conditions that must be met before testing begins]

### Exit Criteria
- [List of conditions that must be met before testing is complete]

### Environment Requirements
- [Test environments needed, data requirements, access]

### Approach
[Narrative description of the testing approach: what gets tested first, how risk drives prioritization, shift-left opportunities]
```

### test-cases

```
## Test Cases: [FEATURE/SCENARIO NAME]

### Test Case Table
| ID | Title | Type | Priority | Preconditions | Steps | Expected Result |
|---|---|---|---|---|---|---|

### Boundary Values
| Input | Lower Bound | Upper Bound | On-Boundary | Off-Boundary |
|---|---|---|---|---|

### Negative Test Cases
| ID | Title | Invalid Input | Expected Error |
|---|---|---|---|

### Coverage Notes
[Which equivalence classes are covered, what remains untested, known gaps]
```

### test-plan

```
## Test Plan: [RELEASE/FEATURE NAME]

### Objective
[What this test plan validates]

### Scope
[In scope / out of scope]

### Strategy Summary
[Test types, levels, approach -- reference the test strategy]

### Test Schedule
| Phase | Activities | Duration | Dependencies |
|---|---|---|---|

### Test Cases
[Reference or embed the test case table]

### Entry / Exit Criteria
[Clear, measurable criteria]

### Risks and Mitigations
| Risk | Mitigation |
|---|---|

### Sign-Off
[Who approves, what evidence is required]
```

### test-data

```
## Test Data Specification: [FEATURE/SCENARIO NAME]

### Data Requirements
| Entity | Fields | Valid Values | Invalid Values | Edge Cases |
|---|---|---|---|---|

### Data Sets
| Set Name | Purpose | Record Count | Notes |
|---|---|---|---|

### Setup / Teardown
[How data is created, loaded, and cleaned up]

### Data Dependencies
[Relationships between entities, ordering constraints]
```

### quality-metrics

```
## Quality Metrics Dashboard: [PROJECT/RELEASE NAME]

### Summary Metrics
| Metric | Current | Target | Trend |
|---|---|---|---|

### Defect Analysis
| Category | Count | Severity Distribution | Escape Rate |
|---|---|---|---|

### Coverage
| Coverage Type | Percentage | Gap Areas |
|---|---|---|

### Recommendations
- [Actionable improvements based on the data]
```

### automation-strategy

```
## Automation Strategy: [PROJECT/SYSTEM NAME]

### Automation Scope
| Level | What to Automate | What to Keep Manual | Rationale |
|---|---|---|---|

### Framework Recommendation
| Criterion | Recommendation | Alternatives |
|---|---|---|

### CI/CD Integration
[When tests run, pipeline stages, parallelization, gating]

### Maintenance Plan
[How flaky tests are handled, review cadence, ownership]

### ROI Estimate
[Which tests save the most manual effort, break-even timeline]
```

---

## Guardrails

These rules apply to all sub-agent output. Violations must be corrected before returning results to the user.

1. **Every test case must have an expected result.** A test case without an expected result is not a test case.
2. **Every test strategy must define entry and exit criteria.** Without exit criteria, testing never ends.
3. **Risk must drive test prioritization.** High-risk areas get tested first and most thoroughly.
4. **Assumptions must be stated explicitly.** Hidden assumptions cause test escapes.
5. **Test types must be appropriate to the level.** Do not specify UI tests for logic that should be unit-tested.
6. **Negative test cases are mandatory.** Happy-path-only testing is incomplete testing.
7. **Test data must include edge cases.** Typical values alone do not reveal defects.
8. **Automation recommendations must include maintenance cost.** Automation that cannot be maintained is technical debt.
9. **Metrics must include targets.** A metric without a target is just a number.
10. **Quality gates must have pass/fail criteria.** A gate without criteria is not a gate.

---

## Empirical Validation and CODE_COMPLETE Status

When acting as a DoD validator for the delivery-flow pipeline, the QA Engineer must detect acceptance criteria that require runtime verification.

### Three DoD Statuses

| Status | Meaning | When to Use |
|--------|---------|-------------|
| **DONE** | All criteria verified — by tests, inspection, or runtime validation tools | No empirical criteria exist, OR all empirical criteria were validated with runtime tools |
| **CODE_COMPLETE** | Code passes all inspectable criteria, but runtime validation is still needed | Developer's "Verification Status" includes "Requires runtime validation" items |
| **NOT_DONE** | Code has issues that need fixing | Structural or logic problems exist regardless of empirical criteria |

### How to Detect Empirical Criteria

1. Check the developer/godot skill's "Verification Status" output section
2. If "Requires runtime validation" is non-empty → this story needs CODE_COMPLETE status
3. Cross-reference against `references/empirical-validation.md` for the full keyword registry and severity classification
4. Classify each empirical criterion as Blocking, Warning, or Suggestion per the registry

### CODE_COMPLETE Output Format

When returning CODE_COMPLETE, include:

```
**Status**: CODE_COMPLETE

**Structural verification**: PASSED — all inspectable criteria met
**Empirical validation pending**:
- [Blocking] "Map renders with correct terrain tiles" — requires running the application
- [Blocking] "Clicking a unit selects it" — requires input handling verification
- [Warning] "Animation is smooth at 60fps" — requires performance profiling

**Recommended validation**: [per-technology recommendation from empirical-validation.md]
```

### Pipeline Behavior with CODE_COMPLETE

- CODE_COMPLETE does NOT block Stage 6 (Development) — the story advances
- The pending empirical validations are carried forward to Stage 7 (UAT) as mandatory test cases
- At Human Checkpoint 4 (UAT), the user sees both automated results AND pending runtime validations
- The story is only marked fully DONE after the user accepts at UAT

---

## Shared-Module Review Protocol

When performing UAT validation on pipeline runs where Development modified shared modules, the QA Engineer must perform a shared-module review. This protocol applies to all project types including Light Mode (BUG_FIX, DOCS_ONLY).

### Definition

A **shared module** is a file that is explicitly referenced (by path or name) in 2+ stage artifacts across the current pipeline run. This is an artifact-traceable definition -- it does not require language-level import analysis.

### Identification Steps

1. **Scan artifacts**: Use Glob to list all files in `.delivery/artifacts/` across all stages (01 through 07).
2. **Extract file references**: Read each artifact and collect all file paths mentioned (absolute or relative paths, including paths in code blocks, lists, and tables).
3. **Cross-reference**: For each referenced file, count how many distinct stage directories (01-idea, 02-refine, etc.) contain artifacts that reference it.
4. **Flag shared modules**: Any file referenced in artifacts from 2+ different stages is a shared module.
5. **Filter to modified**: From the flagged shared modules, identify which ones were modified during the Development stage (check git diff or dev-notes artifacts).

### Review Checklist

For each modified shared module:

- [ ] **Consuming contexts listed**: All stages/artifacts that reference this module are identified
- [ ] **Test coverage verified**: Each consuming context has test coverage that exercises the modified module's behavior
- [ ] **Integration impact assessed**: Changes to the shared module do not break assumptions made by consuming contexts
- [ ] **Cross-context regression tested**: If exploratory testing sessions were run, shared-module interactions were included in the cross-story interaction charter

### Output Format

Document the shared-module review as a section in the UAT test plan:

```
### Shared-Module Review <!-- retro c8f2 -->

**Shared modules identified**: [count]

| Module Path | Stages Referencing | Modified in Dev | Test Coverage | Status |
|---|---|---|---|---|
| [path] | [stage list] | Yes/No | [coverage description] | PASS/FAIL/N/A |

**Findings**: [any gaps or risks identified]
```

If no shared modules were modified during Development, document: "No shared modules modified -- review not applicable."

---

## Sub-Agent Interface

### Input (from Product-Owner or user)

The sub-agent accepts context in this JSON-compatible structure when receiving output from the Product-Owner skill:

```json
{
  "feature": "Feature name",
  "user_stories": [
    {
      "id": "US-001",
      "title": "Story title",
      "acceptance_criteria": ["AC1", "AC2", "AC3"]
    }
  ],
  "constraints": ["Performance: < 200ms response", "Accessibility: WCAG 2.1 AA"],
  "risk_areas": ["Payment processing", "Data migration"],
  "technology_stack": ["Python 3.12", "FastAPI", "PostgreSQL"]
}
```

When this structured input is available, the sub-agent should derive test cases from acceptance criteria and align test strategy with the stated risk areas.

### Output

The sub-agent returns structured markdown matching the Output Contract for the task type (see above). The main agent passes this through to the user without modification.

---

## User Commands

| Command | Action |
|---|---|
| `strategy` | Generate a test strategy for the current feature or system |
| `cases` | Design test cases for the current feature or acceptance criteria |
| `automate` | Produce an automation strategy for the current test scope |
| `metrics` | Generate a quality metrics dashboard or analysis |
| `regression` | Build a regression test plan for the current release |
| `explore` | Create exploratory testing charters for the current feature |
| `accept` | Finalize -- write any pending test artifacts to disk |

---

## References

- `references/test-strategy.md` -- Test pyramid, risk-based testing, shift-left, test types taxonomy, entry/exit criteria
- `references/test-case-patterns.md` -- Equivalence partitioning, boundary analysis, decision tables, state transitions, Given-When-Then format
- `references/test-automation.md` -- Automation pyramid, framework selection, CI/CD integration, flaky test management, mocking strategies
- `references/quality-metrics.md` -- Defect density, coverage metrics, escape rate, MTTR/MTTF, quality gates, cost of quality
- `references/empirical-validation.md` -- Empirical validation registry: technology-specific patterns requiring runtime verification, keyword detection, severity classification, recommended validation tools
- `references/exploratory-testing.md` -- Session-based exploratory testing: SBET charters, HICCUPPS heuristics, tour-based exploration, cross-story regression detection, game-specific patterns
- `references/milestone-testing.md` -- Milestone validation protocols by project type: Web/React, API/Backend, Enterprise/B2B, Mobile, CLI with role-specific checklists and critical path testing
- `references/security-scanning.md` -- Inline security scanning: secrets detection, injection patterns, XSS, path traversal, language-specific patterns
