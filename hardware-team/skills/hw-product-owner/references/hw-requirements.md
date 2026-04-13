# Hardware Requirements Capture Patterns

This reference provides structured patterns for capturing hardware product requirements, building constraint matrices, and performing regulatory landscape scans.

## 1. Requirements Capture Framework

### 1.1 Requirement Categories

Hardware requirements span six categories. Every product must address each category, even if the answer is "not applicable" with justification.

| Category | Covers | Examples |
|----------|--------|----------|
| Functional | What the product does | Signal processing, data acquisition, power conversion, user interaction |
| Electrical | Electrical performance | Input voltage range, current draw, signal integrity, EMI emissions |
| Mechanical | Physical form factor | Dimensions, weight, mounting, connectors, enclosure |
| Environmental | Operating conditions | Temperature range, humidity, vibration, altitude, IP rating |
| Reliability | Lifetime and failure | MTBF target, derating strategy, storage conditions, warranty period |
| Regulatory | Compliance obligations | FCC, CE, UL, RoHS, REACH, WEEE, country-specific certifications |

### 1.2 Writing Good Hardware Requirements

Every requirement must follow these rules:

1. **Measurable** -- Include a numeric target or pass/fail criterion. "Low power" is not a requirement; "Standby power < 50mW" is.
2. **Testable** -- Specify how the requirement will be verified (analysis, simulation, test, or inspection).
3. **Unambiguous** -- One interpretation only. Avoid "adequate," "sufficient," "fast," "reliable" without quantification.
4. **Traceable** -- Every requirement has a unique ID and traces to a source (market need, standard, constraint).
5. **Prioritized** -- P1 (Must Have), P2 (Should Have), P3 (Could Have). No requirement should lack a priority.

### 1.3 Verification Methods

| Method | When to Use | Cost | Confidence |
|--------|------------|------|-----------|
| **Analysis** | Mathematical proof or calculation | Low | Medium -- depends on model accuracy |
| **Simulation** | SPICE, thermal, mechanical FEA | Medium | Medium-High -- depends on model fidelity |
| **Test** | Physical measurement on prototype or production unit | High | High -- real-world validation |
| **Inspection** | Visual or dimensional check | Low | High for physical attributes |

**Rule of thumb:** Every P1 requirement should be verified by Test. P2/P3 requirements may use Analysis or Simulation if test cost is prohibitive, with risk documented.

## 2. Constraint Matrix Template

The constraint matrix captures hard limits and soft targets for the product. Hard limits are non-negotiable; soft targets are optimization goals.

```markdown
| Constraint | Target (soft) | Hard Limit | Source | Notes |
|-----------|--------------|-----------|--------|-------|
| Unit BOM cost | $X.XX | $Y.YY | Business case | At target production volume |
| NRE budget | $X,XXX | $Y,YYY | Project budget | Tooling, test fixtures, certs |
| Schedule to prototype | X weeks | Y weeks | Market window | From concept approval |
| Schedule to production | X months | Y months | Market window | From concept approval |
| Input voltage | 5V nominal | 4.5-5.5V | USB spec | If USB-powered |
| Power consumption (active) | <X mW | <Y mW | Battery life target | At typical load |
| Power consumption (standby) | <X mW | <Y mW | Battery life target | Sleep/idle mode |
| PCB size | X x Y mm | A x B mm | Enclosure constraint | Including keep-outs |
| Weight | <X g | <Y g | Application constraint | Including enclosure |
| Operating temperature | 0C to 50C | -10C to 60C | Deployment environment | Ambient, not junction |
| Storage temperature | -20C to 70C | -40C to 85C | Shipping/warehousing | Non-operating |
| Humidity | 20-80% RH | 10-90% RH non-condensing | Deployment environment | |
| Vibration | -- | Per IEC 60068-2-6 | Application-dependent | If applicable |
```

### Constraint Prioritization

When constraints conflict (and they will), use this priority order unless the project explicitly overrides:

1. **Safety** -- Non-negotiable. Never trade safety for cost or schedule.
2. **Regulatory compliance** -- Required for market access. Cannot ship without it.
3. **Hard functional requirements** -- Core product value proposition.
4. **Cost** -- BOM budget determines business viability.
5. **Schedule** -- Market window and commitment dates.
6. **Performance beyond minimum** -- Nice-to-have optimization.

## 3. Regulatory Landscape Checklist

### 3.1 By Target Market

| Market | Mandatory Standards | Agency | Notes |
|--------|-------------------|--------|-------|
| **United States** | FCC Part 15 (EMC), UL/ETL (safety) | FCC, OSHA/NRTL | Class A (industrial) or Class B (residential). Intentional radiators need FCC Part 15 Subpart C/E. |
| **European Union** | CE marking: EMC Directive (2014/30/EU), LVD (2014/35/EU), RED (2014/53/EU if radio), RoHS (2011/65/EU), REACH, WEEE | EU notified bodies | Self-declaration for most products. RED requires notified body if no harmonized standard. |
| **United Kingdom** | UKCA marking (mirrors CE) | UK approved bodies | Post-Brexit requirement. Transitional acceptance of CE marking has deadlines. |
| **Canada** | ISED (formerly IC) | ISED | Often tested alongside FCC. |
| **China** | CCC (mandatory for listed products), SRRC (radio) | CNCA, MIIT | CCC scope is specific product categories. Many electronics exempt if not in CCC catalog. |
| **Japan** | PSE (safety), VCCI (EMC, voluntary but expected) | METI, VCCI | VCCI is voluntary but major retailers require it. |
| **South Korea** | KC mark | KCC, KATS | |
| **Australia/NZ** | RCM (EMC + safety) | ACMA, EESS | |

### 3.2 By Product Type

| Product Type | Key Standards | Notes |
|-------------|--------------|-------|
| Consumer electronics (no radio) | FCC Part 15B, CE EMC+LVD, UL 62368-1 | Most common baseline |
| WiFi/BT product | FCC Part 15C, CE RED, IC RSS-247 | Radio certification required in every market |
| Battery-powered (Li-ion) | UN 38.3, IEC 62133, UL 2054 | Shipping regulations (IATA DGR) also apply |
| Medical adjacent | IEC 60601-1 (if medical), IEC 62368-1 (if not) | Classification determines regulatory burden |
| Industrial | IEC 61010-1, FCC Part 15 Class A | Less stringent EMC (Class A vs. Class B) |
| Automotive | ISO 11452, ISO 7637, AEC-Q grades | Entirely different regulatory framework |

### 3.3 Environmental Compliance

| Regulation | Scope | Key Requirements |
|-----------|-------|-----------------|
| **RoHS** (EU 2011/65/EU) | Restricted substances in electronics | Lead, mercury, cadmium, hex-chromium, PBB, PBDE below thresholds |
| **REACH** (EU 1907/2006) | Chemical substances | SVHC (Substances of Very High Concern) declaration. Updated regularly. |
| **WEEE** (EU 2012/19/EU) | End-of-life electronics | Producer responsibility for recycling. Registration and labeling required. |
| **Prop 65** (California) | Chemicals known to cause cancer/reproductive harm | Warning label requirement if product contains listed chemicals. |
| **Conflict minerals** | Tin, tantalum, tungsten, gold (3TG) | SEC reporting for public companies. Due diligence for supply chain. |

## 4. BOM Budget Framework

### 4.1 Budget Categories

| Category | Typical Allocation | Notes |
|----------|-------------------|-------|
| Active components (MCU, ICs, regulators) | 30-45% | Highest cost items. Drive architecture decisions. |
| Passive components (R, C, L, ferrites) | 5-15% | Low per-unit cost but high part count. |
| Connectors and mechanical | 10-20% | USB, headers, mounting hardware, standoffs |
| PCB fabrication | 10-20% | Layer count and special features (impedance control, blind vias) drive cost |
| Assembly (SMT + through-hole) | 5-15% | Setup cost amortized over volume. Extended parts cost more. |
| Margin / contingency | 15-20% | For unforeseen component cost increases, design changes, BOM growth |

### 4.2 Volume-Dependent Pricing

BOM cost is NOT a single number. Always specify at which volume:

| Volume Tier | Typical Price Point | Use For |
|------------|-------------------|---------|
| 1-10 units | Prototype pricing (highest) | EVT (Engineering Validation Test) builds |
| 10-100 units | Small batch | DVT (Design Validation Test) / pilot runs |
| 100-1,000 units | Production pricing | Initial production |
| 1,000-10,000 units | Volume pricing | Standard production |
| 10,000+ units | High-volume pricing | Mass production. Negotiate with suppliers. |

### 4.3 Cost Tracking Rules

1. **Initial budget** is set during Concept stage based on market analysis and competitive products
2. **Budget is updated** at each stage gate when new cost information becomes available
3. **Overruns > 10%** of category allocation require a trade-off decision record
4. **Total BOM overrun > 5%** of hard limit triggers pipeline PAUSE for stakeholder review
5. **Cost reductions** found during DFM/DFA are tracked as savings against the original budget
