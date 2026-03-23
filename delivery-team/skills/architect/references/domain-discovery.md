# Domain Discovery Interviews

Before designing architecture or decomposing a system, the architect must gather domain context that isn't in the PRD or code. This reference defines structured interview protocols -- one per decomposition strategy -- where the architect interviews the Product Owner and escalates to the human when stakeholder input is needed.

## Interview Protocol

### How Domain Discovery Works

1. **Select questions** based on the configured decomposition strategy (from config or auto-detected)
2. **Invoke Product Owner** (product-delivery skill) with the questions and project context
3. **Evaluate answers**: sufficient, partial, or insufficient for architectural decisions
4. **Follow up** on partial answers with targeted questions
5. **Escalate** to human for questions the PO can't answer (needs real stakeholder input)
6. **Record** all answers in the architecture artifact as a "Domain Discovery" section

### When to Run Discovery

- Before every `design` or `decompose` task
- When switching decomposition strategies (new questions for new approach)
- When the architect encounters ambiguity during design (ad-hoc questions)
- NOT needed for: `review`, `document` (ADR), `model` (C4), or `evaluate` tasks

---

## Volatility Discovery (for IDesign decomposition)

The IDesign method discovers volatility through business process walkthroughs, NOT by asking "what changes?" directly. Follow Juval Lowy's approach: document first, analyze second.

### Step 1: Business Process Walkthrough (the core interview)

Walk through every major business process end-to-end:

1. "Walk me through how [core business process] works from start to finish."
2. "What are the steps? Who is involved at each step? What decisions are made?"
3. "What data moves between steps? In what format?"
4. "Are there variations of this process? When does the process branch?"
5. "What happens when things go wrong in this process? How are errors handled?"

Repeat for each major business process. Document as: activity → decision → activity → outcome.

### Step 2: Change History Analysis

After documenting the processes, explore what has changed:

6. "In the last 12 months, which parts of this process changed? Why?"
7. "Which changes were easy (stayed contained) and which were painful (spread everywhere)?"
8. "What's on the roadmap that will change these processes in the next 6-12 months?"
9. "Have any external integrations or regulations forced process changes?"

### Step 3: Commonality and Volatility Identification

Review the documented processes together with the PO:

10. "Looking at these processes together, which activities appear in multiple processes?" (commonalities)
11. "Which of these steps would you say change most often? Why?" (volatilities)
12. "If [step] changed, what else in the process would need to change?" (encapsulation boundaries)
13. "Which parts are commodity (everyone does it the same) vs unique to your business?" (build vs buy)

### Step 4: Decomposition Validation

Test the proposed decomposition with real scenarios:

14. "Let me test our decomposition: if [real upcoming change] happens, here's what would change in the system. Does that seem contained?"
15. "Does this component grouping make sense to you? Would changes stay isolated?"
16. "Are there changes I haven't considered that would break this structure?"

### Escalation Triggers
Escalate to human if:
- PO cannot walk through the business processes (needs domain expert)
- Change history is unavailable (needs organizational knowledge)
- Validation scenarios reveal the decomposition doesn't contain changes

Reference: Juval Lowy, "Righting Software" (Addison-Wesley, 2019) for the complete IDesign methodology.

---

## DDD Domain Discovery (for strategic DDD decomposition)

Ask these questions to identify subdomains and bounded contexts:

### Core Domain
1. "What is your competitive advantage -- what do you do that competitors can't easily copy?"
2. "If you had to pick the ONE thing that makes this product valuable, what is it?"
3. "Where do you invest the most development effort? Where should you?"

### Subdomain Boundaries
4. "Walk me through the core business process end to end."
5. "When you say [term], does it mean the same thing to everyone? Or do different teams define it differently?"
6. "Where do different departments disagree about how things should work?"

### Context Mapping
7. "Which teams or systems need to communicate to complete a business process?"
8. "Where do handoffs happen between teams? Are they smooth or painful?"
9. "Which external systems do you depend on? Do you control their APIs?"

### Strategic Classification
10. "Which capabilities are commodity (everyone in your industry does it the same way)?"
11. "Which capabilities are necessary but not what makes you special?"
12. "Which capabilities would you outsource if you could? Which would you NEVER outsource?"

---

## Team Topology Discovery (for inverse Conway decomposition)

Ask these questions to understand team structure and cognitive load:

### Current Structure
1. "How are engineering teams organized today? What does each team own?"
2. "How big is each team? Who reports to whom?"
3. "Which teams communicate most frequently? About what specifically?"

### Pain Points
4. "Where do handoffs between teams slow things down?"
5. "Which teams are overloaded -- owning too many things?"
6. "Which parts of the system require specialist knowledge that only one or two people have?"

### Desired State
7. "If you could reorganize teams to deliver faster, what would you change?"
8. "What capabilities do multiple teams need that a platform team could provide?"
9. "Which teams should be able to deploy independently?"

### Cognitive Load
10. "Which teams struggle to understand their full scope?"
11. "When a new developer joins a team, how long until they're productive? Which teams take longest?"

---

## Event Storming Discovery (for event-driven decomposition)

Ask these questions to discover domain events and business processes:

### Events
1. "What are the most important things that HAPPEN in your business? (Things that occurred -- past tense)"
2. "What events trigger other events? (When X happens, Y must happen)"
3. "Which events involve money, compliance, or legal obligations?"

### Commands and Actors
4. "Who or what triggers each of those events? Is it a person, a schedule, or another system?"
5. "What decisions must be made before an event can occur? What information is needed to make that decision?"

### Policies and Reactions
6. "What are the business rules -- 'When X happens, we always do Y'?"
7. "Are there rules that are sometimes broken or have exceptions? What are the exceptions?"

### Pain Points
8. "Which processes are error-prone or frequently fail? What goes wrong?"
9. "Where do things get stuck waiting for approval, information, or a system response?"
10. "What workarounds exist because the system doesn't support the real process?"

---

## Evaluating PO Answers

After the PO responds, classify each answer:

| Classification | Meaning | Action |
|---------------|---------|--------|
| **Sufficient** | PO answered with specific, confident detail | Record and proceed |
| **Partial** | PO answered generally but lacks specifics | Ask targeted follow-up |
| **Uncertain** | PO gave an answer but flagged uncertainty | Record with caveat, consider escalation |
| **Cannot answer** | PO lacks the domain knowledge to answer | Escalate to human |

### Follow-Up Question Patterns

For partial answers:
- "Can you give a specific example of [vague answer]?"
- "How often does [thing] happen? Once a day? Once a month? Once a year?"
- "Who in the organization would know the answer to [specific gap]?"

For uncertain answers:
- "What would you ASSUME the answer is? And what's the risk if you're wrong?"
- "Is there documentation, a wiki, or a subject matter expert who knows for sure?"

---

## Escalation Format

When the PO can't answer and real stakeholder input is needed:

```markdown
## Domain Discovery Escalation

**Decomposition strategy**: [volatility / DDD / team-topology / event-storming]
**Interview completed**: [date]

### Questions Answered (by PO)
[List of answered questions with summarized answers]

### Questions Requiring Stakeholder Input

| # | Question | Why It Matters | Suggested Respondent |
|---|----------|---------------|---------------------|
| 1 | [question] | [which architectural decision this informs] | [CTO / domain expert / team lead / etc.] |
| 2 | [question] | [which architectural decision this informs] | [suggested role] |

### Impact If Unanswered
[What assumptions the architect will make and the risks of those assumptions]

### Options
1. **Provide answers** -- answer the questions above, architect will incorporate
2. **Accept assumptions** -- architect proceeds with stated assumptions and risks
3. **Schedule stakeholder session** -- arrange interview with the suggested respondents
```

---

## Recording Domain Discovery

All discovery answers are recorded in the architecture artifact:

```markdown
## Domain Discovery

**Strategy**: [volatility / DDD / team-topology / event-storming]
**Source**: PO interview + [human input if escalated]
**Date**: [date]

### Key Findings

| Finding | Source | Confidence | Architectural Impact |
|---------|--------|-----------|---------------------|
| [finding] | PO | High/Medium/Low | [how this shapes the architecture] |

### Assumptions (from unanswered questions)
- [Assumption]: [risk if wrong]

### Raw Interview Notes
[Q&A format -- question and answer for each]
```

This section becomes part of `.delivery/artifacts/04-architecture.md` and is referenced by ADRs.
