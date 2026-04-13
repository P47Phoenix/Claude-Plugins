# DFM Gate Reference

**Status**: COMPLETE (US-404)
**Version**: 1.0
**Architecture Reference**: Section 3.1 (Gate Index), quality-gates.md Section 5a
**Parent Gate Definition**: `quality-gates.md` Section 5a (DFM Gate)

This file is the authoritative reference for DFM Gate validation logic, fab-specific rule sets, and manufacturability review workflows. It supplements the gate criteria defined in `quality-gates.md`.

---

## Overview

The DFM (Design for Manufacturability) Gate validates that the PCB design is producible at the target fabrication house within standard capabilities. It runs at Stage 5 alongside the BOM Gate.

**Gate type**: Automated
**Primary role**: Manufacturing Engineer
**Consumes**: `kicad-happy:jlcpcb` or `kicad-happy:pcbway` (per `target_fab` config)

---

## Validation Workflow

```
DFM Gate activates
  |
  +-- 1. Load target fab from .hardware/config.yml (`target_fab` key)
  |     +-- jlcpcb --> dispatch kicad-happy:jlcpcb
  |     +-- pcbway --> dispatch kicad-happy:pcbway
  |     +-- custom --> load .hardware/fab-rules/<name>.yml
  |
  +-- 2. Extract design parameters from KiCad PCB
  |     +-- Trace widths (per layer, per net class)
  |     +-- Trace spacing (per layer, per net class)
  |     +-- Via drill sizes and annular rings
  |     +-- Board layer count and stackup
  |     +-- Surface finish requirements
  |     +-- Solder mask apertures
  |     +-- Copper-to-edge clearances
  |     +-- Component footprints
  |
  +-- 3. Compare against fab capability rules
  |     +-- Each parameter checked against fab minimum/maximum
  |     +-- Violations classified by severity per quality-gates.md
  |
  +-- 4. Evaluate DFM-specific checks
  |     +-- Fiducial marks present and correctly placed
  |     +-- Panelization compatibility
  |     +-- Solder paste aperture optimization
  |     +-- Component footprint availability in fab library
  |
  +-- 5. Gate Evaluation
        +-- Zero violations --> DONE
        +-- Any violation --> NOT_DONE with remediation plan
```

---

## Fab Capability Rule Sets

### JLCPCB Standard Process

| Parameter | Minimum | Maximum | Severity if Violated |
|-----------|---------|---------|---------------------|
| Trace width | 0.127mm (5mil) | -- | Critical |
| Trace spacing | 0.127mm (5mil) | -- | Critical |
| Via drill diameter | 0.3mm (12mil) | 6.3mm | Critical |
| Via annular ring | 0.13mm | -- | Major |
| Via aspect ratio | -- | 8:1 | Major |
| Board thickness | 0.4mm | 2.4mm | Major |
| Board layers | 1 | 20 | Major |
| Copper weight (outer) | 1oz | 2oz | Minor |
| Copper weight (inner) | 0.5oz | 1oz | Minor |
| Min drill-to-copper | 0.2mm | -- | Major |
| Min copper-to-edge | 0.25mm | -- | Critical |
| Silkscreen line width | 0.15mm | -- | Minor |
| Solder mask web | 0.1mm | -- | Minor |
| Solder mask dam | 0.1mm | -- | Minor |
| Min BGA pad pitch | 0.4mm | -- | Major |

### JLCPCB Advanced Process

| Parameter | Minimum | Maximum | Notes |
|-----------|---------|---------|-------|
| Trace width | 0.09mm (3.5mil) | -- | Requires advanced process selection |
| Trace spacing | 0.09mm (3.5mil) | -- | Additional cost |
| Via drill diameter | 0.15mm (micro via) | -- | Laser drilled, blind/buried supported |
| Via annular ring | 0.1mm | -- | |
| Via aspect ratio | -- | 10:1 | |

### PCBWay Standard Process

| Parameter | Minimum | Maximum | Severity if Violated |
|-----------|---------|---------|---------------------|
| Trace width | 0.1mm (4mil) | -- | Critical |
| Trace spacing | 0.1mm (4mil) | -- | Critical |
| Via drill diameter | 0.2mm (8mil) | 6.5mm | Critical |
| Via annular ring | 0.15mm | -- | Major |
| Via aspect ratio | -- | 8:1 | Major |
| Board thickness | 0.2mm | 6.0mm | Major |
| Board layers | 1 | 14 | Major |
| Copper weight (outer) | 1oz | 13oz | Minor |
| Min copper-to-edge | 0.25mm | -- | Critical |
| Silkscreen line width | 0.15mm | -- | Minor |
| Solder mask web | 0.1mm | -- | Minor |
| Min BGA pad pitch | 0.35mm | -- | Major |

### PCBWay Advanced Process

| Parameter | Minimum | Maximum | Notes |
|-----------|---------|---------|-------|
| Trace width | 0.075mm (3mil) | -- | HDI process |
| Trace spacing | 0.075mm (3mil) | -- | HDI process |
| Via drill diameter | 0.15mm | -- | Laser micro via |
| Board layers | 1 | 32 | HDI multilayer |

---

## Trace and Space Validation

### Evaluation Logic

```
For each net_class NC in PCB design:
  For each trace T in NC:
    IF T.width < fab.min_trace_width:
      RETURN finding(severity=Critical,
        parameter="trace_width",
        min_value=fab.min_trace_width,
        board_value=T.width,
        location=T.layer + ", net " + T.net,
        remediation="Widen trace from {T.width} to {fab.min_trace_width} minimum")

    IF T.clearance_to_nearest < fab.min_trace_spacing:
      RETURN finding(severity=Critical,
        parameter="trace_spacing",
        min_value=fab.min_trace_spacing,
        board_value=T.clearance_to_nearest,
        location=T.layer + " between " + T.net + " and " + T.adjacent_net,
        remediation="Increase spacing from {T.clearance} to {fab.min_trace_spacing}")
```

### Controlled Impedance Traces

When impedance-controlled net classes are defined:

- [ ] **Major**: Trace width matches stackup calculator output for target impedance
- [ ] **Major**: Dielectric thickness consistent with fab stackup offering
- [ ] **Minor**: Impedance tolerance within +/-10% of target (standard fab capability)

---

## Via Size Validation

### Evaluation Logic

```
For each via V in PCB:
  IF V.drill < fab.min_drill:
    RETURN finding(severity=Critical, parameter="via_drill",
      min_value=fab.min_drill, board_value=V.drill)

  IF V.annular_ring < fab.min_annular_ring:
    RETURN finding(severity=Major, parameter="annular_ring",
      min_value=fab.min_annular_ring, board_value=V.annular_ring)

  aspect_ratio = board_thickness / V.drill
  IF aspect_ratio > fab.max_aspect_ratio:
    RETURN finding(severity=Major, parameter="via_aspect_ratio",
      max_value=fab.max_aspect_ratio, board_value=aspect_ratio,
      remediation="Increase drill size or reduce board thickness")
```

---

## Layer Count and Stackup

| Check | Severity | Condition |
|-------|----------|-----------|
| Layer count within fab range | Major | `board.layers <= fab.max_layers` |
| Stackup symmetry | Major | Layer stackup is symmetric about center (prevents warping) |
| Layer count optimization | Minor | Could reduce layers without routing congestion |

---

## Surface Finish Compatibility

| Finish | Compatible With | Incompatible With | Cost Tier |
|--------|----------------|-------------------|-----------|
| HASL (leaded) | Through-hole heavy, non-RoHS | Fine pitch (<0.5mm), BGA | Low |
| HASL (lead-free) | Through-hole heavy, RoHS | Fine pitch (<0.5mm), BGA | Low |
| ENIG | Fine pitch, BGA, gold fingers | -- | Medium |
| OSP | Standard SMT, cost-sensitive | Long shelf life, multiple reflow | Low |
| Immersion Tin | Standard SMT, press-fit | Long shelf life (whisker risk) | Low |
| Immersion Silver | High-frequency, flat surface | Long-term storage (tarnish) | Medium |
| Hard Gold | Edge connectors, high-wear contacts | Large areas (cost) | High |

### Validation Rule

```
IF board.has_bga AND surface_finish IN [HASL_leaded, HASL_lead_free]:
  RETURN finding(severity=Major,
    description="BGA components require flat surface finish (ENIG recommended)",
    remediation="Change surface finish from HASL to ENIG")

IF board.rohs_required AND surface_finish == HASL_leaded:
  RETURN finding(severity=Major,
    description="RoHS compliance requires lead-free surface finish",
    remediation="Change to HASL lead-free, ENIG, or OSP")
```

---

## General DFM Checks

### Fiducial Marks

- [ ] **Major**: Minimum 3 fiducial marks per board (2 for panel)
- [ ] **Major**: Fiducials placed on diagonal corners for rotation detection
- [ ] **Minor**: Fiducial diameter 1.0mm with 2.0mm clearance ring (IPC-7351 standard)

### Panelization

- [ ] **Minor**: Board outline rectangular or with clean break-away tabs
- [ ] **Minor**: V-score compatible edges (straight lines only)
- [ ] **Minor**: Tab-route breakaway tabs with mouse bites where V-score not possible
- [ ] **Minor**: Tooling holes for panel registration (2.4mm diameter, 3 per panel)

### Solder Paste Apertures

- [ ] **Major**: Aperture size matches IPC-7525 guidelines for component pitch
- [ ] **Major**: Fine-pitch components (<0.5mm pitch) use reduced apertures (80% of pad)
- [ ] **Minor**: Area ratio > 0.66 for all apertures (paste release reliability)

### Component Footprint Availability

- [ ] **Major**: All footprints available in target fab's component library (if using assembly service)
- [ ] **Minor**: Custom footprints flagged for manual verification

---

## kicad-happy Integration Dispatch

```
DFM Gate
  |
  +-- IF target_fab == "jlcpcb":
  |     +-- kicad-happy:jlcpcb --> JLCPCB-specific DFM rules, part availability, assembly constraints
  |
  +-- IF target_fab == "pcbway":
  |     +-- kicad-happy:pcbway --> PCBWay-specific DFM rules, turnkey assembly rules
  |
  +-- ALWAYS:
        +-- kicad-happy:kicad --> PCB design parameter extraction, DRC baseline
```

---

## Finding Format

```yaml
- rule_id: "DFM-TRC-001"
  parameter: "trace_width"
  min_value: "0.127mm"
  board_value: "0.10mm"
  pass: false
  severity: critical
  location: "Layer F.Cu, net VCC_3V3, near U3"
  remediation: "Widen trace from 0.10mm to 0.127mm minimum, or select advanced process capability (+$cost)"
```

---

## Output Artifacts

- `.hardware/artifacts/05-dfm-dfa/dfm-report.md` -- Full DFM validation report
- `.hardware/artifacts/05-dfm-dfa/dfa-report.md` -- Design for Assembly report
- `.hardware/artifacts/05-dfm-dfa/yield-assessment.md` -- Yield risk assessment
