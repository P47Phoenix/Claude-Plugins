# Safety Standards Reference

This reference provides safety standard requirements for the Compliance Engineer, focusing on IEC 62368-1 (current) and IEC 60950-1 (legacy, withdrawn but still referenced in some markets).

## 1. IEC 62368-1: Audio/Video, IT, and Communication Technology Equipment

IEC 62368-1 replaced both IEC 60950-1 (IT equipment) and IEC 60065 (AV equipment). It uses a hazard-based safety engineering (HBSE) approach rather than prescriptive construction rules.

### 1.1 Energy Source Classification

IEC 62368-1 classifies energy sources by the potential for pain or injury:

| Class | Description | Limits (example for steady-state touch current) |
|-------|-------------|-------|
| Class 1 (ES1) | No pain or injury under normal or abnormal conditions | <= 0.5 mA AC (0.2 mA DC) |
| Class 2 (ES2) | Pain but no injury under normal or abnormal conditions | <= 3.5 mA AC (for duration > 1s) |
| Class 3 (ES3) | Potential for injury | Above Class 2 limits |

### 1.2 Safeguard Types

| Safeguard | Purpose | Example |
|-----------|---------|---------|
| Basic safeguard | Prevents contact with ES2/ES3 under normal conditions | Insulation, enclosure, limited energy circuit |
| Supplementary safeguard | Prevents contact with ES2/ES3 under single-fault conditions | Double/reinforced insulation, protective earthing |
| Reinforced safeguard | Single safeguard providing equivalent protection to basic + supplementary | Reinforced insulation rated for full working voltage |

### 1.3 Key Evaluation Areas

#### Electrical Insulation and Creepage/Clearance

| Parameter | What to Check |
|-----------|---------------|
| Working voltage | Measure/calculate across every insulation barrier |
| Pollution degree | Typically PD2 for enclosed equipment, PD3 for open/ventilated |
| Overvoltage category | OVC II for equipment connected to mains |
| Creepage distance | Per IEC 62368-1 Table 17 (based on working voltage, pollution degree, material group) |
| Clearance distance | Per IEC 62368-1 Table 16 (based on working voltage, overvoltage category) |

**Design rule of thumb for mains-connected equipment (250 Vrms, PD2, Material Group IIIb):**
- Minimum reinforced insulation creepage: 6.4 mm
- Minimum reinforced insulation clearance: 5.0 mm (sea level), derate per altitude table

#### Overcurrent Protection

- Every branch circuit from a Class 3 energy source must have overcurrent protection
- Protection device must be rated for the maximum fault current at that point
- Fuse or PTC must interrupt before conductor temperature exceeds its rating

#### Thermal Requirements

| Component | Temperature Limit |
|-----------|------------------|
| External enclosure surfaces (touchable, metal) | 70 C max (normal operation) |
| External enclosure surfaces (touchable, plastic) | 80 C max (normal operation) |
| Internal wiring insulation | Per insulation material rating |
| PCB (FR-4) | 130 C max (single-fault condition) |

#### Fire Enclosure

- Equipment must have a fire enclosure rated to contain any internal ignition
- Minimum V-1 flammability rating for fire enclosure materials (V-0 preferred)
- Openings in fire enclosure must not allow flame propagation (size limits apply)

### 1.4 Safety Analysis Checklist Template

```markdown
| # | Requirement | Clause | Status | Evidence |
|---|-------------|--------|--------|----------|
| S-01 | Energy source classification complete | 6.2 | PASS/FAIL/NA | <reference> |
| S-02 | All ES3 sources have basic + supplementary safeguards | 6.4 | PASS/FAIL/NA | <reference> |
| S-03 | Creepage distances meet Table 17 | 5.4.3 | PASS/FAIL/NA | <measurement> |
| S-04 | Clearance distances meet Table 16 | 5.4.2 | PASS/FAIL/NA | <measurement> |
| S-05 | Overcurrent protection on all Class 3 branches | 6.5.3 | PASS/FAIL/NA | <schematic ref> |
| S-06 | Touch temperature limits met | 9.2 | PASS/FAIL/NA | <thermal analysis> |
| S-07 | Fire enclosure material rating >= V-1 | 6.6 | PASS/FAIL/NA | <material spec> |
| S-08 | Protective earthing verified (if applicable) | 5.6 | PASS/FAIL/NA | <design ref> |
| S-09 | Marking and documentation complete | Clause 4 | PASS/FAIL/NA | <label review> |
| S-10 | Component safety certifications verified | 5.5 | PASS/FAIL/NA | <component list> |
```

## 2. IEC 60950-1 (Legacy)

IEC 60950-1 was withdrawn in 2020 but some existing products and certain markets still reference it. Key differences from IEC 62368-1:

| Aspect | IEC 60950-1 | IEC 62368-1 |
|--------|-------------|-------------|
| Approach | Prescriptive construction rules | Hazard-based safety engineering |
| Energy classification | SELV/TNV/Hazardous | ES1/ES2/ES3 |
| Insulation | Basic/Supplementary/Reinforced/Double | Basic/Supplementary/Reinforced safeguards |
| Fire enclosure | V-1 minimum | Same (V-1 minimum) |

**Migration note:** When reviewing designs originally certified to IEC 60950-1, map SELV circuits to ES1, TNV circuits to ES2, and hazardous voltage circuits to ES3 as a starting point. A full IEC 62368-1 analysis is still required.

## 3. UL Certification Considerations

### 3.1 UL Listing vs. Recognition vs. Classification

| Type | Scope | Mark |
|------|-------|------|
| UL Listed | Complete end product | UL mark in circle |
| UL Recognized | Component for use in a Listed product | Backward UR mark |
| UL Classified | Product evaluated for specific properties only | UL mark with classification statement |

### 3.2 Component-Level UL Recognition

For safety-critical components, verify UL recognition status:

| Component Type | Why UL Recognition Matters |
|---------------|---------------------------|
| Power transformers | Insulation system, thermal ratings verified |
| Optocouplers (across safety barrier) | Reinforced insulation rating verified |
| Fuses | Breaking capacity and time-current curve verified |
| Connectors (mains-connected) | Current rating, flammability verified |
| Enclosure plastics | Flammability rating (V-0/V-1/HB) verified |

**Design rule:** Use UL-recognized components for all safety-critical functions. Using non-recognized components requires additional testing and may delay certification.

## 4. Pre-Compliance Safety Assessment Output

The CompE safety analysis should identify issues that would block UL/TUV/CSA certification BEFORE engaging the test lab. This saves time and money by fixing design issues in the AI-execution stage rather than discovering them during formal testing.

**Key deliverable:** A safety analysis document with:
1. Energy source classification for every power domain
2. Safeguard inventory (what protects users from each ES2/ES3 source)
3. Creepage/clearance measurements or calculations
4. Component safety certification status (recognized/not recognized)
5. Thermal analysis summary
6. Fire enclosure assessment
7. List of items requiring lab evaluation (cannot be fully assessed by design review alone)
