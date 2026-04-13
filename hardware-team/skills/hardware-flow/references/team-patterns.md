# Hardware Team Collaboration Patterns

> "Five patterns to bind the team. No design shall pass unchallenged."

## Decision Matrix: When to Use Each Pattern

Select the collaboration pattern based on the situation. Multiple patterns may apply to a single stage -- they execute in the order listed below (evaluator-optimizer first, then adversarial, then review board, then BOM reconciliation, then consensus).

| Situation | Pattern | Rationale |
|-----------|---------|-----------|
| After any stage produces an artifact | Evaluator-Optimizer | Catch quality issues before gate validation |
| Schematic or layout decisions with assumptions | Adversarial Review | Challenge assumptions, find blind spots, stress-test completeness |
| Cross-discipline review checkpoints (Schematic, Layout, DFM) | Design Review Board | Multiple engineering disciplines needed for high-stakes go/no-go |
| BOM finalization with multi-source components | BOM Reconciliation | Cross-supplier validation prevents single-source risk and pricing errors |
| Cross-discipline alignment (compliance + manufacturing + EE) | Consensus | Compliance scope, production readiness, and shared commitments need mutual agreement |

---

## Pattern 1: Evaluator-Optimizer Loop (Hardware)

**Dispatch rule**: Dispatch the producer and the evaluator as SEPARATE Agent tool calls. One role = one sub-agent invocation. Never collapse "produce and self-evaluate" into a single compound prompt.

### When to Use

After any stage produces its primary artifact, before gate validation. This is the first quality pass -- it catches obvious issues cheaply before invoking the full gate validator panel.

### Dispatch: Sequential

This pattern is inherently sequential (produce, evaluate, revise, re-evaluate). No parallelism within this pattern.

### Hardware-Specific Evaluation Criteria

Unlike software artifacts where quality is often subjective, hardware artifacts have measurable physical constraints. Evaluators must check:

- **Electrical correctness**: Voltage levels, current budgets, power sequencing, thermal margins
- **Physical constraints**: Board dimensions, layer count vs routing complexity, component clearances
- **Manufacturing feasibility**: Component availability, lead times, assembly compatibility
- **Regulatory alignment**: Compliance region requirements traced to design decisions

### Protocol

1. Primary agent produces the artifact and writes it to the stage output path.
2. Evaluator agent receives:
   - The artifact FILE PATH (not content) -- evaluator reads it from disk
   - The quality gate criteria for this stage (from `quality-gates.md`)
   - Instruction to evaluate each criterion strictly as PASS or FAIL with explanation
3. Evaluator writes findings to: `.hardware/artifacts/{stage}/qa-evaluator/evaluation-round-{N}.md`
4. If all criteria PASS: proceed to gate validation.
5. If any criteria FAIL: route back to primary agent with:
   - The artifact file path (agent re-reads its own work)
   - The findings file path (agent reads evaluator feedback)
   - Task description: "Revise your artifact to address the findings. Read both files."
6. Primary agent revises the artifact, addressing each failing criterion explicitly.
7. Re-evaluate (repeat from step 2).
8. Maximum iterations: 3 (or stage-specific override from `quality-gates.md`).
9. If still failing after max iterations: escalate to human with all finding file paths shown.

### Evaluator Role Assignment by Stage

| Stage | Producer Role | Evaluator Role |
|-------|--------------|----------------|
| 1. Concept | HW Product Owner | HW Product Owner (self-eval with distinct prompt) |
| 2. Schematic | Electrical Engineer | Electrical Engineer (distinct evaluator prompt) |
| 3. Layout | PCB Layout Engineer | PCB Layout Engineer (distinct evaluator prompt) |
| 5. DFM/DFA | Manufacturing Engineer | Manufacturing Engineer (distinct evaluator prompt) |
| 6. Compliance | Compliance Engineer | Compliance Engineer (distinct evaluator prompt) |

### Key Principle

The evaluator is not the same agent invocation as the producer. Even when both use the same role skill, the separation of roles (produce vs. evaluate) with distinct prompts produces meaningfully better results than self-review.

---

## Pattern 2: Adversarial Review (Forced-Find Prompting)

**Dispatch rule**: Dispatch the challenger as a SEPARATE Agent tool call from the producer. One role = one sub-agent invocation. Never ask the producer to "also challenge its own work."

### When to Use

- **Stage 2 (Schematic)**: Challenge component selection assumptions, derating margins, simulation coverage, missing protection circuits
- **Stage 3 (Layout)**: Challenge routing decisions, impedance assumptions, thermal management adequacy
- **Stage 5 (DFM/DFA)**: Challenge yield estimates, assembly assumptions, BOM cost projections
- **Stage 6 (Compliance)**: Challenge compliance gap analysis, missing standards, evidence sufficiency

### Dispatch: Sequential

Adversarial review runs sequentially after the evaluator-optimizer loop. The challenger is a single agent.

### Isolation Rule

Challenger receives ONLY the artifact file path. No production conversation, no evaluator-optimizer history, no orchestrator reasoning. Strict isolation ensures independent judgment.

### Forced-Find Prompting

The challenger MUST find at least 3 issues. This is not optional. The instruction is:

> "You MUST identify at least 3 issues, risks, or gaps in this artifact. If you cannot find 3, look harder -- check edge cases, failure modes, environmental extremes, supply chain risks, and regulatory gaps. Zero findings is not an acceptable output."

### Hardware-Specific Challenge Areas

| Domain | Challenge Focus |
|--------|----------------|
| Electrical | Missing protection circuits, inadequate derating, thermal runaway paths, EMI coupling |
| Component | Single-source risk, end-of-life parts, long lead times, inadequate second-source |
| Manufacturing | Tombstoning risk, solder bridging, thermal relief inadequacy, fiducial placement |
| Compliance | Missing test standards, untested frequency bands, insufficient shielding |
| Environmental | Operating temperature range gaps, humidity exposure, vibration tolerance |

### Protocol

1. Primary artifact is complete and has passed the evaluator-optimizer loop.
2. Spawn challenger agent with explicit adversarial instruction:
   - Artifact file path ONLY (no other context)
   - Forced-find minimum: 3 issues
   - Challenge categories: electrical, component, manufacturing, compliance, environmental
3. Challenger writes findings to: `.hardware/artifacts/{stage}/adversarial/challenge-{N}.md`
4. Producer receives challenger findings and MUST respond to each:
   - **Accept**: describe the fix and implement it
   - **Reject with evidence**: cite specific data (simulation result, datasheet spec, standard clause) that refutes the finding
   - **Defer**: acknowledge the risk and document it as a known limitation with mitigation plan
5. Response written to: `.hardware/artifacts/{stage}/adversarial/response-{N}.md`
6. If any accepted findings exist: artifact is revised before proceeding to gate.

---

## Pattern 3: Design Review Board (Multi-Role Schematic/Layout Review)

**Dispatch rule**: Each reviewer is a SEPARATE Agent tool call. All reviewers dispatch in PARALLEL. Reviewers do NOT see each other's findings.

### When to Use

Activated when `review.design_review_board: true` in `.hardware/config.yml`. Runs AFTER the primary gate passes, before advancing to the next stage.

- **After Schematic Review Gate**: EE, PCB Layout, MfgE, and CompE reviewers evaluate schematic
- **After DRC Gate**: EE, PCB Layout, MfgE, and CompE reviewers evaluate layout
- **After DFM+BOM Gate**: EE, PCB Layout, MfgE, and CompE reviewers evaluate DFM package

### Reviewer Perspectives (Parallel Dispatch)

| Reviewer Role | Reviews For | Key Questions |
|---------------|------------|---------------|
| Electrical Engineer | Electrical correctness | Are derating margins adequate? Are protection circuits complete? Is the power tree sound? |
| PCB Layout Engineer | Layout feasibility | Can this schematic be routed on N layers? Are footprints correct? Any placement conflicts? |
| Manufacturing Engineer | Manufacturability | Are components available? Any assembly concerns? DFM red flags? |
| Compliance Engineer | Regulatory alignment | Will this pass EMC? Are required certifications achievable? Any compliance blockers? |

### Protocol

1. Gate passes (Schematic Review, DRC, or DFM+BOM).
2. Dispatch 4 reviewer agents in PARALLEL, each receiving:
   - The stage artifacts file path(s)
   - Their role-specific review perspective
   - Instruction: "Review from your discipline's perspective. Identify blocking issues, warnings, and suggestions."
3. Each reviewer writes findings to: `.hardware/artifacts/{stage}/drb/{role}-review.md`
4. After ALL reviewers complete, the orchestrator:
   - Collects all findings
   - Deduplicates (same issue found by multiple reviewers = single finding with multiple attestors)
   - Categorizes: BLOCKING (must fix before advancing), WARNING (should fix), SUGGESTION (consider)
5. If any BLOCKING findings: route back to stage producer for resolution, then re-run DRB.
6. If no BLOCKING findings: advance to next stage. Warnings and suggestions are recorded for downstream awareness.
7. Maximum DRB iterations: 2. After 2 rounds with unresolved blockers, escalate to human.

---

## Pattern 4: BOM Reconciliation (Cross-Supplier Validation)

**Dispatch rule**: The Manufacturing Engineer is the primary agent. Sourcing validation dispatches kicad-happy skills via the integration layer.

### When to Use

- **Stage 5 (DFM/DFA)**: BOM validation phase -- after kicad-happy:bom returns the initial BOM
- **Stage 8 (Production Release)**: Final BOM freeze -- before production release approval

### Purpose

BOM Reconciliation cross-validates component sourcing across multiple distributors to prevent:
- **Single-source risk**: Components available from only one distributor
- **Pricing discrepancies**: >20% price variance across distributors signals potential issues
- **Lifecycle risk**: End-of-life or NRND (Not Recommended for New Designs) parts
- **Lead time risk**: Components with lead times exceeding the project timeline

### Protocol

1. Manufacturing Engineer invokes `kicad-happy:bom` to get the current BOM.
2. For each critical component (or all components if `bom.full_reconciliation: true`):
   a. Query primary distributor via kicad-happy sourcing skill (per config `bom.primary_distributor`)
   b. Query at least one secondary distributor for cross-validation
   c. Compare: price, stock quantity, lead time, lifecycle status
3. Flag discrepancies:
   - **SINGLE_SOURCE**: Component found at only one distributor --> WARNING
   - **PRICE_VARIANCE**: >20% price difference across sources --> WARNING
   - **EOL_RISK**: Part marked end-of-life or NRND at any source --> BLOCKING
   - **LEAD_TIME_RISK**: Lead time exceeds `bom.max_lead_time_weeks` config --> WARNING
   - **STOCK_RISK**: Total available stock < 2x order quantity --> WARNING
4. Write reconciliation report to: `.hardware/artifacts/{stage}/bom-reconciliation.md`
5. BOM Gate evaluates reconciliation flags as part of its pass/fail criteria.

### Reconciliation Report Format

```markdown
## BOM Reconciliation Report
- Date: {timestamp}
- Total components: {count}
- Components reconciled: {count}
- Flags: {BLOCKING: N, WARNING: N, CLEAN: N}

### Flagged Components
| Ref | MPN | Flag | Detail | Recommended Action |
|-----|-----|------|--------|-------------------|
| ... | ... | ...  | ...    | ...               |
```

---

## Pattern 5: Consensus (Cross-Discipline Alignment)

**Dispatch rule**: Each discipline representative is a SEPARATE Agent tool call dispatched in PARALLEL. The orchestrator synthesizes a consensus position.

### When to Use

- **Compliance scope decisions**: Which regions/standards to target (EE + CompE + MfgE + HW PO must agree)
- **Component substitution decisions**: When a component is unavailable and alternatives affect multiple disciplines
- **Production readiness decisions**: Before advancing from DFM/DFA to Compliance (all roles weigh in)
- **Rework scope decisions**: When a rework path affects multiple disciplines (e.g., compliance failure requiring both schematic and layout changes)

### Protocol

1. Orchestrator frames the decision question with:
   - Context (what triggered the decision)
   - Options (enumerated, with known trade-offs)
   - Constraints (budget, timeline, regulatory, technical)
2. Dispatch relevant role agents in PARALLEL, each receiving:
   - The decision context
   - Their role-specific evaluation criteria
   - Instruction: "Evaluate each option from your discipline's perspective. State your preferred option and WHY."
3. Each role writes its position to: `.hardware/artifacts/{stage}/consensus/{role}-position.md`
4. After ALL roles complete, the orchestrator:
   - Synthesizes positions into a comparison matrix
   - Identifies agreement (all roles prefer same option) or disagreement
5. If AGREEMENT: document the consensus and proceed.
6. If DISAGREEMENT: present the comparison matrix to the user with:
   - Each role's position and rationale
   - The orchestrator's recommended resolution (weighted by which discipline is most affected)
   - Request for human decision
7. Document the final decision (whether consensus or human-decided) in: `.hardware/artifacts/{stage}/consensus/decision-{topic}.md`

### Consensus vs. Design Review Board

These patterns serve different purposes:
- **DRB**: Reviews an existing artifact for issues. Produces findings.
- **Consensus**: Resolves a forward-looking decision where no artifact exists yet. Produces a decision.

---

## Pattern Execution Order Within a Stage

When multiple patterns apply to a single stage, they execute in this order:

```
1. Evaluator-Optimizer Loop (always first)
   |
2. Adversarial Review (if applicable to this stage)
   |
3. Gate Evaluation
   |
4. Design Review Board (if enabled and gate passed)
   |
5. BOM Reconciliation (DFM/DFA and Production Release only)
   |
6. Consensus (only when a cross-discipline decision arises)
```

Consensus can be triggered at any point when a cross-discipline decision is needed. It interrupts the normal flow, resolves the decision, then resumes.
