# Reference Test Fixture Specification

**Status**: COMPLETE (US-400)
**Version**: 1.0
**Architecture Reference**: Section 12.2 (Test Fixture Coverage)

This document specifies the reference test fixture used to validate all hardware pipeline validation gates. Actual KiCad project files are out of scope for this story -- this is the specification that defines what the fixture must contain, how to create it, and how to update it.

---

## Purpose

The reference test fixture is a KiCad project with intentionally seeded defects across all validation categories. It provides:

1. **Measurable gate benchmarks** -- each gate can be run against known defects with expected outcomes
2. **Offline testability** -- static pricing data eliminates live API dependencies
3. **Regression detection** -- changes to gate logic can be validated against stable fixture data
4. **North Star metric quantification** -- detection rate measured as (defects detected / defects seeded)

---

## Fixture Contents

The test fixture directory (`hardware-team/references/test-fixtures/`) must contain:

| File | Description | Used By |
|------|-------------|---------|
| `reference.kicad_sch` | KiCad schematic with 10 seeded defects across 7 categories | Schematic Review Gate (US-401) |
| `reference.kicad_pcb` | KiCad PCB layout with 4+ DFM/DRC violations | DRC Gate (US-402), DFM Gate (US-404) |
| `reference-bom.csv` | BOM CSV with 4+ issue types | BOM Gate (US-403) |
| `reference-pricing.json` | Static pricing data for offline BOM validation | BOM Gate (US-403) |
| `MANIFEST.md` | Seeded defect manifest with expected outcomes | All gates |

---

## Seeded Defect Categories

### Schematic Defects (7 categories, minimum 10 defects)

Each defect maps to one of the 7 Schematic Review Gate categories. At least one defect per category, with some categories having multiple defects to reach the minimum of 10.

| Defect ID | Category | Description | Location in KiCad | Expected Severity | Expected Detection Gate |
|-----------|----------|-------------|-------------------|-------------------|------------------------|
| SCH-PWR-001 | Power Integrity | Missing bulk capacitance on LDO output (1uF instead of required 4.7uF) | Sheet 1, U3 output | Critical | Schematic Review |
| SCH-PWR-002 | Power Integrity | No inrush current limiting on main power input | Sheet 1, J1 power input | Major | Schematic Review |
| SCH-SIG-001 | Signal Integrity | USB differential pair missing series termination resistors | Sheet 2, USB D+/D- | Major | Schematic Review |
| SCH-DER-001 | Component Derating | Capacitor C7 rated 6.3V on 5V rail (only 80% margin, below 50% ceramic guideline) | Sheet 1, C7 | Major | Schematic Review |
| SCH-PUL-001 | Pull-ups/Pull-downs | I2C bus missing pull-up resistors | Sheet 2, I2C_SCL/I2C_SDA | Critical | Schematic Review |
| SCH-PUL-002 | Pull-ups/Pull-downs | Reset pin floating (no pull-up to VCC) | Sheet 1, U1 NRST | Critical | Schematic Review |
| SCH-DEC-001 | Decoupling | IC U2 missing local 100nF decoupling capacitor on VDD pin | Sheet 1, U2 pin 8 | Critical | Schematic Review |
| SCH-VLT-001 | Voltage Level Compatibility | 5V GPIO connected directly to 3.3V-only input without level shifter | Sheet 2, U4 pin 12 | Critical | Schematic Review |
| SCH-THR-001 | Thermal | Voltage regulator U3 dissipating >1W with no thermal vias or heatsink | Sheet 1, U3 | Major | Schematic Review |
| SCH-THR-002 | Thermal | Hot LDO placed adjacent to temperature-sensitive MEMS sensor | Sheet 1, U3/U6 proximity | Minor | Schematic Review |

### PCB Layout Defects (4+ DRC/DFM violations)

| Defect ID | Category | Description | Location in KiCad | Expected Severity | Expected Detection Gate |
|-----------|----------|-------------|-------------------|-------------------|------------------------|
| PCB-TRC-001 | Trace Width Violation | 0.10mm trace on net VCC_3V3 (JLCPCB min: 0.127mm) | F.Cu, near U3 | Critical | DRC, DFM |
| PCB-VIA-001 | Via Size Violation | 0.25mm drill via (JLCPCB min: 0.30mm) | Via at (45.2, 22.1) | Critical | DRC, DFM |
| PCB-MSK-001 | Solder Mask Violation | Solder mask aperture too small on fine-pitch QFP (0.05mm web) | U2, LQFP-48 | Minor | DFM |
| PCB-CLR-001 | Clearance Violation | 0.08mm copper-to-copper clearance (JLCPCB min: 0.127mm) | F.Cu, VCC_3V3 to GND | Critical | DRC |
| PCB-FID-001 | Missing Fiducials | No fiducial marks for SMT assembly alignment | Board corners | Major | DFM |
| PCB-EDG-001 | Copper-to-Edge | Copper pour 0.15mm from board edge (min: 0.25mm) | Board edge, GND pour | Critical | DFM |

### BOM Defects (4+ issue types)

| Defect ID | Category | Description | Component | MPN | Expected Severity | Expected Detection Gate |
|-----------|----------|-------------|-----------|-----|-------------------|------------------------|
| BOM-OBS-001 | Obsolete Component | IC U4 is marked OBSOLETE by manufacturer | U4 | MC34063ADR | Critical | BOM |
| BOM-BUD-001 | Budget Exceeded | Total BOM cost exceeds budget by 15% due to expensive RF module | U7 | CC2652R1FRGZR | Major | BOM |
| BOM-SRC-001 | Single Source | MCU available from only one manufacturer (ST only) | U1 | STM32F401RET6 | Warning | BOM |
| BOM-NRD-001 | NRND Component | Voltage regulator marked NRND, no longer recommended for new designs | U3 | LM317BDCKG3 | Major | BOM |
| BOM-EOL-001 | EOL Announced | Connector manufacturer announced end of life | J3 | USB3150-30-A | Major | BOM |
| BOM-LED-001 | Long Lead Time | Specialty sensor with 12-week lead time | U6 | BME280 | Major | BOM |

### Compliance Defects (seeded in design, detected by compliance checklist)

| Defect ID | Category | Description | Expected Severity | Expected Detection Gate |
|-----------|----------|-------------|-------------------|------------------------|
| CMP-ESD-001 | Missing ESD Protection | External USB connector has no TVS protection diode | Major | Compliance |
| CMP-CMC-001 | Missing CM Filtering | No common-mode choke on external cable interface | Major | Compliance |
| CMP-GND-001 | Ground Plane Split | Ground plane split under high-speed signal trace | Major | Compliance (EMC) |

---

## Static Pricing Data Format (reference-pricing.json)

The pricing file enables offline BOM validation without live distributor API calls:

```json
{
  "pricing_date": "2026-04-01",
  "currency": "USD",
  "fixture_version": "1.0",
  "bom_budget": 25.00,
  "production_volume": 1000,
  "components": [
    {
      "mpn": "STM32F401RET6",
      "manufacturer": "ST Microelectronics",
      "unit_price_1": 5.50,
      "unit_price_100": 4.20,
      "unit_price_1000": 3.80,
      "stock": 15000,
      "lifecycle": "active",
      "distributor": "DigiKey",
      "lead_time_weeks": 2,
      "second_source": null
    },
    {
      "mpn": "MC34063ADR",
      "manufacturer": "ON Semiconductor",
      "unit_price_1": 0.00,
      "unit_price_100": 0.00,
      "unit_price_1000": 0.00,
      "stock": 0,
      "lifecycle": "obsolete",
      "distributor": "DigiKey",
      "lead_time_weeks": null,
      "second_source": null
    }
  ]
}
```

**Key constraints**:
- Pricing is static (snapshot, not live) so tests are deterministic
- `bom_budget` included in the file so the BOM gate can test budget-exceeded scenarios
- Obsolete components have `stock: 0` and `lifecycle: "obsolete"`
- NRND components have `lifecycle: "nrnd"` with non-zero stock (still available but not recommended)

---

## MANIFEST.md Structure

The manifest is the single source of truth for what defects are seeded and their expected outcomes:

```markdown
# Test Fixture Manifest

## Fixture Version: 1.0
## Created: YYYY-MM-DD
## Last Updated: YYYY-MM-DD

### Defect Registry

| Defect ID | Category | File | Location | Gate | Expected Severity | Expected Result |
|-----------|----------|------|----------|------|-------------------|-----------------|
| SCH-PWR-001 | Power Integrity | reference.kicad_sch | Sheet 1, U3 | Schematic Review | Critical | NOT_DONE |
| ... | ... | ... | ... | ... | ... | ... |

### Expected Gate Results

| Gate | Expected Result | Blocking Defects | Warning Defects |
|------|----------------|------------------|-----------------|
| Schematic Review | NOT_DONE | SCH-PWR-001, SCH-PUL-001, SCH-PUL-002, SCH-DEC-001, SCH-VLT-001 | SCH-SIG-001, SCH-DER-001, SCH-THR-001, SCH-THR-002 |
| DRC | NOT_DONE | PCB-TRC-001, PCB-VIA-001, PCB-CLR-001 | PCB-MSK-001 |
| BOM | NOT_DONE | BOM-OBS-001, BOM-BUD-001, BOM-NRD-001, BOM-EOL-001, BOM-LED-001 | BOM-SRC-001 |
| DFM | NOT_DONE | PCB-TRC-001, PCB-VIA-001, PCB-EDG-001 | PCB-MSK-001, PCB-FID-001 |
| Compliance | NOT_DONE | CMP-ESD-001, CMP-CMC-001, CMP-GND-001 | -- |

### Detection Rate Target

North Star metric: >80% category detection rate per gate
- Schematic Review: 7/7 categories seeded, target >=6 detected
- DRC: 4 violation types seeded, target >=3 detected
- BOM: 4+ issue types seeded, target >=3 detected
- DFM: 4+ violation types seeded, target >=3 detected
- Compliance: 3 issues seeded, target >=2 detected
```

---

## How to Create the Fixture

1. **Create a minimal KiCad project** with a simple mixed-signal design (MCU + LDO + USB + I2C sensor + MEMS sensor)
2. **Seed schematic defects** per the table above -- deliberately introduce each defect and document its exact location
3. **Create PCB layout** from the schematic, then seed layout defects (narrow traces, small vias, tight clearances)
4. **Export BOM** to CSV, then edit to include obsolete/NRND MPNs with realistic part data
5. **Create static pricing JSON** with pricing data that triggers budget-exceeded condition
6. **Write MANIFEST.md** documenting every seeded defect with expected gate outcomes
7. **Validate** by running each gate against the fixture and confirming expected NOT_DONE results

### Design Guidance

The reference design should be:
- **Realistic** -- not a toy circuit. Use real component MPNs and datasheets
- **Minimal** -- only enough complexity to exercise all defect categories (target: 15-20 components)
- **Self-contained** -- no external dependencies beyond standard KiCad libraries
- **Documented** -- every intentional defect clearly commented in the KiCad project

---

## How to Update the Fixture

When adding new gate criteria or validation rules:

1. **Check if existing defects cover the new rule** -- if yes, no fixture change needed
2. **If new defect category**: add a defect to the appropriate KiCad file, update MANIFEST.md
3. **If new pricing scenario**: add a component to reference-pricing.json, update reference-bom.csv
4. **Always update MANIFEST.md** with any new defects (this is the source of truth)
5. **Re-run all gates** against updated fixture to confirm no regressions
6. **Bump fixture version** in MANIFEST.md header

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | TBD | Initial fixture specification (US-400) |
