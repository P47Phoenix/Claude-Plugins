# product-delivery SKILL.md — F-25 audit

**Auditor:** Celebrimbor (Solution Architect)
**Target:** `delivery-team/skills/product-delivery/SKILL.md` (685 LOC)
**Trait under examination:** F-25 (Opus 4.7 — more literal instruction following)
**Pattern library:** `prompt-engineer/SKILL.md` v4-7-1
**Audit date:** 2026-04-22

---

## Audit Methodology

F-25 hazard surface: instructions that rely on *inference* ("use judgement", "as appropriate", "consider X", vague quantifiers, unbounded lists). On 4.7, literal execution may do one of three things:
1. Skip the inferred step entirely (no imperative hook to grab).
2. Over-execute — treat a soft suggestion as a hard rule.
3. Diverge from 4.6's prior behaviour in ways that are hard to predict without a dispatch shape.

For each audited rule I apply the following disposition:
- **CONCRETE_RECOMMENDATION** — rewording required. Cite Pattern 4.2 when the fix is a dispatch-shape (agent prompt, signal block, task routing). Cite Pattern 4.4 when the fix is instruction voicing.
- **DONE_WITH_REASON** — the rule is fine as-is; literal 4.7 execution produces the intended behaviour.

Sections that are pure *templates* (Patterns 1–12, JSON schemas, tables of artifact shapes) are excluded — they are scaffolds for output structure, not instructions whose inference could drift. I audit only the *imperative* prose wrapped around them.

---

## Role: Product Owner

### Instruction at line 25: "If ambiguous, ask before proceeding. Do not assume."
- Status: DONE_WITH_REASON
- Rationale: Already uses Pattern 4.4 calibrated voicing. Two plain imperatives ("ask", "Do not assume"). 4.7's literal execution is exactly "ask when ambiguous; never assume" — which is the intended behaviour. No inference gap.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (reference only; no change).

### Instruction at line 38: "Read **only** the relevant reference file(s) from the routing table -- do NOT read all reference files"
- Status: DONE_WITH_REASON
- Rationale: This is the *correct* literal form. Bold `only` and the explicit `do NOT` boundary close the inference gap. 4.7 will honour this precisely where 4.6 might have loaded extras "for safety".
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 131: "If the request is ambiguous, state the two most likely task types and ask which applies before producing output."
- Status: DONE_WITH_REASON
- Rationale: Fully specified — quantifier is exact ("the two most likely"), ordering is explicit ("before producing output"). 4.7 literal execution matches intent.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 174: "**INVEST validation** (apply silently, surface issues)"
- Status: CONCRETE_RECOMMENDATION
- Rationale: "Apply silently" is inference-dependent. A literal 4.7 reader may either (a) suppress the validation entirely because it was told to stay silent, or (b) dump the full INVEST matrix because "surface issues" is the only positive signal. The conjunction is ambiguous. Pattern 4.4 fix: convert to two calibrated imperatives with a dispatch shape.
- Proposed rewording:
  ```
  **INVEST validation:**
  - Run all six checks (Independent, Negotiable, Valuable, Estimable, Small, Testable) on every story.
  - Do not include passing checks in the output.
  - For each failing check, append one line in the Notes/Constraints section:
    `[INVEST ISSUE: Not <criterion> -- <specific reason and recommended split/fix>]`
  ```
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing.

### Instruction at line 182: "If any INVEST criterion fails, flag it: `[INVEST ISSUE: Not Small -- consider splitting at: ...]`"
- Status: DONE_WITH_REASON (assuming the line 174 recommendation above is applied)
- Rationale: The flag format itself is concrete. Pairs correctly with the rewording above.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing.

### Instruction at line 534: "Each acceptance criterion is independently testable (a QA engineer can write a test from it)"
- Status: DONE_WITH_REASON
- Rationale: The parenthetical ("a QA engineer can write a test from it") is a concrete, operational test. 4.7 literal execution has an objective check, not a fuzzy "looks testable" heuristic.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 535: 'No "should", "might", "could" in acceptance criteria -- use "must" or present tense assertions'
- Status: DONE_WITH_REASON
- Rationale: Enumerated forbidden vocabulary + enumerated allowed vocabulary. Maximally literal, zero inference.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (exemplary).

### Instruction at line 536: 'User role is specific (not "user" -- e.g., "authenticated customer", "admin user", "guest visitor")'
- Status: DONE_WITH_REASON
- Rationale: Explicit negative example + three positive exemplars. 4.7 has a concrete anti-pattern to reject against.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 548: "Success metrics are measurable (SMART)"
- Status: CONCRETE_RECOMMENDATION
- Rationale: "SMART" is an acronym that depends on the reader recalling all five letters. On 4.7 literal execution, a PRD may pass this check by satisfying Specific+Measurable only (the two most salient), silently skipping Achievable/Relevant/Time-bound. The inference gap is the acronym expansion.
- Proposed rewording:
  ```
  Every success metric must declare all five SMART attributes:
  - Specific: names a single observable outcome.
  - Measurable: has a numeric value or pass/fail test.
  - Achievable: has a credible path given current team + timeline.
  - Relevant: maps to a stated Goal or OKR in the same PRD.
  - Time-bound: names a deadline or measurement window.
  Reject metrics missing any attribute and list the missing attribute in Open Questions.
  ```
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing.

### Instruction at line 553: 'Sprint goal is a single sentence expressing user/business value (not "complete stories X, Y, Z")'
- Status: DONE_WITH_REASON
- Rationale: Positive constraint ("single sentence", "user/business value") + explicit negative exemplar. Zero inference required.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 555: "Commitment does not exceed 80% of capacity (buffer for interruptions)"
- Status: DONE_WITH_REASON
- Rationale: Quantified threshold. Literal execution is deterministic.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (exemplary — a quantified NFR rather than "leave some buffer").

### Instruction at line 559: "Review defect categories in retrospectives -- which are persistent?"
- Status: CONCRETE_RECOMMENDATION
- Rationale: The trailing rhetorical question ("which are persistent?") is inference-dependent. "Persistent" has no defined threshold. 4.7 may either skip the persistence analysis or apply an arbitrary cutoff (e.g., "mentioned twice = persistent"). No dispatch shape for the finding.
- Proposed rewording:
  ```
  In every retrospective, categorise defects opened since the last retro by root-cause tag.
  Mark a category as "persistent" when it has appeared in three or more consecutive retros.
  For each persistent category, produce one row in the Action Items table with owner and due date.
  ```
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing.

### Instruction at line 561: "Monitor rate trend -- is the defect rate decreasing over time?"
- Status: CONCRETE_RECOMMENDATION
- Rationale: Same class of defect as line 559. Rhetorical question substitutes for an imperative. "Over time" is unquantified. On 4.7 the check may be skipped or rendered as a one-line "yes/no" opinion with no calculation.
- Proposed rewording:
  ```
  Compute the linear slope of defects/story across the trailing six sprints.
  If slope >= 0, raise a Warning finding in the retrospective report with the sprint numbers and rates.
  ```
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing.

---

## Role: Scrum Master (Scrum Bag)

### Instruction at line 566: "Every retrospective must produce action items with assigned owners and due dates"
- Status: DONE_WITH_REASON
- Rationale: Three concrete required fields (action / owner / due date). `must` is appropriate — a retrospective without action items is a process failure. Pattern 4.4 reserves the strong marker correctly.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 567: "Velocity analysis must include at least 3 sprints of data for trend identification"
- Status: DONE_WITH_REASON
- Rationale: Quantified minimum. No inference gap.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (exemplary).

### Instruction at line 568: "Metrics must have baselines before targets can be set"
- Status: DONE_WITH_REASON
- Rationale: Ordering constraint is explicit ("before"). Literal execution is deterministic.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 569: "Process improvement recommendations must be specific and actionable, not generic"
- Status: CONCRETE_RECOMMENDATION
- Rationale: "Specific and actionable, not generic" is self-referentially under-specified — it tells the model to avoid vagueness without naming the test for specificity. On 4.7, "specific" becomes a subjective filter the model applies to its own output, which leaks.
- Proposed rewording:
  ```
  Every process-improvement recommendation must include all of:
  - Trigger: the observed behaviour or metric that motivates the change.
  - Action: a single imperative verb + object (e.g., "Add WIP limit of 3 to In-Progress column").
  - Owner: a named role or person.
  - Success signal: the metric or observable that confirms the change worked.
  - Review date: when the team re-checks the success signal.
  Reject any recommendation missing one of these five fields.
  ```
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing.

### Instruction at line 570: "Ceremony facilitation guides must include time-boxes for each activity"
- Status: DONE_WITH_REASON
- Rationale: Concrete required field ("time-boxes for each activity"). No inference.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 571: "Team health assessments must preserve psychological safety -- no individual attribution of problems"
- Status: DONE_WITH_REASON
- Rationale: The positive constraint ("preserve psychological safety") is paired with a concrete negative rule ("no individual attribution of problems"). The negative rule is the operational anchor — 4.7 has a literal "do not attribute to individuals" check.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

---

## Role: Data Analyst

### Instruction at line 575: "Every metric must have a precise definition and a formula -- no ambiguous metrics"
- Status: DONE_WITH_REASON
- Rationale: Two required fields (definition, formula) + explicit negative ("no ambiguous metrics"). The two required fields are the literal test.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 576: "Experiments must have a hypothesis stated before the test plan is designed"
- Status: DONE_WITH_REASON
- Rationale: Ordering constraint is explicit. Literal execution is deterministic.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 577: 'Sample size calculations must be explicit -- no "run it and see"'
- Status: DONE_WITH_REASON
- Rationale: Explicit + named anti-pattern. 4.7 has a literal rejection target.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (exemplary).

### Instruction at line 578: "Dashboard designs must specify the audience and the decisions the dashboard supports"
- Status: DONE_WITH_REASON
- Rationale: Two required output fields. Literal.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 579: 'Data quality assessments must define what "quality" means for each data field'
- Status: DONE_WITH_REASON
- Rationale: Required deliverable per field. Inference-free.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 580: "Reporting cadence must match the decision cadence -- daily metrics for daily decisions, weekly for weekly"
- Status: DONE_WITH_REASON
- Rationale: Constraint stated abstractly but immediately grounded with two concrete exemplars. 4.7 can interpolate additional cadences (hourly, monthly) from the pattern.
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

---

## Cross-cutting: Sub-Agent Invocation Shape (lines 33–77)

### Instruction at lines 35–40: the four-step sub-agent invocation procedure
- Status: DONE_WITH_REASON
- Rationale: This section already embodies Pattern 4.2 — the four-step procedure + the prompt template (lines 46–77) define a dispatch shape with bracketed slots (`[ROLE]`, `[PASTE FULL CONTENTS …]`, `[TASK TYPE]`, `[DESCRIBE WHAT THE USER WANTS]`, context list, output requirements 1–5). The literal shape is load-bearing; 4.7 will populate slots rather than reinvent the template.
- Pattern citation: Pattern 4.2 — 4.7-Aware Role Prompt Skeleton (well-applied). The only absence is an explicit `SIGNAL BLOCK:` line at the end of the template; however, the Output contract (lines 608–621) supplies an equivalent JSON-shaped terminator for agentic-flow callers, so the absence does not create a literal-execution hazard for interactive callers.

### Instruction at line 42: "Do not inline role-specific knowledge into the main context."
- Status: DONE_WITH_REASON
- Rationale: Plain imperative, no inference. The boundary ("main context") is defined earlier (line 11).
- Pattern citation: Pattern 4.4 — Calibrated Instruction Voicing (well-applied).

### Instruction at line 623: "`downstream_ready: false` means the artifact has open questions that must be resolved before a downstream agent can act on it. Always populate `open_questions` when `downstream_ready` is false."
- Status: DONE_WITH_REASON
- Rationale: Conditional imperative is exact ("when downstream_ready is false → populate open_questions"). Dispatch-shape compatible — downstream orchestrators parse the JSON deterministically.
- Pattern citation: Pattern 4.2 — 4.7-Aware Role Prompt Skeleton (the output contract is the signal block equivalent).

---

## Summary

- **Total instructions audited:** 24
- **Concrete recommendations:** 5 (lines 174, 548, 559, 561, 569)
- **Done-with-reason:** 19
- **Pattern 4.2 citations:** 2 (lines 33–77 dispatch shape, line 623 contract)
- **Pattern 4.4 citations:** 22 (all audited imperatives were voicing-calibration candidates)

### Overall Assessment

The product-delivery SKILL.md is already Pattern 4.4-compliant across most of its imperative prose. The five concrete recommendations cluster around two failure modes:

1. **Silent-operation ambiguity** (line 174) — "apply silently, surface issues" is the one place the skill asks for partial output without specifying the partition rule. 4.7 may over- or under-output.
2. **Rhetorical questions as imperatives** (lines 559, 561) — defect-monitoring guardrails use "which are persistent?" and "is the defect rate decreasing?" in place of imperatives. 4.7 treats these as informational, not as commands to compute and flag.
3. **Acronym shorthand + vague self-reference** (lines 548, 569) — "SMART" and "specific and actionable, not generic" rely on the reader recalling/defining criteria. Expanding each into an enumerated field list closes the gap.

No changes to `CRITICAL:` / `NEVER` markers are warranted — the skill reserves strong voicing appropriately and does not over-deploy it.

### Recommended follow-up

The five concrete recommendations above can be applied in a single follow-up edit pass to SKILL.md lines 174, 548, 559, 561, 569. They are independent and non-breaking — each converts a softly-worded guardrail into an enumerated checklist or quantified threshold. The frontmatter forward-compatibility header (Pattern 4.6) has already been applied as part of this audit (Part B).
