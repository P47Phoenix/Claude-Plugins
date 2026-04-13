# Schematic Review Gate

**Status**: COMPLETE (US-401)
**Version**: 1.0
**Architecture Reference**: Section 10.1, 10.1.1, 10.2, 10.3, 10.4
**Story**: US-401 -- Schematic Review Gate
**Minimum Model Tier**: Sonnet+ (all reviewers)

The Schematic Review Gate is the multi-reviewer validation gate for Stage 2 (Schematic). It applies the iterative review agent pattern from issue #76 to catch electrical design errors before layout begins. No design flaw shall pass unchallenged. And my code!

---

## 1. Review Categories

The gate covers 7 review categories. Every reviewer must explicitly report coverage status for each.

| # | Category ID | Category Name | What It Checks |
|---|-------------|---------------|----------------|
| 1 | `power-integrity` | Power Integrity | Bulk caps, decoupling, voltage regulator stability, power sequencing, inrush current |
| 2 | `signal-integrity` | Signal Integrity | Termination, impedance matching, crosstalk risk, high-speed routing, differential pairs |
| 3 | `component-derating` | Component Derating | Voltage/current/temperature derating vs. operating conditions, thermal limits |
| 4 | `pull-ups-pull-downs` | Missing Pull-ups/Pull-downs | Floating inputs, I2C bus pull-ups, reset pins, enable pins, SPI chip-selects, unused GPIOs |
| 5 | `decoupling` | Decoupling Strategy | Per-IC decoupling, capacitor value selection, placement distance, ESR, bulk capacitance |
| 6 | `voltage-level-compat` | Voltage Level Compatibility | Logic level translation, mixed-voltage interfaces, tolerance bands, ADC/DAC reference voltages |
| 7 | `thermal` | Thermal Considerations | Power dissipation, thermal relief, heat sink requirements, junction temperature calculations |

Full pass/fail criteria for each category are defined in `quality-gates.md` Section 2 (Schematic Review Gate validators).

---

## 2. Reviewer Agent Roster

Each reviewer is a named specialist persona dispatched as an independent sub-agent. They carry no shared context during review -- each sees only the schematic and their reference material. Blunt as a dwarven war hammer, each has a specialty domain.

| Persona | Specialty | Primary Categories | Model Tier |
|---------|-----------|-------------------|------------|
| **Vera** (Verification Engineer) | Net connectivity and pull-up/pull-down verification | `pull-ups-pull-downs`, `voltage-level-compat` | Sonnet+ |
| **Netty** (Signal Integrity Specialist) | Signal integrity and impedance analysis | `signal-integrity`, `decoupling` | Sonnet+ |
| **Professor Surge** (Power Domain Expert) | Power integrity and sequencing | `power-integrity`, `decoupling` | Sonnet+ |
| **Dr. Priya** (Derating & Reliability Analyst) | Component derating and thermal analysis | `component-derating`, `thermal` | Sonnet+ |
| **Marco** (Cross-Domain Generalist) | Full-spectrum review across all 7 categories | All categories | Sonnet+ |

### Reviewer Assignment Rules

- **Default** (2 passes): Dispatch Marco as Reviewer 1 and one specialist (rotated or selected based on design complexity) as Reviewer 2.
- **3+ passes**: Dispatch Marco plus 2+ specialists. Prioritize specialists whose primary categories match identified risk areas from the Concept stage requirements.
- **Every reviewer** covers ALL 7 categories regardless of specialty. Specialty determines depth of analysis, not scope of coverage.

### Why Named Personas

Named personas are not cosmetic. They enforce behavioral differentiation in prompted output. A reviewer named "Professor Surge" with a power domain specialty prompt produces more domain-specific findings than a generic "Reviewer 2" prompt. The forced-find mechanism benefits from domain framing because it pushes the reviewer to dig deeper in their area of expertise.

---

## 3. Forced-Find Prompting

Each reviewer receives this instruction block in their sub-agent prompt. No shortcuts, no hand-waving -- you MUST dig, like mining mithril from the deep places.

```
## Forced-Find Protocol

You MUST identify at least 2 potential issues across the 7 review categories.
If you believe none are real issues, explain why each candidate was dismissed
with specific technical justification.

For EACH of the 7 categories, report whether you examined it:
  CATEGORY_EXAMINED: <category-id>
  or
  CATEGORY_NOT_EXAMINED: <category-id> (with reason)

A finding is a structured object with these fields:
- id: Unique identifier (format: SCH-<CATEGORY_ABBREV>-<NNN>, e.g., SCH-PWR-001)
- severity: critical | major | minor | info
- category: One of the 7 category IDs listed above
- component: Reference designator (e.g., "U3", "C7") -- null for net/board-level
- net: Net name (e.g., "VCC_3V3") -- null for component/board-level
- board_issue_id: From the board issue ID enum -- null for component/net-level
- description: What the issue is and why it matters
- fix: Specific recommended remediation
- location: Sheet number, component, or net reference

For any finding that is board-level (not tied to a specific component or net),
you MUST include a board_issue_id field with a value from the board issue enum:
global-decoupling, power-sequencing, ground-plane, thermal-management,
emc-shielding, stack-up, voltage-domain-isolation, clock-distribution.
If none of the enum values fit, use "other-<brief-descriptor>" and the finding
will be treated as distinct (not deduplicated).

After all findings, emit a coverage summary:
COVERAGE: <N>/7 categories examined
```

### Forced-Find Minimum

Each reviewer must produce at least **2 candidate findings**. This is hardcoded in the gate framework (architecture Section 10.3). The minimum exists to counteract the "looks fine to me" failure mode where reviewers rubber-stamp designs without deep analysis.

If a reviewer produces fewer than 2 findings AND does not provide dismissal explanations, the orchestrator flags the review as **incomplete** and re-dispatches that reviewer with an escalated prompt:

```
Your previous review produced <N> findings with no dismissal explanations.
This does not meet the forced-find minimum of 2. Re-examine the schematic
with deeper analysis. If the design is truly clean, explain at least 2
candidate issues you considered and why they were dismissed.
```

---

## 4. Model Tier Requirements

Per architecture Section 10.4 and issue #76 learnings: Haiku is insufficient for geometric and spatial reasoning tasks. The Schematic Review Gate demands strong analytical reasoning across multiple categories.

| Component | Minimum Tier | Rationale |
|-----------|-------------|-----------|
| All review personas (Vera, Netty, Professor Surge, Dr. Priya, Marco) | **Sonnet+** | Multi-category forced-find review demands structured reasoning about circuit topology, derating calculations, and signal integrity analysis |
| Deduplication engine | N/A (deterministic algorithm) | Not an LLM step -- runs as orchestrator logic |
| Coverage check | N/A (deterministic algorithm) | Not an LLM step -- runs as orchestrator logic |
| Gate evaluation | N/A (deterministic algorithm) | Not an LLM step -- follows severity threshold table |
| Documentation-only review (e.g., reviewing schematic annotations for completeness) | **Haiku** acceptable | Text-based review with no spatial/circuit reasoning |

**Enforcement (Phase 1)**: Documentation-only. The orchestrator announces the recommended tier at dispatch but does not programmatically block. Programmatic enforcement is a Phase 2 enhancement.

---

## 5. Parallel Dispatch Pattern

Reviewers are spawned in parallel using multiple Agent tool calls in a single orchestrator message. Each reviewer is an independent sub-agent with its own context -- they do not see each other's work. Like dwarves mining separate tunnels, each one digs alone.

### Dispatch Template (Orchestrator)

The orchestrator dispatches all configured reviewers in a single message containing N Agent tool calls:

```
[Agent tool call 1 - Reviewer 1 (Marco)]
PERSONA: Marco (Cross-Domain Generalist)
ROLE: electrical-engineer
TASK: Schematic Review -- Pass 1

Load: electrical-engineer/SKILL.md + schematic-review.md
Invoke: kicad-happy:kicad for schematic analysis
Apply: Forced-Find Protocol (Section 3 above)
Review: ALL 7 categories
Produce: Structured findings list

[Paste schematic artifact paths here]
[Paste forced-find prompt block here]

[Agent tool call 2 - Reviewer 2 (Specialist)]
PERSONA: Professor Surge (Power Domain Expert)
ROLE: electrical-engineer
TASK: Schematic Review -- Pass 2

Load: electrical-engineer/SKILL.md + schematic-review.md
Invoke: kicad-happy:kicad for schematic analysis
Apply: Forced-Find Protocol (Section 3 above)
Review: ALL 7 categories (depth focus on power-integrity, decoupling)
Produce: Structured findings list

[Paste schematic artifact paths here]
[Paste forced-find prompt block here]

[Agent tool call 3..N - Additional reviewers if configured]
```

### Key Constraints

1. **No shared context**: Each Agent tool call creates an isolated sub-agent. Reviewer 2 does NOT receive Reviewer 1's findings.
2. **All reviewers dispatch in one message**: The orchestrator sends all Agent tool calls in a single response so they execute in parallel.
3. **Each reviewer loads the same references**: `electrical-engineer/SKILL.md` + `schematic-review.md` + the forced-find prompt.
4. **Each reviewer invokes `kicad-happy:kicad`**: For schematic analysis (netlist, component data, pin connections).
5. **Number of reviewers**: Controlled by `review.schematic_review_passes` config (default: 2, range: 1-5).

---

## 6. Deduplication Engine

The deduplication engine runs as a deterministic algorithm in the orchestrator -- NOT as an LLM inference step. This is non-negotiable. Gate decisions depend on deduplication results, and gates must be deterministic per the Business Rules Engine principle. No guesswork, no fuzzy matching. Solid as stone.

### Algorithm

After all reviewer findings are collected, the orchestrator runs deduplication:

```
INPUT: findings[] from all reviewers (flat list)
OUTPUT: deduplicated_findings[] with confirmed_by counts

1. Sort findings by scope:
   - Component-level: component is non-null
   - Net-level: component is null, net is non-null
   - Board-level: both component and net are null

2. For each scope, apply matching rules:

   COMPONENT-LEVEL:
     Match on: component (exact, case-insensitive) AND category (exact)
     Example: (C7, component-derating) from Reviewer 1 matches (c7, component-derating) from Reviewer 2

   NET-LEVEL:
     Match on: net (exact, case-insensitive) AND category (exact)
     Example: (VCC_3V3, power-integrity) from Reviewer 1 matches (vcc_3v3, power-integrity) from Reviewer 2

   BOARD-LEVEL:
     Match on: category (exact) AND board_issue_id (exact, case-insensitive)
     Example: (decoupling, global-decoupling) from Reviewer 1 matches (decoupling, global-decoupling) from Reviewer 2
     EXCEPTION: If board_issue_id is null/empty, the finding is DISTINCT (conservative fallback)

3. For each group of duplicates, merge:
   - severity: Keep HIGHEST (critical > major > minor > info)
   - description: Concatenate with reviewer attribution:
     "Reviewer 1 (Marco): <desc1>. Reviewer 2 (Professor Surge): <desc2>."
   - fix: Keep both fix suggestions, attributed by reviewer
   - confirmed_by: Count of reviewers who independently identified this finding
   - id: Keep the first reviewer's ID

4. Emit deduplicated findings list
```

### Board Issue ID Enum

For board-level findings (not tied to a specific component or net), reviewers must classify using this enum:

| `board_issue_id` | Description |
|-------------------|-------------|
| `global-decoupling` | Global decoupling strategy insufficient or absent |
| `power-sequencing` | Power supply sequencing order incorrect or uncontrolled |
| `ground-plane` | Ground plane integrity issue (splits, insufficient copper, impedance) |
| `thermal-management` | Board-level thermal dissipation strategy inadequate |
| `emc-shielding` | Board-level EMC/EMI shielding strategy inadequate |
| `stack-up` | PCB stackup creates systemic signal/power integrity issues |
| `voltage-domain-isolation` | Mixed voltage domains lack proper isolation or level shifting |
| `clock-distribution` | Clock distribution topology creates systemic jitter/skew issues |

If none fit, the reviewer uses `other-<brief-descriptor>` and the finding is treated as distinct (not deduplicated).

### Why Deterministic

Two smiths may name the same flaw differently, but the flaw itself is one. An LLM-based dedup step would introduce non-determinism into gate outcomes -- the same findings could produce different deduplicated results on re-run, potentially flipping a gate between DONE and NOT_DONE. The deterministic algorithm eliminates this entirely.

---

## 7. Convergence Detection

The gate uses a **coverage-based stopping criterion** (not finding-overlap coincidence). Per architecture Section 10.1 (F-11 resolution):

### Coverage Check Algorithm

```
INPUT: All reviewer outputs (findings + CATEGORY_EXAMINED signals)
OUTPUT: coverage_met (boolean)

1. Initialize coverage_map: { category_id: false } for all 7 categories

2. For each reviewer output:
   a. For each CATEGORY_EXAMINED signal: set coverage_map[category_id] = true
   b. For each finding: set coverage_map[finding.category] = true
      (producing a finding in a category implies examination)

3. Evaluate:
   - If ALL 7 categories are covered (all true): coverage_met = true
   - If configured passes reached: coverage_met = true (regardless of coverage)
   - Otherwise: coverage_met = false
```

### Two-Clean Shortcut (Optional Enhancement)

If `review.early_stop_on_clean` is enabled in config (default: false):
- If 2 consecutive reviewers produce zero findings after forced-find dismissal analysis, the gate may terminate early.
- This is an OPTIMIZATION only. The coverage check remains the primary stopping criterion.
- Early stop is logged: `"Early stop: 2 consecutive clean reviews after N passes."`

### Class Saturation Detection

If `review.class_saturation_detection` is enabled in config (default: false):
- Track the distribution of findings across categories after deduplication.
- If additional review passes stop producing NEW unique findings (all findings from pass N+1 are duplicates of passes 1..N), the category is "saturated."
- If ALL categories with findings are saturated, additional passes are unlikely to produce new insights.
- Saturation is logged: `"Class saturation detected: N categories saturated after M passes."`

### Default Behavior

With default config (no early-stop, no saturation detection):
- Run exactly `review.schematic_review_passes` passes (default: 2)
- Check coverage after all passes complete
- If coverage < 7/7 after all passes: log which categories were not examined (informational, does not block gate evaluation)

---

## 8. Integration with Pipeline

The Schematic Review Gate plugs into the hardware-flow pipeline at Stage 2 (Schematic) as the primary DoD gate.

### Pipeline Position

```
Stage 1 (Concept) --> Concept Gate --> DONE
  |
  v
Stage 2 (Schematic)
  |
  +-- EE sub-agent produces schematic artifacts
  |   +-- .hardware/artifacts/02-schematic/schematic-review.md
  |   +-- .hardware/artifacts/02-schematic/component-rationale.md
  |   +-- .hardware/artifacts/02-schematic/simulation-results.md
  |   +-- .hardware/artifacts/02-schematic/firmware-interface.md
  |
  +-- Schematic Review Gate activates (THIS GATE)
  |   +-- Dispatch N reviewers in parallel (Section 5)
  |   +-- Collect findings
  |   +-- Run deduplication (Section 6)
  |   +-- Run coverage check (Section 7)
  |   +-- Evaluate gate (severity thresholds per gate_strictness)
  |
  +-- Gate result:
      +-- DONE: All findings below blocking threshold --> advance to Stage 3 (Layout)
      +-- NOT_DONE: Blocking findings exist --> trigger self-correction
          +-- Findings returned to EE sub-agent for remediation
          +-- Up to 3 self-correction iterations (per quality-gates.md)
          +-- If still NOT_DONE: escalate to human
```

### Entry Conditions

- Stage 2 (Schematic) work product complete
- Schematic artifacts exist at `.hardware/artifacts/02-schematic/`
- KiCad schematic file (`.kicad_sch`) available for analysis

### Exit Conditions (DoD)

- All 7 review categories examined by at least one reviewer
- Zero findings at or above the blocking severity threshold (per `gate_strictness`)
- Non-blocking findings documented in gate results for visibility
- Gate result recorded in `.hardware/state.md`

### Gate Evaluation (Severity Thresholds)

Governed by `gate_strictness` in `.hardware/config.yml` (default: `standard`):

| Strictness | Critical | Major | Minor |
|------------|----------|-------|-------|
| `strict` | BLOCKS (NOT_DONE) | BLOCKS (NOT_DONE) | BLOCKS (NOT_DONE) |
| `standard` | BLOCKS (NOT_DONE) | BLOCKS (NOT_DONE) | PASS (logged) |
| `relaxed` | BLOCKS (NOT_DONE) | PASS (logged as warning) | PASS (logged) |

Zero findings = DONE (clean pass) regardless of strictness.

### Self-Correction Integration

When the gate returns NOT_DONE:

1. The orchestrator extracts blocking findings from the gate results
2. Findings are formatted as remediation guidance and passed to the EE sub-agent
3. The EE sub-agent addresses the findings and regenerates affected artifacts
4. The Schematic Review Gate re-runs (full cycle: new reviewers, dedup, coverage)
5. Repeat up to `rework.max_rework_iterations` (default: 3)
6. If still NOT_DONE: pipeline pauses and escalates to human

### Design Review Board Integration

After the Schematic Review Gate passes, the Design Review Board (US-501) may optionally activate as a cross-discipline review if `review.design_review_board` is enabled for the post-Schematic transition. The Design Review Board uses the same deduplication engine and finding format but dispatches multiple ROLES (EE, PCB Layout, MfgE, CompE) rather than multiple EE reviewers.

### Config Parameters

| Parameter | Config Key | Default | Range | Description |
|-----------|-----------|---------|-------|-------------|
| Review passes | `review.schematic_review_passes` | 2 | 1-5 | Number of independent reviewer sub-agents |
| Forced-find minimum | (hardcoded) | 2 | N/A | Minimum candidate findings per reviewer |
| Gate strictness | `gate_strictness` | `standard` | strict/standard/relaxed | Severity blocking thresholds |
| Early stop on clean | `review.early_stop_on_clean` | false | true/false | Enable two-clean shortcut |
| Class saturation | `review.class_saturation_detection` | false | true/false | Enable saturation detection |
| Coverage threshold | (hardcoded) | 7/7 | N/A | All categories must be examined |

### Gate Result Format

```yaml
gate: schematic-review-gate
stage: 2
result: DONE | NOT_DONE | WAIVED
passes_run: 2
coverage: 7/7
findings_total: 5
findings_after_dedup: 3
findings_by_severity:
  critical: 0
  major: 1
  minor: 2
  info: 0
blocking_findings: 1
confirmed_findings: 1    # findings identified by 2+ reviewers
reviewers:
  - persona: Marco
    findings_count: 3
    categories_examined: 7
  - persona: Professor Surge
    findings_count: 4
    categories_examined: 7
gate_strictness: standard
timestamp: "2026-04-12T14:00:00Z"
```

---

## Cross-References

- `quality-gates.md` Section 2 -- Full validator criteria for all 7 categories
- `quality-gates.md` -- Self-correction protocol, severity definitions, gate strictness
- `pipeline-stages.md` -- Stage 2 (Schematic) entry/exit conditions
- Architecture Section 10 -- Iterative review agent pattern
- Architecture Section 10.1.1 -- Deterministic deduplication algorithm
- Architecture Section 10.4 -- Model tier requirements
