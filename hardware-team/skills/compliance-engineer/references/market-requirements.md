# Market-Specific Regulatory Requirements Reference

This reference provides market-specific regulatory requirements for the Compliance Engineer, covering FCC (US), CE (EU), and UL (safety) certification paths.

## 1. FCC (United States)

### 1.1 Applicability

- **Authority:** Federal Communications Commission, 47 CFR Part 15
- **Scope:** Any electronic device that can emit RF energy (intentionally or unintentionally)
- **Classification:** Intentional radiators (Part 15 Subpart C/D/E) vs. Unintentional radiators (Part 15 Subpart B)

Most hardware projects in this pipeline are **unintentional radiators** (Subpart B) unless they contain a wireless module.

### 1.2 Device Classification

| Class | Environment | Emission Limits | Typical Products |
|-------|-------------|-----------------|------------------|
| Class A | Commercial/industrial | Less stringent | Server boards, industrial controllers |
| Class B | Residential | More stringent (6-10 dB tighter) | Consumer devices, IoT, home equipment |

**Default assumption:** If the product may be used in a residential environment, design to Class B limits.

### 1.3 Key Test Requirements (Subpart B -- Unintentional Radiators)

| Test | Frequency Range | Standard | Notes |
|------|----------------|----------|-------|
| Radiated emissions | 30 MHz - 1 GHz (above 1 GHz if clock >108 MHz) | ANSI C63.4 | Measured at 3 m or 10 m |
| Conducted emissions | 150 kHz - 30 MHz | ANSI C63.4 | Measured on AC mains power cord |
| AC power line harmonics | N/A (EU only) | N/A | Not required for FCC |
| Voltage flicker | N/A (EU only) | N/A | Not required for FCC |

### 1.4 FCC Authorization Paths

| Path | When | Process |
|------|------|---------|
| Supplier's Declaration of Conformity (SDoC) | Unintentional radiators (most PCBs) | Self-declaration, test report on file, FCC compliance statement |
| Certification | Intentional radiators, restricted devices | Test by accredited lab, file with FCC via TCB |

### 1.5 FCC Pre-Compliance Checklist

```markdown
| # | Requirement | Evidence | Status |
|---|-------------|----------|--------|
| F-01 | Device classification determined (Class A/B) | Product use case analysis | |
| F-02 | Authorization path identified (SDoC/Certification) | Radiator type assessment | |
| F-03 | EMC pre-compliance analysis complete | kicad-happy:emc report | |
| F-04 | Radiated emission risk assessed | EMC report, Section: board edge radiation, clock routing | |
| F-05 | Conducted emission risk assessed | EMC report, Section: I/O filtering, PDN | |
| F-06 | FCC compliance statement text prepared | Per 47 CFR 15.19 | |
| F-07 | FCC label requirements defined | Per 47 CFR 15.19 (electronic labeling if applicable) | |
| F-08 | Test lab selected (if formal testing needed) | Accredited lab (A2LA or NVLAP) | |
```

### 1.6 FCC Compliance Statement Text

For Class B devices (SDoC):
> This device complies with Part 15 of the FCC Rules. Operation is subject to the following two conditions: (1) this device may not cause harmful interference, and (2) this device must accept any interference received, including interference that may cause undesired operation.

## 2. CE Marking (European Union)

### 2.1 Applicable Directives

| Directive | Number | Applies When |
|-----------|--------|-------------|
| EMC Directive | 2014/30/EU | All electrical/electronic equipment |
| Low Voltage Directive (LVD) | 2014/35/EU | Equipment with rated voltage 50-1000 VAC or 75-1500 VDC |
| Radio Equipment Directive (RED) | 2014/53/EU | Equipment with intentional radio transmitter/receiver |
| RoHS Directive | 2011/65/EU | All EEE (see environmental.md) |

**Typical hardware project:** EMC Directive + LVD (if mains-connected) + RoHS. Add RED only if the product contains a wireless module.

### 2.2 Harmonized Standards

| Standard | Directive | Purpose |
|----------|-----------|---------|
| EN 55032 | EMC | Emissions limits for multimedia equipment |
| EN 55035 | EMC | Immunity requirements for multimedia equipment |
| EN 61000-3-2 | EMC | Harmonic current emissions (mains-connected equipment) |
| EN 61000-3-3 | EMC | Voltage flicker (mains-connected equipment) |
| EN 62368-1 | LVD | Safety (see safety-standards.md) |
| EN 301 489-x | RED | EMC for radio equipment (standard varies by radio type) |
| EN 300 xxx | RED | Radio performance (standard varies by radio type) |

### 2.3 CE Conformity Assessment

| Step | Description |
|------|-------------|
| 1. Identify directives | Determine which directives apply to the product |
| 2. Identify standards | Select harmonized standards for each directive |
| 3. Assess conformity | Test/analyze against each standard |
| 4. Compile Technical File | All evidence of conformity in one package |
| 5. Draft DoC | Declaration of Conformity signed by EU-based responsible person |
| 6. Affix CE mark | Mark product and/or packaging |

### 2.4 CE Pre-Compliance Checklist

```markdown
| # | Requirement | Evidence | Status |
|---|-------------|----------|--------|
| CE-01 | Applicable directives identified | Directive applicability analysis | |
| CE-02 | Harmonized standards selected | Standard selection rationale | |
| CE-03 | EMC emissions pre-compliance complete | kicad-happy:emc report mapped to EN 55032 | |
| CE-04 | EMC immunity risk assessed | Design review against EN 55035 categories | |
| CE-05 | Harmonic current assessment (if mains) | Power supply topology analysis | |
| CE-06 | Safety assessment complete (if LVD applies) | Safety analysis per EN 62368-1 | |
| CE-07 | RoHS compliance verified | Environmental checklist | |
| CE-08 | Technical File structure defined | Document index | |
| CE-09 | DoC template prepared | Draft DoC with correct legal text | |
| CE-10 | EU responsible person identified | Business action (not design) | |
```

### 2.5 Declaration of Conformity Template

```markdown
## EU DECLARATION OF CONFORMITY

**Manufacturer:** <company name and address>
**Product:** <product name>
**Model:** <model number>

This declaration of conformity is issued under the sole responsibility of the manufacturer.

**Object of the declaration:** <product description>

The object of the declaration described above is in conformity with the relevant Union harmonization legislation:
- EMC Directive 2014/30/EU
- [Low Voltage Directive 2014/35/EU]
- [RoHS Directive 2011/65/EU]

Reference to the relevant harmonized standards used:
- EN 55032:<year>
- EN 55035:<year>
- [EN 62368-1:<year>]

Signed for and on behalf of: <name, function, signature, date>
```

## 3. UL Certification (Safety -- North America)

### 3.1 Overview

UL certification is voluntary in the US (unlike CE in the EU) but is often required by:
- Major retailers (Amazon, Best Buy, etc.)
- Commercial building codes (NEC/NFPA)
- Insurance requirements
- Customer procurement policies

### 3.2 Applicable UL Standards

| Standard | Scope |
|----------|-------|
| UL 62368-1 | Audio/Video, IT, and Communication Technology Equipment |
| UL 60950-1 | IT equipment (legacy, transitioning to 62368-1) |
| UL 61010-1 | Measurement, control, and laboratory equipment |
| UL 508A | Industrial control panels |

### 3.3 UL Pre-Certification Checklist

```markdown
| # | Requirement | Evidence | Status |
|---|-------------|----------|--------|
| UL-01 | Applicable UL standard identified | Product classification | |
| UL-02 | Safety-critical components are UL-recognized | Component UL file numbers | |
| UL-03 | Creepage/clearance meet UL standard | PCB layout measurements | |
| UL-04 | Overcurrent protection adequate | Schematic analysis | |
| UL-05 | Thermal design within limits | Thermal analysis/simulation | |
| UL-06 | Fire enclosure requirements met | Material flammability ratings | |
| UL-07 | Product marking requirements defined | UL marking guide review | |
| UL-08 | Test lab selected | UL CTDP or partner lab | |
```

## 4. Multi-Region Compliance Matrix

When a product targets multiple markets, use this matrix to track requirements across regions:

```markdown
## Multi-Region Compliance Matrix
**Project:** <project_name>

| Requirement Category | FCC (US) | CE (EU) | UL (Safety) | Notes |
|---------------------|----------|---------|-------------|-------|
| EMC emissions | Part 15 Sub B | EN 55032 | N/A | Test to tighter limit (usually CE) |
| EMC immunity | N/A (not required) | EN 55035 | N/A | EU-only requirement |
| Harmonic currents | N/A | EN 61000-3-2 | N/A | Mains-connected only |
| Safety | Voluntary (UL) | EN 62368-1 (via LVD) | UL 62368-1 | Same base standard |
| RoHS | N/A (no federal req) | 2011/65/EU | N/A | EU requirement, often adopted voluntarily |
| REACH | N/A | (EC) 1907/2006 | N/A | EU requirement |
| Labeling | FCC ID / compliance statement | CE mark + DoC | UL mark | All may be on same label |
```

**Design strategy:** When targeting multiple regions, design to the most stringent requirement in each category. This avoids redesign when adding a new market.
