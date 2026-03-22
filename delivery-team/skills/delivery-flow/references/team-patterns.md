# Team Collaboration Patterns

## Decision Matrix: When to Use Each Pattern

Select the collaboration pattern based on the situation. Multiple patterns may apply to a single stage -- they execute in the order listed below (evaluator-optimizer first, then adversarial, then review board if applicable).

| Situation | Pattern | Rationale |
|-----------|---------|-----------|
| After any stage produces an artifact | Evaluator-Optimizer | Catch quality issues before DoD validation |
| Requirements or design decisions with assumptions | Adversarial Review | Challenge assumptions, find blind spots, stress-test completeness |
| Go/no-go or multi-domain decisions | Multi-Perspective Review Board | Multiple expert perspectives needed for high-stakes decisions |
| Mid-stage question crossing domain boundaries | Decision Ownership Routing | Route to the right expert, avoid bottlenecks and uninformed decisions |
| Technology or architecture trade-offs with two valid options | Debate | Structured argumentation produces better-reasoned decisions |
| Cross-team alignment requiring buy-in from all parties | Consensus | Sprint plans, release scope, and shared commitments need mutual agreement |

---

## Pattern 1: Evaluator-Optimizer Loop

### When to Use

After any stage produces its primary artifact, before Team DoD validation. This is the first quality pass -- it catches obvious issues cheaply before invoking the full validator panel.

### Protocol

1. Primary agent produces the artifact.
2. Evaluator agent receives:
   - The artifact
   - The quality gate criteria for this stage (from quality-gates.md)
   - Instruction to evaluate each criterion strictly as PASS or FAIL with explanation
3. If all criteria PASS: proceed to Team DoD validation.
4. If any criteria FAIL: construct feedback and route back to primary agent:
   - Include the artifact, the failing criteria, and specific actionable feedback
   - Each piece of feedback must reference the exact section that fails and state what change is needed
5. Primary agent revises the artifact, addressing each failing criterion explicitly.
6. Re-evaluate (repeat from step 2).
7. Maximum iterations: 3 (or stage-specific override from quality-gates.md).
8. If still failing after max iterations: escalate to human with all attempts shown.

### Key Principle

The evaluator is not the same agent as the producer. Even when both are driven by the same underlying model, the separation of roles (produce vs. evaluate) with distinct prompts produces meaningfully better results than self-review.

### Evaluator Agent Prompt Template

```
You are a quality evaluator for the [STAGE NAME] stage.
Evaluate this artifact against the following criteria:

[CRITERIA LIST from quality-gates.md for this stage]

For each criterion:
- State PASS or FAIL
- If FAIL: quote the specific section that fails, explain WHY it fails
  (not just that it does), and provide an actionable fix that the author
  can implement without further clarification

Do not be lenient. Apply the criteria as written. A vague or partially
addressed criterion is a FAIL.

Artifact to evaluate:
---
[ARTIFACT CONTENT]
---
```

---

## Pattern 2: Adversarial Review (Red Team / Devil's Advocate)

### When to Use

- Stage 2 (Refine): Challenge requirements completeness, hidden assumptions, and missing personas
- Stage 4 (Architect): Challenge design decisions, trade-offs, failure mode coverage, and security posture
- Stage 5 (Plan): Challenge estimates, risk assessments, and capacity assumptions

### Protocol

1. Primary artifact is complete and has passed the evaluator-optimizer loop.
2. Spawn challenger agent with explicit adversarial instruction.
3. Challenger produces:
   - **Challenged assumptions**: Each assumption identified, with the consequence if it is wrong
   - **Missing edge cases**: Scenarios not considered that could cause failures
   - **Alternative approaches**: Other ways to solve the problem, with trade-offs
   - **Unaddressed risks**: What could go wrong that is not mitigated
   - **Confidence rating (1-5)**: Overall assessment of production-readiness
4. If confidence is 2 or below: **dynamic escalation to human immediately**, regardless of pipeline position.
5. If confidence is 3-5: primary agent receives the challenger output and must:
   - Address each challenged assumption: accept the challenge and revise, or rebut with specific reasoning
   - Add missing edge cases to the artifact, or explain why they are explicitly out of scope
   - Acknowledge alternative approaches and document why the chosen approach is preferred for this context
   - Address unaddressed risks with mitigation or acceptance rationale
6. Revised artifact incorporates all valid challenges. Invalid challenges are rebutted with reasoning preserved in the artifact (as ADR-style rationale or inline notes).

### Confidence Rating Scale

- **5**: Production-ready. No significant concerns. Challenger found only minor suggestions.
- **4**: Minor concerns that are addressable without rework. Solid foundation.
- **3**: Moderate concerns. Some areas need revision, but the overall direction is sound.
- **2**: Significant concerns. Major revision or rethinking needed. ESCALATE.
- **1**: Fundamental issues with the approach. Reconsider entirely. ESCALATE.

### Challenger Agent Prompt Template

```
You are a devil's advocate. Your job is to stress-test this artifact by
finding weaknesses, blind spots, and risks. You are NOT being helpful --
you are trying to break this.

Be SPECIFIC for every issue you raise. Generic criticism is useless.

1. **Challenged assumptions**: What assumptions does this artifact make?
   For each: what happens if the assumption is wrong?
2. **Missing edge cases**: What scenarios are not addressed? What inputs,
   states, or conditions could cause failure?
3. **Risks**: What could go wrong that is not mitigated? Consider
   technical, business, operational, and security risks.
4. **Alternatives**: What other approaches exist? For each, state why it
   might be better and what trade-off the current approach is making.
5. **Confidence rating (1-5)**: How production-ready is this artifact?
   State your rating and justify it in 2-3 sentences.

Cite exact sections of the artifact. Do not provide generic criticism.
If you cannot find issues, state that explicitly -- do not invent problems.

Artifact to challenge:
---
[ARTIFACT CONTENT]
---
```

---

## Pattern 3: Multi-Perspective Review Board

### When to Use

- Stage 3 (Design): Before advancing to Architect, to ensure the design is feasible, valuable, and testable
- Stage 7 (UAT): Go/no-go decision before release

### Protocol

1. Identify 3 specialist reviewers based on the artifact type:
   - **Technical Reviewer** (Architect skill): Evaluates feasibility, scalability, maintainability, and technical debt risk
   - **Business Reviewer** (Product Owner via product-delivery): Evaluates value alignment, user need coverage, scope adherence, and market fit
   - **Risk Reviewer** (QA Engineer + Security): Evaluates quality risks, test coverage gaps, security vulnerabilities, and compliance concerns
2. Spawn each reviewer sequentially. Each receives:
   - The artifact
   - Role-specific evaluation criteria
   - Instruction to vote RECOMMEND or BLOCK
3. Each reviewer produces:
   - Findings with severity: **Critical** (must fix), **Warning** (should fix), **Suggestion** (nice to have)
   - Vote: **RECOMMEND** (artifact is acceptable from this perspective) or **BLOCK** (artifact has issues that must be resolved)
   - If BLOCK: the specific concern that must be resolved, stated as a clear requirement
4. Synthesis:
   - **Any BLOCK**: Route the blocking concern to the Decision Owner for that domain (see Pattern 4). Decision Owner attempts resolution.
   - Decision Owner resolves the concern: re-run only the blocking reviewer to verify resolution.
   - **All RECOMMEND**: Proceed to the next stage.
5. If a BLOCK cannot be resolved after Decision Owner attempt: escalate to human with the blocking concern, the Decision Owner's analysis, and suggested options.

### Reviewer Prompt Template

```
You are reviewing this [ARTIFACT TYPE] from a [PERSPECTIVE] perspective.

Evaluate against these criteria:
[ROLE-SPECIFIC CRITERIA]

Produce:
1. Findings with severity (Critical / Warning / Suggestion) -- be specific,
   cite sections, explain impact
2. Vote: RECOMMEND or BLOCK
3. If BLOCK: state the SPECIFIC concern that must be resolved before
   proceeding. Frame it as a requirement, not a question.

Do not BLOCK for Suggestions or minor Warnings. BLOCK only for Critical
findings or Warning clusters that collectively indicate a systemic issue.

Artifact:
---
[ARTIFACT CONTENT]
---
```

---

## Pattern 4: Decision Ownership Routing

### When to Use

At any point during pipeline execution when a decision must be made that falls outside the primary agent's domain expertise. Common triggers:

- Self-correction identifies an issue the primary agent lacks expertise to resolve
- DoD validator raises a concern in another domain
- Mid-stage question arises that requires specialized judgment
- Two agents disagree and a domain expert must arbitrate

### Routing Matrix

| Issue Type | Signal Keywords | Decision Owner | Skill |
|-----------|----------------|----------------|-------|
| Scope and value | "should we include", "MVP", "nice-to-have", "user value", "priority", "cut scope" | Product Owner | product-delivery |
| Technical feasibility | "can we build", "performance", "scalability", "architecture", "tech debt" | Architect | architect |
| Quality and risk | "test coverage", "regression risk", "quality trade-off", "defect severity" | QA Engineer | quality |
| Process and timeline | "sprint capacity", "velocity", "deadline", "ceremony", "estimate", "burndown" | Scrum Master | product-delivery |
| Data and metrics | "how to measure", "analytics", "KPI", "baseline", "A/B test", "experiment design" | Data Analyst | product-delivery |
| Security and compliance | "security concern", "compliance", "GDPR", "audit", "vulnerability", "threat model" | Compliance Officer | architect |
| UX and usability | "user experience", "usability", "accessibility", "flow", "confusing", "friction" | UX Designer | ui |
| Deployment and infra | "deploy", "infrastructure", "CI/CD", "environment", "scaling", "rollback" | DevOps | operations |

### Protocol

1. Issue arises during stage execution. Source can be: self-correction loop, DoD validation, adversarial review, or explicit agent output.
2. Classify issue type using signal keywords from the routing matrix.
3. Spawn Decision Owner sub-agent with:
   - The issue description (what decision is needed)
   - Relevant context: current artifact, upstream artifacts, pipeline state, constraints
   - Request for a decision with rationale
4. Decision Owner produces:
   - **Decision**: Clear statement of the chosen path
   - **Rationale**: Why this decision, citing specific context and trade-offs
   - **Conditions**: Under what circumstances this decision should be revisited
   - **Caveats**: Risks accepted or deferred by this decision
5. Record the decision in pipeline state for downstream visibility and future reference.
6. If the Decision Owner cannot make a confident decision (insufficient information, equal trade-offs, or out of their domain): escalate to human with the decision context, options analyzed, and the Decision Owner's analysis.

### Multi-Signal Conflicts

When an issue matches multiple signal categories:

- Use the **most specific** match (e.g., "GDPR compliance for the login flow" matches Security/Compliance, not UX)
- If genuinely cross-cutting, route to the Decision Owner whose domain has the highest impact if the decision is wrong
- Include the other relevant Decision Owners as reviewers of the decision (they can flag concerns but the primary owner decides)

---

## Pattern 5: Debate Pattern

### When to Use

- Stage 4 (Architect): Technology choices, architecture style decisions, build vs. buy, framework selection
- Any point where two or more valid approaches exist and the choice has significant downstream consequences
- When the team needs a documented record of why a particular path was chosen (ADR generation)

### Protocol

1. **Frame the debate**: "[Option A] vs [Option B] for [specific context and constraints]"
   - The framing must include project constraints, NFRs, team capabilities, and timeline -- generic debates are not useful
2. Spawn **PRO agent** (argues for Option A):
   - Must provide 3 or more specific arguments grounded in this project's context (not generic advantages)
   - Must address how the risks of Option A are mitigated in this context
   - Must explain why Option B is worse for this specific situation
3. Spawn **CON agent** (argues for Option B):
   - Same requirements as PRO but reversed -- argues for Option B, against Option A
   - Must not simply mirror the PRO arguments -- must present independent reasoning
4. Spawn **JUDGE agent** (Enterprise Architect or senior technical role):
   - Receives both arguments plus the full project constraints
   - Decides with documented rationale, citing the specific arguments that were most compelling
   - States conditions under which the decision should be revisited (e.g., "if traffic exceeds 10K RPS, reconsider")
   - If arguments are equally compelling and no clear winner exists: returns DEADLOCK and escalates to human
5. Produce an Architecture Decision Record (ADR) from the debate outcome:
   - Title, context, decision, consequences (positive and negative), revisit conditions

### PRO Agent Template

```
Argue in favor of [OPTION A] for this project.

Context:
- Project type: [TYPE]
- Key constraints: [CONSTRAINTS]
- NFRs: [NFRS]
- Team: [TEAM SIZE, EXPERIENCE, FAMILIARITY]
- Timeline: [TIMELINE]

Provide:
1. At least 3 specific advantages of [OPTION A] for THIS project
   (not generic advantages -- why does it matter HERE?)
2. Evidence or precedent for each advantage (prior projects, benchmarks,
   documented case studies, or first-principles reasoning)
3. How the known risks of [OPTION A] are mitigated in this context
4. Why [OPTION B] is worse for THIS specific situation (cite specific
   constraints or requirements that make it less suitable)
```

### CON Agent Template

```
Argue in favor of [OPTION B] for this project.

Context:
- Project type: [TYPE]
- Key constraints: [CONSTRAINTS]
- NFRs: [NFRS]
- Team: [TEAM SIZE, EXPERIENCE, FAMILIARITY]
- Timeline: [TIMELINE]

Provide:
1. At least 3 specific advantages of [OPTION B] for THIS project
2. Evidence or precedent for each advantage
3. How the known risks of [OPTION B] are mitigated in this context
4. Why [OPTION A] is worse for THIS specific situation
```

### JUDGE Agent Template

```
Decide between two options based on the arguments presented.

Option A arguments:
---
[PRO OUTPUT]
---

Option B arguments:
---
[CON OUTPUT]
---

Project constraints:
[CONSTRAINTS, NFRS, TEAM, TIMELINE]

Produce:
1. **Decision**: A or B
2. **Rationale**: Cite the specific arguments that were most compelling
   and explain why they outweigh the counterarguments
3. **Revisit conditions**: Under what circumstances should this decision
   be reconsidered? Be specific (thresholds, events, timelines)
4. **Risks to monitor**: What risks come with the chosen approach that
   need active monitoring?
5. If you truly cannot decide: state "DEADLOCK" and explain precisely
   why the arguments are equally compelling -- what additional information
   would break the tie?
```

---

## Pattern 6: Consensus Protocol

### When to Use

- Stage 5 (Plan): Aligning Scrum Master, Product Owner, QA Engineer, and DevOps on sprint plan, scope, estimates, and deployment strategy
- Any cross-cutting decision that affects multiple domains simultaneously and requires buy-in from all parties (not just a single Decision Owner)
- Release planning, capacity allocation, and cross-team coordination

### Why Consensus Instead of Decision Ownership

Decision Ownership routes to one expert. Consensus is used when no single expert can make the decision alone because it genuinely spans multiple domains and all parties must commit to the outcome. Sprint planning is the canonical example: the PO sets priority, the SM guards capacity, the QA validates test feasibility, and DevOps confirms deployment readiness. All four must agree for the plan to be realistic.

### Protocol

**Round 1 -- Independent Analysis:**

- Each participating agent independently analyzes the topic
- Each produces: position, reasoning, concerns, and estimate (if applicable)
- No agent sees another agent's output during Round 1
- This independence prevents anchoring bias

**Round 2 -- Review and Respond:**

- Each agent receives ALL other agents' Round 1 outputs
- Each responds with:
  - Areas of agreement (cite specific points from other agents)
  - Areas of disagreement (with reasoning -- not just "I disagree" but why)
  - Revised position if their view has changed after seeing other perspectives
  - What remains unresolved from their perspective

**Round 3 -- Convergence (only if disagreements remain after Round 2):**

- Orchestrator identifies the specific points of contention from Round 2
- Each agent provides a final position on ONLY the contested points
- Responses must be short and focused -- no restating of agreed positions
- Each agent must explicitly state whether they can ACCEPT the emerging consensus even if it differs from their initial position

**Synthesis:**

- If consensus reached (all agents agree or all agents explicitly accept a compromise): record the agreed position as the decision, noting any conditions or caveats
- If not (any agent cannot accept): present the unresolved disagreement to the human with:
  - Each agent's final position and reasoning
  - What was agreed upon (partial consensus)
  - What specifically remains contested
  - The orchestrator's assessment of why consensus failed

### Consensus Agent Template (Round 1)

```
You are the [ROLE] on the delivery team. Independently analyze this topic:

[TOPIC DESCRIPTION]
[RELEVANT CONTEXT: upstream artifacts, constraints, timeline]

Provide:
1. Your position on the topic (clear statement)
2. Your reasoning (cite specific concerns from YOUR domain -- not generic)
3. Risks you see from your perspective
4. Your estimate if applicable (effort, timeline, or scope)
5. Assumptions you are making (state them explicitly so others can challenge)

Be honest about uncertainty. If you lack information to form a confident
position, say so and state what information you would need.
```

### Consensus Agent Template (Round 2)

```
Review your teammates' positions and respond.

Your Round 1 position:
---
[YOUR ROUND 1 OUTPUT]
---

Teammate positions:
---
[ALL OTHER AGENTS' ROUND 1 OUTPUTS, labeled by role]
---

Respond:
1. Where do you agree? (cite specific points from specific teammates)
2. Where do you disagree? (explain WHY -- what does your domain expertise
   tell you that conflicts with their position?)
3. Has your position changed after seeing other perspectives? If so,
   state your revised position and what changed your mind.
4. What remains unresolved? (specific points, not vague concerns)
```

### Consensus Agent Template (Round 3 -- Convergence)

```
Final round. Address ONLY the contested points below.

Contested points:
[LIST OF SPECIFIC UNRESOLVED ITEMS FROM ROUND 2]

For each contested point:
1. Your final position (brief)
2. Can you ACCEPT the emerging group position even if it differs from yours?
   (Yes/No -- if No, state what would need to change for you to accept)
```

---

## Pattern Sequencing Within a Stage

When multiple patterns apply to a single stage, execute them in this order:

1. **Evaluator-Optimizer Loop** -- ensures baseline quality before expensive patterns
2. **Adversarial Review** -- stress-tests the artifact after it passes basic quality
3. **Debate** -- resolves specific technical decisions surfaced during prior patterns
4. **Multi-Perspective Review Board** -- final multi-domain assessment
5. **Consensus** -- alignment across team on cross-cutting decisions
6. **Team DoD Validation** -- final gate before stage advancement

Decision Ownership Routing can trigger at ANY point in this sequence when a domain-specific question arises. It is not a sequenced pattern but a routing mechanism.

Not every stage uses every pattern. The stage routing matrix in project-types.md determines which stages are active, and the stage definition determines which patterns are invoked. The decision matrix at the top of this document maps situations to patterns.
