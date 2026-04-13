# Component Selection Criteria

This reference defines the component selection methodology, scoring criteria, lifecycle policy, and second-source requirements used by the Electrical Engineer during component-selection tasks.

## Selection Process

1. **Define requirements** -- Extract electrical, mechanical, thermal, and cost requirements from the hardware PRD and schematic design
2. **Search candidates** -- Use kicad-happy sourcing skills (DigiKey primary, then Mouser, LCSC, element14) to find candidates
3. **Evaluate candidates** -- Score each candidate against the weighted criteria matrix
4. **Select and document** -- Choose the best candidate, document rationale, and flag risks

## Weighted Criteria Matrix

| Criterion | Weight (1-5) | Scoring Guide |
|-----------|-------------|---------------|
| **Electrical fit** | 5 | 5=exact match to requirements; 4=meets all requirements with margin; 3=meets minimum requirements; 2=meets most but not all; 1=significant shortfall |
| **Lifecycle status** | 4 | 5=Active, production; 4=Active, new product; 3=Active but mature (5+ years); 2=NRND (not recommended for new designs); 1=Obsolete/EOL |
| **Unit cost** | 4 | Score relative to BOM budget target: 5=under 50% of allocation; 4=under 75%; 3=at target; 2=up to 125%; 1=over 125% |
| **Stock availability** | 3 | 5=>1000 units in stock; 4=100-1000; 3=10-100; 2=<10 in stock; 1=out of stock (lead time only) |
| **Package/footprint** | 3 | 5=standard package, existing footprint in library; 4=standard package, footprint needs creation; 3=non-standard but available; 2=fine-pitch/BGA requiring special handling; 1=custom/obsolete package |
| **Thermal margin** | 3 | 5=runs cool (junction temp <50% of max); 4=comfortable margin (50-70%); 3=adequate (70-85%); 2=tight (85-95%); 1=at limit (>95%) |
| **Second-source available** | 2 | 5=3+ alternative sources; 4=2 alternative sources; 3=1 alternative source; 2=pin-compatible but not parametric-compatible alt; 1=sole-source, no alternatives |

**Weighted total** = SUM(weight * score) for each criterion.

## Lifecycle Policy

| Status | Policy | Action Required |
|--------|--------|----------------|
| **Active** | Approved for new designs | None |
| **Active (mature, 5+ years)** | Approved with caution | Verify manufacturer roadmap; identify alternate source |
| **NRND** (Not Recommended for New Designs) | Avoid for new designs | Must document explicit risk acceptance OR select alternative |
| **Obsolete / EOL** | Prohibited for new designs | Select alternative. Existing designs: plan last-time buy or redesign |

**BOM Gate impact**: Components with NRND or obsolete status cause BOM Gate to return NOT_DONE unless explicitly risk-accepted in the component rationale.

## Second-Source Requirements

| Component Category | Second-Source Requirement |
|-------------------|------------------------|
| **MCU / SoC** | Strongly recommended (single-source acceptable if sole-source is strategic and lead time is managed) |
| **Voltage regulators** | Required for main power rails; recommended for secondary rails |
| **Passives (R, C, L)** | Recommended (commodity, usually easy to find alternates) |
| **Connectors** | Required for board-to-board and external connectors (tooling dependency) |
| **Specialty ICs** (RF, sensor, codec) | Single-source acceptable if no pin-compatible alternative exists; document the risk |

**Single-source flagging**: When no second source exists, flag it in the Component Selection Matrix. The BOM Gate will classify this as a warning (not blocking unless config requires second-source for all parts).

## Distributor Priority and Usage

| Priority | Distributor | Skill | Best For |
|----------|------------|-------|----------|
| 1 | DigiKey | `kicad-happy:digikey` | Primary search, datasheet retrieval, prototype ordering |
| 2 | Mouser | `kicad-happy:mouser` | Cross-reference pricing, secondary availability check |
| 3 | LCSC | `kicad-happy:lcsc` | JLCPCB assembly compatibility (basic vs. extended parts), China-sourced pricing |
| 4 | element14 | `kicad-happy:element14` | Regional availability (Newark US, Farnell EU/UK), alternate sourcing |

**When to query multiple sources:**
- **Always for key active components** (MCUs, regulators, ICs >$1): DigiKey + at least one alternate
- **Always when JLCPCB is the target fab**: Check LCSC for basic/extended classification
- **For common passives**: One source is sufficient (commodity parts)
- **When stock is low at primary source**: Check all sources for availability

## Datasheet Review Checklist

Before selecting any component, verify the following from the datasheet:

1. **Absolute maximum ratings** -- ensure no operating condition exceeds these
2. **Recommended operating conditions** -- design to these, not absolute max
3. **Electrical characteristics** -- verify key parameters meet requirements at your operating temperature
4. **Package dimensions** -- verify footprint compatibility
5. **Thermal resistance** (theta-JA, theta-JC) -- needed for thermal analysis
6. **Application circuit** -- compare with your schematic; verify external component values
7. **Ordering information** -- verify correct package variant, temperature grade, tape-and-reel vs. tube

## Cost Tracking

All component costs should reference:
- **Quantity**: Use qty 100 for prototype pricing, qty 1000+ for production estimates
- **Currency**: USD
- **Date**: Pricing is volatile; record the date of the price check
- **Source**: Which distributor provided the price

The BOM Gate will validate total BOM cost against the budget target set by the HW Product Owner.
