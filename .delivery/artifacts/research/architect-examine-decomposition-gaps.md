# Architect Decomposition & Review Board — Gap Report

Role: Solution Architect (examine-first discovery).
Scope: `delivery-team/skills/architect/` references and delivery-flow pipeline stages 4 & 5.

## Phase 1 — Examined Artifacts

- `delivery-team/skills/architect/SKILL.md` (Prior Art Analysis exists)
- `delivery-team/skills/architect/references/volatility-decomposition.md` (220 lines)
- `delivery-team/skills/architect/references/strategic-ddd.md` (279 lines)
- `delivery-team/skills/architect/references/event-storming.md`, `domain-discovery.md`, `architecture-patterns.md` (present, not primary)
- `delivery-team/skills/delivery-flow/references/pipeline-stages.md` (Stage 4 lines 333–410, Stage 5 lines 415–497)
- `delivery-team/skills/delivery-flow/references/team-patterns.md` Pattern 3 Multi-Perspective Review Board (lines 334–416)
- `delivery-team/skills/delivery-flow/references/config-schema.md` `dod_validators` (lines 57–63)
- `.delivery/memory/topics/defect-patterns.md` — no architect-decomposition defects recorded

## Phase 2 — Gap Report

### Gap 1: Löwy "Golden Rule" (decompose by volatility, NOT functionality)

**PARTIAL.** `volatility-decomposition.md:7` states "Volatility-based decomposition identifies WHAT CHANGES and encapsulates it behind stable interfaces" and `:181` anti-pattern "Layer-based decomposition pretending to be volatility-based". The explicit, named **Golden Rule** ("Never decompose based on functionality") from Löwy's *Righting Software* Ch.2 is **not stated as a rule**. The warning against functional decomposition disguised as volatility (`:181`) only covers the layer variant, not the broader functional trap. Severity: **blocking design-quality issue** — this is the single most misapplied principle in IDesign and the PO named it explicitly.

### Gap 2: Implementation-detail contamination at decomposition step (Lambda/ECR/SQS/language)

**YES — confirmed gap.** `volatility-decomposition.md` Phases 1–4 (`:49-96`) never prohibit naming cloud services, runtimes, or languages during decomposition. `:188-208` "Applying IDesign to Microservices" discusses extraction criteria but still does not forbid implementation leakage during the analysis phase. `strategic-ddd.md` has the same gap — Phases 1–4 are model/language-first but contain no explicit "no implementation nouns" rule. Severity: **blocking** — this is the PO's core complaint and the pattern is identical in both paradigms as predicted.

### Gap 3: Architect in Stage 5 (Plan) participation

**YES — confirmed gap.** `pipeline-stages.md:428-449` Stage 5 invokes PO, QA, Scrum Bag, DevOps. Architect is **not** an invoked participant. Architect artifacts are read as *input files* only. Architect appears only in Stage 5 DoD validators (`config-schema.md:61`) — a passive post-hoc review, not active participation in sequencing, effort estimation, or interface-first planning. This directly contradicts `volatility-decomposition.md:97-120` Phase 5 which assigns the architect to implementation sequencing, interface design, and effort estimation. Severity: **blocking for IDesign-style delivery**.

### Gap 4: Architecture Board Review (configurable multi-reviewer loop)

**PARTIAL.** `team-patterns.md:334-416` Multi-Perspective Review Board exists with 3 fixed roles (Technical/Business/Risk) and is already used at Stage 4 via the Evaluator-Optimizer Loop (`pipeline-stages.md:369-390`). It supports parallel dispatch, context isolation per reviewer, and BLOCK/RECOMMEND voting. What is **missing**: (a) configurable reviewer roster per stage, (b) multiple architect personas (solution + enterprise + data + security + domain-specific) as distinct reviewers rather than one "Technical Reviewer", (c) iterative loop (currently single-pass except when embedded in evaluator-optimizer). No `architecture_board` config block exists. Severity: **minor-to-moderate** — the primitive exists; the specialization does not.

## Phase 3 — Options

### Option A — In-place enhancement (S)

Edit `volatility-decomposition.md` and `strategic-ddd.md` to add: (1) named Golden Rule section with Löwy quote, (2) "No Implementation Nouns at Decomposition" guardrail with banned-word list (Lambda/ECS/SQS/Kafka/Postgres/Python/etc.) applied through Phases 1–4, (3) functional-decomposition-trap anti-pattern with worked example. Add Architect invocation step to Stage 5 Plan between steps 1 and 3 (`pipeline-stages.md`) for task_type `implementation-sequencing` producing `.delivery/artifacts/05-plan/architect/sequencing.md`. Reversibility: high. Risk: low. **Does not address Gap 4.**

### Option B — Paradigm-as-skill (L/XL)

Extract each decomposition paradigm to its own skill (`architect-volatility/`, `architect-ddd/`, `architect-functional/`, `architect-event-storming/`) each with `overview.md`, `golden-rules.md`, `process.md`, `anti-patterns.md`, `review-criteria.md`, `worked-examples.md`. Architect skill becomes a router that detects paradigm from signals and dispatches. Reversibility: medium (splitting is easy, merging back is harder). Risk: medium — fragments the architect knowledge base, increases context-loading complexity, creates cross-skill consistency burden. **This option is itself large enough to warrant running through the delivery pipeline as a FEATURE.**

### Option C — PO+Architect Design Sprint sub-workflow + configurable Architecture Board (M/L)

Add a new mini-flow `architect-design-sprint.md` invoked from Stage 4 that iterates: PO presents business processes → Architect does volatility analysis → PO validates with change scenarios → Architect refines → loop until change-scenario validation passes (max 3 iterations). Add new `architecture_board` config block (schema below) enabling configurable reviewer roster + custom personas + per-reviewer context isolation + loop count. Keeps paradigms as references (not skills) but adds process rigor and the configurable board. Reversibility: medium. Risk: low-medium.

**Proposed `architecture_board` config schema:**

```yaml
architecture_board:
  enabled: true
  stages: [architect]                 # which stages trigger the board
  loop_max_iterations: 2              # 1 = single pass; 2+ = iterative
  reviewers:
    - id: solution_architect
      skill: delivery-team:architect
      role: solution
      perspective: "implementability, trade-offs, patterns"
      references: [architecture-patterns.md, quality-attributes.md]
    - id: volatility_reviewer
      skill: delivery-team:architect
      role: solution
      perspective: "IDesign golden rule compliance, implementation-leakage detection"
      references: [volatility-decomposition.md]
    - id: domain_reviewer
      skill: delivery-team:architect
      role: solution
      perspective: "DDD bounded context integrity, ubiquitous language"
      references: [strategic-ddd.md, domain-discovery.md]
    - id: security_reviewer
      skill: delivery-team:architect
      role: security
  quorum: all_recommend                # or: majority, unanimous_critical
  block_escalation: decision_owner
```

## Recommendation

**Option A + the configurable `architecture_board` slice of Option C, sequenced in that order.** Option A is the minimum viable fix that closes the three blocking gaps (Golden Rule, implementation-leakage guardrails, Architect-in-Plan) in a single small PR. The Architecture Board config slice layers on cleanly afterward because the Multi-Perspective Review Board primitive already exists — we are only parameterizing it.

**Option B is NOT recommended as the first move.** Paradigm-as-skill is attractive but (i) the current reference files are already well-scoped, (ii) extraction is XL and should itself go through the delivery pipeline as a FEATURE with its own PRD, and (iii) most of the PO's pain is content gaps and pipeline wiring, not skill topology.

**Pipeline sizing:** Option A fits a single direct edit session. Option C's config slice is a FEATURE-sized pipeline run (schema bump, team-patterns extension, migration, validator). Option B is FEATURE-XL and must run through the full delivery pipeline if pursued.
