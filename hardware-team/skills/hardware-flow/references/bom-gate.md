# BOM Gate Reference

**Status**: COMPLETE (US-403)
**Version**: 1.0
**Architecture Reference**: Section 3.1 (Gate Index), quality-gates.md Section 5b
**Parent Gate Definition**: `quality-gates.md` Section 5b (BOM Gate)

This file is the authoritative reference for BOM Gate validation logic, integration dispatch, and remediation workflows. It supplements the gate criteria defined in `quality-gates.md`.

---

## Overview

The BOM Gate validates that the Bill of Materials is producible, affordable, and supply-chain resilient before prototype ordering. It runs at Stage 5 alongside the DFM Gate.

**Gate type**: Automated
**Primary role**: Manufacturing Engineer
**Consumes**: `kicad-happy:bom`, `kicad-happy:digikey`, `kicad-happy:mouser`, `kicad-happy:lcsc`, `kicad-happy:element14`

---

## Validation Workflow

```
BOM Gate activates
  |
  +-- 1. Load BOM from kicad-happy:bom (parsed from KiCad schematic)
  |     +-- Extract all components with MPN, quantity, value, footprint
  |     +-- Cross-reference against schematic netlist (no orphan components)
  |
  +-- 2. Cost Validation
  |     +-- Load bom_budget from .hardware/config.yml
  |     +-- Query pricing via kicad-happy sourcing skills (or reference-pricing.json for offline)
  |     +-- Calculate per-unit BOM cost at target volume
  |     +-- Compare against budget threshold
  |     +-- If budget exceeded --> NOT_DONE (Major)
  |
  +-- 3. Component Availability Check
  |     +-- Query stock levels at configured distributors
  |     +-- Flag components with zero stock at all distributors --> Critical
  |     +-- Flag components with lead time > 4 weeks --> Major
  |     +-- Flag components available at only 1 distributor --> Minor
  |
  +-- 4. Lifecycle Status Check
  |     +-- Query lifecycle status per component
  |     +-- OBSOLETE --> Critical (blocks gate)
  |     +-- NRND --> Major (blocks gate, requires substitution or risk acceptance)
  |     +-- EOL announced --> Major (requires transition plan)
  |     +-- Active with <5yr expected life --> Minor
  |
  +-- 5. Second-Source Validation
  |     +-- For each component, search for pin/function-compatible alternatives
  |     +-- Single-source + config `second_source_required: true` --> Blocking
  |     +-- Single-source + config `second_source_required: false` --> Warning
  |     +-- Critical-path components (MCU, power, RF) always flagged if single-source --> Major
  |
  +-- 6. Gate Evaluation
        +-- All checks pass --> DONE
        +-- Any Critical/Major finding --> NOT_DONE (triggers self-correction)
```

---

## Cost Validation Logic

### Budget Source

The BOM budget is sourced from `.hardware/config.yml`:

```yaml
bom_budget: 25.00          # USD per unit (null = unconstrained)
production_volume: 1000     # Target volume for pricing tier
currency: USD               # ISO 4217 currency code
```

### Cost Calculation

```
For each component C in BOM:
  unit_price = best_price(C, production_volume)    # Lowest across configured distributors
  extended_price = unit_price * C.quantity
  total_bom_cost += extended_price

IF bom_budget IS NOT NULL AND total_bom_cost > bom_budget:
  RETURN finding(severity=Major, issue="budget-exceeded",
    detail="BOM cost ${total_bom_cost} exceeds budget ${bom_budget} by ${variance}")
```

### Cost Breakdown Report

The gate produces a cost breakdown by category:

| Category | Example Components | Target % |
|----------|-------------------|----------|
| ICs (MCU, regulators, interfaces) | STM32, LDO, USB PHY | 40-60% |
| Passives (R, C, L, ferrites) | 0402 resistors, MLCC caps | 10-20% |
| Connectors | USB-C, headers, JST | 10-20% |
| Mechanicals (standoffs, enclosure) | Screws, spacers | 5-15% |
| PCB fabrication | Board cost per unit | 10-25% |

### Offline Testing Support

For offline validation (test fixture, CI, environments without API access):

1. BOM Gate checks for `reference-pricing.json` in test fixture directory
2. If present AND no live API configured, pricing data is loaded from the static file
3. Static pricing format:

```json
{
  "pricing_date": "2026-04-01",
  "currency": "USD",
  "components": [
    {
      "mpn": "STM32F401RET6",
      "unit_price_1": 5.50,
      "unit_price_100": 4.20,
      "unit_price_1000": 3.80,
      "stock": 15000,
      "lifecycle": "active",
      "distributor": "DigiKey",
      "lead_time_weeks": 2
    }
  ]
}
```

---

## Component Availability Rules

| Condition | Severity | Action |
|-----------|----------|--------|
| Zero stock at ALL distributors | Critical | Gate blocks. Remediation: find alternate MPN or distributor |
| Stock < prototype quantity needed | Major | Gate blocks. Remediation: split order across distributors or find alternate |
| Lead time > 4 weeks | Major | Gate blocks unless waiver granted. Remediation: pre-order or find faster source |
| Stock < production volume quantity | Minor | Logged. Remediation: confirm allocation or find additional source |
| Available at only 1 distributor | Minor | Logged. Supply chain resilience warning |

---

## Lifecycle Status Rules

| Status | Severity | Gate Behavior | Required Action |
|--------|----------|---------------|-----------------|
| `ACTIVE` | None | Pass | None |
| `NRND` (Not Recommended for New Design) | Major | Blocks gate | Document alternative component AND either substitute or provide explicit risk acceptance with justification |
| `EOL` (End of Life announced) | Major | Blocks gate | Document transition plan with timeline and replacement component |
| `OBSOLETE` | Critical | Blocks gate | Mandatory substitution. No waiver permitted for new designs |
| `UNKNOWN` | Minor | Pass with warning | Confirm lifecycle status with manufacturer |

### Lifecycle Evidence Format

```yaml
- component: "U5"
  mpn: "STM32F401RET6"
  lifecycle_status: active
  lifecycle_source: "DigiKey product page, retrieved 2026-04-12"
  expected_longevity: ">10 years (ST long-life program)"
```

---

## Second-Source Validation Rules

### Config-Driven Behavior

```yaml
# .hardware/config.yml
second_source_required: false    # true = single-source blocks gate; false = warning only
```

### Evaluation Matrix

| Component Type | Single-Source (required=true) | Single-Source (required=false) |
|----------------|------------------------------|-------------------------------|
| MCU / SoC | Critical (blocks) | Major (blocks) |
| Power regulators | Critical (blocks) | Major (blocks) |
| RF / wireless | Critical (blocks) | Warning (logged) |
| Sensors | Major (blocks) | Warning (logged) |
| Passives (standard series) | Warning (logged) | Info (logged) |
| Connectors (standard) | Warning (logged) | Info (logged) |
| Custom / ASIC | Critical (blocks) | Major (blocks) |

### Second-Source Documentation Format

```yaml
- component: "U5"
  mpn: "STM32F401RET6"
  manufacturer: "ST Microelectronics"
  second_sources:
    - mpn: "STM32F411RET6"
      manufacturer: "ST Microelectronics"
      compatibility: "pin-compatible, superset features"
      notes: "Same manufacturer -- does not mitigate fab disruption risk"
    - mpn: "GD32F401RET6"
      manufacturer: "GigaDevice"
      compatibility: "pin-compatible, register-level differences in USB peripheral"
      notes: "True second source from different manufacturer"
```

---

## kicad-happy Integration Dispatch

The BOM Gate orchestrates multiple kicad-happy skills:

```
BOM Gate
  |
  +-- kicad-happy:bom          --> Parse BOM from KiCad project, generate unified BOM
  +-- kicad-happy:digikey      --> Query DigiKey for pricing, stock, lifecycle
  +-- kicad-happy:mouser       --> Query Mouser for pricing, stock, lifecycle
  +-- kicad-happy:lcsc         --> Query LCSC for pricing, stock, lifecycle (JLCPCB parts)
  +-- kicad-happy:element14    --> Query Newark/Farnell for pricing, stock, lifecycle
```

### Dispatch Priority

1. If `target_fab: jlcpcb` --> prioritize `kicad-happy:lcsc` (same parts library)
2. Always query at least 2 distributors for price comparison
3. Use `kicad-happy:bom` as the aggregation layer (it coordinates distributor queries)

---

## Finding Format

```yaml
- component: "U5"
  mpn: "STM32F401RET6"
  issue: "single-source"
  severity: warning
  category: "second-source"
  detail: "Only available from ST Microelectronics. No pin-compatible second source identified."
  recommendation: "Consider GD32F401RET6 (GigaDevice, pin-compatible) or redesign for multi-source MCU family"
  distributor_data:
    digikey: { stock: 15000, unit_price: 5.50, lead_time_weeks: 2 }
    mouser: { stock: 8200, unit_price: 5.45, lead_time_weeks: 2 }
    lcsc: { stock: 0, unit_price: null, lead_time_weeks: null }
```

---

## Output Artifacts

- `.hardware/artifacts/05-dfm-dfa/bom-validation.md` -- Full BOM validation report with all findings
