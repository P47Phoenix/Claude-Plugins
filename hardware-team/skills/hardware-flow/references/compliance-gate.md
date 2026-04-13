# Compliance Gate Reference

**Status**: COMPLETE (US-405)
**Version**: 1.0
**Architecture Reference**: Section 3.1 (Gate Index), quality-gates.md Section 6
**Parent Gate Definition**: `quality-gates.md` Section 6 (Compliance Gate)

This file is the authoritative reference for Compliance Gate validation logic, per-market regulatory checklists, evidence-linking protocol, and kicad-happy:emc integration. It supplements the gate criteria defined in `quality-gates.md`.

---

## Overview

The Compliance Gate validates that the design meets all regulatory requirements for configured target markets. Every requirement must be linked to evidence (test report, analysis, or design artifact) -- unlinked requirements block the gate.

**Gate type**: Evidence-linked checklist
**Primary role**: Compliance Engineer
**Consumes**: `kicad-happy:emc`, `kicad-happy:kidoc`

---

## Validation Workflow

```
Compliance Gate activates
  |
  +-- 1. Load compliance_regions from .hardware/config.yml
  |     +-- e.g., [FCC, CE, UL, RoHS, REACH]
  |     +-- Each region expands into a checklist of requirements
  |
  +-- 2. Generate per-region checklist
  |     +-- Each requirement has: standard clause, description, evidence field, status
  |     +-- Status starts as "pending" (no evidence linked)
  |
  +-- 3. Dispatch kicad-happy:emc for EMC pre-compliance analysis
  |     +-- Receives EMC risk score and findings per check category
  |     +-- Links EMC report as evidence for EMC-related requirements
  |
  +-- 4. Dispatch kicad-happy:kidoc for documentation package generation
  |     +-- Generates compliance documentation templates
  |     +-- Links documentation artifacts as evidence
  |
  +-- 5. Evaluate evidence linkage
  |     +-- For each requirement: check that evidence_artifact exists and status is pass/fail
  |     +-- ANY requirement with status "pending" (no evidence) --> NOT_DONE
  |     +-- ANY requirement with status "fail" --> NOT_DONE
  |
  +-- 6. Gate Evaluation
        +-- All requirements pass with linked evidence --> DONE
        +-- Any gap --> NOT_DONE with missing evidence list
```

---

## Per-Market Regulatory Requirements

### FCC (United States)

**Applicable standard**: 47 CFR Part 15 (Unintentional Radiators)
**Classification**: Class B (residential) unless config specifies Class A (commercial)

| ID | Requirement | Standard Clause | Severity | Evidence Required |
|----|-------------|----------------|----------|-------------------|
| FCC-01 | Conducted emissions pre-compliance | 47 CFR 15.107 | Critical | EMC analysis report from kicad-happy:emc |
| FCC-02 | Radiated emissions pre-compliance | 47 CFR 15.109 | Critical | EMC analysis report from kicad-happy:emc |
| FCC-03 | ESD protection on external interfaces | 47 CFR 15.33 | Major | Schematic review showing TVS/ESD diodes on all external I/O |
| FCC-04 | Common-mode filtering on external cables | Best practice | Major | Schematic review showing CM chokes on cable interfaces |
| FCC-05 | Ground plane integrity | Best practice | Major | PCB layout review confirming unbroken ground plane under signals |
| FCC-06 | FCC marking requirements identified | 47 CFR 15.19 | Minor | Label design or marking specification |
| FCC-07 | FCC ID application prep (if intentional radiator) | 47 CFR Part 15 Subpart C | Critical (if applicable) | Test lab engagement plan |

### CE (European Union)

**Applicable directives**: EMC Directive 2014/30/EU, LVD 2014/35/EU, RED 2014/53/EU (if wireless), RoHS 2011/65/EU

#### EMC Directive (EN 55032 / EN 55035)

| ID | Requirement | Standard Clause | Severity | Evidence Required |
|----|-------------|----------------|----------|-------------------|
| CE-EMC-01 | Conducted emissions pre-compliance | EN 55032, CISPR 32 | Critical | EMC analysis report |
| CE-EMC-02 | Radiated emissions pre-compliance | EN 55032, CISPR 32 | Critical | EMC analysis report |
| CE-EMC-03 | ESD immunity assessment | EN 55035, IEC 61000-4-2 | Major | ESD protection design review |
| CE-EMC-04 | Electrical fast transient (burst) immunity | EN 55035, IEC 61000-4-4 | Major | Burst protection design review |
| CE-EMC-05 | Surge immunity assessment | EN 55035, IEC 61000-4-5 | Major | Surge protection design review |
| CE-EMC-06 | Radiated immunity assessment | EN 55035, IEC 61000-4-3 | Major | Shielding and filtering review |
| CE-EMC-07 | Conducted immunity assessment | EN 55035, IEC 61000-4-6 | Major | Filtering design review |
| CE-EMC-08 | Technical documentation package structure | Annex III | Minor | Documentation template prepared |

#### Radio Equipment Directive (if wireless)

| ID | Requirement | Standard Clause | Severity | Evidence Required |
|----|-------------|----------------|----------|-------------------|
| CE-RED-01 | Radio equipment essential requirements | RED Article 3.2 | Critical | RF design compliance analysis |
| CE-RED-02 | Spectrum efficiency | RED Article 3.2(a) | Major | RF parameter design review |
| CE-RED-03 | Notified body engagement (if required) | RED Article 17 | Major | Test lab engagement plan |

#### Low Voltage Directive

| ID | Requirement | Standard Clause | Severity | Evidence Required |
|----|-------------|----------------|----------|-------------------|
| CE-LVD-01 | Safety assessment per IEC 62368-1 | EN 62368-1 | Critical | Safety analysis report |
| CE-LVD-02 | Creepage and clearance analysis | IEC 62368-1, Table 26-28 | Critical | PCB layout analysis |
| CE-LVD-03 | Touch current within limits | IEC 62368-1 Clause 5.2 | Major | Design calculation |

### UL (United States -- optional)

| ID | Requirement | Standard Clause | Severity | Evidence Required |
|----|-------------|----------------|----------|-------------------|
| UL-01 | UL-recognized components (capacitors, transformers) | UL 60950-1 / UL 62368-1 | Critical | BOM review with UL file numbers |
| UL-02 | PCB material flammability (UL 94 V-0 minimum) | UL 94 | Major | PCB material specification |
| UL-03 | Overcurrent protection on all power inputs | UL 62368-1 | Major | Schematic review showing fuses/PTC |
| UL-04 | Fire enclosure material rating | UL 62368-1 | Major | Enclosure material specification |
| UL-05 | UL file preparation checklist | UL process | Minor | Checklist template |

### RoHS (if configured)

| ID | Requirement | Standard Clause | Severity | Evidence Required |
|----|-------------|----------------|----------|-------------------|
| RoHS-01 | All BOM components RoHS compliant | Directive 2011/65/EU | Critical | Per-component RoHS declaration from BOM data |
| RoHS-02 | Solder paste RoHS compliant | Directive 2011/65/EU | Major | Solder paste datasheet |
| RoHS-03 | Surface finish RoHS compliant (lead-free) | Directive 2011/65/EU | Major | PCB fab specification |
| RoHS-04 | Declaration of Conformity prepared | Directive 2011/65/EU, Annex VI | Minor | DoC template |

### REACH (if configured)

| ID | Requirement | Standard Clause | Severity | Evidence Required |
|----|-------------|----------------|----------|-------------------|
| REACH-01 | SVHC screening on BOM | Regulation EC 1907/2006, Article 33 | Major | SVHC screening report |
| REACH-02 | REACH compliance documentation | Regulation EC 1907/2006 | Minor | Documentation template |

### WEEE (if applicable)

| ID | Requirement | Standard Clause | Severity | Evidence Required |
|----|-------------|----------------|----------|-------------------|
| WEEE-01 | WEEE marking requirements identified | Directive 2012/19/EU | Minor | Marking specification |
| WEEE-02 | WEEE registration for target markets | Directive 2012/19/EU | Info | Registration checklist |

---

## Evidence-Linking Protocol

Every compliance requirement must be linked to a specific evidence artifact. The gate evaluates evidence completeness, not the evidence content itself.

### Evidence Record Format

```yaml
- requirement_id: "FCC-01"
  requirement: "Conducted emissions pre-compliance"
  standard_clause: "47 CFR 15.107"
  evidence_artifact: ".hardware/artifacts/06-compliance/emc-report.md"
  evidence_section: "Section 3.1 - Conducted Emissions Analysis"
  status: pass          # pass | fail | pending
  notes: "Pre-compliance EMC analysis via kicad-happy:emc. Risk score: 3/10 (low)"
  reviewed_by: "Compliance Engineer"
  review_date: "2026-04-12"
```

### Status Definitions

| Status | Meaning | Gate Impact |
|--------|---------|-------------|
| `pass` | Evidence exists, reviewed, and requirement satisfied | No impact (good) |
| `fail` | Evidence exists but requirement NOT satisfied | NOT_DONE -- triggers self-correction |
| `pending` | No evidence linked (artifact missing or not yet generated) | NOT_DONE -- missing evidence blocks gate |

### Gate Logic

```
checklist = generate_checklist(config.compliance_regions)

For each requirement R in checklist:
  IF R.status == "pending":
    missing_evidence.append(R)
  ELIF R.status == "fail":
    failed_requirements.append(R)

IF len(missing_evidence) > 0 OR len(failed_requirements) > 0:
  RETURN NOT_DONE with:
    - missing_evidence list (requirements without linked evidence)
    - failed_requirements list (requirements that failed review)
    - remediation guidance per failed requirement
ELSE:
  RETURN DONE with complete compliance package
```

---

## kicad-happy Integration Dispatch

```
Compliance Gate
  |
  +-- kicad-happy:emc
  |     +-- 17 check categories, 42 rule IDs
  |     +-- Produces EMC risk score (0-10 scale)
  |     +-- Findings linked as evidence for FCC-01, FCC-02, CE-EMC-01 through CE-EMC-07
  |     +-- Report saved to .hardware/artifacts/06-compliance/emc-report.md
  |
  +-- kicad-happy:kidoc
        +-- Generates compliance documentation templates
        +-- Technical file structure for CE marking
        +-- Declaration of Conformity templates
        +-- Report saved to .hardware/artifacts/06-compliance/compliance-package.md
```

### EMC Risk Score Mapping

| Risk Score (kicad-happy:emc) | Compliance Gate Interpretation |
|------------------------------|-------------------------------|
| 0-3 (Low) | Pass -- low pre-compliance risk |
| 4-6 (Medium) | Pass with warnings -- recommend pre-compliance testing |
| 7-8 (High) | Fail -- design changes recommended before test lab engagement |
| 9-10 (Critical) | Fail -- significant EMC issues detected, redesign required |

---

## Compliance Package Structure

When the gate passes, it produces a structured compliance package:

```
.hardware/artifacts/06-compliance/
  +-- emc-report.md                  # EMC pre-compliance analysis (from kicad-happy:emc)
  +-- safety-analysis.md             # Safety assessment (creepage, clearance, fusing)
  +-- environmental-checklist.md     # RoHS, REACH, WEEE compliance status
  +-- compliance-package.md          # Master compliance summary with evidence links
  +-- evidence-matrix.md             # Requirement-to-evidence traceability matrix
```

---

## Output Artifacts

- `.hardware/artifacts/06-compliance/emc-report.md` -- EMC pre-compliance analysis
- `.hardware/artifacts/06-compliance/safety-analysis.md` -- Safety assessment
- `.hardware/artifacts/06-compliance/environmental-checklist.md` -- Environmental compliance
- `.hardware/artifacts/06-compliance/compliance-package.md` -- Master compliance package
