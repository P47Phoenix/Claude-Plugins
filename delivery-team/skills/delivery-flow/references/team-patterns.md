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

**Dispatch rule**: Dispatch the producer and the evaluator as SEPARATE Agent tool calls. One role = one sub-agent invocation. Never collapse "produce and self-evaluate" into a single compound prompt.

### When to Use

After any stage produces its primary artifact, before Team DoD validation. This is the first quality pass -- it catches obvious issues cheaply before invoking the full validator panel.

### Dispatch: Sequential

This pattern is inherently sequential (produce, evaluate, revise, re-evaluate). No parallelism within this pattern.

### Protocol

1. Primary agent produces the artifact and writes it to its namespaced output path.
2. Evaluator agent receives:
   - The artifact FILE PATH (not content) -- evaluator reads it from disk
   - The quality gate criteria for this stage (from quality-gates.md)
   - Instruction to evaluate each criterion strictly as PASS or FAIL with explanation
3. Evaluator writes findings to: `{stage}/qa-evaluator/evaluation-round-{N}.md`
4. If all criteria PASS: proceed to Team DoD validation.
5. If any criteria FAIL: route back to primary agent with:
   - The artifact file path (agent re-reads its own work)
   - The findings file path (agent reads evaluator feedback)
   - Task description: "Revise your artifact to address the findings. Read both files."
6. Primary agent revises the artifact, addressing each failing criterion explicitly.
7. Re-evaluate (repeat from step 2).
8. Maximum iterations: 3 (or stage-specific override from quality-gates.md).
9. If still failing after max iterations: escalate to human with all finding file paths shown.

### Key Principle

The evaluator is not the same agent as the producer. Even when both are driven by the same underlying model, the separation of roles (produce vs. evaluate) with distinct prompts produces meaningfully better results than self-review.

### Evaluator Agent Prompt Template

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {evaluator_skill}
TASK_TYPE: evaluation
ROLE: qa-evaluator

Begin your response with "SKILL_LOADED: {evaluator_skill}" to confirm skill activation.

--- TASK ---
Evaluate the artifact against the following criteria. For each criterion,
state PASS or FAIL. If FAIL: quote the specific section that fails, explain
WHY it fails (not just that it does), and provide an actionable fix that the
author can implement without further clarification. Do not be lenient. Apply
the criteria as written. A vague or partially addressed criterion is a FAIL.

--- INPUT ARTIFACTS (read these files) ---
- {artifact_file_path}: The artifact to evaluate
- {quality_gates_path}: Gate criteria for this stage

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}
{stage_lessons_if_loaded}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your findings to: {stage}/qa-evaluator/evaluation-round-{N}.md

When complete, respond with ONLY this signal block:
STATUS: {DONE | NOT_DONE}
ARTIFACT: {stage}/qa-evaluator/evaluation-round-{N}.md
SUMMARY: {one sentence, max 200 characters}
{if NOT_DONE: FINDINGS: {bullet list of specific failures}}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

---

## Pattern 2: Adversarial Review (Red Team / Devil's Advocate)

**Dispatch rule**: Dispatch the challenger as a SEPARATE Agent tool call from the producer. One role = one sub-agent invocation. Never ask the producer to "also challenge its own work". For multi-loop adversarial review, use the **Isolated Adversarial Loop** variant (Pattern 2b) — each loop is a fresh sub-agent with no prior-loop context.

### When to Use

- Stage 2 (Refine): Challenge requirements completeness, hidden assumptions, and missing personas
- Stage 4 (Architect): Challenge design decisions, trade-offs, failure mode coverage, and security posture
- Stage 5 (Plan): Challenge estimates, risk assessments, and capacity assumptions

### Dispatch: Sequential

Adversarial review runs sequentially after the evaluator-optimizer loop. The challenger is a single agent.

### Isolation Note

Challenger receives ONLY the artifact file path. No production conversation, no evaluator-optimizer history, no orchestrator reasoning. This strict isolation ensures the challenger forms an independent judgment unconditioned by how the artifact was produced or evaluated.

### Protocol

1. Primary artifact is complete and has passed the evaluator-optimizer loop.
2. Spawn challenger agent with explicit adversarial instruction. Challenger receives ONLY:
   - The artifact file path (challenger reads it from disk)
   - The adversarial template
   - Gate criteria for this stage
3. Challenger writes findings to: `{stage}/challenger/challenge.md`
4. Challenger produces:
   - **Challenged assumptions**: Each assumption identified, with the consequence if it is wrong
   - **Missing edge cases**: Scenarios not considered that could cause failures
   - **Alternative approaches**: Other ways to solve the problem, with trade-offs
   - **Unaddressed risks**: What could go wrong that is not mitigated
   - **Confidence rating (1-5)**: Overall assessment of production-readiness
5. If confidence is 2 or below: **dynamic escalation to human immediately**, regardless of pipeline position.
6. If confidence is 3-5: primary agent receives the artifact file path + challenge file path and must:
   - Address each challenged assumption: accept the challenge and revise, or rebut with specific reasoning
   - Add missing edge cases to the artifact, or explain why they are explicitly out of scope
   - Acknowledge alternative approaches and document why the chosen approach is preferred for this context
   - Address unaddressed risks with mitigation or acceptance rationale
7. Revised artifact incorporates all valid challenges. Invalid challenges are rebutted with reasoning preserved in the artifact (as ADR-style rationale or inline notes).

### Confidence Rating Scale

- **5**: Production-ready. No significant concerns. Challenger found only minor suggestions.
- **4**: Minor concerns that are addressable without rework. Solid foundation.
- **3**: Moderate concerns. Some areas need revision, but the overall direction is sound.
- **2**: Significant concerns. Major revision or rethinking needed. ESCALATE.
- **1**: Fundamental issues with the approach. Reconsider entirely. ESCALATE.

### Challenger Agent Prompt Template

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {challenger_skill}
TASK_TYPE: adversarial-review
ROLE: challenger

Begin your response with "SKILL_LOADED: {challenger_skill}" to confirm skill activation.

--- TASK ---
You are a devil's advocate. Your job is to stress-test this artifact by
finding weaknesses, blind spots, and risks. You are NOT being helpful --
you are trying to break this.

Be SPECIFIC for every issue you raise. Generic criticism is useless.

1. Challenged assumptions: What assumptions does this artifact make?
   For each: what happens if the assumption is wrong?
2. Missing edge cases: What scenarios are not addressed? What inputs,
   states, or conditions could cause failure?
3. Risks: What could go wrong that is not mitigated? Consider
   technical, business, operational, and security risks.
4. Alternatives: What other approaches exist? For each, state why it
   might be better and what trade-off the current approach is making.
5. Confidence rating (1-5): How production-ready is this artifact?
   State your rating and justify it in 2-3 sentences.

Cite exact sections of the artifact. Do not provide generic criticism.
If you cannot find issues, state that explicitly -- do not invent problems.

--- INPUT ARTIFACTS (read these files) ---
- {artifact_file_path}: The artifact to challenge

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your findings to: {stage}/challenger/challenge.md

When complete, respond with ONLY this signal block:
STATUS: {RECOMMEND | BLOCK}
ARTIFACT: {stage}/challenger/challenge.md
SUMMARY: {one sentence, max 200 characters}
FINDINGS: {bullet list of key challenges}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

---

## Pattern 2b: Isolated Adversarial Loop

**Dispatch rule**: Each loop iteration dispatches a FRESH sub-agent with zero prior-loop context. One loop = one Agent tool call. Never paste prior findings into a new reviewer's prompt.

### When to Use

- Stage 4 (Architect) — when the artifact's correctness depends on surfacing
  deep structural issues that a single reviewer pass can anchor away
- Any time the single-pass Adversarial Review (Pattern 2) has produced a
  suspicious "clean" result on the first try
- Whenever `pipeline.collaboration_patterns` includes `adversarial` and the
  current stage is marked to use the isolated variant

### Core Guarantee: Fresh Context Every Loop

The whole point of this variant is that a single fresh reviewer's clean pass
**proves nothing** about convergence. Fresh reviewers produce non-monotonic
critique sets — loop N+1 may raise an entirely disjoint set of issues that
loop N had no context for. See ADR-003 for the rationale.

Therefore:

- Every reviewer dispatch is a fresh sub-agent whose prompt contains **only**
  the current artifact and the reviewer brief + taxonomy.
- **NO** prior findings. **NO** "this is loop N". **NO** fix summaries.
- The Architect revision sub-agent sees the **current** loop's findings only,
  not prior loops' findings, to prevent compound patching against contradictory
  priorities.

### Issue Class Taxonomy

Reviewers MUST tag each finding with exactly one class from this fixed taxonomy:

```
coupling | security | data-integrity | naming | testability | performance | docs
```

Untagged or invalid-tag findings are bucketed as `misc` and counted as a new
class (conservative — prevents taxonomy evasion).

### Convergence Rules (ADR-003)

Terminate the loop when ANY of the following holds:

1. **Two-clean rule**: Two *consecutive* loops return zero findings.
   Exit `converged (two_clean)`.
2. **No-new-classes rule**: Two *consecutive* loops produce findings, but
   every finding in each belongs to an issue class raised in an earlier loop.
   Exit `converged (class_saturated)`. Residuals documented.
3. **Hard cap**: `N >= pipeline.max_self_correction` (default 3). Exit
   `cap_reached`. Residuals documented and surfaced to the human checkpoint.

A single zero-finding loop is **not** sufficient. A clean pass at N=1 with
no prior clean loop does NOT exit — it re-runs the reviewer on the same
artifact to seek the second consecutive clean.

`cap_reached` is a **documented exit**, not a failure. The human checkpoint
decides whether residuals are acceptable or require manual remediation.

### Loop Protocol Pseudocode

```
function isolated_adversarial_loop(artifact, max_iter):
    loops = []
    N = 0
    while N < max_iter:
        N += 1

        # Loop 1 (and every subsequent loop): FRESH sub-agent.
        # Prompt contains ONLY the current artifact plus the reviewer brief
        # and taxonomy. NO prior findings. NO loop number. NO fix summaries.
        reviewer = dispatch_fresh_subagent(
            role="adversarial_reviewer",
            inputs=[artifact, reviewer_brief, taxonomy],
            context_leak=False,
        )
        findings = reviewer.return_findings()   # [{issue, class}, ...]
        classes  = { f.class for f in findings }
        loops.append({"findings": findings, "classes": classes, "N": N})

        # Rule 1: two-clean
        if len(findings) == 0:
            if len(loops) >= 2 and len(loops[-2]["findings"]) == 0:
                return {"status": "converged", "reason": "two_clean", "loops": loops}
            # Single clean loop: keep going, do NOT exit.
            # Architect has nothing to fix; re-dispatch reviewer on same artifact.
            continue

        # Rule 2: no-new-classes (track issue CLASSES across loops)
        if len(loops) >= 3:
            prior_union_before_prev = union(l["classes"] for l in loops[:-2])
            prior_union_before_curr = union(l["classes"] for l in loops[:-1])
            prev_classes    = loops[-2]["classes"]
            current_classes = loops[-1]["classes"]
            if (prev_classes.issubset(prior_union_before_prev) and
                current_classes.issubset(prior_union_before_curr)):
                document_residuals(findings)
                return {"status": "converged", "reason": "class_saturated",
                        "loops": loops}

        # Otherwise: Architect (fresh dispatch) revises artifact.
        # Architect sees CURRENT findings only, not prior loops.
        artifact = dispatch_fresh_subagent(
            role="architect_revise",
            inputs=[artifact, findings],
        ).revised_artifact()

    # Rule 3: hard cap — documented exit, not a failure.
    document_residuals(loops[-1]["findings"])
    return {"status": "cap_reached", "loops": loops}
```

### Invariants

- **Reviewer context isolation**: every reviewer dispatch is a fresh sub-agent
  with zero prior-loop context. Enforced by the dispatch wrapper and audited
  by the compound-role detector in `audit_agent_prompt.py`.
- **Architect context scoping**: the Architect revision sub-agent sees the
  **current** loop's findings only, not prior loops' findings.
- **Cap-reached is a documented exit**, not a failure. Human checkpoint decides
  whether to accept residuals.
- **N=1 clean pass** continues to N=2 with the same artifact. A clean first
  pass proves nothing.

See ADR-003 for the full decision record.

---

## Pattern 3: Multi-Perspective Review Board

**Dispatch rule**: Dispatch each reviewer as a SEPARATE Agent tool call, all in parallel in a single message. Three reviewers = three Agent calls. Never fuse two reviewers into one compound prompt.

### When to Use

- Stage 3 (Design): Before advancing to Architect, to ensure the design is feasible, valuable, and testable
- Stage 7 (UAT): Go/no-go decision before release

### Dispatch: PARALLEL

ALL reviewers run in parallel using multiple Agent calls in a single message. No reviewer sees another's output. Each reviewer writes to its own file in `{stage}/review-board/`. The orchestrator gathers signals only -- it does not read or relay artifact content between reviewers.

### Protocol

1. Identify 3 specialist reviewers based on the artifact type:
   - **Technical Reviewer** (Architect skill): Evaluates feasibility, scalability, maintainability, and technical debt risk
   - **Business Reviewer** (Product Owner via product-delivery): Evaluates value alignment, user need coverage, scope adherence, and market fit
   - **Risk Reviewer** (QA Engineer + Security): Evaluates quality risks, test coverage gaps, security vulnerabilities, and compliance concerns
2. Dispatch ALL reviewers in parallel (single message with N Agent calls). Each receives:
   - The artifact FILE PATH (not content) -- reviewer reads it from disk
   - Role-specific evaluation criteria
   - Instruction to vote RECOMMEND or BLOCK
   - No reviewer's prompt references any other reviewer
3. Each reviewer writes to: `{stage}/review-board/{role}-review.md`
4. Each reviewer produces:
   - Findings with severity: **Critical** (must fix), **Warning** (should fix), **Suggestion** (nice to have)
   - Vote: **RECOMMEND** (artifact is acceptable from this perspective) or **BLOCK** (artifact has issues that must be resolved)
   - If BLOCK: the specific concern that must be resolved, stated as a clear requirement
5. Orchestrator gathers signals (STATUS, FINDINGS) from all reviewers. Does not read review content.
6. Synthesis:
   - **Any BLOCK**: Route the blocking concern to the Decision Owner for that domain (see Pattern 4). Decision Owner receives the blocking review file path + artifact file path.
   - Decision Owner resolves the concern: re-run only the blocking reviewer to verify resolution.
   - **All RECOMMEND**: Proceed to the next stage.
7. If a BLOCK cannot be resolved after Decision Owner attempt: escalate to human with the blocking review file path, the Decision Owner's analysis file path, and suggested options.

### Reviewer Prompt Template

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {reviewer_skill}
TASK_TYPE: review
ROLE: {reviewer_role}

Begin your response with "SKILL_LOADED: {reviewer_skill}" to confirm skill activation.

--- TASK ---
You are reviewing this artifact from a {perspective} perspective.
Evaluate against the criteria below. Produce findings with severity
(Critical / Warning / Suggestion) -- be specific, cite sections, explain
impact. Vote RECOMMEND or BLOCK. If BLOCK: state the SPECIFIC concern that
must be resolved before proceeding. Frame it as a requirement, not a question.
Do not BLOCK for Suggestions or minor Warnings. BLOCK only for Critical
findings or Warning clusters that collectively indicate a systemic issue.

--- INPUT ARTIFACTS (read these files) ---
- {artifact_file_path}: The artifact to review

--- GATE CRITERIA ---
{role_specific_criteria}

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your review to: {stage}/review-board/{role}-review.md

When complete, respond with ONLY this signal block:
STATUS: {RECOMMEND | BLOCK}
ARTIFACT: {stage}/review-board/{role}-review.md
SUMMARY: {one sentence, max 200 characters}
{if BLOCK: FINDINGS: {bullet list of blocking concerns}}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

---

## Pattern 4: Decision Ownership Routing

**Dispatch rule**: The Decision Owner is a SEPARATE Agent tool call dispatched on demand. One role = one sub-agent invocation. Never ask another agent to "also make this decision".

### When to Use

At any point during pipeline execution when a decision must be made that falls outside the primary agent's domain expertise. Common triggers:

- Self-correction identifies an issue the primary agent lacks expertise to resolve
- DoD validator raises a concern in another domain
- Mid-stage question arises that requires specialized judgment
- Two agents disagree and a domain expert must arbitrate

### Dispatch: On-demand (single agent)

Decision Ownership is not a sequenced pattern but a routing mechanism. The Decision Owner is always a single agent invoked on demand, already isolated by nature.

### Isolation Note

Decision Owner receives the issue description + relevant artifact file paths. Not artifact content, not discussion history. The Decision Owner reads artifacts from disk to form an independent judgment.

### Routing Matrix

| Issue Type | Signal Keywords | Decision Owner | Skill |
|-----------|----------------|----------------|-------|
| Scope and value | "should we include", "MVP", "nice-to-have", "user value", "priority", "cut scope" | Product Owner | product-delivery |
| Technical feasibility | "can we build", "performance", "scalability", "architecture", "tech debt" | Architect | architect |
| Quality and risk | "test coverage", "regression risk", "quality trade-off", "defect severity" | QA Engineer | quality |
| Process and timeline | "sprint capacity", "velocity", "deadline", "ceremony", "estimate", "burndown" | Scrum Bag | product-delivery |
| Data and metrics | "how to measure", "analytics", "KPI", "baseline", "A/B test", "experiment design" | Data Analyst | product-delivery |
| Security and compliance | "security concern", "compliance", "GDPR", "audit", "vulnerability", "threat model" | Compliance Officer | architect |
| UX and usability | "user experience", "usability", "accessibility", "flow", "confusing", "friction" | UX Designer | ui |
| Deployment and infra | "deploy", "infrastructure", "CI/CD", "environment", "scaling", "rollback" | DevOps | operations |

### Protocol

1. Issue arises during stage execution. Source can be: self-correction loop, DoD validation, adversarial review, or explicit agent output.
2. Classify issue type using signal keywords from the routing matrix.
3. Spawn Decision Owner sub-agent using the Agent Invocation Template with:
   - The issue description (what decision is needed)
   - Relevant artifact file paths (Decision Owner reads them from disk)
   - Request for a decision with rationale
4. Decision Owner produces:
   - **Decision**: Clear statement of the chosen path
   - **Rationale**: Why this decision, citing specific context and trade-offs
   - **Conditions**: Under what circumstances this decision should be revisited
   - **Caveats**: Risks accepted or deferred by this decision
5. Decision Owner responds with signal block:
   ```
   STATUS: DONE
   ARTIFACT: {decision_file_path}
   SUMMARY: {one sentence, max 200 characters}
   ```
6. Record the decision in pipeline state for downstream visibility and future reference.
7. If the Decision Owner cannot make a confident decision (insufficient information, equal trade-offs, or out of their domain): escalate to human with the decision context, options analyzed, and the Decision Owner's analysis file path.

### Multi-Signal Conflicts

When an issue matches multiple signal categories:

- Use the **most specific** match (e.g., "GDPR compliance for the login flow" matches Security/Compliance, not UX)
- If genuinely cross-cutting, route to the Decision Owner whose domain has the highest impact if the decision is wrong
- Include the other relevant Decision Owners as reviewers of the decision (they can flag concerns but the primary owner decides)

---

## Pattern 5: Debate Pattern

**Dispatch rule**: Dispatch PRO, CON, and JUDGE as SEPARATE Agent tool calls. PRO + CON in parallel (single message, two Agent calls), JUDGE sequentially after. Three roles = three Agent invocations. Never collapse PRO and CON into one compound prompt.

### When to Use

- Stage 4 (Architect): Technology choices, architecture style decisions, build vs. buy, framework selection
- Any point where two or more valid approaches exist and the choice has significant downstream consequences
- When the team needs a documented record of why a particular path was chosen (ADR generation)

### Dispatch: PRO and CON in PARALLEL, then JUDGE sequential

PRO and CON run in parallel using multiple Agent calls in a single message. Neither sees the other's argument -- this is enforced by parallel dispatch with no cross-references in prompts. JUDGE runs sequentially after both complete, receiving both file paths.

### Protocol

1. **Frame the debate**: "[Option A] vs [Option B] for [specific context and constraints]"
   - The framing must include project constraints, NFRs, team capabilities, and timeline -- generic debates are not useful
2. **Step 1 -- Dispatch PRO + CON in parallel** (single message with 2 Agent calls):
   - **PRO agent** (argues for Option A) writes to: `{stage}/debate-pro/argument.md`
     - Must provide 3 or more specific arguments grounded in this project's context (not generic advantages)
     - Must address how the risks of Option A are mitigated in this context
     - Must explain why Option B is worse for this specific situation
   - **CON agent** (argues for Option B) writes to: `{stage}/debate-con/argument.md`
     - Same requirements as PRO but reversed -- argues for Option B, against Option A
     - Must not simply mirror the PRO arguments -- must present independent reasoning
3. **Step 2 -- Dispatch JUDGE sequentially** after both PRO and CON complete:
   - JUDGE receives: PRO argument file path + CON argument file path + project constraints
   - JUDGE reads both argument files from disk
   - JUDGE writes to: `{stage}/debate-judge/decision.md`
   - Decides with documented rationale, citing the specific arguments that were most compelling
   - States conditions under which the decision should be revisited (e.g., "if traffic exceeds 10K RPS, reconsider")
   - If arguments are equally compelling and no clear winner exists: returns DEADLOCK and escalates to human
4. Produce an Architecture Decision Record (ADR) from the debate outcome:
   - Title, context, decision, consequences (positive and negative), revisit conditions

### PRO Agent Template

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {architect_skill}
TASK_TYPE: debate
ROLE: debate-pro

Begin your response with "SKILL_LOADED: {architect_skill}" to confirm skill activation.

--- TASK ---
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

--- INPUT ARTIFACTS (read these files) ---
- {prd_path}: Product requirements
- {architecture_path}: Current architecture (if available)

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your argument to: {stage}/debate-pro/argument.md

When complete, respond with ONLY this signal block:
STATUS: DONE
ARTIFACT: {stage}/debate-pro/argument.md
SUMMARY: {one sentence, max 200 characters}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

### CON Agent Template

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {architect_skill}
TASK_TYPE: debate
ROLE: debate-con

Begin your response with "SKILL_LOADED: {architect_skill}" to confirm skill activation.

--- TASK ---
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

--- INPUT ARTIFACTS (read these files) ---
- {prd_path}: Product requirements
- {architecture_path}: Current architecture (if available)

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your argument to: {stage}/debate-con/argument.md

When complete, respond with ONLY this signal block:
STATUS: DONE
ARTIFACT: {stage}/debate-con/argument.md
SUMMARY: {one sentence, max 200 characters}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

### JUDGE Agent Template

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {architect_skill}
TASK_TYPE: debate-judge
ROLE: debate-judge

Begin your response with "SKILL_LOADED: {architect_skill}" to confirm skill activation.

--- TASK ---
Decide between two options based on the arguments presented.
Read both argument files from disk. Do not rely on summaries.

Produce:
1. Decision: A or B
2. Rationale: Cite the specific arguments that were most compelling
   and explain why they outweigh the counterarguments
3. Revisit conditions: Under what circumstances should this decision
   be reconsidered? Be specific (thresholds, events, timelines)
4. Risks to monitor: What risks come with the chosen approach that
   need active monitoring?
5. If you truly cannot decide: state "DEADLOCK" and explain precisely
   why the arguments are equally compelling -- what additional information
   would break the tie?

--- INPUT ARTIFACTS (read these files) ---
- {stage}/debate-pro/argument.md: PRO argument (Option A)
- {stage}/debate-con/argument.md: CON argument (Option B)
- {constraints_path}: Project constraints, NFRs, team, timeline

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your decision to: {stage}/debate-judge/decision.md

When complete, respond with ONLY this signal block:
STATUS: {DONE | DEADLOCK}
ARTIFACT: {stage}/debate-judge/decision.md
SUMMARY: {one sentence, max 200 characters}
{if DEADLOCK: FINDINGS: {why arguments are equally compelling}}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

---

## Pattern 6: Consensus Protocol

**Dispatch rule**: Each participant in each round is a SEPARATE Agent tool call, all participants dispatched in parallel within a round. N participants × R rounds = N Agent calls per round. Never collapse two participants into one compound prompt.

### When to Use

- Stage 5 (Plan): Aligning Scrum Bag, Product Owner, QA Engineer, and DevOps on sprint plan, scope, estimates, and deployment strategy
- Any cross-cutting decision that affects multiple domains simultaneously and requires buy-in from all parties (not just a single Decision Owner)
- Release planning, capacity allocation, and cross-team coordination

### Why Consensus Instead of Decision Ownership

Decision Ownership routes to one expert. Consensus is used when no single expert can make the decision alone because it genuinely spans multiple domains and all parties must commit to the outcome. Sprint planning is the canonical example: the PO sets priority, the SM guards capacity, the QA validates test feasibility, and DevOps confirms deployment readiness. All four must agree for the plan to be realistic.

### Dispatch: PARALLEL per round, sequential between rounds

Round 1: ALL participants in PARALLEL with strict isolation. Round 2: ALL participants in PARALLEL with all R1 file paths provided. Round 3 (if needed): ALL participants in PARALLEL with contested points + all R2 file paths. Each participant writes to its own file per round.

### Protocol

**Round 1 -- Independent Analysis (PARALLEL, strict isolation):**

- Dispatch all participating agents in parallel (single message with N Agent calls)
- Each independently analyzes the topic
- Each produces: position, reasoning, concerns, and estimate (if applicable)
- Each writes to: `{stage}/consensus/r1/{role}-position.md`
- No participant sees another's R1 output -- enforced by parallel dispatch with no cross-references
- This independence prevents anchoring bias

**Round 2 -- Review and Respond (PARALLEL, with all R1 paths):**

- Dispatch all participants in parallel (single message with N Agent calls)
- Each receives: their own R1 file path + ALL other participants' R1 file paths
- Each reads all R1 positions from disk
- Each writes to: `{stage}/consensus/r2/{role}-response.md`
- Each responds with:
  - Areas of agreement (cite specific points from other agents)
  - Areas of disagreement (with reasoning -- not just "I disagree" but why)
  - Revised position if their view has changed after seeing other perspectives
  - What remains unresolved from their perspective

**Round 3 -- Convergence (PARALLEL, only if disagreements remain after Round 2):**

- Orchestrator identifies the specific points of contention from R2 signals
- Dispatch all participants in parallel (single message with N Agent calls)
- Each receives: contested points + all R2 file paths
- Each writes to: `{stage}/consensus/r3/{role}-final.md`
- Each provides a final position on ONLY the contested points
- Responses must be short and focused -- no restating of agreed positions
- Each agent must explicitly state whether they can ACCEPT the emerging consensus even if it differs from their initial position

**Synthesis:**

- If consensus reached (all agents agree or all agents explicitly accept a compromise): record the agreed position as the decision, noting any conditions or caveats
- If not (any agent cannot accept): present the unresolved disagreement to the human with:
  - Each agent's final position file path
  - What was agreed upon (partial consensus)
  - What specifically remains contested
  - The orchestrator's assessment of why consensus failed

### Consensus Agent Template (Round 1)

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {participant_skill}
TASK_TYPE: consensus
ROLE: {participant_role}

Begin your response with "SKILL_LOADED: {participant_skill}" to confirm skill activation.

--- TASK ---
Independently analyze this topic. Do not reference any other participant's
work -- you are forming your own position first.

{topic_description}

Provide:
1. Your position on the topic (clear statement)
2. Your reasoning (cite specific concerns from YOUR domain -- not generic)
3. Risks you see from your perspective
4. Your estimate if applicable (effort, timeline, or scope)
5. Assumptions you are making (state them explicitly so others can challenge)

Be honest about uncertainty. If you lack information to form a confident
position, say so and state what information you would need.

--- INPUT ARTIFACTS (read these files) ---
{for each upstream artifact:}
- {artifact_file_path}: {description}

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your position to: {stage}/consensus/r1/{role}-position.md

When complete, respond with ONLY this signal block:
STATUS: DONE
ARTIFACT: {stage}/consensus/r1/{role}-position.md
SUMMARY: {one sentence, max 200 characters}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

### Consensus Agent Template (Round 2)

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {participant_skill}
TASK_TYPE: consensus
ROLE: {participant_role}

Begin your response with "SKILL_LOADED: {participant_skill}" to confirm skill activation.

--- TASK ---
Review your teammates' Round 1 positions and respond.

1. Where do you agree? (cite specific points from specific teammates)
2. Where do you disagree? (explain WHY -- what does your domain expertise
   tell you that conflicts with their position?)
3. Has your position changed after seeing other perspectives? If so,
   state your revised position and what changed your mind.
4. What remains unresolved? (specific points, not vague concerns)

--- INPUT ARTIFACTS (read these files) ---
- {stage}/consensus/r1/{own_role}-position.md: Your Round 1 position
{for each other participant:}
- {stage}/consensus/r1/{other_role}-position.md: {other_role}'s Round 1 position

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your response to: {stage}/consensus/r2/{role}-response.md

When complete, respond with ONLY this signal block:
STATUS: {DONE | NOT_DONE}
ARTIFACT: {stage}/consensus/r2/{role}-response.md
SUMMARY: {one sentence, max 200 characters}
{if NOT_DONE: FINDINGS: {bullet list of unresolved points}}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

### Consensus Agent Template (Round 3 -- Convergence)

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {participant_skill}
TASK_TYPE: consensus
ROLE: {participant_role}

Begin your response with "SKILL_LOADED: {participant_skill}" to confirm skill activation.

--- TASK ---
Final round. Address ONLY the contested points below.

Contested points:
{list_of_specific_unresolved_items}

For each contested point:
1. Your final position (brief)
2. Can you ACCEPT the emerging group position even if it differs from yours?
   (Yes/No -- if No, state what would need to change for you to accept)

--- INPUT ARTIFACTS (read these files) ---
{for each participant:}
- {stage}/consensus/r2/{role}-response.md: {role}'s Round 2 response

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your final position to: {stage}/consensus/r3/{role}-final.md

When complete, respond with ONLY this signal block:
STATUS: {DONE | NOT_DONE}
ARTIFACT: {stage}/consensus/r3/{role}-final.md
SUMMARY: {one sentence, max 200 characters}
{if NOT_DONE: FINDINGS: {what would need to change for acceptance}}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
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
