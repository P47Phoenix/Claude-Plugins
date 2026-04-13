# Make-vs-Buy Decision Framework

This reference provides the structured framework for evaluating whether to design a hardware subsystem custom ("make") or use an off-the-shelf module/component ("buy").

## 1. When to Perform a Make-vs-Buy Analysis

Trigger a make-vs-buy analysis when:

1. **A subsystem can be implemented either as custom circuitry or as a module** (e.g., WiFi: custom RF design vs. module with antenna)
2. **A mechanical component can be standard or custom** (e.g., enclosure: off-the-shelf vs. injection molded)
3. **A capability can be integrated on the main PCB or as a daughter board** (e.g., power supply: on-board regulators vs. external PSU)
4. **Volume projections change significantly** -- A decision made at prototype volumes may not hold at production volumes

## 2. Evaluation Criteria

### 2.1 Standard Criteria Set

Use these criteria as the default set. Add or remove criteria based on the specific subsystem.

| Criterion | Weight Range | Description |
|-----------|-------------|-------------|
| **Unit cost at target volume** | 4-5 | Per-unit BOM cost at the projected production volume |
| **NRE / development cost** | 3-5 | One-time engineering cost for custom design (zero for buy) |
| **Time to first prototype** | 3-5 | Calendar time from decision to working prototype |
| **Time to production** | 3-5 | Calendar time from decision to production-ready design |
| **Supply chain risk** | 3-4 | Number of sources, lead time, lifecycle status |
| **Technical performance** | 2-5 | How well each option meets performance requirements |
| **Integration complexity** | 2-4 | Effort to integrate into the main system (footprint, interfaces, firmware) |
| **Regulatory certification** | 2-5 | Pre-certified modules reduce certification cost and risk |
| **IP ownership** | 1-3 | Custom design means you own the IP; modules may have licensing terms |
| **Future flexibility** | 1-3 | Ability to modify or upgrade the subsystem in future revisions |
| **Manufacturing complexity** | 2-4 | Assembly difficulty, test coverage, rework difficulty |

### 2.2 Weight Guidelines

- **Weight 5:** Business-critical. A bad score here kills the option.
- **Weight 4:** Very important. Strongly influences the decision.
- **Weight 3:** Important but not dominant.
- **Weight 2:** Nice to consider but will not swing the decision alone.
- **Weight 1:** Minor factor. Include for completeness.

**Important:** Set weights BEFORE scoring options. This prevents unconscious bias toward a preferred option.

## 3. Scoring Guide

### 3.1 Score Definitions

| Score | Meaning |
|-------|---------|
| **5** | Excellent -- clearly superior, exceeds requirements |
| **4** | Good -- meets requirements with margin |
| **3** | Adequate -- meets minimum requirements |
| **2** | Marginal -- barely acceptable, risk of not meeting requirements |
| **1** | Poor -- does not meet requirements or introduces unacceptable risk |

### 3.2 Scoring Guidelines by Criterion

#### Unit Cost at Target Volume

| Score | Make (Custom) | Buy (Module/COTS) |
|-------|--------------|-------------------|
| 5 | Custom BOM < 60% of module cost | Module cost < 60% of custom BOM |
| 4 | Custom BOM 60-80% of module cost | Module cost 60-80% of custom BOM |
| 3 | Costs within 20% of each other | Costs within 20% of each other |
| 2 | Custom BOM 120-150% of module cost | Module cost 120-150% of custom BOM |
| 1 | Custom BOM > 150% of module cost | Module cost > 150% of custom BOM |

#### NRE / Development Cost

| Score | Make (Custom) | Buy (Module/COTS) |
|-------|--------------|-------------------|
| 5 | NRE < $1K (simple custom circuit) | $0 NRE (standard module, no customization) |
| 4 | NRE $1K-$5K | Minimal integration effort ($0-$1K) |
| 3 | NRE $5K-$20K | Moderate integration effort ($1K-$5K) |
| 2 | NRE $20K-$50K | Significant integration/customization ($5K-$20K) |
| 1 | NRE > $50K (complex RF, ASIC, custom tooling) | Custom module variant required (> $20K) |

#### Time to First Prototype

| Score | Timeline |
|-------|----------|
| 5 | < 2 weeks |
| 4 | 2-4 weeks |
| 3 | 4-8 weeks |
| 2 | 8-16 weeks |
| 1 | > 16 weeks |

#### Regulatory Certification

| Score | Make (Custom) | Buy (Module/COTS) |
|-------|--------------|-------------------|
| 5 | N/A (subsystem not regulated) | Pre-certified for all target markets |
| 4 | Simple self-declaration sufficient | Pre-certified for primary market |
| 3 | Standard test required, predictable outcome | Partially certified, additional testing needed |
| 2 | Complex testing required, uncertain outcome | Certification status unclear or expired |
| 1 | Novel design, no test standard exists | Not certified, full testing required despite being COTS |

## 4. Decision Record Template

```markdown
## Make-vs-Buy Decision: <Subsystem Name>

**Date:** <ISO 8601>
**Stage:** <Pipeline stage>
**Status:** PROPOSED | ACCEPTED | SUPERSEDED

### Subsystem Description
<What the subsystem does and its key specifications>

### Options

#### Option A: Make (Custom Design)
- **Approach:** <brief description of custom design approach>
- **Estimated NRE:** $<amount>
- **Estimated unit cost at <volume>:** $<amount>
- **Estimated schedule:** <weeks to prototype> / <weeks to production>
- **Key risks:** <list>

#### Option B: Buy (<specific module/component>)
- **Module:** <manufacturer> <part number>
- **Estimated NRE:** $<amount> (integration only)
- **Module unit cost at <volume>:** $<amount>
- **Estimated schedule:** <weeks to prototype> / <weeks to production>
- **Key risks:** <list>

### Weighted Evaluation

| Criterion | Weight | Make Score | Make Weighted | Buy Score | Buy Weighted |
|-----------|--------|-----------|--------------|-----------|-------------|
| Unit cost at volume | <w> | <s> | <w*s> | <s> | <w*s> |
| NRE cost | <w> | <s> | <w*s> | <s> | <w*s> |
| Time to prototype | <w> | <s> | <w*s> | <s> | <w*s> |
| Time to production | <w> | <s> | <w*s> | <s> | <w*s> |
| Supply chain risk | <w> | <s> | <w*s> | <s> | <w*s> |
| Technical performance | <w> | <s> | <w*s> | <s> | <w*s> |
| Integration complexity | <w> | <s> | <w*s> | <s> | <w*s> |
| Regulatory certification | <w> | <s> | <w*s> | <s> | <w*s> |
| IP ownership | <w> | <s> | <w*s> | <s> | <w*s> |
| Future flexibility | <w> | <s> | <w*s> | <s> | <w*s> |
| Manufacturing complexity | <w> | <s> | <w*s> | <s> | <w*s> |
| **TOTAL** | | | **<sum>** | | **<sum>** |

### Break-Even Analysis
- NRE for custom: $<amount>
- Per-unit savings (buy - make): $<amount>
- Break-even volume: <units>
- Expected lifetime volume: <units>
- Ratio (expected / break-even): <ratio>x

### Decision
<MAKE / BUY>

### Rationale
<Why this option was chosen, referencing the weighted scores and break-even analysis>

### Conditions
<Any conditions on this decision -- e.g., "Revisit if volume exceeds 10K units">

### Consequences
- <Positive consequence>
- <Negative consequence / accepted trade-off>
```

## 5. Common Subsystem Archetypes

These archetypes provide starting-point guidance. Every project should perform its own analysis.

| Subsystem | Typical Winner | Rationale | Revisit If |
|-----------|---------------|-----------|-----------|
| **WiFi/BT** | Buy (module) | Pre-certified modules save $10K-$50K in RF certification. Custom only at >50K units. | Volume > 50K AND team has RF expertise |
| **Cellular modem** | Buy (module) | Carrier certification is extremely expensive. Custom is almost never justified. | Almost never |
| **USB interface** | Make (custom) | Standard ICs, well-understood design, low NRE. Modules add unnecessary cost. | Never for USB-only; consider module if USB + hub + charging |
| **Power supply (DC-DC)** | Make (custom) | Standard regulator ICs, reference designs available. Modules are 3-10x unit cost. | Volume < 100 AND schedule critical |
| **Display** | Buy (module) | Display modules include driver, backlight, touch controller. Custom LCD NRE is very high. | Almost never for < 100K units |
| **Motor driver** | Depends on complexity | Simple DC motor: make (single IC). Stepper/BLDC with FOC: buy (module or reference design). | Evaluate per project |
| **Sensor (IMU, environmental)** | Buy (IC/module) | Sensor ICs are standard. Modules only if evaluation/prototyping. Production uses bare ICs. | Always use bare ICs for production |
| **Enclosure** | Buy (standard) at low volume, Make (custom) at high volume | Injection mold tooling is $5K-$50K NRE. Standard enclosures are < $5 each. | Volume > 5K units typically justifies custom tooling |

## 6. Vendor Evaluation Checklist

When evaluating a "buy" option, assess the vendor:

| Factor | Questions to Ask |
|--------|-----------------|
| **Financial stability** | Is the vendor profitable? Risk of discontinuation? |
| **Support quality** | Design support, documentation quality, reference designs, FAE access? |
| **Sample availability** | Can you get samples quickly for evaluation? |
| **MOQ** | Minimum order quantity for production? Compatible with your volumes? |
| **Lead time** | Standard lead time? Lead time during allocation events? |
| **Longevity commitment** | Product lifecycle roadmap? EOL notice period? |
| **Second source** | Is there a pin-compatible or footprint-compatible alternative from another vendor? |
| **Geographic risk** | Where are they manufactured? Tariff exposure? |
| **Compliance** | RoHS/REACH compliance documentation available? |
| **NDA requirements** | Do they require NDA for datasheets or pricing? (red flag for small companies) |
