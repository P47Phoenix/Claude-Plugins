# Quality Gates Reference

**Status**: COMPLETE (US-103)
**Version**: 1.0
**Architecture Reference**: Section 3.1, 10.1, 10.2

This file is the authoritative source for gate definitions, pass/fail criteria, DoD validator dispatch templates, severity levels, gate strictness behavior, self-correction protocol, and hardware-specific gate criteria.

---

## Severity Definitions

| Level | Description | Examples |
|-------|-------------|---------|
| Critical | Design will not function or is unsafe | Missing decoupling on voltage regulator, power rail shorted to ground, component rated below operating voltage |
| Major | Significant design issue affecting reliability or manufacturability | Inadequate derating, missing pull-up on I2C bus, trace width below current capacity |
| Minor | Best practice deviation, cosmetic, or optimization opportunity | Non-ideal decoupling cap placement, silk screen overlap, suboptimal component orientation |
| Info | Informational observation | Alternative component suggestion, layout optimization hint, documentation note |

---

## Gate Strictness Behavior

Governed by `gate_strictness` in `.hardware/config.yml`. Default: `standard`.

| Strictness | Critical | Major | Minor |
|------------|----------|-------|-------|
| `strict` | BLOCKS (NOT_DONE) | BLOCKS (NOT_DONE) | BLOCKS (NOT_DONE) |
| `standard` | BLOCKS (NOT_DONE) | BLOCKS (NOT_DONE) | PASS (logged in gate results) |
| `relaxed` | BLOCKS (NOT_DONE) | PASS (logged as warning) | PASS (logged in gate results) |

Zero findings results in DONE (clean pass) regardless of strictness level.

---

## Self-Correction Protocol

When a gate returns NOT_DONE, the orchestrator triggers self-correction before escalating to rework.

### Iteration Limits

| Parameter | Default | Config Key | Scope |
|-----------|---------|------------|-------|
| Max self-correction iterations per gate | 3 | `rework.max_rework_iterations` | Per individual gate evaluation |
| Max total reworks across pipeline | 10 | `rework.max_total_reworks` | Across all paths in a single pipeline run |

### Self-Correction Flow

```
Stage completes --> Gate evaluates --> NOT_DONE
  |
  +-- Iteration 1: Failing validator feedback returned to stage sub-agent
  |     +-- Sub-agent receives: original artifacts + gate findings + specific remediation guidance
  |     +-- Sub-agent re-executes the failing portion of the stage
  |     +-- Gate re-evaluates
  |     +-- If DONE: pipeline advances
  |     +-- If NOT_DONE: continue to iteration 2
  |
  +-- Iteration 2: Same as iteration 1 with accumulated findings
  |
  +-- Iteration 3 (max): Same pattern
  |     +-- If still NOT_DONE after max iterations:
  |           +-- Pipeline PAUSES
  |           +-- Escalation to human with: gate findings history, iteration count,
  |               recurring failure pattern, recommendation
  |           +-- Human options: override (accept with waiver), rework (trigger rework loop),
  |               abort (stop pipeline)
```

### Escalation Rules

1. **Per-gate exhaustion**: When self-correction iterations for a single gate exceed `max_rework_iterations`, the pipeline pauses and escalates. The escalation message includes:
   - Which gate failed and which validators returned NOT_DONE
   - Findings from each iteration showing the correction trajectory
   - Whether the findings are converging (improving) or oscillating
   - Specific recommendation (rework to earlier stage vs. human override)

2. **Global exhaustion**: When total rework count across ALL paths exceeds `max_total_reworks`, any further rework or self-correction triggers a global pause with full rework history and pattern summary.

3. **Waiver protocol**: A human override of a gate failure is recorded as a waiver in the gate results:
   ```yaml
   - stage: 2
     gate: schematic-review-gate
     result: WAIVED
     waiver_reason: "Accepted risk: minor derating on C7 for prototype only"
     waived_findings: ["SCH-DER-001"]
     timestamp: "2026-04-12T12:30:00Z"
   ```

---

## Gate Index

| Gate | Stage(s) | Type | Validators | kicad-happy Skills |
|------|----------|------|------------|-------------------|
| Concept Gate | 1 | Standard | Requirements Completeness, Feasibility Check | None |
| Schematic Review Gate | 2 | Iterative (multi-reviewer) | 7 category validators (see below) | kicad, spice |
| DRC Gate | 3 | Automated | DRC rules (fab-specific) | kicad |
| Human Confirmation Gate | 4, 7 | Manual | Human approval | None |
| DFM Gate | 5 | Automated | Fab-specific DFM rules | jlcpcb/pcbway |
| BOM Gate | 5 | Automated | Cost, availability, lifecycle, second-source | bom, digikey/mouser/lcsc/element14 |
| Compliance Gate | 6 | Evidence-linked | Per-region regulatory checklist | emc, kidoc |
| Final Gate | 8 | Aggregate | All artifacts complete, all prior gates passed | kidoc, bom |

---

## 1. Concept Gate (Stage 1)

**Type**: Standard
**Primary Role**: HW Product Owner
**Validators**: 2

### Validator: requirements-completeness

| Field | Value |
|-------|-------|
| ID | `requirements-completeness` |
| Description | All functional and non-functional requirements are captured with acceptance criteria |
| Role | HW Product Owner |
| Severity if missing | Major |

**Pass criteria**:
- [ ] Functional requirements documented with measurable acceptance criteria
- [ ] Non-functional requirements documented (power, size, thermal, environmental)
- [ ] Interface requirements documented (connectors, protocols, voltage levels)
- [ ] Regulatory requirements identified (target markets, applicable standards)
- [ ] BOM budget target defined (or explicitly marked as unconstrained)
- [ ] Production volume target defined

**Fail criteria**: Any of the above unchecked.

### Validator: feasibility-check

| Field | Value |
|-------|-------|
| ID | `feasibility-check` |
| Description | Technical feasibility confirmed for key requirements |
| Role | HW Product Owner (with EE input if needed) |
| Severity if missing | Major |

**Pass criteria**:
- [ ] Key components identified and confirmed available (not EOL/NRND)
- [ ] Power budget feasible within constraints
- [ ] Physical size constraints achievable with proposed architecture
- [ ] No known regulatory blockers for target markets
- [ ] Make-vs-buy decisions documented for key subsystems

**Fail criteria**: Any feasibility concern rated Critical or Major without a documented mitigation.

### Output artifacts
- `.hardware/artifacts/01-concept/requirements.md`
- `.hardware/artifacts/01-concept/constraints.md`
- `.hardware/artifacts/01-concept/regulatory-scan.md`
- `.hardware/artifacts/01-concept/bom-budget.md`

---

## 2. Schematic Review Gate (Stage 2)

**Type**: Iterative (multi-reviewer with forced-find prompting)
**Primary Role**: Electrical Engineer
**Validators**: 7 category validators
**Review Passes**: Configured via `review.schematic_review_passes` (default: 2, range: 1-5)

### Architecture

The Schematic Review Gate uses the iterative review agent pattern (architecture Section 10.1):

1. **N parallel reviewers** (each an independent EE sub-agent with forced-find prompting)
2. **Deterministic deduplication** (component + category matching, NOT LLM-based)
3. **Coverage check** (all 7 categories examined by at least one reviewer)
4. **Gate evaluation** (severity thresholds per `gate_strictness` config)

### Forced-Find Prompting

Each reviewer receives:
```
You MUST identify at least 2 potential issues across the 7 review categories.
If you believe none are real, explain why each candidate was dismissed.
For each of the 7 categories, report whether you examined it:
CATEGORY_EXAMINED: <name> or CATEGORY_NOT_EXAMINED: <name>.
```

### 7 Review Category Validators

#### Validator: power-integrity

| Field | Value |
|-------|-------|
| ID | `power-integrity` |
| Description | Power distribution network is robust and stable |
| Role | Electrical Engineer |

**Criteria** (severity levels indicated):
- [ ] **Critical**: Every voltage regulator has adequate input and output bulk capacitance per datasheet
- [ ] **Critical**: Power sequencing requirements met for multi-rail designs
- [ ] **Major**: Voltage regulator stability analysis performed (phase margin, load transient)
- [ ] **Major**: Inrush current within connector/fuse ratings
- [ ] **Minor**: Power indicator LEDs present on each rail (where applicable)
- [ ] **Minor**: Test points on each power rail

#### Validator: signal-integrity

| Field | Value |
|-------|-------|
| ID | `signal-integrity` |
| Description | Signal paths maintain integrity for target data rates |
| Role | Electrical Engineer |

**Criteria**:
- [ ] **Critical**: High-speed signals (>50 MHz) have impedance-controlled routing specified
- [ ] **Critical**: Differential pairs matched in length within tolerance
- [ ] **Major**: Series termination resistors on high-speed outputs
- [ ] **Major**: Crosstalk risk assessed for parallel high-speed traces
- [ ] **Minor**: Signal integrity simulation performed for critical nets
- [ ] **Info**: Rise/fall time budget documented

#### Validator: component-derating

| Field | Value |
|-------|-------|
| ID | `component-derating` |
| Description | All components operated within safe margins |
| Role | Electrical Engineer |

**Criteria**:
- [ ] **Critical**: Voltage derating: no component operated above 80% of absolute max voltage rating
- [ ] **Critical**: Current derating: no component operated above 80% of max current rating at operating temperature
- [ ] **Major**: Temperature derating: components rated for operating temperature range with margin
- [ ] **Major**: Power dissipation within package thermal limits (junction temp calculation)
- [ ] **Minor**: Capacitor voltage derating follows ceramic vs. electrolytic guidelines (50% for ceramic, 60-80% for electrolytic)

#### Validator: pull-ups-pull-downs

| Field | Value |
|-------|-------|
| ID | `pull-ups-pull-downs` |
| Description | No floating inputs; all bus lines properly terminated |
| Role | Electrical Engineer |

**Criteria**:
- [ ] **Critical**: All IC input pins connected (no floating inputs)
- [ ] **Critical**: Reset pins have pull-up/pull-down per datasheet recommendation
- [ ] **Major**: I2C bus has pull-up resistors with correct value for bus capacitance and speed
- [ ] **Major**: SPI chip-select lines have pull-ups to prevent spurious selection
- [ ] **Major**: Enable/shutdown pins explicitly driven (not left floating)
- [ ] **Minor**: Unused GPIO pins configured with weak pull-ups/pull-downs

#### Validator: decoupling

| Field | Value |
|-------|-------|
| ID | `decoupling` |
| Description | Decoupling strategy is complete and correct |
| Role | Electrical Engineer |

**Criteria**:
- [ ] **Critical**: Every IC power pin has a local decoupling capacitor (100nF minimum)
- [ ] **Critical**: High-current ICs (>100mA) have bulk capacitance (10uF+) within 10mm
- [ ] **Major**: Decoupling capacitor values match IC datasheet recommendations
- [ ] **Major**: Ferrite beads or LC filters on analog power pins where specified
- [ ] **Minor**: Capacitor ESR considered for high-frequency decoupling effectiveness
- [ ] **Info**: Decoupling strategy document references component placement guidelines

#### Validator: voltage-level-compat

| Field | Value |
|-------|-------|
| ID | `voltage-level-compat` |
| Description | All interfaces operate within compatible voltage domains |
| Role | Electrical Engineer |

**Criteria**:
- [ ] **Critical**: No 5V signal connected directly to 3.3V-only input without level translation
- [ ] **Critical**: Mixed voltage domain interfaces have explicit level shifters or voltage translators
- [ ] **Major**: Open-drain outputs pulled up to correct voltage domain
- [ ] **Major**: ADC/DAC reference voltages within input range of connected signals
- [ ] **Minor**: Logic family compatibility verified (CMOS/TTL threshold levels)

#### Validator: thermal

| Field | Value |
|-------|-------|
| ID | `thermal` |
| Description | Thermal management is adequate for operating conditions |
| Role | Electrical Engineer |

**Criteria**:
- [ ] **Critical**: Components with >1W dissipation have thermal relief paths (thermal vias, copper pour, heatsink)
- [ ] **Major**: Junction temperature calculations performed for all power semiconductors
- [ ] **Major**: Thermal derating curve consulted for ambient temperature range
- [ ] **Minor**: Hot components not placed adjacent to temperature-sensitive components
- [ ] **Info**: Thermal simulation recommended for designs with >5W total dissipation

### Deduplication Rules

Per architecture Section 10.1.1 -- deterministic, NOT LLM-based:

| Finding Scope | Match Fields | Rule |
|---------------|-------------|------|
| Component-level | `component` + `category` | Exact match (case-insensitive) |
| Net-level | `net` + `category` | Exact match (case-insensitive) |
| Board-level | `category` + `board_issue_id` | Exact match (case-insensitive); unclassified findings treated as distinct |

**Merge behavior**: Keep highest severity, concatenate descriptions with reviewer attribution, tag `confirmed_by: N`.

### Coverage Check

- All 7 categories must be examined by at least one reviewer (CATEGORY_EXAMINED signal)
- Coverage met when all 7 covered OR configured passes reached, whichever first
- Coverage ensures systematic review, not just finding-overlap coincidence

### Finding Format

```yaml
- id: "SCH-PWR-001"
  severity: critical
  category: power-integrity
  component: "U3"          # null for net/board-level
  net: ""                  # e.g., "VCC_3V3" for net-level
  board_issue_id: ""       # e.g., "global-decoupling" for board-level
  description: "U3 (LDO) output capacitor C12 is 1uF; datasheet requires minimum 4.7uF for stability"
  fix: "Replace C12 with 4.7uF or greater ceramic capacitor (X5R/X7R)"
  location: "Sheet 1, U3 output"
  confirmed_by: 2          # Added by dedup engine
```

### Board Issue ID Enum

| ID | Description |
|----|-------------|
| `global-decoupling` | Global decoupling strategy insufficient or absent |
| `power-sequencing` | Power supply sequencing order incorrect or uncontrolled |
| `ground-plane` | Ground plane integrity issue (splits, insufficient copper, impedance) |
| `thermal-management` | Board-level thermal dissipation strategy inadequate |
| `emc-shielding` | Board-level EMC/EMI shielding strategy inadequate |
| `stack-up` | PCB stackup creates systemic signal/power integrity issues |
| `voltage-domain-isolation` | Mixed voltage domains lack proper isolation or level shifting |
| `clock-distribution` | Clock distribution topology creates systemic jitter/skew issues |

### Output artifacts
- `.hardware/artifacts/02-schematic/schematic-review.md`
- `.hardware/artifacts/02-schematic/component-rationale.md`
- `.hardware/artifacts/02-schematic/simulation-results.md`
- `.hardware/artifacts/02-schematic/firmware-interface.md`

---

## 3. DRC Gate (Stage 3)

**Type**: Automated
**Primary Role**: PCB Layout Engineer
**Validators**: 1 (DRC rule set from target fab)
**Consumes**: `kicad-happy:kicad` (PCB/DRC analysis)

### Validator: drc-pass

| Field | Value |
|-------|-------|
| ID | `drc-pass` |
| Description | Design Rule Check passes against target fab capabilities |
| Role | PCB Layout Engineer |

**Hardware-Specific Criteria**:

#### Impedance Control
- [ ] **Critical**: Controlled impedance traces match stackup calculator values within +/-10%
- [ ] **Critical**: Differential pair impedance matches specification (e.g., 90 ohm USB, 100 ohm Ethernet)
- [ ] **Major**: Impedance test coupons included on panel (for production builds)

#### Thermal Analysis
- [ ] **Major**: Copper pour connected to thermal pads via thermal relief or direct connection per requirements
- [ ] **Major**: High-current traces widened per IPC-2221 current capacity charts
- [ ] **Minor**: Thermal vias under QFN/BGA thermal pads (minimum 4 vias per pad)

#### Manufacturing Constraints (fab-specific)
- [ ] **Critical**: Minimum trace width meets fab capability (e.g., JLCPCB: 0.127mm/5mil standard, 0.09mm/3.5mil advanced)
- [ ] **Critical**: Minimum trace spacing meets fab capability
- [ ] **Critical**: Minimum drill size meets fab capability (e.g., JLCPCB: 0.3mm standard, 0.15mm advanced)
- [ ] **Major**: Annular ring meets fab minimum (e.g., JLCPCB: 0.13mm)
- [ ] **Major**: Board outline clearance to copper meets minimum
- [ ] **Minor**: Silkscreen line width meets minimum (typically 0.15mm)
- [ ] **Minor**: Solder mask web width meets minimum (typically 0.1mm)

#### DRC Rule Categories
- [ ] **Critical**: No unconnected nets (ratsnest clean)
- [ ] **Critical**: No copper-to-copper clearance violations
- [ ] **Major**: No courtyard overlaps between components
- [ ] **Major**: No silkscreen-on-pad violations
- [ ] **Minor**: No silkscreen overlap warnings

**Pass criteria**: Zero DRC errors. Warnings are logged but do not block.

**Finding format**:
```yaml
- rule_id: "DRC-CLR-001"
  severity: error
  location: "Layer F.Cu, (45.2mm, 22.1mm)"
  description: "Clearance violation: 0.08mm between net VCC_3V3 and GND (minimum 0.127mm)"
  remediation: "Increase spacing between traces or use narrower trace width with controlled impedance"
```

### Automated DRC Validation Workflow

The DRC gate runs as a fully automated validation with no human intervention required.

#### Execution Sequence

```
DRC Gate activates
  |
  +-- 1. Load target fab capabilities from config (`target_fab` key)
  |     +-- JLCPCB: standard rules (0.127mm trace, 0.3mm drill, 0.13mm annular ring)
  |     +-- PCBWay: standard rules (0.1mm trace, 0.2mm drill, 0.15mm annular ring)
  |     +-- Custom: rules from `.hardware/fab-rules/<fab-name>.yml`
  |
  +-- 2. Dispatch `kicad-happy:kicad` with PCB file path
  |     +-- Extract DRC violations from KiCad DRC report
  |     +-- Parse each violation into structured finding format
  |
  +-- 3. Classify violations by severity
  |     +-- error: clearance, unconnected nets, short circuits --> BLOCKS gate
  |     +-- warning: silkscreen overlap, courtyard overlap --> logged, does NOT block
  |
  +-- 4. Generate remediation guidance per violation
  |     +-- Each finding includes specific fix action (not generic advice)
  |     +-- Location pinpointed to layer, coordinates, and net names
  |
  +-- 5. Evaluate gate result
        +-- Zero errors --> DONE (warnings logged in drc-results.md)
        +-- Any errors --> NOT_DONE (triggers self-correction per Section above)
```

#### Fab-Specific Rule Mapping

| Parameter | JLCPCB Standard | JLCPCB Advanced | PCBWay Standard | PCBWay Advanced |
|-----------|----------------|-----------------|-----------------|-----------------|
| Min trace width | 0.127mm (5mil) | 0.09mm (3.5mil) | 0.1mm (4mil) | 0.075mm (3mil) |
| Min trace spacing | 0.127mm (5mil) | 0.09mm (3.5mil) | 0.1mm (4mil) | 0.075mm (3mil) |
| Min drill size | 0.3mm | 0.15mm (micro via) | 0.2mm | 0.15mm |
| Min annular ring | 0.13mm | 0.1mm | 0.15mm | 0.1mm |
| Min silkscreen width | 0.15mm | 0.1mm | 0.15mm | 0.1mm |
| Min solder mask web | 0.1mm | 0.075mm | 0.1mm | 0.075mm |
| Board thickness range | 0.4-2.4mm | 0.4-2.4mm | 0.2-6.0mm | 0.2-6.0mm |
| Max board layers | 20 | 20 | 14 | 14 |

#### Remediation Guidance Template

Each DRC finding's `remediation` field follows this pattern:

```
[ACTION]: [SPECIFIC_CHANGE] [FROM_VALUE] -> [TO_VALUE] at [LOCATION]
```

Examples:
- "Widen trace from 0.10mm to 0.127mm on net VCC_3V3, Layer F.Cu near U3 pin 1"
- "Increase via drill from 0.25mm to 0.30mm for via at (45.2, 22.1)"
- "Add thermal relief to pad 3 of U7 connected to copper pour on Layer In1.Cu"

### Output artifacts
- `.hardware/artifacts/03-layout/layout-review.md`
- `.hardware/artifacts/03-layout/routing-analysis.md`
- `.hardware/artifacts/03-layout/drc-results.md`

---

## 4. Human Confirmation Gate (Stages 4, 7)

**Type**: Manual
**Primary Role**: Test Engineer (Stage 4), Manufacturing Engineer (Stage 7)
**Pattern**: gate-in / human-action / gate-out (architecture Section 3.4)

### Validator: human-confirmation

| Field | Value |
|-------|-------|
| ID | `human-confirmation` |
| Description | Human confirms physical stage completion |
| Role | Human operator |

**Gate-In Phase** (AI-generated):
- Preparation artifacts generated and presented to user
- Structured action items with numbered checklist
- Artifacts saved to `.hardware/artifacts/<stage-name>/`

**Human-Action Phase** (pipeline pauses):
- Pipeline state transitions to `PAUSED_AWAITING_HUMAN`
- User performs physical work (ordering, assembly, testing, manufacturing)
- User responds: `"<stage> complete"` or `"<stage> failed: <description>"`

**Gate-Out Phase** (AI evaluates):
- On "complete": gate returns DONE, pipeline advances
- On "failed: <description>": rework triggered per rework path table
- On "save pipeline state": state persisted for cross-session resume

**Staleness detection** applies per architecture Section 3.4.1.

### Stage 4 (Prototype) Specific
- Action items: order PCBs, order components, assemble, perform bring-up testing
- Ordering package references target fab (JLCPCB/PCBWay) via kicad-happy skills
- Test procedure generated from test strategy artifacts

### Stage 7 (Pilot Run) Specific
- Action items: transfer to manufacturing, run pilot batch, measure yield
- Manufacturing transfer package generated
- Production test procedure generated
- Yield targets defined and measured

### Output artifacts (Stage 4)
- `.hardware/artifacts/04-prototype/ordering-package.md`
- `.hardware/artifacts/04-prototype/test-procedure.md`
- `.hardware/artifacts/04-prototype/test-fixture-requirements.md`

### Output artifacts (Stage 7)
- `.hardware/artifacts/07-pilot-run/manufacturing-transfer.md`
- `.hardware/artifacts/07-pilot-run/production-test-procedure.md`
- `.hardware/artifacts/07-pilot-run/yield-targets.md`

---

## 5a. DFM Gate (Stage 5)

**Type**: Automated
**Primary Role**: Manufacturing Engineer
**Consumes**: `kicad-happy:jlcpcb` or `kicad-happy:pcbway` (per `target_fab` config)

### Validator: dfm-pass

| Field | Value |
|-------|-------|
| ID | `dfm-pass` |
| Description | Design meets target fab house manufacturability requirements |
| Role | Manufacturing Engineer |

**Hardware-Specific Criteria**:

#### Trace/Space Minimums
- [ ] **Critical**: All trace widths >= fab minimum (JLCPCB standard: 0.127mm, PCBWay standard: 0.1mm)
- [ ] **Critical**: All trace spacing >= fab minimum (JLCPCB standard: 0.127mm, PCBWay standard: 0.1mm)
- [ ] **Major**: Controlled impedance traces use fab-validated stackup values
- [ ] **Minor**: Traces wider than minimum where space permits (reliability margin)

#### Via Sizes
- [ ] **Critical**: Via drill diameter >= fab minimum (JLCPCB: 0.3mm standard, 0.15mm micro)
- [ ] **Critical**: Via annular ring >= fab minimum (JLCPCB: 0.13mm)
- [ ] **Major**: Via aspect ratio within fab capability (typically <=8:1 for standard, <=10:1 for advanced)
- [ ] **Major**: Via-to-pad clearance meets minimum
- [ ] **Minor**: Via-in-pad used only where necessary (adds cost for filled/capped vias)

#### Layer Count
- [ ] **Major**: Board layer count within fab standard offerings (JLCPCB: 1-20 layers)
- [ ] **Major**: Stackup symmetric for mechanical stability
- [ ] **Minor**: Layer count optimized for cost (fewer layers = lower cost)

#### Surface Finish
- [ ] **Major**: Surface finish compatible with component requirements (HASL for through-hole heavy, ENIG for fine-pitch)
- [ ] **Major**: Surface finish compatible with soldering process (lead-free HASL or ENIG for RoHS)
- [ ] **Minor**: Surface finish cost-optimized for production volume

#### General DFM
- [ ] **Critical**: Minimum copper-to-edge clearance met (typically 0.25mm)
- [ ] **Major**: Fiducial marks present for SMT assembly (minimum 3 per board, 2 per panel)
- [ ] **Major**: Component footprints match IPC-7351 or fab library
- [ ] **Major**: Solder paste aperture sizes optimized for component pitch
- [ ] **Minor**: Panelization-friendly board outline (rectangular, V-score or tab-routed)
- [ ] **Minor**: Tooling holes present for panel registration

**Finding format**:
```yaml
- rule_id: "DFM-TRC-001"
  parameter: "trace_width"
  min_value: "0.127mm"
  board_value: "0.10mm"
  pass: false
  location: "Layer F.Cu, net VCC_3V3"
  remediation: "Widen trace from 0.10mm to 0.127mm minimum, or use advanced process capability"
```

### Output artifacts
- `.hardware/artifacts/05-dfm-dfa/dfm-report.md`
- `.hardware/artifacts/05-dfm-dfa/dfa-report.md`
- `.hardware/artifacts/05-dfm-dfa/yield-assessment.md`

---

## 5b. BOM Gate (Stage 5)

**Type**: Automated
**Primary Role**: Manufacturing Engineer
**Consumes**: `kicad-happy:bom`, `kicad-happy:digikey`, `kicad-happy:mouser`, `kicad-happy:lcsc`, `kicad-happy:element14`

### Validator: bom-pass

| Field | Value |
|-------|-------|
| ID | `bom-pass` |
| Description | BOM meets cost, availability, lifecycle, and sourcing requirements |
| Role | Manufacturing Engineer |

**Hardware-Specific Criteria**:

#### Cost Validation
- [ ] **Major**: Total BOM cost per unit <= `bom_budget` from config (if set)
- [ ] **Major**: Cost breakdown by category (ICs, passives, connectors, mechanicals) documented
- [ ] **Minor**: Cost optimization opportunities identified (alternative components, quantity breaks)
- [ ] **Info**: Extended cost calculated at target production volume

#### Component Availability
- [ ] **Critical**: All components in stock at minimum one distributor with sufficient quantity for prototype
- [ ] **Major**: Lead time for all components <= 4 weeks (or flagged with mitigation)
- [ ] **Minor**: Components available at multiple distributors (supply chain resilience)

#### Lifecycle Status
- [ ] **Critical**: No obsolete components (lifecycle: OBSOLETE blocks gate)
- [ ] **Major**: No NRND (Not Recommended for New Design) components without explicit risk acceptance and documented alternative
- [ ] **Major**: No EOL (End of Life) announced components without transition plan
- [ ] **Minor**: Components with >5 year expected lifecycle preferred
- [ ] **Info**: Lifecycle status source documented (distributor, manufacturer)

#### Second-Source Validation
- [ ] **Warning/Blocking**: Single-source components flagged (blocking if `second_source_required: true` in config, warning otherwise)
- [ ] **Major**: Critical path components (MCU, power, RF) have second-source documented
- [ ] **Minor**: Passive components from standard series with multiple manufacturers

**Finding format**:
```yaml
- component: "U5"
  mpn: "STM32F401RET6"
  issue: "single-source"
  severity: warning
  detail: "Only available from ST Microelectronics. No pin-compatible second source identified."
  recommendation: "Consider STM32F411RET6 (pin-compatible, also ST only) or redesign for multi-source MCU family"
```

### Output artifacts
- `.hardware/artifacts/05-dfm-dfa/bom-validation.md`

---

## 6. Compliance Gate (Stage 6)

**Type**: Evidence-linked checklist
**Primary Role**: Compliance Engineer
**Consumes**: `kicad-happy:emc`, `kicad-happy:kidoc`

### Validator: compliance-pass

| Field | Value |
|-------|-------|
| ID | `compliance-pass` |
| Description | Design meets all configured regulatory requirements with evidence |
| Role | Compliance Engineer |

**Hardware-Specific Criteria**:

#### EMC Checklist (per `compliance_regions` config)

**FCC Part 15 (US)**:
- [ ] **Critical**: Conducted emissions pre-compliance assessment performed
- [ ] **Critical**: Radiated emissions pre-compliance assessment performed
- [ ] **Major**: ESD protection on all external interfaces
- [ ] **Major**: Common-mode chokes on external cables/connectors
- [ ] **Major**: Ground plane integrity verified (no unnecessary splits)
- [ ] **Minor**: Shield enclosure design considered (if applicable)

**CE RED (EU)**:
- [ ] **Critical**: EMC pre-compliance per EN 55032 (emissions) and EN 55035 (immunity)
- [ ] **Critical**: Radio equipment requirements if wireless (RED Article 3.2)
- [ ] **Major**: Immunity requirements assessed (ESD, surge, burst, radiated/conducted)
- [ ] **Minor**: Technical documentation package structure prepared

**Each requirement linked to evidence**:
```yaml
- requirement: "FCC Part 15 Subpart B - Radiated Emissions"
  standard_clause: "47 CFR 15.109"
  evidence_artifact: ".hardware/artifacts/06-compliance/emc-report.md"
  status: pass | fail | pending
  notes: "Pre-compliance EMC analysis via kicad-happy:emc. Risk score: 3/10 (low)"
```

#### Safety Checklist

**IEC 62368-1 (IT/AV equipment)**:
- [ ] **Critical**: Hazardous voltage isolation meets creepage/clearance requirements
- [ ] **Critical**: Touch current within limits for applicable class
- [ ] **Major**: Fusing and overcurrent protection on all power inputs
- [ ] **Major**: Fire enclosure requirements met (material flammability rating)
- [ ] **Minor**: Safety markings identified (CE, UL, voltage warnings)

**UL (if configured)**:
- [ ] **Critical**: UL recognition requirements for components (capacitors, transformers)
- [ ] **Major**: PCB material flammability rating (UL 94 V-0 minimum)
- [ ] **Minor**: UL file preparation checklist started

#### Environmental Compliance

**RoHS (if configured)**:
- [ ] **Critical**: All BOM components RoHS compliant (documented per component)
- [ ] **Major**: Solder paste and surface finish RoHS compliant
- [ ] **Minor**: RoHS declaration of conformity template prepared

**REACH (if configured)**:
- [ ] **Major**: SVHC (Substances of Very High Concern) screening performed on BOM
- [ ] **Minor**: REACH compliance documentation template prepared

**WEEE (if applicable)**:
- [ ] **Minor**: WEEE marking requirements identified
- [ ] **Info**: WEEE registration requirements for target markets documented

**Gate logic**: ANY requirement with status `fail` or `pending` (no linked evidence) returns NOT_DONE. All requirements must be `pass` with linked evidence for DONE.

### Output artifacts
- `.hardware/artifacts/06-compliance/emc-report.md`
- `.hardware/artifacts/06-compliance/safety-analysis.md`
- `.hardware/artifacts/06-compliance/environmental-checklist.md`
- `.hardware/artifacts/06-compliance/compliance-package.md`

---

## 7. Final Gate (Stage 8)

**Type**: Aggregate
**Primary Role**: Manufacturing Engineer
**Validators**: Aggregate of all prior gates plus production readiness checks

### Validator: final-aggregate

| Field | Value |
|-------|-------|
| ID | `final-aggregate` |
| Description | All pipeline artifacts complete and all prior gates passed or waived |
| Role | Manufacturing Engineer |

**Pass criteria**:
- [ ] **Critical**: All 7 prior gates have result DONE or WAIVED (no NOT_DONE or PENDING)
- [ ] **Critical**: All artifact files in the artifact registry exist on disk
- [ ] **Critical**: Final BOM matches schematic netlist (no orphan components)
- [ ] **Major**: All waivers have documented justification and risk acceptance
- [ ] **Major**: Compliance package complete for all configured regions
- [ ] **Major**: Production test procedure documented and reviewed
- [ ] **Minor**: Release documentation complete (revision history, known issues, errata)
- [ ] **Info**: Manufacturing transfer package reviewed by manufacturing engineer

**Aggregate check logic**:
```
For each stage S in [1..7]:
  gate_result = state.gates[S].result
  IF gate_result NOT IN [DONE, WAIVED]:
    RETURN NOT_DONE with "Stage {S} gate not passed: {gate_result}"
  IF gate_result == WAIVED:
    LOG WARNING "Stage {S} gate was waived: {waiver_reason}"

For each artifact A in state.artifacts:
  IF NOT file_exists(A.path):
    RETURN NOT_DONE with "Missing artifact: {A.path}"

RETURN DONE
```

### Output artifacts
- `.hardware/artifacts/08-production-release/production-checklist.md`
- `.hardware/artifacts/08-production-release/final-bom.md`
- `.hardware/artifacts/08-production-release/compliance-package.md`
- `.hardware/artifacts/08-production-release/release-documentation.md`

---

## Design Review Board Protocol

The Design Review Board (DRB) is a collaboration pattern activated at key stage transitions when `review.design_review_board: true` in config.

### When DRB Activates
- After Schematic stage (before Layout)
- After Layout stage (before Prototype)
- After DFM/DFA stage (before Compliance)

### DRB Execution

```
Design Review Board
  |
  +-- Dispatch: EE reviewer (schematic/electrical perspective)
  |     +-- Independent context (no shared findings)
  |     +-- Produces: findings from EE perspective
  |
  +-- Dispatch: PCB Layout reviewer (physical/routing perspective)
  |     +-- Independent context
  |     +-- Produces: findings from layout perspective
  |
  +-- Dispatch: MfgE reviewer (manufacturability perspective)
  |     +-- Independent context
  |     +-- Produces: findings from manufacturing perspective
  |
  +-- Dispatch: CompE reviewer (compliance perspective, if compliance regions configured)
  |     +-- Independent context
  |     +-- Produces: findings from compliance perspective
  |
  +-- Aggregation (deterministic dedup, same rules as Schematic Review Gate)
  |     +-- Cross-reviewer deduplication
  |     +-- Unified severity ranking
  |     +-- Results organized by reviewer role
  |
  +-- Gate evaluation per strictness level
```

### DRB Finding Format

Same as Schematic Review Gate finding format, with additional `reviewer_role` field:
```yaml
- id: "DRB-MFG-001"
  reviewer_role: manufacturing-engineer
  severity: major
  category: "manufacturability"
  component: "U3"
  description: "QFN-48 package requires stencil aperture optimization for paste volume"
  fix: "Reduce stencil aperture to 80% of pad size per IPC-7525"
```

---

## DoD Validator Assignment Summary

| Stage | Gate | Validators | Assigned Roles |
|-------|------|------------|----------------|
| 1 - Concept | Concept Gate | requirements-completeness, feasibility-check | HW Product Owner |
| 2 - Schematic | Schematic Review Gate | power-integrity, signal-integrity, component-derating, pull-ups-pull-downs, decoupling, voltage-level-compat, thermal | Electrical Engineer (multi-reviewer) |
| 3 - Layout | DRC Gate | drc-pass | PCB Layout Engineer |
| 4 - Prototype | Human Confirmation Gate | human-confirmation | Human (Test Engineer prepares) |
| 5 - DFM/DFA | DFM Gate + BOM Gate | dfm-pass, bom-pass | Manufacturing Engineer |
| 6 - Compliance | Compliance Gate | compliance-pass | Compliance Engineer |
| 7 - Pilot Run | Human Confirmation Gate | human-confirmation | Human (Manufacturing Engineer prepares) |
| 8 - Prod. Release | Final Gate | final-aggregate | Manufacturing Engineer |
